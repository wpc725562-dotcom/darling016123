#!/usr/bin/env node
// 给 4 学科笔记批量补全 frontmatter
// 用法：node scripts/_fill-frontmatter.mjs [--apply]
//       dry-run 默认（只打印计划，不写文件）

import {readFileSync, writeFileSync, readdirSync} from 'node:fs';
import {join, basename} from 'node:path';

const APPLY = process.argv.includes('--apply');

const SUBJECTS = {
  math:     {root: 'docs/posts/math/notes',     category: 'math-note'},
  computer: {root: 'docs/posts/computer/notes', category: 'computer-note'},
  politics: {root: 'docs/posts/politics/notes', category: 'politics-note'},
  english:  {root: 'docs/posts/english/notes',  category: 'english-note'},
};

// 第一章 / 第二章 ... 学科章节归一
const CHAPTER_BY_SUBJECT = {
  math: {
    '1': '第一章 函数、极限与连续',
    '2': '第二章 导数与微分',
    '3': '第三章 一元函数积分学',
    '4': '第四章 向量代数与空间解析几何',
    '5': '第五章 多元函数微分学',
    '6': '第六章 多元函数积分学',
    '7': '第七章 无穷级数',
    '8': '第八章 常微分方程',
  },
  computer: {
    '1': '第一章 C语言基础',
    '2': '第二章 数据结构',
    '3': '第三章 程序设计与算法',
  },
  politics: {
    '01': '总论',
    '02': '毛泽东思想',
    '03': '新民主主义革命理论',
    '04': '社会主义改造理论',
    '05': '社会主义建设道路初步探索',
    '06': '邓小平理论',
    '07': '"三个代表"重要思想',
    '08': '科学发展观',
    '09': '习近平新时代中国特色社会主义思想',
    '10': '新发展理念',
    '11': '全面深化改革',
    '12': '改革发展与五位一体',
    '13': '全面依法治国',
    '14': '全面从严治党',
    '15': '总体国家安全观',
    '16': '人类命运共同体',
    '17': '辨析论述材料题模板',
    '18': '必背金句与名词',
  },
};

// 计算机 part 归一
const COMPUTER_PART = {
  '1': 'C语言',
  '2': '数据结构',
  '3': '程序设计与算法',
};

// 从文件名推断难度
function inferDifficulty(name) {
  if (/零基础|入门|通俗|大白话|初学/i.test(name)) return 'basic';
  if (/拔高|综合|提升|竞赛|压轴|难点|陷阱/i.test(name)) return 'advanced';
  return 'intermediate';
}

// 从文件名推断频次
function inferFrequency(name) {
  if (/高频|核心|重点|常考|大题/i.test(name)) return 'high';
  if (/低频|冷门|选学/i.test(name)) return 'low';
  return 'medium';
}

// 提取章节号
function chapterKey(name, subject) {
  // math/computer 用 1.X 风格；politics 用 01-X 风格
  const m1 = name.match(/^(\d+)\./);          // 1.X
  const m2 = name.match(/^(\d{2})-/);          // 01-X
  return m1 ? m1[1] : (m2 ? m2[1] : null);
}

// 提取关键名词做 tags
function inferTags(name, content) {
  const tags = [];
  const title = name.replace(/\.md$/, '');
  // 显式标记的关键词
  if (/零基础/.test(title)) tags.push('零基础');
  if (/抓大头/.test(title)) tags.push('抓大头');
  if (/易错|陷阱/.test(title)) tags.push('易错');
  if (/模板|答题|套路/.test(title)) tags.push('答题模板');
  if (/真题/.test(title)) tags.push('真题');
  if (/手把手|演练|例题/.test(title)) tags.push('演练');
  if (/大纲|考纲/.test(title)) tags.push('考纲');
  // 从正文第一句/标题提取主题词
  const fmMatch = content.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  if (fmMatch) {
    const t = fmMatch[1];
    const core = t.match(/[一-龥]{2,}/g)?.slice(0, 3) || [];
    for (const c of core) {
      if (c && !tags.includes(c) && c.length >= 2) tags.push(c);
    }
  }
  return tags.slice(0, 6);  // 限 6 个
}

// 解析已有 fm（兼容 CRLF / LF）
function parseFrontmatter(content) {
  const m = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  if (!m) return {fm: null, body: content};
  return {fm: m[1], body: m[2], raw: m[0]};
}

// 序列化 fm（保留顺序，新字段追加）
function serializeFm(obj) {
  const lines = [];
  for (const [k, v] of Object.entries(obj)) {
    if (Array.isArray(v)) {
      lines.push(`${k}:`);
      for (const item of v) lines.push(`  - ${item}`);
    } else {
      lines.push(`${k}: "${v}"`);
    }
  }
  return lines.join('\n') + '\n';
}

// 解析现有 fm 为 object（保留原序）
function fmToObj(fm) {
  const lines = fm.split('\n');
  const obj = {};
  let currentArrayKey = null;
  for (const line of lines) {
    if (/^(\w+):\s*$/.test(line)) {
      const k = line.match(/^(\w+):/)[1];
      obj[k] = [];
      currentArrayKey = k;
    } else if (/^(\w+):\s*["']?(.+?)["']?\s*$/.test(line)) {
      const m = line.match(/^(\w+):\s*["']?(.+?)["']?\s*$/);
      obj[m[1]] = m[2];
      currentArrayKey = null;
    } else if (/^\s+-\s+(.+?)\s*$/.test(line)) {
      if (currentArrayKey) obj[currentArrayKey].push(line.match(/^\s+-\s+(.+?)\s*$/)[1]);
    }
  }
  return obj;
}

function processFile(filepath, subject) {
  const content = readFileSync(filepath, 'utf8');
  const parsed = parseFrontmatter(content);
  const name = basename(filepath);

  if (!parsed.fm) {
    return {filepath, status: 'skip-no-fm', reason: '文件无 frontmatter'};
  }

  const obj = fmToObj(parsed.fm);
  const addedKeys = [];

  // category 必填（若缺）
  if (!obj.category) {
    obj.category = SUBJECTS[subject].category;
    addedKeys.push('category');
  }

  // chapter
  if (!obj.chapter) {
    const key = chapterKey(name, subject);
    if (key && CHAPTER_BY_SUBJECT[subject]?.[key]) {
      obj.chapter = CHAPTER_BY_SUBJECT[subject][key];
      addedKeys.push('chapter');
    } else if (subject === 'politics' && CHAPTER_BY_SUBJECT.politics[key]) {
      obj.chapter = CHAPTER_BY_SUBJECT.politics[key];
      addedKeys.push('chapter');
    } else if (subject === 'math' && key) {
      obj.chapter = `第 ${key} 章`;
      addedKeys.push('chapter');
    }
  }

  // part（仅 computer）
  if (subject === 'computer' && !obj.part) {
    const key = chapterKey(name, subject);
    if (COMPUTER_PART[key]) {
      obj.part = COMPUTER_PART[key];
      addedKeys.push('part');
    }
  }

  // difficulty
  if (!obj.difficulty) {
    obj.difficulty = inferDifficulty(name);
    addedKeys.push('difficulty');
  }

  // frequency
  if (!obj.frequency) {
    obj.frequency = inferFrequency(name);
    addedKeys.push('frequency');
  }

  // mastery
  if (!obj.mastery) {
    obj.mastery = 'review';
    addedKeys.push('mastery');
  }

  // tags
  if (!obj.tags || (Array.isArray(obj.tags) && obj.tags.length === 0)) {
    const t = inferTags(name, content);
    if (t.length > 0) {
      obj.tags = t;
      addedKeys.push('tags');
    }
  }

  if (addedKeys.length === 0) {
    return {filepath, status: 'skip-complete', reason: 'fm 完整'};
  }

  const newFm = serializeFm(obj);
  const newContent = `---\n${newFm}---\n${parsed.body}`;
  return {filepath, status: 'update', addedKeys, newContent};
}

function main() {
  let totalFiles = 0, skippedNoFm = 0, skippedComplete = 0, willUpdate = 0;
  const updates = [];

  for (const [subject, cfg] of Object.entries(SUBJECTS)) {
    const dir = cfg.root;
    const files = readdirSync(dir).filter(f => f.endsWith('.md'));
    for (const f of files) {
      totalFiles++;
      const filepath = join(dir, f);
      const r = processFile(filepath, subject);
      if (r.status === 'skip-no-fm') skippedNoFm++;
      else if (r.status === 'skip-complete') skippedComplete++;
      else { willUpdate++; updates.push({...r, subject}); }
    }
  }

  console.log(`=== frontmatter 补全计划 ===`);
  console.log(`学科：math / computer / politics / english`);
  console.log(`扫描：${totalFiles} 篇笔记`);
  console.log(`跳过：无 fm 文件 ${skippedNoFm}`);
  console.log(`跳过：fm 已完整 ${skippedComplete}`);
  console.log(`将更新：${willUpdate} 篇\n`);

  // 按学科分组打印
  for (const sub of ['math', 'computer', 'politics', 'english']) {
    const subUpdates = updates.filter(u => u.subject === sub);
    if (subUpdates.length === 0) continue;
    console.log(`--- ${sub}（${subUpdates.length} 篇）---`);
    for (const u of subUpdates.slice(0, 8)) {
      const name = basename(u.filepath);
      console.log(`  ${name}`);
      console.log(`    新增：${u.addedKeys.join(', ')}`);
    }
    if (subUpdates.length > 8) {
      console.log(`  ... 剩余 ${subUpdates.length - 8} 篇`);
    }
    console.log();
  }

  if (APPLY) {
    console.log(`=== 应用更新 ===`);
    for (const u of updates) {
      writeFileSync(u.filepath, u.newContent, 'utf8');
      console.log(`✓ ${basename(u.filepath)}  +${u.addedKeys.join(',+')}`);
    }
    console.log(`\n已写入 ${updates.length} 个文件`);
  } else {
    console.log(`提示：传 --apply 才真正写文件`);
  }
}

main();
