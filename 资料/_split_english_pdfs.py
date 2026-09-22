# -*- coding: utf-8 -*-
"""Split English exam PDFs by year into docs/public/papers/english/."""
from __future__ import annotations

from pathlib import Path
import json
import re

from pypdf import PdfReader, PdfWriter

ROOT = Path(r"D:/专升本/专升本")
SRC = ROOT / "资料/英语真题原卷"
OUT = ROOT / "docs/public/papers/english"
OUT.mkdir(parents=True, exist_ok=True)

# 1-based inclusive page ranges carefully derived from PDF text markers.
# paper = 卷面 only; answers = 答案/解析 only; full = 整年合订（优先给站点用）
RANGES_2013_2023 = {
    # papers (卷面)
    2023: {"paper": (1, 11), "answers": (94, 99)},
    2022: {"paper": None, "answers": (100, 104)},  # 合订本卷面区未单独检出 2022 标题，下面再扫
    2021: {"paper": (12, 21), "answers": (105, 107)},
    2020: {"paper": (22, 29), "answers": (108, 111)},
    2019: {"paper": (30, 37), "answers": (112, 115)},
    2018: {"paper": (38, 45), "answers": (116, 120)},
    2017: {"paper": (46, 53), "answers": (121, 125)},
    2016: {"paper": (54, 61), "answers": (126, 131)},
    2015: {"paper": (62, 69), "answers": (132, 136)},
    2014: {"paper": (70, 77), "answers": (137, 141)},
    2013: {"paper": (78, 85), "answers": (142, 147)},
}

RANGES_2008_2012_PAPER = {
    2012: (1, 9),
    2011: (10, 19),
    2010: (20, 30),
    2009: (31, 40),
    2008: (41, 50),
}


def write_range(reader: PdfReader, start: int, end: int, dest: Path) -> int:
    """start/end are 1-based inclusive."""
    w = PdfWriter()
    for i in range(start - 1, end):
        if 0 <= i < len(reader.pages):
            w.add_page(reader.pages[i])
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("wb") as f:
        w.write(f)
    return end - start + 1


def detect_2022_paper(reader: PdfReader) -> tuple[int, int] | None:
    """Find 2022 paper start if present before 2021 block."""
    for i, page in enumerate(reader.pages[:20]):
        t = page.extract_text() or ""
        if re.search(r"2022\s*年\s*普通高等学校", t[:600]) or re.search(
            r"广东省\s*2022\s*年", t[:600]
        ):
            # end is page before 2021 (page 12 → index 11)
            return (i + 1, 11)
    return None


def main() -> None:
    meta: dict = {"years": {}, "note": "personal study use only"}

    # --- 2013-2023 combined ---
    p1323 = SRC / "广东专插本_英语_真题和答案_2013-2023.pdf"
    r1323 = PdfReader(str(p1323))
    y2022 = detect_2022_paper(r1323)
    if y2022:
        RANGES_2013_2023[2022]["paper"] = y2022
        print("detected 2022 paper", y2022)
    else:
        # 若合订本缺 2022 卷面，仍导出答案；卷面靠 OCR 文本页
        print("WARN: 2022 paper range not found in combined PDF")

    for year, ranges in sorted(RANGES_2013_2023.items(), reverse=True):
        paper = ranges.get("paper")
        answers = ranges.get("answers")
        full_path = OUT / f"{year}-full.pdf"
        paper_path = OUT / f"{year}-paper.pdf"
        ans_path = OUT / f"{year}-answers.pdf"
        w_full = PdfWriter()
        pages_info = {}

        if paper:
            n = write_range(r1323, paper[0], paper[1], paper_path)
            for i in range(paper[0] - 1, paper[1]):
                w_full.add_page(r1323.pages[i])
            pages_info["paper"] = {"start": paper[0], "end": paper[1], "pages": n}
            print(f"{year} paper pages={n} -> {paper_path.name}")

        if answers:
            n = write_range(r1323, answers[0], answers[1], ans_path)
            for i in range(answers[0] - 1, answers[1]):
                w_full.add_page(r1323.pages[i])
            pages_info["answers"] = {
                "start": answers[0],
                "end": answers[1],
                "pages": n,
            }
            print(f"{year} answers pages={n} -> {ans_path.name}")

        if len(w_full.pages) > 0:
            with full_path.open("wb") as f:
                w_full.write(f)
            pages_info["full_pages"] = len(w_full.pages)
            print(f"{year} full pages={len(w_full.pages)} -> {full_path.name}")
        meta["years"][str(year)] = pages_info

    # --- 2008-2012 papers ---
    p0812 = SRC / "广东专插本_英语_真题2008-2012.pdf"
    r0812 = PdfReader(str(p0812))
    for year, (start, end) in sorted(RANGES_2008_2012_PAPER.items(), reverse=True):
        paper_path = OUT / f"{year}-paper.pdf"
        full_path = OUT / f"{year}-full.pdf"
        n = write_range(r0812, start, end, paper_path)
        # full = paper only (answers PDF is scan without reliable page split)
        write_range(r0812, start, end, full_path)
        meta["years"][str(year)] = {
            "paper": {"start": start, "end": end, "pages": n},
            "full_pages": n,
            "answers": None,
            "note": "answers PDF is scanned; open combined local answers if needed",
        }
        print(f"{year} paper/full pages={n}")

    # 2008-2012 answers as one file (scanned, 5 pages)
    ans_src = SRC / "广东专插本_英语_真题答案_2008-2012.pdf"
    if ans_src.exists():
        dest = OUT / "2008-2012-answers.pdf"
        dest.write_bytes(ans_src.read_bytes())
        meta["answers_2008_2012"] = dest.name
        print("copied 2008-2012 answers")

    # --- 2024 full (scanned) ---
    p2024 = SRC / "广东专插本_英语_真题和答案2024年.pdf"
    if p2024.exists():
        dest_full = OUT / "2024-full.pdf"
        dest_full.write_bytes(p2024.read_bytes())
        meta["years"]["2024"] = {
            "full_pages": len(PdfReader(str(p2024)).pages),
            "note": "scanned full volume",
        }
        print(f"2024 full copied pages={meta['years']['2024']['full_pages']}")

    meta_path = OUT / "manifest.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print("manifest ->", meta_path)

    # size summary
    total = sum(p.stat().st_size for p in OUT.glob("*.pdf"))
    print(f"total PDF bytes under public: {total} ({total/1024/1024:.1f} MB)")


if __name__ == "__main__":
    main()
