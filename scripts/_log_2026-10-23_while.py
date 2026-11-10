# -*- coding: utf-8 -*-
"""追加 278 条：1.5 第一课 while 循环（补 D002 欠账）"""
import json, io

LOG = r'D:/deeepseek/zhuan-sheng-ben-notes/备考计划/学习日志.jsonl'

entry = {
    "date": "2026-10-22",
    "subject": "C语言",
    "kind": "lecture",
    "title": "1.5 第一课 while 循环 · 补 D002 欠账（日志此前从「第三课 do-while」才有记录，前两课零记录）",
    "score": "",
    "mastery": "learning",
    "weak": (
        "**D002 卡上标的「循环第 5 章缺 3 节」实际是哪 3 节，本轮查清**：\n"
        "· 1.5 一、while 循环 —— 零 lecture 记录\n"
        "· 1.5 二、while 配套（易错点）—— 零 lecture 记录\n"
        "· 1.5 六、goto 语句 —— 零 lecture 记录\n"
        "日志最早一条 1.5 是第 50 条「第三课 do-while」，**前两课直接跳过**。\n"
        "**goto 判定为「已知缺口 · 低优先级 · 暂不讲」** —— 2022/2024/2026 三年真题零出现，与「8.4 傅里叶级数可能多余」同一判据。"
    ),
    "note": (
        "【教学抓手：不做并列规则表，做「顺序对照」】\n"
        "学生已会 do-while，所以 while 不按新课讲，按**对照**讲。核心只有一句：**判断和循环体谁在前。**\n"
        "· while：① 判断 → ② 循环体（真才进去，假就跳过）\n"
        "· do-while：① 循环体 → ② 判断（先做一次，再决定）\n"
        "**唯一分歧点：条件一开始就是假的时候。** while 做 0 次，do-while 做 1 次。这就是 do-while 存在的唯一理由。\n\n"
        "【逐格账本（$1+2+\\cdots+5$）】\n"
        "| 轮 | 判断 $i\\le5$ | 真假 | 执行后 $sum$ | 执行后 $i$ |\n"
        "| 1 | $1\\le5$ | 真 | 1 | 2 |\n"
        "| 2 | $2\\le5$ | 真 | 3 | 3 |\n"
        "| 3 | $3\\le5$ | 真 | 6 | 4 |\n"
        "| 4 | $4\\le5$ | 真 | 10 | 5 |\n"
        "| 5 | $5\\le5$ | 真 | 15 | 6 |\n"
        "| 6 | $6\\le5$ | **假** | 不动 | 不动 |\n"
        "输出 $sum=15$，退出时 $i=6$。\n"
        "**关键结论：判断次数 = 循环次数 + 1。第 6 轮判断了，但没执行循环体。**\n\n"
        "【分号陷阱】`while (i <= 5);` —— 分号把循环体换成空语句 ⇒ $i$ 永不改变 ⇒ 死循环。\n"
        "这是 2022 单选 11 `int z=2; while(z--); printf(\"z=%d\",z);` 的考点。\n\n"
        "【布置的题（2024 单选 9 真题）】`int a = 1; while (a < 4) printf(\"%d\", a++);` 输出？\n"
        "答案 123。要求逐格写出每轮 $a$ 的值与输出。\n\n"
        "【真题依据（笔记 1.5 章）】2022 单选 11 · 2024 判断 6（「while 退出方式只有条件为假」—— 错，还有 break/return/goto）· "
        "2024 单选 9 · 2026 选择 6。**while 相关三年共 7 处标签，2024 占 5 处。**"
    ),
}

with io.open(LOG, 'a', encoding='utf-8', newline='\n') as f:
    f.write(json.dumps(entry, ensure_ascii=False) + '\n')

with io.open(LOG, 'r', encoding='utf-8') as f:
    n = sum(1 for _ in f)
print('appended -> line', n)
