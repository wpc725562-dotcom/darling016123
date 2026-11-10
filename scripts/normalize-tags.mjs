#!/usr/bin/env node
/**
 * 把全站标签**规范化到受控词表**（2026-10-05）。
 *
 * 做三件事：
 *   1. **丢弃**不在白名单里的标签（长尾：章节名、语法点、题型细目……降级为正文关键词）
 *   2. **按路径前缀注入「科目」**（等价于 mkdocs-material meta 插件的 `.meta.yml` 递归继承）
 *   3. **按文件名补年份**（`2024-英语-刷题版.md` → `2024`）
 *
 * 用法：
 *   node scripts/normalize-tags.mjs            # 干跑，只报告
 *   node scripts/normalize-tags.mjs --write    # 真正写盘
 */
import fs from 'node:fs'
import path from 'node:path'
import { ALLOWED, SUBJECT_RULES, TYPE_RULES, YEAR_RE } from './tags-vocabulary.mjs'
import { splitFrontmatter, readTags, setTags, sameTags, rebuild } from './tags-lib.mjs'

const DOCS = path.join(process.cwd(), 'docs')
const WRITE = process.argv.includes('--write')
const SKIP_DIRS = new Set(['.vitepress', 'public', 'dist', 'node_modules', 'tags'])

function matchRule(rules, rel) {
  for (const [re, tag] of rules) if (re.test(rel)) return tag
  return null
}

const files = []
function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith('.')) continue
    if (e.isDirectory()) { if (!SKIP_DIRS.has(e.name)) walk(path.join(dir, e.name)) }
    else if (e.name.endsWith('.md')) files.push(path.join(dir, e.name))
  }
}
walk(DOCS)

const dropped = new Map()
const added = new Map()
const changed = []
let noFm = 0
let noChange = 0

for (const f of files) {
  const rel = path.relative(DOCS, f).replace(/\\/g, '/')
  const raw = fs.readFileSync(f, 'utf8')
  const sp = splitFrontmatter(raw)
  if (!sp) { noFm++; continue }

  const old = readTags(sp.fm) || []
  const kept = old.filter((t) => ALLOWED.has(t))
  for (const t of old) if (!ALLOWED.has(t)) dropped.set(t, (dropped.get(t) || 0) + 1)

  const subj = matchRule(SUBJECT_RULES, rel)
  const type = matchRule(TYPE_RULES, rel)
  const yearRaw = (path.basename(rel).match(YEAR_RE) || [])[1]
  const year = yearRaw && ALLOWED.has(yearRaw) ? yearRaw : null   // ⚠️ 2027 不在词表内，不能注入

  const next = []
  if (subj) next.push(subj)
  if (type && !next.includes(type)) next.push(type)
  for (const t of kept) if (!next.includes(t)) next.push(t)
  if (year && !next.includes(year)) next.push(year)

  for (const t of next) if (!old.includes(t)) added.set(t, (added.get(t) || 0) + 1)

  if (next.length === 0) continue                      // 无科目也无所属 ⇒ 不动
  if (sameTags(old, next)) { noChange++; continue }

  changed.push({ rel, old, next })
  if (WRITE) {
    const out = rebuild(sp, setTags(sp.fm, next, sp.nl))

    // ── 写盘前的三道自检（上一次就是缺了它们才把 425 个文件写坏）──────────
    //   1. 重建后仍能解析出 frontmatter（说明开头的 `---` 没丢）
    //   2. **正文部分逐字节未变**（最硬的一条：改标签绝不该碰到正文）
    //   3. 读回来的 tags 与预期完全一致
    const chk = splitFrontmatter(out)
    if (!chk) throw new Error(`自检失败（frontmatter 丢失）：${rel}`)
    if (chk.tail !== sp.tail) throw new Error(`自检失败（正文被改动）：${rel}`)
    if (!sameTags(readTags(chk.fm), next)) throw new Error(`自检失败（tags 回读不一致）：${rel}`)

    fs.writeFileSync(f, out, 'utf8')
  }
}

console.log(`扫描 md ${files.length} · 无 frontmatter 跳过 ${noFm} · 已合规 ${noChange} · 需改动 ${changed.length}`)
console.log(`模式：${WRITE ? '✍️  已写盘' : '🔍 干跑（加 --write 才落盘）'}`)

console.log(`\n--- 丢弃的长尾标签（Top 30 / 共 ${dropped.size} 种）---`)
for (const [k, c] of [...dropped.entries()].sort((a, b) => b[1] - a[1]).slice(0, 30)) console.log(`  ${String(c).padStart(3)}  ${k}`)

console.log(`\n--- 新注入的标签 ---`)
for (const [k, c] of [...added.entries()].sort((a, b) => b[1] - a[1])) console.log(`  ${String(c).padStart(3)}  ${k}`)

console.log('\n--- 前 15 个改动样例 ---')
for (const c of changed.slice(0, 15)) {
  console.log(`  ${c.rel}`)
  console.log(`     旧: ${c.old.join(' / ') || '(无)'}`)
  console.log(`     新: ${c.next.join(' / ')}`)
}

if (!WRITE && changed.length) console.log('\n（干跑结束，未写盘）')
