# -*- coding: utf-8 -*-
"""追加 D017 复检 3 条日志。"""
import io
import json
import os

LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   '备考计划', '学习日志.jsonl')

entry = {
    "date": "2026-10-22",
    "subject": "C语言",
    "kind": "quiz",
    "title": "D017 复检 3 条（D010 do-while vs while · D014 全局vs局部 · D016 循环自增）—— 结论 3/3 全对，D014 理由第 2 次同型降级",
    "score": "D010：`do{s+=i;i++;}while(i<0)` 答 `0 1` ✅；换成 `while(i<0)` 答 `0 0` ✅；理由「do-while 至少执行 1 次、条件放后面；while 可能一次都不执行、条件放前面」**全对** → 清账。\nD014：答 `21 10` ✅；理由「改的是盒子里的 x，出来这个 x 就销毁了，不会影响到 main 里的」—— 结论对、机制半对 → 理由降级。\nD016：`while(i++ < 3) s += i` 答 `6 4` ✅；理由「`i++` 先拿原值比较，比较完 i 再加 1」**全对** → 清账。",
    "mastery": "partial",
    "weak": "**D014 理由第 2 次同型错**（前一次是 D013 形参实参）。学生把「函数返回时局部变量销毁」当成「外层 x 不变」的原因。真正的机制是**同名遮蔽**：`f` 里那行 `int x = 20;` 有**类型名 `int`** ⇒ 造了一个**新盒子**，名字也叫 x，它**挡住了**外面的全局 x；编译器找名字「由内向外、找到就停」，一进 `f` 就看见内层 x，压根不会往外看。所以 `x++` 加的是新盒子的 1，**外面的全局 x 从头到尾没被碰过** —— 哪怕 `f` 永不返回，它也还是 10。「销毁」只解释「出函数找不到 x」，不解释「x 不变」。",
    "note": "【与 D013 的区别（必须分清，学生已混两次）】D013 是**值传递**：调用那一瞬间把实参的值**抄一份**塞进形参盒子，两个盒子从出生就是两个。D014 是**遮蔽**：函数里自己用 `int` 造了个同名盒子。共同点是「两个盒子」，区别是「谁造的」—— 一个是外面抄进来的，一个是里面自己造的。\n【当场验证】讲完立刻给对照题：把 `int x = 20;` 改成 `x++;`（去掉 `int`），问输出。正确答案 `11 11`。判据一句话：**有类型名 = 造新盒子（遮蔽）；没类型名 = 用外面那个（真改）**。\n【讲法来源】「有无类型名 = 有没有造新盒子」是 3.7 作用域时立住的抓手，学生当时四样本首次全对，本次复用它纠 D014。\n【判分口径】3 条结论全对，2 条 🟢（D010 / D016）、1 条 🟡（D014，理由降级，明天重排一次）。"
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
