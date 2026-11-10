#!/usr/bin/env node
/**
 * 政治考点 → 「骨架 + 三层挖空」练习页
 *
 * 为什么要有这个脚本：
 *   政治大题的问题从来不是「没看过」，是「看着眼熟、闭卷写不出」。
 *   抄一遍笔记的收益接近 0（手在动、脑子没动）。真正有效的只有一件事：
 *   给一个残缺的骨架，让人把缺的部分补回去，再对答案。
 *
 *   三层不是难度分级，是三种不同的提取强度：
 *     L1 只挖名词 —— 考「记不记得有这几个词」
 *     L2 挖半句   —— 考「知不知道该接哪半句」
 *     L3 只留标题 —— 考「能不能整段复述」
 *   从 L1 到 L3 是同一段话被剥三次，不是三段不同的话。这点很关键：
 *   同源才好定位，才知道自己到底断在第几层。
 *
 * 用法：
 *   node scripts/politics-cloze-gen.mjs                     # 全部笔记 → docs/posts/politics/cloze/
 *   node scripts/politics-cloze-gen.mjs 02-毛泽东思想        # 单篇
 *   node scripts/politics-cloze-gen.mjs --check             # 只报告，不写文件
 *
 * 输入：docs/posts/politics/notes/*.md（frontmatter + 正文）
 * 输出：docs/posts/politics/cloze/<原文件名>.md
 *
 * 设计约束（改之前先读）：
 *   1. 不碰原文件。产物只写到 cloze/ 目录。
 *   2. 代码块、mermaid、frontmatter 一律原样保留 —— 挖空挖到代码里就是坏页。
 *   3. 表格只挖单元格，不动表头和分隔行，否则表格渲染不出来。
 *   4. 挖空标记用 `____`（四个半角下划线），不用 `==高亮==`：
 *      高亮是「已经给了答案」，挖空是「要你填」，语义相反。
 */
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const SRC_DIR = path.join(ROOT, 'docs/posts/politics/notes')
const OUT_DIR = path.join(ROOT, 'docs/posts/politics/cloze')

const BLANK = '____'

/** 数字、《文件》、**加粗**、引号内的术语 —— L1 要挖的东西。 */
const L1_PATTERNS = [
  /\*\*([^*]{2,40})\*\*/g, // 加粗术语
  /《([^》]{2,40})》/g, // 文件名 / 会议名
  /(\d{4})\s*年/g, // 年份
  /“([^”]{2,30})”/g, // 引号术语
]

/** 判断这一行能不能挖。返回 false 的行原样保留。 */
function isProtected(line) {
  const t = line.trim()
  if (!t) return true
  if (t.startsWith('#')) return true // 标题：骨架的主体，不能挖
  if (t.startsWith('```')) return true
  if (t.startsWith('|')) return false // 表格交给专门的函数
  if (/^[-*+]\s/.test(t)) return false
  if (/^\d+\.\s/.test(t)) return false
  return false
}

/** L1：只挖名词。加粗词、书名号、年份、引号术语。 */
function blankLevel1(line) {
  let out = line
  for (const re of L1_PATTERNS) {
    out = out.replace(re, (m, inner) => {
      // 书名号和年份保留外壳，只挖里面的内容，这样结构还看得见
      if (m.startsWith('《')) return `《${BLANK}》`
      if (m.startsWith('“')) return `“${BLANK}”`
      if (/^\d{4}\s*年$/.test(m)) return `${BLANK} 年`
      return BLANK
    })
  }
  return out
}

/**
 * L2：挖半句。
 * 按中文标点切，保留第一个分句，后面全挖 —— 保留的部分是「钩子」，
 * 让人知道该往哪个方向接。切不动（没有标点）就退化成 L1。
 */
function blankLevel2(line) {
  const stripped = line.replace(/^\s*([-*+]|\d+\.)\s+/, '')
  const lead = line.slice(0, line.length - stripped.length)
  const parts = stripped.split(/(?<=[，。；：、])/)
  if (parts.length < 2) return blankLevel1(line)
  const keep = parts[0]
  const hidden = parts.slice(1).join('').replace(/[^\s]/g, '_')
  return `${lead}${keep}${hidden}`
}

/** L3：整段只留骨架。非标题正文一律挖成等长的下划线，保留标点位置。 */
function blankLevel3(line) {
  const stripped = line.replace(/^\s*([-*+]|\d+\.)\s+/, '')
  const lead = line.slice(0, line.length - stripped.length)
  const hidden = stripped.replace(/[^\s，。；：、？！]/g, '_')
  return `${lead}${hidden}`
}

/** 表格：表头 + 分隔行原样，数据行按层挖单元格。 */
function blankTableRow(line, level) {
  const cells = line.split('|')
  return cells
    .map((cell, i) => {
      if (i === 0 || i === cells.length - 1) return cell // 首尾空壳
      if (/^\s*:?-{3,}:?\s*$/.test(cell)) return cell // 分隔行
      const body = cell.trim()
      if (!body) return cell
      if (level === 1) return ` ${blankLevel1(body)} `
      if (level === 2) return ` ${blankLevel2(body)} `
      return ` ${body.replace(/[^\s]/g, '_')} `
    })
    .join('|')
}

/** 把一篇笔记的正文按层处理。返回 { l1, l2, l3 } 三段 markdown。 */
function buildLayers(body) {
  const lines = body.split(/\r?\n/)
  const out = { 0: [], 1: [], 2: [], 3: [] }
  let inFence = false
  let headerDone = false // 表格：前两行（表头+分隔）原样放过
  let h1Skipped = false // 正文自己的 H1 要丢掉：页面标题已经渲染过一次了

  for (const line of lines) {
    if (line.trim().startsWith('```')) {
      inFence = !inFence
      for (const lv of [0, 1, 2, 3]) out[lv].push(line)
      continue
    }
    if (inFence) {
      for (const lv of [0, 1, 2, 3]) out[lv].push(line)
      continue
    }

    if (!h1Skipped && /^#\s/.test(line.trim())) {
      h1Skipped = true
      for (const lv of [0, 1, 2, 3]) out[lv].push('')
      continue
    }

    // 引用块：原文里是口诀和「一句话总结」，往往直接写着答案。
    // L1 留着（第一次看需要钩子），L2/L3 一律挖 —— 不然翻到第三层答案还挂在那儿。
    if (line.trim().startsWith('>')) {
      out[0].push(line)
      out[1].push(line)
      out[2].push(blankLevel2(line))
      out[3].push(blankLevel3(line))
      continue
    }

    if (line.trim().startsWith('|')) {
      const isSep = /^\s*\|[\s:|-]+\|\s*$/.test(line)
      if (isSep || !headerDone) {
        for (const lv of [0, 1, 2, 3]) out[lv].push(line)
        if (isSep) headerDone = true
        continue
      }
      out[0].push(line)
      out[1].push(blankTableRow(line, 1))
      out[2].push(blankTableRow(line, 2))
      out[3].push(blankTableRow(line, 3))
      continue
    }
    headerDone = false

    if (isProtected(line)) {
      for (const lv of [0, 1, 2, 3]) out[lv].push(line)
      continue
    }

    out[0].push(line)
    out[1].push(blankLevel1(line))
    out[2].push(blankLevel2(line))
    out[3].push(blankLevel3(line))
  }

  // out[0] 是原文、out[3] 是 L3，两者逐行 push，索引严格对齐 ——
  // 下游（politics-cloze-anki.py）靠这个对齐关系配对，不要打乱 push 顺序。
  return { l1: out[1].join('\n'), l2: out[2].join('\n'), l3: out[3].join('\n'), raw: out[0].join('\n'), lines: out }
}

/** 统计挖空数量，用作「这页到底有没有挖到东西」的判据。 */
function countBlanks(md) {
  return (md.match(new RegExp(BLANK, 'g')) || []).length
}

function parseFrontmatter(src) {
  const m = src.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/)
  if (!m) return { fm: '', body: src }
  return { fm: m[1], body: src.slice(m[0].length) }
}

function titleOf(fm, fallback) {
  const m = fm.match(/^title:\s*"?(.*?)"?\s*$/m)
  return m ? m[1] : fallback
}

function render(name, fm, layers, stats) {
  const title = titleOf(fm, name)
  return `---
title: "${title} · 挖空练习"
description: "政治理论 · ${title} · 骨架与三层挖空"
category: "politics-cloze"
tags:
  - 政治理论
  - 挖空
---

# ${title} · 挖空练习

> 同一段话剥三层。**先做 L3，做不动再往下退** —— 顺序反过来会骗自己：
> L1 做对了不代表记住了，只代表「这几个词有印象」。

| 层 | 挖了什么 | 什么时候用 |
|:--|:--|:--|
| L1 | 只有名词 | 第一次接触，或考前扫一遍 |
| L2 | 每句只留前半 | 判断「知不知道接哪半句」 |
| L3 | 只留标题和标点 | 检验能不能整段复述 |

本页挖空数：L1 **${stats.l1}** · L2 **${stats.l2}** · L3 **${stats.l3}**

---

## L1 · 只挖名词

${layers.l1}

---

## L2 · 每句留前半

${layers.l2}

---

## L3 · 只留骨架

${layers.l3}

---

## 原文

<details>
<summary>点开对照（先做完再看）</summary>

${layers.raw}

</details>
`
}

function main() {
  const args = process.argv.slice(2)
  const checkOnly = args.includes('--check')
  const target = args.find((a) => !a.startsWith('--'))

  if (!fs.existsSync(SRC_DIR)) {
    console.error(`源目录不存在：${SRC_DIR}`)
    process.exit(1)
  }

  const files = fs
    .readdirSync(SRC_DIR)
    .filter((f) => f.endsWith('.md') && f !== 'index.md')
    // 真题集不挖：挖真题等于把卷子变成填空题，既不像卷子也不像考点。
    // 真题的正确用法是整卷计时做，见 05-练习与真题。
    .filter((f) => !f.startsWith('真题-'))
    .filter((f) => !target || f.includes(target))

  if (files.length === 0) {
    console.error(target ? `没有匹配「${target}」的笔记` : '源目录里没有 .md')
    process.exit(1)
  }

  if (!checkOnly && !fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true })

  let written = 0
  const report = []
  const pairs = []

  for (const file of files) {
    const src = fs.readFileSync(path.join(SRC_DIR, file), 'utf8')
    const { fm, body } = parseFrontmatter(src)
    const layers = buildLayers(body)
    layers.raw = body

    const stats = {
      l1: countBlanks(layers.l1),
      l2: countBlanks(layers.l2),
      l3: countBlanks(layers.l3),
    }

    // 判据：三层必须逐层变多。相等说明这一篇没有可挖的结构（比如全是表格短词），
    // 写出来也是废页，直接报出来让人看一眼，不静默通过。
    const monotonic = stats.l1 <= stats.l2 && stats.l2 <= stats.l3
    report.push({ file, ...stats, monotonic })

    if (checkOnly) continue

    const out = render(file.replace(/\.md$/, ''), fm, layers, stats)
    fs.writeFileSync(path.join(OUT_DIR, file), out, 'utf8')
    written++

    // 同时吐一份配对表给 politics-cloze-anki.py。让它读 JSON 而不是回头解析
    // markdown —— 页面里有 `---` 分隔线、<details> 包裹，按行数对齐会差几行，
    // 按索引配对才是唯一可靠的（两边是同一个数组切出来的）。
    //
    // ★ 卡用 L2 不用 L3：L3 整行挖空，正面只剩一排下划线，翻面之前没有任何
    //   可提取的线索。L2 保留第一个分句当钩子，才构成「给半句、补半句」的提取练习。
    const stem = file.replace(/\.md$/, '')
    for (let i = 0; i < layers.lines[2].length; i++) {
      const front = layers.lines[2][i].trim()
      const back = layers.lines[0][i].trim()
      if (!front || !back) continue
      if (!front.includes(BLANK)) continue
      if (front.startsWith('#') || front.startsWith('|')) continue
      if (back.length < 12) continue
      // 引用块（`> 🎯 一句话…`、口诀）不当答案：它是总结，不是被挖的那句话。
      if (back.startsWith('>')) continue
      // 正面必须还剩「钩子」。整行被挖成 `_ __ ___` 的卡没有提取价值 ——
      // 学习者看到一排下划线，除了翻面没有别的动作可做。
      const readable = front.replace(/[_\s，。；：、？！（）()《》「」“”"'\-—|>#*]/g, '')
      if (readable.length < 6) continue
      pairs.push({ front, back, source: stem })
    }
  }

  console.log(`\n=== 政治挖空生成 ===`)
  console.log(`源：${files.length} 篇 · 输出：${checkOnly ? '未写（--check）' : `${written} 篇 → ${OUT_DIR}`}`)

  if (!checkOnly) {
    const pairFile = path.join(OUT_DIR, '_pairs.json')
    fs.writeFileSync(pairFile, JSON.stringify(pairs, null, 0), 'utf8')
    console.log(`配对表：${pairs.length} 对 → ${path.relative(ROOT, pairFile)}（供 Anki 加卡用）`)
  }
  console.log(`\n${'文件'.padEnd(34)} L1   L2   L3   递增`)
  for (const r of report) {
    const flag = r.monotonic ? '' : '  ← 不递增'
    console.log(
      `${r.file.padEnd(34)} ${String(r.l1).padStart(3)}  ${String(r.l2).padStart(3)}  ${String(r.l3).padStart(3)}${flag}`
    )
  }

  const bad = report.filter((r) => !r.monotonic)
  if (bad.length) {
    console.log(`\n⚠️ ${bad.length} 篇三层不递增，产物可能没有练习价值，逐篇看一眼。`)
    process.exit(2)
  }
  console.log(`\n✅ 全部 ${report.length} 篇三层递增，挖空有效。`)
}

main()
