#!/usr/bin/env python3
"""数据结构资料取页工具（严蔚敏《数据结构》C语言版）

🔴 两个 PDF 的性质完全不同（2026-09-27 实测）：

| PDF | 页数 | 文字层 | 用法 |
|:--|:--:|:--|:--|
| 教材 `数据结构c_严蔚敏.pdf`（30 MB） | 347 | **纯扫描**（只有水印 www.TopSage.com） | **必须渲染** |
| 答案 `数据结构习题集答案_严蔚敏.pdf`（609 KB） | 113 | **文字版**（正文完整，公式散成字符） | 可检索 + 渲染 |

用法：
    python scripts/dsbook.py --book 教材 --page 6      # 渲染教材某页
    python scripts/dsbook.py --book 答案 --page 6      # 渲染答案某页
    python scripts/dsbook.py --book 答案 --text 6      # 看答案某页文字层
    python scripts/dsbook.py --book 答案 --find "斐波那契"   # 检索（仅答案有效）
    python scripts/dsbook.py --list                    # 列出两个 PDF 的状态

输出：D:/_dsbook/<book>_p<N>.png
"""
import argparse
import pathlib
import sys

BASE = pathlib.Path('D:/deeepseek/zhuan-sheng-ben-notes/_downloads/教材PDF')
BOOKS = {
    '教材': BASE / '数据结构c_严蔚敏.pdf',
    '答案': BASE / '数据结构习题集答案_严蔚敏.pdf',
}
OUTDIR = pathlib.Path('D:/_dsbook')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--book', choices=list(BOOKS), default='答案')
    ap.add_argument('--page', type=int, help='物理页码（从 1 数）')
    ap.add_argument('--text', type=int, help='只输出该页文字层')
    ap.add_argument('--find', type=str, help='全文检索关键词')
    ap.add_argument('--list', action='store_true', help='列出两个 PDF 的状态')
    ap.add_argument('--dpi', type=int, default=150)
    a = ap.parse_args()

    import pymupdf

    if a.list:
        print('=== 两个 PDF 的状态 ===')
        for name, p in BOOKS.items():
            if not p.exists():
                print(f'  {name}: ❌ 不存在')
                continue
            d = pymupdf.open(p)
            # 抽样 3 页判断文字层
            probe = [3, 10, 30]
            chars = sum(len(d[i].get_text()) for i in probe if i < d.page_count)
            kind = '文字版 ✅' if chars > 500 else '扫描版 ❌（需渲染）'
            print(f'  {name}: {p.name}')
            print(f'     {d.page_count} 页 · {p.stat().st_size} B · 抽样 {len(probe)} 页 {chars} 字符 ⇒ {kind}')
        return

    pdf = BOOKS[a.book]
    if not pdf.exists():
        sys.exit(f'❌ 不存在：{pdf}')
    d = pymupdf.open(pdf)
    print(f'📖 [{a.book}] {pdf.name} · 共 {d.page_count} 页')

    if a.find:
        hits = [i + 1 for i in range(d.page_count) if a.find in d[i].get_text()]
        print(f'🔍 「{a.find}」命中 {len(hits)} 页：{hits[:30]}')
        if not hits and a.book == '教材':
            print('   ⚠️ 教材是扫描版 —— 检索无效，请用 --page 渲染')
        return

    if a.text:
        p = a.text - 1
        if not (0 <= p < d.page_count):
            sys.exit(f'❌ 页码超范围（1~{d.page_count}）')
        t = d[p].get_text()
        print(f'\n--- 第 {a.text} 页 · 文字层（{len(t)} 字符）---')
        if len(t) < 30:
            print('⚠️ 文字层几乎为空 ⇒ 这页是【扫描图】，请用 --page 渲染')
        print(t)
        return

    if a.page:
        p = a.page - 1
        if not (0 <= p < d.page_count):
            sys.exit(f'❌ 页码超范围（1~{d.page_count}）')
        OUTDIR.mkdir(parents=True, exist_ok=True)
        f = OUTDIR / f'{a.book}_p{a.page}.png'
        d[p].get_pixmap(dpi=a.dpi).save(f)
        print(f'✅ 已渲染 → {f}')
        print(f'   大小 {f.stat().st_size} B · dpi {a.dpi}')
        return

    ap.print_help()


if __name__ == '__main__':
    main()
