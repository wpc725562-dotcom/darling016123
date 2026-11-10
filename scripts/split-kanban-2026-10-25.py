#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 `学习进度看板.md` 的历史流水切出去，本体只留当前状态。

为什么要它（2026-10-25）：
  看板 161 KB / 380 行，但它自称「AI 跨会话交接的**单一事实源**」。
  问题在于 161 KB **超过任何一次能完整读入的上下文** —— 这个文件已经不可能
  被"读完"，只能被 grep。更糟的是它的七个区块里**四个停在 9 月**：

    上次会话完成的事   → 2026-09-09（46 天前）
    本周任务           → 2026-09-07 ~ 09-13（46 天前，还挂着 7 条未打勾）
    一句话当前状态     → 最新一条 10-17
    科目进度条         → 最后更新 09-24

  只有顶部那条 `last_updated` 在动 ⇒ 它已从「看板」退化成「日志堆积」。
  它甚至留着 `每日配额 4-5h`（与 2026-10-22 定的 3h 是两套数）和
  「截至本次会话还没做过任何一道题」（此时日志已有 174 条 quiz）。

切法（不删任何信息，逐字搬出）：
  归档 ①  原第   1– 74 行  头部 + last_updated 历史栈（单行最长 6854 字符）
  归档 ②  原第  76– 93 行  「一句话当前状态」里的历史条目 + 四科旧状态
  归档 ③  原第 107–249 行  2026-09-09 会话完整记录 + 09-07~09-13 本周任务
  保留    原第  94–106 行  三次自我顿悟 / 教学法体系 / 已知缺口（长期有效）
  保留    原第 250–380 行  待验证区 / 科目进度条 / 弱项画像 / 快速索引

新增（替掉过时区块）：
  · 当前状态表（进度引自 `章节地图-2026-10-23.md`，断档数由 study-log:check 现算）
  · 当前阶段与配额（3h 口径 + 战略放弃）
  · 上次会话（D018 · 2026-10-24，来自学习日志）
  · 本周任务（2026-10-19 ~ 10-25，来自学习日志与日卡）

护栏：
  1. 按**标题标记**定位，不按行号 —— 行号会漂，标题是内容。
  2. 归档文件逐字保留原文，不重排、不改写。
  3. 幂等：若检测到新头部已存在（含 `_archive/看板历史.md`），直接退出不改。
  4. 写完校验：表格行数一致、无控制字符。

用法：python scripts/split-kanban-2026-10-25.py [--dry-run]
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOARD = ROOT / "备考计划" / "学习进度看板.md"
ARCHIVE = ROOT / "备考计划" / "_archive" / "看板历史.md"

MARK_STATE = "## 🎯 一句话当前状态"
MARK_AWAKE = "**🎯 学生三次自我顿悟**"
MARK_PHASE = "## 📌 当前阶段"
MARK_VERIFY = "## 🔍 待验证区"

HEADER = """# 📊 学习进度看板（AI 交接单一事实源）

> 🤖 **本文件是 AI 教练跨会话交接的核心文件**，但它**只放当前状态**。
> 📦 **历史流水已迁出** → `备考计划/_archive/看板历史.md`
>    （2026-10-25 搬出：原 161 KB / 380 行里，第 1–74 行是 `last_updated` 历史栈、
>    第 107–249 行是 2026-09 的会话详情。原因：161 KB 超过任何一次能完整读入的上下文，
>    而看板的职责是回答「我现在学到哪了」，不是记日记。）
> 📌 **进度的唯一事实源是 `07-学习计划/章节地图-2026-10-23.md`** —— 本文件的进度数字引自它并注明日期。
> 🔄 **更新协议**：会话结束只刷新「当前状态 / 上次会话 / 本周任务」三区。
>    ⚠️ **不要往这里追加历史**：流水写 `备考计划/学习日志.jsonl`，复盘写 `_archive/看板历史.md`。

**last_updated**: 2026-10-25（03:05 重构：历史栈迁出 · 补当前状态快照 · 配额改 3h 口径）
"""

NEW_STATE = """
---

## 🎯 当前状态（2026-10-25 · D019）

**距大概率考试日 2027-03-28 还有 154 天。**

| 科目 | 分值 | 进度 | 最近动作 | 状态 |
|:---|--:|:---|:---|:--:|
| 计算机 | 200 | C 语言 **11/11 ✅** · 数据结构 **3.5/9** | 2.5 树：术语 + 结点数公式全对（10-24） | 🟡 |
| 高数 | 100 | **26/70 节**（约 37 分） | 3.5 三角代换收口：`∫dx/√(36−x²)` 四步全对（10-24） | 🟡 |
| 英语 | 100 | 阅读 🟡 · 完形 🟡 · **语法填空 / 作文 / 词形转换 从未练** | 2022 完形余 7 空 5/7（10-23） | 🟠 |
| 政治 | 100 | **0** | 未启动 | 🔴 |

**断档（按考试科目合并 · `npm run study-log:check` 现算）**

| 考试科目 | 落账条数 | 最近 | 断档 |
|:---|--:|:---|:---|
| 计算机 | 167 | 2026-10-24 | — （C语言 135 / 数据结构 23 / 计算机 9） |
| 高等数学 | 60 | 2026-10-24 | — |
| 英语 | 34 | 2026-10-23 | 断 1 天 |
| 政治 | 0 | — | **从未落账** |

**三个真正的缺口（不是「没资料」，是「没做」）**

1. **政治 0** —— 100 分、占 20%，四科里唯一完全没开始的。启动日 **2026-10-26（明天）**，
   路线见 `政治启动路线-第1周-2026-10-26至11-01.md`（19 篇 / 7 天 / 每天 25 分钟）。
2. **数据结构 2.5 遍历未过** —— 10-24 收口时推到 10-25；2.4 串/数组/广义表未开。
3. **错题本五科全空** —— 不是懒：`学习日志.jsonl` 174 条 quiz 里 **0 条带考点编号**，
   错题本的「考点编号」列填不出来。已加硬拦：`2026-10-25` 起新 quiz 无编号 = 检查报错。
"""

NEW_PHASE = """
## 📌 当前阶段与配额

| 事项 | 口径 | 依据 |
|:---|:---|:---|
| 每日总配额 | **3 小时**（高产日实测，不是 4.5h） | `00-先看这个.md` 规则 2 |
| 排课顺序 | **政治排最前**（唯一 0 进度的科目） | 裁决：政治优先 → 真题优先 → 建库让位 |
| 复检 | 只走 Anki；**错题进错题本不进 Anki** | `00-先看这个.md` 规则 1、4 |
| 校准 | **每周日一次限时诊断**（轮换 高数 → 计算机 → 政治） | `00-先看这个.md` 规则 5；D026 首次 |
| 战略放弃 | 高数 G8 空间解析几何 / 傅里叶 / 交错级数 / KMP / 英语汉译英·概要·议论文 | `总体规划-2027-2026-10-24.md` |
"""

NEW_LAST = """
## ✅ 上次会话（D018 · 2026-10-24）

**有效学习 2h21m**（00:22–02:43）· Anki 到期 107 张全为复习卡。

- **高数 3.5 三角代换收口**：`∫dx/√(36−x²)` 四步全对，**第 ④ 步「换回」第一次自己走出来**
  （此前 10-23 三次都缺这一步）。
- **数据结构 2.5 树**：术语三连测（叶子 / 深度全对，树的度连错两次后修正）·
  结点数公式 1001/1000/2000 三题全对 · 符号体系复检 7 结点树四空全对。
- **未完成**：2.5 树的**遍历**未过，推到 10-25。

## 📝 本周任务（2026-10-19 ~ 10-25）

- [x] 高数 3.4 根式代换收口（10-23：四步全对，且避开了 `dx = 2t dt` 陷阱）
- [x] 高数 3.5 三角代换三型闭环（10-23：sin / tan / sec 全部走通）
- [x] 数据结构 2.1–2.3 首讲 + 验收（10-23：出栈序列判据真正掌握）
- [x] 数据结构 2.5 术语 + 结点数公式（10-24）
- [ ] **数据结构 2.5 遍历**（推到 10-25）
- [ ] 数据结构 2.4 串 / 数组 / 广义表（KMP 跳过）
- [ ] **政治 10-26 启动**（第 1 周 19 篇 / 每天 25 分钟）
"""

ARCHIVE_HEAD = """# 📦 学习进度看板 · 历史归档

> 2026-10-25 从 `学习进度看板.md` 切出。**不删信息：以下是原文逐字搬出，未做任何改写。**
>
> 切出原因：原文件 161 KB / 380 行，其中第 1–74 行是 `last_updated` 历史栈
> （**单行最长 6854 字符**），第 107–249 行是 2026-09-09 那次会话的完整记录和
> 09-07~09-13 那一周的任务清单。这些内容本身有价值，但它们让看板
> **无法被完整读入上下文**，而看板的职责是「回答我现在学到哪了」。
>
> 今后：**流水写 `备考计划/学习日志.jsonl`**（结构化、可统计），
> 本文件只做冷归档，不再追加日常记录。

---

## 一、原头部 + last_updated 历史栈（原第 1–74 行）

"""

ARCHIVE_MID = """
---

## 二、「一句话当前状态」里的历史条目 + 四科旧状态（原第 76–93 行）

> 这部分记录的是 2026-10-17 及更早的每日状态。最新状态见看板本体「当前状态」表。

"""

ARCHIVE_TAIL = """
---

## 三、2026-09-09 会话完整记录 + 2026-09-07~09-13 本周任务（原第 107–249 行）

> 这一段包含看板**最早期的完整教学实录**（20 分钟微课 + 6 题实测、第二轮实测、
> 那一周的全部任务清单与逐条销账）。信息密度很高，是「零基础怎么起步」的一手档案。
> 但它停在 2026-09-13，此后 6 周的进展都在 `学习日志.jsonl` 里。
"""


def main() -> int:
    dry = "--dry-run" in sys.argv
    if not BOARD.exists():
        print(f"找不到 {BOARD}")
        return 1

    text = BOARD.read_text(encoding="utf-8")
    if "_archive/看板历史.md" in text:
        print("⏭️  已拆分过（头部已含归档指针），不重复执行。")
        return 0

    lines = text.split("\n")

    def find(marker: str) -> int:
        for i, ln in enumerate(lines):
            if ln.startswith(marker):
                return i
        raise SystemExit(f"✗ 找不到标记：{marker}")

    i_state = find(MARK_STATE)
    i_awake = find(MARK_AWAKE)
    i_phase = find(MARK_PHASE)
    i_verify = find(MARK_VERIFY)

    # 切片（0-based）
    part_head = lines[0:i_state]              # 原 1..74
    part_oldstate = lines[i_state + 1:i_awake]  # 原 76..93
    part_sep = lines[i_phase:i_verify]        # 原 107..249
    keep_long = lines[i_awake:i_phase]        # 原 94..106
    keep_tail = lines[i_verify:]              # 原 250..380

    print("切片核对：")
    print(f"  归档① 原第   1–{i_state:>3} 行  {len(part_head):>4} 行  last_updated 历史栈")
    print(f"  归档② 原第 {i_state+2:>3}–{i_awake:>3} 行  {len(part_oldstate):>4} 行  旧每日状态")
    print(f"  归档③ 原第 {i_phase+1:>3}–{i_verify:>3} 行  {len(part_sep):>4} 行  09-09 会话 + 09-07~13 任务")
    print(f"  保留  原第 {i_awake+1:>3}–{i_phase:>3} 行  {len(keep_long):>4} 行  顿悟 / 教学法 / 已知缺口")
    print(f"  保留  原第 {i_verify+1:>3}–{len(lines):>3} 行  {len(keep_tail):>4} 行  待验证 / 进度条 / 弱项 / 索引")

    # ── 归档文件 ──
    archive = (
        ARCHIVE_HEAD
        + "\n".join(part_head).rstrip()
        + "\n"
        + ARCHIVE_MID
        + "\n".join(part_oldstate).strip()
        + "\n"
        + ARCHIVE_TAIL
        + "\n".join(part_sep).rstrip()
        + "\n"
    )

    # ── 新看板 ──
    long_block = "\n".join(keep_long).rstrip()
    # 给「三次自我顿悟」那段换个不随日期变的标题
    long_block = long_block.replace(MARK_AWAKE, "## 🧭 长期结论（不随日期变）\n\n" + MARK_AWAKE, 1)

    board = (
        HEADER
        + NEW_STATE
        + NEW_PHASE
        + "\n---\n\n"
        + long_block
        + "\n"
        + NEW_LAST
        + "\n---\n\n"
        + "\n".join(keep_tail).lstrip("\n")
    )
    if not board.endswith("\n"):
        board += "\n"

    # ── 校验 ──
    for name, content in (("归档", archive), ("看板", board)):
        ctrl = [(i, ord(c)) for i, c in enumerate(content) if ord(c) < 32 and c not in "\n\t"]
        if ctrl:
            print(f"✗ 中止：{name}检出 {len(ctrl)} 个控制字符，未写盘。前 5 个：{ctrl[:5]}")
            return 1
    # 表格行列一致性（kanban:check 会查，这里先自检）
    for content_name, content in (("看板", board),):
        tbl = [ln for ln in content.split("\n") if ln.startswith("|")]
        widths = {}
        for ln in tbl:
            n = ln.count("|")
            widths[n] = widths.get(n, 0) + 1
        if len(widths) > 1:
            print(f"⚠️  {content_name}表格竖线数不统一：{widths}（kanban:check 可能报错，请核对）")

    print("\n结果：")
    print(f"  归档 → {ARCHIVE.relative_to(ROOT)}  {len(archive.encode('utf-8')):,} 字节")
    print(f"  看板 → {BOARD.relative_to(ROOT)}  "
          f"{len(text.encode('utf-8')):,} → {len(board.encode('utf-8')):,} 字节"
          f"（{len(lines)} → {len(board.split(chr(10)))} 行）")

    if dry:
        print("\n（--dry-run，未写盘）")
        return 0

    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVE.write_text(archive, encoding="utf-8")
    BOARD.write_text(board, encoding="utf-8")
    print("\n✅ 已写入")
    return 0


if __name__ == "__main__":
    sys.exit(main())
