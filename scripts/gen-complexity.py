# -*- coding: utf-8 -*-
"""算法复杂度增长曲线"""
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

fig, ax = plt.subplots(figsize=(3.5, 2.5))
n = np.linspace(1, 20, 200)
curves = [
    ('O(1)', np.ones_like(n), '#27AE60', '-'),
    ('O(log n)', np.log2(n), '#2F6B9E', '-'),
    ('O(n)', n, '#E67E22', '-'),
    ('O(n log n)', n*np.log2(n), '#8E44AD', '-'),
    ('O(n²)', n**2, '#C0392B', '-'),
    ('O(2ⁿ)', 2**n, '#7F8C8D', '--'),
]
for label, y, c, ls in curves:
    ax.plot(n, y, color=c, lw=1.3, ls=ls, label=label)
ax.set_xlabel('输入规模 n', fontsize=7)
ax.set_ylabel('运行时间（操作次数）', fontsize=7)
ax.set_title('常见时间复杂度增长对比', fontsize=8)
ax.set_xlim(1, 20); ax.set_ylim(0, 60)
ax.legend(fontsize=5.5, frameon=False, ncol=2)
ax.spines[['top','right']].set_visible(False)
ax.grid(alpha=0.25, lw=0.4)
fig.tight_layout()
fig.savefig(f'{OUT}/complexity-curves.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ complexity-curves.png')