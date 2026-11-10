#!/usr/bin/env node
/**
 * 同步 docs/index.md 里**两处会自动过期**的内容：
 *   ① 「本站有什么」表格里的数字（`<!-- STATS:START -->` / `<!-- STATS:END -->`）；
 *   ② 顶部横幅的「内容更新至 X」（`<!-- DATE:START -->` / `<!-- DATE:END -->`）。
 *
 * ★ 为什么需要它：这些东西原来是手写的，内容一长就过期。
 *   2026-09-20 审计实测三处全错：
 *     高数写「50+ 章节」→ 实际 69 篇
 *     计算机写「20 篇知识点」→ 实际 37 篇
 *     英语写「2008–2024 / 17 年」→ 实际 2005–2025 / 21 年
 *   而且审计当天下午就有人在往计算机笔记里加文件 —— 手写数字**必然**漂移。
 *   所以这里不再「改对一次」，而是让它可重新生成。
 *
 *   ★ 2026-10-05 加 ②：横幅的日期从 2026-09-21 起就没人动过，**落后了半个月**。
 *     现在由 `content-dates.mjs` 按 git 提交时间自动算（与 `/updates/` 页同源）。
 *     注意**首页自身被排除在日期计算之外**（`latestContentDateForHome`）——
 *     否则「改一次横幅」就会把日期顶到今天，变成自指。
 *
 * 用法：
 *   node scripts/sync-home-stats.mjs            # 重写两处
 *   node scripts/sync-home-stats.mjs --check    # 只校验；过期则退出码 1
 *
 * 设计约束：
 *   ① 只改标记之间的内容，正文其余部分一个字节不动；
 *   ② 「真题 / 同型演练」的区分**只依据文件自身的标签**（前 30 行里的
 *      「同型演练」），不猜、不按文件名推断。标签没有的年份就不声称；
 *   ③ 排除「黄金知识汇编」「备考指南」这类带年份但非试卷的文件。
 */
import { readdirSync, readFileSync, writeFileSync } from 'node:fs'
import { join, dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { latestContentDateForHome } from './content-dates.mjs'

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const DOCS = join(ROOT, 'docs')
const INDEX = join(DOCS, 'index.md')
const CHECK = process.argv.includes('--check')

const START = '<!-- STATS:START -->'
const END = '<!-- STATS:END -->'
const DATE_START = '<!-- DATE:START -->'
const DATE_END = '<!-- DATE:END -->'

// ── 笔记篇数：目录 → 需要排除的 meta / 审计产物 ────────────────────────
const NOTE_DIRS = [
  {
    label: '高数章节笔记', route: '/posts/math/notes/',
    dir: 'docs/posts/math/notes',
    exclude: /^(index|syllabus)\.md$|^2025-真题回忆版\.md$/,
    note: '（第 9–11 章为部分收录）',
    source: '`高等数学/`',
  },
  {
    label: '计算机知识点', route: '/posts/computer/notes/',
    dir: 'docs/posts/computer/notes',
    exclude: /^(index|syllabus)\.md$|^audit-|^pengge-|^全书索引目录\.md$|^真题考点分布\.md$|^高频错题汇总\.md$/,
    note: '',
    source: '本站原创',
  },
  {
    label: '政治系统笔记', route: '/posts/politics/notes/',
    dir: 'docs/posts/politics/notes',
    exclude: /^index\.md$|^真题-政治历年/,
    unit: '个模块',
    note: '',
    source: '`政治理论/`',
  },
  {
    label: '英语系统笔记', route: '/posts/english/notes/',
    dir: 'docs/posts/english/notes',
    exclude: /^index\.md$/,
    note: '',
    source: '`编程技能/专升本英语/`',
  },
]

// ── 真题年份：目录 → 需要排除的「带年份但非试卷」文件 ─────────────────
//   source 是**试卷原件所在目录**（相对仓库根）。注意 `计算机程序设计/`
//   在仓库根**不存在** —— 它实际是 `历年真题/计算机程序设计/`。原首页漏了
//   `历年真题/` 前缀，于是那一格指向一个不存在的目录（2026-09-20 实测）。
const EXAM_DIRS = [
  { label: '高数真题', route: '/posts/math/', dir: 'docs/posts/math', source: '`历年真题/高等数学/`' },
  { label: '计算机真题', route: '/posts/computer/', dir: 'docs/posts/computer', source: '`历年真题/计算机程序设计/`' },
  { label: '英语真题', route: '/posts/english/', dir: 'docs/posts/english', source: '`历年真题/公共英语/`' },
  { label: '政治真题', route: '/posts/politics/', dir: 'docs/posts/politics', source: '`历年真题/政治理论/`' },
]
// 带年份但不是试卷：知识汇编 / 备考指南 / 通关手册 / 原卷文字版之外的手册类
const NON_PAPER_RE = /汇编|指南|手册|模板|索引|规划|计划|大纲/

function mdFiles(rel) {
  try {
    return readdirSync(join(ROOT, rel)).filter((f) => f.endsWith('.md'))
  } catch {
    return []
  }
}

function countNotes(cfg) {
  return mdFiles(cfg.dir).filter((f) => !cfg.exclude.test(f)).length
}

/** 读一个试卷文件的前 30 行，判断它是否自称「同型演练」。 */
function isDrill(rel, name) {
  try {
    const head = readFileSync(join(ROOT, rel, name), 'utf-8')
      .split('\n').slice(0, 30).join('\n')
    return head.includes('同型演练')
  } catch {
    return false
  }
}

/** 返回 { years: [...], drill: Set }，年份来自文件名开头，排除手册类。 */
/** 读一个试卷文件的前 30 行，判断它是否自述「无该年 PDF 原件」。 */
function isRawOnly(rel, name) {
  try {
    const head = readFileSync(join(ROOT, rel, name), 'utf-8')
      .split('\n').slice(0, 30).join('\n')
    return head.includes('无该年 PDF 原件')
  } catch {
    return false
  }
}

/** 返回 { years: [...], drill: Set, raw: Set }，年份来自文件名开头，排除手册类。 */
function examYears(cfg) {
  const years = new Set()
  const drill = new Set()
  const raw = new Set()
  for (const f of mdFiles(cfg.dir)) {
    const m = f.match(/^(20\d{2})/)
    if (!m) continue
    if (NON_PAPER_RE.test(f)) continue
    years.add(m[1])
    if (isDrill(cfg.dir, f)) drill.add(m[1])
    if (isRawOnly(cfg.dir, f)) raw.add(m[1])
  }
  return { years: [...years].sort(), drill, raw }
}

/** 把连续年份压成 `2018–2026` 形式。 */
function compress(years) {
  if (!years.length) return '—'
  const parts = []
  let s = years[0]
  let p = years[0]
  for (let i = 1; i <= years.length; i++) {
    const y = years[i]
    const prev = Number(p)
    if (y && Number(y) === prev + 1) { p = y; continue }
    parts.push(s === p ? s : `${s}–${p}`)
    s = y; p = y
  }
  return parts.join('、')
}

/** 生成「规模」列：年份区间 + 只依据标签的同型演练说明。 */
function describeExams(cfg) {
  const { years, drill, raw } = examYears(cfg)
  if (!years.length) return '—'
  const real = years.filter((y) => !drill.has(y))
  const range = compress(years)
  const n = years.length
  let s
  if (!drill.size) s = `**${range}**（${n} 年，全为真题）`
  else if (!real.length) s = `**${range}**（${n} 年，全为同型演练）`
  else s = `**${range}**（${compress(real)} 真题 + ${compress([...drill].sort())} 同型演练）`
  // 来源等级：只有原始 md、本库无 PDF 原件的年份，不能与「已按 PDF 文字层重建」的年份同列。
  const rawReal = [...raw].filter((y) => !drill.has(y)).sort()
  if (rawReal.length) s = s.replace(/）$/, `；其中 ${compress(rawReal)} 无 PDF 原件、不含答案）`)
  return s
}

function buildBlock(EOL) {
  const rows = []
  for (const cfg of NOTE_DIRS) {
    const n = countNotes(cfg)
    const unit = cfg.unit || '篇'
    const note = cfg.note ? `（${cfg.note.replace(/^（|）$/g, '')}）` : ''
    rows.push(`| ${cfg.label} | [${cfg.route}](${cfg.route}) | **${n} ${unit}**${note} | ${cfg.source} |`)
  }
  for (const cfg of EXAM_DIRS) {
    rows.push(`| ${cfg.label} | [${cfg.route}](${cfg.route}) | ${describeExams(cfg)} | ${cfg.source} |`)
  }
  rows.push('| 题库总入口 | [/posts/题库/](/posts/题库/) | 6 个题库 | 自建 |')
  rows.push('| 备考规划 | [/guide/bili-plan/](/guide/bili-plan/) | 四科 B 站吸收规划 | 自建 |')

  return [
    START,
    '| 区块 | 站内位置 | 规模 | 来源 |',
    '|:---|:---|:---|:---|',
    ...rows,
    END,
  ].join(EOL)
}

// ── 主流程 ────────────────────────────────────────────────────────────
const src = readFileSync(INDEX, 'utf-8')

// ★ 跟随文件自身的行尾符。
//   实测 2026-09-20：本仓库工作区全是 CRLF（`index.md` 143 个 CRLF、0 个纯 LF），
//   而 `.gitattributes` 写的是 `* text=auto eol=lf`（期望 LF）。若这里硬用 '\n'
//   拼接，就会往一个 CRLF 文件里塞一段 LF 块 —— 整块在 git 里显示为全行改动，
//   还会把行尾规范化搅乱。所以先探再拼。
const EOL = src.includes('\r\n') ? '\r\n' : '\n'

/** 取一个标记区间的当前内容与期望内容。 */
function region(name, startMark, endMark, expected) {
  const i = src.indexOf(startMark)
  const j = src.indexOf(endMark)
  if (i === -1 || j === -1) {
    console.error(`❌ ${INDEX} 里找不到 ${startMark} / ${endMark} 标记，无法同步「${name}」。`)
    process.exit(2)
  }
  return { name, i, end: j + endMark.length, before: src.slice(i, j + endMark.length), after: expected }
}

const regions = [
  region('「本站有什么」表格', START, END, buildBlock(EOL)),
  // ⚠️ `after` 必须**带上标记本身** —— 区间是从 START 到 END 的整段，
  //    只回写日期会把两个标记吃掉，下一次运行就找不到区间了（实测踩过）。
  region('横幅「内容更新至」', DATE_START, DATE_END, DATE_START + (latestContentDateForHome(ROOT) || '（未知）') + DATE_END),
]

const stale = regions.filter((r) => r.before !== r.after)

if (!stale.length) {
  console.log('✅ 首页统计与横幅日期均为最新，无需改动。')
  process.exit(0)
}

if (CHECK) {
  console.log('❌ 首页有过期内容：')
  for (const r of stale) {
    console.log(`\n  【${r.name}】`)
    const a = r.before.split(EOL)
    const b = r.after.split(EOL)
    for (let k = 0; k < Math.max(a.length, b.length); k++) {
      if (a[k] !== b[k]) {
        console.log(`    现在: ${a[k] ?? '(无)'}`)
        console.log(`    应为: ${b[k] ?? '(无)'}`)
      }
    }
  }
  console.log('\n跑 `npm run home:stats` 重新生成。')
  process.exit(1)
}

// 从后往前替换，避免前面的改动让后面的下标失效。
let out = src
for (const r of [...stale].sort((a, b) => b.i - a.i)) {
  out = out.slice(0, r.i) + r.after + out.slice(r.end)
}
writeFileSync(INDEX, out, 'utf-8')
console.log('✅ 已同步 docs/index.md：')
for (const r of stale) console.log(`  · ${r.name} → ${r.after.replace(/\r?\n/g, ' ').trim()}`)
