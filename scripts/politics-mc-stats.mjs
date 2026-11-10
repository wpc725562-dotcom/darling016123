#!/usr/bin/env node
/**
 * 政治理论真题 · 多项选择题答案项数分布统计
 *
 * 为什么要有这个脚本：
 *   笔记里长期写着「多选宁缺毋滥」。但专升本多选是**无部分分**规则
 *   （「未选、错选、多选或少选均无分」），此时「少选」= 0 分，
 *   「宁缺毋滥」未必是对的策略。要判断，必须先知道真实答案的项数分布。
 *
 * 口径（必须严格按章节切段，否则会数错）：
 *   只统计 `## 二、多项选择题` 到 `## 三、辨析题` 之间的 `答案：XX`。
 *   反例：2024.md 第 736 行起是「附 · 主观题答题模板（非题目）」区，
 *   里面的 `答案：ABCD` 是答题要点编号，不是多选答案。全文件正则会把它们
 *   误计成多选全选（实测会多出 5 个），所以不能偷懒用全文件 grep。
 *
 * 用法：
 *   node scripts/politics-mc-stats.mjs          # 人读
 *   node scripts/politics-mc-stats.mjs --json   # 机读
 *
 * 退出码：
 *   0 正常；1 某年提取到的题数不是 10（说明格式变了或切段失败，不能静默通过）
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const POSTS = path.join(__dirname, '..', 'docs', 'posts', 'politics');

/** 只收「一份卷子一个文件」的年份；2020-政治-刷题版 是 2020.md 的派生版，不重复计入 */
const YEARS = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026];
const EXPECT_PER_YEAR = 10;

const RE_MC_HEAD = /^#{2,3}\s*二、多项选择/m;
const RE_NEXT_HEAD = /^#{2,3}\s*三、辨析/m;
const RE_ANSWER = /答案\s*[:：]\s*\**\s*([A-D]{2,4})/g;

function extractMcAnswers(text) {
  const head = text.search(RE_MC_HEAD);
  if (head < 0) return null; // 没有多选章节
  let seg = text.slice(head);
  const nextRel = seg.slice(5).search(RE_NEXT_HEAD);
  if (nextRel > 0) seg = seg.slice(0, nextRel + 5);
  return [...seg.matchAll(RE_ANSWER)].map((m) => m[1]);
}

function main() {
  const asJson = process.argv.includes('--json');
  const dist = { 2: 0, 3: 0, 4: 0 };
  const perYear = [];
  const problems = [];
  let total = 0;

  for (const y of YEARS) {
    const f = path.join(POSTS, `${y}.md`);
    if (!fs.existsSync(f)) {
      problems.push(`${y}.md 不存在`);
      continue;
    }
    const answers = extractMcAnswers(fs.readFileSync(f, 'utf8'));
    if (answers === null) {
      problems.push(`${y}.md 找不到「## 二、多项选择题」标题`);
      continue;
    }
    if (answers.length !== EXPECT_PER_YEAR) {
      problems.push(
        `${y}.md 多选区提取到 ${answers.length} 个答案，预期 ${EXPECT_PER_YEAR} 个` +
          `（格式变了或切段失败，请人工核对）`
      );
    }
    const c = { 2: 0, 3: 0, 4: 0 };
    for (const a of answers) if (c[a.length] !== undefined) c[a.length]++;
    perYear.push({ year: y, n: answers.length, d2: c[2], d3: c[3], d4: c[4] });
    total += answers.length;
    for (const k of [2, 3, 4]) dist[k] += c[k];
  }

  const pct = (x) => (total ? ((x / total) * 100).toFixed(1) + '%' : '-');

  // 期望命中率：已确定 k 项正确、其余不确定时，两种策略的得分概率
  //   策略「宁缺毋滥」= 只填确定的 k 项 → 命中当且仅当真实答案恰为 k 项
  //   策略「补全为 ABCD」        → 命中当且仅当真实答案为 4 项
  // 前提：已确定的 k 项确实在正确答案中（否则两种策略都是 0）
  const strategy = [2, 3].map((k) => ({
    determined: k,
    keepOnly: total ? dist[k] / total : 0,
    fillAll: total ? dist[4] / total : 0,
  }));

  if (asJson) {
    console.log(
      JSON.stringify(
        { total, dist, pct: { d2: pct(dist[2]), d3: pct(dist[3]), d4: pct(dist[4]) }, perYear, strategy, problems },
        null,
        2
      )
    );
  } else {
    console.log('=== 政治真题 · 多项选择题答案项数分布 ===');
    console.log('口径：只统计「## 二、多项选择题」到「## 三、辨析题」之间\n');
    console.log('年份 | 题数 | 2 项 | 3 项 | 4 项(全选)');
    console.log(':---:|:---:|:---:|:---:|:---:');
    for (const r of perYear) console.log(`${r.year} | ${r.n} | ${r.d2} | ${r.d3} | ${r.d4}`);
    console.log(`**合计** | **${total}** | **${dist[2]}** | **${dist[3]}** | **${dist[4]}**`);
    console.log(`占比 | 100% | ${pct(dist[2])} | ${pct(dist[3])} | ${pct(dist[4])}`);

    console.log('\n=== 无部分分规则下的策略对比 ===');
    console.log('（评分规则：「未选、错选、多选或少选均无分」⇒ 少选也是 0 分）\n');
    for (const s of strategy) {
      const better = s.fillAll > s.keepOnly ? '补全' : '宁缺毋滥';
      console.log(
        `已确定 ${s.determined} 项：只填这 ${s.determined} 项 → ${(s.keepOnly * 100).toFixed(1)}%；` +
          `补全为 ABCD → ${(s.fillAll * 100).toFixed(1)}%　⇒ 期望更高：${better}`
      );
    }

    if (problems.length) {
      console.log('\n⚠️ 发现问题：');
      for (const p of problems) console.log('  - ' + p);
    } else {
      console.log('\n✅ 每年均提取到 10 道多选题，切段正常。');
    }
  }

  process.exit(problems.length ? 1 : 0);
}

main();
