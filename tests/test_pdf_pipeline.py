# -*- coding: utf-8 -*-
"""
pdf_pipeline.py 核心逻辑单元测试
覆盖：detect() 文件类型分流、parse_pages() 页号解析

运行：python -m pytest tests/ -v
或（无 pytest）：python tests/test_pdf_pipeline.py
"""
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import pdf_pipeline

# ★ 2026-09-23：mock 必须打在 `pymupdf` 上，不能打在 `fitz` 上。
#   `scripts/pdf_pipeline.py` 内部用 `import pymupdf as fitz`（PyMuPDF 1.24+ 的正式名；
#   `import fitz` 会打 "The `fitz` API is deprecated ... Use `import pymupdf` instead."）。
#   关键：`fitz` 与 `pymupdf` 是**两个不同的模块对象**（实测 1.28.2 下 __file__ 不同），
#   函数里的 `fitz` 只是 pymupdf 的**局部别名** —— 所以
#   `mock.patch(PDF_MOD + ".open")` 改的是另一个模块的属性，对被测代码毫无影响，
#   真实 `fitz.open("s.pdf")` 于是抛 FileNotFoundError，被 detect() 的 except
#   捕获成 "error:no such file: 's.pdf'" ⇒ 5 条用例全挂（CI run 35786037791）。
#   改 import 名字时，这里必须同步改。
PDF_MOD = "pymupdf"


class TestDetectFileType(unittest.TestCase):
    """detect(): 文件后缀分流"""

    def test_docx(self):
        self.assertEqual(pdf_pipeline.detect(Path("x.docx")), "docx")
        self.assertEqual(pdf_pipeline.detect(Path("x.DOCX")), "docx")

    def test_non_pdf(self):
        self.assertEqual(pdf_pipeline.detect(Path("x.txt")), "unknown")
        self.assertEqual(pdf_pipeline.detect(Path("x.md")), "unknown")
        self.assertEqual(pdf_pipeline.detect(Path("x")), "unknown")

    def test_pdf_open_error(self):
        """pymupdf 打不开 -> 返回 error:... 而不是崩溃"""
        with mock.patch(PDF_MOD + ".open", side_effect=RuntimeError("cannot open")):
            result = pdf_pipeline.detect(Path("bad.pdf"))
            self.assertTrue(result.startswith("error:"))


class TestDetectScanHeuristics(unittest.TestCase):
    """detect(): 扫描件 vs 文本层的启发式判断（mock pymupdf 返回假文本）"""

    def _mock_doc(self, page_texts):
        pages = []
        for t in page_texts:
            p = mock.Mock()
            p.get_text.return_value = t
            pages.append(p)
        doc = mock.Mock()
        doc.__len__ = mock.Mock(return_value=len(pages))
        doc.__getitem__ = mock.Mock(side_effect=lambda i: pages[i])
        return doc

    def test_empty_scan(self):
        """无可提取文本 -> scan"""
        with mock.patch(PDF_MOD + ".open", return_value=self._mock_doc([""])):
            self.assertEqual(pdf_pipeline.detect(Path("scan.pdf")), "scan")

    def test_short_text_scan(self):
        """提取内容过少(<80字符) -> scan"""
        doc = self._mock_doc(["hello world short"])
        with mock.patch(PDF_MOD + ".open", return_value=doc):
            self.assertEqual(pdf_pipeline.detect(Path("s.pdf")), "scan")

    def test_text_layer_chinese(self):
        """大量中文 -> text-layer"""
        doc = self._mock_doc(["这是一段正常的试卷文本。" * 30])
        with mock.patch(PDF_MOD + ".open", return_value=doc):
            self.assertEqual(pdf_pipeline.detect(Path("t.pdf")), "text-layer")

    def test_text_layer_english(self):
        """大量英文/数字 -> text-layer"""
        doc = self._mock_doc(["The quick brown fox jumps over the lazy dog. " * 20])
        with mock.patch(PDF_MOD + ".open", return_value=doc):
            self.assertEqual(pdf_pipeline.detect(Path("t.pdf")), "text-layer")

    def test_replacement_char_scan(self):
        """大量替换符(乱码) -> scan"""
        doc = self._mock_doc(["�" * 50 + "abc"])
        with mock.patch(PDF_MOD + ".open", return_value=doc):
            self.assertEqual(pdf_pipeline.detect(Path("garbled.pdf")), "scan")


class TestParsePages(unittest.TestCase):
    """parse_pages(): 页号区间解析"""

    def test_none_all(self):
        self.assertEqual(pdf_pipeline.parse_pages(None, 5), [0, 1, 2, 3, 4])

    def test_single(self):
        self.assertEqual(pdf_pipeline.parse_pages("3", 5), [2])

    def test_range(self):
        self.assertEqual(pdf_pipeline.parse_pages("1-3", 5), [0, 1, 2])

    def test_commas(self):
        self.assertEqual(pdf_pipeline.parse_pages("1,3,5", 5), [0, 2, 4])

    def test_mixed(self):
        self.assertEqual(pdf_pipeline.parse_pages("1-2,4", 5), [0, 1, 3])

    def test_out_of_range(self):
        """越界页码被截断（hi 钳制到 n）"""
        self.assertEqual(pdf_pipeline.parse_pages("99", 3), [0, 1])

    def test_zero_based_input(self):
        """0 起点会与空起始歧义，返回单页（已知行为，注意）"""
        self.assertEqual(pdf_pipeline.parse_pages("0-1", 5), [0])

    def test_open_ended_known_bug(self):
        """已知缺陷：'2-' 开放区间会抛 ValueError（int('')）——上游调用需避免"""
        with self.assertRaises(ValueError):
            pdf_pipeline.parse_pages("2-", 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
