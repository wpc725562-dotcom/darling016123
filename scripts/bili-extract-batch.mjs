#!/usr/bin/env node
/**
 * B 站课程字幕 → 知识点卡片 · 批量提炼编排器
 *
 * 依据 `_extract/_BATCH-PLAN.md` 与 `_extract/_INSTRUCTIONS.md`。
 *
 * 用法：
 *   node scripts/bili-extract-batch.mjs --pilot                 # 5 个试点单元
 *   node scripts/bili-extract-batch.mjs --limit=20              # 只跑 20 个
 *   node scripts/bili-extract-batch.mjs --conc=2 --max-chars=50000
 *   node scripts/bili-extract-batch.mjs --only=BV1swAWerEzS     # 限定某门课
 *   node scripts/bili-extract-batch.mjs --retry-fail            # 重跑 _fail 里的
 *   node scripts/bili-extract-batch.mjs --dry                   # 只出计划不调用
 *
 * 关键设计（每条都对应规划里的一个坑）：
 *   1. 输入只认 _units_verified/，绝不读 _units/
 *   2. 一律 stream:true —— 非流式在 ~270s 会被中间盒掐断（实测 502 ECONNRESET）
 *   3. 首行/覆盖行由脚本按输入头**覆盖**，不信模型
 *   4. 按 === Pn | 边界切片，单片 ≤ maxChars 字符
 *   5. 产物存在即跳过（断点续跑，无状态文件）
 *   6. finish_reason == 'length' 直接判失败（半截 md 能过一部分校验，很隐蔽）
 *   7. 模型回 ⚠️ 视为「上游数据报废」，进 _reject 不重试
 */
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const ROOT = 'D:/deeepseek/zhuan-sheng-ben-notes';
const DATA = path.join(ROOT, 'data/bili-analyze');
const UNITS = path.join(DATA, '_units_verified');
const EXTRACT = path.join(DATA, '_extract');
const PARTS = path.join(EXTRACT, '_parts');
const FAILS = path.join(EXTRACT, '_fail');
const REJECT = path.join(EXTRACT, '_reject');

const ENDPOINT = process.env.OFM_BASE || 'http://127.0.0.1:18999/v1';
const KEY = process.env.OFM_KEY || 'kilo-free';
const MODEL = process.env.OFM_MODEL || 'dots-studio/dots-3-note-preview:free';
// 主模型偶尔会对大请求返回 400（网关把它路由到拒收大请求的上游），换模型是最省事的绕法。
// 实测 41k 字符的切片：dots-3-note 400，beam-free 6.8s 200，nemotron-3.5-super-vl 24.1s 200。
const FALLBACKS = (process.env.OFM_FALLBACKS
  || 'reflection/beam-free,nvidia/nemotron-3.5-super-vl:free').split(',').map((s) => s.trim()).filter(Boolean);
const MODELS = [MODEL, ...FALLBACKS];

// ── 参数 ──
const argv = process.argv.slice(2);
const flag = (n) => argv.includes(`--${n}`);
const opt = (n, d) => {
  const a = argv.find((x) => x.startsWith(`--${n}=`));
  return a ? a.split('=')[1] : d;
};
const CONC = Number(opt('conc', 2));
const MAXCHARS = Number(opt('max-chars', 50000));
const LIMIT = Number(opt('limit', 0));
const ONLY = opt('only', '');
const MAXINPUT = Number(opt('max-input', 0));   // 只跑输入字符数 ≤ 此值的单元
const MININPUT = Number(opt('min-input', 0));   // 只跑输入字符数 ≥ 此值的单元
const PILOT = flag('pilot');
const DRY = flag('dry');
const RETRY_FAIL = flag('retry-fail');
const REWORK = flag('rework');   // 重提炼存量里校验不过的（先备份到 _extract/_bad/）
// 按目标视频分级过滤，依据 `_TARGET-VIDEOS.md` / `_target-videos.json`
//   --tier=P0,P1     只要主线和专项
//   --tier=!P3       只要不是排除项（等价于 P0,P1,P2E,P2B）
const TIER_OPT = opt('tier', '');
const TIER_MAP = (() => {
  const p = path.join(EXTRACT, '_target-videos.json');
  if (!fs.existsSync(p)) return null;
  const j = JSON.parse(fs.readFileSync(p, 'utf8'));
  const m = {};
  for (const [t, arr] of Object.entries(j.tiers || {})) for (const x of arr) m[x.bv] = t;
  return m;
})();
const TIER_FILTER = (() => {
  if (!TIER_OPT) return null;
  if (!TIER_MAP) {
    console.error('✗ 用了 --tier 但找不到 _extract/_target-videos.json');
    process.exit(2);
  }
  const neg = TIER_OPT.startsWith('!');
  const set = new Set(TIER_OPT.replace(/^!/, '').split(',').map((s) => s.trim()).filter(Boolean));
  return { neg, set };
})();
const tierOf = (unitId) => TIER_MAP?.[unitId.replace(/_\d+$/, '')] || 'UNKNOWN';
const tierOk = (unitId) => {
  if (!TIER_FILTER) return true;
  const t = tierOf(unitId);
  return TIER_FILTER.neg ? !TIER_FILTER.set.has(t) : TIER_FILTER.set.has(t);
};

const PILOT_UNITS = [
  'BV1zoY66wEx4_218',   // ~2k 字符，单节
  'BV1UM4m127xY_109',   // 19.2k，已冒烟通过
  'BV1swAWerEzS_40',    // 46.6k，已冒烟通过
  'BV1UM4m127xY_106',   // 104k，需切片
  'BV1He4y1r7fc_141',   // 259KB / 预计 7 片，最重一类
];

for (const d of [PARTS, FAILS, REJECT]) fs.mkdirSync(d, { recursive: true });
const GAPS = path.join(EXTRACT, '_COVERAGE-GAPS.md');
if (!fs.existsSync(GAPS)) {
  fs.writeFileSync(GAPS, [
    '# 覆盖率缺口台账',
    '',
    '> 长单元切片后，个别片被模型判定「内容与课程无关」（字幕串台）。',
    '> 那几节不参与提炼，但单元产物照常落地。**每一条缺口都必须记在这里，不许静默。**',
    '>',
    '> 与 `_units_verified/` 剔除未校验分P 是同一类处理，区别只是这一步在提炼阶段才发现。',
    '',
    '| 单元 | 总片数 | 被剔除的片 | 模型给的理由 |',
    '|---|--:|---|---|',
    '',
  ].join('\n'), 'utf8');
}

// ── 提示词：复用 _INSTRUCTIONS.md，只加四条例行补丁 ──
const SPEC = fs.readFileSync(path.join(EXTRACT, '_INSTRUCTIONS.md'), 'utf8');

function systemPrompt({ chars, targetPoints, isSlice, sliceNote, isFirstSlice }) {
  return `${SPEC}

---
## 本次运行的附加约定（覆盖上文冲突处）

1. 你不是在操作文件，而是在直接返回 Markdown 正文。不要提到 Write 工具、不要提路径。
2. 第 1 行和第 2 行（标题与覆盖行）**由程序回填**，你可以照格式写，写错不影响结果。
3. 本单元输入约 ${chars} 字符，目标 **${targetPoints} 个 ### 知识点**（±20%），主题 6–12 个。
   字数不设上限，按内容需要写；但**宁可少而准，不要多而水**。
4. 每个 ### 下：**要点 / 关键概念 / 出处** 三行必写；**相互关系**没有就整行省略，
   不要写「无」「暂无」。
5. 若输入内容与课程主题无关（字幕串台、广告、歌词、无关 vlog、纯音乐），
   **只输出一行**：\`⚠️ <单元名> 内容与课程无关：<前两句原文>\`
   不要基于它提炼任何知识点。这不是失败，是正常出口。
${isSlice ? `\n6. 本段是长单元的一个切片：${sliceNote}\n   只提炼本段出现的分P，不要推测其它分P的内容。\n` : ''}${
    isSlice && !isFirstSlice
      ? `\n7. **本片不是开头。** 不要写课程总述、备考规划、整体策略、题型全景这类跨片内容——
   前面已经写过了。只提炼本片独有的具体知识点（某个词义辨析、某道题的套路、某个易错点）。\n`
      : ''
  }`;
}

// ── 读单元 ──
function readUnit(file) {
  const raw = fs.readFileSync(file, 'utf8');
  const lines = raw.split(/\r?\n/);
  const head = {};
  for (const l of lines.slice(0, 8)) {
    const m = l.match(/^#\s*(unit|学科|视频|已校验分P)\s*[:：]\s*(.+)$/);
    if (m) head[m[1]] = m[2].trim();
  }
  const name = head.unit || path.basename(file, '.txt');
  // 按 === Pn | 边界切成节
  const chunks = raw.split(/^(?==== P\d+ \|)/m);
  const preamble = chunks[0];
  const sections = chunks.slice(1);
  const pages = [...raw.matchAll(/^=== P(\d+) \|/gm)].map((x) => Number(x[1]));
  return {
    name, raw, head,
    subject: head['学科'] || '',
    video: head['视频'] || '',
    preamble, sections, pages,
    pLo: pages.length ? Math.min(...pages) : 0,
    pHi: pages.length ? Math.max(...pages) : 0,
  };
}

/** 切片：按节累积，单片 ≤ maxChars；单节本身超限时按句子硬切 */
function slice(unit, maxChars) {
  const out = [];
  let cur = [];
  let curLen = 0;
  for (const s of unit.sections) {
    if (s.length > maxChars) {
      // 单节超限：先冲掉当前累积，再把这一节按行硬切
      if (cur.length) { out.push(cur.join('')); cur = []; curLen = 0; }
      const head = s.match(/^=== P\d+ \|[^\n]*\n/)?.[0] || '';
      const body = s.slice(head.length);
      const linesArr = body.split('\n');
      let buf = head;
      for (const ln of linesArr) {
        if (buf.length + ln.length + 1 > maxChars && buf.length > head.length) {
          out.push(buf);
          buf = head + `（接上）\n` + ln + '\n';
        } else {
          buf += ln + '\n';
        }
      }
      if (buf.trim()) out.push(buf);
      continue;
    }
    if (curLen + s.length > maxChars && cur.length) {
      out.push(cur.join(''));
      cur = [s]; curLen = s.length;
    } else {
      cur.push(s); curLen += s.length;
    }
  }
  if (cur.length) out.push(cur.join(''));
  return out;
}

// ── 流式调用 ──
async function callModel(sys, user, maxTokens, model = MODEL) {
  const t0 = Date.now();
  const res = await fetch(`${ENDPOINT}/chat/completions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${KEY}` },
    body: JSON.stringify({
      model,
      messages: [{ role: 'system', content: sys }, { role: 'user', content: user }],
      max_tokens: maxTokens,
      stream: true,
    }),
    signal: AbortSignal.timeout(900000),
  });
  if (!res.ok) {
    const t = await res.text().catch(() => '');
    throw Object.assign(new Error(`HTTP ${res.status} ${t.slice(0, 160)}`), { kind: 'http', status: res.status });
  }
  const reader = res.body.getReader();
  const dec = new TextDecoder();
  let buf = '', text = '', finish = '', usage = {};
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += dec.decode(value, { stream: true });
    const lines = buf.split('\n');
    buf = lines.pop() || '';
    for (const line of lines) {
      const s = line.trim();
      if (!s.startsWith('data:')) continue;
      const p = s.slice(5).trim();
      if (p === '[DONE]') continue;
      try {
        const j = JSON.parse(p);
        const d = j.choices?.[0]?.delta?.content;
        if (d) text += d;
        if (j.choices?.[0]?.finish_reason) finish = j.choices[0].finish_reason;
        if (j.usage) usage = j.usage;
      } catch { /* 半包 */ }
    }
  }
  return { text, finish, usage, sec: (Date.now() - t0) / 1000 };
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function withRetry(fn, tag, attempts = 3) {
  let last;
  for (let i = 0; i < attempts; i++) {
    if (i) {
      // 400 是上游 1 秒内就返回的硬拒，等太久没意义；429/5xx 才需要退避
      const is400 = last?.kind === 'http' && last.status === 400;
      await sleep(is400 ? 700 * i : [5000, 20000, 45000][i - 1] ?? 45000);
    }
    try {
      const r = await fn();
      if (r.finish === 'length') throw Object.assign(new Error('finish_reason=length（被 max_tokens 截断）'), { kind: 'trunc' });
      if (!r.text.trim()) throw Object.assign(new Error('空输出'), { kind: 'empty' });
      if (r.text.trim().startsWith('⚠️')) return { ...r, reject: true };
      if (!/^###\s+/m.test(r.text)) throw Object.assign(new Error('无 ### 知识点'), { kind: 'empty' });
      return r;
    } catch (e) {
      last = e;
      // 400 也要重试：实测同一个请求有时 200 有时 400，报错里带 provider_name（如 AtlasCloud），
      // 是网关按请求路由到不同上游导致的，不是内容问题。只有 401/403/404 才是真·不可重试。
      if (e.kind === 'http' && [401, 403, 404].includes(e.status)) break;
      console.log(`      ↻ ${tag} 第${i + 1}次失败: ${e.message.slice(0, 80)}`);
    }
  }
  throw last;
}

/** 在行边界把一段文本对半切（尽量切在 === Pn 或空行处） */
function splitHalf(text) {
  const mid = Math.floor(text.length / 2);
  // 从中间往后找最近的 === Pn 标记，找不到就找空行
  const pIdx = text.indexOf('\n=== P', mid);
  if (pIdx > 0 && pIdx - mid < 8000) return [text.slice(0, pIdx + 1), text.slice(pIdx + 1)];
  const nl = text.indexOf('\n\n', mid);
  if (nl > 0) return [text.slice(0, nl + 2), text.slice(nl + 2)];
  return [text.slice(0, mid), text.slice(mid)];
}

/** 调一片：先主模型；主模型连吃 400 就换备选模型；全都 400 才考虑对半切 */
async function callSlice(sys, text, maxTok, tag, depth = 0) {
  const chain = depth === 0 ? MODELS : MODELS.slice(0, 1);
  let lastErr;
  for (const m of chain) {
    const short = m.split('/')[1]?.slice(0, 14) || m;
    try {
      const r = await withRetry(() => callModel(sys, text, maxTok, m), `${tag}[${short}]`);
      if (m !== MODEL) console.log(`\n      ⇄ ${tag} 改由 ${m} 完成`);
      return r;
    } catch (e) {
      lastErr = e;
      // 只有「上游 400 / 5xx」才值得换模型；401/403/404 换也没用
      const worthSwitch = e.kind === 'http' ? ![401, 403, 404].includes(e.status) : true;
      if (!worthSwitch) throw e;
    }
  }
  if (lastErr?.kind === 'http' && lastErr.status === 400 && depth < 2 && text.length > 14000) {
    const [a, b] = splitHalf(text);
    console.log(`\n      ✂ ${tag} 全模型 400，切成 ${(a.length / 1000).toFixed(0)}k+${(b.length / 1000).toFixed(0)}k 重试`);
    const ra = await callSlice(sys, a, maxTok, `${tag}a`, depth + 1);
    if (ra.reject) return ra;
    const rb = await callSlice(sys, b, maxTok, `${tag}b`, depth + 1);
    if (rb.reject) return ra;
    return { text: ra.text + '\n' + rb.text, finish: 'stop', usage: {}, sec: ra.sec + rb.sec };
  }
  throw lastErr;
}

// ── 合并多片 ──
function mergeParts(parts, unit) {
  const seen = new Map();      // ### 标题 -> {fields}
  const order = [];            // 主题顺序
  const topicMap = new Map();  // ## 标题 -> [### 块文本]
  for (const txt of parts) {
    const body = txt.replace(/^\s*\r?\n/, '');
    const lines = body.split(/\r?\n/);
    // 丢掉模型写的前两行（标题/覆盖），后面统一回填
    let i = 0;
    while (i < lines.length && !/^##\s+/.test(lines[i])) i++;
    const rest = lines.slice(i).join('\n');
    // 拆主题
    const topics = rest.split(/^##\s+/m).slice(1);
    for (const t of topics) {
      const tLines = t.split(/\r?\n/);
      const tName = tLines[0].trim();
      const tBody = tLines.slice(1).join('\n');
      if (!topicMap.has(tName)) { topicMap.set(tName, []); order.push(tName); }
      // 拆知识点
      const blocks = tBody.split(/^###\s+/m).slice(1);
      for (const b of blocks) {
        const bLines = b.split(/\r?\n/);
        const bName = bLines[0].trim();
        const bBody = bLines.slice(1).join('\n').trim();
        if (seen.has(bName)) {
          // 出处取并集
          const prev = seen.get(bName);
          const p1 = (prev.body.match(/\*\*出处\*\*[：:]\s*([^\n]+)/) || [, ''])[1];
          const p2 = (bBody.match(/\*\*出处\*\*[：:]\s*([^\n]+)/) || [, ''])[1];
          const ps = [...new Set([...p1.matchAll(/P(\d+)/g), ...p2.matchAll(/P(\d+)/g)].map((x) => Number(x[1])))].sort((a, b2) => a - b2);
          if (ps.length) {
            seen.set(bName, { body: prev.body.replace(/\*\*出处\*\*[：:][^\n]*/, `**出处**：${ps.map((p) => `P${p}`).join(', ')}`) });
          }
          continue;
        }
        seen.set(bName, { body: bBody });
        topicMap.get(tName).push(`### ${bName}\n${bBody}`);
      }
    }
  }
  // 重拼：主题下没有任何 ### 的丢掉
  const outTopics = [];
  for (const t of order) {
    const blocks = topicMap.get(t);
    if (!blocks || !blocks.length) continue;
    // 去重（同名 ### 可能被追加到多个主题下）
    const uniq = [];
    const seenB = new Set();
    for (const b of blocks) {
      const n = b.split('\n')[0];
      if (seenB.has(n)) continue;
      seenB.add(n); uniq.push(b);
    }
    outTopics.push(`## ${t}\n\n${uniq.join('\n\n')}`);
  }
  return outTopics.join('\n\n');
}

/** 回填首行与覆盖行 */
function buildHeader(unit) {
  const h1 = `# ${unit.name} · ${unit.subject} · ${unit.video}`;
  const h2 = `> 覆盖：P${unit.pLo}–P${unit.pHi}（${unit.pages.length} 节）`;
  return `${h1}\n\n${h2}\n\n`;
}

// ── 单单元处理 ──
async function processUnit(unit, stats) {
  const slices = slice(unit, MAXCHARS);
  const maxTok = unit.raw.length > MAXCHARS ? 64000 : 32000;
  console.log(`  ▸ ${unit.name}  ${(unit.raw.length / 1000).toFixed(0)}k字/${unit.pages.length}节 → ${slices.length} 片`);

  const partTexts = [];
  const rejects = [];
  const sliceErrors = [];
  for (let i = 0; i < slices.length; i++) {
    const s = slices[i];
    const ps = [...s.matchAll(/^=== P(\d+) \|/gm)].map((x) => Number(x[1]));
    const sliceNote = `第 ${i + 1}/${slices.length} 片，含 P${Math.min(...ps)}–P${Math.max(...ps)}（${ps.length} 节）`;
    const target = Math.max(6, Math.round((s.length / 10000) * 3.0));
    const sys = systemPrompt({
      chars: s.length, targetPoints: target,
      isSlice: slices.length > 1, sliceNote, isFirstSlice: i === 0,
    });
    const user = (i === 0 ? unit.preamble : '') + s;
    const tag = slices.length > 1 ? `${unit.name} p${i + 1}` : unit.name;
    process.stdout.write(`     · ${unit.name} 片 ${i + 1}/${slices.length} (${(s.length / 1000).toFixed(0)}k字, 目标${target}点) `);
    let r;
    try {
      r = await callSlice(sys, user, maxTok, tag);
    } catch (e) {
      // 单片失败不拖死整个单元：记下来，继续下一片
      sliceErrors.push({ slice: i + 1, error: String(e.message).slice(0, 200) });
      console.log(`✗ 本片失败：${e.message.slice(0, 100)}`);
      continue;
    }
    if (r.reject) {
      // 单片上报无关内容 ≠ 整个单元报废：一个长单元里夹着几节纯题目/纯音乐是常见的。
      // 只有全部片都上报，才认定这个单元整体报废。
      rejects.push({ i: i + 1, text: r.text.trim() });
      console.log(`⚠️ 本片上报无关内容，跳过（继续其它片）`);
      continue;
    }
    console.log(`✓ ${r.sec.toFixed(0)}s out=${r.usage?.completion_tokens ?? '?'}`);
    fs.writeFileSync(path.join(PARTS, `${unit.name}__p${String(i + 1).padStart(2, '0')}.md`), r.text, 'utf8');
    partTexts.push(r.text);
  }

  if (!partTexts.length) {
    const detail = rejects.map((x) => `片${x.i}: ${x.text.split(/\r?\n/)[0].slice(0, 100)}`).join('\n');
    if (rejects.length === slices.length) {
      fs.writeFileSync(path.join(REJECT, `${unit.name}.md`), detail + '\n', 'utf8');
      console.log(`     ⚠️ 全部 ${slices.length} 片都上报无关内容 → _reject`);
      stats.reject++;
    } else {
      fs.writeFileSync(path.join(FAILS, `${unit.name}.json`),
        JSON.stringify({ unit: unit.name, stage: 'all-slices-failed', slices: slices.length, rejects, sliceErrors }, null, 2), 'utf8');
      console.log(`     ✗ 所有片都没出内容 → _fail`);
      stats.fail++;
    }
    return;
  }
  if (sliceErrors.length) {
    // ★ 有片是「调用失败」时绝不能落地产物：buildHeader 按整个单元的 P 范围回填，
    //   缺片也会照样通过 C2 校验，形成静默的覆盖率缺口。
    console.log(`     ⚠ 失败 ${sliceErrors.length} 片 → 不落地产物，进 _fail 等重试`);
    fs.writeFileSync(path.join(PARTS, `${unit.name}__partial.json`),
      JSON.stringify({ unit: unit.name, slices: slices.length, ok: partTexts.length, rejects, sliceErrors }, null, 2), 'utf8');
    fs.writeFileSync(path.join(FAILS, `${unit.name}.json`),
      JSON.stringify({ unit: unit.name, stage: 'incomplete-slices', slices: slices.length, ok: partTexts.length, rejects, sliceErrors }, null, 2), 'utf8');
    stats.fail++;
    return;
  }
  if (rejects.length) {
    // 片是「模型判定无关内容」——那几节字幕确实串台了，跟 _units_verified 剔除未校验分P 是同一类处理：
    // 产物照常落地，但缺口必须记账，不许静默。
    const gapLine = `| \`${unit.name}\` | ${slices.length} | ${rejects.map((x) => x.i).join(', ')} | ${rejects.map((x) => x.text.replace(/^⚠️\s*/, '').split(/\r?\n/)[0].slice(0, 60)).join(' / ')} |`;
    fs.appendFileSync(path.join(EXTRACT, '_COVERAGE-GAPS.md'), gapLine + '\n', 'utf8');
    console.log(`     （${rejects.length} 片字幕串台已剔除，缺口记进 _COVERAGE-GAPS.md）`);
  }

  const merged = buildHeader(unit) + mergeParts(partTexts, unit) + '\n';
  const outPath = path.join(EXTRACT, `${unit.name}.md`);
  fs.writeFileSync(outPath, merged, 'utf8');

  // 校验
  const c = spawnSync(process.execPath, [path.join(ROOT, 'scripts/check-extract.mjs'),
    path.join(UNITS, `${unit.name}.txt`), outPath], { encoding: 'utf8' });
  const ok = c.status === 0;
  if (!ok) {
    console.log(`     ✗ 校验未过：\n${(c.stdout || '').split('\n').filter((l) => l.includes('✗') || l.includes('⚠')).slice(0, 4).join('\n')}`);
    fs.writeFileSync(path.join(FAILS, `${unit.name}.json`),
      JSON.stringify({ unit: unit.name, stage: 'validate', report: c.stdout }, null, 2), 'utf8');
    stats.fail++;
  } else {
    stats.pass++;
  }
}

// ── 主流程 ──
const all = fs.readdirSync(UNITS).filter((f) => f.endsWith('.txt')).map((f) => f.replace(/\.txt$/, ''));

/** --rework：把存量校验不过的产物挪到 _bad/，让它们重新进入待办 */
function stageRework() {
  const c = spawnSync(process.execPath, [path.join(ROOT, 'scripts/check-extract.mjs'), '--all'], { encoding: 'utf8' });
  const bad = (c.stdout || '').split('\n').filter((l) => /^✗ BV/.test(l)).map((l) => l.split(/\s+/)[1]);
  if (!bad.length) { console.log('没有需要重提炼的产物。'); return []; }
  const BAD = path.join(EXTRACT, '_bad');
  fs.mkdirSync(BAD, { recursive: true });
  for (const n of bad) {
    const src = path.join(EXTRACT, `${n}.md`);
    if (fs.existsSync(src)) fs.renameSync(src, path.join(BAD, `${n}.md`));
  }
  console.log(`已把 ${bad.length} 个不合格产物挪到 _extract/_bad/：${bad.join(', ')}`);
  return bad;
}
const reworkList = REWORK ? stageRework() : null;

let todo = all.filter((n) => {
  if (ONLY && !n.startsWith(ONLY)) return false;
  if (PILOT) return PILOT_UNITS.includes(n);
  if (REWORK) return reworkList.includes(n);
  if (RETRY_FAIL) return fs.existsSync(path.join(FAILS, `${n}.json`));
  if (!tierOk(n)) return false;
  if (fs.existsSync(path.join(EXTRACT, `${n}.md`))) return false;
  if (fs.existsSync(path.join(REJECT, `${n}.md`))) return false;
  if (MAXINPUT || MININPUT) {
    const len = fs.statSync(path.join(UNITS, `${n}.txt`)).size;
    // statSync 给的是字节数，中文 3 字节，换算成字符数
    const chars = fs.readFileSync(path.join(UNITS, `${n}.txt`), 'utf8').length;
    if (MAXINPUT && chars > MAXINPUT) return false;
    if (MININPUT && chars < MININPUT) return false;
  }
  return true;
});

// 排序：先按目标分级（P0 → P1 → P2E → P2B → P3），再按 BV、再按 P 号
const TIER_RANK = { P0: 0, P1: 1, P2E: 2, P2B: 3, P3: 4, UNKNOWN: 5 };
todo.sort((a, b) => {
  const ra = TIER_RANK[tierOf(a)] ?? 5, rb = TIER_RANK[tierOf(b)] ?? 5;
  if (ra !== rb) return ra - rb;
  const pa = a.match(/^(BV\w+)_(\d+)$/), pb = b.match(/^(BV\w+)_(\d+)$/);
  if (!pa || !pb) return a.localeCompare(b);
  if (pa[1] !== pb[1]) return pa[1].localeCompare(pb[1]);
  return Number(pa[2]) - Number(pb[2]);
});
if (LIMIT) todo = todo.slice(0, LIMIT);

console.log('══════ B 站课程批量提炼 ══════');
console.log(`模型      : ${MODEL}`);
console.log(`端点      : ${ENDPOINT}`);
console.log(`并发      : ${CONC}   单片上限: ${MAXCHARS} 字符`);
console.log(`待处理    : ${todo.length} 个单元`);
if (TIER_FILTER) {
  const dist = {};
  for (const n of todo) dist[tierOf(n)] = (dist[tierOf(n)] || 0) + 1;
  console.log(`分级过滤  : ${TIER_OPT}  →  ${Object.entries(dist).map(([k, v]) => `${k}=${v}`).join(' ')}`);
} else {
  const dist = {};
  for (const n of todo) dist[tierOf(n)] = (dist[tierOf(n)] || 0) + 1;
  console.log(`⚠ 未用 --tier，按全量跑（分级分布 ${Object.entries(dist).map(([k, v]) => `${k}=${v}`).join(' ')}）`);
}
if (DRY) {
  for (const n of todo) {
    const u = readUnit(path.join(UNITS, `${n}.txt`));
    console.log(`  [${tierOf(n)}] ${n}  ${(u.raw.length / 1000).toFixed(0)}k字/${u.pages.length}节 → ${slice(u, MAXCHARS).length} 片`);
  }
  process.exit(0);
}

const stats = { pass: 0, fail: 0, reject: 0 };
const t0 = Date.now();
let idx = 0;
async function worker(w) {
  for (;;) {
    const i = idx++;
    if (i >= todo.length) return;
    const n = todo[i];
    console.log(`\n[${i + 1}/${todo.length}] ${n} (worker ${w})`);
    try {
      await processUnit(readUnit(path.join(UNITS, `${n}.txt`)), stats);
    } catch (e) {
      console.log(`     ✗ 失败：${e.message.slice(0, 160)}`);
      fs.writeFileSync(path.join(FAILS, `${n}.json`),
        JSON.stringify({ unit: n, stage: 'call', error: String(e.message) }, null, 2), 'utf8');
      stats.fail++;
    }
  }
}

await Promise.all(Array.from({ length: Math.max(1, CONC) }, (_, i) => worker(i + 1)));

const min = ((Date.now() - t0) / 60000).toFixed(1);
console.log(`\n══════ 完成 ${min} 分钟 ══════`);
console.log(`PASS ${stats.pass} / FAIL ${stats.fail} / REJECT ${stats.reject}`);
console.log(`产物: ${EXTRACT}`);
console.log(`失败: ${FAILS}    报废: ${REJECT}`);
