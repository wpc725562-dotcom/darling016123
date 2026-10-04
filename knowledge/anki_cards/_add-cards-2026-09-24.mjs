// 09-24 建卡：E56 / E58 / 进制转换 / 有理化 / 英语词形
// 用法：先开 Anki（AnkiConnect 需在线），再
//   node knowledge/anki_cards/_add-cards-2026-09-24.mjs
// 建卡纪律：只有已学过 / 已过关的考点才建（超前卡是负债）

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

const DECK_C = '专升本-C语言错题';
const DECK_EN = '专升本英语-语法';
const DECK_CS = '专升本-计算机基础';
const DECK_MATH = '专升本-高数错题';

const toNote = (deck, front, back, tags) => ({
  deckName: deck,
  modelName: '问答题',
  fields: { 正面: front, 背面: back },
  options: { allowDuplicate: false },
  tags,
});

const cards = [
  // ── C 语言 · E56 ──
  toNote(DECK_C,
    'E56：<br><code>for (j = 1; j &lt;= 6; j++) printf("*");</code><br>循环结束后 <code>j</code> 是几？为什么？',
    '<b>7</b><br><br><code>j++</code> 跟在<b>循环体后面</b> —— 顺序是：<br>初始化 → 判断 → 体 → <code>j++</code> → 判断 → 体 → <code>j++</code> → … → 判断(假) → 退出<br><br>判断失败时<b>没有体，就没有 <code>j++</code></b>。<br>所以 <code>j</code> 停在 <b>N+1</b>（这里 N=6 → 7）。',
    ['C语言', 'E56', 'for', '循环变量终值']),

  // ── C 语言 · E58 ──
  toNote(DECK_C,
    'E58：<br><code>for (i = 1; i &lt;= 4; i++) { for (j = 1; j &lt;= 5 - i; j++) printf("*"); printf("\\n"); }</code><br>每一行各印几个 <code>*</code>？',
    '<b>4、3、2、1</b>（共 10 个）<br><br>把 <code>i</code> 一行一行代进去：<br>i=1 → 5−1=4 → 4 个<br>i=2 → 5−2=3 → 3 个<br>i=3 → 5−3=2 → 2 个<br>i=4 → 5−4=1 → 1 个<br><br>⚠️ <b>内层上限含外层变量时，必须逐行代入</b> —— 只代一行 = 取样偏差。',
    ['C语言', 'E58', '嵌套循环', '逐行代入']),

  // ── 计算机基础 · 进制转换（两条）──
  toNote(DECK_CS,
    '「几进制就乘几的次方」—— 为什么底数是「几进制」的那个「几」？',
    '因为<b>「逢几进一」</b>。<br><br>满「几」就往前进一位 ⇒ 上一位等于下一位的「几」倍。<br><br>十进制逢十进一 → 10⁰、10¹、10²<br>二进制逢二进一 → 2⁰、2¹、2²<br>八进制逢八进一 → 8⁰、8¹、8²<br>十六进制逢十六进一 → 16⁰、16¹、16²<br><br><b>名字里的那个数，就是要乘的底数。</b>',
    ['计算机基础', '进制转换', '基数']),

  toNote(DECK_CS,
    '十进制 ↔ 某进制：什么时候<b>除</b>，什么时候<b>乘</b>？跟「16 比 10 大」有关系吗？',
    '<b>拆用除、合用乘 —— 跟基数大小无关。</b><br><br>把<b>一个大数</b> → <b>拆成几位</b> → <b>除</b>（45 → 2D，除 16 取余、余数倒着读）<br>把<b>几位</b> → <b>合回一个大数</b> → <b>乘</b>（2D → 45，2×16¹ + 13×16⁰）<br><br>「除 16」不是「除以一个大数」，是<b>按 16 个一组分堆</b>。<br><br>自检：余数只能是 0~1（二）/ 0~7（八）/ 0~15（十六，10~15 写成 A~F）。',
    ['计算机基础', '进制转换', '方向']),

  // ── 高数 · 有理化 ──
  toNote(DECK_MATH,
    '高数：$\frac{0}{0}$ 型里<b>分子带根号</b>怎么办？<br>求 $\lim_{x\to0}\frac{\sqrt{x+4}-2}{x}$',
    '<b>上下同乘「共轭式」</b>（把中间的减号改成加号），再用<b>平方差</b>消掉根号。<br><br>共轭式 = $\sqrt{x+4}+2$<br><br>$\frac{(\sqrt{x+4}-2)(\sqrt{x+4}+2)}{x(\sqrt{x+4}+2)}=\frac{(x+4)-4}{x(\sqrt{x+4}+2)}=\frac{x}{x(\sqrt{x+4}+2)}$<br><br>约掉 $x$ → $\frac{1}{\sqrt{x+4}+2}$ → 代 0 → $\frac{1}{2+2}=$ <b>$\frac14$</b><br><br>⚠️ 约 $x$ 的理由：$x\to0$ 但 $x\neq0$。',
    ['高数', '有理化', '0/0型', '共轭式']),

  // ── 英语 · 词形转换 ──
  toNote(DECK_EN,
    '词形转换：<code>able</code> / <code>nature</code> / <code>kind</code> 分别在需要<b>名词</b>或<b>形容词</b>时写成什么？',
    'able → <b>ability</b>（-le → -ility）<br>nature → <b>natural</b>（名词 + -al = 形容词）<br>kind → <b>kindness</b>（形容词 + -ness = 名词）<br><br><b>先判词性，再变形</b> —— 位置信号：<br>名词前 → 形容词 · 冠词/物主代词后 → 名词 · 动词旁 → 副词 · 介词后 → -ing',
    ['英语', '词形转换']),
];

(async () => {
  const decks = [...new Set(cards.map(c => c.deckName))];
  for (const d of decks) {
    await invoke('createDeck', { deck: d });
    console.log('牌组就绪:', d);
  }

  const notes = cards.map(c => ({ ...c, fields: { ...c.fields, 背面: c.fields.背面.replace(/\\n/g, '<br>') } }));
  const ids = await invoke('addNotes', { notes });
  console.log('\naddNotes 返回:', ids.map(x => x === null ? 'null(重复)' : x).join(', '));

  const ok = ids.filter(x => x !== null);
  if (ok.length) {
    const info = await invoke('notesInfo', { notes: ok });
    console.log('\n=== 回读校验 ===');
    for (const n of info) {
      const f = Object.values(n.fields).map(v => v.value.replace(/<[^>]+>/g, '').slice(0, 48));
      console.log('  [', n.modelName, ']', f[0], '→', f[1]);
    }
  }
  console.log('\n写入', ok.length, '张，重复跳过', ids.length - ok.length, '张');
})();
