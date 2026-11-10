#!/usr/bin/env node
/**
 * 生成 `/tags/` 标签索引页（横向入口）。
 *
 * 为什么是**单页**而不是「每个标签一页」：
 *   本库只有 39 个标签、每标签平均 ~10 页。拆成 39 个路由会多出 39 个
 *   「只在正文被引用、没有 sidebar 入口」的黄灯页（check-nav-coverage 会全报 nav-missing）。
 *   单页 + 右侧 outline 已经是完整的横向入口，且零新增孤立页。
 *
 * 用法：
 *   node scripts/gen-tags.mjs            # 生成
 *   node scripts/gen-tags.mjs --check    # 只校验已生成内容是否最新（CI 用）
 */
import fs from 'node:fs'
import path from 'node:path'
import { VOCAB, YEARS } from './tags-vocabulary.mjs'
import { splitFrontmatter, readTags } from './tags-lib.mjs'
import { loadSrcExclude, isExcluded } from './src-exclude.mjs'

const ROOT = process.cwd()
const DOCS = path.join(ROOT, 'docs')
const OUT = path.join(DOCS, 'tags', 'index.md')
const CHECK = process.argv.includes('--check')
const SKIP_DIRS = new Set(['.vitepress', 'public', 'dist', 'node_modules', 'tags'])

// ★ 2026-10-05 修：**必须排除 `srcExclude` 的页面**。
//   这些文件在 docs/ 里躺着，但**不进构建** ⇒ 站点上没有这一页。
//   生成器若不排除，就会把它们写成链接 ⇒ 构建时报 dead link
//   （实测 31 处：`posts/math/notes/index.generated` + 10 份 `audit-*` 审计报告）。
//   ⚠️ 而 `check-links.mjs` 当时**也漏检**这类正文链接（只查了 config 的 link:）
//   ⇒ 生成器与检查器一起错。规则只认 `src-exclude.mjs` 一处。
const EXCLUDE = loadSrcExclude()

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith('.')) continue
    const p = path.join(dir, e.name)
    if (e.isDirectory()) { if (!SKIP_DIRS.has(e.name)) walk(p, out) }
    else if (e.name.endsWith('.md')) out.push(p)
  }
  return out
}

const pages = []
for (const f of walk(DOCS)) {
  const rel = path.relative(DOCS, f).replace(/\\/g, '/')
  if (isExcluded(rel, EXCLUDE)) continue
  const sp = splitFrontmatter(fs.readFileSync(f, 'utf8'))
  if (!sp) continue
  const tags = readTags(sp.fm)
  if (!tags || !tags.length) continue
  const t = sp.fm.match(/^title:[ \t]*(.*)$/m)
  const h1 = sp.tail.match(/^#[ \t]+(.+)$/m)
  const title = (t ? t[1].trim().replace(/^["']|["']$/g, '') : null) || (h1 ? h1[1].trim() : null) || path.basename(rel, '.md')
  const url = '/' + rel.replace(/\.md$/, '').replace(/\/index$/, '/')
  pages.push({ url, title, tags })
}

const byTag = new Map()
for (const p of pages) for (const t of p.tags) {
  if (!byTag.has(t)) byTag.set(t, [])
  byTag.get(t).push(p)
}
for (const arr of byTag.values()) arr.sort((a, b) => a.url.localeCompare(b.url, 'zh'))

const DIMS = [
  ['科目', VOCAB.科目],
  ['类型', VOCAB.类型],
  ['用途', VOCAB.用途],
  ['年份', [...YEARS].reverse()],
]

const L = []
L.push('---')
L.push('title: "标签索引"')
L.push('description: "全站按标签横向检索 —— 科目 / 类型 / 用途 / 年份 四个维度。找到一页之后，从这里跳到同类内容的其它页。"')
L.push('---')
L.push('')
L.push('# 🏷️ 标签索引')
L.push('')
L.push('> ⚙️ 本页由 `scripts/gen-tags.mjs` **自动生成**，请勿手改。')
L.push('> 要调整标签，改页面 frontmatter 的 `tags:`，然后跑 `node scripts/gen-tags.mjs`。')
L.push('> 标签必须在 `scripts/tags-vocabulary.mjs` 的受控词表内，否则 `node scripts/check-tags.mjs` 会**报错退出**。')
L.push('')
L.push(`共 **${pages.length}** 页、**${byTag.size}** 个标签。右侧「本页目录」可直接跳到某个标签。`)
L.push('')

L.push('## 一、按维度浏览')
L.push('')
for (const [name, list] of DIMS) {
  const rows = list.filter((t) => byTag.has(t)).map((t) => `| [${t}](#${t}) | ${byTag.get(t).length} |`)
  if (!rows.length) continue
  L.push(`**${name}**`)
  L.push('')
  L.push('| 标签 | 页数 |')
  L.push('|:--|--:|')
  L.push(...rows)
  L.push('')
}

L.push('## 二、标签详情')
L.push('')
for (const [name, list] of DIMS) {
  for (const t of list) {
    const arr = byTag.get(t)
    if (!arr) continue
    L.push(`### ${t}`)
    L.push('')
    L.push(`<sub>${name} · ${arr.length} 页</sub>`)
    L.push('')
    for (const p of arr) L.push(`- [${p.title}](${p.url})`)
    L.push('')
  }
}

const content = L.join('\n')

if (CHECK) {
  const cur = fs.existsSync(OUT) ? fs.readFileSync(OUT, 'utf8') : ''
  if (cur !== content) { console.error('❌ docs/tags/index.md 不是最新，请跑 node scripts/gen-tags.mjs'); process.exit(1) }
  console.log('✅ docs/tags/index.md 已是最新')
} else {
  fs.mkdirSync(path.dirname(OUT), { recursive: true })
  fs.writeFileSync(OUT, content, 'utf8')
  console.log(`✅ 已生成 docs/tags/index.md · ${pages.length} 页 / ${byTag.size} 标签 / ${content.split('\n').length} 行`)
}
