import { readFileSync, writeFileSync } from 'node:fs';

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

const V = '专升本英语-写题陌生词汇';

const newCards = [
  ['In 1969, the pollution was ___ along the Cuyahoga River.<br><br>（糟糕的）',
   '<b>terrible</b> —— 糟糕的、可怕的'],
  ['... the pollution was terrible ___ the Cuyahoga River.<br><br>（沿着）',
   '<b>along</b> —— 沿着（介词，顺着一条线）<br><br>⚠️ 不是"相伴" —— 它只表示位置，没有"一起"的意思'],
  ['It was ___ that it could ever be cleaned up.<br><br>（无法想象的）',
   '<b>unimaginable</b> —— 无法想象的<br><br>拆开记：un-（不）+ imagine（想象）+ -able（能……的）'],
  ['The river was so polluted that it actually ___ ___ and burned.<br><br>（起火）',
   '<b>caught fire</b> —— 起火、着火<br><br>catch 的过去式是 <b>caught</b>（不是 catched）'],
  ['Maybe you are ___ an impossible situation.<br><br>（面对）',
   '<b>facing</b> —— 面对（face 的现在分词）<br><br>be + doing = 进行时：正在面对'],
  ['Maybe you are facing an ___ ___.<br><br>（棘手的困境）',
   '<b>impossible situation</b> —— 无法解决的处境、棘手的困境'],
  ["... don't know how to control your ___ ___ use.<br><br>（信用卡）",
   '<b>credit card</b> —— 信用卡'],
  ['While there are ___ ___ of instant transformation...<br><br>（精彩的故事）',
   '<b>amazing stories</b> —— 精彩的故事、令人惊叹的故事'],
  ['... the changes are gradual and ___ a lot of effort and work.<br><br>（需要）',
   '<b>require</b> —— 需要、要求'],
];

const notes = newCards.map((p) => ({
  deckName: V,
  modelName: '问答题',
  fields: { 正面: p[0], 背面: p[1] },
  options: { allowDuplicate: false },
  tags: ['英语生词', '语法填空2014', '精读0919'],
}));

const res = await invoke('addNotes', { notes });
console.log('新增卡片:');
res.forEach((id, i) => console.log('  ' + (i + 1) + ': ' + id));

const tsvPath = 'D:/deeepseek/zhuan-sheng-ben-notes/knowledge/anki_cards/英语-写题陌生词汇-cards.tsv';
const old = readFileSync(tsvPath, 'utf8').replace(/\n+$/, '');
const added = newCards.map((p) => p[0] + '\t' + p[1]).join('\n');
writeFileSync(tsvPath, old + '\n' + added + '\n', 'utf8');

const total = (await invoke('findCards', { query: 'deck:"' + V + '"' })).length;
console.log('牌组总卡数:', total);
