// 补建 09-24 英语阅读（2022 Passage A）的「短语/搭配」卡
// 🔴 起因：09-24 阅读破零后，只建了 1 张词形转换卡（语法牌组），
//    那篇的短语/搭配一张没建 —— 这是「做完题 ≠ 落完账」的第 7 次漏建卡。
// 选词依据：学生自陈缺口是「词认得，句子连起来不认识」⇒ 收【短语/搭配】而不是孤立单词。
// 卡型：沿用「写题陌生词汇」牌组的现有格式 —— 正面 = 原句挖空，背面 = 英文 + 中文 + 出处
const A = 'http://127.0.0.1:8765';

async function inv(action, params = {}) {
  const r = await fetch(A, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action, version: 6, params }),
  });
  const d = await r.json();
  if (d.error) throw new Error(action + ': ' + d.error);
  return d.result;
}

const DECK = '专升本英语-写题陌生词汇';
const SRC = '2022 广东专升本 阅读 Passage A';

// [正面（原句挖空）, 背面, 标签]
const items = [
  ['Danish people welcome New Year\'s Day by ___ unused plates and glasses against the doors.',
   '<b>smashing</b> —— 砸、摔碎（smash 的现在分词）<br><br>⚠️ 别跟 <code>smash</code>（动词原形）混',
   '短语'],
  ['This action is performed with the aim of ___ ___ evil spirits.',
   '<b>warding off</b> —— 驱赶、挡开（恶灵）<br><br>📌 <code>with the aim of</code> = 目的是',
   '短语'],
  ['They throw bread at the walls to ___ ___ evil spirits and bring good luck in.',
   '<b>scare away</b> —— 吓跑、赶走<br><br>📌 近义：<code>ward off</code>（驱赶）· <code>scare away</code>（吓跑）',
   '短语'],
  ['Each grape is a representation of a month of ___ ___ in the coming year.',
   '<b>good fortune</b> —— 好运<br><br>📌 近义：<code>good luck</code> · <code>lucky</code>',
   '短语'],
  ['If you are able to get all of them into your mouth, all of your wishes will ___ ___.',
   '<b>come true</b> —— 实现（愿望）<br><br>⚠️ 不用被动：不能说 <code>be come true</code>',
   '短语'],
  ['Some people stand on chairs and jump off them at midnight ___ ___ ___ ___ bringing good luck.',
   '<b>in the hopes of</b> —— 怀着……的希望<br><br>📌 对比 <code>with the aim of</code>（目的是）',
   '短语'],
  ['In preparation for New Year\'s Day, people in Ireland make sure their entire house is cleaned without a ___.',
   '<b>spot</b> —— 污点、斑点<br><br>📌 <code>without a spot</code> = 一尘不染',
   '短语'],
  ['They have the custom of throwing bread at the walls as the clock ___ midnight.',
   '<b>approaches</b> —— 临近、接近<br><br>📌 这里是动词，不是名词「方法」',
   '短语'],
  ['Every year, millions of people ___ ___ Berlin for one of Europe\'s largest New Year\'s Eve celebrations.',
   '<b>flock to</b> —— 涌向、成群结队地去<br><br>📌 <code>flock</code> 本义是「羊群」',
   '短语'],
  ['They throw parties, watch fireworks, and drink a German ___ ___.',
   '<b>sparkling wine</b> —— 起泡酒（如香槟）<br><br>📌 不是「发光酒」',
   '短语'],
  ['Families ___ lead at home by holding a flame beneath a tablespoon, then putting it into water.',
   '<b>melt</b> —— 熔化<br><br>⚠️ 过去式 <code>melted</code> / 过去分词 <code>melted</code> 或 <code>molten</code>（金属）',
   '短语'],
  ['They bake St. Basil\'s Cake with one special ___ — a coin made of gold or silver.',
   '<b>ingredient</b> —— 配料、成分<br><br>📌 搭配：<code>a special ingredient</code>',
   '短语'],
  ['A heart or ring shape ___ an upcoming wedding while a pig is a sign of plenty of food.',
   '<b>indicates</b> —— 表明、指示<br><br>📌 <code>indicate</code> 比 <code>show</code> 正式，阅读里常见',
   '短语'],
  ['A heart or ring shape indicates an ___ wedding while a pig is a sign of plenty of food.',
   '<b>upcoming</b> —— 即将到来的<br><br>📌 近义：<code>coming</code> · <code>approaching</code>',
   '短语'],
];

const notes = items.map(([front, back, tag]) => ({
  deckName: DECK,
  modelName: '问答题',
  fields: { 正面: front + '<br><br>（出处：' + SRC + '）', 背面: back },
  options: { allowDuplicate: false },
  tags: ['英语', '阅读生词', tag, '2022阅读A'],
}));

(async () => {
  console.log('待建:', notes.length, '张（2022 Passage A 的短语/搭配）');
  const ids = await inv('addNotes', { notes });
  const ok = ids.filter(x => x !== null);
  console.log('写入', ok.length, '张 | 重复跳过', ids.length - ok.length, '张');

  // 回读校验（必须看实际内容，不信「接口没报错」）
  const info = await inv('notesInfo', { notes: ok });
  console.log('\n=== 回读全部 ===');
  for (const n of info) {
    const f = String(n.fields['正面'].value).replace(/<[^>]+>/g, ' ').replace(/\.\.\./g, '…').slice(0, 58);
    const b = String(n.fields['背面'].value).replace(/<[^>]+>/g, ' ').split('——')[0].trim();
    console.log('  ' + f);
    console.log('     → ' + b);
  }

  const all = await inv('findCards', { query: 'deck:"' + DECK + '"' });
  console.log('\n牌组现有:', all.length, '张（原 23 + 新建', ok.length, '）');

  const bad = info.filter(n => /\\[a-z]/.test(String(n.fields['背面'].value)));
  console.log('LaTeX 残留:', bad.length === 0 ? '无 ✅' : '⚠️ ' + bad.length);
})();
