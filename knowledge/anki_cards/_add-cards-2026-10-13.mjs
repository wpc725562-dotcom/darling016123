// 10-13 建卡：错题本第 5 件补账（断卡 24 天后的第一次）
// 用法：先开 Anki（AnkiConnect 需在线），再
//   node knowledge/anki_cards/_add-cards-2026-10-13.mjs
// 建卡纪律：只有已学过 / 已过关的考点才建（超前卡是负债）
//
// 本批来源：2026-10-13 错题本 #C010 / #C011 / #C012 / #M003 / #E002
//          + 2 条方法卡（英语「先判词性」· 高数「乘里层导数」）

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
  // ── C 语言 · #C010 关系表达式的值 ──
  toNote(DECK_C,
    '#C010：<code>10 != 9</code> 这个表达式的值是几？<br>（A. 0　B. 1　C. true　D. 非 0）',
    '<b>B（1）</b><br><br><code>10 != 9</code> 问的是「10 是不是不等于 9」—— 答案「<b>是</b>」 ⇒ 真 ⇒ <b>值 1</b>。<br><br>🔑 <b>C 语言里任何关系表达式/逻辑表达式的值只有两个：</b><br>真 → <b>1</b>　·　假 → <b>0</b><br><br>⚠️ <code>!=</code> 读「不等于」。<code>10 != 9</code> 是<b>真</b>（10 确实不等于 9），所以是 <b>1</b>，不是 0。<br><br>记法：<b>「是」= 1，「否」= 0</b>。',
    ['C语言', 'C010', '关系表达式', '真值']),

  // ── C 语言 · #C011 sizeof(指针) ──
  toNote(DECK_C,
    '#C011：<code>char s[] = "hello"; char *p = s;</code><br>求 <code>sizeof(s)</code> / <code>sizeof(p)</code> / <code>strlen(s)</code>（按 32 位口径）',
    '<b>6 / 4 / 5</b><br><br>🔑 <b>关键：<code>sizeof(p)</code> 问的是「指针这张纸条本身多大」，跟它指向什么无关。</b><br><br>· <code>sizeof(s)</code> = <b>6</b> —— 数组占多少装多少，<code>"hello"</code> 5 个字符 + 结尾 <code>\\0</code> 1 个 = 6<br>· <code>sizeof(p)</code> = <b>4</b> —— 指针固定大小（<b>32 位 4 字节 / 64 位 8 字节</b>），指向 <code>char</code> 还是 <code>double</code> 都一样<br>· <code>strlen(s)</code> = <b>5</b> —— 数到 <code>\\0</code> 停，<b>不含</b> <code>\\0</code><br><br>⚠️ 考试按 <b>32 位</b>算 ⇒ <code>sizeof(p)</code> 选 4。本机 64 位会得 8，别被实机结果带偏。',
    ['C语言', 'C011', 'sizeof', '指针', 'strlen']),

  // ── 计算机 · #C012 三错区分 ──
  toNote(DECK_CS,
    '#C012：<br>①「数组越界」属于哪种错误？<br>②「函数只有声明、没有定义」属于哪种错误？',
    '① <b>运行错误</b> —— 编译过了、链接过了，跑起来才炸<br>② <b>链接错误</b> —— 符号找不到（有声明没定义）<br><br>🔑 <b>口诀：语法找编译，符号找链接，越界除零找运行。</b><br><br>| 错 | 看什么 | 例子 |<br>| :-- | :-- | :-- |<br>| 编译错 | <b>语法</b> | 缺分号、变量未声明 |<br>| 链接错 | <b>符号</b> | 只有声明没定义、函数名拼错 |<br>| 运行错 | <b>值</b> | 数组越界、除零、空指针 |',
    ['计算机基础', 'C012', '编译链接运行', '三错']),

  // ── 高数 · #M003 链式法则里层导数 ──
  toNote(DECK_MATH,
    '#M003：<code>y = e^(2x)</code>，求 <code>y′</code> 和 <code>y″</code>',
    '<b>y′ = 2e^(2x)　·　y″ = 4e^(2x)</b><br><br>🔴 我第一次答的是 <code>y′ = e^(2x)</code> —— <b>漏乘了里层导数 2</b>。<br><br><b>剥洋葱三步：</b><br>① <b>外层求导</b>：<code>e^□</code> 求导还是 <code>e^□</code><br>② <b>里层原样抄</b>：□ = 2x<br>③ <b>再乘里层导数</b>：<code>(2x)′ = 2</code> ⇒ <b>2e^(2x)</b><br><br>再求一次（还是同三步）：<code>(2e^(2x))′</code> = 2·(e^(2x))′ = 2·2e^(2x) = <b>4e^(2x)</b><br><br>⚠️ <b><code>e^x</code> 求导还是自己，是因为里层导数恰好是 1</b>（乘了看不出来）。括号里只要不是光秃秃的 x，这个「1」就变了。',
    ['高数', 'M003', '链式法则', '里层导数', '高阶导数']),

  // ── 英语 · #E002 先判词性 ──
  toNote(DECK_EN,
    '#E002：语法填空<br><code>the ___ (introduce) of the new system…</code><br>空格填什么形式？为什么？',
    '<b>introduction</b><br><br>🔑 <b>判据：<code>the</code> 后面接名词。</b><br><br>「the ___ of the new system」—— 这里是「新系统的<b>引入</b>」，需要一个<b>名词</b>。<br><br><b>动词 → 名词的后缀：</b><br>· <code>-tion</code>：introduce → <b>introduction</b> · inform → information<br>· <code>-ment</code>：manage → management · develop → development<br>· <code>-ance</code>：perform → performance<br><br>⚠️ <b>有提示词的第一步永远是「先判词性」</b>（名词 / 动词 / 形容词 / 副词），<b>再变形式</b>。<br>我首测时直接按「动词变三单」填了 <code>introduces</code> —— 错在<b>跳过了判词性</b>。',
    ['英语', 'E002', '词性判断', '词性转换']),

  // ── 英语 · 方法卡（今天最有价值的一条）──
  toNote(DECK_EN,
    '语法填空：<b>有提示词的题目，第一动作是什么？</b>',
    '<b>先判词性</b> —— 定它在这句里该是名词 / 动词 / 形容词 / 副词，<b>再变形式</b>。<br><br>🔴 <b>为什么这条最重要：</b><br>2017 第 2 篇首测 <b>2/10</b>，5 道提示词题<b>全按「动词变三单 / 形容词」直接填</b>；<br>讲了这条之后重做 → <b>9/10</b>。<br><br><b>位置信号表：</b><br>· 冠词 <code>the</code> / 物主代词后 → <b>名词</b><br>· 名词前 → <b>形容词</b><br>· 动词旁 → <b>副词</b><br>· 介词后 → <b>-ing</b>（动名词）<br><br>词性定了，形式就只剩几种可能，<b>不会再凭感觉造词</b>。',
    ['英语', '方法卡', '词性判断', '语法填空']),

  // ── 高数 · 方法卡 ──
  toNote(DECK_MATH,
    '高数：看到一个「套娃」函数（括号里不是光秃秃的 x），求导时要多做什么？',
    '<b>回头乘上「里层导数」</b>（链式法则）。<br><br><b>剥洋葱三步：</b><br>① 外层求导<br>② 里层原样抄<br>③ <b>再乘里层导数</b> ← 最容易丢的一步<br><br><b>常见对照：</b><br>· <code>e^x</code> → <code>e^x</code>（里层导数 1，看不出变化）<br>· <code>e^(2x)</code> → <code>2e^(2x)</code><br>· <code>e^(3x)</code> → <code>3e^(3x)</code><br>· <code>e^(x²)</code> → <code>2x·e^(x²)</code><br>· <code>sin(2x)</code> → <code>2cos(2x)</code><br><br>⚠️ 直观理解：<b>里层跑得多快，外层就跟着快多少倍。</b>',
    ['高数', '方法卡', '链式法则', '里层导数']),
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
