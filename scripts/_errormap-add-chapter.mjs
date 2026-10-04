#!/usr/bin/env node
// 给 易错点地图.json 的每个 cat 加 chapter / chapter_id 字段
// 让笔记库 frontmatter 的 chapter 字段能 join errormap

import {readFileSync, writeFileSync} from 'node:fs';

const PATH = '备考计划/易错点地图.json';

const CHAPTER_MAP = {
  // subject: 'computer' or 'math'
  limit:  {chapter_id: '1',  chapter_name: '第一章 函数、极限与连续',         subject: 'math'},
  semi:   {chapter_id: '1',  chapter_name: '第一章 C语言基础',                 subject: 'computer'},
  sym:    {chapter_id: '1',  chapter_name: '第一章 C语言基础',                 subject: 'computer'},
  eval:   {chapter_id: '1',  chapter_name: '第一章 C语言基础',                 subject: 'computer'},
  branch: {chapter_id: '1.4', chapter_name: '第一章 C语言基础 · 1.4 选择结构', subject: 'computer'},
  loop:   {chapter_id: '1.5', chapter_name: '第一章 C语言基础 · 1.5 循环结构', subject: 'computer'},
  arr:    {chapter_id: '1.7', chapter_name: '第一章 C语言基础 · 1.7 数组',     subject: 'computer'},
  io:     {chapter_id: '1.9', chapter_name: '第一章 C语言基础 · 1.9 输入输出', subject: 'computer'},
  disc:   {chapter_id: '1',  chapter_name: '第一章 C语言基础',                 subject: 'computer'},
};

const raw = readFileSync(PATH, 'utf8');
const data = JSON.parse(raw);
let added = 0;
for (const cat of data.cats) {
  const m = CHAPTER_MAP[cat.id];
  if (m && !cat.chapter) {
    cat.chapter = m.chapter_name;
    cat.chapter_id = m.chapter_id;
    cat.subject = m.subject;
    added++;
  }
}
data.schema = Math.max(data.schema || 1, 2);  // 升 schema=2 表示加字段
data.mergedWithNotesRepo = true;
data.mergedAt = new Date().toISOString().slice(0, 10);

writeFileSync(PATH, JSON.stringify(data, null, 2) + '\n', 'utf8');
console.log(`已写入 ${added} 个 cat 的 chapter 字段`);
console.log(`schema 升到 ${data.schema}`);
