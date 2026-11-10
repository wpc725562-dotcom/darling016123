# -*- coding: utf-8 -*-
"""2024 Passage B 生词卡 · 7 张（4 个自报生词 + install + 态度四词 + 第6题四选项动词）

用法：
  python _add-passageB-words-2026-10-23.py --apply
"""
import json
import sys
import urllib.request

ANKI = 'http://127.0.0.1:8765'
DECK = '专升本::英语::语境词'
MODEL = '问答题'

CARDS = [
    ("`ease` 什么意思？<br>原文：`being in and around nature <b>eases</b> anxiety`",
     "**缓解、减轻**（动词）<br>"
     "`ease anxiety` = 缓解焦虑<br>"
     "同义：`relieve`<br><br>"
     "📌 也可作名词「轻松、安逸」：`with ease` = 轻松地",
     ['英语', '生词', '真题2024', 'PassageB']),

    ("`take up` 什么意思？<br>原文：`curtains would <b>take up</b> the wall space for maps`",
     "**占用（空间 / 时间）**<br>"
     "`take up space` = 占地方 · `take up time` = 占时间<br><br>"
     "📌 另一个常见义：**开始从事** —— `take up a hobby` = 培养一个爱好<br>"
     "⚠️ 两个意思都很常考，看宾语判断：接 space/time → 占用；接 hobby/sport → 开始做",
     ['英语', '生词', '真题2024', 'PassageB', '多义词']),

    ("`frequently` 什么意思？<br>原文：`students ... want to come in more <b>frequently</b>`",
     "**频繁地、经常**（副词）<br>"
     "形容词：`frequent` · 反义：`rarely` / `seldom`<br>"
     "同义：`often`",
     ['英语', '生词', '真题2024', 'PassageB']),

    ("`donate` 什么意思？<br>原文：`The program has <b>donated</b> and installed \"tree ceilings\"`",
     "**捐赠**（动词）<br>"
     "名词：`donation`（捐赠物 / 捐款）<br>"
     "`donate A to B` = 把 A 捐给 B",
     ['英语', '生词', '真题2024', 'PassageB']),

    ("`install` 什么意思？<br>原文：`<b>installing</b> green curtains` / `<b>installed</b> \"tree ceilings\"`",
     "**安装**（动词）<br>"
     "名词：`installation`<br>"
     "⚠️ 第 7 题的干扰项 B 就是 `installing green curtains` —— 词认识，但那是**被否决的方案**",
     ['英语', '生词', '真题2024', 'PassageB']),

    ("阅读「态度题」四个标准选项词各是什么意思？<br>`Favorable` / `Shocked` / `Cautious` / `Doubtful`",
     "**Favorable** 赞成的、有利的 → <b>正面</b><br>"
     "**Shocked** 震惊的 → 一时情绪，<b>通常不是态度答案</b><br>"
     "**Cautious** 谨慎的 → 偏负面<br>"
     "**Doubtful** 怀疑的 → 负面<br><br>"
     "📌 态度题动作：把整段描述性词归到「正面 / 负面 / 中立」三档，再选词。<br>"
     "⚠️ 别抓单个词（如 `surprising` → 选 `Shocked` 是 2024 Passage B 第 9 题的原坑）。",
     ['英语', '阅读', '态度题', '高频']),

    ("2024 Passage B 第 6 题四个选项动词各是什么意思？<br>`relieve` / `boost` / `regulate` / `shorten`",
     "**relieve** 缓解、减轻<br>"
     "**boost** 提升、促进<br>"
     "**regulate** 调节、规范<br>"
     "**shorten** 缩短<br><br>"
     "原文：`It makes their concentration span shorter` ⇒ 对应 **shorten**（正确答案 C）<br>"
     "⚠️ 干扰项 A `relieves their anxiety` 把原文 `eases anxiety` 偷换成了「**减少**焦虑」—— 原文说的是「缺乏窗户影响心理健康」，不是缓解。",
     ['英语', '阅读', '同义替换', '真题2024']),
]


def invoke(action, **params):
    payload = json.dumps({'action': action, 'version': 6, 'params': params}).encode()
    req = urllib.request.Request(ANKI, payload, {'Content-Type': 'application/json'})
    data = json.loads(urllib.request.urlopen(req, timeout=20).read())
    if data.get('error'):
        raise RuntimeError(f'{action}: {data["error"]}')
    return data['result']


def main():
    apply = '--apply' in sys.argv
    decks = invoke('deckNames')
    if DECK not in decks:
        print('牌组不存在：', DECK)
        print('含「英语」的牌组：', [d for d in decks if '英语' in d])
        return 1

    notes = [{
        'deckName': DECK,
        'modelName': MODEL,
        'fields': {'正面': f, '背面': b},
        'tags': t,
        'options': {'allowDuplicate': False, 'duplicateScope': 'deck'},
    } for f, b, t in CARDS]

    print(f'准备写入 {len(notes)} 张 → {DECK}')
    for i, (f, _, _) in enumerate(CARDS, 1):
        print(f'  {i}. {f.split("<br>")[0][:50]}')
    if not apply:
        print('\n[试运行] 加 --apply 才真写入')
        return 0

    res = invoke('addNotes', notes=notes)
    print(f'\n写入结果：成功 {sum(1 for r in res if r)} / {len(res)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
