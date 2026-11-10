#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bili_zhenti_frames.py —— 从画面帧 OCR 结果重建题面（补 bili_zhenti_extract.py 缺的那一环）。

背景
----
`bili_zhenti_extract.py` 的 docstring 写明它**不负责读画面认题面**（那是多模态的事），
只做「逐字稿按题号切段 + 挑候选帧」。于是「画面 → 题面」这一环一直是空的。

本脚本补这一环：读 `bili_ocr_frames.py` 产出的 `_ocr.jsonl`，把 204 张帧的文字
**跨帧合并**成一份题面，每个字段标注来自哪一帧（evidence）。

为什么不能只靠字幕
------------------
字幕是老师口播，念题时会**跳过空格**、选项只说「A 跟 B 当选项」，
所以字幕里既没有空格位置也没有完整选项 —— 用它恢复的题面不能做题。
画面帧里是完整原卷扫描，题干、空格、四个选项全在。

三个关键设计（都是踩过的坑）
----------------------------
1. **必须过滤中文讲解行**。老师手写的红笔批注（「选A」「三单」「同位语」）也会被 OCR 认出来，
   混进题面就废了。判据用**英文占比**：题面行英文占比 > 55%，否则丢弃。
2. **同一题要跨帧取「最完整」版本**。贴纸、弹幕、鼠标会遮挡局部，
   但遮挡位置每帧不同 → 取字符数最多的变体，天然互补。
3. **按 y 坐标排序再读**。rapidocr 返回顺序不保证是阅读顺序（原脚本 docstring 已警告）。

用法
----
    python scripts/bili_zhenti_frames.py data/bili-analyze/e2021-p1
    python scripts/bili_zhenti_frames.py data/bili-analyze/e2021-p1 --min-en 0.5
    python scripts/bili_zhenti_frames.py data/bili-analyze/e2021-rest   # 多分P一起

输出
----
    <dir>/_questions.md    人读的题面（含 evidence 帧号）
    <dir>/_questions.json  机读（q_no / stem / options / frames）

退出码：0 成功 / 5 参数错 / 6 没找到 _ocr.jsonl
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

QNO = re.compile(r"^\s*(\d{1,2})\s*[.．。]\s*(.*)$")
QNO_I = re.compile(r"^\s*[Il]\s*[.．]\s*([A-Z].*)$")
OPT = re.compile(r"([A-D])\s*[.．]\s*")
EN = re.compile(r"[A-Za-z]")
ZH = re.compile(r"[\u4e00-\u9fff]")


def en_ratio(s: str) -> float:
    """英文占比：只统计字母和中文字，忽略空格标点数字。"""
    a = len(EN.findall(s))
    z = len(ZH.findall(s))
    return a / (a + z) if (a + z) else 0.0


def cut_zh(s: str) -> str:
    """把行内出现的中文及其后内容截掉（题面是英文，中文必是老师批注）。"""
    m = ZH.search(s)
    return s[:m.start()].rstrip(" .·、-") if m else s


def load_frames(d: pathlib.Path) -> list[dict]:
    p = d / "_ocr.jsonl"
    if not p.exists():
        for sub in d.rglob("_ocr.jsonl"):
            p = sub
            break
    if not p.exists():
        print(f"[ERR] 没有 _ocr.jsonl：{d}", file=sys.stderr)
        sys.exit(6)
    rows = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        lines = r.get("lines") or []
        lines.sort(key=lambda x: (x["box"][0][1], x["box"][0][0]))
        rows.append({"frame": r.get("frame", ""), "lines": lines})
    return rows


def to_visual_lines(lines: list[dict]) -> list[dict]:
    """把 OCR 的碎片行按 y 聚成「视觉行」，行内按 x 排序拼接。

    踩过的坑（这一条是整套解析的关键）：
    rapidocr 会把**同一行**拆成多个 line —— 原卷的题干跨了版心，
    左半句在 x=31、右半句在 x=209，是两个独立 line 但 y 只差 1px。
    如果不先聚类，就会把「3.Mywifeand」和「smoke, bul we don't...」当成两行，
    更糟的是把选项行当成题干续行。
    """
    if not lines:
        return []
    lines = sorted(lines, key=lambda x: (x["box"][0][1], x["box"][0][0]))
    groups: list[dict] = []
    for ln in lines:
        y = ln["box"][0][1]
        if groups and abs(y - groups[-1]["y"]) < 12:
            groups[-1]["parts"].append((ln["box"][0][0], ln.get("t") or ""))
        else:
            groups.append({"y": y, "parts": [(ln["box"][0][0], ln.get("t") or "")]})
    return [{"y": g["y"],
             "t": " ".join(t for _, t in sorted(g["parts"]))}
            for g in groups]


def parse_frame(fr: dict, min_en: float) -> dict[int, dict]:
    """一帧 → {题号: {stem:[], opts:{A:[],...}}}

    三条硬规则（都是踩过的坑）：
      ① 含中文的行整行丢弃 —— 题面是英文，出现中文必是老师红笔批注；
      ② 题干在**第一个选项出现时立即关闭** —— 否则下一题的题干会被并进上一题；
      ③ 题号 "I."/"l." 按 OCR 混淆还原成第 1 题。
    """
    out: dict[int, dict] = {}
    cur = None
    stem_left = 0
    for vl in to_visual_lines(fr["lines"]):
        t = (vl["t"] or "").strip()
        if not t or ZH.search(t):
            continue
        if en_ratio(t) < min_en:
            continue

        m = QNO.match(t)
        q = int(m.group(1)) if m else None
        rest = m.group(2).strip() if m else ""
        if q is None:
            mi = QNO_I.match(t)
            if mi:
                q, rest = 1, mi.group(1).strip()
        if q is not None and 1 <= q <= 80:
            cur = q
            stem_left = 2
            out.setdefault(cur, {"stem": [], "opts": {}})
            if rest:
                out[cur]["stem"].append(rest)
            continue

        if cur is None:
            continue
        parts = OPT.split(t)
        if len(parts) >= 3:
            stem_left = 0
            i = 1
            while i + 1 < len(parts):
                k = parts[i].upper()
                v = parts[i + 1].strip(" .·、-")
                if v:
                    out[cur]["opts"].setdefault(k, []).append(v)
                i += 2
        elif stem_left > 0:
            out[cur]["stem"].append(t)
            stem_left -= 1
    return out


def join_cn_free(parts: list[str]) -> str:
    s = " ".join(parts)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([,.;:!?])", r"\1", s)
    return s


def norm_key(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def pick_mode(cands: list[str]) -> str:
    """从多帧候选里取「众数」，同频时取最长。

    两次踩坑的合并结论：
      · 纯取最长 → 会把「上一题的选项残留」并进来；
      · 纯取众数 → 会选到被贴纸挡住后半句的短版本（短版本帧数更多）。
    正解：先按出现次数筛出**达到最高频一半**的候选，再在其中取最长。
    """
    if not cands:
        return ""
    cnt: dict[str, int] = {}
    raw: dict[str, str] = {}
    for c in cands:
        k = norm_key(c)
        if not k:
            continue
        cnt[k] = cnt.get(k, 0) + 1
        if len(c) > len(raw.get(k, "")):
            raw[k] = c
    if not cnt:
        return ""
    top = max(cnt.values())
    keep = [k for k, v in cnt.items() if v * 2 >= top]
    return raw[max(keep, key=lambda k: len(k))]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--min-en", type=float, default=0.55,
                    help="题面行英文占比下限，低于此判为中文讲解丢弃（默认 0.55）")
    ap.add_argument("--out-suffix", default="_questions")
    a = ap.parse_args()

    for dstr in a.dirs:
        d = pathlib.Path(dstr)
        frames = load_frames(d)
        stems: dict[int, list[str]] = {}
        opts: dict[int, dict[str, list[str]]] = {}
        ev: dict[int, set[str]] = {}

        for fr in frames:
            got = parse_frame(fr, a.min_en)
            for q, blk in got.items():
                stem = join_cn_free(blk["stem"])
                if stem:
                    stems.setdefault(q, []).append(stem)
                    ev.setdefault(q, set()).add(fr["frame"])
                for k, vals in blk["opts"].items():
                    v = join_cn_free(vals)
                    if v:
                        opts.setdefault(q, {}).setdefault(k, []).append(v)

        merged = {}
        for q in sorted(set(stems) | set(opts)):
            o = {k: pick_mode(v) for k, v in opts.get(q, {}).items()}
            ov = [v for v in o.values() if len(v) > 4]
            cand = stems.get(q, [])
            keep = [c for c in cand
                    if not any(v.lower() in c.lower() for v in ov)]
            merged[q] = {"stem": pick_mode(keep or cand), "opts": o}

        qs = sorted(merged)
        if not qs:
            print(f"[WARN] {d} 没解析出题号", file=sys.stderr)
            continue

        md = [f"# 画面帧重建题面 · {d.name}", "",
              f"> 来源：{len(frames)} 帧 OCR ｜ 解析出 **{len(qs)} 题**（{qs[0]}–{qs[-1]}）",
              f"> 过滤阈值：题面行英文占比 ≥ {a.min_en}", "",
              "> ⚠️ OCR 有拼写噪声（如 best→besi），**选项和空格已恢复但需人工校对**。", ""]
        js = {}
        for q in qs:
            m = merged[q]
            md.append(f"## 第 {q} 题")
            md.append("")
            md.append(f"**{m['stem'] or '（题干缺失）'}**")
            md.append("")
            for k in "ABCD":
                md.append(f"- **{k}.** {m['opts'].get(k) or '（缺）'}")
            md.append("")
            if ev.get(q):
                md.append(f"<sub>evidence: {', '.join(sorted(ev[q]))}</sub>")
                md.append("")
            js[q] = {"stem": m["stem"], "options": m["opts"],
                     "frames": sorted(ev.get(q, []))}

        (d / f"{a.out_suffix}.md").write_text("\n".join(md), encoding="utf-8")
        (d / f"{a.out_suffix}.json").write_text(
            json.dumps(js, ensure_ascii=False, indent=2), encoding="utf-8")

        miss = [q for q in qs if len([k for k in "ABCD" if merged[q]["opts"].get(k)]) < 4]
        print(f"[{d.name}] {len(frames)} 帧 → {len(qs)} 题（{qs[0]}–{qs[-1]}）"
              f"｜选项不全 {len(miss)} 题 {miss[:8]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
