#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""诊断：为什么有些分P 的字幕没下下来。

背景
    bili_fetch_subs.py 跑完报「失败 271」，报错一律是 unknown url type: ''
    —— 这是 urllib 收到空字符串 URL 时的报错。但手工复探同样的分P 又能拿到
    正常 URL。所以需要一次性把全部缺失分P 探一遍，把「探到的原始返回」记下来，
    而不是靠猜。

判据（本脚本输出）
    ok           探到轨道且 subtitle_url 非空 → 纯瞬时失败，重跑即可
    empty_url    探到轨道但 subtitle_url 为空 → 真问题，要看 is_lock / type
    no_track     一条轨都没有 → 真无字幕，走 ASR
    need_login   need_login_subtitle=True 但 0 轨 → 登录态没生效

用法
    python scripts/bili_diag_missing.py            # 探全部缺失分P
    python scripts/bili_diag_missing.py --jobs 6
产出
    data/bili-analyze/_diag_missing.json
"""
import argparse
import importlib.util
import json
import pathlib
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# ★ E1（2026-09-20）：锚定到脚本位置，别依赖 CWD。
ROOT = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'bili-analyze'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ba = load('ba', 'scripts/bili_analyze.py')
fs = load('fs', 'scripts/bili_fetch_subs.py')

_LOCK = threading.Lock()
ROWS = []


def probe_one(bv, pno, cid, dur):
    """探一个分P，返回一行诊断记录。"""
    row = {'bv': bv, 'p': pno, 'cid': cid, 'dur': dur, 'verdict': '?'}
    try:
        subs, need = ba.probe_subtitle(cid, bv)
    except Exception as e:
        row['verdict'] = 'probe_error'
        row['err'] = str(e)[:80]
        return row
    row['need_login'] = need
    row['n_tracks'] = len(subs)
    if not subs:
        row['verdict'] = 'need_login' if need else 'no_track'
        return row
    row['tracks'] = [{k: v for k, v in s.items()
                      if k in ('lan', 'lan_doc', 'is_lock', 'type',
                               'subtitle_url', 'ai_status', 'id_str')}
                     for s in subs[:4]]
    urls = [(s.get('subtitle_url') or s.get('subtitleUrl') or '') for s in subs]
    if any(urls):
        row['verdict'] = 'ok'
    else:
        row['verdict'] = 'empty_url'
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jobs', type=int, default=6)
    a = ap.parse_args()

    sd, src = ba.get_sessdata()
    if not sd:
        raise SystemExit('!! 没有 SESSDATA')
    ba.COOKIE = sd
    print('SESSDATA: %s' % src)

    miss = json.loads((ROOT / '_missing_parts.json').read_text(encoding='utf-8'))
    tasks = []
    for bv, pages in miss.items():
        m = ba.get_meta(bv)
        by_p = {p['page']: p for p in m['pages']}
        for pno in pages:
            p = by_p.get(pno)
            if p:
                tasks.append((bv, pno, p['cid'], p['duration']))
    print('待诊断 %d 个分P\n' % len(tasks))

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(probe_one, *t) for t in tasks]
        for fu in as_completed(futs):
            r = fu.result()
            with _LOCK:
                ROWS.append(r)

    ROWS.sort(key=lambda r: (r['verdict'], r['bv'], r['p']))
    (ROOT / '_diag_missing.json').write_text(
        json.dumps(ROWS, ensure_ascii=False, indent=1), encoding='utf-8', newline='\n')

    import collections
    cnt = collections.Counter(r['verdict'] for r in ROWS)
    print('=' * 66)
    print('用时 %.1f 分' % ((time.time() - t0) / 60))
    for k, v in cnt.most_common():
        print('  %-14s %4d' % (k, v))
    print()
    for verdict in ('empty_url', 'need_login', 'probe_error'):
        rows = [r for r in ROWS if r['verdict'] == verdict]
        if not rows:
            continue
        print('--- %s（%d 个，前 8 条）---' % (verdict, len(rows)))
        for r in rows[:8]:
            print('  %s P%d dur=%ss need_login=%s tracks=%s'
                  % (r['bv'], r['p'], r['dur'], r.get('need_login'),
                     json.dumps(r.get('tracks', []), ensure_ascii=False)[:220]))
        print()
    print('明细已写出 %s' % (ROOT / '_diag_missing.json'))


if __name__ == '__main__':
    main()
