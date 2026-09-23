# 📄 可打印版真题（HTML + PDF）

本目录由脚本自动生成，供打印练习使用。

## 目录

| 目录 | 内容 | 格式 |
|:---|:---|:---|
| `../printable/*.html` | 各科真题可打印 HTML | 浏览器打开 → Ctrl+P 打印 |
| `papers/printable/*.pdf` | 已生成的 PDF 版 | 直接打印 |

## 重新生成

```bash
# 1. Markdown → 可打印 HTML
python scripts/md-to-printable.py --all

# 2. HTML → PDF（需本机 Chrome）
node scripts/html-to-pdf.mjs          # 全部
node scripts/html-to-pdf.mjs math     # 只转数学
```

脚本行为由 `tests/test_md_to_printable.py` 锁定（77 项断言），改脚本前先跑：

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## 覆盖范围

覆盖 `docs/posts/{math,computer,english,politics}/` 下**除 `index.md` 外**的全部
markdown（即 `--all` 的完整输出），含历年真题、刷题版、学习手册、教材目录基准、
真题对照表与黄金知识汇编。每科源文件数：

| 前缀 | 科目 | 源文件数 |
|:---|:---|:---|
| `math-*` | 高等数学 | 16 |
| `computer-*` | 计算机基础与程序设计 | 18 |
| `english-*` | 公共英语 | 46 |
| `politics-*` | 政治理论 | 17 |
| | **合计** | **97** |

## 已知局限

**数学公式不渲染。** 转换器不引入 MathJax/KaTeX，`$...$` 与 `$$...$$` 以 LaTeX
源码形式输出（约 3749 处）。原因是 `scripts/html-to-pdf.mjs` 用 Chrome headless
直接打印、没有 `--virtual-time-budget`，即使挂上 CDN 也等不到异步渲染完成。
需要公式的场合请用站点页面 —— VitePress 的 `markdown.math` 已在构建期渲染。

**个别源文件缺陷会原样带入产物**，不是转换器问题：

- `computer/原卷文字版.md`：扫描件 OCR 提取，正文里有 31 处孤立 `**` 与 8 处
  残缺链接（形如 `[文本](URL 带空格)`），产物中保持字面量。
- `english/2026-英语-刷题版.md`、`politics/2025.md`：粗体 `**` 跨两个相邻源码行
  书写。CommonMark 会把相邻行合成一段从而配对成功，本转换器逐行成段，因此
  4 处 `**` 保持字面量。**不能靠「合并相邻行」修** —— 本语料里有大量
  PDF/OCR 抽取页（如 `politics/2022-政治大题通关手册.md` 单块 2276 行），
  每行是独立碎片，合并会灾难性粘成一整段。

> 生成时间：2026-09-23 · 源文件在 `docs/posts/` 下对应 markdown
