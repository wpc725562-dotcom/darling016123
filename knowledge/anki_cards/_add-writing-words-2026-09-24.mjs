// 建「专升本英语-写作词（输入答案）」小组
// 依据：英语-写作模板优化-2026-09-24.md（5 类应用文：邀请信/求职信/投诉信/劝说信/NOTICE）
// 词源：2022 邀请信范文（学生提供）+ 2017 投诉信 + 2016 求职信 + 2014 劝说信 + NOTICE 模板
// 卡型：问答题（输入答案）—— 正面=中文提示，背面=英文答案，打字作答，机器判对错
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
const MODEL = '问答题（输入答案）';

// [中文提示（正面）, 英文答案（背面）, 标签]
const items = [
  // ── A. 万能句式（整句默写 · 8）──
  ['你好吗？最近怎么样？（书信寒暄）', 'How is everything going?', '万能句式'],
  ['以下是关于此事的一些细节。（过渡句）', 'Here are some relevant details about this matter.', '万能句式'],
  ['首先，……（要点并列 1）', 'First and foremost,', '万能句式'],
  ['此外，……（要点并列 2）', 'Furthermore,', '万能句式'],
  ['最后但同样重要的是，……（要点并列 3）', 'Last but not least,', '万能句式'],
  ['期待你的早日回复。（收尾）', 'I am looking forward to hearing from you soon.', '万能句式'],
  ['综合考虑以上所有因素，我真诚地希望……', 'Taking all these factors into consideration, I sincerely hope', '万能句式'],
  ['您真诚的（书信落款）', 'Yours sincerely,', '万能句式'],

  // ── B. 邀请信（6）──
  ['我写信是为了邀请你……（邀请信来意）', 'I am writing to invite you to', '邀请信'],
  ['邀请（动词）', 'invite', '邀请信'],
  ['邀请（名词）', 'invitation', '邀请信'],
  ['展览', 'exhibition', '邀请信'],
  ['活动', 'activity', '邀请信'],
  ['接受（邀请）', 'accept', '邀请信'],

  // ── C. 投诉信（5）──
  ['我写信是为了投诉……（投诉信来意）', 'I am writing to complain about', '投诉信'],
  ['改进（服务）', 'improve', '投诉信'],
  ['服务', 'service', '投诉信'],
  ['不耐烦的（形容导游）', 'impatient', '投诉信'],
  ['部分退款', 'partial refund', '投诉信'],

  // ── D. 求职信（6）──
  ['我写信是为了申请……职位（求职信来意）', 'I am writing to apply for the position of', '求职信'],
  ['申请（动词短语）', 'apply for', '求职信'],
  ['毕业于……', 'graduate from', '求职信'],
  ['学士学位', "bachelor's degree", '求职信'],
  ['奖项 / 获奖', 'award', '求职信'],
  ['面试', 'interview', '求职信'],

  // ── E. 劝说信（4）──
  ['沉迷于（网络游戏）', 'indulge in', '劝说信'],
  ['浪费时间', 'waste time', '劝说信'],
  ['损害（健康）', 'harm', '劝说信'],
  ['珍惜（学习时光）', 'treasure', '劝说信'],

  // ── F. NOTICE 通知（5）──
  ['丰富（校园生活）', 'enrich', 'NOTICE'],
  ['校园生活', 'campus life', 'NOTICE'],
  ['组织 / 举办（活动）', 'organize', 'NOTICE'],
  ['预定于……（举行）', 'be scheduled to', 'NOTICE'],
  ['参加（活动）', 'participate', 'NOTICE'],

  // ── G. 高分小词（3）──
  ['有意义的', 'meaningful', '高分词'],
  ['难忘的', 'unforgettable', '高分词'],
  ['真诚地（副词）', 'sincerely', '高分词'],
];

const notes = items.map(([cn, en, tag]) => ({
  deckName: DECK,
  modelName: MODEL,
  fields: { 正面: cn, 背面: en },
  options: { allowDuplicate: false },
  tags: ['英语', '写作词', tag],
}));

(async () => {
  await inv('createDeck', { deck: DECK });
  console.log('牌组就绪:', DECK);
  console.log('笔记类型:', MODEL, '（正面=中文提示，背面=英文答案，打字作答）');
  console.log('待建:', notes.length, '张');

  const ids = await inv('addNotes', { notes });
  const ok = ids.filter(x => x !== null);
  console.log('\n写入', ok.length, '张 | 重复跳过', ids.length - ok.length, '张');

  // 回读抽查
  const info = await inv('notesInfo', { notes: ok.slice(0, 4) });
  console.log('\n=== 回读抽查 4 张 ===');
  for (const n of info) {
    console.log('  [' + n.modelName + ']', n.fields['正面'].value, '→', n.fields['背面'].value);
  }

  // 全库统计
  const all = await inv('findCards', { query: 'deck:"' + DECK + '"' });
  console.log('\n牌组现有卡片:', all.length, '张');

  // 检查有没有 LaTeX 残留
  const allInfo = await inv('notesInfo', { notes: ok });
  const bad = allInfo.filter(n => /\\[a-z]/.test(n.fields['背面'].value));
  console.log('LaTeX 残留检查:', bad.length === 0 ? '无 ✅' : '⚠️ ' + bad.length + ' 张有问题');
})();
