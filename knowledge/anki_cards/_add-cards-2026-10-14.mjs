// 10-14 建卡：凌晨复检暴露的新缺口（C语言 7 张 + 高数 1 张）
// 用法：先开 Anki（AnkiConnect 需在线），再
//   node knowledge/anki_cards/_add-cards-2026-10-14.mjs
// 建卡纪律：只有已学过 / 已过关的考点才建（超前卡是负债）
//
// 本批来源：2026-10-14 凌晨三轮复检
//   ① C语言 复检批 5 题（a++ 落地时机 / 求余 / 逗号表达式）
//   ② C语言 1.8 指针复检 6 题（大面积回生）
//   ③ 高数 复检批（链式法则里层导数是常数时漏乘）

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
const DECK_MATH = '专升本-高数错题';

const toNote = (deck, front, back, tags) => ({
  deckName: deck,
  modelName: '问答题',
  fields: { 正面: front, 背面: back },
  options: { allowDuplicate: false },
  tags,
});

const cards = [
  // ── C 语言 · #C013 后缀 ++ 的语义（本轮最核心）──
  toNote(DECK_C,
    '#C013：<code>int a = 5;<br>int b = a++;</code><br>执行完，<code>a</code> 和 <code>b</code> 各是几？为什么？',
    '<b>b = 5　·　a = 6</b><br><br>🔑 <b>口诀：后缀 ++ —— 「先交货，后涨价」。</b><br><br>· <code>b = a++</code> 分两步：<br>　① <b>交货</b>：把 a 当前的旧值 <b>5</b> 交给 b ⇒ <b>b = 5</b><br>　② <b>涨价</b>：交完货，a 自己加 1 ⇒ <b>a = 6</b><br><br>⚠️ 我错了两次（题1 和题4）—— 都<b>只看了「交出去的货」，漏了「涨价后的 a」</b>。<br><br>| 写法 | b 拿到 | a 最后 |<br>| :-- | :-- | :-- |<br>| <code>b = a++</code>（后缀） | 旧值 <b>5</b> | <b>6</b> |<br>| <code>b = ++a</code>（前缀） | 新值 <b>6</b> | <b>6</b> |<br><br><b>不管前缀后缀，a 最后都 +1</b>；差别只在 b 拿到的是旧值还是新值。',
    ['C语言', 'C013', '自增', 'a++', '落地时机']),

  // ── C 语言 · #C014 逗号表达式取末值 + a 已更新 ──
  toNote(DECK_C,
    '#C014：<code>int a = 5;<br>int x = (a++, a + 10);</code><br><code>x</code> 是几？<code>a</code> 是几？',
    '<b>a = 6　·　x = 16</b><br><br>🔑 <b>逗号表达式取「最后一个」的值。</b><br><br>· <code>a++</code> 执行完，a 已经变成 <b>6</b> —— 它吐出的 5 <b>被丢掉，不算数</b><br>· 所以第二个 <code>a + 10</code> 里的 a 是<b>更新后的 6</b>：6 + 10 = <b>16</b><br><br>⚠️ 我答了 x = 5 —— 错在<b>把 a++ 吐出的旧值捡回来用了</b>。<br><br>对照：<code>x = (a++, a * 3)</code>（a 从 1 开始）⇒ a 变 2 ⇒ 2×3 = <b>6</b>。<b>同一个套路</b>：逗号表达式要的是<b>后面的 a</b>，不是 a++ 吐出来的那个。',
    ['C语言', 'C014', '逗号表达式', 'a++']),

  // ── C 语言 · #C015 求余运算 ──
  toNote(DECK_C,
    '#C015：<code>1900 % 400</code> 等于几？',
    '<b>300</b><br><br>🔑 <b>求余 = 被除数 − 商 × 除数</b>（先算商，再减回去）。<br><br>· 商 = 1900 ÷ 400 = <b>4</b>（整数除法，取整）<br>· 1900 − 400 × 4 = 1900 − 1600 = <b>300</b><br><br>⚠️ 我答了 3 —— <b>少算两个 0，凭感觉</b>。<br><br>用途：<b>判断能不能整除</b>。例：<code>year % 4 == 0</code> 读作「year 能被 4 整除」。<br>（顺带：<code>1900 % 400</code> = 300 ≠ 0 ⇒ 1900 <b>不是</b>闰年 —— 这正是 4.4 闰年题的核心判据）',
    ['C语言', 'C015', '求余', '百分号']),

  // ── C 语言 · #C016 *p++ 的顺序 ──
  toNote(DECK_C,
    '#C016：<code>int a[3] = {10, 20, 30};<br>int *p = a;<br>printf("%d ", *p++);<br>printf("%d", *p);</code><br>印出什么？',
    '<b>10 20</b><br><br>🔑 <code>*p++</code> 等价于 <code>*(p++)</code> —— <b>先取 p 旧值指向的内容，然后 p 才后移</b>。<br><br>① <code>*p++</code>：p 指向 a[0] ⇒ 取出 <b>10</b>，印 <code>10</code>；<b>取完之后</b> p 才 +1 挪到 a[1]<br>② 再印 <code>*p</code> ⇒ p 已在 a[1] ⇒ <b>20</b><br><br>⚠️ 我答 <code>20 10</code> —— 把顺序当成了「先移再取」，<b>那是 <code>*++p</code></b>。<br><br>🔑 <b>和后缀 ++ 同一条道理：先交货，后涨价。</b><br>· <code>*p++</code>：先取旧位置的内容，再移<br>· <code>(*p)++</code>：先取内容，再把<b>那个内容</b>加 1<br>· <code>*++p</code>：先把 p 移一格，再取',
    ['C语言', 'C016', '指针', 'p++', '读程']),

  // ── C 语言 · #C017 数组名传参降级 ──
  toNote(DECK_C,
    '#C017：<code>void f(int arr[]) {<br>  printf("%d", sizeof(arr) / sizeof(arr[0]));<br>}<br>int main() { int a[10] = {0}; f(a); }</code><br>32 位下印几？为什么不是 10？',
    '<b>1</b><br><br>🔑 <b>数组名一进函数，就「瘦身」成指针。</b><br><br>· 主函数里的 <code>a</code> 是「整个数组」（10 × 4 = 40 字节）<br>· 传进 <code>f(a)</code> 的<b>不是整个数组，是首地址</b> ⇒ 形参 <code>arr</code> 本质是<b>指针</b><br>· 所以函数里的 <code>sizeof(arr)</code> = <b>指针大小 = 4</b>（32 位），不是 40<br>· <code>4 / 4 = 1</code><br><br>⚠️ 我答「看不懂」—— 这个概念<b>完全没建立</b>。<br><br><b>一句话：<code>sizeof</code> 在函数里量不出数组长度</b>（因为它拿到的是指针，不是数组）。<br>👉 想在函数里知道长度，必须<b>额外传一个长度参数</b>。',
    ['C语言', 'C017', '指针', '数组名降级', 'sizeof']),

  // ── C 语言 · #C018 二维数组 a vs a[0] ──
  toNote(DECK_C,
    '#C018：<code>int a[3][5];</code><br><code>sizeof(a[0])</code> 和 <code>sizeof(a)</code> 各是几？',
    '<b>sizeof(a[0]) = 20　·　sizeof(a) = 60</b>（32 位，int = 4 字节）<br><br>🔑 <b><code>a</code> 管行，<code>a[0]</code> 管元素。</b><br><br>· <code>a[0]</code> = <b>第 0 行</b> = 5 个 int = 5 × 4 = <b>20</b><br>· <code>a</code> = <b>整个二维数组</b> = 3 行 × 5 个 × 4 = <b>60</b><br><br>⚠️ 我答「不知道」—— 这个概念<b>没建立</b>。<br><br><b>楼层比喻：</b>二维数组 = 3 层楼，每层 5 间房。<br>· <code>a</code> = 整栋楼（60）<br>· <code>a[0]</code> = 第 0 层（20）<br>· <code>a[0][0]</code> = 第 0 层第 0 间（4）',
    ['C语言', 'C018', '二维数组', 'sizeof', '读程']),

  // ── C 语言 · #C019 数组名比地址不比内容 ──
  toNote(DECK_C,
    '#C019：<code>char s[] = "Hello";<br>char t[] = "Hello";<br>printf("%d", s == t);</code><br>印几？',
    '<b>0</b>（不相等）<br><br>🔑 <b>数组名 <code>s</code> / <code>t</code> 是「门牌号」，不是「里面的内容」。</b><br><br>· 两个 <code>"Hello"</code> 是<b>两块不同的地</b>（各自分配了独立空间）<br>· <code>s == t</code> 比的是<b>门牌号（地址）</b> ⇒ 两块地不一样 ⇒ <b>0</b><br><br>⚠️ 我答 1 —— 以为比的是内容。<br><br><b>要比内容，用 <code>strcmp(s, t)</code>：</b><br>· 返回 <b>0</b> 表示<b>相同</b>（注意：是 0 = 相同，和 <code>==</code> 的直觉相反）<br>· 返回正数 / 负数表示不同<br><br>📌 这是 2026 真题考点。',
    ['C语言', 'C019', '数组名', 'strcmp', '地址']),

  // ── 高数 · #M004 链式法则：里层导数是常数时别漏 ──
  toNote(DECK_MATH,
    '#M004：<code>y = ln(3x)</code>，求 <code>y′</code>',
    '<b>y′ = 1/x</b><br><br>🔴 我答了 <code>1/(3x)</code> —— <b>漏乘里层导数 3</b>。<br><br><b>剥洋葱三步：</b><br>① <b>外层求导</b>：<code>ln(□)</code> 的导数是 <code>1/□</code> ⇒ <code>1/(3x)</code><br>② 里层原样抄：□ = 3x<br>③ <b>再乘里层导数</b>：<code>(3x)′ = 3</code> ⇒ <code>1/(3x) × 3 = 1/x</code><br><br>⚠️ <b>我的规律性错误（第 4 次）：</b><br>· 里层导数是<b>常数</b>时<b>漏乘</b>（<code>e^(2x)</code> 的 2 · <code>ln(3x)</code> 的 3）<br>· 里层导数是<b>含 x 的式子</b>时<b>记得乘</b>（<code>ln(x²)</code> 的 2x）<br><br><b>🔧 固定动作（不再讲道理）：</b>算完外层导数后，<b>强制回头单独写一行「□′ = ?」</b>。常数也是数，不能跳。<br><br><b>✅ 捷径自查：</b><code>ln(3x) = ln3 + lnx</code> ⇒ 常数 ln3 求导为 0 ⇒ 答案<b>必然是 1/x</b>。我写的 <code>1/(3x)</code> 分母还带 x，形状就不对。<br><br><b>外层导数表：</b><br>· <code>e^□</code> → <code>e^□</code>　·　<code>ln□</code> → <code>1/□</code><br>· <code>sin□</code> → <code>cos□</code>　·　<code>□ⁿ</code> → <code>n□ⁿ⁻¹</code>',
    ['高数', 'M004', '链式法则', '里层导数', 'ln']),
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
      const f = Object.values(n.fields).map(v => v.value.replace(/<[^>]+>/g, '').slice(0, 46));
      console.log('  [' + n.modelName + ']', f[0], '→', f[1]);
    }
  }
  console.log('\n写入', ok.length, '张，重复跳过', ids.length - ok.length, '张');
})();
