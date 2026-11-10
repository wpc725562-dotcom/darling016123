# -*- coding: utf-8 -*-
"""更新 studio 知识点完成度：政治导论 / 中特体系 / 计算机查找

用法：python update-studio-20261028.py [--dry]
"""
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

TARGET = Path(r"D:/studio/data/knowledge-progress.json")
DRY = "--dry" in sys.argv

UPDATES = {
    ("政治理论", "马克思主义中国化时代化"): {
        "state": "active",
        "evidence": (
            "**导论 4 篇已讲（D021 学习日 = 10-27 13:00 → 10-28 06:00）**："
            "00-1-1 马克思主义中国化命题（毛泽东 1938 六届六中全会《论新阶段》）· 00-1-2 内涵 · "
            "00-1-3 进程 · **00-1-4 理论成果及其关系（主体通过）**——"
            "五大成果（毛邓三科习）+ 四块牌子（开篇之作／跨世纪发展／新世纪新阶段的新发展／新篇章）+ "
            "**毛三条「来是归」**（来＝马列主义在中国的运用和发展；是＝被实践证明了的、关于中国革命和建设的、"
            "正确的理论原则和经验总结；归＝中国共产党集体智慧的结晶）"
            "（选择题 6 全对 + 9 空手写默写 + 3 反向提取全对）+ 十七大 2007 把邓三科打包成体系。\n\n"
            "⚠️ 判 **active 不判 done**：剩「一脉相承 5 条／与时俱进 5 条／共同点 3 条」共 **13 点未讲**；"
            "按 R7 过关三条件，**跨日冷启动复测通过才转 done**。\n\n"
            "📌 已建 8 张 Anki 卡（tag `D021`，牌组 `专升本::政治::A级64篇默写`），"
            "并已把该牌组 `new.perDay` 从 0 调到 8（原为 0 ⇒ 卡建了也不会出现）。"
        ),
    },
    ("政治理论", "中国特色社会主义理论体系"): {
        "state": "active",
        "evidence": (
            "**10-28 首次触及（D021）**：00-1-4 讲了体系**由哪几块拼成**——五大理论成果 + 四块牌子定位；"
            "**党的十七大（2007）**正式提出「中国特色社会主义理论体系」概念，"
            "把邓小平理论、「三个代表」、科学发展观打包，标志理论与实践进一步成熟。\n\n"
            "🔴 关键易错点（当天实测踩中）：**毛泽东思想不属于本体系**——体系从邓小平开始算，毛在门外。\n\n"
            "⇒ 只到「构成与提出」这一层，**体系内部的逻辑关系（一脉相承／与时俱进，13 点）未讲**，判 active 不判 done。"
        ),
    },
    ("计算机基础与程序设计", "⑱ 查找"): {
        "state": "active",
        "evidence": (
            "**2.7 已讲 5.5/6 节（10-27 → 10-28，D021 学习日）**：\n"
            "① 基本概念与 ASL（$ASL=\\sum p_ic_i$，等概率时 $=\\frac{c_1+\\cdots+c_n}{n}$）\n"
            "② 顺序查找 $(n+1)/2$ · 分块查找 $\\frac{b+1}{2}+\\frac{s+1}{2}$（折半前提：有序 + 顺序存储）\n"
            "③ 折半查找 + **判定树**（11 元素查 27 手工三行表全对；代码坑 `low<=high`、`high=mid-1`；"
            "比较次数＝层数，树高 $=\\lceil\\log_2(n+1)\\rceil$）\n"
            "④ 二叉排序树（建树 / **中序必递增** / 删除三情况 / 有序插入退化成斜线 $ASL=(n+1)/2$）\n"
            "⑤ 哈希表（除留余数 $H(key)=key\\bmod p$、线性探测 $H_i=(H+1)\\bmod m$；"
            "9 码全对 $ASL=15/9\\approx1.67$、$\\alpha\\approx0.82$；**ASL 只与 $\\alpha$ 有关、与 $n$ 无关**）\n"
            "⑥ **平衡二叉树（partial）**：平衡因子 = 左高 − 右高、最小不平衡子树 = 从插入点往上回溯第一个、"
            "扶正＝「三个数里拎中间当根」（第 1 版讲法被退，第 2 版讲通）；**题 2 未确认**。\n\n"
            "🔴 **剩 B 树 / B+ 树未讲**（m 阶五条性质、$\\lceil m/2\\rceil$、B+ 叶子链表）⇒ **整章未关账，判 active。**\n\n"
            "📌 真题实测：2021–2024 四套原卷里查找只考折半（2022 判断 / 2023 单选 / 2024 单选），"
            "平衡二叉树与 B 树 **四年 0 命中**。"
        ),
    },
}


def main():
    data = json.loads(TARGET.read_text(encoding="utf-8"))
    changed = []

    for subj in data["subjects"]:
        for mod in subj["modules"]:
            key = (subj["subject"], mod["name"])
            if key not in UPDATES:
                continue
            new = UPDATES[key]
            old_state = mod["state"]
            mod["state"] = new["state"]
            mod["evidence"] = new["evidence"]
            changed.append((subj["subject"], mod["name"], old_state, new["state"]))

    if not changed:
        print("❌ 一个都没匹配上，检查模块名。")
        return

    data["updatedAt"] = "2026-10-28"

    print(f"{'[DRY] ' if DRY else ''}命中 {len(changed)} 个模块：")
    for s, n, o, w in changed:
        print(f"  · {s} / {n}：{o} → {w}")

    if DRY:
        print("\n[DRY] 未写盘。")
        return

    backup = TARGET.with_name(
        f"knowledge-progress.json.bak-02-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    )
    shutil.copy2(TARGET, backup)
    TARGET.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"\n✅ 已写盘。备份：{backup.name}")


if __name__ == "__main__":
    main()
