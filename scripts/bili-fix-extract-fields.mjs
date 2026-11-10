#!/usr/bin/env node
/**
 * 修「要点」缺标签的产物（不重提炼，只补格式）
 *
 * 问题长什么样
 * ------------
 * 规范要求每个 `###` 下四行：要点 / 关键概念 / 相互关系 / 出处。
 * 但模型常把「要点」写成**无标签的正文首行**：
 *
 *     ### UNIX与C语言的历史渊源
 *     - 肯·汤普森和丹尼斯·里奇在1969年开发了极简版UNIX操作系统…   ← 缺 `- **要点**：`
 *     - **关键概念**：`UNIX`、`汇编语言`…
 *     - **相互关系**：…
 *     - **出处**：P1
 *
 * 校验器判 C5「缺要点」是对的，但**内容是全的**，补个标签就行。
 * 重提炼一个 100k 字符的单元要 3 片 × 45 秒，而补标签是毫秒级。
 *
 * 用法
 * ----
 *   node scripts/bili-fix-extract-fields.mjs                 # 干跑，报可修数
 *   node scripts/bili-fix-extract-fields.mjs --write         # 真改（备份到 _fieldbak/）
 *   node scripts/bili-fix-extract-fields.mjs --only=BV11T411q7Qw
 *
 * 只处理「要点缺失 + 首行是裸文本」这一种。其它缺陷（整块只有一句话、
 * 出处指向不存在的 P 号）不动 —— 那些要重提炼。
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = 'D:/deeepseek/zhuan-sheng-ben-notes';
const EXTRACT = path.join(ROOT, 'data/bili-analyze/_extract');
const BAK = path.join(EXTRACT, '_fieldbak');

const argv = process.argv.slice(2);
const WRITE = argv.includes('--write');
const ONLY = (argv.find((x) => x.startsWith('--only=')) || '').split('=')[1] || '';

const FIELD_RE = /^-\s*\*\*(要点|关键概念|相互关系|出处)\*\*\s*[：:]/;
const ANY_FIELD_RE = /^-\s*\*\*(要点|关键概念|相互关系|出处)\*\*/;

const files = fs.readdirSync(EXTRACT).filter((f) => /^BV.*\.md$/.test(f))
  .filter((f) => !ONLY || f.startsWith(ONLY));

let totalFixed = 0, totalFiles = 0;
const details = [];

for (const f of files) {
  const p = path.join(EXTRACT, f);
  const raw = fs.readFileSync(p, 'utf8');
  const eol = raw.includes('\r\n') ? '\r\n' : '\n';
  const lines = raw.split(/\r?\n/);

  // 按 ### 切块
  const idx = [];
  lines.forEach((l, i) => { if (/^###\s+/.test(l)) idx.push(i); });
  if (!idx.length) continue;

  const out = lines.slice();
  let fixed = 0;
  // 从后往前改，避免下标位移
  for (let k = idx.length - 1; k >= 0; k--) {
    const start = idx[k];
    const end = k + 1 < idx.length ? idx[k + 1] : lines.length;
    const block = lines.slice(start + 1, end);
    const hasPoint = block.some((l) => /^-\s*\*\*要点\*\*/.test(l));
    if (hasPoint) continue;
    // 找第一个非空行
    let j = 0;
    while (j < block.length && !block[j].trim()) j++;
    if (j >= block.length) continue;
    const first = block[j];
    // 只处理「裸文本行」：以 `- ` 开头但没有 `**`，或者压根不是列表项
    const bare = (first.startsWith('- ') && !first.includes('**')) || (!first.startsWith('- ') && !ANY_FIELD_RE.test(first));
    if (!bare) continue;
    // 若首行本身就是别的字段（关键概念等），说明真的缺要点，不硬塞
    if (ANY_FIELD_RE.test(first)) continue;
    const content = first.replace(/^-\s*/, '').trim();
    if (!content) continue;
    out[start + 1 + j] = `- **要点**：${content}`;
    fixed++;
  }
  if (!fixed) continue;

  totalFiles++;
  totalFixed += fixed;
  details.push({ f, fixed });
  if (WRITE) {
    fs.mkdirSync(BAK, { recursive: true });
    fs.writeFileSync(path.join(BAK, f), raw, 'utf8');
    fs.writeFileSync(p, out.join(eol), 'utf8');
  }
}

console.log(`${WRITE ? '已修' : '可修'} ${totalFiles} 个文件 / ${totalFixed} 个块`);
for (const d of details.sort((a, b) => b.fixed - a.fixed)) console.log(`  ${WRITE ? '✓' : '·'} ${d.f}  +${d.fixed}`);
if (!WRITE && totalFiles) console.log('\n干跑结束，加 --write 执行（备份到 _extract/_fieldbak/）');
if (WRITE && totalFiles) console.log('\n下一步：node scripts/check-extract.mjs --all   # 复核');
