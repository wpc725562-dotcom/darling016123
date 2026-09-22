#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""英语「刷题版」→《真题页模板》形态 · 纯搬运前置脚本

为什么单独一个脚本
------------------
英语刷题版（2019–2024）用的是 HTML `<details>` 折叠 + `**N. 题干**` 加粗题面，
而《真题页模板》用 `### 第 N 题` + `::: details`。这层差异是**结构性的、可机械判定**的，
所以放在转换器之前做纯搬运 —— 跟 `zhenti_promote_compact.py` 同样的分工：

    前置脚本只搬不重写（改形态，不改内容）
    转换器只统一不发明（编号、折叠、结构表、速查表）

搬运规则
--------
1. `**N. 题干**`（整行加粗）/ `**N.** 其余` / `**N. 题干** 其余`
                           → `### 第 N 题` + 空行 + 题干
2. 题干里粘着第一个选项（`**51. A．burned**`、`**21.** A. practice`）
                           → 拆成 `- **A.** burned` 独立一行
3. `### Passage X…`        → `#### Passage X…`
   （`###` 在模板里保留给题号；Passage 是包住后面几道题的上一级容器）
4. `- A. xxx` / `- - A. xxx` → `- **A.** xxx`
5. `<details>` → 删；`<summary>…</summary>` → 删；`</details>` → 删
   **不在这里生成 `::: details`** —— 折叠交给转换器按 `**答案：X**` 起头生成。
   前置若自己包一层，转换器又按 `answer_start` 折一次，就是折叠套折叠。
6. 折叠块内部的 `---` → 删（会把 `:::` 容器截断，写作范文那几处）
7. `**答案**：X` → `**答案：X**`；折叠块里没有答案行的（写作范文）补 `**答案：参考范文**`
8. 第一个 `## Part ` 之前插入 `## 试卷结构` 占位表 + `---`
   （占位表会被转换器按配置整块替换成正式的 5 列表；不先放一个，
    转换器找不到 `## 试卷结构` 就无处安放，`## 题目一览` 也会插错位置）

用法
----
    python scripts/zhenti_promote_english.py --file docs/posts/english/2019-英语-刷题版.md --out /tmp/x.md
    python scripts/zhenti_promote_english.py --file … --apply      # 覆盖前自动备份

★ 默认 dry-run，必须显式 `--apply` 才写回原文件；备份不可覆盖（同名往后编号）。
"""

import argparse
import datetime
import json
import os
import pathlib
import re
import shutil
import sys

# 本脚本依赖同级模块 zhenti_log，显式把 scripts/ 加进 sys.path（理由见 zhenti_lint.py）。
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

# ★ E3（2026-09-20）：诊断走 logging（stderr），正式输出仍走 print（stdout）。
from zhenti_log import add_logging_args, get_logger, setup_from_args  # noqa: E402

LOG = get_logger(__name__)

# ★ 日期可注入（2026-09-20，修 F1d）。
#   与 zhenti_convert.py / zhenti_promote_compact.py 对齐：原来是裸
#   `datetime.date.today().isoformat()`，写在模块顶层 —— `--apply` 的备份名
#   `.<mode>-<DATE>` 于是**跨天跑会变**，同一份输入产不出同一批文件，
#   「同输入同输出」这类验收标准没法成立。
#   需要复现时设 ZHENTI_DATE=2026-09-19 即可。
DATE = os.environ.get("ZHENTI_DATE") or datetime.date.today().isoformat()

# 选项字母后面的分隔符：半角点 / 顿号 / **全角点**（2019 完形写成 `A．burned`）
# ★ 到 E 不是到 D —— 2022 起的「七选五」是 A–E 五个选项，
#   只认 A–D 会把 E 那行漏成 `- - E. …` 原样留在页面上。
OPT_HEAD = r"[A-E][\.、．]"
# `**N.` 起头的行，剩下的部分再细分（下面注释里解释为什么只用一个正则）
Q_RE = re.compile(r"^\*\*(\d{1,2})\.\s*(.*)$")
# 粘在题干里的第一个选项
OPT_GLUED_RE = re.compile(r"^(%s)\s*(.*)$" % OPT_HEAD)
# 已经是列表的选项：`- A. xxx`，以及被误写成嵌套列表的 `- - A. xxx`
OPT_ITEM_RE = re.compile(r"^-\s*-\s*(%s)\s*(.*)$" % OPT_HEAD)
OPT_ITEM2_RE = re.compile(r"^-\s*(%s)\s*(.*)$" % OPT_HEAD)
PASSAGE_RE = re.compile(r"^###\s+(Passage\b.*)$")
ANS_LABEL_RE = re.compile(r"^\*\*答案\*\*\s*[：:]\s*(.*)$")

PLACEHOLDER = [
    "## 试卷结构",
    "",
    "| 大题 | 题号 | 题量 | 分值 | 核心考查 |",
    "|:---|:--:|--:|--:|:---|",
    "",
    "---",
    "",
]

# ── 精析版专用的「清垃圾」判据 ──
# 精析版（`2020-英语-精析版.md`）是 OCR 直接整理稿，正文里混着原卷的排版残渣：
#   `Part II Reading Comprehension` / `Passage 1` / `Passage3` / `Part III Cloze` /
#   `Part IV Writing` + 一整段漏到这里的写作答案（`66.【写作思路】… The Library`）。
# 这些行**没有 markdown 前缀**，会被转换器当正文原样留下 ——
# 落在某道题的折叠块里，读者点开看到一段莫名其妙的英文。
# 规律：它们总是紧贴下一条 `---` 之上（原卷分页处）。所以「从残渣行删到下一个 --- 之前」。
STRAY_BLOCK_RE = re.compile(
    r"^(?:Part\s+[IVX]+\s+(?:Reading\s+Comprehension|Cloze|Writing)|Passage\s?\d+)\s*$")


def strip_stray(lines):
    """删掉 OCR 残渣：从残渣行起，删到下一个 `---` 之前（不含 `---`）。"""
    res, i, n, killed = [], 0, len(lines), 0
    while i < n:
        if STRAY_BLOCK_RE.match(lines[i].strip()):
            i += 1
            killed += 1
            while i < n and lines[i].strip() != "---":
                i += 1
            continue
        res.append(lines[i])
        i += 1
    return res, killed


def insert_struct(lines):
    """在第一个 `## Part ` 之前插 `## 试卷结构` 占位表（转换器按配置整块替换）。

    精析版自己没有「试卷结构」章节，不先放一个占位：
      · 5 列结构表无处安放（转换器只替换、不凭空插入）
      · `## 题目一览` 找不到锚点，会退化成「插到文件第 1 行之后」——直接顶到导语上面

    ★ 已经插过就原样返回。这个脚本要能被 `zhenti_regress.py` 反复重放：
      回归验证拿的 `.bak` 是**已经搬运过**的文件，若无条件插入，
      每重放一次就多出一张占位表，回归永远对不上。
    """
    if any(ln.strip() == "## 试卷结构" for ln in lines):
        return lines
    for i, ln in enumerate(lines):
        if re.match(r"^##\s+Part\s+[IVX]+\b", ln.strip()):
            head = list(lines[:i])
            while head and head[-1].strip() == "":
                head.pop()
            if head and head[-1].strip() != "---":
                head.append("")
                head.append("---")
            return head + [""] + PLACEHOLDER + list(lines[i:])
    return lines


def split_qno(text):
    """`**N.` 之后的内容 → (题干, 粘在题面的第一个选项或 None)。

    ★ 为什么只用一个 `^\\*\\*(\\d{1,2})\\.\\s*(.*)$` 再手工剥 `**`：
      源文件里题面有三种写法，靠一条正则区分会写成一团：
        `**1. Tom sold … now.**`        （整行加粗，闭合 ** 在行尾）
        `**21.** A. practice`           （只有题号加粗，** 紧跟点号）
        `**66. 假定你是李华。** 留学生…`（加粗只包住第一句）
      统一成「先取出 `**N.` 后面的全部，再按第一个 `**` 切成 加粗段 / 其余段」，
      三种写法就是同一个动作，也不怕题面里再出现星号。
    """
    body = text
    if "**" in body:
        head, rest = body.split("**", 1)
        stem = (head.strip() + " " + rest.strip()).strip()
    else:
        stem = body.strip()
    m = OPT_GLUED_RE.match(stem)
    if m:
        return "", f"- **{m.group(1)[0]}.** {m.group(2).strip()}"
    return stem, None


def tidy(lines):
    """压掉多余空行，并把被空行拆开的选项列表重新接上。

    两个必须做的收尾（不做的话转换器接不住）：
    1. **连续空行压成一个**。`flush_block()` 会在块首块尾各补一个空行，
       源文件自己也有空行，叠起来就是双空行；转换器对双空行的容忍度不一致，
       渲染看不出问题但会让回归比对永远报差异。
    2. **选项之间不留空行**。`**51. A．burned**` 拆出来的 `- **A.** burned`
       和源文件里紧随其后的 `- **B.** turned` 之间原本有一条空行 ——
       markdown 会把它们切成**两个列表**，读者看到的是「A 一个列表、B–D 另一个」，
       编号样式还会重来一遍。
    """
    res = []
    for ln in lines:
        if ln.strip() == "":
            if not res or res[-1].strip() == "":
                continue
            res.append("")
            continue
        if (re.match(r"^- \*\*[A-E]\.\*\*", ln.strip()) and res
                and res[-1].strip() == "" and len(res) >= 2
                and re.match(r"^- \*\*[A-E]\.\*\*", res[-2].strip())):
            res.pop()  # 撤掉夹在两个选项之间的那条空行
        res.append(ln)
    return res


def promote(text):
    lines = text.split("\n")
    out = []
    log = {"q": 0, "opt": 0, "passage": 0, "ans": 0, "dash": 0}
    inside = False          # 是否在 <details> 块内
    block = []              # <details> 块的内容
    # ★ 已经有 `## 试卷结构` 就不再插占位表 —— 保证本脚本可被反复重放（见 insert_struct）。
    placed_struct = any(ln.strip() == "## 试卷结构" for ln in lines)

    def flush_block():
        """把 <details> 块的内容吐出来（前置只负责「脱掉 HTML 外壳」）。"""
        if not block:
            return
        body = [ln for ln in block if ln.strip() != "---"]  # 规则 6
        log["dash"] += len(block) - len(body)
        while body and body[0].strip() == "":
            body.pop(0)
        while body and body[-1].strip() == "":
            body.pop()
        if not any(ln.strip().startswith("**答案") for ln in body):
            # 写作范文那几个块没有答案行 —— 补一行，否则转换器不会为它开折叠
            body = ["**答案：参考范文**", ""] + body
        out.append("")
        out.extend(body)
        out.append("")

    for raw in lines:
        s = raw.strip()

        if s == "<details>":
            inside, block = True, []
            continue
        if s == "</details>":
            inside = False
            flush_block()
            block = []
            continue
        if inside:
            if s.startswith("<summary>"):
                continue
            m = ANS_LABEL_RE.match(s)
            if m:
                block.append(f"**答案：{m.group(1).strip()}**")
                log["ans"] += 1
                continue
            block.append(raw)
            continue

        if not placed_struct and re.match(r"^##\s+Part\s+[IVX]+\b", s):
            if out and out[-1].strip() != "":
                out.append("")
            out.extend(PLACEHOLDER)
            placed_struct = True

        m = PASSAGE_RE.match(s)
        if m:
            out.append(f"#### {m.group(1)}")
            log["passage"] += 1
            continue

        m = Q_RE.match(s)
        if m:
            qno = int(m.group(1))
            stem, glued = split_qno(m.group(2))
            if out and out[-1].strip() != "":
                out.append("")
            out.append(f"### 第 {qno} 题")
            out.append("")
            if stem:
                out.append(stem)
                out.append("")
            if glued:
                out.append(glued)
                out.append("")
                log["opt"] += 1
            log["q"] += 1
            continue

        for rx in (OPT_ITEM_RE, OPT_ITEM2_RE):
            m = rx.match(s)
            if m:
                out.append(f"- **{m.group(1)[0]}.** {m.group(2).strip()}")
                log["opt"] += 1
                break
        else:
            out.append(raw)

    if inside:  # 文件末尾没闭合（理论不该发生）
        flush_block()

    return "\n".join(tidy(out)).strip() + "\n", log


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", help="要搬运的源文件")
    ap.add_argument("--spec", help="JSON 清单（含 file / mode 字段）；与 --file 二选一")
    ap.add_argument("--mode", choices=["zuoti", "jingxi"], default="zuoti",
                    help="zuoti=刷题版（HTML details 形态）；jingxi=精析版（只需清 OCR 残渣）")
    ap.add_argument("--out", help="dry-run 输出路径")
    ap.add_argument("--apply", action="store_true", help="覆盖原文件（自动备份）")
    add_logging_args(ap)
    args = ap.parse_args()
    setup_from_args(args)

    mode, target = args.mode, args.file
    if args.spec:
        spec = json.loads(pathlib.Path(args.spec).read_text(encoding="utf-8"))
        target = spec.get("file")
        mode = spec.get("mode", mode)
    LOG.debug("mode=%s · spec=%s · file=%s · apply=%s", mode, args.spec, target, args.apply)
    if not target:
        LOG.error("既没给 --file 也没给 --spec（或 spec 里没有 file 字段）")
        print("必须给 --file 或 --spec")
        return 1

    src = pathlib.Path(target)
    if not src.exists():
        LOG.error("源文件不存在：%s", src)
        print(f"文件不存在: {src}")
        return 1
    text = src.read_text(encoding="utf-8")

    if mode == "jingxi":
        lines, killed = strip_stray(text.split("\n"))
        new = "\n".join(tidy(insert_struct(lines))).strip() + "\n"
        LOG.info("精析版 %s：清 OCR 残渣 %d 处", src.name, killed)
        print(f"{src.name}: [精析版] 清除 OCR 残渣 {killed} 处 · 补 `## 试卷结构` 占位")
    else:
        # ★ 局部变量原叫 `log`，与 logger `LOG` 只差大小写，读起来容易串。
        #   纯改名，不改行为。
        new, stats = promote(text)
        LOG.info("刷题版 %s：题号 %d · 选项 %d · Passage %d · 答案行 %d · 丢弃折叠内 --- %d",
                 src.name, stats["q"], stats["opt"], stats["passage"],
                 stats["ans"], stats["dash"])
        print(f"{src.name}: 题号 {stats['q']} · 选项 {stats['opt']} · Passage {stats['passage']} "
              f"· 答案行 {stats['ans']} · 丢弃折叠内 --- {stats['dash']}")
    print(f"  原 {len(text)} 字符 → 新 {len(new)} 字符")

    if args.apply:
        bak = src.with_suffix(src.suffix + f".orig-{DATE}")
        k = 2
        while bak.exists():
            bak = src.with_suffix(src.suffix + f".orig-{DATE}.{k}")
            k += 1
        shutil.copy2(src, bak)
        src.write_text(new, encoding="utf-8", newline="\n")
        LOG.info("已覆盖 %s，原件 → %s", src.name, bak.name)
        print(f"  已覆盖，原件 → {bak.name}")
    elif args.out:
        p = pathlib.Path(args.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(new, encoding="utf-8", newline="\n")
        LOG.info("dry-run 输出 → %s", p)
        print(f"  dry-run 输出 → {p}")
    else:
        LOG.info("未指定 --out / --apply，未写任何文件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
