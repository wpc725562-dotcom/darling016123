#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用默认重试次数复测：接口是否仍能取到 AI 字幕轨。"""
import importlib.util
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('ba', str(HERE / 'bili_analyze.py'))
ba = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ba)

COOKIE, src = ba.get_sessdata(None)
print('SESSDATA:', '已加载' if COOKIE else '缺失', '|', src)

# 已知有字幕的分P
CASES = [
    ('BV1Bp4y1D747', 553902206, 'P3 五十音（上）— 已知有字幕'),
    ('BV1Bp4y1D747', 217514552, 'P2 课程简介 — 已知有字幕'),
]
for bv, cid, tag in CASES:
    try:
        subs, need = ba.probe_subtitle(cid, bv)
        print(f'\n{tag}\n  cid={cid} need_login={need} 轨数={len(subs)}')
        for s in subs:
            print('   ', {k: v for k, v in s.items() if k in
                          ('lan', 'lan_doc', 'subtitle_url', '_verified')})
    except Exception as e:
        print(f'\n{tag}\n  cid={cid} 异常: {type(e).__name__}: {e}')
