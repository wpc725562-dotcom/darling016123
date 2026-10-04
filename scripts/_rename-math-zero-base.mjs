#!/usr/bin/env node
// 给 math 1.x 加 1.Xa 后缀（统一零基础命名约定，参照 computer 1.Xa/b 约定）
// dry-run 默认，--apply 才真改名 + 改 title

import {readFileSync, writeFileSync, renameSync, readdirSync} from 'node:fs';
import {join} from 'node:path';

const APPLY = process.argv.includes('--apply');
const DIR = 'docs/posts/math/notes';

// 收集要改的 (跳过 1.11-极限求值零基础-抓大头.md, 它已带零基础后缀)
const targets = [];
for (const f of readdirSync(DIR)) {
  const m = f.match(/^(1\.\d+)-(.+)\.md$/);
  if (!m) continue;
  const chapter = m[1], rest = m[2];
  if (chapter === '1.11') continue;  // 已含零基础
  if (chapter.endsWith('a') || chapter.endsWith('b')) continue;  // 已是 a/b 版
  // 改名 = 1.X → 1.Xa
  const newName = `${chapter}a-${rest}.md`;
  targets.push({oldName: f, newName, oldPath: join(DIR, f), newPath: join(DIR, newName), chapter});
}

console.log(`=== math 1.x 零基础命名统一计划 ===`);
console.log(`扫描：${readdirSync(DIR).filter(f => /^1\.\d+-/.test(f)).length} 个 1.x 文件`);
console.log(`改名：${targets.length} 个（跳过 1.11-极限求值零基础-抓大头.md）`);
console.log();
for (const t of targets) {
  console.log(`  ${t.oldName}`);
  console.log(`  → ${t.newName}`);
}

if (!APPLY) {
  console.log(`\n提示：传 --apply 才真改名`);
  process.exit(0);
}

console.log(`\n=== 应用 ===`);
for (const t of targets) {
  // 改文件内容里的 title（如果有"1.X"字样但不带 a）
  const c = readFileSync(t.oldPath, 'utf8');
  const c2 = c.replace(/(title:\s*["']?)1\.(\d+)(["']?)/g, (m, p1, p2, p3) => `${p1}1.${p2}a${p3}`);
  writeFileSync(t.oldPath, c2, 'utf8');
  // 改名
  renameSync(t.oldPath, t.newPath);
  console.log(`✓ ${t.oldName} → ${t.newName}`);
}
console.log(`\n完成 ${targets.length} 个文件改名`);
