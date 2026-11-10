#!/usr/bin/env node
/**
 * 验证「标签真的进了本地搜索索引」（**产物层**校验，2026-10-05 新增）。
 *
 * 为什么需要单独一个脚本：
 *   2026-10-05 给本地搜索加「标签可被搜到」时，写法**构建通过、检查器全绿，但功能完全没生效** ——
 *   原写法把标签当 markdown 标题拼到 HTML 最前面，而 VitePress 的
 *   `splitPageIntoSections()` **第一句就是 `result.shift()`**，把「第一个标题之前的内容」整块丢掉。
 *   ⇒ 拼了等于没拼。`check-links` / `check-md-hazards` / `health` **一个都测不出**这类问题：
 *   它们检查「链接通不通、语法炸不炸」，不是「功能有没有生效」。
 *
 * 本脚本的口径（**可证伪**）：
 *   找「标签词**不出现在自己正文**里」的页面（标签只写在 frontmatter，而 frontmatter 不进渲染结果），
 *   然后在**构建产物**的搜索索引里搜这个标签，断言这些页面能被命中，
 *   且**命中字段是 `text`**（不是 title/titles —— 那说明命中的是标题，不是我们注入的标签）。
 *
 * 前置：必须先跑过一次构建（需要 `dist/assets/chunks/@localSearchIndexroot.*.js`）。
 *
 * 用法：
 *   node scripts/check-search-tags.mjs            # 抽样 12 个页/标签对
 *   node scripts/check-search-tags.mjs --all      # 全量
 *   node scripts/check-search-tags.mjs --json
 */
import fs from 'node:fs'
import path from 'node:path'
import { pathToFileURL } from 'node:url'
import MiniSearch from 'minisearch'
import { loadSrcExclude, isExcluded } from './src-exclude.mjs'
import { splitFrontmatter, readTags } from './tags-lib.mjs'

const ROOT = process.cwd()
const DOCS = path.join(ROOT, 'docs')
const CHUNKS = path.join(DOCS, '.vitepress', 'dist', 'assets', 'chunks')
const SAMPLE = process.argv.includes('--all') ? Infinity : 12
const JSON_OUT = process.argv.includes('--json')
const SKIP_DIRS = new Set(['.vitepress', 'public', 'dist', 'node_modules', 'tags', 'updates'])

if (!fs.existsSync(CHUNKS)) {
  console.error('❌ 找不到构建产物目录：' + path.relative(ROOT, CHUNKS))
  console.error('   请先跑一次构建（node scripts/build-docs.mjs --no-trash），本脚本只校验**产物**。')
  process.exit(1)
}
const idxFile = fs.readdirSync(CHUNKS).find((x) => x.startsWith('@localSearchIndexroot'))
if (!idxFile) {
  console.error('❌ 构建产物里没有 @localSearchIndexroot.*.js（本地搜索被关掉了？）')
  process.exit(1)
}

/* ---------- 1. 找「标签词不在自己正文里」的页/标签对 ---------- */
const EXCLUDE = loadSrcExclude()
const cases = []
;(function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith('.')) continue
    const p = path.join(dir, e.name)
    if (e.isDirectory()) {
      if (!SKIP_DIRS.has(e.name)) walk(p)
      continue
    }
    if (!e.name.endsWith('.md')) continue
    const rel = path.relative(DOCS, p).split(path.sep).join('/')
    if (isExcluded(rel, EXCLUDE)) continue
    const sp = splitFrontmatter(fs.readFileSync(p, 'utf8'))
    if (!sp) continue
    const tags = readTags(sp.fm)
    if (!tags || !tags.length) continue
    const route = '/' + rel.replace(/\.md$/, '').replace(/\/index$/, '/')
    for (const t of tags) {
      // 正文（tail，不含 frontmatter）里没有这个标签词 ⇒ 命中只可能来自注入
      if (!sp.tail.includes(t)) cases.push({ route, tag: t })
    }
  }
})(DOCS)

if (!cases.length) {
  console.log('⚠️ 没有找到「标签词不在正文里」的页/标签对 —— 无法证伪，跳过。')
  process.exit(0)
}

/* ---------- 2. 载入产物索引，逐个搜 ---------- */
const mod = await import(pathToFileURL(path.join(CHUNKS, idxFile)).href)
const ms = MiniSearch.loadJSON(mod.default, {
  fields: ['title', 'titles', 'text'],
  storeFields: ['title', 'titles'],
})

const picked = cases.length > SAMPLE ? cases.filter((_, i) => i % Math.ceil(cases.length / SAMPLE) === 0).slice(0, SAMPLE) : cases
const fails = []
const results = []
for (const c of picked) {
  const base = '/darling016123' + (c.route.endsWith('/') ? c.route.slice(0, -1) : c.route)
  const hits = ms.search(c.tag).filter((x) => x.id === base || x.id.startsWith(base + '#'))
  const byText = hits.find((x) => JSON.stringify(x.match || {}).includes('"text"'))
  const ok = Boolean(byText)
  if (!ok) fails.push(c)
  results.push({ route: c.route, tag: c.tag, ok, matched: hits.length })
}

if (JSON_OUT) {
  console.log(JSON.stringify({ indexFile: idxFile, total: cases.length, sampled: picked.length, fails, results }, null, 2))
} else {
  console.log('=== 标签是否真的进了搜索索引（产物层校验）===')
  console.log('索引文件: ' + idxFile)
  console.log('「标签词不在正文里」的页/标签对: ' + cases.length + '（抽样 ' + picked.length + '）')
  console.log('')
  for (const r of results) {
    console.log((r.ok ? '✅' : '❌') + ' 搜[' + r.tag + '] → ' + r.route + '  （命中 ' + r.matched + ' 节）')
  }
  if (fails.length) {
    console.error('\n❌ ' + fails.length + ' 个抽样未被标签命中 ⇒ 「标签进搜索」没有真正生效。')
    console.error('   检查 docs/.vitepress/config.mts 的 search.options._render：')
    console.error('   · 标签必须注入到**第一个标题之后**（注入到 HTML 最前面会被 splitPageIntoSections 的 result.shift() 丢掉）')
    console.error('   · 注入形式要能被 clearHtmlTags() 保留文字（如 <span hidden>标签</span>）')
  } else {
    console.log('\n✅ 全部抽样命中，且命中字段为 `text` ⇒ 标签确实进了被索引的正文。')
  }
}
process.exit(fails.length ? 1 : 0)
