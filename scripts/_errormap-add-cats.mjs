#!/usr/bin/env node
// 给 errormap 加 3 个新 cat（2.2 线性表 / 2.5 树和二叉树 / 1.10 文件操作）
// 数据源：审计报告里的「薄弱或缺失 / 高频丢分陷阱」节

import {readFileSync, writeFileSync} from 'node:fs';

const PATH = '备考计划/易错点地图.json';

const NEW_CATS = [
  {
    id: 'list',
    name: '线性表（链表/顺序表）',
    icon: '🔗',
    tone: 'orange',
    chapter_id: '2.2',
    chapter: '第二章 数据结构 · 2.2 线性表',
    subject: 'computer',
    items: [
      { id: 'L01', t: '循环链表判尾/判空：p->next != head（L01）', hot: 3 },
      { id: 'L02', t: '链表删除 p->next = q->next 时，先存 q 别先丢', hot: 2 },
      { id: 'L03', t: '带头结点单链表判空：head->next == NULL（非 head == NULL）', hot: 3 },
      { id: 'L04', t: '链式存储结点结构：数据域 + 指针域 两部分', hot: 2 },
      { id: 'L05', t: '循环链表 ≠ 单链表，多了"首尾相连"判定', hot: 3 },
      { id: 'L06', t: '双向链表：前驱 + 后继 两个指针，删除要改两处', hot: 2 },
      { id: 'L07', t: '静态链表用数组模拟，"游标" = 下标，next[i] = 下个元素的下标', hot: 2 },
    ],
  },
  {
    id: 'tree',
    name: '树与二叉树',
    icon: '🌳',
    tone: 'green',
    chapter_id: '2.5',
    chapter: '第二章 数据结构 · 2.5 树和二叉树',
    subject: 'computer',
    items: [
      { id: 'T01', t: '完全二叉树叶子数公式 ⌈n/2⌉ 的推导：最后一层可能不满，从下往上反推', hot: 3 },
      { id: 'T02', t: '单支树（斜树）：n 个结点高度 = n（不是 ⌈log₂n⌉）', hot: 3 },
      { id: 'T03', t: '树的深度 ≠ 结点的度（深度=最大层次，度=孩子数）', hot: 3 },
      { id: 'T04', t: '满二叉树 ⊂ 完全二叉树，反之不成立', hot: 2 },
      { id: 'T05', t: '哈夫曼树高度计算：合并时谁小先合，结果未必平衡', hot: 3 },
      { id: 'T06', t: '遍历序列还原二叉树：先序+中序 或 中序+后序 可唯一还原', hot: 3 },
      { id: 'T07', t: '二叉排序树（BST）：左 < 根 < 右，插入/查找 O(h)', hot: 3 },
      { id: 'T08', t: '平衡二叉树（AVL）：左右子树高度差 ≤ 1，失衡时旋转调整', hot: 3 },
    ],
  },
  {
    id: 'file',
    name: '文件操作',
    icon: '📂',
    tone: 'cyan',
    chapter_id: '1.10',
    chapter: '第一章 C语言基础 · 1.10 文件操作',
    subject: 'computer',
    items: [
      { id: 'F01', t: 'fopen 失败返回 NULL，不判断就用 fp 会段错误', hot: 3 },
      { id: 'F02', t: '"w" 模式会清空已有文件！追加用 "a"，不是 "w"', hot: 3 },
      { id: 'F03', t: 'fclose 成功返回 0，失败返回 EOF（不是 -1）', hot: 2 },
      { id: 'F04', t: '文件名常量必须用双引号（"data.txt"，不是 <data.txt>）', hot: 2 },
      { id: 'F05', t: 'fread/fwrite 用于二进制文件，文本文件用 fscanf/fprintf', hot: 2 },
    ],
  },
];

const raw = readFileSync(PATH, 'utf8');
const data = JSON.parse(raw);
const existing = new Set(data.cats.map(c => c.id));

let added = 0;
for (const nc of NEW_CATS) {
  if (!existing.has(nc.id)) {
    data.cats.push(nc);
    added++;
    console.log(`+ ${nc.id} (${nc.name}) chapter_id=${nc.chapter_id}`);
  } else {
    console.log(`(skip ${nc.id}, 已存在)`);
  }
}

data.updatedAt = new Date().toISOString().slice(0, 10);
data.schema = Math.max(data.schema || 1, 3);

writeFileSync(PATH, JSON.stringify(data, null, 2) + '\n', 'utf8');
console.log(`\n已写入 ${added} 个新 cat`);
console.log(`总 cat 数：${data.cats.length}`);
console.log(`schema 升到 ${data.schema}`);
