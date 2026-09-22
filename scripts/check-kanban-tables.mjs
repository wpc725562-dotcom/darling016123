#!/usr/bin/env node
/**
 * 校验 Markdown 表格的列数一致性。
 *
 * 为什么会有它：`学习进度看板.md` 的单行「详情」单元格里塞了大量行内代码，
 * 而 C 语言里 `||`（逻辑或）**天生带两个竖线**。只要忘了转义，整张表就会被撑成
 * 十几列，Markdown 渲染出来是散的 —— 但文件本身完全合法，肉眼扫过去也不报错。
 *
 * 2026-09-20 深夜实测：看板里有 3 行中招（行 252 / 294 / 324），其中 2 行是
 * 之前就有的存量缺陷。修完之后把检查固化成这个脚本。
 *
 * 判据：同一张表（连续以 `|` 开头的行）里，每行的单元格数必须等于表头行。
 * 转义写法 `\|` 和 `\\|` 都算普通字符，不参与切分。
 *
 * 用法：node scripts/check-kanban-tables.mjs [文件路径...]
 *      默认校验 备考计划/学习进度看板.md
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..');
const BS = String.fromCharCode(92); // 反斜杠

const args = process.argv.slice(2);
const files = args.length
  ? args
  : [path.join(ROOT, '备考计划', '学习进度看板.md')];

/** 按未被反斜杠转义的竖线切分；返回的段数含首尾空段 */
function splitCells(line) {
  const segs = [];
  let cur = '';
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '|' && line[i - 1] !== BS) { segs.push(cur); cur = ''; }
    else cur += ch;
  }
  segs.push(cur);
  return segs;
}

let totalBad = 0;

for (const file of files) {
  if (!fs.existsSync(file)) {
    console.log('跳过（不存在）: ' + file);
    continue;
  }
  const lines = fs.readFileSync(file, 'utf8').split('\n');
  const rel = path.relative(ROOT, file) || file;
  console.log('==== ' + rel + ' ====');

  let headerLine = null; // 表头所在行号（1-based）
  let headerCols = 0;
  let bad = 0;

  lines.forEach((line, i) => {
    const t = line.trim();
    if (!t.startsWith('|')) { headerLine = null; return; }

    const cols = splitCells(t).length - 2;
    if (headerLine === null) { headerLine = i + 1; headerCols = cols; return; }
    if (cols !== headerCols) {
      bad++;
      console.log(
        '  X 行' + (i + 1) + ' 列数 ' + cols +
        '，表头行' + headerLine + ' 是 ' + headerCols +
        '  →  ' + t.slice(0, 70)
      );
    }
  });

  if (bad) {
    console.log('  ' + bad + ' 行异常：多半是单元格里有没转义的 `|`（如 `||`），改成 `\\|` 即可');
  } else {
    console.log('  所有表格行列数一致 OK');
  }
  totalBad += bad;
}

console.log();
console.log(totalBad ? '共 ' + totalBad + ' 行异常' : '全部通过');
process.exit(totalBad ? 1 : 0);
