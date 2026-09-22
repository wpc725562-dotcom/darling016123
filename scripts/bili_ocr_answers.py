#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bili_ocr_answers.py —— 从 `_ocr.jsonl` 里抽出「题号 → 答案」，供真题页交叉核对。

背景
----
`bili_ocr_frames.py` 把画面帧 OCR 成 `<目录>/_ocr.jsonl`（每帧一行，含按阅读顺序
排好的文本行）。本脚本在其之上做一层「状态机抽取」：

    逐帧 → 记住当前题号（`12.` / `12、` / `12．`）→ 见到「解析：X」或「答案：X」
         → 记为 (题号, X, 帧号)

很多讲解视频**一屏一题**，题号与「解析：X」同屏；但也有题号被滚动条遮掉的情况，
所以题号状态要**跨帧沿用**（`--carry` 帧窗口内有效）。

为什么不能只比字母
------------------
本库已有判例：某年真题页曾被整体重排题号与选项字母，只比字母会得出
「15 题错 8 题」的假结论。所以本脚本的输出**必须配合人看原帧**：
它只负责把「源画面说了什么」摆出来，裁决归人。

用法
----
    # 抽答案（默认把同题号的所有候选都列出来，冲突可见）
    python scripts/bili_ocr_answers.py data/bili-analyze/p2019-danxuan

    # 与真题页答案速查表比对
    python scripts/bili_ocr_answers.py data/bili-analyze/p2019-danxuan \\
        --expect "D A B A D C A B B C C D B B C D B A D B"

    # 只看某几帧的原文（排查用）
    python scripts/bili_ocr_answers.py data/bili-analyze/p2019-danxuan --show 45 46 47

设计要点
--------
1. **题号要跨帧沿用**：一屏一题时题号常在帧顶，解析行在帧底，中间滚动会分帧。
2. **必须保留帧号**：结论要可回溯，否则与「凭印象说」无异。
3. **候选全部列出**：同一题出现多个不同答案时**不许取多数**，要人工看帧裁决。
4. 有些源把答案写进**题干括号**（`（ABCD）`）而不是「解析：」，用 `--paren` 打开。
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

# 题号：行首 1~2 位数字 + 顿号/点/句点/中文顿号
RE_QNO = re.compile(r"^\s*(\d{1,2})\s*[、.．,，]")
# 「解析：A」/「解析 A」/「答案：ABCD」
RE_ANS = re.compile(r"(?:解析|答案|参考答案|正确选项)\s*[：:·.．]?\s*([A-E]{1,5})(?![\u4e00-\u9fff])")
# 题干括号内答案：（ABCD） 或 (ABC)
RE_PAREN = re.compile(r"[（(]\s*([A-E]{1,5})\s*[）)]")


def load_frames(d: pathlib.Path) -> list[dict]:
    """读 <d>/_ocr.jsonl；兼容把 jsonl 放在 <d>/frames/ 下的写法。"""
    for cand in (d / "_ocr.jsonl", d / "frames" / "_ocr.jsonl"):
        if cand.exists():
            out = []
            with cand.open(encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        out.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
            return out
    raise SystemExit(f"找不到 _ocr.jsonl：{d}（先跑 bili_ocr_frames.py）")


def frame_no(frame: str) -> int:
    m = re.search(r"(\d+)\.jpg$", frame)
    return int(m.group(1)) if m else 0


def extract(frames: list[dict], carry: int = 6, use_paren: bool = False):
    """返回 {题号: [(答案, 帧号, 原文行), ...]}（按出现顺序）。"""
    hits: dict[int, list[tuple[str, str, str]]] = {}
    cur: int | None = None
    cur_age = 0
    for fr in frames:
        fno = frame_no(fr["frame"])
        lines = [ln["t"] for ln in fr.get("lines", [])]
        # 本帧内先更新题号状态（取本帧最后一次出现的题号，通常是最新滚到的那题）
        for t in lines:
            m = RE_QNO.match(t)
            if m:
                n = int(m.group(1))
                if 1 <= n <= 60:
                    cur, cur_age = n, 0
        if cur is not None:
            cur_age += 1
            if cur_age > carry:
                cur = None
        if cur is None:
            continue
        for t in lines:
            m = RE_ANS.search(t)
            if m:
                hits.setdefault(cur, []).append((m.group(1), fr["frame"], t.strip()))
                continue
            if use_paren:
                m = RE_PAREN.search(t)
                if m and re.search(r"[？?（）()]\s*$", t.strip()):
                    hits.setdefault(cur, []).append((m.group(1), fr["frame"], t.strip()))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description="从 _ocr.jsonl 抽「题号 → 答案」")
    ap.add_argument("dirs", nargs="+", help="含 _ocr.jsonl 的目录")
    ap.add_argument("--expect", default="", help="真题页答案，空格分隔，用于逐题比对")
    ap.add_argument(
        "--start",
        type=int,
        default=1,
        help="--expect 第一项对应的题号（多选通常写 21；默认 1）。"
        "★ 不加这个参数会把多选 21–30 当成 1–10 比对，得出「全缺」的假结论",
    )
    ap.add_argument("--carry", type=int, default=6, help="题号跨帧沿用窗口（帧数，默认 6）")
    ap.add_argument("--paren", action="store_true", help="同时认题干括号内的答案")
    ap.add_argument("--show", type=int, nargs="*", default=[], help="打印这些帧的 OCR 原文")
    ap.add_argument("--label", default="", help="本次抽取的标签（如 danxuan）")
    args = ap.parse_args()

    expect = [x.strip().upper() for x in args.expect.split() if x.strip()]
    grand_ok = grand_bad = grand_miss = 0
    for d in args.dirs:
        p = pathlib.Path(d)
        frames = load_frames(p)
        if args.show:
            idx = {frame_no(f["frame"]): f for f in frames}
            for n in args.show:
                f = idx.get(n)
                if not f:
                    print(f"  [无此帧] p01_{n:04d}.jpg")
                    continue
                print(f"  --- p01_{n:04d}.jpg ---")
                for ln in f.get("lines", []):
                    print(f"      {ln['t']}")
            continue

        hits = extract(frames, carry=args.carry, use_paren=args.paren)
        label = args.label or p.name
        print(f"\n=== {label}（{len(frames)} 帧，抽到 {len(hits)} 题）===")
        ok = bad = miss = 0
        for i, exp in enumerate(expect, start=args.start):
            got = hits.get(i, [])
            uniq = []
            for a, f, t in got:
                if a not in uniq:
                    uniq.append(a)
            if not uniq:
                mark, miss = "❓缺", miss + 1
                detail = "源画面未抽到"
            elif len(uniq) == 1 and uniq[0] == exp:
                mark, ok = "✅", ok + 1
                f = next(f for a, f, t in got if a == exp)
                detail = f"{uniq[0]}  @{f}"
            elif len(uniq) == 1:
                mark, bad = "❌", bad + 1
                f = got[0][1]
                detail = f"源 {uniq[0]} ≠ 页 {exp}  @{f}"
            else:
                mark, bad = "⚠️", bad + 1
                detail = f"源多值 {uniq}（页 {exp}）  " + " ".join(
                    f"{a}@{f}" for a, f, t in got[:6]
                )
            print(f"  {mark} Q{i:<2} 页={exp:<4} {detail}")
        if expect:
            print(f"  --- {label}: ✅{ok}  ❌{bad}  ❓{miss} ---")
            grand_ok += ok
            grand_bad += bad
            grand_miss += miss
        else:
            for n in sorted(hits):
                uniq = []
                for a, f, t in hits[n]:
                    if a not in uniq:
                        uniq.append(a)
                ev = " ".join(f"{a}@{f}" for a, f, t in hits[n][:4])
                print(f"  Q{n:<2} {','.join(uniq):<10} {ev}")
    if expect and len(args.dirs) > 1:
        print(f"\n=== 合计：✅{grand_ok}  ❌{grand_bad}  ❓{grand_miss} ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
