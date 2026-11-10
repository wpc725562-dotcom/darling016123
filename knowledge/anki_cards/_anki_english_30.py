# -*- coding: utf-8 -*-
"""
给英语牌组单独建配置并提高新卡上限（不影响 C语言 / 高数）
用法: python _anki_english_30.py          # 试运行
      python _anki_english_30.py --apply  # 真执行
"""
import json, sys, urllib.request

ANKI = 'http://127.0.0.1:8765'
APPLY = '--apply' in sys.argv
TARGET = 30
CFG_NAME = '英语-30新'


def invoke(action, params=None):
    payload = json.dumps({'action': action, 'version': 6, 'params': params or {}}).encode()
    req = urllib.request.Request(ANKI, payload, {'Content-Type': 'application/json'})
    data = json.loads(urllib.request.urlopen(req, timeout=15).read())
    if data.get('error'):
        raise RuntimeError(f'{action}: {data["error"]}')
    return data['result']


decks = [d for d in invoke('deckNames')
         if d == '专升本::英语' or d.startswith('专升本::英语::')]

base = invoke('getDeckConfig', {'deck': '专升本::英语'})
print(f'基准配置: id={base["id"]} name={base["name"]} new.perDay={base["new"]["perDay"]}')

# 探测是否已有同名配置（遍历所有英语牌组的配置名）
known = {}
for d in decks:
    c = invoke('getDeckConfig', {'deck': d})
    known[c['name']] = c['id']
print('英语牌组当前用到的配置:', known)

if CFG_NAME in known:
    new_id = known[CFG_NAME]
    print(f'配置「{CFG_NAME}」已存在 id={new_id}，复用')
else:
    if not APPLY:
        print(f'\n[试运行] 将执行：')
        print(f'  1) 克隆配置 {base["id"]} → 「{CFG_NAME}」')
        print(f'  2) 设 new.perDay={TARGET}（原 {base["new"]["perDay"]}）')
        print(f'  3) 把 {len(decks)} 个英语牌组指向新配置')
        for d in decks:
            print('     -', d)
        print('\n加 --apply 真执行')
        sys.exit(0)
    new_id = invoke('cloneDeckConfigId', {'name': CFG_NAME, 'cloneFrom': base['id']})
    print(f'已克隆 → id={new_id}')

cfg = invoke('getDeckConfig', {'deck': '专升本::英语'})
cfg['id'] = new_id
cfg['name'] = CFG_NAME
cfg['new']['perDay'] = TARGET
if APPLY:
    print('保存配置:', invoke('saveDeckConfig', {'config': cfg}))
    print('分配牌组:', invoke('setDeckConfigId', {'decks': decks, 'configId': new_id}))

print('\n--- 验证 ---')
for d in decks:
    c = invoke('getDeckConfig', {'deck': d})
    print(f'  {d:30s} cfg={c["name"]:12s} new.perDay={c["new"]["perDay"]}')
print('--- 非英语牌组（应保持 20）---')
for d in ['专升本::C语言::知识点', '专升本::高数::知识点']:
    c = invoke('getDeckConfig', {'deck': d})
    print(f'  {d:30s} cfg={c["name"]:12s} new.perDay={c["new"]["perDay"]}')
