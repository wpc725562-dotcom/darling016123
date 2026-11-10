# -*- coding: utf-8 -*-
"""追加 2024 Passage B 阅读日志。"""
import io
import json
import os

LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   '备考计划', '学习日志.jsonl')

entry = {
    "date": "2026-10-23",
    "subject": "英语",
    "kind": "quiz",
    "title": "2024 真题阅读 Passage B · 限时 8 分钟（树天花板）—— 2/4，同义替换已会，新问题是「抓词不抓句子角色」",
    "score": "**6 ✅**（C. It shortens their attention span）：定位句准确抄出 `It makes their concentration span (持续时间) shorter.`，并自己指出 `concentration span → attention span` 是同义替换 —— **昨天卡的那个点，今天通了**。\n**7 ✅（答案对，定位错）**：选 D `printing tree photos onto the ceiling` 正确，但抄的依据句是 `he planned to print pictures of trees onto curtains` —— 那是**被否决的方案**。正确依据是 `However, his colleagues reminded him that curtains would take up the wall space` + `Then he got them printed onto the ceilings`。\n**8 ❌**（答 A. better sense of beauty，应 B. increased attendance）：依据句抄的是 Dave 的 `It is pretty great and beautiful`。但题干是 `The change of the classrooms **led to** the students' ______`，问**因果结果**；Dave 那句是**个人感受**，不是结果。答案句是 Hayden 的 `Overall, the class attendance has gone up`。\n**9 ❌**（答 B. Shocked，应 A. Favorable）：依据句抄的是 `It is surprising to see trees here.`。但 attitude 题问**整体评价**，`surprising` 只是第一句的情绪，后面还有 `pretty great and beautiful` 与 `feels like I am sitting under a tree`（舒适）⇒ 整体正面。",
    "mastery": "partial",
    "weak": "**统一病根：把「词对上了」当成「意思对上了」—— 只看单个词，不看那句话在段落里担任什么角色。** 三处同型：① 第 7 题只读到 `planned to print ... curtains`，没读到紧跟的 `However` 已把 curtains 方案否决 ② 第 8 题抓到 `beautiful` 就选 `beauty`，没看题干 `led to` 要的是**结果**而非**感受** ③ 第 9 题抓到 `surprising` 就选 `Shocked`，没看态度题要的是**整段评价**而非**某一句的情绪**。",
    "note": "【进展（必须记）】昨天 Passage A 的主缺口是「找不到同义替换」，今天第 6 题**主动说出** `concentration span → attention span` —— 该缺口已补。这是本周英语最实质的一次进步。\n【昨天立的规律今天被验证 3 次】**选项里照抄原文词（或原词根/近义词）的往往是陷阱**：第 8 题 A 的 `beauty` ↔ 原文 `beautiful`（错）；第 9 题 B 的 `Shocked` ↔ 原文 `surprising`（错）；第 7 题 B 的 `green curtains` ↔ 原文 `curtains`（错）。三条全中，规律成立，但他尚未建立「看到原词先警惕」的动作。\n【讲法（留存复用）】三个路标词：① `However / But` 后面才是真答案，前面是被否决的方案 ② `Overall / In short` 后面常是总结性答案（第 8 题的 attendance 就在 Overall 后面）③ 态度题看**整段**，把描述性词归到「正面 / 负面 / 中立」三档，不选「最像某个词」的。\n【源文件 bug（未修，待学生定）】`docs/posts/english/2024-英语-刷题版.md` 把**第 5 题（Holiday Farm 门票）放在 `### Passage B` 标题之后**，但它属于 Passage A（农场文）。真实结构是 A 5 题 + B 4 题 + C 6 题 = 15 题。未改动该文件（学习资料默认只读）。\n【待办】完形 1 篇（D016 顺延）· 第 7/8/9 三题的同义替换对建 Anki 卡。"
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
