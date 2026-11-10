#!/usr/bin/env node
/**
 * sync-daily-cards.mjs
 * ------------------------------------------------------------------
 * 把「复检排程-总表.md」的反向视图（每天要复检的清单）灌进 176 张日卡。
 *
 * 三仓库研究的落地对应：
 *   · DeepTutor         → scheduled repetition：知识点按 1/3/7/14/30/60 天回归
 *   · good-learning-skill → 每日课程固定结构：例题 → 变式 → 混合练习
 *   · Study-Mate        → 可运行证据核验：状态落文件、可继承、可核对
 *
 * 每张日卡新增两节（用 HTML 注释做标记，脚本可重复运行、幂等）：
 *   <!-- REVIEW-DUE -->  🔁 复检今天到期   （插在「今日配额」之前 —— 先做这个）
 *   <!-- DAY-CLOSE -->   🧭 本日收口       （插在「今日自查」之前）
 *
 * 原始日卡先整目录备份到 每日/.backup-<日期>/，只改副本。
 * 运行：node scripts/sync-daily-cards.mjs
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..');
const DAILY_DIR = path.join(ROOT, '每日');
const SCHEDULE = path.join(ROOT, '复检排程-总表.md');
const BACKUP_DIR = path.join(DAILY_DIR, '.backup-' + new Date().toISOString().slice(0, 10));

const EOL = '\r\n';
const M_DUE_S = '<!-- REVIEW-DUE:START -->';
const M_DUE_E = '<!-- REVIEW-DUE:END -->';
const M_CLOSE_S = '<!-- DAY-CLOSE:START -->';
const M_CLOSE_E = '<!-- DAY-CLOSE:END -->';

/* ---------- 1. 解析反向视图 ---------- */

function parseReverseView(md) {
  const out = new Map(); // dayNum -> [{from, prio, topic}]
  const lines = md.split(/\r?\n/);
  let inReverse = false;
  for (const line of lines) {
    if (/^##\s*每天要复检的清单/.test(line)) { inReverse = true; continue; }
    if (inReverse && /^##\s/.test(line)) { inReverse = false; continue; }
    if (!inReverse) continue;

    const m = line.match(/^-\s*\*\*D(\d{3})\*\*\s*→\s*(.+)$/);
    if (!m) continue;
    const day = Number(m[1]);
    const items = m[2]
      .split('　｜　')
      .map((s) => s.trim())
      .filter(Boolean)
      .map((piece) => {
        const p = piece.match(/^D(\d{3})（(P\d)）([\s\S]+)$/);
        if (!p) return null;
        return { from: Number(p[1]), prio: p[2], topic: p[3].trim() };
      })
      .filter(Boolean);
    out.set(day, items);
  }
  return out;
}

/* ---------- 2. 生成两节 ---------- */

const PRIO_RANK = { P0: 0, P1: 1, P2: 2, P3: 3 };

function sectionDue(day, items) {
  const head = [
    M_DUE_S,
    '## 🔁 复检今天到期（先做这个，再学新内容）',
    '',
  ];

  if (!items.length) {
    return [
      ...head,
      '> 今天**没有**到期的复检 —— 第 1 天，还没有可回归的条目。',
      '> 从 D002 起，每天都会有条目按 **1 / 3 / 7 / 14 / 30 / 60 天** 的间隔回来。',
      '> 复检形式固定：**同型题 + 换数字 + 要求说出理由**。',
      M_DUE_E,
      '',
    ];
  }

  const sorted = [...items].sort(
    (a, b) => PRIO_RANK[a.prio] - PRIO_RANK[b.prio] || a.from - b.from,
  );

  const rows = sorted.map(
    (it) => `| D${String(it.from).padStart(3, '0')} | ${it.prio} | ${it.topic} | [ ] | [ ] |`,
  );

  const heavy = items.length > 4;

  return [
    ...head,
    '> 知识点的**回归**：学过的条目按 **1 / 3 / 7 / 14 / 30 / 60 天** 间隔回来重考。',
    '> 形式固定：**同型题 + 换数字 + 要求说出理由**（《自学习法》§1③ 三条反作弊探针）。',
    '',
    '| 来自 | 优先 | 主题 | 过 | 没过 |',
    '|:--:|:--:|:--|:--:|:--:|',
    ...rows,
    '',
    `**今天共 ${items.length} 条。** 过 → \`计划总表-v2.csv\` 状态列标 🟢；没过 → 标 🔴，**明天再排一次**。`,
    heavy
      ? '> ⚠️ 超过 4 条：先做 **P0/P1**，P2/P3 可顺延（顺延不超过 3 天）。'
      : '> 做完再开新内容 —— 复检排在学新东西之前，这是这套系统里唯一不能挪的一步。',
    M_DUE_E,
    '',
  ];
}

function sectionClose(day, items) {
  const n = items.length;
  const first = n
    ? `- [ ] 复检到期的 **${n}** 条全部走完（过 → 🟢 ／ 没过 → 🔴 明天重排）`
    : '- [ ] 今天无复检到期（第 1 天）—— 直接开始新内容';

  return [
    M_CLOSE_S,
    '## 🧭 本日收口（睡前 1 分钟）',
    '',
    first,
    '- [ ] 今日复盘条目自己标一次状态：⬜ 未开始 · 🟡 待复检 · 🟢 已过关 · 🔵 已稳固 · 🔴 复检未过',
    '- [ ] **推进日**：块 A（计算机）或块 B（高数）**完成任一** → ✔ ｜ 都没完成 → ✘',
    '      —— 这是唯一的第一性指标（目标 50%，实测 23%），比「学了几个小时」重要得多',
    M_CLOSE_E,
    '',
  ];
}

/* ---------- 3. 读写 ---------- */

function stripMarked(lines, start, end) {
  const a = lines.indexOf(start);
  if (a === -1) return lines;
  const b = lines.indexOf(end, a);
  if (b === -1) return lines;
  // 连同后面紧跟的空行一起删
  let tail = b + 1;
  while (tail < lines.length && lines[tail] === '') tail++;
  return [...lines.slice(0, a), ...lines.slice(tail)];
}

function insertBefore(lines, predicate, block) {
  const i = lines.findIndex(predicate);
  if (i === -1) throw new Error('找不到插入锚点');
  return [...lines.slice(0, i), ...block, ...lines.slice(i)];
}

function syncCard(file, items) {
  const raw = fs.readFileSync(file, 'utf8');
  const day = Number(path.basename(file).match(/^D(\d{3})/)[1]);

  let lines = raw.split(EOL);
  if (lines.length === 1) lines = raw.split('\n'); // 容错：万一不是 CRLF

  lines = stripMarked(lines, M_DUE_S, M_DUE_E);
  lines = stripMarked(lines, M_CLOSE_S, M_CLOSE_E);

  lines = insertBefore(lines, (l) => l.startsWith('## ⏱ 今日配额'), sectionDue(day, items));
  lines = insertBefore(lines, (l) => l.startsWith('## 🔍 今日自查'), sectionClose(day, items));

  const next = lines.join(EOL);
  const changed = next !== raw;
  if (changed) fs.writeFileSync(file, next, 'utf8');
  return { day, count: items.length, changed };
}

/* ---------- main ---------- */

const md = fs.readFileSync(SCHEDULE, 'utf8');
const reverse = parseReverseView(md);
if (reverse.size === 0) {
  console.error('[fail] 没能从 复检排程-总表.md 解析出反向视图');
  process.exit(1);
}

// 备份（只备份一次，已存在就跳过）
if (!fs.existsSync(BACKUP_DIR)) {
  fs.mkdirSync(BACKUP_DIR, { recursive: true });
  for (const f of fs.readdirSync(DAILY_DIR)) {
    if (f.endsWith('.md')) fs.copyFileSync(path.join(DAILY_DIR, f), path.join(BACKUP_DIR, f));
  }
  console.log(`[ok] 已备份原日卡 → ${path.relative(ROOT, BACKUP_DIR)}/`);
} else {
  console.log(`[--] 备份目录已存在，跳过备份 → ${path.relative(ROOT, BACKUP_DIR)}/`);
}

const files = fs
  .readdirSync(DAILY_DIR)
  .filter((f) => /^D\d{3}-.*\.md$/.test(f))
  .sort();

let totalItems = 0;
let changed = 0;
let maxDay = 0;
let maxCount = 0;
const emptyDays = [];

for (const f of files) {
  const day = Number(f.match(/^D(\d{3})/)[1]);
  const items = reverse.get(day) ?? [];
  const r = syncCard(path.join(DAILY_DIR, f), items);
  if (r.changed) changed++;
  totalItems += items.length;
  if (items.length > maxCount) { maxCount = items.length; maxDay = day; }
  if (!items.length) emptyDays.push(day);
}

console.log(`[ok] 日卡同步        : ${files.length} 张，写入 ${changed} 张`);
console.log(`[ok] 反向视图覆盖    : ${reverse.size} 天有到期条目`);
console.log(`[ok] 复检条目总数    : ${totalItems} 条（平均 ${(totalItems / files.length).toFixed(1)} 条/天）`);
console.log(`[ok] 单日最多        : D${String(maxDay).padStart(3, '0')} → ${maxCount} 条`);
console.log(`[ok] 无到期日        : ${emptyDays.length ? emptyDays.map((d) => 'D' + String(d).padStart(3, '0')).join(' ') : '无'}`);
