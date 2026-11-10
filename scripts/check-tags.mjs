#!/usr/bin/env node
/**
 * 标签白名单校验 —— **不在受控词表内直接 exit 1**。
 *
 * 抄的是 mkdocs-material tags 插件的 `tags_allowed` 设计：
 * 「若某页面引用了不在白名单内的标签，插件会**停止构建**」。
 * 只 `console.warn` 等于没检查 —— 长尾会悄悄涨回来（本库实测从 121 涨到 251）。
 *
 * 用法：
 *   node scripts/check-tags.mjs          # 有越界标签则退出码 1
 *   node scripts/check-tags.mjs --json
 */
import fs from 'node:fs'
import path from 'node:path'
import { ALLOWED, VOCAB, YEARS } from './tags-vocabulary.mjs'
import { splitFrontmatter, readTags } from './tags-lib.mjs'
import { loadSrcExclude, isExcluded } from './src-exclude.mjs'

const DOCS = path.join(process.cwd(), 'docs')
const JSON_OUT = process.argv.includes('--json')
const SKIP_DIRS = new Set(['.vitepress', 'public', 'dist', 'node_modules', 'tags'])

// ★ 2026-10-05：**与 `gen-tags.mjs` 口径对齐** —— 被 `srcExclude` 排除的页面不进构建，
//   它们不会出现在 `/tags/` 页上，其标签也就不属于「已发布的标签体系」。
//   不排除的后果是**同一件事两个数字**（check-tags 报 370、gen-tags 报 359），
//   而「口径不一致」正是今天 dead-link 事故的根因，不能再留。
const EXCLUDE = loadSrcExclude()

const files = []
const skipped = []
function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith('.')) continue
    const p = path.join(dir, e.name)
    if (e.isDirectory()) { if (!SKIP_DIRS.has(e.name)) walk(p) }
    else if (e.name.endsWith('.md')) {
      const rel = path.relative(DOCS, p).replace(/\\/g, '/')
      if (isExcluded(rel, EXCLUDE)) skipped.push(rel)
      else files.push(p)
    }
  }
}
walk(DOCS)

const bad = new Map()   // tag -> [rel...]
const all = new Map()
let tagged = 0

for (const f of files) {
  const rel = path.relative(DOCS, f).replace(/\\/g, '/')
  const sp = splitFrontmatter(fs.readFileSync(f, 'utf8'))
  if (!sp) continue
  const tags = readTags(sp.fm)
  if (!tags || !tags.length) continue
  tagged++
  for (const t of tags) {
    all.set(t, (all.get(t) || 0) + 1)
    if (!ALLOWED.has(t)) {
      if (!bad.has(t)) bad.set(t, [])
      bad.get(t).push(rel)
    }
  }
}

if (JSON_OUT) {
  console.log(JSON.stringify({ scanned: files.length, skippedBySrcExclude: skipped.length, tagged, distinct: all.size, violations: [...bad].map(([t, p]) => ({ tag: t, pages: p })) }, null, 2))
} else {
  const skipNote = skipped.length ? ` · 已按 srcExclude 跳过 ${skipped.length} 个（不参与构建）` : ''
  console.log(`标签白名单校验：扫描 ${files.length} 个 md${skipNote} · 有标签 ${tagged} 个 · 不同标签 ${all.size} 个`)
  console.log(`受控词表：科目 ${VOCAB.科目.length} + 类型 ${VOCAB.类型.length} + 用途 ${VOCAB.用途.length} + 年份 ${YEARS.length} = ${ALLOWED.size} 个`)
  if (bad.size === 0) {
    console.log('✅ 全部标签都在白名单内')
  } else {
    console.log(`\n❌ 发现 ${bad.size} 个越界标签：`)
    for (const [t, pages] of [...bad].sort((a, b) => b[1].length - a[1].length)) {
      console.log(`   「${t}」 ${pages.length} 处  → ${pages.slice(0, 3).join(', ')}${pages.length > 3 ? ' …' : ''}`)
    }
    console.log('\n修法：改页面 frontmatter 的 tags，或把它加进 scripts/tags-vocabulary.mjs（慎加）。')
  }
}

if (bad.size) process.exit(1)
