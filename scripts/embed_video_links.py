# -*- coding: utf-8 -*-
"""把『考点→B站视频』映射嵌入 docs/posts/computer/notes/ 每篇考纲笔记末尾。幂等。"""
import os

BASE = os.path.join(os.path.dirname(__file__), "..", "docs", "posts", "computer", "notes")
MARK = "## 📺 配套视频"

# 映射: 笔记名(空格形式，脚本里用docs文件名连字符形式) -> (标题, 链接, 提示)
MAP = {
  "1.1 C语言概述与基本概念": [
    ("升本啦 P2-P3 C语言概述与第一个程序", "https://www.bilibili.com/video/BV1KU4y167ds?p=2", "共24P 按教材分帧"),
    ("强哥 P4~P18 细化打点", "https://www.bilibili.com/video/BV1Ye411Y7Ue?p=4", "134P 单考点"),
  ],
  "1.2 数据的存储与运算": [
    ("强哥 P20~P70 数据类型/进制/运算符最全", "https://www.bilibili.com/video/BV1Ye411Y7Ue?p=20", "整型实型溢出/进制"),
    ("升本啦 P5 顺序程序设计", "https://www.bilibili.com/video/BV1KU4y167ds?p=5", ""),
  ],
  "1.3 顺序程序设计": [
    ("升本啦 P5 顺序/输入输出", "https://www.bilibili.com/video/BV1KU4y167ds?p=5", ""),
    ("强哥 P71~P89 输出/scanf/putchar/getchar", "https://www.bilibili.com/video/BV1Ye411Y7Ue?p=71", ""),
  ],
  "1.4 选择结构程序设计": [
    ("升本啦 P6~P10 关系/逻辑 + if + switch", "https://www.bilibili.com/video/BV1KU4y167ds?p=6", ""),
    ("强哥 P90~P116 选择结构", "https://www.bilibili.com/video/BV1Ye411Y7Ue?p=90", "短路/else匹配"),
  ],
  "1.5 循环结构程序设计": [
    ("升本啦 P11~16 while/do/for", "https://www.bilibili.com/video/BV1KU4y167ds?p=11", ""),
    ("强哥 P117~130 循环细节", "https://www.bilibili.com/video/BV1Ye411Y7Ue?p=117", "水仙花"),
  ],
  "1.6 数组": [
    ("升本啦 P17~19 一/二维/字符数组", "https://www.bilibili.com/video/BV1KU4y167ds?p=17", ""),
    ("强哥 P131~P134 数组定义/引用", "https://www.bilibili.com/video/BV1Ye411Y7Ue?p=131", ""),
  ],
  "1.7 函数": [
    ("升本啦 P20~24 函数/参数/作用域", "https://www.bilibili.com/video/BV1KU4y167ds?p=20", ""),
    ("翁恺 P68~74 函数定义/参数传递/本地变量", "https://www.bilibili.com/video/BV1dr4y1n7vA?p=68", "浙大翁恺 1894万"),
  ],
  "1.8 指针": [
    ("翁恺 P81~P87 取地址/指针/指针与数组/const/动态内存", "https://www.bilibili.com/video/BV1dr4y1n7vA?p=81", "指针专篇最权威"),
    ("翁恺 P84 指针与数组 sizeof陷阱", "https://www.bilibili.com/video/BV1dr4y1n7vA?p=84", ""),
  ],
  "1.9 结构体与共用体": [
    ("翁恺 P85 指针与const", "https://www.bilibili.com/video/BV1dr4y1n7vA?p=85", ""),
    ("严蔚敏华科大 P25 C语言结构体补充讲解", "https://www.bilibili.com/video/BV11T411q7Qw?p=25", ""),
    ("易懂C 联合union共用体 15分钟", "https://www.bilibili.com/video/BV1sz4y1a7cP", "共用体专讲"),
  ],
  "1.10 文件操作": [
    ("下位考点 · 抓不到对口免费公开课", "", "建议练谭浩强第10章习题+本笔记"),
  ],
  "1.11 程序运行环境与调试": [
    ("翁恺 P1~P10 C语言简史/装DevC++/第一个程序/调试", "https://www.bilibili.com/video/BV1dr4y1n7vA?p=1", "环境与调试"),
    ("翁恺 P19 交换变量顺便看Dev调试", "https://www.bilibili.com/video/BV1dr4y1n7vA?p=19", ""),
  ],
  "2.1 数据结构基本概念": [
    ("严蔚敏华科大 P2~P3 第一章 绪论", "https://www.bilibili.com/video/BV11T411q7Qw?p=2", "基本概念/算法分析"),
    ("严蔚敏本人 P46~P60 本人串讲", "https://www.bilibili.com/video/BV11T411q7Qw?p=46", ""),
  ],
  "2.2 线性表": [
    ("严蔚敏 华科大 P4~P6 第二章 线性表", "https://www.bilibili.com/video/BV11T411q7Qw?p=4", "顺序/链式"),
  ],
  "2.3 栈和队列": [
    ("严蔚敏 华科大 P7~P18 栈队列/表达式/汉诺塔/循环队列", "https://www.bilibili.com/video/BV11T411q7Qw?p=7", ""),
  ],
  "2.4 串、数组和广义表": [
    ("严蔚敏 华科大 P19~P27 串/数组/结构体", "https://www.bilibili.com/video/BV11T411q7Qw?p=19", ""),
  ],
  "2.5 树和二叉树": [
    ("严蔚敏 华科大 P28~P32 第六章 树与二叉树", "https://www.bilibili.com/video/BV11T411q7Qw?p=28", ""),
  ],
  "2.6 图": [
    ("严蔚敏 华科大 P33~P36 第七章 图", "https://www.bilibili.com/video/BV11T411q7Qw?p=33", ""),
  ],
  "2.7 查找": [
    ("严蔚敏 华科大 P37~P40 第九章 查找", "https://www.bilibili.com/video/BV11T411q7Qw?p=37", ""),
  ],
  "2.8 排序": [
    ("严蔚敏 华科大 P41~P44 第十章 排序", "https://www.bilibili.com/video/BV11T411q7Qw?p=41", ""),
  ],
  "2.9 算法基本概念与分析": [
    ("升本啦 P4 算法概念", "https://www.bilibili.com/video/BV1KU4y167ds?p=4", ""),
    ("强哥 P15~P19 算法特征", "https://www.bilibili.com/video/BV1Ye411Y7Ue?p=15", ""),
  ],
}

# docs 侧文件名：空格 -> 连字符
def fname_key(name):
    return name.replace(" ", "-")

def embed(fname_key_name, rows):
    path = os.path.join(BASE, fname_key_name + ".md")
    if not os.path.exists(path):
        return (False, "缺文件: " + fname_key_name)
    with open(path, encoding="utf-8") as f:
        body = f.read()
    if "配套视频" in body:
        return (False, "已含: " + fname_key_name)
    lines = [MARK, "", "> 复习到本考点 → 先看视频补讲，再刷上面「闭卷挑战」。", ""]
    for t, url, tip in rows:
        if not url:
            lines.append("- " + t)
            continue
        s = (" · " + tip) if tip else ""
        lines.append("- [" + t + "](" + url + ")" + s)
    lines.append("")
    # ★ E2（2026-09-20）：补 newline="\n"。默认 newline=None 在 Windows 上会把
    #   `\n` 翻译成 `\r\n`，同一份输入换个平台就产出不同字节 —— 与 write_text 同类。
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write("\n" + "\n".join(lines) + "\n")
    return (True, "已嵌入: " + fname_key_name)

if __name__ == "__main__":
    ok = fail = 0
    for name, rows in MAP.items():
        key = fname_key(name)
        if not os.path.exists(os.path.join(BASE, key + ".md")):
            print("!! 缺文件", key); fail += 1; continue
        ok_, msg = embed(key, rows)
        print(("OK  " if ok_ else "!!  ") + msg)
        if ok_: ok += 1
        else: fail += 1
    print("完成 %d 篇, 失败 %d" % (ok, fail))
