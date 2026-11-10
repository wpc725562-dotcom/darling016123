// 2026-10-20 会话错题建卡脚本
// 用法：node _add-cards-2026-10-20.mjs          预演（只看不改）
//       node _add-cards-2026-10-20.mjs --apply  真正写入
//
// 本场共 12 张：英语写作 8 张（首篇成文的 8 处错）+ C语言 3 张（1.1/1.2 补验的错）
//              + ASCII 1 张（顺带补的必背值）
// 来源：学习日志 2026-10-20 / 2026-10-21 相关条目

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

// 牌组名不写死：按关键词在现有牌组里找，找不到再建。避免把卡推进错的牌组。
function pickDeck(allDecks, mustHave, fallback) {
  const hit = allDecks.find((d) => mustHave.every((k) => d.includes(k)));
  return hit || fallback;
}

const CARDS = [
  {
    subject: '英语',
    tags: ['英语', '写作', '中秋'],
    front: '「中秋节」的英文怎么写？（注意：不要写成 Mouth Part / Month Part）',
    back: 'Mid-Autumn Festival\n\n这是 2026 邀请信的关键词，写错等于偏题，直接掉到 1-2 分。',
  },
  {
    subject: '英语',
    tags: ['英语', '写作', '搭配'],
    front: '「邀请某人参加某活动」，最不容易拼错的写法是什么？',
    back:
      'invite sb to + 名词\n\n例：I am writing to invite you to our Mid-Autumn Festival party.\n\n' +
      '比 invite sb to participate in ... 更短：不用拼 participate，也不用管 in 放哪。',
  },
  {
    subject: '英语',
    tags: ['英语', '写作', '被动'],
    front: '「晚会将于下周五举办」—— 用主动还是被动？句子怎么造？',
    back:
      '被动：The party will be held in the school hall.\n\n' +
      '晚会是「被」举办的。will 后面只能跟动词原形，所以是 will be held，不是 will held。',
  },
  {
    subject: '英语',
    tags: ['英语', '写作', '语法'],
    front: 'such as 后面接动词时，用什么形式？',
    back:
      '动名词 doing\n\n' +
      '对：such as admiring the moon and tasting mooncakes\n' +
      '错：such as admire the moon and taste mooncakes\n\n' +
      'such as 是介词短语，后面要名词性质的东西。',
  },
  {
    subject: '英语',
    tags: ['英语', '写作', '介词'],
    front: 'next Friday 前面要不要加 at？',
    back:
      '不加。\n\n' +
      'next / last / this + 时间，前面一律不加介词。\n' +
      '对：next Friday　错：at next Friday\n\n' +
      '具体钟点才用 at：at 7 p.m.',
  },
  {
    subject: '英语',
    tags: ['英语', '写作', '格式'],
    front: '书信作文的落款怎么写？漏了会怎样？',
    back: 'Yours sincerely,\nLi Hua\n\n漏了扣格式分（得分四条之一：格式正确）。',
  },
  {
    subject: '英语',
    tags: ['英语', '写作', '结构'],
    front: '一篇书信作文里「I am writing to ...」能出现几次？',
    back: '只能 1 次。\n\n这是「来意句」，全文只需交代一次来意。出现两次 = 重复，扣分。',
  },
  {
    subject: '英语',
    tags: ['英语', '写作', '来意句'],
    front: '五个体裁的「来意句」分别是哪一句？',
    back:
      '邀请：I am writing to invite you to ______ .\n' +
      '求职：I am writing to apply for the position of ______ .\n' +
      '投诉：I am writing to complain about ______ .\n' +
      '劝说：I am writing to express my concern about ______ .\n' +
      '建议：Thanks for your email asking about ______ . I am writing to give you some suggestions.\n\n' +
      '一套骨架，只换这一句。',
  },
  {
    subject: 'C语言',
    tags: ['C语言', '1.1', '标识符'],
    front: '标识符可以由哪些字符组成？a-b 合法吗？',
    back:
      '只能由字母、数字、下划线组成；不能数字开头；不能是关键字。\n\n' +
      'a-b 不合法 —— 减号是运算符，不在标识符字符集里。a-b 是「a 减 b」一个表达式。\n\n' +
      '对比：下划线可以（print_star 是一个名字），减号不可以。',
  },
  {
    subject: 'C语言',
    tags: ['C语言', '1.1', 'main'],
    front: 'C 程序的入口函数怎么写？写错会怎样？',
    back:
      'main —— 四个字母，顺序不能换。\n\n' +
      '写成 mian 编译器报「未定义标识符」，程序根本跑不起来。\n' +
      '应用题手写代码时第一行写错，后面全白写。',
  },
  {
    subject: 'C语言',
    tags: ['C语言', '1.2', '逗号表达式'],
    front: 'int a=1, b=2; 求 (a=3, b=4, a+b) 的值。a 和 b 被赋值了吗？',
    back:
      '7。\n\n' +
      '逗号表达式：从左往右依次算，取最后一个的值。\n' +
      '前两步真的执行了 —— a 现在是 3，b 现在是 4。\n' +
      '不是「只执行最后一个」。',
  },
  {
    subject: 'C语言',
    tags: ['C语言', '1.2', 'ASCII'],
    front: "ASCII 值：'A' / 'a' / '0' 分别是多少？",
    back: "'A' = 65\n'a' = 97\n'0' = 48\n\nprintf(\"%d\", c) 打编码；printf(\"%c\", c) 打字符。",
  },
];

async function main() {
  const decks = await invoke('deckNames');
  const deckFor = {
    英语: pickDeck(decks, ['英语', '错题'], '专升本::英语::错题'),
    C语言: pickDeck(decks, ['C语言', '错题'], '专升本::C语言::错题'),
  };

  console.log('===== 2026-10-20 建卡 · ' + (APPLY ? '执行' : '预演 dry-run') + ' =====');
  console.log('英语 → ' + deckFor.英语);
  console.log('C语言 → ' + deckFor.C语言);
  console.log('共 ' + CARDS.length + ' 张\n');

  for (const d of new Set(Object.values(deckFor))) {
    const exists = decks.includes(d);
    console.log((exists ? '牌组已存在 ' : '需要新建   ') + d);
    if (APPLY && !exists) await invoke('createDeck', { deck: d });
  }
  console.log('');

  const notes = CARDS.map((c) => ({
    deckName: deckFor[c.subject],
    // 本机 Anki 是中文界面：「问答题」= Basic，字段名是「正面 / 背面」
    modelName: '问答题',
    fields: { 正面: c.front, 背面: c.back },
    tags: c.tags,
    options: { allowDuplicate: false, duplicateScope: 'deck' },
  }));

  if (!APPLY) {
    notes.forEach((n, i) => {
      console.log('[' + (i + 1) + '] ' + n.deckName);
      console.log('    Q: ' + n.fields.Front.split('\n')[0]);
    });
    console.log('\n预演结束。加 --apply 才真正写入。');
    return;
  }

  const ids = await invoke('addNotes', { notes });
  const ok = ids.filter((x) => x !== null).length;
  console.log('写入成功 ' + ok + ' / ' + ids.length);
  ids.forEach((id, i) => {
    if (id === null) console.log('  未写入（可能重复）：' + CARDS[i].front.split('\n')[0]);
  });
}

main().catch((e) => {
  console.error('失败：' + e.message);
  console.error('Anki 是否已打开？AnkiConnect 是否在 127.0.0.1:8765 监听？');
  process.exit(1);
});
