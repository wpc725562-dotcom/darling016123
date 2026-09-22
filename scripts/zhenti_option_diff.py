#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""真题页 × 官方卷面 —— 选项一致性核对（v2，修正了 v1 的抽取 bug）

v1 的 bug：官方 PDF 里同一行偶尔挤两个选项（`A. would rather than B. rather had`），
只认行首 `A.` 的正则会漏掉 B，于是把后面不相干的四行当成选项 —— 造成**假不符**。
实测：2021.md 被误报 2 题不符（第 2、12 题），实际完全一致。

v2 改法：在题块内**按 `[ABCD].` 标记切分**，不依赖行首。

用法：python zhenti_option_diff.py --paper D:/tmp/p2021.txt --page docs/posts/english/2021.md
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

# 本脚本依赖同级模块 zhenti_log，显式把 scripts/ 加进 sys.path（理由见 zhenti_lint.py）。
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

# ★ E3（2026-09-20）：诊断走 logging（stderr），正式输出仍走 print（stdout）。
from zhenti_log import add_logging_args, get_logger, setup_from_args  # noqa: E402

LOG = get_logger(__name__)


def norm(s: str) -> str:
    """只留字母数字 —— 吸收 OCR 的空格粘连与标点差异。"""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def parse_paper(text: str, lo: int, hi: int) -> dict[int, list[str]]:
    """按题号切块，块内按 A./B./C./D. 标记抽选项（支持一行多选项）。"""
    lines = text.replace("\r", "").split("\n")
    starts: list[tuple[int, int]] = []
    for i, ln in enumerate(lines):
        m = re.match(r"^\s*(\d{1,2})\.\s+\S", ln)
        if m:
            n = int(m.group(1))
            if lo <= n <= hi:
                starts.append((n, i))
    starts.sort(key=lambda t: t[1])

    out: dict[int, list[str]] = {}
    for idx, (n, i) in enumerate(starts):
        j = starts[idx + 1][1] if idx + 1 < len(starts) else min(i + 40, len(lines))
        block = "\n".join(lines[i:j])
        # 去掉题号本身，再按选项标记切分
        block = re.sub(r"^\s*\d{1,2}\.\s+", "", block)
        parts = re.split(r"(?<![A-Za-z])([ABCD])\.\s*", block)
        opts: list[str] = []
        for k in range(1, len(parts) - 1, 2):
            val = norm(parts[k + 1].split("\n")[0])   # 只取该选项行首一段
            if val:
                opts.append(val)
        if len(opts) >= 4 and n not in out:
            out[n] = opts[:4]
    return out


def parse_page(path: str, lo: int, hi: int) -> dict[int, list[str]]:
    text = open(path, encoding="utf-8").read().replace("\r", "")
    out: dict[int, list[str]] = {}
    parts = re.split(r"^#{2,3}\s*(?:第\s*)?(\d+)\s*[.题、]?\s*$", text, flags=re.M)
    for i in range(1, len(parts) - 1, 2):
        n = int(parts[i])
        if not (lo <= n <= hi):
            continue
        body = parts[i + 1]
        opts = [norm(m.group(2))
                for m in re.finditer(r"^[\s>*-]*(?:\*\*)?([ABCD])(?:\*\*)?\s*[.、．]\s*(.+)$",
                                    body, flags=re.M)]
        opts = [o for o in opts if o]
        if opts:
            out[n] = opts
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper", required=True)
    ap.add_argument("--page", required=True)
    ap.add_argument("--lo", type=int, default=1)
    ap.add_argument("--hi", type=int, default=30)
    ap.add_argument("--label", default="")
    add_logging_args(ap)
    a = ap.parse_args()
    setup_from_args(a)

    LOG.debug("paper=%s · page=%s · 题号区间 %d–%d", a.paper, a.page, a.lo, a.hi)
    paper = parse_paper(open(a.paper, encoding="utf-8").read(), a.lo, a.hi)
    page = parse_page(a.page, a.lo, a.hi)
    LOG.debug("卷面解析 %d 题 · 页面解析 %d 题", len(paper), len(page))

    nums = sorted(set(paper) & set(page))
    bad, ok = [], []
    for n in nums:
        p, q = set(paper[n]), page[n]
        hit = sum(1 for x in q if x in p)
        (ok if hit >= 3 else bad).append((n, hit, len(q), paper[n], page[n]))

    name = a.label or a.page
    LOG.info("%s 选项比对：可比 %d 题 · 一致 %d · 不一致 %d", name, len(nums), len(ok), len(bad))
    if bad:
        LOG.warning("%s 有 %d 道题选项不一致：%s", name, len(bad),
                    ",".join(str(b[0]) for b in bad))
    print(f"{name}  vs  官方卷面  （可比 {len(nums)} 题）")
    print(f"  选项一致 : {len(ok)} 题")
    print(f"  不一致   : {len(bad)} 题" + (("  → " + ",".join(str(b[0]) for b in bad)) if bad else ""))
    for n, hit, tot, p, q in bad[:6]:
        print(f"    第 {n} 题（命中 {hit}/{tot}）")
        print(f"      卷面: {p}")
        print(f"      页面: {q}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
