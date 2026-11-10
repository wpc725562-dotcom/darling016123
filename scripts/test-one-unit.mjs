/**
 * 单单元提炼冒烟测试 —— 验证「号池模型能否按 _extract 的硬契约产出 md」。
 *
 * 用法：node test-one-unit.mjs <unit-txt> [model]
 * 默认模型 dots-studio/dots-3-note-preview:free（512K ctx / 460K out / 中文笔记向）
 *
 * 判据（与 bili-to-studio-kaodian-import §3 一致）：
 *   - 首行 # <BV>_<NN> · <科目> · <标题>
 *   - 有 > 覆盖：Px–Py（N 节）
 *   - 每个 ### 下四行字段齐全且顺序固定：要点 / 关键概念 / 相互关系 / 出处
 *   - 出处里的 P 号必须在输入里真实存在
 *   - 密度 3.2–3.8 个 ### / 万字符
 */
import fs from 'node:fs';
import path from 'node:path';

const ENDPOINT = process.env.OFM_BASE || 'http://127.0.0.1:18999/v1';
const KEY = process.env.OFM_KEY || 'kilo-free';
const unitPath = process.argv[2];
const MODEL = process.argv[3] || 'dots-studio/dots-3-note-preview:free';
if (!unitPath) { console.error('用法: node test-one-unit.mjs <unit.txt> [model]'); process.exit(1); }

const base = path.basename(unitPath, '.txt');
const m = base.match(/^(BV[0-9A-Za-z]+)_(\d+)$/);
if (!m) { console.error('文件名不符合 <BV>_<NN>.txt'); process.exit(1); }
const [, BV, NN] = m;

const raw = fs.readFileSync(unitPath, 'utf8');
const pages = [...raw.matchAll(/^=== P(\d+) \| (.+?) \|/gm)].map((x) => ({ p: Number(x[1]), title: x[2].trim() }));
if (!pages.length) { console.error('输入里没有 === Pn | 标记'); process.exit(1); }
const pLo = Math.min(...pages.map((x) => x.p));
const pHi = Math.max(...pages.map((x) => x.p));
const chars = raw.length;

const SYS = `你是专升本课程的字幕提炼员。输入是 B 站课程的 ASR 字幕拼接，每个分P 以
"=== P3 | 【第一章】1.1 函数的概念 | 1750s ===" 开头，正文逐句一行、无标点、有同音错字。

输出必须严格遵守下面的 Markdown 契约，不要任何前言后语、不要代码块包裹：

# ${BV}_${NN} · <科目> · <视频标题原文>

> 覆盖：P${pLo}–P${pHi}（${pages.length} 节）

## <主题名>

### <知识点名>
- **要点**：<一到三句，讲清是什么/怎么用>
- **关键概念**：\`概念A\`、\`概念B\`
- **相互关系**：<与前后知识点的关系，或与考点的关系>
- **出处**：P<n>

硬性规则：
1. **出处**里的 P 号只能取输入里真实存在的 === Pn | 标记，绝对不许编造或外推。
2. 每个 ### 下面四行必须齐全，顺序固定为 要点 / 关键概念 / 相互关系 / 出处，少一行就算失败。
3. 丢掉自我介绍、招生宣传、花絮、"点赞投币"、资料下载引导这类内容。
4. 提炼密度参考：每万字符 3.2–3.8 个 ###。本单元 ${chars} 字符，目标 ${
  Math.round((chars / 10000) * 3.2)}–${Math.round((chars / 10000) * 3.8)} 个知识点，6–12 个 ## 主题。
5. 同音错字要按上下文纠正（如「诺比达」→洛必达）。`;

const body = {
  model: MODEL,
  messages: [
    { role: 'system', content: SYS },
    { role: 'user', content: raw },
  ],
  max_tokens: Number(process.env.MAXTOK || 32000),
  stream: !!process.env.STREAM,
};

const t0 = Date.now();
const res = await fetch(`${ENDPOINT}/chat/completions`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${KEY}` },
  body: JSON.stringify(body),
  signal: AbortSignal.timeout(600000),
});

/** 流式收 SSE，拼回完整文本；同时记录首字节/首 token 时刻，用来区分「排队慢」和「生成慢」 */
async function readStream(r) {
  const reader = r.body.getReader();
  const dec = new TextDecoder();
  let buf = '';
  let text = '';
  let usage = {};
  let firstByte = 0;
  let chunks = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    if (!firstByte) firstByte = Date.now();
    buf += dec.decode(value, { stream: true });
    const lines = buf.split('\n');
    buf = lines.pop() || '';
    for (const line of lines) {
      const s = line.trim();
      if (!s.startsWith('data:')) continue;
      const payload = s.slice(5).trim();
      if (payload === '[DONE]') continue;
      try {
        const j = JSON.parse(payload);
        const d = j.choices?.[0]?.delta?.content;
        if (d) { text += d; chunks++; }
        if (j.usage) usage = j.usage;
      } catch { /* 半个 JSON，忽略 */ }
    }
  }
  return { text, usage, firstByte: firstByte ? ((firstByte - t0) / 1000).toFixed(1) : '?', chunks };
}

const elapsed0 = ((Date.now() - t0) / 1000).toFixed(1);
if (!res.ok) {
  const t = await res.text();
  console.log(`✗ HTTP ${res.status} ${elapsed0}s: ${t.slice(0, 300)}`);
  process.exit(1);
}
let out, usage, ttfb = '-', nChunk = 0;
if (body.stream) {
  const r = await readStream(res);
  out = r.text; usage = r.usage; ttfb = r.firstByte; nChunk = r.chunks;
} else {
  const j = await res.json();
  if (j.error) {
    console.log(`✗ 调用失败 ${res.status} ${elapsed0}s: ${JSON.stringify(j.error).slice(0, 300)}`);
    process.exit(1);
  }
  out = j.choices[0].message.content || '';
  usage = j.usage || {};
}
const elapsed = ((Date.now() - t0) / 1000).toFixed(1);

// ── 契约校验 ──
const lines = out.replace(/^\s*\r?\n/, '').split(/\r?\n/);
const headOk = new RegExp(`^#\\s*${BV}_${NN}\\s*·`).test(lines[0] || '');
const coverLine = lines.find((l) => /^>\s*覆盖：/.test(l)) || '';
const topics = (out.match(/^##\s+/gm) || []).length;
const points = (out.match(/^###\s+/gm) || []).length;

// 四行字段完整性：逐个 ### 块检查
const blocks = out.split(/^###\s+/m).slice(1);
let fieldOk = 0, fieldBad = [];
const ORDER = ['要点', '关键概念', '相互关系', '出处'];
for (const b of blocks) {
  const got = [...b.matchAll(/^-\s*\*\*(要点|关键概念|相互关系|出处)\*\*[：:]/gm)].map((x) => x[1]);
  if (got.length === 4 && got.every((v, i) => v === ORDER[i])) fieldOk++;
  else fieldBad.push((b.split('\n')[0] || '').slice(0, 20) + ` [${got.join('/') || '无'}]`);
}

// 出处 P 号真实性
const validP = new Set(pages.map((x) => x.p));
const cited = [...out.matchAll(/\*\*出处\*\*[：:]\s*P(\d+)/g)].map((x) => Number(x[1]));
const badP = [...new Set(cited.filter((p) => !validP.has(p)))];

const density = chars > 0 ? (points / (chars / 10000)).toFixed(2) : '0';

console.log('══════ 单单元提炼冒烟 ══════');
console.log(`单元      : ${base}  (${(chars / 1024).toFixed(1)} KB / ${chars} 字符 / ${pages.length} 节 P${pLo}–P${pHi})`);
console.log(`模型      : ${MODEL}`);
console.log(`耗时      : ${elapsed}s  (首字节 ${ttfb}s${nChunk ? ` / ${nChunk} 个增量` : ''})`);
console.log(`用量      : in=${usage.prompt_tokens} out=${usage.completion_tokens} total=${usage.total_tokens}`);
console.log(`输出长度  : ${out.length} 字符`);
console.log('');
console.log(`① 首行契约     : ${headOk ? '✓' : '✗'}  ${(lines[0] || '').slice(0, 70)}`);
console.log(`② 覆盖行       : ${coverLine ? '✓' : '✗'}  ${coverLine.slice(0, 60)}`);
console.log(`③ ## 主题数    : ${topics}  ${topics >= 6 && topics <= 12 ? '✓ 在 6–12 内' : '⚠ 超出 6–12'}`);
console.log(`④ ### 知识点数 : ${points}`);
console.log(`⑤ 提炼密度     : ${density} 个/万字符  ${density >= 3.2 && density <= 3.8 ? '✓ 达标' : density < 3.2 ? '⚠ 偏粗' : '⚠ 偏密'}`);
console.log(`⑥ 四行字段齐全 : ${fieldOk}/${blocks.length} 块合规${fieldBad.length ? '  异常块: ' + fieldBad.slice(0, 3).join(' | ') : ''}`);
console.log(`⑦ 出处 P 号真实: ${badP.length === 0 ? '✓ 全部命中' : '✗ 编造 ' + badP.join(',')}  (引用 ${cited.length} 处)`);

const pass = headOk && coverLine && fieldOk === blocks.length && badP.length === 0 && points > 0;
console.log('');
console.log(pass ? '结论：✓ 契约全部通过，可批量' : '结论：✗ 有未通过项，需调提示词或换模型');

const outPath = path.join(path.dirname(unitPath), '..', '_extract', `${base}.md`);
fs.writeFileSync(outPath.replace('_units', '_units') + '.smoke', out, 'utf8');
console.log(`\n产物已存: ${outPath}.smoke`);
console.log('\n──────── 输出前 900 字符 ────────');
console.log(out.slice(0, 900));
