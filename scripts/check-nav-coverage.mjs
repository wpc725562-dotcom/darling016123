#!/usr/bin/env node
/**
 * 反向检查：docs/ 里哪些页面「没有导航入口」。
 *
 * ── 为什么需要它 ────────────────────────────────────────────────────────
 * `check-links.mjs` 只做**正向**验证：导航里写的链接，目标文件存在吗？
 * 它永远发现不了反向问题：**页面存在，但没有任何导航指向它**。
 * 这类页面照常构建、能被站内搜索到、正文之间互相引用，但用户从侧边栏找不到。
 *
 * ── 两个关键设计（都是踩过坑才加的）────────────────────────────────────
 * 1. `srcExclude` **从 config.mts 解析**，不硬编码复刻。
 *    硬编码的副本会随 config 漂移，最后报出一堆假孤儿。
 *
 * 2. 区分两种"孤儿"，严重性差一个数量级：
 *      · `nav-missing`    —— 没有导航入口，但**别的页面正文链到了它** ⇒ 可达到，属体验问题
 *      · `unreachable`    —— 连正文都没引用 ⇒ 真的到不了，属缺陷
 *    只按「不在 config 里」就断言"不可达"是错的：本库实测有 11 个页面
 *    被 section index 的汇总表链着，一直点得到，只是没进 sidebar。
 *
 * ── 用法 ────────────────────────────────────────────────────────────────
 *   node scripts/check-nav-coverage.mjs            # 报告，永远退出 0
 *   node scripts/check-nav-coverage.mjs --strict   # 存在 unreachable 则退出 1
 *   node scripts/check-nav-coverage.mjs --json     # 机器可读
 */
import fs from 'node:fs'
import path from 'node:path'

const ROOT = process.cwd()
const DOCS = path.join(ROOT, 'docs')
const CFG = path.join(DOCS, '.vitepress', 'config.mts')

const argv = process.argv.slice(2)
const STRICT = argv.includes('--strict')
const JSON_OUT = argv.includes('--json')

/* ---------- 1. 解析 config.mts ---------- */

const cfg = fs.readFileSync(CFG, 'utf8')

/** 取出 `srcExclude: [ ... ]` 块里的字符串字面量 */
function parseSrcExclude(src) {
  const i = src.indexOf('srcExclude')
  if (i < 0) return []
  const start = src.indexOf('[', i)
  const end = src.indexOf(']', start)
  if (start < 0 || end < 0) return []
  const block = src.slice(start + 1, end)
  return [...block.matchAll(/'([^']+)'|"([^"]+)"/g)].map((m) => m[1] || m[2])
}

/** 取出所有导航链接（nav + sidebar 的 link: 值） */
function parseNavLinks(src) {
  const out = new Set()
  for (const m of src.matchAll(/["']?link["']?\s*:\s*['"]([^'"]+)['"]/g)) out.add(m[1])
  return out
}

const EXCLUDE_GLOBS = parseSrcExclude(cfg)
const NAV_LINKS = parseNavLinks(cfg)

/* ---------- 2. glob → RegExp（支持 ** * ?） ---------- */

function globToRe(g) {
  let re = ''
  for (let i = 0; i < g.length; i++) {
    const c = g[i]
    if (c === '*') {
      if (g[i + 1] === '*') { re += '.*'; i++ ; if (g[i + 1] === '/') i++ }
      else re += '[^/]*'
    } else if (c === '?') re += '[^/]'
    else re += c.replace(/[.+^${}()|[\]\\]/g, '\\$&')
  }
  return new RegExp('^' + re + '$')
}
const EXCLUDE_RES = EXCLUDE_GLOBS.map(globToRe)

/* ---------- 3. 遍历 docs ---------- */

function walk(dir, out = []) {
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const n = ent.name
    if (n.startsWith('.') || n === 'node_modules' || n === 'dist' || n === 'cache') continue
    const p = path.join(dir, n)
    if (ent.isDirectory()) walk(p, out)
    else if (n.endsWith('.md')) out.push(p)
  }
  return out
}

const allMd = walk(DOCS)
const pages = []
for (const f of allMd) {
  const rel = path.relative(DOCS, f).replace(/\\/g, '/')
  if (EXCLUDE_RES.some((re) => re.test(rel))) continue
  pages.push({ file: f, rel })
}

/* ---------- 4. slug 归一 ---------- */

const norm = (s) =>
  String(s).replace(/^\/+/, '').replace(/\.md$/, '').replace(/\/index$/, '').replace(/\/+$/, '')

const navSlugs = new Set([...NAV_LINKS].map(norm))

/* ---------- 5. 正文引用图 ---------- */

const inbound = new Map() // slug -> Set(引用方 rel)
for (const { file, rel } of pages) {
  const text = fs.readFileSync(file, 'utf8')
  const self = norm(rel)
  for (const m of text.matchAll(/\]\(([^)\s]+?)(?:#[^)]*)?\)/g)) {
    let target = m[1]
    if (/^(https?:|mailto:|#)/.test(target)) continue
    if (target.startsWith('.')) {
      // 相对路径 → 基于当前文件目录解析
      target = path.posix.normalize(path.posix.join(path.posix.dirname(rel), target))
    }
    const slug = norm(target)
    if (slug === self) continue
    if (!inbound.has(slug)) inbound.set(slug, new Set())
    inbound.get(slug).add(rel)
  }
}

/* ---------- 6. 判定 ---------- */

/** 首页 docs/index.md 服务在 `/`，本来就不该出现在任何 sidebar 里 */
const HOME = 'index'

const orphans = []
for (const { rel } of pages) {
  const slug = norm(rel)
  if (slug === HOME) continue
  if (navSlugs.has(slug)) continue
  // 目录型页面：/posts/xxx/index.md → slug 'posts/xxx'
  const refs = inbound.get(slug) || new Set()
  orphans.push({
    rel,
    slug,
    kind: refs.size > 0 ? 'nav-missing' : 'unreachable',
    refs: [...refs],
  })
}

const unreachable = orphans.filter((o) => o.kind === 'unreachable')
const navMissing = orphans.filter((o) => o.kind === 'nav-missing')

/* ---------- 7. 输出 ---------- */

if (JSON_OUT) {
  console.log(JSON.stringify({ checked: pages.length, total: allMd.length, navMissing, unreachable }, null, 2))
} else {
  console.log(`纳入检查: ${pages.length} / 全部 md ${allMd.length}`)
  console.log(`已解析 srcExclude ${EXCLUDE_GLOBS.length} 条 · 导航链接 ${NAV_LINKS.size} 条\n`)

  const group = (arr) => {
    const by = {}
    for (const o of arr) {
      const d = o.rel.split('/').slice(0, -1).join('/') || '.'
      ;(by[d] ||= []).push(o)
    }
    return Object.entries(by).sort()
  }

  if (unreachable.length) {
    console.log(`🔴 真不可达（无导航入口 + 无正文引用）: ${unreachable.length}`)
    for (const [d, arr] of group(unreachable)) {
      console.log(`  【${d}】`)
      for (const o of arr) console.log(`    - ${o.rel.split('/').pop()}`)
    }
    console.log()
  } else {
    console.log('🔴 真不可达: 0 ✅\n')
  }

  if (navMissing.length) {
    console.log(`🟡 无导航入口（但正文有引用，可达到）: ${navMissing.length}`)
    for (const [d, arr] of group(navMissing)) {
      console.log(`  【${d}】${arr.length} 篇`)
      for (const o of arr.slice(0, 4)) {
        console.log(`    - ${o.rel.split('/').pop()}  ← 被 ${o.refs.length} 处引用`)
      }
      if (arr.length > 4) console.log(`    … 另 ${arr.length - 4} 篇`)
    }
    console.log()
  } else {
    console.log('🟡 无导航入口: 0 ✅')
  }

  console.log('提示：加 sidebar 条目可消掉 🟡；🔴 应优先处理。')
}

if (STRICT && unreachable.length) {
  console.error(`\n✗ --strict：存在 ${unreachable.length} 个不可达页面`)
  process.exit(1)
}
