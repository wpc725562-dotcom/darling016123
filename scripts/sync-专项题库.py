#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 Obsidian 侧的「专项题库」转成 VitePress 站点版。

背景：本仓库是「Obsidian 源库 + VitePress 站点」双结构，同一份内容存两份：
  - Obsidian 侧：历年真题/计算机程序设计/专项题库/  → 用 [[wiki 链接]]
  - 站点侧：   docs/posts/computer/专项题库/         → 用 /绝对路径 链接

⚠️ 不要用 scripts/sync-obsidian-to-blog.mjs 来做这件事——该脚本模板已过时，
   会删掉 config.mts 的 PWA 配置与日语板块（约 -290 行）。本脚本只做定向转换。

用法：
    python scripts/sync-专项题库.py            # 转换并写入
    python scripts/sync-专项题库.py --dry-run  # 只看会写哪些文件
"""

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "历年真题", "计算机程序设计", "专项题库")
DST = os.path.join(ROOT, "docs", "posts", "computer", "专项题库")

# wiki 链接前缀 → 站点绝对路径前缀
# ⚠️ 顺序敏感：更具体的规则必须排在更宽泛的规则前面
LINK_MAP = [
    ("../../../../docs/posts/computer/notes/", "/posts/computer/notes/"),
    ("../../../../docs/posts/", "/posts/"),
    ("../../../../docs/guide/", "/guide/"),
    ("../../../../资料/高频考点统计/", "/posts/高频考点/"),
    # Obsidian 侧目录名与站点路由名不一致的，需要单独映射
    ("../考点拆分/_索引", "/posts/computer/topics/"),
    ("../_索引", "/posts/computer/"),
    ("../", "/posts/computer/"),
]

WIKI_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


def convert_link(target: str, label: str) -> str:
    """把 [[target|label]] 转成 [label](站点路径)。"""
    # 表格内为防竖线被当作列分隔符会写成 [[x\|y]]，这里先剥掉转义反斜杠
    target = target.strip().rstrip("\\").strip()
    label = (label or target).strip().rstrip("\\").strip()

    # 索引文件 → 目录链接
    if target.startswith("_索引"):
        return f"[{label}](/posts/computer/专项题库/)"

    for prefix, repl in LINK_MAP:
        if target.startswith(prefix):
            rest = target[len(prefix):]
            # 去掉可能的 .md 后缀
            rest = re.sub(r"\.md$", "", rest)
            return f"[{label}]({repl}{rest})"

    # 同级文件（无路径分隔符，如 [[01-数组与字符串专项|→ 进入]]）
    if "/" not in target:
        rest = re.sub(r"\.md$", "", target)
        return f"[{label}](/posts/computer/专项题库/{rest})"

    # 无法映射：保留为纯文本，避免产生死链
    return label


def convert(text: str) -> str:
    # 1) 修 wiki 链接
    text = WIKI_RE.sub(lambda m: convert_link(m.group(1), m.group(2)), text)

    # 2) 修相对路径的图片/文件引用
    text = text.replace("](../../../../", "](/")

    # 3) VitePress 折叠块：::: details 已经是兼容写法，无需改
    return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="只列出将写入的文件")
    args = ap.parse_args()

    if not os.path.isdir(SRC):
        print(f"❌ 源目录不存在：{SRC}", file=sys.stderr)
        return 1

    os.makedirs(DST, exist_ok=True)
    written = 0

    for name in sorted(os.listdir(SRC)):
        if not name.endswith(".md"):
            continue
        src_path = os.path.join(SRC, name)
        dst_name = "index.md" if name == "_索引.md" else name
        dst_path = os.path.join(DST, dst_name)

        with open(src_path, encoding="utf-8") as f:
            raw = f.read()
        out = convert(raw)

        if args.dry_run:
            print(f"  [dry] {name} → docs/posts/computer/专项题库/{dst_name}")
            continue

        with open(dst_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(out)
        print(f"  ✅ {name} → docs/posts/computer/专项题库/{dst_name}")
        written += 1

    if args.dry_run:
        print("\n(dry-run，未写入任何文件)")
    else:
        print(f"\n完成：写入 {written} 个文件到 docs/posts/computer/专项题库/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
