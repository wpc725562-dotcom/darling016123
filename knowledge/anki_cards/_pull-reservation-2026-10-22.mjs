// 2026-10-22 凌晨：把「忘了的」reservation 三张卡拉回今天 + 补一张同义替换卡
const ANKI = 'http://127.0.0.1:8765';
const APPLY = process.argv.includes('--apply');

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

async function main() {
  // 1) 找出所有含 reservation 的卡，只处理「语境词」牌组里的那三张句子卡
  const cards = await invoke('findCards', { query: 'reservation' });
  const info = await invoke('cardsInfo', { cards });
  const targets = info
    .filter((c) => c.deckName.includes('语境词'))
    .map((c) => c.cardId);

  console.log('语境词牌组里含 reservation 的卡 =', targets.length, '张');
  info
    .filter((c) => c.deckName.includes('语境词'))
    .forEach((c) => {
      const front = Object.values(c.fields)[0].value.replace(/<[^>]+>/g, '').slice(0, 50);
      console.log('   ·', front);
    });

  // 2) 补一张「同义替换」卡 —— 原卡里只有 make a reservation，没有 book in advance
  const newNotes = [
    {
      deckName: '专升本::英语::语境词',
      modelName: '问答题',
      fields: {
        正面: 'make a reservation = ______（同义替换）<br><br>2024 阅读第 4 题就考这个：原文说 make a reservation，正确选项写的是另一个说法。',
        背面: '<b>book in advance</b><br><br>⚠️ <b>选项里照抄原文词的往往是陷阱</b>：<br>原文有 butterflies → 选项 A. Study butterflies（错）<br>原文有 classes → 选项 D. Sign up for classes（错）<br>正确答案 C 一个原词都没有。',
      },
      tags: ['英语', '同义替换', '阅读', '真题'],
      options: { allowDuplicate: false, duplicateScope: 'deck' },
    },
    {
      deckName: '专升本::英语::语境词',
      modelName: '问答题',
      fields: {
        正面: 'take walk-ins 是什么意思？',
        背面: '接待「<b>没预约直接走进来的客人</b>」<br>walk-in = 没预约直接上门的人<br>所以 The farm doesn\'t take walk-ins ⇒ <b>必须提前预订</b>。',
      },
      tags: ['英语', '短语', '阅读'],
      options: { allowDuplicate: false, duplicateScope: 'deck' },
    },
  ];

  console.log('\n待补新卡 =', newNotes.length, '张');
  newNotes.forEach((n, i) => console.log(`   ${i + 1}. ${n.fields.正面.replace(/<[^>]+>/g, '').slice(0, 50)}`));

  if (!APPLY) {
    console.log('\n预演结束。加 --apply 执行。');
    return;
  }

  if (targets.length) {
    await invoke('setDueDate', { cards: targets, days: '0' });
    console.log('\n✅ 已把这', targets.length, '张卡的到期日改成今天');
  }
  const ids = await invoke('addNotes', { notes: newNotes });
  console.log('✅ addNotes：成功', ids.filter((x) => x !== null).length, '/', newNotes.length);
}

main().catch((e) => { console.error('ERROR:', e.message); process.exit(1); });
