#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wire_runtime_layers.py —— 把「检索 / 诊断 / 校准」三层接进 D020–D026 日卡。

背景
----
学习系统七层的实测诊断：输入 100% / 目标分解 90%，但
检索 15% / 诊断 5%（五科错题本全空）/ 校准 20%（整卷模考 0 次）。

日卡里已有的问题（不是「没有」，是「指错了」）：
1. `- [ ] 今日错题已进 Anki 专升本::错题集`
   —— 错题**已经有专门的错题本**（五科各一份 `资料/电子书蒸馏/0X-*/错题本.txt`，
      带 A–E 错因分类、8 列行格式），这行却把错题往 Anki 塞。
      结果：每题都做卡 = 成本高 = 实际一条都不记。**五科错题本至今全空就是这么来的。**
2. `- [ ] **英语** Anki 15min`
   —— 只有复习，没有增量。卡池会枯竭。缺的是「新卡从哪来」的判据。
3. 完全没有「校准」—— 学了两周，不知道自己实际几分。

本脚本只做前两件（零成本，不加时间）。第三件（限时诊断）要占 45 分钟，
只能在 D026 腾时间，单独手改，见该文件的「🔬 周诊断」小节。

改动清单
--------
| 范围 | 原文 | 改成 |
|:--|:--|:--|
| D021–D026 | `- [ ] 今日错题已进 Anki ...` | 错题本判据行（≤3 条 / 错因 A–E / 错 2 次才进 Anki） |
| D021–D025 | `- [ ] **英语** Anki 15min` | 加「新卡 ≤3 张，只从『说不出来』的来」 |
| D020–D026 | `3. 错题进 Anki ...` | 指向对应科目 `错题本.txt` |

★ D026 的 Anki 行**不动** —— 那天 Anki 挪进收口，另改。

安全措施
--------
1. 备份 `<file>.bak-20261025-wire`
2. 每个替换都要求「命中次数 == 1」，否则跳过并报错（不猜位置）
3. 改完检查控制字符（`ord(c) < 32`）—— 本项目踩过 `\\1` 变 `\\x01` 吃掉整行的坑
4. 幂等：已改过的文件不再命中原文，重跑不会叠加

用法
----
    python scripts/wire_runtime_layers.py --dry-run
    python scripts/wire_runtime_layers.py
"""
from __future__ import annotations

import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DAYDIR = pathlib.Path(r"D:\专升本总库\07-学习计划\每日")
BAK = ".bak-20261025-wire"

OLD_WRONG = "- [ ] 今日错题已进 Anki `专升本::错题集`"
NEW_WRONG = (
    "- [ ] **错题本**：今天错了的，按对应科目 `错题本.txt` 追加 **≤3 条**\n"
    "      （章 / 题号 / 考点编号 / **错因 A–E** / 一句话错因）\n"
    "      —— 同一题错**第 2 次**才做成 Anki 卡，第一次只记文本（每题做卡 = 一条都记不成）"
)

OLD_ANKI = "- [ ] **英语** Anki 15min"
NEW_ANKI = (
    "- [ ] **英语** Anki 15min（其中 3min 做新卡：**只从今天读笔记时「说不出来」的那条来**，≤3 张）"
)

OLD_LEDGER = "3. 错题进 Anki `专升本::错题集`"
NEW_LEDGER = (
    "3. 错题追加进 `资料/电子书蒸馏/0X-<科目>/错题本.txt` —— **错因必须选 A–E**，写「粗心」等于没写"
)


def find_day(prefix: str) -> pathlib.Path | None:
    hits = sorted(DAYDIR.glob(f"{prefix}-*.md"))
    return hits[0] if hits else None


def apply_one(text: str, old: str, new: str, label: str, tag: str) -> tuple[str, bool]:
    n = text.count(old)
    if n == 0:
        print(f"    · {tag} {label}: 未命中（可能已改过）")
        return text, False
    if n > 1:
        print(f"    ✗ {tag} {label}: 命中 {n} 次，拒绝自动改")
        return text, False
    print(f"    ✓ {tag} {label}: 1 处")
    return text.replace(old, new), True


def main() -> int:
    dry = "--dry-run" in sys.argv
    if not DAYDIR.is_dir():
        print(f"[ERR] 日卡目录不存在：{DAYDIR}")
        return 1

    plan: list[tuple[str, list[tuple[str, str, str]]]] = []
    for i in range(20, 27):
        tag = f"D{i:03d}"
        ops = []
        if 21 <= i <= 26:
            ops.append((OLD_WRONG, NEW_WRONG, "错题行"))
        if 21 <= i <= 25:          # ★ D026 不动 Anki 行
            ops.append((OLD_ANKI, NEW_ANKI, "Anki行"))
        ops.append((OLD_LEDGER, NEW_LEDGER, "落账3"))
        plan.append((tag, ops))

    changed = 0
    for tag, ops in plan:
        p = find_day(tag)
        if not p:
            print(f"[skip] {tag}: 找不到日卡")
            continue
        text = p.read_text(encoding="utf-8")
        print(f"[{tag}] {p.name}")
        new_text, any_hit = text, False
        for old, new, label in ops:
            new_text, hit = apply_one(new_text, old, new, label, tag)
            any_hit = any_hit or hit
        if not any_hit:
            continue

        bad = [(k + 1, c, ord(c)) for k, ln in enumerate(new_text.split("\n"))
               for c in ln if ord(c) < 32 and c != "\t"]
        if bad:
            print(f"    ✗ 出现控制字符 {bad[:3]} → 不写盘")
            continue

        if dry:
            changed += 1
            continue
        bak = p.with_suffix(p.suffix + BAK)
        if not bak.exists():
            bak.write_text(text, encoding="utf-8", newline="\n")
        p.write_text(new_text, encoding="utf-8", newline="\n")
        changed += 1

    print(f"\n{'[dry-run] 将改' if dry else '已改'} {changed} 张卡")
    return 0


if __name__ == "__main__":
    sys.exit(main())
