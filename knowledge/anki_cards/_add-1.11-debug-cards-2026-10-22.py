# -*- coding: utf-8 -*-
"""1.11 调试速查卡 · 12 张（VS 快捷键 / GDB / 内存泄漏 / 三道闸门 / 宏陷阱）

用法：
  python _add-1.11-debug-cards-2026-10-22.py          试运行，只打印
  python _add-1.11-debug-cards-2026-10-22.py --apply  真写入
"""
import json
import sys
import urllib.request

ANKI = 'http://127.0.0.1:8765'
DECK = '专升本::C语言::知识点'
MODEL = '问答题'

CARDS = [
    # —— 三道闸门（今天首讲，掉过坑）——
    ("链接错误发生之前，编译是成功的吗？`.obj` 生成了吗？",
     "**编译是成功的，`.obj` 已经生成。**<br><br>"
     "编译器只查「名字表」，不看函数身体在不在。<br>"
     "链接器才去找身体 —— 找不到就报「无法解析的外部符号」。<br><br>"
     "⚠️ 这是 2026 选择 8 最爱挖的坑：**看到链接错误，说明 `.obj` 已经有了**。",
     ['1.11', '三道闸门', '高频']),

    ("函数只写了声明 `void hello(void);` 却没写函数体，会报什么错？",
     "**链接错误**（不是编译错误）。<br><br>"
     "声明 = 报名表上有个名字 → 编译器放行 → `.obj` 生成。<br>"
     "定义 = 真的来了个人 → 链接器点人头 → 找不到 → `.exe` 生成失败。<br><br>"
     "**声明只让编译通过，定义才让链接通过。**",
     ['1.11', '三道闸门', '声明vs定义']),

    ("`#define N 5;` 之后写 `int a = N * 2;`，展开成什么？报什么错？",
     "展开成 **`int a = 5; * 2;`**<br><br>"
     "抄写员把 `N` 换成 `5;`，**连分号一起**。<br>"
     "`int a = 5;` 已是完整语句，剩下的 `* 2;` 没有左操作数 → **编译错误，`.obj` 生成不了**。<br><br>"
     "⇒ 宏定义结尾**不能加分号**。",
     ['1.11', '预处理', '宏', '高频']),

    ("`#define S(a,b) a*b`，那么 `S(2+3, 4)` 等于多少？",
     "**14**，不是 20。<br><br>"
     "展开成 `2 + 3 * 4` → 先乘后加 = 14。抄写员**不会替你加括号**。<br>"
     "安全写法：`#define S(a,b) ((a)*(b))`",
     ['1.11', '预处理', '宏', '陷阱']),

    # —— VS 快捷键 ——
    ("Visual Studio 里设置 / 取消断点的快捷键是？", "**F9**", ['1.11', 'VS', '快捷键']),

    ("VS 里 **F10** 和 **F11** 有什么区别？",
     "**F10 = 逐过程**：把整个函数当一步走完，**不进函数内部**。<br>"
     "**F11 = 逐语句**：一句一句往里钻，**会进入函数内部**。<br><br>"
     "想看清函数里发生了什么 → F11；只想跨过这行 → F10。",
     ['1.11', 'VS', '快捷键', '高频']),

    ("VS 里「开始调试」和「继续到下一个断点」是同一个键吗？",
     "**是，都是 F5。**<br>"
     "没在调试时按 F5 = 启动调试；调试暂停时按 F5 = 继续跑到下一个断点。<br><br>"
     "配套：`Shift+F11` 跳出当前函数 · `Shift+F5` 停止调试。",
     ['1.11', 'VS', '快捷键']),

    ("VS 的「调用堆栈」窗口看的是什么？",
     "**函数调用的层级关系** —— 谁调了谁，一层层往上排。<br><br>"
     "程序崩在深处时，靠它看「我是从哪条路走到这里的」。",
     ['1.11', 'VS', '调试窗口']),

    # —— GDB ——
    ("用 GDB 调试，编译时要加什么参数？不加会怎样？",
     "加 **`-g`**：`gcc -g a.c -o a`<br><br>"
     "`-g` 生成调试信息。不加也能用 GDB 打开，但**看不到源码行号和变量名**，退化成汇编级单步。",
     ['1.11', 'GDB', '高频']),

    ("判断：「GDB 只能调试带 `-g` 参数编译的程序。」",
     "**×**<br><br>"
     "没 `-g` 也能用 GDB 打开，只是看不到源码行号与变量名、退化为汇编级单步。<br>"
     "「只能」太绝对。正确说法：**带 `-g` 才能做源码级调试**。",
     ['1.11', 'GDB', '判断题', '陷阱']),

    # —— 内存泄漏 ——
    ("内存泄漏用什么工具检测？属于哪一类错误？",
     "**检测**：`valgrind`（Linux）；VS 用诊断工具或 `_CrtDumpMemoryLeaks()`。<br>"
     "**归类**：**运行时错误** —— 编译能过、链接能过，跑起来才出事。<br><br>"
     "避免：`malloc` 与 `free` 成对，**每一个出口路径都要 free**。",
     ['1.11', '内存泄漏', '运行时错误']),

    ("判断：「程序正常运行结束，就一定没有内存泄漏。」",
     "**×**<br><br>"
     "泄漏在运行期间**一直存在**，只是进程退出时被操作系统**整体回收**了 —— 那是善后，不是没漏。<br>"
     "程序不崩、结果也对 ≠ 没泄漏。",
     ['1.11', '内存泄漏', '判断题', '陷阱']),
]


def invoke(action, **params):
    payload = json.dumps({'action': action, 'version': 6, 'params': params}).encode()
    req = urllib.request.Request(ANKI, payload, {'Content-Type': 'application/json'})
    data = json.loads(urllib.request.urlopen(req, timeout=20).read())
    if data.get('error'):
        raise RuntimeError(f'{action}: {data["error"]}')
    return data['result']


def main():
    apply = '--apply' in sys.argv
    try:
        decks = invoke('deckNames')
    except Exception as e:
        print('AnkiConnect 连不上（Anki 没开？）：', e)
        return 1

    if DECK not in decks:
        print('牌组不存在：', DECK)
        print('现有含「C语言」的牌组：', [d for d in decks if 'C语言' in d])
        return 1

    notes = [
        {
            'deckName': DECK,
            'modelName': MODEL,
            'fields': {'正面': front, '背面': back},
            'tags': tags,
            'options': {'allowDuplicate': False, 'duplicateScope': 'deck'},
        }
        for front, back, tags in CARDS
    ]

    print(f'准备写入 {len(notes)} 张 → {DECK}')
    for i, (front, _, _) in enumerate(CARDS, 1):
        print(f'  {i:2}. {front[:46]}')

    if not apply:
        print('\n[试运行] 加 --apply 才真写入')
        return 0

    res = invoke('addNotes', notes=notes)
    ok = sum(1 for r in res if r)
    print(f'\n写入结果：成功 {ok} / {len(res)}')
    for i, r in enumerate(res, 1):
        if not r:
            print(f'  第 {i} 张失败（可能重复）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
