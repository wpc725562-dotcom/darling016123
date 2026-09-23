# -*- coding: utf-8 -*-
"""md-to-printable.py 核心逻辑单元测试

覆盖 md_to_html() 的：
  · 空行 → 间距块（连续空行只出一个 gap）
  · 表格结构（一张 md 表 → 一张闭合的 HTML 表）
  · 代码块 / 水平线 / `::: ` 容器 / 行内格式 / 链接 / 行尾

★ 为什么专门测这些：原实现把大量 markdown 语法**字面量**直接吐进产物，
  而可打印 HTML 与 PDF 是给人打印练习用的，这些泄漏肉眼可见。
  2026-09-23 实测的泄漏规模（97 个源文件）：

  | 缺陷                        | 次数 | 文件 |
  |-----------------------------|------|------|
  | 水平线 `---` → `<p>---</p>` | 2529 | 55   |
  | `::: ` 容器标记原样漏出     | 4148 | 30   |
  | 表格单元格内 `**` / `` ` `` |  564 | 37   |
  | ` ``` ` 代码块未处理        |  336 | 14   |
  | `[文本](url)` 链接未处理    |  503 | 52   |
  | 表格：每行新开一张未闭合表  |  ——  | 全部 |

  这些测试把修好的行为钉住，防止有人「顺手改回去」。

运行：python -m pytest tests/ -v
或（无 pytest）：python tests/test_md_to_printable.py
"""
import importlib.util
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# 文件名带连字符，不能直接 import，用 spec 从路径加载
_spec = importlib.util.spec_from_file_location(
    "md_to_printable", ROOT / "scripts" / "md-to-printable.py")
md_to_printable = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(md_to_printable)

GAP = "<div class='gap'></div>"


class TestBlankLineGap(unittest.TestCase):
    """空行 → 间距块：连续空行只出一个"""

    def test_single_blank_line(self):
        html = md_to_printable.md_to_html("a\n\nb")
        self.assertEqual(html.count(GAP), 1)

    def test_consecutive_blank_lines_collapse(self):
        """★ 核心回归：3 个连续空行只能产生 1 个 gap（原来会产生 3 个）"""
        html = md_to_printable.md_to_html("a\n\n\n\nb")
        self.assertEqual(html.count(GAP), 1)

    def test_many_blank_lines_collapse(self):
        html = md_to_printable.md_to_html("a\n" + "\n" * 8 + "b")
        self.assertEqual(html.count(GAP), 1)

    def test_no_blank_line_no_gap(self):
        html = md_to_printable.md_to_html("a\nb")
        self.assertEqual(html.count(GAP), 0)

    def test_two_separated_groups(self):
        """被内容隔开的两段空行，各自出一个 gap"""
        html = md_to_printable.md_to_html("a\n\n\nb\n\n\nc")
        self.assertEqual(html.count(GAP), 2)

    def test_blank_run_after_closed_list(self):
        """空行紧跟列表：仍只出一个 gap（列表闭合产生的 </ol> 不算 gap）"""
        html = md_to_printable.md_to_html("1. x\n\n\n2. y")
        self.assertEqual(html.count(GAP), 1)

    def test_frontmatter_skipped(self):
        """frontmatter 不参与输出，也不产生 gap"""
        html = md_to_printable.md_to_html("---\ntitle: t\n---\n\n# H\n")
        self.assertNotIn("title: t", html)
        self.assertIn("<h1>H</h1>", html)


class TestBasicBlocks(unittest.TestCase):
    """基本块级语法不被破坏"""

    def test_headings(self):
        html = md_to_printable.md_to_html("# a\n\n## b\n\n### c")
        for tag in ("<h1>a</h1>", "<h2>b</h2>", "<h3>c</h3>"):
            self.assertIn(tag, html)

    def test_unordered_and_ordered(self):
        self.assertIn("<li>x</li>", md_to_printable.md_to_html("- x"))
        self.assertIn("<li>y</li>", md_to_printable.md_to_html("1. y"))

    def test_unordered_items_wrapped_in_ul(self):
        """★ 原实现只吐裸 <li>，从不输出 <ul>（97 个产物里 <ul> 为 0 个，
        裸露 <li> 8430 个 / 74 个文件 —— 非法 HTML）"""
        html = md_to_printable.md_to_html("- a\n- b")
        self.assertIn("<ul>", html)
        self.assertEqual(html.count("<ul>"), 1)
        self.assertEqual(html.count("</ul>"), 1)
        self.assertIn("<li>a</li>", html)
        self.assertIn("<li>b</li>", html)

    def test_ordered_items_wrapped_in_ol(self):
        html = md_to_printable.md_to_html("1. a\n2. b")
        self.assertEqual(html.count("<ol>"), 1)
        self.assertEqual(html.count("</ol>"), 1)

    def test_list_closed_at_end_of_document(self):
        html = md_to_printable.md_to_html("- a\n- b")
        self.assertTrue(html.rstrip().endswith("</ul>"))

    def test_list_switch_closes_previous_container(self):
        """无序 → 有序 必须关掉 <ul> 再开 <ol>"""
        html = md_to_printable.md_to_html("- a\n1. b")
        self.assertEqual(html.count("<ul>"), 1)
        self.assertEqual(html.count("</ul>"), 1)
        self.assertEqual(html.count("<ol>"), 1)
        self.assertEqual(html.count("</ol>"), 1)

    def test_no_bare_li(self):
        """任何 <li> 都必须落在 <ul>/<ol> 之内

        判据：把成对的列表容器整块挖掉后，正文里不应再剩 <li>。
        （不能比 count(li) == count(ul)+count(ol)，一个容器可含多个 <li>。）
        """
        for src in ["- a\n- b", "1. a\n2. b", "- a\n\n1. b", "# H\n\n- a",
                    "| x |\n|:--|\n| 1 |\n\n- a", "- a\n- b\n\ntail"]:
            html = md_to_printable.md_to_html(src)
            stripped = re.sub(r"<ul>.*?</ul>", "", html, flags=re.S)
            stripped = re.sub(r"<ol>.*?</ol>", "", stripped, flags=re.S)
            self.assertNotIn("<li>", stripped, msg=f"裸 <li> 出现在: {src!r}")

    def test_blockquote(self):
        self.assertIn("<blockquote>q</blockquote>", md_to_printable.md_to_html("> q"))

    def test_inline_bold_and_code(self):
        html = md_to_printable.md_to_html("**b** and `c`")
        self.assertIn("<strong>b</strong>", html)
        self.assertIn("<code>c</code>", html)

    def test_table_opens(self):
        """表格至少会生成 table 标签与表头单元格"""
        html = md_to_printable.md_to_html("| a | b |\n|:--|:--|\n| 1 | 2 |")
        self.assertIn("<table", html)
        self.assertIn("<th>a</th>", html)
        self.assertNotIn("<p>|:--|:--|</p>", html)

    def test_table_body_in_same_table(self):
        """★ 2026-09-23 修复：一张 markdown 表 → 一张 HTML 表（且闭合）

        原实现用 `out[-1].startswith("<table>")` 判断「是否已在表格内」，
        但真正写入的开标签带属性（`<table border='1' cellpadding='6' …>`），
        该判断**恒为假** ⇒ 每一行都新开一张表、单元格一律落进 `<th>`，
        而且 `</table>` 从未被输出过（函数里根本没有表格状态）。
        实测 docs/posts/math/2021.md：源里 1 张 6 行表 → 输出 6 张未闭合单行表。

        现改为显式 `in_table` 状态 + 「离开表格即闭合」。
        """
        html = md_to_printable.md_to_html("| a | b |\n|:--|:--|\n| 1 | 2 |")
        self.assertEqual(html.count("<table"), 1)
        self.assertEqual(html.count("</table>"), 1)
        self.assertIn("<th>a</th>", html)
        self.assertIn("<td>1</td>", html)

    def test_table_closed_before_following_block(self):
        """表格后紧跟段落时表格须已闭合，否则段落会落进表格内部"""
        html = md_to_printable.md_to_html("| a |\n|:--|\n| 1 |\n\n段落")
        self.assertLess(html.index("</table>"), html.index("<p>段落</p>"))

    def test_two_tables_stay_separate(self):
        """被空行隔开的两张表 → 两张独立且各自闭合的表"""
        html = md_to_printable.md_to_html("| a |\n|:--|\n| 1 |\n\n| b |\n|:--|\n| 2 |")
        self.assertEqual(html.count("<table"), 2)
        self.assertEqual(html.count("</table>"), 2)
        self.assertIn("<td>1</td>", html)
        self.assertIn("<td>2</td>", html)

    def test_html_escaped(self):
        self.assertIn("&lt;script&gt;", md_to_printable.md_to_html("<script>"))


class TestCodeFence(unittest.TestCase):
    """``` 代码块：原实现完全未处理，336 处代码块被当普通段落吐出来"""

    def test_fence_wraps_in_pre_code(self):
        html = md_to_printable.md_to_html("```c\nint main(){}\n```")
        self.assertIn("<pre><code>", html)
        self.assertIn("</code></pre>", html)
        self.assertIn("int main(){}", html)

    def test_fence_content_not_parsed_as_markdown(self):
        """代码块内的 ** 与 # 不得被当成 markdown"""
        html = md_to_printable.md_to_html("```\n**not bold**\n# not heading\n```")
        self.assertNotIn("<strong>", html)
        self.assertNotIn("<h1>", html)

    def test_fence_content_escaped(self):
        html = md_to_printable.md_to_html("```\nif (a < b) x();\n```")
        self.assertIn("a &lt; b", html)
        self.assertNotIn("a < b", html)

    def test_fence_preserves_indentation(self):
        html = md_to_printable.md_to_html("```\n    indented\n```")
        self.assertIn("    indented", html)

    def test_unclosed_fence_is_closed(self):
        """源里漏写收尾 ``` 时，产物不能留下未闭合的 pre"""
        html = md_to_printable.md_to_html("```\nx")
        self.assertEqual(html.count("<pre><code>"), 1)
        self.assertEqual(html.count("</code></pre>"), 1)

    def test_two_fences(self):
        html = md_to_printable.md_to_html("```\na\n```\n\n```\nb\n```")
        self.assertEqual(html.count("<pre><code>"), 2)
        self.assertEqual(html.count("</code></pre>"), 2)

    def test_quoted_fence(self):
        """引用块内的代码块 `> ```c` … `> ``` `：前缀 `> ` 须剥掉"""
        html = md_to_printable.md_to_html("> ```c\n> int a;\n> ```")
        self.assertEqual(html.count("<pre><code>"), 1)
        self.assertEqual(html.count("</code></pre>"), 1)
        self.assertIn("int a;", html)
        self.assertNotIn("&gt; int a;", html)
        self.assertNotIn("```", html)

    def test_quoted_fence_does_not_break_plain_blockquote(self):
        """普通引用块不受影响"""
        html = md_to_printable.md_to_html("> 只是引用")
        self.assertIn("<blockquote>只是引用</blockquote>", html)
        self.assertNotIn("<pre>", html)


class TestInlineCodeProtection(unittest.TestCase):
    """行内代码必须先取出后还原，否则代码里的 ** 会被当成粗体标记

    实测 math/2023.md：先做粗体时产出
    `<code>limit((1+x<strong>2)</strong>(1/x**2), x, 0) == E</code>`（幂运算符被吃）。
    """

    def test_power_operator_survives(self):
        html = md_to_printable.md_to_html("`x**2`")
        self.assertIn("<code>x**2</code>", html)
        self.assertNotIn("<strong>", html)

    def test_real_sympy_snippet(self):
        html = md_to_printable.md_to_html("`limit((1+x**2)**(1/x**2), x, 0) == E`")
        self.assertNotIn("<strong>", html)
        self.assertIn("x**2", html)

    def test_bold_outside_code_still_works(self):
        html = md_to_printable.md_to_html("**粗** 与 `a**b`")
        self.assertIn("<strong>粗</strong>", html)
        self.assertIn("<code>a**b</code>", html)

    def test_code_in_table_cell_protected(self):
        html = md_to_printable.md_to_html("| `a**b` |\n|:--|\n| 1 |")
        self.assertIn("<th><code>a**b</code></th>", html)
        self.assertNotIn("<strong>", html)

    def test_unpaired_bold_left_literal(self):
        """源里孤立未配对的 ** 保持字面量（OCR 噪声、跨行粗体都属此类）"""
        html = md_to_printable.md_to_html("答 案 : C** : 考点")
        self.assertIn("C**", html)
        self.assertNotIn("<strong>", html)


class TestHorizontalRule(unittest.TestCase):
    """水平线：原实现输出字面量 <p>---</p>（2529 处 / 55 个文件）"""

    def test_dash_hr(self):
        html = md_to_printable.md_to_html("a\n\n---\n\nb")
        self.assertIn("<hr>", html)
        self.assertNotIn("<p>---</p>", html)

    def test_star_and_underscore_hr(self):
        self.assertIn("<hr>", md_to_printable.md_to_html("a\n\n***\n\nb"))
        self.assertIn("<hr>", md_to_printable.md_to_html("a\n\n___\n\nb"))

    def test_list_item_containing_dashes_still_a_list(self):
        """`- ---` 是列表项，不是水平线（列表判定必须优先）"""
        html = md_to_printable.md_to_html("- ---")
        self.assertIn("<li>---</li>", html)
        self.assertNotIn("<hr>", html)

    def test_bold_only_line_is_not_hr(self):
        html = md_to_printable.md_to_html("**b**")
        self.assertIn("<strong>b</strong>", html)
        self.assertNotIn("<hr>", html)


class TestContainerMarker(unittest.TestCase):
    """VitePress ::: 容器：原实现不识别，标记原样漏出（4148 处 / 30 个文件）"""

    def test_details_title_kept_marker_gone(self):
        html = md_to_printable.md_to_html("::: details 展开看答案速查表\n\n内容\n\n:::")
        self.assertNotIn(":::", html)
        self.assertNotIn("details", html)
        self.assertIn("展开看答案速查表", html)
        self.assertIn("内容", html)

    def test_bare_marker_produces_nothing(self):
        html = md_to_printable.md_to_html("a\n\n:::\n\nb")
        self.assertNotIn(":::", html)
        self.assertIn("<p>a</p>", html)
        self.assertIn("<p>b</p>", html)

    def test_tip_without_title(self):
        html = md_to_printable.md_to_html("::: tip\n\n注意\n\n:::")
        self.assertNotIn(":::", html)
        self.assertNotIn("tip", html)
        self.assertIn("注意", html)

    def test_tip_with_title(self):
        html = md_to_printable.md_to_html("::: tip 小技巧\n\n注意\n\n:::")
        self.assertIn("小技巧", html)
        self.assertNotIn(":::", html)


class TestInlineInAllBlocks(unittest.TestCase):
    """行内格式必须对标题/列表/引用/表格单元格一致生效

    原实现只对段落做粗体与行内代码替换，其余一律 html.escape() 直出，
    于是 `**合计**`（564 处 / 37 个文件）在产物里就是带星号的字面量。
    """

    def test_bold_in_table_cell(self):
        html = md_to_printable.md_to_html("| **合计** |\n|:--|\n| 1 |")
        self.assertIn("<th><strong>合计</strong></th>", html)
        self.assertNotIn("**合计**", html)

    def test_bold_in_heading(self):
        html = md_to_printable.md_to_html("# **重点**")
        self.assertIn("<h1><strong>重点</strong></h1>", html)

    def test_code_in_list_item(self):
        html = md_to_printable.md_to_html("- 用 `printf` 输出")
        self.assertIn("<li>用 <code>printf</code> 输出</li>", html)

    def test_bold_in_blockquote(self):
        html = md_to_printable.md_to_html("> **注意**")
        self.assertIn("<blockquote><strong>注意</strong></blockquote>", html)

    def test_link_rendered(self):
        """链接：原实现原样漏出 [文本](url)（503 处 / 52 个文件）"""
        html = md_to_printable.md_to_html("[考纲](https://a.example/x)")
        self.assertIn('<a href="https://a.example/x">考纲</a>', html)
        self.assertNotIn("](https://", html)

    def test_link_with_bold_text(self):
        html = md_to_printable.md_to_html("[**重点**](https://a.example)")
        self.assertIn("<strong>重点</strong>", html)
        self.assertIn("<a href=", html)


class TestLineEndings(unittest.TestCase):
    """CRLF 输入必须与 LF 输出等价（源里有 88 个文件是 CRLF）"""

    def test_crlf_same_as_lf(self):
        lf = md_to_printable.md_to_html("a\n\nb\n\n| x |\n|:--|\n| 1 |")
        crlf = md_to_printable.md_to_html("a\r\n\r\nb\r\n\r\n| x |\r\n|:--|\r\n| 1 |")
        self.assertEqual(lf, crlf)

    def test_lone_cr_normalized(self):
        self.assertEqual(
            md_to_printable.md_to_html("a\rb"),
            md_to_printable.md_to_html("a\nb"))

    def test_crlf_fence_content_has_no_stray_cr(self):
        html = md_to_printable.md_to_html("```\r\ncode\r\n```\r\n")
        self.assertNotIn("\r", html)
        self.assertIn("code", html)


# ─────────────────────── 公式（构建期预渲染）───────────────────────
#
# ★ 为什么公式要抽成占位符而不是直接输出 LaTeX：
#   可打印产物是给人打印练习用的。原实现把 `$...$` 原样吐出，97 个文件里
#   454 个显示公式 + 3720 个行内公式全是裸 LaTeX，打印出来没法看。
#   现在第一步抽成 HTML 注释占位符 `<!--MJX <d> <base64>-->`，
#   第二步 scripts/printable-math.mjs 用 MathJax 渲染成内联 SVG 写回。
#   本类测的是**第一步**的契约（占位符格式、边界、守卫）。

MARK = re.compile(r"<!--MJX ([01]) ([A-Za-z0-9+/=]*)-->")


def markers(html):
    """返回 [(display:int, latex:str)]"""
    import base64
    out = []
    for m in MARK.finditer(html):
        out.append((int(m.group(1)), base64.b64decode(m.group(2)).decode("utf-8")))
    return out


class TestMathDisplayBlock(unittest.TestCase):
    """$$ 独占一行的三行式显示公式（本文档集里 154 个块）"""

    def test_three_line_block(self):
        html = md_to_printable.md_to_html("$$\n\\lim_{x\\to 0}\\frac{1}{x}\n$$")
        ms = markers(html)
        self.assertEqual(len(ms), 1)
        self.assertEqual(ms[0][0], 1)          # display
        self.assertEqual(ms[0][1], "\\lim_{x\\to 0}\\frac{1}{x}")

    def test_multiline_content_joined_with_newline(self):
        html = md_to_printable.md_to_html("$$\na \\\\\nb\n$$")
        self.assertEqual(markers(html)[0][1], "a \\\\\nb")

    def test_content_not_parsed_as_markdown(self):
        """★ LaTeX 里的 _ * # 若被当 markdown 会直接毁掉公式"""
        html = md_to_printable.md_to_html("$$\na_1 * b_2 \\# c\n$$")
        latex = markers(html)[0][1]
        self.assertEqual(latex, "a_1 * b_2 \\# c")
        self.assertNotIn("<strong>", html)
        self.assertNotIn("<em>", html)

    def test_single_line_block(self):
        html = md_to_printable.md_to_html("$$f'(x) = 2x + \\sin x$$")
        ms = markers(html)
        self.assertEqual(len(ms), 1)
        self.assertEqual(ms[0], (1, "f'(x) = 2x + \\sin x"))

    def test_unclosed_block_still_emitted(self):
        """漏了收尾 $$ 时不能静默丢公式（与未闭合 ``` 行为一致：吞掉其后全部内容）"""
        html = md_to_printable.md_to_html("$$\n\\alpha + \\beta")
        ms = markers(html)
        self.assertEqual(len(ms), 1)
        self.assertEqual(ms[0][1], "\\alpha + \\beta")

    def test_unclosed_block_swallows_rest_like_fence(self):
        html = md_to_printable.md_to_html("$$\n\\alpha\n\n正文")
        self.assertEqual([x[1] for x in markers(html)], ["\\alpha\n\n正文"])
        self.assertNotIn("<p>正文</p>", html)

    def test_display_block_closes_open_list(self):
        html = md_to_printable.md_to_html("- a\n$$\nx\n$$\n- b")
        self.assertEqual(html.count("<ul>"), 2)
        self.assertEqual(html.count("</ul>"), 2)

    def test_two_blocks_stay_separate(self):
        html = md_to_printable.md_to_html("$$\na\n$$\n\n$$\nb\n$$")
        self.assertEqual([x[1] for x in markers(html)], ["a", "b"])

    def test_dollar_inside_fence_is_literal(self):
        html = md_to_printable.md_to_html("```\n$$\n\\alpha\n$$\n```")
        self.assertEqual(markers(html), [])
        self.assertIn("\\alpha", html)


class TestMathInline(unittest.TestCase):
    """行内 $...$（本文档集里 3715 处）"""

    def test_simple_inline(self):
        html = md_to_printable.md_to_html("令 $x = 1$ 代入")
        ms = markers(html)
        self.assertEqual(ms, [(0, "x = 1")])

    def test_latex_special_chars_survive_escaping(self):
        """★ 公式必须在 html.escape() 之前取出，否则 < > & 会被转义坏"""
        html = md_to_printable.md_to_html("当 $x < y$ 且 $a \\& b$ 时")
        self.assertEqual([x[1] for x in markers(html)], ["x < y", "a \\& b"])

    def test_bold_inside_math_not_eaten(self):
        """$a ** b$ 里的星号不能被粗体正则吃掉"""
        html = md_to_printable.md_to_html("$x**2$ 与 **粗体**")
        self.assertEqual([x[1] for x in markers(html)], ["x**2"])
        self.assertIn("<strong>粗体</strong>", html)

    def test_four_dollar_signs_are_two_inline(self):
        html = md_to_printable.md_to_html("$a$ 与 $b$")
        self.assertEqual([x[1] for x in markers(html)], ["a", "b"])

    def test_inline_in_table_cell_and_heading_and_quote(self):
        html = md_to_printable.md_to_html(
            "| 答案 | $\\dfrac12$ |\n|:--|:--|\n\n## 见 $x^2$\n\n> 由 $\\pi$ 得")
        self.assertEqual([x[1] for x in markers(html)],
                         ["\\dfrac12", "x^2", "\\pi"])

    def test_inline_does_not_span_lines(self):
        html = md_to_printable.md_to_html("价格 $100\n和 $200 元")
        self.assertEqual(markers(html), [])


class TestMathGuard(unittest.TestCase):
    """★ 散文/货币守卫 —— 这条是实测踩出来的，不是过度设计。

    英文阅读理解文里有**同一行两个货币 $**：
        english/2024.md L37  `- **A.** $50. &emsp; B. $70.`
    朴素配对会把 `50. &emsp; B. ` 当成公式渲染，**整段选项文字直接消失**。
    全量核验：3720 处行内匹配里守卫拒绝 5 处，人工确认全是散文/货币（误杀 0）。
    """

    def test_currency_pair_not_treated_as_math(self):
        html = md_to_printable.md_to_html("- **A.** $50. 和 B. $70.")
        self.assertEqual(markers(html), [])
        self.assertIn("$50.", html)          # 字面量必须原样保留
        self.assertIn("$70.", html)

    def test_currency_with_space_and_comma(self):
        html = md_to_printable.md_to_html("An ad may cost $ 250,000 per minute.")
        self.assertEqual(markers(html), [])
        self.assertIn("250,000", html)

    def test_english_prose_pair(self):
        html = md_to_printable.md_to_html(
            "there was $80 in the billfold, persuaded the thief to sit down and talk. He then counted $32.")
        self.assertEqual(markers(html), [])
        self.assertIn("billfold", html)
        self.assertIn("$32", html)

    def test_formula_with_spaces_is_still_math(self):
        """误杀检查：带空格的**真公式**不能被守卫拦下"""
        for src, latex in [
            ("当 $x \\to 0$ 时", "x \\to 0"),
            ("$f(x) = x^2$", "f(x) = x^2"),
            ("$a \\cdot b$", "a \\cdot b"),
            ("$\\sin 3x$", "\\sin 3x"),
            ("$y = 2 \\ln x$", "y = 2 \\ln x"),
            ("$S = \\pi r^2$", "S = \\pi r^2"),
        ]:
            with self.subTest(src=src):
                self.assertEqual([x[1] for x in markers(md_to_printable.md_to_html(src))],
                                 [latex])

    def test_pure_number_formula_is_math(self):
        """$4$ / $0,1$ 这类纯数字是**答案值**，是真公式，不能当货币拦掉"""
        html = md_to_printable.md_to_html("答案 | $4$ | $0,1$")
        self.assertEqual([x[1] for x in markers(html)], ["4", "0,1"])

    def test_variable_list_is_math(self):
        """★ 误杀检查：`$a, b$`（变量并列）必须放过。

        守卫若简化成「含空格且无 LaTeX 记号就拒」，这处会被误杀 ——
        实测 math/2024.md L477 就有 `$a, b$`。条件③（含 CJK 或含 >=2 字母拉丁词）
        正是为了把它和 `50. 和 B. ` 区分开。
        """
        html = md_to_printable.md_to_html("设 $a, b$ 为常数")
        self.assertEqual([x[1] for x in markers(html)], ["a, b"])

    def test_cjk_prose_pair_rejected(self):
        """中文散文配对（旧守卫因只有单个拉丁字母 B 而漏掉）"""
        html = md_to_printable.md_to_html("- **A.** $50. 和 B. $70.")
        self.assertEqual(markers(html), [])
        self.assertIn("$50.", html)
        self.assertIn("$70.", html)

    def test_prose_guard_function_directly(self):
        f = md_to_printable._looks_like_prose
        self.assertTrue(f(" 250,000 or more"))
        self.assertTrue(f("50. &emsp; B. "))
        self.assertTrue(f("50. 和 B. "))
        self.assertFalse(f("x \\to 0"))
        self.assertFalse(f("a, b"))           # 无 CJK、无 >=2 字母词 ⇒ 是公式
        self.assertFalse(f("\\alpha"))        # 无空格
        self.assertFalse(f("x + y"))          # 有运算符 ⇒ 公式


class TestMathCodeProtection(unittest.TestCase):
    """行内代码里的 $ 是代码内容，不是公式"""

    def test_dollar_in_inline_code(self):
        html = md_to_printable.md_to_html("不合法：`$123`、`$ABC`")
        self.assertEqual(markers(html), [])
        self.assertIn("<code>$123</code>", html)
        self.assertIn("<code>$ABC</code>", html)

    def test_math_looking_code_not_rendered(self):
        html = md_to_printable.md_to_html("写成 `$x^2$` 即可")
        self.assertEqual(markers(html), [])
        self.assertIn("<code>$x^2$</code>", html)

    def test_lone_dollar_literal(self):
        html = md_to_printable.md_to_html("解析：n=8，结果 37$。")
        self.assertEqual(markers(html), [])
        self.assertIn("37$", html)


class TestMathMarkerFormat(unittest.TestCase):
    """占位符格式契约（printable-math.mjs 按这个格式解析）"""

    def test_marker_is_html_comment(self):
        """★ 必须是注释：忘了跑第二步时注释不渲染，不会把 base64 印在纸上"""
        html = md_to_printable.md_to_html("$x$")
        self.assertEqual(html, "<p><!--MJX 0 eA==--></p>")
        self.assertRegex(html, r"<!--MJX 0 [A-Za-z0-9+/=]+-->")

    def test_marker_has_no_comment_terminator_risk(self):
        """base64 字母表不含 -，所以拼不出提前闭合注释的 -->"""
        import base64
        for latex in ["a-b", "a--b", "-->", "\\frac{-1}{2}"]:
            mk = md_to_printable._math_marker(latex, False)
            body = mk[len("<!--MJX 0 "):-len("-->")]
            self.assertNotIn("-", body)
            self.assertEqual(base64.b64decode(body).decode("utf-8"), latex)

    def test_display_flag_encoded(self):
        self.assertTrue(md_to_printable._math_marker("x", True).startswith("<!--MJX 1 "))
        self.assertTrue(md_to_printable._math_marker("x", False).startswith("<!--MJX 0 "))

    def test_unicode_latex_roundtrip(self):
        import base64
        mk = md_to_printable._math_marker("\\text{当 } x \\to 0", False)
        body = mk[len("<!--MJX 0 "):-len("-->")]
        self.assertEqual(base64.b64decode(body).decode("utf-8"), "\\text{当 } x \\to 0")


class TestEscapedSplit(unittest.TestCase):
    """表格切列必须与 markdown-it `escapedSplit()` 语义一致。

    ★ 为什么专门测：原实现是 `s.strip("|").split("|")`（裸 split），
      而 markdown-it 的 table 规则**只认 `\\|` 是转义竖线** —— 行内代码 span 里的
      `||` 会被当列分隔符切碎，渲染时 `for (i=0; i<columnCount; i++)` 只取前 N 格，
      **超出的内容静默消失**。实测站点与产物都中招：
        · docs/posts/computer/2025.md L1104/L1105 各丢 2 格
        · docs/posts/computer/模拟卷/卷三-拔高冲刺卷-答案.md L20 丢 8 格
          （含整段 `= 3 || 9 && -1 = 3 || 1 = 1` 推导）
    """

    def split(self, line):
        cells = md_to_printable.escaped_split(line)
        if cells and cells[0] == "":
            cells.pop(0)
        if cells and cells[-1] == "":
            cells.pop()
        return [c.strip() for c in cells]

    def test_plain_row(self):
        self.assertEqual(self.split("| a | b | c |"), ["a", "b", "c"])

    def test_no_outer_pipes(self):
        self.assertEqual(self.split("a | b"), ["a", "b"])

    def test_bare_pipe_inside_code_splits(self):
        """裸 `|` 在代码 span 里**仍然会切** —— 这是 markdown-it 的真实行为，别"修"它。"""
        self.assertEqual(self.split("| a | `&&`、`||` 的结果 |"),
                         ["a", "`&&`、`", "", "` 的结果"])

    def test_escaped_pipe_does_not_split(self):
        """`\\|` 不切列 —— 这是唯一可用的修法。"""
        self.assertEqual(self.split("| a | `&&`、`\\|\\|` 的结果 |"),
                         ["a", "`&&`、`||` 的结果"])

    def test_escaped_pipe_backslash_is_consumed(self):
        """★ 关键：反斜杠必须被**吃掉**，否则渲染出来会多出 `\\`。"""
        cells = self.split("| `\\|\\|` |")
        self.assertEqual(cells, ["`||`"])
        self.assertNotIn("\\", cells[0])

    def test_full_row_from_real_defect(self):
        """真实缺陷行：修复前后列数与内容对比。"""
        bad = ("| **逻辑运算的结果值** | `&&`、`||` 的结果**不是**两边的原值，"
               "而是 **1（真）或 0（假）** |")
        good = bad.replace("`||`", "`\\|\\|`")
        self.assertEqual(len(self.split(bad)), 4)      # 表头只有 2 列 ⇒ 后 2 格被丢弃
        self.assertEqual(len(self.split(good)), 2)
        self.assertEqual(self.split(good)[1],
                         "`&&`、`||` 的结果**不是**两边的原值，而是 **1（真）或 0（假）**")

    def test_multiple_escaped_pipes_in_one_cell(self):
        line = ("| 3 | **B** | 1.2 优先级 | `+` 和 `-` 优先级高于 `\\|\\|` 和 `&&`，"
                "等价于 `a \\|\\| (b + c) && (b - c)` = `3 \\|\\| 9 && -1` = `1`。 |")
        cells = self.split(line)
        self.assertEqual(len(cells), 4)
        self.assertIn("`||`", cells[3])
        self.assertIn("`a || (b + c) && (b - c)`", cells[3])
        self.assertNotIn("\\", cells[3])

    def test_js_substring_semantics(self):
        """JS substring(a,b) 在 a>b 时交换参数；Python 切片返回空串 —— 必须对齐。"""
        self.assertEqual(md_to_printable._js_substring("abcdef", 4, 2), "cd")
        self.assertEqual(md_to_printable._js_substring("abcdef", 2, 4), "cd")

    def test_adjacent_escaped_pipes(self):
        self.assertEqual(self.split("| \\|\\| |"), ["||"])


class TestTableColumnTruncation(unittest.TestCase):
    """表格行多出列时：按表头列数截断（对齐 markdown-it），且**不静默**。"""

    def test_row_padded_to_header_width(self):
        md = "| a | b |\n|:--|:--|\n| 1 |\n"
        html = md_to_printable.md_to_html(md)
        self.assertEqual(html.count("<td>"), 2)

    def test_extra_cells_truncated_and_warned(self):
        md = ("| a | b |\n|:--|:--|\n| 1 | x `||` y |\n")
        import io
        import contextlib
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            html = md_to_printable.md_to_html(md)
        # 截断到表头列数
        self.assertEqual(html.count("<td>"), 2)
        # 且必须报出来（截断即丢内容，不能静默）
        self.assertIn("表格列数超出", err.getvalue())

    def test_padding_does_not_warn(self):
        """少于表头列数只是补空，不丢内容 ⇒ 不该告警（免得真信号被噪声淹没）。"""
        md = "| a | b |\n|:--|:--|\n| 1 |\n"
        import io
        import contextlib
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            md_to_printable.md_to_html(md)
        self.assertEqual(err.getvalue(), "")

    def test_escaped_row_no_warning(self):
        md = ("| a | b |\n|:--|:--|\n| 1 | x `\\|\\|` y |\n")
        import io
        import contextlib
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            html = md_to_printable.md_to_html(md)
        self.assertEqual(html.count("<td>"), 2)
        self.assertNotIn("表格列数超出", err.getvalue())
        self.assertIn("<code>||</code>", html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
