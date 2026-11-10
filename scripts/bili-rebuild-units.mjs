#!/usr/bin/env node
/**
 * 修复「单元内容与字幕源错位」的单元（原地重建，id 不变）
 *
 * 背景
 * ----
 * 2026-09-18 建单元时用的字幕是**串台**的（B 站 x/player/v2 约 68% 概率返回别的视频的字幕轨）。
 * 2026-09-19 00:49 字幕重新下载成正确版本，但**单元文件没重建** ——
 * `_units_verified/` 里留着一批「段头写 P62 讲 static，正文是三国演义段子」的单元。
 *
 * 为什么 `bili_filter_units.py` 拦不住
 * ----------------------------------
 * 它只按 `_verify.jsonl` / `_verify2.jsonl` 里的 **p 号** 判 ok。
 * 而 P62 在 B 站上**确实是** C 语言课，aid+cid 与标题词重合度都通过
 * （cos=0.84 / ov=0.80 / verdict=trusted）——
 * 校验对象是「这个分P 是不是这门课」，不是「单元文件里这段字是不是这个分P 的字幕」。
 * 两层校验之间存在一个**结构性的洞**。
 *
 * 检测方法（见 `check-unit-align.mjs`）
 * ------------------------------------
 * 对单元里每个 `=== Pn |` 段，取段内最长的 3 行当指纹，
 * 看它是否出现在 `subtitle_pNN.txt` 里。一次都不中 ⇒ 该段错位。
 *
 * 实测：434 个单元里 51 个错位，错位段 747/1153 = **64.8%**
 * —— 与「68% 概率串台」高度吻合，反证了检测是对的。
 *
 * 用法
 * ----
 *   node scripts/bili-rebuild-units.mjs              # 干跑，只列清单
 *   node scripts/bili-rebuild-units.mjs --write      # 真改（原文件备份到 _units/_stale/）
 *   node scripts/bili-rebuild-units.mjs --write --only=BV17a7K64ELH
 *
 * ⚠️ 重建后**必须重跑提炼**：已提炼的产物是基于错位内容生成的，全是垃圾。
 *    脚本会把对应的 `_extract/<unit>.md` 移到 `_extract/_bad/`。
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = 'D:/deeepseek/zhuan-sheng-ben-notes';
const DATA = path.join(ROOT, 'data/bili-analyze');
const UNITS = path.join(DATA, '_units');
const VERIFIED = path.join(DATA, '_units_verified');
const EXTRACT = path.join(DATA, '_extract');
const STALE = path.join(UNITS, '_stale');
const BAD = path.join(EXTRACT, '_bad');

const argv = process.argv.slice(2);
const WRITE = argv.includes('--write');
const ONLY = (argv.find((x) => x.startsWith('--only=')) || '').split('=')[1] || '';

/** 检测一个单元里哪些分P 段错位 */
function detect(unitId) {
  const up = path.join(VERIFIED, `${unitId}.txt`);
  if (!fs.existsSync(up)) return null;
  const bv = unitId.replace(/_\d+$/, '');
  const dir = path.join(DATA, bv);
  const u = fs.readFileSync(up, 'utf8');
  const segs = [...u.matchAll(/^=== P(\d+) \|([^\n]*)===\s*$/gm)];
  const bad = [];
  for (let i = 0; i < segs.length; i++) {
    const p = Number(segs[i][1]);
    const start = segs[i].index + segs[i][0].length;
    const end = i + 1 < segs.length ? segs[i + 1].index : u.length;
    const body = u.slice(start, end).trim();
    if (body.length < 30) continue;
    const sp = path.join(dir, `subtitle_p${String(p).padStart(2, '0')}.txt`);
    if (!fs.existsSync(sp)) continue;
    const sub = fs.readFileSync(sp, 'utf8');
    const cand = body.split(/\r?\n/).map((l) => l.trim()).filter((l) => l.length >= 8)
      .sort((a, b) => b.length - a.length).slice(0, 3);
    if (!cand.length) continue;
    if (!cand.some((c) => sub.includes(c))) bad.push(p);
  }
  return bad;
}

/** 读某 BV 的分P 校验结论：{p: ok}。verify2 优先（cos 复核），否则 verify（aid+cid） */
function loadVerify(bv) {
  const dir = path.join(DATA, bv);
  for (const name of ['_verify2.jsonl', '_verify.jsonl']) {
    const p = path.join(dir, name);
    if (!fs.existsSync(p)) continue;
    const m = {};
    for (const line of fs.readFileSync(p, 'utf8').split(/\r?\n/)) {
      if (!line.trim()) continue;
      try { const j = JSON.parse(line); if (typeof j.p === 'number') m[j.p] = j.ok === true; } catch { /* 跳过坏行 */ }
    }
    if (Object.keys(m).length) return m;
  }
  return {};
}

/** 用当前字幕源重建单元正文（保持 id 与段顺序） */
function rebuild(unitId) {
  const src = path.join(UNITS, `${unitId}.txt`);
  const bv = unitId.replace(/_\d+$/, '');
  const dir = path.join(DATA, bv);
  const raw = fs.readFileSync(src, 'utf8');
  const lines = raw.split(/\r?\n/);
  const header = [];
  let i = 0;
  while (i < lines.length && lines[i].startsWith('#')) header.push(lines[i++]);
  const verify = loadVerify(bv);
  const segs = [...raw.matchAll(/^=== P(\d+) \|([^\n]*)===\s*$/gm)];
  const out = [];
  let missing = 0, dropped = 0, kept = 0;
  for (const m of segs) {
    const p = Number(m[1]);
    const title = m[2];
    // ★ 只拼「校验通过」的分P —— 重建不能成为绕过 verify 的后门
    if (Object.keys(verify).length && verify[p] === false) { dropped++; continue; }
    const sp = path.join(dir, `subtitle_p${String(p).padStart(2, '0')}.txt`);
    if (!fs.existsSync(sp)) { missing++; continue; }
    const body = fs.readFileSync(sp, 'utf8').trim();
    if (!body) { missing++; continue; }
    out.push(`=== P${p} |${title}===`);
    out.push(body);
    out.push('');
    kept++;
  }
  if (!out.length) return { ok: false, reason: '无可拼接段' };
  // ★ `_units/` 的单元文件**本来就没有头部** —— 那 5 行 `# unit:` / `# 学科:` /
  //   `# 视频:` / `# 已校验分P:` / `# ⚠️` 全部由 `bili_filter_units.py` 生成到
  //   `_units_verified/`。所以这里不能"保留头部"，也不能凭空造一个：
  //   第一版就是拿空 header 拼出 `\n\n` 开头、还覆盖写了 verified，
  //   把 51 个单元的头部整段清空了。
  //   正确做法：只写 `_units/`，verified 交给 filter 重新生成。
  const body = out.join('\n');
  const text = header.length ? `${header.join('\n')}\n\n${body}` : body;
  return { ok: true, text, segs: segs.length, kept, missing, dropped, chars: text.length };
}

const all = fs.readdirSync(VERIFIED).filter((f) => /^BV.*_\d+\.txt$/.test(f)).map((f) => f.replace(/\.txt$/, ''));
const targets = [];
for (const id of all) {
  if (ONLY && !id.startsWith(ONLY)) continue;
  const bad = detect(id);
  if (bad && bad.length) targets.push({ id, bad });
}
console.log(`扫描 ${all.length} 个单元 → 错位 ${targets.length} 个`);
if (!targets.length) process.exit(0);

for (const d of [STALE, BAD]) if (WRITE) fs.mkdirSync(d, { recursive: true });

let changed = 0, charsBefore = 0, charsAfter = 0, badCleared = 0;
for (const t of targets) {
  const before = fs.readFileSync(path.join(VERIFIED, `${t.id}.txt`), 'utf8');
  const r = rebuild(t.id);
  if (!r.ok) { console.log(`  ✗ ${t.id} 重建失败：${r.reason}`); continue; }
  const after = detect2(t.id, r.text);
  charsBefore += before.length;
  charsAfter += r.text.length;
  if (after.length) console.log(`  ⚠ ${t.id} 重建后仍有 ${after.length} 段错位（${after.slice(0, 4).join(',')}）`);
  else badCleared++;
  if (WRITE) {
    fs.writeFileSync(path.join(STALE, `${t.id}.txt`), before, 'utf8');
    fs.writeFileSync(path.join(UNITS, `${t.id}.txt`), r.text, 'utf8');
    // ★ 不写 VERIFIED —— 那 5 行头部（# unit / # 学科 / # 视频 / # 已校验分P / # ⚠️）
    //   由 `bili_filter_units.py` 生成，直接覆盖会把头部清空。
    //   改完必须跑一次 filter 让 verified 重新生成。
    const md = path.join(EXTRACT, `${t.id}.md`);
    if (fs.existsSync(md)) {
      fs.renameSync(md, path.join(BAD, `${t.id}.md`));
    }
  }
  changed++;
  console.log(`  ${WRITE ? '✓' : '·'} ${t.id}  错位段 ${t.bad.length} → ${after.length}  字符 ${before.length} → ${r.text.length}${r.missing ? `（缺 ${r.missing} 个分P 字幕）` : ''}`);
}
console.log(`\n${WRITE ? '已重建' : '可重建'} ${changed} 个单元 | 字符 ${charsBefore} → ${charsAfter} | 错位清零 ${badCleared}/${changed}`);
if (!WRITE) console.log('干跑结束，加 --write 执行');

/** 对给定正文做同样的错位检测（不落盘） */
function detect2(unitId, text) {
  const bv = unitId.replace(/_\d+$/, '');
  const dir = path.join(DATA, bv);
  const segs = [...text.matchAll(/^=== P(\d+) \|([^\n]*)===\s*$/gm)];
  const bad = [];
  for (let i = 0; i < segs.length; i++) {
    const p = Number(segs[i][1]);
    const start = segs[i].index + segs[i][0].length;
    const end = i + 1 < segs.length ? segs[i + 1].index : text.length;
    const body = text.slice(start, end).trim();
    if (body.length < 30) continue;
    const sp = path.join(dir, `subtitle_p${String(p).padStart(2, '0')}.txt`);
    if (!fs.existsSync(sp)) continue;
    const sub = fs.readFileSync(sp, 'utf8');
    const cand = body.split(/\r?\n/).map((l) => l.trim()).filter((l) => l.length >= 8)
      .sort((a, b) => b.length - a.length).slice(0, 3);
    if (!cand.length) continue;
    if (!cand.some((c) => sub.includes(c))) bad.push(p);
  }
  return bad;
}
