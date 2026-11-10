#!/usr/bin/env node
/**
 * 政治默写册 · 按篇拆分器
 *
 * 为什么需要它：
 *   两本默写册合计 483 KB（毛中特 178 KB / 习概 305 KB），整本贴不进网页 AI。
 *   但 A 档是「一天一篇」，一天只需要那一篇 —— 所以按篇切成 64 个文件，
 *   每个含【默写区（只给标签和字数）+ 答案区（原文）】，
 *   网页 AI 既能抽默写、又能判分。
 *
 * 输出：备考计划/网页AI开课包/8-政治默写-按篇贴/<毛中特|习概>-篇NN-<名>.md
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.join(__dirname, '..');
const DIST = path.join(REPO, '资料', '电子书蒸馏');
const OUT_ROOT = path.join(REPO, '备考计划', '网页AI开课包', '8-政治默写-按篇贴');

const TODAY = '2026-11-03';
const BOOKS = [
  { file: '00-政治默写册-毛中特21篇.md', book: '毛中特' },
  { file: '00-政治默写册-习概43篇.md', book: '习概' },
];

/** 把一本书按 `# 第X部分` 切成两段 */
function splitParts(text) {
  const lines = text.split('\n');
  const parts = { pre: [], quiz: [], answer: [] };
  let cur = 'pre';
  for (const ln of lines) {
    if (/^#\s+第一部分/.test(ln)) { cur = 'quiz'; continue; }
    if (/^#\s+第二部分/.test(ln)) { cur = 'answer'; continue; }
    parts[cur].push(ln);
  }
  return {
    pre: parts.pre.join('\n'),
    quiz: parts.quiz.join('\n'),
    answer: parts.answer.join('\n'),
  };
}

/** 把一段按 `## NN｜…` 切成 篇号 → 内容 的映射 */
function splitPieces(text) {
  const out = new Map();
  const lines = text.split('\n');
  let cur = null;
  let buf = [];
  const flush = () => {
    if (cur !== null) out.set(cur.no, { ...cur, body: buf.join('\n').trim() });
  };
  for (const ln of lines) {
    const m = ln.match(/^##\s+(\d{1,3})｜\s*(.+)$/);
    if (m) {
      flush();
      const no = parseInt(m[1], 10);
      const rest = m[2].trim();
      // rest 形如「毛 1-2-2　毛泽东思想活的灵魂」（考点编号与篇名之间是全角空格 U+3000）
      // ⚠️ 不能用 /(\S+)\s+(.+)/：JS 的 \s 会把全角空格也吃掉，
      //    结果 code 只剩「毛」、name 变成「1-2-2　毛泽东思想…」，文件名就错位了。
      const idx = rest.indexOf('　');
      const code = idx > 0 ? rest.slice(0, idx).trim() : rest;
      const name = idx > 0 ? rest.slice(idx + 1).trim() : rest;
      cur = { no, code, name, raw: rest };
      buf = [];
    } else if (cur !== null) {
      buf.push(ln);
    }
  }
  flush();
  return out;
}

function safeName(s) {
  return s.replace(/[\\/:*?"<>|　\s]+/g, '').slice(0, 40);
}

function main() {
  let count = 0;
  const rows = [];
  fs.mkdirSync(OUT_ROOT, { recursive: true });

  for (const { file, book } of BOOKS) {
    const full = path.join(DIST, file);
    if (!fs.existsSync(full)) {
      console.error(`❌ 找不到 ${full}`);
      continue;
    }
    const text = fs.readFileSync(full, 'utf8').replace(/\r\n/g, '\n');
    const { quiz, answer } = splitParts(text);
    const qz = splitPieces(quiz);
    const an = splitPieces(answer);

    for (const no of [...qz.keys()].sort((a, b) => a - b)) {
      const q = qz.get(no);
      const a = an.get(no);
      const title = `${book} · 第 ${String(no).padStart(2, '0')} 篇 · ${q.code} ${q.name}`;
      const content = `# 政治默写 · ${title}

> **来源**：\`资料/电子书蒸馏/${file}\` · 导出于 ${TODAY}
> **用法**：先贴 \`0-教练规则\` + \`5-政治-状态卡\`，再贴本文件，说「抽我第 ${String(no).padStart(2, '0')} 篇」。
> **判分口径**：踩点给分，**只认原词**，不认同义改写。
> ⚠️ **本文件含答案。** 先只看「一、默写区」，默完再往下看「二、答案区」。

---

## 一、默写区（只给标签和字数）

${q.body}

---

## 二、答案区（我默完再给我看）

${a ? a.body : '> ⚠️ 本篇答案区未找到，请查原书。'}
`;
      const outName = `${book}-篇${String(no).padStart(2, '0')}-${safeName(q.code)}-${safeName(q.name)}.md`;
      const outFile = path.join(OUT_ROOT, outName);
      fs.writeFileSync(outFile, content, 'utf8');
      count++;
      rows.push({
        book,
        no: String(no).padStart(2, '0'),
        name: q.name,
        kb: Math.round(Buffer.byteLength(content) / 1024),
        file: outName,
        hasAnswer: !!a,
      });
    }
  }

  console.log(`=== 已写出 ${count} 篇 ===`);
  const byBook = new Map();
  for (const r of rows) {
    if (!byBook.has(r.book)) byBook.set(r.book, { n: 0, kb: 0, miss: 0 });
    const b = byBook.get(r.book);
    b.n++;
    b.kb += r.kb;
    if (!r.hasAnswer) b.miss++;
  }
  for (const [b, v] of byBook) {
    console.log(`${b}  ${v.n} 篇 · ${v.kb} KB${v.miss ? ` · ⚠️ ${v.miss} 篇缺答案` : ''}`);
  }
  const sizes = rows.map((r) => r.kb);
  console.log(`单篇体积：${Math.min(...sizes)}–${Math.max(...sizes)} KB`);
  const big = rows.filter((r) => r.kb > 20);
  if (big.length) console.log(`⚠️ 超过 20 KB：${big.map((r) => r.file).join(', ')}`);
}

main();
