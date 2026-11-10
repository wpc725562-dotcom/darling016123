# -*- coding: utf-8 -*-
"""重写学习日志最后两条（前一次经 shell 传参时 \\a 被解析成控制字符，导致 arcsin 损坏）。"""
import json
import io

PATH = "D:/deeepseek/zhuan-sheng-ben-notes/备考计划/学习日志.jsonl"

rows = [
    {
        "date": "2026-10-24",
        "subject": "高数",
        "kind": "quiz",
        "title": "3.5 复检 ∫dx/√(25−x²) —— 前三步全对，第④步把 5cos t/5cos t 算成 1/5，且丢了积分号",
        "score": (
            "**学生手写**：\n"
            "判型「常数 − x²」✅\n"
            "令 $x=5\\sin t$，$dx=5\\cos t\\,dt$ ✅\n"
            "$\\sqrt{25-25\\sin^2t}=\\sqrt{25(1-\\sin^2t)}=5\\cos t$ ✅\n"
            "「代入得 $\\dfrac{5\\cos t}{5\\cos t}=\\dfrac{1}{5}$」❌"
        ),
        "mastery": "failed",
        "weak": (
            "三处错：① $\\int$ 与 $dt$ 全丢，积分式退化成算术分数式；"
            "② $\\dfrac{5\\cos t}{5\\cos t}$ 应为 $1$，写成 $\\dfrac15$；"
            "③ 没有 $\\int 1\\,dt=t$，没有换回 $x$。"
        ),
        "note": (
            "**病根不是不会三角代换，是「把积分式当分数式求值」** —— 与 3.4「$\\int 1\\,dt$ 写成 1」同源。\n\n"
            "给出两条可复用自检：\n"
            "① 每一行检查 $\\int$ 与 $dt$ 是否成对；\n"
            "② 不定积分结果必须是含 $x$ 的函数 $+C$，出现纯数字 100% 是中途丢了 $\\int$。"
        ),
    },
    {
        "date": "2026-10-24",
        "subject": "高数",
        "kind": "quiz",
        "title": "3.5 收口 · ∫dx/√(36−x²) 四步全对，第④步第一次自己走出来",
        "score": (
            "**学生手写**：\n"
            "令 $x=6\\sin t$，$dx=6\\cos t\\,dt$ ✅\n"
            "$\\int\\dfrac{6\\cos t\\,dt}{6\\cos t}$ ✅（积分号与 $dt$ 都保住）\n"
            "$\\int 1\\,dt=t+C$ ✅\n"
            "$t=\\arcsin\\dfrac{x}{6}$ ✅\n"
            "结论 $\\arcsin\\dfrac{x}{6}+C$ ✅"
        ),
        "mastery": "pass",
        "weak": (
            "无致命错。一处书写瑕疵：先写 $t=\\dfrac{x}{\\sin 6}$ 后自行划掉改为 $\\arcsin\\dfrac{x}{6}$，"
            "暴露「把 $\\sin$ 当乘数除过去」的倾向。"
        ),
        "note": (
            "10-23 起连续两次漏第④步，**本次补上**。\n\n"
            "**3.5 三角代换 sin / tan / sec 三型全部闭环。**\n"
            "下一步 3.6 分部积分有硬前置：3.2 基本积分公式表只讲了幂函数一行，必须先补全。"
        ),
    },
]

lines = io.open(PATH, encoding="utf-8").read().rstrip("\n").split("\n")
assert len(lines) >= 2, "日志行数异常"
lines = lines[:-2] + [json.dumps(r, ensure_ascii=False) for r in rows]
io.open(PATH, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")

check = [json.loads(l) for l in io.open(PATH, encoding="utf-8") if l.strip()]
print("total", len(check))
print(check[-1]["score"])
