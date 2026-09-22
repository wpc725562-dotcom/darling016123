import { writeFileSync } from 'node:fs';

const ANKI = 'http://127.0.0.1:8765';

async function invoke(action, params = {}) {
  const res = await fetch(ANKI, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action, version: 6, params }),
  });
  const data = await res.json();
  if (data.error) throw new Error(action + ': ' + data.error);
  return data.result;
}

const G = '专升本英语-语法';
const V = '专升本英语-写题陌生词汇';

// ============ 语法卡：全部来自 2015 全国I卷第 1 篇（阳朔游记）============
// 前三张是 09-21 实际答错的三个空
const grammar = [
  // 🔴 错题 1
  ['It was raining lightly when I ___ (arrive) in Yangshuo.<br><br>🔴 你填了 <b>arriving</b> —— 为什么错？',
   '<b>arrived</b><br><br>判据：<b>点动作 vs 线动作</b><br>· <code>was raining</code> 雨<b>能持续</b> → 线动作 → 用进行时<br>· <code>arrive</code> 到达是<b>一刹那</b> → 点动作 → 用一般过去时<br><br>⚠️ arrive / leave / start / stop 这类都是点动作，不能用进行时。'],

  // 🔴 错题 2
  ['A few hours ___, I\u2019d been at home in Hong Kong.<br><br>🔴 你填了 <b>after</b> —— 为什么错？',
   '<b>before / earlier</b>（几个小时<b>前</b>）<br><br>线索：<code>I\u2019d been</code> = had been（<b>过去完成时</b>）→ 表示「<b>过去的过去</b>」→ 需要「在……之前」的时间状语<br><br>⚠️ after 指向<b>之后</b>，与 had been 的时态逻辑矛盾。'],

  // 🔴 错题 3
  ['it\u2019s only an hour away ___ car<br><br>🔴 你填了 <b>for</b> —— 为什么错？',
   '<b>by</b> —— <code>by car</code> 乘汽车<br><br>固定搭配：<b>by + 交通工具</b>（car / bus / train / plane / bike）<br>⚠️ <b>不加冠词</b>：<code>by car</code> ✅ / <code>by a car</code> ❌<br><br>本句意思：开车只要一小时。'],

  // ⭐ 你主动问的那个问题
  ['It was raining when I ___ (arrive) in Yangshuo.<br><br>空前的 <code>when I</code> 是什么结构？<b>为什么这里必须填谓语</b>？',
   '<b>时间状语从句</b>。<br><br>判据：<b>从句里有主语 <code>I</code> → 必须有谓语</b> → 填 <code>arrived</code><br><br>⚠️ 关键：「一个句子只有一个谓语」管的是<b>一个分句</b>。主句和从句<b>各有各的谓语</b>：<br>· 主句 <code>was raining</code><br>· 从句 <code>arrived</code><br><br>对比：<code>when arriving</code> 合法 —— 因为它<b>省略了主语</b>，已经不是从句了。'],

  // 非谓语 · 被动
  ['A study of travelers ___ (conduct) by the website TripAdvisor names Yangshuo...<br><br>填什么？<b>看什么线索</b>？',
   '<b>conducted</b>（过去分词）<br><br>线索：看到空后 <b>by</b> → <b>被动</b>关系 → 用过去分词<br>（一份研究<b>被</b>网站<b>进行</b>）<br><br>结构：过去分词短语作<b>后置定语</b>，修饰 <code>study</code>。'],

  // 非谓语 · 主动
  ['... quick getaways here for people ___ (live) in Shanghai and Hong Kong.<br><br>填什么？为什么？',
   '<b>living</b>（现在分词）<br><br>线索：<code>people</code> 和 <code>live</code> 是<b>主动</b>关系（人<b>自己</b>住）→ 现在分词<br><br>对比记忆：<br>· <code>conducted by</code> 被动 → 过去分词<br>· <code>people living</code> 主动 → 现在分词'],

  // 定语从句
  ['... the waters of the Li River ___ are pictured by artists...<br><br>填什么关系词？为什么？',
   '<b>that / which</b><br><br>先行词 <code>Li River</code> 是<b>物</b>，在从句里作<b>主语</b> → that / which<br><br>⚠️ 不能用 who —— who 只能指<b>人</b>。'],

  // 名词复数
  ['... pictured by artists in so many Chinese ___ (painting).<br><br>填什么？',
   '<b>paintings</b><br><br>线索：<b>so many</b> 后面必须跟<b>可数名词复数</b>。<br>（so many + 复数名词是固定搭配）'],

  // 主谓一致
  ['Yangshuo ___ (be) really beautiful.<br><br>填什么？',
   '<b>is</b><br><br>Yangshuo 是<b>单数</b>地名 → 用 is。<br><br>⚠️ 中文说「阳朔很漂亮」不带单复数概念，但英语里地名按单数处理。'],
];

// ============ 生词卡：2015 第 1 篇 ============
const vocab = [
  ['... with its ___ ___.<br><br>（呛人的雾霾）',
   '<b>choking smog</b> —— 呛人的雾霾<br><br>· choke 使窒息、呛到<br>· smog = smoke（烟）+ fog（雾）<br><br>（香港家里呛人的雾霾 ↔ 后文「这里空气干净」形成对比）'],

  ['... a dream place for tourists seeking the ___ mountain tops ...<br><br>（石灰岩）',
   '<b>limestone</b> —— 石灰岩<br><br>拆开记：lime（石灰）+ stone（石头）<br><br>（桂林的石灰岩山峰，也就是「喀斯特地貌」）'],

  ['It was raining lightly when I arrived in Yangshuo just before ___.<br><br>（黎明、破晓）',
   '<b>dawn</b> —— 黎明、破晓<br><br><code>just before dawn</code> = 天刚亮之前'],

  ['I\u2019d ___ nearby Guilin ... Instead, I\u2019d head straight for Yangshuo.<br><br>（跳过、略过不去）',
   '<b>skipped</b> —— 跳过、略过<br><br>⚠️ 双写 p 再加 ed：skip → <b>skipped</b><br><br>（作者跳过桂林、直奔阳朔）'],

  ['Instead, I\u2019d head straight for Yangshuo.<br><br>（直奔、径直前往）',
   '<b>head straight for</b> —— 直奔、径直前往<br><br>· head 作动词 = 朝……去<br>· straight = 直接、不绕路'],

  ['... and offers all the ___ of the better-known city.<br><br>（风景、景色）',
   '<b>scenery</b> —— 风景、景色<br><br>⚠️ <b>不可数名词</b>，没有复数形式（不能说 sceneries）'],

  ['... names Yangshuo as one of the top 10 ___ in the world.<br><br>（目的地）',
   '<b>destination</b> —— 目的地<br><br><code>top 10 destinations</code> = 十大目的地'],

  ['... arranges quick ___ here for people living in Shanghai and Hong Kong.<br><br>（短假出游）',
   '<b>getaway</b> —— 短假出游、逃离日常的小旅行<br><br>拆开记：get + away（走开）→ 出去放松一趟<br><br><code>quick getaway</code> = 说走就走的短途旅行'],
];

for (const d of [G, V]) {
  await invoke('createDeck', { deck: d });
  console.log('牌组就绪:', d);
}

const toNote = (deck, pair, tags) => ({
  deckName: deck,
  modelName: '问答题',
  fields: { 正面: pair[0], 背面: pair[1] },
  options: { allowDuplicate: false },
  tags,
});

const notes = [
  ...grammar.map((p) => toNote(G, p, ['英语语法', '语法填空2015'])),
  ...vocab.map((p) => toNote(V, p, ['英语生词', '语法填空2015'])),
];

console.log(`\n准备写入 ${notes.length} 张（语法 ${grammar.length} + 生词 ${vocab.length}）`);
const res = await invoke('addNotes', { notes });
console.log('addNotes 返回:');
let ok = 0, dup = 0;
res.forEach((id, i) => {
  if (id === null) { dup++; console.log(`  ${i + 1}: 已存在，跳过`); }
  else { ok++; console.log(`  ${i + 1}: ${id}`); }
});
console.log(`→ 新建 ${ok} 张，跳过重复 ${dup} 张`);

// TSV 落盘（项目惯例）
const tsv = (arr) => arr.map((p) => p[0] + '\t' + p[1]).join('\n');
const base = 'D:/deeepseek/zhuan-sheng-ben-notes/knowledge/anki_cards/';
writeFileSync(base + '英语-语法填空2015-语法-cards.tsv', tsv(grammar) + '\n', 'utf8');
writeFileSync(base + '英语-语法填空2015-生词-cards.tsv', tsv(vocab) + '\n', 'utf8');
console.log('\nTSV 已写入 knowledge/anki_cards/');

// ============ 回读校验（不可省）============
console.log('\n=== 回读校验 ===');
for (const d of [G, V]) {
  const ids = await invoke('findCards', { query: `deck:"${d}"` });
  console.log(`  ${d}: ${ids.length} 张`);
}
const gNotes = await invoke('findNotes', { query: `deck:"${G}" tag:语法填空2015` });
const vNotes = await invoke('findNotes', { query: `deck:"${V}" tag:语法填空2015` });
console.log(`  带「语法填空2015」标签: 语法 ${gNotes.length} 张 / 生词 ${vNotes.length} 张`);

const spot = await invoke('notesInfo', { notes: [gNotes[0], gNotes[gNotes.length - 1], vNotes[0], vNotes[vNotes.length - 1]] });
console.log('\n=== 抽查 4 张实际内容 ===');
spot.forEach((n, i) => {
  console.log(`--- ${i + 1} (id ${n.noteId}) ---`);
  console.log('  正面:', (n.fields['正面']?.value || '').replace(/<[^>]+>/g, ' ').slice(0, 90));
  console.log('  背面:', (n.fields['背面']?.value || '').replace(/<[^>]+>/g, ' ').slice(0, 90));
});
