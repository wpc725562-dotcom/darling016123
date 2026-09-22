#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把「学科知识地图」（data/bili-analyze/_extract/_subject/*.md）落成笔记站页面。

为什么要在仓库外先合并
    语料 728 万字符 → 79 个单元卡片 → 18 份课程大纲 → 3 份学科地图。
    前三步都在 `data/bili-analyze/`（已 gitignore）里做，避免污染笔记库。

为什么拆页
    computer 13.6 万字符、math 14.6 万字符。单页塞进 VitePress 会又慢又难用，
    所以按考纲模块拆成若干页。

用法
    python scripts/bili_build_knowledge_map.py            # 写入 docs/
    python scripts/bili_build_knowledge_map.py --dry-run  # 只看拆分统计
"""
import argparse
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "bili-analyze", "_extract", "_subject")
DST = os.path.join(ROOT, "docs", "guide", "knowledge-map")

# 拆分方案：学科 -> [(输出文件, 页面标题, 章节区间(1-based, 闭区间), 一句话说明)]
PLAN = {
    "computer": [
        ("basics.md", "计算机基础与 Office",
         (1, 9), "计算机基础知识、数制与编码、操作系统、Word / Excel / PPT、多媒体、网络、信息安全"),
        ("c-language.md", "C 语言基础",
         (10, 20), "C 语言概述与程序开发、数据类型与常量变量、运算符与表达式、顺序/选择/循环结构、函数与递归、数组、字符与字符串、数据在内存中的存储"),
        ("c-advanced.md", "C 语言进阶与工程",
         (21, 27), "指针进阶与类型识别、结构体/位段/联合体/枚举、动态内存管理与程序内存区域、文件操作、编译链接与预处理、调试与常见错误、经典例题与项目实践"),
        ("data-structures.md", "数据结构与真题题型",
         (28, 39), "绪论与复杂度、线性表、栈与队列、串、树与二叉树、图、查找、排序、真题题型套路"),
    ],
    "math": [
        ("limits-derivatives.md", "极限 · 导数 · 微分学应用",
         (1, 3), "函数极限连续、导数与微分、微分中值定理与导数应用"),
        ("integrals.md", "积分 · 微分方程",
         (4, 6), "不定积分、定积分及其应用、常微分方程"),
        ("advanced.md", "多元微积分 · 级数 · 线代 · 证明",
         (7, 12), "向量代数与空间解析几何、多元函数微分学、二重积分、无穷级数、线性代数、证明专项"),
    ],
    "english": [
        ("english.md", "英语语法与题型",
         (1, 12), "句子主干、词法、谓语体系、时态、语态、情态、非谓语、虚拟语气、从句、特殊句式、题型专项"),
    ],
}

SUBJECT_CN = {"computer": "计算机", "math": "高数", "english": "英语"}

CH_RE = re.compile(r"^## ", re.M)

# ★ VitePress/Vue 构建隐患：正文里裸的 `<` 会被 Vue 当标签起始。
#   字幕提炼产物里满是数学不等式（`−R<t<R`、`0<x<1`），
#   而检查器的判据是 `/<([A-Z][A-Za-z0-9]*)[\s/>]/` —— 连 `<R ` 这种（大写字母后跟空格）
#   都会被判成未注册组件，构建会挂。
#   所以策略是**代码外所有裸 `<` 一律转义成 `&lt;`**（渲染出来仍是 `<`，视觉无差）。
#   行内代码里不动 —— markdown-it 本来就转义行内代码里的尖括号。
def escape_angle(text):
    """把代码外的裸 `<` 转成 `&lt;`。返回 (新文本, 修了几处)。"""
    n = text.count("<")
    return text.replace("<", "&lt;"), n


# ★ 第二个隐患：LaTeX 下标记法 `_{...}` / `^{...}`。
#   提炼产物里到处是 `lim_{x→0}`、`f_{x}`、`x^{n}`。markdown-it 会把里面的 `_` 当强调定界符，
#   生成的 `<em>` 又带着 `{x→0}` 被 Vue 当**属性绑定**解析 → 生成的 JS 里出现 `{ x→0: "" }`
#   → rollup 报 `Unexpected character '→'`，**构建直接失败**（实测 339 处）。
#   修法：把 `_{...}` / `^{...}` 整段里的 `_ ^ { }` 全部反斜杠转义。
#   markdown-it 会把 `\_` 渲染成 `_`、`\{` 渲染成 `{`，**视觉完全不变**。
def escape_math(text):
    """转义 `_{...}` / `^{...}` 里的 `_ ^ { }`。返回 (新文本, 修了几处)。"""
    out = []
    i = 0
    fixed = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c in "_^" and i + 1 < n and text[i + 1] == "{":
            depth = 0
            j = i + 1
            while j < n:
                if text[j] == "{":
                    depth += 1
                elif text[j] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            if j < n:                          # 找到配对的 }
                seg = text[i:j + 1]
                out.append(seg.replace("_", "\\_").replace("^", "\\^")
                              .replace("{", "\\{").replace("}", "\\}"))
                fixed += 1
                i = j + 1
                continue
        out.append(c)
        i += 1
    return "".join(out), fixed


def sanitize(text):
    """对**行内代码之外**的文本做两项转义（先 LaTeX 后尖括号）。返回 (新文本, 总修改数)。"""
    parts = text.split("`")
    fixed = 0
    for i in range(0, len(parts), 2):          # 偶数下标 = 代码之外
        parts[i], n1 = escape_math(parts[i])
        parts[i], n2 = escape_angle(parts[i])
        fixed += n1 + n2
    return "`".join(parts), fixed


def split_chapters(text):
    """把学科地图按 `## ` 切成 [(标题, 正文)]。"""
    idx = [m.start() for m in CH_RE.finditer(text)]
    if not idx:
        return []
    head = text[:idx[0]]
    out = []
    for i, s in enumerate(idx):
        e = idx[i + 1] if i + 1 < len(idx) else len(text)
        block = text[s:e]
        title = block.split("\n", 1)[0][3:].strip()
        out.append((title, block))
    return head, out


def count_points(block):
    return len(re.findall(r"^### ", block, re.M))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    manifest = {}
    for subj, pages in PLAN.items():
        src = os.path.join(SRC, "%s.md" % subj)
        if not os.path.exists(src):
            print("!! 缺源文件 %s" % src)
            return 1
        with io.open(src, encoding="utf-8") as fh:
            text = fh.read()
        head, chapters = split_chapters(text)
        total_pts = sum(count_points(b) for _, b in chapters)
        print("=" * 74)
        print("%s（%s）：%d 章 / %d 知识点 / %d 字符"
              % (SUBJECT_CN[subj], subj, len(chapters), total_pts, len(text)))
        used = 0
        for fname, title, (lo, hi), desc in pages:
            picked = chapters[lo - 1:hi]
            used += len(picked)
            body = "\n".join(b for _, b in picked)
            pts = sum(count_points(b) for _, b in picked)
            chars = len(body)
            print("  → %-22s 章 %2d–%2d（%2d 章）%4d 知识点 %7d 字符  %s"
                  % (fname, lo, hi, len(picked), pts, chars, title))
            manifest.setdefault(subj, []).append(
                (fname, title, desc, len(picked), pts, chars))
            if args.dry_run:
                continue
            outdir = os.path.join(DST, subj) if len(pages) > 1 else DST
            if len(pages) == 1:
                outdir = DST
            if not os.path.isdir(outdir):
                os.makedirs(outdir)
            header = (
                "# %s · %s\n\n"
                "> %s\n\n"
                "> 本页 %d 章 / %d 条知识点。来源与可信度说明见"
                "[知识地图总览](/guide/knowledge-map/)。\n\n"
                % (SUBJECT_CN[subj], title, desc, len(picked), pts)
            )
            out = os.path.join(outdir, fname)
            body, nfix = sanitize(body)
            if nfix:
                print("     ⚠️ 转义 %d 处（裸 `<` + LaTeX 下标）" % nfix)
            with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(header + body.lstrip("\n") + "\n")
        if used != len(chapters):
            print("  ⚠️ 章节覆盖不全：用了 %d / 共 %d" % (used, len(chapters)))
    print("=" * 74)
    if args.dry_run:
        print("[dry-run] 未写文件。")
    else:
        print("已写入 %s" % DST)
    return 0


if __name__ == "__main__":
    sys.exit(main())
