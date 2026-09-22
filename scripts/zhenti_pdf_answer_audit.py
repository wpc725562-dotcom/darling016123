#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""zhenti_pdf_answer_audit.py —— 用站内 PDF 原卷合集校验「答案键」三方一致性。

背景
----
`docs/public/papers/politics/2012-2019-政治合集.pdf`（2012–2019 八年合订）**带完整文字层**，
且每年都附《参考答案及评分标准》。它一直躺在站点下载目录里，此前**从未被用来校验页面**。
本脚本把它作为**第三方基准**，与另外两处答案做三方比对：

    ① PDF 原卷合集（`--pdf`）           ← 权威源，带文字层
    ② 原卷文字版 note（`--note`）        ← 页面题面的直接来源（OCR 誊录，有噪声）
    ③ 各年真题页的「答案速查表」（`--pages`）

为什么值得做
------------
- note 是从公开资料 OCR 誊录的，**带零散垃圾字符**（如「这z是」「中g国」）。年份页由 note 派生，
  可能**继承同音/形近错误**。三方比对能把「誊录错」和「PDF 本身错」区分开。
- 判据必须是**三方**：只有 note 与页面一致、而 PDF 不同时，才可能是 PDF 版次问题；
  三方一致才算闭环。

用法
----
    python scripts/zhenti_pdf_answer_audit.py \\
        --pdf docs/public/papers/politics/2012-2019-政治合集.pdf \\
        --note docs/posts/politics/notes/真题-政治历年2012-2019.md \\
        --pages docs/posts/politics

设计要点
--------
1. **答案块要截断**：从「参考答案」/「试卷答案」/「答案及评分标准」起，到「三、辨析题」止。
   不截断会把主观题解析里的 `（2 分）`、题号（如「36.（1）」）误当答案。
2. **同题号取首次出现**：主观题解析里会出现「36.（1）」，若不取首次会覆盖客观题答案。
3. **note 与页面题号分隔符不同**：note 用 `、`（2012–2015）或 `．`（2018–2019），
   页面是表格。三条解析器各自独立，不要复用正则。
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

# 「广东省2015年普通高等学校本科插班生招生考试《政治理论》答案及评分标准」
RE_HEAD = re.compile(r"广东省\s*(20\d\d)\s*年[^\n]{0,60}?(?:参考答案|试卷答案|答案及评分标准)")
# ★ 分隔符可能**重复**：2016 年 PDF 里写成 `1.、C`（点 + 顿号），只认一个会漏掉该题
RE_PAIR = re.compile(r"(\d{1,2})\s*[．.、]+\s*([A-E]{1,5})(?![A-Za-z0-9])")
# ★ PDF 文字层自带 OCR 错：2012 年第 11 题写成 `ll.C`（两个小写 L 冒充 11）。
#   誊录页忠实地抄了这个错。解析前先归一化，否则该题静默缺失。
RE_LL_AS_11 = re.compile(r"(?<![A-Za-z])ll(\s*[．.]\s*[A-E])")
RE_SUBJ_END = re.compile(r"三\s*[、．.]\s*辨析题")


def parse_key(text: str) -> dict[int, str]:
    """从一段「答案 + 评分标准」文本里抽客观题答案键。"""
    text = RE_LL_AS_11.sub(r"11\1", text)
    pairs: dict[int, str] = {}
    for m in RE_PAIR.finditer(text):
        n = int(m.group(1))
        if 1 <= n <= 30 and n not in pairs:
            pairs[n] = m.group(2)
    return pairs


def keys_from_pdf(path: pathlib.Path) -> dict[int, dict[int, str]]:
    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(str(path))
    pages = []
    for i in range(len(doc)):
        tp = doc[i].get_textpage()
        pages.append(tp.get_text_range(0, tp.count_chars()))
    whole = "\n".join(pages)

    out: dict[int, dict[int, str]] = {}
    heads = list(RE_HEAD.finditer(whole))
    for k, m in enumerate(heads):
        year = int(m.group(1))
        end = heads[k + 1].start() if k + 1 < len(heads) else len(whole)
        body = whole[m.end():end]
        cut = RE_SUBJ_END.search(body)
        if cut:
            body = body[:cut.start()]
        body = body.replace("www.gzzkgk.cn", "")
        out[year] = parse_key(body)
    return out


def keys_from_note(path: pathlib.Path) -> dict[int, dict[int, str]]:
    text = path.read_text(encoding="utf-8")
    out: dict[int, dict[int, str]] = {}
    heads = list(RE_HEAD.finditer(text))
    for k, m in enumerate(heads):
        year = int(m.group(1))
        end = heads[k + 1].start() if k + 1 < len(heads) else len(text)
        body = text[m.end():end]
        cut = RE_SUBJ_END.search(body)
        if cut:
            body = body[:cut.start()]
        out[year] = parse_key(body)
    return out


def keys_from_page(path: pathlib.Path) -> dict[int, str]:
    """解析真题页 `## 题目一览` 里的答案速查表（多行，每行 10 题）。

    ★ 表结构是「题号行 → `|:--:|` 分隔行 → 答案行」，**中间隔了一行**，
      不能拿「下一个 `|` 开头行」当答案行（那样只会拿到分隔行）。
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    out: dict[int, str] = {}
    for i, ln in enumerate(lines):
        m = re.match(r"^\|\s*题号\s*\|(.+)\|\s*$", ln)
        if not m:
            continue
        nums = [c.strip() for c in m.group(1).split("|")]
        for j in range(i + 1, min(i + 4, len(lines))):
            m2 = re.match(r"^\|\s*答案\s*\|(.+)\|\s*$", lines[j])
            if not m2:
                continue
            vals = [c.strip().strip("*") for c in m2.group(1).split("|")]
            for n, v in zip(nums, vals):
                if re.fullmatch(r"\d{1,2}", n) and re.fullmatch(r"[A-E]{1,5}", v):
                    out[int(n)] = v
            break
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="PDF 原卷合集 × note × 真题页 三方答案比对")
    ap.add_argument("--pdf", required=True, help="带文字层的原卷合集 PDF")
    ap.add_argument("--note", help="原卷文字版 note（.md）")
    ap.add_argument("--pages", help="真题页目录（如 docs/posts/politics）")
    ap.add_argument("--quiet", action="store_true", help="只打印差异与汇总")
    args = ap.parse_args()

    pdf_keys = keys_from_pdf(pathlib.Path(args.pdf))
    note_keys = keys_from_note(pathlib.Path(args.note)) if args.note else {}
    page_keys = {}
    if args.pages:
        for p in sorted(pathlib.Path(args.pages).glob("20*.md")):
            if re.fullmatch(r"20\d\d", p.stem):
                page_keys[int(p.stem)] = keys_from_page(p)

    years = sorted(pdf_keys)
    total_ok = total_diff = total_miss = 0
    print(f"PDF 覆盖年份：{years}")
    for y in years:
        pk = pdf_keys.get(y, {})
        nk = note_keys.get(y, {})
        gk = page_keys.get(y, {})
        if not args.quiet:
            print(f"\n=== {y} ===")
        for q in range(1, 31):
            vals = {
                "PDF": pk.get(q, "-"),
                "note": nk.get(q, "-") if args.note else None,
                "page": gk.get(q, "-") if args.pages else None,
            }
            shown = {k: v for k, v in vals.items() if v is not None}
            # ★ 两边都缺（都是 "-"）不是「一致」—— 那是**双盲**，不是互相印证（踩过）
            if all(v == "-" for v in shown.values()):
                total_miss += 1
                print(f"  ❓ Q{q:<2} 三方均缺（{', '.join(shown)}）")
                continue
            agree = len(set(shown.values())) == 1
            if agree:
                total_ok += 1
            elif "-" in shown.values():
                total_miss += 1
            else:
                total_diff += 1
            # ★ 计数必须在 quiet 过滤**之前**，否则 --quiet 下汇总恒为 0（踩过）
            if args.quiet and agree:
                continue
            if agree:
                if not args.quiet:
                    print(f"  ✅ Q{q:<2} {'='.join(shown.values())}")
            else:
                tag = "❓" if "-" in shown.values() else "❌"
                detail = "  ".join(f"{k}={v}" for k, v in shown.items())
                print(f"  {tag} Q{q:<2} {detail}")
    print(f"\n=== 汇总：一致 {total_ok} · 冲突 {total_diff} · 缺项 {total_miss} ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
