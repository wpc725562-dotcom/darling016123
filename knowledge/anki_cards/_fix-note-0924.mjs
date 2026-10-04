// 修复 note 1790192698625（高数·有理化）—— LaTeX 反斜杠在 JS 字符串里被转义吃掉了
// 改用纯文本（符合教练手册 §2.0.7 键盘写法约定，也更稳）
const NOTE_ID = 1790192698625;

const front = [
  '高数：<b>0/0 型</b>里，分子带根号怎么办？',
  '<br><br>求 <code>lim(x→0) (√(x+4) − 2) / x</code>',
].join('');

const back = [
  '<b>上下同乘「共轭式」</b>（把中间的减号改成加号），再用<b>平方差</b>消掉根号。',
  '<br><br>共轭式 = <code>√(x+4) + 2</code>',
  '<br><br><code>[√(x+4) − 2] × [√(x+4) + 2]</code>',
  '<br><code>────────────────────────</code>',
  '<br><code>x × [√(x+4) + 2]</code>',
  '<br><br>分子用平方差：<code>(√(x+4))² − 2² = (x+4) − 4 = x</code>',
  '<br><br>约掉 x → <code>1 / [√(x+4) + 2]</code>',
  '<br><br>代 x=0 → <code>1 / (2+2)</code> = <b>1/4</b>',
  '<br><br>⚠️ 约 x 的理由：<b>x 趋近于 0 但不等于 0</b>（所以 x ≠ 0，可以约）。',
].join('');

(async () => {
  const r = await fetch('http://127.0.0.1:8765', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'updateNoteFields',
      version: 6,
      params: { note: { id: NOTE_ID, fields: { 正面: front, 背面: back } } },
    }),
  });
  const d = await r.json();
  console.log('updateNoteFields:', JSON.stringify(d));

  // 回读校验
  const r2 = await fetch('http://127.0.0.1:8765', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action: 'notesInfo', version: 6, params: { notes: [NOTE_ID] } }),
  });
  const d2 = await r2.json();
  for (const [k, v] of Object.entries(d2.result[0].fields)) {
    console.log('[' + k + ']', v.value.replace(/<[^>]+>/g, ' ').slice(0, 220));
  }
  console.log('\n残留 LaTeX 反斜杠:', /\\[a-z]/.test(JSON.stringify(d2.result[0].fields)) ? '⚠️ 有' : '无 ✅');
})();
