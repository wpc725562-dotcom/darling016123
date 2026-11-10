#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""归一 `备考计划/学习日志.jsonl` 里越出受控词表的 mastery / kind 值。

为什么要它（2026-10-25）：
  `npm run check:all` 当时 15 项红 5 项，其中 study-log:check 报了 **54 处**
  字段越界，ledger:check 又报了一遍同样的问题。根因不是"写错了"，而是
  **同一个语义长出了多个写法**，而校验器只认白名单里的那一个：

    mastery  白名单 4 个 (passed/partial/failed/na)，实际用了 8 个
             pass×14 · pending×13 · n/a×8 · learning×4  ← 39 条越界
    kind     白名单 7 个，实际用了 9 个
             audit×12 · note×3                         ← 15 条越界

  这类病这仓库犯过第二次：`check-study-log.mjs` 头部注释记着第一次
  （一条高数写成「高等数学」→ 每日计划误判「高数断档 10 天」）。
  那次是 1 条，这次 54 处。

归一依据（逐条看过原文，不是猜的）：
  · pending ×13 —— 全部是「讲了但还没验收」的 lecture / quiz ⇒ 归 na（未判定）
  · learning ×4 —— 全部是「在学」的 lecture                  ⇒ 归 na（未判定）
  · n/a ×8      —— 全部是 audit，语义就是「不适用」          ⇒ 归 na（同义写法）
  · pass ×14    —— 「学会了」的另一种写法                    ⇒ 归 passed（同义写法）
  · audit ×12   —— 真实新类型（审计/对账/更正/核查）          ⇒ 保留，登记进 KINDS
  · note ×3     —— 语义各不相同，逐条归并到已有类型，不留泛类型：
        行232「3.1 首讲失败…推倒重讲」        ⇒ lecture
        行254「学习日口径修正 · D016…」        ⇒ audit
        行262「1.11 收尾 · 速查卡交付…」        ⇒ summary

护栏：
  1. 每处替换必须命中预期次数，否则整体放弃、不猜位置。
  2. 只动 `"mastery": "…"` / `"kind": "…"` 这两个字段的字面量，
     其余字节原样保留（不重新 dumps，避免键序与转义漂移）。
  3. 幂等：改完再跑一次应报「0 处改动」。
  4. 改完校验每行仍是合法 JSON，且不含控制字符（ord < 32）。

用法：python scripts/normalize-log-schema-2026-10-25.py [--dry-run]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "备考计划" / "学习日志.jsonl"

# ── 全局同义写法归一：(字段, 旧值, 新值, 预期条数) ────────────────────
GLOBAL_RULES = [
    ("mastery", "pass", "passed", 14),
    ("mastery", "n/a", "na", 8),
    ("mastery", "pending", "na", 13),
    ("mastery", "learning", "na", 4),
]

# ── note 逐条归并：(title 关键词, 新 kind, 说明) ──────────────────────
# 用 title 关键词定位而不是行号 —— 行号会随增删漂移，title 是内容。
NOTE_RULES = [
    ("3.1 首讲失败", "lecture", "首讲失败也是讲课，只是密度没对上"),
    ("学习日口径修正", "audit", "对账/更正类，与 audit 同义"),
    ("1.11 收尾", "summary", "收尾交付，与 summary 同义"),
]


def count_field(lines: list[str], field: str, value: str) -> int:
    """数某个字段等于某值的行数（只认 JSON 里的字面量，不认正文）。"""
    pat = re.compile(rf'"{field}":\s*"{re.escape(value)}"')
    return sum(1 for ln in lines if pat.search(ln))


def main() -> int:
    dry = "--dry-run" in sys.argv
    if not LOG.exists():
        print(f"找不到 {LOG}")
        return 1

    raw = LOG.read_text(encoding="utf-8")
    lines = raw.split("\n")

    changed = 0
    report: list[str] = []

    # ① 全局同义归一
    for field, old, new, expect in GLOBAL_RULES:
        got = count_field(lines, field, old)
        if got == 0:
            report.append(f"  ⏭️  {field}: {old!r} 已是 0 条，跳过（幂等）")
            continue
        if got != expect:
            print(f"✗ 中止：{field}={old!r} 预期 {expect} 条，实得 {got} 条。")
            print("  条数不符说明文件已被改过，脚本不猜位置。请先人工核对。")
            return 1
        pat = re.compile(rf'"{field}":(\s*)"{re.escape(old)}"')
        for i, ln in enumerate(lines):
            if pat.search(ln):
                lines[i] = pat.sub(rf'"{field}":\1"{new}"', ln, count=1)
                changed += 1
        report.append(f"  ✅ {field}: {old} → {new}  {got} 条")

    # ② note 逐条归并（先数清总数，再按 title 关键词定位）
    note_total = count_field(lines, "kind", "note")
    if note_total:
        if note_total != len(NOTE_RULES):
            print(f"✗ 中止：kind=note 实得 {note_total} 条，规则只写了 {len(NOTE_RULES)} 条。")
            print("  新增的 note 记录需要先人工判定语义，脚本不猜。")
            return 1
        for keyword, new_kind, why in NOTE_RULES:
            hits = [i for i, ln in enumerate(lines)
                    if '"kind": "note"' in ln and keyword in ln]
            if len(hits) != 1:
                print(f"✗ 中止：title 含 {keyword!r} 的 note 记录实得 {len(hits)} 条（应为 1）。")
                return 1
            i = hits[0]
            lines[i] = lines[i].replace('"kind": "note"', f'"kind": "{new_kind}"', 1)
            changed += 1
            report.append(f"  ✅ note → {new_kind}  「{keyword}…」  （{why}）")
    else:
        report.append("  ⏭️  kind=note 已是 0 条，跳过（幂等）")

    print("归一计划：")
    print("\n".join(report))
    print(f"\n合计改动 {changed} 处")

    if dry:
        print("（--dry-run，未写盘）")
        return 0
    if changed == 0:
        print("无需改动，文件原样保留。")
        return 0

    # ③ 写盘前校验：每行仍是合法 JSON
    bad = []
    for n, ln in enumerate(lines, 1):
        if not ln.strip():
            continue
        try:
            json.loads(ln)
        except json.JSONDecodeError as e:
            bad.append((n, str(e)))
    if bad:
        print(f"✗ 中止：{len(bad)} 行不再是合法 JSON，未写盘。")
        for n, e in bad[:5]:
            print(f"    行{n}: {e}")
        return 1

    out = "\n".join(lines)
    # ④ 写盘前校验：不得引入控制字符（\t \n 除外）—— 踩过 `\1` 变八进制吃掉整行的坑
    ctrl = [(i, ord(c)) for i, c in enumerate(out) if ord(c) < 32 and c not in "\n\t"]
    if ctrl:
        print(f"✗ 中止：检出 {len(ctrl)} 个控制字符，未写盘。前 5 个：{ctrl[:5]}")
        return 1

    LOG.write_text(out, encoding="utf-8")
    print(f"\n✅ 已写入 {LOG}")
    print("   下一步：node scripts/check-study-log.mjs 应转绿")
    return 0


if __name__ == "__main__":
    sys.exit(main())
