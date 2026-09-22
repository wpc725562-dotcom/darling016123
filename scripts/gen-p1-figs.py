# -*- coding: utf-8 -*-
"""P1 批：计算机 6 张图
1. 四种基本逻辑结构（集合/线性/树形/图形）
2. 哈夫曼树构造过程（权值 {2,3,5,7}）
3. KMP next 数组（abaabc 前后缀）
4. 对称矩阵压缩存储
5. 哈希冲突处理（线性探测 vs 链地址）
6. 二维数组行优先存储
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
import numpy as np
from _figstyle import setup_style, FIGS_DIR  # noqa: E402

setup_style(journal='nature', lang='zh')
OUT = FIGS_DIR

# ============ 图 1：四种基本逻辑结构 ============
fig, axes = plt.subplots(1, 4, figsize=(7.2, 2.0))
def draw_struct(ax, title, kind):
    ax.set_title(title, fontsize=7)
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.1, 1.1); ax.axis('off')
    if kind == 'set':
        # 集合：散点
        for x, y in [(0,0.3),(-0.4,-0.2),(0.4,-0.2),(0,-0.7)]:
            ax.add_patch(Circle((x,y), 0.12, fc='#E8F1F8', ec='#2F6B9E', lw=1.0))
    elif kind == 'linear':
        # 线性：链
        for i in range(4):
            ax.add_patch(Rectangle((-0.75+i*0.5, -0.2), 0.42, 0.42, fc='#E8F1F8', ec='#2F6B9E', lw=1.0))
            if i < 3:
                ax.annotate('', xy=(-0.33+i*0.5, 0), xytext=(-0.75+i*0.5+0.42, 0),
                            arrowprops=dict(arrowstyle='->', lw=0.8, color='#2F6B9E'))
    elif kind == 'tree':
        # 树形
        nodes = [(0,0.7),(-0.5,-0.1),(0.5,-0.1),(-0.75,-0.8),(0.75,-0.8)]
        for (x,y) in nodes:
            ax.add_patch(Circle((x,y), 0.12, fc='#E8F1F8', ec='#2F6B9E', lw=1.0))
        for (x1,y1,x2,y2) in [(0,0.58,-0.5,0.02),(0,0.58,0.5,0.02),(-0.5,-0.22,-0.75,-0.68),(0.5,-0.22,0.75,-0.68)]:
            ax.plot([x1,x2],[y1,y2], color='#2F6B9E', lw=0.7)
    else:
        # 图形
        nodes = [(0,0.5),(-0.6,-0.4),(0.6,-0.4)]
        for (x,y) in nodes:
            ax.add_patch(Circle((x,y), 0.12, fc='#E8F1F8', ec='#2F6B9E', lw=1.0))
        for i in range(3):
            for j in range(i+1,3):
                ax.plot([nodes[i][0],nodes[j][0]],[nodes[i][1],nodes[j][1]], color='#2F6B9E', lw=0.7)
for ax, title, kind in zip(axes,
    ['集合结构\n(无关系)', '线性结构\n(1:1)', '树形结构\n(1:N)', '图形结构\n(N:N)'],
    ['set','linear','tree','graph']):
    draw_struct(ax, title, kind)
fig.tight_layout()
fig.savefig(f'{OUT}/logical-structures.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ logical-structures.png')

# ============ 图 2：哈夫曼树构造 ============
fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.2))
steps = [
    ('① 合并 2+3=5', [(5,0,0.8),(5,0.6,0.8),(7,1.2,0.8)], [(0.25,0.6,0.75,0.6)]),
    ('② 合并 5+5=10', [(10,0,0.8),(7,0.6,0.8)], [(0.25,0.6,0.75,0.6)]),
    ('③ 合并 10+7=17', [(17,0,0.8)], []),
]
for ax, (title, nodes, edges) in zip(axes, steps):
    ax.set_title(title, fontsize=7)
    for x, y, r in nodes:
        ax.add_patch(Circle((x,y), r, fc='#E8F1F8', ec='#2F6B9E', lw=1.0))
        ax.text(x, y, str(int(r*10)), ha='center', va='center', fontsize=8)
    for (x1,y1,x2,y2) in edges:
        ax.plot([x1,x2],[y1,y2], color='#2F6B9E', lw=0.8)
    ax.set_xlim(-0.5, 2.5); ax.set_ylim(-0.8, 1.2); ax.axis('off')
# 最终树 + 编码
fig2, ax = plt.subplots(figsize=(3.5, 2.4))
# 哈夫曼树结构（2,3,5,7 → 17）
# 根17 → 左10 → (5(2,3)) | 右7
nodes = {'17':(0,1.2,'17'), '10':(-0.6,0.4,'10'), '7':(0.8,0.4,'7'), '5':(-0.8,-0.3,'5'), '2':(-1.0,-0.9,'2'), '3':(-0.6,-0.9,'3'), '5b':(0.1,-0.9,'5')}
for (x,y,label) in nodes.values():
    ax.add_patch(Circle((x,y), 0.16, fc='#E8F1F8', ec='#2F6B9E', lw=1.0))
    ax.text(x, y, label, ha='center', va='center', fontsize=6.5)
edges = [('17','10','0'),('17','7','1'),('10','5','0'),('10','5b','1'),('5','2','0'),('5','3','1')]
for (a,b,label) in edges:
    x1,y1,_ = nodes[a]; x2,y2,_ = nodes[b]
    ax.plot([x1,x2],[y1,y2], color='#2F6B9E', lw=0.7)
    mx, my = (x1+x2)/2, (y1+y2)/2
    ax.text(mx, my, label, fontsize=6, color='#C0392B')
ax.text(1.6, 1.0, 'WPL = 2×3+3×3\n+5×2+7×1 = 32', fontsize=6, color='#444')
ax.set_title('哈夫曼树与编码（左0右1）', fontsize=7)
ax.set_xlim(-1.4, 2.4); ax.set_ylim(-1.2, 1.5); ax.axis('off')
fig2.tight_layout()
fig2.savefig(f'{OUT}/huffman-tree.png', dpi=300, bbox_inches='tight')
plt.close(fig); plt.close(fig2)
print('✅ huffman-tree.png')

# ============ 图 3：KMP next 数组 ============
fig, ax = plt.subplots(figsize=(3.5, 2.4))
T = 'abaabc'
next_arr = [0, 1, 1, 2, 2, 3]
ax.set_title("KMP 模式串 abaabc 的 next 数组", fontsize=7.5)
# 模式串行
for i, ch in enumerate(T):
    rect = Rectangle((i*0.5, 1.2), 0.48, 0.45, fc='#E8F1F8', ec='#2F6B9E', lw=1.0)
    ax.add_patch(rect)
    ax.text(i*0.5+0.24, 1.42, ch, ha='center', va='center', fontsize=9)
    ax.text(i*0.5+0.24, 1.05, f'j={i+1}', ha='center', va='center', fontsize=5.5, color='#888')
# next 行
for i, v in enumerate(next_arr):
    rect = Rectangle((i*0.5, 0.4), 0.48, 0.45, fc='#FFE9C9', ec='#E6A23C', lw=1.0)
    ax.add_patch(rect)
    ax.text(i*0.5+0.24, 0.62, str(v), ha='center', va='center', fontsize=9)
ax.text(-0.5, 1.4, 'T:', ha='right', va='center', fontsize=7)
ax.text(-0.5, 0.62, 'next:', ha='right', va='center', fontsize=7)
# 说明
ax.text(0, 0, 'next[1]=0 规定；next[j] = 前 j-1 个字符最长相等前后缀 + 1', fontsize=5.8, color='#444')
ax.text(0, -0.25, '例：ab 前缀 a 后缀 b 不等 → next[3]=1；aba 前缀 ab 后缀 ba 不等', fontsize=5.8, color='#444')
ax.set_xlim(-1.2, 3.4); ax.set_ylim(-0.4, 1.8); ax.axis('off')
fig.tight_layout()
fig.savefig(f'{OUT}/kmp-next.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ kmp-next.png')

# ============ 图 4：对称矩阵压缩 ============
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.4))
# 左：对称矩阵
ax = axes[0]
ax.set_title('对称矩阵（下三角按行存储）', fontsize=7)
mat = [[1,2,3,4,5],[2,6,7,8,9],[3,7,10,11,12],[4,8,11,13,14],[5,9,12,14,15]]
for i in range(5):
    for j in range(5):
        fc = '#E8F1F8' if j <= i else '#F0F0F0'
        rect = Rectangle((j*0.5, (4-i)*0.5), 0.48, 0.48, fc=fc, ec='#888', lw=0.5)
        ax.add_patch(rect)
        ax.text(j*0.5+0.24, (4-i)*0.5+0.24, str(mat[i][j]), ha='center', va='center', fontsize=6)
ax.text(0.7, -0.3, 'a[i][j] 存到 k = i(i+1)/2 + j', fontsize=6, ha='center', color='#C0392B')
ax.set_xlim(-0.3, 2.8); ax.set_ylim(-0.5, 2.8); ax.axis('off')
# 右：压缩一维数组
ax = axes[1]
ax.set_title('一维压缩数组 SA[0..14]（下三角）', fontsize=7)
flat = [1,2,6,3,7,10,4,8,11,13,5,9,12,14,15]
for i, v in enumerate(flat):
    rect = Rectangle((i*0.28, 0.6), 0.26, 0.5, fc='#FFE9C9', ec='#E6A23C', lw=0.6)
    ax.add_patch(rect)
    ax.text(i*0.28+0.13, 0.85, str(v), ha='center', va='center', fontsize=5.5)
    ax.text(i*0.28+0.13, 0.45, str(i), ha='center', va='center', fontsize=4.5, color='#888')
ax.text(2.1, 1.35, 'n(n+1)/2 = 15 个元素', fontsize=6, ha='center', color='#444')
ax.set_xlim(-0.2, 4.5); ax.set_ylim(0.3, 1.6); ax.axis('off')
fig.tight_layout()
fig.savefig(f'{OUT}/symmetric-matrix.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ symmetric-matrix.png')

# ============ 图 5：哈希冲突处理 ============
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.2))
# 左：线性探测
ax = axes[0]
ax.set_title('开放定址：线性探测（冲突往后挪）', fontsize=7)
buckets = ['', '50', '', '', '', '12', '26']
for i, v in enumerate(buckets):
    rect = Rectangle((i*0.55, 0.3), 0.5, 0.7, fc='#E8F1F8' if v else '#F5F5F5', ec='#2F6B9E', lw=0.8)
    ax.add_patch(rect)
    if v: ax.text(i*0.55+0.25, 0.65, v, ha='center', va='center', fontsize=7)
    ax.text(i*0.55+0.25, 0.15, str(i), ha='center', va='center', fontsize=5, color='#888')
# 26 冲突标记
ax.annotate('26%7=5\n冲突→探测6', xy=(5.5*0.55+0.25, 0.3), xytext=(3.2, 1.2),
            fontsize=5.5, color='#C0392B', arrowprops=dict(arrowstyle='->', lw=0.7, color='#C0392B'))
ax.set_xlim(-0.3, 4.0); ax.set_ylim(-0.2, 1.7); ax.axis('off')
# 右：链地址
ax = axes[1]
ax.set_title('链地址法：冲突挂链表', fontsize=7)
for i in range(4):
    rect = Rectangle((0, i*0.55+0.3), 0.7, 0.5, fc='#F5F5F5', ec='#888', lw=0.6)
    ax.add_patch(rect)
    ax.text(0.35, i*0.55+0.55, str(i+1), ha='center', va='center', fontsize=6)
# 地址 3 的链表：3 → 12 → 24
chain = [(1.3, 0.85), (2.1, 0.85), (2.9, 0.85)]
labels = ['3', '12', '24']
for (x, y), v in zip(chain, labels):
    rect = Rectangle((x, y), 0.6, 0.5, fc='#FFE9C9', ec='#E6A23C', lw=1.0)
    ax.add_patch(rect)
    ax.text(x+0.3, y+0.25, v, ha='center', va='center', fontsize=7)
for i in range(2):
    ax.annotate('', xy=(chain[i+1][0], chain[i][1]+0.25), xytext=(chain[i][0]+0.6, chain[i][1]+0.25),
                arrowprops=dict(arrowstyle='->', lw=0.8, color='#E6A23C'))
ax.text(0.2, 1.6, '3%7=3 → 冲突，全部挂到 3 号链表', fontsize=5.5, color='#444')
ax.set_xlim(-0.3, 4.0); ax.set_ylim(-0.2, 2.0); ax.axis('off')
fig.tight_layout()
fig.savefig(f'{OUT}/hash-collision.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ hash-collision.png')

# ============ 图 6：二维数组行优先 ============
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.2))
# 左：二维表格 a[3][4]
ax = axes[0]
ax.set_title('二维数组 a[3][4]（逻辑）', fontsize=7)
for i in range(3):
    for j in range(4):
        rect = Rectangle((j*0.55, (2-i)*0.55), 0.5, 0.5, fc='#E8F1F8', ec='#2F6B9E', lw=0.8)
        ax.add_patch(rect)
        ax.text(j*0.55+0.25, (2-i)*0.55+0.25, f'a[{i}][{j}]', ha='center', va='center', fontsize=5.5)
ax.text(1.1, -0.25, '按行优先 → 拍平', fontsize=6.5, ha='center', color='#C0392B')
ax.set_xlim(-0.3, 2.6); ax.set_ylim(-0.5, 1.9); ax.axis('off')
# 右：内存
ax = axes[1]
ax.set_title('连续内存（行优先）', fontsize=7)
flat = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3)]
for i, (r,c) in enumerate(flat):
    rect = Rectangle((i*0.35, 0.6), 0.33, 0.5, fc='#FFE9C9', ec='#E6A23C', lw=0.6)
    ax.add_patch(rect)
    ax.text(i*0.35+0.16, 0.85, f'{r},{c}', ha='center', va='center', fontsize=4.5)
    ax.text(i*0.35+0.16, 0.45, f'{100+i*4}', ha='center', va='center', fontsize=4, color='#888')
ax.text(2.2, 1.35, '地址 = 基址 + (i×列数 + j) × sizeof', fontsize=5.8, ha='center', color='#444')
ax.set_xlim(-0.2, 4.6); ax.set_ylim(0.3, 1.6); ax.axis('off')
fig.tight_layout()
fig.savefig(f'{OUT}/2d-array-memory.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ 2d-array-memory.png')
print('\nP1 批计算机 6 张全部完成')