#!/usr/bin/env node
/**
 * 存量产物首行/覆盖行回填器
 *
 * 背景：模型看到 B 站那种带关键词堆砌的长标题会自己"整理"，
 * 把 `【】` 改成 `（）`、把 UP 主括注重复一遍。存量 235 个产物里 27 个是这个问题。
 * 输入文件头 4 行本来就有权威值，直接回填即可，不用重跑模型。
 *
 * 用法：
 *   node scripts/bili-fix-extract-head.mjs            # 干跑，只报告会改什么
 *   node scripts/bili-fix-extract-head.mjs --write    # 真改（改前备份到 _extract/_headbak/）
 *   node scripts/bili-fix-extract-head.mjs --only=BV17a7K64ELH
 *
 * 只改第 1 行（标题）与第 2 行（覆盖行），正文一个字不碰。
 * 覆盖行按输入单元实际的 P 范围与节数重算，不采信产物里写的。
 */
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const ROOT = 'D:/deeepseek/zhuan-sheng-ben-notes';
const DATA = path.join(ROOT, 'data/bili-analyze');
const UNITS = path.join(DATA, '_units_verified');
const EXTRACT = path.join(DATA, '_extract');
const BAK = path.join(EXTRACT, '_headbak');

const argv = process.argv.slice(2);
const WRITE = argv.includes('--write');
const ONLY = (argv.find((a) => a.startsWith('--only=')) || '').split('=')[1] || '';

function unitHead(name) {
  const raw = fs.readFileSync(path.join(UNITS, `${name}.txt`), 'utf8');
  const lines = raw.split(/\r?\n/);
  const h = {};
  for (const l of lines.slice(0, 8)) {
    const m = l.match(/^#\s*(unit|学科|视频)\s*[:：]\s*(.+)$/);
    if (m) h[m[1]] = m[2].trim();
  }
  const pages = [...raw.matchAll(/^=== P(\d+) \|/gm)].map((x) => Number(x[1]));
  return {
    h1: `# ${h.unit || name} · ${h['学科'] || ''} · ${h['视频'] || ''}`,
    h2: `> 覆盖：P${Math.min(...pages)}–P${Math.max(...pages)}（${pages.length} 节）`,
  };
}

/** 用 check-extract 判断该产物除了 C1/C2 之外还有没有别的问题 */
function onlyHeadErrors(name, mdPath) {
  const c = spawnSync(process.execPath, [path.join(ROOT, 'scripts/check-extract.mjs'),
    path.join(UNITS, `${name}.txt`), mdPath], { encoding: 'utf8' });
  const errs = (c.stdout || '').split('\n').filter((l) => /^\s+✗ C\d/.test(l));
  if (!errs.length) return { clean: true, errs };
  const other = errs.filter((l) => !/✗ C[12]\b/.test(l));
  return { clean: false, onlyHead: other.length === 0, errs };
}

const mds = fs.readdirSync(EXTRACT).filter((f) => /^BV.*\.md$/.test(f));
let fixed = 0, skipped = 0, needRework = [];
const changes = [];

for (const f of mds) {
  const name = f.replace(/\.md$/, '');
  if (ONLY && !name.startsWith(ONLY)) continue;
  if (!fs.existsSync(path.join(UNITS, `${name}.txt`))) { skipped++; continue; }
  const mdPath = path.join(EXTRACT, f);
  const r = onlyHeadErrors(name, mdPath);
  if (r.clean) continue;
  if (!r.onlyHead) { needRework.push(name); continue; }

  const want = unitHead(name);
  const raw = fs.readFileSync(mdPath, 'utf8');
  const EOL = raw.includes('\r\n') ? '\r\n' : '\n';   // 保住原文件的换行风格，别把整个文件重写一遍
  const lines = raw.split(/\r?\n/);
  // 找到第一条非空行（标题）与紧随的覆盖行
  let i = 0;
  while (i < lines.length && !lines[i].trim()) i++;
  const oldH1 = lines[i] || '';
  let j = i + 1;
  while (j < lines.length && !lines[j].trim()) j++;
  const oldH2 = lines[j] || '';
  const body = lines.slice(j + 1).join(EOL);

  changes.push({ name, oldH1, newH1: want.h1, oldH2, newH2: want.h2 });
  if (WRITE) {
    fs.mkdirSync(BAK, { recursive: true });
    fs.writeFileSync(path.join(BAK, f), raw, 'utf8');
    fs.writeFileSync(mdPath, `${want.h1}${EOL}${EOL}${want.h2}${EOL}${body}`, 'utf8');
  }
  fixed++;
}

console.log(`═══ 首行/覆盖行回填 ${WRITE ? '（已写入）' : '（干跑）'} ═══`);
for (const c of changes) {
  console.log(`\n${c.name}`);
  if (c.oldH1 !== c.newH1) console.log(`  标题  - ${c.oldH1.slice(0, 90)}\n        + ${c.newH1.slice(0, 90)}`);
  if (c.oldH2 !== c.newH2) console.log(`  覆盖  - ${c.oldH2.slice(0, 70)}\n        + ${c.newH2.slice(0, 70)}`);
}
console.log(`\n可回填 ${fixed} 个 | 需重提炼 ${needRework.length} 个 | 跳过（无输入单元）${skipped} 个`);
if (needRework.length) console.log(`需重提炼：${needRework.join(', ')}`);
if (!WRITE && fixed) console.log('\n加 --write 才会真改（改前备份到 _extract/_headbak/）。');
