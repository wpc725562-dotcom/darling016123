# -*- coding: utf-8 -*-
"""D017 中途报数快照（18:40）—— 回应学生「今天学习了多久 今天英语还没学 anki也没完成」"""
import io, json

PATH = r'D:/deeepseek/zhuan-sheng-ben-notes/备考计划/学习日志.jsonl'

rows = [
    {
        "date": "2026-10-23",
        "subject": "综合",
        "kind": "audit",
        "title": "D017 学习日中途报数（截至 18:40）—— 有效学习 3h09m，Anki 0 张，英语 0 条",
        "score": "",
        "mastery": "n/a",
        "weak": "学生自己判断「英语还没学、Anki 没完成」属实，不是错觉。今日 15:29–18:38 连续 3h09m 全在数据结构和 3.5，Anki 一张未刷、英语零记录。",
        "note": (
            "取证：scripts/_study_time_v2.py \"2026-10-23 13:00\" \"2026-10-23 18:40\" "
            "→ Anki 复习事件 0 条 · 会话消息 115 条 · 有效学习 1 段 15:29→18:38 = 3h09m（无 >30min 断档）。"
            "交叉验证 AnkiConnect getNumCardsReviewedToday = 0，getCollectionStatsHTML = \"No cards have been studied today\"。"
            "\\n\\n"
            "【关键归属】凌晨 00:45–03:42 的 2h57m（Anki 209 条）属于 **D016 学习日**，不是今天。"
            "今天英语的 6 条记录（2024 阅读 Passage B / 2022 完形 ×2 / 假阴性更正 / D016 对账）全部落在该时段。"
            "学生若觉得自己「今天学过英语」，是把 D016 的账记到了 D017 头上 —— 学习日边界（13:00→次日04:00）必须再强调一次。"
            "\\n\\n"
            "【今日已做】数据结构 17 条记录（2.1/2.2/2.3 三节 + 记忆恢复包 + 重讲两块地基）；高数 22 条记录（3.5 三型去根号 + 三角六函数 + dx 打通 + d/∫ 纠错）。"
            "\\n\\n"
            "【Anki 欠账快照】叶子牌组加总 120 张：英语 92（1-核心高频 rev18 / 语境词 new7+rev36 / 语法 new10+rev1 / 写作词 rev7 / 错题 new13）；"
            "C语言 24（知识点 rev1+lrn9 / 错题 rev14）；高数 3；计算机基础 1。估算 22–28 分钟，正好一个「最小任务 25 分钟」。"
            "\\n\\n"
            "【隐藏欠账】今日 39 条学习记录里，2.1/2.2/2.3/3.5 的知识点**全部没有转成 Anki 卡**（知识点牌组今日仅 rev1）。"
            "学完即忘的风险实打实存在，明天需补建卡。"
        ),
    }
]

with io.open(PATH, 'a', encoding='utf-8') as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

with io.open(PATH, encoding='utf-8') as f:
    n = sum(1 for line in f if line.strip())
print('已追加', len(rows), '条，当前总行数', n)
