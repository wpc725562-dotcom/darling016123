#!/usr/bin/env node
/**
 * `srcExclude` 的唯一解析入口（2026-10-05 抽出）。
 *
 * 为什么要有这个模块：
 *   「哪些 md **不参与构建**」这件事，站内至少 4 个脚本都要知道 ——
 *   `check-md-hazards` / `check-nav-coverage` / `check-links` / 以及生成器
 *   （`gen-tags` / `gen-updates`）。各写一份的下场是**口径漂移**：
 *   2026-10-05 实测，`gen-tags.mjs` 与 `gen-updates.mjs` 都没读 `srcExclude`，
 *   于是把「被排除、站点上不存在」的页面写进了 `/tags/` 与 `/updates/`，
 *   构建时报 **31 处 dead link**；而 `check-links.mjs` 因为**正文链接那一段没套 srcExclude**，
 *   全程沉默、打印「无死链」—— 检查器和生成器一起错，谁也没拦住。
 *
 * ⇒ 规则只有一处：**`docs/.vitepress/config.mts` 的 `srcExclude` 块**。
 *   本模块只做两件事：解析它、判断某个 docs 相对路径是否命中。
 *
 * 用法：
 *   import { loadSrcExclude, isExcluded } from './src-exclude.mjs'
 *   const EX = loadSrcExclude()
 *   if (isExcluded('posts/computer/notes/audit-1.8-指针-审计报告.md', EX)) continue
 */
import { existsSync, readFileSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const CONFIG = join(ROOT, 'docs', '.vitepress', 'config.mts')

/**
 * 读 `config.mts` 的 `srcExclude: [...]`，返回**原始 glob 字符串数组**（相对 docs/，正斜杠）。
 * 取不到就返回空数组（不抛错 —— 检查脚本不应该因为解析失败而崩）。
 *
 * ★★ 必须先剥掉块内的 `//` 行注释，否则会**把注释里的示例路径当成真规则**。
 *    2026-10-05 实测：`srcExclude` 块的注释里写着「`index.md` 是它的严格超集」
 *    与「`.gitignore` 的 `*.bak-*` 只挡 git」——
 *    朴素的「抓所有引号内容」会解析出 17 条（真规则只有 13 条），
 *    其中 `index.md` 这条**会把站点首页排除掉**，`check-links` 随即把
 *    「指向首页的链接」误报成死链。注释里的反引号同样会被当成引号。
 *    ⇒ 先按行去掉 `//` 之后的内容，再抽引号。
 */
export function loadSrcExcludePatterns() {
  if (!existsSync(CONFIG)) return []
  const text = readFileSync(CONFIG, 'utf-8')
  const m = text.match(/srcExclude\s*:\s*\[([\s\S]*?)\]/)
  if (!m) return []
  const body = m[1]
    .split(/\r?\n/)
    .map((line) => {
      const i = line.indexOf('//')
      return i >= 0 ? line.slice(0, i) : line
    })
    .join('\n')
  const out = []
  for (const hit of body.matchAll(/['"]([^'"]+)['"]/g)) {
    const v = hit[1].trim().replace(/^\.?\//, '')
    if (v) out.push(v.replace(/\\/g, '/'))
  }
  return out
}

/**
 * 极简 glob → 正则。只支持 `**`（跨目录）与 `*`（单层），够用且不必引依赖。
 * 注意 `**` 后紧跟斜杠时允许**零层**（所以 `**` + `/README.md` 能匹配根部的 README.md）。
 */
export function globToRe(glob) {
  let re = ''
  for (let i = 0; i < glob.length; i++) {
    const c = glob[i]
    if (c === '*' && glob[i + 1] === '*') {
      i++
      if (glob[i + 1] === '/') {
        re += '(?:.*/)?'
        i++
      } else {
        re += '.*'
      }
    } else if (c === '*') {
      re += '[^/]*'
    } else if (c === '?') {
      re += '[^/]'
    } else if ('.+^$()[]{}|\\'.includes(c)) {
      re += '\\' + c
    } else {
      re += c
    }
  }
  return new RegExp('^' + re + '$')
}

/** 预编译版：`loadSrcExclude()` → `RegExp[]`。 */
export function loadSrcExclude() {
  return loadSrcExcludePatterns().map(globToRe)
}

/** `rel` 是相对 `docs/` 的正斜杠路径（可带或不带 `.md`）。 */
export function isExcluded(rel, patterns) {
  const norm = String(rel).replace(/\\/g, '/').replace(/^\.?\//, '')
  for (const p of patterns) {
    if (typeof p === 'string') {
      if (p === norm) return true
      if (p.includes('*') && globToRe(p).test(norm)) return true
    } else if (p.test(norm)) {
      return true
    }
  }
  return false
}

export { ROOT, CONFIG }
