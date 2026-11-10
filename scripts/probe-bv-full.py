#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""逐分P 全量探测某 BV 的字幕轨，输出统计 + 无轨分P 清单。"""
import importlib.util
import json
import pathlib
import sys
import time

SCRIPTS = pathlib.Path('D:/deeepseek/zhuan-sheng-ben-notes/scripts')
spec = importlib.util.spec_from_file_location('ba', str(SCRIPTS / 'bili_analyze.py'))
ba = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ba)

bv = sys.argv[1]
survey = json.loads(pathlib.Path('D:/专升本资料/_manifest/survey.json').read_text(encoding='utf-8'))
by_bv = {c['bvid']: c for c in survey}
sd, _ = ba.get_sessdata(None)
ba.COOKIE = sd

c = by_bv.get(bv)
if not c:
    meta = ba.get_meta(bv)
    parts = [{'p': i + 1, 't': t, 'cid': cid} for i, (t, cid) in enumerate(zip(meta['pages_title'], meta['pages_cid']))]
    title = meta.get('title', '')
else:
    parts = c['parts']
    title = c['title']

hit, miss, fail = [], [], []
for p in parts:
    try:
        subs, _ = ba.probe_subtitle(p['cid'], bv)
    except Exception as e:
        fail.append('P%d(%s)' % (p['p'], e))
        continue
    if subs and (subs[0].get('subtitle_url') or subs[0].get('subtitleUrl')):
        hit.append(p['p'])
    else:
        miss.append(p['p'])
    time.sleep(0.12)

print('BV =', bv, '|', title[:40])
print('总分P %d | 有轨 %d | 无轨 %d | 异常 %d' % (len(parts), len(hit), len(miss), len(fail)))
if miss:
    print('无轨分P：', ','.join(str(x) for x in miss))
if fail:
    print('异常：', '; '.join(fail))
