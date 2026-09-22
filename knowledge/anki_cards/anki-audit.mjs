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

const decks = [
  '专升本::C语言',
  '专升本::高数',
  '专升本-C语言错题',
  '专升本-高数错题',
];

const strip = (s) => s.replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();

for (const d of decks) {
  const noteIds = await invoke('findNotes', { query: 'deck:"' + d + '"' });
  const infos = await invoke('notesInfo', { notes: noteIds });
  const cardIds = await invoke('findCards', { query: 'deck:"' + d + '"' });
  const cards = await invoke('cardsInfo', { cards: cardIds });
  const stat = { new: 0, learn: 0, review: 0, suspended: 0 };
  for (const c of cards) {
    if (c.queue === -1) stat.suspended++;
    else if (c.queue === 0) stat.new++;
    else if (c.queue === 1 || c.queue === 3) stat.learn++;
    else stat.review++;
  }
  console.log('\n===== ' + d + ' —— 笔记 ' + infos.length + ' 条 / 卡片 ' + cards.length + ' 张 =====');
  console.log('状态: 新 ' + stat.new + ' | 学习中 ' + stat.learn + ' | 待复习 ' + stat.review + ' | 暂停 ' + stat.suspended);
  console.log('标签集合: ' + [...new Set(infos.flatMap((n) => n.tags))].join(', '));
  infos.forEach((n, i) => {
    console.log('  ' + (i + 1) + '. [' + n.id + '] ' + strip(n.fields['正面'].value).slice(0, 70));
  });
}
