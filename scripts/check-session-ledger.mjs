#!/usr/bin/env node
/**
 * check-session-ledger.mjs —— 学习会话「落账」检查（只读，不改任何文件）
 *
 * 为什么需要它
 * ------------
 * 每次学习会话收工要落四笔账：看板 / 学习日志 / 错题本 / 开场卡。
 * 这四步是**纯手工流程，漏一步没有任何提示**。本站已经因为「漏登记」出过四次事故：
 *   · 24 份学习资料文件在、内容完整，只是没登记进侧栏 → 等于对读者不存在
 *   · 22 个模拟卷页面全部导航不可达
 *   · 英语真题 4 个年份页侧栏找不到
 *   · 一条死链在 nav + sidebar 各引用一次，文件从来不存在
 * 四次全是同一个根因：**加东西要动两个地方，第二步漏了没人知道**。
 *
 * 结论：绑定两步手工流程的地方，必须有一道自动检查。
 *
 * 用法
 * ----
 *   node scripts/check-session-ledger.mjs              # 检查（默认 3 天内算新鲜）
 *   node scripts/check-session-ledger.mjs --days 1     # 收紧到 1 天
 *   node scripts/check-session-ledger.mjs --json       # 机器可读输出
 *   node scripts/check-session-ledger.mjs --selftest   # 证明它「有能力失败」
 *
 * 退出码：0 = 全通过；1 = 有失败项
 *
 * ⚠️ --selftest 不是装饰。一个永远报「通过」的检查器和「没有检查」无法区分，
 *    这和「工具瞎了」是同一件事。所以本脚本必须能被证明会失败。
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(__dirname, '..');

const LEDGER = path.join(REPO, '备考计划', '学习日志.jsonl');
const BOARD = path.join(REPO, '备考计划', '学习进度看板.md');
const MISTAKES = path.join(REPO, '备考计划', '错题本模板.md');
const CARDS_DIR = path.join(REPO, '备考计划', '开新话题');

// 实际用到的 5 种（2026-09-17 从 38 条记录实查，不是猜的）。
// ⚠️ 这几行**不要靠记忆改**：跑了发现新 kind 就加进来，并想想它该不该算学习量。
//    lecture/quiz = 真学习量；anki = 复习；feedback = 反馈；tool = 改工具（**一律不算学习量**）
const VALID_KINDS = ['lecture', 'quiz', 'anki', 'feedback', 'tool'];
const VALID_MASTERY = ['passed', 'partial', 'failed', 'na'];
const REQUIRED_FIELDS = ['date', 'subject', 'kind', 'title'];

// ---------------------------------------------------------------- 纯函数层
// 校验逻辑写成纯函数，好让 --selftest 能直接喂坏数据进来。

/** 从 markdown 里取 `**last_updated**: YYYY-MM-DD` */
export function parseLastUpdated(markdown) {
  const m = markdown.match(/last_updated\*{0,2}\s*[:：]\s*(\d{4}-\d{2}-\d{2})/);
  return m ? m[1] : null;
}

/** 取所有 #C数字 编号（**任何位置**，含正文交叉引用）。
 *  用途：从「看板」这类散文里找出它提到了哪些错题编号。 */
export function extractIds(text) {
  const ids = new Set();
  for (const m of text.matchAll(/#C(\d{1,4})\b/g)) ids.add(`C${String(Number(m[1]))}`);
  return ids;
}

/**
 * 取错题**定义行**里的编号 —— 只认标题行（`### 错题 #C001` / `### #C006 a`）。
 *
 * ★ 2026-09-23 修正：原实现用「全文任意位置」的 `#C\d{1,4}` 去查重复，于是
 *   正文里的**交叉引用**也被当成编号声明 ⇒ 误报重复。
 *   实测 `备考计划/错题本模板.md`（错题本本身完全正常）：
 *     · #C007 在行 192 **定义**，行 219 / 220 **引用**
 *     · #C001 / #C006 在行 317 被**引用**（「实际 #C001~#C006 均已销账」）
 *   ⇒ 旧实现报「重复编号：#C7, #C1, #C6」，1/7 项常年红着。
 *   本文件自检用例里「错题编号重复」用的是两个**标题行**
 *   （`### #C006 a\n### #C006 b`），说明本意就是只认定义行。
 *
 * 返回**数组**（不去重）——查重复需要看见每个定义。
 */
export function extractDefinedIds(text) {
  const ids = [];
  for (const line of text.split(/\r?\n/)) {
    if (!/^\s{0,3}#{1,6}\s/.test(line)) continue; // 只认 markdown 标题行
    for (const m of line.matchAll(/#C(\d{1,4})\b/g)) ids.push(`C${Number(m[1])}`);
  }
  return ids;
}

/** 解析 jsonl，返回 {records, errors} */
export function parseLedger(raw) {
  const records = [];
  const errors = [];
  const lines = raw.split(/\r?\n/);
  lines.forEach((line, i) => {
    if (!line.trim()) return;
    let obj;
    try {
      obj = JSON.parse(line);
    } catch (e) {
      errors.push(`第 ${i + 1} 行不是合法 JSON：${e.message}`);
      return;
    }
    for (const f of REQUIRED_FIELDS) {
      if (!obj[f]) errors.push(`第 ${i + 1} 行缺字段 \`${f}\``);
    }
    if (obj.date && !/^\d{4}-\d{2}-\d{2}$/.test(obj.date)) {
      errors.push(`第 ${i + 1} 行 date 格式不对（要 YYYY-MM-DD）：${obj.date}`);
    }
    if (obj.kind && !VALID_KINDS.includes(obj.kind)) {
      errors.push(`第 ${i + 1} 行 kind 不认识：${obj.kind}（已知 ${VALID_KINDS.join(' / ')}；若是新类别请加进脚本的 VALID_KINDS）`);
    }
    if (obj.mastery && !VALID_MASTERY.includes(obj.mastery)) {
      errors.push(`第 ${i + 1} 行 mastery 不认识：${obj.mastery}（已知 ${VALID_MASTERY.join(' / ')}）`);
    }
    records.push(obj);
  });
  return { records, errors };
}

/** 天数差（today - date），按自然日 */
export function daysBetween(dateStr, today) {
  const d = new Date(`${dateStr}T00:00:00Z`);
  const t = new Date(`${today}T00:00:00Z`);
  if (Number.isNaN(d.getTime())) return null;
  return Math.round((t - d) / 86400000);
}

/** 找重复编号 */
export function findDuplicates(ids) {
  const seen = new Map();
  const dup = new Set();
  for (const id of ids) {
    if (seen.has(id)) dup.add(id);
    seen.set(id, true);
  }
  return dup;
}

// ---------------------------------------------------------------- 检查层

function runChecks(env, opts) {
  const { today, days, ledgerRaw, boardRaw, mistakesRaw, cardFiles } = env;
  const results = [];

  const add = (name, ok, detail) => results.push({ name, ok, detail });

  // ---- 1. 学习日志：能解析、字段齐、格式对
  const { records, errors } = parseLedger(ledgerRaw);
  add(
    '学习日志 JSON 合法且字段完整',
    errors.length === 0,
    errors.length ? errors.slice(0, 8).join('\n      ') : `${records.length} 条记录全部通过`
  );

  // 刚好卡在窗口边界时提示 —— 「通过」不等于「新鲜」。
  // 例：窗口 3 天、最新条目恰是 3 天前，判定通过，但其实随时会翻红。
  const boundaryHint = (age) =>
    age === days ? `　⚠️ 刚好卡在 ${days} 天边界，明天就会翻红，别当它是「新鲜」` : '';

  // ---- 2. 学习日志：新鲜度
  const dates = records.map((r) => r.date).filter(Boolean).sort();
  const newest = dates[dates.length - 1] || null;
  const ledgerAge = newest ? daysBetween(newest, today) : null;
  const ledgerDetail = !newest
    ? '一条都没有'
    : ledgerAge === null
      ? `最新一条 ${newest}（日期解析不出来，无法判断新鲜度）`
      : `最新一条 ${newest}（${ledgerAge} 天前）${boundaryHint(ledgerAge)}`;
  add(`学习日志在 ${days} 天内有新条目`, ledgerAge !== null && ledgerAge <= days, ledgerDetail);

  // ---- 3. 看板 last_updated 新鲜度
  const boardDate = parseLastUpdated(boardRaw);
  const boardAge = boardDate ? daysBetween(boardDate, today) : null;
  const boardDetail = !boardDate
    ? '看板里找不到 `**last_updated**: YYYY-MM-DD`'
    : boardAge === null
      ? `last_updated = ${boardDate}（日期解析不出来）`
      : `last_updated = ${boardDate}（${boardAge} 天前）${boundaryHint(boardAge)}`;
  add(`看板 last_updated 在 ${days} 天内`, boardAge !== null && boardAge <= days, boardDetail);

  // ---- 4. 错题本编号无重复
  //   只数**定义行**里的编号。正文交叉引用不算声明（详见 extractDefinedIds 注释）。
  const definedIds = extractDefinedIds(mistakesRaw);
  const mistakeIds = new Set(definedIds);
  const dups = findDuplicates(definedIds);
  add(
    '错题本编号无重复',
    dups.size === 0,
    dups.size ? `重复编号：${[...dups].map((d) => '#' + d).join(', ')}` : `${mistakeIds.size} 个编号`
  );

  // ---- 5. 看板提到的错题编号，错题本里得有
  //   boardIds 用「全文出现」—— 看板是散文，提到即算；
  //   但「错题本里有没有」必须以**定义**为准，否则悬空引用会被放过。
  const boardIds = extractIds(boardRaw);
  const missing = [...boardIds].filter((id) => !mistakeIds.has(id));
  add(
    '看板提到的错题编号都在错题本里',
    missing.length === 0,
    missing.length ? `错题本里找不到：${missing.map((m) => '#' + m).join(', ')}` : `${boardIds.size} 个编号对得上`
  );

  // ---- 6. 开场卡齐 + 引用教练手册
  const cardIssues = [];
  for (const f of cardFiles) {
    const p = path.join(CARDS_DIR, f);
    let text = '';
    try {
      text = fs.readFileSync(p, 'utf8');
    } catch {
      cardIssues.push(`${f} 读不到`);
      continue;
    }
    if (!text.includes('教练手册-教学纪律')) cardIssues.push(`${f} 没指向教练手册`);
  }
  add(
    '开场卡都在且指向教练手册',
    cardIssues.length === 0,
    cardIssues.length ? cardIssues.join('；') : `${cardFiles.length} 份开场卡`
  );

  // ---- 7. 分布快照（信息性，永远 ok）
  // 目的不是判对错，是**让漂移可见**：哪天出现第 6 种 kind，这里一眼能看到。
  const tally = (key) => {
    const c = {};
    for (const r of records) {
      const v = r[key] ?? '(空)';
      c[v] = (c[v] || 0) + 1;
    }
    return Object.entries(c).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k}×${v}`).join(' · ');
  };
  const realStudy = records.filter((r) => r.kind === 'lecture' || r.kind === 'quiz').length;
  add(
    '分布快照（信息）',
    true,
    `共 ${records.length} 条 · 其中真学习量(lecture+quiz) ${realStudy} 条\n` +
      `kind: ${tally('kind')}\n` +
      `subject: ${tally('subject')}\n` +
      `mastery: ${tally('mastery')}`
  );

  return results;
}

// ---------------------------------------------------------------- 自检层

function selftest() {
  const today = '2026-09-17';
  const good = {
    today,
    days: 3,
    ledgerRaw: JSON.stringify({
      date: '2026-09-17', subject: 'C语言', kind: 'quiz',
      title: '测试', score: '1/1', mastery: 'passed', weak: '', note: '',
    }),
    boardRaw: '**last_updated**: 2026-09-17\n提到 #C006 这笔账',
    mistakesRaw: '### #C006 阶梯漏看\n',
    cardFiles: ['C语言.md'],
  };

  const scenarios = [
    {
      name: '全绿样本',
      env: good,
      expectFail: false,
    },
    {
      name: '日志缺字段',
      env: { ...good, ledgerRaw: JSON.stringify({ date: '2026-09-17', subject: 'C语言' }) },
      expectFail: true,
      expectIn: '缺字段',
    },
    {
      name: '日志日期格式错',
      env: { ...good, ledgerRaw: JSON.stringify({ date: '2026/09/17', subject: 'C语言', kind: 'quiz', title: 'x' }) },
      expectFail: true,
      expectIn: '格式不对',
    },
    {
      name: '看板过期',
      env: { ...good, boardRaw: '**last_updated**: 2026-08-01' },
      expectFail: true,
      expectIn: 'last_updated',
    },
    {
      name: '错题编号重复',
      env: { ...good, mistakesRaw: '### #C006 a\n### #C006 b\n' },
      expectFail: true,
      expectIn: '重复编号',
    },
    {
      // ★ 2026-09-23：正文里的交叉引用不是编号声明，不能算重复。
      //   旧实现扫全文 ⇒ 真实错题本（#C007 定义 1 次、正文引用 2 次）被误报重复。
      name: '正文引用不算重复',
      env: {
        ...good,
        mistakesRaw: '### 错题 #C006 a\n\n见 #C006 的复检记录；另 #C001~#C006 均已销账。\n',
      },
      expectFail: false,
    },
    {
      // ★ 2026-09-23：看板提到的编号必须在错题本里**有定义**。
      //   只在正文里被引用（悬空引用）不算有 —— 这条是收紧后的行为。
      name: '悬空引用要报错',
      env: {
        ...good,
        mistakesRaw: '### 错题 #C005 a\n\n另见 #C006 的复检记录。\n',
      },
      expectFail: true,
      expectIn: '找不到',
    },
    {
      name: '看板提到但错题本没有',
      env: { ...good, mistakesRaw: '### #C001 别的东西\n' },
      expectFail: true,
      expectIn: '找不到',
    },
    {
      name: 'JSON 整行坏掉',
      env: { ...good, ledgerRaw: '{ 这不是 json' },
      expectFail: true,
      expectIn: '不是合法 JSON',
    },
    {
      // 「通过」≠「新鲜」：日志与看板都恰好 3 天前，判定仍算过，
      // 但必须带出边界提示，否则用户会以为明天还能过。
      name: '刚好卡窗口边界',
      env: {
        ...good,
        ledgerRaw: JSON.stringify({
          date: '2026-09-14', subject: 'C语言', kind: 'quiz',
          title: '边界', score: '1/1', mastery: 'passed', weak: '', note: '',
        }),
        boardRaw: '**last_updated**: 2026-09-14\n提到 #C006 这笔账',
      },
      expectFail: false,
      expectWarnIn: '边界',
    },
  ];

  console.log('🧪 自检：故意喂坏数据，看检查器会不会亮\n');
  let allGood = true;
  for (const sc of scenarios) {
    const res = runChecks(sc.env, { days: sc.env.days });
    const failed = res.filter((r) => !r.ok);
    const didFail = failed.length > 0;
    const detail = failed.map((f) => f.detail).join(' | ');
    const allDetail = res.map((r) => r.detail).join(' | ');
    let ok;
    if (sc.expectFail) {
      ok = didFail && (!sc.expectIn || detail.includes(sc.expectIn));
    } else {
      ok = !didFail && (!sc.expectWarnIn || allDetail.includes(sc.expectWarnIn));
    }
    allGood = allGood && ok;
    console.log(
      `${ok ? '✅' : '❌'} ${sc.name.padEnd(18, ' ')} 期望${
        sc.expectFail ? '报错' : sc.expectWarnIn ? '通过但带提示' : '通过'
      } · 实际${didFail ? '报错' : '通过'}` +
      (didFail ? `\n     └─ ${detail.slice(0, 160)}` : sc.expectWarnIn ? `\n     └─ ${allDetail.slice(0, 160)}` : '')
    );
  }
  console.log(
    allGood
      ? '\n✅ 自检通过：这个检查器**有能力失败**，它的「全绿」才有意义。'
      : '\n❌ 自检失败：检查器有哑掉的条目，别信它的全绿。'
  );
  process.exit(allGood ? 0 : 1);
}

// ---------------------------------------------------------------- 主流程

function main() {
  const argv = process.argv.slice(2);

  if (argv.includes('--selftest')) return selftest();

  const daysIdx = argv.indexOf('--days');
  const days = daysIdx >= 0 ? Number(argv[daysIdx + 1]) : 3;
  const asJson = argv.includes('--json');

  const read = (p) => {
    try {
      return fs.readFileSync(p, 'utf8');
    } catch (e) {
      console.error(`❌ 读不到 ${p}：${e.message}`);
      process.exit(1);
    }
  };

  let cardFiles = [];
  try {
    cardFiles = fs.readdirSync(CARDS_DIR).filter((f) => f.endsWith('.md'));
  } catch {
    /* 目录不存在时留空，由检查项报出来 */
  }

  const today = new Date().toISOString().slice(0, 10);
  const results = runChecks(
    {
      today,
      days,
      ledgerRaw: read(LEDGER),
      boardRaw: read(BOARD),
      mistakesRaw: read(MISTAKES),
      cardFiles,
    },
    { days }
  );

  const failed = results.filter((r) => !r.ok);

  if (asJson) {
    console.log(JSON.stringify({ today, days, results, failed: failed.length }, null, 2));
  } else {
    console.log(`📒 学习会话落账检查 · 基准日 ${today} · 新鲜度阈值 ${days} 天\n`);
    for (const r of results) {
      console.log(`${r.ok ? '✅' : '❌'} ${r.name}`);
      console.log(`     ${r.detail.split('\n').join('\n     ')}`);
    }
    console.log(
      failed.length
        ? `\n❌ ${failed.length}/${results.length} 项没过。收工落账有缺 —— 补完再开新课。`
        : `\n✅ ${results.length}/${results.length} 项全过。`
    );
  }

  process.exit(failed.length ? 1 : 0);
}

// 只在直接运行时跑 main（被 import 时不跑）
if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(fileURLToPath(import.meta.url))) {
  main();
}
