# -*- coding: utf-8 -*-
"""把 1.10 文件操作的全部素材合并成一个 txt。"""
import io
import os

BASE = r"D:/deeepseek/zhuan-sheng-ben-notes"
OUT = os.path.join(BASE, "资料", "1.10-文件操作-全量知识点.txt")

SEP = "=" * 78
SUB = "-" * 78


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


def read_lines(path, start, end=None):
    """start / end 都是 1-based，end 含。"""
    with io.open(path, encoding="utf-8") as f:
        lines = f.readlines()
    return "".join(lines[start - 1:end])


parts = []

# ---------- 头部 ----------
parts.append(SEP)
parts.append("1.10 文件操作 · 全量知识点合集")
parts.append("生成时间：2026-10-22")
parts.append("用途：喂给 AI 做知识抽取 / 题库生成 / 讲义重排")
parts.append(SEP)
parts.append("")
parts.append("【目录】")
parts.append("  一、核心笔记（studio 笔记站 · 零基础讲义，结构化）")
parts.append("  二、真题考点审计（考什么、考几年、怎么错）")
parts.append("  三、笔记站章节审计（覆盖度检查）")
parts.append("  四、B站网课讲义（鹏哥 C 语言 · 文件章节，分两段）")
parts.append("     4.1 文件操作基础 + 顺序读写（fputc/fgetc/feof）")
parts.append("     4.2 顺序读写（fputs/fgets · fprintf/fscanf · fwrite/fread）+ 随机读写 + 缓冲区")
parts.append("  五、studio 知识点看板元数据")
parts.append("")
parts.append("【说明】各部分按来源分节，内容未删改。第四部分是网课整理的讲义体，")
parts.append("        每条按「要点 / 关键概念 / 相互关系 / 出处」四栏写，可直接当题库素材。")
parts.append("")

# ---------- 一、核心笔记 ----------
parts.append(SEP)
parts.append("一、核心笔记（studio 笔记站 · 1.10 文件操作）")
parts.append(SEP)
parts.append("")
parts.append(read(os.path.join(BASE, "docs/posts/computer/notes/1.10-文件操作.md")))
parts.append("")

# ---------- 二、真题考点审计 ----------
parts.append(SEP)
parts.append("二、真题考点审计（文件操作章节）")
parts.append(SEP)
parts.append("")
parts.append(read(os.path.join(BASE, "knowledge/audit/文件操作章节-历年真题考点审计报告.md")))
parts.append("")

# ---------- 三、笔记站章节审计 ----------
parts.append(SEP)
parts.append("三、笔记站章节审计（1.10 覆盖度检查）")
parts.append(SEP)
parts.append("")
parts.append(read(os.path.join(BASE, "docs/posts/computer/notes/audit-1.10-文件操作-审计报告.md")))
parts.append("")

# ---------- 四、B站网课讲义 ----------
parts.append(SEP)
parts.append("四、B站网课讲义（鹏哥 C 语言 2026 · 文件章节）")
parts.append(SEP)
parts.append("")
parts.append(SUB)
parts.append("4.1 文件操作基础 + 顺序读写（fputc / fgetc / feof）")
parts.append("来源：BV17a7K64ELH_29 第 143–205 行")
parts.append(SUB)
parts.append("")
parts.append(read_lines(os.path.join(BASE, "data/bili-analyze/_extract/BV17a7K64ELH_29.md"), 143, 205))
parts.append("")
parts.append(SUB)
parts.append("4.2 格式化读写 / 二进制块读写 / 随机读写 / 缓冲区")
parts.append("来源：BV17a7K64ELH_30 第 1–62 行")
parts.append(SUB)
parts.append("")
parts.append(read_lines(os.path.join(BASE, "data/bili-analyze/_extract/BV17a7K64ELH_30.md"), 1, 62))
parts.append("")

# ---------- 五、studio 元数据 ----------
parts.append(SEP)
parts.append("五、studio 知识点看板元数据")
parts.append(SEP)
parts.append("")
parts.append("模块：⑩ 文件")
parts.append("分值：5 分")
parts.append("状态：active（10-21 整章 7 块已全部讲完并通过关口题）")
parts.append("")
parts.append("【七块章地图 + 真题打点】")
parts.append("  3.1 文件的基本概念（文本文件 / 二进制文件、文件指针）—— 概念题")
parts.append("  3.2 打开文件 fopen —— 2018/2019/2020 填空 10（连续三年）· 2021 单选 8 · 2023 单选 2")
parts.append("  3.3 关闭文件 fclose —— 2023 判断 9（成功返回 0）")
parts.append("  3.4 文件的读写（fgetc/fputc · fgets/fputs · fprintf/fscanf · fread/fwrite）—— 2022 单选 15")
parts.append("  3.5 文件定位（fseek / rewind / ftell）—— 低频")
parts.append("  3.6 完整文件操作示例 —— 应用题素材")
parts.append("  3.7 检测文件末尾（feof / 返回值判断）—— 2022 填空 3（4 分，问「遇到文件结束函数值为__」→ 非 0）")
parts.append("")
parts.append("【三个返回值（判断题专考）】")
parts.append("  fopen 打开失败 → NULL")
parts.append("  fclose 关闭成功 → 0")
parts.append("  fgetc 读到末尾 → EOF（值 -1）")
parts.append("")
parts.append("【三个坑】")
parts.append("  坑 1：fgetc 到末尾返回 EOF，不是 NULL 也不是 0")
parts.append("  坑 2：fgets(str, n, fp) 最多读 n-1 个字符（留一个给 '\\0'），且会把换行符 '\\n' 一起读进来")
parts.append("  坑 3：fprintf 的格式串里，除 % 开头的占位符外，其余字符（空格、x=、+）全部原样照抄")
parts.append("")
parts.append(SEP)
parts.append("（完）")
parts.append(SEP)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with io.open(OUT, "w", encoding="utf-8-sig") as f:
    f.write("\n".join(parts))

size = os.path.getsize(OUT)
chars = len("\n".join(parts))
print("输出:", OUT)
print("字节:", size, "| 字符:", chars)
