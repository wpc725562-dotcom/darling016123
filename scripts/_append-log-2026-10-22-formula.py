# -*- coding: utf-8 -*-
"""追加 3.2 公式表补完日志。"""
import io
import json
import os

LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   '备考计划', '学习日志.jsonl')

entry = {
    "date": "2026-10-22",
    "subject": "高数",
    "kind": "quiz",
    "title": "3.2 基本积分公式表补完 · 「求导表倒着读」机制 + 三题全对（含负号坑）",
    "score": "机制：积分表不是新表，是 2.3 求导表**倒着读**。示范两条（`∫1/x dx = ln|x|+C` 说明绝对值来由 · `∫eˣdx = eˣ+C` 指出它是唯一「自己就是自己原函数」的函数），其余让学生自己倒。\n三题手写作答（附图）：① `∫cos x dx = sin x + C` ✅ ② `∫sin x dx = -cos x + C` ✅（负号没丢，这是本题唯一坑）③ `∫1/(1+x²)dx = arctan x + C` ✅ —— **3/3 全对，一次过**。\n补完剩余三条：`∫aˣdx = aˣ/ln a + C`（强调是除不是乘）· `∫sec²x dx = tan x + C` · `∫1/√(1-x²)dx = arcsin x + C`。九条齐。",
    "mastery": "passed",
    "weak": "",
    "note": "【讲法（关键，留存复用）】**积分表 = 求导表倒着读**，不是另背一张表。正着读「$x^2$ 求导得 $2x$」，倒着读「什么求导得 $2x$？$x^2$」。九条公式不是九个知识点，是**同一个动作做了九次** —— 这样讲避免了并列规则表（学生对该形式无效）。\n【前置确认（出题前查过）】2.3 求导表覆盖 12 条：`C` / `xⁿ` / `1/x` / `√x` / `sin` / `tan` / `eˣ` / `aˣ` / `ln` / `log_a` / `arcsin` / `arctan` —— 全部学过，所以「倒着读」不违反铁律。\n【事实更正】此前我在看板与 MEMORY 里写「3.2 公式表只有幂函数一行」，易被理解成资料缺失。实际**笔记 `3.2-直接积分法.md` 的表是完整的 9 条**，缺的是「讲过并验过的只有幂函数与常数 k」。是教学缺口，不是资料缺口。\n【绝对值说明】`∫1/x dx = ln|x| + C` 的绝对值不是装饰：`(ln x)'=1/x` 只在 `x>0` 成立，而 `1/x` 在负数侧也有定义 ⇒ 必须写 `|x|`。\n【下一步】3.4 第二类换元法之根式代换（`t = √[n]{ax+b}` 去根号）。"
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
