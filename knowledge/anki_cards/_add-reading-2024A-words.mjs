// 补建 2024 Passage A 的生词/短语卡（学生点名要 pet-friendly 和 camping）
// 另含第 4 题的断点词「make a reservation = book in advance」（同义替换缺口）
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
const SRC = '2024 广东专升本 阅读 Passage A';

const items = [
  ['And it is ___-___. Your four-legged friends can have a good time there.',
   '<b>pet-friendly</b> —— 宠物友好的（允许带宠物的）<br><br>📌 <code>名词 + friendly</code> 构词法：<br>user-friendly（用户友好的）· eco-friendly（环保的）',
   '生词'],
  ['And it is pet-friendly. Your ___-___ friends can have a good time there.',
   '<b>four-legged friends</b> —— 「四条腿的朋友」= <b>宠物的委婉说法</b><br><br>⚠️ <b>不是「爬行朋友」</b>！<br><code>four-legged</code> = four（四）+ legged（有腿的）= <b>四条腿的</b><br>（爬行 = <code>crawl</code> / <code>reptile</code>，完全不同的词）',
   '生词'],
  ['The village also offers walking tours, workshops, two-day ___ experiences, and barbecue areas.',
   '<b>camping</b> —— 露营（camp 的动名词）<br><br>📌 搭配：<code>go camping</code> · <code>a camping trip</code> · <code>two-day camping experiences</code>（两天一夜的露营体验）',
   '生词'],
  ['The farm doesn\'t take ___-___, so you need to make a reservation before heading out there.',
   '<b>take walk-ins</b> —— 接待「临时上门的客人」（不需要预约的散客）<br><br>📌 <code>walk-in</code> = 没预约直接走进来的人<br>⚠️ 原句是 <code>doesn\'t take walk-ins</code> = <b>不接待没预约的客人</b>',
   '生词'],
  ['The farm doesn\'t take walk-ins, so you need to ___ ___ ___ before heading out there.',
   '<b>make a reservation</b> —— 预订<br><br>🔴 <b>同义替换（阅读题最爱考）</b>：<br><code>make a reservation</code> = <code>book</code> = <code>book in advance</code>（提前预订）<br>⇒ 原文说「要预订」，选项说的是「提前订票」，<b>是同一件事</b>',
   '同义替换'],
  ['Admission: $12 per person　　（门票）',
   '<b>admission</b> —— 入场费、门票<br><br>📌 <code>admission: $12 per person</code> = 每人 12 美元<br>⚠️ 不是「承认」（那是另一个义项）',
   '生词'],
  ['Sunrise Village is home to one of the largest rice production areas in the city.',
   '<b>be home to</b> —— 是……的所在地 / 栖息着<br><br>📌 <code>The farm is home to 80% of the city\'s butterfly species.</code>',
   '生词'],
];

const notes = items.map(([front, back, tag]) => ({
  deckName: DECK,
  modelName: '问答题',
  fields: { 正面: front + '<br><br>（出处：' + SRC + '）', 背面: back },
  options: { allowDuplicate: false },
  tags: ['英语', '阅读生词', tag, '2024阅读A'],
}));

(async () => {
  console.log('待建:', notes.length, '张');
  const ids = await inv('addNotes', { notes });
  const ok = ids.filter(x => x !== null);
  console.log('写入', ok.length, '张 | 重复跳过', ids.length - ok.length, '张');

  const info = await inv('notesInfo', { notes: ok });
  console.log('\n=== 回读全部 ===');
  for (const n of info) {
    const f = String(n.fields['正面'].value).replace(/<[^>]+>/g, ' ').slice(0, 56);
    const b = String(n.fields['背面'].value).replace(/<[^>]+>/g, ' ').split('——')[0].trim().slice(0, 30);
    console.log('  ' + f);
    console.log('     → ' + b);
  }

  const all = await inv('findCards', { query: 'deck:"' + DECK + '"' });
  console.log('\n牌组现有:', all.length, '张');
  const bad = info.filter(n => /\\[a-z]/.test(String(n.fields['背面'].value)));
  console.log('LaTeX 残留:', bad.length === 0 ? '无 ✅' : '⚠️ ' + bad.length);
})();
