#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把「字幕 + 提示词」打包成一个文件 —— 供**网页版 AI**（无 API）使用。

为什么需要它
    知识地图的提炼链（字幕 → 单元 → 知识点卡片）目前依赖 API。一旦没有免费 API，
    就只能「打开网页 AI → 把资料复制给它 → 把结果粘回来」。
    手工拼「提示词 + 语料」既慢又容易漏，本脚本把这一步变成**一次复制**。

设计原则
    ① 一个产物文件 = 一次完整的复制粘贴（提示词在前、语料在后，中间有分隔线）。
    ② 提示词**固定**（4 种任务）—— 网页 AI 输出格式稳定，粘回来才能脚本化落站。
    ③ 不做任何联网 / 不调用任何模型 —— 纯本地文本处理。

用法
    # 提炼知识点卡片（最常用：补知识地图）
    python scripts/offline-pack.py --bv BV1QKbZ6xEea --p 4 --task extract

    # 多源讲法对比（同一考点取多个来源）
    python scripts/offline-pack.py --bv BV1QKbZ6xEea:4,BV1Do4y1h7om:1 --task compare

    # 出题 / 讲解
    python scripts/offline-pack.py --bv BV1QKbZ6xEea --p 12 --task quiz --n 10
    python scripts/offline-pack.py --bv BV1QKbZ6xEea --p 4 --task explain

    # 多集一起打包（一个文件塞多集，适合短集）
    python scripts/offline-pack.py --bv BV1QKbZ6xEea --p 4,5,6 --task extract

产出
    data/offline-feed/<BV>_pNN_<task>.md      打开 → 全选 → 粘进网页 AI
    data/offline-feed/out-<同名>.md           ← AI 的输出粘到这里（供后续落站）

★ 注意
    - 字幕是语音识别产物，有错字（「石头老师」会被识别成「史德老师」）。
      提示词里已声明这一点，让 AI 自己容忍。
    - 单次语料过长时（> 5 万字）建议拆集，或改用 --truncate 截断。
"""
import argparse
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BILI = os.path.join(ROOT, "data", "bili-analyze")
FEED = os.path.join(ROOT, "data", "offline-feed")
TITLES = os.path.join(BILI, "_part_titles_all.json")

SEP = "\n\n" + "=" * 72 + "\n\n"

# ---- 提示词模板（固定；改这里 = 改所有产物的问法）---------------------------

PROMPTS = {
    "extract": """你是专升本（广东）教研助手。下面是 B站课程的**逐句字幕**（语音识别产物，可能有个别错字，请自行容忍，不要因此漏掉考点）。

请把它提炼成「知识点卡片」，**严格按下面格式**，每条卡片三行，不要加别的字段：

### <知识点名>
- **要点**：<是什么 / 怎么用 / 为什么；1–3 句，具体到可操作>
- **关键概念**：`概念1`、`概念2`
- **相互关系**：<前置知识 / 易混点；没有就写「——」>

硬性要求：
1. **只提炼考点**，不要复述课堂废话（「大家好」「我们来看」「这个很重要」）。
2. 一集控制在 **5–15 条**，宁少勿滥。
3. 公式、数字、英文术语、例句**原样保留**，不要改写。
4. **不要输出任何前言、总结、寒暄** —— 直接从 `### ` 开始输出卡片。""",

    "compare": """你是专升本（广东）教研助手。下面是**同一个考点**在多个来源里的讲法（逐句字幕，语音识别产物）。

请**只依据下面文本**输出三节（不要引入文本之外的知识）：

## 一、各源怎么讲
每个来源一小节，2–4 句概括它的**独特说法**（它强调什么、用什么比喻、给什么口诀）。

## 二、冲突与互补
用表格：| 维度 | 各源说法 | 合并结论 |
只列**真有分歧**或**互相补充**的维度；没有分歧就写「无冲突」。

## 三、合并讲法
一段话（可直接讲给学生听），把各源优点合起来。文本没提到的写「未涉及」，不要脑补。""",

    "quiz": """你是专升本（广东）出题老师。依据下面的语料出题。

格式（每题独立成块）：

**第 N 题** <题干>
A. …
B. …
C. …
D. …
**答案**：<字母>　**依据**：<语料里的原句或考点>

要求：
1. 难度对齐**广东专升本**（不要出高考压轴难度）。
2. **不要出语料之外的内容** —— 每题都要能在语料里找到依据。
3. 题干要具体（给情境、给句子），不要出「以下说法正确的是」这种空题。
4. 出完题**不要写解析**（解析我自己写）。""",

    "explain": """你是给**零基础学生**讲课的老师。用下面的语料，把这一集讲清楚。

要求：
1. **结论先行** —— 先说「这集要解决什么问题」，再展开。
2. 每一步都解释**为什么**，不要只给结论。
3. 技术术语保留英文原词，但第一次出现要解释。
4. 不要客套话、不要「好问题」「让我们来看看」这类填充。
5. 最后给一句**「一句话记住」**。""",
}


def load_titles():
    if not os.path.exists(TITLES):
        return {}
    with io.open(TITLES, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_spec(spec):
    """'BV1xx:4,5' 或 'BV1xx' → [(bv, [p...])]；多 BV 用逗号分隔的 'BV:ps' 形式。"""
    out = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if ":" in chunk:
            bv, ps = chunk.split(":", 1)
            pages = [int(x) for x in ps.split("+") if x.strip()]
            out.append((bv.strip(), pages))
        else:
            out.append((chunk, None))
    return out


def read_sub(bv, p, truncate=None):
    path = os.path.join(BILI, bv, "subtitle_p%02d.txt" % p)
    if not os.path.exists(path):
        return None
    with io.open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    if truncate and len(text) > truncate:
        text = text[:truncate] + "\n…（已截断）"
    return text


def part_title(titles, bv, p):
    info = titles.get(bv, {})
    for pg in info.get("pages", []):
        if pg.get("p") == p:
            return pg.get("part", "")
    return ""


def main():
    ap = argparse.ArgumentParser(description="打包字幕+提示词，供网页版 AI 使用")
    ap.add_argument("--bv", required=True,
                    help="BV 号；多集用 'BV1xx:4+5'，多源用 'BV1xx:4,BV1yy:1'")
    ap.add_argument("--p", default=None, help="分P（可省略，改用 --bv 里的冒号写法）")
    ap.add_argument("--task", required=True, choices=sorted(PROMPTS.keys()))
    ap.add_argument("--n", type=int, default=10, help="quiz 任务出几道题（默认 10）")
    ap.add_argument("--truncate", type=int, default=None, help="单集截断到 N 字符")
    ap.add_argument("--out", default=None, help="输出路径（默认 data/offline-feed/）")
    ap.add_argument("--dry-run", action="store_true", help="只打印统计，不写文件")
    args = ap.parse_args()

    titles = load_titles()
    specs = parse_spec(args.bv)
    if args.p and specs and specs[0][1] is None:
        specs[0] = (specs[0][0], [int(x) for x in args.p.split(",") if x.strip()])

    blocks, name_bits, total = [], [], 0
    for bv, pages in specs:
        if pages is None:
            # 没给分P：取该 BV 全部
            d = os.path.join(BILI, bv)
            if not os.path.isdir(d):
                print("  ✗ 找不到 %s" % bv, file=sys.stderr)
                continue
            pages = sorted(int(m.group(1)) for m in
                           (re.match(r"subtitle_p(\d+)\.txt$", x) for x in os.listdir(d))
                           if m)
        for p in pages:
            text = read_sub(bv, p, args.truncate)
            if text is None:
                print("  ✗ 缺字幕 %s P%d" % (bv, p), file=sys.stderr)
                continue
            title = part_title(titles, bv, p) or titles.get(bv, {}).get("title", "")
            owner = titles.get(bv, {}).get("owner", "")
            head = "【来源 %s · P%d】%s%s" % (bv, p, ("%s · " % owner) if owner else "", title)
            blocks.append("## " + head + "\n\n" + text.strip())
            name_bits.append("%s_p%02d" % (bv, p))
            total += len(text)
            print("  ✓ %s P%d · %d 字符" % (bv, p, len(text)))

    if not blocks:
        print("没有任何语料，退出。", file=sys.stderr)
        return 1

    prompt = PROMPTS[args.task]
    if args.task == "quiz":
        prompt = prompt.replace("出题。", "出 **%d 道**题。" % args.n)

    body = SEP.join(blocks)
    out_name = args.out or os.path.join(FEED, "%s_%s.md" % ("_".join(name_bits)[:60], args.task))
    out_base = os.path.basename(out_name)
    if out_base.endswith(".md"):
        out_base = out_base[:-3]
    doc = (
        "<!-- 网页版 AI 打包文件 · 由 scripts/offline-pack.py 生成 -->\n"
        "<!-- 用法：全选下面内容 → 粘进网页版 AI（Kimi / 豆包 / 通义 / ChatGPT 等）→ 把它的回答粘到 out-%s.md -->\n"
        "%s\n\n"
        "----- 以下全部是提示词 -----\n\n%s\n\n"
        "----- 以下全部是语料（共 %d 字符）-----\n\n%s\n"
    ) % (out_base, "# 任务：%s" % args.task, prompt, total, body)

    if args.dry_run:
        print("\n[dry-run] 共 %d 块 · %d 字符 → %s" % (len(blocks), total, out_name))
        return 0

    os.makedirs(os.path.dirname(out_name), exist_ok=True)
    with io.open(out_name, "w", encoding="utf-8") as f:
        f.write(doc)
    print("\n✅ 已写出：%s" % out_name)
    print("   共 %d 块 · %d 字符 —— 打开后全选复制，粘进网页版 AI" % (len(blocks), total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
