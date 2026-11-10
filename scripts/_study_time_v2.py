# -*- coding: utf-8 -*-
"""学习时长取证 v2：Anki 复习时间戳（硬证据） ∪ 会话消息时间戳。

为什么需要两个来源：
  · 会话时间戳只覆盖「和我说话」的时刻，Anki 刷卡、纸面做题、看视频都不产生消息。
  · Anki revlog 是他亲手点的，是「当时确实在学」最硬的证据。
  · 两个来源取并集，再按 30 分钟断档规则切段。

用法：
  python _study_time_v2.py "2026-10-22 13:00" "2026-10-23 04:00"
"""
import io, json, os, sys, urllib.request
from datetime import datetime, timedelta, timezone

TZ = timezone(timedelta(hours=8))
ROOT = r'C:/Users/Administrator/.workbuddy-ai/projects'
SKIP = ('arc-bbp-audit',)
ANKI = 'http://127.0.0.1:8765'


def parse(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M').replace(tzinfo=TZ)


def inv(action, **params):
    payload = json.dumps({'action': action, 'version': 6, 'params': params}).encode()
    req = urllib.request.Request(ANKI, payload, {'Content-Type': 'application/json'})
    data = json.loads(urllib.request.urlopen(req, timeout=20).read().decode())
    if data.get('error'):
        raise RuntimeError(f'{action}: {data["error"]}')
    return data['result']


def anki_stamps(t0, t1):
    out = {}
    start = int(t0.timestamp() * 1000)
    for deck in inv('deckNames'):
        try:
            rows = inv('cardReviews', deck=deck, startID=start) or []
        except Exception:
            continue
        for r in rows:
            ms = r[0]
            dt = datetime.fromtimestamp(ms / 1000, TZ)
            if t0 <= dt < t1:
                out[ms] = dt
    return sorted(out.values())


def msg_stamps(t0, t1):
    out = []
    for dirpath, _, files in os.walk(ROOT):
        if any(s in dirpath for s in SKIP):
            continue
        for fn in files:
            if not fn.endswith('.jsonl'):
                continue
            try:
                f = io.open(os.path.join(dirpath, fn), encoding='utf-8', errors='ignore')
            except OSError:
                continue
            with f:
                for line in f:
                    try:
                        d = json.loads(line)
                    except Exception:
                        continue
                    if d.get('type') != 'message' or d.get('role') not in ('user', 'assistant'):
                        continue
                    ts = d.get('timestamp')
                    if not isinstance(ts, (int, float)):
                        continue
                    dt = datetime.fromtimestamp(ts / 1000, TZ)
                    if t0 <= dt < t1:
                        out.append(dt)
    return sorted(out)


def segments(stamps, gap_min=30):
    if not stamps:
        return []
    gap = timedelta(minutes=gap_min)
    segs, start, prev = [], stamps[0], stamps[0]
    for dt in stamps[1:]:
        if dt - prev > gap:
            segs.append((start, prev))
            start = dt
        prev = dt
    segs.append((start, prev))
    return segs


def main():
    t0 = parse(sys.argv[1]) if len(sys.argv) > 1 else parse('2026-10-22 13:00')
    t1 = parse(sys.argv[2]) if len(sys.argv) > 2 else parse('2026-10-23 04:00')

    a = anki_stamps(t0, t1)
    m = msg_stamps(t0, t1)
    print(f'窗口：{t0:%Y-%m-%d %H:%M} → {t1:%Y-%m-%d %H:%M}（GMT+8）')
    print(f'Anki 复习事件 {len(a)} 条 · 会话消息 {len(m)} 条')

    for label, stamps in (('Anki', a), ('会话', m)):
        if not stamps:
            print(f'\n{label}：窗口内无记录')
            continue
        print(f'\n{label}：{stamps[0]:%m-%d %H:%M} → {stamps[-1]:%m-%d %H:%M}')
        segs = segments(stamps)
        tot = sum((y - x for x, y in segs), timedelta())
        mins = int(tot.total_seconds() // 60)
        for x, y in segs:
            d = int((y - x).total_seconds() // 60)
            print(f'    {x:%m-%d %H:%M} → {y:%m-%d %H:%M}   {d // 60}h{d % 60:02d}m')
        print(f'    小计 {mins // 60}h{mins % 60:02d}m（{len(segs)} 段）')

    union = sorted(set(a) | set(m))
    segs = segments(union)
    tot = sum((y - x for x, y in segs), timedelta())
    mins = int(tot.total_seconds() // 60)
    print(f'\n=== 并集（Anki ∪ 会话），30 分钟断档 ===')
    print(f'有效学习段 {len(segs)} 段：')
    for x, y in segs:
        d = int((y - x).total_seconds() // 60)
        print(f'  {x:%m-%d %H:%M} → {y:%m-%d %H:%M}   {d // 60}h{d % 60:02d}m')
    print(f'\n有效学习时长 = {mins // 60}h{mins % 60:02d}m（{mins} 分钟）')
    print('\n扣除的断档（>30 分钟）：')
    for i in range(len(segs) - 1):
        g = segs[i + 1][0] - segs[i][1]
        d = int(g.total_seconds() // 60)
        print(f'  {segs[i][1]:%m-%d %H:%M} → {segs[i + 1][0]:%m-%d %H:%M}   断 {d // 60}h{d % 60:02d}m')


if __name__ == '__main__':
    main()
