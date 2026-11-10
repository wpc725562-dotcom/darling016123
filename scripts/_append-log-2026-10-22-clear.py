# -*- coding: utf-8 -*-
"""追加 D016 清账日志：高数 Anki 9 张已刷完，D016 零遗留。"""
import io
import json
import os

LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   '备考计划', '学习日志.jsonl')

entry = {
    "date": "2026-10-22",
    "subject": "综合",
    "kind": "summary",
    "title": "D016 清账 · 高数 Anki 9 张已于 02:14–02:15 刷完，D016 零遗留；有效时长 4h17m → 4h20m",
    "score": "直读 `collection.anki2` 的 `revlog` 实证（Anki 已关闭，只读，不依赖 AnkiConnect）：学习日 10-21 15:00 → 10-22 04:00 共 **232 条**复习；其中 **02:13 之后 9 条**全部落在 `专升本::高数::知识点`，时间 02:14:17–02:15:25。该牌组 `total=9 / new=0 / rev=9` —— **9 张全部今天刷完，一张不剩**。数字自洽：223（此前记录）+ 9 = 232。",
    "mastery": "passed",
    "weak": "我上一条汇报说「今天还剩高数 Anki 8 张新卡没刷，是 D016 唯一遗留」—— **错的**。学生在 02:14 就刷完了，我在 02:50 还在按 02:12 的旧快照报账。根因：**我拿「最后一次核对时点」当「现在」**，中间没重新取数就下结论。",
    "note": "【时长修正】末段由 00:56–02:12 延到 **00:56–02:15**（02:12→02:14 断 2 分钟，≤30 分钟不断档）⇒ 末段 1h16m → 1h19m，**D016 有效学习时长 4h17m → 4h20m**。\n【D016 最终清单·全部清零】高数 3.1 ✅ 3.2 ✅ 3.3 ✅ · 计算机 1.10 七块 ✅ + 闭卷默写 ✅ · 英语 2024 Passage A 4/5 ✅ · D016 复检 3 条 ✅ · 类型转换补讲 ✅ · Anki **232 条** ✅ · 建卡 29 张 ✅ · **高数 9 张已刷 ✅**。\n【唯一顺延】完形填空 1 篇未做（当日英语份额被 2024 Passage A 占掉），移到 D017。\n【教训·已升级为纪律】**汇报「还剩什么」之前必须重新取数，不能用几十分钟前的快照。** Anki 这类有独立账本（`revlog`）的科目，一律以账本为准，不以我的记忆或上一轮输出为准。同类风险：看板「仅剩 X」这类句子，写的时候就要标「截至 HH:MM」。\n【顺带查到的库存】`专升本::C语言::知识点` 还剩 **1 张** new 卡；`英语::语境词` 29 new · `英语::语法` 11 new · `英语::错题` 8 new（今日未动，属正常——配额先给高频）。"
}

line = json.dumps(entry, ensure_ascii=False)
existing = io.open(LOG, encoding='utf-8').read()
if entry['title'] in existing:
    print('已存在，跳过')
else:
    with io.open(LOG, 'a', encoding='utf-8', newline='\n') as f:
        f.write(line + '\n')
    print('已追加')
with io.open(LOG, encoding='utf-8') as f:
    print('当前行数:', sum(1 for _ in f))
