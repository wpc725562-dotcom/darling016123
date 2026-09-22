#!/usr/bin/env node
/**
 * 校验 `备考计划/学习日志.jsonl` 的结构与科目名一致性。
 *
 * 为什么会有它：这份文件是**全项目的唯一学习事实源** —— 门户「🪞 复盘」页、
 * 「学习进度看板.md」的断档天数、每日计划的配额判定，全都读它。但它只是逐行 JSON，
 * 没有任何 schema 约束，于是长出过两类真实缺陷：
 *
 *   1. **坏行**：手写时漏了引号/逗号 → 消费者只能"跳过坏行"，数据静默变少。
 *   2. **科目名同义重复**：2026-09-19 那条高数记录写成了 `高等数学`，而其余四条写
 *      `高数` → 按科目统计时它被漏掉，导致 09-20 的每日计划**误判「高数断档 10 天」**
 *      （实际只断 1 天），优先级被排错。这类错误文件本身完全合法，不报错、看不见。
 *
 * 用法：node scripts/check-study-log.mjs [日志路径]
 *      默认 备考计划/学习日志.jsonl
 *      退出码 0 = 全过；1 = 有缺陷
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..');

const file = process.argv[2] || path.join(ROOT, '备考计划', '学习日志.jsonl');

// ── 允许的科目名（白名单）──────────────────────────────
// 新增科目时改这里；写错名字会被下面第 3 项检查抓出来。
const SUBJECTS = ['C语言', '高数', '英语', '政治', '数据结构', '计算机', '综合', '工具'];

// 常见别名 → 规范名。命中时给出可执行的修法提示。
const ALIASES = {
  高等数学: '高数',
  数学: '高数',
  高数上册: '高数',
  c语言: 'C语言',
  C: 'C语言',
  'C 语言': 'C语言',
  英文: '英语',
  计算机基础: '计算机',
};

// ── 允许的记录类型（白名单）──────────────────────────
// 2026-09-21 实查：文件里真实出现过的是 quiz / tool / lecture / anki / feedback。
// 第一版漏了 anki 和 feedback，被这个脚本自己抓出来了 —— 白名单要按实查写，不能凭印象。
const KINDS = ['quiz', 'lecture', 'tool', 'anki', 'feedback'];
const MASTERY = ['passed', 'partial', 'failed', 'na'];
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

if (!fs.existsSync(file)) {
  console.error('找不到文件: ' + file);
  process.exit(1);
}

const raw = fs.readFileSync(file, 'utf8');
const lines = raw.split('\n');
const problems = [];
const entries = [];

lines.forEach((line, i) => {
  const n = i + 1;
  if (!line.trim()) return;

  let o;
  try { o = JSON.parse(line); }
  catch (e) { problems.push('行' + n + ' JSON 解析失败: ' + e.message); return; }

  // 1. 必填字段
  for (const f of ['date', 'subject', 'kind', 'title']) {
    if (!o[f] || typeof o[f] !== 'string') problems.push('行' + n + ' 缺字段或类型不对: ' + f);
  }
  // 2. 日期格式
  if (o.date && !DATE_RE.test(o.date)) problems.push('行' + n + ' date 格式应为 YYYY-MM-DD，实际: ' + o.date);
  // 3. 科目名（关键检查 —— 抓同义重复）
  if (o.subject && !SUBJECTS.includes(o.subject)) {
    const fix = ALIASES[o.subject] ? '，应改为「' + ALIASES[o.subject] + '」' : '，不在白名单里';
    problems.push('行' + n + ' subject 异常: 「' + o.subject + '」' + fix);
  }
  // 4. 枚举值
  if (o.kind && !KINDS.includes(o.kind)) problems.push('行' + n + ' kind 异常: ' + o.kind);
  if (o.mastery && !MASTERY.includes(o.mastery)) problems.push('行' + n + ' mastery 异常: ' + o.mastery);

  entries.push(o);
});

// ── 输出 ────────────────────────────────────────────
console.log('==== ' + path.relative(ROOT, file) + ' ====');
console.log('总行数 ' + lines.filter(x => x.trim()).length + ' | 有效记录 ' + entries.length);

console.log('\n-- 各科目落账（按最近日期排序）--');
const bySub = {};
for (const e of entries) (bySub[e.subject] = bySub[e.subject] || []).push(e.date);
const rows = Object.entries(bySub).map(([s, ds]) => {
  const uniq = [...new Set(ds)].sort();
  return { s, count: ds.length, last: uniq[uniq.length - 1], days: uniq.length };
});
rows.sort((a, b) => (a.last < b.last ? 1 : a.last > b.last ? -1 : 0));

const latest = rows.reduce((m, r) => (r.last > m ? r.last : m), '');
for (const r of rows) {
  const gap = latest
    ? Math.round((new Date(latest) - new Date(r.last)) / 86400000)
    : 0;
  const flag = gap === 0 ? '  ' : gap >= 7 ? '  <== 断档 ' + gap + ' 天' : '  断 ' + gap + ' 天';
  console.log('  ' + r.s.padEnd(6) + ' ' + String(r.count).padStart(3) + ' 条 | 最近 ' + r.last + flag);
}

const never = SUBJECTS.filter(s => !bySub[s]);
if (never.length) console.log('\n  从未落账: ' + never.join(' / '));

console.log();
if (problems.length) {
  console.log('发现 ' + problems.length + ' 处问题:');
  for (const p of problems) console.log('  X ' + p);
  process.exit(1);
}
console.log('结构与科目名校验通过 OK');
