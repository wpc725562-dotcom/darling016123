#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""探测若干 B站 日语视频的分P 数与 AI 字幕可用性（只探测，不下载）。

用途：确认 N1 阶段日语视频是否还有可用的 AI 字幕轨，
以便决定「从视频提炼」还是「按教材补齐」。
"""
import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('ba', str(HERE / 'bili_analyze.py'))
ba = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ba)

COOKIE, src = ba.get_sessdata(None)
print('SESSDATA:', '已加载' if COOKIE else '缺失', '|', src)

TARGETS = [
    ('BV1hK4y1S7hz', '小昊子 0-N1语法全掌握 100集'),
    ('BV14T4y1Y78G', '研习社-小李来了 日语0-N1全套'),
    ('BV1j741167og', '周业繁 大家的日本语'),
    ('BV1Bp4y1D747', '阿飞老师 新标日0-N1（已有）'),
]

for bv, name in TARGETS:
    try:
        meta = ba.get_meta(bv)
        if not meta:
            print(f'{bv}  {name}: get_meta 失败')
            continue
        pages = meta.get('pages') or []
        print(f'\n=== {bv}  {name} ===')
        print(f'  分P总数: {len(pages)}')
        for p in pages[:3]:
            print(f'    P{p.get("page")}: {p.get("part")}  cid={p.get("cid")}')
        # 探测前 3 个分P 的字幕轨
        for p in pages[:3]:
            cid = p.get('cid')
            try:
                r = ba.probe_subtitle(cid, bv, retries=3)
            except Exception as e:
                print(f'    P{p.get("page")} 探测异常: {e}')
                continue
            print(f'    P{p.get("page")} 字幕探测 -> {r}')
    except Exception as e:
        print(f'{bv} {name} 异常: {e}')
