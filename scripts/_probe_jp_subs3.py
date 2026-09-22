#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""探测 B站 日语视频的字幕可用性（修正版：显式设置模块级 COOKIE）。

★ 坑：bili_analyze 的模块级 COOKIE 只在 main() 里被赋值。
   直接 import 后调用 probe_subtitle() 会**不带 cookie**，
   于是 need_login_subtitle=True、subtitles=[] —— 表现为「全部无字幕」。
   必须先 ba.COOKIE = <sessdata>。
"""
import importlib.util
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('ba', str(HERE / 'bili_analyze.py'))
ba = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ba)

ck, src = ba.get_sessdata(None)
ba.COOKIE = ck                      # ★ 关键
print('SESSDATA:', '已加载' if ck else '缺失', '|', src)

TARGETS = [
    ('BV1Bp4y1D747', '阿飞老师 新标日0-N1', 3),
    ('BV1hK4y1S7hz', '小昊子 0-N1语法全掌握100集', 4),
    ('BV14T4y1Y78G', '研习社-小李来了 日语0-N1全套', 4),
    ('BV1j741167og', '周业繁 大家的日本语', 3),
]

for bv, name, n in TARGETS:
    meta = ba.get_meta(bv) or {}
    pages = meta.get('pages') or []
    print(f'\n=== {bv}  {name} | 分P={len(pages)} ===')
    for p in pages[:n]:
        cid = p.get('cid')
        try:
            subs, need = ba.probe_subtitle(cid, bv, retries=6)
        except Exception as e:
            print(f'  P{p.get("page")} 异常 {type(e).__name__}: {e}')
            continue
        tag = '有字幕' if subs else '无字幕'
        ver = subs[0].get('_verified') if subs else None
        print(f'  P{p.get("page")} [{tag}] need={need} verified={ver} :: {p.get("part")}')
