# -*- coding: utf-8 -*-
"""查 Anki 实况：今日复习量、高数牌组新卡是否已刷、各牌组待办。"""
import json
import urllib.request

ANKI = 'http://127.0.0.1:8765'


def invoke(action, **params):
    payload = json.dumps({'action': action, 'version': 6, 'params': params}).encode()
    req = urllib.request.Request(ANKI, payload, {'Content-Type': 'application/json'})
    data = json.loads(urllib.request.urlopen(req, timeout=20).read())
    if data.get('error'):
        raise RuntimeError(f'{action}: {data["error"]}')
    return data['result']


print('=== 今日总复习量 ===')
print('getNumCardsReviewedToday =', invoke('getNumCardsReviewedToday'))

decks = invoke('deckNames')
print('\n=== 牌组 ===')
for d in decks:
    if d == 'Default':
        continue
    print(' -', d)

print('\n=== 今日各牌组已评卡片数（rated:1）===')
for d in decks:
    if d == 'Default':
        continue
    try:
        n = len(invoke('findCards', query=f'deck:"{d}" rated:1'))
    except Exception as e:
        n = f'ERR {e}'
    print(f'  {d:40} {n}')

print('\n=== 高数牌组剩余新卡 ===')
for d in decks:
    if '高数' in d:
        new = invoke('findCards', query=f'deck:"{d}" is:new')
        due = invoke('findCards', query=f'deck:"{d}" is:due')
        print(f'  {d:40} new={len(new):4}  due={len(due):4}')

print('\n=== 全部待复习/新卡 ===')
for d in decks:
    if d == 'Default':
        continue
    new = invoke('findCards', query=f'deck:"{d}" is:new')
    due = invoke('findCards', query=f'deck:"{d}" is:due')
    if new or due:
        print(f'  {d:40} new={len(new):4}  due={len(due):4}')
