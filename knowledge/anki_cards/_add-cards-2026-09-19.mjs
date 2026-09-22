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

const grammar = [
  ['语法填空：空位<b>后面</b>跟着 <b>than</b>，该填什么词性？',
   '比较级（-er / more ...）<br><br>例：the water in the river is ___ (clean) than ever<br>→ <b>cleaner</b>'],
  ['语法填空：空位<b>前面是 be（is / was）</b>，在描述主语，该填什么词性？',
   '形容词<br><br>例：Just be ___ (patience).<br>→ <b>patient</b>'],
  ['语法填空：空位<b>后面是名词</b>，该填什么词性？',
   '形容词<br><br>例：___ (amaze) stories<br>→ <b>amazing</b>'],
  ['语法填空：空位是<b>主语</b>、后面跟着 <b>are</b>，该填什么词性？',
   '名词复数<br><br>例：the ___ (change) are gradual<br>→ <b>changes</b>'],
  ['语法填空：空位在<b>修饰动词</b>，该填什么词性？',
   '副词（-ly）<br><br>例：it ___ (actual) caught fire<br>→ <b>actually</b>'],
  ['英语语法填空：看到一个空位，<b>第一步</b>该问自己什么？',
   '先问「<b>这个空在句子里干什么活</b>」—— 看空位前后有什么词，再决定词性。<br><br>不要凭感觉造词（actualed / amazily 这种英语里不存在的形式）。'],
];

const vocab = [
  ['Finally, that hard work ___ ___ and now the water in the river is cleaner than ever.<br><br>（努力工作终于有了回报）',
   '<b>paid off</b> —— （努力 / 付出）得到回报、奏效'],
  ['While there are amazing stories of ___ ___, for most of us the changes are gradual.<br><br>（瞬间的转变）',
   '<b>instant transformation</b> —— 瞬间的转变<br><br>instant 立即的 / transformation 转变'],
  ['For most of us the changes are ___ and require a lot of effort and work.<br><br>（逐渐的）',
   '<b>gradual</b> —— 逐渐的、渐进的<br><br>副词形式：gradually'],
  ['It took years of work to reduce the ___ pollution.<br><br>（工业的）',
   '<b>industrial</b> —— 工业的<br><br>名词形式：industry 工业'],
  ['It took years of work to reduce the industrial ___.<br><br>（污染）',
   '<b>pollution</b> —— 污染'],
  ['The river wasn\u2019t changed in a few days ___ even a few months.<br><br>（甚至）',
   '<b>even</b> —— 甚至（加强"连……也"的语气）'],
];

for (const d of [G, V]) {
  await invoke('createDeck', { deck: d });
  console.log('deck ok:', d);
}

const toNote = (deck, pair, tags) => ({
  deckName: deck,
  modelName: '问答题',
  fields: { 正面: pair[0], 背面: pair[1] },
  options: { allowDuplicate: false },
  tags,
});

const notes = [
  ...grammar.map((p) => toNote(G, p, ['英语语法', '词性判断'])),
  ...vocab.map((p) => toNote(V, p, ['英语生词', '语法填空2014'])),
];

const res = await invoke('addNotes', { notes });
console.log('addNotes result:');
res.forEach((id, i) => console.log('  ' + (i + 1) + ': ' + id));

const tsv = (arr) => arr.map((p) => p[0] + '\t' + p[1]).join('\n');
const base = 'D:/deeepseek/zhuan-sheng-ben-notes/knowledge/anki_cards/';
writeFileSync(base + '英语-词性判断-语法-cards.tsv', tsv(grammar) + '\n', 'utf8');
writeFileSync(base + '英语-写题陌生词汇-cards.tsv', tsv(vocab) + '\n', 'utf8');
console.log('TSV written.');

const counts = {};
for (const d of [G, V]) {
  counts[d] = (await invoke('findCards', { query: 'deck:"' + d + '"' })).length;
}
console.log('deck counts:', JSON.stringify(counts));
