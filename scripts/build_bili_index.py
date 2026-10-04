#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_bili_index.py —— 把「石头老师」全程课字幕（106 集）建成【按考点可检索】的讲法索引

用途：
  02 讲不通时，能直接查到「这个考点在石头老师的第几集、他的讲法关键词是什么」，
  而不必让学生花 30-40 分钟去看视频。

输入：data/bili-analyze/BV18CL26WEJ3/subtitle_p*.txt
输出：备考计划/石头老师讲法索引-2026-09-25.md
"""
import pathlib
import re
import collections
import json

ROOT = pathlib.Path('D:/deeepseek/zhuan-sheng-ben-notes')
SRC = ROOT / 'data/bili-analyze/BV18CL26WEJ3'
OUT = ROOT / '备考计划/石头老师讲法索引-2026-09-25.md'

# 考纲 12 章 → (关键词, 权重)
# 权重设计：章节【专属词】= 3 分；【较专】= 2 分；【通用词】= 1 分。
# 原因：后面章节的开头常会说「上节课我们讲了极限」——「极限」是通用词，
#       若不降权，会把后面各章误归到第一章（2026-09-25 实测踩过）。
CHAPTERS = [
    ('1 函数与极限', [
        ('等价无穷小', 3), ('两个重要极限', 3), ('间断点', 3), ('无穷小', 3),
        ('数列的极限', 3), ('夹逼', 3), ('函数的连续性', 3),
        ('函数的基本特性', 2), ('反函数', 2), ('复合函数', 2), ('基本初等函数', 2),
        ('连续', 2), ('极限', 1), ('函数', 1),
    ]),
    ('2 导数与微分', [
        ('高阶导数', 3), ('隐函数求导', 3), ('参数方程', 3), ('幂指函数', 3),
        ('单侧导数', 3), ('可导', 3), ('求导', 2), ('导数', 2), ('微分', 2),
    ]),
    ('3 微分中值定理与导数应用', [
        ('中值定理', 3), ('罗尔', 3), ('拉格朗日', 3), ('柯西', 3), ('洛必达', 3),
        ('泰勒', 3), ('拐点', 3), ('渐近线', 3), ('凹凸', 3),
        ('单调', 2), ('极值', 2), ('最值', 2),
    ]),
    ('4 不定积分', [
        ('不定积分', 3), ('原函数', 3), ('分部积分', 3), ('有理函数', 3), ('换元', 2),
    ]),
    ('5 定积分', [
        ('定积分', 3), ('牛顿', 3), ('莱布尼茨', 3), ('变限积分', 3), ('反常积分', 3), ('广义积分', 3),
    ]),
    ('6 定积分的应用', [
        ('旋转体', 3), ('弧长', 3), ('微元', 3), ('面积', 2), ('体积', 2),
    ]),
    ('7 微分方程', [
        ('微分方程', 3), ('可分离变量', 3), ('一阶线性', 3), ('常系数', 3), ('特解', 3), ('通解', 3),
    ]),
    ('8 向量代数与空间解析几何', [
        ('数量积', 3), ('向量积', 3), ('平面方程', 3), ('空间直线', 3), ('曲面', 3), ('向量', 2),
    ]),
    ('9 多元函数微分法', [
        ('偏导数', 3), ('全微分', 3), ('方向导数', 3), ('梯度', 3), ('多元函数', 3),
    ]),
    ('10 重积分', [
        ('二重积分', 3), ('三重积分', 3), ('极坐标', 3),
    ]),
    ('11 曲线积分与曲面积分', [
        ('曲线积分', 3), ('曲面积分', 3), ('格林公式', 3),
    ]),
    ('12 无穷级数', [
        ('收敛半径', 3), ('幂级数', 3), ('审敛', 3), ('交错级数', 3), ('P级数', 3),
        ('傅里叶', 3), ('级数', 2),
    ]),
]

# 常见「讲法金句」模式（类比/口诀类）
PATTERNS = [
    (r'(?:就|像|好比|相当于)[^。！？]{0,20}(?:一样|似的|等于)', '类比'),
    (r'(?:记住|记牢|一定要背|背下来|口诀)[^。！？]{0,26}', '口诀'),
    (r'(?:易错|雷区|坑|千万别|不能|切忌)[^。！？]{0,26}', '易错'),
    (r'(?:秒杀|大招|绝招|技巧|最快)[^。！？]{0,26}', '技巧'),
]


def load_eps():
    eps = {}
    for f in SRC.glob('subtitle_p*.txt'):
        n = int(re.search(r'p(\d+)', f.name).group(1))
        t = f.read_text(encoding='utf-8', errors='replace')
        t = re.sub(r'\s+', ' ', t).strip()
        eps[n] = t
    return dict(sorted(eps.items()))


CN_NUM = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6,
          '七': 7, '八': 8, '九': 9, '十': 10, '十一': 11, '十二': 12}


def classify(text):
    """三段式分类（2026-09-25 三轮迭代后定型）：
      ① 【第X章直判】—— 老师常在开头说「我们正式进入到第X章」，这条最可靠，直接判；
      ② 【开头 500 字加权】—— 专属词 3 分 / 较专 2 分 / 通用 1 分；
      ③ 【全文加权兜底】—— 开头无信号时才用。

    为什么不能只用全文关键词：后面各章开头会说「上节课我们讲了极限」，
    「极限」这类通用词会把它们误归到第一章（实测误判过 p021/p069/p073）。
    """
    head = text[:500]

    # ① 第X章直判
    m = re.search(r'第(十一|十二|[一二三四五六七八九十])章', head)
    if m:
        idx = CN_NUM.get(m.group(1))
        if idx and 1 <= idx <= 12:
            name = [c for c, _ in CHAPTERS][idx - 1]
            return name, 999, {'直判': name}

    # ② 开头加权
    score = collections.Counter()
    for chap, kws in CHAPTERS:
        for k, w in kws:
            score[chap] += head.count(k) * w
    # ③ 全文兜底
    if not score or max(score.values()) == 0:
        for chap, kws in CHAPTERS:
            for k, w in kws:
                score[chap] += text.count(k) * w
    if not score or max(score.values()) == 0:
        return '（未分类）', 0, {}
    top, n = score.most_common(1)[0]
    return top, n, dict(score.most_common(4))


def head_topic(text, n=34):
    """抓主题句"""
    m = re.search(r'(?:这节课|这节课咱们来|今天咱们来|咱们来|这一节|接下来|下面)(?:继续)?(?:学习|讲|看)(.{2,30})', text)
    if m:
        return m.group(1).strip('。， 好那')
    return text[:n]


def main():
    eps = load_eps()
    print(f'读入 {len(eps)} 集')

    rows = []
    for n, t in eps.items():
        chap, hits, dist = classify(t)
        rows.append({'p': n, 'chap': chap, 'hits': hits, 'topic': head_topic(t), 'len': len(t), 'dist': dist})

    by_chap = collections.defaultdict(list)
    for r in rows:
        by_chap[r['chap']].append(r)

    total = sum(r['len'] for r in rows)

    lines = []
    lines.append('# 📺 石头老师高数全程课 · 讲法索引')
    lines.append('')
    lines.append('> **用途**：02 讲不通时，**按考点直接查到「在第几集、他的讲法关键词是什么」**，不必让学生花 30–40 分钟看视频。')
    lines.append('> **来源**：`data/bili-analyze/BV18CL26WEJ3/`（B站「专升本摸着史的上岸」，UP 主自称**石头老师**，本名石志强）')
    lines.append(f'> **规模**：**{len(eps)} 集** · 总字幕 **{total:,} 字** · 平均 **{total // len(eps)} 字/集**')
    lines.append('> **生成**：`scripts/build_bili_index.py`（可重跑）')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## §0 怎么用这个索引')
    lines.append('')
    lines.append('| 场景 | 怎么用 |')
    lines.append('|:--|:--|')
    lines.append('| **我讲不通某考点** | 在下面的章节表里找该考点 → 拿到集号 → 我读那集字幕，用他的讲法重讲 |')
    lines.append('| **某节我讲不好 / 学生缺这节** | 直接看对应那集（表格里有集号） |')
    lines.append('| **想找「他的易错提醒」** | 看 §2 的「易错/口诀/类比」摘录 |')
    lines.append('')
    lines.append('> ⚠️ **定位**：视频当「讲解的第二来源」，**不替代**出题 / 判卷 / 跨日复检。')
    lines.append('> ⚠️ **分类是自动的**（按关键词命中数），**可能有误判** —— 用之前先扫一眼该集的主题句。')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## §1 按考纲章节分组（集号 → 主题）')
    lines.append('')

    order = [c for c, _ in CHAPTERS] + ['（未分类）']
    for chap in order:
        rs = by_chap.get(chap)
        if not rs:
            continue
        lines.append(f'### {chap} —— **{len(rs)} 集**')
        lines.append('')
        lines.append('| 集 | 主题（首句提取） | 字幕字数 |')
        lines.append('|:--:|:--|:--:|')
        for r in rs:
            t = r['topic'].replace('|', '/')[:46]
            lines.append(f'| **p{r["p"]:03d}** | {t} | {r["len"]:,} |')
        lines.append('')

    lines.append('---')
    lines.append('')
    lines.append('## §1.5 全部集数速查表（按集号 · **查这个比查分类可靠**）')
    lines.append('')
    lines.append('> ⚠️ **分类是自动的、准确率约八成** —— **实际查询请以本表的「主题句」为准**。')
    lines.append('')
    lines.append('| 集 | 自动分类 | 主题句（首句提取） | 字数 |')
    lines.append('|:--:|:--|:--|:--:|')
    for r in rows:
        t = r['topic'].replace('|', '/')[:44]
        c = r['chap'].replace('|', '/')
        lines.append(f'| **p{r["p"]:03d}** | {c} | {t} | {r["len"]:,} |')
    lines.append('')

    lines.append('---')
    lines.append('')
    lines.append('## §2 讲法片段摘录（易错 / 口诀 / 类比）')
    lines.append('')
    lines.append('> 从各集字幕里**正则抓取**的「讲法类句子」—— 02 讲不通时可借用的现成说法。')
    lines.append('')

    cnt = 0
    for n, t in eps.items():
        got = []
        for pat, kind in PATTERNS:
            for m in re.finditer(pat, t):
                s = m.group(0).strip()
                if 6 <= len(s) <= 60:
                    got.append((kind, s))
        # 去重 + 限流
        seen = set()
        picked = []
        for kind, s in got:
            if s in seen:
                continue
            seen.add(s)
            picked.append((kind, s))
            if len(picked) >= 3:
                break
        if picked:
            lines.append(f'**p{n:03d}**')
            for kind, s in picked:
                lines.append(f'- `{kind}` {s}')
            lines.append('')
            cnt += 1
        if cnt >= 40:
            break

    lines.append('---')
    lines.append('')
    lines.append('## 附：重跑方式')
    lines.append('')
    lines.append('```bash')
    lines.append('python scripts/build_bili_index.py')
    lines.append('```')
    lines.append('')
    lines.append('⚠️ **诚实标注**：① 主题句是**正则从字幕首段抓的**，可能抓偏；② 章节分类按**关键词命中数**，跨章内容可能归错；')
    lines.append('③ 「讲法片段」是**正则抓的候选句**，用之前 02 会先读上下文确认，**不当原话引用**。')

    OUT.write_text('\n'.join(lines), encoding='utf-8', newline='\n')
    print(f'✅ 已生成：{OUT}')
    print()
    print('=== 各章集数分布 ===')
    for chap in order:
        rs = by_chap.get(chap)
        if rs:
            print(f'  {chap:32s} {len(rs):3d} 集')
    print()
    print('=== 讲法片段覆盖集数 ===', cnt)


if __name__ == '__main__':
    main()
