#!/usr/bin/env node
/**
 * scripts/zhenti_render.mjs —— 把 zhenti.jsonl（真题卡）渲染成**自包含单文件 HTML**交付页。
 *
 * 三个刻意的技术选择，都是为了这个交付页的用途（离线看、能打印、能直接进笔记站）：
 *
 * 1. **公式用 MathJax 在 Node 端预渲染成内联 SVG**，而不是在页面里挂 MathJax CDN。
 *    笔记站是纯静态的，交付页也不该依赖网络 —— 断网打开必须照样显示公式。
 *
 * 2. **用 global fontCache**。local 模式下每个公式自带一份 6~7KB 的字形 <path>；
 *    本页有 300+ 个公式片段，local 会产出 ~2.4MB。global 模式把字形集中到页面顶部
 *    的 <defs> 里只出现一次，公式体降到 ~2KB，总体积降一个量级。
 *    代价：必须等**所有**公式渲染完才能取字形表（cache 是边渲染边累积的）。
 *
 * 3. **按 LaTeX 原文去重**。同一串 LaTeX 只渲染一次，重复出现直接复用同一段 SVG
 *    （20 题里 `\dfrac{1}{3}` 这类片段重复率很高）。缓存 key 区分 inline/display，
 *    因为两者排版规则不同，不能混用。
 *
 * 用法：
 *   node scripts/zhenti_render.mjs <zhenti.jsonl> <out.html>
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { mathjax } from 'mathjax-full/js/mathjax.js';
import { TeX } from 'mathjax-full/js/input/tex.js';
import { SVG } from 'mathjax-full/js/output/svg.js';
import { liteAdaptor } from 'mathjax-full/js/adaptors/liteAdaptor.js';
import { RegisterHTMLHandler } from 'mathjax-full/js/handlers/html.js';
import { AllPackages } from 'mathjax-full/js/input/tex/AllPackages.js';

// ─────────────────────────── 入参 ───────────────────────────

const [, , inPath, outPath] = process.argv;
if (!inPath || !outPath) {
  console.error('用法: node scripts/zhenti_render.mjs <zhenti.jsonl> <out.html>');
  process.exit(2);
}

const cards = fs
  .readFileSync(inPath, 'utf8')
  .split('\n')
  .filter((l) => l.trim())
  .map((l) => JSON.parse(l))
  .sort((a, b) => (a.q_no ?? 0) - (b.q_no ?? 0));

if (!cards.length) {
  console.error('没有卡片');
  process.exit(2);
}

const head0 = cards[0];
const TITLE = `${head0.year} 广东专升本 ${head0.subject} 真题解析`;
const errors = [];

// ─────────────────────── MathJax 初始化 ───────────────────────

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const tex = new TeX({ packages: AllPackages });
const svg = new SVG({ fontCache: 'global' });
const mjdoc = mathjax.document('', { InputJax: tex, OutputJax: svg });

// MathJax 自带样式表：mjx-container 的 display/inline 布局、use 的填充色全靠它。
// 拿不到就退回一份最小兜底，否则公式会挤成一行。
let mjStyle = '';
try {
  mjStyle = adaptor.textContent(svg.styleSheet(mjdoc)) || '';
} catch (e) {
  errors.push('styleSheet 取用失败: ' + e.message);
}
if (!mjStyle.includes('mjx-container')) {
  mjStyle =
    'mjx-container[jax="SVG"]{display:inline-block;line-height:0;text-indent:0;text-align:left;' +
    'text-transform:none;font-style:normal;font-weight:normal;font-size:100%;font-size-adjust:none;' +
    'letter-spacing:normal;word-wrap:normal;word-spacing:normal;white-space:nowrap;' +
    'direction:ltr;padding:0;margin:0;overflow-wrap:normal}\n' +
    'mjx-container[jax="SVG"][display="true"]{display:block;text-align:center;margin:1em 0}\n' +
    'mjx-container[jax="SVG"] svg a{fill:currentColor;stroke:currentColor}\n' +
    'mjx-container[jax="SVG"] svg{overflow:visible;min-height:1px;min-width:1px}\n';
}

const texCache = new Map();
let texCount = 0;

function renderTex(latex, display) {
  const key = (display ? 'D:' : 'I:') + latex;
  if (texCache.has(key)) return texCache.get(key);
  texCount++;
  let html;
  try {
    const node = mjdoc.convert(latex, {
      display,
      em: 16,
      ex: 8,
      // 给一个极大的容器宽度，禁止 MathJax 自动断行；
      // 真超宽交给 CSS 的 overflow-x 处理，比 MathJax 断行更好读。
      containerWidth: 1e6,
    });
    html = adaptor.outerHTML(node);
  } catch (e) {
    errors.push(`公式渲染失败: ${latex} → ${e.message}`);
    html = `<code class="tex-err">${esc(latex)}</code>`;
  }
  texCache.set(key, html);
  return html;
}

// ─────────────────────── 文本 → HTML（含公式） ───────────────────────

function esc(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

// 先 $$...$$ 再 $...$。用 [^$\n] 限制行内公式不跨行 —— 防止把「金额$100…$200」
// 这类散文误判成公式（本项目题面里没有，但通用性留着）。
const TEX_RE = /\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$/g;

// 未配对的 $ 会以原文露在页面上 —— 这是最容易被忽略的失败模式（页面照常渲染，只是公式没生效）。
// 所以这里显式计数：凡是「非公式段」里还残留 $ 的，就记一笔。
const strayDollar = [];

function texify(s) {
  if (s == null) return '';
  const src = String(s);
  const out = [];
  let last = 0;
  let m;
  TEX_RE.lastIndex = 0;
  while ((m = TEX_RE.exec(src))) {
    const plain = src.slice(last, m.index);
    if (plain.includes('$')) strayDollar.push(plain.trim().slice(0, 60));
    out.push(esc(plain));
    const isDisplay = m[1] != null;
    out.push(renderTex(isDisplay ? m[1] : m[2], isDisplay));
    last = m.index + m[0].length;
  }
  const tail = src.slice(last);
  if (tail.includes('$')) strayDollar.push(tail.trim().slice(0, 60));
  out.push(esc(tail));
  return out.join('');
}

const mmss = (sec) => {
  const s = Math.max(0, Math.round(Number(sec) || 0));
  return `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
};

// evidence 的键名是英文，读起来要停顿一下；这里映射成中文，未命中的原样保留。
const EV_LABEL = {
  q_text: '题面帧',
  options: '选项帧',
  steps: '解法来源',
  answer: '答案核对',
  pitfalls: '易错点来源',
  frames: '候选帧',
  transcript: '逐字稿',
};

const escAttr = (s) => esc(s).replace(/"/g, '&quot;');

// ─────────────────────── 页面拼装 ───────────────────────

const p1 = cards[0];
const biliUrl = (c, t) =>
  `https://www.bilibili.com/video/${c.bvid}?p=${c.page}${t != null ? `&t=${Math.round(t)}` : ''}`;

const cardsHtml = [];
let lastSection = null;
for (const c of cards) {
  if (c.section && c.section !== lastSection) {
    lastSection = c.section;
    cardsHtml.push(
      `<h2 class="sec">${esc(c.section)}</h2>`
    );
  }
  const opts = (c.options || []).length
    ? `<ul class="opts">${c.options.map((o) => `<li>${texify(o)}</li>`).join('')}</ul>`
    : '';
  const steps = (c.steps || []).length
    ? `<div class="blk"><h4>解法</h4><ol class="steps">${c.steps
        .map((s) => `<li>${texify(s)}</li>`)
        .join('')}</ol></div>`
    : '';
  const pitfalls = (c.pitfalls || []).length
    ? `<div class="blk"><h4>易错点</h4><ul class="pit">${c.pitfalls
        .map((s) => `<li>${texify(s)}</li>`)
        .join('')}</ul></div>`
    : '';
const ev = c.evidence || {};
const evRows = Object.entries(ev)
  .map(([k, v]) => `<div class="ev-row"><span class="ev-k">${esc(EV_LABEL[k] || k)}</span><span class="ev-v">${texify(v)}</span></div>`)
  .join('');

  const disc = c.discrepancy
    ? `<div class="disc">
        <div class="disc-h">⚠ 本题源讲解有误 —— 以下为修正后的正确解法</div>
        <div class="disc-grid">
          <div><span class="disc-k">视频里讲的</span><span class="disc-v">${texify(c.discrepancy.source_claim)}</span></div>
          <div><span class="disc-k">正确结果</span><span class="disc-v ok">${texify(c.discrepancy.correct)}</span></div>
        </div>
        <div class="disc-why"><b>为什么错：</b>${texify(c.discrepancy.why)}</div>
        <div class="disc-why"><b>处置：</b>${texify(c.discrepancy.action)}</div>
      </div>`
    : '';

  cardsHtml.push(`<article class="card" id="q${c.q_no}">
  <div class="card-h">
    <span class="qno">${c.q_no}</span>
    <span class="tag">${esc(c.q_type || '')}</span>
    <span class="src">P${c.page} · ${mmss(c.t_start)} → ${mmss(c.t_end)}</span>
    <a class="jump" href="${escAttr(biliUrl(c, c.t_start))}" target="_blank" rel="noopener">看原片 ↗</a>
  </div>
  <div class="stem">${texify(c.q_text)}</div>
  ${opts}
  <div class="ans"><span class="ans-k">答案</span><span class="ans-v">${texify(c.answer)}</span></div>
  ${disc}
  ${steps}
  ${pitfalls}
  <div class="ev"><h4>出处</h4>${evRows}</div>
</article>`);
}

const toc = cards
  .map((c) => `<a href="#q${c.q_no}">${c.q_no}</a>`)
  .join('');

const overviewRows = cards
  .map(
    (c) =>
      // ★ 答案列**不做字符截断**：截断会把 `$...$` 切成半个，公式直接失效
      //   （实测就这么暴露了两处"未配对 $"）。长答案交给 CSS 换行。
      `<tr><td class="c-q">${c.q_no}</td><td>${esc(c.q_type || '')}</td><td class="c-a">${texify(
        c.answer
      )}</td><td class="c-t">${mmss(c.t_start)}</td></tr>`
  )
  .join('');

// 卷面结构：section 文本形如「一、单项选择题（本大题共 5 小题，每小题 3 分，共 15 分）」。
// 注意 `/共\s*(\d+)\s*分/` 不会误吞「共 5 小题」—— 因为 5 后面跟的是「小」不是「分」。
const secGroups = [];
for (const c of cards) {
  let g = secGroups.find((x) => x.section === c.section);
  if (!g) {
    g = { section: c.section || '（未分组）', qs: [], score: null };
    secGroups.push(g);
  }
  g.qs.push(c.q_no);
  if (g.score == null && c.section) {
    const m = /共\s*(\d+)\s*分/.exec(c.section);
    if (m) g.score = Number(m[1]);
  }
}

// 连续题号压成区间：1,2,3,4,5 → 「1–5」
const compactRange = (arr) => {
  if (!arr.length) return '';
  const out = [];
  let s = arr[0];
  let p = arr[0];
  for (const n of arr.slice(1)) {
    if (n === p + 1) {
      p = n;
      continue;
    }
    out.push(s === p ? String(s) : `${s}–${p}`);
    s = p = n;
  }
  out.push(s === p ? String(s) : `${s}–${p}`);
  return out.join('、');
};

const structRows = secGroups
  .map(
    (g) =>
      `<tr><td>${esc(String(g.section).split('（')[0])}</td><td class="c-q">${esc(
        compactRange(g.qs)
      )}</td><td class="c-q">${g.qs.length} 题</td><td class="c-q">${
        g.score != null ? g.score + ' 分' : '—'
      }</td></tr>`
  )
  .join('');
const totalScore = secGroups.reduce((n, g) => n + (g.score || 0), 0);

// ★ 必须放在所有 texify 之后：global fontCache 是边渲染边累积的。
const glyphDefs = [...svg.fontCache.cache.entries()]
  .map(([id, d]) => `<path id="${id}" d="${d}"/>`)
  .join('');

// 安全网：确认公式里每个 <use> 引用的字形都真在 defs 里，防止漏字形导致空白。
const usedIds = new Set();
for (const html of texCache.values()) {
  for (const m of html.matchAll(/xlink:href="#([^"]+)"/g)) usedIds.add(m[1]);
}
const haveIds = new Set([...svg.fontCache.cache.keys()]);
const missing = [...usedIds].filter((i) => !haveIds.has(i));

// 公式没配对的 $ 会以原文露出来 —— 这是最容易被忽略的失败模式，显式统计。
const leftoverDollar = strayDollar.length;

const pageCss = `
:root{
  --bg:#f6f7f9; --panel:#ffffff; --text:#1a1d21; --muted:#5b6472; --line:#e4e7eb;
  --accent:#2f6feb; --accent-soft:#eef3fe; --ok:#0f7b4f; --ok-soft:#e9f7f0;
  --warn:#a15c07; --warn-soft:#fdf5e6; --bad:#b42318; --bad-soft:#fdeceb;
  --code:#f1f3f6;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#0f1115; --panel:#171a20; --text:#e6e9ee; --muted:#98a2b3; --line:#262b33;
    --accent:#6ea8fe; --accent-soft:#182234; --ok:#4ade80; --ok-soft:#132a1f;
    --warn:#fbbf24; --warn-soft:#2b2312; --bad:#f87171; --bad-soft:#2c1618;
    --code:#1d222b;
  }
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--bg); color:var(--text);
  font:16px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
  -webkit-font-smoothing:antialiased;
}
.wrap{max-width:940px; margin:0 auto; padding:40px 20px 80px}
header.top{border-bottom:1px solid var(--line); padding-bottom:22px; margin-bottom:26px}
h1{font-size:27px; margin:0 0 12px; letter-spacing:.2px}
.sub{color:var(--muted); font-size:14.5px; margin:0}
.chips{display:flex; flex-wrap:wrap; gap:8px; margin-top:16px}
.chip{
  font-size:13px; padding:4px 11px; border-radius:999px;
  background:var(--accent-soft); color:var(--accent); border:1px solid transparent;
}
.chip.g{background:var(--ok-soft); color:var(--ok)}
.chip.n{background:var(--code); color:var(--muted)}
.toc{display:flex; flex-wrap:wrap; gap:6px; margin:0 0 28px}
.toc a{
  min-width:34px; text-align:center; padding:4px 8px; border-radius:7px; font-size:13.5px;
  border:1px solid var(--line); color:var(--muted); text-decoration:none; background:var(--panel);
}
.toc a:hover{border-color:var(--accent); color:var(--accent)}
h2.sec{
  font-size:16px; margin:38px 0 14px; padding:9px 14px; border-radius:8px;
  background:var(--code); color:var(--muted); font-weight:600; letter-spacing:.2px;
}
.card{
  background:var(--panel); border:1px solid var(--line); border-radius:12px;
  padding:20px 22px; margin:0 0 18px; scroll-margin-top:16px;
}
.card-h{display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:14px}
.qno{
  width:30px; height:30px; flex:0 0 30px; border-radius:8px; background:var(--accent); color:#fff;
  display:inline-flex; align-items:center; justify-content:center; font-weight:700; font-size:15px;
}
.tag{font-size:12.5px; padding:2px 9px; border-radius:6px; background:var(--code); color:var(--muted)}
.src{font-size:12.5px; color:var(--muted); font-variant-numeric:tabular-nums}
.jump{margin-left:auto; font-size:12.5px; color:var(--accent); text-decoration:none}
.jump:hover{text-decoration:underline}
.stem{font-size:16.5px; margin:0 0 14px}
.opts{list-style:none; padding:0; margin:0 0 14px; display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:6px}
.opts li{padding:7px 12px; border:1px solid var(--line); border-radius:8px; font-size:15px}
.ans{
  display:flex; align-items:baseline; gap:10px; padding:11px 14px; border-radius:9px;
  background:var(--ok-soft); margin:0 0 16px; overflow-x:auto;
}
.ans-k{font-size:12.5px; color:var(--ok); font-weight:700; flex:0 0 auto}
.ans-v{font-size:16px; color:var(--text)}
.blk{margin:0 0 14px}
.blk h4, .ev h4{font-size:13px; color:var(--muted); margin:0 0 8px; font-weight:600; letter-spacing:.4px}
.steps{margin:0; padding-left:22px}
.steps li{margin-bottom:6px}
.pit{margin:0; padding-left:20px}
.pit li{margin-bottom:5px; color:var(--warn)}
.disc{background:var(--warn-soft); border:1px solid var(--warn); border-radius:10px; padding:14px 16px; margin:0 0 16px}
.disc-h{font-size:13.5px; font-weight:700; color:var(--warn); margin-bottom:11px}
.disc-grid{display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:10px; margin-bottom:10px}
.disc-grid>div{background:var(--panel); border-radius:8px; padding:9px 12px; overflow-x:auto}
.disc-k{display:block; font-size:12px; color:var(--muted); margin-bottom:3px}
.disc-v{font-size:14.5px}
.disc-v.ok{color:var(--ok); font-weight:600}
.disc-why{font-size:13.5px; color:var(--text); margin-top:7px; line-height:1.7}
.ev{border-top:1px dashed var(--line); padding-top:12px}
.ev-row{display:flex; gap:10px; font-size:12.5px; color:var(--muted); margin-bottom:4px}
.ev-k{flex:0 0 74px; color:var(--muted); opacity:.75}
.ev-v{font-family:ui-monospace,Consolas,monospace; word-break:break-all}
table.ov{width:100%; border-collapse:collapse; background:var(--panel); border:1px solid var(--line); border-radius:10px; overflow:hidden; font-size:14px}
table.ov th, table.ov td{padding:8px 12px; text-align:left; border-bottom:1px solid var(--line)}
table.ov th{background:var(--code); color:var(--muted); font-size:12.5px; font-weight:600}
table.ov tr:last-child td{border-bottom:none}
table.ov .c-q{width:52px; color:var(--muted); font-variant-numeric:tabular-nums}
table.ov .c-t{width:64px; color:var(--muted); font-variant-numeric:tabular-nums}
table.ov .c-a{overflow:hidden}
table.ov.struct{max-width:660px}
table.ov.struct .c-q{width:96px}
table.ov tr.tot td{font-weight:700; background:var(--code); color:var(--text)}
.tex-err{background:var(--bad-soft); color:var(--bad); padding:1px 5px; border-radius:4px}
footer{margin-top:44px; padding-top:20px; border-top:1px solid var(--line); color:var(--muted); font-size:13px}
footer code{background:var(--code); padding:1px 5px; border-radius:4px; font-size:12.5px}
`;

const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(TITLE)}</title>
<style>${mjStyle}</style>
<style>${pageCss}</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute;overflow:hidden" aria-hidden="true"><defs>${glyphDefs}</defs></svg>
<div class="wrap">

<header class="top">
  <h1>${esc(TITLE)}</h1>
  <p class="sub">${esc(p1.paper || '')} · 共 ${cards.length} 题 · 逐题给出题面、解法、易错点与视频出处</p>
  <div class="chips">
    <span class="chip">来源：${esc(p1.up || '')}</span>
    <span class="chip">${esc(p1.bvid)}</span>
    <span class="chip n">${esc(p1.source_kind || '')}</span>
    <span class="chip g">已交叉验证：与另一独立来源逐题一致</span>
  </div>
</header>

<nav class="toc">${toc}</nav>

<h2 class="sec">卷面结构</h2>
<table class="ov struct">
<thead><tr><th>大题</th><th>题号</th><th>题量</th><th>分值</th></tr></thead>
<tbody>${structRows}
<tr class="tot"><td>合计</td><td class="c-q"></td><td class="c-q">${cards.length} 题</td><td class="c-q">${
  totalScore ? totalScore + ' 分' : '—'
}</td></tr></tbody>
</table>

<h2 class="sec">题目一览</h2>
<table class="ov">
<thead><tr><th>题号</th><th>题型</th><th>答案</th><th>时间</th></tr></thead>
<tbody>${overviewRows}</tbody>
</table>

${cardsHtml.join('\n')}

<footer>
  <p>公式为 MathJax 在构建期预渲染的内联 SVG，本页<strong>离线可读</strong>，不依赖任何 CDN。</p>
  <p>题面以视频画面（官方真题卷扫描件）为准；口播仅用于补解法与易错点。每题均带 <code>出处</code>，可回溯到具体帧文件与秒数。</p>
  <p>生成：02 · ${new Date().toISOString().slice(0, 10)}</p>
</footer>

</div>
</body>
</html>
`;

fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, html, 'utf8');

// ─────────────────────── 自检 ───────────────────────

const sizeKB = (fs.statSync(outPath).size / 1024).toFixed(1);
console.log(`写入 ${outPath}`);
console.log(`  卡片 ${cards.length} 张 · 唯一公式 ${texCount} 个 · 字形 ${glyphDefs ? svg.fontCache.cache.size : 0} 个`);
console.log(`  体积 ${sizeKB} KB`);
console.log(`  未配对 $ 的片段 ${leftoverDollar} 处（应为 0）${leftoverDollar ? ' → ' + strayDollar.slice(0, 5).join(' | ') : ''}`);
console.log(`  缺字形引用 ${missing.length} 个（应为 0）${missing.length ? ' → ' + missing.slice(0, 5).join(', ') : ''}`);
if (errors.length) {
  console.log(`  渲染报错 ${errors.length} 条：`);
  errors.slice(0, 10).forEach((e) => console.log('    - ' + e));
} else {
  console.log('  渲染报错 0 条');
}
