# -*- coding: utf-8 -*-
"""2022 完形 31/32/33 对仗组 · 2 张判据卡

用法：
  python _add-cloze-duizhang-cards-2026-10-23.py --apply
"""
import sys
import urllib.request
import json

ANKI = 'http://127.0.0.1:8765'
DECK = '专升本::英语::错题'
MODEL = '问答题'

CARDS = [
    ("完形里一组**对仗**（同一句或相邻句里两个以上空、`and / while / however` 两侧结构对称）填完了，怎么验对错？",
     "**把两半连起来读，必须读成一句完整的「甲这样 ↔ 乙那样」。读不成对照，就是错。**<br><br>"
     "2022 第 31 / 32 / 33 空：<br>"
     "`If you are a <u>31</u>, you will be able to maintain constant speed with <u>32</u> hand. "
     "Men, however, when tapping with their left hand will <u>33</u> down.`<br><br>"
     "❌ 我填的 `right` + `shut`，连起来读：<br>"
     "「如果你是女人，你能用右手保持匀速。然而男人用左手敲时会<b>关闭</b>。」<br>"
     "→ 这不是对照，是<b>断裂</b>。<br><br>"
     "✅ 正解 `either` + `slow`，连起来读：<br>"
     "「女人<b>两只手都行</b>；然而男人只有右手行，<b>左手会掉速</b>。」<br>"
     "→ 对照成立。<br><br>"
     "📌 用这条判据验 32 的四个选项，一次排掉三个：<br>"
     "`right` → 女人只有右手行，男人右手也行 ⇒ 男女一样，`however` 没东西可反转 ✗<br>"
     "`neither` → 女人两只都不行 ⇒ 比男人还差，`however` 更不成立 ✗<br>"
     "`left` → 女人只有左手行 ⇒ 与男人正相反，但原文零依据 ✗<br>"
     "`either` → 女人两只都行 ↔ 男人只有右手行 ✓",
     ['英语', '完形', '判据', '对仗', '真题2022']),

    ("完形里填**对比项**（`however / but / while / unlike` 前后那一空），选词的第一条限制是什么？",
     "**必须和原文说的是同一个维度。速度 ↔ 速度，开关 ↔ 开关，不许换维度。**<br><br>"
     "2022 第 33 空：`Men, however, when tapping with their left hand will <u>33</u> down.`<br>"
     "前文说的维度是 `maintain constant speed` —— <b>速度</b>。<br><br>"
     "✅ `slow down` ＝ 速度降下来 → <b>同维度</b><br>"
     "❌ `shut down` ＝ 停机／关闭 → <b>开关维度</b>，换了维度<br><br>"
     "⚠️ 我选 `shut` 的原因是「`shut down` 是个熟搭配」。<b>搭配熟 ≠ 维度对。</b><br><br>"
     "📌 补一条：`shut down` 的主语一般不是人做小动作 —— 机器 / 公司 / 系统才 shut down，"
     "人敲桌子不会 shut down。",
     ['英语', '完形', '判据', '同维度', '真题2022']),
]


def invoke(action, **params):
    payload = json.dumps({'action': action, 'version': 6, 'params': params}).encode()
    req = urllib.request.Request(ANKI, payload, {'Content-Type': 'application/json'})
    data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode())
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
        print(f'  {i}. {f[:46]}')
    if not apply:
        print('\n[试运行] 加 --apply 才真写入')
        return 0

    res = invoke('addNotes', notes=notes)
    print(f'\n写入结果：成功 {sum(1 for r in res if r)} / {len(res)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
