#!/usr/bin/env node
/**
 * 把「非目标视频」的提炼产物归档（不删除，移出主库）
 *
 * 为什么要归档而不是留着
 * --------------------
 * 153 个视频里只有 25 个该提炼（P0+P1）。剩下 111 个是**同质备用池**和**排除项**：
 *   · P2B：高数 4 个同质全程班（陈哥/杰哥/米哥/学士帽），讲的内容和石头老师几乎一样
 *   · P3：高考不考题型（听力/口语/读后续写）、日语课、空壳、噪声字幕
 *
 * 它们的产物如果留在 `_extract/`，学科合并（`_merged.json`）会把
 * 「极限的定义」写 5 遍、把高考听力笔记混进专升本知识库。
 *
 * 归档 ≠ 删除：万一某天要查「陈哥怎么讲极限」，产物还在 `_archive/`。
 *
 * 用法
 * ----
 *   node scripts/bili-archive-nontarget.mjs                      # 干跑，按 P2B+P3
 *   node scripts/bili-archive-nontarget.mjs --write              # 真移
 *   node scripts/bili-archive-nontarget.mjs --tier=P3 --write    # 只归档 P3
 *   node scripts/bili-archive-nontarget.mjs --restore            # 从 _archive/ 搬回来
 *
 * 归档后必须重新生成合并产物：
 *   node scripts/bili_merge_extract.mjs   （或仓库里对应的 merge 命令）
 * 否则 `_merged.json` 里还留着已归档的 unit。
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = 'D:/deeepseek/zhuan-sheng-ben-notes';
const EXTRACT = path.join(ROOT, 'data/bili-analyze/_extract');
const ARCHIVE = path.join(EXTRACT, '_archive');
const TARGETS = path.join(EXTRACT, '_target-videos.json');

const argv = process.argv.slice(2);
const WRITE = argv.includes('--write');
const RESTORE = argv.includes('--restore');
const TIER_OPT = (argv.find((x) => x.startsWith('--tier=')) || '').split('=')[1] || 'P2B,P3';

if (!fs.existsSync(TARGETS)) {
  console.error('✗ 找不到 _target-videos.json，先跑筛选');
  process.exit(2);
}
const j = JSON.parse(fs.readFileSync(TARGETS, 'utf8'));
const tiers = j.tiers || {};
const want = new Set(TIER_OPT.split(',').map((s) => s.trim()).filter(Boolean));

const bvTier = {};
for (const [t, arr] of Object.entries(tiers)) for (const x of arr) bvTier[x.bv] = t;

const tierOf = (unitId) => bvTier[unitId.replace(/_\d+$/, '')] || 'UNKNOWN';

fs.mkdirSync(ARCHIVE, { recursive: true });

if (RESTORE) {
  const files = fs.readdirSync(ARCHIVE).filter((f) => /^BV.*\.md$/.test(f));
  console.log(`从 _archive/ 搬回 ${files.length} 个产物`);
  for (const f of files) {
    if (fs.existsSync(path.join(EXTRACT, f))) {
      console.log(`  ⚠ ${f} 主库已有同名文件，跳过`);
      continue;
    }
    if (WRITE) fs.renameSync(path.join(ARCHIVE, f), path.join(EXTRACT, f));
    else console.log(`  · ${f}`);
  }
  if (!WRITE) console.log('\n干跑结束，加 --write 执行');
  process.exit(0);
}

const mds = fs.readdirSync(EXTRACT).filter((f) => /^BV.*\.md$/.test(f));
const picked = [];
const byTier = {};
for (const f of mds) {
  const name = f.replace(/\.md$/, '');
  const t = tierOf(name);
  if (!want.has(t)) continue;
  const st = fs.statSync(path.join(EXTRACT, f));
  picked.push({ f, name, t, size: st.size });
  byTier[t] = (byTier[t] || 0) + 1;
}

console.log(`目标分级：${[...want].join(',')}`);
console.log(`主库产物 ${mds.length} 个 → 命中 ${picked.length} 个（${Object.entries(byTier).map(([k, v]) => `${k}=${v}`).join(' ')}）`);

if (!picked.length) { console.log('没有需要归档的。'); process.exit(0); }

// 台账：谁被归档了、为什么
const lines = [
  '# 归档台账 · 非目标视频的提炼产物',
  '',
  `> 生成于 ${new Date().toISOString().slice(0, 19).replace('T', ' ')}，分级 ${[...want].join(' / ')}`,
  '> 依据 `_TARGET-VIDEOS.md`：P2B 是同质备用池、P3 是排除项（不考题型 / 非四科 / 空壳 / 噪声）。',
  '> **归档不是删除** —— 要查某个备用源怎么讲某章，产物还在这里。',
  '>',
  '> 恢复：`node scripts/bili-archive-nontarget.mjs --restore --write`',
  '',
  '| 单元 | 分级 | 体积 | 归档理由 |',
  '|---|:--:|--:|---|',
];
for (const p of picked.sort((a, b) => a.name.localeCompare(b.name))) {
  const bv = p.name.replace(/_\d+$/, '');
  const meta = (tiers[p.t] || []).find((x) => x.bv === bv) || {};
  const why = meta.why || '';
  lines.push(`| \`${p.name}\` | ${p.t} | ${(p.size / 1024).toFixed(0)}KB | ${why.replace(/\|/g, '｜')} |`);
}
lines.push('');
lines.push(`合计 ${picked.length} 个产物 / ${(picked.reduce((s, p) => s + p.size, 0) / 1048576).toFixed(1)} MB`);
lines.push('');

if (!WRITE) {
  console.log('\n干跑结束。加 --write 执行。');
  for (const p of picked.slice(0, 15)) console.log(`  · ${p.name}  [${p.t}] ${(p.size / 1024).toFixed(0)}KB`);
  if (picked.length > 15) console.log(`  … 其余 ${picked.length - 15} 个`);
  process.exit(0);
}

for (const p of picked) fs.renameSync(path.join(EXTRACT, p.f), path.join(ARCHIVE, p.f));
fs.writeFileSync(path.join(ARCHIVE, '_MANIFEST.md'), lines.join('\n'), 'utf8');
console.log(`\n已归档 ${picked.length} 个 → _extract/_archive/`);
console.log('台账：_extract/_archive/_MANIFEST.md');
console.log('⚠ 下一步必须重新生成合并产物，否则 _merged.json 里还留着已归档的 unit');
