# -*- coding: utf-8 -*-
"""第三批 P0 配图：数据结构 6 张核心算法/结构图
1. 冒泡排序逐趟演化（2.8-排序.md）
2. 折半查找区间收缩（2.7-查找.md）
3. DFS/BFS 图遍历（2.6-图.md）
4. 邻接矩阵 vs 邻接表（2.6-图.md）
5. struct vs union 内存布局（1.9-结构体与共用体.md）
6. 循环队列判满/判空（2.3-栈和队列.md）
输出到 docs/public/figs/
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle
import numpy as np
from _figstyle import setup_style, FIGS_DIR  # noqa: E402

setup_style(journal='nature', lang='zh')
OUT = FIGS_DIR

# ============ 图 1：冒泡排序逐趟演化 ============
data = [49, 38, 65, 97, 76, 13, 27]
passes = []
cur = data[:]
passes.append(cur[:])
for i in range(len(cur)-1):
    for j in range(len(cur)-1-i):
        if cur[j] > cur[j+1]:
            cur[j], cur[j+1] = cur[j+1], cur[j]
    passes.append(cur[:])

fig, axes = plt.subplots(len(passes), 1, figsize=(3.5, 5.2), sharex=True)
xpos = np.arange(len(data))
for idx, (ax, arr) in enumerate(zip(axes, passes)):
    colors = ['#2F6B9E']*len(arr)
    ax.bar(xpos, arr, color=colors, width=0.6, edgecolor='white', lw=0.5)
    for xi, v in zip(xpos, arr):
        ax.text(xi, v+2, str(v), ha='center', fontsize=6)
    ax.set_ylabel(f'第{idx}趟' if idx > 0 else '初始', fontsize=6)
    ax.set_ylim(0, 115)
    ax.set_yticks([])
    ax.spines[['top', 'right', 'left']].set_visible(False)
fig.suptitle('冒泡排序逐趟演化（最大值沉底）', fontsize=8, y=0.99)
fig.tight_layout()
fig.savefig(f'{OUT}/bubble-sort.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ 图1 冒泡排序: bubble-sort.png')

# ============ 图 2：折半查找区间收缩 ============
arr = [12, 18, 21, 35, 45, 55, 66]
target = 21
fig, ax = plt.subplots(figsize=(3.5, 2.4))
y = 0
# 第一步 mid=35
ax.bar(xpos, [1]*7, color=['#E8F1F8']*7, width=0.7)
for i, v in enumerate(arr):
    ax.text(i, 0.5, str(v), ha='center', fontsize=8)
ax.set_yticks([])
ax.set_xticks([])
ax.spines[['top','right','left']].set_visible(False)
# 用分段标注代替
fig2, ax2 = plt.subplots(figsize=(3.5, 2.8))
steps = [
    ('① mid=35(下标3)', [0, 2], 'low=0 high=6', '#C0392B'),
    ('② 35>21 → high=2', [0, 2], 'mid=18(下标1)', '#E67E22'),
    ('③ 18<21 → low=2', [2, 2], 'mid=21 ✓ 找到', '#27AE60'),
]
for k, (title, rng, note, color) in enumerate(steps):
    yy = 2.2 - k*0.8
    for i in range(7):
        fc = color if rng[0] <= i <= rng[1] else '#F0F0F0'
        rect = Rectangle((i*0.55, yy), 0.5, 0.55, fc=fc, ec='#888', lw=0.6)
        ax2.add_patch(rect)
        ax2.text(i*0.55+0.25, yy+0.28, str(arr[i]), ha='center', va='center', fontsize=6.5)
    ax2.text(-0.3, yy+0.28, title, ha='right', va='center', fontsize=6)
    ax2.text(4.4, yy+0.28, note, ha='left', va='center', fontsize=6, color=color)
ax2.set_xlim(-2.2, 6.5); ax2.set_ylim(-0.3, 2.8); ax2.axis('off')
ax2.set_title('折半查找找 21（每次排除一半）', fontsize=7.5)
fig2.tight_layout()
fig2.savefig(f'{OUT}/binary-search.png', dpi=300, bbox_inches='tight')
plt.close(fig2)
print('✅ 图2 折半查找: binary-search.png')

# ============ 图 3：DFS/BFS 图遍历 ============
# 图：1-2, 1-3, 2-4, 3-4, 4-5
pos = {1: (0, 1.4), 2: (-1.0, 0.4), 3: (1.0, 0.4), 4: (0, -0.4), 5: (1.8, -0.9)}
edges = [(1,2),(1,3),(2,4),(3,4),(4,5)]
dfs_seq = [1, 2, 4, 3, 5]
bfs_seq = [1, 2, 3, 4, 5]

fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.8))
for ax, (title, seq, color) in zip(axes, [
    ('DFS 深度优先 · 走迷宫', dfs_seq, '#C0392B'),
    ('BFS 广度优先 · 逐层波浪', bfs_seq, '#2F6B9E'),
]):
    for a, b in edges:
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], color='#AAAAAA', lw=0.9, zorder=1)
    for node, (x, y) in pos.items():
        circ = Circle((x, y), 0.22, fc='white', ec='#555', lw=1.0, zorder=2)
        ax.add_patch(circ)
        ax.text(x, y, str(node), ha='center', va='center', fontsize=7.5, zorder=3)
    # 访问顺序标注
    for order, node in enumerate(seq, 1):
        x, y = pos[node]
        ax.text(x+0.28, y+0.28, str(order), fontsize=6.5, color=color, fontweight='bold', zorder=4)
    ax.set_title(title, fontsize=7.5)
    ax.set_xlim(-1.5, 2.6); ax.set_ylim(-1.3, 1.9)
    ax.axis('off')
    ax.text(0.55, -1.65, '→'.join(map(str, seq)), fontsize=8, color=color, ha='center', fontweight='bold')
fig.tight_layout()
fig.savefig(f'{OUT}/dfs-bfs.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ 图3 DFS/BFS: dfs-bfs.png')

# ============ 图 4：邻接矩阵 vs 邻接表 ============
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.6))
# 左：无向图
ax = axes[0]
for a, b in edges:
    ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], color='#AAAAAA', lw=0.9)
for node, (x, y) in pos.items():
    circ = Circle((x, y), 0.2, fc='#E8F1F8', ec='#2F6B9E', lw=1.0)
    ax.add_patch(circ)
    ax.text(x, y, str(node), ha='center', va='center', fontsize=7.5)
ax.set_title('无向图 G（5 顶点 5 边）', fontsize=7.5)
ax.set_xlim(-1.5, 2.6); ax.set_ylim(-1.3, 1.9); ax.axis('off')

# 右：邻接矩阵（对称）
ax = axes[1]
ax.set_title('邻接矩阵（对称，5×5）', fontsize=7.5)
mat = [[0]*5 for _ in range(5)]
for a, b in edges:
    mat[a-1][b-1] = mat[b-1][a-1] = 1
for i in range(5):
    for j in range(5):
        rect = Rectangle((j*0.42, (4-i)*0.42), 0.4, 0.4,
                         fc='#2F6B9E' if mat[i][j] else '#F5F5F5',
                         ec='#888', lw=0.5)
        ax.add_patch(rect)
        ax.text(j*0.42+0.2, (4-i)*0.42+0.2, str(mat[i][j]), ha='center', va='center', fontsize=6, color='white' if mat[i][j] else '#444')
# 行标签
for i in range(5):
    ax.text(-0.25, (4-i)*0.42+0.2, str(i+1), ha='right', va='center', fontsize=6)
for j in range(5):
    ax.text(j*0.42+0.2, 2.3, str(j+1), ha='center', va='bottom', fontsize=6)
ax.set_xlim(-0.5, 2.4); ax.set_ylim(-0.2, 2.5); ax.axis('off')
ax.text(1.0, -0.45, '空间 O(n²) · 查边 O(1)', fontsize=6, ha='center', color='#444')
fig.tight_layout()
fig.savefig(f'{OUT}/adjacency.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ 图4 邻接矩阵: adjacency.png')

# ============ 图 5：struct vs union 内存布局 ============
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.2))
# struct：独立格子（含对齐）
ax = axes[0]
ax.set_title('struct S { char c; int i; } → 8 字节（含对齐）', fontsize=7)
for j, (label, w) in enumerate([('c', 1), ('(填充)', 1), ('i', 2), ('i', 2)]):
    rect = Rectangle((j*0.7, 0.3), 0.65, 1.0, fc='#E8F1F8' if label != '(填充)' else '#F0F0F0',
                     ec='#2F6B9E' if label != '(填充)' else '#CCC', lw=1.0)
    ax.add_patch(rect)
    if label != '(填充)':
        ax.text(j*0.7+0.32, 0.8, label, ha='center', va='center', fontsize=7.5)
ax.text(1.4, -0.15, '各成员独立存放', fontsize=6, ha='center', color='#444')
ax.set_xlim(-0.3, 3.1); ax.set_ylim(-0.4, 1.6); ax.axis('off')
# union：共享同一块
ax = axes[1]
ax.set_title('union U { char c; int i; } → 4 字节（共享）', fontsize=7)
rect = Rectangle((0.2, 0.3), 2.1, 1.0, fc='#FFE9C9', ec='#E6A23C', lw=1.4)
ax.add_patch(rect)
ax.text(0.7, 0.8, 'c', ha='center', va='center', fontsize=8)
ax.text(1.6, 0.8, 'i', ha='center', va='center', fontsize=8)
ax.text(1.25, 1.45, '同一块内存', fontsize=6, ha='center', color='#E6A23C')
ax.text(1.25, -0.15, 'sizeof(union) = 最大成员', fontsize=6, ha='center', color='#444')
ax.set_xlim(-0.3, 2.8); ax.set_ylim(-0.4, 1.8); ax.axis('off')
fig.tight_layout()
fig.savefig(f'{OUT}/struct-union.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ 图5 struct/union: struct-union.png')

# ============ 图 6：循环队列判满/判空 ============
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.2))
# 循环队列环形示意
def draw_ring(ax, title, full=True):
    n = 8
    angles = np.linspace(90, 90-360, n, endpoint=False)
    ax.set_title(title, fontsize=7)
    for i in range(n):
        a = np.radians(angles[i])
        x, y = np.cos(a)*0.8, np.sin(a)*0.8
        occupied = (i < 4)  # 前 4 格有元素
        fc = '#E8F1F8' if occupied else '#F5F5F5'
        ec = '#2F6B9E' if occupied else '#BBB'
        circ = Circle((x, y), 0.16, fc=fc, ec=ec, lw=1.0)
        ax.add_patch(circ)
        ax.text(x, y, str(i+1), ha='center', va='center', fontsize=5.5,
                color='#2F6B9E' if occupied else '#999')
    # front / rear 标注（满时 rear+1==front）
    if full:
        f_idx, r_idx = 1, 5  # front=2号格, rear=6号格 → (rear+1)%8 == front
        label = '(rear+1)%8 == front → 满'
    else:
        f_idx, r_idx = 1, 1
        label = 'front == rear → 空'
    a_f = np.radians(angles[f_idx]); a_r = np.radians(angles[r_idx])
    ax.annotate('front', xy=(np.cos(a_f)*0.8, np.sin(a_f)*0.8), xytext=(-1.15, -0.95),
                fontsize=6, color='#C0392B', arrowprops=dict(arrowstyle='->', lw=0.8, color='#C0392B'))
    ax.annotate('rear', xy=(np.cos(a_r)*0.8, np.sin(a_r)*0.8), xytext=(1.15, -0.95),
                fontsize=6, color='#2F6B9E', arrowprops=dict(arrowstyle='->', lw=0.8, color='#2F6B9E'))
    ax.text(0, -1.35, label, fontsize=6, ha='center', color='#444')
    ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.6, 1.2); ax.axis('off')

draw_ring(axes[0], '满状态（牺牲一格区分满/空）', full=True)
draw_ring(axes[1], '空状态', full=False)
fig.tight_layout()
fig.savefig(f'{OUT}/circular-queue.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ 图6 循环队列: circular-queue.png')
print('\n全部 6 张图生成完毕')
