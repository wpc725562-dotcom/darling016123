# -*- coding: utf-8 -*-
"""追加 1.11 预处理/宏 日志。"""
import io
import json
import os

LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   '备考计划', '学习日志.jsonl')

entry = {
    "date": "2026-10-22",
    "subject": "C语言",
    "kind": "quiz",
    "title": "1.11 第二块 · 预处理与宏 —— `#define N 5;` 连分号替换，答「编译错误、不生成 .obj」✅",
    "score": "题目：`#define N 5;` + `int a = N * 2;`，问会怎样、卡哪道闸门。\n过程：学生先问「N 后面会给他替换成 100？」（把上一例的 `100` 串到这题）→ 澄清「是 `5`，而且连分号一起换成 `5;`」→ 给出展开结果 `int a = 5; * 2;` → 学生答「**错误编译？不生成 .obj**」✅ 正确。",
    "mastery": "passed",
    "weak": "",
    "note": "【讲法（留存复用）】**预处理 = 翻译官开工前的抄写员，只会剪贴，不懂 C**。`#include` 是把头文件整段贴进来、`#define` 是把字串原样换掉、`#ifdef` 是看宏定义过没有决定留不留。三个指令共用这一个比喻，不列表格。\n【宏陷阱示例】`#define S(a,b) a*b` → `S(2+3,4)` 展开成 `2 + 3 * 4 = 14`（不是 20），因为抄写员不替人加括号；安全写法 `((a)*(b))`。\n【四个考点可从同一句推出来（不背）】① 在**预处理**阶段处理，不是编译 —— 抄写员在翻译官之前 ② 展开是**纯文本替换、不做语法检查** —— 抄写员不懂语法 ③ 宏**没有类型** —— 抄写员不认类型 ④ 定义**结尾不加分号** —— 分号会被当成替换内容抄进去（本题即是证明）。\n【学生卡点】把「上一个例子的数值 100」当成通用答案 —— 属读题时把示例当规则（与 3.3 首题把 `∫u²du=u³/3` 当公式同型）。同类风险需留意：**例子里的具体数字不能当规则记**。\n【1.11 剩余】VS 调试快捷键（F9/F5/F10/F11）· GDB（真题概率小）· 内存泄漏 —— 快捷键与 GDB 打包成 Anki 速查卡，不占当堂时间。内存泄漏下一块讲（同时是数据结构链表的 `malloc`/`free` 硬前置，全库零记录）。"
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
