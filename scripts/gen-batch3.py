# -*- coding: utf-8 -*-
"""第三波：高数剩余 P0 8 张 + 计算机剩余 P0 5 张 = 13 张图"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
import numpy as np
from _figstyle import setup_style, FIGS_DIR  # noqa: E402

setup_style(journal='nature', lang='zh')
OUT = FIGS_DIR

# ============ 高数 1：函数图像（基本初等函数）============
fig, ax = plt.subplots(figsize=(3.5, 2.4))
x = np.linspace(-3, 3, 300)
funcs = [
    (lambda t: t**2, 'y=x²', '#2F6B9E'),
    (lambda t: t**3, 'y=x³', '#C0392B'),
    (lambda t: np.sin(t), 'y=sin x', '#27AE60'),
    (lambda t: np.exp(t), 'y=eˣ', '#E67E22'),
]
for f, label, c in funcs:
    ax.plot(x, f(x), label=label, color=c, lw=1.5)
ax.axhline(0, color='#888', lw=0.5); ax.axvline(0, color='#888', lw=0.5)
ax.set_xlim(-3, 3); ax.set_ylim(-3, 5)
ax.legend(fontsize=6, frameon=False)
ax.set_title('基本初等函数图像', fontsize=8)
ax.spines[['top','right']].set_visible(False)
fig.tight_layout(); fig.savefig(f'{OUT}/basic-functions.png', dpi=300, bbox_inches='tight'); plt.close(fig)
print('✅ basic-functions.png')

# ============ 高数 2：极限趋近示意 ============
fig, ax = plt.subplots(figsize=(3.5, 2.4))
x = np.linspace(-2, 3, 500)
f = lambda t: 0.5*(t-0.5)**2 + 1.2
ax.plot(x, f(x), color='#2F6B9E', lw=1.5, label='y=f(x)')
x0 = 1.5
delta = 0.8
ax.axvline(x0, color='#C0392B', lw=0.8, ls='--', alpha=0.6)
ax.axhline(f(x0), color='#C0392B', lw=0.8, ls='--', alpha=0.6)
ax.scatter([x0], [f(x0)], s=30, color='#C0392B', zorder=3)
# δ-ε 区间
ax.fill_between(x, 0, f(x), where=(x>x0-delta)&(x<x0+delta), color='#C0392B', alpha=0.12)
ax.text(x0, f(x0)+0.4, '(x₀, f(x₀))', fontsize=6.5, ha='center', color='#C0392B')
ax.annotate('', xy=(x0-0.8, f(x0)-0.15), xytext=(x0+0.8, f(x0)-0.15),
            arrowprops=dict(arrowstyle='<->', lw=1, color='#C0392B'))
ax.text(x0, f(x0)-0.6, 'δ', ha='center', fontsize=7, color='#C0392B')
ax.text(0.5, 3.5, 'x→x₀ 时 f(x)→f(x₀)', fontsize=7, color='#444')
ax.set_xlim(-2, 3); ax.set_ylim(0, 4.5); ax.legend(fontsize=6, frameon=False)
ax.spines[['top','right']].set_visible(False)
fig.tight_layout(); fig.savefig(f'{OUT}/limit-approach.png', dpi=300, bbox_inches='tight'); plt.close(fig)
print('✅ limit-approach.png')

# ============ 高数 3：极值凹凸性 ============
fig, ax = plt.subplots(figsize=(3.5, 2.4))
x = np.linspace(-2.5, 2.5, 300)
f = lambda t: 0.3*t**3 - 0.5*t**2 - 0.8*t + 1.5
y = f(x)
ax.plot(x, y, color='#2F6B9E', lw=1.8)
# 极大值点
x_max, y_max = -0.65, f(-0.65)
ax.scatter([x_max], [y_max], s=40, color='#C0392B', zorder=3)
ax.annotate('极大值', xy=(x_max, y_max), xytext=(x_max-1.2, y_max+0.8), fontsize=7,
            arrowprops=dict(arrowstyle='->', lw=0.8, color='#C0392B'))
# 极小值点
x_min, y_min = 1.32, f(1.32)
ax.scatter([x_min], [y_min], s=40, color='#C0392B', zorder=3)
ax.annotate('极小值', xy=(x_min, y_min), xytext=(x_min+0.5, y_min+0.8), fontsize=7,
            arrowprops=dict(arrowstyle='->', lw=0.8, color='#C0392B'))
# 拐点
x_inf = 0.33
ax.axvline(x_inf, color='#E67E22', lw=0.8, ls='--', alpha=0.6)
ax.text(x_inf+0.05, 1.2, '拐点\n(凹凸变化)', fontsize=6.5, color='#E67E22')
ax.axhline(0, color='#888', lw=0.5)
ax.set_title('函数的极值与凹凸性', fontsize=8)
ax.set_xlim(-2.5, 2.5); ax.set_ylim(-1, 3.5)
ax.spines[['top','right']].set_visible(False)
fig.tight_layout(); fig.savefig(f'{OUT}/extremum-concavity.png', dpi=300, bbox_inches='tight'); plt.close(fig)
print('✅ extremum-concavity.png')

# ============ 高数 4：中值定理几何 ============
fig, ax = plt.subplots(figsize=(3.5, 2.4))
x = np.linspace(0, 4, 300)
f = lambda t: 0.3*(t-2)**3 + 0.5*t + 1
y = f(x)
ax.plot(x, y, color='#2F6B9E', lw=1.8, label='y=f(x)')
# 端点连线（割线）
a, b = 0.5, 3.5
ax.plot([a, b], [f(a), f(b)], '--', color='#C0392B', lw=1.2, label='端点的连线')
# 中点切线平行于割线
c = 2.0
df = lambda t: 0.9*(t-2)**2 + 0.5
k = df(c)
ax.plot(x, f(c) + k*(x-c), '-.', color='#27AE60', lw=1.2, label='平行切线')
ax.scatter([c], [f(c)], s=30, color='#27AE60', zorder=3)
ax.annotate('∃ξ∈(a,b)\nf\'(ξ)=[f(b)-f(a)]/(b-a)', xy=(c, f(c)), xytext=(c+0.6, f(c)+0.6), fontsize=6.5,
            arrowprops=dict(arrowstyle='->', lw=0.8))
ax.set_xlim(0, 4); ax.set_ylim(0, 4.5)
ax.legend(fontsize=6, frameon=False); ax.set_title('拉格朗日中值定理', fontsize=8)
ax.spines[['top','right']].set_visible(False)
fig.tight_layout(); fig.savefig(f'{OUT}/mean-value-theorem.png', dpi=300, bbox_inches='tight'); plt.close(fig)
print('✅ mean-value-theorem.png')

# ============ 高数 5：平面图形面积 ============
fig, ax = plt.subplots(figsize=(3.5, 2.4))
x = np.linspace(0, 3, 300)
f = lambda t: -0.5*(t-1.5)**2 + 3
g = lambda t: 0.6*t + 0.5
ax.fill_between(x, f(x), g(x), where=(x>=0.5)&(x<=2.5), alpha=0.3, color='#C0392B')
ax.fill_between(x, f(x), g(x), where=(x>=0.5)&(x<=2.5), alpha=0.35, color='#2F6B9E')
ax.plot(x, f(x), color='#2F6B9E', lw=1.5, label='y=f(x)')
ax.plot(x, g(x), color='#C0392B', lw=1.5, label='y=g(x)')
ax.text(1.5, 2.5, 'S = ∫[f(x)-g(x)]dx', fontsize=7, ha='center', color='#444')
ax.set_xlim(0, 3); ax.set_ylim(0, 4); ax.legend(fontsize=6, frameon=False)
ax.set_title('求平面图形的面积', fontsize=8); ax.spines[['top','right']].set_visible(False)
fig.tight_layout(); fig.savefig(f'{OUT}/area-between-curves.png', dpi=300, bbox_inches='tight'); plt.close(fig)
print('✅ area-between-curves.png')

# ============ 高数 6：旋转体体积 ============
fig, ax = plt.subplots(figsize=(3.5, 2.8))
x = np.linspace(0, 2, 300)
f = lambda t: 1.5 + 0.5*np.sin(2*t) + 0.3*t
y = f(x)
# 旋转体轮廓（生成旋转体形状）
theta = np.linspace(0, 2*np.pi, 30)
X = x[:, None]
Y = y[:, None] * np.cos(theta)
Z = y[:, None] * np.sin(theta)
# 画横截面圆环（示意）
for xi in [0.3, 0.8, 1.3, 1.8]:
    idx = np.argmin(np.abs(x - xi))
    r = y[idx]
    phi = np.linspace(0, 2*np.pi, 40)
    ax.plot(r*np.cos(phi), r*np.sin(phi), '-', color='#C0392B', lw=0.7, alpha=0.5)
ax.plot(x, y, color='#2F6B9E', lw=2.0, label='平面曲线')
ax.plot(x, -y, color='#2F6B9E', lw=0.8, ls='--', alpha=0.5)
ax.fill_between(x, y, -y, alpha=0.08, color='#2F6B9E')
ax.set_xlim(0, 2.2); ax.set_ylim(-2.8, 2.8)
ax.set_title('旋转体（绕 x 轴旋转）', fontsize=8)
ax.axis('equal'); ax.spines[['top','right']].set_visible(False)
fig.tight_layout(); fig.savefig(f'{OUT}/solid-of-revolution.png', dpi=300, bbox_inches='tight'); plt.close(fig)
print('✅ solid-of-revolution.png')

# ============ 高数 7：泰勒多项式逼近 ============
fig, ax = plt.subplots(figsize=(3.5, 2.4))
x = np.linspace(-2, 2, 300)
f = lambda t: np.exp(t)
# 泰勒展开指数函数
ax.plot(x, f(x), 'k-', lw=1.8, label='eˣ (真实)')
for n, c in [(1, '#C0392B'), (2, '#E67E22'), (3, '#27AE60'), (5, '#2F6B9E')]:
    approx = np.ones_like(x)
    term = np.ones_like(x)
    for i in range(1, n+1):
        term *= x / i
        approx += term
    ax.plot(x, approx, '--', color=c, lw=1.0, label=f'P{n}(x) (n={n})')
ax.set_xlim(-2, 2); ax.set_ylim(-1, 5)
ax.legend(fontsize=5.5, frameon=False, ncol=2)
ax.set_title('泰勒多项式逼近 eˣ（阶数越高越准）', fontsize=7.5)
ax.spines[['top','right']].set_visible(False)
fig.tight_layout(); fig.savefig(f'{OUT}/taylor-approximation.png', dpi=300, bbox_inches='tight'); plt.close(fig)
print('✅ taylor-approximation.png')

# ============ 高数 8：渐近线 ============
fig, ax = plt.subplots(figsize=(3.5, 2.4))
x = np.linspace(-5, 5, 500)
f = lambda t: (2*t**2 + 1) / (t - 1)
y = f(x)
y = np.clip(y, -15, 15)
ax.plot(x, y, color='#2F6B9E', lw=1.2, label='y=f(x)')
ax.axvline(1, color='#C0392B', lw=1.0, ls='--', label='垂直渐近线 x=1')
k = 2
ax.plot(x, k*x + 2, color='#27AE60', lw=1.0, ls='--', label='斜渐近线 y=2x+2')
ax.set_xlim(-4, 4.5); ax.set_ylim(-12, 12)
ax.legend(fontsize=6, frameon=False); ax.set_title('函数曲线的渐近线', fontsize=8)
ax.spines[['top','right']].set_visible(False)
fig.tight_layout(); fig.savefig(f'{OUT}/asymptotes.png', dpi=300, bbox_inches='tight'); plt.close(fig)
print('✅ asymptotes.png')

# ============ 计算机 1：顺序表插入/删除复杂度 ============
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.0))
for ax, title, label, color, fill in zip(axes,
    ['顺序表插入（元素后移）', '顺序表删除（元素前移）'],
    ['在第 i 位插入 → n-i+1 个元素后移', '删除第 i 位 → n-i 个元素前移'],
    ['#C0392B', '#2F6B9E'], ['#FDD', '#DDF']):
    for i in range(6):
        rect = Rectangle((i*0.5, 0.2), 0.45, 0.8, fc='white', ec='#888', lw=0.8)
        ax.add_patch(rect)
        ax.text(i*0.5+0.22, 0.6, str(i+1), ha='center', va='center', fontsize=7)
    # 标记插入/删除位置
    insert = 3
    rect = Rectangle((insert*0.5, 0.2), 0.45, 0.8, fc=fill, ec=color, lw=1.5)
    ax.add_patch(rect)
    ax.text(insert*0.5+0.22, 0.6, '↓', ha='center', va='center', fontsize=9, color=color)
    # 箭头表示移动方向
    for i in range(insert, 5):
        ax.annotate('', xy=((i+1)*0.5+0.22, 0.2), xytext=(i*0.5+0.22, 0.2),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.0))
    ax.set_title(title, fontsize=7.5)
    ax.text(0.5, -0.15, label, fontsize=6, ha='center', color='#444')
    ax.set_xlim(-0.3, 3.5); ax.set_ylim(-0.3, 1.3); ax.axis('off')
fig.tight_layout(); fig.savefig(f'{OUT}/seqlist-insert-delete.png', dpi=300, bbox_inches='tight'); plt.close(fig)
print('✅ seqlist-insert-delete.png')

# ============ 计算机 2：Prim 最小生成树 ============
fig, axes = plt.subplots(1, 4, figsize=(7.2, 1.8))
# 图：顶点 1-5，边：1-3(1), 3-2(2), 1-2(3), 3-5(4), 2-4(5), 3-4(6), 4-5(7)
poses = {1: (0, 0.8), 2: (-1.0, 0), 3: (1.0, 0), 4: (-0.8, -0.7), 5: (1.2, -0.7)}
edges_all = [(1,3,1),(1,2,3),(3,2,2),(3,5,4),(2,4,5),(3,4,6),(4,5,7)]
# 每步选中的边
steps = [
    ([], [1, 3], [], '① 选 1-3(1)'),
    ([(1,3)], [1,3,2], [(1,3),(3,2)], '② 加 3-2(2)'),
    ([(1,3),(3,2)], [1,3,2,5], [(1,3),(3,2),(3,5)], '③ 加 3-5(4)'),
    ([(1,3),(3,2),(3,5)], [1,3,2,5,4], [(1,3),(3,2),(3,5),(2,4)], '④ 加 2-4(5)'),
]
for ax, (sel, verts, tree, title) in zip(axes, steps):
    all_vertices = set(range(1,6))
    for a,b,w in edges_all:
        is_tree = (a,b) in tree or (b,a) in tree
        is_candidate = False
        for ta,tb,tw in [(a,b,w),(b,a,w)]:
            if (ta in verts and tb not in verts) or (tb in verts and ta not in verts):
                is_candidate = True
        if is_tree:
            ec = '#C0392B'; lw = 2.5
        elif is_candidate:
            ec = '#E67E22'; lw = 1.2
        else:
            ec = '#CCC'; lw = 0.6
        ax.plot([poses[a][0], poses[b][0]], [poses[a][1], poses[b][1]], color=ec, lw=lw, zorder=1)
        mx, my = (poses[a][0]+poses[b][0])/2, (poses[a][1]+poses[b][1])/2
        ax.text(mx+0.05, my+0.05, str(w), fontsize=5.5, color='#666')
    for v, (x,y) in poses.items():
        fc = '#FFE9C9' if v in verts else '#F5F5F5'
        circ = Circle((x,y), 0.18, fc=fc, ec='#555', lw=0.8)
        ax.add_patch(circ)
        ax.text(x, y, str(v), ha='center', va='center', fontsize=7)
    ax.set_title(title, fontsize=6.5); ax.set_xlim(-1.5, 1.8); ax.set_ylim(-1.1, 1.3); ax.axis('off')
fig.tight_layout(); fig.savefig(f'{OUT}/prim-mst.png', dpi=300, bbox_inches='tight'); plt.close(fig)
print('✅ prim-mst.png')

# ============ 计算机 3：快排挖坑填数 ============
fig, ax = plt.subplots(figsize=(3.5, 2.6))
data = [49, 38, 65, 97, 76, 13, 27]
steps_qs = [
    (0, 6, '初始', [49, 38, 65, 97, 76, 13, 27], '#C0392B'),
    (0, 6, '挖坑 pivot=49', ['空', 38, 65, 97, 76, 13, 27], '#E67E22'),
    (0, 6, '右 27 填左坑', [27, 38, 65, 97, 76, 13, '空'], '#E67E22'),
    (2, 5, '左 65 填右坑', [27, 38, '空', 97, 76, 13, 65], '#E67E22'),
    (2, 5, '右 13 填左坑', [27, 38, 13, 97, 76, '空', 65], '#E67E22'),
    (3, 4, '左 97 填右坑', [27, 38, 13, '空', 76, 97, 65], '#E67E22'),
    (3, 3, '基准归位 49', [27, 38, 13, 49, 76, 97, 65], '#27AE60'),
]
for k, (low, high, desc, arr, color) in enumerate(steps_qs):
    yy = 2.2 - k*0.32
    for i, v in enumerate(arr):
        fc = '#FFF' if v == '空' else ('#E8F1F8' if low <= i <= high else '#F0F0F0')
        if v == '空':
            fc = '#FFE9C9'
        rect = Rectangle((i*0.72, yy), 0.65, 0.28, fc=fc, ec='#888', lw=0.5)
        ax.add_patch(rect)
        ax.text(i*0.72+0.32, yy+0.14, str(v) if v != '空' else '□', ha='center', va='center', fontsize=6, color='#444')
    ax.text(-0.9, yy+0.14, desc, ha='right', va='center', fontsize=5.5, color=color)
ax.set_xlim(-1.5, 5.5); ax.set_ylim(-0.1, 2.6); ax.axis('off')
ax.set_title('快速排序第一趟划分（挖坑填数，基准 49）', fontsize=7)
fig.tight_layout(); fig.savefig(f'{OUT}/quicksort-partition.png', dpi=300, bbox_inches='tight'); plt.close(fig)
print('✅ quicksort-partition.png')

# ============ 计算机 4：完全二叉树数组映射 ============
fig, ax = plt.subplots(figsize=(3.5, 2.6))
# 树形结构
tree = {'A': ('B','C'), 'B': ('D','E'), 'C': ('F','G'), 'D': (None,None), 'E': (None,None), 'F': (None,None), 'G': (None,None)}
tpos = {'A': (0, 1.2), 'B': (-0.8, 0.5), 'C': (0.8, 0.5), 'D': (-1.2, -0.2), 'E': (-0.4, -0.2), 'F': (0.4, -0.2), 'G': (1.2, -0.2)}
for node, (l,r) in tree.items():
    x, y = tpos[node]
    if l: ax.plot([x, tpos[l][0]], [y, tpos[l][1]], color='#888', lw=0.8)
    if r: ax.plot([x, tpos[r][0]], [y, tpos[r][1]], color='#888', lw=0.8)
    circ = Circle((x, y), 0.2, fc='#E8F1F8', ec='#2F6B9E', lw=1.0)
    ax.add_patch(circ)
    ax.text(x, y, node, ha='center', va='center', fontsize=7)
# 数组下标
arr = ['A','B','C','D','E','F','G']
for i, v in enumerate(arr):
    rect = Rectangle((2.5 + i*0.4, 0.3 + (1-i%2)*0.5), 0.35, 0.4, fc='#E8F1F8', ec='#2F6B9E', lw=0.8)
    ax.add_patch(rect)
    ax.text(2.5+i*0.4+0.17, 0.5+(1-i%2)*0.5, v, ha='center', va='center', fontsize=6.5)
    ax.text(2.5+i*0.4+0.17, 0.05+(1-i%2)*0.5, str(i+1), ha='center', va='center', fontsize=5, color='#888')
# 连线：树→数组
for i, v in enumerate(arr):
    if v in tpos:
        tx, ty = tpos[v]
        ax.annotate('', xy=(2.5+i*0.4+0.17, 0.3+(1-i%2)*0.5), xytext=(tx, ty-0.2),
                    arrowprops=dict(arrowstyle='->', lw=0.5, color='#C0392B', alpha=0.5))
ax.set_title('完全二叉树 → 顺序存储（父 i → 左 2i 右 2i+1）', fontsize=7)
ax.set_xlim(-1.5, 5.5); ax.set_ylim(-0.5, 1.6); ax.axis('off')
fig.tight_layout(); fig.savefig(f'{OUT}/complete-tree-array.png', dpi=300, bbox_inches='tight'); plt.close(fig)
print('✅ complete-tree-array.png')

# ============ 计算机 5：广义表嵌套结构 ============
fig, ax = plt.subplots(figsize=(3.5, 2.2))
ax.set_title('广义表 L=(a,(b,c),(d,(e,f))) 括号嵌套结构', fontsize=7)
# 用文字和括号画层次
lines = [
    (0, 'L = (', 0),
    (1, '  a,', 0),
    (1, '  (', 0.5),
    (2, '    b,', 0.3),
    (2, '    c', 0.3),
    (1, '  ),', 0.5),
    (1, '  (', 0.5),
    (2, '    d,', 0.3),
    (2, '    (', 0.8),
    (3, '      e,', 0.5),
    (3, '      f', 0.5),
    (2, '    )', 0.8),
    (1, '  )', 0.5),
    (0, ')', 0),
]
for i, (level, text, extra) in enumerate(lines):
    yy = 1.5 - i*0.14
    ax.text(extra, yy, text, fontsize=5.5, fontfamily='monospace', color='#2F6B9E' if text.strip().endswith(',') or text.strip()==')' or text.strip()=='L = (' else '#444')
ax.text(0, -0.2, '深度 = 3（最大嵌套层数） | 长度 = 3（3 个元素）', fontsize=6.5, color='#444')
ax.set_xlim(-0.2, 3.5); ax.set_ylim(-0.3, 1.7); ax.axis('off')
fig.tight_layout(); fig.savefig(f'{OUT}/generalized-list.png', dpi=300, bbox_inches='tight'); plt.close(fig)
print('✅ generalized-list.png')

print('\n全部 13 张图生成完毕')