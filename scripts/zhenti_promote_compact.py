#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scripts/zhenti_promote_compact.py —— 「紧凑形态 → 模板形态」前置提升。

为什么需要这一步
----------------
模板要求每道题是一个 `### 第 N 题 · 主题` 标题 + 折叠解析。但早年整理出来的
真题页，有几个大题是用**紧凑形态**记的 —— 信息没丢，只是没拆成题：

| 形态 | 长什么样 | 典型出处 |
|---|---|---|
| `table` | `\\| 21 \\| 一个 C 程序里只有一个 main \\| √ \\|` | 2023/2021 判断题 |
| `bold_items` | `**1. 字符数组有哪些输入输出方式？**` | 2023 填空/简答 |
| `bare_items` | `31. 三种基本结构：顺序、选择、循环` | 2021 填空题 |

这些形态 zhenti_convert.py **故意不处理** —— 它的输入契约是「每题一个 `### N.`」，
硬塞表格解析进去会把转换器变成一个什么都吃的泥团，改一处崩三处。

所以拆成两步：本脚本先把紧凑形态**原样搬**成 `### N.` 形态（不重写一个字），
再交给 zhenti_convert.py 去做编号 / 折叠 / 结构表 / 速查表。职责清楚，
而且第二步是幂等可回归的（见 zhenti_regress.py）。

用法
----
    python scripts/zhenti_promote_compact.py --spec scripts/zhenti_cfg/promote2023.json
    python scripts/zhenti_promote_compact.py --spec ... --apply     # 覆盖（自动备份）

安全
----
默认 dry-run，只打印将要改动的行数与片段。`--apply` 才落盘，落盘前备份到
`<file>.pre-promote-<日期>`。**不会**改动没有被 spec 点名的章节。
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

# ★ E3（2026-09-20）：诊断走 logging（stderr），正式输出仍走 main() 里的 log()/print。
from zhenti_log import add_logging_args, get_logger, setup_from_args  # noqa: E402

LOG = get_logger(__name__)

DATE = os.environ.get("ZHENTI_DATE") or datetime.date.today().isoformat()

SEC_RE = re.compile(r"^##\s+(.+?)\s*$")
ROW_RE = re.compile(r"^\|(.+)\|\s*$")
BOLD_ITEM_RE = re.compile(r"^\*\*(\d{1,2})\.\s*(.+?)\*\*\s*$")
BARE_ITEM_RE = re.compile(r"^(\d{1,2})\.(?!\d)\s*(\S.*)$")
HR_RE = re.compile(r"^-{3,}\s*$")


def cells(line):
    """把 `| a | b | c |` 拆成 ['a','b','c']（去掉首尾空段）。"""
    parts = [c.strip() for c in line.strip().strip("|").split("|")]
    return parts


def is_sep_row(parts):
    return all(re.fullmatch(r":?-{2,}:?", c or "") for c in parts) and parts


def promote_table(lines, i, spec, log):
    """从下标 i 起找一张表，产出 `### N.` 块。返回 (新行, 停止下标)。

    ★ 表头必须靠「结构」认出来，不能靠「第一行」——
      调用方传进来的 `lines` 前面可能还有空行和引言（`rest` 从章节正文开头算起），
      直接拿 lines[0] 当表头会把空行或引言当表头，然后**表头行本身**被当成
      第一条数据，凭空多出一题（`### #. 命题`）——实测踩过。
      判据：第一行「首列是纯数字」的表格行才是数据行，它上面那行是表头。
    """
    # ── 1. 定位表头：第一行「首列是纯数字」的数据行，往上找最近的一行表格行 ──
    h = None
    j = i
    while j < len(lines):
        s = lines[j].strip()
        if not ROW_RE.match(s):
            j += 1
            if h is not None:
                break
            continue
        parts = cells(s)
        if parts and re.fullmatch(r"\d{1,2}", parts[0]) and not is_sep_row(parts):
            h = j
            break
        j += 1
    if h is None:
        log("    表格：没找到数据行，跳过")
        return [], i
    head_idx = None
    for k in range(h - 1, i - 1, -1):
        if ROW_RE.match(lines[k].strip()) and not is_sep_row(cells(lines[k])):
            head_idx = k
            break
    header = cells(lines[head_idx]) if head_idx is not None else []
    idx = {name: (header.index(name) if name in header else -1)
           for name in ("qno", "stem", "ans", "why")}
    for k, v in (spec.get("cols") or {}).items():
        idx[k] = v

    norm = spec.get("ans_normalize") or {}
    split_re = re.compile(spec["ans_split"]) if spec.get("ans_split") else None
    label = spec.get("hint") or ""
    out = []
    n_item = 0
    i = h
    while i < len(lines):
        s = lines[i].strip()
        if not ROW_RE.match(s):
            break
        parts = cells(s)
        if is_sep_row(parts):
            i += 1
            continue
        if len(parts) <= max(idx["qno"], idx["stem"], idx["ans"]):
            i += 1
            continue
        qno, stem, ans = parts[idx["qno"]], parts[idx["stem"]], parts[idx["ans"]]
        why = parts[idx["why"]] if 0 <= idx["why"] < len(parts) else ""
        # ans_split：把「答案 + 括号里的解释」拆开
        #   （2021 判断题的答案列写成 `×（含 \0 占 2）`，
        #    整串塞进 `> **答案：…**` 会让加粗包住解释，速查表里也太长）
        if split_re:
            m2 = split_re.match(ans.strip())
            if m2:
                ans = m2.group(1)
                if not why:
                    why = m2.group(2)
        for k, v in norm.items():
            if ans.strip() == k:
                ans = v
                break
        out.append(f"### {qno}. {stem}")
        out.append("")
        out.append(f"> **答案：{ans}**" + (f" · 考点 {label}" if label else ""))
        out.append("")
        if why:
            out.append(why)
            out.append("")
        out.append("")
        n_item += 1
        i += 1
    log(f"    表格 → {n_item} 题")
    return out, i


def promote_items(lines, i, spec, log, bold=True):
    """把 `**N. 题面**` 或 `N. 题面` 形态的列表搬成 `### N. 题面`。"""
    pat = BOLD_ITEM_RE if bold else BARE_ITEM_RE
    out = []
    n_item = 0
    sub_lead = spec.get("ans_lead")
    sub_new = spec.get("ans_lead_new")
    while i < len(lines):
        s = lines[i].strip()
        m = pat.match(s)
        if m:
            out.append(f"### {m.group(1)}. {m.group(2)}")
            out.append("")
            n_item += 1
            i += 1
            continue
        if sub_lead and s == sub_lead:
            out.append(sub_new)
            i += 1
            continue
        out.append(lines[i])
        i += 1
    log(f"    列表 → {n_item} 题")
    return out, i


def apply_subs(lines, subs, log):
    """按 spec.line_subs 做行内替换：[[正则, 替换], …]。

    只作用于**被点名章节**的正文 —— 同一份卷子里 `> 答案：**` 这种写法
    可能同时出现在别的章节，全局替换会误伤。
    """
    if not subs:
        return lines
    out, cnt = [], 0
    for ln in lines:
        new = ln
        for pat, rep in subs:
            new2, k = re.subn(pat, rep, new)
            if k:
                cnt += k
                new = new2
        out.append(new)
    if cnt:
        log(f"    行内替换 {cnt} 处")
    return out


def run(text, spec, log):
    lines = text.split("\n")
    targets = spec.get("sections") or {}
    res = []
    i, n = 0, len(lines)
    hit = 0
    while i < n:
        s = lines[i].strip()
        m = SEC_RE.match(s)
        if m and m.group(1) in targets:
            name = m.group(1)
            sp = targets[name]
            res.append(lines[i])
            i += 1
            # ── 先把本节正文整段收下来（到下一个 `## ` 为止）──
            body = []
            while i < n:
                if SEC_RE.match(lines[i].strip()) and lines[i].strip().startswith("## "):
                    break
                body.append(lines[i])
                i += 1
            # ── 定位形态起点：跳过引言，停在第一个表格行 / 题号行 ──
            k = 0
            while k < len(body) and body[k].strip() and not ROW_RE.match(body[k].strip()) \
                    and not BOLD_ITEM_RE.match(body[k].strip()) \
                    and not BARE_ITEM_RE.match(body[k].strip()):
                k += 1
            head, rest = body[:k], body[k:]
            if sp.get("form") == "table":
                blk, stop = promote_table(rest, 0, sp, log)
                # ★ 表格后面往往还有正文（2023 判断题表后有「四条值得展开的」）。
                #   promote_table 只吃表，剩下的必须接回去 —— 否则静默丢内容。
                blk = blk + list(rest[stop:])
            elif sp.get("form") == "bold_items":
                blk, _ = promote_items(rest, 0, sp, log, bold=True)
            elif sp.get("form") == "bare_items":
                blk, _ = promote_items(rest, 0, sp, log, bold=False)
            else:
                blk = list(rest)
            blk = apply_subs(blk, sp.get("line_subs") or [], log)
            res.extend(head)
            res.extend(blk)
            hit += 1
            continue
        res.append(lines[i])
        i += 1
    log(f"  处理章节 {hit} 个")
    return "\n".join(res)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", help="dry-run 输出路径（供回归脚本串管线用）")
    ap.add_argument("--apply", action="store_true")
    add_logging_args(ap)
    args = ap.parse_args()
    setup_from_args(args)

    def log(x):
        print(x)

    sp = json.loads(pathlib.Path(args.spec).read_text(encoding="utf-8"))
    src = pathlib.Path(sp["file"])
    LOG.debug("spec=%s → file=%s · apply=%s · out=%s", args.spec, src, args.apply, args.out)
    if not src.exists():
        LOG.error("源文件不存在：%s", src)
        log(f"文件不存在: {src}")
        return 1
    text = src.read_text(encoding="utf-8")
    new = run(text, sp, log)
    log(f"  {src.name}: {len(text)} → {len(new)} 字符")
    LOG.info("promote %s：%d → %d 字符", src.name, len(text), len(new))
    if new == text:
        LOG.info("%s 无改动（promote 规则对它是恒等的）", src.name)
        log("  无改动")
    if args.apply:
        bak = src.with_suffix(src.suffix + f".pre-promote-{DATE}")
        # ★ 备份**只写一次**（2026-09-20，修 D4）。
        #   原来没有存在性检查，同名直接 shutil.copy2 覆盖 ——
        #   同一天跑两次，第二次就把**第一次（= 更早、更接近原始）的备份**冲掉了。
        #   `--apply` 是可重复执行的（改了 promote 规则要重跑），所以这不是假想场景。
        #   做法与 zhenti_convert.py 的 `.bak-<日期>` 编号保持一致（base → .2 → .3 …）。
        k = 2
        while bak.exists():
            bak = src.with_suffix(src.suffix + f".pre-promote-{DATE}.{k}")
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
        LOG.info("dry-run，未写盘（加 --apply 落盘）")
        log("  （dry-run，未写盘；加 --apply 落盘）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
