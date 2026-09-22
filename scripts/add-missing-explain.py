# -*- coding: utf-8 -*-
"""给 2021/2022 真题里 8 道「有答案、无解析」的数据结构选择题补解析。

为什么补：这 8 道是 2021/2022 唯一涉及 图/查找/栈/线性表/算法 的选择题，
而数据结构是看板 0% 的科目 —— 没有解析就没法自学。
全部标注「站内补注」，与真题原文解析区分开。

用法：python scripts/add-missing-explain.py [--apply]
不带 --apply 时只做 dry-run 校验（检查锚点唯一、下一行为空）。
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
APPLY = "--apply" in sys.argv

# (文件, 题干锚点, 答案行锚点, 解析正文)
FIXES = [
    ("历年真题/计算机程序设计/2021.md",
     "### 13. 适用于折半查找的是",
     "**答案：D** · 考点 [[2.7 查找]]",
     "折半查找的两个前提：**顺序存储**（要能随机访问，直接跳到 mid）"
     "和**关键字有序**（否则不知道往哪半边找）。链式存储做不到 O(1) 定位中间元素，"
     "所以 A/B 排除；顺序但无序无法比较取舍，C 排除。（站内补注）"),

    ("历年真题/计算机程序设计/2021.md",
     "### 16. 对新算法作性能分析的主要目的是",
     "**答案：C** · 考点 [[2.9 算法基本概念与分析]]",
     "性能分析 = 估算时间/空间复杂度，目的是**判断效率高低、找出瓶颈并改进**，"
     "从而在多个可行算法里选出合适的。A/B/D 是设计算法时同时要考虑的因素，"
     "但不属于「性能分析」这个动作的目的。（站内补注）"),

    ("历年真题/计算机程序设计/2021.md",
     "### 17. 数据结构在计算机内存中的表示是指",
     "**答案：C** · 考点 [[2.1 数据结构基本概念]]",
     "逻辑结构 = 数据元素之间的抽象关系（与机器无关）；"
     "**存储结构（物理结构）= 逻辑结构在计算机内存中的表示**，"
     "分顺序存储与链式存储两大类。题干问的是「内存中的表示」→ 存储结构。（站内补注）"),

    ("历年真题/计算机程序设计/2021.md",
     "### 19. 单链表 a 是 b 的前驱",
     "**答案：D** · 考点 [[2.2 线性表]]",
     "插入必须先接后、再断前：`a->link=c; c->link=b;` —— "
     "先让 c 指向 b（此刻 a→b 这条链还在），再让 a 指向 c。"
     "若反过来先执行 `a->link=c` 而 c 的后继还没设，b 及其后面所有结点就全丢了。"
     "选项 A（`c->link=b->link; b->link=c;`）是「在 b 之后插入」的写法，插入位置不对。（站内补注）"),

    ("历年真题/计算机程序设计/2021.md",
     "### 20. 递归算法实现一般需利用",
     "**答案：B** · 考点 [[2.3 栈和队列]]",
     "递归调用要把每一层的「返回地址 + 局部变量」按**后进先出**的顺序保存和恢复 —— "
     "最后被调用的那一层最先返回，正好是栈。系统用「递归工作栈」实现。"
     "队列是先进先出，做不到这一点。（站内补注）"),

    ("历年真题/计算机程序设计/2022.md",
     "### 6. 删除 p 所指结点的**直接后继**",
     "**答案：D** · 考点 [[2.2 线性表]]",
     "要删的是 p 的直接后继 `q = p->next`，所以让 p 直接越过 q 指向 q 的后继："
     "`p->next = p->next->next`。A 让 p 指向自己（成环）；"
     "B 只改了指针变量 p 本身，链表结构没变；C 跳过了两个结点，删的是「后继的后继」。（站内补注）"),

    ("历年真题/计算机程序设计/2022.md",
     "### 7. 有向图所有顶点出度总和与入度总和比值",
     "**答案：C** · 考点 [[2.6 图]]",
     "每条弧 `<v,w>` 恰好贡献 v 的一个出度和 w 的一个入度，一一对应。"
     "所以 **Σ出度 = Σ入度 = 弧数**，两者恒等，比值恒为 1。（站内补注）"),

    ("历年真题/计算机程序设计/2022.md",
     "### 20. 队列和栈的共同点是",
     "**答案：D** · 考点 [[2.3 栈和队列]]",
     "栈和队列都是**操作受限的线性表** —— 插入和删除只能在端点进行"
     "（栈在同一端，队列在一端插、另一端删）。A「先进先出」是队列的特点，"
     "B「先进后出」和 C「后进先出」都是栈的特点，都只描述了其中一种。（站内补注）"),
]

errors = []
applied = 0
for rel, head_anchor, ans_anchor, text in FIXES:
    p = ROOT / rel
    t = p.read_text(encoding="utf-8")
    hi = t.find(head_anchor)
    if hi < 0:
        errors.append(f"[锚点缺失] {rel} :: {head_anchor}")
        continue
    # 答案行必须在这个 ### 之后、下一个 ### 之前
    nxt = t.find("\n### ", hi)
    seg_end = nxt if nxt > 0 else len(t)
    ai = t.find(ans_anchor, hi, seg_end)
    if ai < 0:
        errors.append(f"[答案行缺失] {rel} :: {ans_anchor}")
        continue
    if t.count(ans_anchor) != 1:
        errors.append(f"[锚点不唯一 {t.count(ans_anchor)} 次] {rel} :: {ans_anchor}")
        continue
    line_end = t.find("\n", ai)
    if line_end < 0:
        errors.append(f"[答案行无换行] {rel} :: {ans_anchor}")
        continue
    # 已有解析就不重复插
    if "**解析**" in t[ai:seg_end]:
        errors.append(f"[已有解析，跳过] {rel} :: {ans_anchor}")
        continue
    # ★ 插入串**不带尾部换行** —— 答案行后面本来就有一个空行，
    #   写成 "\n**解析**：…\n" 会变成两个连续空行（markdown 虽能忍，但 diff 难看）。
    insert = f"\n**解析**：{text}"
    new = t[:line_end] + insert + t[line_end:]
    if APPLY:
        p.write_text(new, encoding="utf-8", newline="\n")
    applied += 1
    print(f"  {'✅ 写入' if APPLY else '✓ 校验通过'}  {rel.split('/')[-1]}  {head_anchor[:34]}")

print()
if errors:
    print("⚠️ 问题：")
    for e in errors:
        print("   " + e)
    sys.exit(1)
print(f"{'已写入' if APPLY else '可写入'} {applied} 处" + ("（dry-run，加 --apply 才落盘）" if not APPLY else ""))
