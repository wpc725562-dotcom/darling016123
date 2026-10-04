#!/usr/bin/env node
// 把 branch/loop/arr 三 cat 从 chapter_id='1.4'/'1.5'/'1.7' 改回 '1'
// 让它们走父子匹配聚合到「C语言基础」父章节下

import {readFileSync, writeFileSync} from 'node:fs';

const PATH = '备考计划/易错点地图.json';
const TARGETS = {
  branch: { from: '1.4', to: '1', chapter_name: '第一章 C语言基础 · 分支（if/switch）' },
  loop:   { from: '1.5', to: '1', chapter_name: '第一章 C语言基础 · 循环' },
  arr:    { from: '1.7', to: '1', chapter_name: '第一章 C语言基础 · 数组' },
};

const raw = readFileSync(PATH, 'utf8');
const data = JSON.parse(raw);
let changed = 0;

for (const cat of data.cats) {
  if (TARGETS[cat.id] && cat.chapter_id === TARGETS[cat.id].from) {
    cat.chapter_id = TARGETS[cat.id].to;
    cat.chapter = TARGETS[cat.id].chapter_name;
    changed++;
    console.log(`✓ ${cat.id}: ${TARGETS[cat.id].from} → ${TARGETS[cat.id].to}（${TARGETS[cat.id].chapter_name}）`);
  }
}

data.updatedAt = new Date().toISOString().slice(0, 10);
writeFileSync(PATH, JSON.stringify(data, null, 2) + '\n', 'utf8');
console.log(`\n已改 ${changed} 个 cat，schema 不动`);
