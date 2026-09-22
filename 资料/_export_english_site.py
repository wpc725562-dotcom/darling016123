# -*- coding: utf-8 -*-
"""Export English exam notes to VitePress docs/posts/english/.

- 完整 OCR 卷面不再截断
- 页首嵌入站点内 PDF 预览（docs/public/papers/english/）
"""
from pathlib import Path
import re

ROOT = Path(r"D:/专升本/专升本")
SRC = ROOT / "历年真题/公共英语"
DST = ROOT / "docs/posts/english"
PUBLIC = ROOT / "docs/public/papers/english"
DST.mkdir(parents=True, exist_ok=True)

# 与 config.mts base 保持一致
BASE = "/darling016123"


def pdf_block(year: int) -> str:
    """HTML embed + download links if public PDFs exist."""
    full = PUBLIC / f"{year}-full.pdf"
    paper = PUBLIC / f"{year}-paper.pdf"
    answers = PUBLIC / f"{year}-answers.pdf"
    combo_ans = PUBLIC / "2008-2012-answers.pdf"

    links = []
    embed_src = None
    if full.exists():
        embed_src = f"{BASE}/papers/english/{year}-full.pdf"
        links.append(f"[📥 完整卷面 PDF]({embed_src})")
    if paper.exists() and not full.exists():
        embed_src = f"{BASE}/papers/english/{year}-paper.pdf"
        links.append(f"[📥 卷面 PDF]({embed_src})")
    elif paper.exists() and full.exists():
        links.append(f"[📥 仅卷面]({BASE}/papers/english/{year}-paper.pdf)")
    if answers.exists():
        links.append(f"[📥 答案解析 PDF]({BASE}/papers/english/{year}-answers.pdf)")
    if year <= 2012 and combo_ans.exists():
        links.append(
            f"[📥 2008–2012 答案合订]({BASE}/papers/english/2008-2012-answers.pdf)"
        )

    if not embed_src and not links:
        return (
            "## 在线试卷\n\n"
            "> 本年份暂无站点内嵌 PDF，请使用下方 OCR 卷面文本刷题。\n\n"
        )

    parts = [
        "## 在线试卷（直接看，不用开本地 PDF）\n",
        "> 仅供个人备考 · 回忆/汇编卷 · 排版以 PDF 为准；下方另有可复制 OCR 文本。\n",
    ]
    if links:
        parts.append(" · ".join(links) + "\n")
    if embed_src:
        parts.append(
            f"""
<div class="pdf-frame">
  <iframe
    class="pdf-embed"
    src="{embed_src}#view=FitH"
    title="{year} 英语真题 PDF"
    loading="lazy"
  ></iframe>
</div>

<p class="pdf-hint">若内嵌预览空白，点上方「完整卷面 PDF」新标签打开，或用手机横屏浏览。</p>
"""
        )
    return "\n".join(parts) + "\n"


def to_site_md(text: str, year: int) -> str:
    def repl_wiki(m):
        inner = m.group(1)
        if "|" in inner:
            target, label = inner.split("|", 1)
        else:
            target, label = inner, inner
        label = label.strip()
        if "_索引" in target or target.strip() == "_索引":
            return f"[英语索引](/posts/english/)"
        if "总索引" in target:
            return f"[总索引](/guide/)"
        if "00-资料" in target or "资料来源" in target:
            return f"[资料说明](/guide/sources)"
        if "作文模板" in target:
            return label
        if "英语知识库" in target:
            return label
        m2 = re.search(r"(20\d{2})", target)
        if m2:
            y = m2.group(1)
            return f"[{label}](/posts/english/{y})"
        return label

    text = re.sub(r"\[\[([^\]]+)\]\]", repl_wiki, text)

    # escape Vue mustache
    text = text.replace("{{", "{​{").replace("}}", "}​}")

    # 不再截断卷面；仅规范化 details 标题
    def keep_paper(m):
        body = m.group(1)
        return (
            f"<details open>\n<summary>点击折叠 {year} 年试卷 OCR 全文"
            f"（可复制；空格粘连以 PDF 为准）</summary>\n\n```\n{body}\n```\n\n</details>"
        )

    text = re.sub(
        r"<details>\s*<summary>点击展开[^<]*</summary>\s*```(.*?)```\s*</details>",
        keep_paper,
        text,
        flags=re.S,
    )

    # 去掉「请对照本地 PDF」式措辞 → 指向在线试卷
    text = text.replace("对照本地 PDF", "对照上方在线 PDF")
    text = text.replace("本地原卷：`资料/英语真题原卷/`", "在线原卷：见本页「在线试卷」")
    text = re.sub(
        r"刷题时以 PDF 为准。",
        "刷题时以本页在线 PDF 为准。",
        text,
    )

    # 资料文件表：改成站点路径
    text = re.sub(
        r"## 资料文件[\s\S]*?(?=---\s*\n\s*←|---\s*\n\s*返回：|$)",
        f"""## 资料文件

| 文件 | 说明 |
|:---|:---|
| 本页「在线试卷」 | 站点内嵌 PDF，浏览器直接看 |
| `{BASE}/papers/english/{year}-full.pdf` | 完整卷（卷面±答案） |
| Obsidian `历年真题/公共英语/{year}.md` | 同源笔记 |

---

""",
        text,
        count=1,
    )

    text = re.sub(
        r"返回：.*",
        f"← [英语真题总览](/posts/english/) · [首页](/)",
        text,
    )

    # 把 PDF 块插到一级标题后（frontmatter 外的 # 标题之后）
    body = text.lstrip()
    # 源笔记以 # 开头；插入在第一个 --- 分隔块之后的结构：标题+引用 后
    insert_at = None
    m = re.search(r"(# 公共英语[^\n]*\n(?:\n|>[^\n]*\n)+)", body)
    if m:
        insert_at = m.end()
    else:
        m2 = re.search(r"(^# .+\n)", body, re.M)
        insert_at = m2.end() if m2 else 0

    block = pdf_block(year)
    if insert_at is not None:
        body = body[:insert_at] + "\n" + block + body[insert_at:]
    else:
        body = block + body

    fm = (
        "---\n"
        f"title: 公共英语 {year} 真题详解\n"
        f"description: 广东专升本公共英语 {year} · 在线试卷 + 写作范文 + 答案解析\n"
        "---\n\n"
    )
    return fm + body


def main():
    years = []
    for p in sorted(SRC.glob("*.md")):
        if p.name.startswith("_"):
            continue
        m = re.match(r"(20\d{2})\.md", p.name)
        if not m:
            continue
        year = int(m.group(1))
        md = to_site_md(p.read_text(encoding="utf-8"), year)
        out = DST / f"{year}.md"
        out.write_text(md, encoding="utf-8", newline="\n")
        years.append(year)
        has_pdf = (PUBLIC / f"{year}-full.pdf").exists() or (
            PUBLIC / f"{year}-paper.pdf"
        ).exists()
        print(f"site {year}.md {len(md)} chars pdf={has_pdf}")

    rows = []
    for y in sorted(years, reverse=True):
        has_pdf = (PUBLIC / f"{y}-full.pdf").exists() or (
            PUBLIC / f"{y}-paper.pdf"
        ).exists()
        if y == 2024:
            status = "在线 PDF + 解析范文"
        elif y >= 2013:
            status = "在线 PDF + 卷面 OCR + 解析" if has_pdf else "卷面 OCR + 解析"
        else:
            status = "在线 PDF + 卷面 OCR" if has_pdf else "卷面 OCR"
        if y == 2022 and not (PUBLIC / "2022-paper.pdf").exists():
            status = "答案 PDF + 卷面 OCR（合订本缺独立卷面页）"
        rows.append(f"| [{y}](/posts/english/{y}) | {status} |")

    index = f"""---
title: 公共英语 · 真题总览
description: 广东专升本公共英语 2008–2024 真题详解 · 在线试卷
---

# 公共英语 · 真题总览

> 试卷 **直接嵌在网页里**，不用打开本地 PDF。
> OCR 文本可能有空格粘连；**以页内 PDF 预览为准**。

## 年份列表

| 年份 | 状态 |
|:---:|:---|
{chr(10).join(rows)}

## 怎么刷

1. 点年份 → 上方 **在线试卷** 限时整套
2. 做完再展开答案 PDF / 解析
3. 每周默写 2 篇写作（书信 + NOTICE）
4. 错题记搭配

## 试卷文件目录

站点路径：`{BASE}/papers/english/`
（如 `2023-full.pdf` = 卷面+答案）

← [回首页](/)
"""
    (DST / "index.md").write_text(index, encoding="utf-8", newline="\n")
    print("index years:", sorted(years, reverse=True))


if __name__ == "__main__":
    main()
