#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""英语 8 份真题页 · 转换配置生成器

为什么不手写配置
----------------
配置里唯一的大块数据是 `answers`（46–66 条），而它本来就在源文件里
（刷题版是 `**答案**：X`，精析版是 `- **答案**：X`）。手抄一遍必然抄错，
抄完还没法复核；从源文件抽，抽错了对着源文件一眼能看出来，重跑一次就重建。

生成的两类配置
--------------
· `english2019/2020/2021/2022/2023/2024/2025.json` —— 刷题版，走
  `zhenti_promote_english.py --mode zuoti` 前置，再进转换器
· `english2020jingxi.json` —— 精析版，走 `--mode jingxi` 清 OCR 残渣，再进转换器

用法
----
    python scripts/zhenti_cfg_english.py            # 生成/覆盖
    python scripts/zhenti_cfg_english.py --check    # 只报告差异，不写
"""

import argparse
import json
import pathlib
import re
import sys

# 本脚本依赖同级模块 zhenti_log，显式把 scripts/ 加进 sys.path（理由见 zhenti_lint.py）。
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

# ★ E3（2026-09-20）：诊断走 logging（stderr），正式输出仍走 print（stdout）。
from zhenti_log import add_logging_args, get_logger, setup_from_args  # noqa: E402

LOG = get_logger(__name__)

ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG_DIR = ROOT / "scripts" / "zhenti_cfg"
ENG = "docs/posts/english"

# 2019–2021 老题型（词汇语法 / 阅读 / 完形 / 写作）
OLD_SECTIONS = {
    "Part I 词汇语法": ["1–30", "30", "30"],
    "Part II 阅读理解": ["31–50", "20", "40"],
    "Part III 完形填空": ["51–65", "15", "15"],
    "Part IV 写作": ["66", "1", "15"],
}
OLD_TITLES = {
    "Part I 词汇语法": "Part I 词汇语法（本大题共 30 小题，每小题 1 分，共 30 分）",
    "Part II 阅读理解": "Part II 阅读理解（本大题共 20 小题，每小题 2 分，共 40 分）",
    "Part III 完形填空": "Part III 完形填空（本大题共 15 小题，每小题 1 分，共 15 分）",
    "Part IV 写作": "Part IV 写作（本大题共 1 小题，共 15 分）",
}
OLD_CORE = {
    "Part I 词汇语法": "冠词、时态、非谓语、词义辨析、情景交际",
    "Part II 阅读理解": "细节理解、推理判断、主旨大意、观点态度",
    "Part III 完形填空": "语境词义、固定搭配、逻辑衔接",
    "Part IV 写作": "应用文（通知 / 邮件）",
}

# 2022 起新题型（阅读 / 七选五 / 完形 / 语法填空 / 写作）
NEW_SECTIONS = {
    "Part I 阅读理解": ["1–15", "15", "30"],
    "Part II 七选五": ["16–20", "5", "10"],
    "Part III 完形填空": ["21–35", "15", "30"],
    "Part IV 语法填空": ["36–45", "10", "15"],
    "Part V 写作": ["46", "1", "15"],
}
NEW_TITLES = {
    "Part I 阅读理解": "Part I 阅读理解（本大题共 15 小题，每小题 2 分，共 30 分）",
    "Part II 七选五": "Part II 七选五（本大题共 5 小题，每小题 2 分，共 10 分）",
    "Part III 完形填空": "Part III 完形填空（本大题共 15 小题，每小题 2 分，共 30 分）",
    "Part IV 语法填空": "Part IV 语法填空（本大题共 10 小题，每小题 1.5 分，共 15 分）",
    "Part V 写作": "Part V 写作（本大题共 1 小题，共 15 分）",
}
NEW_CORE = {
    "Part I 阅读理解": "细节理解、推理判断、主旨大意、观点态度",
    "Part II 七选五": "语篇衔接、逻辑顺序",
    "Part III 完形填空": "语境词义、固定搭配、逻辑衔接",
    "Part IV 语法填空": "词形变化、介词、连词、时态语态",
    "Part V 写作": "应用文（邮件 / 通知 / 申请信）",
}

RELATED = [
    "[英语总览](/posts/english/)",
    "[真题题型对照表](/posts/english/真题题型对照表)",
    "[教材目录基准](/posts/english/教材目录基准)",
]

# (配置名, 年份, 形态, 源文件, 额外直通章节, total_note 后缀)
ZUOTI = [
    ("english2019", "2019", "old", f"{ENG}/2019-英语-刷题版.md", [], ""),
    ("english2020", "2020", "old", f"{ENG}/2020-英语-刷题版.md",
     ["原卷作文评分说明"], ""),
    # ★ 2021 的阅读 / 完形「只有答案表、没有题」。
    #   一开始想把这两节整节设成 passthru（原样保留），但那样它们的标题就停在
    #   `## Part II 阅读理解（第31–50题）` 的老写法上，跟别的大题不一致。
    #   实际跑下来发现**不必直通**：这两节的正文只有一句 ⚠️ 引用块 + 一张答案表，
    #   既不含题号也不含 `**答案：` 行，转换器本来就不会动它们，
    #   让标题走正常的大题分支反而更整齐。
    ("english2021", "2021", "old", f"{ENG}/2021-英语-刷题版.md", [],
     "（全卷 66 题齐备；阅读与完形原卷未给逐题解析，本页这两部分只列答案）"),
    # ★ 2022–2024 的 note_tail 原先是「完形填空 21–35 原卷只留下 A 选项」——
    #   那句话**早已不成立**（2022 本就四选项齐备；2023/2024 的 B/C/D 于 2026-09-21 补齐），
    #   而 JSON 里手工维护的 `total_note` 已经改对了。两处相反 = 谁也不知道该信哪个。
    #   这里跟 JSON 对齐。（`total_note` 本身走 merge_hand 保留，此表只影响全新生成。）
    ("english2022", "2022", "new", f"{ENG}/2022-英语-刷题版.md", [], ""),
    ("english2023", "2023", "new", f"{ENG}/2023-英语-刷题版.md", [], "（全卷 46 题齐备）"),
    ("english2024", "2024", "new", f"{ENG}/2024-英语-刷题版.md", [], "（全卷 46 题齐备）"),
    ("english2025", "2025", "new", f"{ENG}/2025-英语-刷题版.md", [], "（全卷 46 题齐备）"),
]

JINGXI = f"{ENG}/2020-英语-精析版.md"

# ★ 生成器**不该覆盖**的字段：它们记的是「本轮做了什么修正 / 为什么这一格是 ✅
#   而不是 ⚠️」这类判例信息，机器无从重算，覆盖一次就永久丢失。
#   实测（2026-09-21）：读 `.orig` 后 7 份配置的 `answers` **零差异**，
#   全部差异都落在这个集合里 —— 说明「答案靠抽、散文靠写」这个分工是成立的。
HAND_KEYS = ("description", "total_note", "_note", "covered", "topics")


def resolve_source(rel):
    """配置的源：优先取该页的 `.orig-<DATE>`（**前置搬运前**的形态）。

    ★ 为什么不能直接读页面：页面是**转换后**的产物 —— 题号变成 `### 第 N 题`、
    答案行变成 `**答案：X**`（折在 `::: details` 里）、精析版的 `- **考点**：`
    已被折成标题后缀。而下面三个抽取器读的都是**转换前**的形态，
    直接读页面会**一个都抽不到**，于是生成出 `answers: {}` 的配置 ——
    重跑一次就把配置的答案速查表清空，而且全程不报错。
    """
    p = ROOT / rel
    cands = sorted(p.parent.glob(p.name + ".orig-*"))
    if not cands:
        LOG.warning("%s 没有 `.orig-*` 备份，退回读页面本身（抽取结果可能为空）", rel)
        return p
    if len(cands) > 1:
        LOG.warning("%s 有 %d 份 `.orig-*`，按字典序取最后一份：%s",
                    rel, len(cands), cands[-1].name)
    return cands[-1]


def merge_hand(name, cfg):
    """把既有配置里**手工维护**的字段（及生成器不产出的键）合并回来。

    键序按既有文件走，这样「重跑一次不动一个字节」是可验收的。
    """
    p = CFG_DIR / f"{name}.json"
    if not p.exists():
        return cfg
    old = json.loads(p.read_text(encoding="utf-8"))
    out = {}
    for k in list(old) + [k for k in cfg if k not in old]:
        if k in old and k in HAND_KEYS:
            out[k] = old[k]
        elif k in cfg:
            out[k] = cfg[k]
        elif k in old:
            out[k] = old[k]
    return out


def answers_zuoti(path):
    """从刷题版源文件抽答案：跟最近一个 `**N.` 题面配对。

    ★ 不能只按行序取第 N 个 `**答案**` —— 写作范文那个 `<details>` 块里
      压根没有答案行，一旦有缺失，后面所有题号会整体错位一格。
      按「最近见过的题号」配对，缺了就是缺了，不会连累别人。
    """
    ans, cur, qs = {}, None, []
    for ln in path.read_text(encoding="utf-8").split("\n"):
        s = ln.strip()
        m = re.match(r"^\*\*(\d{1,2})\.", s)
        if m:
            cur = int(m.group(1))
            qs.append(cur)
            continue
        m = re.match(r"^\*\*答案\*\*\s*[：:]\s*(.*)$", s)
        if m and cur:
            ans[str(cur)] = m.group(1).strip()
    return ans, qs


def answers_jingxi(path):
    """从精析版源文件抽答案：`### 第 N 题` 下面紧跟 `- **答案**：X`。"""
    ans, cur, qs = {}, None, []
    for ln in path.read_text(encoding="utf-8").split("\n"):
        s = ln.strip()
        m = re.match(r"^###\s*第\s*(\d+)\s*题", s)
        if m:
            cur = int(m.group(1))
            qs.append(cur)
            continue
        m = re.match(r"^-\s*\*\*答案\*\*\s*[：:]\s*(.*)$", s)
        if m and cur:
            ans[str(cur)] = m.group(1).strip()
    return ans, qs


def topics_jingxi(path):
    """精析版的主题名，两级来源：

    1. `- **考点**：X`（词汇语法 1–30、完形 51–65 有这一行）
    2. 阅读理解 31–50 没有 `考点` 行，但 `精析` 正文的第一个词就是题型
       （`C推理判断题。…` / `D事实细节题。…` / `A主旨大意题。…`）——
       它就是考点，抽出来即可，不必手抄。
    第 66 题是写作，两者都没有，手工补一个。
    """
    top, cur = {}, None
    for ln in path.read_text(encoding="utf-8").split("\n"):
        s = ln.strip()
        m = re.match(r"^###\s*第\s*(\d+)\s*题", s)
        if m:
            cur = m.group(1)
            continue
        m = re.match(r"^-\s*\*\*考点\*\*\s*[：:]\s*(.*)$", s)
        if m and cur:
            top[cur] = m.group(1).strip().lstrip("]")
            continue
        # 题型名前面那个「选项字母」在 OCR 里可能被粘成两个字符
        # （第 31 题写成 `IC推理判断题。` —— `1` 被识别成 `I`，跟答案 C 连在一起），
        # 所以字母位放宽到 0–3 个，别写死 `[A-D]?`。
        m = re.match(r"^-\s*\*\*精析\*\*\s*[：:]\s*[A-Za-z]{0,3}\s*([\u4e00-\u9fff]{2,8}题)", s)
        if m and cur and cur not in top:
            top[cur] = m.group(1)
    top["66"] = "应用文写作"
    return top


def build_zuoti(name, year, shape, rel, extras, note_tail):
    sections = OLD_SECTIONS if shape == "old" else NEW_SECTIONS
    titles = OLD_TITLES if shape == "old" else NEW_TITLES
    core = OLD_CORE if shape == "old" else NEW_CORE
    total = "66" if shape == "old" else "46"

    ans, qs = answers_zuoti(resolve_source(rel))
    missing = [q for q in qs if str(q) not in ans]
    for q in missing:
        ans[str(q)] = "见范文"  # 写作题在源文件里没有 `**答案**` 行

    cfg = {
        "file": rel,
        "year": year,
        "subject": "公共英语",
        "title": f"{year}年广东专插本《公共英语》真题+逐题详解",
        "description": f"广东专升本公共英语 {year} 真题，{len(qs)} 题逐题答案与解析"
                       f"（全站真题统一排版）。",
        "tags": f"[专插本, 公共英语, 真题, {year}]",
        "sections": sections,
        "core": core,
        "total": [total, "100"],
        "total_note": "满分 100 分 · 120 分钟" + note_tail,
        "section_titles": titles,
        "answer_start": ["^\\*\\*答案[：:]"],
        "fold_tail": True,
        "toc_chunk": 10,
        "answers": {k: ans[k] for k in sorted(ans, key=int)},
        "related": RELATED,
    }
    if extras:
        cfg["passthru_sections"] = extras
    if missing:
        cfg["_note"] = ("写作题（" + "/".join(str(q) for q in missing)
                        + "）在源文件里是参考范文，没有 `**答案**` 行；"
                          "`**答案：参考范文**` 由 zhenti_promote_english.py 补。")
    return name, cfg, len(qs), missing


def build_jingxi():
    rel = JINGXI
    ans, qs = answers_jingxi(resolve_source(rel))
    missing = [q for q in qs if str(q) not in ans]
    for q in missing:
        ans[str(q)] = "见范文"
    cfg = {
        "file": rel,
        "year": "2020",
        "subject": "公共英语",
        "title": "2020年广东专插本《公共英语》真题精析版",
        "description": "广东专升本公共英语 2020 真题精析：66 题逐题给出答案、翻译、考点与精析"
                       "（全站真题统一排版）。",
        "tags": "[专插本, 公共英语, 真题, 精析, 2020]",
        "sections": OLD_SECTIONS,
        "core": OLD_CORE,
        "total": ["66", "100"],
        "total_note": "满分 100 分 · 120 分钟 · 本页为精析版，逐题含翻译与考点",
        "section_titles": OLD_TITLES,
        # 精析版的答案是**无序列表**（`- **答案**：D`），不是引用块。
        "answer_start": ["^-\\s*\\*\\*答案\\*\\*[：:]"],
        "fold_tail": True,
        # 折进去之前先脱掉列表符号：模板用 `**答案：D**`，不是 `- **答案**：D`
        "fold_line_subs": [
            ["^-\\s+\\*\\*(答案|翻译|考点|精析|写作思路|参考范文|题目要求)\\*\\*\\s*[：:]",
             "**\\1**："],
        ],
        "toc_chunk": 10,
        "topics": topics_jingxi(resolve_source(rel)),
        "answers": ans,
        "related": RELATED,
    }
    if missing:
        cfg["_note"] = ("第 " + "/".join(str(q) for q in missing)
                        + " 题是写作题，源文件只有范文、没有 `- **答案**` 行，"
                          "所以页面上不会出现折叠块 —— 范文本身就在题面下方。")
    return "english2020jingxi", cfg, len(qs), missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只报告差异，不写文件")
    add_logging_args(ap)
    args = ap.parse_args()
    setup_from_args(args)
    LOG.debug("check=%s · CFG_DIR=%s", args.check, CFG_DIR)

    made = []
    for spec in ZUOTI:
        made.append(build_zuoti(*spec))

    made.append(build_jingxi())
    LOG.debug("生成 %d 份配置（刷题版 %d + 精析版 1）", len(made), len(ZUOTI))

    rc = 0
    for name, cfg, nq, missing in made:
        p = CFG_DIR / f"{name}.json"
        old = p.read_text(encoding="utf-8") if p.exists() else ""
        # ★ 空答案守卫：抽到 0 条、而既有配置里明明有答案 ⇒ 一定是「源形态变了」，
        #   不能把 7 份配置的答案表一起清空。宁可失败。
        if not cfg["answers"]:
            LOG.error("配置 %s：抽到 0 条答案，拒绝写入（源形态可能变了）。"
                      "既有配置里有 %d 条。", name, len(
                          json.loads(old).get("answers", {}) if old else {}))
            print(f"  {name:18s} ✗ 抽到 0 条答案，拒绝写入")
            rc = 1
            continue
        cfg = merge_hand(name, cfg)
        new = json.dumps(cfg, ensure_ascii=False, indent=2) + "\n"
        flag = "不变" if old == new else ("新建" if not old else "更新")
        # ★ 日志放在 --check 的 continue **之前** —— 否则 check 模式下一条都不出，
        #   而 check 恰恰是最需要看明细的场景。
        #   「缺答案」用 debug 不用 warning：精析版按设计就没有答案表，
        #   当 warning 报会在每次运行里刷一屏，最后必然被无视。
        LOG.info("配置 %s：%s · 题 %d · 答案 %d", name, flag, nq, len(cfg["answers"]))
        if missing:
            LOG.debug("配置 %s：缺答案 %s", name, missing)
        if args.check:
            print(f"  {name:18s} {flag}  题 {nq}  答案 {len(cfg['answers'])}"
                  + (f"  缺答案 {missing}" if missing else ""))
            continue
        if old != new:
            p.write_text(new, encoding="utf-8", newline="\n")
        print(f"  {name:18s} {flag}  题 {nq}  答案 {len(cfg['answers'])}"
              + (f"  缺答案 {missing}" if missing else ""))
    return rc


if __name__ == "__main__":
    sys.exit(main())
