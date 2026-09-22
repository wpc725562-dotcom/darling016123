#!/usr/bin/env node
/**
 * 修复被 spacing 脚本误伤的 URL（github. com → github.com, www. xxx → www.xxx）
 * 用法：node scripts/fix-url-damage.mjs [--dry-run]
 *
 * 覆盖两类破坏：
 *   ① 域名 / 顶级域被拆：`github. com`、`. cn`
 *   ② **文件扩展名被拆**：`2020-full. pdf`、`2023. md`  ← 2026-09-20 补
 *      原来只有 ①，于是 4 个英语页共 10 处扩展名坏链一直修不到。
 */
import { readFileSync, writeFileSync, readdirSync, statSync } from 'node:fs'
import { join, dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const DRY = process.argv.includes('--dry-run')

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name)
    if (name.startsWith('.') || name === 'node_modules' || name === 'dist' || name === 'cache' || name === '.git') continue
    if (statSync(p).isDirectory()) walk(p, out)
    else if (p.endsWith('.md')) out.push(p)
  }
  return out
}

function fixUrls(text) {
  let count = 0
  // 1. 域名被拆：github. com → github.com（含 https:// 后的）
  text = text.replace(/(https?:\/\/[a-zA-Z0-9_-]+)\. ([a-zA-Z]{2,5})\b/g, (m, a, b) => { count++; return `${a}.${b}` })
  // 2. www. xxx → www.xxx（www 后空格）
  text = text.replace(/\b(www)\. ([a-zA-Z0-9])/g, (m, a, b) => { count++; return `${a}.${b}` })
  // 3. 常见顶级域被拆：. com / . cn / . org 等（前面是域名片段）
  text = text.replace(/([a-zA-Z0-9_-])\. (com|cn|org|net|edu|io|gov|info|me|co)\b/g, (m, a, b) => { count++; return `${a}.${b}` })
  // 4. ★ 2026-09-20 补：**文件扩展名**被拆（`. pdf` / `. md` / `. png` …）。
  //
  //    上面 1–3 只认「域名 + 顶级域」，于是文件扩展名这一类**完全没覆盖**：
  //      `/papers/english/2020-full. pdf`            → 三条规则都修不到
  //      `…/blob/main/历年真题/公共英语/2023. md`     → 同上
  //    实测 4 个英语页共 10 处坏链因此存活至今。
  //
  //    为什么这么久没被发现：当时的死链检查器正则是 /\(([^)\s]+)\)/，
  //    要求链接目标**不含空白** —— 这些坏链整条匹配不上，既不计数也不报错。
  //    修复工具漏这一类 + 检查器漏这一类，两处失守叠加，坏链才藏了下来。
  //
  //    只在 markdown 链接 / 图片目标内修，避免误伤正文里「句号 + 空格」的正常行文。
  text = text.replace(/(\]\([^)]*?)\. (pdf|md|html?|png|jpe?g|gif|webp|svg|zip|csv|xlsx?|mp3|mp4|json|txt)\b/gi,
    (m, pre, ext) => { count++; return `${pre}.${ext}` })
  // 5. 裸 URL 里的扩展名被拆（不在 markdown 语法内，如正文直接写 https://x.com/a. pdf）
  text = text.replace(/(https?:\/\/[^\s)]*?)\. (pdf|md|html?|png|jpe?g|gif|webp|svg|zip|csv|xlsx?|mp3|mp4|json|txt)\b/gi,
    (m, pre, ext) => { count++; return `${pre}.${ext}` })
  return { text, count }
}

const files = walk(ROOT)
let total = 0
for (const f of files) {
  const content = readFileSync(f, 'utf-8')
  const { text, count } = fixUrls(content)
  if (count > 0) {
    total += count
    if (!DRY) writeFileSync(f, text, 'utf-8')
    console.log(`${DRY ? '🔍' : '✅'} ${count} 处 | ${f.slice(ROOT.length + 1)}`)
  }
}
console.log(`\n${DRY ? '🔍 发现' : '✅ 修复'} ${total} 处 URL 破坏`)
