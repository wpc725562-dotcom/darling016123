#!/usr/bin/env node
/**
 * 提炼产物校验器 —— 严格按 `_extract/_INSTRUCTIONS.md` 的契约检查 md。
 *
 * 与 test-one-unit.mjs 的区别：那个是「调模型 + 粗校验」的冒烟器，
 * 这个是**纯校验器**，既能查单文件也能扫全目录，且判据直接来自规范原文，
 * 不掺我自己发明的密度指标。
 *
 * 用法：
 *   node scripts/check-extract.mjs <unit.txt> [extract.md]      # 单文件
 *   node scripts/check-extract.mjs --all                        # 扫全部已提炼
 *   node scripts/check-extract.mjs --all --only=BV1swAWerEzS    # 只看某个 BV
 *
 * 判据（逐条对应 _INSTRUCTIONS.md）：
 *   C1 首行 `# <单元名> · <学科> · <视频名>（<UP主>）`，且单元名=文件名、
 *      学科/视频与输入文件第 2/3 行**逐字相同**（规范 §输出格式）
 *   C2 有 `> 覆盖：P<首>–P<末>（<节数> 节）`，且 P 范围/节数与输入一致（§输出格式）
 *   C3 无 frontmatter、无「本单元小结」尾注（§输出格式 末条）
 *   C4 只用 ## 与 ### 两级；每个 ### 都挂在某个 ## 下（§输出格式）
 *   C5 每个 ### 必有 要点 / 关键概念 / 出处；相互关系可整行省略，
 *      但若出现必须排在第 3 位（§3 硬性要求 3）
 *   C6 出处 P 号必须真实存在于输入（§3 硬性要求 3 + §输出格式）
 *   C7 长度 2000–4000 字，单节单元放宽到 800 字起（§长度）
 *   C8 无过渡语/鸡汤/互动引导（§1 只写知识点）
 *   C9 若输出是 `⚠️ ... 内容与课程无关` 则判为 WARN（上游数据问题，不算产物）
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = 'D:/deeepseek/zhuan-sheng-ben-notes/data/bili-analyze';
const UNITS = path.join(ROOT, '_units_verified');
const EXTRACT = path.join(ROOT, '_extract');

const BANNED = [
  '老师说', '老师讲', '同学们', '大家好', '接下来我们', '这节课', '本节课',
  '点赞', '投币', '一键三连', '关注我', '本单元小结', '以上就是',
];

/** 读输入单元，抽头部元信息与 P 号集合 */
function readUnit(txt) {
  const raw = fs.readFileSync(txt, 'utf8');
  const lines = raw.split(/\r?\n/);
  const head = {};
  for (const l of lines.slice(0, 8)) {
    const m = l.match(/^#\s*(unit|学科|视频|已校验分P)\s*[:：]\s*(.+)$/);
    if (m) head[m[1]] = m[2].trim();
  }
  const pages = [...raw.matchAll(/^=== P(\d+) \|/gm)].map((x) => Number(x[1]));
  return {
    raw,
    name: head.unit || path.basename(txt, '.txt'),
    subject: head['学科'] || '',
    video: head['视频'] || '',
    verified: head['已校验分P'] || '',
    pages,
    pLo: pages.length ? Math.min(...pages) : 0,
    pHi: pages.length ? Math.max(...pages) : 0,
  };
}

/** 视频名比对：把全角/半角括号、空白、连接符统一后再比；
 *  允许产出是输入的真前缀（截断关键词堆砌是合理的），不允许改写。 */
function normTitle(s) {
  return s
    .replace(/[（(]/g, '(').replace(/[）)]/g, ')')
    .replace(/[【\[]/g, '[').replace(/[】\]]/g, ']')
    .replace(/[，,]/g, ',')
    .replace(/[：:]/g, ':')
    .replace(/\s+/g, '')
    .toLowerCase();
}
function videoMatches(inputTitle, outTitle) {
  const a = normTitle(inputTitle);
  const b = normTitle(outTitle);
  if (a === b) return true;
  // 产出是输入的前缀（去掉尾部 UP 主括注后再比一次）
  const bNoUp = b.replace(/\([^()]*\)$/, '');
  return a.startsWith(b) || (bNoUp.length > 6 && a.startsWith(bNoUp));
}

/** 逐条校验，返回 {errors, warns, stats} */
function check(unit, out) {
  const errors = [];
  const warns = [];
  const stats = {};

  // ── 前置：无关内容上报 ──
  if (/^\s*⚠️/.test(out)) {
    warns.push(`C9 模型上报「内容与课程无关」：${out.split(/\r?\n/)[0].slice(0, 80)}`);
    return { errors, warns, stats, skipped: true };
  }

  const lines = out.split(/\r?\n/);
  // 去掉首尾空行后取首行
  const body = out.replace(/^\s*\r?\n/, '');
  const first = (body.split(/\r?\n/)[0] || '').trim();

  // C1 首行
  const fm = first.match(/^#\s+(\S+)\s+·\s+(.+?)\s+·\s+(.+)$/);
  if (!fm) {
    errors.push(`C1 首行不符：${first.slice(0, 90)}`);
  } else {
    const [, name, subj, vid] = fm;
    if (name !== unit.name) errors.push(`C1 单元名不符：文件是 ${unit.name}，首行写 ${name}`);
    // 学科允许加限定词（「计算机」→「计算机（数据结构）」），但必须以输入头的学科开头
    if (unit.subject && !subj.trim().startsWith(unit.subject)) {
      errors.push(`C1 学科不符：输入头写「${unit.subject}」，产出写「${subj.trim()}」`);
    }
    // 视频名允许截断（B 站标题常带关键词堆砌），但不许改写/编造
    if (unit.video && !videoMatches(unit.video, vid.trim())) {
      errors.push(`C1 视频名不符：输入头写「${unit.video.slice(0, 40)}…」，产出写「${vid.trim().slice(0, 40)}…」`);
    }
    if (!/（[^）]+）\s*$/.test(vid.trim())) warns.push(`C1 视频名末尾缺（UP主）`);
  }

  // C2 覆盖行
  const cover = lines.find((l) => /^>\s*覆盖：/.test(l)) || '';
  if (!cover) {
    errors.push('C2 缺 `> 覆盖：` 行');
  } else {
    // 单节单元写成 `P10（1 节）` 是合法的；老批次有 `（32 页，31 个知识点）` 写法
    const cm = cover.match(/P(\d+)(?:\s*[–\-~]\s*P(\d+))?\s*[（(]\s*(\d+)\s*(?:节|页)/);
    if (!cm) {
      errors.push(`C2 覆盖行格式不符：${cover.slice(0, 60)}`);
    } else {
      const lo = Number(cm[1]);
      const hi = Number(cm[2] || cm[1]);
      const n = Number(cm[3]);
      if (lo !== unit.pLo) errors.push(`C2 起始 P 不符：应为 P${unit.pLo}，写 P${lo}`);
      if (hi !== unit.pHi) errors.push(`C2 结束 P 不符：应为 P${unit.pHi}，写 P${hi}`);
      if (n !== unit.pages.length) errors.push(`C2 节数不符：应为 ${unit.pages.length}，写 ${n}`);
    }
  }

  // C3 frontmatter / 尾注
  if (/^---\s*\r?\n/.test(body)) errors.push('C3 出现 frontmatter');
  if (/本单元小结|^\s*>\s*全文完/m.test(out)) errors.push('C3 出现文件尾注/小结');

  // C4 层级
  const h2 = (out.match(/^##\s+/gm) || []).length;
  const h3 = (out.match(/^###\s+/gm) || []).length;
  const h1 = (out.match(/^#\s+/gm) || []).length;
  stats.h2 = h2; stats.h3 = h3;
  if (h1 !== 1) errors.push(`C4 一级标题应为 1 个，实为 ${h1}`);
  if (h3 === 0) errors.push('C4 没有任何 ### 知识点');
  // 第一个 ### 之前必须出现过 ##
  const firstH2 = out.search(/^##\s+/m);
  const firstH3 = out.search(/^###\s+/m);
  if (firstH3 >= 0 && (firstH2 < 0 || firstH3 < firstH2)) errors.push('C4 存在游离在 ## 之前的 ###');
  if (h2 === 0) errors.push('C4 没有任何 ## 主题');

  // C5 四字段（相互关系可选）
  const blocks = out.split(/^###\s+/m).slice(1);
  let ok = 0;
  const bad = [];
  for (const b of blocks) {
    const title = (b.split(/\r?\n/)[0] || '').slice(0, 18);
    const got = [...b.matchAll(/^\s*-\s*\*\*(要点|关键概念|相互关系|出处)\*\*\s*[：:]/gm)].map((x) => x[1]);
    const need = ['要点', '关键概念', '出处'];
    const missing = need.filter((k) => !got.includes(k));
    if (missing.length) { bad.push(`${title} 缺 ${missing.join('/')}`); continue; }
    // 顺序：去掉可选的相互关系后必须严格递增
    const order = got.filter((k) => k !== '相互关系');
    const expect = ['要点', '关键概念', '出处'];
    if (order.join() !== expect.join()) { bad.push(`${title} 顺序乱 ${got.join('/')}`); continue; }
    if (got.includes('相互关系') && got[2] !== '相互关系') { bad.push(`${title} 相互关系位置错 ${got.join('/')}`); continue; }
    ok++;
  }
  stats.blocks = blocks.length;
  stats.blocksOk = ok;
  if (bad.length) errors.push(`C5 ${blocks.length - ok}/${blocks.length} 块字段不合规：${bad.slice(0, 3).join('；')}`);

  // C6 出处 P 号真实性
  const valid = new Set(unit.pages);
  const cited = [...out.matchAll(/\*\*出处\*\*[：:]\s*([^\n]+)/g)]
    .flatMap((m) => [...m[1].matchAll(/P(\d+)/g)].map((x) => Number(x[1])));
  const ghost = [...new Set(cited.filter((p) => !valid.has(p)))];
  stats.cited = cited.length;
  if (ghost.length) errors.push(`C6 出处含不存在的 P 号：${ghost.join(',')}`);

  // C7 长度（中文字符 + 西文词，粗略按非空白字符计）
  const len = out.replace(/\s/g, '').length;
  stats.len = len;
  const minLen = unit.pages.length <= 1 ? 800 : 2000;
  if (len < minLen) warns.push(`C7 偏短：${len} 字（下限 ${minLen}）`);
  if (len > 4400) warns.push(`C7 偏长：${len} 字（上限 4000）`);

  // C8 禁语
  const hits = BANNED.filter((w) => out.includes(w));
  if (hits.length) errors.push(`C8 出现过渡语/互动引导：${hits.join('、')}`);

  return { errors, warns, stats };
}

/** 打印单条结果 */
function report(unitPath, mdPath) {
  const unit = readUnit(unitPath);
  const out = fs.readFileSync(mdPath, 'utf8');
  const { errors, warns, stats, skipped } = check(unit, out);
  const tag = skipped ? 'WARN' : errors.length ? 'FAIL' : 'PASS';
  const sig = errors.map((e) => e.slice(0, 2)).filter((v, i, a) => a.indexOf(v) === i).join('');
  const label = `${unit.name}  ${(unit.raw.length / 1024).toFixed(0)}KB/${unit.pages.length}节`;
  if (tag === 'PASS' && !warns.length) {
    console.log(`✓ ${label}  h2=${stats.h2} h3=${stats.h3} ${stats.len}字`);
  } else {
    console.log(`${tag === 'FAIL' ? '✗' : '⚠'} ${label}  h2=${stats.h2} h3=${stats.h3} ${stats.len}字  [${sig || '-'}]`);
    for (const e of errors) console.log(`    ✗ ${e}`);
    for (const w of warns) console.log(`    ⚠ ${w}`);
  }
  return { tag, unit, errors, warns, stats };
}

// ── 入口 ──
const argv = process.argv.slice(2);
if (argv.includes('--all')) {
  const onlyArg = argv.find((a) => a.startsWith('--only='));
  const only = onlyArg ? onlyArg.split('=')[1] : '';
  // --tier=P0,P1 / --tier=!P3 —— 按目标视频分级过滤（依据 _target-videos.json）
  const tierArg = argv.find((a) => a.startsWith('--tier='));
  let tierMap = null, tierFilter = null;
  const tp = path.join(EXTRACT, '_target-videos.json');
  if (tierArg && fs.existsSync(tp)) {
    const j = JSON.parse(fs.readFileSync(tp, 'utf8'));
    tierMap = {};
    for (const [t, arr] of Object.entries(j.tiers || {})) for (const x of arr) tierMap[x.bv] = t;
    const raw = tierArg.split('=')[1];
    const neg = raw.startsWith('!');
    tierFilter = { neg, set: new Set(raw.replace(/^!/, '').split(',').map((s) => s.trim()).filter(Boolean)) };
  }
  const tierOf = (name) => (tierMap ? tierMap[name.replace(/_\d+$/, '')] || 'UNKNOWN' : 'UNKNOWN');
  const tierOk = (name) => {
    if (!tierFilter) return true;
    const t = tierOf(name);
    return tierFilter.neg ? !tierFilter.set.has(t) : tierFilter.set.has(t);
  };

  const mds = fs.readdirSync(EXTRACT).filter((f) => /^BV.*\.md$/.test(f));
  let pass = 0, fail = 0, warn = 0;
  const fails = [];
  const byTier = {};
  for (const f of mds) {
    if (only && !f.startsWith(only)) continue;
    const name = f.replace(/\.md$/, '');
    if (!tierOk(name)) continue;
    const up = path.join(UNITS, `${name}.txt`);
    if (!fs.existsSync(up)) { warn++; console.log(`⚠ ${name}  输入单元不在 _units_verified`); continue; }
    const r = report(up, path.join(EXTRACT, f));
    const t = tierOf(name);
    byTier[t] = byTier[t] || { pass: 0, fail: 0, warn: 0 };
    byTier[t][r.tag === 'PASS' ? 'pass' : r.tag === 'FAIL' ? 'fail' : 'warn']++;
    if (r.tag === 'PASS') pass++; else if (r.tag === 'FAIL') { fail++; fails.push(name); } else warn++;
  }
  console.log(`\n汇总：PASS ${pass} / FAIL ${fail} / WARN ${warn}（共 ${pass + fail + warn}）`);
  if (tierMap) {
    console.log('按分级：' + Object.entries(byTier).sort()
      .map(([t, v]) => `${t} PASS ${v.pass}/FAIL ${v.fail}/WARN ${v.warn}`).join(' | '));
  }
  if (fails.length) console.log(`FAIL 清单：${fails.join(', ')}`);
} else {
  const unitPath = argv[0];
  if (!unitPath) {
    console.error('用法: node scripts/check-extract.mjs <unit.txt> [extract.md] | --all [--only=BVxxx]');
    process.exit(1);
  }
  const name = path.basename(unitPath, '.txt');
  const mdPath = argv[1] || path.join(EXTRACT, `${name}.md`);
  const r = report(unitPath, mdPath);
  process.exit(r.tag === 'FAIL' ? 1 : 0);
}
