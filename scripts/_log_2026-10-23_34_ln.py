# -*- coding: utf-8 -*-
"""追加 275 条：3.4 复测题（根号内带系数）学生 ①②③ 全对 + ln 步骤精讲"""
import json, io

LOG = r'D:/deeepseek/zhuan-sheng-ben-notes/备考计划/学习日志.jsonl'

entry = {
    "date": "2026-10-23",
    "subject": "高数",
    "kind": "quiz",
    "title": "3.4 复测 · $\\int dx/(1+\\sqrt{2x+1})$ 学生 ①②③ 全对，且避开了 $dx=2t\\,dt$ 的套用陷阱；追问 $\\ln|1+t|$ 的来由",
    "score": (
        "学生手写：\n"
        "令 $\\sqrt{2x+1}=t$ ✓ · $t^2=2x+1$ ✓ · $x=\\dfrac{t^2-1}{2}$ ✓ · **$dx=t\\,dt$ ✓**\n"
        "$\\dfrac{t}{1+t}=\\dfrac{(1+t)-1}{1+t}=1-\\dfrac{1}{1+t}$ ✓\n\n"
        "**关键：$dx=t\\,dt$ 写对了，没有套用上一题的 $2t\\,dt$。** 这道题就是专门设计来测这个的 —— "
        "根号里加了系数 2，机械记忆 $2t\\,dt$ 的人必错。他没中招，说明学到的是方法不是结果。\n"
        "（尚未写出最终答案，停在拆分处）"
    ),
    "mastery": "partial",
    "weak": (
        "**唯一提问：$\\ln\\lvert 1+t\\rvert$ 这一步怎么来的。** 学生原话「这里的 ln|1+t| 再讲解一下」。\n"
        "⇒ 不是算错，是**不知道这一步凭什么成立**。他能照着抄，但没接上 3.2 公式表和 3.3 凑微分。"
    ),
    "note": (
        "【讲解：三步接上】\n"
        "**① 公式表第 3 条**（3.2 已讲）：$\\int\\dfrac{1}{u}du=\\ln|u|+C$\n"
        "**② 用 3.3 凑微分套上去**：$\\int\\dfrac{1}{1+t}dt=\\int\\dfrac{1}{1+t}\\,d(1+t)$ —— 因为 $d(1+t)=dt$。\n"
        "令 $u=1+t$ ⇒ $\\int\\dfrac{1}{u}du=\\ln|u|=\\ln|1+t|$。\n"
        "**关键：$d(1+t)=dt$，$t$ 的系数是 1，所以不用补任何系数。**\n"
        "**③ 绝对值**：$\\ln$ 只吃正数。$(\\ln x)'=\\frac1x$ 只在 $x>0$ 成立；$(\\ln|x|)'=\\frac1x$ 对 $x\\ne0$ 都成立，所以写 $|u|$。\n\n"
        "【本题为什么能去掉绝对值】$t=\\sqrt{2x+1}\\ge0$ ⇒ $1+t\\ge1>0$ ⇒ $|1+t|=1+t$。\n\n"
        "【对照（防错探针）】分母里 $t$ 的系数不是 1 时必须补倒数：\n"
        "$d(1+2t)=2dt$ ⇒ $\\int\\dfrac{1}{1+2t}dt=\\dfrac12\\ln|1+2t|$\n"
        "$d(1-t)=-dt$ ⇒ $\\int\\dfrac{1}{1-t}dt=-\\ln|1-t|$\n"
        "**判据：看 $d(\\text{分母})$ 是不是恰好等于 $dt$。是 → 直接用公式；不是 → 按倍数补。**\n\n"
        "【本题最终答案（学生未写）】$\\sqrt{2x+1}-\\ln\\left(1+\\sqrt{2x+1}\\right)+C$\n"
        "验算：$\\frac{1}{\\sqrt{2x+1}}\\left[1-\\frac{1}{1+\\sqrt{2x+1}}\\right]=\\frac{1}{1+\\sqrt{2x+1}}$ ✓\n"
        "**注意这题没有系数 2** —— 因为 $dx=t\\,dt$ 里本来就没有 2。上一题的 2 是反解出来的，不是背出来的。"
    ),
}

with io.open(LOG, 'a', encoding='utf-8', newline='\n') as f:
    f.write(json.dumps(entry, ensure_ascii=False) + '\n')

with io.open(LOG, 'r', encoding='utf-8') as f:
    n = sum(1 for _ in f)
print('appended -> line', n)
