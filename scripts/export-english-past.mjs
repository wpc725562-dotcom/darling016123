/* 导出「以往题目」全部篇章为 Markdown，供其他 AI 读取。
   源：D:/studio/past-english-data.js（文章 + 逐段译文 + 错因）
       D:/studio/past-english-freq.js（真题高频词字典，>=5 次）
   正文里把命中高频词的词加粗（与 Studio 页面同一套规则），篇末附本篇词表。
   用法：node scripts/export-english-past.mjs [输出路径] */

import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');
const STUDIO = 'D:/studio';
const OUT = process.argv[2] || path.join(ROOT, '导出/英语以往题目-精读合辑.md');

/* ---------- 载入 Studio 数据 ---------- */
function loadWindowVar(file, names) {
  const code = fs.readFileSync(file, 'utf8');
  const win = {};
  new Function('window', code)(win);
  const out = {};
  for (const n of names) out[n] = win[n];
  return out;
}

const { PAST_ARTICLES, PAST_PENDING } = loadWindowVar(
  path.join(STUDIO, 'past-english-data.js'),
  ['PAST_ARTICLES', 'PAST_PENDING']
);
const { PAST_FREQ } = loadWindowVar(
  path.join(STUDIO, 'past-english-freq.js'),
  ['PAST_FREQ']
);

const MIN = 5;

/* 与 past-english.html 的 lookup() 完全一致：只做屈折还原，不做派生 */
function lookup(raw) {
  const b = raw.toLowerCase();
  const forms = [
    b,
    b.replace(/ies$/, 'y'), b.replace(/ied$/, 'y'),
    b.replace(/es$/, ''), b.replace(/s$/, ''),
    b.replace(/ing$/, 'e'), b.replace(/ing$/, ''),
    b.replace(/ed$/, 'e'), b.replace(/ed$/, ''), b.replace(/d$/, ''),
    b.replace(/ly$/, ''),
  ];
  for (const f of forms) {
    if (f.length < 3) continue;
    const v = PAST_FREQ[f];
    if (v && v[0] >= MIN) return { n: v[0], short: v[1], full: v[2], base: f };
  }
  return null;
}

/* 给英文段加粗高频词，并收集本篇词表 */
function markHighFreq(en, hits) {
  return en.replace(/[A-Za-z][A-Za-z'-]*/g, (w) => {
    const v = lookup(w);
    if (!v) return w;
    hits.set(v.base, { word: w, n: v.n, full: v.full });
    return `**${w}**`;
  });
}

/* HTML → Markdown */
function toMd(s) {
  return String(s)
    .replace(/<b>/g, '**').replace(/<\/b>/g, '**')
    .replace(/<em>/g, '*').replace(/<\/em>/g, '*')
    .replace(/<[^>]+>/g, '')
    .replace(/\*\*\s*\*\*/g, '')
    .trim();
}

/* ---------- 拼装 ---------- */
const ready = PAST_ARTICLES.filter((a) => a.status === 'ready');
const parts = [];
const allHits = new Map();

parts.push(`# 广东专升本 · 英语以往题目精读合辑

> **用途**：供 AI 阅读、出题、讲评使用。收录实际做过的英语真题文章，每篇含原文、逐段中译、答案、错题诊断。
> **来源**：\`历年真题/公共英语/20XX.md\` 与当次订正记录，经 Studio「以往题目」页汇编。
> **规模**：已精读 ${ready.length} 篇 + 待补 ${PAST_PENDING.length} 篇。
> **生成**：2026-11-05，脚本 \`scripts/export-english-past.mjs\`。

## 给 AI 的读法说明

1. **每篇结构**：篇头信息 → 原文与逐段译文（\`[n]\` 段号对应）→ 答案 → 方法提示 → 错题与判据。
2. **正文中加粗的词**，是「广东省专升本英语真题中出现 ≥ 5 次」的高频词，篇末附词表（含完整释义）。加粗只作提示，不影响原文。
3. **「错题与判据」是本人实际踩过的坑**，含错误选项与正确选项的对照。讲评时请优先复述判据，再讲题。
4. **译文为意译**，用于理解句意，不是标准答案。原文以英文段为准。
5. **词表按原形收录**：文中加粗的 \`offering\` / \`provides\` / \`designed\` 等，在词表里归到 \`offer\` / \`provide\` / \`design\`。释义按原形词条给出，遇到 \`-s / -ed / -ing / -ly\` 形式请按原形理解。
6. 待补篇目只有记录、没有原文，请勿据此出题。

---

# 一、已精读（${ready.length} 篇）
`);

for (const a of ready) {
  const hits = new Map();
  const paras = a.paras.map(([en, zh], i) => {
    const marked = markHighFreq(en, hits);
    return `**[${i + 1}]**\n\n> ${marked}\n\n${toMd(zh)}`;
  });

  for (const [k, v] of hits) {
    if (!allHits.has(k)) allHits.set(k, v);
  }

  const doneList = (a.done || [])
    .map((d) => `${d.date} ${d.score}`)
    .join('；');

  let sec = `\n## ${a.year} ${a.kind}　${a.title}\n\n`;
  sec += `- **来源**：${a.source}\n`;
  sec += `- **规格**：${a.info}\n`;
  sec += `- **成绩**：${doneList}${a.lastScore ? `（最近：${a.lastScore}）` : ''}\n`;
  sec += `- **答案**：${a.answers}\n\n`;

  sec += `### 原文与译文\n\n${paras.join('\n\n')}\n\n`;

  if (a.notice) sec += `### 方法提示\n\n${toMd(a.notice)}\n\n`;

  if (a.wrong && a.wrong.length) {
    sec += `### 错题与判据\n\n`;
    for (const w of a.wrong) sec += `- ${toMd(w)}\n`;
    sec += '\n';
  }

  if (hits.size) {
    const rows = [...hits.entries()]
      .sort((x, y) => y[1].n - x[1].n)
      .map(([base, v]) => `| ${base} | ${v.full} | ${v.n} |`);
    sec += `### 本篇高频词（≥${MIN} 次）\n\n| 词 | 释义 | 真题出现 |\n|:---|:---|--:|\n${rows.join('\n')}\n`;
  }

  parts.push(sec);
}

/* 待补篇目 */
parts.push(`\n---\n\n# 二、待补译文（${PAST_PENDING.length} 篇）\n\n> 这些篇目做过、有成绩记录，但逐段译文尚未补。原文在 \`历年真题/公共英语/\` 对应年份文件里。\n\n| 年份 | 题型 | 篇目 | 做过的记录 |\n|:---|:---|:---|:---|\n`);
for (const p of PAST_PENDING) {
  parts.push(`| ${p.year} | ${p.kind} | ${p.title} | ${p.done} |\n`);
}

/* 总词表 */
const globalRows = [...allHits.entries()]
  .map(([k, v]) => ({ base: k, ...v }))
  .sort((x, y) => y.n - x.n || x.base.localeCompare(y.base))
  .map((v) => `| ${v.base} | ${v.full} | ${v.n} |`);

parts.push(`\n---\n\n# 三、全部高频词总表（${globalRows.length} 词）\n\n> 收录范围：本合辑 ${ready.length} 篇精读文章中出现 ≥ ${MIN} 次的词。释义取自 \`资料/电子书蒸馏/05-英语/词汇表.txt\`。\n\n| 词 | 释义 | 真题出现 |\n|:---|:---|--:|\n${globalRows.join('\n')}\n`);

fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, parts.join(''), 'utf8');

const size = fs.statSync(OUT).size;
const totalEn = ready.reduce(
  (s, a) => s + a.paras.reduce((t, [en]) => t + en.length, 0),
  0
);
console.log(`✅ ${OUT}`);
console.log(`   ${ready.length} 篇精读 + ${PAST_PENDING.length} 篇待补 · 英文原文 ${totalEn} 字符 · 高频词 ${globalRows.length} 个 · 文件 ${(size / 1024).toFixed(1)} KB`);
