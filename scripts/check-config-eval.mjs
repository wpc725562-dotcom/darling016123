#!/usr/bin/env node
/**
 * `docs/.vitepress/config.mts` 的 **nav / sidebar 结构预检**（2026-10-05）。
 *
 * 为什么需要（而不是「反正构建会报错」）：
 *   config 已 1400+ 行、nav/sidebar 是深度嵌套的对象字面量。**少一个逗号**这类错误
 *   会让整个 `vitepress build` 挂掉，而一次完整构建要 **5 分半** —— 拿 5 分钟换一个
 *   立刻就能知道的答案，非常不划算。本脚本用 `new Function` **真求值**这两个块，
 *   秒级给出结论。
 *
 *   ⚠️ 关键点：**配平检查抓不到缺逗号**。`{ a: 1 b: 2 }` 的花括号是配平的，但语法非法。
 *   所以不能只数括号，必须真的 `new Function` 求值一次。
 *
 * 除语法外还断言三条 VitePress 的硬约束：
 *   1. `nav` 嵌套 **最多两层**（顶层项 → 分组 → 叶子；`NavItemChildren.items` 不能再嵌）；
 *   2. 每个 sidebar 顶层键都有 `items`，且每组都有 `text`；
 *   3. 统计 nav 叶子链接数 / sidebar 顶层键数，供人工比对（不是断言，只打印）。
 *
 * 用法：
 *   node scripts/check-config-eval.mjs          # 预检（失败 exit 1）
 *   node scripts/check-config-eval.mjs --json   # 机器可读
 */
import fs from 'node:fs'
import path from 'node:path'

const ROOT = process.cwd()
const CFG = path.join(ROOT, 'docs', '.vitepress', 'config.mts')
const JSON_OUT = process.argv.includes('--json')

const src = fs.readFileSync(CFG, 'utf8')

/**
 * 从 `from` 起按括号配平切片。**会跳过字符串与行注释**，
 * 否则注释里的 `{` / 字符串里的 `]` 会把配平算错。
 */
function sliceBalanced(from, open, close) {
  let depth = 0
  let started = false
  for (let j = from; j < src.length; j++) {
    const c = src[j]
    if (c === "'" || c === '"' || c === '`') {
      const q = c
      j++
      while (j < src.length && src[j] !== q) {
        if (src[j] === '\\') j++
        j++
      }
      continue
    }
    if (c === '/' && src[j + 1] === '/') {
      while (j < src.length && src[j] !== '\n') j++
      continue
    }
    if (c === open) {
      depth++
      started = true
    } else if (c === close) {
      depth--
      if (started && depth === 0) return src.slice(from, j + 1)
    }
  }
  return null
}

const problems = []

function grab(key, open, close) {
  const k = src.indexOf(key + ': ' + open)
  if (k < 0) {
    problems.push(`找不到 \`${key}: ${open}\`（config 里没有这个块？）`)
    return null
  }
  const from = src.indexOf(open, k)
  const block = sliceBalanced(from, open, close)
  if (!block) {
    problems.push(`${key} 括号不配平（缺 ${close}？）`)
    return null
  }
  try {
    return new Function('return (' + block + ')')()
  } catch (e) {
    problems.push(`${key} 语法非法 —— ${e.message}（**常见原因：对象属性之间少逗号**）`)
    return null
  }
}

const nav = grab('nav', '[', ']')
const sidebar = grab('sidebar', '{', '}')

/* ---------- nav 检查 ---------- */
let navLeaves = 0
let navDepth = 0
if (nav) {
  if (!Array.isArray(nav)) problems.push('nav 不是数组')
  else {
    const maxDepth = (items, d = 0) => {
      let m = d
      for (const it of items) if (it.items) m = Math.max(m, maxDepth(it.items, d + 1))
      return m
    }
    navDepth = maxDepth(nav)
    // 顶层项 = 深度 0；它下面的分组 = 深度 1；叶子的 link 在深度 1 或 2 上。
    if (navDepth > 2) problems.push(`nav 嵌套 ${navDepth} 层，超过 VitePress 上限 2 层`)
    ;(function walk(items) {
      for (const it of items) {
        if (!it.text) problems.push(`nav 有节点缺 \`text\``)
        if (it.link) navLeaves++
        if (it.items) walk(it.items)
      }
    })(nav)
  }
}

/* ---------- sidebar 检查 ---------- */
const sidebarKeys = sidebar ? Object.keys(sidebar) : []
if (sidebar) {
  for (const k of sidebarKeys) {
    const groups = sidebar[k]
    if (!Array.isArray(groups)) {
      problems.push(`sidebar['${k}'] 不是数组`)
      continue
    }
    for (const g of groups) {
      if (!g.text) problems.push(`sidebar['${k}'] 有分组缺 \`text\``)
      if (!Array.isArray(g.items)) problems.push(`sidebar['${k}'] 分组「${g.text}」缺 \`items\``)
    }
  }
}

/* ---------- 输出 ---------- */
const result = {
  ok: problems.length === 0,
  navTopLevel: nav ? nav.length : 0,
  navMaxDepth: navDepth,
  navLeafLinks: navLeaves,
  sidebarKeys: sidebarKeys.length,
  problems,
}

if (JSON_OUT) {
  console.log(JSON.stringify(result, null, 2))
} else {
  console.log('=== config.mts 结构预检 ===')
  console.log(`nav 顶层项 ${result.navTopLevel} 个 · 最大嵌套 ${result.navMaxDepth} 层 · 叶子链接 ${result.navLeafLinks} 条`)
  console.log(`sidebar 顶层键 ${result.sidebarKeys} 个`)
  if (problems.length) {
    console.error('\n❌ 发现 ' + problems.length + ' 个问题：')
    for (const p of problems) console.error('   · ' + p)
  } else {
    console.log('\n✅ nav / sidebar 真求值通过，结构约束全部满足')
  }
}

process.exit(result.ok ? 0 : 1)
