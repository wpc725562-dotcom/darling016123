#!/usr/bin/env python3
"""
从官方《政治理论》真题合集 PDF 抽出客观题答案（单选 1-20 / 多选 21-30）。

为什么需要它：
    站内 `docs/posts/politics/YYYY.md` 的页首写着「权威源：站内 PDF 原卷合集（41 页，**带完整文字层**）
    —— 单选 20/20 + 多选 10/10 逐题核对，与页面零冲突」。
    这句话里的「带完整文字层」是错的：`pdftotext` 出来只剩 `A B C D` 和页码，中文全丢
    （PDF 字体编码问题）。也就是说，之前那次「核对」不可能是靠文字层做的。
    这个脚本用渲染 + OCR 把客观题答案抽成机器可读，让「核对过没有」变成可复现的事。

难点：答案页本身不写年份。
    合集是「本年试题页 → 本年答案页」的顺序，所以答案页归属**最近一次出现的试题年份**。
    年份只从试题页的卷头认（`广东省 2018 年普通高等学校本科插班生招生考试`），
    不认正文里提到的年份 —— 正文里「2010 年举办亚运会」这种会把归属带偏。

输出：data/politics-answer-keys.json
    { "2018": { "pages": [32,33,34,35,36], "answers": {"1":"B", ...} } }

用法：
    python scripts/extract-politics-keys.py                # 全量
    python scripts/extract-politics-keys.py --diag         # 只打印每页归属，不写文件
    python scripts/extract-politics-keys.py --year 2018    # 只看一年
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
PDF = ROOT / "docs" / "public" / "papers" / "politics" / "2012-2019-政治合集.pdf"
OUT = ROOT / "data" / "politics-answer-keys.json"

# 卷头年份：必须同时出现「年」和考试字样，避免把正文里的年份当卷头
HEADER_YEAR = re.compile(r"(20\d{2})\s*年[^。\n]{0,12}(?:招生考试|专插本|专升本)")

# 答案条目：`11、A` / `21、BC` / `23、ABCD`。字母后必须是空白、行尾或下一个题号。
ANSWER_ENTRY = re.compile(r"(?<!\d)(\d{1,2})\s*[、.．]\s*([A-E]{1,5})(?=\s|$|\s*\d)")

# 单个 OCR 块就是一条答案时优先用它，精度最高
ANSWER_BOX = re.compile(r"^\s*(\d{1,2})\s*[、.．]\s*([A-E]{1,5})\s*$")

_engine: RapidOCR | None = None


def engine() -> RapidOCR:
    global _engine
    if _engine is None:
        _engine = RapidOCR()
    return _engine


def ocr_page(page: pymupdf.Page, dpi: int = 500) -> list[str]:
    """渲染一页并 OCR，返回文本块列表（按阅读顺序）。dpi 要给足，单字母在低分辨率下会整块漏检。"""
    pix = page.get_pixmap(dpi=dpi)
    tmp = OUT.parent / f"._ocr_pol_{page.number}.png"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    pix.save(tmp)
    try:
        result, _ = engine()(str(tmp))
    finally:
        tmp.unlink(missing_ok=True)

    items = []
    for box, text, _score in result or []:
        items.append((min(p[1] for p in box), min(p[0] for p in box), text))
    items.sort(key=lambda it: (round(it[0] / 20), it[1]))
    return [t for _, _, t in items]


def extract_answers(texts: list[str]) -> dict[int, str]:
    answers: dict[int, str] = {}
    for t in texts:
        box = ANSWER_BOX.match(t)
        if box:
            no = int(box.group(1))
            if 1 <= no <= 30:
                answers.setdefault(no, box.group(2))
            continue
        for no_s, ans in ANSWER_ENTRY.findall(t):
            no = int(no_s)
            if 1 <= no <= 30:
                answers.setdefault(no, ans)
    return answers


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--diag", action="store_true", help="只打印每页归属与抽到的题数")
    ap.add_argument("--year", help="只输出这一年")
    args = ap.parse_args()

    doc = pymupdf.open(PDF)

    # 第一遍：OCR 全部页面，先拿到文本，再统一切块
    pages: list[dict] = []
    for pno in range(doc.page_count):
        texts = ocr_page(doc[pno])
        joined = " ".join(texts)
        pages.append(
            {
                "no": pno + 1,
                "texts": texts,
                "is_paper_start": bool(re.search(r"一\s*、\s*单项选择题", joined))
                and "本大题共" in joined,
                "answers": extract_answers(texts),
            }
        )

    # 第二遍：按「答案组」切分，不按试题块，也不按正文年份。
    #
    # 两次踩坑换来的做法：
    #   1. 按正文里的年份词判断 —— 2019 卷的卷头在合集里被裁掉了，而它的题干里全是
    #      「2018 年 5 月 16 日…」，结果整卷被误判成 2018（实测就是这么错的）。
    #   2. 按「一、单项选择题（本大题共…）」切试题块 —— 答案页的评分标准里也有同样的小节标题，
    #      41 页切出 15 个块，对不上 8 年。
    #
    # 客观题答案只出现在答案页，且每年恰好一组（可能跨两页），所以直接按答案组切：
    # 连续出现的答案页算一组，组序即年份序（合集逐年编排）。
    # 归属是否正确由 scripts/zhenti-answer-crosscheck.mjs 的比对结果反证 ——
    # 若年份错位，正确率会掉到 25% 左右，不会碰巧全对。
    groups: list[dict] = []
    for p in pages:
        ans = p["answers"]
        if len(ans) < 10:
            continue
        if groups and p["no"] - groups[-1]["pages"][-1] <= 1:
            groups[-1]["pages"].append(p["no"])
            for no, a in ans.items():
                groups[-1]["answers"].setdefault(str(no), a)
        else:
            groups.append({"pages": [p["no"]], "answers": dict(ans)})

    years = [str(2012 + i) for i in range(len(groups))]
    by_year = {y: g for y, g in zip(years, groups)}

    if args.diag:
        print(f"识别出 {len(groups)} 个答案组（应为 8 组 = 2012..2019）")
        print(f"{'年份':>6} {'页':>10} {'题数':>4}")
        for y, g in by_year.items():
            print(f"{y:>6} {','.join(map(str, g['pages'])):>10} {len(g['answers']):>4}")
        if len(groups) != 8:
            print("⚠️ 组数不是 8，年份归属不可信，先别写文件", file=sys.stderr)
        return 0

    if args.year:
        by_year = {k: v for k, v in by_year.items() if k == args.year}

    # 完整性检查：单选 1-20 + 多选 21-30，共 30 题
    for y, v in sorted(by_year.items()):
        # 键统一转成字符串再判，否则 int 键和 str 比较会「全缺」（踩过一次）
        v["answers"] = {str(k): a for k, a in sorted(v["answers"].items(), key=lambda kv: int(kv[0]))}
        v["count"] = len(v["answers"])
        missing = [n for n in range(1, 31) if str(n) not in v["answers"]]
        v["missing"] = missing
        print(
            f"{y}  {v['count']:2d}/30 题  页 {v['pages'][0]}–{v['pages'][-1]}"
            + (f"  缺 {','.join(map(str, missing))}" if missing else "  齐")
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(dict(sorted(by_year.items())), ensure_ascii=False, indent=1), "utf-8")
    print(f"\n已写入 {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
