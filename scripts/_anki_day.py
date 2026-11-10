# -*- coding: utf-8 -*-
"""查指定学习日的 Anki 复习实况（默认 D017 = 10-22 15:00 → 10-23 04:00）。"""
import sqlite3
import sys
from collections import Counter
from datetime import datetime
from urllib.parse import quote

DB = r'C:\Users\Administrator\AppData\Roaming\Anki2\账户 1\collection.anki2'

# 学习日边界（学生作息 15:00 起 → 次日 04:00 睡，跨零点不切分）
START = datetime(2026, 10, 22, 15, 0)
END = datetime(2026, 10, 23, 4, 0)
if len(sys.argv) >= 3:
    START = datetime.strptime(sys.argv[1], '%Y-%m-%d %H:%M')
    END = datetime.strptime(sys.argv[2], '%Y-%m-%d %H:%M')

print('DB mtime:', datetime.fromtimestamp(__import__('os').path.getmtime(DB)).strftime('%Y-%m-%d %H:%M:%S'))
print('现在     :', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

con = sqlite3.connect('file:' + quote(DB.replace('\\', '/')) + '?mode=ro', uri=True)
cur = con.cursor()
did2name = {int(r[0]): r[1] for r in cur.execute('SELECT id, name FROM decks')}

t0, t1 = int(START.timestamp() * 1000), int(END.timestamp() * 1000)
rows = cur.execute(
    'SELECT r.id, r.cid, c.did FROM revlog r JOIN cards c ON c.id = r.cid '
    'WHERE r.id >= ? AND r.id < ? ORDER BY r.id', (t0, t1)).fetchall()

print(f'\n=== 学习日 {START:%m-%d %H:%M} → {END:%m-%d %H:%M} ===')
print(f'复习条数 {len(rows)} · 去重卡片 {len(set(r[1] for r in rows))}')
if rows:
    print('  首条', datetime.fromtimestamp(rows[0][0] / 1000).strftime('%m-%d %H:%M:%S'),
          '| 末条', datetime.fromtimestamp(rows[-1][0] / 1000).strftime('%m-%d %H:%M:%S'))
    for name, n in Counter(did2name.get(r[2], str(r[2])) for r in rows).most_common():
        print(f'  {name:42} {n:4}')

print('\n=== 各牌组剩余 new / 待复习（Anki 关闭时为上次快照）===')
for did, name in sorted(did2name.items(), key=lambda x: x[1]):
    if name == 'Default':
        continue
    new = cur.execute('SELECT COUNT(*) FROM cards WHERE did=? AND queue=0', (did,)).fetchone()[0]
    rev = cur.execute('SELECT COUNT(*) FROM cards WHERE did=? AND queue=2', (did,)).fetchone()[0]
    tot = cur.execute('SELECT COUNT(*) FROM cards WHERE did=?', (did,)).fetchone()[0]
    if tot:
        print(f'  {name:42} new={new:4} rev={rev:4} total={tot:4}')

con.close()
