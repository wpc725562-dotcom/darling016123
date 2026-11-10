#!/usr/bin/env node
/**
 * 讲课/验收配比审计：「讲了 N 节，零验收」的章有哪些
 *
 * 为什么需要这个：
 *   2026-10-19 查日志发现 `C语言 1.7 函数` 讲了 4 节课，**一条 quiz 都没有**，
 *   4 条记录全是 `lecture` + `partial`。而它是「数据结构后置」的前置条件之一
 *   （见 `备考计划/网页AI开课包/1-C语言-状态卡.md`：1.7/1.8/1.9 都过跨日复检才开数据结构）。
 *   结果是：数据结构一直开不了，但看板上只显示「数据结构 0%」，看不出真正卡在哪。
 *
 *   `1.8 指针` 也踩过同一个坑 —— 日志里有一条
 *   「首次实战（四轮做题 · 此前 7 课零练习）· 🔴 查出 3 个」。
 *   ⇒ 这不是偶发，是流程病：**讲完不验，等后面一次性补，补出来的洞更大。**
 *
 * 判据：
 *   lecture >= 4 且 quiz == 0  ⇒ 红灯（该验了，而且欠了很多）
 *   lecture >= 2 且 quiz == 0  ⇒ 黄灯（留意）
 *
 * 只统计 C 语言章号（1.1–1.11）与数据结构章号（2.1–2.9）。
 * 1.9 章内部的小节号是 3.x（笔记 3.1–3.11），**不当作独立模块**，避免误判。
 *
 * 用法：node scripts/audit-lecture-quiz.mjs [--json]
 * 退出码：0 = 无红灯；1 = 有红灯（说明存在讲了 4 节以上却零验收的章）
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const LOG = path.join(__dirname, '..', '备考计划', '学习日志.jsonl');

/**
 * 合法章号白名单。用精确匹配，不靠正则猜。
 * `3.1`–`3.11` 是 `1.9 结构体` 章内部的小节号（见 `docs/posts/computer/notes/1.9-结构体与共用体.md`
 * 的 3.1–3.11），日志里常直接写「3.8 结构体内存」，所以要映射回 1.9，
 * 否则 1.9 的讲课记录会全部变成「无法归类」，看板显示 0 讲课 —— 第一次跑就是这样漏了 76 条。
 */
const CHAPTERS = [
  ...Array.from({ length: 11 }, (_, i) => `1.${i + 1}`), // C 语言 1.1–1.11
  ...Array.from({ length: 9 }, (_, i) => `2.${i + 1}`), // 数据结构 2.1–2.9
];

/** 章内小节号 → 所属章号 */
const SECTION_ALIAS = Object.fromEntries(
  Array.from({ length: 11 }, (_, i) => [`3.${i + 1}`, '1.9'])
);

const RED_LECTURES = 4;
const YELLOW_LECTURES = 2;

function chapterOf(title) {
  const t = title || '';
  const all = [...CHAPTERS, ...Object.keys(SECTION_ALIAS)];
  // 按长度降序匹配，保证 1.10 / 1.11 不会被 1.1 抢走
  const sorted = all.sort((a, b) => b.length - a.length);
  for (const ch of sorted) {
    // 章号前后不能紧跟数字，避免 1.1 命中 1.10
    const re = new RegExp(`(?<![\\d.])${ch.replace('.', '\\.')}(?![\\d])`);
    if (re.test(t)) return SECTION_ALIAS[ch] || ch;
  }
  return null;
}

function main() {
  const asJson = process.argv.includes('--json');
  if (!fs.existsSync(LOG)) {
    console.error(`找不到学习日志：${LOG}`);
    process.exit(1);
  }

  const rows = fs
    .readFileSync(LOG, 'utf8')
    .split('\n')
    .filter(Boolean)
    .map((l) => {
      try {
        return JSON.parse(l);
      } catch {
        return null;
      }
    })
    .filter(Boolean);

  const byCh = new Map();
  let unmatched = 0;

  for (const r of rows) {
    if (!['lecture', 'quiz'].includes(r.kind)) continue;
    const ch = chapterOf(r.title);
    if (!ch) {
      unmatched++;
      continue;
    }
    const cur = byCh.get(ch) || { lecture: 0, quiz: 0, lastLecture: '', lastQuiz: '', passed: 0 };
    if (r.kind === 'lecture') {
      cur.lecture++;
      if (r.date > cur.lastLecture) cur.lastLecture = r.date;
    } else {
      cur.quiz++;
      if (r.mastery === 'passed') cur.passed++;
      if (r.date > cur.lastQuiz) cur.lastQuiz = r.date;
    }
    byCh.set(ch, cur);
  }

  const report = [...byCh.entries()]
    .map(([ch, v]) => ({
      chapter: ch,
      ...v,
      level: v.lecture >= RED_LECTURES && v.quiz === 0 ? 'red' : v.lecture >= YELLOW_LECTURES && v.quiz === 0 ? 'yellow' : 'ok',
    }))
    .sort((a, b) => {
      const rank = { red: 0, yellow: 1, ok: 2 };
      return rank[a.level] - rank[b.level] || a.chapter.localeCompare(b.chapter, 'zh', { numeric: true });
    });

  const reds = report.filter((r) => r.level === 'red');
  const yellows = report.filter((r) => r.level === 'yellow');

  if (asJson) {
    console.log(JSON.stringify({ reds, yellows, report, unmatched }, null, 2));
    process.exit(reds.length ? 1 : 0);
  }

  console.log('=== 讲课 / 验收配比审计 ===');
  console.log(`数据源：${path.relative(path.join(__dirname, '..'), LOG)}`);
  console.log(`判据：讲满 ${RED_LECTURES} 节仍零验收 = 🔴；讲满 ${YELLOW_LECTURES} 节零验收 = 🟡\n`);

  console.log('章 | 讲课 | 验收 | 验收通过 | 最近讲课 | 最近验收 | 状态');
  console.log(':---|:---:|:---:|:---:|:---|:---|:---');
  for (const r of report) {
    const flag = r.level === 'red' ? '🔴 该验了' : r.level === 'yellow' ? '🟡 留意' : '✅';
    console.log(
      `${r.chapter} | ${r.lecture} | ${r.quiz} | ${r.passed} | ${r.lastLecture || '-'} | ${r.lastQuiz || '-'} | ${flag}`
    );
  }

  if (reds.length) {
    console.log(`\n🔴 ${reds.length} 个章「讲了很多但一次没验」：${reds.map((r) => r.chapter).join('、')}`);
    console.log('   这些章在进度看板上只会显示「进行中」，看不出真实风险 —— 讲了不等于会。');
  }
  if (yellows.length) {
    console.log(`🟡 ${yellows.length} 个章刚开始讲、还没验：${yellows.map((r) => r.chapter).join('、')}`);
  }
  if (unmatched) {
    console.log(
      `\nℹ️ 有 ${unmatched} 条 lecture/quiz 记录没写章号、未计入 —— ` +
        `多为 2026-09-24 之前的早期记录（当时还没按「C语言 1.x」命名），以及高数/英语/政治的记录。`
    );
    console.log('   本脚本只审「标题里写了计算机章号」的记录，所以早期历史课的配比看不到。');
  }
  if (!reds.length) console.log('\n✅ 没有「讲了 4 节以上却零验收」的章。');

  process.exit(reds.length ? 1 : 0);
}

main();
