#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描 BV14T4y1Y78G 中 N1 相关分P 的字幕可用性（高重试，结论要可信）。

输出一份「哪些分P 能从视频提炼」的清单。
"""
import importlib.util
import pathlib
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('ba', str(HERE / 'bili_analyze.py'))
ba = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ba)
ck, src = ba.get_sessdata(None)
ba.COOKIE = ck
print('SESSDATA 已加载\n')

BV = 'BV14T4y1Y78G'
meta = ba.get_meta(BV) or {}
pages = {p['page']: p for p in (meta.get('pages') or [])}
targets = list(range(143, 185))
print(f'扫描 P{targets[0]}-P{targets[-1]} 共 {len(targets)} 个分P（重试 20 次）\n')

lock = threading.Lock()
results = {}


def work(pno):
    p = pages.get(pno)
    if not p:
        return
    try:
        subs, need = ba.probe_subtitle(p['cid'], BV, retries=20)
        r = ('有' if subs else '无', bool(subs[0].get('_verified')) if subs else None)
    except Exception as e:
        r = ('错:' + type(e).__name__, None)
    with lock:
        results[pno] = (r, p.get('part'))


with ThreadPoolExecutor(max_workers=5) as ex:
    list(as_completed([ex.submit(work, n) for n in targets]))

hit = [n for n, v in results.items() if v[0][0] == '有']
miss = [n for n, v in results.items() if v[0][0] == '无']
err = [n for n, v in results.items() if v[0][0].startswith('错')]

print('=== 有字幕的分P ===')
for n in sorted(hit):
    print(f'  P{n:>3} verified={results[n][0][1]} :: {results[n][1]}')
print(f'\n=== 无字幕的分P（{len(miss)} 个）===')
for n in sorted(miss):
    print(f'  P{n:>3} :: {results[n][1]}')
if err:
    print(f'\n=== 异常（{len(err)} 个）===')
    for n in sorted(err):
        print(f'  P{n:>3} {results[n][0][0]} :: {results[n][1]}')
print(f'\n汇总：有 {len(hit)} / 无 {len(miss)} / 异常 {len(err)}')
