#!/usr/bin/env node
/* gen-review-schedule.mjs —— 给「专升本176天计划」补上缺失的反馈闭环
 *
 * 为什么需要它（2026-10-07 研究三个 GitHub 项目后得出）：
 *   · DeepTutor 的核心学习闭环里有 **计划性重复（scheduled repetition）**——
 *     知识点按固定间隔回来重考。原计划总表只有「今日复盘主题」一列，
 *     一个条目出现一次就再也不回来了 ⇒ 这是最大的结构缺口。
 *   · DeepTutor 还有 **掌握度硬门槛**（mastery gate）与 Task Board 状态；
 *     原表没有任何位置记录状态 ⇒ 表只能是计划，不能变成记录。
 *   · darling 自己 10-03 的《自学习法》也写了「到期格子按 [0,1,3,7,14,30,60] 天出同型题」，
 *     但这条只写在文档里，没落到表上。
 *
 * 本脚本做两件事（**只增列，不改原 10 列**）：
 *   1. 计划总表-v2.csv  = 原表 + 3 列（复检到期 / 状态 / 推进日）
 *   2. 复检排程-总表.md = 反向视图：每条复盘条目在 D+n 的哪几天必须回来
 *
 * 用法：node scripts/gen-review-schedule.mjs
 * 幂等：重复跑结果一致；不覆盖任何原文件。
 */

import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');
const SRC = path.join(ROOT, '计划总表.csv');
const OUT_CSV = path.join(ROOT, '计划总表-v2.csv');
const OUT_MD = path.join(ROOT, '复检排程-总表.md');

/* 复检间隔（天）—— 与 darling《自学习法》§1⑤ 的 [0,1,3,7,14,30,60] 一致，去掉 0（当天不算复检） */
const INTERVALS = [1, 3, 7, 14, 30, 60];
const TOTAL_DAYS = 176;

const pad = (n) => 'D' + String(n).padStart(3, '0');

/* ---------- 读原始 CSV（UTF-8 + BOM，LF/CRLF 自适应） ---------- */

const raw = fs.readFileSync(SRC, 'utf8');
const hasBom = raw.charCodeAt(0) === 0xfeff;
const body = hasBom ? raw.slice(1) : raw;
const eol = body.includes('\r\n') ? '\r\n' : '\n';

const lines = body.split(/\r?\n/).filter((l) => l.length > 0);
const header = lines[0].split(',');
const rows = lines.slice(1).map((l) => l.split(','));

if (header.length !== 10) throw new Error('表头列数不是 10，已中止：' + header.length);
if (rows.length !== TOTAL_DAYS) throw new Error(`数据行不是 ${TOTAL_DAYS} 行，已中止：` + rows.length);

/* 防御：任一单元格含 ASCII 逗号 ⇒ 说明有引号包裹，本脚本的朴素 split 不成立，必须停下 */
for (const [i, r] of rows.entries()) {
  if (r.length !== 10) throw new Error(`第 ${i + 1} 行解析出 ${r.length} 列（应为 10），该行含未处理的引号/逗号，已中止`);
}

/* ---------- 派生：复检到期 ---------- */

/** 第 n 天要复检哪些天（该天的复盘条目在 D+1/3/7/14/30/60 回来） */
function dueOn(n) {
  return INTERVALS.map((k) => n - k).filter((d) => d >= 1).map(pad);
}

/* ---------- 输出 1：计划总表-v2.csv ---------- */

const NEW_COLS = ['复检到期（间隔1/3/7/14/30/60）', '状态', '推进日'];
const v2 = [header.concat(NEW_COLS)];
for (const [i, r] of rows.entries()) {
  const n = i + 1;
  v2.push(r.concat([dueOn(n).join(' ') || '—', '', '']));
}

const outCsv = (hasBom ? '\ufeff' : '') + v2.map((r) => r.join(',')).join(eol) + eol;
fs.writeFileSync(OUT_CSV, outCsv, 'utf8');

/* ---------- 自检：原 10 列必须逐字节未变 ---------- */

const back = fs.readFileSync(OUT_CSV, 'utf8').replace(/^\ufeff/, '').split(/\r?\n/).filter(Boolean);
const origColsKept = back.every((line, i) => {
  const cols = line.split(',');
  const want = i === 0 ? header : rows[i - 1];
  return want.every((cell, j) => cols[j] === cell);
});
if (!origColsKept) throw new Error('自检失败：原 10 列有改动，已中止');

/* ---------- 输出 2：复检排程-总表.md ---------- */

const stageOf = (n) => rows[n - 1][3];
const themeOf = (n) => rows[n - 1][9];
const prioOf = (n) => rows[n - 1][8];

let md = '';
md += '# 复检排程 · 总表\n\n';
md += '> **这张表补的是「计划总表」缺的那一环：知识点的回归。**\n';
md += '>\n';
md += '> 研究结论（2026-10-07，来自三个 GitHub 项目）：\n';
md += '> · **DeepTutor** 的学习闭环里有 *计划性重复（scheduled repetition）* —— 知识点按固定间隔回来重考；\n';
md += '> · **good-learning-skill** 的每日课程把「例题 → 变式 → 混合练习」写成固定结构；\n';
md += '> · **Study-Mate** 强调「按可运行证据核验」并「进度落文件、可继承」。\n';
md += '>\n';
md += '> 三者共同指向同一件事：**一个知识点只讲一次、只测一次，等于没学。**\n';
md += '> 原计划总表每个条目只出现一次就再也不回来 —— 这是最大的结构缺口。\n';
md += '>\n';
md += `> **间隔规则**：每条的复盘条目在 **D+${INTERVALS.join(' / D+')}** 各回来一次（与《自学习法-2026-10-03》§1⑤ 一致）。\n`;
md += '> 到期当天**只重考、不重讲**：出同型题，撤掉讲义与表格，独立做对才算过。\n\n';

md += '## 怎么用\n\n';
md += '1. **每天早上**先看本表「今天要复检」那一节 —— 那是**必须**做的，排在学新内容之前。\n';
md += '2. 复检形式固定：**同型题 + 换数字 + 要求说出理由**（《自学习法》§1③ 三条反作弊探针）。\n';
md += '3. 过 → 在 `计划总表-v2.csv` 的「状态」列标 🟢；没过 → 标 🔴 并在次日再排一次。\n';
md += '4. 一天到期超过 4 条时：**先做 P0/P1**，P2/P3 可顺延（但顺延不超过 3 天）。\n\n';

md += '## 状态图例（`计划总表-v2.csv` 的「状态」列）\n\n';
md += '| 记号 | 含义 | 依据 |\n';
md += '|:--:|:--|:--|\n';
md += '| ⬜ | 未开始 | 默认 |\n';
md += '| 🟡 | 待复检（当天做对） | 有脚手架/同场次做对 —— **不算掌握** |\n';
md += '| 🟢 | 已过关 | 撤掉脚手架、**跨日**独立做对 |\n';
md += '| 🔵 | 已稳固 | 过关后再做对**一道变式题**（换数字 + 换条件） |\n';
md += '| 🔴 | 复检未过 | 到期那天没做对 ⇒ 次日重排 |\n';
md += '| ⛔ | 跳过 | 明确决定不做（如 P3 低产出项） |\n\n';
md += '> 「推进日」列：**块 A（计算机）或块 B（高数）至少完成一个** 才记 ✔。\n';
md += '> 这个数就是《自学习法》里唯一的第一性指标 —— **推进日密度（目标 50%，实测 23%）**。\n\n';

md += '---\n\n## 按天索引\n\n';

let curStage = null;
for (let n = 1; n <= TOTAL_DAYS; n++) {
  const st = stageOf(n);
  if (st !== curStage) {
    curStage = st;
    md += `\n### ${st}\n\n`;
    md += '| 天 | 复盘主题 | 优先 | 该条在哪些天必须回来 |\n';
    md += '|:--:|:--|:--:|:--|\n';
  }
  const backDays = INTERVALS.map((k) => n + k)
    .filter((d) => d <= TOTAL_DAYS)
    .map(pad);
  md += `| ${pad(n)} | ${themeOf(n)} | ${prioOf(n)} | ${backDays.join(' · ') || '（考试前不再回来）'} |\n`;
}

md += '\n---\n\n## 每天要复检的清单（反向视图）\n\n';
md += '> 这是**每天早上真正要看的那一栏**：第 N 天到期的是哪几天的条目。\n\n';

let curStage2 = null;
for (let n = 1; n <= TOTAL_DAYS; n++) {
  const due = dueOn(n).map((d) => Number(d.slice(1)));
  if (due.length === 0) continue;
  const st = stageOf(n);
  if (st !== curStage2) {
    curStage2 = st;
    md += `\n### ${st}\n\n`;
  }
  const items = due.map((d) => `${pad(d)}（${prioOf(d)}）${themeOf(d)}`).join('　｜　');
  md += `- **${pad(n)}** → ${items}\n`;
}

md += '\n---\n\n*由 `scripts/gen-review-schedule.mjs` 生成 · 输入：`计划总表.csv`（只读，未改动）· 生成于 2026-10-07*\n';
md += '*间隔依据：darling《自学习法-2026-10-03》§1⑤ + DeepTutor 的 scheduled repetition 机制*\n';

fs.writeFileSync(OUT_MD, md, 'utf8');

/* ---------- 报告 ---------- */

const maxDue = Math.max(...Array.from({ length: TOTAL_DAYS }, (_, i) => dueOn(i + 1).length));
console.log('[ok] 计划总表-v2.csv   :', v2.length - 1, '行 ×', v2[0].length, '列（原 10 列逐格校验未变）');
console.log('[ok] 复检排程-总表.md :', (Buffer.byteLength(md, 'utf8') / 1024).toFixed(1) + ' KB');
console.log('[ok] 单日最多到期条数 :', maxDue);
console.log('[ok] 原文件未改动     :', SRC);
