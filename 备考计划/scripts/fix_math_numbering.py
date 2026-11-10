# -*- coding: utf-8 -*-
"""修三处真实缺陷：
1) D022-D024 高数是「加练 · 弱项补强」无判据占位 → 换成具体节次 + G 编号
2) D025/D026 的「4.1/4.2」与章节地图「第四章=空间解析几何」冲突 → 改回 3.x
3) D022/D025 英语行「Anki 15min（Anki 15min + ...）」重复嵌套 → 拆平
4) D020 的「3.6」补上考点笔记文件名 G4-6，否则用户去笔记目录会翻到 G3-6 曲线的渐近线
"""
import re, pathlib

BASE = pathlib.Path(r"D:\专升本总库\07-学习计划\每日")

MATH = {
    "D022": "3.7 定积分的概念（考点笔记 `G5-1-定积分的概念.txt`）",
    "D023": "3.8 牛顿-莱布尼兹公式及定积分性质（`G5-2`）",
    "D024": "3.9 定积分的换元法（`G5-3`）",
    "D025": "3.10 定积分的分部积分法（`G5-4`）",
    "D026": "3.11 积分变限函数及其导数（`G5-5`，需洛必达 `G3-2`）",
}
ENG = {
    "D022": "Anki 15min + 阅读 1 篇（限时）",
    "D025": "Anki 15min + 阅读 1 篇（限时）",
}
MATH_ROW = re.compile(r"^\| 上午 \| \*\*高数\*\* \| 1h \| .*\|$", re.M)
ENG_ROW = re.compile(r"^\| 碎片 \| \*\*英语\*\* \| 20min \| .*\|$", re.M)

for day in ["D022", "D023", "D024", "D025", "D026"]:
    p = sorted(BASE.glob(day + "-*.md"))[0]
    s = p.read_text(encoding="utf-8")
    n0 = len(MATH_ROW.findall(s))
    new = f"| 上午 | **高数** | 1h | {MATH[day]} |"
    s2 = MATH_ROW.sub(lambda m: new, s, count=1)
    if day in ENG:
        n1 = len(ENG_ROW.findall(s2))
        e = f"| 碎片 | **英语** | 20min | {ENG[day]} |"
        s2 = ENG_ROW.sub(lambda m: e, s2, count=1)
    else:
        n1 = "-"
    bad = sum(1 for c in s2 if ord(c) < 9 or (13 < ord(c) < 32))
    p.write_text(s2, encoding="utf-8")
    print(f"{p.name:32s} 高数行{n0} 英语行{n1} 控制字符{bad}")

# D020：两处「3.6 分部积分」补 G4-6
p = sorted(BASE.glob("D020-*.md"))[0]
s = p.read_text(encoding="utf-8")
s2 = s.replace("### ③ 高数 3.6 分部积分 —— 25 分钟",
               "### ③ 高数 **3.6 分部积分**（考点笔记 `G4-6-分部积分法.txt`）—— 25 分钟")
s2 = s2.replace("| ③ | 高数 3.6 分部积分 | [ ] | 三道例题独立写完 ___/3 |",
                "| ③ | 高数 3.6 分部积分（`G4-6`） | [ ] | 三道例题独立写完 ___/3 |")
bad = sum(1 for c in s2 if ord(c) < 9 or (13 < ord(c) < 32))
p.write_text(s2, encoding="utf-8")
print(f"{p.name:32s} 改动 {'OK' if s2 != s else 'NO-CHANGE'} 控制字符{bad}")
