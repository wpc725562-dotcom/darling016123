#!/usr/bin/env node
/**
 * 站点死链检查脚本（VitePress markdown 链接）
 * 用法：
 *   node scripts/check-links.mjs                # 检查全部（默认）
 *   node scripts/check-links.mjs --quick        # 只检查本地 .md 链接，跳过外链
 *   node scripts/check-links.mjs --json         # JSON 输出
 *
 * 检查四类问题：
 *   ① markdown 链接 [text](target) 的目标文件是否存在
 *   ② 图片链接 ![](/xxx.png) 的目标文件是否存在
 *   ③ Obsidian 双链 [[xxx]] 是否有对应笔记
 *   ④ config.mts 的 nav / sidebar 链接是否存在
 *      （含「是否被 srcExclude 排除」—— 源文件在、但页面不进构建，站点上就是 404）
 *
 * ★ 另有第五类「URL 内含空白」：`[下载](/papers/x-full. pdf)`。
 *   上面 ① 的正则要求目标不含空白，这类链接**整条匹配不上**，因此 ①② 都
 *   漏检 —— 旧版会打印「无死链」。2026-09-20 实测漏掉 10 处，故单独补断言。
 *   修数据不够，正则本身的盲区必须在这里堵。
 */
import { readdirSync, statSync, readFileSync, writeFileSync, unlinkSync } from 'node:fs'
import { join, dirname, resolve, extname, sep, relative } from 'node:path'
import { fileURLToPath } from 'node:url'
import { tmpdir } from 'node:os'

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const DOCS = join(ROOT, 'docs')
const QUICK = process.argv.includes('--quick')
const JSON_OUT = process.argv.includes('--json')

function walk(dir) {
  const out = []
  for (const name of readdirSync(dir)) {
    const p = join(dir, name)
    if (name.startsWith('.') || name === 'node_modules' || name === 'dist' || name === 'cache') continue
    if (statSync(p).isDirectory()) out.push(...walk(p))
    else if (extname(p) === '.md') out.push(p)
  }
  return out
}

function resolveLink(fromFile, link) {
  // 去掉锚点、query
  const clean = link.split('#')[0].split('?')[0]
  if (!clean || /^https?:|^mailto:|^tel:/.test(clean)) return null // 外链跳过（quick 模式）
  if (QUICK && /^https?:/.test(clean)) return null
  const base = dirname(fromFile)
  let target = clean
  if (target.endsWith('.md')) target = target.slice(0, -3)
  // VitePress cleanUrls: /xxx 或 xxx -> xxx.md 或 xxx/index.md
  const candidates = [
    resolve(base, target + '.md'),
    resolve(base, target, 'index.md'),
    resolve(base, clean), // 原样（可能带 .md 或已存在）
  ]
  // 绝对路径（以 / 开头 → 先查 public 静态资源，再查 DOCS）
  if (clean.startsWith('/')) {
    const publicTargets = [join(ROOT, 'docs', 'public', clean.slice(1))]
    if (existsAny(publicTargets)) return [publicTargets[0]]
    return [join(DOCS, clean.slice(1) + '.md'), join(DOCS, clean.slice(1), 'index.md'), join(DOCS, clean.slice(1))]
  }
  return candidates
}

function existsAny(paths) {
  return paths.some((p) => { try { return statSync(p).isFile() } catch { return false } })
}

const files = walk(DOCS)
const broken = []
let totalLinks = 0

for (const f of files) {
  const content = readFileSync(f, 'utf-8')
  // ★ 先剔除行内代码 `...`，再匹配链接。
  //   为什么：文档里经常**举例说明**某个写法有问题，例如
  //   `docs/posts/真题索引.md:130` 为了记录「指向 _templates/ 的链接会让构建失败」
  //   这个坑，正文里写了一个字面量的链接示例。检查器把示例当成真链接，
  //   于是常年报 1 处死链 —— 结果 `check-links` 永远退出 1，没法当门禁用。
  //   （2026-09-20 实测。）Obsidian 双链那段本来就用 stripCode，这里对齐。
  const scannable = content.replace(/`[^`\n]*`/g, '')
  // markdown 链接 [text](target)：排除代码块内的误匹配（如 a[i][j]）
  // 只匹配 target 是「合理的链接形式」：含 / . : # 或为普通文件名
  const mdLinks = [...scannable.matchAll(/\[[^\]]*\]\(([^)\s]+)\)/g)]
  for (const m of mdLinks) {
    const link = m[1]
    // 过滤误匹配：target 不含 / . : # 且不是常见文件扩展名 → 跳过（如 i≥j 场景的残留）
    if (!/[\/\.:#]/.test(link) && !/[a-zA-Z0-9_-]+\.[a-zA-Z]+/.test(link)) continue
    totalLinks++
    const resolved = resolveLink(f, link)
    if (!resolved) continue
    if (!existsAny(resolved)) broken.push({ file: f.slice(ROOT.length + 1), link })
  }
  // 图片链接 ![](/xxx.png)
  const imgLinks = [...scannable.matchAll(/!\[[^\]]*\]\(([^)\s]+)\)/g)]
  for (const m of imgLinks) {
    totalLinks++
    const link = m[1]
    if (/^https?:/.test(link)) continue
    const resolved = resolveLink(f, link)
    if (!resolved) continue
    if (!existsAny(resolved)) broken.push({ file: f.slice(ROOT.length + 1), link })
  }
}

// ============ URL 内含空白检查 ============
// ★ 为什么必须单独查：上面 markdown 链接的正则是 /\(([^)\s]+)\)/ —— 要求链接
//   目标**不含空白**。于是 `/papers/english/2020-full. pdf` 这种写法整个链接
//   匹配不上：既不进 totalLinks，也不进 broken。检查器于是打印「无死链」，
//   而页面上那个「下载 PDF」按钮点下去是 404。
//
//   实测 2026-09-20：4 个英语页共 10 处这种链接（8 处站内 PDF + 2 处 GitHub
//   链接），旧版检查器**一处都没报**，只报了 1 处无关的 /_templates/ 死链。
//   漏检的原因是正则，不是数据 —— 所以修数据不够，必须在这里补断言。
//
//   这里的正则故意允许目标含空白，专门把它们揪出来。
const SPACE_LINK_RE = /\[[^\]]*\]\(([^)]*)\)/g
const SPACE_EXT_RE = /\.\s+(pdf|md|html|png|jpe?g|gif|webp|svg|zip|csv|xlsx?)\b/i
const spaceLinks = []

for (const f of files) {
  const lines = readFileSync(f, 'utf-8').split('\n')
  let inFence = false
  lines.forEach((line, i) => {
    // 跳过围栏代码块：里面的写法是示例，不是真链接
    if (/^\s*(```|~~~)/.test(line)) { inFence = !inFence; return }
    if (inFence) return
    // 跳过行内代码 `...`，避免把反引号里的示例当成缺陷
    const scannable = line.replace(/`[^`]*`/g, '')
    for (const m of scannable.matchAll(SPACE_LINK_RE)) {
      const target = m[1]
      if (/\s/.test(target) && SPACE_EXT_RE.test(target)) {
        spaceLinks.push({ file: f.slice(ROOT.length + 1), line: i + 1, link: target.trim() })
      }
    }
  })
}

// ============ Obsidian 双链检查 [[xxx]] ============
// 语义：目标相对仓库根解析；带 | 时取 | 前为路径；路径优先，再按 basename 全库匹配
// 检查全库（docs + 源库）中的所有 [[双链]]
const WIKI_RE = /\[\[([^\]]+?)\]\]/g

// 去掉围栏代码块与行内代码：反引号里的 [[x]] 是「在讲这个写法」，不是真链接。
// 不剥离会稳定误报（例：文档里写 `[[章节]]` 说明双链格式）。
function stripCode(s) {
  return s
    .replace(/```[\s\S]*?```/g, '')
    .replace(/~~~[\s\S]*?~~~/g, '')
    .replace(/`[^`\n]*`/g, '')
}

// 这些 [[...]] 是 Markdown 扩展指令，不是文件双链，必须跳过
// （[[toc]] 由 markdown-it 的 table-of-contents 插件渲染成目录，无对应文件；
//   2026-09-17 修复：此前会误报为死链，与 scripts/health-check.mjs 的 SKIP_WIKI 保持一致）
const SKIP_WIKI = new Set(['toc', 'tableofcontents'])
const allMd = walk(ROOT).filter((p) => !p.includes('node_modules') && !p.includes('.obsidian'))

// ★ 双链目标必须落在 docs/ 内（2026-09-22 补）
//   `[[双链]]` 是 Obsidian 语法，VitePress 不认识它 —— 源文件在 docs/ 下时，
//   这串会**原样输出到页面**。此时「目标存在」≠「读者点得到」：
//   目标若躺在仓库根（Obsidian 源库），站点上根本没有这一页。
//   实测 `[[../_考题模板排序|考题模板排序]]` 按 basename 命中了仓库根的
//   `历年真题/_考题模板排序.md`，旧版据此报「无死链」—— 而读者点不到。
const docsMd = allMd.filter((p) => p.startsWith(DOCS + sep))
const wikiBroken = []
let wikiTotal = 0
for (const f of allMd) {
  const content = stripCode(readFileSync(f, 'utf-8'))
  for (const m of content.matchAll(WIKI_RE)) {
    wikiTotal++
    let raw = m[1].trim()
    // 拆显示名：| 或 \| 都是「路径|显示名」分隔，取第一段为路径
    const target = raw.replace(/\\\|/g, '|').split('|')[0].trim()
    if (!target) continue
    // 跳过 Markdown 扩展指令（[[toc]] 等），不是 Obsidian 双链 —— 不跳过会稳定误报
    if (SKIP_WIKI.has(target.toLowerCase())) continue
    const rel = target.replace(/\\/g, '/').replace(/^\/+/, '')
    // 路径优先：先去掉尾部转义 \ 再匹配
    const relClean = rel.replace(/\\+$/, '')
    // 源文件在 docs/ 下 ⇒ 只在 docs/ 内解析目标（站点上没有 docs/ 外的页面）
    const pool = f.startsWith(DOCS + sep) ? docsMd : allMd
    const pathHit = pool.find((p) => {
      const rp = p.slice(ROOT.length + 1).replace(/\\/g, '/')
      return rp === relClean + '.md' || rp === relClean || rp.startsWith(relClean + '/')
    })
    if (pathHit) continue
    // basename 匹配（Obsidian 语义：文件名去路径，也允许指向同名目录）
    // 归一化：去尾部/全部反斜杠转义、空格↔连字符、去 _ 前缀与括号
    const norm = (s) => s.replace(/\\/g, '').replace(/[_（）()]/g, '').replace(/\s+/g, '-').toLowerCase()
    const base = norm(relClean.split('/').pop())
    const baseHit = pool.some((p) => {
      const name = norm(p.split(sep).pop().replace(/\.md$/, ''))
      return name === base || (base.length >= 4 && name.startsWith(base))
    })
    // 目录匹配：全库同名目录（Obsidian 可链接到文件夹）
    const dirHit = base.length >= 4 && pool.some((p) => {
      const dirName = norm(p.split(sep).slice(-2)[0])
      return dirName === base
    })
    // 跳过已知的代码示例文档（agent-troubleshoot 讲链接修复，含伪链接）
    const isExampleDoc = f.includes('agent-troubleshoot')
    if (!baseHit && !dirHit && !isExampleDoc) wikiBroken.push({ file: f.slice(ROOT.length + 1), link: `[[${target}]]` })
  }
}

// 合并到输出
for (const b of wikiBroken) broken.push(b)
totalLinks += wikiTotal
const wikiNote = wikiTotal ? `（含 ${wikiTotal} 个 Obsidian 双链）` : ''

// ============ 导航链接检查（config.mts 的 nav / sidebar）============
// 背景：上面只扫正文 markdown 链接。config.mts 里的 `link:` 从未被校验 ——
// 写错一个路径，只有等整站构建（~135 秒）才会暴露，而且报错点离现场很远。
// 这里把 config 里的 link: 也当作链接源，逐个解析。
const CONFIG = join(DOCS, '.vitepress', 'config.mts')

// ★ srcExclude 盲区（2026-09-21 补）
//   旧版只查「源文件在不在」—— 源文件当然在（它就躺在 docs/ 里），于是放行。
//   但 srcExclude 的页面**不进构建** ⇒ dist 里没有它 ⇒ 站点上点进去 404。
//   实测 `link: '/guide/bili-scraping'` 就是这样藏了很久的死链：
//   sidebar 有链接，srcExclude 有 'guide/bili-scraping.md'，检查器全程沉默。
function globToRe(g) {
  let re = ''
  for (let i = 0; i < g.length; i++) {
    const c = g[i]
    if (c === '*' && g[i + 1] === '*') {
      i++
      if (g[i + 1] === '/') { re += '(?:.*/)?'; i++ } else { re += '.*' }
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

function parseSrcExclude(cfgText) {
  const m = cfgText.match(/srcExclude:\s*\[([\s\S]*?)\]/)
  if (!m) return []
  return [...m[1].matchAll(/['"]([^'"]+)['"]/g)].map((x) => globToRe(x[1]))
}

function checkConfigLinks(configPath) {
  const out = []
  let total = 0
  let cfg
  try {
    cfg = readFileSync(configPath, 'utf-8')
  } catch {
    return { total: 0, broken: out, unreadable: true }
  }
  const excludeRes = parseSrcExclude(cfg)
  for (const m of cfg.matchAll(/link:\s*['"]([^'"]+)['"]/g)) {
    const link = m[1]
    // 外链、模板串跳过
    if (/^https?:|^mailto:|^tel:/.test(link) || link.includes('${')) continue
    total++
    const resolved = resolveLink(configPath, link)
    if (!resolved) continue
    const hit = resolved.find((p) => { try { return statSync(p).isFile() } catch { return false } })
    if (!hit) { out.push(link); continue }
    // 源文件在，但被 srcExclude 排除 ⇒ 站点上不会有这一页
    const rel = relative(DOCS, hit).split(sep).join('/')
    if (excludeRes.some((re) => re.test(rel))) {
      out.push(`${link}  ← 被 srcExclude 排除（${rel}），站点上不会有这一页`)
    }
  }
  return { total, broken: out, unreadable: false }
}

// ---- 自检：证明这个检查「有能力失败」 ----
if (process.argv.includes('--selftest')) {
  const tmp = join(tmpdir(), `vitepress-navcheck-selftest-${process.pid}.mts`)
  const scenarios = [
    { name: '正常链接（应通过）', body: `link: '/guide/零基础总入口'`, expectFail: false },
    { name: '不存在的页面（应报错）', body: `link: '/guide/这个页面肯定不存在-xyz'`, expectFail: true },
    { name: '外链（应跳过）', body: `link: 'https://example.com/nope'`, expectFail: false },
    { name: '模板串（应跳过）', body: 'link: `${base}foo`', expectFail: false },
    {
      name: '被 srcExclude 排除（应报错）',
      body: `link: '/guide/bili-scraping'`,
      extra: `srcExclude: [ 'guide/bili-scraping.md' ],`,
      expectFail: true,
    },
    {
      name: 'srcExclude 通配不误伤（应通过）',
      body: `link: '/guide/零基础总入口'`,
      extra: `srcExclude: [ 'guide/bili-scraping.md', '_templates/**', '**/README.md' ],`,
      expectFail: false,
    },
  ]
  let allGood = true
  console.log('── 导航链接检查 · 自检 ──')
  try {
    for (const sc of scenarios) {
      writeFileSync(tmp, `export default { ${sc.extra ?? ''} themeConfig: { nav: [ { ${sc.body} } ] } }\n`)
      const r = checkConfigLinks(tmp)
      const didFail = r.broken.length > 0
      const ok = sc.expectFail ? didFail : !didFail
      allGood = allGood && ok
      console.log(`${ok ? '✅' : '❌'} ${sc.name.padEnd(22, ' ')} 期望${sc.expectFail ? '报错' : '通过'} · 实际${didFail ? '报错' : '通过'}${didFail ? ` → ${r.broken.join(', ')}` : ''}`)
    }
  } finally {
    try { unlinkSync(tmp) } catch {}
  }

  // ---- 代码片段剥离 · 自检 ----
  console.log('\n── 代码片段剥离 · 自检 ──')
  const codeCases = [
    {
      name: '反引号里的 [[x]] 不算链接',
      src: '写法是 `[[章节]]` 这样',
      expectFound: 0,
    },
    {
      name: '正文里的 [[x]] 仍要算',
      src: '见 [[1.1 C语言概述与基本概念]] 一节',
      expectFound: 1,
    },
    {
      name: '围栏代码块里的 [[x]] 不算链接',
      src: '```md\n关联：[[01-某某]]\n```',
      expectFound: 0,
    },
    {
      name: '代码外与代码内混排，只算代码外的',
      src: '`[[甲]]` 是真写法，[[乙]] 是真链接，`[[丙]]`',
      expectFound: 1,
    },
  ]
  for (const c of codeCases) {
    const found = [...stripCode(c.src).matchAll(WIKI_RE)].length
    const ok = found === c.expectFound
    allGood = allGood && ok
    console.log(`${ok ? '✅' : '❌'} ${c.name.padEnd(30, ' ')} 期望抓到 ${c.expectFound} 个 · 实际 ${found} 个`)
  }
  console.log(allGood ? '\n自检全部符合预期。' : '\n自检失败：检查逻辑本身有问题。')
  process.exit(allGood ? 0 : 1)
}

const nav = checkConfigLinks(CONFIG)
for (const link of nav.broken) {
  broken.push({ file: 'docs/.vitepress/config.mts（导航）', link })
}

if (JSON_OUT) {
  console.log(JSON.stringify({
    totalLinks, navLinks: nav.total,
    brokenCount: broken.length, broken,
    spaceLinkCount: spaceLinks.length, spaceLinks,
  }, null, 2))
  process.exit(broken.length || spaceLinks.length ? 1 : 0)
}

if (spaceLinks.length) {
  console.log(`❌ 发现 ${spaceLinks.length} 处「URL 内含空白」的链接（旧版正则会整条漏掉它们）：`)
  for (const s of spaceLinks) console.log(`  ${s.file}:${s.line} -> ${s.link}`)
}

if (broken.length === 0 && spaceLinks.length === 0) {
  console.log(`✅ 无死链（检查 ${files.length} 个文件，${totalLinks} 个链接${wikiNote}；导航 ${nav.total} 个链接）`)
} else {
  if (broken.length) {
    console.log(`❌ 发现 ${broken.length} 处死链（共 ${totalLinks} 个链接${wikiNote}；导航 ${nav.total} 个链接）：`)
    for (const b of broken) console.log(`  ${b.file} -> ${b.link}`)
  }
  process.exit(1)
}
