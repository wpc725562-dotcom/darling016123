#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""B站真题卡 × 笔记真题页 · 逐项对比

用途
----
把 `data/bili-zhenti/<BV>/extract/zhenti.jsonl`（从 B站 讲解视频的字幕 + 画面帧
抽出来的真题卡）跟 `docs/posts/<学科>/<年份>.md`（笔记站里的真题页）**按题号配对**，
逐题比题面与答案，给出三档结论。

为什么要单独写一个脚本
----------------------
1. **LaTeX 写法差异会把朴素字符串比较变成噪音。** 同一个答案，笔记页写
   `y=-\frac13x+1`，B站卡写 `y=-\dfrac{1}{3}x+1` —— 这是同一条答案。
   不归一化就会报出一堆假「不一致」，比不比对还糟。
2. **结论必须分档，不能只有「一致 / 不一致」两档。** 表达式题在没有符号计算引擎
   的情况下无法自动判定等价，硬报「不一致」是误导。所以第三档是
   **「需人工判定」** —— 明确说出「我没法自动判」，而不是猜。
3. 对比结果要能被复核：每一条都带 `evidence`（B站卡的出处）+ 笔记页行号。

判据（按可靠性从高到低）
------------------------
| 类型 | 判据 | 可靠性 |
|:---|:---|:---|
| 选择题（答案是个位字母 A–D） | 字母完全相等 | 确定 |
| 数值答案 | 解析成数后按容差比 | 确定 |
| 表达式答案 | 归一化 LaTeX 后字符串相等 | 高 |
| 表达式答案（归一化后不等） | 相似度 ≥ 阈值 → 「表述差异」；否则「需人工判定」 | 中 |

用法
----
    python scripts/bili_zhenti_diff.py --bv BV1Y3L36bEf1 --page docs/posts/math/2026.md
    python scripts/bili_zhenti_diff.py --bv BV1Y3L36bEf1 --page docs/posts/math/2026.md --json out.json
"""
import argparse
import difflib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ZHENTI_DIR = ROOT / "data" / "bili-zhenti"

# ── 笔记页解析 ───────────────────────────────────────────────────────────────
# 题号标题：`### 第 12 题 · 高阶导数`
NOTE_Q_RE = re.compile(r"^###\s*第\s*(\d{1,2})\s*题\s*(?:[·：:]\s*(.*))?$")
# 折叠块内的答案行，实际形态不止一种：
#     `**答案：$60$**`                      （数学，纯答案）
#     `**答案：B** · 考点 **1.2 数据的存储与运算**`   （计算机，带考点后缀）
#     `> **答案：A**`                       （块引用）
#     `回忆答案：**C. \`&a\`**`              （回忆版把选项写进答案里）
#     `**答案：<br>B**`                     （答案前有折行）
#
# ★ 原来写的是 `^\*\*答案[：:]\s*(.*?)\*\*\s*$` —— 末尾锚定 `\*\*\s*$` 是错的。
#   带考点后缀的行里，非贪婪捕获会一路吃到**最后一个** `**`：
#       `**答案：B** · 考点 **1.2 数据的存储与运算**`
#         → 捕获成 `B** · 考点 **1.2 数据的存储与运算`
#   于是 compare_answer() 的 `CHOICE_RE = ^([A-D])$` 永不命中，
#   所有这类题都落进「统一化后完全相同」或相似度兜底 ——
#   也就是说「答案一致」这个判断，**从来没有逐项比过选项字母**。
#   实测影响面：docs/posts 下 4 个文件、101 行
#   （2024.md 37、2025.md 34、2025-真题回忆版.md 29、2021.md 1）。
#
#   修法：不锚定行尾，只取「答案：」之后第一对 `**…**` 之间的内容。
#   ⚠️ 前面的 `(?:\*\*)?` 必须用**可选组**而不是 `\*{0,2}` —— 后者是贪婪的，
#      会把 `答案` 前那对 `**` 吃掉，然后要求 `：` 之后再出现一对 `**`，
#      于是 `**答案：B**` 一条都匹配不上（实测：整个语料 0 命中）。
NOTE_ANS_RE = re.compile(
    r"^>?\s*(?:\*\*)?\s*(?:回忆)?答案\s*[:：]\s*(?:\*\*)?\s*(.+?)\s*\*\*")
DETAILS_OPEN_RE = re.compile(r"^:::\s*details")


def clean_answer(v: str) -> str:
    """答案值的收尾清理。`**答案：<br>B**` 这种折行要抹掉，否则字母比对会失败。"""
    v = re.sub(r"<br\s*/?>", "", v, flags=re.I)
    return v.replace("&nbsp;", " ").strip()


def parse_note_page(path: pathlib.Path):
    """把笔记真题页解析成 {题号: {stem, answer, line}}。

    ★ 题面取「题号标题」到「::: details」之间的所有行。
      不取折叠块里的内容 —— 那里是解析，不是题面。
    """
    lines = path.read_text(encoding="utf-8").split("\n")
    out = {}
    cur = None
    for i, ln in enumerate(lines):
        s = ln.strip()
        m = NOTE_Q_RE.match(s)
        if m:
            cur = {
                "no": int(m.group(1)),
                "topic": (m.group(2) or "").strip(),
                "line": i + 1,
                "stem": [],
                "answer": None,
                "answer_line": None,
            }
            out[cur["no"]] = cur
            continue
        if cur is None:
            continue
        if DETAILS_OPEN_RE.match(s):
            # 折叠块开始 → 题面收集到此为止，转去块里找答案
            cur["_in_details"] = True
            continue
        if cur.get("_in_details"):
            if s == ":::":
                cur["_in_details"] = False
                continue
            if cur["answer"] is None:
                ma = NOTE_ANS_RE.match(s)
                if ma:
                    cur["answer"] = clean_answer(ma.group(1))
                    cur["answer_line"] = i + 1
            continue
        # 折叠块外、题号标题之后 = 题面
        if s and s != "---":
            cur["stem"].append(s)
    for c in out.values():
        c["stem"] = "\n".join(c["stem"])
        c.pop("_in_details", None)
    return out


# ── LaTeX 归一化 ─────────────────────────────────────────────────────────────
def norm_latex(s: str) -> str:
    """把 LaTeX 里「写法差异 ≠ 语义差异」的部分抹平。

    ★ 这里只做**保义**替换，不做任何化简 —— 脚本没有符号计算能力，
      一旦开始「猜等价」，报出来的「一致」就不可信了。
    """
    if not s:
        return ""
    t = s
    # 数学模式标记
    t = t.replace("$$", "").replace("$", "")
    t = t.replace("\\(", "").replace("\\)", "").replace("\\[", "").replace("\\]", "")
    # 分式：大小写与尺寸变体
    t = re.sub(r"\\(?:d|t)frac\b", r"\\frac", t)
    # 纯排版命令
    for cmd in ["\\displaystyle", "\\limits", "\\left", "\\right", "\\bigl", "\\bigr",
                "\\Bigl", "\\Bigr", "\\biggl", "\\biggr", "\\Biggl", "\\Biggr",
                "\\big", "\\Big", "\\bigg", "\\Bigg", "\\!", "\\,", "\\;", "\\:",
                "\\quad", "\\qquad", "\\nolimits", "\\operatorname"]:
        t = t.replace(cmd, "")
    # `\mathrm{d}x` / `\mathrm dx` → `dx`（笔记页用 \mathrm d，B站卡常直接写 dx）
    t = re.sub(r"\\mathrm\s*\{\s*d\s*\}", "d", t)
    t = re.sub(r"\\mathrm\s+d\b", "d", t)
    t = re.sub(r"\\rm\s*\{\s*d\s*\}", "d", t)
    t = re.sub(r"\\text\s*\{\s*([^{}]*?)\s*\}", r"\1", t)
    # 空白：LaTeX 里空白几乎总是不敏感的
    t = re.sub(r"\\[,;:!]", "", t)
    t = re.sub(r"\s+", "", t)
    # ★ 隐式花括号：LaTeX 允许省略「单字符」参数的花括号，但**笔记页和 B站卡
    #   不会用同一种写法** —— 笔记写 `x^2`、`\frac13`，卡里常写 `x^{2}`、`\frac{1}{3}`。
    #   不抹平这一层，同一条答案会被报成「需人工判定」，对比结果就没法用了。
    #   只处理**单字符**参数：多字符必须带花括号，否则没法确定边界。
    #   `\frac13x` 按 LaTeX 规则是 `\frac{1}{3}x`；`\frac1x` 是 `\frac{1}{x}`
    #   —— 两个参数都是「单个 token」，token 就是单个字符。
    t = re.sub(r"\\frac([A-Za-z0-9])([A-Za-z0-9])", r"\\frac{\1}{\2}", t)
    # 上下标：`^2` → `^{2}`、`_x` → `_{x}`；已经是 `^{...}` 的不动（`{` 不在字符类里）
    t = re.sub(r"\^([A-Za-z0-9])(?![A-Za-z0-9])", r"^{\1}", t)
    t = re.sub(r"(?<![\\\^])_([A-Za-z0-9])(?![A-Za-z0-9])", r"_{\1}", t)
    # 同义命令
    t = t.replace("\\to", "\\rightarrow")
    t = t.replace("\\dfrac", "\\frac")
    # 中文全角括号统一
    t = t.replace("（", "(").replace("）", ")")
    t = t.replace("，", ",").replace("。", ".")
    return t.strip()


NUM_RE = re.compile(r"^[-+]?\d+(?:\.\d+)?$")


def to_number(s: str):
    """能解析成数就返回 float，否则 None。支持 `$4$`、`4`、`-1`、`1/2`。"""
    if s is None:
        return None
    t = norm_latex(s)
    if NUM_RE.match(t):
        return float(t)
    m = re.match(r"^(-?\d+)/(\d+)$", t)
    if m:
        return float(m.group(1)) / float(m.group(2))
    return None


CHOICE_RE = re.compile(r"^([A-D])$")   # 保留：报告里用它说明历史缺陷；判定已改用 choice_letter()
# ★ `回忆答案：**C. `&a`**` —— 回忆版把**选项原文**写进了答案里。
#   旧正则压根解析不到这类行（`^\*\*答案` 要求行首就是 `**答案`，而这里是
#   `回忆答案：**…**`），所以 computer/2023.md 的可比对行数是 0。
#   新正则能解析出来了，但 `CHOICE_RE = ^([A-D])$` 不认 `C. `&a``，
#   于是 ① 分支会拿 `C. `&a`` 去跟 B站卡的 `C` 做**全串**比较 → 恒判「不一致」。
#   这是**假不一致**，比不比对还糟：它会让人以为笔记页的答案写错了。
#   所以选择题判定统一走 choice_letter()，只取开头的字母。
#   实测（2026-09-20）：computer/2023.md 45 题里 36 题是这种形态。
CHOICE_PREFIX_RE = re.compile(r"^([A-D])\s*(?:[\.、:：]|$)")


def choice_letter(v: str):
    """从答案值里取选项字母。

    `B` → `B`；`C. `&a`` → `C`；`正确` / `$x^2$` → None（不是选择题答案）。
    """
    if not v:
        return None
    m = CHOICE_PREFIX_RE.match(v.strip())
    return m.group(1) if m else None


def compare_answer(note_ans, bili_ans):
    """返回 (verdict, detail)。verdict ∈ {一致, 表述差异, 不一致, 需人工判定, 笔记缺答案}"""
    if not note_ans:
        return "笔记缺答案", f"B站卡答案 = {bili_ans!r}"
    if not bili_ans:
        return "需人工判定", "B站卡没有答案字段"

    na, ba = norm_latex(note_ans), norm_latex(bili_ans)

    # ① 选择题：字母。★ 只比开头的字母 —— 笔记页可能写成 `C. `&a``（带选项原文），
    #   B站卡写 `C`。全串比较会把它们判成「不一致」（假不一致）。
    ln, lb = choice_letter(na), choice_letter(ba)
    if ln or lb:
        if ln == lb:
            return "一致", "选择题字母相同"
        return "不一致", f"笔记 {note_ans!r} vs B站 {bili_ans!r}"

    # ② 数值
    vn, vb = to_number(note_ans), to_number(bili_ans)
    if vn is not None and vb is not None:
        if abs(vn - vb) < 1e-9:
            return "一致", f"数值相同（{vn:g}）"
        return "不一致", f"数值不同：笔记 {vn:g} vs B站 {vb:g}"

    # ③ 表达式：归一化后相等
    if na == ba:
        return "一致", "归一化后完全相同"

    # ④ 一方是「见解析」这类非答案占位
    PLACEHOLDER = ("见解析", "证明题,无具体数值", "证明题，无具体数值", "略")
    if na in PLACEHOLDER or ba in PLACEHOLDER:
        return "需人工判定", f"一方是占位表述：笔记 {note_ans!r} / B站 {bili_ans!r}"

    # ⑤ 相似度
    r = difflib.SequenceMatcher(None, na, ba).ratio()
    if r >= 0.93:
        return "表述差异", f"相似度 {r:.3f} —— 疑为同一答案的不同写法"
    return "需人工判定", f"相似度 {r:.3f}：笔记 {note_ans!r} vs B站 {bili_ans!r}"


# ── 卷面样板词 ───────────────────────────────────────────────────────────────
# 只用于**过滤缺失片段的报告**，不参与覆盖度计算。
# 理由：B站卡的题面是**卷面原样**（`…=$ ______`、`已知函数…，则…`），
# 笔记页是**人读改写**（`求 …。`）。两者之间「已知 / 函数 / 求 / =______」
# 这些差异是体例，不是内容。全部报出来会把真正的内容缺漏淹掉 ——
# 实测 20 题里 19 题都命中「=______」，噪音率 95%。
# ★ 数学内容（公式、数字、字母、不等式）**不在**这个表里，所以
#   `0<x<1`、`y'+3y=f(x)` 这类真缺漏仍然会被报出来。
BOILER_RE = re.compile(
    r"[=_\s\.。，,；;：:（）()]+"
    r"|已知|设|函数|求|计算|判断|则|下列|以下|其中|上述|该|其|所|中"
    r"|极限|积分|二重积分|定积分|不定积分|区域|直线|曲线|平面|所围成|围成"
    r"|以及|满足方程|满足初始条件|之间|一条|确定|并求|并|的|是|为|在|处|和|与|或|若|由|且|问"
)


def is_boilerplate(seg: str) -> bool:
    """整段都是卷面样板词 / 空白 → 不算「内容缺漏」。"""
    return BOILER_RE.sub("", seg) == ""


def compare_stem(note_stem, bili_stem):
    """题面比对 —— 判据是「B站卡里的内容有多少能在笔记页里找到」，不是字符串相等。

    ★ 为什么不能用「相似度 ≥ 阈值」：
      两边的**体例本来就不一样**，而且这个差异是系统性的 ——
        笔记页（人读）   ：`求 $\\lim_{n\\to\\infty}(2+\\frac1n)$。`
        B站卡（卷面原样）：`$\\lim_{n\\to\\infty}(2+\\dfrac{1}{n})=$ ______`
      同一道题，字符串相似度只有 0.899。把阈值压到 0.85 能过，但那样真正的
      缺漏也会被一起放过 —— 阈值调参在这里是治标。

    ★ 真正要回答的问题是：**B站源里出现了某个条件/数据，笔记页里有没有？**
      所以改成「覆盖度」：用 difflib 的对齐块把「B站有、笔记没有」的片段抠出来，
      覆盖度 = 1 − 缺失长度 / B站长度。返回的 `missing` 就是可直接用于补全的清单。

    返回 (verdict, detail, missing_segments)
    """
    if not note_stem:
        return "笔记缺题面", "", []
    if not bili_stem:
        return "需人工判定", "B站卡没有题面字段", []

    a, b = norm_latex(note_stem), norm_latex(bili_stem)
    if a == b:
        return "一致", "归一化后完全相同", []

    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    missing = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        # insert：b 有、a 没有；replace：两边都有但对不上 —— 两种都算「笔记没覆盖」
        if tag in ("insert", "replace") and j2 > j1:
            missing.append(b[j1:j2])
    miss_len = sum(len(x) for x in missing)
    cov = 1.0 - miss_len / max(len(b), 1)

    # ★ 覆盖度按**原始**缺失长度算（不剔除样板词）—— 否则阈值失去可比性；
    #   但**报告出来的**只保留非样板片段，这样「缺什么」是可直接照着补的。
    notable = [x for x in missing if len(x) >= 2 and not is_boilerplate(x)]
    notable = list(dict.fromkeys(notable))  # 去重，保持顺序

    if cov >= 0.92:
        return "一致", f"覆盖度 {cov:.3f}", notable
    if cov >= 0.70:
        return "表述差异", f"覆盖度 {cov:.3f}", notable
    return "需人工判定", f"覆盖度 {cov:.3f}", notable


def load_cards(bv: str):
    p = ZHENTI_DIR / bv / "extract" / "zhenti.jsonl"
    if not p.exists():
        return None, p
    cards = []
    for ln in p.read_text(encoding="utf-8").split("\n"):
        if ln.strip():
            cards.append(json.loads(ln))
    return cards, p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bv", required=True, help="BV 号")
    ap.add_argument("--page", required=True, help="笔记真题页路径（相对仓库根）")
    ap.add_argument("--json", help="把结构化结果写到这里")
    args = ap.parse_args()

    cards, cp = load_cards(args.bv)
    if cards is None:
        print(f"✗ 找不到真题卡：{cp}")
        return 1
    page = ROOT / args.page
    if not page.exists():
        print(f"✗ 找不到笔记页：{page}")
        return 1

    notes = parse_note_page(page)
    print(f"B站卡：{cp.relative_to(ROOT)} —— {len(cards)} 题")
    print(f"笔记页：{args.page} —— 解析到 {len(notes)} 题")
    print()

    # ★ 空对比护栏（2026-09-20 加）。
    #   解析到 0 题时，下面会为每张卡打印「笔记缺此题」—— 那看起来像一份
    #   正常的「笔记页还没补」报告，实际上**整场对比是空的**，什么都没验。
    #   实测：`--page docs/posts/computer/2026.md` 就是这个情况（那页是
    #   61 行的改革说明，本来就没有题目小节）。分不清「真没题」和
    #   「题头形态不认」是最典型的静默失败，所以这里硬失败。
    if cards and not notes:
        print("✗ 笔记页解析到 0 题 —— 这场对比是**空的**，不是「全都不一致」。")
        print("  本脚本只认 `### 第 N 题` 形态的题头。请确认该页确实有题目小节，")
        print("  或换一个真题页。（`docs/posts/computer/2026.md` 是说明页，无题目。）")
        return 1

    rows = []
    for c in cards:
        no = int(c["q_no"])
        n = notes.get(no)
        if not n:
            rows.append({
                "q_no": no, "topic": "", "stem_verdict": "笔记缺此题",
                "stem_detail": "", "ans_verdict": "笔记缺此题", "ans_detail": "",
                "note_ans": None, "bili_ans": c.get("answer"),
                "note_line": None, "evidence": c.get("evidence"),
            })
            continue
        sv, sd, smiss = compare_stem(n["stem"], c.get("q_text"))
        av, ad = compare_answer(n["answer"], c.get("answer"))
        rows.append({
            "q_no": no, "topic": n["topic"], "stem_verdict": sv, "stem_detail": sd,
            "stem_missing": smiss,
            "ans_verdict": av, "ans_detail": ad,
            "note_ans": n["answer"], "bili_ans": c.get("answer"),
            "note_line": n["line"], "note_ans_line": n["answer_line"],
            "evidence": c.get("evidence"),
        })

    # ★ 第二道空对比护栏：题头认得出，但**一个题号都没配上**。
    #   典型成因是编号体系不同（B站卡用卷面题号、笔记页从小节重新编号），
    #   这时全表都是「笔记缺此题」，同样什么都没验。
    matched = sum(1 for r in rows if r["ans_verdict"] != "笔记缺此题")
    if rows and matched == 0:
        print("✗ 题号一个都没配上（%d 张卡 vs %d 个题号）—— 这场对比是**空的**。"
              % (len(cards), len(notes)))
        print("  多半是两边的编号体系不同（卷面题号 vs 小节编号）。请人工核对。")
        return 1

    w = 4
    print(f"{'题号':<{w}} {'答案':<10} {'题面':<10} 说明")
    print("-" * 78)
    for r in rows:
        print(f"{r['q_no']:<{w}} {r['ans_verdict']:<10} {r['stem_verdict']:<10} {r['ans_detail'][:44]}")

    print()
    from collections import Counter
    print("答案：", dict(Counter(r["ans_verdict"] for r in rows)))
    print("题面：", dict(Counter(r["stem_verdict"] for r in rows)))

    if args.json:
        outp = pathlib.Path(args.json)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(json.dumps({
            "bv": args.bv, "page": args.page, "rows": rows,
        }, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
        print(f"\n结构化结果 → {outp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
