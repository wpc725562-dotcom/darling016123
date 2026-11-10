#!/usr/bin/env node
/**
 * coach.mjs —— 教练流程检查器
 *
 * 为什么需要这个（2026-10-22 学生原话：「你这怎么让我放心 每次都没成系统」）：
 *
 *   当天暴露的 5 个错，全部是「事后发现」而不是「事前拦住」：
 *     1. 高数第三章节号映射错（卡片写 3.4=三角代换，笔记实际 3.4=根式代换，整体偏一节）
 *     2. 每日卡排期跳步 4 次（1.10 / 3.3 / 3.4 / 3.5 全跳过未讲的节）
 *     3. 学习日边界算错（按日历 00:00 切，学生作息是 15:00 起床→次日 04:00 睡）
 *     4. B 站讲义对比断了 9 天（最后一份 10-09，之后开 4 节新课一份没做）
 *     5. 铁律「没教过的不出题」违反 3 次
 *
 *   共同根因：**所有检查都依赖「我记得」，而 AI 会忘。**
 *   ⇒ 把检查从「记忆」搬到「脚本」，让它在开课前/收口前强制拦一道。
 *
 * 用法：
 *   node scripts/coach.mjs map 高数              # 列出笔记真实节号映射
 *   node scripts/coach.mjs taught 高数           # 列出日志里已讲过的节
 *   node scripts/coach.mjs check 高数 3.4        # 开课前检查：能不能讲
 *   node scripts/coach.mjs card D017             # 检查某张每日卡的排期合法性
 *   node scripts/coach.mjs review D017           # 检查某张每日卡的复检条目是否有讲课记录
 *
 * 退出码：0 = 全绿；1 = 有 ❌ 阻断项；2 = 只有 ⚠️ 提醒
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, '..');

const NOTES_DIR = {
  高数: path.join(ROOT, 'docs', 'posts', 'math', 'notes'),
  计算机: path.join(ROOT, 'docs', 'posts', 'computer', 'notes'),
  英语: path.join(ROOT, 'docs', 'posts', 'english', 'notes'),
};

/** 笔记目录名 ↔ 日志 subject 字段的别名映射（日志里计算机写作「C语言」） */
const SUBJECT_ALIAS = {
  高数: ['高数'],
  计算机: ['C语言', '计算机', '数据结构'],
  英语: ['英语'],
};
const LOG = path.join(ROOT, '备考计划', '学习日志.jsonl');
const BILI = path.join(ROOT, 'data', 'bili-analyze', '_extract');
/* 日卡目录。2026-10-31 从桌面改为本仓库 —— 依据 `00-先看这个.md` 规则 12：
   唯一真相源是 `备考计划/`，桌面那份只读。此前这里读桌面，导致「在项目里改日卡、
   coach 却看不见」，两边一旦分叉就没人说得清哪份算数。
   实测两边 392 个文件 md5 全同，所以切换路径不改任何行为，只是把源指向正确的地方。 */
const CARD_DIR = path.join(ROOT, '备考计划', '每日');

/**
 * 真题对照表（2026-10-26 加）。
 * 学生原话：「每次开课除了看 studio 里的知识，还要对比网课和真题，每次都会忘记参考这些」。
 * 光有 biliHits（网课）不够，缺真题这一半 —— 真题定「讲多深」，网课定「怎么讲」。
 */
const REAL_EXAM = {
  高数: path.join(ROOT, 'docs', 'posts', 'math', '真题章节对照表.md'),
  计算机: path.join(ROOT, 'docs', 'posts', 'computer', '真题章节对照表.md'),
  英语: path.join(ROOT, 'docs', 'posts', 'english', '真题题型对照表.md'),
};

const GREEN = '\x1b[32m', YELLOW = '\x1b[33m', RED = '\x1b[31m', DIM = '\x1b[2m', RESET = '\x1b[0m';
const ok = (s) => `${GREEN}✅${RESET} ${s}`;
const warn = (s) => `${YELLOW}⚠️ ${RESET} ${s}`;
const bad = (s) => `${RED}❌${RESET} ${s}`;

/* ---------- 数据加载 ---------- */

/** 从笔记文件名提取节号与标题：`3.4-第二类换元法之根式代换.md` */
function loadNotes(subject) {
  const dir = NOTES_DIR[subject];
  if (!dir || !fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .filter((f) => f.endsWith('.md') && /^\d+\.\d+/.test(f))
    .map((f) => {
      const m = f.match(/^(\d+\.\d+[a-z]?)-(.+)\.md$/);
      if (!m) return null;
      return { no: m[1], title: m[2], file: f };
    })
    .filter(Boolean)
    .sort((a, b) => cmpNo(a.no, b.no));
}

function cmpNo(a, b) {
  const pa = a.match(/(\d+)\.(\d+)([a-z]?)/);
  const pb = b.match(/(\d+)\.(\d+)([a-z]?)/);
  if (!pa || !pb) return a.localeCompare(b);
  const d = (+pa[1] - +pb[1]) || (+pa[2] - +pb[2]);
  return d !== 0 ? d : (pa[3] || '').localeCompare(pb[3] || '');
}

function loadLog() {
  if (!fs.existsSync(LOG)) return [];
  return fs.readFileSync(LOG, 'utf8')
    .split('\n')
    .filter((l) => l.trim())
    .map((l) => { try { return JSON.parse(l); } catch { return null; } })
    .filter(Boolean);
}

/**
 * 从日志判断某科目已讲过哪些节号。
 *
 * ⚠️ 三条踩过的坑（2026-10-22 逐条修）：
 *   ① 全文搜会把「2.4 链式法则（含 2.5 预告）」里的 2.5 误判成已讲
 *      ⇒ 改为「只取标题里前 2 个**笔记目录中真实存在**的节号」
 *   ② 只匹配标题开头会漏掉「C语言 1.8 指针 第 5 课」「数据结构 2.2 线性表」这类写法
 *      ⇒ 不再要求开头，全文找但必须命中笔记白名单
 *   ③ 日志 subject 写「C语言」而笔记目录叫「计算机」
 *      ⇒ 用 SUBJECT_ALIAS 映射
 *   ④ 1.9 结构体章内部有 3.x 小节号（3.8 结构体内存），会被算成数据结构 3.x
 *      ⇒ 白名单天然挡掉（计算机笔记只有 1.x / 2.x）
 */
function taughtSections(subject) {
  const valid = new Set(loadNotes(subject).map((n) => n.no));
  const rows = loadLog();
  const set = new Set();
  const aliases = SUBJECT_ALIAS[subject] || [subject];
  for (const r of rows) {
    if (!aliases.includes(r.subject)) continue;
    if (!['lecture', 'quiz'].includes(r.kind)) continue;
    const text = r.title || '';
    // 排除「整章自测/测验」类记录 —— 它们标题里会写「2.1–2.5」这种区间，
    // 会把没讲过的节（2.5 隐函数）误算成已讲。讲课/当堂验收才作数。
    if (/自测|测验|限时|整章|全章/.test(text)) continue;
    // 只看标题前 24 个字符：既覆盖「C语言 1.8 指针 第 5 课」「1.1 + 1.2 补验」这类写法，
    // 又不会抓到括号里顺带提一句的后继节号（如「2.4 链式法则（含 2.5 预告）」）。
    const head = text.slice(0, 24);
    const re = /\b(\d+\.\d+[a-z]?)\b/g;
    let m;
    while ((m = re.exec(head))) {
      if (valid.has(m[1])) set.add(m[1]);
    }
  }
  return set;
}

/** B 站讲义里含关键词的文件 */
function biliHits(keyword) {
  if (!fs.existsSync(BILI)) return [];
  const hits = [];
  for (const f of fs.readdirSync(BILI)) {
    if (!f.endsWith('.md')) continue;
    const txt = fs.readFileSync(path.join(BILI, f), 'utf8');
    if (txt.includes(keyword)) {
      const head = txt.split('\n').find((l) => l.startsWith('# ')) || '';
      hits.push({ file: f, head: head.replace(/^#\s*/, '').slice(0, 70) });
    }
  }
  return hits;
}

/**
 * 真题对照表里含关键词的表格行。
 * 只扫 `|` 开头的表格行 —— 说明文字里提到考点名不算命中（同 cardSections 的教训）。
 * 返回 null 表示该科没有对照表文件（区别于「有文件但没命中」）。
 */
function realExamHits(subject, keyword) {
  const file = REAL_EXAM[subject];
  if (!file || !fs.existsSync(file)) return null;
  const lines = fs.readFileSync(file, 'utf8').split('\n');
  const hits = [];
  let section = '';
  for (const line of lines) {
    if (/^#{2,3}\s/.test(line)) section = line.replace(/^#+\s*/, '').trim();
    if (!line.startsWith('|') || /^\|[\s:|-]+\|$/.test(line)) continue;
    if (line.includes(keyword)) hits.push({ section, line: line.trim() });
  }
  return { file, hits };
}

/**
 * 每日卡「今日配额表」里的节号引用。
 * 只扫配额表那一列，不扫全文 —— 全文扫会把说明文字里提到的节号（如「3.5=三角代换」）
 * 误判成「今天要讲 3.5」。2026-10-22 第一版就报了 3 个假跳步。
 * 同时剔除 `~~删除线~~` 里的内容（那是被改掉的旧排期）。
 */
function cardSections(cardId) {
  const files = fs.readdirSync(CARD_DIR).filter((f) => f.startsWith(cardId));
  if (!files.length) return null;
  const file = path.join(CARD_DIR, files[0]);
  const txt = fs.readFileSync(file, 'utf8');

  // 抓配额表：`| 时段 | **科目** | 时长 | 今日内容 |`
  const quotaLines = txt.split('\n').filter((l) => /^\|\s*(上午|下午|碎片|睡前)/.test(l));
  const refs = new Set();
  for (const line of quotaLines) {
    const cols = line.split('|');
    const content = (cols[4] || '').replace(/~~.*?~~/g, ''); // 剔删除线
    const re = /\b(\d+\.\d+)\b/g;
    let m;
    while ((m = re.exec(content))) refs.add(m[1]);
  }
  return { file, name: files[0], refs: [...refs].sort(cmpNo), txt, quotaLines };
}

/* ---------- 命令 ---------- */

function cmdMap(subject) {
  const notes = loadNotes(subject);
  const taught = taughtSections(subject);
  if (!notes.length) {
    console.log(bad(`${subject} 没有找到带节号的笔记`));
    return 1;
  }
  console.log(`\n${subject} · 笔记真实节号映射（共 ${notes.length} 节）\n`);
  for (const n of notes) {
    const isTaught = taught.has(n.no);
    const mark = isTaught ? `${GREEN}已讲${RESET}` : `${DIM}未讲${RESET}`;
    console.log(`  ${n.no.padEnd(6)} ${mark}  ${n.title}`);
  }
  const done = notes.filter((n) => taught.has(n.no)).length;
  console.log(`\n  进度：${done}/${notes.length} = ${Math.round((done / notes.length) * 100)}%\n`);
  return 0;
}

function cmdTaught(subject) {
  const set = taughtSections(subject);
  console.log(`\n${subject} 已讲节号（日志 lecture/quiz 记录）：`);
  console.log('  ' + ([...set].sort(cmpNo).join(' · ') || '（无）') + '\n');
  return 0;
}

function cmdCheck(subject, no) {
  const notes = loadNotes(subject);
  const target = notes.find((n) => n.no === no);
  const taught = taughtSections(subject);
  let code = 0;

  console.log(`\n开课前检查 · ${subject} ${no}\n`);

  if (!target) {
    console.log(bad(`笔记里没有 ${no} 这一节 —— 节号可能写错了`));
    const near = notes.filter((n) => n.no.startsWith(no.split('.')[0] + '.')).map((n) => `${n.no}=${n.title}`);
    console.log(`   ${DIM}本章实际节号：${near.join(' · ')}${RESET}\n`);
    return 1;
  }

  console.log(ok(`笔记存在：${target.title}`));
  console.log(`   ${DIM}${target.file}${RESET}`);

  // 1. 铁律：这一节讲过没
  if (taught.has(no)) {
    console.log(ok(`日志有记录 → 已讲过（复检/加深可开）`));
  } else {
    console.log(warn(`日志零记录 → 首次开讲（按密度上限：1 例 + 1 组记号 + 1 题）`));
  }

  // 2. 前置：同章上一节讲了吗
  const idx = notes.findIndex((n) => n.no === no);
  if (idx > 0) {
    const prev = notes[idx - 1];
    if (taught.has(prev.no)) {
      console.log(ok(`前置 ${prev.no}（${prev.title}）已讲`));
    } else {
      console.log(bad(`前置 ${prev.no}（${prev.title}）**未讲** —— 先补它`));
      code = 1;
    }
  }

  // 3. 真题对照（2026-10-26 新规矩：开课前必须查真题 —— 真题定「讲多深」）
  const kw = target.title.replace(/（.*?）|\(.*?\)/g, '').slice(0, 4);
  if (kw.length <= 2) {
    console.log(warn(`关键词「${kw}」只有 ${kw.length} 字 → 命中会混进无关讲义，换更具体的词再查`));
  }
  const ex = realExamHits(subject, kw);
  if (ex === null) {
    console.log(warn(`${subject} 没有真题对照表 → 手动查 docs/posts/${subject === '计算机' ? 'computer' : subject === '高数' ? 'math' : 'english'}/ 下的真题文件`));
    code = code || 2;
  } else if (!ex.hits.length) {
    console.log(warn(`真题表里没搜到「${kw}」→ 换关键词重搜；确认真没考过 = 只出客观题，别深讲`));
    code = code || 2;
  } else {
    console.log(ok(`真题命中 ${ex.hits.length} 条（关键词「${kw}」）→ 按这些题型定练习形式`));
    for (const h of ex.hits.slice(0, 6)) {
      console.log(`   ${DIM}[${h.section}] ${h.line.slice(0, 88)}${RESET}`);
    }
    if (ex.hits.length > 6) console.log(`   ${DIM}…另 ${ex.hits.length - 6} 条${RESET}`);
  }

  // 4. B 站讲义（2026-10-22 新规矩：开课前必须扫 —— 网课定「怎么讲」）
  const hits = biliHits(kw);
  if (hits.length) {
    console.log(ok(`B 站有 ${hits.length} 份对应讲义（关键词「${kw}」）→ 开课前扫一遍讲法`));
    for (const h of hits.slice(0, 4)) console.log(`   ${DIM}${h.file}  ${h.head}${RESET}`);
    if (hits.length > 4) console.log(`   ${DIM}…另 ${hits.length - 4} 份${RESET}`);
  } else {
    console.log(warn(`B 站没搜到「${kw}」→ 换关键词再搜一次，或确认网课没覆盖`));
    code = code || 2;
  }

  console.log('');
  return code;
}

function cmdCard(cardId) {
  const card = cardSections(cardId);
  if (!card) {
    console.log(bad(`找不到 ${cardId} 开头的每日卡`));
    return 1;
  }
  const mathNotes = loadNotes('高数');
  const compNotes = loadNotes('计算机');
  const mathTaught = taughtSections('高数');
  const compTaught = taughtSections('计算机');

  console.log(`\n每日卡排期检查 · ${card.name}\n`);

  // 高数节号：卡片里出现的 3.x
  const mathRefs = card.refs.filter((r) => /^3\./.test(r));
  const compRefs = card.refs.filter((r) => /^1\.(9|10|11)$|^2\./.test(r));

  if (mathRefs.length) {
    console.log(`高数节号引用：${mathRefs.join(' · ')}`);
    console.log(`  ${DIM}（只对「今日主任务」= 第一个节号做跳步判定；其余仅列状态，`
      + `因为配额表里常写「3.5=三角代换」这类说明文字）${RESET}`);
    for (let i = 0; i < mathRefs.length; i++) {
      const r = mathRefs[i];
      const note = mathNotes.find((n) => n.no === r);
      if (!note) {
        console.log(bad(`  ${r} 在笔记里不存在 → 节号映射错`));
        continue;
      }
      const idx = mathNotes.findIndex((n) => n.no === r);
      const prev = idx > 0 ? mathNotes[idx - 1] : null;
      const thisOk = mathTaught.has(r);
      const prevOk = prev ? mathTaught.has(prev.no) : true;
      const isMain = i === 0;
      const jump = isMain && prev && !prevOk && !thisOk;

      console.log(
        `  ${r} = ${note.title}  ${thisOk ? GREEN + '已讲' + RESET : DIM + '未讲' + RESET}` +
        (isMain ? `  ${DIM}← 今日主任务${RESET}` : '') +
        (jump ? `  ${RED}← 前置 ${prev.no} 未讲，跳步！${RESET}` : '')
      );
      if (jump) console.log(`      ${DIM}应先讲 ${prev.no}（${prev.title}）${RESET}`);
    }
    console.log('');
  }

  if (compRefs.length) {
    console.log(`计算机节号引用：${compRefs.join(' · ')}`);
    for (const r of compRefs) {
      const note = compNotes.find((n) => n.no === r);
      console.log(`  ${r} ${note ? '= ' + note.title : '（笔记里无此节）'}  ${compTaught.has(r) ? GREEN + '已讲' + RESET : DIM + '未讲' + RESET}`);
    }
    console.log('');
  }

  return 0;
}

/**
 * 复检条目合法性：该知识点**全库**有没有讲课记录。
 *
 * ⚠️ 不按「来源日 D0XX 那天的日志」查 —— 复检条目的来源日是「上次复检日」，
 * 不是「首次讲课日」。第一版按来源日查，把 D010 `do-while`（实际 09-20 就讲过）
 * 误判成「补学任务」。2026-10-22 修。
 *
 * 判据：全库 lecture/quiz 记录里，有没有标题或备注含该关键词。
 * 命中 → ✅；未命中 → ⚠️ 提示人工确认（不判死，因为关键词提取本身不可靠）。
 */
function cmdReview(cardId) {
  const card = cardSections(cardId);
  if (!card) {
    console.log(bad(`找不到 ${cardId} 开头的每日卡`));
    return 1;
  }
  const rows = loadLog().filter((r) => ['lecture', 'quiz'].includes(r.kind));
  console.log(`\n复检条目合法性检查 · ${card.name}\n`);

  const lines = card.txt.split('\n').filter((l) => /^\|\s*D\d{3}\s*\|/.test(l));
  if (!lines.length) {
    console.log(warn('卡上没有找到复检表行'));
    return 0;
  }

  let problems = 0;
  for (const line of lines) {
    const cols = line.split('|').map((c) => c.trim());
    const from = cols[1], pri = cols[2], topic = (cols[3] || '').replace(/~~/g, '');
    const voided = /作废|不复检/.test(topic);

    // 关键词：取主题里的第一个实词（去掉反引号/星号/括号）
    const keys = topic
      .replace(/[`*_（）()]/g, ' ')
      .split(/[\s·、,，vs]+/)
      .filter((w) => w.length >= 2 && !/^\d/.test(w))
      .slice(0, 3);

    const hits = rows.filter((r) => {
      const blob = `${r.title || ''} ${r.note || ''}`;
      return keys.some((k) => blob.includes(k));
    });

    let status;
    if (voided) status = `${DIM}已作废，应剔除${RESET}`;
    else if (hits.length) {
      status = ok(`全库 ${hits.length} 条讲课/验收记录（如 ${hits[0].date}「${(hits[0].title || '').slice(0, 18)}…」）`);
    } else {
      status = warn(`全库搜「${keys.join('/')}」零命中 → 人工确认是否讲过`);
      problems++;
    }
    console.log(`  ${from} ${pri.padEnd(3)} ${topic.slice(0, 30).padEnd(32)} ${status}`);
  }
  console.log(`\n  共 ${lines.length} 条，${problems} 条待人工确认\n`);
  return problems ? 2 : 0;
}

/** D001=2026-10-07，逐日推 */
function dayToDate(id) {
  const n = parseInt(id.slice(1), 10);
  const base = new Date('2026-10-07T00:00:00');
  base.setDate(base.getDate() + (n - 1));
  return base.toISOString().slice(0, 10);
}

/* ---------- 入口 ---------- */

const [cmd, a1, a2] = process.argv.slice(2);
let code = 0;

switch (cmd) {
  case 'map': code = cmdMap(a1); break;
  case 'taught': code = cmdTaught(a1); break;
  case 'check': code = cmdCheck(a1, a2); break;
  case 'card': code = cmdCard(a1); break;
  case 'review': code = cmdReview(a1); break;
  default:
    console.log(`
coach.mjs —— 教练流程检查器

  node scripts/coach.mjs map 高数          笔记真实节号映射 + 进度
  node scripts/coach.mjs taught 高数       日志里已讲过的节号
  node scripts/coach.mjs check 高数 3.4    开课前检查（笔记/铁律/前置/B站讲义）
  node scripts/coach.mjs card D017         每日卡排期合法性（跳步检测）
  node scripts/coach.mjs review D017       复检条目是否有讲课记录
`);
    code = 1;
}

process.exit(code);
