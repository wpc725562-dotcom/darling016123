#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""scripts/zhenti_bootstrap_cfg.py —— 从真题页里抽答案，生成转换配置的骨架。

为什么要有它：zhenti_convert.py 的配置里 topics / core / section_titles 必须人判断，
但 answers 是纯抽取劳动 —— 30+ 份卷子 × 20 题手工抄一遍既慢又容易抄错。
本脚本只做这一件事：把每题的答案抓出来，打印成可以直接粘进 JSON 的片段。

支持四种答案形态（都是实测出来的）：
  A. `> **答案与解析**` / `> **B**。…`            （2019/2020 选择题）
  B. `> **答案**` 换行 `> $\\dfrac{1}{3}x$`        （2019/2020 填空题）
  C. `11. 题面 → **$1/2$**` 行内答案              （2019/2020 计算题）
  D. `> **答案：C**` 与 `> **答案：** $12x^2$`     （2021–2024，冒号可在加粗内或外）
  E. 抓不到的（综合题裸文本）留空，人工补

用法：python scripts/zhenti_bootstrap_cfg.py docs/posts/math/2020.md
"""

import json
import pathlib
import re
import sys

# 本脚本依赖同级模块 zhenti_log，显式把 scripts/ 加进 sys.path（理由见 zhenti_lint.py）。
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

# ★ E3（2026-09-20）：诊断走 logging（stderr）。
#   本脚本的 stdout 是「可以直接粘进 JSON 的片段」，属于**数据**，
#   诊断绝不能混进去 —— 所以这里只加 logger，不动任何 print。
from zhenti_log import get_logger  # noqa: E402

LOG = get_logger(__name__)

HEAD_QNO_RE = re.compile(r"^###\s*(?:第\s*)?(\d{1,2})\b(.*)$")
BARE_QNO_RE = re.compile(r"^(\d{1,2})\.\s+(\S.*)$")
ANS_INLINE_RE = re.compile(r"\s*→\s*(.+)$")
# `> **答案：C**` / `> **答案：** $12x^2$` / `> **参考答案：** …` / `**答案：C** · 考点 …`
# 三种都要接住：第三种是计算机 2021/2022 的裸行写法（没有 `>`）
ANS_LABEL_RE = re.compile(r"^>?\s*\*\*(?:参考)?答案\s*[：:]\s*(.*?)\*\*\s*(.*)$")
ANS_HEAD_RE = re.compile(r"^>?\s*\*\*(?:参考)?答案(与解析)?\*\*\s*$")
# 第四种：计算机 2023 的 `回忆答案：**C. \`&a\`** · 考点 [link]`
ANS_BARE_RE = re.compile(r"^(?:回忆)?答案\s*[：:]\s*\*\*(.+?)\*\*")
# 大题标题，用来算本节题号偏移（计算机卷每节从 1 重编号）
SECTION_RE = re.compile(r"^##\s*([一二三四五六七八九十]+)、\s*(.+?)\s*$")


def clean(s):
    s = s.strip()
    s = re.sub(r"^>\s?", "", s).strip()
    s = s.strip("*").strip()
    s = re.sub(r"[。．]$", "", s)
    return s


def extract(text, qno_base=None):
    qno_base = qno_base or {}
    lines = text.split("\n")
    cur = None
    cur_base = 0
    last_q = 0
    res = {}
    i = 0
    n = len(lines)
    while i < n:
        s = lines[i].strip()
        # ★ 一旦进入复核记录 / 考点分布 / 备考建议区就停 —— 那里的有序列表
        #   （`6. 求导去积分号 → 解微分方程`）会被 BARE_QNO_RE 当成第 6 题，
        #   把真答案覆盖掉（2024 实测踩过）。
        if re.match(r"^##\s*(考点分布|复核记录|回炉|备考建议)", s):
            break
        ms = SECTION_RE.match(s)
        if ms:
            cur_base = int(qno_base.get(ms.group(2).split("（")[0], 0))
        q = None
        m = HEAD_QNO_RE.match(s)
        if m:
            q = int(m.group(1)) + cur_base
            rest = m.group(2)
        else:
            m2 = BARE_QNO_RE.match(s)
            if m2:
                q, rest = int(m2.group(1)) + cur_base, m2.group(2)
        if q is not None:
            # ★ 单调性保护：解析里常有 `1. …` `2. …` 这样的有序列表
            #   （2024 第 13 题的折半查找步骤、2025 第 1 题的复杂度对照），
            #   不设防的话它们会被当成「第 1 题」，把真答案覆盖掉。
            #   题号在卷面上是递增的，所以「不比上一题大」的一律不认。
            if q <= last_q:
                i += 1
                continue
            last_q = q
            cur = q
            res.setdefault(q, "")
            mi = ANS_INLINE_RE.search(rest)
            if mi:
                res[q] = clean(mi.group(1))
            i += 1
            continue
        if cur is not None:
            mb2 = ANS_BARE_RE.match(s)
            if mb2:
                val = clean(mb2.group(1))
                # `C. `&a`` 这种只留选项字母；判断题的「对/错」直接留
                mo = re.match(r"^([A-D])\b", val)
                res[cur] = mo.group(1) if mo else val
                i += 1
                continue
            ml = ANS_LABEL_RE.match(s)
            if ml:
                val = ml.group(1).strip() or ml.group(2).strip()
                res[cur] = clean(val)
                i += 1
                continue
            if ANS_HEAD_RE.match(s):
                # 形态 A：下一行的 `> **B**。…` 里取加粗内容；形态 B：下一行就是答案
                j = i + 1
                if j < n:
                    nx = lines[j].strip()
                    mb = re.match(r"^>\s*\*\*(.+?)\*\*", nx)
                    if mb:
                        res[cur] = clean(mb.group(1))
                    elif nx.startswith(">"):
                        res[cur] = clean(nx)
                i += 1
                continue
        i += 1
    return res


def main():
    if len(sys.argv) < 2:
        LOG.error("没给页面路径；用法：zhenti_bootstrap_cfg.py <页面.md> [配置.json]")
        print(__doc__)
        return 1
    p = pathlib.Path(sys.argv[1])
    qno_base = {}
    if len(sys.argv) > 2:
        qno_base = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")).get("section_qno_base", {})
    LOG.debug("抽取答案：%s（section_qno_base 覆盖 %d 段）", p, len(qno_base))
    ans = extract(p.read_text(encoding="utf-8"), qno_base)
    # ★ 「抽不到答案」是这个脚本最常见的失败形态（答案形态不在支持列表里），
    #   而它的 stdout 是纯数据、看不出异常。所以这里把计数报到日志里。
    LOG.info("%s 抽到 %d 题答案", p.name, len(ans))
    if not ans:
        LOG.warning("%s 一题都没抽到 —— 检查答案形态是否在上面列的 A–E 里", p.name)
    print(f"# {p}  共 {len(ans)} 题")
    for k in sorted(ans, key=lambda x: int(x)):
        print(f'    "{k}": "{ans[k].replace(chr(92), chr(92) * 2)}",')
    return 0


if __name__ == "__main__":
    sys.exit(main())
