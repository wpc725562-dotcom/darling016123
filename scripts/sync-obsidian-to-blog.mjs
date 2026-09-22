/**
 * 将 Obsidian 源库学习内容同步到 VitePress docs
 * - 高数章节笔记
 * - 计算机 1.1–2.9 知识点
 * - 各科真题（不覆盖已完整的详解页）
 * - 英语系统学习笔记
 * - 重写侧栏 config.mts + 各科 index
 *
 * ⚠️ 危险（2026-09-04 实测）：本脚本的模板已落后于 docs/ 里的人工精修内容。
 * 直接 `npm run docs:sync` 会删掉 config.mts 的 PWA 配置、日语板块、四科
 * 「学习手册」导航（-290 行），以及 english/notes/grammar.md 的 Mermaid
 * 时态时间轴与真题专项链接（-69 行）。跑完必须 `git diff` 逐文件核对，
 * 或先 `git stash`/提交再跑。新增的 guardSource() 只防「源目录缺失→写空
 * 索引」这一类，防不住模板过时导致的覆盖。
 *
 * 🛑 2026-09-22 已加 guardDeprecated() 运行时守卫：检测到「docs 侧已分叉」
 * 或「config.mts 含 sync 不产出的人工内容」时直接 exit 1，不再默认放行。
 * 确实要跑就显式 `--force`；先用 `--dry-run --force` 看影响面（不落盘）。
 * 起因：2026-09-22 完成 33 个文件的导航/编号修复，这些成果全在 docs/ 侧，
 * 一次误跑会全部回退。
 *
 * ⚠️ 2025 例外（2026-08-30 补记）：docs/posts/math/2025.md 是人工聚合页
 * （3 张 gif 回忆版），顶层 历年真题/高等数学/ 无 2025.md 源（_索引.md 已
 * 声明该缺口），syncYearPapers 不会覆盖它，但 writeConfig 重建侧边栏时
 * 「2025 回忆版 📷」条目会丢——跑完 sync 后需把它手工加回 config.mts
 * 数学年份组（插在 2026 与 2024 之间）。
 */
import fs from 'node:fs'
import path from 'node:path'

const ROOT = process.cwd()
const DOCS = path.join(ROOT, 'docs')

const stats = { written: 0, skipped: 0, files: [] }

/**
 * --dry-run：只走一遍逻辑、打印将要写哪些文件，一个字节都不落盘。
 * 用途：在 `--force` 真正同步之前先看影响面（配合 guardDeprecated 使用）。
 */
const DRY_RUN = process.argv.includes('--dry-run') || process.env.SYNC_DRY === '1'

function ensureDir(p) {
  if (DRY_RUN) return
  fs.mkdirSync(p, { recursive: true })
}

function writeFile(rel, content) {
  const abs = path.join(DOCS, rel)
  ensureDir(path.dirname(abs))
  if (!DRY_RUN) fs.writeFileSync(abs, content, 'utf8')
  stats.written++
  stats.files.push(rel)
}

function read(p) {
  return fs.readFileSync(p, 'utf8')
}

function listMd(dir) {
  if (!fs.existsSync(dir)) return []
  const out = []
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, ent.name)
    if (ent.isDirectory()) out.push(...listMd(full))
    else if (ent.name.endsWith('.md') && !ent.name.startsWith('_')) out.push(full)
  }
  return out
}

/**
 * 源目录缺失/无匹配笔记时中止该科的同步。
 * 否则会用空列表覆盖已上线的 index.md，把整科导航清空（2026-09-04 实测
 * 计算机程序设计/ 不存在，syncComputerNotes 会写出空索引覆盖 40 篇笔记入口）。
 */
function guardSource(label, srcRoot, files) {
  const rel = path.relative(ROOT, srcRoot).replace(/\\/g, '/')
  if (!fs.existsSync(srcRoot)) {
    console.warn(`⚠️  跳过 ${label}：源目录 ${rel}/ 不存在，保留站点现有页面不动`)
    return false
  }
  if (files.length === 0) {
    console.warn(`⚠️  跳过 ${label}：${rel}/ 下没有可同步的 .md，保留站点现有页面不动`)
    return false
  }
  return true
}

/** Obsidian → VitePress Markdown */
function convertMd(raw, { title, description = '', extraFront = {} } = {}) {
  let body = raw.replace(/\r\n/g, '\n')

  // 去掉源文件顶层 # 标题（frontmatter 已有 title 时再补一个 h1）
  // 保留正文

  // callout: > [!success]- 标题  → 引用块
  body = body.replace(
    /^>\s*\[!(\w+)\][+-]?\s*(.*)$/gm,
    (_, type, label) => {
      const map = {
        success: '✅ 答案与解析',
        tip: '💡 提示',
        warning: '⚠️ 注意',
        note: '📝 说明',
        info: 'ℹ️ 说明',
        question: '❓ 问题',
        example: '📌 示例',
      }
      const t = map[String(type).toLowerCase()] || label || type
      return `> **${label?.trim() || t}**`
    },
  )

  // [[path|label]] → [label](href)
  body = body.replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, (_, p, label) => {
    const href = wikiToHref(p.trim())
    return href ? `[${label.trim()}](${href})` : label.trim()
  })
  // [[path]]
  body = body.replace(/\[\[([^\]]+)\]\]/g, (_, p) => {
    const name = p.trim()
    const href = wikiToHref(name)
    const label = name.split('/').pop().replace(/\.md$/, '')
    return href ? `[${label}](${href})` : label
  })

  // 相对 md 链接里的空格编码（可选保留）
  body = body.replace(/\]\(([^)]+\.md)\)/g, (m, link) => {
    if (link.startsWith('http')) return m
    return `](${encodeURI(link.replace(/%20/g, ' '))})`
  })

  // 清理多余空行
  body = body.replace(/\n{4,}/g, '\n\n\n').trim() + '\n'

  // 若正文不以 # 开头，补标题
  if (!/^#\s/m.test(body.split('\n').slice(0, 5).join('\n'))) {
    body = `# ${title}\n\n${body}`
  }

  const fm = {
    title,
    description: description || title,
    ...extraFront,
  }
  const yaml = Object.entries(fm)
    .map(([k, v]) => `${k}: ${JSON.stringify(String(v))}`)
    .join('\n')

  return `---\n${yaml}\n---\n\n${body}`
}

/** 粗略把 wiki path 映射到站内路径（够用即可） */
function wikiToHref(p) {
  const s = p.replace(/\\/g, '/').replace(/\.md$/, '')

  if (s.includes('历年真题/高等数学/')) {
    const y = s.match(/(\d{4})$/)
    if (y) return `/posts/math/${y[1]}`
    return '/posts/math/'
  }
  if (s.includes('历年真题/计算机程序设计/考点拆分')) return '/posts/computer/topics/'
  if (s.includes('历年真题/计算机程序设计/')) {
    const y = s.match(/(\d{4})$/)
    if (y) return `/posts/computer/${y[1]}`
    return '/posts/computer/'
  }
  if (s.includes('历年真题/政治理论/')) {
    const y = s.match(/(\d{4})$/)
    if (y) return `/posts/politics/${y[1]}`
    return '/posts/politics/'
  }
  if (s.includes('历年真题/公共英语/')) {
    const y = s.match(/(\d{4})$/)
    if (y) return `/posts/english/${y[1]}`
    return '/posts/english/'
  }
  if (s.includes('历年真题')) return '/guide/sources'

  if (s.includes('计算机程序设计/') || /^计算机程序设计\/\d/.test(s) || /^\d\.\d/.test(s)) {
    const m = s.match(/(\d\.\d+)\s*(.*)$/)
    if (m) return `/posts/computer/notes/${slugNote(m[1], m[2] || '')}`
  }
  if (s === '计算机程序设计' || s.endsWith('/计算机程序设计')) return '/posts/computer/'

  if (s.includes('高等数学/')) {
    // 章内笔记
    const base = path.basename(s)
    const m = base.match(/^(\d+\.\d+)\s*(.*)$/)
    if (m) return `/posts/math/notes/${slugNote(m[1], m[2] || '')}`
  }
  if (s === '高等数学' || s.endsWith('/高等数学')) return '/posts/math/'

  if (s.includes('专升本英语') || s.includes('编程技能')) {
    const map = {
      专升本英语考试概述与题型分析: 'overview',
      作文模板与高分句型: 'writing',
      历年真题分类与讲解: 'past-papers-guide',
      语法考点精讲: 'grammar',
      阅读理解高分技巧: 'reading',
      高频词汇速记: 'vocabulary',
      英语知识库: 'notes/',
    }
    for (const [k, v] of Object.entries(map)) {
      if (s.includes(k)) return `/posts/english/notes/${v}`.replace(/notes\/notes\//, 'notes/')
    }
    return '/posts/english/notes/'
  }
  if (s === '英语') return '/posts/english/'
  if (s === '政治' || s.endsWith('/政治')) return '/posts/politics/'
  if (s.includes('政治理论/')) {
    const base = path.basename(s)
    const m = base.match(/^(\d{2})-(.+)$/)
    if (m) return `/posts/politics/notes/${m[1]}-${slugifyCn(m[2])}`
    if (base.startsWith('00-')) return '/posts/politics/notes/00-syllabus'
    return '/posts/politics/notes/'
  }

  return null
}

function slugifyCn(s) {
  return String(s || '')
    .replace(/[\\/:*?"<>|]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
}

function slugNote(num, title) {
  const t = (title || '')
    .replace(/[\\/:*?"<>|]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
  return t ? `${num}-${t}` : String(num)
}

function chapterMetaFromPath(filePath) {
  // .../高等数学/第一章 函数与极限/1.1 函数的概念.md
  const rel = path.relative(path.join(ROOT, '高等数学'), filePath).replace(/\\/g, '/')
  const parts = rel.split('/')
  const chapter = parts.length > 1 ? parts[0] : '其他'
  const base = path.basename(filePath, '.md')
  const m = base.match(/^(\d+\.\d+)\s*(.*)$/)
  const num = m ? m[1] : base
  const title = m ? (m[2] ? `${m[1]} ${m[2]}` : m[1]) : base
  const slug = slugNote(num, m ? m[2] : base)
  return { chapter, num, title, slug, rel }
}

// ─────────── 同步：高数章节 ───────────
function syncMathNotes() {
  const srcRoot = path.join(ROOT, '高等数学')
  const files = listMd(srcRoot)
  if (!guardSource('高等数学章节笔记', srcRoot, files)) return { byChapter: new Map(), ordered: [] }
  const byChapter = new Map()

  for (const f of files) {
    const meta = chapterMetaFromPath(f)
    // 只同步「1.1 标题」式章节笔记，跳过 00-大纲 等总览页
    if (!/^\d+\.\d+/.test(String(meta.num))) {
      stats.skipped++
      continue
    }
    const raw = read(f)
    const content = convertMd(raw, {
      title: meta.title,
      description: `高等数学 · ${meta.chapter} · ${meta.title}`,
      extraFront: { category: 'math-note', chapter: meta.chapter },
    })
    writeFile(`posts/math/notes/${meta.slug}.md`, content)
    if (!byChapter.has(meta.chapter)) byChapter.set(meta.chapter, [])
    byChapter.get(meta.chapter).push(meta)
  }

  // 排序：按 num
  for (const arr of byChapter.values()) {
    arr.sort((a, b) => String(a.num).localeCompare(String(b.num), 'zh', { numeric: true }))
  }

  // 章节索引
  const chapterOrder = [
    '第一章 函数与极限',
    '第二章 一元函数微分学',
    '第三章 一元函数积分学',
    '第四章 向量与空间几何',
    '第五章 多元函数',
    '第六章 重积分与曲线积分',
    '第七章 常微分方程',
    '第八章 无穷级数',
  ]
  const ordered = [
    ...chapterOrder.filter((c) => byChapter.has(c)),
    ...[...byChapter.keys()].filter((c) => !chapterOrder.includes(c)).sort(),
  ]

  let indexBody = `---
title: "高等数学 · 章节笔记"
description: "从 Obsidian 同步的 8 章系统笔记"
---

# 高等数学 · 章节笔记

> 从 Obsidian 源库 \`高等数学/\` 同步。含核心知识、速记表与闭卷挑战答案块。

| 章节 | 篇数 |
|:---|:---:|
${ordered.map((c) => `| ${c} | ${byChapter.get(c)?.length || 0} |`).join('\n')}

`
  for (const ch of ordered) {
    const items = byChapter.get(ch) || []
    indexBody += `\n## ${ch}\n\n`
    for (const it of items) {
      indexBody += `- [${it.title}](/posts/math/notes/${it.slug})\n`
    }
  }
  indexBody += `\n← [真题总览](/posts/math/) · [回首页](/)\n`
  writeFile('posts/math/notes/index.md', indexBody)

  return { byChapter, ordered }
}

// ─────────── 同步：计算机知识点 ───────────
function syncComputerNotes() {
  const srcRoot = path.join(ROOT, '计算机程序设计')
  const files = listMd(srcRoot)
  if (!guardSource('计算机知识点笔记', srcRoot, files)) return []
  const items = []

  for (const f of files) {
    const base = path.basename(f, '.md')
    const m = base.match(/^(\d+\.\d+)\s*(.*)$/)
    if (!m) continue
    const num = m[1]
    const titlePart = m[2] || ''
    const title = `${num} ${titlePart}`.trim()
    const slug = slugNote(num, titlePart)
    const part = num.startsWith('1.') ? 'C语言' : '数据结构'
    const raw = read(f)
    const content = convertMd(raw, {
      title,
      description: `计算机程序设计 · ${part} · ${title}`,
      extraFront: { category: 'computer-note', part },
    })
    writeFile(`posts/computer/notes/${slug}.md`, content)
    items.push({ num, title, slug, part })
  }

  items.sort((a, b) => String(a.num).localeCompare(String(b.num), 'zh', { numeric: true }))

  const cPart = items.filter((i) => i.part === 'C语言')
  const dPart = items.filter((i) => i.part === '数据结构')

  let indexBody = `---
title: "计算机 · 知识点笔记"
description: "C 语言 1.1–1.11 + 数据结构 2.1–2.9"
---

# 计算机 · 知识点笔记

> 从 Obsidian \`计算机程序设计/\` 同步。对应谭浩强 + 严蔚敏考点。

## C 语言（1.1–1.11）

${cPart.map((i) => `- [${i.title}](/posts/computer/notes/${i.slug})`).join('\n')}

## 数据结构（2.1–2.9）

${dPart.map((i) => `- [${i.title}](/posts/computer/notes/${i.slug})`).join('\n')}

## 推荐刷题路径

1. [2024 全卷详解](/posts/computer/2024) 摸底
2. [考点拆分](/posts/computer/topics/) 回炉
3. 回本页系统笔记补概念

← [真题总览](/posts/computer/) · [回首页](/)
`
  writeFile('posts/computer/notes/index.md', indexBody)
  return items
}

// ─────────── 同步：政治系统笔记 ───────────
function syncPoliticsNotes() {
  const srcRoot = path.join(ROOT, '政治理论')
  const files = listMd(srcRoot)
  if (!guardSource('政治系统笔记', srcRoot, files)) return []
  const items = []

  for (const f of files) {
    const base = path.basename(f, '.md')
    // 00-考试大纲与题型 / 01-马克思主义中国化时代化
    const m = base.match(/^(\d{2})-(.+)$/)
    if (!m) continue
    const num = m[1]
    const titlePart = m[2]
    const title = `${num} ${titlePart}`
    const slug = `${num}-${slugifyCn(titlePart)}`
    const raw = read(f)
    const content = convertMd(raw, {
      title,
      description: `政治理论 · ${title}`,
      extraFront: { category: 'politics-note' },
    })
    writeFile(`posts/politics/notes/${slug}.md`, content)
    items.push({ num, title, slug, titlePart })
  }

  items.sort((a, b) => String(a.num).localeCompare(String(b.num), 'zh', { numeric: true }))

  let indexBody = `---
title: "政治理论 · 系统笔记"
description: "按 2026 广东专升本政治大纲模块整理"
---

# 政治理论 · 系统笔记

> 从 Obsidian \`政治理论/\` 同步。对齐公开考纲：毛中特 + 习思想 + 时政答题模板。

| # | 笔记 |
|:---:|:---|
${items.map((i) => `| ${i.num} | [${i.title}](/posts/politics/notes/${i.slug}) |`).join('\n')}

## 推荐路径

1. [00 大纲题型](/posts/politics/notes/00-考试大纲与题型) → [18 金句](/posts/politics/notes/18-必背金句与名词)
2. 按 01–15 模块闭卷默写
3. 回 [真题总览](/posts/politics/) 做 2018–2024 演练

← [真题总览](/posts/politics/) · [回首页](/)
`
  // fix links if slug uses slugifyCn (Chinese kept)
  indexBody = `---
title: "政治理论 · 系统笔记"
description: "按 2026 广东专升本政治大纲模块整理"
---

# 政治理论 · 系统笔记

> 从 Obsidian \`政治理论/\` 同步。对齐公开考纲：毛中特 + 习思想 + 时政答题模板。

| # | 笔记 |
|:---:|:---|
${items.map((i) => `| ${i.num} | [${i.title}](/posts/politics/notes/${i.slug}) |`).join('\n')}

## 推荐路径

1. 先过 **00 大纲** + **18 金句**
2. 按 01–15 模块闭卷默写
3. 回 [真题总览](/posts/politics/) 做 2018–2024 演练
4. 主观题用 **17 答题模板**

← [真题总览](/posts/politics/) · [回首页](/)
`
  writeFile('posts/politics/notes/index.md', indexBody)
  return items
}

// ─────────── 同步：真题年份（不覆盖完整页） ───────────
function syncYearPapers(subject, srcDir, outDir, { skipYears = [], label }) {
  const years = []
  if (!fs.existsSync(srcDir)) return years
  for (const name of fs.readdirSync(srcDir)) {
    if (!/^\d{4}\.md$/.test(name)) continue
    const year = name.slice(0, 4)
    if (skipYears.includes(year)) {
      stats.skipped++
      years.push({ year, status: 'kept-full' })
      continue
    }
    const raw = read(path.join(srcDir, name))
    const content = convertMd(raw, {
      title: `${label} · ${year}`,
      description: `广东专升本 ${label} ${year} 真题演练（Obsidian 同步）`,
      extraFront: { category: 'exam', year },
    })
    // 若目标已是超长详解（>15KB），跳过
    const dest = path.join(DOCS, outDir, `${year}.md`)
    if (fs.existsSync(dest) && fs.statSync(dest).size > 15000) {
      stats.skipped++
      years.push({ year, status: 'kept-existing-full' })
      continue
    }
    writeFile(path.join(outDir, `${year}.md`).replace(/\\/g, '/'), content)
    years.push({ year, status: 'synced' })
  }
  years.sort((a, b) => Number(b.year) - Number(a.year))
  return years
}

// ─────────── 同步：英语学习笔记 ───────────
function syncEnglishNotes() {
  const map = [
    ['00-考试大纲与题型补强.md', 'syllabus', '考试大纲与题型补强'],
    ['专升本英语考试概述与题型分析.md', 'overview', '考试概述与题型分析'],
    ['作文模板与高分句型.md', 'writing', '作文模板与高分句型'],
    ['历年真题分类与讲解.md', 'past-papers-guide', '历年真题分类与讲解'],
    ['语法考点精讲.md', 'grammar', '语法考点精讲'],
    ['阅读理解高分技巧.md', 'reading', '阅读理解高分技巧'],
    ['高频词汇速记.md', 'vocabulary', '高频词汇速记'],
  ]
  const srcDir = path.join(ROOT, '编程技能/专升本英语/笔记')
  const items = []
  for (const [file, slug, title] of map) {
    const full = path.join(srcDir, file)
    if (!fs.existsSync(full)) continue
    const content = convertMd(read(full), {
      title,
      description: `公共英语 · ${title}`,
      extraFront: { category: 'english-note' },
    })
    writeFile(`posts/english/notes/${slug}.md`, content)
    items.push({ slug, title })
  }

  // 知识库当 notes 首页
  const kb = path.join(ROOT, '编程技能/专升本英语/英语知识库.md')
  if (fs.existsSync(kb)) {
    let body = convertMd(read(kb), {
      title: '英语 · 学习笔记',
      description: '公共英语系统笔记导航',
    })
    // 追加站内链接清单
    body += `\n\n## 本站笔记入口\n\n${items
      .map((i) => `- [${i.title}](/posts/english/notes/${i.slug})`)
      .join('\n')}\n\n## 历年真题\n\n- [2008–2024 真题总览](/posts/english/)\n`
    writeFile('posts/english/notes/index.md', body)
  } else {
    writeFile(
      'posts/english/notes/index.md',
      `---\ntitle: "英语 · 学习笔记"\n---\n\n# 英语 · 学习笔记\n\n${items
        .map((i) => `- [${i.title}](/posts/english/notes/${i.slug})`)
        .join('\n')}\n`,
    )
  }
  return items
}

// ─────────── 更新各科总览 ───────────
function updateIndexes({ mathChapters, computerNotes, mathYears, compYears, polYears, engNotes, politicsNotes }) {
  // math index
  writeFile(
    'posts/math/index.md',
    `---
title: "高等数学 · 总览"
description: "真题 + 章节笔记"
---

# 高等数学 · 总览

> 真题正文嵌题（Sakiko 体例）+ Obsidian 系统章节笔记，全部在站内阅读。

## 历年真题

| 年份 | 页面 | 说明 |
|:---:|:---|:---|
| **2026** | [全卷详解](/posts/math/2026) | Sakiko 体例 · 完整 |
| **2024** | [全卷详解](/posts/math/2024) | Sakiko 体例 · 完整 |
${mathYears
  .filter((y) => !['2024', '2026'].includes(y.year))
  .map((y) => `| ${y.year} | [演练页](/posts/math/${y.year}) | Obsidian 同步 · 骨架/同型 |`)
  .join('\n')}

## 章节笔记（系统课）

→ **[打开章节目录](/posts/math/notes/)**（${[...mathChapters.byChapter.values()].reduce((n, a) => n + a.length, 0)} 篇）

${mathChapters.ordered
  .map((ch) => {
    const items = mathChapters.byChapter.get(ch) || []
    return `### ${ch}\n\n${items.map((i) => `- [${i.title}](/posts/math/notes/${i.slug})`).join('\n')}`
  })
  .join('\n\n')}

## 学习路径

1. 先刷 [2026](/posts/math/2026) / [2024](/posts/math/2024) 摸底
2. 错题回章节笔记闭卷挑战
3. 再做 2018–2023 同型演练

← [回首页](/)
`,
  )

  // computer index
  writeFile(
    'posts/computer/index.md',
    `---
title: "计算机程序设计 · 总览"
description: "真题 + 知识点 + 考点拆分"
---

# 计算机程序设计 · 总览

> 广东普通专升本统考：**《计算机基础与程序设计》** · 满分 200 · 150 分钟

## 推荐先看

| 页面 | 说明 |
|:---|:---|
| [**2024 全卷详解**](/posts/computer/2024) | 题 + 答 + 逐步解析 · 完整 |
| [**知识点笔记**](/posts/computer/notes/) | C 1.1–1.11 + 数据结构 2.1–2.9 |
| [**考点拆分**](/posts/computer/topics/) | 01–05 分批刷 |

## 历年真题

| 年份 | 页面 | 状态 |
|:---:|:---|:---|
| 2024 | [全卷详解](/posts/computer/2024) | 完整 |
${compYears
  .filter((y) => y.year !== '2024')
  .map((y) => `| ${y.year} | [演练页](/posts/computer/${y.year}) | Obsidian 同步 |`)
  .join('\n')}

## 知识点（系统课）

### C 语言

${computerNotes
  .filter((i) => i.part === 'C语言')
  .map((i) => `- [${i.title}](/posts/computer/notes/${i.slug})`)
  .join('\n')}

### 数据结构

${computerNotes
  .filter((i) => i.part === '数据结构')
  .map((i) => `- [${i.title}](/posts/computer/notes/${i.slug})`)
  .join('\n')}

## 试卷结构

| 题型 | 题量 | 分值 |
|:---|:---:|:---:|
| 单选题 | 20 | 60 |
| 判断题 | 10 | 20 |
| 填空题 | 5 | 20 |
| 简答题 | 4 | 40 |
| 计算题 | 3 | 30 |
| 应用题 | 3 | 30 |
| **合计** | | **200** |

← [回首页](/)
`,
  )

  // politics index
  writeFile(
    'posts/politics/index.md',
    `---
title: "政治理论 · 总览"
description: "系统笔记 + 2018–2024 真题演练"
---

# 政治理论 · 总览

> 广东普通专升本公共课《政治理论》· 满分 100 · 120 分钟
> 系统笔记按 **2026 公开考纲** 模块整理；真题为同型演练（非原卷全文）。

## 推荐先看

| 页面 | 说明 |
|:---|:---|
| [**系统笔记**](/posts/politics/notes/) | 大纲 · 毛中特 · 习思想 · 答题模板 · 金句（${politicsNotes?.length || 0} 篇） |
| [00 考试大纲与题型](/posts/politics/notes/${politicsNotes?.find((i) => i.num === '00')?.slug || '00-考试大纲与题型'}) | 题型分值 + 范围 |
| [18 必背金句](/posts/politics/notes/${politicsNotes?.find((i) => i.num === '18')?.slug || '18-必背金句与名词'}) | 考前默写 |

## 系统笔记

${(politicsNotes || []).map((i) => `- [${i.title}](/posts/politics/notes/${i.slug})`).join('\n')}

## 历年真题演练

| 年份 | 页面 |
|:---:|:---|
${polYears.map((y) => `| ${y.year} | [打开](/posts/politics/${y.year}) |`).join('\n')}

## 试卷结构（常见）

| 题型 | 分值 |
|:---|:---:|
| 单选 20 | 20 |
| 多选 10 | 20 |
| 辨析 2 | 14 |
| 问答 3 | 21 |
| 论述 1 | 10 |
| 材料 1 | 15 |
| **合计** | **100** |

## 学习建议

1. 先过系统笔记 00 + 18（题型 + 金句）
2. 01–15 分模块闭卷默写
3. 按年做同型演练；材料题用 17 四步法
4. 时政以**当年大纲**时间区间为准

← [回首页](/)
`,
  )

  // english index — 保留年份列表，追加学习笔记入口
  const engYears = []
  for (let y = 2024; y >= 2008; y--) {
    if (fs.existsSync(path.join(DOCS, `posts/english/${y}.md`))) engYears.push(String(y))
  }
  writeFile(
    'posts/english/index.md',
    `---
title: "公共英语 · 总览"
description: "真题正文嵌入 + 系统学习笔记"
---

# 公共英语 · 总览

> 题目嵌在正文里（Sakiko 体例）+ Obsidian 系统学习笔记。

## 系统学习笔记

| 笔记 | 说明 |
|:---|:---|
| [学习笔记首页](/posts/english/notes/) | 知识库总导航 |
${engNotes.map((i) => `| [${i.title}](/posts/english/notes/${i.slug}) | 从 Obsidian 同步 |`).join('\n')}

## 历年真题（正文嵌题）

| 年份 | 页面 |
|:---:|:---|
${engYears.map((y) => `| ${y} | [打开](/posts/english/${y}) |`).join('\n')}

## 怎么刷

1. 先过 [考试概述](/posts/english/notes/overview) + [高频词汇](/posts/english/notes/vocabulary)
2. 近三年真题：[2024](/posts/english/2024) / [2023](/posts/english/2023) / [2022](/posts/english/2022)
3. 写作默写 [作文模板](/posts/english/notes/writing)

← [回首页](/)
`,
  )
}

// ─────────── 首页 ───────────
function updateHome() {
  writeFile(
    'index.md',
    `---
layout: home
title: 广东专升本 · 复习笔记
hero:
  name: 广东专升本
  text: 复习笔记站
  tagline: Obsidian 全库上站 · Sakiko 式正文嵌题 · 樱花二次元主题
  image:
    src: /avatar.webp
    alt: 看板娘
  actions:
    - theme: brand
      text: 高数章节笔记
      link: /posts/math/notes/
    - theme: brand
      text: 计算机知识点
      link: /posts/computer/notes/
    - theme: brand
      text: 政治系统笔记
      link: /posts/politics/notes/
    - theme: alt
      text: 英语真题
      link: /posts/english/
    - theme: alt
      text: GitHub
      link: https://github.com/wpc725562-dotcom/darling016123

features:
  - title: Obsidian 学习库上站
    details: 高数 50+ 章节、计算机 1.1–2.9、政治 19 模块、英语系统笔记、各科真题——不再只开本地库。
  - title: 题目嵌在正文里
    details: 题干、选项、答案解析直接写在 Markdown 页面中，可搜索、可复制、可公式渲染。
  - title: 二次元主题
    details: 樱花色 · 暗色网格 · 左下 Live2D · 樱花粒子 · 音乐按钮 · 阅读进度条。
  - title: 零服务器
    details: VitePress + GitHub Pages。源库仍在 Obsidian，网站是可读可刷的网页版。
---

<div class="hero-sakura">

# 怎么刷（推荐顺序）

1. **计算机** → [知识点](/posts/computer/notes/) → [2024 全卷](/posts/computer/2024) → [考点拆分](/posts/computer/topics/)
2. **高数** → [章节笔记](/posts/math/notes/) → [2026](/posts/math/2026) / [2024](/posts/math/2024)
3. **英语** → [学习笔记](/posts/english/notes/) → 近三年真题
4. **政治** → [系统笔记](/posts/politics/notes/) → [真题演练](/posts/politics/)

</div>

## 科目入口

<div class="home-grid">
  <a class="home-card" href="./posts/math/notes/">
    <h3>📐 高数章节</h3>
    <p>函数极限 · 微分 · 积分 · 多元 · 级数 · 全库同步</p>
  </a>
  <a class="home-card" href="./posts/computer/notes/">
    <h3>💻 计算机知识点</h3>
    <p>C 1.1–1.11 + 数据结构 2.1–2.9</p>
  </a>
  <a class="home-card" href="./posts/english/notes/">
    <h3>英文 英语笔记</h3>
    <p>词汇 · 语法 · 阅读 · 作文模板</p>
  </a>
  <a class="home-card" href="./posts/math/2026">
    <h3>📝 高数 2026 卷</h3>
    <p>Sakiko 同款正文嵌题 + 公式</p>
  </a>
  <a class="home-card" href="./posts/computer/2024">
    <h3>📝 计算机 2024 卷</h3>
    <p>全卷详解 · 单选到编程</p>
  </a>
  <a class="home-card" href="./posts/english/">
    <h3>📝 英语真题</h3>
    <p>2008–2024 正文嵌入</p>
  </a>
  <a class="home-card" href="./posts/politics/notes/">
    <h3>📕 政治系统笔记</h3>
    <p>大纲 · 毛中特 · 习思想 · 金句 · 答题模板</p>
  </a>
  <a class="home-card" href="./posts/politics/">
    <h3>📕 政治真题</h3>
    <p>2018–2024 同型演练</p>
  </a>
  <a class="home-card" href="./posts/computer/topics/">
    <h3>🎯 考点拆分</h3>
    <p>C 基础 · 指针 · 链表 · 树图 · 手写</p>
  </a>
</div>

## 本站有什么（相对 Obsidian）

| 区块 | 站内位置 | 来源 |
|:---|:---|:---|
| 高数章节 50+ 篇 | [/posts/math/notes/](/posts/math/notes/) | \`高等数学/\` |
| 计算机 20 篇知识点 | [/posts/computer/notes/](/posts/computer/notes/) | \`计算机程序设计/\` |
| 英语系统笔记 | [/posts/english/notes/](/posts/english/notes/) | \`编程技能/专升本英语/\` |
| 政治系统笔记 | [/posts/politics/notes/](/posts/politics/notes/) | \`政治理论/\` 19 模块 |
| 高数真题 | [/posts/math/](/posts/math/) | 2024/2026 完整 + 历年演练 |
| 计算机真题 | [/posts/computer/](/posts/computer/) | 2024 完整 + 历年演练 |
| 英语真题 | [/posts/english/](/posts/english/) | 2008–2024 |
| 政治真题 | [/posts/politics/](/posts/politics/) | 2018–2024 充实演练 |

## 和 Sakiko 的关系（透明说明）

| 项 | 说明 |
|:---|:---|
| 视觉 / 主题 | 参考 [a3292334877-star/blog](https://github.com/a3292334877-star/blog) 樱花主题与 Live2D |
| 高数 2024/2026 详解 | 移植其公开回忆版文 |
| 你的增量 | **Obsidian 全科学习库**、英语 17 年、计算机考点拆分与知识点 |
| 版权边界 | 回忆版仅供个人备考；主题保留致谢 |

## 本地预览

\`\`\`bash
cd "D:/专升本/专升本"
npm install
npm run docs:dev
\`\`\`

## 资料边界

本站真题为**考生回忆版 / OCR 汇编 / 同型演练**，非考试院原卷。详见 [使用说明](/guide/) 与 [资料边界](/guide/sources)。
`,
  )
}

// ─────────── config.mts 侧栏 ───────────
function writeConfig({ mathChapters, computerNotes, mathYears, compYears, polYears, engNotes, politicsNotes }) {
  const mathNoteItems = []
  for (const ch of mathChapters.ordered) {
    const items = mathChapters.byChapter.get(ch) || []
    // 侧栏按章折叠：章作 text，下面 items
    mathNoteItems.push({
      text: ch.replace(/^第/, '').slice(0, 12),
      collapsed: true,
      items: items.map((i) => ({
        text: i.title.length > 18 ? i.title.slice(0, 18) + '…' : i.title,
        link: `/posts/math/notes/${i.slug}`,
      })),
    })
  }

  const compC = computerNotes.filter((i) => i.part === 'C语言')
  const compD = computerNotes.filter((i) => i.part === '数据结构')

  const mathYearLinks = [
    { text: '真题总览', link: '/posts/math/' },
    { text: '章节笔记总览', link: '/posts/math/notes/' },
    { text: '2026 全卷', link: '/posts/math/2026' },
    { text: '2024 全卷', link: '/posts/math/2024' },
    ...mathYears
      .filter((y) => !['2024', '2026'].includes(y.year))
      .map((y) => ({ text: `${y.year} 演练`, link: `/posts/math/${y.year}` })),
  ]

  const compYearLinks = [
    { text: '真题总览', link: '/posts/computer/' },
    { text: '知识点总览', link: '/posts/computer/notes/' },
    { text: '2024 全卷', link: '/posts/computer/2024' },
    ...compYears
      .filter((y) => y.year !== '2024')
      .map((y) => ({ text: `${y.year} 演练`, link: `/posts/computer/${y.year}` })),
  ]

  const engYearLinks = []
  for (let y = 2024; y >= 2008; y--) {
    if (fs.existsSync(path.join(DOCS, `posts/english/${y}.md`))) {
      engYearLinks.push({ text: String(y), link: `/posts/english/${y}` })
    }
  }

  const config = `import { defineConfig } from 'vitepress'

// GitHub Pages 项目站固定 base
const base = process.env.VITEPRESS_BASE || '/darling016123/'

export default defineConfig({
  title: '专升本笔记 · Sakiko 风',
  description: 'Obsidian 全库 + 历年真题详解 · 公共课 + 计算机',
  lang: 'zh-CN',
  base,
  cleanUrls: true,
  lastUpdated: true,
  ignoreDeadLinks: true,

  head: [
    ['link', { rel: 'icon', href: \`\${base}favicon.svg\` }],
    ['meta', { name: 'theme-color', content: '#e4596f' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }],
    ['link', { href: 'https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@600;700&display=swap', rel: 'stylesheet' }],
  ],

  markdown: {
    math: true,
    lineNumbers: true,
    theme: {
      light: 'github-light',
      dark: 'github-dark',
    },
  },

  themeConfig: {
    logo: '/favicon.svg',
    siteTitle: '专升本笔记',
    outline: {
      level: [2, 3],
      label: '本页目录',
    },
    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索', buttonAriaLabel: '搜索' },
          modal: {
            noResultsText: '没有结果',
            resetButtonTitle: '清空',
            footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' },
          },
        },
      },
    },
    nav: [
      { text: '首页', link: '/' },
      {
        text: '高数',
        items: [
          { text: '章节笔记', link: '/posts/math/notes/' },
          { text: '真题总览', link: '/posts/math/' },
          { text: '2026 全卷', link: '/posts/math/2026' },
          { text: '2024 全卷', link: '/posts/math/2024' },
        ],
      },
      {
        text: '计算机',
        items: [
          { text: '知识点', link: '/posts/computer/notes/' },
          { text: '2024 全卷', link: '/posts/computer/2024' },
          { text: '考点拆分', link: '/posts/computer/topics/' },
          { text: '真题总览', link: '/posts/computer/' },
        ],
      },
      {
        text: '英语',
        items: [
          { text: '学习笔记', link: '/posts/english/notes/' },
          { text: '真题总览', link: '/posts/english/' },
          { text: '2024', link: '/posts/english/2024' },
          { text: '2023', link: '/posts/english/2023' },
        ],
      },
      {
        text: '政治',
        items: [
          { text: '系统笔记', link: '/posts/politics/notes/' },
          { text: '真题总览', link: '/posts/politics/' },
          { text: '大纲题型', link: '/posts/politics/notes/${politicsNotes?.find((i) => i.num === '00')?.slug || ''}' },
        ],
      },
      { text: '使用说明', link: '/guide/' },
      {
        text: 'GitHub',
        link: 'https://github.com/wpc725562-dotcom/darling016123',
      },
    ],
    sidebar: {
      '/posts/math/': [
        {
          text: '高等数学 · 真题',
          items: ${JSON.stringify(mathYearLinks, null, 12).replace(/\n/g, '\n          ')},
        },
${mathNoteItems
  .map(
    (g) => `        {
          text: ${JSON.stringify('笔记 · ' + g.text)},
          collapsed: true,
          items: ${JSON.stringify(g.items, null, 12).replace(/\n/g, '\n          ')},
        },`,
  )
  .join('\n')}
      ],
      '/posts/computer/': [
        {
          text: '计算机 · 真题',
          items: ${JSON.stringify(compYearLinks, null, 12).replace(/\n/g, '\n          ')},
        },
        {
          text: 'C 语言知识点',
          collapsed: false,
          items: ${JSON.stringify(
            compC.map((i) => ({ text: i.title, link: `/posts/computer/notes/${i.slug}` })),
            null,
            12,
          ).replace(/\n/g, '\n          ')},
        },
        {
          text: '数据结构知识点',
          collapsed: false,
          items: ${JSON.stringify(
            compD.map((i) => ({ text: i.title, link: `/posts/computer/notes/${i.slug}` })),
            null,
            12,
          ).replace(/\n/g, '\n          ')},
        },
        {
          text: '2024 考点拆分',
          items: [
            { text: '拆分索引', link: '/posts/computer/topics/' },
            { text: '01 C 语言基础', link: '/posts/computer/topics/01-c-basics' },
            { text: '02 数组指针', link: '/posts/computer/topics/02-array-pointer' },
            { text: '03 链表栈队列', link: '/posts/computer/topics/03-list-stack-queue' },
            { text: '04 树图与查找', link: '/posts/computer/topics/04-tree-graph' },
            { text: '05 手写编程', link: '/posts/computer/topics/05-coding' },
          ],
        },
      ],
      '/posts/english/': [
        {
          text: '英语 · 学习笔记',
          items: [
            { text: '笔记总览', link: '/posts/english/notes/' },
${engNotes.map((i) => `            { text: ${JSON.stringify(i.title)}, link: '/posts/english/notes/${i.slug}' },`).join('\n')}
          ],
        },
        {
          text: '公共英语 · 真题',
          items: [
            { text: '真题总览', link: '/posts/english/' },
${engYearLinks.map((i) => `            { text: ${JSON.stringify(i.text)}, link: '${i.link}' },`).join('\n')}
          ],
        },
      ],
      '/posts/politics/': [
        {
          text: '政治 · 系统笔记',
          items: [
            { text: '笔记总览', link: '/posts/politics/notes/' },
${(politicsNotes || []).map((i) => `            { text: ${JSON.stringify(i.title.length > 16 ? i.title.slice(0, 16) + '…' : i.title)}, link: '/posts/politics/notes/${i.slug}' },`).join('\n')}
          ],
        },
        {
          text: '政治 · 真题演练',
          items: [
            { text: '真题总览', link: '/posts/politics/' },
${polYears.map((y) => `            { text: '${y.year}', link: '/posts/politics/${y.year}' },`).join('\n')}
          ],
        },
      ],
      '/guide/': [
        {
          text: '使用说明',
          items: [
            { text: '站点说明', link: '/guide/' },
            { text: '资料边界', link: '/guide/sources' },
          ],
        },
      ],
    },
    socialLinks: [
      {
        icon: 'github',
        link: 'https://github.com/wpc725562-dotcom/darling016123',
      },
    ],
    footer: {
      message: '仅供个人学习 · 考生回忆版 · 非考试院原卷',
      copyright: '内容整理自公开回忆版与个人 Obsidian 笔记',
    },
    docFooter: {
      prev: '上一篇',
      next: '下一篇',
    },
    lastUpdatedText: '最后更新',
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '菜单',
    darkModeSwitchLabel: '主题',
    lightModeSwitchTitle: '切到浅色',
    darkModeSwitchTitle: '切到深色',
  },
})
`
  if (!DRY_RUN) fs.writeFileSync(path.join(DOCS, '.vitepress/config.mts'), config, 'utf8')
  stats.written++
  stats.files.push('.vitepress/config.mts')
}

// ─────────── guide 轻更 ───────────
function updateGuide() {
  writeFile(
    'guide/index.md',
    `---
title: 站点说明
---

# 站点说明

本站是广东专升本复习笔记的 **VitePress 网页版**，源内容在本地 Obsidian 库：

\`D:/专升本/专升本\`

## 内容从哪来

| 区块 | Obsidian 路径 | 网站路径 |
|:---|:---|:---|
| 高数章节 | \`高等数学/\` | [/posts/math/notes/](/posts/math/notes/) |
| 计算机知识点 | \`计算机程序设计/\` | [/posts/computer/notes/](/posts/computer/notes/) |
| 英语笔记 | \`编程技能/专升本英语/\` | [/posts/english/notes/](/posts/english/notes/) |
| 政治笔记 | \`政治理论/\` | [/posts/politics/notes/](/posts/politics/notes/) |
| 各科真题 | \`历年真题/\` | \`/posts/{math,computer,english,politics}/\` |

重新同步（本地）：

\`\`\`bash
cd "D:/专升本/专升本"
node scripts/sync-obsidian-to-blog.mjs
npm run docs:build
\`\`\`

## 阅读建议

- **刷概念**：章节 / 知识点笔记（含闭卷答案块）
- **刷真题**：2024/2026 完整卷优先，再回溯演练页
- **搜索**：顶栏本地搜索可跨页找公式与关键词

## 主题

樱花二次元主题 + Live2D 参考开源博客 [a3292334877-star/blog](https://github.com/a3292334877-star/blog)。

详见 [资料边界](/guide/sources)。
`,
  )
}

// ─────────── 废弃守卫（2026-09-22 新增）───────────
/**
 * 本脚本的模板已落后于 docs/ 的人工精修内容，直接跑会静默覆盖（见文件头注释）。
 * 守卫在下列任一条件成立时中止，避免「辛苦修完被一次同步回退」：
 *   ① docs/posts/math/notes/ 的 md 数 > 源 高等数学/ 的 md 数（docs 侧已有人工新增）
 *   ② docs/.vitepress/config.mts 含 sync 模板不产出的人工内容标志（日语 / 学习手册 / manifest）
 *
 * 逃生舱（确实要同步时）：
 *   node scripts/sync-obsidian-to-blog.mjs --dry-run --force   # 先看影响面，不落盘
 *   node scripts/sync-obsidian-to-blog.mjs --force             # 真写
 * 跑前务必 git stash 或提交；跑后 git diff --stat 逐文件核对。
 */
function guardDeprecated() {
  if (process.argv.includes('--force') || process.env.SYNC_FORCE === '1') {
    console.warn('⚠️  --force：跳过废弃守卫，后果自负。建议先 git stash，跑完 git diff --stat 核对。')
    return
  }

  const reasons = []

  const srcMath = listMd(path.join(ROOT, '高等数学'))
  const docsMath = listMd(path.join(DOCS, 'posts/math/notes'))
  if (docsMath.length > srcMath.length) {
    reasons.push(
      `docs/posts/math/notes/ 有 ${docsMath.length} 个 md，源 高等数学/ 只有 ${srcMath.length} 个` +
        ` ⇒ 已分叉 ${docsMath.length - srcMath.length} 个，docs 侧有人工新增内容`,
    )
  }

  const cfgPath = path.join(DOCS, '.vitepress/config.mts')
  if (fs.existsSync(cfgPath)) {
    const cfg = read(cfgPath)
    const hit = ['日语', '学习手册', 'manifest'].filter((m) => cfg.includes(m))
    if (hit.length) {
      reasons.push(
        `docs/.vitepress/config.mts 含人工内容标志：${hit.join(' / ')}` +
          ' —— sync 重建整个 sidebar 时会删掉它们',
      )
    }
  }

  if (!reasons.length) return

  console.error('')
  console.error('🛑 已阻止 docs:sync —— 本脚本会覆盖 docs/ 的人工精修内容')
  console.error('')
  reasons.forEach((r, i) => console.error(`   ${i + 1}. ${r}`))
  console.error('')
  console.error('   docs/ 才是站点事实源；本脚本模板已落后（见文件头注释）。')
  console.error('   实测跑一次会删掉 PWA 配置、日语板块、四科「学习手册」导航（-290 行）。')
  console.error('')
  console.error('   确实要跑：')
  console.error('     git stash                                                  # 或先提交')
  console.error('     node scripts/sync-obsidian-to-blog.mjs --dry-run --force   # 先看影响面')
  console.error('     node scripts/sync-obsidian-to-blog.mjs --force             # 真写')
  console.error('     git diff --stat                                            # 逐文件核对')
  console.error('')
  process.exit(1)
}

// ─────────── main ───────────
function main() {
  guardDeprecated()
  console.log(DRY_RUN ? '🔄 Sync Obsidian → VitePress（dry-run · 不落盘）…' : '🔄 Sync Obsidian → VitePress …')

  const mathChapters = syncMathNotes()
  const computerNotes = syncComputerNotes()
  const engNotes = syncEnglishNotes()
  const politicsNotes = syncPoliticsNotes()

  const mathYears = syncYearPapers(
    'math',
    path.join(ROOT, '历年真题/高等数学'),
    'posts/math',
    { skipYears: ['2024', '2026'], label: '高等数学' },
  )
  // 确保 2024/2026 仍在列表
  if (!mathYears.find((y) => y.year === '2024')) mathYears.unshift({ year: '2024', status: 'kept' })
  if (!mathYears.find((y) => y.year === '2026')) mathYears.unshift({ year: '2026', status: 'kept' })
  mathYears.sort((a, b) => Number(b.year) - Number(a.year))

  const compYears = syncYearPapers(
    'computer',
    path.join(ROOT, '历年真题/计算机程序设计'),
    'posts/computer',
    { skipYears: ['2024'], label: '计算机程序设计' },
  )
  if (!compYears.find((y) => y.year === '2024')) compYears.unshift({ year: '2024', status: 'kept' })
  compYears.sort((a, b) => Number(b.year) - Number(a.year))

  const polYears = syncYearPapers(
    'politics',
    path.join(ROOT, '历年真题/政治理论'),
    'posts/politics',
    { skipYears: [], label: '政治理论' },
  )

  updateIndexes({ mathChapters, computerNotes, mathYears, compYears, polYears, engNotes, politicsNotes })
  updateHome()
  updateGuide()
  writeConfig({ mathChapters, computerNotes, mathYears, compYears, polYears, engNotes, politicsNotes })

  console.log(JSON.stringify({ dryRun: DRY_RUN, written: stats.written, skipped: stats.skipped, sample: stats.files.slice(0, 20) }, null, 2))
  console.log(
    DRY_RUN
      ? `✅ dry-run 完成 · 将写 ${stats.written} files · skipped ${stats.skipped}（未落盘）`
      : `✅ done · wrote ${stats.written} files · skipped ${stats.skipped}`,
  )
}

main()
