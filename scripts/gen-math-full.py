# -*- coding: utf-8 -*-
"""高数补全批：10 张重点函数图
1. 两个重要极限（sinx/x 与 (1+1/x)^x）
2. 导数几何应用：切线 + 单调性
3. 曲率：弯曲程度与曲率圆
4. 多元极值：极小/极大/鞍点三维示意
5. 二重积分：积分区域（X 型）
6. 三重积分：积分区域
7. 正项级数：收敛 vs 发散部分和
8. 幂级数：收敛半径内逼近
9. 方向导数与梯度：等高线 + 梯度场
10. 微分方程：斜率场
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

# ============ 1. 两个重要极限 ============
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.4))
# sinx/x
ax = axes[0]
x = np.linspace(-6, 6, 400)
y = np.sin(x)/x
ax.plot(x, y, color='#2F6B9E', lw=1.5)
ax.axhline(1, color='#C0392B', ls='--', lw=0.8)
ax.text(2.2, 1.05, 'y=1（极限值）', fontsize=6.5, color='#C0392B')
ax.set_title(r'$\lim_{x\to0} \frac{\sin x}{x}=1$', fontsize=8)
ax.set_xlim(-6, 6); ax.set_ylim(-0.5, 1.4)
ax.spines[['top','right']].set_visible(False)
ax.grid(alpha=0.25, lw=0.4)
# (1+1/x)^x
ax = axes[1]
x = np.linspace(1, 20, 300)
y = (1+1/x)**x
ax.plot(x, y, color='#2F6B9E', lw=1.5)
ax.axhline(np.e, color='#C0392B', ls='--', lw=0.8)
ax.text(6.5, np.e+0.06, r'y=e≈2.718', fontsize=6.5, color='#C0392B')
ax.set_title(r'$\lim_{x\to\infty}(1+\frac{1}{x})^x=e$', fontsize=8)
ax.set_xlim(1, 20); ax.set_ylim(1.5, 3.0)
ax.spines[['top','right']].set_visible(False)
ax.grid(alpha=0.25, lw=0.4)
fig.tight_layout()
fig.savefig(f'{OUT}/important-limits.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ important-limits.png')

# ============ 2. 导数几何应用：切线+单调性 ============
fig, ax = plt.subplots(figsize=(3.5, 2.4))
x = np.linspace(-2.4, 2.4, 400)
y = x**3 - 3*x
ax.plot(x, y, color='#2F6B9E', lw=1.5, label='y=x³-3x')
# 切线在 x=1.5
xt = 1.5; slope = 3*xt**2 - 3
ax.plot([xt-1.2, xt+1.2], [xt**3-3*xt - slope*1.2, xt**3-3*xt + slope*1.2], '--', color='#C0392B', lw=1.0)
ax.scatter([xt], [xt**3-3*xt], color='#C0392B', s=25, zorder=5)
# 极值点
for xe, label in [(-1, '极大'), (1, '极小')]:
    ax.scatter([xe], [xe**3-3*xe], color='#E67E22', s=25, zorder=5)
    ax.annotate(label, (xe, xe**3-3*xe), textcoords='offset points', xytext=(10, 8), fontsize=6.5, color='#E67E22')
ax.axhline(0, color='#888', lw=0.5); ax.axvline(0, color='#888', lw=0.5)
ax.text(-2.2, 3.2, "f'>0 增", fontsize=6.5, color='#27AE60')
ax.text(-0.6, -2.2, "f'<0 减", fontsize=6.5, color='#C0392B')
ax.text(1.5, 3.0, "f'>0 增", fontsize=6.5, color='#27AE60')
ax.set_title('导数符号与单调性/极值', fontsize=8)
ax.legend(fontsize=6, frameon=False)
ax.set_xlim(-2.5, 2.5); ax.set_ylim(-3.5, 3.5)
ax.spines[['top','right']].set_visible(False)
fig.tight_layout()
fig.savefig(f'{OUT}/tangent-monotonic.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ tangent-monotonic.png')

# ============ 3. 曲率 ============
fig, ax = plt.subplots(figsize=(3.5, 2.4))
x = np.linspace(-2, 2, 300)
y = x**2
ax.plot(x, y, color='#2F6B9E', lw=1.5, label='y=x²')
# 顶点处曲率圆：r=1/2
th = np.linspace(0, 2*np.pi, 100)
r = 0.5
ax.plot(r*np.cos(th), r*np.sin(th) + r, '--', color='#C0392B', lw=1.0, label='曲率圆 r=0.5')
ax.scatter([0], [0], color='#E67E22', s=25, zorder=5)
ax.text(0.05, -0.25, '顶点最弯', fontsize=6.5, color='#E67E22')
ax.text(1.4, 0.6, '越远越直', fontsize=6.5, color='#888')
ax.set_title('曲率：顶点最弯，远离顶点越平', fontsize=7.5)
ax.legend(fontsize=6, frameon=False, loc='lower right')
ax.set_xlim(-2, 2); ax.set_ylim(-0.3, 2.4)
ax.spines[['top','right']].set_visible(False)
ax.set_aspect('equal')
fig.tight_layout()
fig.savefig(f'{OUT}/curvature.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ curvature.png')

# ============ 4. 多元极值：鞍点 ============
fig = plt.figure(figsize=(3.5, 2.6))
ax = fig.add_subplot(111, projection='3d')
x = np.linspace(-1.5, 1.5, 40); y = np.linspace(-1.5, 1.5, 40)
X, Y = np.meshgrid(x, y)
# 鞍点 z = x² - y²
Z = X**2 - Y**2
ax.plot_surface(X, Y, Z, alpha=0.7, cmap='RdBu_r', edgecolor='none')
ax.scatter([0], [0], [0], color='#C0392B', s=40)
ax.text(0, 0, 0.2, '鞍点 (0,0)', fontsize=6.5, color='#C0392B')
ax.set_title('鞍点：x 方向极小、y 方向极大（AC-B²<0）', fontsize=6.5)
ax.set_xlabel('x', fontsize=6); ax.set_ylabel('y', fontsize=6); ax.set_zlabel('z', fontsize=6)
fig.tight_layout()
fig.savefig(f'{OUT}/saddle-point.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ saddle-point.png')

# ============ 5. 二重积分区域（X 型） ============
fig, ax = plt.subplots(figsize=(3.5, 2.4))
x = np.linspace(0, 2, 200)
y1 = x**2
y2 = 2*x
ax.fill_between(x, y1, y2, alpha=0.3, color='#2F6B9E')
ax.plot(x, y1, color='#2F6B9E', lw=1.2, label='y=x²')
ax.plot(x, y2, color='#C0392B', lw=1.2, label='y=2x')
ax.text(1.1, 2.6, 'D: 0≤x≤2\nx²≤y≤2x', fontsize=7, ha='center', color='#2F6B9E')
# 竖直条示意
ax.plot([1.5, 1.5], [1.5**2, 3], color='#E67E22', lw=1.5)
ax.text(1.55, 2.3, '先积 y', fontsize=6.5, color='#E67E22')
ax.set_title('二重积分 X 型区域（画图定限）', fontsize=7.5)
ax.legend(fontsize=6, frameon=False, loc='upper left')
ax.set_xlim(-0.1, 2.3); ax.set_ylim(-0.2, 4.3)
ax.spines[['top','right']].set_visible(False)
ax.grid(alpha=0.25, lw=0.4)
fig.tight_layout()
fig.savefig(f'{OUT}/double-integral-region.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ double-integral-region.png')

# ============ 6. 三重积分区域 ============
fig = plt.figure(figsize=(3.5, 2.6))
ax = fig.add_subplot(111, projection='3d')
# 圆柱区域示意：z=0 到 z=2, x²+y²≤1
th = np.linspace(0, 2*np.pi, 40)
r = np.linspace(0, 1, 20)
TH, R = np.meshgrid(th, r)
X = R*np.cos(TH); Y = R*np.sin(TH)
Z0 = np.zeros_like(X); Z2 = np.full_like(X, 2)
ax.plot_surface(X, Y, Z0, alpha=0.3, color='#2F6B9E')
ax.plot_surface(X, Y, Z2, alpha=0.3, color='#C0392B')
# 侧面
t = np.linspace(0, 2*np.pi, 60)
for z in np.linspace(0, 2, 5):
    ax.plot(np.cos(t), np.sin(t), z, color='#E67E22', lw=0.5, alpha=0.5)
ax.set_title('三重积分区域：圆柱 x²+y²≤1, 0≤z≤2', fontsize=6.5)
ax.set_xlabel('x', fontsize=6); ax.set_ylabel('y', fontsize=6); ax.set_zlabel('z', fontsize=6)
fig.tight_layout()
fig.savefig(f'{OUT}/triple-integral-region.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ triple-integral-region.png')

# ============ 7. 正项级数收敛 vs 发散 ============
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.4))
# 收敛：调和级数变体 1/n²
n = np.arange(1, 60)
sn = np.cumsum(1/n**2)
ax = axes[0]
ax.plot(n, sn, color='#2F6B9E', lw=1.5)
ax.axhline(np.pi**2/6, color='#C0392B', ls='--', lw=0.8)
ax.text(30, np.pi**2/6+0.08, 'π²/6≈1.64', fontsize=6.5, color='#C0392B')
ax.set_title('Σ1/n² 收敛（部分和有上界）', fontsize=7.5)
ax.set_xlim(0, 60); ax.set_ylim(0, 1.9)
ax.spines[['top','right']].set_visible(False)
# 发散：调和级数 1/n
n = np.arange(1, 60)
sn = np.cumsum(1/n)
ax = axes[1]
ax.plot(n, sn, color='#C0392B', lw=1.5)
ax.set_title('Σ1/n 发散（部分和一直增长）', fontsize=7.5)
ax.set_xlim(0, 60); ax.set_ylim(0, 5)
ax.spines[['top','right']].set_visible(False)
fig.tight_layout()
fig.savefig(f'{OUT}/series-convergence.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ series-convergence.png')

# ============ 8. 幂级数收敛半径 ============
fig, ax = plt.subplots(figsize=(3.5, 2.4))
x = np.linspace(-1.2, 1.2, 400)
# 几何级数部分和逼近 1/(1-x)
f = 1/(1-x)
ax.plot(x, f, 'k--', lw=1.0, alpha=0.5, label='1/(1-x)')
for N, c in [(2, '#C0392B'), (4, '#E67E22'), (8, '#27AE60'), (16, '#2F6B9E')]:
    sn = np.zeros_like(x)
    for k in range(N):
        sn += x**k
    ax.plot(x, sn, color=c, lw=1.0, label=f'S{N}')
ax.axvline(1, color='#888', ls=':', lw=0.8)
ax.text(1.02, 2, 'x=1 收敛半径边界', fontsize=6, color='#888')
ax.set_title('幂级数 Σxⁿ 收敛半径 R=1（部分和逼近）', fontsize=7)
ax.legend(fontsize=5, frameon=False, ncol=2)
ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1, 6)
ax.spines[['top','right']].set_visible(False)
ax.grid(alpha=0.2, lw=0.4)
fig.tight_layout()
fig.savefig(f'{OUT}/power-series-radius.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ power-series-radius.png')

# ============ 9. 方向导数与梯度 ============
fig, ax = plt.subplots(figsize=(3.5, 2.6))
x = np.linspace(-2, 2, 30); y = np.linspace(-2, 2, 30)
X, Y = np.meshgrid(x, y)
Z = X**2 + Y**2
cs = ax.contour(X, Y, Z, levels=8, colors='#2F6B9E', alpha=0.7, linewidths=0.8)
ax.clabel(cs, fontsize=5)
# 梯度场 = (2x, 2y)
gx, gy = 2*X, 2*Y
ax.quiver(X[::3,::3], Y[::3,::3], gx[::3,::3], gy[::3,::3], color='#C0392B', scale=30, width=0.004)
ax.text(0.05, 2.1, '梯度方向=等高线法向=最速上升', fontsize=6, color='#C0392B')
ax.set_title('梯度场：垂直等高线指向上升方向', fontsize=7.5)
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.2, 2.2)
ax.set_aspect('equal')
ax.spines[['top','right']].set_visible(False)
fig.tight_layout()
fig.savefig(f'{OUT}/gradient-field.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ gradient-field.png')

# ============ 10. 微分方程斜率场 ============
fig, ax = plt.subplots(figsize=(3.5, 2.4))
# y' = x（解 y = x²/2 + C）
x = np.linspace(-2, 2, 17); y = np.linspace(-1, 3, 17)
X, Y = np.meshgrid(x, y)
U = np.ones_like(X)
V = X  # y'=x
ax.quiver(X, Y, U, V, color='#2F6B9E', alpha=0.6, scale=20, width=0.004)
# 解曲线
for C in [-0.5, 0, 0.8]:
    xs = np.linspace(-2, 2, 100)
    ax.plot(xs, xs**2/2 + C, color='#C0392B', lw=1.2)
ax.set_title("斜率场 y'=x 与解曲线 y=x²/2+C", fontsize=7.5)
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-1.2, 3.2)
ax.set_aspect('equal')
ax.spines[['top','right']].set_visible(False)
fig.tight_layout()
fig.savefig(f'{OUT}/slope-field.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ slope-field.png')
print('\n高数补全 10 张完成')