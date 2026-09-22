# -*- coding: utf-8 -*-
"""第二批 P0 配图：高数 2 张核心几何图
1. 导数几何意义：切线斜率（2.1-导数的定义）
2. 定积分几何意义：曲线下面积黎曼和（3.7-定积分的概念）
输出到 docs/public/figs/，Nature 单栏风格
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

# ============ 图 1：导数几何意义——切线斜率 ============
fig, ax = plt.subplots(figsize=(3.5, 2.6))
x = np.linspace(-0.5, 2.8, 300)
f = lambda t: 0.5*(t-1.2)**3 - (t-1.2)**2 + 2.1  # 平滑曲线
y = f(x)
ax.plot(x, y, color='#2F6B9E', lw=1.8, label='y = f(x)')
# 切点
x0, y0 = 1.5, f(1.5)
# 切线斜率 = 导数
def df(t): return 1.5*(t-1.2)**2 - 2*(t-1.2)
k = df(x0)
ax.plot(x, y0 + k*(x-x0), '--', color='#C0392B', lw=1.4, label="切线 (斜率 k=f'(x0))")
# 割线（Δx 较大）
x1 = 2.2; y1 = f(x1)
k_sec = (y1-y0)/(x1-x0)
ax.plot([x0, x1], [y0, y1], '-.', color='#888', lw=1.2, label='割线 (Δy/Δx)')
ax.scatter([x0, x1], [y0, y1], s=18, color='black', zorder=3)
ax.annotate('(x0, f(x0))', xy=(x0, y0), xytext=(x0-1.1, y0+0.9), fontsize=6.5,
            arrowprops=dict(arrowstyle='->', lw=0.8, color='#444'))
ax.text(1.7, 3.4, 'k > 0 曲线上升', fontsize=6, color='#C0392B')
ax.set_xlabel('x'); ax.set_ylabel('y')
ax.legend(fontsize=5.8, loc='lower right', frameon=False)
ax.set_xlim(-0.5, 2.8); ax.set_ylim(-0.5, 4.5)
ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout()
fig.savefig(f'{OUT}/derivative-tangent.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ 图1 导数切线: derivative-tangent.png')

# ============ 图 2：定积分几何意义——黎曼和 ============
fig, ax = plt.subplots(figsize=(3.5, 2.6))
g = lambda t: 0.4*t**2 + 1.2
x = np.linspace(0, 4, 300)
ax.plot(x, g(x), color='#2F6B9E', lw=1.8, label='y = f(x)')
# 黎曼和矩形（n=8）
n = 8
a, b = 0.5, 3.5
xs = np.linspace(a, b, n+1)
for i in range(n):
    xi = xs[i]
    hi = g(xi)
    ax.add_patch(plt.Rectangle((xi, 0), xs[i+1]-xi, hi,
                 fc='#E8A0A0', ec='#C0392B', lw=0.5, alpha=0.55))
ax.fill_between(x, g(x), 0, where=(x>=a)&(x<=b), color='#2F6B9E', alpha=0.15)
ax.set_xlabel('x'); ax.set_ylabel('y')
ax.text(1.6, 3.6, '∫ f(x)dx = 曲线下面积', fontsize=6.5, color='#C0392B')
ax.text(0.6, 0.5, '切成 n 个窄条\n宽度 dx · 高度 f(x)', fontsize=6, color='#444')
ax.set_xlim(0, 4.2); ax.set_ylim(0, 5)
ax.spines[['top', 'right']].set_visible(False)
ax.legend(fontsize=6, loc='upper left', frameon=False)
fig.tight_layout()
fig.savefig(f'{OUT}/integral-riemann.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ 图2 定积分黎曼和: integral-riemann.png')
print('\n全部 2 张图生成完毕')
