# -*- coding: utf-8 -*-
"""第一批 P0 配图：计算机板块 4 张核心数据结构图
1. 二叉树三序遍历（先/中/后序路径）
2. 链表插入"先挂后连"两步图
3. 栈 LIFO 进出示意
4. 指针内存模型图
输出到 docs/public/figs/，Nature 单栏风格（scipilot 规范）
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Rectangle
import numpy as np
from _figstyle import setup_style, FIGS_DIR  # noqa: E402

setup_style(journal='nature', lang='zh')
OUT = FIGS_DIR

# ============ 图 1：二叉树三序遍历 ============
def draw_binary_tree(ax, pos, node, x, y, dx, visited=None, order_text=""):
    """递归画二叉树，visited 为 (节点, 序号) 列表"""
    if node is None:
        return
    children = {'A': ('B', 'C'), 'B': ('D', 'E'), 'C': ('F', 'G'),
                'D': (None, None), 'E': (None, None), 'F': (None, None), 'G': (None, None)}
    l, r = children.get(node, (None, None))
    if l:
        ax.plot([x, x-dx], [y, y-0.55], color='#888888', lw=1.0, zorder=1)
        draw_binary_tree(ax, pos, l, x-dx, y-0.55, dx/2)
    if r:
        ax.plot([x, x+dx], [y, y-0.55], color='#888888', lw=1.0, zorder=1)
        draw_binary_tree(ax, pos, r, x+dx, y-0.55, dx/2)
    # 节点
    num = ""
    if visited:
        for v in visited:
            if v[0] == node:
                num = f"\n[{v[1]}]"
                break
    circle = plt.Circle((x, y), 0.22, fc='#E8F1F8', ec='#2F6B9E', lw=1.2, zorder=2)
    ax.add_patch(circle)
    ax.text(x, y, node + num, ha='center', va='center', fontsize=9, zorder=3)

# 三张子图：先序/中序/后序
fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.4))
orders = [
    ('先序 · 根→左→右', [('A',1),('B',2),('D',3),('E',4),('C',5),('F',6),('G',7)]),
    ('中序 · 左→根→右', [('D',1),('B',2),('E',3),('A',4),('F',5),('C',6),('G',7)]),
    ('后序 · 左→右→根', [('D',1),('E',2),('B',3),('F',4),('G',5),('C',6),('A',7)]),
]
for ax, (title, visited) in zip(axes, orders):
    ax.set_xlim(-1.4, 1.4); ax.set_ylim(-0.8, 0.9)
    ax.axis('off')
    ax.set_title(title, fontsize=8)
    draw_binary_tree(ax, None, 'A', 0, 0.55, 0.7, visited=visited)
    # 底部序列
    seq = ' '.join(v[0] for v in visited)
    ax.text(0, -0.95, seq, ha='center', va='top', fontsize=8.5, color='#2F6B9E', fontweight='bold')
fig.tight_layout()
fig.savefig(f'{OUT}/binary-tree-traversal.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ 图1 二叉树三序遍历: binary-tree-traversal.png')

# ============ 图 2：链表插入"先挂后连" ============
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.2))
# 步骤 1：先挂 s->next = p->next
ax = axes[0]
ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis('off')
ax.set_title('① 先挂：s->next = p->next（新结点先指向 b）', fontsize=7.5)
# 结点 p -> a -> b
for (x, label) in [(1, 'p'), (3, 'a'), (6, 'b')]:
    r = Rectangle((x, 1.2), 1.4, 1.0, fc='white', ec='#2F6B9E', lw=1.2)
    ax.add_patch(r)
    ax.text(x+0.7, 1.7, label, ha='center', va='center', fontsize=9)
# 新结点 s
r = Rectangle((8, 2.6), 1.4, 1.0, fc='#FFE9C9', ec='#E6A23C', lw=1.5)
ax.add_patch(r)
ax.text(8.7, 3.1, 's', ha='center', va='center', fontsize=9)
# 箭头：p->a, a->b, s->b
for (x1,y1,x2,y2,c) in [(2.4,1.7,3,1.7,'#555'), (4.4,1.7,6,1.7,'#555'), (8.7,2.6,6.8,1.9,'#E6A23C')]:
    ax.annotate('', xy=(x2,y2), xytext=(x1,y1),
                arrowprops=dict(arrowstyle='->', color=c, lw=1.3))
ax.text(7.8, 1.9, 'next', fontsize=6, color='#E6A23C')
ax.text(0.2, 0.2, 's->next = p->next\nb 还连着 a，链未断', fontsize=6.5, color='#444')

# 步骤 2：后连 p->next = s
ax = axes[1]
ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis('off')
ax.set_title('② 后连：p->next = s（a 再指向 s）', fontsize=7.5)
for (x, label) in [(1, 'p'), (3, 'a'), (6, 'b')]:
    r = Rectangle((x, 1.2), 1.4, 1.0, fc='white', ec='#2F6B9E', lw=1.2)
    ax.add_patch(r)
    ax.text(x+0.7, 1.7, label, ha='center', va='center', fontsize=9)
r = Rectangle((8, 2.6), 1.4, 1.0, fc='#FFE9C9', ec='#E6A23C', lw=1.5)
ax.add_patch(r)
ax.text(8.7, 3.1, 's', ha='center', va='center', fontsize=9)
# 新箭头：a->s, s->b
ax.annotate('', xy=(8, 2.9), xytext=(4.4, 1.9), arrowprops=dict(arrowstyle='->', color='#2F6B9E', lw=1.5))
ax.annotate('', xy=(6.8, 1.9), xytext=(8.7, 2.6), arrowprops=dict(arrowstyle='->', color='#E6A23C', lw=1.3))
ax.text(5.5, 2.2, 'next', fontsize=6, color='#2F6B9E')
ax.text(0.2, 0.2, 'p->next = s\n顺序反了会丢链！', fontsize=6.5, color='#C0392B')
fig.tight_layout()
fig.savefig(f'{OUT}/linkedlist-insert.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ 图2 链表插入两步图: linkedlist-insert.png')

# ============ 图 3：栈 LIFO 进出示意 ============
fig, ax = plt.subplots(figsize=(3.5, 2.6))
ax.set_xlim(0, 6); ax.set_ylim(0, 5); ax.axis('off')
# 栈体
for i in range(4):
    r = Rectangle((2, 0.3+i*0.85), 2.2, 0.75, fc='white', ec='#2F6B9E', lw=1.1)
    ax.add_patch(r)
# 栈中元素（自底向上：1 2 3）
labels = ['栈底', '1', '2', '3(栈顶)']
for i, lab in enumerate(labels):
    ax.text(3.1, 0.68+i*0.85, lab, ha='center', va='center', fontsize=7.5)
# 箭头 push 4
ax.annotate('', xy=(3.1, 4.0), xytext=(3.1, 4.7), arrowprops=dict(arrowstyle='->', color='#C0392B', lw=1.5))
ax.text(3.5, 4.45, 'push(4)', fontsize=7.5, color='#C0392B')
# 箭头 pop
ax.annotate('', xy=(1.2, 4.0), xytext=(0.5, 4.7), arrowprops=dict(arrowstyle='->', color='#2F6B9E', lw=1.5))
ax.text(0.2, 4.45, 'pop()', fontsize=7.5, color='#2F6B9E')
ax.text(0.4, 0.2, '后进先出 LIFO：\n只能从栈顶进出', fontsize=6.5, color='#444')
fig.tight_layout()
fig.savefig(f'{OUT}/stack-lifo.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ 图3 栈 LIFO 示意: stack-lifo.png')

# ============ 图 4：指针内存模型 ============
fig, ax = plt.subplots(figsize=(3.5, 2.4))
ax.set_xlim(0, 7); ax.set_ylim(0, 4); ax.axis('off')
# 变量 a 的内存格子
r = Rectangle((0.8, 1.6), 1.8, 1.2, fc='#E8F1F8', ec='#2F6B9E', lw=1.3)
ax.add_patch(r)
ax.text(1.7, 2.2, 'a', ha='center', va='center', fontsize=10)
ax.text(1.7, 1.75, '值=42', ha='center', va='center', fontsize=7)
ax.text(1.7, 1.1, '地址: 0x7F00', ha='center', va='center', fontsize=6, color='#777')
# 指针 p
r = Rectangle((4.2, 1.6), 2.2, 1.2, fc='#FFE9C9', ec='#E6A23C', lw=1.3)
ax.add_patch(r)
ax.text(5.3, 2.2, 'p', ha='center', va='center', fontsize=10)
ax.text(5.3, 1.75, '存地址 → 0x7F00', ha='center', va='center', fontsize=7)
ax.text(5.3, 1.1, 'p 指向 a', ha='center', va='center', fontsize=6, color='#888')
# 箭头 p -> a
ax.annotate('', xy=(2.6, 2.2), xytext=(4.2, 2.2), arrowprops=dict(arrowstyle='->', color='#E6A23C', lw=1.8))
ax.text(0.3, 3.3, '*p 就是 a 的别名\n*p = 100 ⇒ a = 100', fontsize=6.5, color='#444')
fig.tight_layout()
fig.savefig(f'{OUT}/pointer-memory.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('✅ 图4 指针内存模型: pointer-memory.png')
print('\n全部 4 张图生成完毕')
