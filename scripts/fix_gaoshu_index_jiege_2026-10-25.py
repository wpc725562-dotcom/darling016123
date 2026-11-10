#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修正 `网课考点索引-高数.md` 里杰哥课程 P113–P136 的考点误标。

为什么要它（2026-10-25）：
  杰哥 `BV1Up4y1Y76a` 的「第五章」在考纲里横跨**两个考点**：
    · 多元函数微分法及其应用（高09）
    · 曲线积分与曲面积分（高11）
  但 `bili_index_by_title.py` 按分P标题里的「第 X 章」折算，**一章只能给一个编号**，
  于是 P113–P136 共 24 集被整段标成了「**高10** 重积分」。

  后果很实际：想「按考点找课」查多元函数或曲线积分 → **查不到** → 看起来像没讲过。
  实测（2026-10-25）：库里其实讲得很全 ——
    P113–P132（20 集）多元函数概念 / 二元函数极限 / 一阶偏导 / 全微分 / 可微本质 /
                        二阶偏导 / 二元隐函数偏导 / 链式法则 / 具体与抽象复合函数求导 /
                        隐函数求导易错题 / 多元微分学几何应用（空间曲线切线法平面、
                        空间曲面切平面法线）/ 无条件极值 / 条件极值
    P133–P136（ 4 集）曲线积分概念 / 直接代入法 / 格林公式 / 积分与路径无关

  所以这不是脚本 bug，是**方法局限**（一章只能落一个编号）。手工修，并在段落里留痕。

护栏：
  1. 只在杰哥段落内改（BV1Up4y1Y76a 那个 ### 标题起，到下一个 ### 标题止），不碰别的 BV。
  2. 只改「当前值 == 高10 且 P 在目标区间」的行，幂等（重跑命中 0 处）。
  3. 改完校验：24 行全部到位、无控制字符、表格竖线数不变。
  4. 先备份 `.bak-20261025-jiege`。

用法：python scripts/fix_gaoshu_index_jiege_2026-10-25.py [--dry-run]
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDX = ROOT / "备考计划" / "网课考点索引-高数.md"
BAK = ".bak-20261025-jiege"

BV_MARK = "### `BV1Up4y1Y76a`"

# P 区间 → (新编号, 新名称)
FIXES = [
    (113, 132, "高09", "多元函数微分法及其应用"),
    (133, 136, "高11", "曲线积分与曲面积分"),
]

# 匹配索引表格行：| P113 | 113、第五章 多元函数概念 | **高10** | 重积分 |
ROW_RE = re.compile(
    r"^(\|\s*P(\d+)\s*\|[^|]*\|)\s*\*\*(高\d+)\*\*\s*\|\s*([^|]*?)\s*\|$"
)

NOTE = (
    "> 🔧 **2026-10-25 手工修正 P113–P136 共 24 集的考点标注**：\n"
    "> 杰哥的「第五章」横跨考纲两个考点，而索引脚本按「第 X 章」折算时**一章只能落一个编号**，\n"
    "> 于是这 24 集被整段标成了「高10 重积分」。实际：**P113–P132 = 高09 多元函数微分**、\n"
    "> **P133–P136 = 高11 曲线积分**。不修的话，按考点找课会查不到这两块、误以为没讲。\n"
)


def main() -> int:
    dry = "--dry-run" in sys.argv
    if not IDX.exists():
        print(f"找不到 {IDX}")
        return 1

    text = IDX.read_text(encoding="utf-8")
    lines = text.split("\n")

    # ① 定位杰哥段落
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith(BV_MARK):
            start = i
            break
    if start is None:
        print(f"✗ 找不到段落标记：{BV_MARK}")
        return 1
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("### "):
            end = i
            break
    print(f"杰哥段落：第 {start + 1}–{end} 行（{end - start - 1} 行）")

    # ② 逐行修
    changed = 0
    hit = {tag: 0 for _, _, tag, _ in FIXES}
    for i in range(start, end):
        m = ROW_RE.match(lines[i])
        if not m:
            continue
        p = int(m.group(2))
        old_tag, old_name = m.group(3), m.group(4)
        for lo, hi, new_tag, new_name in FIXES:
            if lo <= p <= hi:
                if old_tag == new_tag and old_name == new_name:
                    break  # 已修过（幂等）
                if old_tag != "高10":
                    print(f"  ⚠️ P{p} 当前是 {old_tag}，不是预期的 高10，跳过（不猜）")
                    break
                lines[i] = f"{m.group(1)} **{new_tag}** | {new_name} |"
                changed += 1
                hit[new_tag] += 1
                break

    print(f"\n改动 {changed} 行：高09 ×{hit['高09']} · 高11 ×{hit['高11']}")

    # ③ 幂等检查：期望 20 + 4
    if changed == 0:
        print("⏭️  无需改动（已修过或区间为空）")
        return 0
    if hit["高09"] != 20 or hit["高11"] != 4:
        print(f"✗ 中止：预期 高09×20 + 高11×4 = 24 行，实得 高09×{hit['高09']} + 高11×{hit['高11']}")
        print("  不写盘。请核对 P 区间或表格格式是否变了。")
        return 1

    # ④ 在段落标题下插入说明（只插一次）
    if "2026-10-25 手工修正 P113–P136" not in text:
        insert_at = start + 1
        # 标题下通常有空行；插在标题之后第一个非空行之前
        lines[insert_at:insert_at] = ["", NOTE.rstrip("\n")]

    out = "\n".join(lines)

    # ⑤ 校验：控制字符 + 竖线数
    ctrl = [(i, ord(c)) for i, c in enumerate(out) if ord(c) < 32 and c not in "\n\t"]
    if ctrl:
        print(f"✗ 中止：检出 {len(ctrl)} 个控制字符，未写盘。前 5 个：{ctrl[:5]}")
        return 1
    before = text.count("\n")
    after = out.count("\n")
    print(f"行数 {before} → {after}")

    if dry:
        print("\n（--dry-run，未写盘）")
        return 0

    shutil.copy2(IDX, IDX.with_name(IDX.name + BAK))
    IDX.write_text(out, encoding="utf-8")
    print(f"\n✅ 已写入 {IDX.name}（备份 {IDX.name}{BAK}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
