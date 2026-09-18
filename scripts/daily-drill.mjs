#!/usr/bin/env node
/**
 * 每日刷题计划 + 随机抽题（零基础友好版）
 *
 * 用法：
 *   node scripts/daily-drill.mjs                     # 默认：总量 15 题，随机分布到各题库源，难度 6:3:1，顺序打散
 *   node scripts/daily-drill.mjs --total 20           # 指定总题量（随机分配到各源）
 *   node scripts/daily-drill.mjs --count 5            # 旧模式：每个源各抽 5 题（9 源会出 45 题，门户已不用，仅手动专项刷题时用）
 *   node scripts/daily-drill.mjs --subject 高数        # 只抽某个源（源名见 --list）
 *   node scripts/daily-drill.mjs --level 基础          # 锁定难度：基础/中档/拔高/全部
 *   node scripts/daily-drill.mjs --ratio 8,2,0        # 基础:中档:拔高 配比（默认 6,3,1）
 *   node scripts/daily-drill.mjs --grouped            # 按源分块输出（默认打散交错）
 *   node scripts/daily-drill.mjs --open               # 答案默认展开（默认是折叠，逼自己先回想）
 *   node scripts/daily-drill.mjs --list               # 列出各源题量 + 难度分布
 *
 * 针对零基础的三条设计原则：
 *   1. 答案必须自包含 —— 题库里的「解析 / 解 / 考点 / 错误改正」原样带出，绝不出现"见原文档"。
 *   2. 难度必须可见 —— 每题标 ★/★★/★★★，并按配比抽题，不是无脑随机。
 *   3. 科目随机交错 —— 默认把不同源打散混排（交错练习），不做「政治5道+高数5道」的分块。
 *      这一条同时是记忆科学的「interleaving」要求，看板「科学规则」区已写明。
 */
import { readFileSync, writeFileSync, existsSync } from 'node:fs'
import { join, dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..')

/* ★ 本文件是「顶层执行」脚本：`import()` 它会直接跑主流程，**静默覆盖当天的
   计划文件**（题序会变，且原文件不在 git 里、无法还原）。
   2026-09-18 调试时踩过一次。这里加守卫：非直接执行（被 import）时不写文件。
   调试要引用本文件的函数：复制成 scripts/_dd-debug.mjs（ROOT 靠脚本位置推，
   所以必须放仓库内），并在末尾加 `export { ... }` 后 import。 */
const IS_MAIN = !!process.argv[1] &&
  resolve(process.argv[1]) === fileURLToPath(import.meta.url)
const args = process.argv.slice(2)
const getArg = (name) => { const i = args.indexOf('--' + name); return i >= 0 ? args[i + 1] : undefined }
const hasFlag = (name) => args.includes('--' + name)

const subjectArg = getArg('subject')
const countArg = getArg('count')
const count = parseInt(countArg || '5', 10)
const totalArg = parseInt(getArg('total') || '15', 10)
const output = getArg('output')
const levelArg = getArg('level') || '全部'
const openExplicit = hasFlag('open')   /* 旧 --closed 已废弃：现在默认就是折叠 */
const grouped = hasFlag('grouped')
const plain = hasFlag('plain')
/* 提取练习：答案默认折叠 —— 先逼自己回想 30 秒，再展开照抄。
   --open 显式要求默认展开（例如临睡前纯抄写、不带脑子过一遍时用）。 */
const openFlag = openExplicit ? ' open' : ''

// ============ 题库源（bank key -> 解析方式） ============
const BANKS = {
  /* —— 零基础扫盲层：看板头号缺口是「符号盲区」，现有三个题库全部默认已识字 —— */
  '高数扫盲': { file: '资料/零基础扫盲题库.md', type: 'short', part: 1, subject: '高等数学' },
  'C语言扫盲': { file: '资料/零基础扫盲题库.md', type: 'short', part: 2, subject: 'C语言' },
  /* —— 计算与编程主战场（广东专升本计算机类 = 高数 + C语言 + 数据结构） —— */
  '高数': { file: '资料/高数计算题专项训练.md', type: 'calc', subject: '高等数学' },
  'C语言考点': { file: 'docs/posts/computer/notes/3.1-高频考点强化练习.md', type: 'cnChoice', subject: 'C语言' },
  'C语言编程': { file: 'docs/posts/computer/notes/3.4-循环与数组综合编程专项.md', type: 'tProg', subject: 'C语言' },
  'C语言改错': { file: 'docs/posts/computer/notes/3.0-改错题专项训练.md', type: 'fixErr', subject: 'C语言' },
  '计算机同型': { file: 'docs/posts/computer/notes/3.2-更多同型练习题.md', type: 'numChoice', subject: '计算机' },
  '简答': { file: '资料/高频简答题库.md', type: 'short', subject: '计算机' },
  /* —— 真题：2018–2026 计算机真题（单选 + 判断），带考点 ——
     这是**唯一覆盖数据结构 2.x 全章**的题源（树/图/查找/排序），别删。 */
  '计算机真题': {
    files: [
      '历年真题/计算机程序设计/2021.md',
      '历年真题/计算机程序设计/2022.md',
      '历年真题/计算机程序设计/2024.md',
      'docs/posts/computer/2025-真题回忆版.md',
      'docs/posts/computer/2026-回忆版详解.md',
    ],
    type: 'examChoice',
    subject: '计算机',
  },
  /* —— 记忆类 —— */
  '政治': { file: '资料/政治选择题题库.md', type: 'choice', subject: '政治' },
}

const LV = { 基础: 1, 中档: 2, 拔高: 3 }
const STARS = { 1: '★', 2: '★★', 3: '★★★' }
const LVNAME = { 1: '基础', 2: '中档', 3: '拔高' }

/* ---- 难度关键词表（判据全部来自题库自带的「考点」括号 / Part 名，不额外造标签） ---- */
const MATH_HARD = /二重积分|极坐标|换序|幂级数|泰勒|拉格朗日|柯西|弧长|旋转体|综合|第二类换元|递推|不等式证明|隐函数|参数方程/
const MATH_EASY = /抓大头|直接代入|约分|等价无穷小|两个重要极限|基本极限|定义域|幂函数求导|求导公式|直接积分|基本公式|四则运算|复合函数求导/
const CS_HARD = /二叉树|图|哈希|KMP|复杂|时间复杂度|空间复杂度|建树|遍历序列|排序稳定性/
const CS_EASY = /sizeof|strlen|运算符|三目|整数除法|取余|自增|自减|选择结构|输入输出|数据类型|常量|变量|关键字/

function mathLevel(topic, kaodian) {
  const s = (topic || '') + ' ' + (kaodian || '')
  if (MATH_HARD.test(s)) return LV.拔高
  if (MATH_EASY.test(s)) return LV.基础
  return LV.中档
}
function csLevel(text, subjectName) {
  const s = (subjectName || '') + ' ' + (text || '')
  if (CS_HARD.test(s)) return LV.中档
  if (CS_EASY.test(s)) return LV.基础
  return LV.中档
}

// ============ 通用工具 ============
const norm = (c) => c.replace(/\r\n/g, '\n')
const clean = (s) => String(s || '').replace(/\n{3,}/g, '\n\n').trim()

/** 判断一段是不是「只有考点、没有解析」。
    ★ 判断题的答案行尾常跟一个考点链接，**真解析在它下面一段**：
        **答案：√** · [[2.2 线性表]]
        <空行>
        线性表基本特性（首元无前驱，末元无后继）。
    只取「答案行后的第一段」→ 解析变成考点名（实测 2024 判断题 10/10 中招）。 */
function isPointNoise(p) {
  const s = String(p || '')
    .replace(/\[\[[^\]]*\]\]/g, '')
    .replace(/\[[^\]]*\]\([^)]*\)/g, '')
    .replace(/考点\s*\*\*[^*]*\*\*/g, '')
    .replace(/考点/g, '')
    .replace(/[·|>#*\s:：]/g, '')
  return s.length === 0
}

/* 从 block 里抽 `> **xxx**：yyy` 引用行（题库里解析/错误/易错都是这个格式） */
function quotes(block) {
  const out = []
  const re = /^>\s*\*\*([^*]+?)\*\*\s*[：:]*\s*([\s\S]*?)(?=\n>\s*\*\*|\n(?![>\s])|$)/gm
  let m
  while ((m = re.exec(block))) {
    const k = m[1].trim()
    let v = m[2].trim()
    /* 去掉行内残留的 "> " 引用符号 */
    v = v.replace(/^>[\s]*/gm, '').replace(/^>\s*$/gm, '').trim()
    if (k && v) out.push({ k, v })
  }
  return out
}

function pickQuote(qs, kw) { return qs.filter(q => new RegExp(kw).test(q.k)).map(q => q.v).join('\n\n') }

// ============ 解析器 ============
/** 政治选择题题库：`**单选题 Q1.**` / `**单选题 Q91.（模拟）**` + `> **答案**：C` + `> **解析**：…` */
function parseChoice(content) {
  const blocks = norm(content).split(/(?=\*\*(?:单选|多选)题 Q\d+\.)/)
  const items = []
  for (const b of blocks) {
    const m = b.match(/^\*\*(单选|多选)题 Q(\d+)\.(（[^）]*）)?\*\*(.*?)(?=\n> \*\*答案)/s)
    if (!m) continue
    const qs = quotes(b.slice(b.indexOf('> **答案')))
    const sim = !!m[3]
    items.push({
      q: clean(m[4]),
      stemLabel: m[1],
      ans: (b.match(/> \*\*答案\*\*：([A-D]+)/) || [])[1] || '?',
      explain: pickQuote(qs, '解析'),
      level: sim ? LV.拔高 : (m[1] === '多选' ? LV.中档 : LV.基础),
      levelNote: sim ? '时政模拟' : '',
    })
  }
  return items
}

/** 高数计算题：`### 计算题 #1（考点）` + `**题目**：` + `**解**：…` + `**考点**：…` */
function parseCalc(content) {
  const text = norm(content)
  /* 章节位置用于兜底定级 */
  const chapterAt = (idx) => [...text.slice(0, idx).matchAll(/##\s*第([一二三四五六七八九十]+)章/g)].length
  const re = /###\s*计算题 #(\d+)（(.+?)）\n\n\*\*题目\*\*：([\s\S]*?)(?=\n\*\*解\*\*)/g
  const items = []
  let m
  while ((m = re.exec(text))) {
    const tail = text.slice(m.index)
    const sol = tail.match(/\*\*解\*\*：\n([\s\S]*?)(?=\n\*\*考点\*\*：|\n###\s*计算题|\n---\s*$)/)
    const kp = tail.match(/\*\*考点\*\*：(.+)/)
    const topic = m[2]
    let level = mathLevel(topic, kp && kp[1])
    if (level === LV.中档 && chapterAt(m.index) <= 1 && +m[1] <= 8) level = LV.基础
    items.push({
      q: clean(m[3]),
      topic,
      solution: clean(sol && sol[1]),
      kaodian: kp ? kp[1].trim() : '',
      level,
    })
  }
  return items
}

/**
 * 简答题库 / 零基础扫盲题库：`**Q1** 问题` + `**A1**` + 答案正文，`---` 分隔。
 * 旧版按 `\d+\.\s` 抓"编号行"，会把答案里的 `1. **有穷性**：…` 当成题目 —— 本版修掉。
 * opts.part：只取指定 `## Part N` 段（扫盲题库 Part 1=高数符号，Part 2=C语言符号）。
 */
function parseShort(content, opts = {}) {
  const text = norm(content)
  /* Part 头的归属必须按「Q 的位置」判定，不能看 chunk 里有没有头：
     下一个 Part 的标题常紧跟在上一 Part 最后一题的答案后面，会被切进同一个 chunk。 */
  const marks = [...text.matchAll(/##\s*Part\s*(\d+)[：:]\s*(.+?)（/g)]
    .map(m => ({ at: m.index, no: +m[1], name: m[2].trim() }))
  const partAt = (idx) => {
    let cur = { no: 0, name: '' }
    for (const m of marks) { if (m.at <= idx) cur = m; else break }
    return cur
  }
  const items = []
  /* lookahead split 不丢字符，故按 chunk 长度累加即可还原其在原文的精确起点 */
  const chunks = text.split(/(?=\*\*Q\d+\*\*)/)
  let at = 0
  for (const c of chunks) {
    const pos = at
    at += c.length
    const qm = c.match(/^\*\*Q(\d+)\*\*\s*(.+)/)
    if (!qm) continue
    const { no: partNo, name: partName } = partAt(pos)
    if (opts.part && partNo !== opts.part) continue
    const am = c.match(new RegExp(`\\*\\*A${qm[1]}\\*\\*\\s*\\n([\\s\\S]*?)(?=\\n---\\s*\\n|\\n\\*\\*Q\\d+\\*\\*|$)`))
    const sol = clean(am && am[1])
    items.push({
      q: qm[2].trim(),
      sub: opts.part ? '' : partName,   /* 指定 part 时该信息冗余，不再显示 */
      solution: sol,
      explain: '',
      level: sol.length <= 220 ? LV.基础 : LV.中档,
    })
  }
  return items
}

/**
 * 3.1 高频考点强化练习：`### 考点 N：名称（考频 ★★★★★）` + `**题 N**：题干` + `> **答案：B**` + `> **解析**：…`
 * 题号在每个考点内重新从 1 开始，所以必须带考点上下文。
 */
function parseCnChoice(content) {
  const text = norm(content)
  let topic = '', freq = 0
  const items = []
  for (const c of text.split(/(?=\*\*题 \d+\*\*)/)) {
    const km = c.match(/###\s*考点\s*\d+[：:]\s*(.+?)（考频\s*([★]+)/)
    if (km) { topic = km[1].trim(); freq = (km[2] || '').length }
    const qm = c.match(/^\*\*题\s*(\d+)\*\*[：:]\s*([\s\S]*?)(?=\n> \*\*答案)/)
    if (!qm) continue
    const qs = quotes(c.slice(c.indexOf('> **答案')))
    items.push({
      q: clean(qm[2]),
      topic,
      ans: (c.match(/\*\*答案[：:]\s*([A-D]+)/) || [])[1] || '?',
      explain: pickQuote(qs, '解析'),
      /* 数据结构类考点整体高于 C 语言基础考点；考频只影响"要不要多练"，不影响难度 */
      level: csLevel(topic, topic),
    })
  }
  return items
}

/**
 * 3.2 更多同型练习题：`## C 语言部分` / `## 数据结构部分` + `### 12. 题干` + `> **答案：D**` + `> **解析：**` + `> **💡 秒懂技巧：**`
 * 末尾有「## 答案速查」表，必须跳过，否则会把速查行当题目。
 */
function parseNumChoice(content) {
  const text = norm(content)
  let sec = ''
  const items = []
  for (const c of text.split(/(?=###\s*\d+\.\s)/)) {
    const sm = c.match(/##\s*(C 语言部分|数据结构部分)/)
    if (sm) sec = sm[1].replace(/\s+/g, '')
    if (/^##\s*答案速查/.test(c) || sec === '' && !c.match(/^###\s*\d+\./)) continue
    const qm = c.match(/^###\s*(\d+)\.\s*(.+?)(?=\n> \*\*答案)/s)
    if (!qm) continue
    const body = c.slice(c.indexOf('> **答案'))
    const qs = quotes(body)
    items.push({
      q: clean(qm[2]),
      sub: sec,
      topic: sec,
      ans: (c.match(/\*\*答案[：:]\s*([A-D]+)/) || [])[1] || '?',
      explain: [pickQuote(qs, '解析'), pickQuote(qs, '秒懂技巧')].filter(Boolean).join('\n\n'),
      level: /数据结构/.test(sec) ? LV.中档 : LV.基础,
    })
  }
  return items.filter(it => it.q)
}

/**
 * 计算机真题（`历年真题/计算机程序设计/*.md`、`docs/posts/computer/*.md`）：
 *   `### N. 题干（ ）`
 *   `A. x  B. y  C. z  D. w`（也可能每行一个）
 *   `**答案：B** · 考点 [[1.2 数据的存储与运算]]`
 *   `**解析**：…`
 * 判断题长这样：`**答案：√**`（无 A/B/C/D）。
 *
 * ⚠️ 这个格式跟其它题库不同 —— 别的题库答案是引用行 `> **答案**：C`，
 *    真题是**行内加粗** `**答案：B**`，所以必须单独一个解析器。
 */
function parseExamChoice(content) {
  const text = norm(content)
  const items = []
  for (const c of text.split(/(?=###\s*\d+\.\s)/)) {
    if (!/^###\s*\d+\.\s/.test(c)) continue
    const blk = c.split(/\n##(?!#)/)[0]          // 不跨 ## 小节
    const am = blk.match(/\*\*答案[：:]\s*(.+?)\*\*/)
    if (!am) continue
    const raw = am[1].trim()
    const isTF = /^[√×对错]$/.test(raw)
    if (!isTF && !/^[A-Da-d]$/.test(raw)) continue

    const qm = blk.match(/^###\s*\d+\.\s*([^\n]+)/)
    if (!qm) continue
    const head = blk.slice(blk.indexOf('\n') + 1, am.index)

    let optText = ''
    const inline = head.match(
      /A\s*[\.、:：]\s*(.+?)\s+B\s*[\.、:：]\s*(.+?)\s+C\s*[\.、:：]\s*(.+?)\s+D\s*[\.、:：]\s*(.+?)\s*$/m)
    if (inline) {
      optText = ['A', 'B', 'C', 'D'].map((L, i) => `${L}. ${inline[i + 1].trim()}`).join('　')
    } else {
      optText = head.split('\n').filter(l => /^\s*[A-D]\s*[\.、:：]/.test(l)).map(l => l.trim()).join('\n')
    }

    const pm = blk.match(/\[\[([^\]|]+)/) || blk.match(/\[([^\]]+)\]\([^)]*\)/)
    const topic = pm ? pm[1].trim() : ''
    /* ★ 解析标记有两种写法：`**解析**：` 和 `**解析**（下标 0…6，已升序）：`
       —— 括号可能在冒号前面，只认冒号会漏掉一大批。
       终止条件用 `---` / 下一个 `###`，并**保留换行**（解析常有编号步骤）。 */
    const em = blk.match(/\*\*解析\*\*\s*(?:（[^）]*）)?\s*[：:]?\s*([\s\S]*?)(?=\n---|\n#{2,4}\s|$)/)
    /* 判断题常没有 `**解析**` 标记，解析就是答案行之后的正文。
       ★ 但答案行里带 `· 考点 [[1.2 …]]`（站点副本用的是 `[1.2 …](url)`），
         必须先把这段剥掉，否则它会跑进解析里变成第一段。 */
    /* 判断题常没有 `**解析**` 标记，解析就是答案行之后的正文。
       ★ 但答案行里带 `· 考点 [[1.2 …]]`（站点副本用的是 `[1.2 …](url)`），
         而且**它自成一段，真解析在下一段** —— 逐段跳过「纯考点/纯链接」段，
         取第一段有实质内容的。只取第一段会让解析变成考点名。 */
    let explain = em ? clean(em[1]) : ''
    if (!explain) {
      const tail = blk.slice(am.index + am[0].length)
      for (const p of tail.split(/\n\s*\n/)) {
        if (isPointNoise(p)) continue
        const cand = clean(p)
        if (cand.length > 3) { explain = cand; break }
      }
    }

    const stem = clean(qm[1])
    items.push({
      q: clean(stem + (optText ? '\n\n' + optText : '')),
      sub: topic,
      topic,
      ans: isTF ? (raw === '√' || raw === '对' ? '对' : '错') : raw.toUpperCase(),
      explain,
      level: csLevel(stem + ' ' + topic, '计算机'),
    })
  }
  return items.filter(it => it.q && it.q.length < 400)
}

/**
 * 3.4 循环与数组综合编程专项：`## ② 基础层` / `③ 数组核心层` / `④ 真题同型层` + `### T1 标题`
 *   + 代码 + `> **答案：2550**` / `> **答案**：…` + `> **解析**：` + `> **易错**：`
 * 分层标题直接就是难度，不需要猜。
 */
function parseTProg(content) {
  const text = norm(content)
  let layer = LV.中档
  const items = []
  for (const c of text.split(/(?=###\s*T\d+\s)/)) {
    const hm = c.match(/##\s*[①②③④⑤]\s*(.+?)（/)
    if (hm) {
      const h = hm[1]
      layer = /基础/.test(h) ? LV.基础 : /真题|综合/.test(h) ? LV.拔高 : LV.中档
    }
    const qm = c.match(/^###\s*T(\d+)\s+(.+?)\n([\s\S]*?)(?=\n> \*\*答案|$)/)
    if (!qm) continue
    const body = c.slice(c.indexOf('> **答案'))
    const qs = quotes(body)
    const ansLine = c.match(/\*\*答案[：:]\*\*?\s*([^\n]+)/) || c.match(/\*\*答案\*\*[：:]\s*([^\n]+)/)
    items.push({
      q: clean(qm[2] + '\n\n' + qm[3]),
      topic: '编程题',
      ans: ansLine ? ansLine[1].trim() : '见下方完整解答',
      solution: '',
      explain: [pickQuote(qs, '解析'), pickQuote(qs, '易错')].filter(Boolean).join('\n\n'),
      level: layer,
    })
  }
  return items
}

/**
 * 3.0 改错题专项：`### 题 N：标题` + 错误代码 + `> **错误 1**：…` + `> **解析**：…`
 * 答案是「怎么改」，必须原样带出，否则用户看不出自己错在哪。
 */
function parseFixErr(content) {
  const text = norm(content)
  const items = []
  for (const c of text.split(/(?=###\s*题\s*\d+[：:])/)) {
    /* 答案锚点有两种写法：引用块 `> **错误 N**：`（题1-15）或 <details> 内的 `**错误 N**：`/`**答案：X**`（题16-17） */
    const qm = c.match(/^###\s*题\s*(\d+)[：:]\s*(.+?)\n([\s\S]*?)(?=\n> \*\*错误|\n> \*\*参考|\n<details>)/)
    if (!qm) continue
    const anchor = ['> **错误', '> **参考', '<details>'].map(s => c.indexOf(s)).filter(i => i >= 0)
    if (!anchor.length) continue
    const body = c.slice(Math.min(...anchor))
    const qs = quotes(body)
    const fixes = qs.filter(q => /错误/.test(q.k)).map(q => q.v)
    /* <details> 版：整块原样带出，去掉 HTML 壳 */
    const det = body.match(/<details>[\s\S]*?<\/summary>([\s\S]*?)<\/details>/)
    const detTxt = !fixes.length && det
      ? det[1].replace(/^\*\*答案[：:]\s*([A-D])\*\*/m, (_, a) => `**答案**：$1`).trim() : ''
    items.push({
      q: clean(qm[2] + (det && /（　　）/.test(qm[3]) ? '' : '（找出并改正下面代码中的错误）') + '\n\n' + qm[3]),
      topic: '改错题',
      ans: fixes.length ? fixes.join('\n') : (detTxt ? '见下方完整解答' : '见下方完整解答'),
      solution: fixes.length ? '' : detTxt,
      explain: [pickQuote(qs, '解析'), pickQuote(qs, '参考')].filter(Boolean).join('\n\n'),
      level: +qm[1] <= 6 ? LV.基础 : +qm[1] <= 15 ? LV.中档 : LV.拔高,
    })
  }
  return items
}

const PARSERS = {
  choice: parseChoice,
  calc: parseCalc,
  short: parseShort,
  cnChoice: parseCnChoice,
  numChoice: parseNumChoice,
  tProg: parseTProg,
  fixErr: parseFixErr,
  examChoice: parseExamChoice,
}

function loadBank(key) {
  const bank = BANKS[key]
  /* 一个题库可以由多个文件拼成（真题按年份分文件） */
  const fileList = bank.files || [bank.file]
  const items = []
  let found = 0
  for (const rel of fileList) {
    const file = join(ROOT, rel)
    if (!existsSync(file)) continue
    found++
    const content = readFileSync(file, 'utf-8')
    for (const it of PARSERS[bank.type](content, { part: bank.part })) {
      it.bank = key
      it.subject = bank.subject || key
      items.push(it)
    }
  }
  /* 同年真题在两个目录各有一份，按题干去重 */
  const seen = new Set()
  const uniq = items.filter(it => {
    const k = it.q.replace(/\s/g, '').slice(0, 60)
    if (seen.has(k)) return false
    seen.add(k)
    return true
  })
  return { key, items: uniq, missing: found === 0, file: fileList.join(' + ') }
}

// ============ 抽题（随机分布的核心） ============
function shuffle(a) {
  const x = [...a]
  for (let i = x.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[x[i], x[j]] = [x[j], x[i]]
  }
  return x
}

/** 按难度配比从 items 抽 n 道；某档不够就按 基础->中档->拔高 借，保证题量不缩水 */
function pickByRatio(items, n, ratio) {
  const buckets = { 1: [], 2: [], 3: [] }
  for (const it of items) (buckets[it.level] || buckets[2]).push(it)
  for (const k of Object.keys(buckets)) buckets[k] = shuffle(buckets[k])
  const wSum = ratio.reduce((s, x) => s + x, 0) || 1
  const quota = ratio.map(w => Math.floor(n * w / wSum))
  let short = n - quota.reduce((s, x) => s + x, 0)
  for (let i = 0; i < 3 && short > 0; i++) if (ratio[i] > 0) { quota[i]++; short-- }
  const out = []
  for (let lvl = 1; lvl <= 3; lvl++) {
    let want = quota[lvl - 1]
    while (want-- > 0 && buckets[lvl].length) out.push(buckets[lvl].pop())
  }
  let deficit = n - out.length
  for (let lvl = 1; lvl <= 3 && deficit > 0; lvl++)
    while (deficit > 0 && buckets[lvl].length) { out.push(buckets[lvl].pop()); deficit-- }
  return out
}

/** ★ 轨道（考试科目）判定。
    为什么要它：`计算机真题` 是唯一覆盖数据结构 2.x 全章的题源，但它只占
    113 题里的 34，且多为中档/拔高 —— 在 6:3:1 配比下几乎抽不到。
    实测（15 次 × 15 题 = 225 题）：数据结构只出现 **1 次 = 0.4%**，
    而它是整整一门考试科目（看板进度 0%）。按源分配权重解决不了这个问题 ——
    必须按「科目轨道」兜底，否则源再多也轮不到它。 */
function trackOf(it) {
  const t = it.topic || ''
  if (/^2\./.test(t)) return '数据结构'
  if (it.subject === '高等数学') return '高数'
  if (it.subject === '政治') return '政治'
  if (/^1\./.test(t)) return 'C语言'
  if (it.subject === 'C语言') return 'C语言'
  if (/数据结构|线性表|栈|队列|串|二叉树|树|图|查找|排序|算法/.test(t)) return '数据结构'
  return '综合'
}

/** 轨道下限：**只做「替换」，不改总题数**。
    某轨道不足下限时，从该轨道取还没被选的题，替换掉「当前题量最多的源」里的一张。
    牺牲者排除两处：本轨道已有的题、以及新题所在源（否则会把刚补进去的又换出来）。 */
function applyTrackFloor(picked, usable, total) {
  const floor = Math.max(1, Math.round(total * 0.15))
  for (const [track, min] of Object.entries({ 数据结构: floor })) {
    let got = picked.filter(it => trackOf(it) === track).length
    if (got >= min) continue
    const chosen = new Set(picked)
    const cands = []
    for (const l of usable) for (const it of l.items)
      if (trackOf(it) === track && !chosen.has(it)) cands.push(it)
    if (!cands.length) continue
    shuffle(cands)
    while (got < min && cands.length) {
      const next = cands.pop()
      const cnt = {}
      for (const it of picked) cnt[it.bank] = (cnt[it.bank] || 0) + 1
      let victim = null, best = -1
      for (const it of picked) {
        if (trackOf(it) === track) continue
        if (it.bank === next.bank) continue
        if (cnt[it.bank] > best) { best = cnt[it.bank]; victim = it }
      }
      if (!victim) break
      picked.splice(picked.indexOf(victim), 1, next)
      got++
    }
  }
  return picked
}

/** 源权重：广东专升本计算机类 = 高数 + C 语言 + 数据结构 是主战场，政治/简答是记忆类副科。
    随机分布不是平均分布 —— 平均会让一半题量落在背诵科，与「数计优先」的备考策略相反。 */
const BANK_WEIGHT = {
  '高数': 3, '高数扫盲': 2,
  'C语言编程': 3, 'C语言考点': 2, 'C语言改错': 2, 'C语言扫盲': 2,
  '计算机同型': 2, '简答': 1, '政治': 1,
}

/** 把 total 道题随机分配到各源：先每源保底 1 题，余量按"加权轮盘随机"分，保证每次分布不同 */
function distribute(total, keys) {
  const alloc = Object.fromEntries(keys.map(k => [k, 0]))
  if (!keys.length) return alloc
  let left = total
  /* 保底：每源 1 题（不超过 total） */
  for (const k of shuffle(keys)) { if (left <= 0) break; alloc[k] = 1; left-- }
  /* 余量按权重轮盘：权重越高的源越容易抽到，但仍有随机性 */
  const bag = []
  for (const k of keys) for (let i = 0; i < (BANK_WEIGHT[k] || 1); i++) bag.push(k)
  const cap = { 高数: 6, 'C语言编程': 5 }   /* 大题库可以多堆；小源不超 4 */
  let guard = 0
  while (left > 0 && guard++ < 20000) {
    const k = bag[Math.floor(Math.random() * bag.length)]
    if (alloc[k] >= (cap[k] || 4)) continue   /* 单源上限，避免全堆一科 */
    alloc[k]++; left--
  }
  /* 若因单源上限没分完：放宽上限，但每次补「当前题量最少」的源（同分则随机），
     避免旧写法 keys[left % keys.length] 反复补同一批源造成的分布偏置。 */
  while (left > 0) {
    const min = Math.min(...keys.map((k) => alloc[k]))
    const cands = keys.filter((k) => alloc[k] === min)
    alloc[cands[Math.floor(Math.random() * cands.length)]]++
    left--
  }
  return alloc
}

// ============ 渲染 ============
function render(it, idx) {
  const L = []
  const tag = it.levelNote ? `${LVNAME[it.level]}·${it.levelNote}` : LVNAME[it.level]
  const head = `### ${idx + 1}. 【${it.subject}】${it.topic ? `【${it.topic}】` : ''}${it.sub && it.sub !== it.topic ? `【${it.sub}】` : ''} ${STARS[it.level]} ${tag}`
  L.push(head, '', it.q, '')
  /* 先给"30 秒提示"再给解答，避免一眼看到答案 */
  const hints = hint(it)
  /* 答案默认折叠后，必须在折叠块外留一句行动指令，否则会「点开只见题干不知做什么」。 */
  const peek = openFlag ? '' : '　👉 想满 30 秒还不动，就展开下面的解答照抄一遍，合上再默写。'
  L.push(`> 🧭 **先想 30 秒**：${hints || '先别看答案，用自己的话说一遍这题要考什么。'}${peek}`, '')
  const ans = []
  if (it.ans && it.ans !== '见下方完整解答' && !it.solution) {
    ans.push(`**答案**：${it.ans}`, '')
  }
  if (it.solution) ans.push('**完整解答（照着抄一遍，然后合上默写）**：', '', it.solution, '')
  if (it.explain) ans.push('**解析**：', '', it.explain, '')
  if (it.kaodian) ans.push('**这题在考什么**：', '', it.kaodian, '')
  if (!ans.length) ans.push(`**答案**：${it.ans || '?'}`, '')
  /* 统一用 <details> 承载答案：GitHub / VitePress 里折叠好看，
     门户靠 details 边界把「题干」和「完整讲解」切开（--open 时默认展开，便于照抄）。 */
  if (plain) L.push(...ans, '---', '')
  else L.push(`<details${openFlag}>`, '<summary>💡 看完整解答与讲解</summary>', '', ...ans, '', '</details>', '')
  return L
}

/* 不剧透式提示：只说"这题要你调用哪个概念" */
function hint(it) {
  const s = (it.topic || '') + ' ' + (it.kaodian || '') + ' ' + (it.q || '')
  if (it.level === LV.基础) return '这题是基础题，直接照抄解答再默写一遍即可。'
  if (/极限|lim/.test(s)) return '先辨认符号：x 在往哪儿靠？是 0/0 还是 ∞/∞ 型？'
  if (/积分/.test(s)) return '先问自己：这是求导的逆运算，能不能直接套基本积分表？'
  if (/导/.test(s)) return '先写出要用哪条求导公式，再动手算。'
  if (/改错/.test(s)) return '逐行只查四件事：分号、== 与 =、scanf 的 &、数组下标越界。'
  if (/编程|循环|数组/.test(s)) return '先默写最小框架 #include + int main + return 0，再往里填循环。'
  if (/数据结构/.test(s) || /二叉树|栈|队列|排序|哈希/.test(s)) return '先在草稿上画出结构，再算 —— 这科靠画不靠想。'
  if (/多选|单选/.test(it.subject) || /^[A-D]\./.test(it.q)) return '先排除明显错的两个选项，再在剩下的里二选一。'
  return '这题不用算，只需要把概念用自己的话说一遍。'
}

// ============ --list ============
if (args.includes('--list')) {
  console.log('📚 题库源题量与难度分布：')
  let sum = 0
  for (const key of Object.keys(BANKS)) {
    const { items, missing, file } = loadBank(key)
    if (missing) { console.log(`  ${key.padEnd(12)} ⚠️ 文件不存在 ${file}`); continue }
    const d = { 1: 0, 2: 0, 3: 0 }
    for (const it of items) d[it.level]++
    const noSol = items.filter(i => !i.solution && !i.explain && (!i.ans || i.ans === '?' )).length
    sum += items.length
    console.log(`  ${key.padEnd(12)} ${String(items.length).padStart(4)} 题  基础${String(d[1]).padStart(4)} 中档${String(d[2]).padStart(4)} 拔高${String(d[3]).padStart(3)}${noSol ? `  ⚠️${noSol} 题缺解答` : ''}   ← ${BANKS[key].file}`)
  }
  console.log(`  ${'合计'.padEnd(11)} ${sum} 题`)
  console.log('  参数：--total 15  --level 基础|中档|拔高|全部  --ratio 6,3,1  --grouped  --open')
  process.exit(0)
}

// ============ 主流程 ============
let ratio = [6, 3, 1]
const rArg = getArg('ratio')
if (rArg) {
  const r = rArg.split(',').map(x => parseInt(x, 10))
  if (r.length === 3 && r.every(x => !Number.isNaN(x))) ratio = r
}
if (levelArg !== '全部') {
  const only = LV[levelArg]
  if (!only) { console.error(`未知难度：${levelArg}（可选 基础/中档/拔高/全部）`); process.exit(2) }
  ratio = [0, 0, 0]; ratio[only - 1] = 1
}

const keys = subjectArg ? [subjectArg] : Object.keys(BANKS)
if (subjectArg && !BANKS[subjectArg]) {
  console.error(`未知题库源：${subjectArg}\n可选：${Object.keys(BANKS).join(' / ')}`)
  process.exit(2)
}

const loaded = []
for (const k of keys) {
  const { items, missing } = loadBank(k)
  if (missing || !items.length) { loaded.push({ key: k, items: [], bad: true }); continue }
  loaded.push({ key: k, items })
}
const usable = loaded.filter(l => !l.bad)

/* 抽题：--count 走"每源 N 题"旧语义，否则走"总量随机分布" */
let picked = []
if (countArg) {
  for (const l of usable) picked.push(...pickByRatio(l.items, Math.min(count, l.items.length), ratio))
} else {
  const alloc = distribute(totalArg, usable.map(l => l.key))
  for (const l of usable) {
    const n = Math.min(alloc[l.key], l.items.length)
    if (n > 0) picked.push(...pickByRatio(l.items, n, ratio))
  }
}
/* ★ 轨道兜底：保证数据结构这类「真题里有题、但按配比抽不到」的科目每天必出。
   放在交错之前，且只替换不改数量。 */
applyTrackFloor(picked, usable, countArg ? picked.length : totalArg)

/* 科目交错：默认打散（除非 --grouped 按源分块） */
if (!grouped) picked = shuffle(picked)

const today = new Date()
const p2 = (n) => String(n).padStart(2, '0')
const dateStr = `${today.getFullYear()}-${p2(today.getMonth() + 1)}-${p2(today.getDate())}`
const d = { 1: 0, 2: 0, 3: 0 }
for (const it of picked) d[it.level]++
const subjCount = {}
for (const it of picked) subjCount[it.subject] = (subjCount[it.subject] || 0) + 1

const lines = [
  `# 📅 每日刷题计划 · ${dateStr}`,
  '',
  `> 由 \`scripts/daily-drill.mjs\` 生成。共 **${picked.length}** 题：基础 ${d[1]} / 中档 ${d[2]} / 拔高 ${d[3]}。`,
  `> 难度配比 基础:中档:拔高 = ${ratio.join(':')}${levelArg !== '全部' ? `（锁定「${levelArg}」）` : ''}，题库与顺序随机${grouped ? '（按源分块）' : '（科目交错混排）'}。`,
  '> **零基础正确用法**：读题 → 想 30 秒 → **照抄完整解答 → 合上默写一遍**。做不出来是正常的，不要硬憋，也不要因为不会就跳过。',
  '',
]

if (grouped) {
  for (const l of usable) {
    const mine = picked.filter(it => it.bank === l.key)
    if (!mine.length) continue
    lines.push(`## ${l.key}（${mine.length} 题）`, '')
    mine.forEach((it, i) => lines.push(...render(it, i)))
  }
} else {
  /* 交错输出：只按题号平铺，科目在标题里 */
  picked.forEach((it, i) => lines.push(...render(it, i)))
}
lines.push(`> 分布：${Object.entries(subjCount).map(([k, v]) => `${k} ${v}`).join(' · ')}`)
lines.push('', `共 ${picked.length} 题。错题登记：docs/checklists/错题本模板.md`,
  `重抽一次（换题）：node scripts/daily-drill.mjs --total ${picked.length}`)

const out = output ? join(ROOT, output) : join(ROOT, 'plan', `每日刷题-${dateStr}.md`)
if (!IS_MAIN) {
  /* 被 import（调试）：只算不写，绝不碰当天的计划文件 */
  console.error('[import 模式] 未写文件。要生成计划请直接执行本脚本。')
} else {
  writeFileSync(out, lines.join('\n'), 'utf-8')
  console.log(`✅ 已生成：${out}`)
  console.log(`   ${picked.length} 题（基础${d[1]}/中档${d[2]}/拔高${d[3]}）｜ ${Object.entries(subjCount).map(([k, v]) => k + v).join(' ')}｜ 缺解答 ${picked.filter(i => !i.solution && !i.explain && (!i.ans || i.ans === '?')).length} 题`)
}
