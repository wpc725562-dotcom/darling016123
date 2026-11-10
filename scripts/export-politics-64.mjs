/* 导出政治 64 篇必背原文，供其他 AI 读取。
   源：00-政治默写册-毛中特21篇.md / 00-政治默写册-习概43篇.md
   取「答案区」原文 + 「默写区」的考频/题型/章节元信息 + 真题回放表。
   原文按每行约 30 字硬换行，导出时重排为自然段落，不删改任何字。
   用法：node scripts/export-politics-64.mjs [输出路径] */

import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');
const SRC = path.join(ROOT, '资料/电子书蒸馏');
const OUT = process.argv[2] || path.join(ROOT, '导出/政治必背64篇-原文.md');

const BOOKS = [
  { file: '00-政治默写册-毛中特21篇.md', label: '毛中特', count: 21 },
  { file: '00-政治默写册-习概43篇.md', label: '习概', count: 43 },
];

/* 这些开头是新块，不与上一行合并 */
const BLOCK_START = /^\s*(#{1,6}\s|【|[·•]|[-*+]\s|\d+[.、]\s?|[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]|\||>|×|√|---|```)/;
/* 缩进后仍算新项的符号（缩进列表） */
const INDENT_ITEM = /^\s{2,}([·•]|[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]|\d+[.、]|[-*+]\s)/;

function joinSmart(prev, next) {
  const a = prev.slice(-1);
  const b = next.charAt(0);
  const ascii = /[A-Za-z0-9)]/;
  return ascii.test(a) && ascii.test(b) ? prev + ' ' + next : prev + next;
}

/* 把硬换行重排成自然段 */
function reflow(md) {
  const out = [];
  for (const raw of md.split('\n')) {
    const line = raw.replace(/\s+$/, '');
    if (!line.trim()) { out.push(''); continue; }

    const prev = out.length ? out[out.length - 1] : '';
    const indented = /^\s{2,}/.test(raw);
    const startsBlock = BLOCK_START.test(line);
    const isIndentItem = INDENT_ITEM.test(raw);

    // 缩进续行 → 无条件并入上一行（缩进的新列表项除外）
    if (indented && !isIndentItem && prev) {
      out[out.length - 1] = joinSmart(prev, line.trim());
      continue;
    }
    // 顶格续行 → 并入上一行
    if (!indented && !startsBlock && prev && !BLOCK_START.test(prev)) {
      out[out.length - 1] = joinSmart(prev, line);
      continue;
    }
    out.push(line);
  }
  // 压缩连续空行
  return out.join('\n').replace(/\n{3,}/g, '\n\n');
}

/* 按 `## NN｜...` 切篇 */
function splitArticles(text) {
  const chunks = text.split(/\n(?=## \d{2}｜)/);
  return chunks.slice(1).map((chunk) => {
    const lines = chunk.split('\n');
    const head = lines[0].replace(/^##\s*/, '').trim();
    return { head, body: lines.slice(1).join('\n') };
  });
}

/* 从默写区篇身取：元信息行 + 真题回放表 */
function parseQuizBody(body) {
  const lines = body.split('\n');
  const meta = lines.find((l) => l.includes('考频')) || '';
  const table = [];
  let inTable = false;
  for (const l of lines) {
    if (/^\*\*真题回放\*\*/.test(l.trim())) { table.push(l.trim()); inTable = true; continue; }
    if (inTable) {
      if (/^\|/.test(l)) { table.push(l.trim()); continue; }
      if (l.trim() === '') continue;
      break;
    }
  }
  return { meta: meta.trim(), table };
}

/* 答案区：拆「第一遍 / 第二遍」 */
function splitAnswer(body) {
  const idx = body.search(/###\s*第二遍/);
  if (idx < 0) return { must: body, disc: '' };
  return {
    must: body.slice(0, idx),
    disc: body.slice(idx),
  };
}

function cleanAnswerBlock(s) {
  return s.replace(/^\s*###\s*第[一二]遍[^\n]*\n?/, '').trim();
}

const parts = [];
let totalChars = 0;
const toc = [];

for (const book of BOOKS) {
  const text = fs.readFileSync(path.join(SRC, book.file), 'utf8');
  const ansAt = text.indexOf('# 第二部分');
  if (ansAt < 0) throw new Error(book.file + ' 找不到第二部分');
  const quiz = splitArticles(text.slice(0, ansAt));
  const ans = splitArticles(text.slice(ansAt));

  if (quiz.length !== ans.length) {
    throw new Error(`${book.label} 篇数不一致：默写区 ${quiz.length} / 答案区 ${ans.length}`);
  }

  parts.push(`\n\n---\n\n# ${book.label}（${book.count} 篇）\n`);

  ans.forEach((a, i) => {
    const q = quiz[i];
    const { meta, table } = parseQuizBody(q.body);
    const { must, disc } = splitAnswer(a.body);
    const mustText = cleanAnswerBlock(must);
    const discText = cleanAnswerBlock(disc);

    const seq = a.head.slice(0, 2);
    const rest = a.head.slice(3).trim();
    toc.push(`| ${book.label} ${seq} | ${rest} |`);

    let sec = `\n## ${book.label}-${seq}　${rest}\n\n`;
    if (meta) sec += meta + '\n\n';
    if (table.length) {
      sec += table[0] + '\n\n' + table.slice(1).join('\n') + '\n\n';
    }
    sec += `### 必背要点（原文）\n\n${reflow(mustText)}\n`;
    if (discText) sec += `\n### 易错辨析（原文）\n\n${reflow(discText)}\n`;
    parts.push(sec);

    totalChars += mustText.replace(/\s/g, '').length;
  });
}

const header = `# 广东专升本 · 政治必背 64 篇（原文合辑）

> **用途**：供 AI 阅读、出题、背诵检查、批改使用。内容为考点笔记原文照抄，未改写、未增补。
> **来源**：\`资料/电子书蒸馏/01-毛中特/考点笔记/\` 与 \`02-习概/考点笔记/\`，经 \`00-政治默写册\` 汇编。
> **规模**：毛中特 21 篇 + 习概 43 篇 = 64 篇，必背要点正文约 ${Math.round(totalChars / 1000)} 千字。
> **生成**：2026-11-05，脚本 \`scripts/export-politics-64.mjs\`。

## 给 AI 的读法说明

1. **每篇结构统一**：标题 → \`考频 / 题型 / 章节\` 元信息 → 真题回放表 → \`必背要点（原文）\` → \`易错辨析（原文）\`。
2. **【】方括号是骨架标签**，如【总述】【（一）实事求是】。标签本身也是考点结构的一部分，出题时不要省略。
3. **数字编号（1. 2. 3.）是必背条目**，考试按条给分。条目里的「定位 / 含义 / 形成脉络 / 三个就要」是这一条的小标题。
4. **「×」开头是错误命题，「√」开头是正确表述**，用于辨析题。注意：真题里真命题是按比例掺进去的，不是一对一错。
5. **引号内是原文引用**，尤其毛泽东著作原话与党的文献表述，不可改动字词。
6. **考频 ★ 数越多，真题命中次数越高**。★★★★★ 为最高频。
7. 需要针对某篇出题时，请严格以「必背要点」的条目为单位，一条一题或一题多问，不要引入原文之外的表述。

## 目录

| 编号 | 考点 |
|:---|:---|
${toc.join('\n')}
`;

fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, header + parts.join(''), 'utf8');

const size = fs.statSync(OUT).size;
console.log(`✅ ${OUT}`);
console.log(`   ${toc.length} 篇 · 必背正文 ${totalChars} 字 · 文件 ${(size / 1024).toFixed(1)} KB`);
