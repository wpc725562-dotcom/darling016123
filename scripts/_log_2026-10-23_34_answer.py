# -*- coding: utf-8 -*-
"""追加 274 条：3.4 根式代换 · 学生作答，拆分与换回全对，唯一错丢系数 2"""
import json, io

LOG = r'D:/deeepseek/zhuan-sheng-ben-notes/备考计划/学习日志.jsonl'

entry = {
    "date": "2026-10-23",
    "subject": "高数",
    "kind": "quiz",
    "title": "3.4 根式代换 · $\\int dx/(1+\\sqrt{x+1})$ 作答：拆分与换回全对，唯一错是丢掉系数 2",
    "score": (
        "学生手写：\n"
        "$\\int(1-\\frac{1}{1+t})dt=t-\\ln|1+t|$ ✓ **拆分完全正确**\n"
        "代入 $t=\\sqrt{x+1}$ ⇒ $\\sqrt{x+1}-\\ln(1+\\sqrt{x+1})$ ✓ **换回正确，绝对值也去对了**\n\n"
        "**唯一错误：丢掉系数 2。** 正确应为 $2\\sqrt{x+1}-2\\ln(1+\\sqrt{x+1})+C$。\n"
        "**次要：漏写 $+C$。**\n\n"
        "⇒ **前一轮诊断出的真实卡点（同次分式不会拆）已经过了。** 这是他今天第二个实质突破。"
    ),
    "mastery": "partial",
    "weak": (
        "**系数 2 是在第 ② 步产生的（$dx=2t\\,dt$），第 ③ 步写式子时容易只抄 $\\frac{t}{1+t}$，把 2 落下。**\n"
        "学生写的是 $\\int(1-\\frac{1}{1+t})dt$，把 2 提前提出去之后就忘了它还在外面。"
    ),
    "note": (
        "【自查法直接暴露错误】把学生的答案求导：\n"
        "$\\left[\\sqrt{x+1}-\\ln(1+\\sqrt{x+1})\\right]'=\\frac{1}{2\\sqrt{x+1}}-\\frac{1}{1+\\sqrt{x+1}}\\cdot\\frac{1}{2\\sqrt{x+1}}"
        "=\\frac{1}{2\\sqrt{x+1}}\\cdot\\frac{\\sqrt{x+1}}{1+\\sqrt{x+1}}=\\frac{1}{2(1+\\sqrt{x+1})}$\n"
        "**正好是原被积函数的一半** ⇒ 一眼看出前面少乘 2。\n"
        "⇒ **验算法不仅判对错，还能定位错在哪个系数上。这是今天该带走的第三个动作。**\n\n"
        "【防丢机制（本轮交付）】**不要把系数提出来，让它留在分子里一起拆。**\n"
        "$\\dfrac{2t}{1+t}$：凑 $2t=2(1+t)-2$\n"
        "$\\Rightarrow\\dfrac{2t}{1+t}=\\dfrac{2(1+t)-2}{1+t}=2-\\dfrac{2}{1+t}$\n"
        "$\\Rightarrow\\int\\left(2-\\dfrac{2}{1+t}\\right)dt=2t-2\\ln|1+t|$\n"
        "**每一项自带系数，结构上丢不掉。** 比「记得乘 2」可靠。\n\n"
        "【标准答案】$2\\sqrt{x+1}-2\\ln\\left(1+\\sqrt{x+1}\\right)+C$\n"
        "验算：$\\frac{1}{\\sqrt{x+1}}\\left[1-\\frac{1}{1+\\sqrt{x+1}}\\right]=\\frac{1}{1+\\sqrt{x+1}}$ ✓\n\n"
        "【3.4 状态】**收口** —— 令 / 反解 / 代回 / 算 / 换回 五步全部走通，仅剩系数意识。"
    ),
}

with io.open(LOG, 'a', encoding='utf-8', newline='\n') as f:
    f.write(json.dumps(entry, ensure_ascii=False) + '\n')

with io.open(LOG, 'r', encoding='utf-8') as f:
    n = sum(1 for _ in f)
print('appended -> line', n)
