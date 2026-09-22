#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""从 B站 画面帧里判读「蓝色字标注型答案」。

背景：有些讲解视频**不用文字写答案**，而是把正确选项**标成蓝色**。
离线 OCR 只读文字、读不到颜色，于是这类源会被误判成「不给答案」。
本脚本把 OCR 的**行 box** 与**像素颜色**融合：对每个 OCR 行算非背景像素的平均 RGB，
据此判定该行是「蓝」还是「黑」，再把「选项字母 → 颜色」累积成「题号 → 答案」。

用法：
    python scripts/bili_color_answers.py <帧目录> [--expect "ABCD AB CD ..."] [--start 21]
                                          [--thr-br 25] [--thr-bg 15] [--show 28]

参数：
    --expect    真题页答案，空格分隔，用于逐题比对
    --start     --expect 第一项对应的题号（多选通常写 21；默认 1）
                ★ 不加这个参数会把多选 21–30 当成 1–10 比对，得出「全缺」的假结论
    --thr-br    蓝判定阈值：B 通道 − R 通道（默认 25）
    --thr-bg    蓝判定阈值：B 通道 − G 通道（默认 15）
    --show      打印这些题号在每帧里的原始判色明细

★ 三条踩坑（实测）：
  1. **必须用 OCR 的行 box 定义区域**，不要手工估坐标 —— 手工估的 y 会整体错位一行，
     把「B 行」当成「A 行」，结论全反。
  2. **同一题要跨帧投票**：讲者是**逐项标记**的，某帧可能只标了前两项。
     取「该选项在所有帧里的多数颜色」比取单帧稳。
  3. **OCR 把两行合并时颜色会失真**：如 C、D 被识别成一行，则黑 + 蓝 平均成「偏蓝但不纯」。
     脚本会把它标成 `?`，**不要当成黑**。
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict

try:
    from PIL import Image
except ImportError:
    sys.exit("需要 Pillow：pip install Pillow")

BG = 205                      # 三通道都 > BG 视为背景
RE_QNO = re.compile(r"^\s*(\d{1,2})\s*[、.．]\s*\S")
RE_OPT = re.compile(r"^\s*([A-D])\s*[、.．]?\s*(\S.*)$")


def line_color(img, box):
    """对一行（OCR box）算非背景像素的平均 RGB。"""
    xs = [p[0] for p in box]
    ys = [p[1] for p in box]
    x0, x1 = int(min(xs)), int(max(xs))
    y0, y1 = int(min(ys)), int(max(ys))
    px = img.convert("RGB").load()
    w, h = img.size
    x1 = min(x1, w)
    y1 = min(y1, h)
    rs = gs = bs = n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y]
            if r > BG and g > BG and b > BG:
                continue
            rs += r
            gs += g
            bs += b
            n += 1
    if n == 0:
        return None
    return rs / n, gs / n, bs / n, n


def is_blue(rgb, thr_br, thr_bg):
    r, g, b = rgb[0], rgb[1], rgb[2]     # line_color 返回 (r, g, b, n)，多取一个像素数
    return (b - r) > thr_br and (b - g) > thr_bg


def looks_merged(text):
    """行内出现两个及以上「选项字母 + 中文」=> OCR 把多行合并了，整行颜色不可信。

    ★ 注意不能只认 `A.` / `A、` 这种带分隔符的写法：实测 Q27 的合并行长这样 ——
      `C推进国家体系体系和治理能力民主化D推进国家治理体系和治理能力现代化`（**字母后直接跟中文**）。
      第一版只认带分隔符的写法，于是漏判成「一整行黑」，把 D 的蓝色丢掉。
    """
    letters = re.findall(r"(?<![A-Za-z])[A-D](?=[\u4e00-\u9fff])", text)
    return len(letters) >= 2, letters


def split_colors(img, box, n):
    """把一行的 box 按 x 均分成 n 段，返回每段的平均色。"""
    xs = [p[0] for p in box]
    ys = [p[1] for p in box]
    x0, x1 = int(min(xs)), int(max(xs))
    y0, y1 = int(min(ys)), int(max(ys))
    out = []
    for i in range(n):
        sx0 = x0 + (x1 - x0) * i // n
        sx1 = x0 + (x1 - x0) * (i + 1) // n
        out.append(line_color(img, [[sx0, y0], [sx1, y0], [sx1, y1], [sx0, y1]]))
    return out


def main():
    ap = argparse.ArgumentParser(description="从画面帧判读「蓝色标注型」答案")
    ap.add_argument("dirs", nargs="+", help="含 _ocr.jsonl 与 frames/ 的目录")
    ap.add_argument("--expect", default=None, help="真题页答案，空格分隔")
    ap.add_argument("--start", type=int, default=1, help="--expect 第一项的题号")
    ap.add_argument("--thr-br", type=int, default=25)
    ap.add_argument("--thr-bg", type=int, default=15)
    ap.add_argument("--show", type=int, nargs="*", default=[], help="打印这些题的逐帧判色明细")
    args = ap.parse_args()

    # votes[q][opt] = [blue_cnt, black_cnt]
    votes = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    detail = defaultdict(list)
    n_frames = 0

    for d in args.dirs:
        ocr = os.path.join(d, "_ocr.jsonl")
        frdir = os.path.join(d, "frames")
        if not os.path.exists(ocr):
            print(f"⚠ 跳过（无 _ocr.jsonl）：{d}")
            continue
        rows = [json.loads(l) for l in open(ocr, encoding="utf-8")]
        for rec in rows:
            fn = rec["frame"]
            fp = os.path.join(frdir, fn)
            if not os.path.exists(fp):
                continue
            n_frames += 1
            img = Image.open(fp)
            cur_q = None
            for ln in rec["lines"]:
                t = ln["t"].strip()
                m = RE_QNO.match(t)
                if m:
                    cur_q = int(m.group(1))
                    continue
                mo = RE_OPT.match(t)
                if not mo or cur_q is None:
                    continue
                opt, rest = mo.group(1), mo.group(2)
                # 排除界面元素：选项正文太短或含 UI 关键词
                if len(rest) < 2 or re.search(r"(bilibili|WPS|标题|标送|标遇|伴学|专升本)", t):
                    continue
                c = line_color(img, ln["box"])
                if not c:
                    continue
                merged, letters = looks_merged(t)
                if merged:
                    # ★ 合并行整行颜色不可信（黑+蓝会平均成「偏蓝但不纯」），
                    #   按 x 均分逐段判色，与行内字母一一对应，把被合并掉的选项救回来。
                    for let, seg in zip(letters, split_colors(img, ln["box"], len(letters))):
                        if not seg:
                            continue
                        b_ = is_blue(seg, args.thr_br, args.thr_bg)
                        votes[cur_q][let][0 if b_ else 1] += 1
                        if cur_q in args.show:
                            detail[cur_q].append((fn, let, tuple(round(v, 1) for v in seg),
                                                  "蓝" if b_ else "黑", "切分"))
                    continue
                blue = is_blue(c, args.thr_br, args.thr_bg)
                votes[cur_q][opt][0 if blue else 1] += 1
                if cur_q in args.show:
                    detail[cur_q].append((fn, opt, tuple(round(v, 1) for v in c),
                                          "蓝" if blue else "黑", ""))

    print(f"\n=== 判色扫描：{n_frames} 帧，{len(votes)} 个题号 ===")
    results = {}
    for q in sorted(votes):
        picks = []
        for opt in "ABCD":
            v = votes[q].get(opt)
            if not v:
                continue
            blue_cnt, black_cnt = v
            if blue_cnt > black_cnt:
                picks.append(opt)
        results[q] = "".join(picks)
        print(f"  Q{q:<2} 判出 = {results[q] or '(无)'}")

    if args.expect:
        exp = args.expect.split()
        print(f"\n=== 与真题页比对（--start {args.start}）===")
        ok = bad = miss = 0
        for i, e in enumerate(exp):
            q = args.start + i
            got = results.get(q, "")
            if not got:
                miss += 1
                print(f"  ❓缺 Q{q:<2} 页={e:<6} 源画面未判出")
            elif got == e:
                ok += 1
                print(f"  ✅同 Q{q:<2} 页={e:<6} 源={got}")
            else:
                bad += 1
                print(f"  ❌异 Q{q:<2} 页={e:<6} 源={got}")
        print(f"  --- 合计：✅{ok}  ❌{bad}  ❓{miss} ---")

    for q in args.show:
        print(f"\n=== Q{q} 逐帧明细 ===")
        for fn, opt, rgb, tag, mg in detail.get(q, []):
            print(f"  {fn}  {opt}  rgb={rgb}  {tag}{(' ' + mg) if mg else ''}")


if __name__ == "__main__":
    main()
