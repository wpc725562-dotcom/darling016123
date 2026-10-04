#!/usr/bin/env node
// 给 audit-*.md 批量加 chapter_id + chapter fm 字段
// 数据源: 当前 title 解析得到的章节号（脚本 fallback 路径）

import {readFileSync, writeFileSync, readdirSync} from 'node:fs';
import {join} from 'node:path';

const DIR = 'docs/posts/computer/notes';

// chapter_id → chapter 中文名映射
const CHAPTER_NAMES = {
  '1.8': '第一章 C语言基础 · 1.8 指针',
  '1.9': '第一章 C语言基础 · 1.9 结构体与共用体',
  '1.10': '第一章 C语言基础 · 1.10 文件操作',
  '1.11': '第一章 C语言基础 · 1.11 程序运行环境与调试',
  '2.2': '第二章 数据结构 · 2.2 线性表',
  '2.5': '第二章 数据结构 · 2.5 树和二叉树',
  '2.6': '第二章 数据结构 · 2.6 图',
  '2.8': '第二章 数据结构 · 2.8 排序',
  '3.0': '第三章 程序设计与算法 · 3.0 改错题专项',
};

let changed = 0, skipped = 0;
const files = readdirSync(DIR).filter(f => /^audit-/.test(f) && f.endsWith('.md'));

for (const f of files) {
  const fp = join(DIR, f);
  const content = readFileSync(fp, 'utf8');

  // 已含 chapter_id 跳过
  if (/^chapter_id:/m.test(content.split('\n').slice(0, 15).join('\n'))) {
    skipped++;
    continue;
  }

  // 从 title 提章节号
  const titleMatch = content.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  if (!titleMatch) continue;
  const chapMatch = titleMatch[1].match(/(\d+\.\d+)/);
  if (!chapMatch) continue;
  const cid = chapMatch[1];
  const cname = CHAPTER_NAMES[cid];
  if (!cname) {
    console.log(`? ${f}: chapter_id=${cid} 无预设中文名, 跳过`);
    continue;
  }

  // 插入到 fm 中（category 字段之后）
  const fmEndMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
  if (!fmEndMatch) continue;

  const fmBody = fmEndMatch[1];
  const newFmBody = fmBody + `\nchapter: "${cname}"\nchapter_id: "${cid}"`;
  const newContent = content.replace(fmEndMatch[0], `---\n${newFmBody}\n---\n`);

  writeFileSync(fp, newContent, 'utf8');
  changed++;
  console.log(`✓ ${f}: + chapter_id=${cid}`);
}

console.log(`\n已改 ${changed} 个 audit, 跳过 ${skipped} 个`);
