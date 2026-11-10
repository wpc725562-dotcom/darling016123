# -*- coding: utf-8 -*-
"""追加 276 条：3.4 复测收口 —— 方法全对，两处书写错误（∫1dt 写成 1、答案后缀 dx）"""
import json, io

LOG = r'D:/deeepseek/zhuan-sheng-ben-notes/备考计划/学习日志.jsonl'

entry = {
    "date": "2026-10-23",
    "subject": "高数",
    "kind": "quiz",
    "title": "3.4 复测收口 · $\\int dx/(1+\\sqrt{2x+1})$：方法五步全对，两处书写错误",
    "score": (
        "学生最终写：$1-\\ln(1+\\sqrt{2x+1})\\,dx+C$\n\n"
        "**方法层全对**：令 $\\sqrt{2x+1}=t$ ✓ · $x=\\frac{t^2-1}{2}$ ✓ · $dx=t\\,dt$ ✓ · 拆分 ✓ · 换回 ✓ · 带 $+C$ ✓ · 无多余系数 ✓\n\n"
        "**两处错，都是书写层**：\n"
        "① $\\int 1\\,dt$ 写成 $1$ —— 应为 $t$\n"
        "② 答案后缀了一个 $dx$\n\n"
        "正确：$\\sqrt{2x+1}-\\ln\\left(1+\\sqrt{2x+1}\\right)+C$"
    ),
    "mastery": "partial",
    "weak": (
        "**① $\\int 1\\,dt=1$ 这个错，与 15 分钟前同一动作做对过（当时写的是 $t-\\ln|1+t|$，$t$ 是对的）。**\n"
        "⇒ 判定为**笔误/疲劳**，不是概念错。但必须让验算抓出来，不能靠我判。\n"
        "**② 答案后缀 $dx$** —— 这是概念性的：以为答案里还得带着 $dx$。"
    ),
    "note": (
        "【讲解：积分号和 $dx$ 是一对括号】\n"
        "$\\int\\ \\cdots\\ dx$ —— 积分号开口，$dx$ 收口，**同时出现、同时消失**。\n"
        "积分一旦做完，这一对括号就一起没了，答案里不可能还剩一个 $dx$。\n"
        "类比：$\\sqrt{\\phantom{x}}$ 的横线是括号，根号算完了，横线也就不存在了。\n\n"
        "【验算如何抓出 ①】\n"
        "对 $1-\\ln(1+\\sqrt{2x+1})$ 求导：第一项导数为 $0$，第二项为 $-\\dfrac{1}{\\left(1+\\sqrt{2x+1}\\right)\\sqrt{2x+1}}$\n"
        "⇒ 结果与被积函数 $\\dfrac{1}{1+\\sqrt{2x+1}}$ 差了整整一项，**验算立刻暴露**。\n"
        "⇒ **验算法今天第三次立功**（第一次抓系数 2、第二次确认 $dx=t\\,dt$、这次抓 $\\int1dt$）。这个动作要固化成每道必做。\n\n"
        "【3.4 最终状态：收口】\n"
        "令 → 反解 → 代回 → 算 → 换回，五步全部独立走通，两道题（含带系数变式）都过。\n"
        "剩余问题全部是书写层，不是方法层。\n\n"
        "【今日高数小结】3.1 / 3.2 / 3.3 / 3.4 四节完成。第三章 17 节中已过 4 节。"
    ),
}

with io.open(LOG, 'a', encoding='utf-8', newline='\n') as f:
    f.write(json.dumps(entry, ensure_ascii=False) + '\n')

with io.open(LOG, 'r', encoding='utf-8') as f:
    n = sum(1 for _ in f)
print('appended -> line', n)
