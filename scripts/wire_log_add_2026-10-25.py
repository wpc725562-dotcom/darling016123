#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 D020–D026 七张日卡的「落账」一条改成走 `npm run log:add`。

为什么要它（2026-10-25）：
  日卡收口第 1 条写的是「写进 `学习日志.jsonl`」—— 这是一句**没有闸门**的指令。
  结果是 174 条 quiz 里有 **0 条**带考点编号，而编号是掌握度引擎的唯一口粮：
  同一个 key 出现 ≥3 次才可能判过关，没编号 ⇒ 引擎读数是空的 ⇒
  错题本「考点编号」列填不出来 ⇒ 五科错题本全空 ⇒ 诊断层 5%。

  已有 `scripts/log-add.mjs` 会在**写盘前**拦住无编号的 quiz（退出码 1，不写盘），
  但 174 条历史全是手写绕过去的 —— 「规范写在文档里」已证明不够，得做成绕不过的入口。

  所以日卡的落账动作改成：**必须走 `npm run log:add`**。
  同时检查器侧已加硬拦：2026-10-25 起的新 quiz 无编号 = `study-log:check` 报错。

护栏：
  1. 每张卡必须命中恰好 1 处，否则跳过该卡并报告（不猜位置）。
  2. 幂等：已含 `log:add` 的卡直接跳过。
  3. 先备份 `.bak-20261025-logadd`。
  4. 改完检查控制字符。

用法：python scripts/wire_log_add_2026-10-25.py [--dry-run]
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DAILY = Path("D:/专升本总库/07-学习计划/每日")
BAK = ".bak-20261025-logadd"

# (匹配旧行, 替换新行) —— 两种原格式
RULES = [
    (
        "1. 写进 `备考计划/学习日志.jsonl`",
        "1. 写进 `备考计划/学习日志.jsonl` —— **必须走 `npm run log:add`**\n"
        "   （手写会绕过编号检查：174 条 quiz 有 **0 条**带考点编号，就是这么来的。\n"
        "   无编号 ⇒ 掌握度引擎空转 ⇒ 错题本「考点编号」列填不出来 ⇒ 五科错题本全空）",
    ),
    (
        "1. 写进 `学习日志.jsonl`",
        "1. 写进 `学习日志.jsonl` —— **必须走 `npm run log:add`**\n"
        "   （手写会绕过编号检查。quiz 的 title 里必须带 `#C006` / `#D05` / `#M013` / `#E007` 这类编号）",
    ),
]

TARGETS = sorted(DAILY.glob("D02[0-6]-*.md"))


def main() -> int:
    dry = "--dry-run" in sys.argv
    if not DAILY.exists():
        print(f"找不到 {DAILY}")
        return 1
    if not TARGETS:
        print("找不到 D020–D026 日卡")
        return 1

    changed = 0
    for f in TARGETS:
        text = f.read_text(encoding="utf-8")
        if "log:add" in text:
            print(f"  ⏭️  {f.name} 已含 log:add，跳过（幂等）")
            continue

        hit_rule = None
        for old, new in RULES:
            # 行首锚定，避免误伤「（写进 `学习日志.jsonl`，下周拿来对比）」这类行内提及
            if re.search(rf"^{re.escape(old)}$", text, re.MULTILINE):
                hit_rule = (old, new)
                break
        if not hit_rule:
            print(f"  ⚠️  {f.name} 找不到唯一的「1. 写进 …」行，跳过（不猜位置）")
            continue

        old, new = hit_rule
        n = len(re.findall(rf"^{re.escape(old)}$", text, re.MULTILINE))
        if n != 1:
            print(f"  ⚠️  {f.name} 命中 {n} 处（应为 1），跳过")
            continue

        out = re.sub(rf"^{re.escape(old)}$", new.replace("\\", "\\\\"), text, count=1, flags=re.MULTILINE)

        ctrl = [(i, ord(c)) for i, c in enumerate(out) if ord(c) < 32 and c not in "\n\t"]
        if ctrl:
            print(f"  ✗ {f.name} 检出控制字符，跳过。前 5 个：{ctrl[:5]}")
            continue

        if not dry:
            shutil.copy2(f, f.with_name(f.name + BAK))
            f.write_text(out, encoding="utf-8")
        changed += 1
        print(f"  ✅ {f.name}")

    print(f"\n合计改动 {changed} 张卡" + ("（--dry-run，未写盘）" if dry else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
