# -*- coding: utf-8 -*-
"""追加 277 条：诊断出「积分=照抄」误解 —— ∫1dt 为什么等于 t"""
import json, io

LOG = r'D:/deeepseek/zhuan-sheng-ben-notes/备考计划/学习日志.jsonl'

entry = {
    "date": "2026-10-23",
    "subject": "高数",
    "kind": "quiz",
    "title": "诊断 · $\\int 1\\,dt$ 为什么等于 $t$ 而不是 $1$ —— 学生把「积分」当成「照抄」",
    "score": "",
    "mastery": "failed",
    "weak": (
        "学生原话：「这里为什么是 $t-\\ln(1+t)$，我得出这个（$1-\\ln(1+t)$）；为什么后面这个 1 变成了 $t$」\n\n"
        "**这不是笔误，是概念缺口。** 他的心智模型是「积分＝把被积式抄下来」，所以被积式里的 $1$ 就原样留在答案里。\n"
        "⇒ 上一轮我判成「疲劳笔误」是**错的**，要更正。他 15 分钟前写对 $t$ 是照搬了上一题的模板，不是真懂。"
    ),
    "note": (
        "【讲解三条，任一条都能独立立住】\n"
        "**① 反导数**：谁的导数是 $1$？$t$ 的导数是 $1$，所以 $\\int 1\\,dt=t$。\n"
        "**② 幂函数公式取 $n=0$**：$\\int t^n dt=\\dfrac{t^{n+1}}{n+1}$，令 $n=0$ ⇒ $\\int t^0dt=\\dfrac{t^1}{1}=t$。**常数 1 就是 $t^0$。**\n"
        "**③ 反证**：若答案是 $1$，则 $(1)'=0\\ne1$，验算当场挂。\n\n"
        "【核心一句话】**积分是反求导，不是照抄。** 被积式抄下来当答案，等于没积分。\n\n"
        "【拆开写】$\\int\\left(1-\\dfrac{1}{1+t}\\right)dt=\\int 1\\,dt-\\int\\dfrac{1}{1+t}dt=t-\\ln|1+t|$\n"
        "两项分别积，减号照搬。\n\n"
        "【账本（带验算列）】\n"
        "| 被积式 | 积分结果 | 验算 |\n"
        "| $1$ | $t$ | $(t)'=1$ ✓ |\n"
        "| $\\dfrac{1}{1+t}$ | $\\ln|1+t|$ | $(\\ln|1+t|)'=\\dfrac{1}{1+t}$ ✓ |\n\n"
        "【待观察】这个缺口是否影响过 3.2 直接积分法（当时三题全对）。若 3.2 时能做对 $\\int k\\,dx=kx$，"
        "说明是「多步式子中丢掉常数项」的场景性问题，不是纯概念缺失。需在下一次复检时用 $\\int(2-\\frac{1}{x})dx$ 同型题验证。"
    ),
}

with io.open(LOG, 'a', encoding='utf-8', newline='\n') as f:
    f.write(json.dumps(entry, ensure_ascii=False) + '\n')

with io.open(LOG, 'r', encoding='utf-8') as f:
    n = sum(1 for _ in f)
print('appended -> line', n)
