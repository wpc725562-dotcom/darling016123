# -*- coding: utf-8 -*-
"""按「学习日 + 30 分钟断档」规则，从**全部会话记录**计算有效学习时长。

学习日口径（学生 2026-10-23 更正）：13:00 起床 → 次日 03:00–04:00 睡。
一个学习日可能跨多个会话文件，必须合并后统一算断档。

用法：
  python _study_time.py "2026-10-22 13:00" "2026-10-23 04:00"
  python _study_time.py "2026-10-22 13:00" "2026-10-23 04:00" --detail
"""
import io, json, os, sys
from collections import Counter
from datetime import datetime, timedelta, timezone

TZ = timezone(timedelta(hours=8))
ROOT = r'C:/Users/Administrator/.workbuddy-ai/projects'
SKIP = ('arc-bbp-audit',)


def parse(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M').replace(tzinfo=TZ)


def main():
    t0 = parse(sys.argv[1]) if len(sys.argv) > 1 else parse('2026-10-22 13:00')
    t1 = parse(sys.argv[2]) if len(sys.argv) > 2 else parse('2026-10-23 04:00')
    detail = '--detail' in sys.argv

    stamps = []
    per_file = Counter()
    for dirpath, _, files in os.walk(ROOT):
        if any(s in dirpath for s in SKIP):
            continue
        for fn in files:
            if not fn.endswith('.jsonl'):
                continue
            path = os.path.join(dirpath, fn)
            tag = os.path.basename(dirpath)[:34]
            try:
                f = io.open(path, encoding='utf-8', errors='ignore')
            except OSError:
                continue
            with f:
                for line in f:
                    try:
                        d = json.loads(line)
                    except Exception:
                        continue
                    if d.get('type') != 'message':
                        continue
                    if d.get('role') not in ('user', 'assistant'):
                        continue
                    ts = d.get('timestamp')
                    if not isinstance(ts, (int, float)):
                        continue
                    dt = datetime.fromtimestamp(ts / 1000, TZ)
                    if t0 <= dt < t1:
                        stamps.append((dt, d['role']))
                        per_file[tag] += 1

    stamps.sort(key=lambda x: x[0])
    if not stamps:
        print('窗口内无消息')
        return

    print(f'窗口：{t0:%Y-%m-%d %H:%M} → {t1:%Y-%m-%d %H:%M}（GMT+8）')
    print(f'扫描目录：{ROOT}（已排除 {", ".join(SKIP)}）')
    print(f'消息条数：{len(stamps)}（user {sum(1 for _, r in stamps if r == "user")} / '
          f'assistant {sum(1 for _, r in stamps if r == "assistant")}）')
    print(f'首条 {stamps[0][0]:%m-%d %H:%M:%S} · 末条 {stamps[-1][0]:%m-%d %H:%M:%S}')
    if detail:
        print('按会话：')
        for k, v in per_file.most_common():
            print(f'  {k}  {v}')

    GAP = timedelta(minutes=30)
    segs, seg_start, prev = [], stamps[0][0], stamps[0][0]
    for dt, _ in stamps[1:]:
        if dt - prev > GAP:
            segs.append((seg_start, prev))
            seg_start = dt
        prev = dt
    segs.append((seg_start, prev))

    total = sum((b - a for a, b in segs), timedelta())
    print('\n断档阈值：>30 分钟不计')
    print(f'有效学习段 {len(segs)} 段：')
    for a, b in segs:
        m = int((b - a).total_seconds() // 60)
        print(f'  {a:%m-%d %H:%M} → {b:%m-%d %H:%M}   {m // 60}h{m % 60:02d}m')

    mins = int(total.total_seconds() // 60)
    print(f'\n有效学习时长 = {mins // 60}h{mins % 60:02d}m（{mins} 分钟）')

    print('\n被扣除的断档（>30 分钟）：')
    for i in range(len(segs) - 1):
        gap = segs[i + 1][0] - segs[i][1]
        m = int(gap.total_seconds() // 60)
        print(f'  {segs[i][1]:%m-%d %H:%M} → {segs[i + 1][0]:%m-%d %H:%M}   断 {m // 60}h{m % 60:02d}m')


if __name__ == '__main__':
    main()
