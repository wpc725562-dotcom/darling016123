#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scripts/zhenti_lint.py —— 真题页模板合规检查 / 自动修复。

背景：真题页统一格式后，最容易出问题的地方不是内容，而是 **Markdown 容器的空行**。
`::: details xxx` 之后若紧跟表格或加粗文本（没有空行），markdown-it 不会把它当块级元素解析 ——
页面照常打开、不报错，但表格会退化成一堆竖线文字。这种失败**肉眼扫代码看不出来**，必须机器查。

用法：
    python scripts/zhenti_lint.py docs/posts/math/2025.md            # 只检查
    python scripts/zhenti_lint.py docs/posts/math/2025.md --fix      # 修可自动修的
    python scripts/zhenti_lint.py docs/posts/math/*.md --fix         # 批量
"""

import argparse
import json
import pathlib
import re
import sys

# 本脚本现在依赖同级模块 zhenti_log，显式把 scripts/ 加进 sys.path ——
# 调用方可能从任意 cwd 起（`zhenti_convert.py` 也会 import 本模块），
# 光靠「同目录」在 `python -m scripts.zhenti_lint` 下是 import 不到的。
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

# ★ E3（2026-09-20）：诊断走 logging（stderr），正式输出仍走 print（stdout）。
#   两者必须分开 —— `--json` 会把整个 stdout 重定向到 stderr 再只打一个 JSON，
#   诊断若混在 stdout 里就会污染机器可读输出。
from zhenti_log import add_logging_args, get_logger, setup_from_args  # noqa: E402

LOG = get_logger(__name__)

# ───────────────────────── 检查项 ─────────────────────────

TITLE_RE = re.compile(r"^###\s+(.+)$", re.M)
# 合规的题号标题：### 第 N 题 · 主题
GOOD_QNO_RE = re.compile(r"^###\s+第\s*\d+\s*题\s*·\s*\S")
# 光秃秃的题号标题（没主题名）
BARE_QNO_RE = re.compile(r"^###\s+第\s*\d+\s*题\s*$")
# 两种旧体例
BAD_QNO_PATTERNS = [
    (re.compile(r"^###\s+\d+\.\s"), "旧体例 `### 1. …`"),
    (re.compile(r"^###\s+第\s*\d+\s*题[：:]"), "旧体例 `### 第 N 题：…`（中文冒号）"),
]
# 大题标题：中文序号（`## 一、单项选择题`）或英语卷的 `## Part I 词汇语法`
SECTION_RE = re.compile(r"^##\s+(?:[一二三四五六七八九十]+、|Part\s+[IVX]+\s)")
DETAILS_OPEN_RE = re.compile(r"^:::+\s*details\b")
FENCE_RE = re.compile(r"^:::+\s*$")


def fix_container_blank_lines(text: str) -> tuple[str, int]:
    """给 ::: 容器标记的内外侧补空行。

    只改「标记行与其相邻内容之间」的空行，不动容器内部内容 —— 这是可逆且安全的。
    返回 (新文本, 修复处数)。
    """
    lines = text.split("\n")
    out: list[str] = []
    fixed = 0
    for i, ln in enumerate(lines):
        s = ln.strip()
        is_close = s == ":::"
        is_open = s.startswith(":::") and not is_close

        # 闭标记前要有空行
        if is_close and out and out[-1].strip() != "":
            out.append("")
            fixed += 1
        out.append(ln)
        # 开标记后要有空行
        if is_open and i + 1 < len(lines) and lines[i + 1].strip() != "":
            out.append("")
            fixed += 1
    return "\n".join(out), fixed


def check(path: pathlib.Path, text: str) -> list[str]:
    """返回问题列表（人类可读）。"""
    problems: list[str] = []
    lines = text.split("\n")

    # ── frontmatter ──
    if not text.startswith("---\n"):
        problems.append("缺 frontmatter")
    else:
        fm_end = text.find("\n---", 4)
        fm = text[4:fm_end] if fm_end > 0 else ""
        for key in ("title", "year", "subject", "description"):
            if not re.search(rf"^{key}\s*:", fm, re.M):
                problems.append(f"frontmatter 缺 `{key}`")
        # year 必须带引号（YAML 里 2025 会被解析成整数）
        m = re.search(r"^year\s*:\s*(.+)$", fm, re.M)
        if m and not m.group(1).strip().startswith(('"', "'")):
            problems.append("`year` 未加引号（会被 YAML 当整数解析）")

    # ── 容器空行 ──
    _, nfix = fix_container_blank_lines(text)
    if nfix:
        problems.append(f"::: 容器内外缺空行 {nfix} 处（--fix 可自动修）")

    # ── 题号标题体例 ──
    for ln in lines:
        for pat, label in BAD_QNO_PATTERNS:
            if pat.match(ln):
                problems.append(f"{label} → {ln[:46]}")
                break

    # ── 主题名：只查「这一页本来就在用主题名」的页面 ──
    #   ★ 为什么改成条件检查：英语刷题版（2019–2024）的源文件里根本没有
    #     逐题考点信息 —— 阅读/完形/七选五这些题型「每题考什么」就是题型本身，
    #     硬编一个主题名只会变成跟大题标题重复的噪音。
    #     但 2026 高数、2020 英语精析版这种**逐题有考点**的页面必须写全，
    #     漏一个就是漏了一个可扫读的索引。判据：页面里出现过任意一个
    #     `### 第 N 题 · 主题`，就按「全页都要有」来查。
    if any(GOOD_QNO_RE.match(ln) for ln in lines):
        for ln in lines:
            if BARE_QNO_RE.match(ln):
                problems.append(f"缺主题名（本页其它题都写了） → {ln[:46]}")

    # ── 大题标题必须带分值 ──
    for ln in lines:
        if SECTION_RE.match(ln) and "分" not in ln:
            problems.append(f"大题标题缺分值 → {ln[:46]}")

    # ── 结构完整性 ──
    if "## 试卷结构" not in text:
        problems.append("缺 `## 试卷结构` 章节")
    if "## 题目一览" not in text:
        problems.append("缺 `## 题目一览` 章节")

    # ── 裸 LaTeX 残留（没有 $ 包裹的 \frac 等）──
    #   ★ 必须跟踪 `$$` 块与代码围栏：2026 的解析写成
    #       $$
    #       \lim_{x\to0}\frac{\sin4x}{x}
    #       $$
    #     块内那几行天然不带 `$`，早期版本会逐行报「裸 LaTeX」——
    #     是误报，不是真问题。误报多了这个检查就没人看了。
    in_display = False
    in_fence = False
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if s.count("$$") % 2 == 1:
            in_display = not in_display
            continue
        if in_display:
            continue
        if re.search(r"(?<!\$)\\(frac|dfrac|lim|int|sum|sqrt)\b", ln) and "$" not in ln:
            problems.append(f"第 {i} 行可能有裸 LaTeX：{ln[:40]}")
            break

    # ── details 数量与题目数量是否匹配（每题一个答案块）──
    n_q = len([l for l in lines if GOOD_QNO_RE.match(l)])
    n_det = len([l for l in lines if DETAILS_OPEN_RE.match(l)])
    if n_q and n_det < n_q:
        problems.append(f"题目 {n_q} 道，但 `::: details` 只有 {n_det} 个（每题都该有答案块）")

    return problems


QNO_HDR_RE = re.compile(r"^###\s*第\s*(\d{1,3})\s*题", re.M)


def check_config(cfg_path: pathlib.Path, text: str) -> list:
    """配置 ↔ 页面 的一致性检查（2026-09-20，修 D2 / D3）。

    契约见 `scripts/zhenti_cfg/SCHEMA.md`：
      · `total`   = **全卷** [题量, 满分]（不是「本页有多少题」）
      · `covered` = 本页已还原的题量；省略则默认 = `total[0]`
      · `sections[name]` = **全卷**该大题的 [题号区间, 卷面小题数, 分值]，
        用于「试卷结构」表 —— 它描述整张卷子，不是本页。
        ★ 校验的是**题号区间的覆盖**，不是「卷面小题数 == 题号个数」：
          材料分析题是 1 小题占 2 个题号，拿后者去比前者会误报。

    返回 `[(severity, msg)]`，`severity ∈ {'fail', 'note'}`。
    `note` = 配置里已用 `gap_note` 显式承认的缺口，报出来但不判失败。

    ★ 为什么需要它：修复前**没有任何地方**会发现
      「配置声明 21–30（10 题），页面只有 21–28（8 题）」——
      配置、页面、报告三方都沉默，学习者看到的是「这章只有 8 题」。
    """
    out = []
    fail = lambda m: out.append(("fail", m))
    note = lambda m: out.append(("note", m))

    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    except Exception as e:
        return [("fail", f"配置无法读取：{type(e).__name__}: {e}")]

    nos = [int(x) for x in QNO_HDR_RE.findall(text)]
    actual = len(nos)
    gap_note = cfg.get("gap_note")
    acknowledge = (lambda m: note(m)) if gap_note else (lambda m: fail(m))

    total = cfg.get("total")
    covered = cfg.get("covered")
    tq = None
    if not isinstance(total, (list, tuple)) or len(total) != 2:
        fail("total 必须是 [题量, 满分] 两元组（语义见 zhenti_cfg/SCHEMA.md）")
    else:
        try:
            tq = int(total[0])
        except (TypeError, ValueError):
            fail(f"total[0] 不是数字：{total[0]!r}")

    if tq is not None:
        declared = None
        if covered is None:
            declared = tq
        else:
            try:
                declared = int(covered)
            except (TypeError, ValueError):
                fail(f"covered 不是数字：{covered!r}")
        if declared is not None:
            if actual != declared:
                field = "total[0]" if covered is None else "covered"
                fail(f"页面实际 {actual} 题，但 {field} 声明 {declared} 题"
                     f"（差 {actual - declared:+d}）")
            if covered is not None and declared < tq:
                if gap_note:
                    note(f"本页覆盖 {declared}/{tq} 题（已声明：{gap_note}）")
                else:
                    fail(f"covered={declared} < total[0]={tq}"
                         f"（本页只还原了全卷的一部分），但没有 gap_note 说明缺口")

    for name, v in (cfg.get("sections") or {}).items():
        if not isinstance(v, (list, tuple)) or len(v) < 2:
            fail(f"sections[{name}] 必须是 [题号区间, 题量, 分值]")
            continue
        rng, cnt = v[0], v[1]
        if rng is None:
            continue          # 显式声明「本节无题号」，合法
        s = str(rng).strip().replace("–", "-").replace("—", "-")
        parts = [p.strip() for p in s.split("-") if p.strip()]
        try:
            lo = int(parts[0])
            hi = int(parts[-1]) if len(parts) > 1 else lo
        except (ValueError, IndexError):
            fail(f"sections[{name}][0] 区间解析不出题号：{rng!r}"
                 f"（该节确实无题号请写 null）")
            continue
        slots = hi - lo + 1

        got = sum(1 for x in nos if lo <= x <= hi)
        # ★ `got == 0` → 本节本页未还原（如「其余各段以摘要保留」）。
        #   这不是缺口，而是**覆盖范围**问题，已由 covered / gap_note 统一表达。
        #   只有「开了头没做完」（本节有题但不够）才算缺口。
        if got == 0:
            continue
        # ★ 判据是**区间覆盖**，不是「题量列 == 题号个数」（2026-09-20 修正）。
        #   一开始我把 `sections[name][1]` 当题号个数去比，于是
        #   politics2023「六、材料分析题 37–38 / 1（两问）」被判成「不是数字」。
        #   那是**误报** —— 题量列写的是**卷面小题数**，而材料分析题本就是
        #   1 小题占 2 个题号。两列语义不同，拿一个去校验另一个必然出错。
        #   现在：区间覆盖不全 → 缺口（由 gap_note 决定 fail / note）；
        #   题量列只在「纯整数且与题号个数不符」时提示一句，不判失败。
        if got != slots:
            miss = sorted(set(range(lo, hi + 1)) - set(nos))
            extra = f"，缺 {len(miss)} 题：{miss}" if miss else ""
            acknowledge(f"sections[{name}]：声明 {rng}（{slots} 个题号），"
                        f"页面只有 {got} 个{extra}")
        try:
            want = int(cnt)
        except (TypeError, ValueError):
            want = None      # 形如 `1（两问）` 的**带注释显示值**，合法，不校验
        if want is not None and want != slots:
            note(f"sections[{name}]：题量写 {want}，但区间 {rng} 占 {slots} 个题号 —— "
                 f"若是有意（多问合并计分）请写成 `{want}（说明）` 这种带注释形式")

    out.extend(check_answers(cfg, text, fail, note))
    return out


# ── 配置 answers ↔ 页面逐题 `**答案：X**`（2026-09-20 新增）────────────
#   ★ 为什么必须加：修 english2022 时发现，页面顶部由配置生成的「答案速查表」
#     与页面正文的逐题答案**可以整表不一致**，而当时 lint 全绿 ——
#     因为旧的一致性检查只比「题号覆盖」，从不比**答案值**。
#     实测 english2022 配置 31/45 处与官方答案页不符，学生按速查表核对会得到
#     31 个错答案。这是「两个来源各自沉默」的典型：页面正文对、速查表错，
#     谁都不报警。
#
#   分级（避免把「页面比配置写得更详细」误判成错误）：
#     · 两边都是「见解析/见范文」类占位 → 等价，OK
#     · 归一化后完全相等                    → OK
#     · 两边都是**封闭集合**答案（单选 A–E、多选字母串、判断对错、
#       语法填空的短英文词）却不等          → fail（**真冲突**，如 B vs C）
#     · 其余（含 LaTeX / 中文表述）          → note（详略差异，人工看一眼即可）
#
#   ★ 为什么封闭集合才判 fail：数学/主观题的「配置答案」是**速查表用的简写**
#     （`\dfrac1e x` 之于 `\dfrac{1}{e}x`、`极大值 $-1$` 之于
#     `有极大值 $f(0)=-1$，无极小值`），本来就该比正文短。拿它判失败会连报 5 处
#     误报，检查就没人看了。而 A/B/C/D、doing/what 这类值**没有「更简写」的余地**，
#     不等就是错。
PLACEHOLDER_RE = re.compile(r"见解析|见范文|参考范文|见下|答案略|^略$")
# 封闭集合：单选/多选字母、判断对错、语法填空短英文词
CLOSED_RE = re.compile(r"^(?:[A-Ea-e]{1,6}|正确|错误|[√×]|[A-Za-z]{1,12})$")


def _norm_ans(s) -> str:
    """归一化答案文本：去掉 markdown 装饰、LaTeX 括号与反斜杠、所有空白。

    ★ 必须吃掉 `{}`：`\\dfrac1e x` 与 `\\dfrac{1}{e}x` 是同一个答案的两种写法，
      不归一化就会被判成冲突（实测误报）。
    """
    s = str(s)
    for ch in ("`", "$", "\\", "*", "{", "}", " ", "\u3000", "\t", "\r", "\n"):
        s = s.replace(ch, "")
    return s


def check_answers(cfg: dict, text: str, fail, note) -> list:
    """比对配置 `answers` 与页面逐题答案。返回 `[(severity, msg)]`。"""
    answers = cfg.get("answers")
    if not isinstance(answers, dict) or not answers:
        return []

    # 逐题切段：`### 第 N 题` 起，到**下一个任意级标题**止。
    # ★ 必须止于任意 `###`/`##`，不能只止于 `### 第 N 题` ——
    #   否则最后一题的段会一路吞到页尾的「附 · …」小节，
    #   把附件的 `**答案：ABCD**` 当成该题答案（实测踩过，politics2024 第 38 题）。
    body = {}
    segs = list(re.finditer(r"^###\s*第\s*(\d{1,3})\s*题.*$", text, re.M))
    for i, m in enumerate(segs):
        start = m.end()
        end = segs[i + 1].start() if i + 1 < len(segs) else len(text)
        nxt = re.search(r"^#{1,3}\s", text[start:end], re.M)
        seg = text[start:start + nxt.start()] if nxt else text[start:end]
        a = re.search(r"\*\*答案[：:]\s*([^*\n]+?)\*\*", seg)
        if a:
            body[m.group(1)] = a.group(1).strip()

    out = []
    for q, want in answers.items():
        got = body.get(str(q))
        if got is None:
            continue                      # 该题本页未收录答案，由 covered/gap_note 表达
        nw, ng = _norm_ans(want), _norm_ans(got)
        if nw == ng:
            continue
        if PLACEHOLDER_RE.search(nw) and PLACEHOLDER_RE.search(ng):
            continue                      # 「见范文」vs「参考范文」：同义占位
        if CLOSED_RE.match(nw) and CLOSED_RE.match(ng):
            fail(f"第 {q} 题：**配置答案与页面正文冲突** —— 配置 `{want}`，页面 `{got}`。"
                 f"两者都是封闭集合答案（不存在「更详细」的余地），必有一错。"
                 f"页面顶部「答案速查表」由配置生成、正文由转换器写，"
                 f"学习者按速查表核对会拿到错答案。请按权威来源（原卷/官方答案页）定谁对。")
        else:
            note(f"第 {q} 题：配置写 `{want}`，页面写 `{got}` —— 表述详略不同"
                 f"（速查表用简写是允许的），如需一致请手工对齐")
    return out


def files_from_configs() -> tuple:
    """从 `scripts/zhenti_cfg/*.json` 收集所有真题页路径。

    ★ 为什么要开这个入口：以前只能在 shell 里 `for c in zhenti_cfg/*.json`
      再逐个 `python -c 'print(json.load(...)["file"])'` 拼参数。在 Windows 上
      这条路会翻车 —— Python 的 stdout 是文本模式，`\\n` 会被翻成 `\\r\\n`，
      于是每个路径末尾都多带一个 `\\r`，`pathlib` 判定「不存在」，
      linter 安静地跳过 23 份、只检查到 1 份，最后还打印「合计 0 个问题」，
      看着像全站通过。这类「静默少查」比报错危险得多，索性收进脚本里。

    ★ 返回值改成 `(files, broken)`（2026-09-20，修 A4）：
      原来坏 JSON 是 `except Exception: continue` —— 配置写坏一个字符，
      那一页就**从检查清单里消失**，而汇总行照旧打印「合计 0 个问题」。
      这和上面那段注释里描述的「静默少查」是**同一个病**，只是入口不同。
      现在把坏配置连同异常一起返回，由 main() 计成失败。
    """
    cfg_dir = pathlib.Path(__file__).resolve().parent / "zhenti_cfg"
    out, seen, broken = [], set(), []
    for c in sorted(cfg_dir.glob("*.json")):
        if c.name.startswith("promote"):
            continue
        try:
            rel = json.loads(c.read_text(encoding="utf-8")).get("file")
        except Exception as e:
            broken.append((c.name, "%s: %s" % (type(e).__name__, e)))
            continue
        if not rel:
            # 有 JSON 但没有 `file` 键 —— 同样是「这一页悄悄没被查」
            broken.append((c.name, "缺少 `file` 字段"))
            continue
        if rel not in seen:
            seen.add(rel)
            out.append(rel)
    return out, broken


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--all-configs", action="store_true",
                    help="检查 zhenti_cfg/*.json 里登记的全部页面（不用手拼路径）")
    ap.add_argument("--fix", action="store_true", help="自动修复可修的项")
    # ── 结构化输出（2026-09-20，修 E3）──
    #   E3 的要害：没有任何地方能把「跑了什么、结果如何」汇总成机器可判定的东西。
    #   退出码只给一个比特；`--json` 给逐项明细，让上层能聚合。
    #   ★ 实现同 zhenti_regress.py：`--json` 时整个 stdout 重定向到 stderr，
    #     跑完只往真 stdout 打一个 JSON。这样**任何一处 print 都不会污染 JSON**，
    #     也不存在「以后新加的 print 忘了改」的问题。
    ap.add_argument("--json", action="store_true",
                    help="输出机器可读的 JSON（人类可读文本转到 stderr）")
    add_logging_args(ap)
    args = ap.parse_args()
    setup_from_args(args)

    as_json = args.json
    real_stdout = sys.stdout
    if as_json:
        sys.stdout = sys.stderr
    LOG.debug("lint 启动：files=%s · all_configs=%s · fix=%s · json=%s",
              args.files, args.all_configs, args.fix, as_json)

    files = list(args.files)
    broken_cfgs = []
    if args.all_configs:
        files, broken_cfgs = files_from_configs()
    if not files:
        ap.error("没给文件；要么列文件，要么加 --all-configs")

    total_problems = 0
    fixed_files = 0
    missing_files = 0
    file_results = []      # 逐页明细（--json 用）
    cfg_results = []       # 逐配置明细（--json 用）

    # ★ 坏配置要报出来（2026-09-20，修 A4）。修复前它是 `except: continue`，
    #   于是「配置写坏」= 该页从清单里消失，而汇总行照样说「合计 0 个问题」。
    for name, why in broken_cfgs:
        LOG.warning("配置 zhenti_cfg/%s 读不了（%s）—— 该页未被检查，本次通过不可信", name, why)
        print(f"[!] zhenti_cfg/{name} —— 配置无法读取（{why}）")
        print("      该页**没有**被检查。修好配置再跑，否则这份通过是假的。")
        file_results.append({"file": None, "config": name, "status": "broken_config",
                             "problems": [why], "fixed": 0})

    for f in files:
        p = pathlib.Path(f)
        if not p.exists():
            # ★ 配置里登记了、但文件不存在 —— 这是问题，不是「跳过」。
            #   修复前这里只 print 一句就 continue，退出码也不变，
            #   于是「页面被删了 / 路径写错了」在 CI 里等于没发生。
            print(f"[!] {f} —— 文件不存在（配置里登记了但磁盘上没有）")
            LOG.warning("配置登记的页面不存在：%s", f)
            missing_files += 1
            file_results.append({"file": f, "status": "missing", "problems": [],
                                 "fixed": 0})
            continue
        text = p.read_text(encoding="utf-8")

        fixed_n = 0
        if args.fix:
            new, n = fix_container_blank_lines(text)
            if n:
                p.write_text(new, encoding="utf-8", newline="\n")
                text = new
                fixed_files += 1
                fixed_n = n
                print(f"[修复] {p.name} —— 补了 {n} 处容器空行")

        probs = check(p, text)
        total_problems += len(probs)
        if probs:
            print(f"\n[!] {p.name} —— {len(probs)} 个问题")
            for x in probs:
                print(f"      · {x}")
        else:
            print(f"[OK] {p.name}")
        file_results.append({
            "file": f, "status": "problems" if probs else "ok",
            "problems": probs, "fixed": fixed_n,
        })

    # ── 配置 ↔ 页面 一致性（修 D2 / D3）──
    #   只在 --all-configs 时跑：它需要配置里的 total/covered/sections，
    #   光给文件路径没法验。
    cfg_problems = 0
    if args.all_configs:
        cfg_dir = pathlib.Path(__file__).resolve().parent / "zhenti_cfg"
        print()
        for c in sorted(cfg_dir.glob("*.json")):
            if c.name.startswith("promote"):
                continue
            try:
                rel = json.loads(c.read_text(encoding="utf-8")).get("file")
            except Exception:
                # ★ A6 复核（2026-09-20）：**有意**吞掉 —— 但前提是它真的被报过。
                #   坏 JSON / 缺 `file` 键已由 files_from_configs() 收进 broken_cfgs，
                #   并在上面的循环里逐条打印、计入退出码。这里的 continue 只是
                #   避免重复报，不是静默漏查。（修 A4 之前这里是**真的**静默漏查。）
                continue
            if not rel:
                continue
            page = pathlib.Path(rel)
            if not page.exists():
                continue          # 缺失文件已由 files_from_configs() 计入 missing_files
            probs = check_config(c, page.read_text(encoding="utf-8"))
            fails = [m for s, m in probs if s == "fail"]
            notes = [m for s, m in probs if s == "note"]
            if fails or notes:
                cfg_problems += len(fails)
                head = f"[!] {c.name} —— {len(fails)} 个配置不一致"
                if notes:
                    head += f"，另有 {len(notes)} 条已声明的缺口"
                print(head)
                for m in fails:
                    print(f"      ✗ {m}")
                for m in notes:
                    print(f"      · {m}")
            cfg_results.append({"config": c.name, "file": rel,
                                "fails": fails, "notes": notes})
        if not cfg_problems:
            print("[OK] 配置 ↔ 页面 一致性：全部吻合")

    print(f"\n合计 {total_problems} 个问题"
          + (f"，配置不一致 {cfg_problems}" if cfg_problems else "")
          + (f"，缺失文件 {missing_files}" if missing_files else "")
          + (f"，坏配置 {len(broken_cfgs)}" if broken_cfgs else "")
          + (f"，修复 {fixed_files} 个文件" if args.fix else ""))

    # ★ 退出码必须反映结果，否则这个脚本不能当闸门用。
    #   修复前这里是无条件 `return 0` —— 实测造一个 5 个问题的页面，
    #   stdout 打印「合计 5 个问题」而退出码是 0，挂在 pre-commit / CI
    #   上等于永远通过。
    rc = 1 if (total_problems or missing_files or broken_cfgs or cfg_problems) else 0
    LOG.info("lint 汇总：问题 %d · 配置不一致 %d · 缺失文件 %d · 坏配置 %d · 修复文件 %d → rc=%d",
             total_problems, cfg_problems, missing_files, len(broken_cfgs), fixed_files, rc)
    if rc:
        LOG.warning("lint 未通过：退出码 1（问题 %d / 缺失 %d / 坏配置 %d / 配置不一致 %d）",
                    total_problems, missing_files, len(broken_cfgs), cfg_problems)
        print("退出码 1 —— 有问题未解决。")

    if as_json:
        sys.stdout = real_stdout
        json.dump({
            "tool": "zhenti_lint",
            "all_configs": args.all_configs,
            "fix_applied": args.fix,
            "totals": {
                "problems": total_problems,
                "config_inconsistencies": cfg_problems,
                "missing_files": missing_files,
                "broken_configs": len(broken_cfgs),
                "files_fixed": fixed_files,
            },
            "exit_code": rc,
            "files": file_results,
            "configs": cfg_results,
        }, real_stdout, ensure_ascii=False, indent=2)
        real_stdout.write("\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
