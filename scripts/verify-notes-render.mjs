// 用 CDP 打开 VitePress dev server 的页面，读 document.body.innerText，
// 确认指定文字真的渲染出来了（而不是只存在于 .md 源文件里）。
//
// 为什么需要它
//   VitePress dev server 是 SPA：直接 curl 只会拿到 468 字节的壳，
//   markdown 是客户端渲染的。要么跑完整 build（约 140s，且会清 .temp
//   把正在跑的 dev server 搞崩），要么走 CDP 读真实 DOM —— 后者秒级。
//
// 用法
//   node scripts/verify-notes-render.mjs [cdpPort=9222] [devPort=5188]
//
// 改页面对照表
//   编辑下面 PAGES：每项是 [笔记文件名（不含 .md）, [必须出现的文字片段...]]。
//   探针里**不要带反引号**（渲染后 code 标记会消失，会假失败）；
//   需要匹配加粗文字时写纯文本即可（脚本会自动去掉 **）。
//
// 前置
//   dev server 在跑（默认 5188）；调试 Chrome 带 --remote-debugging-port=9222 在跑。
const CDP = Number(process.argv[2] || 9222);
const DEV = Number(process.argv[3] || 5188);
const SITE = `http://127.0.0.1:${DEV}/darling016123/`;

// 每项：[相对站点根的路径（不含 .md）, [必须出现的文字片段...]]
const PAGES = [
  ['posts/computer/notes/1.1-C语言概述与基本概念', ['标识符的「三条规则」', '函数的位置，考试怎么设陷阱', '是关键字']],
  ['posts/computer/notes/1.2-数据的存储与运算', ['的结果是正是负', '一律的实型常量都是 double', '按权求和', '标准化指数形式']],
  ['posts/computer/notes/1.6-数组', ['地址常量', '列号不能省、行号可以省', '画图']],
  ['posts/computer/notes/1.8-指针', ['指针变量」是同一个东西吗', '单目运算符', '取值（解引用）运算符']],
  ['posts/computer/notes/1.10-文件操作', ['执行成功时返回什么', '成功 = 0', '只讲了 1 个点']],
  ['posts/computer/notes/2.2-线性表', ['存储单元**必须不能连续**', '先挂后连', '逻辑关系']],
  ['posts/computer/notes/2.4-串、数组和广义表', ['空格串简称空串', '以 T 为首的子串', '广义表', 'string.h']],
  ['guide/bili-plan/computer', ['分P → 章节映射表', '鹏哥 C 语言', '唯一完整源']],
];

async function newTab() {
  const r = await fetch(`http://127.0.0.1:${CDP}/json/new?about:blank`, { method: 'PUT' });
  return r.json();
}
async function closeTab(id) {
  await fetch(`http://127.0.0.1:${CDP}/json/close/${id}`);
}

function connect(wsUrl) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    let id = 0;
    const pending = new Map();
    ws.addEventListener('open', () => resolve({
      send(method, params = {}) {
        const mid = ++id;
        ws.send(JSON.stringify({ id: mid, method, params }));
        return new Promise((res, rej) => pending.set(mid, { res, rej }));
      },
      close: () => ws.close(),
    }));
    ws.addEventListener('error', reject);
    ws.addEventListener('message', (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id && pending.has(msg.id)) {
        const { res, rej } = pending.get(msg.id);
        pending.delete(msg.id);
        msg.error ? rej(new Error(JSON.stringify(msg.error))) : res(msg.result);
      }
    });
  });
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let pass = 0, fail = 0;

for (const [path, probes] of PAGES) {
  const tab = await newTab();
  const c = await connect(tab.webSocketDebuggerUrl);
  const name = path;
  try {
    await c.send('Page.enable');
    await c.send('Runtime.enable');
    await c.send('Page.navigate', { url: SITE + path.split('/').map(encodeURIComponent).join('/') });
    await sleep(2500);
    const { result } = await c.send('Runtime.evaluate', {
      expression: 'document.body.innerText',
      returnByValue: true,
    });
    const text = result.value || '';
    const missing = probes.filter((p) => !text.includes(p.replace(/\*\*/g, '')));
    const ok = text.length > 2000 && missing.length === 0;
    if (ok) pass++; else fail++;
    console.log(`${ok ? 'OK  ' : 'FAIL'} ${name}  (${text.length} 字符)` +
      (missing.length ? `  缺: ${missing.join(' / ')}` : ''));
  } catch (e) {
    fail++;
    console.log(`ERR  ${name}  ${e.message}`);
  } finally {
    c.close();
    await closeTab(tab.id);
  }
}

console.log(`\n${pass} 通过 / ${fail} 失败`);
process.exit(fail ? 1 : 0);
