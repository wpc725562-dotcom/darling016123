#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_ocr_stray_letters.py —— 清除誊录文本里零散的 OCR 垃圾字母。

背景
----
`docs/posts/politics/notes/真题-政治历年2012-2019.md` 是从公开资料誊录的
（PDF 扫描件 OCR），正文里混进了 **210 处**孤立小写字母（`k` / `g` / `c` / `z` / `l`），
形如「历史**k**条件」「发展**g**，」「中**g**国」。它们大多是**每页页脚**被识别成一个字母，
所以呈**等距分布**（每约 48 行一个单独的 `k` 行）。

危害不止「不好看」：
    `2k8.ABCD` —— 2013 年多选第 28 题的答案**被一个 `k` 拆散**，
    任何按 `(\\d+)[．.]([A-E]+)` 解析答案键的程序都会**静默漏掉这一题**。

★ 不能一刀切删「所有孤立小写字母」—— 有几处是**被误认成字母的字符**，要改而不是删：
    - `c．建议逐步实行城乡按…` → 这是**选项 C**，应改成大写 `C．`
    - `ll.C 12.A …`            → 这是**题号 11**，应改成 `11.`
    - `(l)对外开放和…` / `37．答：(l)…` → 这是**序号 (1)**，应改成 `(1)`

用法
----
    # 只看会改什么（默认 dry-run，打印逐行差异）
    python scripts/fix_ocr_stray_letters.py <文件> [<文件>…]

    # 真正写回
    python scripts/fix_ocr_stray_letters.py <文件> --apply

设计要点
--------
1. **先特判、后通删**：顺序错了会把 `c．` 的选项字母一起删掉。
2. **必须打印逐行差异**：这类「删字符」的改动最容易误伤，不看 diff 不该落盘。
3. **删完要收拾空格**：`A．杭州湾大桥 z B．港珠澳大桥` 删掉 `z` 后会留双空格。
4. **行尾/行首的孤立字母**单独处理，避免把 `…发展。（2分）g` 的句号后空格弄乱。
"""

from __future__ import annotations

import argparse
import difflib
import pathlib
import re
import sys

# 只删这些字母 —— 政治誊录里出现的垃圾字母集合（大写不动，`A`~`E` 是选项）
STRAY = "kgczl"

RE_LONE_LINE = re.compile(rf"^\s*[{STRAY}]{{1,2}}\s*$")
RE_INLINE = re.compile(rf"(?<![A-Za-z0-9])[{STRAY}]{{1,2}}(?![A-Za-z0-9])")

# 先特判：这些不是垃圾，是被误认的字符
# ★ 带 `^` 的规则**必须加 `re.M`** —— 否则 `^` 只匹配整个字符串开头，规则静默失效
#   （本脚本第一版就踩了：`c．建议…` 的选项字母被后面的通删规则吃掉了）
SPECIAL: list[tuple[re.Pattern[str], str, str]] = [
    (re.compile(r"^(\s*)ll(\s*[．.])", re.M), r"\g<1>11\g<2>", "题号 ll. → 11."),
    (re.compile(r"\(l\)"), "(1)", "序号 (l) → (1)"),
    (re.compile(r"^(\s*)c(\s*[．.])", re.M), r"\g<1>C\g<2>", "选项 c. → C."),
    (re.compile(r"(\d)k(\d)"), r"\g<1>\g<2>", "数字被字母拆开（2k8 → 28）"),
]


def fix_text(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    for pat, rep, desc in SPECIAL:
        text, n = pat.subn(rep, text)
        if n:
            notes.append(f"{desc} × {n}")

    lines = text.split("\n")
    out: list[str] = []
    dropped = 0
    for ln in lines:
        if RE_LONE_LINE.match(ln):
            dropped += 1
            continue  # 整行丢弃（行内容只有垃圾字母）
        out.append(ln)
    if dropped:
        notes.append(f"整行垃圾字母行 × {dropped}")

    text = "\n".join(out)
    text, n = RE_INLINE.subn("", text)
    if n:
        notes.append(f"行内孤立垃圾字母 × {n}")

    # 收拾残留空格：CJK 之间的双空格、行尾空格
    text = re.sub(r"([\u4e00-\u9fff，。、；：（）]) {2,}(?=[\u4e00-\u9fffA-E（])", r"\1 ", text)
    text = re.sub(r"[ \t]+$", "", text, flags=re.M)
    return text, notes


def main() -> int:
    ap = argparse.ArgumentParser(description="清除誊录文本里的 OCR 垃圾字母")
    ap.add_argument("files", nargs="+", help="要处理的文本文件")
    ap.add_argument("--apply", action="store_true", help="写回文件（默认只 dry-run）")
    args = ap.parse_args()

    rc = 0
    for f in args.files:
        p = pathlib.Path(f)
        old = p.read_text(encoding="utf-8")
        new, notes = fix_text(old)
        if old == new:
            print(f"[{p.name}] 无需修改")
            continue
        print(f"\n=== {p.name} ===")
        for n in notes:
            print(f"  · {n}")
        diff = list(
            difflib.unified_diff(
                old.splitlines(), new.splitlines(), "before", "after", lineterm="", n=0
            )
        )
        changed = [d for d in diff if d.startswith(("+", "-")) and not d.startswith(("+++", "---"))]
        print(f"  改动行数：{len(changed)} / {len(old.splitlines())}")
        for d in diff[:60]:
            print(f"    {d}")
        if len(diff) > 60:
            print(f"    … 还有 {len(diff) - 60} 行差异未显示")
        if args.apply:
            p.write_text(new, encoding="utf-8", newline="\n")
            print("  ✅ 已写回")
        else:
            print("  （dry-run，未写回；加 --apply 生效）")
            rc = 0
    return rc


if __name__ == "__main__":
    sys.exit(main())
