# -*- coding: utf-8 -*-
"""追加 D014 当场修复验证日志。"""
import io
import json
import os

LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   '备考计划', '学习日志.jsonl')

entry = {
    "date": "2026-10-22",
    "subject": "C语言",
    "kind": "quiz",
    "title": "D014 当场修复验证 · 去掉 int 的对照题答 `11 11`，遮蔽判据立住",
    "score": "对照题（把 `int x = 20;` 改成裸 `x++;`）：输出答 **`11 11`** ✅。理由「这里不是定义 x，没用 int，而是直接使用了 x，不是新建变量，直接用外面那一个全局 x，修改会同步生效」—— **结论与机制全对**。",
    "mastery": "passed",
    "weak": "",
    "note": "【判据已立住】「**有类型名 = 造新盒子（遮蔽）；没类型名 = 用外面那个（真改）**」这一句他这次自己完整说出来了，而且是主动用「不是新建变量」来对照上一题。\n【与前一次的差别】原题他给的是「改的是盒子里的 x，出来这个 x 就销毁了」—— 方向对、因果接错；对照题他把因果接正了（不是「销毁所以没影响」，是「压根没碰过外面那个」）。\n【判分】D014 由 🟡 升为**同场次通过**，仍按规矩记 🟡（跨日复检过了才 🟢），明天 D018 再排一次即可升。\n【讲法留存】区分两类「两个盒子」：D013 值传递 = 外面抄一份进来；D014 遮蔽 = 里面自己造一个。共同点是两个盒子，区别是**谁造的**。"
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
