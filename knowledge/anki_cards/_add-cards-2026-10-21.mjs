// 1.10 文件操作 · 建卡脚本
// 用法：node _add-cards-2026-10-21.mjs          先预演（不写入）
//      node _add-cards-2026-10-21.mjs --apply   真正写入
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
    front: 'fputc 的参数顺序？',
    back: '<code>fputc(ch, fp);</code><br>念作：<b>写哪个字符 · 到哪个文件</b>',
    tags: ['C语言', '文件', '函数参数'],
  },
  {
    front: 'fputs 的参数顺序？',
    back: '<code>fputs(str, fp);</code><br>念作：<b>写哪个字符串 · 到哪个文件</b>',
    tags: ['C语言', '文件', '函数参数'],
  },
  {
    front: 'fgets 的参数顺序？',
    back: '<code>fgets(str, n, fp);</code><br>念作：<b>存到哪 · 最多多少 · 从哪个文件</b>',
    tags: ['C语言', '文件', '函数参数'],
  },
  {
    front: 'fgets(str, 10, fp) 最多读几个字符？为什么？',
    back: '<b>9 个。</b><br>n 是「最多读 n-1 个」—— 要给字符串结尾的 <code>\'\\0\'</code> 留一个位置。',
    tags: ['C语言', '文件', 'fgets'],
  },
  {
    front: 'fgets 读入一行之后，字符串里除了 hello 这样的内容，还常常多出什么？',
    back: '<b>换行符 <code>\'\\n\'</code>。</b><br>只要这一行没超长，fgets 会把换行符也一起装进字符串。',
    tags: ['C语言', '文件', 'fgets'],
  },
  {
    front: "'\\n' 和 '\\0' 的区别是什么？",
    back: "<b>'\\n'</b>：文件里<b>真实存在</b>的换行字符，fgets 会把它读进来 —— 这才是「多出来」的那个。<br><b>'\\0'</b>：C 语言给每个字符串加的<b>结束标志</b>，所有字符串都有，不是从文件读的。",
    tags: ['C语言', '文件', 'fgets'],
  },
  {
    front: 'fprintf 的参数顺序？为什么 fp 在最前面？',
    back: '<code>fprintf(fp, "格式", 变量);</code><br>念作：<b>到哪个文件 · 按什么格式 · 写什么</b><br>句子开头就是文件，所以 fp 排第一。',
    tags: ['C语言', '文件', '函数参数'],
  },
  {
    front: 'fscanf 的参数顺序？',
    back: '<code>fscanf(fp, "格式", &amp;变量);</code><br>念作：<b>从哪个文件 · 按什么格式 · 读到哪</b>',
    tags: ['C语言', '文件', '函数参数'],
  },
  {
    front: 'fwrite 的参数顺序？',
    back: '<code>fwrite(buf, size, count, fp);</code><br>念作：<b>把什么 · 每块多大 · 几块 · 到哪个文件</b>',
    tags: ['C语言', '文件', '函数参数'],
  },
  {
    front: 'fread 的参数顺序？',
    back: '<code>fread(buf, size, count, fp);</code><br>念作：<b>存到哪 · 每块多大 · 几块 · 从哪个文件</b>',
    tags: ['C语言', '文件', '函数参数'],
  },
  {
    front: 'fopen 的 "r" / "w" / "a" 三种模式，文件已存在时分别怎样？',
    back: '<b>"r"</b> 从头读，不删内容；文件不存在则<b>打开失败</b><br><b>"w"</b> <b>把原内容全部清空</b>，再从头写<br><b>"a"</b> 保留原内容，<b>接着末尾往后写</b>',
    tags: ['C语言', '文件', 'fopen'],
  },
  {
    front: '三个文件函数的特殊返回值：fopen 打开失败 / fclose 关闭成功 / fgetc 读到末尾，各返回什么？',
    back: '<code>fopen</code> → <b>NULL</b><br><code>fclose</code> → <b>0</b>（成功返回 0，不是 1）<br><code>fgetc</code> → <b>EOF</b>（值是 -1）',
    tags: ['C语言', '文件', '返回值'],
  },
  {
    front: '文本文件和二进制文件的区别？',
    back: '<b>文本文件</b>存字符的 ASCII 码：数字 123 → <code>\'1\'\'2\'\'3\'</code> 三个字节，记事本能看懂。<br><b>二进制文件</b>把内存里的字节原样存：int 123 → <code>7B 00 00 00</code> 四个字节，记事本打开是乱码。',
    tags: ['C语言', '文件', '概念'],
  },
  {
    front: 'fprintf(fp, "%d %d", 3, 5) 写进文件的内容是什么？',
    back: '<b><code>3 5</code></b>（三个字符：\'3\'、空格、\'5\'）<br>格式串里除了 % 开头的占位符，其余字符（空格、x=、+ 等）<b>全部原样照抄</b>。',
    tags: ['C语言', '文件', 'fprintf'],
  },
  {
    front: '「把缓冲区数据写入文件」和「写入硬盘」是一回事吗？',
    back: '<b>是同一件事。</b>文件就在硬盘上。<br>卷子上一律说「写入文件 / 存入文件 / 保存到文件」，都指同一个动作，不要因为字面不同就判错。',
    tags: ['C语言', '文件', '概念'],
  },
  {
    front: 'fclose 除了关闭文件，还做了什么？',
    back: '把<b>缓冲区里尚未写入的数据刷到文件（硬盘）</b>。<br>所以写了文件却不 fclose 就结束程序，缓冲区里没倒出去的数据可能丢失。',
    tags: ['C语言', '文件', 'fclose'],
  },
];

async function main() {
  const allDecks = await invoke('deckNames');
  // 牌组名不写死：按关键词找，找不到才建。避免把卡推进错的牌组。
  const hit = allDecks.find((d) => d.includes('C语言') && d.includes('知识'));
  const deckName = hit || '专升本::C语言::知识点';
  if (!hit) await invoke('createDeck', { deck: deckName });

  const modelName = '问答题';
  const fields = await invoke('modelFieldNames', { modelName });
  console.log('牌组 =', deckName);
  console.log('模板 =', modelName, '| 字段 =', fields);

  const notes = CARDS.map((c) => ({
    deckName,
    modelName,
    fields: { 正面: c.front, 背面: c.back },
    tags: c.tags,
    options: { allowDuplicate: false, duplicateScope: 'deck' },
  }));

  console.log('待写入', notes.length, '张');
  if (!APPLY) {
    notes.forEach((n, i) => console.log(`  ${i + 1}. ${CARDS[i].front}`));
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
