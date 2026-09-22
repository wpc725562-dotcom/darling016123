"""批量 OCR ForestDeer 缓存盘里的扫描件 PDF -> 资料/ForestDeer文字版/

源文件在 D:/专升本/_pdf_cache/forestdeer/（仓库外，不进 Git）。
输出按学科分子目录，文件名去掉「（公众号：xxx）」等引流噪声。
支持断点续跑：已 OCR 的页会被跳过。

用法:
  python scripts/ocr_forestdeer_batch.py --list
  python scripts/ocr_forestdeer_batch.py [--dpi 200] [--limit N]
"""

from __future__ import annotations

import argparse
import io
import os
import re
import sys
import time

import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_vision_ocr import (  # noqa: E402
    MODEL,
    OutOfCredit,
    api_key,
    ocr_page,
    render_page,
    sort_pages,
)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ★ E1（2026-09-20）：仓库外的数据缓存，路径按本机现状写死 → 改成可覆盖。
#       FORESTDEER_CACHE=/path/to/forestdeer python scripts/ocr_forestdeer_batch.py
CACHE = os.environ.get("FORESTDEER_CACHE") or r"D:\专升本\_pdf_cache\forestdeer"
OUT = os.path.join(REPO, "资料", "ForestDeer文字版")

NOISE = re.compile(r"（公众号：[^）]*）|\(公众号：[^)]*\)|_unlocked|_\(1\)|\(\d+\)")


def clean_name(stem: str) -> str:
    s = NOISE.sub("", stem)
    s = re.sub(r"\s+", " ", s).strip(" -_")
    return s


def out_path(pdf: str) -> str:
    rel = os.path.relpath(pdf, CACHE)
    subj = rel.split(os.sep)[0]
    stem = os.path.splitext(os.path.basename(pdf))[0]
    return os.path.join(OUT, subj, clean_name(stem) + ".md")


def done_pages(md: str) -> set[int]:
    if not os.path.exists(md):
        return set()
    return {int(m) for m in re.findall(r"<!-- OCR-PAGE (\d+) -->", io.open(md, encoding="utf-8").read())}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--limit", type=int, default=0, help="只处理前 N 个文件（调试用）")
    args = ap.parse_args()

    pdfs = []
    for dirpath, _, files in os.walk(CACHE):
        for f in sorted(files):
            if f.lower().endswith(".pdf"):
                pdfs.append(os.path.join(dirpath, f))
    pdfs.sort()

    plan = []
    for pdf in pdfs:
        doc = pymupdf.open(pdf)
        n = doc.page_count
        doc.close()
        md = out_path(pdf)
        todo = [p for p in range(1, n + 1) if p not in done_pages(md)]
        if todo:
            plan.append((pdf, md, n, todo))
    if args.limit:
        plan = plan[: args.limit]

    total_pages = sum(len(t) for _, _, _, t in plan)
    print(f"待处理 {len(plan)} 个文件 / {total_pages} 页 -> {OUT}\n", flush=True)
    if args.list:
        for _, md, n, todo in plan:
            print(f"  {n:3d}页 待{len(todo):3d}  {os.path.relpath(md, REPO)}")
        return 0

    key = api_key()
    for idx, (pdf, md, n, todo) in enumerate(plan, 1):
        rel = os.path.relpath(md, REPO)
        print(f"[{idx}/{len(plan)}] {rel} ({len(todo)}/{n}页)", flush=True)
        os.makedirs(os.path.dirname(md), exist_ok=True)
        if not os.path.exists(md):
            io.open(md, "w", encoding="utf-8", newline="\n").write(
                f"# {os.path.splitext(os.path.basename(pdf))[0]}\n\n"
                f"> 视觉模型 OCR（`{MODEL}` via baiapi）· 源 {n} 页 · dpi={args.dpi} · "
                f"{time.strftime('%Y-%m-%d')}\n"
                f"> 源文件：ForestDeer 上游扫描件，缓存于 `D:/专升本/_pdf_cache/forestdeer/`（不进 Git）\n"
                f"> **需人工校对**；政治背诵类内容请以官方教材表述为准。\n"
            )
        for pno in todo:
            try:
                text = ocr_page(key, render_page(pdf, pno, args.dpi))
            except OutOfCredit as exc:
                print(f"  !! 余额不足，停止：{exc}", flush=True)
                return 3
            except RuntimeError as exc:
                print(f"  !! p{pno} 跳过: {str(exc)[:100]}", flush=True)
                continue
            with open(md, "a", encoding="utf-8", newline="\n") as f:
                f.write(f"\n<!-- OCR-PAGE {pno} -->\n\n{text}\n")
            time.sleep(1.0)
        sort_pages(md)
        print(f"   -> 完成，现有 {len(done_pages(md))}/{n} 页", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
