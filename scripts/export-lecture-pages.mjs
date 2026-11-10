#!/usr/bin/env node
/**
 * 讲义（笔记站 docs/posts/*\/notes/）导出器 —— 给网页 AI 贴的版本
 *
 * 为什么需要它：
 *   用户指的那批「1.6a 数组 —— 零基础能看懂版」不是 `资料/电子书蒸馏/考点笔记`
 *   （那是蒸馏骨架），而是 `docs/posts/*\/notes/` 里的**讲义页**：
 *   有比喻、有代码、有真题回链、有实测输出。这才是「怎么讲」的载体。
 *   网页 AI 要教我，最该拿到的其实是这批。
 *
 * 处理：
 *   1. 剥掉 YAML frontmatter，压成一行元信息（日期/难度/章节/考频）
 *   2. 跳过 .bak / index.md / audit-*
 *   3. 每份加「怎么用」抬头
 *
 * 输出：备考计划/网页AI开课包/10-讲义-按节贴/<科目>/
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.join(__dirname, '..');
const DOCS = path.join(REPO, 'docs', 'posts');
const OUT_ROOT = path.join(REPO, '备考计划', '网页AI开课包', '10-讲义-按节贴');

const TODAY = '2026-11-03';

const SUBJECTS = [
  { dir: 'computer', label: '计算机', sub: '计算机（C 语言 + 数据结构）' },
  { dir: 'math', label: '高数', sub: '高等数学' },
  { dir: 'english', label: '英语', sub: '英语' },
  { dir: 'politics', label: '政治', sub: '政治理论' },
];

/** 解析 YAML frontmatter（只取我们要的几个简单标量字段） */
function parseFront(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!m) return { meta: {}, body: text };
  const raw = m[1];
  const body = text.slice(m[0].length);
  const meta = {};
  for (const line of raw.split(/\r?\n/)) {
    // 只认 `key: "value"` / `key: value` 这种单行标量，忽略数组与缩进块
    const kv = line.match(/^([A-Za-z_\u4e00-\u9fa5][\w\u4e00-\u9fa5]*):\s*(.+)$/);
    if (!kv) continue;
    let v = kv[2].trim();
    if (/^\[/.test(v) || /^>|^\||^#/.test(v)) continue;
    v = v.replace(/^["']|["']$/g, '');
    if (v === '' || v === '|' || v === '>') continue;
    meta[kv[1]] = v;
  }
  return { meta, body };
}

function main() {
  let written = 0;
  const rows = [];
  fs.mkdirSync(OUT_ROOT, { recursive: true });

  for (const { dir, label, sub } of SUBJECTS) {
    const src = path.join(DOCS, dir, 'notes');
    if (!fs.existsSync(src)) continue;
    const outDir = path.join(OUT_ROOT, label);
    fs.mkdirSync(outDir, { recursive: true });

    const files = fs
      .readdirSync(src)
      .filter((f) => f.endsWith('.md'))
      .filter((f) => !/\.bak|^index\.md$|^audit-/i.test(f))
      // 政治那份「真题-政治历年2012-2019.md」是 8 套原卷合订（147 KB / 1918 行），
      // 不是讲义。它由 scripts/export-politics-zhenti.mjs 按年拆开单独放。
      .filter((f) => !/^真题-/.test(f))
      .sort((a, b) => a.localeCompare(b, 'zh-Hans-CN', { numeric: true }));

    for (const f of files) {
      const text = fs.readFileSync(path.join(src, f), 'utf8').replace(/\r\n/g, '\n');
      const { meta, body } = parseFront(text);
      const bits = [];
      if (meta.date) bits.push(`日期 ${meta.date}`);
      if (meta.chapter) bits.push(`章节 ${meta.chapter}`);
      if (meta.difficulty) bits.push(`难度 ${meta.difficulty}`);
      if (meta.frequency) bits.push(`考频 ${meta.frequency}`);
      if (meta.mastery) bits.push(`掌握 ${meta.mastery}`);
      const metaLine = bits.length ? bits.join(' · ') : '';

      const title = meta.title || f.replace(/\.md$/, '');
      const desc = meta.description ? `\n> **一句话内容**：${meta.description}` : '';

      // 正文开头若已有同名 H1，去掉 —— 否则文件里会出现两个一模一样的标题
      let bodyOut = body.replace(/^\s*\n/, '');
      const h1 = bodyOut.match(/^#\s+(.+?)\s*\n/);
      if (h1 && h1[1].trim() === title.trim()) {
        bodyOut = bodyOut.slice(h1[0].length).replace(/^\s*\n/, '');
      }

      const out = `# ${title}

> **这是什么**：${sub} 的**讲义页**（不是考点骨架，是「怎么讲」的完整版）${metaLine ? `\n> **元信息**：${metaLine}` : ''}${desc}
> **用法**：先贴 \`0-教练规则\` + 对应科目 \`状态卡\`，再贴本文件，说「按这一节教我」。
> **来源**：\`docs/posts/${dir}/notes/${f}\` · 导出于 ${TODAY}

---

${bodyOut}`;

      const outFile = path.join(outDir, f);
      fs.writeFileSync(outFile, out, 'utf8');
      written++;
      rows.push({
        subject: label,
        kb: Math.round(Buffer.byteLength(out) / 1024),
        chars: [...out].length,
        file: path.relative(OUT_ROOT, outFile).replace(/\\/g, '/'),
      });
    }
  }

  console.log(`=== 已写出 ${written} 份讲义 ===`);
  const by = new Map();
  for (const r of rows) {
    if (!by.has(r.subject)) by.set(r.subject, { n: 0, kb: 0, chars: 0 });
    const a = by.get(r.subject);
    a.n++;
    a.kb += r.kb;
    a.chars += r.chars;
  }
  for (const [s, a] of by) {
    console.log(`${s.padEnd(8)} ${String(a.n).padStart(3)} 份 · ${String(a.kb).padStart(4)} KB · 约 ${a.chars} 字`);
  }
  const sizes = rows.map((r) => r.kb).sort((a, b) => a - b);
  console.log(`单份体积：${sizes[0]}–${sizes[sizes.length - 1]} KB（中位 ${sizes[Math.floor(sizes.length / 2)]} KB）`);
  const big = rows.filter((r) => r.kb > 40);
  if (big.length) {
    console.log(`⚠️ 超过 40 KB 的 ${big.length} 份（贴之前确认上下文够）：`);
    for (const r of big.sort((a, b) => b.kb - a.kb).slice(0, 8)) console.log(`   ${r.kb} KB · ${r.file}`);
  }
}

main();
