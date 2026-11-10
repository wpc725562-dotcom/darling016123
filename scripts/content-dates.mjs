#!/usr/bin/env node
/**
 * 「站点内容页 + 各自最后修改时间」的**唯一**采集入口（2026-10-05 抽出）。
 *
 * 为什么要有这个模块：
 *   「最新内容日期」这件事有两个消费方 ——
 *     ① `gen-updates.mjs`：生成 `/updates/` 按周时间线 + RSS；
 *     ② `sync-home-stats.mjs`：把首页横幅「内容更新至 X」写成**自动**的
 *        （原来手写在 `docs/index.md` 里，2026-10-05 发现还停在 09-21，落后半个月）。
 *   两处各写一份取日期的逻辑 ⇒ 迟早给出两个不同的「最新日期」。
 *
 * 口径（三条，缺一不可）：
 *   1. **`srcExclude` 的页不算** —— 它们不进构建，站点上不存在（见 `src-exclude.mjs`）；
 *   2. 生成物目录（`tags/` `updates/`）不算 —— 否则列表**自我污染**（每次重跑都刷新自己）；
 *   3. 时间取「**git 提交时间**」与「**文件 mtime**」里**较晚者** ——
 *      只用 git 会让**未提交的改动看不见**，只用 mtime 会在换机器/重新克隆后全变成克隆时间。
 */
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import { splitFrontmatter } from './tags-lib.mjs'
import { loadSrcExclude, isExcluded } from './src-exclude.mjs'

const SKIP_DIRS = new Set(['.vitepress', 'public', 'dist', 'node_modules', 'tags', 'updates'])

/**
 * 「元页面」—— 站点自身的说明页，不是备考内容。默认从所有日期计算里排除。
 *
 * 目前只有首页 `index.md`。**必须排除，否则会打成一个死循环**：
 *   `sync-home-stats` 每次都会重写首页横幅 ⇒ 首页 mtime 每次都变成「现在」
 *   ⇒ `/updates/` 里首页那条永远是「刚刚改的」（噪声不是信号），
 *   而且每次同步完 `/updates/` 都立刻过期，`updates:gen:check` 永远红。
 *   （2026-10-05 实测踩到：同步首页后 `updates:gen:check` 立刻报不是最新。）
 */
export const META_PAGES = ['index.md']

/** 一次 `git log` 取每个文件的最近提交时间；失败则全部回退 mtime。 */
function loadGitDates(root) {
  const map = new Map()
  try {
    const out = execFileSync(
      'git',
      ['log', '--pretty=format:__C__%cI', '--name-only', '--', 'docs'],
      { cwd: root, encoding: 'utf8', maxBuffer: 256 * 1024 * 1024 }
    )
    let cur = null
    for (const line of out.split('\n')) {
      if (line.startsWith('__C__')) {
        cur = line.slice(5).trim()
        continue
      }
      const p = line.trim()
      if (!p || !p.endsWith('.md')) continue
      if (!map.has(p)) map.set(p, cur) // 第一次出现 = 最近一次提交
    }
  } catch (e) {
    console.warn('⚠️ git log 失败，全部回退到 mtime：' + e.message)
  }
  return map
}

/**
 * @param {string} root 仓库根（默认 process.cwd()）
 * @param {{ignore?: string[]}} [opts] `ignore` 是**相对 docs/ 的路径**，默认 `META_PAGES`
 * @returns {{rel:string,url:string,title:string,desc:string,date:string}[]} 按 date 倒序
 */
export function collectContentPages(root = process.cwd(), opts = {}) {
  const DOCS = path.join(root, 'docs')
  const EXCLUDE = loadSrcExclude()
  const ignore = new Set(opts.ignore ?? META_PAGES)
  const gitDate = loadGitDates(root)
  const pages = []

  function handle(p) {
    const rel = path.relative(DOCS, p).replace(/\\/g, '/')
    if (isExcluded(rel, EXCLUDE)) return
    if (ignore.has(rel)) return
    const raw = fs.readFileSync(p, 'utf8')
    const sp = splitFrontmatter(raw)
    const t = sp ? sp.fm.match(/^title:[ \t]*(.*)$/m) : null
    const h1 = sp ? sp.tail.match(/^#[ \t]+(.+)$/m) : null
    const title =
      (t ? t[1].trim().replace(/^["']|["']$/g, '') : null) ||
      (h1 ? h1[1].trim() : null) ||
      path.basename(rel, '.md')
    const d = sp ? sp.fm.match(/^description:[ \t]*(.*)$/m) : null
    const desc = d ? d[1].trim().replace(/^["']|["']$/g, '') : ''
    const g = gitDate.get('docs/' + rel)
    const mtime = fs.statSync(p).mtime.toISOString()
    const date = g && new Date(g) > new Date(mtime) ? g : mtime
    const url = '/' + rel.replace(/\.md$/, '').replace(/\/index$/, '/')
    pages.push({ rel, url, title, desc, date })
  }

  ;(function walk(dir) {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      if (e.name.startsWith('.')) continue
      const p = path.join(dir, e.name)
      if (e.isDirectory()) {
        if (!SKIP_DIRS.has(e.name)) walk(p)
      } else if (e.name.endsWith('.md')) {
        handle(p)
      }
    }
  })(DOCS)

  pages.sort((a, b) => b.date.localeCompare(a.date))
  return pages
}

/**
 * 把 ISO 时间转成**本地** `YYYY-MM-DD`。
 *
 * ★ 为什么不能用 `toISOString().slice(0,10)`：那是 **UTC** 日期。
 *   本机在 GMT+8 ⇒ 早上 8 点前改的东西会算成「昨天」，
 *   与 `/updates/` 的按周分组（用的是**本地** `setHours(0,0,0,0)`）口径不一致。
 *   2026-10-05 实测：本地 05:32 改的首页，`toISOString()` 给出 `2026-10-04`。
 */
export function localDate(iso) {
  const d = new Date(iso)
  return (
    d.getFullYear() +
    '-' +
    String(d.getMonth() + 1).padStart(2, '0') +
    '-' +
    String(d.getDate()).padStart(2, '0')
  )
}

/**
 * 最新一页的日期（**本地** `YYYY-MM-DD`）；没有页面时返回 null。
 * 默认已排除 `META_PAGES`（首页），理由见该常量的注释。
 */
export function latestContentDate(root = process.cwd(), opts = {}) {
  const pages = collectContentPages(root, opts)
  if (!pages.length) return null
  return localDate(pages[0].date)
}

/** 首页横幅用的「内容更新至」日期（= `latestContentDate`，语义别名，便于阅读）。 */
export function latestContentDateForHome(root = process.cwd()) {
  return latestContentDate(root)
}

export { SKIP_DIRS }
