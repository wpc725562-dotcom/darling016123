# -*- coding: utf-8 -*-
"""
把 2026 讲义 md 清洗成可蒸馏的纯文本快照。
只做机械清理，不改写内容：
  1. 去掉 PDF 分页注释 <!-- 原 PDF 第 N 页 ... -->
  2. 图片占位符 > [图: xxx]  -> [注] xxx（保留注释框里的有效信息）
  3. 去掉广告/页眉页脚行
  4. 压缩连续空行
输出到 资料/电子书蒸馏/_raw/{computer,gaoshu,english}.txt
"""
import os
import re

ROOT = r"D:/deeepseek/zhuan-sheng-ben-notes"
SRC = os.path.join(ROOT, "资料/2026讲义")
OUT = os.path.join(ROOT, "资料/电子书蒸馏/_raw")

JOBS = [
    ("【精编讲义】2026广东专插本《计算机基础与程序设计》.md", "computer.txt"),
    ("【精编讲义】2026广东专插本《高等数学》.md", "gaoshu.txt"),
    ("【精编讲义】2026广东专插本《英语基础与写作》.md", "english.txt"),
    ("【黄金知识汇编】2026广东专插本《计算机基础与程序设计》.md", "computer-gold.txt"),
    ("【黄金知识汇编】2026广东专插本《高等数学 》.md", "gaoshu-gold.txt"),
    ("【黄金知识汇编】2026广东专插本《英语基础与写作》.md", "english-gold.txt"),
]

# 广告 / 页眉页脚 / 水印行，整行删除
JUNK = [
    "专插本网课可比市场价实惠很多倍开通",
    "正版网课内部价开通",
    "扫一扫看课",
    "对应网课（每年按照最新考纲更新）",
    "课程精讲班",
]

RE_PAGE = re.compile(r"<!--\s*原 PDF 第\s*\d+\s*页[^>]*-->")
RE_IMG = re.compile(r"^>\s*\[图:\s*(.*?)\]\s*$")


def clean(text: str) -> str:
    lines = text.splitlines()
    out = []
    for ln in lines:
        if RE_PAGE.search(ln):
            continue
        stripped = ln.strip()
        if not stripped:
            out.append("")
            continue
        if any(j in stripped for j in JUNK) and len(stripped) < 60:
            continue
        m = RE_IMG.match(stripped)
        if m:
            body = m.group(1).strip()
            # 纯播放器截图这类没有知识点价值的，直接丢掉
            if "视频播放" in body or "播放器" in body or "扫一扫" in body:
                continue
            out.append("[注] " + body)
            continue
        out.append(ln.rstrip())

    # 压缩 3 行以上空行为 1 行
    res, blank = [], 0
    for ln in out:
        if ln == "":
            blank += 1
            if blank > 1:
                continue
        else:
            blank = 0
        res.append(ln)
    return "\n".join(res).strip() + "\n"


def main():
    os.makedirs(OUT, exist_ok=True)
    for fn, out_name in JOBS:
        p = os.path.join(SRC, fn)
        if not os.path.exists(p):
            print(f"[跳过] 不存在：{fn}")
            continue
        raw = open(p, encoding="utf-8", errors="replace").read()
        cleaned = clean(raw)
        dst = os.path.join(OUT, out_name)
        open(dst, "w", encoding="utf-8").write(cleaned)
        print(f"[写出] {out_name}  {len(cleaned)} 字符  {cleaned.count(chr(10))} 行")


if __name__ == "__main__":
    main()
