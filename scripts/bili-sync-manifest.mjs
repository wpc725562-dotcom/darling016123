#!/usr/bin/env node
/**
 * 把 `_units/` 里所有单元文件同步进 `_units/_manifest.json`
 *
 * 为什么需要
 * --------
 * `bili_filter_units.py` **只处理 manifest 里有的条目**。
 * 而 `bili_build_units.py --bv X --append` 跑过多次之后，有几次没把新条目并进 manifest，
 * 结果 `_units/` 有 450 个文件、manifest 只有 264 条 —— **186 个单元不在 filter 的视野内**。
 *
 * 后果：
 *   · 它们已经躺在 `_units_verified/` 里（filter 不 rmtree，所以没被删）
 *   · 但**再跑一次 filter 也不会重新校验它们**
 *   · 字幕重下之后，这些单元既不会更新、也不会被标记为过期
 *
 * 用法
 * ----
 *   node scripts/bili-sync-manifest.mjs            # 干跑，只报缺口
 *   node scripts/bili-sync-manifest.mjs --write    # 补进 manifest（原文件备份为 .bak-<时间>）
 *
 * 补出来的条目字段与 `bili_build_units.py` 产出的完全一致：
 *   { unit, subject, bv, video_title, owner, pages, chars, file }
 * 其中 subject / video_title 从单元文件头部读，pages 从 `=== Pn |` 段头读，
 * owner 从 `<BV>/report.md` 的 `- UP:` 行读（读不到就留空，不猜）。
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = 'D:/deeepseek/zhuan-sheng-ben-notes';
const DATA = path.join(ROOT, 'data/bili-analyze');
const VERIFIED = path.join(DATA, '_units_verified');
const UNITS = path.join(DATA, '_units');
const MANIFEST = path.join(UNITS, '_manifest.json');

const WRITE = process.argv.includes('--write');
// --refresh：不新增条目，只把已有条目里空掉的 subject / video_title / owner 补回来
const REFRESH = process.argv.includes('--refresh');

const manifest = JSON.parse(fs.readFileSync(MANIFEST, 'utf8'));
const have = new Set(manifest.map((x) => x.unit));
const files = fs.readdirSync(UNITS).filter((f) => /^BV.*_\d+\.txt$/.test(f));

// ★ `_units/` 的单元文件**没有头部** —— 那 5 行 `# unit:` / `# 学科:` / `# 视频:` 是
//   `bili_filter_units.py` 生成到 `_units_verified/` 的。所以 subject / video_title
//   必须从别处取：科目查 CATALOG 导出的 `_subject-map.json`，标题查 `<BV>/_ytdlp_meta.json`
//   或 `report.md` 的首行。第一版直接从单元文件里 regex 抓，186 条全空。
const SUBJ = fs.existsSync(path.join(DATA, '_subject-map.json'))
  ? JSON.parse(fs.readFileSync(path.join(DATA, '_subject-map.json'), 'utf8')) : {};
// `_part_titles_all.json` 是 bili_build_units.py 的全量分P 标题缓存，
// 里面每条都带 {title, owner} —— 这是 owner 唯一可靠的来源（report.md 只有部分视频有）
const PART_TITLES = fs.existsSync(path.join(DATA, '_part_titles_all.json'))
  ? JSON.parse(fs.readFileSync(path.join(DATA, '_part_titles_all.json'), 'utf8')) : {};

function metaOf(bv) {
  const out = { title: '', owner: '' };
  const pt = PART_TITLES[bv];
  if (pt) { out.title = pt.title || ''; out.owner = pt.owner || ''; }
  const mp = path.join(DATA, bv, '_ytdlp_meta.json');
  if (fs.existsSync(mp)) {
    try { const t = JSON.parse(fs.readFileSync(mp, 'utf8')).title; if (t && !out.title) out.title = t; } catch { /* 忽略坏 json */ }
  }
  const rp = path.join(DATA, bv, 'report.md');
  if (fs.existsSync(rp)) {
    const head = fs.readFileSync(rp, 'utf8').slice(0, 1500);
    const mu = head.match(/- UP:\s*(.+)/);
    if (mu && !out.owner) out.owner = mu[1].trim();
    if (!out.title) {
      const mt = head.match(/^#\s+(.+)$/m);
      if (mt) out.title = mt[1].trim();
    }
  }
  return out;
}

/** 从 `_units_verified/<unit>.txt` 的 5 行头部里抠 subject / video_title
 *  ⚠️ 不拆 owner —— 标题本身常带全角括号（「…（1-200题 ）专升本高数真题分类密训 || …」），
 *     用 `（(.+)）$` 去拆会把标题尾巴当成 UP 主名。owner 只认 `_part_titles_all.json`。 */
function verifiedHead(unit) {
  const p = path.join(VERIFIED, `${unit}.txt`);
  if (!fs.existsSync(p)) return null;
  const h = fs.readFileSync(p, 'utf8').slice(0, 2000);
  if (!/^# unit:/m.test(h)) return null;
  const subj = (h.match(/^# 学科:\s*(.+)$/m) || [, ''])[1].trim();
  let vid = (h.match(/^# 视频:\s*(.+)$/m) || [, ''])[1].trim();
  // 只在「结尾是一个短括号」时才剥掉 owner 尾巴（UP 主名一般 <20 字）
  const m = vid.match(/^([\s\S]+)（([^（）]{1,20})）\s*$/);
  if (m) vid = m[1].trim();
  return { subject: subj, video_title: vid };
}

const added = [];
for (const f of files) {
  const unit = f.replace(/\.txt$/, '');
  if (have.has(unit)) continue;
  const raw = fs.readFileSync(path.join(UNITS, f), 'utf8');
  const bv = unit.replace(/_\d+$/, '');
  const m = metaOf(bv);
  // 单元文件若确实有头部（新式单元可能有），优先用文件里的
  const hs = (raw.match(/^# 学科:\s*(.+)$/m) || [, ''])[1].trim();
  const ht = (raw.match(/^# 视频:\s*(.+)$/m) || [, ''])[1].trim();
  const vh = verifiedHead(unit) || {};
  const pages = [...raw.matchAll(/^=== P(\d+) \|/gm)].map((x) => Number(x[1]));
  added.push({
    unit,
    subject: hs || SUBJ[bv] || vh.subject || '',
    bv,
    video_title: ht || m.title || vh.video_title || '',
    owner: m.owner || vh.owner || '',
    pages,
    chars: raw.length,
    file: `_units/${f}`,
  });
}

console.log(`manifest ${manifest.length} 条 | _units ${files.length} 个 | 缺 ${added.length} 条`);
if (!added.length && !REFRESH) { console.log('已一致，无需补。'); process.exit(0); }

// --refresh：把已有条目里空掉/写坏的字段从权威来源补回来
let base = manifest;
let refreshed = 0;
if (REFRESH) {
  base = manifest.map((x) => {
    const pt = PART_TITLES[x.bv] || {};
    const h = verifiedHead(x.unit) || {};
    // owner 只认 _part_titles_all.json；其次接受「短且不含 |」的旧值（report.md 来的）
    const ownerOk = x.owner && x.owner.length <= 20 && !x.owner.includes('|');
    const next = {
      ...x,
      subject: x.subject || SUBJ[x.bv] || h.subject || '',
      video_title: x.video_title || h.video_title || pt.title || '',
      owner: pt.owner || (ownerOk ? x.owner : ''),
    };
    if (next.subject !== x.subject || next.video_title !== x.video_title || next.owner !== x.owner) refreshed++;
    return next;
  });
  const stillEmpty = base.filter((x) => !x.video_title).length;
  const noOwner = base.filter((x) => !x.owner).length;
  console.log(`--refresh：补回 ${refreshed} 条字段 | 仍无标题 ${stillEmpty} 条 | 仍无 owner ${noOwner} 条`);
}

const byBv = {};
for (const a of added) byBv[a.bv] = (byBv[a.bv] || 0) + 1;
console.log('缺条目的视频：' + Object.entries(byBv).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k}×${v}`).join(' '));
const noSubject = added.filter((a) => !a.subject).length;
const noPages = added.filter((a) => !a.pages.length).length;
if (noSubject) console.log(`⚠ ${noSubject} 条读不到 # 学科: 行`);
if (noPages) console.log(`⚠ ${noPages} 条读不到 === Pn | 段头`);

if (!WRITE) { console.log('\n干跑结束，加 --write 写入。'); process.exit(0); }

// 排序：先 BV，再单元序号，保持「同一门课连续」的既有习惯
const rank = (u) => {
  const m = u.match(/^(BV\w+)_(\d+)$/);
  return m ? [m[1], Number(m[2])] : [u, 0];
};
const merged = [...base, ...added].sort((a, b) => {
  const [ba, na] = rank(a.unit), [bb, nb] = rank(b.unit);
  if (ba !== bb) return ba < bb ? -1 : 1;
  return na - nb;
});

const stamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
fs.copyFileSync(MANIFEST, `${MANIFEST}.bak-${stamp}`);
fs.writeFileSync(MANIFEST, JSON.stringify(merged, null, 1), 'utf8');
console.log(`\n已写入 ${merged.length} 条（原 ${manifest.length} + 新 ${added.length}）`);
console.log(`备份：${path.basename(MANIFEST)}.bak-${stamp}`);
console.log('下一步：python scripts/bili_filter_units.py   # 让 filter 重新校验这批');
