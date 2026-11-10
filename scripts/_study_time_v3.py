# -*- coding: utf-8 -*-
"""学习时长取证 v3：Anki 走 sqlite 直读（AnkiConnect 未开时可用） ∪ 会话消息时间戳。"""
import io, json, os, sqlite3, sys, pathlib
from datetime import datetime, timedelta, timezone

TZ = timezone(timedelta(hours=8))
ROOT = r'C:/Users/Administrator/.workbuddy-ai/projects'
SKIP = ('arc-bbp-audit',)
DB = pathlib.Path(r'C:/Users/Administrator/AppData/Roaming/Anki2/账户 1/collection.anki2')


def parse(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M').replace(tzinfo=TZ)


def anki_stamps(t0, t1):
    uri = 'file:%s?mode=ro' % DB.as_posix().replace(' ', '%20')
    con = sqlite3.connect(uri, uri=True)
    ms0 = int(t0.timestamp() * 1000)
    ms1 = int(t1.timestamp() * 1000)
    rows = con.execute('select id from revlog where id>=? and id<?', (ms0, ms1)).fetchall()
    con.close()
    return sorted(datetime.fromtimestamp(r[0] / 1000, TZ) for r in rows)


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
    t0 = parse(sys.argv[1])
    t1 = parse(sys.argv[2])
    a = anki_stamps(t0, t1)
    m = msg_stamps(t0, t1)
    print(f'窗口 {t0:%m-%d %H:%M} → {t1:%m-%d %H:%M} · Anki {len(a)} 条 · 会话 {len(m)} 条')
    for label, stamps in (('Anki', a), ('会话', m)):
        if not stamps:
            print(f'{label}: 无')
            continue
        segs = segments(stamps)
        tot = sum((y - x for x, y in segs), timedelta())
        print(f'{label} {stamps[0]:%H:%M}→{stamps[-1]:%H:%M}:', end=' ')
        print(' · '.join(f'{x:%H:%M}-{y:%H:%M}({int((y-x).total_seconds()//60)}m)' for x, y in segs))
    union = sorted(set(a) | set(m))
    segs = segments(union)
    tot = sum((y - x for x, y in segs), timedelta())
    mins = int(tot.total_seconds() // 60)
    print(f'\n=== 并集（30 分钟断档）===')
    for x, y in segs:
        print(f'  {x:%H:%M} → {y:%H:%M}  {int((y-x).total_seconds()//60)} 分钟')
    print(f'有效学习时长 = {mins//60}h{mins%60:02d}m（{mins} 分钟，{len(segs)} 段）')


if __name__ == '__main__':
    main()
