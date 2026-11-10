// 2026-10-21 第二批：高数 3.1/3.2 关键点 + C 语言类型转换
// 用法：node _add-cards-2026-10-21-b.mjs          预演
//      node _add-cards-2026-10-21-b.mjs --apply   写入
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
  // ---------- 高数 ----------
  {
    subject: '高数',
    front: '∫xⁿ dx = ?',
    back: '<b>xⁿ⁺¹ / (n+1) + C</b>　（n ≠ −1）<br>记忆：<b>指数升一格，除以新指数</b>',
    tags: ['高数', '积分', '公式'],
  },
  {
    subject: '高数',
    front: '不定积分后面为什么一定要写 +C？',
    back: '因为<b>常数的导数是 0</b>。<br>x²、x²+3、x²−5 求导都得 2x，所以反推回去有<b>无穷多个</b>答案，只能写 C 占位。<br>漏 C = 答案不完整，不是格式问题。',
    tags: ['高数', '积分', '概念'],
  },
  {
    subject: '高数',
    front: '∫2x dx 怎么算？系数怎么处理？',
    back: '2 · (x²/2) = <b>x²</b><br>方法：<b>系数照抄在最前面，只对 x 用公式</b>（指数升一格、除以新指数）。',
    tags: ['高数', '积分', '系数'],
  },
  {
    subject: '高数',
    front: '∫k dx = ?（k 是常数）',
    back: '<b>kx + C</b>',
    tags: ['高数', '积分', '公式'],
  },
  {
    subject: '高数',
    front: '∫[f(x) ± g(x)]dx 能不能拆成两个积分分别算？',
    back: '<b>能。</b>∫f dx ± ∫g dx<br>理由：求导能拆和差，积分是求导的倒带，所以也能拆。',
    tags: ['高数', '积分', '线性性质'],
  },
  {
    subject: '高数',
    front: '∫(x²+3x)dx 拆开算完，C 要写几个？',
    back: '<b>只写一个</b>，写在最后。<br>两个 C 加起来还是一个任意常数，写两个是多余写法，会扣分。',
    tags: ['高数', '积分', '易错'],
  },
  {
    subject: '高数',
    front: '积分算完怎么检查对不对？',
    back: '<b>把答案求导，看能不能变回题目。</b><br>例：(x³)\' = 3x²，所以 ∫3x²dx = x³+C 是对的。',
    tags: ['高数', '积分', '验算'],
  },
  {
    subject: '高数',
    front: '[∫f(x)dx]\' 和 ∫f\'(x)dx，哪个有 C？',
    back: '<b>[∫f dx]\'</b> —— <b>没有 C</b>（先积得到 F+C，再求导时 C 被擦掉）<br><b>∫f\'dx</b> —— <b>有 C</b>（积分必须补占位符）<br>一句话：<b>C 是积分生的，被求导杀的。</b>',
    tags: ['高数', '积分', '积导互逆'],
  },
  // ---------- C 语言 · 类型转换 ----------
  {
    subject: 'C语言',
    front: '(int)3.9 = ?',
    back: '<b>3</b><br>直接把小数点后面<b>砍掉</b>，不四舍五入。3.999 也是 3。',
    tags: ['C语言', '类型转换'],
  },
  {
    subject: 'C语言',
    front: '(int)-3.9 = ?',
    back: '<b>−3</b><br>向<b>零方向</b>截断，不是向下取整（向下取整会得 −4）。',
    tags: ['C语言', '类型转换'],
  },
  {
    subject: 'C语言',
    front: 'int a=7, b=2; 那 (double)a/b 和 (double)(a/b) 分别等于多少？',
    back: '<b>(double)a/b = 3.5</b>（只管 a，把 a 变 7.0 再除）<br><b>(double)(a/b) = 3.0</b>（括号先算 7/2=3，再转成 3.0）<br>规律：<b>强转写在谁前面，就只改谁。</b>',
    tags: ['C语言', '类型转换'],
  },
];

async function main() {
  const allDecks = await invoke('deckNames');
  // 牌组名不写死：按关键词找，找不到才建。
  function pick(mustHave, fallback) {
    const hit = allDecks.find((d) => mustHave.every((k) => d.includes(k)));
    return hit || fallback;
  }
  const deckFor = {
    高数: pick(['高数', '知识'], '专升本::高数::知识点'),
    C语言: pick(['C语言', '知识'], '专升本::C语言::知识点'),
  };

  const modelName = '问答题';
  const fields = await invoke('modelFieldNames', { modelName });
  console.log('模板 =', modelName, '| 字段 =', fields);
  console.log('牌组 =', deckFor);

  const notes = CARDS.map((c) => ({
    deckName: deckFor[c.subject],
    modelName,
    fields: { 正面: c.front, 背面: c.back },
    tags: c.tags,
    options: { allowDuplicate: false, duplicateScope: 'deck' },
  }));

  console.log('待写入', notes.length, '张');
  if (!APPLY) {
    notes.forEach((n, i) => console.log(`  ${i + 1}. [${CARDS[i].subject}] ${CARDS[i].front}`));
    console.log('\n预演结束。加 --apply 真正写入。');
    return;
  }

  const ids = await invoke('addNotes', { notes });
  const ok = ids.filter((x) => x !== null).length;
  console.log('addNotes 返回：成功', ok, '/', notes.length);
  ids.forEach((id, i) => {
    if (id === null) console.log('  失败:', CARDS[i].front);
  });
}

main().catch((e) => {
  console.error('ERROR:', e.message);
  process.exit(1);
});
