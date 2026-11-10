# -*- coding: utf-8 -*-
"""追加 1.11 收尾日志。"""
import io
import json
import os

LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   '备考计划', '学习日志.jsonl')

entry = {
    "date": "2026-10-22",
    "subject": "C语言",
    "kind": "note",
    "title": "1.11 收尾 · 速查卡交付（VS 快捷键 / GDB / 内存泄漏），12 张 Anki 卡脚本就绪待写入",
    "score": "速查卡四块：① **VS 快捷键**（F9 断点 · F5 启动/继续 · F11 逐语句进函数 · F10 逐过程不进 · Shift+F11 跳出 · Shift+F5 停止）② **调试窗口**（监视可看可改 / 自动窗口 / 局部变量 / 调用堆栈 / 内存）③ **GDB 九步**（`gcc -g` → `gdb a` → `b` → `r` → `n`/`s` → `p` → `set var` → `c` → `q`）④ **内存泄漏三问**（是什么 / 用 valgrind 或 `_CrtDumpMemoryLeaks()` 查 / 归运行时错误）。",
    "mastery": "na",
    "weak": "",
    "note": "【为什么不当堂讲】VS 快捷键与 GDB 是纯记忆内容、真题概率低（2026 仅选择 8 一处，考的是三种错误分类），占用当堂时间性价比低 ⇒ 打包成速查卡 + Anki 卡。\n【卡片脚本】`knowledge/anki_cards/_add-1.11-debug-cards-2026-10-22.py`，12 张，牌组 `专升本::C语言::知识点`，笔记类型「问答题」，字段 `正面`/`背面`。其中 4 张是今天讲的核心（链接错误前 `.obj` 已生成 · 声明无定义报链接错误 · `#define N 5;` 连分号替换 · `S(2+3,4)=14`），4 张 VS 快捷键，2 张 GDB，2 张内存泄漏判断题。\n【待执行】Anki 当前未启动（`collection.anki2` mtime 停在 02:19，AnkiConnect 无响应）⇒ 脚本支持 `--apply`，学生打开 Anki 后一条命令即写入。\n【易错点留存】「GDB 只能调试带 `-g` 的程序」是 ×，没 `-g` 也能开、只是退化成汇编级单步；「程序正常结束 = 没泄漏」也是 ×，泄漏在运行期一直在，进程退出才被 OS 整体回收。\n【1.11 完成度】三道闸门 ✅ · 预处理与宏 ✅ · 内存泄漏 ✅ · 速查卡交付 ✅。**C 语言 1.1–1.11 主干至此全部走完**（1.8 还剩第 8 课函数指针与 3.7 动态内存的正式讲次，今天以 1.11 内存泄漏名义补了 malloc/free 的核心）。"
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
