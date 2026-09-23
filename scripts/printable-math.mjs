#!/usr/bin/env node
/**
 * scripts/printable-math.mjs —— 把可打印 HTML 里的公式占位符渲染成内联 SVG。
 *
 * 这是 `print:html` 的**第二步**：
 *   1. scripts/md-to-printable.py   把 `$...$` / `$$...$$` 抽成 `<!--MJX <d> <b64>-->`
 *   2. 本脚本                        用 mathjax-full 渲染成内联 SVG 写回
 *   3. scripts/html-to-pdf.mjs       Chrome headless 打印成 PDF
 *
 * 为什么是**构建期**渲染而不是在页面里挂 MathJax CDN：
 *   产物是给离线看、直接打印用的。挂 CDN 就有两个后果 —— 断网打开是裸 LaTeX；
 *   而且 html-to-pdf.mjs 用 `--print-to-pdf` 没有 `--virtual-time-budget`，
 *   异步渲染根本等不到，PDF 里还是裸 LaTeX。
 *   （实测确认：产物 HTML 原先**完全没有**任何数学渲染器，所以「加个 budget 就好」
 *     这个思路是错的 —— 没有异步渲染可等。）
 *
 * 三个关键实现点，照搬同仓库已验证的 scripts/zhenti_render.mjs：
 *   1. `fontCache: 'global'` —— 字形只在页面顶部出现一次。local 模式下每个公式
 *      自带一份 6~7KB 字形，本页有几千个公式，体积会差一个量级。
 *      代价：cache 是**边渲染边累积**的，必须全部渲染完再取。
 *   2. MathJax 自带样式表必须一起内联，否则 mjx-container 的 inline/display
 *      布局全失效、公式挤成一行。
 *   3. 缓存 key 要区分 inline/display —— 同一串 LaTeX 的两种排版规则不同，不能共用。
 *
 * 用法：
 *   node scripts/printable-math.mjs            # 处理 docs/public/printable 下所有 html
 *   node scripts/printable-math.mjs math       # 只处理 math 前缀
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

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const HTML_DIR = path.join(ROOT, 'docs', 'public', 'printable');
const filter = process.argv[2] || '';

// ─────────────────────── MathJax 初始化 ───────────────────────

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const tex = new TeX({ packages: AllPackages });
const svg = new SVG({ fontCache: 'global' });
const mjdoc = mathjax.document('', { InputJax: tex, OutputJax: svg });

let mjStyle = '';
try {
  mjStyle = adaptor.textContent(svg.styleSheet(mjdoc)) || '';
} catch (e) {
  console.error('⚠️  styleSheet 取用失败: ' + e.message);
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
const errors = [];

function renderTex(latex, display) {
  const key = (display ? 'D:' : 'I:') + latex;
  if (texCache.has(key)) return texCache.get(key);
  let html;
  try {
    const node = mjdoc.convert(latex, {
      display,
      em: 16,
      ex: 8,
      // 给极大容器宽度，禁止 MathJax 自动断行；真超宽交给 CSS 的 overflow-x。
      containerWidth: 1e6,
    });
    html = adaptor.outerHTML(node);
  } catch (e) {
    errors.push(`公式渲染失败: ${latex.slice(0, 60)} → ${e.message}`);
    html = `<code class="tex-err">${latex}</code>`;
  }
  texCache.set(key, html);
  return html;
}

// ─────────────────────── 主流程 ───────────────────────

// 占位符格式由 scripts/md-to-printable.py 的 _math_marker() 定义。
// base64 字母表不含 `-`，所以不可能拼出 `-->` 提前闭合注释。
const MARK_RE = /<!--MJX ([01]) ([A-Za-z0-9+/=]*)-->/g;

const files = fs
  .readdirSync(HTML_DIR)
  .filter((f) => f.endsWith('.html') && (!filter || f.startsWith(filter)))
  .sort();

if (!files.length) {
  console.error(`没有可处理的 html（目录 ${HTML_DIR}，过滤 "${filter}"）`);
  process.exit(2);
}

let processed = 0;
let skipped = 0;
let totalMarkers = 0;
const report = [];

for (const f of files) {
  const full = path.join(HTML_DIR, f);
  const src = fs.readFileSync(full, 'utf8');

  // 幂等：没有占位符就跳过（别重复注入样式与 defs）
  if (!src.includes('<!--MJX ')) {
    if (src.includes('mjx-container')) {
      skipped++;
      report.push({ f, markers: 0, note: '已渲染过，跳过' });
    } else {
      skipped++;
      report.push({ f, markers: 0, note: '无公式' });
    }
    continue;
  }

  const usedIds = new Set();
  let n = 0;

  const replaced = src.replace(MARK_RE, (_m, d, b64) => {
    const latex = Buffer.from(b64, 'base64').toString('utf8');
    const html = renderTex(latex, d === '1');
    n++;
    for (const mm of html.matchAll(/xlink:href="#([^"]+)"/g)) usedIds.add(mm[1]);
    return html;
  });

  if (n === 0) {
    skipped++;
    report.push({ f, markers: 0, note: '占位符未匹配到' });
    continue;
  }

  // 本文件只注入**自己用到**的字形，避免把全量字形表塞进每个文件
  const defs = [...usedIds]
    .map((id) => {
      const d = svg.fontCache.cache.get(id);
      return d ? `<path id="${id}" d="${d}"/>` : '';
    })
    .filter(Boolean)
    .join('');

  const missingGlyphs = [...usedIds].filter((id) => !svg.fontCache.cache.has(id));

  // 注入：样式进 <head>，字形 defs 紧贴 <body>。
  // ★ 隐藏容器不能用 display:none —— 那会破坏跨 SVG 的 <use> 引用。
  let outHtml = replaced.replace(
    '</head>',
    `<style>${mjStyle}</style>\n<style>mjx-container[jax="SVG"]{max-width:100%}\nmjx-container[jax="SVG"][display="true"]{overflow-x:auto;overflow-y:hidden}\n</style>\n</head>`
  );
  outHtml = outHtml.replace(
    '<body>',
    `<body>\n<svg width="0" height="0" style="position:absolute;overflow:hidden" aria-hidden="true"><defs>${defs}</defs></svg>`
  );

  fs.writeFileSync(full, outHtml, 'utf8');
  processed++;
  totalMarkers += n;
  report.push({ f, markers: n, glyphs: usedIds.size, missing: missingGlyphs.length });
}

// ─────────────────────── 自检 ───────────────────────

const glyphCount = svg.fontCache.cache.size;
const missingGlyphFiles = report.filter((r) => r.missing);
const stillMarked = files.filter((f) =>
  fs.readFileSync(path.join(HTML_DIR, f), 'utf8').includes('<!--MJX ')
);

// 标签配平
let badContainer = [];
let leftoverDollar = [];
for (const f of files) {
  const t = fs.readFileSync(path.join(HTML_DIR, f), 'utf8');
  const open = (t.match(/<mjx-container\b/g) || []).length;
  const close = (t.match(/<\/mjx-container>/g) || []).length;
  if (open !== close) badContainer.push(`${f} (${open}/${close})`);
  // 残留 $：先挖掉 code/pre/style/公式，剩下的才是「露在纸面上的 $」
  const stripped = t
    .replace(/<code[\s\S]*?<\/code>/g, '')
    .replace(/<pre[\s\S]*?<\/pre>/g, '')
    .replace(/<style[\s\S]*?<\/style>/g, '')
    .replace(/<mjx-container[\s\S]*?<\/mjx-container>/g, '');
  const c = (stripped.match(/\$/g) || []).length;
  if (c) leftoverDollar.push([f, c]);
}

const totalDollar = leftoverDollar.reduce((a, b) => a + b[1], 0);

console.log(`处理 ${files.length} 个文件：渲染 ${processed} 个，跳过 ${skipped} 个`);
console.log(`占位符替换总数 ${totalMarkers}`);
console.log(`唯一公式 ${texCache.size} 个 · 字形 ${glyphCount} 个`);
console.log(`渲染报错 ${errors.length} 条${errors.length ? '：' : ''}`);
errors.slice(0, 10).forEach((e) => console.log('   - ' + e));
console.log(`缺字形引用的文件 ${missingGlyphFiles.length} 个（应为 0）`);
missingGlyphFiles.slice(0, 5).forEach((r) => console.log(`   - ${r.f}: 缺 ${r.missing} 个`));
console.log(`残留未替换的占位符 ${stillMarked.length} 个文件（应为 0）${stillMarked.length ? '：' + stillMarked.slice(0, 5).join(', ') : ''}`);
console.log(`<mjx-container> 开闭不等的文件 ${badContainer.length} 个（应为 0）${badContainer.length ? '：' + badContainer.slice(0, 5).join(', ') : ''}`);
console.log(`正文残留 $ 共 ${totalDollar} 处，分布在 ${leftoverDollar.length} 个文件（货币/OCR 字面量，属预期）`);
leftoverDollar.slice(0, 8).forEach(([f, c]) => console.log(`   - ${f}: ${c}`));

const bad =
  errors.length ||
  missingGlyphFiles.length ||
  stillMarked.length ||
  badContainer.length;
console.log(bad ? '\n❌ 自检未通过' : '\n✅ 自检通过');
if (bad) process.exit(1);
