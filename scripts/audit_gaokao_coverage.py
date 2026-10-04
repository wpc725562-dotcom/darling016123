#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""盘点「高考英语」学科的字幕覆盖率：哪些分P 没有字幕轨。

判据
    分母 = `_part_titles_all.json` 里该 BV 的 pages（B站元数据，权威）
    分子 = 磁盘上 `subtitle_pNN.txt` 的个数
    差集 = 无字幕轨的分P（必须走 ASR 才能补）

用法
    python scripts/audit_gaokao_coverage.py
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "bili-analyze")

# 从 CATALOG 里取「高考英语」的 BV 清单
src = io.open(os.path.join(ROOT, "scripts", "bili_fetch_subs.py"),
              encoding="utf-8").read()
m = re.search(r"^CATALOG\s*=\s*(\{.*?^\})", src, re.M | re.S)
CAT = eval(m.group(1))
TARGET = "高考英语"
bvs = CAT[TARGET]

titles = json.load(io.open(os.path.join(DATA, "_part_titles_all.json"),
                           encoding="utf-8"))

tot_parts = 0
have = 0
no_sub = []          # (bv, p, part_title, dur)
no_meta = []
no_dir = []

for bv in bvs:
    meta = titles.get(bv)
    if not meta or not meta.get("pages"):
        no_meta.append(bv)
        continue
    d = os.path.join(DATA, bv)
    if not os.path.isdir(d):
        no_dir.append(bv)
        continue
    on_disk = set()
    for fn in os.listdir(d):
        mm = re.match(r"subtitle_p(\d+)\.txt$", fn)
        if mm:
            on_disk.add(int(mm.group(1)))
    for pg in meta["pages"]:
        p = pg["p"]
        tot_parts += 1
        if p in on_disk:
            have += 1
        else:
            no_sub.append((bv, p, pg.get("part", ""), pg.get("dur", 0)))

print("=" * 74)
print("学科：%s    CATALOG %d 个 BV" % (TARGET, len(bvs)))
print("-" * 74)
print("  分P 总数        %5d" % tot_parts)
print("  有字幕          %5d  (%.1f%%)" % (have, 100.0 * have / max(tot_parts, 1)))
print("  无字幕轨        %5d  (%.1f%%)" % (len(no_sub),
                                            100.0 * len(no_sub) / max(tot_parts, 1)))

# ★ 2026-09-25：语料里现在混入了**本地 ASR 补录**的字幕文件（B站端本来没有轨）。
#   它们「有字幕」但不是 B站 提供的 —— 不区分就是**过度声称**。
#   来源记在各 BV 的 `_asr.jsonl`（`_verify.jsonl` 未改动，语义是「通过 aid+cid 校验」）。
_asr = 0
_asr_sec = 0
for bv in bvs:
    p = os.path.join(ROOT, "data", "bili-analyze", bv, "_asr.jsonl")
    if not os.path.isfile(p):
        continue
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        _asr += 1
        _asr_sec += r.get("audio_sec") or 0
if _asr:
    print("    ├ 其中 **本地 ASR 补录**  %5d 个（%.1f 小时）"
          % (_asr, _asr_sec / 3600))
    print("    └ B站原生字幕           %5d 个" % (have - _asr))
print("  无元数据的 BV    %5d  %s" % (len(no_meta), no_meta[:5]))
print("  无目录的 BV      %5d  %s" % (len(no_dir), no_dir[:5]))

# 无字幕按时长排序：长的优先（内容多，值得 ASR）
no_sub.sort(key=lambda x: -x[3])
print("-" * 74)
print("无字幕轨分P（按时长降序，前 40）")
print("  %-14s %4s %6s  %s" % ("BV", "P", "时长", "分P标题"))
for bv, p, t, dur in no_sub[:40]:
    print("  %-14s %4d %5ds  %s" % (bv, p, dur, t[:46]))
if len(no_sub) > 40:
    print("  ... 另有 %d 个" % (len(no_sub) - 40))

# 汇总：无字幕的分P 落在哪些 BV、各几个
from collections import Counter
c = Counter(bv for bv, _, _, _ in no_sub)
print("-" * 74)
print("无字幕分P 按 BV 汇总（>=2 个的）")
for bv, n in c.most_common():
    if n >= 2:
        title = (titles.get(bv) or {}).get("title", "?")
        tot = len((titles.get(bv) or {}).get("pages", []))
        print("  %-14s %2d / %-3d  %s" % (bv, n, tot, title[:44]))

total_dur = sum(d for _, _, _, d in no_sub)
print("-" * 74)
print("无字幕总时长：%d 秒 ≈ %.1f 小时" % (total_dur, total_dur / 3600.0))
print("=" * 74)
sys.exit(0)
