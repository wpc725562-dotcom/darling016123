// 2026-10-21 补卡：feof 两张（2022 真题填空考点 + 时序陷阱）
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

const CARDS = [
  {
    front: '【2022 真题·填空 4 分】feof(fp) 函数用来判断文件是否结束，如果遇到文件结束，则函数值为＿＿',
    back: '<b>非 0</b>（真）',
    tags: ['C语言', '文件', 'feof', '真题'],
  },
  {
    front: '文件刚打开、一个字都没读，feof(fp) 返回什么？',
    back: '<b>0</b><br>feof 只报告「上一次读有没有撞到末尾」。没读过 = 没撞过 = 0。<br>⚠️ 它不是「预测后面还有没有字符」。',
    tags: ['C语言', '文件', 'feof', '易错'],
  },
];

async function main() {
  const allDecks = await invoke('deckNames');
  const hit = allDecks.find((d) => d.includes('C语言') && d.includes('知识'));
  const deckName = hit || '专升本::C语言::知识点';
  const modelName = '问答题';
  const notes = CARDS.map((c) => ({
    deckName,
    modelName,
    fields: { 正面: c.front, 背面: c.back },
    tags: c.tags,
    options: { allowDuplicate: false, duplicateScope: 'deck' },
  }));
  console.log('牌组 =', deckName, '| 待写入', notes.length, '张');
  if (!APPLY) return console.log('预演结束');
  const ids = await invoke('addNotes', { notes });
  console.log('addNotes 返回：成功', ids.filter((x) => x !== null).length, '/', notes.length);
}

main().catch((e) => { console.error('ERROR:', e.message); process.exit(1); });
