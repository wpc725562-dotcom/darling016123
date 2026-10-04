// 改 Anki 每日上限：复习 200→400 · 新卡 40→15
// 依据：英语-单词记忆方法-2026-09-24.md §4（真实到期 617 被上限 200 卡住）
// 快照备份：D:/_anki-snap-0924/（三文件）
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

(async () => {
  const cfg = await inv('getDeckConfig', { deck: '专升本英语-高频词' });
  console.log('=== 改前 ===');
  console.log('  configId =', cfg.id, '| name =', cfg.name);
  console.log('  new.perDay =', cfg.new.perDay, '| rev.perDay =', cfg.rev.perDay);

  const before = { new: cfg.new.perDay, rev: cfg.rev.perDay };

  cfg.new.perDay = 15;   // 40 → 15（1034 张存量，别一次挤爆复习）
  cfg.rev.perDay = 400;  // 200 → 400（真实到期 617）

  const ok = await inv('saveDeckConfig', { config: cfg });
  console.log('\nsaveDeckConfig 返回:', ok);

  // 回读校验
  const after = await inv('getDeckConfig', { deck: '专升本英语-高频词' });
  console.log('\n=== 回读校验 ===');
  console.log('  new.perDay:', before.new, '→', after.new.perDay, after.new.perDay === 15 ? '✅' : '❌');
  console.log('  rev.perDay:', before.rev, '→', after.rev.perDay, after.rev.perDay === 400 ? '✅' : '❌');

  // 抽查另一个牌组（应同步，因为共用 config id 1）
  const other = await inv('getDeckConfig', { deck: '专升本-C语言错题' });
  console.log('\n=== 抽查「专升本-C语言错题」（共用同一配置，应同步）===');
  console.log('  new.perDay =', other.new.perDay, '| rev.perDay =', other.rev.perDay,
    (other.new.perDay === 15 && other.rev.perDay === 400) ? '✅ 已同步' : '❌ 未同步');
})();
