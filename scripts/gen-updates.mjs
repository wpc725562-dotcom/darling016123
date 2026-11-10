#!/usr/bin/env node
/**
 * 生成「最近更新」归档页 + RSS feed（2026-10-05）。
 *
 * 为什么需要（尤其是单人维护的站）：
 *   `lastUpdated: true` 只在**每页页脚**显示一个日期，全站没有「我上次改到哪了」的入口。
 *   对一个人维护 400+ 页的库，这个入口**给自己用比给读者用更值钱**。
 *
 * 数据来源：`git log --name-only`（一次调用取全部文件的最近提交时间），
 * 未提交/未跟踪的文件回退到 mtime。
 *
 * 用法：
 *   node scripts/gen-updates.mjs            # 生成
 *   node scripts/gen-updates.mjs --check    # 只校验是否最新（CI 用）
 */
import fs from 'node:fs'
import path from 'node:path'
import { collectContentPages } from './content-dates.mjs'

const ROOT = process.cwd()
const DOCS = path.join(ROOT, 'docs')
const OUT_MD = path.join(DOCS, 'updates', 'index.md')
const OUT_XML = path.join(DOCS, 'public', 'feed.xml')
const SITE = 'https://wpc725562-dotcom.github.io/darling016123'
const CHECK = process.argv.includes('--check')
const MAX_FEED = 30
const WEEKS = 10

/* ---------- 1. 采集内容页 + 各自最后修改时间 ---------- */
// ★ 2026-10-05：这段逻辑抽到了 `scripts/content-dates.mjs`，因为**首页横幅的
//   「内容更新至 X」也要用同一个日期**（见 `sync-home-stats.mjs`）。
//   两处各写一份 ⇒ 迟早给出两个不同的「最新日期」。
//   该模块已经处理好三件事：排除 `srcExclude` 的页（否则链到不存在的页面 → dead link）、
//   排除生成物目录（否则列表自我污染）、git 时间与 mtime **取较晚者**。
const pages = collectContentPages(ROOT)

/* ---------- 2. 生成 /updates/ ---------- */
const weekOf = (iso) => {
  const d = new Date(iso)
  const day = (d.getDay() + 6) % 7                    // 周一=0
  d.setDate(d.getDate() - day); d.setHours(0, 0, 0, 0)
  return d
}
// ★ 用**本地**时间显示（`toISOString()` 是 UTC，本机 GMT+8 会差 8 小时：
//   本地 05:32 改的东西会显示成前一天 21:32，读者看着像「昨天改的」）。
const fmt = (iso) => {
  const d = new Date(iso)
  const p = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`
}

const byWeek = new Map()
for (const p of pages) {
  const k = weekOf(p.date).toISOString().slice(0, 10)
  if (!byWeek.has(k)) byWeek.set(k, [])
  byWeek.get(k).push(p)
}
const weeks = [...byWeek.entries()].slice(0, WEEKS)

const L = []
L.push('---')
L.push('title: "最近更新"')
L.push('description: "按周列出本站最近改动的页面 —— 单人维护的站，这也是「我上次改到哪了」的自查入口。"')
L.push('---')
L.push('')
L.push('# 🕒 最近更新')
L.push('')
L.push('> ⚙️ 本页由 `scripts/gen-updates.mjs` **自动生成**，请勿手改。')
L.push(`> 数据来自 git 提交时间（未提交的改动回退到文件修改时间）。全站共 ${pages.length} 页。`)
L.push(`> RSS 订阅：[\`${SITE}/feed.xml\`](${SITE}/feed.xml)`)
L.push('')
L.push('## 按周查看')
L.push('')
L.push('| 周（起） | 改动页数 | 跳转 |')
L.push('|:--|--:|:--|')
for (const [k, arr] of weeks) L.push(`| ${k} | ${arr.length} | [看这一周](#w-${k}) |`)
L.push('')
for (const [k, arr] of weeks) {
  L.push(`<a id="w-${k}"></a>`)
  L.push('')
  L.push(`## ${k} 那一周（${arr.length} 页）`)
  L.push('')
  L.push('| 页面 | 时间 |')
  L.push('|:--|:--|')
  for (const p of arr) L.push(`| [${p.title}](${p.url}) | ${fmt(p.date)} |`)
  L.push('')
}
L.push('## 全部页面（按时间倒序，前 100）')
L.push('')
L.push('| 页面 | 时间 |')
L.push('|:--|:--|')
for (const p of pages.slice(0, 100)) L.push(`| [${p.title}](${p.url}) | ${fmt(p.date)} |`)
L.push('')
const md = L.join('\n')

/* ---------- 4. 生成 RSS ---------- */
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
const xml = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<rss version="2.0"><channel>',
  '  <title>专升本笔记 · 最近更新</title>',
  `  <link>${SITE}/</link>`,
  '  <description>广东专升本复习笔记站：四科笔记 · 历年真题 · 知识地图</description>',
  '  <language>zh-CN</language>',
  `  <lastBuildDate>${new Date(pages[0]?.date || Date.now()).toUTCString()}</lastBuildDate>`,
  ...pages.slice(0, MAX_FEED).flatMap((p) => [
    '  <item>',
    `    <title>${esc(p.title)}</title>`,
    `    <link>${SITE}${p.url}</link>`,
    `    <guid isPermaLink="true">${SITE}${p.url}</guid>`,
    `    <pubDate>${new Date(p.date).toUTCString()}</pubDate>`,
    `    <description>${esc(p.desc || p.title)}</description>`,
    '  </item>',
  ]),
  '</channel></rss>',
  '',
].join('\n')

if (CHECK) {
  const a = fs.existsSync(OUT_MD) ? fs.readFileSync(OUT_MD, 'utf8') : ''
  const b = fs.existsSync(OUT_XML) ? fs.readFileSync(OUT_XML, 'utf8') : ''
  if (a !== md || b !== xml) { console.error('❌ updates/feed 不是最新，请跑 node scripts/gen-updates.mjs'); process.exit(1) }
  console.log('✅ updates/index.md 与 public/feed.xml 均为最新')
} else {
  fs.mkdirSync(path.dirname(OUT_MD), { recursive: true })
  fs.mkdirSync(path.dirname(OUT_XML), { recursive: true })
  fs.writeFileSync(OUT_MD, md, 'utf8')
  fs.writeFileSync(OUT_XML, xml, 'utf8')
  console.log(`✅ 已生成 updates/index.md（${pages.length} 页 / 展示 ${weeks.length} 周）与 public/feed.xml（${Math.min(MAX_FEED, pages.length)} 条）`)
  console.log(`   最近 3 条：`)
  for (const p of pages.slice(0, 3)) console.log(`     ${fmt(p.date)}  ${p.title}`)
}
