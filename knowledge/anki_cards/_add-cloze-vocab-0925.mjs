// 新建「专升本英语-完形填空词汇」牌组（学生 2026-09-25 明确要求）
// ⚠️ 坑：Anki 的 duplicate 检查是【跨牌组的】—— 同一个 note type 的第一个字段重复就拒收，
//        即使牌组不同。所以必须先探测哪些已存在，再决定怎么建。
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

const DECK = '专升本英语-完形填空词汇';
const SRC = '2024 完形填空';

const items = [
  ['ashamed', '<b>羞耻的、羞愧的</b><br><br>🔴 <b>你以为</b>：「害羞」<br>⇒ <b>害羞是 <code>shy</code></b>，两个词不一样<br><br>📌 <code>be ashamed of</code> = 为……感到羞愧', '纠错'],
  ['remote', '<b>遥远的、偏僻的</b><br><br>🔴 <b>你以为</b>：「促进」<br>⇒ <b>促进是 <code>promote</code></b><br><br>📌 <code>a remote area</code> = 偏远地区', '纠错'],
  ['appealing', '<b>吸引人的</b><br><br>🔴 <b>你以为</b>：「出现」<br>⇒ <b>出现是 <code>appear</code></b>（动词），<code>appealing</code> 是形容词<br><br>📌 <code>an appealing place</code> = 吸引人的地方', '纠错'],
  ['comments', '<b>评论</b>（名词复数）<br><br>🔴 <b>你以为</b>：「相同」<br>⇒ <b>相同是 <code>common</code></b>，拼写只差一点<br><br>📌 <code>leave a comment</code> = 留个评论', '纠错'],
  ['directions', '<b>方向、指示、说明</b><br><br>🔴 <b>你以为</b>：「美味的」<br>⇒ <b>美味的是 <code>delicious</code></b>，两个词完全无关<br><br>📌 <code>ask for directions</code> = 问路', '纠错'],
  ['observe', '<b>观察</b><br><br>🔴 <b>你以为</b>：「探索」<br>⇒ <b>探索是 <code>explore</code></b><br><br>📌 辨析：<code>observe</code> = 用眼睛看 · <code>explore</code> = 主动去闯', '纠错'],
  ['degree', '<b>程度 / 度（温度）/ 学位</b><br><br>🔴 <b>你以为</b>：「深度」<br>⇒ <b>深度是 <code>depth</code></b><br><br>📌 <code>a university degree</code> = 学位<br><code>to some degree</code> = 在某种程度上', '纠错'],
  ['aimlessly', '<b>漫无目的地</b><br><br>📌 <code>aim</code>（目标）+ <code>-less</code>（没有）+ <code>-ly</code>（副词）<br><br>📌 本文对照：<code>To travel more conveniently</code>（不是漫无目的，是「方便地」）', '生词'],
  ['reasonably', '<b>合理地</b><br><br>📌 <code>reason</code>（理由）→ <code>reasonable</code>（合理的）→ <code>reasonably</code>（副词）<br><b>你猜「reason 是理由」是对的</b> ✅<br><br>📌 <code>reasonably priced</code> = 价格合理', '生词'],
  ['concept', '<b>概念</b><br><br>📌 <code>conceive</code>（构想）→ <code>concept</code>（概念）<br><br>📌 <code>the concept of time</code> = 时间的概念', '生词'],
  ['discovery', '<b>发现</b><br><br>📌 <code>discover</code>（发现）→ <code>discovery</code>（名词）<br><br>📌 <code>a great discovery</code> = 伟大的发现', '生词'],
  ['rewarding', '<b>有回报的、值得的</b><br><br>📌 <code>reward</code>（回报）→ <code>rewarding</code>（形容词）<br><br>📌 <code>a rewarding experience</code> = 有收获的经历<br>⚠️ 不是「被奖励的」（那是 <code>rewarded</code>）', '生词'],
  ['negotiations', '<b>谈判</b>（名词复数）<br><br>📌 <code>negotiate</code>（谈判）→ <code>negotiation</code>（名词）<br><br>📌 <code>peace negotiations</code> = 和平谈判', '生词'],
  ['long for', '<b>渴望、盼望</b><br><br>🔴 <b>2024 完形第 33 题的答案</b>：<br><code>They <b>long for</b> better jobs and better opportunities.</code><br>（他们<b>渴望</b>更好的工作和机会）<br><br>⚠️ 不是 <code>depend on</code>（依赖）—— 「依赖工作」说不通<br><br>📌 近义：<code>yearn for</code> · <code>desire</code>', '答案词'],
];

(async () => {
  await inv('createDeck', { deck: DECK });

  // ── 先探测：哪些正面已存在于其他牌组 ──
  const existing = new Set();
  for (const [front] of items) {
    const found = await inv('findNotes', { query: '"' + front.replace(/"/g, '') + '"' });
    if (found.length) {
      const info = await inv('notesInfo', { notes: found.slice(0, 1) });
      const decks = await inv('cardsInfo', { cards: await inv('findCards', { query: 'nid:' + found[0] }) });
      const deck = decks.length ? (await inv('deckNamesAndIds')) : {};
      const deckName = decks.length ? Object.entries(deck).find(([, id]) => id === decks[0].deckId)?.[0] : '?';
      existing.add(front);
      console.log('  ⚠️ 已存在:', front.padEnd(16), '→ 在牌组「' + deckName + '」');
    }
  }
  console.log('\n已存在', existing.size, '个 | 待新建', items.length - existing.size, '个\n');

  // ── 建卡：已存在的加后缀「（完形纠错）」避免 duplicate 拒收 ──
  const notes = items.map(([front, back, tag]) => ({
    deckName: DECK,
    modelName: '问答题',
    fields: {
      正面: (existing.has(front) ? front + '（完形纠错）' : front),
      背面: back + '<br><br>（出处：' + SRC + '）',
    },
    options: { allowDuplicate: false },
    tags: ['英语', '完形词汇', tag, '2024完形'],
  }));

  const ids = await inv('addNotes', { notes });
  const ok = ids.filter(x => x !== null);
  console.log('✅ 写入', ok.length, '张 | 跳过', ids.length - ok.length, '张');

  const info = await inv('notesInfo', { notes: ok });
  console.log('\n=== 回读全部 ===');
  for (const n of info) {
    const f = String(n.fields['正面'].value).slice(0, 26);
    const b = String(n.fields['背面'].value).replace(/<[^>]+>/g, ' ').split('（出处')[0].trim().slice(0, 40);
    console.log('  ' + f.padEnd(24) + ' → ' + b);
  }

  const all = await inv('findCards', { query: 'deck:"' + DECK + '"' });
  console.log('\n「完形填空词汇」牌组现有:', all.length, '张');
  const bad = info.filter(n => /\\[a-z]/.test(String(n.fields['背面'].value)));
  console.log('LaTeX 残留:', bad.length === 0 ? '无 ✅' : '⚠️ ' + bad.length);
})();
