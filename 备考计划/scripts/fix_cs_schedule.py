# -*- coding: utf-8 -*-
"""计算机排期纠错。
章节地图 §三：2.1/2.2/2.3 已 ✅；2.4-2.9 未做；2.5 树已在 D019 首讲、D020 练遍历。
但 D022 写「C语言一轮收口」（C 语言 1.1-1.11 早已全部讲完），
D025 排「2.1 基本概念」、D026 排「2.2 线性表」—— 两节都已完成，等于白排。
D023/D024 是「加练 · 弱项补强（按错题本选）」无判据占位。
=> 按 2.6 → 2.7 → 2.8 → 2.9 → 2.4 单调补齐，D026 收口时数据结构 9/9 全过。
"""
import re, pathlib

BASE = pathlib.Path(r"D:\专升本总库\07-学习计划\每日")

CS = {
    "D022": "2.6 图（邻接矩阵 / 邻接表 + DFS/BFS 序列，**D6 图必出主观题**）",
    "D023": "2.7 查找（顺序 / 折半 / 二叉排序树 / 哈希）",
    "D024": "2.8 排序（插入 / 冒泡 / 选择 / 快排 / 归并，五种的**手写过程**）",
    "D025": "2.9 算法基本概念与分析（时间 / 空间复杂度，大 O 会算）",
    "D026": "2.4 串、数组和广义表（KMP 跳过）+ **计算机周收口：数据结构 9/9**",
}
ROW = re.compile(r"^\| 下午 \| \*\*计算机\*\* \| 1h \| .*\|$", re.M)

for day, content in CS.items():
    p = sorted(BASE.glob(day + "-*.md"))[0]
    s = p.read_text(encoding="utf-8")
    n = len(ROW.findall(s))
    new = f"| 下午 | **计算机** | 1h | {content} |"
    s2 = ROW.sub(lambda m: new, s, count=1)
    bad = sum(1 for c in s2 if ord(c) < 9 or (13 < ord(c) < 32))
    p.write_text(s2, encoding="utf-8")
    print(f"{p.name:32s} 计算机行{n} 改动{'OK' if s2!=s else 'NO'} 控制字符{bad}")
