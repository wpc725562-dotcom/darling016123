# -*- coding: utf-8 -*-
"""直读 Anki collection.anki2（新版 schema，只读），核对今日真实复习量。"""
import json
import os
import sqlite3
from collections import Counter
from datetime import datetime
from urllib.parse import quote

DB = r'C:\Users\Administrator\AppData\Roaming\Anki2\账户 1\collection.anki2'
print('DB mtime:', datetime.fromtimestamp(os.path.getmtime(DB)).strftime('%Y-%m-%d %H:%M:%S'))
print('现在     :', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

con = sqlite3.connect('file:' + quote(DB.replace('\\', '/')) + '?mode=ro', uri=True)
cur = con.cursor()

did2name = {int(r[0]): r[1] for r in cur.execute('SELECT id, name FROM decks')}

mx = cur.execute('SELECT MAX(id) FROM revlog').fetchone()[0]
print('最后一条复习记录:', datetime.fromtimestamp(mx / 1000).strftime('%Y-%m-%d %H:%M:%S'))

d0 = datetime(2026, 10, 21, 15, 0)
d1 = datetime(2026, 10, 22, 4, 0)
t0, t1 = int(d0.timestamp() * 1000), int(d1.timestamp() * 1000)

rows = cur.execute(
    'SELECT r.id, r.cid, c.did FROM revlog r JOIN cards c ON c.id = r.cid '
    'WHERE r.id >= ? AND r.id < ? ORDER BY r.id', (t0, t1)).fetchall()

print(f'\n=== 学习日 {d0:%m-%d %H:%M} → {d1:%m-%d %H:%M}：{len(rows)} 条复习 ===')
if rows:
    print('  首条', datetime.fromtimestamp(rows[0][0] / 1000).strftime('%m-%d %H:%M:%S'),
          '| 末条', datetime.fromtimestamp(rows[-1][0] / 1000).strftime('%m-%d %H:%M:%S'))
    for name, n in Counter(did2name.get(r[2], str(r[2])) for r in rows).most_common():
        print(f'  {name:42} {n:4}')

t2 = int(datetime(2026, 10, 22, 0, 0).timestamp() * 1000)
today = [r for r in rows if r[0] >= t2]
print(f'\n=== 10-22 00:00 之后：{len(today)} 条 ===')
for name, n in Counter(did2name.get(r[2], str(r[2])) for r in today).most_common():
    print(f'  {name:42} {n:4}')

print('\n=== 最后 20 条明细 ===')
for _id, cid, did in rows[-20:]:
    print('  ', datetime.fromtimestamp(_id / 1000).strftime('%m-%d %H:%M:%S'),
          did2name.get(did, did))

print('\n=== 各牌组剩余 new / 待复习 ===')
for did, name in sorted(did2name.items(), key=lambda x: x[1]):
    if name == 'Default':
        continue
    new = cur.execute('SELECT COUNT(*) FROM cards WHERE did=? AND queue=0', (did,)).fetchone()[0]
    rev = cur.execute('SELECT COUNT(*) FROM cards WHERE did=? AND queue=2', (did,)).fetchone()[0]
    lrn = cur.execute('SELECT COUNT(*) FROM cards WHERE did=? AND queue IN (1,3)', (did,)).fetchone()[0]
    tot = cur.execute('SELECT COUNT(*) FROM cards WHERE did=?', (did,)).fetchone()[0]
    if tot:
        print(f'  {name:42} new={new:4} learn={lrn:3} rev={rev:4} total={tot:4}')

con.close()
