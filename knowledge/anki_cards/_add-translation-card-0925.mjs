// 按学生的自我诊断补卡：第 4 题不是「同义替换没认出来」，是「make a reservation 没译出中文」
// ⇒ 已有的那张是【填空型】（考「记不记得搭配」），缺的是【翻译型】（考「看到词组能不能出中文」）
// 动作：① 把已有那张卡的背面重排（中文提到最前）② 补一张英→中的直译卡 ③ 补一张中→英的写作卡
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
const DECK2 = '专升本英语-写作词（输入答案）';
const SRC = '2024 广东专升本 阅读 Passage A';

(async () => {
  // ── ① 找出已有的那张「make a reservation」填空卡，重排背面 ──
  const ids = await inv('findCards', { query: 'deck:"' + DECK + '" tag:2024阅读A' });
  const info = await inv('notesInfo', { notes: (await inv('cardsInfo', { cards: ids })).map(c => c.note) });
  const target = info.find(n => String(n.fields['背面'].value).includes('make a reservation'));

  if (target) {
    await inv('updateNoteFields', {
      note: {
        id: target.noteId,
        fields: {
          背面: '<b>预订</b>（订房间 / 订位 / 订票都可以用）<br><br>'
              + '<b>make a reservation</b><br>'
              + '<code>make</code> 是「做」，<code>reservation</code> 是「预订（名词）」<br><br>'
              + '🔴 <b>同义替换（阅读题最爱考）</b>：<br>'
              + '<code>make a reservation</code> = <code>book</code> = <code>book in advance</code><br>'
              + '⇒ 原文说「要预订」，选项说「提前订票」，<b>是同一件事</b>',
        },
      },
    });
    console.log('✅ 已重排已有卡片背面（中文「预订」提到最前）| noteId', target.noteId);
  } else {
    console.log('⚠️ 没找到已有的那张卡');
  }

  // ── ② 英→中 直译卡（针对「翻译出了问题」）──
  const note2 = {
    deckName: DECK,
    modelName: '问答题',
    fields: {
      正面: 'make a reservation',
      背面: '<b>预订</b>（订房间 / 订位 / 订票）<br><br>'
          + '📌 <code>reservation</code> = 预订（名词）<br>'
          + '<code>reserve</code> = 预订（动词）<br><br>'
          + '⚠️ <b>2024 阅读第 4 题就是因为这个词组丢的分</b> ——<br>'
          + '原文 <code>you need to make a reservation before heading out there</code><br>'
          + '（你需要<b>预订</b>之后才能去）<br>'
          + '选项 <code>Book in advance</code>（提前订）—— <b>就是它</b>',
    },
    options: { allowDuplicate: false },
    tags: ['英语', '阅读生词', '翻译卡', '2024阅读A'],
  };

  // ── ③ 中→英 写作卡（写作用得到）──
  const note3 = {
    deckName: DECK2,
    modelName: '问答题（输入答案）',
    fields: {
      正面: '预订（订房间 / 订位 / 订票）',
      背面: 'make a reservation',
    },
    options: { allowDuplicate: false },
    tags: ['英语', '写作词', '2024阅读A'],
  };

  const added = await inv('addNotes', { notes: [note2, note3] });
  console.log('✅ 新增 2 张 |', added.filter(x => x !== null).length, '成功');

  // ── 回读 ──
  const back = await inv('notesInfo', { notes: added.filter(x => x !== null) });
  console.log('\n=== 回读新增 ===');
  for (const n of back) {
    console.log('  正面:', String(n.fields['正面'].value).replace(/<[^>]+>/g, ' ').slice(0, 50));
    console.log('  背面:', String(n.fields['背面'].value).replace(/<[^>]+>/g, ' ').slice(0, 90));
    console.log();
  }

  for (const d of [DECK, DECK2]) {
    const all = await inv('findCards', { query: 'deck:"' + d + '"' });
    console.log(d, '→', all.length, '张');
  }
  const bad = [...(target ? [target] : []), ...back].filter(n => /\\[a-z]/.test(String(n.fields['背面'].value)));
  console.log('LaTeX 残留:', bad.length === 0 ? '无 ✅' : '⚠️ ' + bad.length);
})();
