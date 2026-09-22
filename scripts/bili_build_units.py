#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 24 条视频的字幕切片成「提炼工作单元」，供并行子代理消费。

为什么要预拼接
    语料 484 万字符（约 630 万 token），远超单次上下文。走「分片提炼 → 合并」，
    但如果让子代理自己去逐个读 1300 个 subtitle_pXX.txt，光工具调用就要几十次。
    所以这里先把每个单元拼成**一个文件**，子代理只读一次。

单元怎么切
    · 按视频切；单个视频超过 --max-chars（默认 100K）就继续拆成多个单元
    · 每个分P 前插一行 `=== P12 | 标题 | 158s ===`，保留结构信息
      —— 这一行很关键：子代理能据此判断「这一段的主题是什么」

产出
    data/bili-analyze/_units/<unit_id>.txt    单元正文
    data/bili-analyze/_units/_manifest.json   单元清单（科目/BV/分P范围/字符数）
    data/bili-analyze/_part_titles_all.json   全部分P 标题缓存

用法
    python scripts/bili_build_units.py
    python scripts/bili_build_units.py --max-chars 120000
"""
import argparse
import importlib.util
import json
import pathlib

# ★ E1（2026-09-20）：锚定到脚本位置，别依赖 CWD。
ROOT = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'bili-analyze'
UNITS = ROOT / '_units'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fs = load('fs', 'scripts/bili_fetch_subs.py')
ba = load('ba', 'scripts/bili_analyze.py')


def get_titles(bv):
    """取该视频所有分P 的标题。有缓存读缓存。"""
    cache = ROOT / '_part_titles_all.json'
    db = json.loads(cache.read_text(encoding='utf-8')) if cache.exists() else {}
    if bv in db:
        return db[bv]
    m = ba.get_meta(bv)
    db[bv] = {'title': m['title'], 'owner': m.get('owner', ''),
              'pages': [{'p': p['page'], 'part': p['part'],
                         'dur': p['duration']} for p in m['pages']]}
    cache.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding='utf-8', newline='\n')
    return db[bv]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-chars', type=int, default=100000,
                    help='单个单元的字符上限（默认 100K，约 13 万 token）')
    a = ap.parse_args()

    UNITS.mkdir(parents=True, exist_ok=True)
    manifest = []
    seq = 0

    for subject, bvs in fs.CATALOG.items():
        for bv in bvs:
            bvdir = ROOT / bv
            if not bvdir.is_dir():
                continue
            try:
                info = get_titles(bv)
            except Exception as e:
                print('!! %s 取标题失败：%s' % (bv, e))
                continue
            by_p = {p['p']: p for p in info['pages']}

            buf, buf_pages, buf_chars = [], [], 0

            def flush():
                nonlocal seq, buf, buf_pages, buf_chars
                if not buf:
                    return
                seq += 1
                uid = '%s_%02d' % (bv, seq)
                (UNITS / ('%s.txt' % uid)).write_text(
                    '\n\n'.join(buf), encoding='utf-8', newline='\n')
                manifest.append({
                    'unit': uid, 'subject': subject, 'bv': bv,
                    'video_title': info['title'], 'owner': info.get('owner', ''),
                    'pages': list(buf_pages), 'chars': buf_chars,
                    'file': '_units/%s.txt' % uid,
                })
                buf, buf_pages, buf_chars = [], [], 0

            for p in sorted(by_p):
                f = bvdir / ('subtitle_p%02d.txt' % p)
                if not (f.exists() and f.stat().st_size > 0):
                    continue
                txt = f.read_text(encoding='utf-8', errors='ignore').strip()
                if not txt:
                    continue
                meta = by_p[p]
                head = '=== P%d | %s | %ds ===' % (p, meta['part'], meta['dur'])
                buf.append(head + '\n' + txt)
                buf_pages.append(p)
                buf_chars += len(txt) + len(head)
                if buf_chars >= a.max_chars:
                    flush()
            flush()

    (UNITS / '_manifest.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding='utf-8', newline='\n')

    import collections
    print('单元总数 %d' % len(manifest))
    c = collections.Counter(m['subject'] for m in manifest)
    cc = collections.Counter()
    for m in manifest:
        cc[m['subject']] += m['chars']
    print()
    print('%-6s %6s %12s' % ('科目', '单元数', '字符数'))
    for s in ('计算机', '高数', '政治', '英语'):
        print('%-6s %6d %12d' % (s, c[s], cc[s]))
    print('%-6s %6d %12d' % ('合计', len(manifest), sum(cc.values())))
    print()
    print('=== 单元清单 ===')
    for m in manifest:
        pg = m['pages']
        rng = 'P%d' % pg[0] if len(pg) == 1 else 'P%d–P%d' % (pg[0], pg[-1])
        print('  %-22s %-5s %-10s %7d 字符  %s'
              % (m['unit'], m['subject'], rng, m['chars'], m['video_title'][:26]))


if __name__ == '__main__':
    main()
