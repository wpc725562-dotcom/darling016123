# -*- coding: utf-8 -*-
"""生成专升本学习路线思维导图 PNG（PIL 绘制，无外部依赖）。"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1400, 980
IMG = Image.new("RGB", (W, H), "#fff9fb")
D = ImageDraw.Draw(IMG)

# 中文字体（Windows 常见）
def font(sz):
    for name in ["msyh.ttc", "simhei.ttf", "simsun.ttc"]:
        try:
            return ImageFont.truetype(name, sz)
        except Exception:
            # ★ A6 复核（2026-09-20）：**有意**吞掉。这是一串候选字体，
            #   逐个试是设计意图；循环末尾有 load_default() 兜底。
            continue
    return ImageFont.load_default()

F_TITLE = font(40)
F_BIG = font(26)
F_MID = font(20)
F_SMALL = font(16)

# 主题色
PINK = "#e4596f"; DEEP = "#c8455e"; SOFT = "#fdeef1"
ORANGE = "#e6a23c"; GREEN = "#67c23a"; BLUE = "#409eff"

# 布局：中心标题 + 4 大阶段卡片 + 底部目标
def card(x, y, w, h, title, lines, color, fill):
    D.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=fill, outline=color, width=3)
    D.text((x + 18, y + 12), title, font=F_BIG, fill=color)
    ty = y + 50
    for ln in lines:
        D.text((x + 18, ty), ln, font=F_SMALL, fill="#444")
        ty += 26

# 标题
D.text((W // 2 - 210, 30), "广东专升本 · 学习路线图", font=F_TITLE, fill=DEEP)
D.text((W // 2 - 160, 80), "2027 届 · 计算机类 · 四科 500 分", font=F_MID, fill="#888")

# 阶段 0
card(60, 150, 580, 170, "阶段 0 · 概念地基（1-2 周）", [
    "💻 计算机：先懂 C 程序结构，别碰指针",
    "📐 高数：函数与极限（一切的地基）",
    "🏛️ 政治：看大纲读题型，不背",
], BLUE, "#eef6ff")

# 阶段 1
card(720, 150, 620, 170, "阶段 1 · 主攻拉分科", [
    "💻 计算机 200 分：C 基础→程序→数据结构",
    "📐 高数 100 分：函数→极限→导数→积分",
], ORANGE, "#fff8ec")

# 阶段 2
card(60, 360, 580, 150, "阶段 2 · 政治 + 英语维持", [
    "🏛️ 政治：学概念→背模板（17/18 篇）",
    "🇬🇧 英语：每周 1-2 套阅读保手感",
], GREEN, "#f0f9ec")

# 阶段 3
card(720, 360, 620, 150, "阶段 3 · 真题冲刺（最后 2-3 月）", [
    "📐 高数 2026/2024 全卷 · 💻 计算机历年真题",
    "🏛️ 政治 2018-2024 演练",
], PINK, "#fdeef1")

# 箭头连接
D.line([640, 235, 720, 235], fill="#bbb", width=4)
D.line([640, 420, 720, 420], fill="#bbb", width=4)
D.line([350, 320, 350, 360], fill="#bbb", width=4)
D.line([1030, 320, 1030, 360], fill="#bbb", width=4)

# 目标框
D.rounded_rectangle([400, 560, 1000, 660], radius=18, fill="#e8f5e9", outline=GREEN, width=4)
D.text((450, 580), "🎯 目标：公办本科 · 计算机类", font=F_BIG, fill="#2e7d32")
D.text((450, 618), "2027 年 3 月考试 · 全科目 0 基础友好", font=F_MID, fill="#555")

# 底部说明
D.text((W // 2 - 320, 720), "高数不能跳章：函数→极限→导数→积分是硬链条", font=F_SMALL, fill="#999")
D.text((W // 2 - 280, 750), "详细章节导航见 docs/guide/零基础学习路线.md", font=F_SMALL, fill="#bbb")

out = r"C:\Users\Administrator\Desktop\deeepseek\zhuan-sheng-ben-notes\docs\public\roadmap.png"
IMG.save(out)
print("saved:", out, os.path.getsize(out), "bytes")
