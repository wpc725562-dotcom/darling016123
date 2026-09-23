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
 * markdown-it `escapedSplit()` 的逐字移植 —— 表格切列的唯一正确语义。
 *
 * ★ 为什么不能 `line.split('|')`：markdown-it 的 table 规则**只认 `\|` 是转义竖线**，
 *   它既不认行内代码、也不认公式。于是 `` | 考点 | `&&`、`||` 的结果 | `` 会被切成 3 格，
 *   而表头只有 2 列；渲染时 `for (i=0; i<columnCount; i++)` **只取前 2 格**
 *   ⇒ 第 3 格内容**静默消失**（不是渲染成空，是不进 DOM）。
 *   实测：docs/posts/computer/2025.md L1104 丢 2 格、
 *        模拟卷/卷三-拔高冲刺卷-答案.md L20 丢 8 格（含整段 `= 3 || 9 && -1 = 3 || 1 = 1`）。
 *   （列数 4 / 4 / 12 已与构建产物实测校对。）
 */
export function escapedSplit(line) {
  const out = []
  let cur = ''
  let last = 0
  let isEscaped = false
  const jsSub = (s, a, b) => (a > b ? s.substring(b, a) : s.substring(a, b))
  for (let i = 0; i < line.length; i++) {
    const ch = line[i]
    if (ch === '|') {
      if (!isEscaped) {
        out.push(cur + line.substring(last, i))
        cur = ''
        last = i + 1
      } else {
        cur += jsSub(line, last, i - 1)   // `\|`：吃掉反斜杠
        last = i
      }
    }
    isEscaped = ch === '\\'
  }
  out.push(cur + line.substring(last))
  return out
}

/** 表格行的单元格数组（去掉首尾空壳，与 markdown-it 一致）。 */
export function tableCells(line) {
  const cells = escapedSplit(line)
  if (cells.length && cells[0] === '') cells.shift()
  if (cells.length && cells[cells.length - 1] === '') cells.pop()
  return cells.map((c) => c.trim())
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
  // 表格状态：表头列数 + 表头行号（用于报「本行与哪张表不符」）
  let tableCols = null
  let tableStart = 0

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

    // ⑤ 表格行列数与表头不符
    //    ★ 2026-09-23 实测：markdown-it 的 table 规则用 escapedSplit 切列（只认 `\|`），
    //      渲染时 `for (i=0; i<columnCount; i++)` **只取表头那么多格**
    //      ⇒ 多出来的格被**静默丢弃**，内容永久消失，且**不报错**。
    //      真凶几乎总是「行内代码 span 里的裸 `|`」，例如 `` `&&`、`||` `` ——
    //      实测 docs/posts/computer/2025.md L1104 丢 2 格、
    //      模拟卷/卷三-拔高冲刺卷-答案.md L20 丢 8 格（含整段推导）。
    //      修法：给代码 span 里的 `|` 加反斜杠 —— escapedSplit 会吃掉反斜杠，
    //      单元格内容变回 `` `||` `` ⇒ 仍渲染成 `<code>||</code>`，**视觉完全一致**。
    {
      const isSep = (s) => /^\|?[\s:|-]+\|?$/.test(s) && (s.match(/\|/g) || []).length > 1
      if (t.startsWith('|')) {
        if (tableCols === null) {
          if (!isSep(t)) {
            tableCols = tableCells(raw).length
            tableStart = ln
          }
        } else if (!isSep(t)) {
          const n = tableCells(raw).length
          if (n !== tableCols) {
            issues.push({
              line: ln,
              rule: 'table-col-mismatch',
              detail:
                n > tableCols
                  ? `表格行列数 ${n} > 表头 ${tableCols} 列（表起于 L${tableStart}）：超出的 ${n - tableCols} 格会被**静默丢弃**（markdown-it 只渲染到表头列数）。多半是行内代码 span 里的裸 \`|\`，改成 \`\\|\` 即可（渲染结果不变）`
                  : `表格行列数 ${n} < 表头 ${tableCols} 列（表起于 L${tableStart}）：缺的格会渲染成空单元格`,
              text: raw.trim().slice(0, 120),
            })
          }
        }
      } else {
        tableCols = null
      }
    }

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

    // ④ 表格行内公式含**裸竖线** `|`
    //    ★ 2026-09-23 实测：`| 🟡 跳跃间断点 | 左极限 ≠ 右极限 | $y = \frac{|x|}{x}$ |`
    //      在**站点**与**可打印产物**里都被切成
    //      `<td>$y = \frac{</td><td>x</td><td>}{x}$</td>` —— 公式截断、凭空多出两个单元格。
    //      根因：表格行以 `|` 分列，公式里的绝对值/行列式竖线被当成了列分隔符。
    //      修法：把裸 `|` 换成 `\vert`。实测 `\vert x\vert` 与 `|x|` 渲染**完全一致**
    //      （同为 2.552ex），而 `\|` 是 LaTeX 的范数记号（3.557ex，语义不同）**不可用**。
    //      注意 `\|` 本身是合法的（范数），所以只报**未被反斜杠转义**的裸竖线。
    if (t.startsWith('|')) {
      const MATH_RE = /\$\$([^$]+)\$\$|(?<!\$)\$(?!\$)([^$\n]+?)\$(?!\$)/g
      for (const mm of raw.matchAll(MATH_RE)) {
        const body = mm[1] !== undefined ? mm[1] : mm[2]
        if (/(?<!\\)\|/.test(body)) {
          issues.push({
            line: ln,
            rule: 'table-math-pipe',
            detail:
              '表格行内公式含裸竖线 `|`：会被当成列分隔符，公式被切碎并多出单元格。改用 `\\vert`（与 `|` 渲染一致；`\\|` 是范数记号，语义不同）',
            text: raw.trim().slice(0, 120),
          })
        }
      }
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
    {
      name: '表格行内公式含裸竖线（真问题）',
      text: '| 🟡 跳跃间断点 | 左极限 ≠ 右极限 | $y = \\frac{|x|}{x}$ |\n',
      expect: 'table-math-pipe',
    },
    {
      name: '表格行内公式已用 \\vert（应放过）',
      text: '| 🟡 跳跃间断点 | 左极限 ≠ 右极限 | $y = \\frac{\\vert x\\vert}{x}$ |\n',
      expect: null,
    },
    {
      name: '表格行内范数记号 \\|（应放过：那是合法的双竖线）',
      text: '| 二重积分 | $\\|x\\|\\le 1$ | 8.4 |\n',
      expect: null,
    },
    {
      name: '非表格行的公式含裸竖线（应放过：不涉及分列）',
      text: '这里 $|x|<1$ 不在表格里\n',
      expect: null,
    },
    {
      name: '表格行内代码含裸竖线（真问题：格被静默丢弃）',
      text: '| 考点 | 内容 |\n|:---|:---|\n| **逻辑运算** | `&&`、`||` 的结果不是原值 |\n',
      expect: 'table-col-mismatch',
    },
    {
      name: '表格行内代码已用 \\|（应放过：渲染结果不变）',
      text: '| 考点 | 内容 |\n|:---|:---|\n| **逻辑运算** | `&&`、`\\|\\|` 的结果不是原值 |\n',
      expect: null,
    },
    {
      name: '正常表格（应放过）',
      text: '| 考点 | 内容 |\n|:---|:---|\n| 逻辑运算 | 结果值只有 0 或 1 |\n',
      expect: null,
    },
    {
      name: '非表格行代码含 ||（应放过：不涉及分列）',
      text: 'C 的逻辑或是 `a || b`\n',
      expect: null,
    },
    {
      name: '表格行少一格（真问题：渲染成空格）',
      text: '| 考点 | 内容 | 备注 |\n|:---|:---|:---|\n| 逻辑运算 | 结果值 |\n',
      expect: 'table-col-mismatch',
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
