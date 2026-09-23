# -*- coding: utf-8 -*-
"""md-to-printable.py 核心逻辑单元测试

覆盖：md_to_html() 的「空行 → 间距块」语义。

★ 为什么专门测这个：原实现「每遇到一个空行就 append 一个 <div class='gap'>」，
  于是**空行的个数**泄漏成了打印间距 —— 源码写 2 个连续空行，打印版就叠 2 个 gap。
  后果是「全站笔记排版统一」（压缩连续空行）会让 49 个可打印 HTML 与 48 个 PDF
  跟着一起变，源码排版被下游产物反向绑架。2026-09-23 改为「连续空行只出一个 gap」。
  本测试把这个约定钉住，防止有人「顺手改回去」。

运行：python -m pytest tests/ -v
或（无 pytest）：python tests/test_md_to_printable.py
"""
import importlib.util
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

    @unittest.expectedFailure
    def test_table_body_in_same_table(self):
        """★ 已知缺陷（本轮**未修**，故意用 expectedFailure 钉住）

        原实现：`if not out or not out[-1].startswith("<table>")`
        但真正写入的开标签是 `<table border='1' cellpadding='6' style='…'>`，
        **带了属性**，永远不可能以 `<table>` 开头 ⇒ 这个判断恒为 True
        ⇒ 每一行都新开一张表，且单元格一律用 `<th>`。
        结果：可打印 HTML 里所有 markdown 表格都是碎的（N 行 = N 张单行表）。

        修法：把判断改成 `out[-1].startswith("<table")`（去掉 `>`）。

        为什么本轮不修：它会让 49 个可打印 HTML 与 48 个 PDF 大面积变化，
        而 PDF 需本机 Chrome headless 重生成、无法在本轮逐字节验证；
        且该产物集本就已落后于源文件（会新增 23 个文件）。
        修好后本用例会 XPASS，unittest 会以「unexpected success」报错，
        提醒把 expectedFailure 摘掉。
        """
        html = md_to_printable.md_to_html("| a | b |\n|:--|:--|\n| 1 | 2 |")
        self.assertEqual(html.count("<table"), 1)
        self.assertIn("<td>1</td>", html)

    def test_html_escaped(self):
        self.assertIn("&lt;script&gt;", md_to_printable.md_to_html("<script>"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
