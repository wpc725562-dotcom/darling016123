#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""探测 D:/专升本资料 里 8 个本地库没有的 BV 是否有 B站 AI 字幕轨。

不下载，只调 probe_subtitle(cid, bv) 看返回的轨列表是否非空、是否通过 aid+cid 校验。
每个 BV 抽样若干分P（默认首、中、尾各一个），够判「有没有字幕」这件事。
"""
import importlib.util
import json
import pathlib
import sys

SCRIPTS = pathlib.Path('D:/deeepseek/zhuan-sheng-ben-notes/scripts')
spec = importlib.util.spec_from_file_location('ba', str(SCRIPTS / 'bili_analyze.py'))
ba = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ba)

NEW_BVS = [
    'BV1FWiLeFECK',  # 郑多分 政治毛概考点精讲 19
    'BV1YJM46XEud',  # 阿来 2027政治0基础 58
    'BV17b7664EZL',  # 秦天 27年英语零基础 125
    'BV1UXdhBCEkb',  # 刘晓艳 语法精讲 21
    'BV1SnYF6eEcC',  # 米哥 27年高数 60
    'BV1RwXvBpE7q',  # 一灯 计算机精讲 34
    'BV1je41157EL',  # 阿廖 2022数学真题 1
    'BV1QN411B7Qo',  # 老唐 计算机真题 3
]

survey = json.loads(pathlib.Path('D:/专升本资料/_manifest/survey.json').read_text(encoding='utf-8'))
by_bv = {c['bvid']: c for c in survey}

sd, src = ba.get_sessdata(None)
if not sd:
    sys.exit('!! 没有 SESSDATA')
ba.COOKIE = sd
print('SESSDATA 已加载（%s）\n' % src)

for bv in NEW_BVS:
    c = by_bv.get(bv)
    if not c:
        print('%s  不在 survey.json' % bv)
        continue
    parts = c['parts']
    n = len(parts)
    idx = sorted({0, n // 2, n - 1})
    rows = []
    for i in idx:
        p = parts[i]
        try:
            subs, _need = ba.probe_subtitle(p['cid'], bv)
        except Exception as e:
            rows.append('P%d 探轨异常:%s' % (p['p'], e))
            continue
        if not subs:
            rows.append('P%d 无轨' % p['p'])
        else:
            s0 = subs[0]
            url = s0.get('subtitle_url') or s0.get('subtitleUrl') or ''
            rows.append('P%d 有轨 lang=%s verified=%s url=%s'
                        % (p['p'], s0.get('lan') or s0.get('lan_doc'),
                           s0.get('_verified'), 'Y' if url else 'N'))
    print('%-14s %-3d集  %s  %s' % (bv, n, c['owner'][:8], ' | '.join(rows)))
