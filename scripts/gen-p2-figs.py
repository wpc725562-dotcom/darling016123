# -*- coding: utf-8 -*-
"""P2 高价值图：偏导几何意义 + 空间直角坐标系 + 级数部分和逼近"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
import numpy as np
from _figstyle import setup_style, FIGS_DIR  # noqa: E402

setup_style(journal='nature', lang='zh')
OUT = FIGS_DIR

# ============ 图 1：偏导几何意义 ============
fig = plt.figure(figsize=(3.5, 2.8))
ax = fig.add_subplot(111, projection='3d')
x = np.linspace(-1.5, 1.5, 30)
y = np.linspace(-1.5, 1.5, 30)
X, Y = np.meshgrid(x, y)
Z = 0.3*X**2 + 0.4*Y**2 + 1
ax.plot_surface(X, Y, Z, alpha=0.6, cmap='Blues', edgecolor='none')
# 切点
x0, y0, z0 = 0.5, 0.5, 0.3*0.5**2 + 0.4*0.5**2 + 1
ax.scatter([x0], [y0], [z0], color='#C0392B', s=30)
ax.text(x0, y0, z0+0.2, f'({x0},{y0},{z0:.2f})', fontsize=6, color='#C0392B')
# 偏 x 方向切线
tx = np.linspace(-0.5, 1.5, 10)
ty = np.ones_like(tx) * y0
tz = 0.3*tx**2 + 0.4*y0**2 + 1
ax.plot(tx, ty, tz, color='#E67E22', lw=1.5, label='fx 偏导方向')
ax.set_xlabel('x', fontsize=7); ax.set_ylabel('y', fontsize=7); ax.set_zlabel('z', fontsize=7)
ax.set_title('偏导数几何意义：z=f(x,y) 曲面', fontsize=7.5)
ax.legend(fontsize=5.5, frameon=False)
fig.tight_layout()
fig.savefig(f'{OUT}/partial-derivative.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ partial-derivative.png')

# ============ 图 2：空间直角坐标系 ============
fig = plt.figure(figsize=(3.5, 2.8))
ax = fig.add_subplot(111, projection='3d')
ax.set_title('空间直角坐标系', fontsize=8)
ax.quiver(0, 0, 0, 2, 0, 0, color='#C0392B', arrow_length_ratio=0.1, lw=1.5)
ax.quiver(0, 0, 0, 0, 2, 0, color='#27AE60', arrow_length_ratio=0.1, lw=1.5)
ax.quiver(0, 0, 0, 0, 0, 2, color='#2F6B9E', arrow_length_ratio=0.1, lw=1.5)
ax.text(2.1, 0, 0, 'x', fontsize=9, color='#C0392B')
ax.text(0, 2.1, 0, 'y', fontsize=9, color='#27AE60')
ax.text(0, 0, 2.1, 'z', fontsize=9, color='#2F6B9E')
# 点 P
ax.scatter([1.2], [1.0], [0.8], color='#E67E22', s=30)
ax.text(1.2, 1.0, 0.8, 'P(1.2,1.0,0.8)', fontsize=6.5, color='#E67E22')
ax.set_xlim(0, 2.2); ax.set_ylim(0, 2.2); ax.set_zlim(0, 2.2)
ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
fig.tight_layout()
fig.savefig(f'{OUT}/3d-coordinates.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ 3d-coordinates.png')

# ============ 图 3：级数部分和逼近 ============
fig, ax = plt.subplots(figsize=(3.5, 2.4))
x = np.linspace(0, 4*np.pi, 300)
# 级数：sin(x) 的傅里叶级数部分和
f = lambda t: np.sin(t) + 0.5*np.sin(3*t) + 0.3*np.sin(5*t) + 0.2*np.sin(7*t)
ax.plot(x, np.sin(x), 'k-', lw=1.2, alpha=0.3, label='sin(x) 基波')
for n, c, ls in [(1, '#C0392B', '-'), (2, '#E67E22', '--'), (3, '#27AE60', '-.'), (5, '#2F6B9E', ':')]:
    fx = np.sin(x)
    for k in range(1, n):
        fx += (1/(2*k+1)) * np.sin((2*k+1)*x)
    ax.plot(x, fx, color=c, lw=1.0, ls=ls, label=f'S{n} 部分和')
ax.set_xlim(0, 4*np.pi); ax.set_ylim(-2, 2)
ax.legend(fontsize=5.5, frameon=False, ncol=2)
ax.set_title('傅里叶级数部分和逼近（项数越多越接近方波）', fontsize=7.5)
ax.spines[['top','right']].set_visible(False)
fig.tight_layout()
fig.savefig(f'{OUT}/fourier-series.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ fourier-series.png')
print('\n全部完成')