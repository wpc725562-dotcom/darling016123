# -*- coding: utf-8 -*-
"""2024 Passage B 三处陷阱卡 · 3 张

用法：
  python _add-passageB-trap-cards-2026-10-23.py --apply
"""
import json
import sys
import urllib.request

ANKI = 'http://127.0.0.1:8765'
DECK = '专升本::英语::错题'
MODEL = '问答题'

CARDS = [
    ("阅读里看到 `However / But` 该做什么？（以 2024 Passage B 第 7 题为例）",
     "**`However` 一出现，前面那句就作废了 —— 真正的答案在后面。**<br><br>"
     "原文：<br>"
     "`he planned to print pictures of trees onto <u>curtains</u>`<br>"
     "`<b>However</b>, his colleagues reminded him that curtains would take up the wall space`<br>"
     "`So he thought, \"Why not use the ceilings?\"` → `got them printed onto the ceilings`<br><br>"
     "题目问 `Hayden brought nature into classrooms by ______` ⇒ 答案 <b>D. printing tree photos onto the ceiling</b>。<br>"
     "⚠️ 选项 <b>B. installing green curtains on the walls</b> 就是给「只读到 However 之前」的人准备的。",
     ['英语', '阅读', '路标词', 'However', '真题2024']),

    ("题干出现 `led to` / `result in` 时，要选什么？感受还是结果？（2024 Passage B 第 8 题）",
     "**选「客观结果」，不选「个人感受」。**<br><br>"
     "题干：`The change of the classrooms <b>led to</b> the students' ______`<br>"
     "❌ 陷阱：Dave 的 `It is pretty great and <u>beautiful</u>` —— 这是<b>感受</b>，不是结果；对应选项 A `better sense of beauty` 是钓饵。<br>"
     "✅ 答案句：`<b>Overall</b>, the class attendance has gone up because students are happier` ⇒ <b>B. increased attendance</b><br><br>"
     "📌 `<b>Overall / In short / In a word</b>` 后面常是总结性答案。",
     ['英语', '阅读', '路标词', 'led to', '真题2024']),

    ("阅读「态度题」（attitude）该看什么？（2024 Passage B 第 9 题）",
     "**看整段，不看哪个词最像。**<br><br>"
     "Dave 说了三句：<br>"
     "① `It is <u>surprising</u> to see trees here.`（意外）<br>"
     "② `It is <b>pretty great and beautiful</b>.`（好）<br>"
     "③ `When I look up, it feels like I am <b>sitting under a tree</b>.`（舒服）<br>"
     "三句合起来是正面 ⇒ <b>A. Favorable</b><br><br>"
     "❌ 陷阱：只抓 ① 的 `surprising` 去选 <b>B. Shocked</b>。`surprising` 是一时情绪，不是**态度**。<br>"
     "✅ 动作：把整段的描述性词归到「正面 / 负面 / 中立」三档，再选对应词。",
     ['英语', '阅读', '态度题', '真题2024']),
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
        print(f'  {i}. {f[:44]}')
    if not apply:
        print('\n[试运行] 加 --apply 才真写入')
        return 0

    res = invoke('addNotes', notes=notes)
    print(f'\n写入结果：成功 {sum(1 for r in res if r)} / {len(res)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
