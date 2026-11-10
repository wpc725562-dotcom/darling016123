#!/usr/bin/env node
/**
 * 网页 AI 开课包 · 考点原文按章导出器
 *
 * 为什么需要它：
 *   网页 AI 看不到本机硬盘，四科考点笔记共 4.4 MB / 519 个考点文件，
 *   一次全贴必然超上下文。所以按「章」切成 76 个可独立粘贴的包，
 *   学到哪章贴哪章（单包 5–35 KB，中文约 2–12 K 字，任何网页 AI 都吃得下）。
 *
 * 输出：备考计划/网页AI开课包/6-考点原文-按章贴/<科目>/<科目>-第NN章-<章名>.md
 *
 * 用法：node scripts/export-web-ai-pack.mjs [--dry]
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.join(__dirname, '..');
const DIST = path.join(REPO, '资料', '电子书蒸馏');
const OUT_ROOT = path.join(REPO, '备考计划', '网页AI开课包', '6-考点原文-按章贴');

const TODAY = '2026-11-03';
const DRY = process.argv.includes('--dry');

/** 单包上限（KB）。超过就按考点切成多份 —— 96 KB 的 C 语言第 7 章 ≈ 3.2 万字，
 *  贴进上下文较小的网页 AI 会截断，切完每份 30 KB 左右最稳。 */
const SPLIT_AT_KB = 45;

/** 按考点把 entries 贪心切成若干块，每块字符量不超过 limitKB×1024/3（UTF-8 中文 3 字节） */
function splitEntries(entries, limitKB) {
  const withSize = entries.map((e) => ({
    e,
    bytes: Buffer.byteLength(fs.readFileSync(e.full, 'utf8')),
  }));
  const total = withSize.reduce((n, x) => n + x.bytes, 0);
  if (total <= limitKB * 1024) return [entries];

  const nParts = Math.ceil(total / (limitKB * 1024));
  const target = total / nParts;
  const chunks = [];
  let cur = [];
  let acc = 0;
  for (const { e, bytes } of withSize) {
    if (cur.length && acc + bytes > target * 1.15) {
      chunks.push(cur);
      cur = [];
      acc = 0;
    }
    cur.push(e);
    acc += bytes;
  }
  if (cur.length) chunks.push(cur);
  return chunks;
}

/** 读目录下所有 .txt / .md 文件名（不含子目录） */
function listFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((f) => /\.(txt|md)$/i.test(f))
    .sort();
}

/** 从「章节」目录读出 章号 → 章名 的映射 */
function readChapterNames(dir, prefix = '') {
  const map = new Map();
  for (const f of listFiles(dir)) {
    // 例：第05章-定积分.txt / C第05章-循环结构程序设计.txt / D第8章-排序.txt
    const m = f.match(new RegExp(`^${prefix}第0*(\\d+)章[-－](.+)\\.(txt|md)$`));
    if (!m) continue;
    const ch = parseInt(m[1], 10);
    // 同一章若有多个文件（如 D第08章 / D第8章），保留文件名更长（信息更全）的那个
    const prev = map.get(ch);
    if (!prev || m[2].length > prev.length) map.set(ch, m[2]);
  }
  return map;
}

/** 中文体量估算：UTF-8 中文 3 字节/字，混 ASCII，用「字数」口径 */
function charCount(s) {
  return [...s].length;
}

/** 生成一个包文件的内容 */
function buildPack({ subjectLabel, chapterLabel, chapterName, entries, sourceDir, part = null }) {
  const body = entries
    .map((e) => {
      const text = fs.readFileSync(e.full, 'utf8').replace(/\r\n/g, '\n').trimEnd();
      // 原文首行就是【课程】…，直接接在 ## 标题下，避免重复
      return `## ${e.title}\n\n\`\`\`\n${text}\n\`\`\``;
    })
    .join('\n\n---\n\n');

  const totalChars = entries.reduce(
    (n, e) => n + charCount(fs.readFileSync(e.full, 'utf8')),
    0
  );

  const partNote = part
    ? `\n> **本文件是拆分后的第 ${part.idx} / ${part.total} 份** —— 原章太大贴不进上下文，按考点切开了。**按 1→${part.total} 顺序贴**，每贴完一份再贴下一份。`
    : '';

  return `# ${subjectLabel} ${chapterLabel} ${chapterName}

> **这是什么**：${chapterLabel}「${chapterName}」的考点笔记原文，本份含 **${entries.length} 个考点**、约 **${totalChars} 字**。${partNote}
> **怎么用**：先贴 \`0-教练规则\` + 对应科目 \`状态卡\`，再把本文件**全文**贴上去，然后说「开始讲本章第 X 节」。
> **来源**：\`资料/电子书蒸馏/${sourceDir}\` · 导出于 ${TODAY}

---

${body}
`;
}

// ── 各科的切章规则 ────────────────────────────────────────────────

const SPECS = [
  {
    key: '高数',
    subjectLabel: '高等数学',
    notesDir: path.join(DIST, '04-高数', '考点笔记'),
    chapterDir: path.join(DIST, '04-高数', '章节'),
    chapterPrefix: '',
    // G5-2-牛顿… → ch 5
    parse: (f) => {
      const m = f.match(/^G0*(\d+)-\d+-/);
      return m ? parseInt(m[1], 10) : null;
    },
    stripId: (f) => f.replace(/\.(txt|md)$/i, ''),
  },
  {
    key: '计算机-C',
    subjectLabel: '计算机基础 · C 语言',
    notesDir: path.join(DIST, '03-计算机', '考点笔记'),
    chapterDir: path.join(DIST, '03-计算机', '章节'),
    chapterPrefix: 'C',
    parse: (f) => {
      const m = f.match(/^C0*(\d+)-\d+-/);
      return m ? parseInt(m[1], 10) : null;
    },
    stripId: (f) => f.replace(/\.(txt|md)$/i, ''),
    outName: (ch) => `计算机-C第${String(ch).padStart(2, '0')}章`,
  },
  {
    key: '计算机-D',
    subjectLabel: '计算机基础 · 数据结构',
    notesDir: path.join(DIST, '03-计算机', '考点笔记'),
    chapterDir: path.join(DIST, '03-计算机', '章节'),
    chapterPrefix: 'D',
    parse: (f) => {
      const m = f.match(/^D0*(\d+)-\d+-/);
      return m ? parseInt(m[1], 10) : null;
    },
    stripId: (f) => f.replace(/\.(txt|md)$/i, ''),
    outName: (ch) => `计算机-D第${String(ch).padStart(2, '0')}章`,
  },
  {
    key: '毛中特',
    subjectLabel: '政治 · 毛中特',
    notesDir: path.join(DIST, '01-毛中特', '考点笔记'),
    chapterDir: path.join(DIST, '01-毛中特', '章节'),
    chapterPrefix: '',
    parse: (f) => {
      const m = f.match(/^0*(\d+)-\d+-\d+-/);
      return m ? parseInt(m[1], 10) : null;
    },
    stripId: (f) => f.replace(/\.(txt|md)$/i, ''),
    outName: (ch) => `毛中特-第${String(ch).padStart(2, '0')}章`,
  },
  {
    key: '习概',
    subjectLabel: '政治 · 习概',
    notesDir: path.join(DIST, '02-习概', '考点笔记'),
    chapterDir: path.join(DIST, '02-习概', '章节'),
    chapterPrefix: '',
    parse: (f) => {
      const m = f.match(/^0*(\d+)-\d+-\d+-/);
      return m ? parseInt(m[1], 10) : null;
    },
    stripId: (f) => f.replace(/\.(txt|md)$/i, ''),
    outName: (ch) => `习概-第${String(ch).padStart(2, '0')}章`,
  },
  {
    key: '英语',
    subjectLabel: '英语',
    notesDir: path.join(DIST, '05-英语', '考点笔记'),
    chapterDir: null,
    chapterPrefix: null,
    parse: (f) => {
      const m = f.match(/^[EW]0*(\d+)-\d+-/);
      return m ? parseInt(m[1], 10) : null;
    },
    stripId: (f) => f.replace(/\.(txt|md)$/i, ''),
    // 英语没有「章节」目录，组名用该组第一个考点名
    outName: (ch, entries) => {
      const first = entries[0].title.replace(/^[EW]\d+-\d+-/, '');
      return `英语-${ch < 100 ? 'E' : 'W'}第${String(ch).padStart(2, '0')}组-${first}`;
    },
    noChapterName: true,
  },
];

function main() {
  let written = 0;
  const report = [];

  for (const spec of SPECS) {
    const names = spec.chapterDir ? readChapterNames(spec.chapterDir, spec.chapterPrefix) : new Map();
    const files = listFiles(spec.notesDir);

    // 按章聚合
    const groups = new Map();
    for (const f of files) {
      const ch = spec.parse(f);
      if (ch === null) continue;
      if (!groups.has(ch)) groups.set(ch, []);
      groups.get(ch).push({
        full: path.join(spec.notesDir, f),
        title: spec.stripId(f),
      });
    }

    const outDir = path.join(OUT_ROOT, spec.key.startsWith('计算机') ? '计算机' : spec.key.startsWith('毛') || spec.key.startsWith('习') ? '政治' : spec.key);
    if (!DRY) fs.mkdirSync(outDir, { recursive: true });

    for (const ch of [...groups.keys()].sort((a, b) => a - b)) {
      const entries = groups.get(ch);
      const chapterName = spec.noChapterName
        ? entries[0].title.replace(/^[EW]\d+-\d+-/, '')
        : names.get(ch) || `第${ch}章`;
      const chapterLabel = spec.noChapterName ? '' : `第${String(ch).padStart(2, '0')}章`;
      const base = spec.outName ? spec.outName(ch, entries) : `${spec.key}-第${String(ch).padStart(2, '0')}章-${chapterName}`;

      // 单包超过 SPLIT_AT_KB 就按考点切成若干份，保证每个包都贴得进网页 AI
      const chunks = splitEntries(entries, SPLIT_AT_KB);
      chunks.forEach((chunk, idx) => {
        const suffix = chunks.length > 1 ? `-${idx + 1}of${chunks.length}` : '';
        const outFile = path.join(outDir, `${base}${suffix}.md`);
        const content = buildPack({
          subjectLabel: spec.subjectLabel,
          chapterLabel,
          chapterName,
          entries: chunk,
          sourceDir: path.relative(DIST, spec.notesDir).replace(/\\/g, '/'),
          part: chunks.length > 1 ? { idx: idx + 1, total: chunks.length } : null,
        });
        if (!DRY) fs.writeFileSync(outFile, content, 'utf8');
        written++;
        report.push({
          subject: spec.subjectLabel,
          ch: chapterLabel || `组${ch}`,
          name: chapterName,
          n: chunk.length,
          kb: Math.round(Buffer.byteLength(content) / 1024),
          chars: charCount(content),
          file: path.relative(REPO, outFile).replace(/\\/g, '/'),
        });
      });
    }
  }

  // 汇总
  console.log(DRY ? '=== dry run · 不写盘 ===' : `=== 已写出 ${written} 个包 ===`);
  const bySubject = new Map();
  for (const r of report) {
    if (!bySubject.has(r.subject)) bySubject.set(r.subject, { n: 0, kb: 0, chars: 0, packs: 0 });
    const a = bySubject.get(r.subject);
    a.packs++;
    a.n += r.n;
    a.kb += r.kb;
    a.chars += r.chars;
  }
  for (const [s, a] of bySubject) {
    console.log(
      `${s.padEnd(22)} ${String(a.packs).padStart(2)} 包 · ${String(a.n).padStart(3)} 考点 · ${String(a.kb).padStart(4)} KB · 约 ${a.chars} 字`
    );
  }
  console.log(`\n最大单包：${Math.max(...report.map((r) => r.kb))} KB`);
  const big = report.filter((r) => r.kb > 40).sort((a, b) => b.kb - a.kb);
  if (big.length) {
    console.log('⚠️ 超过 40 KB 的包（贴之前确认模型上下文够）：');
    for (const r of big) console.log(`   ${r.kb} KB · ${r.file}`);
  }
  if (DRY) {
    console.log('\n前 8 个包：');
    for (const r of report.slice(0, 8)) console.log(`   ${r.file}  (${r.n} 考点 / ${r.kb} KB)`);
  }
}

main();
