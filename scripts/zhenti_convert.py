#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scripts/zhenti_convert.py —— 把旧格式真题页转换成《真题页模板》规范格式。

为什么要有这个脚本：笔记站里有 30+ 份真题页，横跨三种编号体例、四种答案块写法。
手工改一遍要几百次编辑且极易漏；但纯自动改又会因为各份结构不同而破坏内容。
所以这里走「脚本做机械部分 + 配置提供需要判断的部分」：

  脚本负责（可机械化）：frontmatter 补字段、题号标题体例、选项拆列表、
                        答案块包 ::: details、题间 ---、试卷结构表规范化、题目一览表
  配置提供（必须人判断）：主题名 topics、核心考查 sections、答案速查 answers

★ 安全性：默认 dry-run，只把结果写到 --out 供 diff；必须显式 --apply 才覆盖原文件。
   覆盖前自动备份到 <file>.bak-<日期>。

用法：
    python scripts/zhenti_convert.py --config cfg/math2018.json --out /tmp/x.md
    python scripts/zhenti_convert.py --config cfg/math2018.json --apply
"""

import argparse
import datetime
import json
import os
import pathlib
import re
import shutil
import sys

# 容器空行修复复用 lint 里的实现（同一套判据，避免两处逻辑漂移）。
# 用 pathlib 显式把 scripts/ 加进 sys.path —— 调用方可能从任意 cwd 起，
# 光靠「同目录」是 import 不到的（`python D:/x/scripts/zhenti_convert.py`
# 时 sys.path[0] 确实是 scripts/，但 `python -m scripts.zhenti_convert` 就不是了）。
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from zhenti_lint import fix_container_blank_lines  # noqa: E402
# ★ E3（2026-09-20）：诊断走 logging（写 stderr），正式输出仍走下面的 log()/print。
#   命名区分：`LOG` 是 logger，`log()` 是既有的 stdout 打印函数 —— 不要合并，
#   合并会把给人看的结果挪到 stderr，破坏调用方的 stdout 契约。
from zhenti_log import add_logging_args, get_logger, setup_from_args  # noqa: E402

LOG = get_logger(__name__)

CN_NUM = "一二三四五六七八九十"
# 大题标题：## 一、单项选择题（每题 3 分，共 15 分）
SECTION_RE = re.compile(r"^##\s*([%s]+)、\s*(.+?)\s*$" % CN_NUM)
# ★ 英语卷的大题标题不用中文序号，而是 `## Part I 词汇语法（第1–30题）`。
#   单开一条正则，不并进上面那条 —— 并进去 group(1) 的语义就含糊了
#   （有时是「一」有时是「Part I」），下游拼 key、查 section_titles 全要分叉。
SECTION_PART_RE = re.compile(r"^##\s*(Part\s+[IVX]+)\s+(.+?)\s*$")
# 已是标题的题号：### 1. xxx   /  ### 第 1 题：xxx  /  ### 19.（10 分）xxx
# ★ 只用 \b 抓题号，剩下的交给 strip_qno_sep() 去分隔符。
#   早期版本写成 `[（(]?[^)）]*[)）]?` 想一步跳过括号，结果题面里出现 \Bigr) 时，
#   正则一路吃到那个右括号，把题面 90% 都吞了 —— 输出只剩 "=$"。
#   教训：正则越"聪明"越容易吃掉内容；拆成两步（抓号 → 剥分隔符）反而稳。
HEAD_QNO_RE = re.compile(r"^###\s*(?:第\s*)?(\d{1,2})\b(.*)$")
# 段落形式的题号：6. xxx   （2018 的填空题/计算题就是这样）
# ★ 分隔点后面**不要求**有空格：2019/2020 的综合题写成 `19.（12 分）$G$ 由…`，
#   点和括号之间没有空格。但不能写成 `\.\s*` —— 那会把 `1.5 倍` 当成「第 1 题」。
#   用 `(?!\d)` 卡住：点后面只要不是数字，才认它是题号。
BARE_QNO_RE = re.compile(r"^(\d{1,2})\.(?!\d)\s*(\S.*)$")


def strip_qno_sep(rest):
    """只剥掉题号紧后面的分隔符，绝不越过题面本身。

    覆盖：`.`、`、`、`题：`、`：`、`（10 分）`。

    ★ `题` 后面**必须**跟冒号才剥。早期写成 `^题\\s*[：:]?\\s*`（冒号可选），
      结果 2023 第 15 题 `### 15. 题干缺失 —— 保留原记，不编造` 被剥成
      `干缺失 —— 保留原记，不编造` —— 题面第一个字就是「题」的题目并不罕见。
    """
    rest = rest.strip()
    rest = re.sub(r"^[\.、]\s*", "", rest)
    rest = re.sub(r"^题\s*[：:]\s*", "", rest)
    rest = re.sub(r"^[：:]\s*", "", rest)
    rest = re.sub(r"^[（(]\s*\d+\s*分\s*[)）]\s*", "", rest)
    return rest.strip()
# 选项行：A. xxx  B. xxx  C. xxx  D. xxx（半角或全角空格分隔）
OPT_SPLIT_RE = re.compile(r"\s{1,}(?=[A-D][\.、]\s*\S)")
OPT_HEAD_RE = re.compile(r"^[A-D][\.、]\s*")
# 答案块：连续的 > 引用行
QUOTE_RE = re.compile(r"^>\s?(.*)$")
# ★ 内联答案：2019/2020 的计算题把答案直接缀在题面行尾 —— `11. $\lim…$ → **$1/2$**`。
#   箭头两侧的空格可有可无（2020 第 16 题就写成 `…）→ **$4$**`，箭头紧贴右括号）。
#   不会误伤题面里的 `\to`（那是反斜杠 + 字母 to，不是 U+2192），
#   而 U+2192 出现在题面正文里的概率极低。
INLINE_ANS_RE = re.compile(r"\s*→\s*")
# ★ 直通区：这些二级标题之后的正文不是「卷面题目」，而是复核记录 / 备考建议 / 收尾。
#   一旦遇到就停止一切结构改写、原样复制 —— 否则复核记录里那句
#   `> **诚实声明：** …` 会被当成「某道题的答案」包进 ::: details。
#   ★ 必须容忍「## 七、考点分布与备考建议」这种带序号的写法 ——
#   早期版本写死 `^##\s*(考点分布…)`，2026 的 `## 七、` 前缀直接绕过了保护。
#   cfg.passthru_sections 可以追加项目（2025 计算机的「## 四～六、…」「## 还原说明」）。
PASSTHRU_BASE = r"复核记录|考点分布|回炉"


def build_passthru_re(cfg):
    """直通区判据：命中就原样复制、不再做任何结构改写。

    ★ 两种写法都要接住：
      · 带序号的 `## 七、考点分布与备考建议`（序号可有可无）
      · 前缀不是序号的 `## 2024 考点热力图 → 拆练`、`## 四～六、简答题`（用 `.` 通配）
      早期版本只认第一种，2023 计算机的 `## 先读这一段` 被当成直通后一路吞到文件尾，
      整页 45 题一个字都没转换（实测踩过）。
    """
    extra = cfg.get("passthru_sections") or []
    core = r"(?:[一二三四五六七八九十]+、)?\s*(?:复核记录|考点分布|回炉)"
    pat = r"^##\s*(?:%s" % core
    if extra:
        pat += "|.*(?:" + "|".join(re.escape(e) for e in extra) + ")"
    return re.compile(pat + ")")

# ★ 日期可注入（2026-09-20，修 F1d）。
#   原来是裸 `datetime.date.today()`，写在模块顶层 —— 于是**同一份输入跨天跑
#   会产出不同文件**（frontmatter 的 `date:` 变了），也让「同输入同输出」这类
#   验收标准没法成立。zhenti_regress.py 里那个 norm_dates() 就是在给这个兜底：
#   它把 `date:` 抹成占位符再比对。兜底能救比对，救不了产物本身的不确定性。
#   现在允许用环境变量钉死，需要复现时设 ZHENTI_DATE=2026-09-19 即可。
DATE = os.environ.get("ZHENTI_DATE") or datetime.date.today().isoformat()


def log(*a):
    print(*a)


# ─────────────────────── 解析 ───────────────────────


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    fm_raw = text[4:end]
    body = text[end + 4 :].lstrip("\n")
    fm = {}
    for ln in fm_raw.split("\n"):
        m = re.match(r"^(\w+)\s*:\s*(.*)$", ln)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm, body


def build_frontmatter(fm, subject, year, title):
    """按模板规范重建 frontmatter，保留原有字段（cover/category 等主题可能依赖的不能删）。"""
    out = ["---"]
    out.append(f"title: {title}")
    out.append(f"date: {DATE}")
    desc = fm.get("description", "").strip().strip('"')
    if desc:
        out.append(f"description: {desc}")
    tags = fm.get("tags")
    if tags:
        out.append(f"tags: {tags}")
    else:
        out.append(f"tags: [专插本, {subject}, 真题, {year}]")
    # year 必须带引号，否则 YAML 解析成整数
    out.append(f'year: "{year}"')
    out.append(f'subject: "{subject}"')
    # 保留可能有用的原有字段
    for k in ("cover", "category"):
        if k in fm:
            out.append(f"{k}: {fm[k]}")
    out.append("---")
    return "\n".join(out)


def is_option_line(line):
    """判断是不是「A. … B. … C. … D. …」这种一行装四个选项的写法。"""
    s = line.strip()
    if not s or s.startswith(">") or s.startswith("|") or s.startswith("```"):
        return False
    parts = OPT_SPLIT_RE.split(s)
    if len(parts) != 4:
        return False
    return all(OPT_HEAD_RE.match(p.strip()) for p in parts)


def split_stem_options(rest):
    """把「题面 + 四个选项挤在同一行」拆成 (题面, [选项×4])。

    2023 政治的单选就是这么记的：
        `1. 2022 年是中国共青团成立（ ） A.80 B.90 C.100 D.110`
    题面和选项之间没有任何换行或标记，只有空格 —— 而且选项的点号后面**没有空格**
    （`A.80` 不是 `A. 80`），所以 OPT_SPLIT_RE 早期那版（要求点号后必须有空白）
    整行都认不出选项，四个选项会原样留在题面里。

    判据收紧到「必须是 1 段题面 + 正好 A/B/C/D 四个选项」，否则原样返回 ——
    否则正文里任何一句带 ` A. ` 的话都会被误切。
    """
    parts = [p.strip() for p in OPT_SPLIT_RE.split(rest)]
    if len(parts) != 5 or not parts[0]:
        return rest, None
    letters = [p[0] for p in parts[1:]]
    if letters != ["A", "B", "C", "D"] or not all(OPT_HEAD_RE.match(p) for p in parts[1:]):
        return rest, None
    return parts[0], parts[1:]


def sub_fold_line(line, subs):
    """对折叠块内的一行依次套用 cfg.fold_line_subs 里的正则替换。"""
    for pat, repl in subs:
        line = pat.sub(repl, line)
    return line


def normalize_answer_label(block):
    """把「标签行 + 下一行才是答案」合并成 `**答案：X**`。

    政治卷的写法是两行：
        `> **答案**`      （或 `> **答案要点**`）
        `> **C**`         （或 `> **错误**。三大法宝是…`）
    直接折进去读者会看到加粗的「答案」和加粗的「C」各占一行，像两个标题。
    合并成 `**答案：C**` 才跟模板一致。只认「标签行是纯加粗标签」这一种形态，
    其余原样不动。
    """
    if len(block) < 2:
        return block
    m = re.match(r"^\*\*(答案|答案要点|参考答案)\*\*\s*$", block[0].strip())
    if not m:
        return block
    m2 = re.match(r"^\*\*(.+?)\*\*\s*(.*)$", block[1].strip())
    if not m2:
        return block
    tail = m2.group(2).strip()
    # 尾巴接中文标点时不留空格（`**答案：收敛**（与…比较）` 而不是 `**…** （…）`），
    # 接 ASCII 内容时才补一个空格，免得 `**答案：C**see below` 黏在一起。
    sep = " " if tail and ord(tail[0]) < 128 else ""
    merged = f"**答案：{m2.group(1)}**" + (f"{sep}{tail}" if tail else "")
    return [merged] + block[2:]


def collect_option_block(lines, i):
    """按字母顺序 A→B→C→D 连续收集选项，返回 (选项列表, 下一行下标)。

    三种排版都要接住：
      ① 每个选项各占一行    —— 2022 第 5 题、2024 第 4/5 题（公式太长）
      ② 一行装两个、跨两行  —— 2021 第 19 题（`A. … B. …` 换行 `C. … D. …`）
      ③ 一行装四个          —— is_option_line() 已覆盖，这里是兜底

    为什么必须凑齐 A~D 才认：正文里也常出现 `A. …` 这种行首（比如讲选项的
    解析）。若见到一行就收，会把解析里的字母当成选项搬到题面去。
    所以要求「从 A 开始、按序、不多不少正好四个」，否则整块放弃、原样不动。
    """
    opts, j, want = [], i, 0
    while j < len(lines) and want < 4:
        s = lines[j].strip()
        if not s or s.startswith(">") or s.startswith("|") or s.startswith("```"):
            break
        parts = [p.strip() for p in OPT_SPLIT_RE.split(s)]
        if not parts or not all(OPT_HEAD_RE.match(p) for p in parts):
            break
        if parts[0][0] != "ABCD"[want]:  # 必须接在上一行后面，不能跳号
            break
        opts.extend(parts)
        want += len(parts)
        j += 1
    if want != 4:
        return None, i
    return opts[:4], j


def split_options(line):
    return [p.strip() for p in OPT_SPLIT_RE.split(line.strip())]


def fmt_options(opts):
    """选项统一成无序列表，字母加粗。"""
    out = []
    for o in opts:
        m = re.match(r"^([A-D])[\.、]\s*(.*)$", o)
        if m:
            out.append(f"- **{m.group(1)}.** {m.group(2).strip()}")
        else:
            out.append(f"- {o}")
    return out


# ─────────────────────── 主转换 ───────────────────────


def parse_qno_range(r):
    """把配置里的题号区间解析成 `(lo, hi)`；解析不出来返回 `None`。

    认这些写法：`1–20`（en dash）/ `1-20` / `20`（单值）/ `"1 – 20"`。
    认不出的（`—`、`""`、`None`、`"主观题"`）返回 `None` —— **由调用方决定怎么办**，
    不要在这里 `int()` 硬转：`int("—")` 抛 ValueError（politics2024 就是），
    而把它当 0 又会悄悄改变区间语义。
    """
    if r is None:
        return None
    s = str(r).strip().replace("–", "-").replace("—", "-")
    if not s:
        return None
    parts = [p.strip() for p in s.split("-") if p.strip()]
    if not parts:
        return None
    try:
        lo = int(parts[0])
        hi = int(parts[-1]) if len(parts) > 1 else lo
    except ValueError:
        return None
    return (min(lo, hi), max(lo, hi))


def convert(text, cfg):
    fm, body = split_frontmatter(text)
    year = cfg["year"]
    subject = cfg["subject"]
    topics = {str(k): v for k, v in cfg.get("topics", {}).items()}
    sections = cfg.get("sections", {})
    answers = {str(k): v for k, v in cfg.get("answers", {}).items()}

    # ★ 答案块起始判据。默认 `>` 引用块；但计算机卷有别的写法：
    #   2021/2022 是裸行 `**答案：B** · 考点 …`；
    #   2024 的简答题只有 `**考点**` / `**参考答案**：`，压根没有引用块。
    #   用 `answer_start` 覆盖即可，不必为每种写法改代码。
    starts = cfg.get("answer_start") or [r"^>"]
    FOLD_START_RE = re.compile("|".join(f"(?:{s})" for s in starts))
    # ★ fold_tail：答案块一路吃到下一个题号 / 大题标题 / `---` 为止，
    #   而不是「引用行断掉就结束」。2024/2025 的解析写在引用块**外面**
    #   （`> **答案：C** · 考点 …` 换行 `**解析**：…`），不吃到边界就会漏掉解析。
    fold_tail = bool(cfg.get("fold_tail"))
    # ★ fold_line_subs：对**折叠块内部**的每一行做替换（[[正则, 替换], …]）。
    #   英语精析版的答案/翻译/考点写成无序列表（`- **答案**：D`），
    #   直接折进去读者会看到四个并排的圆点，跟模板的 `**答案：D**` 不一致。
    #   只作用于折叠块 —— 全局替换会误伤正文里的同形文本。
    fold_subs = [(re.compile(a), b) for a, b in (cfg.get("fold_line_subs") or [])]
    # ★ section_qno_base：计算机卷每节从 1 重新编号（单选 1–20、判断 1–10…），
    #   直接转会把两节都变成「第 1 题」。这里按节加偏移，换算成全局题号。
    qno_base = {str(k): int(v) for k, v in (cfg.get("section_qno_base") or {}).items()}
    cur_base = 0
    last_qno = 0
    last_q_idx = -1   # 最近一个题号标题在 out 中的位置
    last_sec_idx = -1  # 最近一个大题标题在 out 中的位置
    PASSTHRU_RE = build_passthru_re(cfg)

    lines = body.split("\n")
    out = []
    stats = {"q": 0, "opts": 0, "ans": 0, "sec": 0}
    i = 0
    n = len(lines)
    # 记录每道题在 out 中的起始下标，用于插 --- 分隔
    q_starts = []
    # ★ 只有出现过题号之后，`>` 引用块才被当作答案块。
    #   否则文件开头那段「来源 / 边界 / 主攻」的元信息 blockquote 会被误包进 ::: details。
    seen_q = False
    _guard = -1  # 主循环前进保护（见循环开头）
    # `:::` 容器（details / tip / warning…）嵌套深度。> 0 时容器内部一律原样通过。
    depth = 0

    # ── 题号范围校验的输入：**在循环外算一次**（2026-09-20，修 D1）──
    #   ★ 为什么必须提出来：这段原来在循环体里，于是「sections 有 `—`」的警告
    #     会**每道题打一遍**（实测 28 题打了 28 遍）。警告变成噪音就等于没有警告。
    ranges = [x for x in (parse_qno_range(v[0]) for v in sections.values()) if x]
    if not ranges:
        log(f"  [警告] {cfg.get('file', '?')}：sections 里没有一条能解析出题号区间"
            f"（值：{[v[0] for v in sections.values()]}），跳过题号范围校验 —— "
            f"否则会把整页题目判无效、静默丢光。")
    else:
        unparsed = [v[0] for v in sections.values()
                    if v[0] is not None and parse_qno_range(v[0]) is None]
        if unparsed:
            log(f"  [警告] {cfg.get('file', '?')}：sections 有 {len(unparsed)} 条区间"
                f"解析不出题号，已跳过：{unparsed} —— 建议改成 null（该节无题号）"
                f"或合法区间，别留 `—` 这类占位符。")

    while i < n:
        # ★ 硬保护：主循环每轮必须让 i 前进。少写一个 i += 1 或某个分支
        #   在「什么都没产出」时还 continue，进程就会原地打转、不报错也不结束 ——
        #   2023 政治那次卡了 4 分钟才被发现。宁可当场炸掉，也不要静默挂死。
        if i == _guard:
            raise RuntimeError(
                f"主循环未前进（i={i}）：{lines[i][:60]!r} —— 检查这条线命中的分支是否漏了 i += 1"
            )
        _guard = i
        line = lines[i]
        stripped = line.strip()

        # ── 容器内部：一律原样通过，不做任何解读 ──
        # ★ 为什么必须挡住：`::: details` / `::: tip` 里的内容是**已经定稿的解析正文**，
        #   转换器不该再对它做任何解读。但主循环原先不区分「容器内 / 容器外」，
        #   于是解析里那种有序列表会被当成卷面题号 —— 数学 2025 第 3 题的解析
        #   列了 4 条理由（`1. … 2. … 3. … 4. …`），`4.` 被认成「第 4 题」：
        #   凭空多出一个题号标题，还把这段解析从折叠块里切了出去。
        #   单调性保护（`qno <= last_qno` 就丢弃）救不了它 —— 4 > 3，正好通过。
        #   已有的 23 份页面没暴露这个问题，是因为它们的折叠块都是转换器
        #   **自己生成**的（生成后直接进 out，不再回到主循环）；
        #   只有「原生容器」的页面才会踩到（math/2025 实测）。
        #   ★ 一并把 PASSTHRU / 大题 / 题号 / 选项 / 答案块全挡住：
        #     容器里出现 `>` 行也不该被再折一层（会折叠套折叠）。
        if depth > 0 or (stripped.startswith(":::") and stripped != ":::"):
            if stripped.startswith(":::") and stripped != ":::":
                depth += 1
            elif stripped == ":::":
                depth -= 1
            out.append(line)
            i += 1
            continue

        # ── 直通区：复核记录 / 考点分布 原样保留；回炉区直接丢弃（页尾统一重写）──
        if PASSTHRU_RE.match(stripped):
            if re.match(r"^##\s*回炉", stripped):
                i = n
                break
            # ★ 复制到「下一个不是直通区的 ## 章节」为止 —— 不能一路吃到文件尾。
            #   2023 计算机的「## 先读这一段」在文件开头，若吃到尾，整页 45 题
            #   一个字都不会被转换（实测踩过）。
            while i < n:
                s3 = lines[i].strip()
                if re.match(r"^##\s*回炉", s3):
                    i = n
                    break
                if s3.startswith("## ") and not PASSTHRU_RE.match(s3):
                    break
                out.append(lines[i])
                i += 1
            continue

        # ── 试卷结构表：整体替换成 5 列 ──
        #   2026 写成 `## 一、试卷结构`（带序号），所以这里也要容忍序号前缀。
        if re.match(r"^##\s*(?:[一二三四五六七八九十]+、)?\s*试卷结构", stripped):
            out.append("## 试卷结构")
            out.append("")
            out.append("| 大题 | 题号 | 题量 | 分值 | 核心考查 |")
            out.append("|:---|:--:|--:|--:|:---|")
            qrange = cfg.get("qrange", {})
            # ★ `null` 的显示映射（2026-09-20，修 D1 的连带面）。
            #   配置里 `sections[name][0]` 有**两个角色**：① 题号范围（给校验用）
            #   ② 结构表里的显示文本。politics2024 第三节（辨析/简答/论述·同型模板）
            #   本来没有题号，以前用一个 `"—"` 同时充当两者 —— 而 `int("—")`
            #   会让「补到第 31 题」直接崩。
            #   现在配置里写 `null`（语义清晰：本节无题号），由这里映射成 `—`。
            #   实测踩过：只把配置改成 null 不改这里，表格会渲染出字面 `None`。
            dash = lambda v: "—" if v is None else v
            for name, (rng, cnt, score) in sections.items():
                out.append(f"| {name} | {dash(rng)} | {dash(cnt)} | {score} |"
                           f" {cfg.get('core', {}).get(name, '')} |")
            total = cfg.get("total", ("20", "100"))
            note = cfg.get("total_note") or "满分 100 分 · 120 分钟"
            out.append(f"| **合计** | | **{total[0]}** | **{total[1]}** | {note} |")
            out.append("")
            # 跳过原来的表格
            i += 1
            while i < n and (lines[i].strip().startswith("|") or lines[i].strip() == ""):
                i += 1
            stats["sec"] += 1
            continue

        # ── 大题标题：补全分值表述 ──
        m = SECTION_RE.match(stripped)
        mp = None if m else SECTION_PART_RE.match(stripped)
        if (m or mp) and not stripped.startswith("###"):
            if m:
                key = f"{m.group(1)}、{m.group(2).split('（')[0]}"
                bare = key.split("、", 1)[-1]
            else:
                # `## Part I 词汇语法（第1–30题）` → key = `Part I 词汇语法`
                key = f"{mp.group(1)} {mp.group(2).split('（')[0]}"
                bare = key
            # drop_sections：整节丢弃（2026 的「## 六、答案速查」已被重写成
            # 「## 题目一览」，留着就是两张重复的答案表）
            if bare in (cfg.get("drop_sections") or []):
                i += 1
                while i < n and not lines[i].strip().startswith("## "):
                    i += 1
                continue
            # 配置里给的标准写法优先
            std = cfg.get("section_titles", {}).get(key)
            # 记录本节题号偏移（计算机卷每节从 1 重编号）
            cur_base = qno_base.get(bare, 0)
            if std:
                if out and out[-1].strip() != "":
                    out.append("")
                out.append(f"## {std}")
            else:
                if out and out[-1].strip() != "":
                    out.append("")
                out.append(f"## {stripped[3:]}")
            out.append("")
            # ★ 这里**故意不**吃掉源文件里紧跟在标题后面的空行，虽然那会造成
            #   「标题 + 两个连续空行」—— 12 份线上文件就是这个形态。
            #   试过改成「吃掉」，正向回归立刻从 24/24 掉到 12/24：因为线上文件
            #   是**更早一版转换器**产出的，它保留了源文件那条空行，而新版不保留，
            #   两者就对不上了。要么改回原样，要么把 12 份页面全部重新落盘 ——
            #   后者会让回归退化成「自己跟自己比」的同义反复，失去独立验证的意义。
            #   双空行在 markdown 里不可见（连续空行会被折叠），所以留着它，
            #   换取回归链路的可信度。见 zhenti_regress.py --idem 的说明。
            i += 1
            last_sec_idx = len(out)  # 本节从这一行开始
            continue

        # ── 题号标题 ──
        qno, rest, label = None, None, None
        m = HEAD_QNO_RE.match(stripped)
        if stripped.startswith("### ") and m:
            qno, raw_rest = int(m.group(1)), m.group(2)
            # ★ `### 第 N 题：主题` / `### 第 N 题 · 主题` —— 分隔符后面是**主题名**，
            #   不是题面。2026 高数、2020 英语精析版、2025 高数全卷用这个体例；
            #   若把它当题面输出，第 19 题就会变成
            #   `### 第 19 题 · 含参数区域面积与最值` 下面再跟一行
            #   `含参数区域面积与最值` —— 主题名被当成题干，读者一脸问号。
            #   ★ 也要接住「光秃秃的 `### 第 N 题`」：英语卷（刷题版）全是这个形态，
            #     HEAD_QNO_RE 的 group(2) 会把题号后面那个「题」字抓进来，
            #     不处理就会在每道题的题面上面多出一行孤零零的「题」。
            #   ★ 分隔符必须把 `·` 一起收进来。早期只写了 `[：:]`，于是
            #     `### 第 1 题 · 极限` 的 `raw_rest` = `" 题 · 极限"` 判不进这条线，
            #     `strip_qno_sep()` 只剥点号/冒号、剥不掉「题 ·」，最后把
            #     `题 · 极限` 当题面原样输出 —— 每道题头上多一行残字。
            #     这个 bug 一直没暴露，是因为回归的输入都是**转换前**的源
            #     （那里写的是 `### 19. 题目…`，走不到这条线）；
            #     只有拿「已转换的页面」当输入时才会踩到（math/2025 实测）。
            #   ★ 顺手把主题名接住（label）：配置的 topics 是权威，但万一漏配了
            #     某一题，也不该把主题名直接丢掉 —— 见下面 topic 的取值。
            msep = re.match(r"^\s*题\s*(?:[：:·]\s*(.*?)\s*)?$", raw_rest)
            if re.search(r"第\s*\d+\s*题", stripped) and msep:
                rest = ""
                label = msep.group(1) or None
            else:
                rest = strip_qno_sep(raw_rest)
        elif not stripped.startswith("#") and not stripped.startswith(">") and not stripped.startswith("|"):
            m2 = BARE_QNO_RE.match(stripped)
            if m2:
                qno, rest = int(m2.group(1)), strip_qno_sep(m2.group(2))

        if qno is not None and cur_base:
            qno += cur_base  # 本节从 1 重编号 → 换算成全局题号

        # ★ 单调性保护：解析里常有 `1. …` `2. …` 有序列表
        #   （计算机 2024 第 13 题的折半查找步骤、2025 第 1 题的复杂度对照），
        #   不设防就会被当成新题号，凭空多出「第 1 题」，还会把该题的
        #   答案块切碎。卷面题号是递增的，所以「不比上一题大」的一律不认。
        if qno is not None and qno <= last_qno:
            qno, rest = None, None

        if qno is not None:
            # 题号必须落在配置声明的范围内，否则多半是正文里的有序列表被误判。
            #
            # ★ 2026-09-20 修 D1。修复前是：
            #       int(r.split("–")[0].replace("–", "-").split("-")[0]) <= qno
            #   两个问题：
            #   ① `int("—")` 抛 ValueError —— politics2024 的
            #      `sections["三、辨析 / 简答 / 论述 · 同型模板"][0] == "—"`，
            #      补到第 31 题就崩。现在走 parse_qno_range()，解析不出就跳过该条。
            #   ② **更危险的方向**：如果一条区间都解析不出来，原来的
            #      `any(... for r in 空序列)` 返回 False → valid=False →
            #      **整页每一题的 qno 都被置 None，题目静默丢光**。
            #      所以「一条都解析不出来」时必须跳过这道校验，而不是全判无效。
            #   `ranges` 已在循环外算好（含警告），这里只做判断。
            if ranges and not any(lo <= qno <= hi for lo, hi in ranges):
                qno = None

        if qno is not None:
            # ★ 内联答案：`11. $\lim…$ → **$1/2$**`（2019/2020 计算题的写法）
            #   要在题面标题和正文分开之前先切掉 `→` 后半段，否则答案会跟着题面
            #   一起留在折叠块外，等于没折叠。
            inline_ans = None
            stem_opts = None
            if rest:
                seg = INLINE_ANS_RE.split(rest, 1)
                if len(seg) == 2 and seg[1].strip():
                    rest, inline_ans = seg[0].strip(), seg[1].strip()
                # ★ 题面与四个选项挤在同一行（政治 2023 单选）→ 先拆开
                rest, stem_opts = split_stem_options(rest)

            # ★ 逐题覆盖：极少数题的题面与答案是用中文冒号/分号黏在一行的
            #   （2020 第 15 题 `$z=…$：$\mathrm{d}z=…$；$\partial^2 z/…$`），
            #   没有任何可机械识别的分隔符。与其让脚本猜，不如在配置里显式写死。
            fix = (cfg.get("q_fix") or {}).get(str(qno))
            if fix:
                rest, inline_ans = fix[0], (fix[1] or None)

            if out and out[-1].strip() != "":
                out.append("")
            if out and out[-1].strip() == "" and len(out) > 1 and out[-2].strip() == "":
                out.pop()
            # ★ 配置里的 topics 是权威来源；没配到就退回标题行自带的主题名（label）。
            #   两者都没有就写成光秃秃的 `### 第 N 题` —— 这是允许的
            #   （英语刷题版全卷如此，见 zhenti_lint.py 里的条件检查）。
            topic = topics.get(str(qno), "") or (label or "")
            head = f"### 第 {qno} 题" + (f" · {topic}" if topic else "")
            q_starts.append(len(out))
            out.append(head)
            out.append("")
            if rest:
                out.append(rest.strip())
                out.append("")
            if stem_opts:
                out.extend(fmt_options(stem_opts))
                out.append("")
                stats["opts"] += 1
            if inline_ans:
                if fold_subs:
                    inline_ans = sub_fold_line(inline_ans, fold_subs)
                out.append("::: details 答案与解析")
                out.append("")
                out.append(inline_ans)
                out.append("")
                out.append(":::")
                out.append("")
                stats["ans"] += 1
            stats["q"] += 1
            seen_q = True
            last_qno = qno
            last_q_idx = len(out)  # 本题从这一行开始
            i += 1
            # ★ 题面不在标题行上时（`### 第 N 题` 换行才是题面），吃掉标题后面那条空行。
            #   不吃的话「标题 + 空行 + 题面」会渲染成标题与题面之间隔两个空行。
            #   ★ 只在 rest 为空时吃 —— 已有页面写的是 `### 1. 题干…`（题干就在标题上），
            #     它们走不到这里，所以这个改动不会让那 16 份页面回归失败。
            if not rest and not inline_ans and not stem_opts:
                while i < n and lines[i].strip() == "":
                    i += 1
            continue

        # ── 选项行：先试「每个选项一行」，再试「一行装四个」──
        if seen_q:
            blk, nxt = collect_option_block(lines, i)
            if blk:
                out.extend(fmt_options(blk))
                out.append("")
                stats["opts"] += 1
                i = nxt
                continue
        if is_option_line(line):
            out.extend(fmt_options(split_options(line)))
            out.append("")
            stats["opts"] += 1
            i += 1
            continue

        # ── 答案块 → ::: details（起始判据由 cfg.answer_start 决定，默认 `>`）──
        # ★ 本节里必须先出现过题号才允许折叠。
        #   否则大题标题下面那句「本节说明」式的引用块（2023 计算机
        #   「## 六、应用编程题」下的「三题都是基础结构默写…」）会变成一个
        #   孤零零的折叠块 —— 没有对应题目，读者不知道它在折什么。
        if FOLD_START_RE.match(line) and seen_q and last_q_idx > last_sec_idx:
            block = []
            # ★ 起始行本身可能就是答案内容：政治卷的简答/论述写成裸行 `要点：…`，
            #   没有 `>` 前缀，这行就是答案正文。引用块形态（`> **答案：C**`）
            #   则相反 —— `>` 只是标记，内容要把前缀剥掉，交给下面的循环处理。
            if not QUOTE_RE.match(line):
                block.append(line)
                i += 1
            while i < n:
                s2 = lines[i].strip()
                # ★ 边界 = 任意级别的标题 / 分隔线。
                #   早期只写 `### ` 和 `## `，漏了 `#### ` ——
                #   英语卷的「分篇标题」（`#### Passage B`）于是被当成解析正文，
                #   一路吞进上一道题的折叠块里：读者点开第 5 题的答案，
                #   会看到整篇 Passage B。用 `^#{1,6}\s` 一次盖全，
                #   免得以后再多一级标题又踩同一个坑。
                if re.match(r"^#{1,6}\s", s2) or s2 == "---":
                    break
                if QUOTE_RE.match(lines[i]):
                    block.append(QUOTE_RE.match(lines[i]).group(1))
                    i += 1
                    continue
                if fold_tail:
                    # ★ fold_tail：一路吃到题号/大题/分隔线。
                    #   2024/2025 的解析写在引用块**外面**（`> **答案：C** · 考点 …`
                    #   换行 `**解析**：…`），不这样吃就会把解析漏在折叠块外。
                    block.append(lines[i])
                    i += 1
                    continue
                # ★ 跨空行续接：2021 第 12 题在「必背对照：」和它的表格之间空了一行，
                #   markdown 把它切成两个引用块。若不续接，一道题会生成两个
                #   ::: details（读者会看到两个折叠条）。判据：下一个**非空**行仍是 `>`。
                j = i
                while j < n and lines[j].strip() == "":
                    j += 1
                if j < n and QUOTE_RE.match(lines[j]):
                    block.extend([""] * (j - i))
                    i = j
                    continue
                break
            # ★ 先合并「标签行 + 答案行」（政治卷的 `> **答案**` 换行 `> **C**`），
            #   再决定要不要丢掉纯标题行。顺序反了就会把 `**答案**` 当标题行 pop 掉，
            #   折叠块里只剩一个孤零零的 `**C**`。
            if fold_subs:
                block = [sub_fold_line(l, fold_subs) for l in block]
            block = normalize_answer_label(block)
            # 去掉块首的「答案与解析 / 答案 / 解析」纯标题行（details 的标题已经说明了）
            # ★ 这一步必须在 normalize_answer_label() **之后**：
            #   高数 2019/2020 是 `> **答案**` 换行 `> $\dfrac13 x$` —— 下一行不是加粗，
            #   合并逻辑不动它，于是 `**答案**` 作为纯标题行被丢掉，只剩公式；
            #   政治是 `> **答案**` 换行 `> **C**` —— 已被合并成 `**答案：C**`，
            #   不再是「纯标题行」，所以不会被丢。
            #   把 `答案` 从这条判据里拿掉就会同时砸掉前者（实测踩过）。
            while block and re.match(r"^\*\*(答案与解析|答案|解析)\*\*\s*$", block[0].strip()):
                block.pop(0)
            # 去掉首尾空行
            while block and block[0].strip() == "":
                block.pop(0)
            while block and block[-1].strip() == "":
                block.pop()
            if block:
                if out and out[-1].strip() != "":
                    out.append("")
                out.append("::: details 答案与解析")
                out.append("")
                out.extend(block)
                out.append("")
                out.append(":::")
                out.append("")
                stats["ans"] += 1
                continue
            # ★ 落空必须**落下去**，不能 continue。
            #   这条线虽然长得像答案起头（比如 `要点：…`），但收集下来是空块 ——
            #   下一个非空行既不是 `>`、fold_tail 又没开，于是 while 一进来就 break。
            #   此时若还 continue，i 一个都没前进，主循环原地打转，进程挂死。
            #   （政治 2023 的简答/论述写成裸行 `要点：…`，把 `^要点[：:]` 加进
            #    answer_start 之后第一次踩到，整个转换器卡了 4 分钟没输出。）
            #   落空就当作普通正文行，交给下面的 out.append(line) 处理。
        out.append(line)
        i += 1

    # ── 大题间 / 题间插 --- ──
    # 规则：`##` 大题标题前插 ---（首个除外）；`### 第 N 题` 前插 ---（紧跟大题标题的除外）。
    # 不能只按「题号前插」—— 那样第 1 题会在大题标题正下方多插一条线，
    # 视觉上把标题和它的第一题割开；而大题标题本身反而没有分隔线。
    final = []
    depth = 0  # `::: details` 嵌套深度
    for ln in out:
        s = ln.strip()
        # ★ 容器内一律不插分隔线。
        #   分隔线是**卷面结构**的分隔（大题之间、题目之间），
        #   而容器里是某道题的解析正文 —— 在里面插 `---` 会把一道题切碎。
        #   更阴的是：fold_body() 就是靠 `---` 判断「这道题的正文到哪结束」的，
        #   在它之前插一条线，等于提前替它做了「正文到此为止」的决定，
        #   于是 `#### （1）…` 那几段全被留在折叠块外面（2026 高数第 19/20 题实测踩过）。
        is_big = s.startswith("## ") and not re.match(r"^##\s*(试卷结构|题目一览)", s)
        # 阅读理解的「分篇」标题（`#### Passage A`）：英语卷一篇短文带 5 道题，
        # 分篇之间要有分隔线，否则读者分不清哪几道题属于同一篇。
        # ★ 判据必须卡到 `Passage` 这个词。写成「凡是 #### 都插线」会误伤
        #   折叠块里 `#### （1）…` 那种小题编号 —— 那正好是上面那条坑。
        is_sub = bool(re.match(r"^####\s+Passage\b", s))
        is_q = bool(re.match(r"^###\s*第\s*\d+\s*题", s))
        if depth == 0 and (is_big or is_sub or is_q):
            prev = next((l.strip() for l in reversed(final) if l.strip()), "")
            skip = (not prev) or prev == "---"
            if (is_q or is_sub) and prev.startswith("##"):
                skip = True  # 大题标题下面的第一个题号 / 分篇标题，不插线
            if not skip:
                while final and final[-1].strip() == "":
                    final.pop()
                final.append("")
                final.append("---")
                final.append("")
        if s.startswith(":::") and s != ":::":
            depth += 1
        elif s == ":::" and depth:
            depth -= 1
        final.append(ln)
    out = final

    # ── 裸文本答案 → ::: details ──
    out = wrap_raw_answers(out, {str(q) for q in cfg.get("raw_answer_qs", [])})

    # ── 「题面 + 解析一体」的页面 → 题面 + 折叠解析 ──
    out = fold_body(out, cfg)

    # ── 同一题被切成两个折叠块的，合并回一个 ──
    out = merge_adjacent_details(out)

    # ── 丢弃页尾的旧导航行（drop_lines）──
    #   模板的页尾是统一的一条 `> 相关：…`。但老页面在它前面还有一条
    #   `← [回真题总览] · [2024 全卷] · …` 的导航行，转换器不认它，
    #   于是新旧两条链接并排留着，读者看到两套「相关链接」。
    #   配置里用正则点名要丢的行，比在正文里靠位置猜安全。
    drop_pats = [re.compile(p) for p in (cfg.get("drop_lines") or [])]
    if drop_pats:
        kept, dropped = [], 0
        for ln in out:
            if any(p.search(ln) for p in drop_pats):
                dropped += 1
                continue
            kept.append(ln)
        out = kept
        stats["dropped"] = dropped

    # ── 插入「题目一览」速查表（放在「试卷结构」之后、第一个 --- 之前）──
    # ★ 页面里已经有 `## 题目一览` 就不再插。
    #   正常流程（转换前源）不会有这张表 —— 它是转换器生成的；但拿**已转换的
    #   页面**当输入时它就在那儿了，无条件插入会得到两张一模一样的答案速查表
    #   （math/2025 实测：43a44,60 凭空多出 17 行）。
    #   顺带这也是「幂等」的一部分：转换器对已转换页面应当是空操作。
    if answers and not any(ln.strip() == "## 题目一览" for ln in out):
        toc = ["## 题目一览", "", "::: details 展开看答案速查表（先自己做完再对）", ""]
        ks = sorted(answers, key=lambda x: int(x))
        # ★ toc_chunk：每行放几题。默认（不配）沿用「对半切」——
        #   高数 20 题 / 计算机 45 题就是按两行排的，改动默认值会让已转换的
        #   16 份页面全部回归失败。英语 66 题对半切是 33 列，手机上一行装不下，
        #   所以英语配置显式写 10。
        chunk = int(cfg.get("toc_chunk") or 0)
        if chunk:
            groups = [ks[i : i + chunk] for i in range(0, len(ks), chunk)]
        else:
            half = (len(ks) + 1) // 2
            groups = [ks[:half], ks[half:]]
        for g in groups:
            toc.append("| 题号 | " + " | ".join(g) + " |")
            toc.append("|:--:|" + ":--:|" * len(g))
            toc.append("| 答案 | " + " | ".join(answers[k] for k in g) + " |")
            toc.append("")
        toc.extend([":::", ""])
        # ★ 插到「## 试卷结构」那张表之后的**第一条 --- 之后**。
        #   不能找全文档「第一个 ---」—— 2025 计算机的导语末尾本来就有一条 ---，
        #   按「第一个 ---」插会把答案速查表顶到「试卷结构」前面去（实测踩过）。
        pos = None
        for idx, ln in enumerate(out):
            if ln.strip() == "## 试卷结构":
                j = idx + 1
                while j < len(out) and out[j].strip() != "---":
                    j += 1
                pos = j + 1 if j < len(out) else idx + 1
                break
        if pos is None:
            pos = 1
        out = out[:pos] + [""] + toc + ["---", ""] + out[pos:]

    # ── 页尾统一成模板的「相关」块 ──
    # ★ 语义是**替换**，不是追加：先把页尾已经存在的「相关」块剥干净，再写标准的那条。
    #   早期只处理了「最后一行恰好是 `---`」这一种形态，因为绝大多数源文件的页尾
    #   就是 `---` + `> 相关：…` 两行，被 `drop_lines` 或折叠逻辑处理掉之后，
    #   剩下的最后一行正好是 `---`。
    #   但 math/2025 的 `## 备考提示` 属于**直通区**，而直通区是整段照抄的 ——
    #   源文件里原有的 `---` + `> 相关：…` 被一起抄了进来，末尾于是停在
    #   `> 相关` 而不是 `---`；旧判断放它过去，标准块再追加一条，
    #   读者在页尾看到两套一模一样的相关链接。
    #   判据改成「末尾是 `> 相关…` 就先把它连同前面的 `---` 一起剥掉」，
    #   对已有页面是无害的超集（它们的末尾是 `---`，走不到新分支）。
    while out and out[-1].strip() == "":
        out.pop()
    if out and out[-1].strip().startswith("> 相关"):
        out.pop()
        while out and out[-1].strip() == "":
            out.pop()
        if out and out[-1].strip() == "---":
            out.pop()
    while out and out[-1].strip() == "":
        out.pop()
    if out and out[-1].strip() == "---":
        out.pop()
        while out and out[-1].strip() == "":
            out.pop()
    related = cfg.get("related") or ["[真题总览](/posts/math/)", "[真题章节对照表](/posts/math/真题章节对照表)"]
    out.extend(["", "---", "", "> 相关：" + " · ".join(related), ""])

    if cfg.get("tags"):
        fm["tags"] = cfg["tags"]
    if cfg.get("description"):
        fm["description"] = cfg["description"]
    head = build_frontmatter(fm, subject, year, cfg.get("title") or fm.get("title", "").strip('"'))
    body = "\n".join(out).strip() + "\n"

    # ── 最后一道：容器内外补空行 ──
    # ★ 转换器自己生成的 ::: details 是规规矩矩带空行的，但**原件里原有的**
    #   `::: tip …` 未必（2025 计算机有 3 处开标记后直接跟表格）。
    #   markdown-it 对「开标记后无空行」的处理是：容器内的表格不当块级元素解析，
    #   退化成一行竖线文字 —— 页面照常打开、构建零报错，肉眼扫代码看不出来。
    #   以前这一步靠事后手工跑 `zhenti_lint.py --fix`，结果是线上文件比
    #   「原件重跑」多几个空行，幂等回归永远报 ✗。并进来，一次成型。
    body, nfix = fix_container_blank_lines(body)
    stats["blankfix"] = nfix

    return head + "\n\n" + body, stats


def split_paragraphs(lines):
    """把一段行列表按空行切成「段落」，返回 [(起, 止), …]（止为开区间）。"""
    res, i, n = [], 0, len(lines)
    while i < n:
        if lines[i].strip() == "":
            i += 1
            continue
        j = i
        while j < n and lines[j].strip() != "":
            j += 1
        res.append((i, j))
        i = j
    return res


def fold_body(out, cfg):
    """把「题面 + 解析写在一起」的页面拆成「题面 + ::: details 折叠解析」。

    为什么单独一个函数：2018–2025 的卷子，解析都规规矩矩写在 `>` 引用块里，
    主循环的引用块分支直接就能折叠。但 2026 不是 —— 它是「解析页」写法：
    题面、推导、答案按段落平铺，中间没有任何标记区分。哪里是题面、哪里开始是解析，
    是**语义判断**，脚本猜不准（有「求」+ 公式的，有直接一整句话的，还有把答案
    写进题面公式里的）。

    所以走「配置声明边界」：`stem_paras[N]` 说明第 N 题的题面占前几个段落，
    `stem_text[N]`（可选）把这几段替换成一句更规范的题面。
    声明错了在 diff 里一眼可见；猜错了则会把题面折进答案、读者看不到题。
    """
    stem_paras = {str(k): int(v) for k, v in (cfg.get("stem_paras") or {}).items()}
    stem_text = {str(k): v for k, v in (cfg.get("stem_text") or {}).items()}
    answers = {str(k): v for k, v in (cfg.get("answers") or {}).items()}
    if not stem_paras:
        return out

    heads = []
    for idx, ln in enumerate(out):
        m = re.match(r"^###\s*第\s*(\d+)\s*题", ln.strip())
        if m:
            heads.append((idx, m.group(1)))
    if not heads:
        return out

    res = list(out[: heads[0][0]])  # 第一个题号之前的内容原样保留
    for pos, (idx, qno) in enumerate(heads):
        nxt = heads[pos + 1][0] if pos + 1 < len(heads) else len(out)
        end = nxt
        for k in range(idx + 1, nxt):
            if out[k].strip().startswith("## ") or out[k].strip() == "---":
                end = k
                break

        body = out[idx + 1 : end]
        # ★ 只处理**被显式声明**的题。
        #   本函数最初只服务 2026（那一卷 20 题全部逐题声明 stem_paras），
        #   后来 2023 计算机的「应用编程题」也要用 —— 但那卷的 1~42 题
        #   已经被主循环折好了。若「没声明 = 题面 0 段」，这 42 题会被
        #   把「题面 + 已有折叠块」整体再包一层，变成折叠套折叠。
        #   判据：不在 stem_paras 里 → 原样放回，一个字节都不动。
        if qno not in stem_paras or any(
            l.strip().startswith("::: details") for l in body
        ):
            res.extend(out[idx:nxt])
            continue

        res.append(out[idx])
        res.append("")

        paras = split_paragraphs(body)
        k = stem_paras.get(qno, 0)
        # ★ 越界必须硬失败，不能静默。
        #
        #   `k > len(paras)` 时：`paras[:k]` 就是**全部**段落（整块正文被当成题面），
        #   而 `paras[k:]` 是空列表 → `rest` 空 → `fold` 空 → `::: details` 折叠块
        #   根本不生成。于是这一题的解析整体消失，退出码却是 0。
        #
        #   实测（2026-09-19）：把 `zhenti_cfg/math2026.json` 的 `stem_paras["6"]`
        #   从正常值改成 99，跑 `--out` → rc=0、无任何告警，产物里第 6 题只剩
        #   题面一行 + 答案，源文件里那段推导整体不见了。
        #
        #   stem_paras 是手写配置，一个数字打错就等于静默删内容；而且
        #   lint 只管排版容器、回归只管「转换器对自己幂等」，**两者都发现不了
        #   内容变少**（把残缺产物再跑一遍仍然逐字节一致）。所以这里硬失败。
        if not (0 <= k <= len(paras)):
            raise SystemExit(
                "配置错误：stem_paras[%s] = %s，但第 %s 题只有 %d 个段落"
                "（配置：%s）\n"
                "  这个值超出段落数时，题面会吞掉整块正文、且不生成折叠块 ——"
                " 等于静默丢掉这一题的解析。\n"
                "  请核对 stem_paras 里这一项，或删掉它让本函数原样放回。"
                % (qno, k, qno, len(paras), cfg.get("file", "?")))
        if qno in stem_text:
            res.extend([stem_text[qno], ""])
        else:
            for (a, b) in paras[:k]:
                res.extend(body[a:b])
                res.append("")

        rest = []
        for (a, b) in paras[k:]:
            rest.extend(body[a:b])
            rest.append("")

        fold = []
        for ln in rest:
            m4 = re.match(r"^####\s*(（\d+）.*)$", ln.strip())
            if m4:
                # 模板要求小题用 `**（1）**` 标注，不新开 #### 标题
                fold.append(f"**{m4.group(1)}**")
                continue
            if re.match(r"^\*\*答案[：:].*\*\*\s*$", ln.strip()):
                continue  # 源里自带的答案行，下面按配置统一重写
            fold.append(ln)
        while fold and fold[0].strip() == "":
            fold.pop(0)
        while fold and fold[-1].strip() == "":
            fold.pop()
        ans = answers.get(qno, "")
        if ans:
            fold = [f"**答案：{ans}**", ""] + fold
        if fold:
            res.extend(["::: details 答案与解析", ""] + fold + ["", ":::", ""])

        res.extend(out[end:nxt])  # 题块与下一个题号之间的 `---`、空行原样保留
    return res


def merge_adjacent_details(out):
    """把「同一道题被切成两个折叠块」合并回一个。

    为什么会切成两块：2023 计算机的第 41 题，答案被写进了标题里
    （`### 2. 读程序：跳过不及格求平均 → n = 5，avg = 81.20`），
    主循环先按行内答案生成一个折叠块；紧接着正文里又有一段 `> ⚠️ …` 说明，
    于是又生成一个。读者会看到同一道题下面挂着两个折叠条。

    判据：两个 `::: details 答案与解析` 之间只隔空行 —— 中间若有任何正文，
    说明它们分属不同的题，不合并。
    """
    res = []
    i, n = 0, len(out)
    while i < n:
        if out[i].strip() != "::: details 答案与解析":
            res.append(out[i])
            i += 1
            continue
        i += 1
        body = []
        while i < n and out[i].strip() != ":::":
            body.append(out[i])
            i += 1
        i += 1  # 吃掉收尾的 :::
        while True:
            k = i
            while k < n and out[k].strip() == "":
                k += 1
            if k >= n or out[k].strip() != "::: details 答案与解析":
                break
            body.append("")
            i = k + 1
            while i < n and out[i].strip() != ":::":
                body.append(out[i])
                i += 1
            i += 1
        while body and body[-1].strip() == "":
            body.pop()
        while body and body[0].strip() == "":
            body.pop(0)
        # ★ 尾部只补到 `:::` 为止，**不**再补空行。
        #   所有折叠块的产生者（主循环 / fold_body / wrap_raw_answers）都在
        #   `:::` 后面统一补了一条空行，`out` 里紧随其后的那一行就是它。
        #   这里再补一次，跟后面那条空行叠起来就是双空行 ——
        #   渲染上没影响，但会让「原件重跑 == 线上文件」的幂等回归全部报 ✗。
        res.extend(["::: details 答案与解析", ""] + body + ["", ":::"])
    return res


def wrap_raw_answers(out, raw_qs):

    """把「答案是裸文本」的题目的答案包进 ::: details。

    为什么需要单独一个函数：多数卷子的答案写成 `>` 引用块，主循环就能包。
    但综合题的答案常常是直接跟在题面后面的 `(1) … (2) …` 裸文本
    （2018 的第 19、20 题就是这样），主循环的引用块分支接不住它们。

    判定边界：题号标题 → 空行 → 题面第一段 → 空行 → 【答案】→ 下一个 ###/##/---。
    题号必须在配置的 raw_answer_qs 里声明 —— 不做自动猜测，
    因为「题面里恰好也有 (1)」的情况并不罕见，猜错会把题面吞进答案。
    """
    res, i, n = [], 0, len(out)
    while i < n:
        ln = out[i]
        m = re.match(r"^###\s*第\s*(\d+)\s*题", ln.strip())
        if m and m.group(1) in raw_qs:
            res.append(ln)
            i += 1
            for _ in range(2):  # 空行 → 题面段 → 空行
                while i < n and out[i].strip() == "":
                    res.append(out[i])
                    i += 1
                if _ == 0:
                    while i < n and out[i].strip() != "":
                        res.append(out[i])
                        i += 1
            buf = []
            while i < n:
                s = out[i].strip()
                if s.startswith("#") or s == "---":
                    break
                buf.append(out[i])
                i += 1
            while buf and buf[-1].strip() == "":
                buf.pop()
            while buf and buf[0].strip() == "":
                buf.pop(0)
            if buf:
                res.append("::: details 答案与解析")
                res.append("")
                res.extend(buf)
                res.append("")
                res.append(":::")
                res.append("")
            continue
        res.append(ln)
        i += 1
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", help="dry-run 输出路径")
    ap.add_argument("--apply", action="store_true", help="覆盖原文件（自动备份）")
    ap.add_argument("--force", action="store_true",
                    help="允许对已转换过的页面再跑一次（正常情况下不该用，见 main() 里的说明）")
    add_logging_args(ap)
    args = ap.parse_args()
    setup_from_args(args)

    cfg = json.loads(pathlib.Path(args.config).read_text(encoding="utf-8"))
    src = pathlib.Path(cfg["file"])
    LOG.debug("配置 %s → file=%s · out=%s · apply=%s", args.config, src, args.out, args.apply)
    if not src.exists():
        LOG.error("源文件不存在：%s（配置 %s 指向它）", src, args.config)
        log(f"文件不存在: {src}")
        return 1

    text = src.read_text(encoding="utf-8")
    LOG.debug("读入 %d 字符 / %d 行", len(text), text.count("\n") + 1)

    # ★ 防二次转换。`--apply` 是原地覆盖，若对着**已经转换过**的文件再跑一遍，
    #   它会把 `### 第 N 题` 当正文、把已有折叠块再包一层，产出一份「转换的转换」——
    #   而且它会先把这份坏产物备份成 `.bak-<日期>.2`，看着像「正常地又跑了一次」。
    #   实测踩过：重跑 5 份页面时忘了先还原，874 行差异。
    #   判据：模板的两张表（`## 题目一览` / `## 试卷结构`）只有转换器会生成。
    if args.apply and not args.force and "## 题目一览" in text:
        LOG.warning("拒绝二次转换：%s 已含 `## 题目一览`（加 --force 可强行继续）", src.name)
        log(f"✗ {src.name} 看起来**已经是转换后的页面**（含 `## 题目一览`）。")
        log("  对着它再 --apply 会得到「转换的转换」。先还原源文件：")
        log(f"    cp '{src}.bak-*' '{src}'      # 取最早那个 .bak（= 转换前的源）")
        log("  确实要重跑就加 --force。")
        return 2

    new, stats = convert(text, cfg)
    LOG.debug("转换完成：题号 %d · 选项行 %d · 答案块 %d · 结构表 %d",
              stats["q"], stats["opts"], stats["ans"], stats["sec"])

    log(f"{src.name}: 题号 {stats['q']} · 选项行 {stats['opts']} · 答案块 {stats['ans']} · 结构表 {stats['sec']}")
    log(f"  原 {len(text)} 字符 → 新 {len(new)} 字符")

    if args.apply:
        # ★ 备份**只写一次**：已存在同名 bak 就往后编号，绝不覆盖。
        #   `--apply` 是可重复执行的（改了转换器要重跑），若每次都覆盖 bak，
        #   第二次就把**转换前的原件**冲掉了 —— 原件没了，
        #   zhenti_regress.py 的「原件重跑 == 线上」就再也验不了。
        bak = src.with_suffix(src.suffix + f".bak-{DATE}")
        k = 2
        while bak.exists():
            bak = src.with_suffix(src.suffix + f".bak-{DATE}.{k}")
            k += 1
        shutil.copy2(src, bak)
        src.write_text(new, encoding="utf-8", newline="\n")
        LOG.info("已覆盖 %s，备份 → %s", src.name, bak.name)
        log(f"  已覆盖，备份 → {bak.name}")
    elif args.out:
        p = pathlib.Path(args.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(new, encoding="utf-8", newline="\n")
        LOG.info("dry-run 输出 → %s", p)
        log(f"  dry-run 输出 → {p}")
    else:
        LOG.info("未指定 --out / --apply，未写任何文件")
        log("  （未指定 --out 或 --apply，什么都没写）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
