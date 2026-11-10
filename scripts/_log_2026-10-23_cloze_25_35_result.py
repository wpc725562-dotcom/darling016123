# -*- coding: utf-8 -*-
"""追加 268 条：2022 完形余 7 空作答结果 5/7"""
import json, io

LOG = r'D:/deeepseek/zhuan-sheng-ben-notes/备考计划/学习日志.jsonl'

entry = {
    "date": "2026-10-23",
    "subject": "英语",
    "kind": "quiz",
    "title": "2022 完形余 7 空（25/30/31/32/33/34/35）—— 5/7，反转信号已建立，对仗组内两个空仍错",
    "score": (
        "学生作答：25 A `published` ✅ · 30 A `keep` ✅ · 31 B `woman` ✅ · **32 D `right` ❌**（应 A `either`）· "
        "**33 D `shut` ❌**（应 C `slow`）· 34 C `experiments` ✅ · 35 B `abilities` ✅。\n"
        "**5/7**。这 7 空我上一轮全部只给指路未给答案 ⇒ 是首次独立完成。对比今天早些时候整篇 3/10，是真进步。"
    ),
    "mastery": "partial",
    "weak": (
        "**两个错同属第 31/32/33 这一组对仗，且都是「用词面配对代替结构对照」。**\n"
        "· 32 答 D `right`：原文出现 `men ... with their left hand`，`left` 在场，于是选镜像词 `right`。这是**词面配对**，不是判据。\n"
        "· 33 答 D `shut`：`shut down` 是熟搭配，于是选它。但前文 `maintain constant speed` 是**速度**维度，反义必须同维度 ⇒ `slow down`。`shut down` 是「停机/关闭」，属**开关**维度。\n"
        "· 两个错合起来读：「如果你是女人，你能用右手保持匀速。然而男人用左手敲时会关闭。」—— 这不是对照，是断裂。"
    ),
    "note": (
        "【已建立的（必须记，别再说他没进步）】\n"
        "31 答 B `woman` 全对，依据是 `Men, however` 这个反转信号 —— **10-23 上午交付的「路标词」动作，在完形里第一次被独立用对**（此前只在阅读 Passage B 第 7 题用过一次且用错）。\n"
        "34 答 C `experiments` 全对 —— `This is one of the many ___` 的回指，说明**骨架意识开始起作用**。\n"
        "25 答 A `published` 全对 —— 我给的指路只有一句「书跟 `according to a recent scientific study` 什么关系」，他自己接上了。\n\n"
        "【本次新增判据（今天第二个可带走的）】\n"
        "**对仗组验收标准：一组对仗填完，把两半连起来读，必须是一句完整的「甲这样 ↔ 乙那样」。读不成对照，就是错。**\n"
        "用它验 32 的四个选项：\n"
        "· `right` → 女人只有右手行，男人右手也行 ⇒ 男女一样，`however` 没东西可反转 ⇒ ×\n"
        "· `neither` → 女人两只都不行，比男人更差 ⇒ `however` 也不成立 ⇒ ×\n"
        "· `left` → 女人只有左手行 ⇒ 与男人正好相反，但原文没有任何依据 ⇒ ×\n"
        "· `either` → 女人两只都行 ↔ 男人只有右手行 ⇒ 对照成立 ⇒ ✓\n"
        "**一个判据排掉三个选项**，与陶然「正负态度一排除，C 绝对不能选」同型。\n\n"
        "【第二个判据：对比项必须同维度】\n"
        "`maintain constant speed`（速度）↔ 反义必须是速度维度（`slow down`），不是开关维度（`shut down`）。\n"
        "补充：`shut down` 的主语通常不是人做小动作 —— 机器/公司/系统才 shut down，人敲桌子不会 shut down。\n\n"
        "【纪律执行情况】\n"
        "我要求交三样（答案 · 依据句 · 题型标签），学生只交了答案。**未追究，但下一轮必须补标签** —— 陶然那套的地基是「先判题型」，只对答案等于跳过了唯一要练的动作。\n\n"
        "【待办】① 补 32/33 的题型标签与依据句 ② 建 Anki 卡：对仗组验收判据 + 同维度判据（2 张）③ 整篇 15 空正确率重算（原 3/10 + 本次 5/7 ⇒ 累计 8/15）"
    ),
}

with io.open(LOG, 'a', encoding='utf-8', newline='\n') as f:
    f.write(json.dumps(entry, ensure_ascii=False) + '\n')

with io.open(LOG, 'r', encoding='utf-8') as f:
    n = sum(1 for _ in f)
print('appended -> line', n)
