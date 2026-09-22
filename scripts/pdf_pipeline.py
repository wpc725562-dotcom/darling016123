#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专升本 PDF/DOCX 分流流水线（本地缓存 → 文本 → 供写 Markdown）

原则：
- 输出只写到缓存目录或 stdout；正式笔记由人/助手校对后写入 历年真题/
- 绝不 git add PDF

用法示例：
  python scripts/pdf_pipeline.py detect "D:/专升本/_pdf_cache/forestdeer/英语/xxx.pdf"
  python scripts/pdf_pipeline.py text   "path/to.pdf" --pages 1-3
  python scripts/pdf_pipeline.py ocr    "path/to-scan.pdf" --pages 1-2 --dpi 250
  python scripts/pdf_pipeline.py docx   "path/to.docx"
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

# ★ A5 残留（2026-09-20）：tesseract OCR 原先没有 timeout —— 外部命令挂住脚本就不返回。
SUBPROC_TIMEOUT = int(os.environ.get("ZHENTI_SUBPROC_TIMEOUT", "600"))


def detect(path: Path) -> str:
    suf = path.suffix.lower()
    if suf == ".docx":
        return "docx"
    if suf != ".pdf":
        return "unknown"
    try:
        # ★ E4 连带（2026-09-20）：`import fitz` 是**已弃用的旧名**，
        #   实测会打 "The `fitz` API is deprecated and will be removed in future.
        #   Use `import pymupdf` instead."。PyMuPDF 1.28 里 `pymupdf` 才是正式名。
        #   用 `as fitz` 保留下面 `fitz.open(...)` 的写法，改动面最小。
        import pymupdf as fitz

        doc = fitz.open(path)
        sample = ""
        for i in range(min(2, len(doc))):
            sample += doc[i].get_text("text") or ""
        cleaned = re.sub(r"\s+", "", sample)
        # 汉字量：扫描件常只有水印/乱码，几乎没有成段中文
        cn = len(re.findall(r"[一-鿿]", sample))
        # 可读英文/数字（精析 PDF 中英混排）
        alnum = len(re.findall(r"[A-Za-z0-9]{2,}", sample))
        # 扫描件：可提取字少，或中英都稀
        if len(cleaned) < 80:
            return "scan"
        if cn < 40 and alnum < 40:
            return "scan"
        # 大量控制符/替换符 → 当扫描
        bad = sample.count("�") + len(re.findall(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", sample))
        if bad > 20 and cn < 80:
            return "scan"
        return "text-layer"
    except Exception as e:
        return f"error:{e}"


def extract_text_pdf(path: Path, pages: str | None, out: Path | None) -> str:
    import pymupdf as fitz

    doc = fitz.open(path)
    idxs = parse_pages(pages, len(doc))
    parts = []
    for i in idxs:
        parts.append(f"===== PAGE {i + 1} =====\n")
        parts.append(doc[i].get_text("text") or "")
        parts.append("\n")
    text = "".join(parts)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8", newline="\n")
    return text


def extract_docx(path: Path, out: Path | None) -> str:
    try:
        from docx import Document
    except ImportError:
        raise SystemExit("需要: pip install python-docx")
    doc = Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8", newline="\n")
    return text


def ocr_pdf(
    path: Path,
    pages: str | None,
    dpi: int,
    out: Path | None,
    engine: str,
) -> str:
    import pymupdf as fitz
    import numpy as np
    from PIL import Image

    doc = fitz.open(path)
    idxs = parse_pages(pages, len(doc))
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    chunks: list[str] = []

    if engine == "rapid":
        from rapidocr_onnxruntime import RapidOCR

        ocr = RapidOCR()
    elif engine == "tesseract":
        import subprocess
        import tempfile
    else:
        raise SystemExit("engine 仅支持 rapid | tesseract")

    for i in idxs:
        page = doc[i]
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        chunks.append(f"===== PAGE {i + 1} =====\n")
        if engine == "rapid":
            arr = np.array(img)
            result, _ = ocr(arr)
            if result:
                for item in result:
                    chunks.append(item[1] + "\n")
        else:
            with tempfile.TemporaryDirectory() as td:
                png = Path(td) / "p.png"
                img.save(png)
                base = Path(td) / "out"
                subprocess.run(
                    ["tesseract", str(png), str(base), "-l", "chi_sim+eng", "--psm", "6"],
                    check=False,
                    capture_output=True,
                    timeout=SUBPROC_TIMEOUT,
                )
                tpath = Path(str(base) + ".txt")
                if tpath.exists():
                    chunks.append(tpath.read_text(encoding="utf-8", errors="replace"))
        chunks.append("\n")

    text = "".join(chunks)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8", newline="\n")
    return text


def parse_pages(spec: str | None, n: int) -> list[int]:
    if not spec:
        return list(range(n))
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            lo, hi = int(a), int(b)
            out.extend(range(max(0, lo - 1), min(n, hi)))
        else:
            i = int(part) - 1
            if 0 <= i < n:
                out.append(i)
    return out or list(range(min(2, n)))


def main() -> None:
    # Windows 控制台
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        # ★ A6 复核（2026-09-20）：**有意**吞掉。这只是让 Windows 控制台别乱码，
        #   失败不影响流水线任何产出（stdout 已被重定向时本来就会抛）。
        pass

    ap = argparse.ArgumentParser(description="专升本 PDF 分流流水线")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_det = sub.add_parser("detect", help="判断 text-layer / scan / docx")
    p_det.add_argument("path")

    p_txt = sub.add_parser("text", help="有文字层 PDF 抽文本")
    p_txt.add_argument("path")
    p_txt.add_argument("--pages", default=None, help="如 1-3 或 1,2,5")
    p_txt.add_argument("-o", "--out", default=None)

    p_ocr = sub.add_parser("ocr", help="扫描件 OCR")
    p_ocr.add_argument("path")
    p_ocr.add_argument("--pages", default="1-2")
    p_ocr.add_argument("--dpi", type=int, default=250)
    p_ocr.add_argument("--engine", choices=["rapid", "tesseract"], default="rapid")
    p_ocr.add_argument("-o", "--out", default=None)

    p_docx = sub.add_parser("docx", help="DOCX 抽文本")
    p_docx.add_argument("path")
    p_docx.add_argument("-o", "--out", default=None)

    p_auto = sub.add_parser("auto", help="detect 后自动 text/ocr/docx")
    p_auto.add_argument("path")
    p_auto.add_argument("--pages", default="1-3")
    p_auto.add_argument("--dpi", type=int, default=250)
    p_auto.add_argument("-o", "--out", default=None)

    args = ap.parse_args()
    path = Path(args.path)
    if not path.exists():
        raise SystemExit(f"文件不存在: {path}")

    if args.cmd == "detect":
        kind = detect(path)
        print(kind)
        return

    out = Path(args.out) if getattr(args, "out", None) else None

    if args.cmd == "text":
        t = extract_text_pdf(path, args.pages, out)
        if not out:
            print(t)
        else:
            print(f"wrote {out} ({len(t)} chars)")
        return

    if args.cmd == "ocr":
        t = ocr_pdf(path, args.pages, args.dpi, out, args.engine)
        if not out:
            print(t)
        else:
            print(f"wrote {out} ({len(t)} chars)")
        return

    if args.cmd == "docx":
        t = extract_docx(path, out)
        if not out:
            print(t)
        else:
            print(f"wrote {out} ({len(t)} chars)")
        return

    if args.cmd == "auto":
        kind = detect(path)
        print(f"# detect: {kind}", file=sys.stderr)
        if kind == "docx":
            t = extract_docx(path, out)
        elif kind == "text-layer":
            t = extract_text_pdf(path, args.pages, out)
        elif kind == "scan":
            t = ocr_pdf(path, args.pages, args.dpi, out, "rapid")
        else:
            raise SystemExit(f"无法处理: {kind}")
        if not out:
            print(t)
        else:
            print(f"wrote {out} ({len(t)} chars)")
        return


if __name__ == "__main__":
    main()
