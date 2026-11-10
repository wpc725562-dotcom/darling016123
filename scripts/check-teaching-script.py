#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""教学脚本 / 易错点手册 的防编造验收器。

背景：把 B 站字幕交给免费模型蒸教材，最大的风险不是「蒸得浅」，是「编原话」——
模型会写出很像讲师语气的句子，但字幕里根本没有。人工逐句核对不现实。

## 引文约定（模型必须遵守，否则本脚本核不到）

只有**同时满足**下面两条的「……」才算「原话」，才会被回查：

  1. 由一个含「原话」字样的行引入（例：`**杰哥原话（P64）**：`）
  2. 该行自带集号 `（Pnn）`

随后紧跟的 `>` 引用块，或该行冒号后的内联内容，其中的「」就是待核引文。

⇒ 正文里为了强调而加的「」（如「最后落到的地方」「缺什么补什么」）不会被误判。
⇒ 反过来说：**想引用原话就必须给集号**，给不出集号的「原话」本身就是可疑的。

## 三件可机械判定的事（零模型）

  1. 编号合法性：### X-N 的 X 在本科错因字母白名单内，编号不重复
  2. 集号存在性：出现的 Pnn 必须真的有 subtitle_pNN.txt
  3. 引文回查：原话必须在所引集字幕里能找到（ASR 有错字 ⇒ 用 6-gram 覆盖率）

用法：
  python scripts/check-teaching-script.py <手册.md> [--subject 高数] [--bv BV1Up4y1Y76a]
退出码：0 全过 / 1 有问题 / 2 参数或文件错误
"""
import argparse
import re
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_SUB = REPO / "data" / "bili-analyze"

# 各科错题本的错因字母（与 资料/电子书蒸馏/*/错题本.txt 一致）
SUBJECT_LETTERS = {
    "高数": set("ABCDEF"),
    "计算机": set("ABCDEF"),
    "英语": set("ABCDEF"),
    "政治": set("ABCD"),   # 政治错题本只有四类
    "auto": set("ABCDEF"),
}

RE_BV = re.compile(r"BV[0-9A-Za-z]{10}")
RE_EP = re.compile(r"[Pp](\d{1,3})(?!\d)")
RE_ENTRY = re.compile(r"^###\s+([A-F])-(\d+)\s*(.*)$")
RE_QUOTE = re.compile(r"[「『]([^」』]{6,300})[」』]")
RE_QUOTE_ASCII = re.compile(r"“([^”]{6,300})”")
RE_MARK = re.compile(r"原话")

PUNCT = set("，。、；：？！…—·「」『』“”‘’（）()《》〈〉,.;:?!\"'`~　 \n\r\t")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    return "".join(ch for ch in s if ch not in PUNCT).lower()


def grams(s: str, n: int = 6) -> set:
    return {s[i:i + n] for i in range(max(0, len(s) - n + 1))}


def coverage(quote: str, haystack: str, n: int = 6) -> float:
    q, h = norm(quote), norm(haystack)
    if len(q) < n:
        return 1.0 if q in h else 0.0
    qg, hg = grams(q, n), grams(h, n)
    if not qg:
        return 0.0
    return len(qg & hg) / len(qg)


def eps_in(line: str):
    """取一行的集号；先把 BV 号挖掉，否则 BV1Up4y1Y76a 里的 p4 会被误当集号。"""
    return [int(x) for x in RE_EP.findall(RE_BV.sub("", line))]


def load_sub(sub_dir: Path, ep: int) -> str:
    for name in (f"subtitle_p{ep:02d}.txt", f"subtitle_p{ep}.txt"):
        p = sub_dir / name
        if p.exists():
            return p.read_text(encoding="utf-8", errors="replace")
    return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("doc")
    ap.add_argument("--subject", default="auto")
    ap.add_argument("--sub-dir", default=None)
    ap.add_argument("--bv", default=None)
    ap.add_argument("--thresh", type=float, default=0.75)
    args = ap.parse_args()

    doc = Path(args.doc)
    if not doc.exists():
        print(f"❌ 找不到文件：{doc}", file=sys.stderr)
        return 2
    text = doc.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    letters = SUBJECT_LETTERS.get(args.subject, SUBJECT_LETTERS["auto"])

    if args.sub_dir:
        sub_dir = Path(args.sub_dir)
    elif args.bv:
        sub_dir = DEFAULT_SUB / args.bv
    else:
        m = RE_BV.search(text)
        if not m:
            print("❌ 文档里没有 BV 号，也没给 --sub-dir / --bv", file=sys.stderr)
            return 2
        sub_dir = DEFAULT_SUB / m.group(0)
    if not sub_dir.is_dir():
        print(f"❌ 字幕目录不存在：{sub_dir}", file=sys.stderr)
        return 2

    print(f"手册：{doc.name}")
    print(f"字幕：{sub_dir.name}")
    print(f"科目：{args.subject}（允许错因字母 {'/'.join(sorted(letters))}）")
    print("=" * 62)

    problems = []
    notes = []

    # ---------- 1. 编号合法性 ----------
    entries, seen = [], {}
    for i, line in enumerate(lines, 1):
        m = RE_ENTRY.match(line.strip())
        if not m:
            continue
        letter, num, title = m.group(1), int(m.group(2)), m.group(3)
        entries.append((i, letter, num, title))
        key = f"{letter}-{num}"
        if letter not in letters:
            problems.append(f"行{i} 错因字母 {letter} 不在本科白名单：{title[:30]}")
        if key in seen:
            problems.append(f"行{i} 编号重复 {key}（首次在行{seen[key]}）")
        else:
            seen[key] = i
    print(f"条目：{len(entries)} 条，编号唯一 {len(seen)} 个")
    if not entries:
        problems.append("没有找到任何 ### X-N 条目，格式不对")

    # ---------- 2. 集号存在性 ----------
    eps = sorted({e for line in lines for e in eps_in(line)})
    missing = [e for e in eps if not load_sub(sub_dir, e)]
    if missing:
        problems.append(f"以下集号没有字幕文件：{missing}")
    print(f"集号：{len(eps)} 个" + (f"（P{eps[0]}–P{eps[-1]}）" if eps else ""))

    # ---------- 3. 引文回查 ----------
    # 两种写法都支持：
    #   (a) 标记行冒号后 / 引用块里用「」包住的句子
    #   (b) 引用块里的整段话（没加「」）—— 逐句核
    #
    # 阈值两档（ASR 噪声是常态，不是异常）：
    #   < 0.30  ⇒ ❌ 高度可疑，几乎肯定不是字幕里的话（计入失败）
    #   0.30–0.60 ⇒ ⚠️ 提示，人工扫一眼（ASR 错字 或 我方改写，不算失败）
    #   ≥ 0.60  ⇒ ✅
    # 依据：实测真引文覆盖率 40–74%（「tan」被 ASR 成「弹起来」这类），编造的基本在 0–20%。
    HARD = 0.30
    checked = bad = soft = no_ep = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        if not RE_MARK.search(line) or line.strip().startswith(">"):
            i += 1
            continue
        eps_here = eps_in(line)
        body = []
        # 只取「原话」之后那个冒号后面的内容 —— 否则会把冒号前我方的话（如「三个必错点：…」）
        # 当成引文，产生假阳性。
        m = re.search(r"原话[^：:]{0,12}[：:](.*)$", line)
        if m:
            body.append(m.group(1))
        j = i + 1
        while j < len(lines) and (lines[j].lstrip().startswith(">") or not lines[j].strip()):
            if lines[j].strip():
                body.append(lines[j].lstrip().lstrip(">").strip())
            j += 1
        blob = "\n".join(body)

        quotes = RE_QUOTE.findall(blob) + RE_QUOTE_ASCII.findall(blob)
        if not quotes:
            # 去 LaTeX 定界符但保留内容（\sin → sin），否则会切断 6-gram
            clean = re.sub(r"\$([^$]*)\$", r"\1", blob)
            clean = re.sub(r"\\([a-zA-Z]+)", r"\1", clean)
            clean = re.sub(r"[*_`#>]", "", clean)
            cand = [s for s in re.split(r"[。！？\n]", clean) if len(norm(s)) >= 8]
            # 剔掉明显是我方注解的句子（不是原话）
            quotes = [s for s in cand
                      if not re.match(r"^\s*(例|（|\(|注|即|用|这|⇒)", s.strip())
                      and "⇒" not in s]

        if quotes and not eps_here:
            no_ep += len(quotes)
            problems.append(f"行{i+1} 引了原话但没给集号（核不了）：{quotes[0][:50]}")
        elif quotes:
            hay = "\n".join(load_sub(sub_dir, e) for e in eps_here)
            for q in quotes:
                checked += 1
                cov = coverage(q, hay)
                if cov < HARD:
                    bad += 1
                    problems.append(
                        f"行{i+1} ❌ 引文高度可疑（覆盖 {cov:.0%} < {HARD:.0%}）"
                        f"｜集 {eps_here}\n    引文：{q[:80]}")
                elif cov < args.thresh:
                    soft += 1
                    notes.append(
                        f"行{i+1} ⚠️ 覆盖率偏低 {cov:.0%}｜集 {eps_here}"
                        f"｜{q[:60]}")
        i = j if j > i else i + 1

    print(f"引文：核查 {checked} 处，高度可疑 {bad} 处" +
          (f"，覆盖率偏低 {soft} 处" if soft else "") +
          (f"，缺集号 {no_ep} 处" if no_ep else ""))

    # ---------- 汇总 ----------
    print("=" * 62)
    if notes:
        print(f"⚠️ {len(notes)} 处覆盖率偏低（可能是 ASR 错字或我方改写，扫一眼即可）：\n")
        for n in notes:
            print("  · " + n)
        print()
    if problems:
        print(f"❌ {len(problems)} 个必须修的问题：\n")
        for p in problems:
            print("  · " + p)
        return 1
    print("✅ 通过：编号合法、集号存在、无高度可疑引文")
    if soft:
        print(f"   （另有 {soft} 处覆盖率偏低，见上，不影响通过）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
