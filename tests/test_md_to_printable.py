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


if __name__ == "__main__":
    unittest.main(verbosity=2)
