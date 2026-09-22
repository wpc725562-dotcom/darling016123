#!/usr/bin/env python3
"""阶段 ③ 真题解析器 —— 逐字稿 × 画面帧 → 真题卡。

════════════════════════════════════════════════════════════════════════
为什么要有这一层（而不是直接让 ② 的产物进站）
════════════════════════════════════════════════════════════════════════

② 的产物是「一段 2 万字的口播 + 60 张截图」，对人是不可读的：
  · 口播里有大量「呃 / 对吧 / 我们来看一下」和 UP 的招生话术；
  · **题面在画面里**，字幕里一个字都没有 —— 只看字幕永远不知道题目是什么。

这一层把两者**按题号对齐**，产出一张张真题卡：

    {q_no, q_type, q_text, options, answer, steps, pitfalls,
     t_start, t_end, evidence}

其中 `evidence` 是硬字段：每个字段都要能指回「哪一帧」或「哪一秒」。

════════════════════════════════════════════════════════════════════════
职责边界（★ 重要）
════════════════════════════════════════════════════════════════════════

本脚本**只做机械对齐**，不做语义提炼：

  它负责                              它不负责
  ─────────────────────────────       ─────────────────────────────
  把逐字稿按题号切段                    读画面、认题面（这需要多模态）
  算出每段的 [t_start, t_end]           写解析、判对错
  挑出该时段内的候选帧                  决定哪道题值得进站
  生成「工作单」给下一步用

所以它的产物是 `_worksheet.*`（工作单），**不是**最终的 `zhenti.jsonl`。
填题面这一步由 agent 读帧完成 —— 这符合启动提示词 §1.2
「不做一键全自动无人值守、宁可每步可中断可检查」。

════════════════════════════════════════════════════════════════════════
用法
════════════════════════════════════════════════════════════════════════

    python scripts/bili_zhenti_extract.py BV1Z4w3znE6h            # 单视频
    python scripts/bili_zhenti_extract.py BV1Z4w3znE6h --page 5   # 只做第 5 P
    python scripts/bili_zhenti_extract.py --all                   # 所有已取内容的
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent / "data" / "bili-zhenti"

# ------------------------------------------------------------------ 题号解析

_CN_DIGIT = {"零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
             "六": 6, "七": 7, "八": 8, "九": 9}


def cn2int(s: str) -> int | None:
    """中文数字 → int，支持 1~99（「一」「十」「十一」「二十」「二十三」）。

    ★ 为什么不用现成的库：这一层是纯字符串处理，引第三方库反而增加
      「语料白名单」之外的依赖（启动提示词 §4 要求语料一律走白名单）。
    """
    s = s.strip()
    if not s:
        return None
    if s.isdigit():
        return int(s)
    if s == "十":
        return 10
    if "十" in s:
        head, _, tail = s.partition("十")
        tens = _CN_DIGIT.get(head, 1) if head else 1
        ones = _CN_DIGIT.get(tail, 0) if tail else 0
        if head and head not in _CN_DIGIT:
            return None
        if tail and tail not in _CN_DIGIT:
            return None
        return tens * 10 + ones
    if len(s) == 1 and s in _CN_DIGIT:
        return _CN_DIGIT[s]
    return None


_NUM = r"(?:[0-9]{1,3}|[零一二三四五六七八九十]{1,3})"

# 题型词 —— 可出现在「第X道」和「题」之间
_TYPE = (r"(?:单选题|多选题|选择题|判断题|填空题|简答题|编程题|综合分析题|综合题|"
         r"分析题|计算题|应用题|辨析题|论述题|材料分析题|案例题|小)")

# 大题号：「第一题」「第 12 题」「第三道题」「第一道编程题」
#   ★ 「第X个」必须排除 —— 「考试真正考的通常是第一个或者第二个公式」里的
#     「第一个」不是题号，早期把「个」放进可选分支，整段被误切成「第1题」。
#   ★ 「第X问」也必须排除 —— 它是**小问**，不是大题。见 SUBQ_RE。
QNO_RE = re.compile(
    r"第\s*(%s)\s*(?:道\s*(?:%s)?|[题])" % (_NUM, _TYPE))

# 小问：「第一问」「第2问」—— 记录成线索，但**不作为大题边界**。
SUBQ_RE = re.compile(r"第\s*(%s)\s*问" % _NUM)

# 「一、选择题」「二、判断题」「六、编程题」—— 大题分节
SECTION_RE = re.compile(
    r"^\s*[（(]?\s*([一二三四五六七八九十])\s*[）)]?\s*[、.．,，]?\s*"
    r"(单选题|多选题|选择题|判断题|填空题|简答题|编程题|综合分析题|综合题|"
    r"分析题|计算题|应用题|辨析题|论述题|材料分析题|案例题)")

# 只提题型名，不带序号（「接下来我们看判断题」）
TYPE_ONLY_RE = re.compile(
    r"(单选题|多选题|选择题|判断题|填空题|简答题|编程题|综合分析题|综合题|"
    r"分析题|计算题|应用题|辨析题|论述题|材料分析题|案例题)")

# 明确的「翻页/换题」信号 —— 这些出现时，即便没读到题号也要切段
NEXT_Q_RE = re.compile(
    r"(下一题|下一道|接下来(?:我们)?(?:来)?(?:看|讲|做)|再来看|"
    r"我们(?:来)?看第|来看第|看第)")

# 纯噪音行（片头片尾 / 招生话术 / 语气词）
NOISE_RE = re.compile(
    r"^(?:嗯+|啊+|哦+|呃+|额+|好+|OK|ok|对|对吧|是吧|然后呢?|那么|"
    r"各位同学(?:大家)?好|大家好|同学们好|哈喽|拜拜|谢谢(?:大家)?(?:观看)?|"
    r"记得(?:一键)?三连|点个关注|关注我|加(?:一下)?(?:QQ|qq|微信)群)[。！!？?…\s]*$")

TS_RE = re.compile(r"^\[(\d{1,2}):(\d{2})\]\s*(.*)$")


def parse_lines(text: str) -> list[tuple[float, str]]:
    """逐字稿 → [(秒, 文本)]。

    ★ 两种来源的格式不同，必须都能吃：
      · ASR 产物：每 300 秒一段，段首带 `[MM:SS]`
      · 字幕产物：每行一条（已由 srt_to_timed_text 加上 `[MM:SS]`）
      没有时间戳的行 → 继承上一行的秒数（宁可粗一点，也不能丢内容）。
    """
    out: list[tuple[float, str]] = []
    cur = 0.0
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith(">"):
            continue
        m = TS_RE.match(line)
        if m:
            cur = int(m.group(1)) * 60 + int(m.group(2))
            line = m.group(3).strip()
        if line:
            out.append((cur, line))
    return out


def mmss(sec: float) -> str:
    s = int(sec)
    return "%02d:%02d:%02d" % (s // 3600, (s % 3600) // 60, s % 60)


# ------------------------------------------------------------------ 切段

def segment(lines: list[tuple[float, str]], duration: float) -> list[dict]:
    """把逐字稿切成「题」段。

    策略（按优先级）：
      1. 显式题号「第X题」→ 新段
      2. 大题分节「三、填空题」→ 新段，并更新 section
      3. 换题信号「下一题 / 接下来我们看」→ 新段（但只在已有内容时才切）

    ★ 为什么保留「无题号段」而不是丢掉：很多 UP 讲选择题时只说
      「选C，因为…」而从不报题号。丢掉这些段等于丢掉半份卷子。
      所以无题号的内容挂到「上一题」下面，并在卡里标记 `q_no: null`。
    """
    segs: list[dict] = []
    cur: dict | None = None
    section = ""
    seen: set[int] = set()          # 本页已出现过的大题号
    local_used = False              # 本节是否已用过「本节第一道」这类引用

    def new_seg(q_no, q_type, t):
        return {"q_no": q_no, "q_type": q_type, "section": section,
                "t_start": t, "t_end": t, "lines": []}

    for t, line in lines:
        sec_m = SECTION_RE.match(line)
        if sec_m:
            section = sec_m.group(2)
            local_used = False
            cur = new_seg(None, section, t)
            cur["lines"].append(line)
            segs.append(cur)
            continue

        q_m = QNO_RE.search(line)
        if q_m:
            n = cn2int(q_m.group(1))
            # ★ 同一题号的复述不切段。
            #   实测：UP 在讲一道编程题时会反复说「第一题…第一题这里…第一题」，
            #   每次都切的话一道题会碎成 6~8 段，工作单直接不可读。
            #   只有题号**变化**（或首次出现）才算新题边界。
            if n is not None and cur is not None and cur.get("q_no") == n:
                cur["lines"].append(line)
                cur["t_end"] = t
                continue
            # ★ 「第一道」在大题内部是**本节第一道**的意思，不是全卷第 1 题。
            #   实测 BV1Y3L36bEf1 P3：UP 说「第一道还是极限的计算问题」，
            #   紧接着下一段就是「下面我们看第12题」—— 说明它是第 11 题。
            #   判据：n==1 且本页已经出现过 >=3 的大题号 → 视为本节引用，
            #   题号置空（保留 q_no_local 线索），仍然切段（它确实是新题）。
            if n == 1 and len(seen) >= 3:
                n = None
                if not local_used:
                    local_used = True
                else:
                    cur["lines"].append(line)
                    cur["t_end"] = t
                    continue
            if n is not None:
                seen.add(n)
            if cur is not None:
                cur["t_end"] = t
            qtype = ""
            tm = TYPE_ONLY_RE.search(line)
            if tm:
                qtype = tm.group(1)
            cur = new_seg(n, qtype or section, t)
            if n is None:
                cur["q_no_local"] = 1
            cur["lines"].append(line)
            segs.append(cur)
            continue

        # 小问「第一问」「第2问」—— 只记线索，不切段
        sq = SUBQ_RE.search(line)
        if sq and cur is not None:
            k = cn2int(sq.group(1))
            if k is not None:
                cur.setdefault("sub_q", [])
                if k not in cur["sub_q"]:
                    cur["sub_q"].append(k)

        if cur is None:
            # 视频开头还没出现任何题号 —— 先开一个占位段，内容不丢
            cur = new_seg(None, "", t)
            segs.append(cur)
        elif NEXT_Q_RE.search(line) and len(cur["lines"]) >= 3:
            # 有换题信号且当前段已有实质内容 → 切新段（题号未知）
            cur["t_end"] = t
            cur = new_seg(None, section, t)
            segs.append(cur)

        cur["lines"].append(line)
        cur["t_end"] = t

    for s in segs:
        s["t_end"] = min(max(s["t_end"], s["t_start"]), duration)
        s["chars"] = sum(len(x) for x in s["lines"])
    return segs


def fix_local_numbering(segs: list[dict]) -> list[dict]:
    """把「本节第一道」误标成的 `第1题` 降级。

    ★ 实测场景（BV1Y3L36bEf1 P3）：本页是计算题，实际从第 11 题开始，
      但 UP 开口说「第一道还是极限的计算问题」—— 这里的「第一道」是
      **本节第一道**，不是全卷第 1 题。紧接着下一段就是「第12题」。

    判据：某段的 q_no==1，而**下一个带题号的段** q_no >= 6 → 判定为节内引用。
      只靠「本页最大题号」不够：单选题本来就是 1~5，会被误伤。
      靠「下一个题号」则很干净 —— 第1题后面跟第2题是正常的，
      第1题后面直接跳到第12题就一定是节内引用。
    """
    idx = [i for i, s in enumerate(segs) if s.get("q_no") is not None]
    for k, i in enumerate(idx):
        if segs[i]["q_no"] != 1:
            continue
        nxt = next((segs[j]["q_no"] for j in idx[k + 1:]), None)
        if nxt is not None and nxt >= 6:
            segs[i]["q_no"] = None
            segs[i]["q_no_local"] = 1
    return segs


def merge_fragments(segs: list[dict], min_chars: int = 30,
                    gap: float = 45.0) -> list[dict]:
    """把「碎片段」并入后一段。

    ★ 为什么需要：UP 常顺口连报题号 ——「第二题，第三题，我们来看第三题」——
      于是切出「第2题」(13 字)「第3题」(12 字) 两个空壳，真内容在第三段。
      这类空壳如果留在工作单里，agent 会照着它去帧里找一道根本不存在的题。

    判据：字符数 < min_chars **且** 与下一段间隔 <= gap 秒。
    两者都要满足 —— 只按字符数会把「最后一道题只讲了 20 字」这种真结尾也吞掉。
    被并入的题号记进 `q_no_hints`，不直接丢弃：它仍是一条线索。
    """
    out: list[dict] = []
    pending: dict | None = None
    for s in segs:
        if pending is not None:
            if s["t_start"] - pending["t_end"] <= gap:
                s["lines"] = pending["lines"] + s["lines"]
                s["chars"] += pending["chars"]
                s["t_start"] = pending["t_start"]
                if pending["q_no"] is not None and pending["q_no"] != s["q_no"]:
                    s.setdefault("q_no_hints", []).append(pending["q_no"])
                if pending.get("q_type") and not s.get("q_type"):
                    s["q_type"] = pending["q_type"]
                pending = None
            else:
                out.append(pending)
                pending = None
        if s["chars"] < min_chars:
            pending = s
        else:
            out.append(s)
    if pending is not None:
        out.append(pending)
    return out


# ------------------------------------------------------------------ 帧对齐

def load_frame_index(frames_dir: pathlib.Path) -> dict[str, float]:
    p = frames_dir / "_index.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            # ★ A6（2026-09-20）：原来坏掉就 `pass`，直接掉进下面的 fpm=1 兜底。
            #   于是「索引存在但坏了」和「索引本来就没有（老产物）」表现完全一样 ——
            #   而两者的后果天差地别：前者会用**错误的 fps** 算出**错误的秒数**，
            #   卡片上标的「第 12 秒」就这么错了，且没有任何迹象。
            print("  [警告] %s 存在但无法解析（%s）—— 退回 fpm=1 兜底，"
                  "本目录的帧→秒映射**可能不准**（该目录用了非 1 的 --fpm 就会全错）。"
                  % (p, e), file=sys.stderr, flush=True)
    # 兜底：按 fpm=1 反推（老产物）。只在**没有索引**时才是可靠的。
    idx = {}
    for f in sorted(frames_dir.glob("p*_*.jpg")):
        try:
            i = int(f.stem.rsplit("_", 1)[1])
        except (IndexError, ValueError):
            continue
        idx[f.name] = float((i - 1) * 60)
    return idx


def frames_for(seg: dict, page: int, index: dict[str, float]) -> list[dict]:
    """挑出该时段内的候选帧。

    ★ 前后各多带一帧：题面往往在 UP 开口讲之前就已经显示在画面上了，
      严格按 [t_start, t_end] 取会漏掉题面那一帧。
    """
    tag = "p%02d" % page
    items = sorted(((n, t) for n, t in index.items() if n.startswith(tag + "_")),
                   key=lambda x: x[1])
    if not items:
        return []
    inside = [(n, t) for n, t in items if seg["t_start"] - 1 <= t <= seg["t_end"] + 1]
    if not inside:
        # 段太短 / 落在两帧之间 → 取时间上最近的一帧
        n, t = min(items, key=lambda x: abs(x[1] - seg["t_start"]))
        inside = [(n, t)]
    i0 = next(i for i, (n, _) in enumerate(items) if n == inside[0][0])
    i1 = next(i for i, (n, _) in enumerate(items) if n == inside[-1][0])
    lo, hi = max(0, i0 - 1), min(len(items) - 1, i1 + 1)
    return [{"file": items[i][0], "t": items[i][1]} for i in range(lo, hi + 1)]


# ------------------------------------------------------------------ 输出

def build_worksheet(bvdir: pathlib.Path, page: int, meta: dict) -> dict | None:
    tr = bvdir / ("transcript_p%02d.md" % page)
    if not tr.exists() or tr.stat().st_size == 0:
        return None
    pg = next((p for p in meta["pages"] if p["page"] == page), None)
    if not pg:
        return None

    lines = parse_lines(tr.read_text(encoding="utf-8"))
    # 噪音行只在「单独成段」时剔除，避免把正文里的「好，我们看」切碎
    segs = segment(lines, pg["duration"])
    index = load_frame_index(bvdir / "frames")

    kept = []
    for s in segs:
        body = [x for x in s["lines"] if not NOISE_RE.match(x)]
        if not body:
            continue
        s["lines"] = body
        s["chars"] = sum(len(x) for x in body)
        kept.append(s)

    kept = merge_fragments(kept)
    kept = fix_local_numbering(kept)
    for s in kept:
        s["frames"] = frames_for(s, page, index)

    # ★ `Path.glob()` 返回的是**生成器**，生成器对象永远 truthy ——
    #   `if (bvdir / "subs").glob(...)` 恒为真，于是 source 字段永远是
    #   "subtitle"，"asr" 分支是死代码。实测：
    #       bool(Path("/不存在的目录").glob("P01.*.txt")) == True
    #   下游只要用它区分「人工字幕 / 机器识别」，判断就全错，而且是
    #   全部偏向同一侧（不是随机错），更难察觉。必须用 any() 真正迭代。
    has_sub = any((bvdir / "subs").glob("P%02d.*.txt" % page))
    # ★ `_quarantine.json` 存在但内容损坏（上次写入被打断）时，
    #   原来的裸 json.loads 会直接抛异常终止整批提取，把前面已跑好的结果一起丢。
    quarantined = 0
    qj = bvdir / "_quarantine.json"
    if qj.exists():
        try:
            quarantined = len(json.loads(qj.read_text(encoding="utf-8")))
        except Exception as e:
            print("  [警告] %s 无法解析（%s），按 0 计" % (qj.name, e))

    return {
        "bvid": meta["bvid"],
        "title": meta["title"],
        "owner": meta["owner"],
        "page": page,
        "part": pg["part"],
        "duration": pg["duration"],
        "source": "subtitle" if has_sub else "asr",
        "quarantined": quarantined,
        "n_segments": len(kept),
        "segments": kept,
    }


def render_md(ws: dict) -> str:
    L = []
    A = L.append
    A("# 真题解析工作单 · %s" % ws["title"])
    A("")
    A("- BV：`%s`  · UP：%s" % (ws["bvid"], ws["owner"]))
    A("- 分P：P%d %s  · 时长 %ss" % (ws["page"], ws["part"], ws["duration"]))
    A("- 文字来源：%s  · 切出 %d 段" % (ws["source"], ws["n_segments"]))
    if ws["quarantined"]:
        A("- ⚠️ 该视频有 %d 条字幕轨被隔离（未进本工作单）" % ws["quarantined"])
    A("")
    A("> 用法：读每段的候选帧 → 填 `q_text / options / answer`，")
    A("> 口播只提供 `steps / pitfalls`。**题面以画面为准，不以口播为准。**")
    A("")
    for i, s in enumerate(ws["segments"], 1):
        A("---")
        A("")
        hints = s.get("q_no_hints") or []
        sq = s.get("sub_q") or []
        A("## 段 %d · %s%s%s%s" % (
            i,
            "第 %s 题" % s["q_no"] if s["q_no"] else
            ("（本节第 1 道，全卷题号待定）" if s.get("q_no_local") else "（未报题号）"),
            "  ·  %s" % s["q_type"] if s["q_type"] else "",
            "  ·  含小问 %s" % "/".join(str(x) for x in sq) if sq else "",
            "  ·  ⚠️ 前置提到过第 %s 题，注意别混"
            % "/".join(str(x) for x in hints) if hints else ""))
        A("")
        A("时间 `%s` → `%s`  ·  %d 字  ·  候选帧 %d 张"
          % (mmss(s["t_start"]), mmss(s["t_end"]), s["chars"], len(s["frames"])))
        A("")
        if s["frames"]:
            A("候选帧：" + "  ".join("`%s`(%s)" % (f["file"], mmss(f["t"]))
                                     for f in s["frames"][:12]))
            if len(s["frames"]) > 12:
                A("（另有 %d 张，见 json）" % (len(s["frames"]) - 12))
            A("")
        A("口播：")
        A("")
        A("```")
        for x in s["lines"][:40]:
            A(x)
        if len(s["lines"]) > 40:
            A("…（另 %d 行）" % (len(s["lines"]) - 40))
        A("```")
        A("")
    return "\n".join(L)


# ------------------------------------------------------------------ 主流程

def die(msg: str, code: int = 5):
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("bvid", nargs="?", default=None)
    ap.add_argument("--all", action="store_true", help="处理所有已取内容的视频")
    ap.add_argument("--page", type=int, default=None, help="只做指定分P")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    out_root = pathlib.Path(a.out) if a.out else ROOT
    if not out_root.exists():
        die("找不到产物目录：%s（先跑 bili_zhenti.py --stage content）" % out_root)

    targets = []
    if a.all:
        targets = [d for d in sorted(out_root.iterdir())
                   if d.is_dir() and d.name.startswith("BV") and (d / "meta.json").exists()]
    elif a.bvid:
        d = out_root / a.bvid
        if not (d / "meta.json").exists():
            die("没有 %s 的 meta.json" % a.bvid, 3)
        targets = [d]
    else:
        die("给一个 BV 号，或用 --all", 5)

    total_seg = 0
    for bvdir in targets:
        meta = json.loads((bvdir / "meta.json").read_text(encoding="utf-8"))
        pages = [a.page] if a.page else [p["page"] for p in meta["pages"]]
        made = []
        for pg in pages:
            ws = build_worksheet(bvdir, pg, meta)
            if not ws:
                continue
            ex = bvdir / "extract"
            ex.mkdir(parents=True, exist_ok=True)
            (ex / ("worksheet_p%02d.json" % pg)).write_text(
                json.dumps(ws, ensure_ascii=False, indent=1) + "\n", encoding="utf-8",
                newline="\n")
            (ex / ("worksheet_p%02d.md" % pg)).write_text(
                render_md(ws), encoding="utf-8", newline="\n")
            made.append((pg, ws["n_segments"], ws["source"]))
            total_seg += ws["n_segments"]

        if made:
            print("%s  %s" % (bvdir.name, meta["title"][:40]))
            for pg, n, src in made:
                print("    P%-3d %3d 段  来源=%s" % (pg, n, src))
            # 回写 stage 状态
            st = meta.setdefault("stages", {})
            st["extract"] = "worksheet"
            meta["extract_at"] = dt.datetime.now().isoformat(timespec="seconds")
            (bvdir / "meta.json").write_text(
                json.dumps(meta, ensure_ascii=False, indent=1) + "\n", encoding="utf-8",
                newline="\n")

    print("\n共切出 %d 段。工作单在 <BV>/extract/worksheet_p*.{md,json}" % total_seg)
    print("下一步：读候选帧填题面 → zhenti.jsonl（由 agent 完成，非本脚本）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
