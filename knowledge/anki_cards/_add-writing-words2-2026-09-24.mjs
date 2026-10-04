// 补建写作词：2026「建议/回复邮件」+ 2025「NOTICE 改期」
// 依据：英语-写作模板优化-2026-09-24.md §3.5 / §4.1
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

const DECK = '专升本英语-写作词（输入答案）';

const items = [
  // ── 2026 建议 / 回复邮件（6）──
  ['感谢你的来信询问……（回复邮件开头，必写）', 'Thanks for your email asking about', '建议邮件'],
  ['我写信是为了给你一些建议。', 'I am writing to give you some suggestions.', '建议邮件'],
  ['推荐（动词）', 'recommend', '建议邮件'],
  ['景区 / 景点', 'scenic spot', '建议邮件'],
  ['交通方式', 'means of transport', '建议邮件'],
  ['欢迎（名词）', 'welcome', '建议邮件'],

  // ── 2025 NOTICE 改期（5）──
  ['很抱歉通知你……（改期通知致歉句）', 'We are sorry to inform you that', 'NOTICE改期'],
  ['推迟 / 延期（动词短语）', 'put off', 'NOTICE改期'],
  ['改为 / 代替（副词）', 'instead', 'NOTICE改期'],
  ['原因（名词）', 'reason', 'NOTICE改期'],
  ['提前通知（动词短语）', 'inform sb. in advance', 'NOTICE改期'],
];

const notes = items.map(([cn, en, tag]) => ({
  deckName: DECK,
  modelName: '问答题（输入答案）',
  fields: { 正面: cn, 背面: en },
  options: { allowDuplicate: false },
  tags: ['英语', '写作词', tag],
}));

(async () => {
  await inv('createDeck', { deck: DECK });
  console.log('待建:', notes.length, '张（2026 建议邮件 6 + 2025 改期通知 5）');

  const ids = await inv('addNotes', { notes });
  const ok = ids.filter(x => x !== null);
  console.log('写入', ok.length, '张 | 重复跳过', ids.length - ok.length, '张');

  const info = await inv('notesInfo', { notes: ok });
  console.log('\n=== 回读全部 ===');
  for (const n of info) {
    console.log('  ' + n.fields['正面'].value + '  →  ' + n.fields['背面'].value);
  }

  const all = await inv('findCards', { query: 'deck:"' + DECK + '"' });
  console.log('\n写作词牌组现有:', all.length, '张');

  const bad = info.filter(n => /\\[a-z]/.test(n.fields['背面'].value));
  console.log('LaTeX 残留:', bad.length === 0 ? '无 ✅' : '⚠️ ' + bad.length);
})();
