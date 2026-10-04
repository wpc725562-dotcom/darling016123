// 审查 2024 完形 15 题的全部选项词（60 个），找出【漏建卡】的
// 判据：① 答案词必建 ② 他说「不知道/不清楚」的必建 ③ 他译错的必建 ④ 他明确说「知道」的不建
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

// 15 题 × 4 选项 = 60 个词，逐个标状态
const audit = [
  ['21', ['guilty', 'confident', 'ashamed', 'proud'], 'guilty', '他说「自信/骄傲」✅ · ashamed 已建'],
  ['22', ['acting', 'traveling', 'filming', 'drawing'], null, '四个都常见，他说「讲的是旅游」'],
  ['23', ['scenery', 'customs', 'history', 'tales'], 'scenery,customs,tales', '🔴 他说「很多不认识，只知道 C 是历史」'],
  ['24', ['allowed', 'forced', 'inspired', 'required'], 'forced', '他说「forced 遭受」❌ 应是「强迫」'],
  ['25', ['city', 'world', 'cultural', 'ecological'], 'ecological', 'ecological 他没提'],
  ['26', ['aimlessly', 'conveniently', 'quickly', 'reasonably'], null, 'aimlessly/reasonably 已建'],
  ['27', ['career', 'concept', 'degree', 'discovery'], null, 'concept/degree/discovery 已建'],
  ['28', ['remote', 'appealing', 'dangerous', 'rewarding'], 'dangerous', '他说「dangerous 危机」❌ 应是「危险的」'],
  ['29', ['make', 'stop', 'leave', 'miss'], null, '四个都常见'],
  ['30', ['taught', 'challenged', 'followed', 'met'], null, '他都说了 ✅'],
  ['31', ['comments', 'negotiations', 'experiences', 'directions'], null, 'comments/negotiations/directions 已建'],
  ['32', ['independent', 'helpful', 'innocent', 'similar'], 'similar,independent,innocent', '🔴 他说「选 B，其他不知道什么意思」——similar 是答案词！'],
  ['33', ['depend on', 'learn from', 'long for', 'begin with'], null, 'long for 已建（答案词）'],
  ['34', ['warning', 'reaction', 'request', 'advice'], 'reaction', '他说「reaction 理由」❌ 应是「反应」'],
  ['35', ['work', 'go', 'observe', 'delay'], null, 'observe 已建；delay 他说「知道」'],
];

// ── 漏建清单 ──
const missing = [
  ['similar', '<b>相似的、类似的</b><br><br>🔴 <b>2024 完形第 32 题的答案</b>：<br><code>people are more <b>similar</b> than we might think</code><br>（人们比我们想的更<b>相似</b>）<br><br>📌 线索在后文：<code>"They are just like us."</code>（他们就跟我们一样）<br><br>⚠️ 别说成 <code>same</code>（same 是「完全相同」，similar 是「相似」）', '答案词'],
  ['scenery', '<b>风景、景色</b>（不可数）<br><br>🔴 <b>2024 完形第 23 题的答案</b>：<br><code>I noticed the amazing <b>scenery</b>, such as the rivers and the mountains</code><br>（我注意到令人惊叹的<b>风景</b>，比如河流和山脉）<br><br>📌 <code>scene</code>（场景）→ <code>scenery</code>（风景，总称）<br>⚠️ 不可数，不能说 <code>a scenery</code>', '答案词'],
  ['customs', '<b>风俗、习俗</b>（复数形式）<br><br>📌 <code>custom</code>（习俗）→ 常用复数 <code>customs</code><br>⚠️ 大写 <code>Customs</code> 是「海关」<br><br>📌 对照：<code>the customs and traditions of the locals</code>（当地人的风俗和传统 —— 2022 阅读 Passage A 首句）', '生词'],
  ['tales', '<b>故事、传说</b><br><br>📌 <code>tale</code> = 故事（比 <code>story</code> 更有「传说」感）<br><br>📌 搭配：<code>fairy tales</code> = 童话<br><code>tell tales</code> = 说闲话', '生词'],
  ['guilty', '<b>内疚的、有罪的</b><br><br>📌 <code>feel guilty about sth</code> = 为某事感到内疚<br><br>⚠️ 与 <code>ashamed</code>（羞耻的）辨析：<br><code>guilty</code> = 做了错事的内疚<br><code>ashamed</code> = 因自己或他人而羞耻', '生词'],
  ['forced', '<b>强迫、被迫</b><br><br>🔴 <b>你译成</b>「遭受」<br>⇒ <b>「遭受」是 <code>suffer</code></b>，<code>forced</code> 是「被强迫」<br><br>📌 <code>be forced to do sth</code> = 被迫做某事<br>📌 原形 <code>force</code> = 力量 / 强迫', '纠错'],
  ['ecological', '<b>生态的、生态学的</b><br><br>📌 <code>ecology</code>（生态学）→ <code>ecological</code>（形容词）<br><br>📌 <code>ecological balance</code> = 生态平衡<br>⚠️ 与 <code>cultural</code>（文化的）区分：一个讲自然，一个讲人文', '生词'],
  ['dangerous', '<b>危险的</b><br><br>🔴 <b>你译成</b>「危机」<br>⇒ <b>「危机」是名词 <code>crisis</code></b>；<code>danger</code> 才是「危险」（名词）<br>⇒ <code>dangerous</code> = danger + ous = <b>危险的（形容词）</b><br><br>📌 本文：<code>some places were considered dangerous</code>', '纠错'],
  ['independent', '<b>独立的</b><br><br>📌 <code>in</code>（不）+ <code>dependent</code>（依赖的）= 不依赖的<br><br>📌 <code>independent</code>（形容词）· <code>independence</code>（名词：独立）<br>⚠️ 不是「依赖的」（那是 <code>dependent</code>）', '生词'],
  ['innocent', '<b>无辜的、天真的</b><br><br>📌 <code>in</code>（不）+ <code>nocent</code>（伤害）= 不伤害人的 → 无辜的<br><br>📌 <code>an innocent child</code> = 天真的孩子<br><code>innocent of the crime</code> = 无罪', '生词'],
  ['reaction', '<b>反应</b><br><br>🔴 <b>你译成</b>「理由」<br>⇒ <b>「理由」是 <code>reason</code></b>，两个词拼写不同<br><br>📌 <code>react</code>（反应）→ <code>reaction</code>（名词）<br>📌 <code>one\'s reaction to sth</code> = 对某事的反应', '纠错'],
];

(async () => {
  console.log('=== 审查：2024 完形 15 题 × 4 选项 = 60 个词 ===\n');
  let totalMissing = 0;
  for (const [q, opts, miss, note] of audit) {
    const flag = miss ? '🔴 漏建' : '✅ 已覆盖';
    console.log(`  ${q}. ${opts.join(' / ')}`);
    console.log(`     ${flag} ${miss ? '→ ' + miss : ''} | ${note}`);
    if (miss) totalMissing += miss.split(',').length;
  }
  console.log(`\n  ⇒ 审查结论：漏建 ${totalMissing} 个，清单如下`);

  await inv('createDeck', { deck: DECK });

  // 探测跨牌组重复
  const existing = new Set();
  for (const [front] of missing) {
    const found = await inv('findNotes', { query: '"' + front.replace(/"/g, '') + '"' });
    if (found.length) { existing.add(front); console.log('  ⚠️ 已存在:', front); }
  }

  const notes = missing.map(([front, back, tag]) => ({
    deckName: DECK,
    modelName: '问答题',
    fields: {
      正面: existing.has(front) ? front + '（完形纠错）' : front,
      背面: back + '<br><br>（出处：' + SRC + '）',
    },
    options: { allowDuplicate: false },
    tags: ['英语', '完形词汇', tag, '2024完形'],
  }));

  const ids = await inv('addNotes', { notes });
  const ok = ids.filter(x => x !== null);
  console.log('\n✅ 补建', ok.length, '张 | 跳过', ids.length - ok.length, '张');

  const info = await inv('notesInfo', { notes: ok });
  console.log('\n=== 回读全部 ===');
  for (const n of info) {
    const f = String(n.fields['正面'].value).slice(0, 22);
    const b = String(n.fields['背面'].value).replace(/<[^>]+>/g, ' ').split('（出处')[0].trim().slice(0, 38);
    console.log('  ' + f.padEnd(22) + ' → ' + b);
  }

  const all = await inv('findCards', { query: 'deck:"' + DECK + '"' });
  console.log('\n「完形填空词汇」牌组现有:', all.length, '张（14 + 补建', ok.length, '）');
  const bad = info.filter(n => /\\[a-z]/.test(String(n.fields['背面'].value)));
  console.log('LaTeX 残留:', bad.length === 0 ? '无 ✅' : '⚠️ ' + bad.length);
})();
