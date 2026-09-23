# -*- coding: utf-8 -*-
"""
真题 Markdown → 可打印 HTML（浏览器打印成 PDF）
用法：
  python scripts/md-to-printable.py <输入.md> [输出.html]
  python scripts/md-to-printable.py --all   # 转换 docs/posts 下所有真题

★ 2026-09-23 修复了一批「markdown 语法字面量漏进产物」的缺陷（详见各分支注释）：
  · 表格：状态改为显式布尔量（原来每行新开一张未闭合表、单元格全落 <th>）
  · 代码块 ``` → <pre><code>（原来完全不处理）
  · 水平线 --- → <hr>（原来是 <p>---</p>）
  · ::: 容器标记剥离，标题保留成一行（原来原样漏出）
  · 行内格式（粗体/行内代码/链接）抽成 _inline()，标题/列表/引用/表格单元格一致生效
  · 行尾 CRLF / 孤立 CR 归一为 LF
  对应的回归测试见 tests/test_md_to_printable.py。

★ 2026-09-23 第二轮：数学公式改为**构建期预渲染**（原来原样输出 LaTeX 源码）。
  本转换器把公式抽成 HTML 注释占位符 `<!--MJX <d> <base64>-->`，
  再由 scripts/printable-math.mjs 用 mathjax-full 渲染成内联 SVG 写回。
  这样产物**离线自包含**（无 CDN、无运行时 JS），Chrome headless 直接打印即可出图。
  ⚠️ 因此本脚本的输出**必须再过一遍 printable-math.mjs**，单独跑会留下注释占位符。
  npm 脚本 `print:html` 已把两步串起来。
"""
import re, sys, html, base64, pathlib

# ─────────────────────── 公式识别 ───────────────────────

# $$...$$ 在前（贪婪度更低的分支要先试），$...$ 在后。
# 行内分支用 [^$\n] 限制不跨行；两侧加负向断言避免把 $$ 误当两个 $。
_MATH_RE = re.compile(r"\$\$(.+?)\$\$|(?<!\$)\$(?!\$)([^$\n]+?)\$(?!\$)")

# 散文/货币守卫（只用于**行内**分支）。三个条件**同时**成立才判为散文：
#   ① 内容含空格
#   ② 内容不含任何 LaTeX 记号（\ ^ _ = + - * / < > ( ) [ ] { } |）
#   ③ 内容含 CJK 汉字 **或** 含 >=2 个字母的拉丁词
#   ⇒ 不渲染，原样保留字面量。
#
# ★ 这条守卫不是过度设计，是实测踩出来的：英文阅读理解文里有**同一行两个货币 $**，
#   例如 english/2024.md L37 `- **A.** $50. &emsp; B. $70.`，
#   朴素配对会把 `50. &emsp; B. ` 当成公式渲染，**整段选项文字直接消失**。
#
# ★ 条件③的两个分支都必要，是踩了两轮才收敛的：
#   · 只用「>=2 字母的拉丁词」→ 漏掉 `50. 和 B. `（只有单个字母 B）——
#     真实语料里恰好是 `&emsp;` 才被抓住，属侥幸，测试用中文一测就露馅。
#   · 只用「含 CJK」→ 漏掉纯英文的 ` 250,000 or more`。
#   · 反过来若改成「含空格且无 LaTeX 记号就拒」，会把 `$a, b$`（合法的变量并列）
#     误杀。加上条件③才既拦住散文又放过 `a, b`。
#
# 全量核验（97 个文件 / 3720 处行内匹配）：拒绝 5 处，人工确认全部是散文或货币；
# `a, b` / `x \to 0` / `f(x) = x^2` / `\sin 3x` / `4` / `0,1` 等样本全部放过（误杀 0）。
# 回归测试见 tests/test_md_to_printable.py 的 TestMathGuard。
_LATEX_HINT = re.compile(r"[\\^_=+\-*/<>()\[\]{}|]")
_CJK_CHAR = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
_LATIN_WORD = re.compile(r"[A-Za-z]{2,}")


def _looks_like_prose(s):
    """行内 `$...$` 的内容是否其实是散文/货币（而非公式）。"""
    if " " not in s:
        return False
    if _LATEX_HINT.search(s):
        return False
    return bool(_CJK_CHAR.search(s) or _LATIN_WORD.search(s))


def _math_marker(latex, display):
    """把一段 LaTeX 变成 HTML 注释占位符，交给 printable-math.mjs 渲染。

    ★ 用注释而不是自定义标签：注释在浏览器里不渲染，所以即使忘了跑第二步，
      页面也只是少个公式，而不会把 base64 字面量印在纸上。
      base64 字母表不含 `-`，因此不可能拼出 `-->` 提前闭合注释。
    """
    b64 = base64.b64encode(latex.encode("utf-8")).decode("ascii")
    return "<!--MJX %d %s-->" % (1 if display else 0, b64)


def _stash_math(text, math_spans):
    """把 text 里的公式换成 \\x01N\\x01 占位符（就地改写 math_spans 并返回新串）。

    ★ 必须在 html.escape() **之前**调用：否则 LaTeX 里的 `<` `>` `&`
      会先被转义成 `&lt;` `&gt;` `&amp;`，MathJax 收到的是坏掉的源码。
    ★ 必须在行内代码**取出之后**调用：`` `$x$` `` 里的 $ 是代码内容，不是公式。
    """
    def _sub(mo):
        display = mo.group(1) is not None
        latex = mo.group(1) if display else mo.group(2)
        if not display and _looks_like_prose(latex):
            return mo.group(0)          # 散文/货币：原样保留
        math_spans.append((latex, display))
        return "\x01%d\x01" % (len(math_spans) - 1)
    return _MATH_RE.sub(_sub, text)


def _inline(text):
    r"""行内格式：保护行内代码 → 提取公式 → 转义 → 链接 → 粗体 → 还原公式 → 还原代码。

    ★ 2026-09-23 新增：原实现只对**段落**做粗体/代码替换，标题、列表项、
    引用块与表格单元格一律走 `html.escape()` 直出，于是 markdown 语法字面量
    直接漏进产物。实测：表格单元格里的 `**合计**` 打印出来就是带星号的
    `**合计**`（564 处 / 37 个文件），链接 `[文本](url)` 原样可见（503 处 / 52 个文件）。
    抽成共用函数后，各处行内格式表现一致。

    ★ 行内代码必须**先取出、后还原**：若先做粗体，`` `x**2` `` 里的幂运算符
    会被 `\*\*(.+?)\*\*` 当成粗体标记吃掉。实测 math/2023.md 出现
    `<code>limit((1+x<strong>2)</strong>(1/x**2), x, 0) == E</code>` 这种错乱。
    公式同理：`` `$x$` `` 必须先被代码取出，否则会被当公式渲染掉。

    ★ 顺序（每一步都有理由，别随手调换）：
      1. 行内代码取出   —— 保护代码里的 $ 与 **
      2. 公式取出       —— 必须在转义前，否则 LaTeX 的 < > & 被转义坏
      3. html.escape    —— 此时串里只剩普通文本
      4. 链接 / 粗体    —— 此时串里已无 $ 和反引号，不会互相干扰
      5. 还原公式       —— 变成 <!--MJX ...--> 注释占位符
      6. 还原行内代码
    """
    code_spans = []
    math_spans = []

    def _stash_code(mo):
        code_spans.append(html.escape(mo.group(1)))
        return "\x00%d\x00" % (len(code_spans) - 1)

    t = re.sub(r"`([^`]+?)`", _stash_code, text)
    t = _stash_math(t, math_spans)
    t = html.escape(t)
    t = re.sub(r"\[([^\]]*)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(
        r"\x01(\d+)\x01",
        lambda mo: _math_marker(*math_spans[int(mo.group(1))]),
        t,
    )
    t = re.sub(r"\x00(\d+)\x00", lambda mo: "<code>%s</code>" % code_spans[int(mo.group(1))], t)
    return t


def md_to_html(md_text, title=""):
    """把常见 markdown 语法转成打印友好的 HTML（够用即可）"""
    # 行尾归一：CRLF / 孤立 CR → LF。
    # markdown-it 在解析前也会做同样的替换（`str.replace(/\r\n?/g,'\n')`），
    # 所以这一步是渲染中性的；不归一的话代码块里会混入 \r。
    md_text = md_text.replace("\r\n", "\n").replace("\r", "\n")
    # 跳过 frontmatter (--- ... ---)
    if md_text.startswith("---"):
        parts = md_text.split("---", 2)
        if len(parts) >= 3:
            md_text = parts[2]
    lines = md_text.split("\n")
    out = []
    # ★ 2026-09-23 修正：列表容器状态改为「哪种列表」而不是布尔 in_ol。
    #   原实现只有 `in_ol` 管有序列表，无序列表分支**直接吐裸 <li>**，
    #   从不输出 <ul>。实测 97 个产物：<li> 8929 个，<ul> **0 个**，
    #   裸露 <li> 8430 个 / 74 个文件 —— 全是非法 HTML（<li> 必须在列表容器内），
    #   浏览器只能靠容错渲染，缩进与项目符号都不受控。
    list_kind = None   # None / "ol" / "ul"
    in_table = False
    in_fence = False
    fence_quoted = False  # 代码块是否由引用块内的 ``` 开启（形如 `> ```c`）
    # ★ 2026-09-23 新增：显示公式块状态。
    #   本文档集里显示公式**主要是三行式**（`$$` 独占一行 / 内容 / `$$` 独占一行）：
    #   实测 908 个 `$$` 里 308 个是「独占一行」的定界符 ⇒ 154 个三行式块，
    #   另有 300 个单行式 `$$...$$`（由 _inline 里的 _MATH_RE 处理）。
    #   三行式不能靠逐行正则，必须用状态机，且块内**不做任何 markdown 解析**
    #   （LaTeX 里的 `_` `*` `#` 若被当成 markdown 会直接毁掉公式）。
    in_display = False
    display_buf = []

    def close_list():
        nonlocal list_kind
        if list_kind:
            out.append("</%s>" % list_kind)
            list_kind = None

    for line in lines:
        s = line.rstrip()
        # ── 代码块内部：原样保留（不解析、不 rstrip，保留缩进）──
        #   兼容引用块内的代码块：`> ```c` … `> ````，需把每行前缀的 `> ` 剥掉。
        if in_fence:
            if re.match(r"^\s*>?\s*```", s):
                out.append("</code></pre>"); in_fence = False
            else:
                out.append(html.escape(re.sub(r"^>\s?", "", line) if fence_quoted else line))
            continue
        # ── 显示公式块内部：原样累积，不解析 markdown ──
        if in_display:
            if s.strip() == "$$":
                out.append(_math_marker("\n".join(display_buf), True))
                in_display = False
                display_buf = []
            else:
                display_buf.append(line)
            continue
        # ★ 2026-09-23 修正：表格状态改为显式布尔量。
        #   原实现用 `out[-1].startswith("<table>")` 判断「是否已在表格内」，
        #   而真实开标签是 `<table border='1' cellpadding='6' ...>`（带属性），
        #   该判断**恒为假** ⇒ 每一行都新开一张表，且 `</table>` 从未被输出。
        #   实测 docs/posts/math/2021.md 源里 1 张 6 行表 → 输出 6 张未闭合单行表，
        #   单元格全部落进 `<th>`、`<td>` 数为 0。
        #   改为显式状态 + 「离开表格即闭合」，与 .gap 的处理方式保持一致。
        is_table_row = s.startswith("|") and s.count("|") > 1
        if in_table and not is_table_row:
            out.append("</table>"); in_table = False
        # ── 代码块起始（含引用块内的 `> ```c`）──
        if s.lstrip().startswith("```") or re.match(r"^>\s*```", s):
            close_list()
            out.append("<pre><code>"); in_fence = True
            fence_quoted = not s.lstrip().startswith("```")
            continue
        # ── 显示公式块起始：独占一行的 `$$` ──
        if s.strip() == "$$":
            close_list()
            in_display = True
            display_buf = []
            continue
        # ── 水平线（--- / *** / ___）──
        #   原实现落到段落分支，产物里出现字面量 `<p>---</p>`（2529 处 / 55 个文件）。
        if s.strip() and re.match(r"^(-{3,}|\*{3,}|_{3,})$", s.strip()):
            close_list()
            out.append("<hr>")
            continue
        # 标题
        m = re.match(r"^(#{1,6})\s+(.*)", s)
        if m:
            close_list()
            lv = len(m.group(1))
            out.append(f"<h{lv}>{_inline(m.group(2))}</h{lv}>")
            continue
        # 有序列表（题目选项 A. B. C. 用列表）
        m = re.match(r"^(\d+)\.\s+(.*)", s)
        if m:
            if list_kind != "ol":
                close_list(); out.append("<ol>"); list_kind = "ol"
            out.append(f"<li>{_inline(m.group(2))}</li>")
            continue
        # 无序列表（原实现只吐裸 <li>，从不输出 <ul>）
        m = re.match(r"^[-*]\s+(.*)", s)
        if m:
            if list_kind != "ul":
                close_list(); out.append("<ul>"); list_kind = "ul"
            out.append(f"<li>{_inline(m.group(1))}</li>")
            continue
        # 引用块
        m = re.match(r"^>\s?(.*)", s)
        if m:
            close_list()
            out.append(f"<blockquote>{_inline(m.group(1))}</blockquote>")
            continue
        # ── 容器标记（VitePress `::: details <标题>` / `::: tip` … `:::`）──
        #   原实现不识别，标记原样漏出（4148 处 / 30 个文件）。
        #   打印版无法折叠 ⇒ 内容一律展开；有标题的容器把标题保留成一行。
        if s.lstrip().startswith(":::"):
            close_list()
            rest = s.lstrip()[3:].strip()
            parts = rest.split(None, 1)
            if parts and parts[0] in ("details", "tip", "warning", "info", "danger", "note"):
                rest = parts[1] if len(parts) > 1 else ""
            if rest:
                out.append(f"<p class='ctitle'>{_inline(rest)}</p>")
            continue
        # 表格分隔行跳过
        if re.match(r"^\|?[\s:|-]+\|?$", s) and s.count("|") > 1:
            continue
        # 表格行（首行作表头 <th>，其余为数据行 <td>）
        if is_table_row:
            close_list()
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not in_table:
                out.append("<table border='1' cellpadding='6' style='border-collapse:collapse;width:100%'>")
                out.append("<tr>" + "".join(f"<th>{_inline(c)}</th>" for c in cells) + "</tr>")
                in_table = True
            else:
                out.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in cells) + "</tr>")
            continue
        # 空行 → 一个间距块
        #
        # ★ 2026-09-23 修正：原实现「每遇到一个空行就 append 一个 gap」，
        #   于是**空行的个数**泄漏成了输出语义 —— 源码里写 2 个连续空行，
        #   打印版就叠 2 个 gap，间距是 1 个空行的两倍。
        #   后果：只要对笔记做任何空白规范化（压连续空行），49 个可打印 HTML
        #   与 48 个 PDF 就会跟着变，源码排版被下游产物反向绑架。
        #   改为「连续空行只出一个 gap」，源码的空白风格与打印间距解耦。
        if not s.strip():
            close_list()
            if not out or not out[-1].startswith("<div class='gap'>"):
                out.append("<div class='gap'></div>")
            continue
        # 普通段落：行内格式统一走 _inline
        close_list()
        out.append(f"<p>{_inline(s)}</p>")
    close_list()
    if in_table: out.append("</table>")
    if in_fence: out.append("</code></pre>")
    # 未闭合的显示公式块（源码里漏了收尾的 $$）也要把已累积内容交出去，
    # 否则公式会**静默消失** —— 这比留个占位符更糟。
    if in_display: out.append(_math_marker("\n".join(display_buf), True))
    return "\n".join(out)

def wrap_html(body, title):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
body {{ font-family: "Microsoft YaHei", "Noto Sans SC", sans-serif; max-width: 800px; margin: 40px auto; padding: 0 24px; font-size: 14px; line-height: 1.8; color: #222; }}
h1 {{ font-size: 22px; border-bottom: 2px solid #333; padding-bottom: 8px; }}
h2 {{ font-size: 18px; margin-top: 24px; }}
h3 {{ font-size: 16px; }}
table {{ margin: 12px 0; }}
th, td {{ text-align: left; vertical-align: top; }}
ul, ol {{ margin: 8px 0; padding-left: 26px; }}
li {{ margin: 2px 0; }}
blockquote {{ border-left: 3px solid #999; margin: 8px 0; padding: 4px 12px; color: #555; background: #f7f7f7; }}
code {{ background: #f0f0f0; padding: 1px 5px; border-radius: 3px; }}
pre {{ background: #f7f7f7; border: 1px solid #e0e0e0; border-radius: 4px; padding: 10px 12px; overflow-x: auto; }}
pre code {{ background: none; padding: 0; }}
hr {{ border: none; border-top: 1px solid #ddd; margin: 18px 0; }}
a {{ color: #1a4d8f; }}
.ctitle {{ background: #eef4fb; border-left: 3px solid #7aa7d9; margin: 10px 0; padding: 6px 12px; color: #24486f; }}
.gap {{ height: 8px; }}
@media print {{ body {{ margin: 0; padding: 0; max-width: none; }} }}
</style>
</head>
<body>
{body}
</body>
</html>"""

def convert(src, dst=None):
    p = pathlib.Path(src)
    text = p.read_text(encoding="utf-8")
    # 标题：优先 frontmatter title，其次第一个 # 行
    title = ""
    fm = re.match(r"^---\n(.*?)\n---", text, re.S)
    if fm:
        tm = re.search(r"^title:\s*(.+)$", fm.group(1), re.M)
        if tm:
            title = tm.group(1).strip().strip('"\'')
    if not title:
        m = re.search(r"^#\s+(.+)$", text, re.M)
        title = m.group(1).strip() if m else p.stem
    body = md_to_html(text)
    html_doc = wrap_html(body, title)
    if dst is None:
        dst = p.with_suffix(".html")
    pathlib.Path(dst).write_text(html_doc, encoding="utf-8", newline="\n")
    return dst, title

if __name__ == "__main__":
    if "--all" in sys.argv:
        repo = pathlib.Path(__file__).resolve().parent.parent
        out_dir = repo / "docs" / "public" / "printable"
        out_dir.mkdir(exist_ok=True)
        for sub in ["math", "computer", "english", "politics"]:
            d = repo / "docs" / "posts" / sub
            if not d.exists(): continue
            for f in sorted(d.glob("*.md")):
                if f.name == "index.md": continue
                dst = out_dir / f"{sub}-{f.stem}.html"
                convert(f, dst)
                print(f"  {dst.name}")
        print("DONE: 已转换 docs/posts 下所有真题为可打印 HTML → docs/public/printable/")
        print("提示：在浏览器打开后用 Ctrl+P 打印为 PDF，或见 README 中 Chrome headless 命令")
    else:
        src = sys.argv[1]
        dst = sys.argv[2] if len(sys.argv) > 2 else None
        dst, title = convert(src, dst)
        print(f"已转换: {src} -> {dst}（{title}）")
