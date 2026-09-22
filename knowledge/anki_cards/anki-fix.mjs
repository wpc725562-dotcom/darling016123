const ANKI = 'http://127.0.0.1:8765';
const APPLY = process.argv.includes('--apply');
const TARGET = '暂存-未学';

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

const strip = (s) => s.replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();

const rules = {
  '专升本::C语言': (f) => {
    if (/极限|lim\(|级数|洛必达|收敛|等价无穷小/.test(f)) return '放错牌组（高数内容）';
    if (/求余|逻辑与|逻辑或|逻辑非|double|未初始化|强制类型转换|注释/.test(f)) return '超前进度（尚未学到）';
    return null;
  },
  '专升本::高数': (f) => {
    if (/3x²\+2x/.test(f)) return null;
    return '超前进度（尚未学到）';
  },
  '专升本-高数错题': (f) => {
    if (/测试卡/.test(f)) return '垃圾测试卡';
    if (/sinx\/x|幂函数求导/.test(f)) return '超前进度（尚未学到）';
    return null;
  },
};

const toMove = [];
console.log('===== 整改清单（' + (APPLY ? '执行' : '预演 dry-run') + '）=====\n');
for (const [deck, rule] of Object.entries(rules)) {
  const noteIds = await invoke('findNotes', { query: 'deck:"' + deck + '"' });
  const infos = await invoke('notesInfo', { notes: noteIds });
  const keep = [];
  console.log('【' + deck + '】');
  for (const n of infos) {
    const front = strip(n.fields['正面'].value);
    const why = rule(front);
    if (why) {
      console.log('  → 移出｜' + why + '｜' + front.slice(0, 48));
      toMove.push({ noteId: n.noteId, cardIds: n.cards, front, why, from: deck });
    } else {
      keep.push(front);
    }
  }
  console.log('  保留 ' + keep.length + ' 张：');
  keep.forEach((k) => console.log('     · ' + k.slice(0, 48)));
  console.log('');
}

console.log('合计移出 ' + toMove.length + ' 张 → 牌组「' + TARGET + '」\n');

if (APPLY) {
  await invoke('createDeck', { deck: TARGET });
  const allCards = toMove.flatMap((x) => x.cardIds);
  await invoke('changeDeck', { cards: allCards, deck: TARGET });
  const counts = {};
  for (const d of [...Object.keys(rules), TARGET]) {
    counts[d] = (await invoke('findCards', { query: 'deck:"' + d + '"' })).length;
  }
  console.log('✅ 执行完成，各牌组现有卡数：');
  console.log(JSON.stringify(counts, null, 1));
} else {
  console.log('（预演模式，未做任何改动。加 --apply 才会真正移动）');
}
