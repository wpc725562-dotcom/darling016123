#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fill_english_cloze.py —— 把 2013–2019 库内真题「卷面正文」的截断处补成完整完形段。

背景
----
`历年真题/公共英语/{2013..2019}.md` 的「卷面正文（OCR）」代码块在
`Part Ⅲ Cloze` 的 Directions 之后就截断了，只留一句
`…（全文见本地 PDF / _by_year 抽取文本）`。
结果：这 7 套卷的**词汇 30 题 + 阅读 4 篇都在**，唯独**完形 15 分没有原文**。

而 `资料/PDF全文抽取/english/<年>-paper.md` 里完形是完整的（正文 + 15 组选项），
只是 PDF 文字层把「____」下划线（图形，不是文字）丢掉了 —— 断行位置就是空位。

本脚本做的事
------------
把截断标记那一行，替换成从 `-paper.md` 里切出来的「Cloze 段」原文，
并在前面加一段说明：空位在断行处，共 15 处，按顺序对应 51–65。

不改动任何其它内容（写作专节、答案速查、复盘法全部原样保留）。

安全措施
--------
1. 先备份到 `<file>.bak-20261025`
2. 只替换**那一行**截断标记；标记找不到就跳过并报错，绝不猜位置
3. 补完逐项校验：完形段有 15 组选项、且原文里 51..65 全部出现
4. 改完检查控制字符（`ord(c) < 32`），本项目踩过 `\\1` 变 `\\x01` 的坑

用法
----
    python scripts/fill_english_cloze.py            # 全部 7 年
    python scripts/fill_english_cloze.py 2019       # 单年
    python scripts/fill_english_cloze.py --dry-run  # 只报告不改
"""
from __future__ import annotations

import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ZHENTI = ROOT / "历年真题" / "公共英语"
PDFDIR = ROOT / "资料" / "PDF全文抽取" / "english"

YEARS = ["2013", "2014", "2015", "2016", "2017", "2018", "2019"]
TRUNC = "…（全文见本地 PDF"
BAK_SUFFIX = ".bak-20261025"


def clean_paper_lines(text: str) -> list[str]:
    """去掉 `-paper.md` 的抬头和分页注释，只留卷面正文。"""
    lines = text.split("\n")
    out = []
    seen_first_page = False
    for ln in lines:
        s = ln.strip()
        if not seen_first_page:
            if s.startswith("<!-- 原 PDF 第"):
                seen_first_page = True
            continue
        if re.match(r"^<!--\s*原 PDF 第\s*\d+\s*页\s*-->$", s):
            continue
        out.append(ln.rstrip())
    # 去掉首尾空行
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return out


def slice_cloze(lines: list[str]) -> list[str] | None:
    """从卷面正文里切出 Cloze 段（Part Ⅲ ... 到 Part IV 之前）。

    起点判据：行里含 `Cloze` 且不含 `|`（排除试卷结构表格行）。
    """
    start = None
    for i, ln in enumerate(lines):
        s = ln.strip()
        if "Cloze" in s and "|" not in s and not s.startswith("|"):
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        s = lines[j].strip()
        if re.match(r"^Part\s*[IVⅣ]", s) or s.startswith("Part IV") or s.startswith("Part Ⅳ"):
            end = j
            break
    seg = lines[start:end]
    while seg and not seg[-1].strip():
        seg.pop()
    return seg or None


def count_options(seg: list[str]) -> int:
    """数「A. xxx」形态的选项行，粗略反映选项组数。"""
    n = 0
    for ln in seg:
        if re.match(r"^\s*(?:\d{1,2}\.\s*)?A[.．、]", ln):
            n += 1
    return n


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    dry = "--dry-run" in sys.argv
    years = args or YEARS

    for y in years:
        md = ZHENTI / f"{y}.md"
        paper = PDFDIR / f"{y}-paper.md"
        if not md.exists() or not paper.exists():
            print(f"[skip] {y}: 缺文件（md={md.exists()} paper={paper.exists()}）")
            continue

        text = md.read_text(encoding="utf-8")
        lines = text.split("\n")

        hit = [i for i, ln in enumerate(lines) if TRUNC in ln]
        if not hit:
            print(f"[skip] {y}: 没有截断标记（可能已补过）")
            continue
        if len(hit) > 1:
            print(f"[ERR ] {y}: 截断标记出现 {len(hit)} 次，拒绝自动改（行 {[h+1 for h in hit]}）")
            continue
        pos = hit[0]

        # ★ 不能只替换「截断标记那一行」。
        #   踩过：原 OCR 片段在截断前已经抄了完形开头几句（还带着 51–55 的印出空号），
        #   只换标记行 → 文件里同时存在「OCR 半截段」和「PDF 完整段」，重复且矛盾。
        #   正解：若 OCR 片段里已经出现 `Part Ⅲ Cloze` 行（且在截断前 40 行内），从那里整段替换；
        #   否则（如 2016 直接断在阅读第 50 题）只替换标记行本身。
        #   ⚠️ 必须限定窗口 —— 无界回溯会跑到「答案解析摘录」里的 Cloze 字样（2016 曾误配到第 79 行）。
        start = pos
        for i in range(pos, max(pos - 40, -1), -1):
            s = lines[i].strip()
            if re.search(r"Part\s*[ⅢⅣIV]+\s*Cloze", s):
                start = i
                break
        # 从被删掉的 OCR 片段里收集「已印出的空号」，保留成对照（这是 PDF 文字层没有的信息）
        ocr_nums = sorted({int(m) for ln in lines[start:pos]
                           for m in re.findall(r"(?<![\d.])(5[1-9]|6\d|70)(?![\d.])", ln)})

        cloze = slice_cloze(clean_paper_lines(paper.read_text(encoding="utf-8")))
        if not cloze:
            print(f"[ERR ] {y}: 从 paper.md 里切不出 Cloze 段")
            continue

        nopt = count_options(cloze)
        body = "\n".join(cloze)
        # ★ 空数各年不同：2015–2019 是 15 空（51–65），2013/2014 是 20 空（51–70）。
        #   判据从原文「There are N blanks」里取，不写死 15 —— 写死会把 2013/2014 判成失败。
        mblank = re.search(r"There\s*are\s*(\d{1,2})\s*blanks", body)
        nblank = int(mblank.group(1)) if mblank else 0
        top = 50 + nblank
        printed = [k for k in range(51, top + 1) if re.search(rf"\b{k}\b", body)]
        # 硬判据：选项组数必须够，且**最高空号必须印出来**（top 是唯一能定位「最后一个空」的锚点）。
        # 软判据：低号缺失只告警 —— 2013/2014 原卷就没印 51–58，属源缺陷不是脚本错。
        if not nblank or nopt < nblank or top not in printed:
            print(f"[ERR ] {y}: 完形段校验失败（声明 {nblank} 空 / 选项组 {nopt} / "
                  f"最高号 {top} 未出现）→ 不动")
            continue
        lost = [k for k in range(51, top + 1) if k not in printed]
        warn = f"｜⚠️ 原卷未印空号 {lost[0]}–{lost[-1]}（共 {len(lost)} 个）" if lost else ""

        block = [
            "> ⚠️ **本段由 `scripts/fill_english_cloze.py` 从 PDF 文字层补回**（2026-10-25）。",
            "> 原 PDF 把「____」下划线画成图形而非文字，文字层里只剩**断行位置** ——",
            f"> 下面共 {nblank} 处断行即 {nblank} 个空位，按顺序对应 **51–{top}**，选项已完整附在正文后。",
        ]
        if ocr_nums:
            block.append(f"> 原 OCR 片段印出过空号 {ocr_nums} —— 可作为前几个空位的对照锚点。")
        block.append("")

        # cloze[0] 是 `Cloze (15%)`（PDF 里 Part 号单独一行被切掉了），补回 Part 号
        if cloze and cloze[0].strip().startswith("Cloze"):
            cloze = ["Part Ⅲ " + cloze[0].strip()] + cloze[1:]

        new_lines = lines[:start] + block + cloze + lines[pos + 1:]
        new_text = "\n".join(new_lines)

        bad = [(i + 1, c, ord(c)) for i, ln in enumerate(new_lines)
               for c in ln if ord(c) < 32 and c != "\t"]
        if bad:
            print(f"[ERR ] {y}: 出现控制字符 {bad[:3]} → 不写盘")
            continue

        print(f"[ok  ] {y}: 完形段 {len(cloze)} 行 / {nblank} 空 / 选项组 {nopt} / 空号 51–{top}{warn}"
              f" → 第 {start+1}–{pos+1} 行替换")
        if dry:
            continue

        bak = md.with_suffix(md.suffix + BAK_SUFFIX)
        if not bak.exists():
            bak.write_text(text, encoding="utf-8", newline="\n")
        md.write_text(new_text, encoding="utf-8", newline="\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
