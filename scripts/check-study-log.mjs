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
/* 白名单从单一事实源来（2026-10-19）。
   原来这些常量在本文件和 check-session-ledger.mjs 里各写一份，
   加一个 kind 要改两处、改漏一处就让另一个检查器一直红着。 */
import { KINDS, SUBJECTS, ALIASES, MASTERY, DATE_RE, EVENT_TYPES, SUBJECT_GROUP, groupOf, hasKpId } from './lib/log-schema.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..');

const file = process.argv[2] || path.join(ROOT, '备考计划', '学习日志.jsonl');

/* 白名单已移到 scripts/lib/log-schema.mjs —— 单一事实源，两个检查器共用。 */

// ★ 2026-10-04：`学习日志.jsonl` 里住着**两种**记录：
//   ① 学习记录（本脚本校验的对象）：{date, subject, kind, title, ...}
//   ② studio 遥测事件（`scripts/studio-receiver.mjs` 从 `_inbox/studio-events.jsonl` 沉淀）：
//      {ts, type:'progress'|'mastery'|'word_master', ...}
//   旧版对每一行都查必填字段 ⇒ 遥测事件被误报「缺字段」（实测 2026-10-04：4 条）。
//   判据用 type 白名单，不用「缺 date」—— 「缺 date」会放过真正写坏的学习记录。
//
// ★ 2026-10-19 补漏：EVENT_TYPES 原本在本文件里又抄了一份（第 40 行），
//   而 log-schema.mjs 早就导出了它。这正是本仓库反复出现的「双份事实源」——
//   将来加一个遥测类型（如 streak），ledger 认、本脚本不认 ⇒ 本脚本又喊狼来了。
//   已改为统一从 lib/log-schema.mjs 引入。

if (!fs.existsSync(file)) {
  console.error('找不到文件: ' + file);
  process.exit(1);
}

const raw = fs.readFileSync(file, 'utf8');
const lines = raw.split('\n');
const problems = [];
const entries = [];
const events = [];

lines.forEach((line, i) => {
  const n = i + 1;
  if (!line.trim()) return;

  let o;
  try { o = JSON.parse(line); }
  catch (e) { problems.push('行' + n + ' JSON 解析失败: ' + e.message); return; }

  // 0. 遥测事件分流（不是学习记录，跳过课程字段校验）
  if (o.type && EVENT_TYPES.includes(o.type)) { events.push(o); return; }

  // 0b. 有 type 但不在白名单：大概率是**新遥测类型**（studio-receiver 加了新事件，
  //     log-schema 没跟上）。旧版会把它当学习记录，于是报 4 条「缺字段」+
  //     在科目表里多出一行 `undefined 1 条 | 最近 undefined 断 NaN 天` ——
  //     报错方向完全指错地方，还污染统计。现在只报一条，并直接说该改哪个文件。
  //     2026-10-19 用一条 `{type:'streak'}` 注入复现过。
  if (o.type && !o.date) {
    problems.push('行' + n + ' 未知事件类型: ' + o.type + '（有 type 无 date，像遥测事件）' +
      ' ⇒ 若是新遥测类型，加进 scripts/lib/log-schema.mjs 的 EVENT_TYPES；' +
      '若是学习记录写错了，删掉 type 并补 date/subject/kind/title');
    return;
  }

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

  // 科目名已经报过问题的记录，不要再进科目统计 ——
  // 否则「各科目落账」表里会多出一行 `undefined`，且参与「断档 N 天」的日期比较（NaN）。
  if (typeof o.subject !== 'string' || !o.subject) return;
  // 行号挂成**非枚举**属性：下游要报「行 N」时能读到 e.__n，
  // 但 Object.keys / JSON.stringify 看不到它，不会污染统计与输出。
  Object.defineProperty(o, '__n', { value: n, enumerable: false });
  entries.push(o);
});

// ── 输出 ────────────────────────────────────────────
console.log('==== ' + path.relative(ROOT, file) + ' ====');
console.log('总行数 ' + lines.filter(x => x.trim()).length + ' | 有效记录 ' + entries.length +
  (events.length ? ' | 遥测事件 ' + events.length + '（非学习记录，不参与断档统计）' : ''));

// ── 落账统计：**按考试科目合并**（2026-10-25 改）──────────────────
// 原来按 subject 逐条比「最近日期」，于是 `C语言` / `数据结构` / `计算机`
// 三个名字各自算一组，报出「计算机 断档 11 天」—— 而实际数据结构昨天刚做。
// 断档判据被「同一张卷子拆成几个名字」搞失真。现在先合并再比，
// 明细仍打印在行尾括号里，不丢信息。
console.log('\n-- 各科目落账（按最近日期排序 · 已按考试科目合并）--');
const bySub = {};
for (const e of entries) (bySub[e.subject] = bySub[e.subject] || []).push(e.date);

const byGroup = {};
for (const [sub, ds] of Object.entries(bySub)) {
  const g = groupOf(sub);
  const slot = (byGroup[g] = byGroup[g] || { count: 0, dates: [], members: {} });
  slot.count += ds.length;
  slot.dates.push(...ds);
  slot.members[sub] = ds.length;
}
const rows = Object.entries(byGroup).map(([g, v]) => {
  const uniq = [...new Set(v.dates)].sort();
  return { s: g, count: v.count, last: uniq[uniq.length - 1], members: v.members };
});
rows.sort((a, b) => (a.last < b.last ? 1 : a.last > b.last ? -1 : 0));

const latest = rows.reduce((m, r) => (r.last > m ? r.last : m), '');
for (const r of rows) {
  const gap = latest
    ? Math.round((new Date(latest) - new Date(r.last)) / 86400000)
    : 0;
  const flag = gap === 0 ? '  ' : gap >= 7 ? '  <== 断档 ' + gap + ' 天' : '  断 ' + gap + ' 天';
  // 明细：只有合并了多个 subject 时才展开，避免单科行变长
  const names = Object.keys(r.members);
  const detail = names.length > 1
    ? '   ← ' + names.sort((a, b) => r.members[b] - r.members[a])
        .map(n => n + ' ' + r.members[n]).join(' / ')
    : '';
  console.log('  ' + r.s.padEnd(6) + ' ' + String(r.count).padStart(3) + ' 条 | 最近 ' +
    r.last + flag + detail);
}

const never = SUBJECTS.filter(s => !byGroup[groupOf(s)]);
if (never.length) console.log('\n  从未落账: ' + never.join(' / '));

// 未登记进 SUBJECT_GROUP 的 subject：它会自成一组、继续制造假断档
const unmapped = [...new Set(entries.map(e => e.subject))].filter(s => !SUBJECT_GROUP[s]);
if (unmapped.length) {
  problems.push('subject 未登记进 SUBJECT_GROUP（会自成一组、制造假断档）: ' + unmapped.join(' / '));
}

// ── 考点编号覆盖率 ────────────────────────────────────────────
// 掌握度引擎要求「同一个 key 出现 ≥3 次」才可能判过关。2026-10-19 实测：
// 328 个自由文本考点名只有 2 个出现过第二次（0.6%），5 个 `#Cxxx` 编号里 4 个出现过
// 第二次（80%）—— 差 130 倍。所以 quiz 带不带编号，直接决定引擎是空转还是有数。
//
// ★ 2026-10-25 改口径：**新记录硬拦，历史豁免**。
//   原来一律只报告不判红，理由是「日志 append-only，历史记录改不动」——这个理由
//   对历史成立，但对新记录不成立，结果变成：174 条 quiz 里 0 条带编号，
//   而检查器每次都只打一行提示、退出码 0，谁也没在意。
//   ⇒ 现在设 KPI_REQUIRED_FROM 分界：这天及以后写的 quiz 没编号 = **错误**。
//      历史（2026-10-25 之前）仍只报告，因为确实改不动（当时就没记这个信息）。
//   这条也是「错题本五科全空」的上游：日志没有考点编号 → 错题本填不出
//   「考点编号」列 → 二刷无判据 → 诊断层读数为空。
const KPI_REQUIRED_FROM = '2026-10-25';
// 编号正则已抽到 log-schema.mjs 的 RE_KP_ID / hasKpId —— 原来这里自己写了一份，
// 只认 C/M/E，**不认 D（数据结构）**，与写入器 log-add.mjs 不一致。
const hasId = hasKpId;
const quizzes = entries.filter(e => e.kind === 'quiz');
if (quizzes.length) {
  const withId = quizzes.filter(hasId);
  const pct = (withId.length / quizzes.length) * 100;
  const mark = pct >= 80 ? '🟢' : pct >= 30 ? '🟡' : '🔴';
  console.log('\n-- 考点编号覆盖率（掌握度引擎的口粮）--');
  console.log('  ' + mark + ' quiz ' + withId.length + '/' + quizzes.length +
    ' 带编号（' + pct.toFixed(1) + '%）');

  const perSub = {};
  for (const e of quizzes) {
    const k = e.subject;
    perSub[k] = perSub[k] || { all: 0, id: 0 };
    perSub[k].all++;
    if (hasId(e)) perSub[k].id++;
  }
  const zero = Object.entries(perSub).filter(([, v]) => v.id === 0).map(([k]) => k);
  if (zero.length) console.log('  编号 0 条的科目: ' + zero.join(' / ') + '（这些科目的引擎读数是空的）');

  // 硬拦：分界日及以后的新 quiz 必须带编号
  const fresh = quizzes.filter(e => e.date >= KPI_REQUIRED_FROM);
  const freshBad = fresh.filter(e => !hasId(e));
  const legacy = quizzes.filter(e => e.date < KPI_REQUIRED_FROM && !hasId(e)).length;
  if (legacy) {
    console.log('  历史无编号 ' + legacy + ' 条（' + KPI_REQUIRED_FROM + ' 前，append-only 改不动，豁免）');
  }
  if (freshBad.length) {
    for (const e of freshBad) {
      problems.push('行' + e.__n + ' quiz 缺考点编号（' + KPI_REQUIRED_FROM +
        ' 起强制）: ' + (e.title || '').slice(0, 40));
    }
    console.log('  ❌ ' + KPI_REQUIRED_FROM + ' 起的 quiz 有 ' + freshBad.length + ' 条无编号');
  } else if (fresh.length) {
    console.log('  ✅ ' + KPI_REQUIRED_FROM + ' 起的 quiz ' + fresh.length + ' 条全部带编号');
  }
  if (pct < 80) {
    console.log('  ⇒ 新记录请走 `npm run log:add`：它在写盘前拦住无编号的 quiz。');
  }
}

console.log();
if (problems.length) {
  console.log('发现 ' + problems.length + ' 处问题:');
  for (const p of problems) console.log('  X ' + p);
  process.exit(1);
}
console.log('结构与科目名校验通过 OK');
