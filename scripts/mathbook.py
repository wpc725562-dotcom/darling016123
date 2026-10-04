#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mathbook —— 同济《高等数学》第八版 扫描版 PDF 取页工具

背景：
  本地 PDF 是【纯扫描版】（442 页，每页 1 张图，0 文字层），
  所以既有的 *.pdf.txt 是 OCR 产物 —— 文字尚可，【公式必坏】（分数线/上下标丢失）。
  正解：**按需把指定页渲染成 PNG**，交给多模态视觉读 → 公式也能读准。

用法：
  python scripts/mathbook.py --book 53            # 按【书页】取（推荐）
  python scripts/mathbook.py --page 70            # 按【物理页】取
  python scripts/mathbook.py --book 51-53         # 取连续几页
  python scripts/mathbook.py --find 无穷小的比较   # 先在 OCR txt 里定位，再渲染
  python scripts/mathbook.py --book 53 --vol 下   # 下册

铁律（2026-09-25 实测）：
  物理页 − 17 = 书页      （上册 物理 p70 = 书 p53 ✅）
  ⚠️ 下册的偏移【未验证】—— 用 --vol 下 时脚本会提示
"""
import argparse
import pathlib
import re
import sys

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf  # 兼容旧名

# 🔴 候选目录（按顺序找，第一个存在的生效）
#    2026-09-27 改：原写法硬编码 zzb-真题库-source，而该目录与桌面那份重复 1.1 GB
#    （实测 94/95 个文件相对路径 + 内容完全相同），准备删它。
#    改成多候选后，删掉任一目录脚本都不会断。
SRC_CANDIDATES = [
    pathlib.Path(r'C:/Users/Administrator/Desktop/广东专升本资料/guangdong-zhuanshengben-resources/高等数学/教材和辅导书'),
    pathlib.Path(r'D:/deeepseek/zzb-真题库-source/高等数学/教材和辅导书'),
]


def _pick_src() -> pathlib.Path:
    for p in SRC_CANDIDATES:
        if (p / '高等数学 第八版 上册.pdf').exists():
            return p
    return SRC_CANDIDATES[0]   # 都不在时返回首个（后续会明确报错）


SRC = _pick_src()
OCR = pathlib.Path(r'D:/deeepseek/zhuan-sheng-ben-notes/历年真题/真题txt/高等数学/教材和辅导书')
OUT = pathlib.Path(r'D:/_mathbook')

PDFS = {
    '上': SRC / '高等数学 第八版 上册.pdf',
    '下': SRC / '高等数学 第八版 下册.pdf',
}
OCRS = {
    '上': OCR / '高等数学 第八版 上册.pdf.txt',
    '下': OCR / '高等数学 第八版 下册.pdf.txt',
}

OFFSET = 17   # 物理页 − 书页（上册实测）


def render(vol: str, pages: list[int], dpi: int = 150) -> list[pathlib.Path]:
    pdf = PDFS[vol]
    if not pdf.exists():
        sys.exit(f'❌ PDF 不存在：{pdf}')
    doc = pymupdf.open(str(pdf))
    OUT.mkdir(parents=True, exist_ok=True)
    out = []
    for pno in pages:                      # pno 是【物理页】(1-based)
        if not (1 <= pno <= doc.page_count):
            print(f'  ⚠️ 物理页 {pno} 超出范围（1–{doc.page_count}），跳过')
            continue
        page = doc[pno - 1]
        pix = page.get_pixmap(dpi=dpi)
        f = OUT / f'{vol}_p{pno}.png'
        pix.save(str(f))
        out.append(f)
        print(f'  ✅ {vol}册 物理 p{pno}（书 p{pno - OFFSET}）→ {f}')
    print(f'\n  总页数：{doc.page_count}')
    doc.close()
    return out


def find(keyword: str, vol: str = '上', limit: int = 8):
    """在 OCR txt 里搜关键词，报告可能所在的书页/物理页。"""
    txt = OCRS[vol]
    if not txt.exists():
        sys.exit(f'❌ OCR txt 不存在：{txt}')
    lines = txt.read_text(encoding='utf-8', errors='replace').splitlines()
    hits = [(i + 1, l.strip()) for i, l in enumerate(lines) if keyword in l]
    if not hits:
        print(f'  ❌ OCR txt 里没找到「{keyword}」')
        return
    print(f'  「{keyword}」在 OCR txt 里命中 {len(hits)} 处（显示前 {limit}）：\n')
    # 反查最近的「--- 第N页 ---」标记
    page_marks = [(i + 1, int(m.group(1)))
                  for i, l in enumerate(lines)
                  if (m := re.match(r'-{2,}\s*第\s*(\d+)\s*页\s*-{2,}', l.strip()))]
    for ln, text in hits[:limit]:
        pdf_page = None
        for mark_ln, pno in page_marks:
            if mark_ln <= ln:
                pdf_page = pno
            else:
                break
        tag = f'物理 p{pdf_page}（书 p{pdf_page - OFFSET}）' if pdf_page else '（未定位到页码标记）'
        print(f'    txt 第 {ln} 行 | {tag}')
        print(f'      {text[:90]}')
    print(f'\n  ⚠️ 注意：OCR 的页码标记可能与真实物理页有偏差，**渲染后请核对页脚页码**。')
    print(f'  建议：python scripts/mathbook.py --page <上面报的物理页>')


def parse_pages(s: str) -> list[int]:
    if '-' in s:
        a, b = s.split('-', 1)
        return list(range(int(a), int(b) + 1))
    return [int(s)]


def main():
    ap = argparse.ArgumentParser(description='同济高数八版 扫描版 PDF 取页工具')
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--book', help='按书页取，如 53 或 51-53')
    g.add_argument('--page', help='按物理页取，如 70 或 68-70')
    g.add_argument('--find', help='在 OCR txt 里搜关键词并定位')
    ap.add_argument('--vol', default='上', choices=['上', '下'], help='上册/下册（默认上）')
    ap.add_argument('--dpi', type=int, default=150, help='渲染 DPI（默认 150）')
    a = ap.parse_args()

    if a.vol == '下':
        print('  ⚠️ 下册的「物理页 − 书页」偏移【尚未验证】，--book 可能不准，请用 --page 并核对页脚。\n')

    if a.find:
        find(a.find, a.vol)
        return

    if a.book:
        pages = [int(x) + OFFSET for x in parse_pages(a.book)]
    else:
        pages = parse_pages(a.page)
    render(a.vol, pages, a.dpi)


if __name__ == '__main__':
    main()
