#!/usr/bin/env node
/**
 * Markdown 构建风险检查（Vue / VitePress 模板层）
 *
 * 为什么需要它：VitePress 把每个 md 页当 Vue 模板编译。
 * 某些在 Markdown 里完全合法的写法，会让 Vue 编译器直接报错，
 * 而**完整的站点构建要跑两分多钟才告诉你**。这个脚本把这类问题提前到秒级。
 *
 * 用法：
 *   node scripts/check-md-hazards.mjs            # 检查 docs/ 下全部 md
 *   node scripts/check-md-hazards.mjs --json
 *   node scripts/check-md-hazards.mjs --selftest # 自检：证明它「有能力失败」
 */
import { readdirSync, statSync, readFileSync, existsSync } from 'node:fs'
import { join, dirname, resolve, extname } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const DOCS = join(ROOT, 'docs')
const JSON_OUT = process.argv.includes('--json')

/**
 * 从主题入口读出「已注册的全局组件」白名单。
 * 注册过的组件出现在 md 里是**正常用法**，不该报警。
 * 读不到就当没有白名单（宁可多报，不可漏报）。
 */
export function loadRegisteredComponents() {
  const out = new Set()
  const candidates = [
    join(DOCS, '.vitepress', 'theme', 'index.ts'),
    join(DOCS, '.vitepress', 'theme', 'index.js'),
  ]
  for (const p of candidates) {
    let src = ''
    try {
      src = readFileSync(p, 'utf-8')
    } catch {
      continue
    }
    // app.component('Name', X) / app.component("Name", X)
    for (const m of src.matchAll(/app\.component\(\s*['"`]([^'"`]+)['"`]/g)) out.add(m[1])
  }
  return out
}

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

/**
 * 读 config.mts 的 srcExclude，返回被排除的相对路径集合（相对 docs/，正斜杠）。
 * 这些文件**不参与构建** —— 里面的风险永远不会让构建失败，不该报成构建风险。
 * （2026-09-18 加：此前 bili-scraping.md 被 srcExclude 排除，却仍被报错，属假阳性。）
 */
function loadSrcExclude() {
  const cfg = join(DOCS, '.vitepress', 'config.mts')
  if (!existsSync(cfg)) return new Set()
  const text = readFileSync(cfg, 'utf-8')
  const m = text.match(/srcExclude\s*:\s*\[([\s\S]*?)\]/)
  if (!m) return new Set()
  const out = new Set()
  for (const hit of m[1].matchAll(/['"`]([^'"`]+)['"`]/g)) {
    const v = hit[1].trim().replace(/^\.?\//, '')
    if (v) out.add(v.replace(/\\/g, '/'))
  }
  return out
}

function isExcluded(rel, patterns) {
  for (const p of patterns) {
    if (p === rel) return true
    // 极简 glob：只支持 **/ 与 *，够用且不必引依赖
    if (p.includes('*')) {
      const re = new RegExp('^' + p.replace(/[.+^${}()|[\]\\]/g, '\\$&')
        .replace(/\*\*/g, '\u0000').replace(/\*/g, '[^/]*').replace(/\u0000/g, '.*') + '$')
      if (re.test(rel)) return true
    }
  }
  return false
}

/**
 * 逐行扫描，返回问题列表。
 * 会跟踪围栏代码块状态：``` 之内一律跳过（VitePress 对围栏块做了保护）。
 */
export function scanText(text, registered = new Set()) {
  const issues = []
  const lines = text.replace(/\r\n/g, '\n').split('\n')
  let fence = false
  let fenceMark = ''
  let fenceLine = 0

  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i]
    const t = raw.trim()
    const ln = i + 1

    // 围栏切换
    const m = t.match(/^(`{3,}|~{3,})/)
    if (m) {
      if (!fence) {
        fence = true
        fenceMark = m[1][0].repeat(3)
        fenceLine = ln
      } else if (t.startsWith(fenceMark) && /^(`{3,}|~{3,})\s*$/.test(t)) {
        fence = false
      }
      continue
    }
    if (fence) continue

    // 行内数学 $...$ 与块级 $$...$$ 会被 KaTeX 在 markdown 阶段吃掉，
    // Vue 看不到里面的内容 —— 所以先摘掉再检查。
    const probe = raw
      .replace(/\$\$[^$]*\$\$/g, '')
      .replace(/\$[^$]*\$/g, '')

    // ★ 行内代码对两类规则的保护是**不对称**的（2026-09-18 用 VitePress 真实渲染器实测）：
    //     `{{ foo }}`  →  <code>{{ foo }}</code>      ← 花括号**不被转义**，Vue 照样插值 → 危险
    //     `<HTML>`     →  <code>&lt;HTML&gt;</code>   ← 尖括号**被转义**，Vue 看不到标签 → 安全
    //   markdown-it 只转义 & < > "，不转义 { }。所以：
    //     · 检查 {{  → 用 probe（保留行内代码）
    //     · 检查标签 → 用 noCode（先摘掉行内代码）
    const noCode = probe
      .replace(/``[^`]*``/g, '')      // 双反引号代码段
      .replace(/`[^`\n]*`/g, '')      // 单反引号代码段

    // ① Vue 插值：{{ ... }} —— 行内代码里的 `{{` 同样会让构建失败
    if (probe.includes('{{')) {
      issues.push({
        line: ln,
        rule: 'vue-interpolation',
        detail: '出现 `{{`：VitePress 会把整页当 Vue 模板，`{{ … }}` 被当成插值表达式，构建报错',
        text: raw.trim().slice(0, 120),
      })
    }

    // ② 未转义的裸 < 后跟大写字母（Vue 会当成组件标签）
    //    行内代码里的 <Foo> 已被 markdown-it 转义成 &lt;Foo&gt;，不算问题 —— 见上方注释
    const tagHit = noCode.match(/<([A-Z][A-Za-z0-9]*)[\s/>]/)
    if (tagHit && !registered.has(tagHit[1])) {
      issues.push({
        line: ln,
        rule: 'vue-component-tag',
        detail: `出现 <${tagHit[1]}>：Vue 会把它当组件，若未注册会构建报错或渲染异常`,
        text: raw.trim().slice(0, 120),
      })
    }

    // ③ 嵌套粗体 **** （渲染出来是乱码）
    if (raw.includes('****')) {
      issues.push({
        line: ln,
        rule: 'nested-bold',
        detail: '出现 `****`：粗体套粗体，渲染结果是四个星号',
        text: raw.trim().slice(0, 120),
      })
    }
  }

  if (fence) {
    issues.push({
      line: fenceLine,
      rule: 'unclosed-fence',
      detail: '代码围栏没有闭合：后面的正文会被整段当成代码',
      text: lines[fenceLine - 1]?.trim().slice(0, 120) || '',
    })
  }

  return issues
}

// ---------------- 自检：证明这个检查「有能力失败」 ----------------
if (process.argv.includes('--selftest')) {
  const cases = [
    {
      name: '行内代码里的 {{（真问题）',
      text: 'C. `int a[3][] = {{1}, {2}, {3}};`\n',
      expect: 'vue-interpolation',
    },
    {
      name: '围栏代码块里的 {{（应放过）',
      text: '```c\nint a[3][] = {{1}, {2}};\n```\n',
      expect: null,
    },
    {
      name: 'LaTeX 的 }}（应放过）',
      text: '$\\dfrac{a}{b}$ 和 $\\dfrac{x}{{y}}$\n',
      expect: null,
    },
    {
      name: '未注册组件式标签（真问题）',
      text: '这里有 <Foo> 标签\n',
      expect: 'vue-component-tag',
    },
    {
      name: '行内代码里的 <Foo>（应放过：markdown-it 会转义尖括号）',
      text: '写作 `<Foo>` 表示组件\n',
      expect: null,
    },
    {
      name: '双反引号代码里的 <Foo>（应放过）',
      text: '写作 ``<Foo>`` 表示组件\n',
      expect: null,
    },
    {
      name: '行内代码 + 裸 <Foo> 混在一行（真问题）',
      text: '写作 `<Foo>`，但这里 <Bar> 是裸的\n',
      expect: 'vue-component-tag',
    },
    {
      name: '已注册组件（应放过）',
      text: '<QuizCard subject="math" />\n',
      expect: null,
      registered: new Set(['QuizCard']),
    },
    {
      name: '嵌套粗体（真问题）',
      text: '> ⚠️ ****1.6 数组** 与 **1.2** 都没有**\n',
      expect: 'nested-bold',
    },
    {
      name: '正常粗体（应放过）',
      text: '**正常粗体** 和 *斜体*\n',
      expect: null,
    },
    {
      name: '未闭合围栏（真问题）',
      text: '正文\n```c\nint a = 1;\n',
      expect: 'unclosed-fence',
    },
  ]
  let allGood = true
  console.log('── Markdown 构建风险检查 · 自检 ──')
  for (const c of cases) {
    const got = scanText(c.text, c.registered ?? new Set())
    const rules = got.map((g) => g.rule)
    let ok
    if (c.expect === null) ok = got.length === 0
    else ok = rules.includes(c.expect)
    allGood = allGood && ok
    console.log(
      `${ok ? '✅' : '❌'} ${c.name.padEnd(30, ' ')} 期望${c.expect ?? '无问题'} · 实际${rules.length ? rules.join(',') : '无问题'}`
    )
  }
  console.log(allGood ? '\n自检全部符合预期。' : '\n自检失败：检查逻辑本身有问题。')
  process.exit(allGood ? 0 : 1)
}

// ---------------- 主流程 ----------------
const registered = loadRegisteredComponents()
const srcExclude = loadSrcExclude()
const allFiles = walk(DOCS)
const files = []
const skipped = []
for (const f of allFiles) {
  const rel = f.replace(ROOT + '\\', '').replace(ROOT + '/', '')
  const inDocs = rel.replace(/^docs[\\/]/, '').replace(/\\/g, '/')
  if (isExcluded(inDocs, srcExclude)) skipped.push(rel)
  else files.push(f)
}
const results = []
for (const f of files) {
  const issues = scanText(readFileSync(f, 'utf-8'), registered)
  if (issues.length) results.push({ file: f.replace(ROOT + '\\', '').replace(ROOT + '/', ''), issues })
}

if (JSON_OUT) {
  console.log(JSON.stringify({ scanned: files.length, skipped: skipped.length, skippedFiles: skipped, registered: [...registered], filesWithIssues: results.length, results }, null, 2))
  process.exit(results.length ? 1 : 0)
}

const skipNote = skipped.length ? `；已按 srcExclude 跳过 ${skipped.length} 个（不参与构建）` : ''

if (results.length === 0) {
  console.log(`✅ 无构建风险（扫描 ${files.length} 个 md 文件${skipNote}；已注册组件 ${registered.size} 个：${[...registered].join(', ') || '无'}）`)
} else {
  const total = results.reduce((n, r) => n + r.issues.length, 0)
  console.log(`❌ 发现 ${total} 处构建风险（涉及 ${results.length} 个文件，共扫描 ${files.length} 个${skipNote}）：`)
  for (const r of results) {
    console.log(`\n  ${r.file}`)
    for (const it of r.issues) {
      console.log(`    L${it.line}  [${it.rule}] ${it.detail}`)
      console.log(`           ${it.text}`)
    }
  }
  process.exit(1)
}
