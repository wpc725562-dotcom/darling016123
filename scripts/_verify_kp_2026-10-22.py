# -*- coding: utf-8 -*-
"""校验 knowledge-progress.json 并输出状态统计。"""
import json, io, sys

P = 'D:/studio/data/knowledge-progress.json'
d = json.load(io.open(P, encoding='utf-8'))
print('JSON 合法 ✓  schema =', d['schema'], '| updatedAt =', d['updatedAt'])
print('caveats 条数:', len(d['caveats']), '(应为 7)')
print()

for s in d['subjects']:
    ms = s['modules']
    cnt = {}
    for m in ms:
        cnt[m['state']] = cnt.get(m['state'], 0) + 1
    has_score = all('score' in m for m in ms)
    print(f"== {s['subject']}（{len(ms)} 模块）")
    print('   ', cnt)
    if has_score:
        tot = sum(m['score'] for m in ms)
        done = sum(m['score'] for m in ms if m['state'] == 'done')
        act = sum(m['score'] for m in ms if m['state'] == 'active')
        print(f'    分值合计 {tot}  | done {done} ({done/tot*100:.0f}%)'
              f'  | done+active {done+act} ({(done+act)/tot*100:.0f}%)')
    for m in ms:
        if m['state'] != 'todo':
            print(f"      [{m['state']:6}] {m['name']}")
    print()

# 全量非 todo 汇总
print('--- 全表非 todo ---')
for s in d['subjects']:
    for m in s['modules']:
        if m['state'] != 'todo':
            print(f"{s['short']:4} {m['state']:6} {m['name']}")
