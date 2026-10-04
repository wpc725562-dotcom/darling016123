// 2026-09-26 建卡（收工第 5 件：建卡审查）
// C语言 8 张 → 「专升本-C语言错题」· 高数 2 张 → 「专升本-高数错题」
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

const CARDS = [
  // ── C语言 ──
  ['专升本-C语言错题',
    'int a[5]; 里，方括号里的 5 是「长度」还是「最大下标」？<br>⇒ 那 a[5] 能不能用？',
    '<b>5 是【长度】（要几个）</b>，不是最大下标。<br><br>' +
    '<b>最大下标 = 长度 − 1 = 4</b><br>' +
    '⇒ 下标只能用 a[0] ~ a[4]，<b>写 a[5] 就越界了</b>。<br><br>' +
    '📌 对照：<code>int a[3][4]</code> → 3 行 4 列 = <b>12 格</b>（不是 4×5=20）',
    'C语言-数组', '2026-09-26'],
  ['专升本-C语言错题',
    '二维数组在内存里是「按行存放」还是「按列存放」？<br>⇒ int a[3][4] 的第 5 个格子是哪个？',
    '<b>按【行】存放</b> —— 先放第 1 行，再放第 2 行。<br><br>' +
    '第 1 行：a[0][0] a[0][1] a[0][2] a[0][3]（4 个）<br>' +
    '<b>第 5 个 = a[1][0]</b>（第 2 行第 1 个）<br><br>' +
    '📌 课本 p164 原文：「先顺序存放第一行的元素，再存放第二行的元素」',
    'C语言-数组', '2026-09-26'],
  ['专升本-C语言错题',
    'int x[3][4]; 时，x 和 x[0] 是不是都表示 x[0][0] 的地址？<br>（2024 真题判断题）',
    '<b>是 ✅（该判断题是对的）</b><br><br>' +
    '关键：<b>二维数组 = 数组的数组</b><br>' +
    'x 是「3 个 int[4]」的首地址<br>' +
    'x[0] 是「第 0 行那个 int[4]」的首地址<br>' +
    '⇒ 两者指向同一块内存起点。<br><br>' +
    '📌 类比：一维数组里 y 和 &y[0] 也相同 —— 同一个道理',
    'C语言-数组', '2026-09-26'],
  ['专升本-C语言错题',
    'char c[] = "China"; 用 %s 输出几个字符？<br>⇒ %c 和 %s 的区别是什么？',
    '输出 <b>5 个字符</b>（China）—— <b>不包括结尾的 \\0</b>。<br><br>' +
    '<b>%c = 一个字符</b>（要循环）<br>' +
    '<b>%s = 一整串</b>（遇 0 就停，只要一个数组名）<br><br>' +
    '⚠️ %s 要写<b>数组名</b>，不是 c[0]',
    'C语言-字符数组', '2026-09-26'],
  ['专升本-C语言错题',
    '用 scanf("%s", s) 输入 <code>How are you</code>，s 里会是什么？<br>⇒ 要读整行怎么办？',
    's 里只有 <b>"How"</b> —— <b>scanf("%s") 遇空格就停</b>。<br><br>' +
    '要读整行（含空格）→ <b>用 gets(s)</b>。<br><br>' +
    '📌 对照：<br>' +
    '读：scanf("%s") 遇空格停 ｜ <b>gets 读整行</b><br>' +
    '写：printf("%s") 不换行 ｜ <b>puts 自动换行</b>',
    'C语言-字符数组', '2026-09-26'],
  ['专升本-C语言错题',
    'strcpy / strcat / strcmp 各自「动的是哪个字符串」？',
    '<b>strcpy(a,b)</b> —— 把 b <b>复制到</b> a（<b>覆盖</b> a 原内容）→ 改 a<br>' +
    '<b>strcat(a,b)</b> —— 把 b <b>接到</b> a <b>后面</b>（a 变长）→ 改 a<br>' +
    '<b>strcmp(a,b)</b> —— <b>只比较，两个都不动</b> → 返回值看正负<br><br>' +
    '⚠️ strcmp 返回值：<b>0 = 相等 · 负 = 左小 · 正 = 左大</b>（只看正负，不记数字）',
    'C语言-字符串函数', '2026-09-26'],
  ['专升本-C语言错题',
    'char s[5] = "ab"; strcat(s, "cde"); 能安全执行吗？',
    '<b>不能 —— 格数不够</b><br><br>' +
    'strcat 需要的格数 = <b>原长度 + 要接的长度 + 1</b>（那个结尾的 0）<br>' +
    '"ab"(2) + "cde"(3) + 结尾 0(1) = <b>6 格</b><br>' +
    's 只有 5 格 ⇒ 装不下 ⇒ <b>越界</b><br><br>' +
    '📌 算格数时【永远别忘了结尾那个 0 也要占一格】<br>' +
    '（改成 char s[6] 就正好够）',
    'C语言-字符串函数', '2026-09-26'],
  ['专升本-C语言错题',
    '从 3 个字符串里找「最大」的，算法思路是什么？<br>（课本例 6.7）',
    '<b>打擂台</b>：先设一个擂主，然后逐个来挑战。<br><br>' +
    '通用版：<br>' +
    '<code>strcpy(string, str[0]);</code>  ← 先设擂主<br>' +
    '<code>for (i=1; i&lt;N; i++)</code><br>' +
    '<code>&nbsp;&nbsp;if (strcmp(str[i], string) &gt; 0)</code><br>' +
    '<code>&nbsp;&nbsp;&nbsp;&nbsp;strcpy(string, str[i]);</code>  ← 挑战者赢了就换擂主<br><br>' +
    '⚠️ 用字符串函数要 <b>#include &lt;string.h&gt;</b>（2024 第 2 题考点）',
    'C语言-算法', '2026-09-26'],
  // ── 高数 ──
  ['专升本-高数错题',
    '两个无穷小比较：比值 → 0 / → ∞ / → 非零常数，分别说明什么？',
    '<b>比值 → 0</b> ⇒ 分子<b>更高阶</b>（跑得更快）<br>' +
    '<b>比值 → ∞</b> ⇒ 分子<b>更低阶</b>（跑得更慢）<br>' +
    '<b>比值 → 非零常数</b> ⇒ <b>同阶</b>（快慢差不多）<br>' +
    '<b>比值 → 1</b> ⇒ <b>等价</b>（同阶的特例）<br><br>' +
    '⚠️ 前提：<b>两个都必须是无无穷小</b>（都趋于 0）',
    '高数-极限', '2026-09-26'],
  ['专升本-高数错题',
    '2x 和 5x 都趋于 0 —— 它们同阶还是不同阶？<br>⇒ 「趋于 0 的速度」看什么？',
    '<b>同阶</b>。<br><br>' +
    '🔴 关键：<b>不看「现在谁大」，看「差距会不会缩小」</b><br>' +
    '2x vs 5x：差距<b>恒定 2.5 倍</b>（从没缩小）⇒ <b>同阶</b><br>' +
    'x vs x²：差距 <b>10 → 100 → 1000 倍</b>（越拉越大）⇒ <b>x² 更高阶</b><br><br>' +
    '🏃 类比：终点是 0 —— 2x 只是<b>起跑线靠前</b>，不是跑得快。',
    '高数-极限', '2026-09-26'],
];

(async () => {
  const notes = CARDS.map(([deck, front, back, tag, src]) => ({
    deckName: deck,
    modelName: '问答题',
    fields: { 正面: front, 背面: back },
    options: { allowDuplicate: false },
    tags: ['专升本', tag, '2026-09-26'],
  }));

  const ids = await inv('addNotes', { notes });
  const ok = ids.filter((x) => x !== null);
  console.log('✅ 建卡', ok.length, '张 | 跳过', ids.length - ok.length, '张（重复）');

  const info = await inv('notesInfo', { notes: ok });
  console.log('\n=== 回读 ===');
  for (const n of info) {
    const f = String(n.fields['正面'].value).replace(/<[^>]+>/g, '').slice(0, 40);
    console.log('  ' + f);
  }
  const bad = info.filter((n) => /\\[a-z]/.test(String(n.fields['背面'].value)));
  console.log('\nLaTeX 残留:', bad.length === 0 ? '无 ✅' : '⚠️ ' + bad.length);
})();
