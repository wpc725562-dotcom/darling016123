#!/usr/bin/env node
/**
 * 检测「单元内容与字幕源是否对齐」
 *
 * 为什么需要这个检测
 * ----------------
 * `bili_filter_units.py` 只按 `_verify.jsonl` / `_verify2.jsonl` 的 **p 号** 判 ok，
 * 它校验的是「这个分P 是不是这门课」，**不是**「单元文件里这段字是不是这个分P 的字幕」。
 *
 * 两层校验之间有个结构性的洞：
 *   2026-09-18 建单元时字幕是串台的（B 站 x/player/v2 约 68% 概率返回别的视频字幕轨）
 *   2026-09-19 00:49 字幕重新下载成正确版本
 *   但单元文件没重建 ⇒ `_units_verified/` 里留着「段头写 P62 讲 static，正文是三国演义段子」
 *
 * 而 P62 在 B 站上**确实是** C 语言课，aid+cid 与标题词重合度都通过
 * （cos=0.84 / ov=0.80 / verdict=trusted）—— 所以 verify 全绿，内容却是错的。
 *
 * 检测原理
 * --------
 * 对单元里每个 `=== Pn |` 段，取段内最长的 3 行（≥8 字）当指纹，
 * 看它是否出现在 `subtitle_pNN.txt` 里。一次都不中 ⇒ 该段错位。
 *
 * 首次实测（2026-10-22）：434 个单元里 **51 个错位，错位段 747/1153 = 64.8%**
 * —— 与「68% 概率串台」高度吻合，反证检测有效。
 *
 * 用法
 * ----
 *   node scripts/check-unit-align.mjs              # 全量，只报数
 *   node scripts/check-unit-align.mjs --verbose    # 列出每个错位单元与分P
 *   node scripts/check-unit-align.mjs --only=BV17a7K64ELH
 *
 * 修复：`node scripts/bili-rebuild-units.mjs --write`
 * 退出码：有错位 → 1（方便挂进 CI / 跑批前置检查）
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = 'D:/deeepseek/zhuan-sheng-ben-notes';
const DATA = path.join(ROOT, 'data/bili-analyze');
const VERIFIED = path.join(DATA, '_units_verified');

const argv = process.argv.slice(2);
const VERBOSE = argv.includes('--verbose');
const ONLY = (argv.find((x) => x.startsWith('--only=')) || '').split('=')[1] || '';

const files = fs.readdirSync(VERIFIED).filter((f) => /^BV.*_\d+\.txt$/.test(f));
const rows = [];
for (const f of files) {
  const unit = f.replace(/\.txt$/, '');
  if (ONLY && !unit.startsWith(ONLY)) continue;
  const bv = unit.replace(/_\d+$/, '');
  const dir = path.join(DATA, bv);
  if (!fs.existsSync(dir)) { rows.push({ unit, bv, bad: -1, tot: 0, badList: ['无字幕目录'] }); continue; }
  const u = fs.readFileSync(path.join(VERIFIED, f), 'utf8');
  const segs = [...u.matchAll(/^=== P(\d+) \|([^\n]*)===\s*$/gm)];
  let bad = 0, tot = 0;
  const badList = [];
  for (let i = 0; i < segs.length; i++) {
    const p = Number(segs[i][1]);
    const start = segs[i].index + segs[i][0].length;
    const end = i + 1 < segs.length ? segs[i + 1].index : u.length;
    const body = u.slice(start, end).trim();
    if (body.length < 30) continue;
    const sp = path.join(dir, `subtitle_p${String(p).padStart(2, '0')}.txt`);
    if (!fs.existsSync(sp)) continue;
    tot++;
    const sub = fs.readFileSync(sp, 'utf8');
    const cand = body.split(/\r?\n/).map((l) => l.trim()).filter((l) => l.length >= 8)
      .sort((a, b) => b.length - a.length).slice(0, 3);
    if (!cand.length) { tot--; continue; }
    if (!cand.some((c) => sub.includes(c))) { bad++; badList.push(`P${p}`); }
  }
  rows.push({ unit, bv, bad, tot, badList });
}

const ok = rows.filter((r) => r.tot > 0 && r.bad === 0);
const badRows = rows.filter((r) => r.bad > 0);
const noSub = rows.filter((r) => r.bad === -1);
const segsBad = badRows.reduce((s, r) => s + r.bad, 0);
const segsTot = badRows.reduce((s, r) => s + r.tot, 0) || 1;

console.log(`单元 ${rows.length} | 对齐 ${ok.length} | 错位 ${badRows.length} | 无字幕 ${noSub.length}`);
if (badRows.length) {
  console.log(`错位段 ${segsBad} / 检查段 ${segsTot} = ${(segsBad / segsTot * 100).toFixed(1)}%`);
  const byBv = {};
  for (const r of badRows) byBv[r.bv] = (byBv[r.bv] || 0) + 1;
  console.log('按视频：' + Object.entries(byBv).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k}×${v}`).join(' '));
  if (VERBOSE) {
    console.log('');
    for (const r of badRows.sort((a, b) => (b.bad / b.tot) - (a.bad / a.tot))) {
      console.log(`  ${r.unit}  ${r.bad}/${r.tot}  ${r.badList.slice(0, 8).join(',')}`);
    }
  }
  console.log('\n修复：node scripts/bili-rebuild-units.mjs --write');
  process.exit(1);
}
console.log('全部对齐。');
