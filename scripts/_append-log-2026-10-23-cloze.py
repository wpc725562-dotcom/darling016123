# -*- coding: utf-8 -*-
"""追加 2022 完形日志（3/10，说明文体超纲）。"""
import io
import json
import os

LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   '备考计划', '学习日志.jsonl')

entry = {
    "date": "2026-10-23",
    "subject": "英语",
    "kind": "quiz",
    "title": "2022 完形填空 · 12 分钟只做到第 10 空，3/10 —— 说明文体超出当前水平，不是退步",
    "score": "学生作答（第 21–30 空，后面主动停手「完全没头绪」）：21 C ❌ · 22 A ❌ · 23 B ❌ · **24 A ✅** · 25 D ❌ · 26 C ❌ · **27 A ✅** · **28 D ✅** · 29 B ❌ · 30 D ❌。\n正确率 3/10。**做对的 3 题全是「词义直接匹配」型**（communicative↔emotional 并列、differently、behave）；**做错的 7 题全是「需要看上下文结构」型**。",
    "mastery": "failed",
    "weak": "**不是词汇问题，是篇章结构问题。** 这篇的答案高度依赖三类信号，学生一个都没用：① **逻辑连接词**（第 2 段开头 `But two books newly published say...` 是论点反转，21 应 `result`〔旧观点：差异是教养的结果〕、26 应 `exist`〔新观点：差异存在〕）② **对仗结构**（22/23：`women can be trained to do <b>jobs</b> that men traditionally do, and men can and should do more <b>housework</b>` —— 女人做男人的工作 ↔ 男人做家务，两空互为镜像）③ **语法结构**（21 的 `the ___ of` 要求名词，29 的 `read a ___ aloud from a book` 要求「一段文字」= passage，不是 word）。",
    "note": "【关键对比（必须记，避免误判学生水平）】2024 完形（**记叙文**，讲一个老师的故事）09-25 做过 **13/15**；2022 完形（**说明文**，讲男女大脑差异 + 双观点 + 实验论证）今天 **3/10**。**同一个学生，同一科，差 10 个空。差的是文体，不是能力。** ⇒ 后续完形按「记叙文 → 应用文 → 说明文」递进，说明文等篇章能力上来再碰。\n【说明文骨架（本次交付的抓手，留存复用）】这篇四段是标准说明文结构：① 第 1 段 = **旧观点**（`psychologists have made us believe that...`）② 第 2 段 = **But + 新观点**（`But two books newly published say that...`）③ 第 3 段 = **实验证据**（`Try this experiment`）④ 第 4 段 = **总结回指**（`This is one of the many experiments that prove...`，34 应 `experiments`）。抓住这个骨架，21/26/34 三空直接出来。\n【学生反应】主动停手并说明「完全没头绪」，不是放弃 —— 12 分钟到了只做到第 10 空，剩余 31–35 空未做。停手是对的，硬做下去只会乱填。\n【今天英语总量】Anki 99 张（语境词 51 + 核心高频 29 + 写作词 18 + 语法 1）· 2024 Passage B 2/4 · 2022 完形 3/10 · 建卡 3 陷阱 + 7 生词 = 10 张。\n【待办】说明文完形先放下；下一次完形选**记叙文或应用文**（如 2023 或 2025 篇，需先查文体）。"
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
