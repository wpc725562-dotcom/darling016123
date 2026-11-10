#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给一串 BV，报「分P数 / 时长 / 抽样字幕轨情况」。

用法：
    python scripts/probe-bv-list.py BV1Bp4y1D747 BV1j741167og ...
    python scripts/probe-bv-list.py --file bvs.txt
    python scripts/probe-bv-list.py --sample 5 BV1xxx      # 抽几个分P（默认 3）

为什么要抽样而不是全量：先花 3 次请求判「这门课有没有字幕」，
有再全量探/抓；没有就直接判 ASR，不浪费 100 次请求。
★ 抽样看到「有」也要留意 §4.3 的教训：单次结果可能是接口抖动，
  真要下结论，全量探一遍再说话。
"""
import importlib.util
import json
import pathlib
import sys
import time

SCRIPTS = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('ba', str(SCRIPTS / 'bili_analyze.py'))
ba = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ba)

args = sys.argv[1:]
sample = 3
if '--sample' in args:
    i = args.index('--sample')
    sample = int(args[i + 1])
    del args[i:i + 2]
bvs = []
if '--file' in args:
    p = args[args.index('--file') + 1]
    bvs = [l.strip() for l in pathlib.Path(p).read_text(encoding='utf-8').splitlines()
           if l.strip() and not l.startswith('#')]
else:
    bvs = args

sd, src = ba.get_sessdata(None)
if not sd:
    sys.exit('!! 没有 SESSDATA')
ba.COOKIE = sd

out = []
for bv in bvs:
    try:
        m = ba.get_meta(bv)
    except Exception as e:
        print('%-14s  取元数据失败: %s' % (bv, e))
        continue
    pages = m.get('pages') or []
    n = len(pages)
    if not n:
        print('%-14s  无分P' % bv)
        continue
    idx = sorted({0, n // 2, n - 1})[:sample]
    rows = []
    for i in idx:
        p = pages[i]
        try:
            subs, _ = ba.probe_subtitle(p['cid'], bv)
        except Exception as e:
            rows.append('P%d:ERR' % p['page'])
            continue
        rows.append('P%d:%d' % (p['page'], len(subs)))
        time.sleep(0.25)
    mins = sum(p.get('dur', 0) for p in pages) // 60
    rec = {'bv': bv, 'title': m.get('title'), 'owner': m.get('owner'),
           'pages': n, 'mins': mins, 'probe': rows}
    out.append(rec)
    print('%-14s %4dP %6.1fh  %-14s %s  %s'
          % (bv, n, mins / 60, (m.get('owner') or '')[:14],
             ' '.join(rows), (m.get('title') or '')[:34]))
    time.sleep(0.3)

print()
print('fallback（靠旧端点拿到轨的次数）=', ba._FALLBACK_HITS[0])
if out:
    pathlib.Path('/tmp/probe-out.json').write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print('已写入 /tmp/probe-out.json')
