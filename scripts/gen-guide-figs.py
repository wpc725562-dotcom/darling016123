# -*- coding: utf-8 -*-
"""指南板块 2 张数据图：
1. 2026 省控线对比（三科总分 vs 专业综合课，按类别）
2. 公办计算机投档线趋势（韩山师范/嘉应学院等）
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from _figstyle import setup_style, FIGS_DIR  # noqa: E402

setup_style(journal='nature', lang='zh')
OUT = FIGS_DIR

# ============ 图 1：2026 省控线对比 ============
cats = ['大学语文', '经济学', '民法', '教育理论', '高等数学', '生态学', '生理学', '管理学', '艺术概论']
total = [130, 110, 145, 125, 105, 120, 135, 110, 110]
comp = [100, 65, 115, 100, 60, 90, 100, 70, 95]

fig, ax = plt.subplots(figsize=(3.5, 2.6))
x = np.arange(len(cats))
w = 0.35
b1 = ax.bar(x - w/2, total, w, label='三科总分线', color='#2F6B9E')
b2 = ax.bar(x + w/2, comp, w, label='专业综合课线', color='#C0392B')
# 高数高亮
ax.get_xticklabels()
for i, c in enumerate(cats):
    if c == '高等数学':
        b1[i].set_color('#27AE60')
        b2[i].set_color('#E67E22')
ax.set_xticks(x)
ax.set_xticklabels(cats, rotation=40, ha='right', fontsize=5.5)
ax.set_ylabel('分数', fontsize=7)
ax.set_ylim(0, 165)
ax.legend(fontsize=5.5, frameon=False)
ax.set_title('2026 广东专升本省控线（9 类）', fontsize=8)
ax.spines[['top','right']].set_visible(False)
ax.grid(axis='y', alpha=0.25, lw=0.5)
fig.tight_layout()
fig.savefig(f'{OUT}/score-line-2026.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ score-line-2026.png')

# ============ 图 2：公办计算机投档线趋势 ============
# 2024 vs 2025 投档线（来源：计算机专业-报考指南.md 与 投档与招生数据.md）
schools = ['深技大\n物联网', '广师大\n计科', '嘉应\n计科', '韩师\n计科', '韩师\n软工', '韩师\n大数据', '韩师\n物联网']
line2024 = [437, 428, None, None, None, None, None]  # 2024 数据
line2025 = [None, None, 423, 420, 416, 411, 409]     # 2025 数据

fig, ax = plt.subplots(figsize=(3.5, 2.4))
x = np.arange(len(schools))
# 2024 已知点
x24 = [i for i, v in enumerate(line2024) if v is not None]
y24 = [v for v in line2024 if v is not None]
ax.bar(x24, y24, 0.35, color='#2F6B9E', alpha=0.7, label='2024 投档线')
for xi, yi in zip(x24, y24):
    ax.text(xi, yi+3, str(yi), ha='center', fontsize=6.5, color='#2F6B9E')
# 2025 已知点
x25 = [i for i, v in enumerate(line2025) if v is not None]
y25 = [v for v in line2025 if v is not None]
ax.bar([i+0.35 for i in x25], y25, 0.35, color='#C0392B', alpha=0.7, label='2025 投档线')
for xi, yi in zip(x25, y25):
    ax.text(xi+0.35, yi+3, str(yi), ha='center', fontsize=6.5, color='#C0392B')
ax.axhline(420, color='#888', ls='--', lw=0.8)
ax.text(6.4, 421, '420 分线', fontsize=6, color='#666', ha='right')
ax.set_xticks(x + 0.17)
ax.set_xticklabels(schools, fontsize=5.5)
ax.set_ylabel('投档分', fontsize=7)
ax.set_ylim(380, 460)
ax.legend(fontsize=5.5, frameon=False)
ax.set_title('公办计算机专业投档线（2024 vs 2025）', fontsize=8)
ax.spines[['top','right']].set_visible(False)
ax.grid(axis='y', alpha=0.25, lw=0.5)
fig.tight_layout()
fig.savefig(f'{OUT}/computer-score-trend.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ computer-score-trend.png')
print('\n全部完成')
