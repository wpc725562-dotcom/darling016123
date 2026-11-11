#!/usr/bin/env python3
"""
从官方答案 PDF 抽出机器可读的答案库。

为什么换校验源：
    v1/v2 拿 ForestDeer 的文字层当校验源，结论是「题号体系不一致」。
    查下去发现两层问题：
      1. YYYY-ForestDeer完整版.md 有串年文件（2008 里塞了 2009 整卷）；
      2. 就算不串年，文字层把答案字母和解析混排，取哪个字母都是启发式。
    真正权威的是 docs/public/papers/english/*-answers.pdf —— 官方答案页扫描件。
    它们是纯图片、没有文字层（pdftotext 出来是空的），所以只能渲染 + OCR。

输出：data/english-answer-keys.json
    { "2010": { "source": "2008-2012-answers.pdf#p3", "answers": {"1":"C", ...} } }

用法：
    python scripts/extract-answer-keys.py            # 全量抽取
    python scripts/extract-answer-keys.py --year 2010  # 只抽一年（调参用）
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pymupdf
from rapidocr_onnxruntime import RapidOCR

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "docs" / "public" / "papers" / "english"
OUT = ROOT / "data" / "english-answer-keys.json"

# 内联格式：`1. C` / `1．C` / `1.C`。字母后面不能紧跟字母（避免把 `2. Bb` 之类吃掉）。
# 允许 A-E：2022 年七选五第 19 题的选项有五个。
PAIR = re.compile(r"(?<!\d)(\d{1,2})\s*[.．]\s*([A-E])(?![A-Za-z])")
NUM_ONLY = re.compile(r"^\d{1,2}$")
LET_ONLY = re.compile(r"^[A-E]$")

# 页眉里的年份：`广东省 2010 年普通高等学校本科插班生招生考试`
HEADER_YEAR = re.compile(r"(20\d{2})\s*年")

_engine: RapidOCR | None = None


def engine() -> RapidOCR:
    global _engine
    if _engine is None:
        _engine = RapidOCR()
    return _engine


def ocr_page(page: pymupdf.Page, dpi: int = 500) -> list[tuple[float, float, str]]:
    """
    渲染一页并 OCR，返回按阅读顺序排好的 (y, x, text)。

    dpi 必须给足。实测同一页 300 dpi 只认出 60/75 题，400 dpi 74 题，500 dpi 才 75 题全中 ——
    答案网格里的单个字母太小，低分辨率下会被直接漏检（不是认错，是整块没输出）。
    """
    pix = page.get_pixmap(dpi=dpi)
    tmp = OUT.parent / f"._ocr_{page.number}.png"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    pix.save(tmp)
    try:
        result, _ = engine()(str(tmp))
    finally:
        tmp.unlink(missing_ok=True)

    items: list[tuple[float, float, str]] = []
    for box, text, _score in result or []:
        ys = [p[1] for p in box]
        xs = [p[0] for p in box]
        items.append((min(ys), min(xs), text))

    # 同一行内的 y 会有几像素抖动，先按 20px 分桶再按 x 排
    items.sort(key=lambda it: (round(it[0] / 20), it[1]))
    return items


def cluster_rows(items: list[tuple[float, float, str]], dpi: int = 500):
    """
    把 OCR 结果按视觉行聚成若干行，行内按 x 排序。

    行距在不同年份的卷面上不一致（有的 100px，有的 120px），所以不能用固定阈值，
    取字高的若干倍作容差。
    """
    tol = max(10.0, dpi * 0.07)
    rows: list[list[tuple[float, str]]] = []
    row_y: list[float] = []
    for y, x, text in items:
        for i, base in enumerate(row_y):
            if abs(y - base) <= tol:
                rows[i].append((x, text))
                break
        else:
            row_y.append(y)
            rows.append([(x, text)])
    for r in rows:
        r.sort()
    order = sorted(range(len(rows)), key=lambda i: row_y[i])
    return [rows[i] for i in order]


def parse_items(items: list[tuple[float, float, str]], dpi: int = 500) -> dict[int, str]:
    """
    解析答案页，同时支持两种版式：
      内联：`1. C   2. B   3. D ...`（2008-2020）
      表格：一行纯题号，下一行纯答案字母（2021 起，Part I/II/III 都是这种网格）
    """
    answers: dict[int, str] = {}
    rows = cluster_rows(items, dpi)

    for idx, row in enumerate(rows):
        texts = [t.strip() for _, t in row]

        inline_hit = False
        for t in texts:
            for no, ans in PAIR.findall(t):
                n = int(no)
                if 1 <= n <= 200:
                    answers.setdefault(n, ans)
                    inline_hit = True
        if inline_hit:
            continue

        # 表格版式：本行全是题号，下一行按 x 对齐全是答案字母
        if len(texts) < 2 or not all(NUM_ONLY.match(t) for t in texts):
            continue
        if idx + 1 >= len(rows):
            continue
        nxt = rows[idx + 1]
        if not all(LET_ONLY.match(t.strip()) for _, t in nxt):
            continue
        for x_num, t_num in row:
            best = None
            for x_let, t_let in nxt:
                if best is None or abs(x_let - x_num) < abs(best[0] - x_num):
                    best = (x_let, t_let.strip())
            # 列宽约 150px，容差给 80px 足够，超出说明这一格答案漏识别了
            if best and abs(best[0] - x_num) <= 80:
                answers.setdefault(int(t_num.strip()), best[1])

    return answers


def parse_page(page: pymupdf.Page, want_year: str, dpi: int = 500) -> tuple[dict[int, str], str | None]:
    items = ocr_page(page, dpi)
    joined = " ".join(t for _, _, t in items)

    m = HEADER_YEAR.search(joined)
    detected = m.group(1) if m else None

    return parse_items(items, dpi), detected


def collect_targets(only_year: str | None):
    """列出 (年份, pdf 路径, 页码)。"""
    targets = []
    for pdf in sorted(PDF_DIR.glob("*-answers.pdf")):
        name = pdf.name
        single = re.match(r"^(\d{4})-answers\.pdf$", name)
        doc = pymupdf.open(pdf)
        if single:
            year = single.group(1)
            if only_year and year != only_year:
                continue
            targets.append((year, pdf, 0))
            continue

        multi = re.match(r"^(\d{4})-(\d{4})-answers\.pdf$", name)
        if not multi:
            print(f"跳过无法识别的文件名：{name}", file=sys.stderr)
            continue
        # 多年度合集：先 OCR 页眉认年份，认不出就按页序倒排（该 PDF 是倒序扫描）
        lo, hi = int(multi.group(1)), int(multi.group(2))
        expected = [str(y) for y in range(hi, lo - 1, -1)]
        for pno in range(doc.page_count):
            if only_year and expected[pno] != only_year:
                continue
            targets.append((expected[pno], pdf, pno))
    return targets


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", help="只抽这一年")
    args = ap.parse_args()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    existing = json.loads(OUT.read_text("utf-8")) if OUT.exists() else {}

    for year, pdf, pno in collect_targets(args.year):
        doc = pymupdf.open(pdf)
        page = doc[pno]
        answers, detected = parse_page(page, year)
        if detected and detected != year:
            # 页眉年份是权威的，以它为准纠正预期
            print(f"⚠️  {pdf.name} 第 {pno + 1} 页页眉是 {detected}，预期 {year}，按 {detected} 记", file=sys.stderr)
            year = detected
        key = {
            "source": f"{pdf.name}#p{pno + 1}",
            "count": len(answers),
            "answers": {str(k): v for k, v in sorted(answers.items())},
        }
        existing[year] = key
        nums = sorted(answers)
        span = f"{nums[0]}..{nums[-1]}" if nums else "空"
        print(f"{year}  {len(answers):3d} 题  {span:8s}  {key['source']}")

    OUT.write_text(json.dumps(dict(sorted(existing.items())), ensure_ascii=False, indent=1), "utf-8")
    print(f"\n已写入 {OUT.relative_to(ROOT)}（{len(existing)} 个年份）")

    # 人工转录的年份覆盖 OCR 结果：OCR 在表格网格版式上会漏检字母，
    # 这些年份的答案由人工逐条读过原页，可信度高于 OCR。
    # 支持两种粒度：patch = 只补漏检的几格；answers = 整年覆盖。
    manual_path = OUT.parent / "english-answer-keys-manual.json"
    if manual_path.exists():
        manual = json.loads(manual_path.read_text("utf-8"))
        patched, overridden = [], []
        for year, entry in manual.items():
            if year.startswith("_"):
                continue
            if "patch" in entry:
                if year not in existing:
                    print(f"⚠️  人工补丁找不到年份 {year}，跳过", file=sys.stderr)
                    continue
                existing[year]["answers"].update(entry["patch"])
                existing[year]["answers"] = dict(
                    sorted(existing[year]["answers"].items(), key=lambda kv: int(kv[0]))
                )
                existing[year]["count"] = len(existing[year]["answers"])
                patched.append(f"{year}({len(entry['patch'])})")
            else:
                existing[year] = {
                    "source": entry["source"],
                    "count": len(entry["answers"]),
                    "answers": dict(sorted(entry["answers"].items(), key=lambda kv: int(kv[0]))),
                }
                overridden.append(year)
        OUT.write_text(json.dumps(dict(sorted(existing.items())), ensure_ascii=False, indent=1), "utf-8")
        if overridden:
            print(f"人工整年覆盖：{', '.join(sorted(overridden))}")
        if patched:
            print(f"人工补格：{', '.join(patched)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
