# -*- coding: utf-8 -*-
"""追加一条 audit 日志：修正第 146 条「2.5 高阶导数」的节号笔误（应为 2.6）。"""
import json
import io
import os

LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   '备考计划', '学习日志.jsonl')

entry = {
    "date": "2026-10-22",
    "subject": "高数",
    "kind": "audit",
    "title": "修正日志笔误 · 第 146 条「2.5 高阶导数」实为 2.6；2.5 隐函数与参数方程求导全库零记录",
    "score": "逐节核对笔记 `docs/posts/math/notes/` 第二章 13 节（2.1–2.13）：2.5 = 隐函数与参数方程求导方法、2.6 = 高阶导数。第 146 条（10-13）标题写「2.5 高阶导数」，内容确实讲的是高阶导数 ⇒ 正确节号是 2.6。第 149 条（10-14 复检）沿用同一编号，同错。",
    "mastery": "na",
    "weak": "连带后果：`scripts/coach.mjs` 的 `taughtSections` 按节号匹配，把第 146 条的「2.5」直接算成「2.5 隐函数已讲」—— `map 高数` 输出因此把 2.5 标成「已讲」、2.6 标成「未讲」，两个正好反了。",
    "note": "【不影响已教内容】10-13 / 10-14 教的确实是高阶导数（二阶三阶导、`y''` 记号、逐阶求导），内容没错，只是编号错。\n【第二章真实进度】已讲：2.1 导数定义 · 2.2 单侧导数 · 2.3 求导公式 · 2.4 链式法则 · **2.6 高阶导数**。**2.5 隐函数与参数方程求导 = 零记录**，不能算已讲。\n【三个连带欠账】① 2.5 隐函数要补（5.3 多元隐函数求导的前置）② 2.7 微分要补 —— 3.3 讲的 `du = φ'(x)dx` 目前只是操作规则，原理欠在 2.7，当时已向学生声明 ③ 2.8 中值定理 / 2.9 洛必达为 P0，deadline 在 3.11 积分变限之前（3.11 要用洛必达处理 0/0）。\n【脚本待修】`taughtSections` 只认节号、不认内容，遇到编号笔误会静默污染 `map` 输出。修法二选一：以 note 里的实际内容为准，或对已知笔误建一张豁免表。"
}

line = json.dumps(entry, ensure_ascii=False)

# 幂等：同标题已存在就不重复追加
existing = io.open(LOG, encoding='utf-8').read()
if entry['title'] in existing:
    print('已存在，跳过')
else:
    with io.open(LOG, 'a', encoding='utf-8', newline='\n') as f:
        f.write(line + '\n')
    print('已追加')

with io.open(LOG, encoding='utf-8') as f:
    print('当前行数:', sum(1 for _ in f))
