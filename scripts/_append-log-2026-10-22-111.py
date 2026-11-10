# -*- coding: utf-8 -*-
"""追加 1.11 首讲日志。"""
import io
import json
import os

LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   '备考计划', '学习日志.jsonl')

entry = {
    "date": "2026-10-22",
    "subject": "C语言",
    "kind": "lecture",
    "title": "1.11 首讲 · 三道闸门（编译/链接/运行）+ 两道题 —— 首答掉坑（判 .obj 生成不了）→ 补讲「声明=报名表」→ 验证答对",
    "score": "按密度上限给「1 个机制 + 1 组记号 + 1 道题」，用三道闸门图讲。\n题 1（有声明无定义的 `hello`）：问能否生成 `.obj`、能否生成 `.exe`。学生答「**生成不了 .obj**」❌ —— 掉进「编译成功但链接失败」这个坑。\n补讲后题 2（把声明那行删掉，问错误类型变不变）：答「**删掉就生成不了 .obj 了**」✅ 正确。",
    "mastery": "partial",
    "weak": "首答把「链接错误」判成「编译错误」。根因：**没有把 3.4「声明 vs 定义」接到「编译 vs 链接」两道闸门上** —— 他知道有 `{}` 是定义、无 `{}` 是声明，但不知道「声明只让编译通过、定义才让链接通过」这层因果。",
    "note": "【讲法（关键，留存复用）】**声明 = 报名表上有个名字；定义 = 真的来了个人。编译器只查报名表，链接器才点人头。** 学生问「没解释函数 hello 的作用？」正好指向这一处 —— 首讲只说了「报了名字找不到人」，漏了「编译器凭什么放行」。补上这一句，题 2 立刻答对。\n【完整对照（已给）】有声明无定义 → 编译过、链接错 → `.obj` ✅ / `.exe` ❌；声明删掉 → 编译错 → `.obj` ❌。同一段代码删一行，错误类型从链接跳到编译。\n【真题打点】2026 选择 8「关于编译错误与运行错误，下列说法正确的是」—— 最爱挖的就是「链接错误之前编译是成功的、`.obj` 已生成」。\n【B 站对比（2 分钟轻检查，结论：无分歧，不写对比文件）】`coach check` 报了 7 份讲义，实读 `BV17a7K64ELH_22/23` 发现讲的是二维数组内存布局与 `static`/`extern` 链接属性，不是三种错误专题；其中「`static` 后其他文件报『无法解析的外部符号』」与本讲链接错误口径一致，无更优抓手。笔记自带的「编译查语法、链接找函数、运行看逻辑」已足够紧凑，直接沿用。\n【1.11 剩余未讲】预处理（`#include` / `#define` / 条件编译 —— 考纲新增高频）· VS 调试快捷键（F9/F5/F10/F11）· GDB · 内存泄漏。下一块从预处理起。"
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
