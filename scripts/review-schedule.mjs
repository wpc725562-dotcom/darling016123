#!/usr/bin/env node
/**
 * 复检调度：算出「今天该复检什么」。
 *
 * 为什么会有它：2026-10-14 的数据诊断发现 —— 输入端很足（听课 39 / 做题 70），
 * 但巩固端是空的（建卡仅 5 次 / 复检执行 0）。根因之一是**复检队列只写「约 XX 到期」，
 * 没有任何东西负责算「今天到底哪几条到期」**，于是队列一路过期（最老 27 天）。
 *
 * 本脚本把「约 XX 到期」变成「今天就是到期日」。
 * 规则依据：备考计划/记忆巩固机制.md（R2 / R3 / R4）
 *
 * 用法：
 *   node scripts/review-schedule.mjs              # 按今天算
 *   node scripts/review-schedule.mjs 2026-10-15   # 指定日期（补算 / 预排）
 *   node scripts/review-schedule.mjs --all        # 额外打印全部节点（调试用）
 *
 * 退出码：0 = 今天无到期；1 = 有到期（方便在开课前做硬卡点）
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..');

// ── 默认配置（必须与 记忆巩固机制.md §4 一致）────────────
// 改默认值请同步改文档，否则两边会漂移。
const DEFAULTS = {
  reviewNodes: [1, 3, 7, 30],
  lecturesPerDaySoftCap: 4,
  lecturesPerDayAfterFailedReview: 2,
  cardBindingRequired: true,
  maxNewCardsPerDay: 20,
  minCardsPerConcept: 1,
  minCardsPerMistake: 1,
  queueClearFirst: true,
  crossDayRequired: true,
  weeklyReciteDay: 'sunday',
  fatigueWindow: ['00:00', '06:00'],
  maxQueuePerDay: 5,
};

const cfgFile = path.join(ROOT, '备考计划', '记忆巩固.config.json');
let cfg = DEFAULTS;
if (fs.existsSync(cfgFile)) {
  try {
    cfg = { ...DEFAULTS, ...JSON.parse(fs.readFileSync(cfgFile, 'utf8')) };
  } catch (e) {
    console.error('配置文件解析失败，改用默认值: ' + e.message);
  }
}

const logFile = path.join(ROOT, '备考计划', '学习日志.jsonl');
if (!fs.existsSync(logFile)) {
  console.error('找不到学习日志: ' + logFile);
  process.exit(1);
}

// ── 日期工具（一律按本地日期，避免 UTC 偏移把到期日算错一天）──
const pad = (n) => String(n).padStart(2, '0');
const fmt = (d) => d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
const addDays = (dateStr, n) => {
  const d = new Date(dateStr + 'T00:00:00');
  d.setDate(d.getDate() + n);
  return fmt(d);
};
const daysBetween = (a, b) =>
  Math.round((new Date(b + 'T00:00:00') - new Date(a + 'T00:00:00')) / 86400000);

const args = process.argv.slice(2);
const showAll = args.includes('--all');
const dateArg = args.find((a) => /^\d{4}-\d{2}-\d{2}$/.test(a));
const today = dateArg || fmt(new Date());

// ── 读日志，只取「新学」记录 ───────────────────────────
// 为什么只取 lecture：quiz 是「做题」，复检任务由 lecture（新知识点）派生；
// 错题另有错题本管理，不在这里重复排期。
const entries = [];
for (const line of fs.readFileSync(logFile, 'utf8').split('\n')) {
  if (!line.trim()) continue;
  let o;
  try { o = JSON.parse(line); } catch { continue; }
  if (!o.date || !o.subject || !o.title) continue;
  if (o.type) continue;                       // 遥测事件
  if (o.kind !== 'lecture') continue;         // 只排「新学」
  if (o.subject === '工具') continue;         // 工具不算学习量（手册禁止项）
  entries.push(o);
}

// ── 知识点关键词：用来判断「这条后来有没有被复检过」──────
// 启发式，不求精确：先抓「1.8 / 2.5」这类编号，抓不到就退化成标题前 6 字。
const keywordOf = (title) => {
  const m = title.match(/\d+\.\d+/);
  if (m) return m[0];
  return title.slice(0, 6);
};

// ── 生成节点任务 ─────────────────────────────────────
const tasks = [];
for (const e of entries) {
  const kw = keywordOf(e.title);
  for (const n of cfg.reviewNodes) {
    const due = addDays(e.date, n);
    // 启发式判定「已复检」：到期日之后，同科目有记录且标题命中同一关键词
    const cleared = entries.some(
      (x) => x.subject === e.subject && x.date > e.date && keywordOf(x.title) === kw
    );
    tasks.push({
      subject: e.subject,
      title: e.title,
      kw,
      learnedOn: e.date,
      node: n,
      due,
      cleared,
    });
  }
}

const dueToday = tasks.filter((t) => t.due === today && !t.cleared);
const overdue = tasks
  .filter((t) => t.due < today && !t.cleared)
  .sort((a, b) => (a.due < b.due ? -1 : a.due > b.due ? 1 : 0));
const upcoming = tasks
  .filter((t) => t.due > today && !t.cleared)
  .sort((a, b) => (a.due < b.due ? -1 : 1))
  .slice(0, 12);

// ── 输出 ────────────────────────────────────────────
console.log('==== 复检调度 · ' + today + ' ====');
console.log('配置 reviewNodes=[' + cfg.reviewNodes.join(',') + '] · queueClearFirst=' +
  cfg.queueClearFirst + ' · 数据源 ' + entries.length + ' 条新学记录');

const line = (t) =>
  '  ' + ('D+' + t.node).padEnd(5) + ' ' + t.subject.padEnd(5) + ' ' +
  t.title.slice(0, 38).padEnd(40) + ' 学于 ' + t.learnedOn + '  到期 ' + t.due;

console.log('\n-- 🔴 今天到期（' + dueToday.length + ' 条）--');
if (!dueToday.length) console.log('  （无）');
else dueToday.forEach((t) => console.log(line(t)));

console.log('\n-- ⏰ 已过期未清（' + overdue.length + ' 条，按到期日升序，最老的排最前）--');
if (!overdue.length) console.log('  （无）');
else {
  const show = showAll ? overdue : overdue.slice(0, 12);
  show.forEach((t) =>
    console.log(line(t) + '  [过期 ' + daysBetween(t.due, today) + ' 天]')
  );
  if (!showAll && overdue.length > show.length)
    console.log('  …… 还有 ' + (overdue.length - show.length) + ' 条（--all 看全）');
}

console.log('\n-- 📅 即将到期（7 天内，最多 12 条）--');
const soon = upcoming.filter((t) => daysBetween(today, t.due) <= 7);
if (!soon.length) console.log('  （无）');
else soon.forEach((t) => console.log(line(t) + '  [还有 ' + daysBetween(today, t.due) + ' 天]'));

console.log('\n▶ 下一步（R4）：先把「今天到期」+「已过期」清完，再开新课。');
console.log('  清队列上限 ' + cfg.maxQueuePerDay + ' 条/天；清不完的顺延，不跳过。');

process.exit(dueToday.length || overdue.length ? 1 : 0);
