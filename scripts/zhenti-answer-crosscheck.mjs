#!/usr/bin/env node
/**
 * 真题答案交叉核对 v3
 *
 * 校验源换了。v1/v2 用的是 ForestDeer 的文字层，结论是「题号体系不一致，无法自动核对」，
 * 那个结论是错的 —— 真实原因有两层：
 *
 *   1. `YYYY-ForestDeer完整版.md` 有**串年文件**：2008 那份的答案块是 2008，
 *      但第 330 行出现 `2009` 标记，后面整卷是 2009 年的卷面。
 *      按题号硬比，等于拿两年的题互相比。
 *   2. 就算不串年，文字层把答案字母和解析混排（`C "The last decade" ...` /
 *      `require  A`），取哪个字母都只能靠启发式。
 *
 * 真正权威的是 `docs/public/papers/english/*-answers.pdf` —— 官方答案页扫描件。
 * 它们没有文字层（pdftotext 出来是空的），所以由 scripts/extract-answer-keys.py
 * 渲染 + OCR 成 `data/english-answer-keys.json`，人工核对过抽不出的年份。
 *
 * 本脚本只做比对，不改文件。差异是线索，改之前要回原卷确认。
 *
 * 用法：
 *   node scripts/zhenti-answer-crosscheck.mjs
 *   node scripts/zhenti-answer-crosscheck.mjs --json
 *   node scripts/zhenti-answer-crosscheck.mjs --md 报告.md
 *   node scripts/zhenti-answer-crosscheck.mjs --parse-fd 2008   # 调试 ForestDeer 解析
 */
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const OFFICIAL = path.join(ROOT, 'data/english-answer-keys.json')
const POLITICS = path.join(ROOT, 'data/politics-answer-keys.json')
const FD_DIR = path.join(ROOT, '历年真题/公共英语')
const TARGET_DIR = path.join(ROOT, 'docs/posts/english')
const POLITICS_DIR = path.join(ROOT, 'docs/posts/politics')

/* ────────────────────────── 官方答案库 ────────────────────────── */

function loadOfficial() {
  if (!fs.existsSync(OFFICIAL)) return {}
  return JSON.parse(fs.readFileSync(OFFICIAL, 'utf8'))
}

function loadPolitics() {
  if (!fs.existsSync(POLITICS)) return {}
  return JSON.parse(fs.readFileSync(POLITICS, 'utf8'))
}

/* ────────────────────── 站内答案速查表解析 ────────────────────── */

/**
 * 站内刷题版的答案速查表。实际存在两种形状：
 *   竖排两对：`| 1 | C | 2 | D |`
 *   末尾横排：`| 题号 | 71 | 72 | 73 | 74 | 75 |` + 分隔行 + `| 答案 | A | A | C | C | B |`
 * 横排是题数为奇数时的收尾块，只认竖排会静默漏掉最后几题。
 * 字母允许 A-E：2022 年七选五第 19 题有五个选项。
 */
function parseSiteAnswers(absPath) {
  const answers = {}
  const lines = fs.readFileSync(absPath, 'utf8').split(/\r?\n/)
  const put = (no, ans) => {
    if (!Number.isInteger(no) || no <= 0 || no > 200) return
    // 政治多选是 `ABC` / `ABCD` 这种多字母，英语是单字母，统一放行 1-5 位
    if (!/^[A-E]{1,5}$/.test(ans)) return
    if (no in answers && answers[no] !== ans) answers[no] = `?${answers[no]}${ans}`
    else answers[no] = ans
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    if (!line.trim().startsWith('|')) continue
    const cells = line.split('|').map((c) => c.trim())

    if (cells[1] === '题号' && cells.length > 3) {
      for (let j = i + 1; j <= i + 2 && j < lines.length; j++) {
        if (!lines[j].trim().startsWith('|')) break
        const ansCells = lines[j].split('|').map((c) => c.trim())
        if (/^:?-+:?$/.test(ansCells[1] ?? '')) continue // 分隔行
        if (ansCells[1] === '答案') {
          for (let k = 2; k < Math.min(cells.length, ansCells.length); k++) {
            put(Number(cells[k]), ansCells[k])
          }
        }
        break
      }
      continue
    }

    for (let k = 1; k + 1 < cells.length; k += 2) put(Number(cells[k]), cells[k + 1])
  }
  return answers
}

/* ────────────────── ForestDeer 文字层（仅作交叉参考） ────────────────── */

const QNO_LINE = /^\s{0,8}(\d{1,3})\s*[.．]?\s*(?:\[\])?\s*$/
const HAS_DOT = /[.．]/
const NOISE = /gzzkgk|QQ:|www\.|^[\s\d|]+$/
const WATERMARK = /(?:www\.gzzkgk\.cn|QQ:\d+|:gzzkgk|\b020-\d+)/g

function stripNoise(line) {
  return line.replace(WATERMARK, '  ')
}

/** 年份标记：整行实质只有年份；只剥小写字母残留（`ww    2009`），不剥大写答案字母。 */
function yearMarkerOf(line) {
  const t = line.trim()
  if (!t || t.length > 24) return null
  const compact = t.replace(/\s+/g, ' ').replace(/^[a-z]{1,4}\s+/, '')
  const m = compact.match(/^((?:19|20)\d{2})$/)
  return m ? m[1] : null
}

/** 外来年份标记必须像一份卷子的开头，否则只是解析里提到的年份。 */
function isForeignYearAt(lines, i, wantYear) {
  const ym = yearMarkerOf(lines[i])
  if (!ym || ym === wantYear) return null
  const y = Number(ym)
  if (y < 2004 || y > 2026) return null
  for (let j = i + 1; j < Math.min(i + 4, lines.length); j++) {
    const t = lines[j].trim()
    if (!t) continue
    return /^Part\s+[IVX]+/i.test(t) || /^#{1,3}\s/.test(t) ? ym : null
  }
  return null
}

/** 主候选 = 第一个能读出字母的行；副候选 = 最后一个独立成行的字母。两者不一致记为歧义。 */
function answerInBlock(blockLines) {
  let first = null
  let lastStandalone = null
  for (const line of blockLines) {
    if (NOISE.test(line)) continue
    if (/^\s*([A-D])\s*$/.test(line)) {
      lastStandalone = line.trim()
      if (!first) first = lastStandalone
      continue
    }
    if (!first) {
      const head = line.match(/^\s*([A-D])(?![A-Za-z])/)
      if (head) first = head[1]
    }
  }
  return { ans: first, alt: lastStandalone, ambiguous: !!first && !!lastStandalone && first !== lastStandalone }
}

function parseForestDeer(absPath, wantYear) {
  const lines = fs.readFileSync(absPath, 'utf8').split(/\r?\n/)
  const answers = {}
  const ambiguous = new Set()
  const foreignYears = []
  let stopLine = -1

  let start = lines.findIndex((l) => /^##\s*试题/.test(l))
  if (start === -1) start = 0
  let end = lines.length
  for (let i = start + 1; i < lines.length; i++) {
    const ym = isForeignYearAt(lines, i, wantYear)
    if (ym) {
      foreignYears.push(ym)
      end = i
      stopLine = i + 1
      break
    }
  }

  let cur = null
  let lastNo = 0
  let buf = []
  const flush = () => {
    if (cur === null) return
    const { ans, ambiguous: amb } = answerInBlock(buf)
    if (ans && !(cur in answers)) {
      answers[cur] = ans
      if (amb) ambiguous.add(cur)
    }
  }

  for (let i = start; i < end; i++) {
    const cl = stripNoise(lines[i])
    const m = cl.match(QNO_LINE)
    if (m) {
      const no = Number(m[1])
      if (!HAS_DOT.test(cl) && no !== lastNo + 1) {
        if (cur !== null) buf.push(cl)
        continue
      }
      if (no <= lastNo && no !== lastNo + 1) {
        if (cur !== null) buf.push(cl)
        continue
      }
      flush()
      cur = no
      lastNo = no
      buf = []
      continue
    }
    if (cur !== null) buf.push(cl)
  }
  flush()

  return { answers, ambiguous, foreignYears, stopLine }
}

/* ────────────────────────────── 主流程 ────────────────────────────── */

function runParseFd(year) {
  const abs = path.join(FD_DIR, `${year}-ForestDeer完整版.md`)
  const { answers, ambiguous, foreignYears, stopLine } = parseForestDeer(abs, year)
  const nos = Object.keys(answers).map(Number).sort((a, b) => a - b)
  console.log(`# ${year}  答案 ${nos.length} 题  题号 ${nos[0]}..${nos[nos.length - 1]}`)
  console.log(`# 外来年份：${foreignYears.join(',') || '无'}${stopLine > 0 ? `（第 ${stopLine} 行截断）` : ''}`)
  console.log(`# 歧义 ${ambiguous.size} 题：${[...ambiguous].join(',') || '无'}`)
  console.log(nos.map((n) => `${n}:${answers[n]}`).join(' '))
}

function main() {
  const args = process.argv.slice(2)
  if (args[0] === '--parse-fd') return runParseFd(args[1])

  const asJson = args.includes('--json')
  const mdIdx = args.indexOf('--md')
  const mdOut = mdIdx !== -1 ? args[mdIdx + 1] : null

  const official = loadOfficial()
  const years = Object.keys(official).sort()
  if (years.length === 0) {
    console.error('没有官方答案库，先跑：python scripts/extract-answer-keys.py')
    process.exit(1)
  }

  const recs = []
  const rows = []

  for (const year of years) {
    const siteFile = `${year}-英语-刷题版.md`
    const siteAbs = path.join(TARGET_DIR, siteFile)
    const truth = official[year].answers

    const rec = {
      year,
      sourceNote: official[year].source,
      sourceCount: Object.keys(truth).length,
      siteCount: 0,
      compared: 0,
      diffs: [],
      missingInSite: [],
      note: '',
      verdict: 'no-site',
    }

    if (!fs.existsSync(siteAbs)) {
      rec.note = `站内缺 ${siteFile}`
      recs.push(rec)
      continue
    }

    const got = parseSiteAnswers(siteAbs)
    rec.siteCount = Object.keys(got).length

    const srcNos = Object.keys(truth).map(Number).sort((a, b) => a - b)
    const overlap = srcNos.filter((n) => n in got)
    rec.compared = overlap.length
    rec.missingInSite = srcNos.filter((n) => !(n in got))

    for (const n of overlap) {
      if (got[n] !== truth[n]) rec.diffs.push({ no: n, site: got[n], source: truth[n] })
    }

    rec.verdict =
      rec.compared === 0 ? 'no-overlap' : rec.diffs.length === 0 ? 'clean' : 'check'
    recs.push(rec)
    for (const d of rec.diffs) rows.push({ year, ...d, file: siteFile })
  }

  // ── 政治理论 ──
  // 站内政治页只做到 2018 起，所以 2012-2017 抽出来了但没有可比对象。
  const politics = loadPolitics()
  const polRecs = []
  const polRows = []
  for (const year of Object.keys(politics).sort()) {
    const siteAbs = path.join(POLITICS_DIR, `${year}.md`)
    const truth = politics[year].answers
    const rec = { year, sourceCount: Object.keys(truth).length, siteCount: 0, compared: 0, diffs: [], verdict: 'no-site' }
    if (!fs.existsSync(siteAbs)) {
      rec.note = `站内无 ${year}.md`
      polRecs.push(rec)
      continue
    }
    const got = parseSiteAnswers(siteAbs)
    rec.siteCount = Object.keys(got).length
    const overlap = Object.keys(truth).map(Number).filter((n) => n in got)
    rec.compared = overlap.length
    for (const n of overlap) {
      if (got[n] !== truth[n]) {
        rec.diffs.push({ no: n, site: got[n], source: truth[n] })
        polRows.push({ year, no: n, site: got[n], source: truth[n] })
      }
    }
    rec.verdict = rec.compared === 0 ? 'no-overlap' : rec.diffs.length === 0 ? 'clean' : 'check'
    polRecs.push(rec)
  }

  // ForestDeer 只用来报告数据完整性问题，不参与判定
  const fdYears = fs
    .readdirSync(FD_DIR)
    .map((f) => f.match(/^(\d{4})-ForestDeer完整版\.md$/))
    .filter(Boolean)
    .map((m) => m[1])
    .sort()
  const spliced = []
  for (const y of fdYears) {
    const { foreignYears, stopLine } = parseForestDeer(path.join(FD_DIR, `${y}-ForestDeer完整版.md`), y)
    if (foreignYears.length) spliced.push({ year: y, foreignYears, stopLine })
  }

  if (asJson) {
    console.log(JSON.stringify({ recs, rows, spliced }, null, 2))
    return
  }

  const totalCompared = recs.reduce((n, r) => n + r.compared, 0)
  const cleanYears = recs.filter((r) => r.verdict === 'clean').length
  const L = []
  // 章节编号跟着实际输出走：没有差异表时不能留下「一、三、四」这种断号
  const CN = ['一', '二', '三', '四', '五']
  let sec = 0
  const h2 = (title) => {
    L.push(`## ${CN[sec++]}、${title}`)
    L.push('')
  }

  L.push('# 真题答案核对（v3 · 官方答案 PDF）')
  L.push('')
  L.push(`> 生成：${new Date().toISOString().slice(0, 19).replace('T', ' ')} · scripts/zhenti-answer-crosscheck.mjs`)
  L.push('> 校验源：`docs/public/papers/english/*-answers.pdf`、`docs/public/papers/politics/2012-2019-政治合集.pdf`（官方答案页扫描件）')
  L.push('> 抽取方式：`scripts/extract-answer-keys.py`、`scripts/extract-politics-keys.py` 渲染 + OCR → `data/*-answer-keys.json`')
  L.push('> 被校验：`docs/posts/english/YYYY-英语-刷题版.md`、`docs/posts/politics/YYYY.md` 的答案速查表')
  L.push('> **差异是线索，不是结论。** 改之前要回原卷确认。')
  L.push('')

  const polCompared = polRecs.reduce((n, r) => n + r.compared, 0)
  const polClean = polRecs.filter((r) => r.verdict === 'clean').length
  if (rows.length === 0 && polRows.length === 0) {
    L.push(
      `**结论：英语 ${recs.length} 个年份 ${recs.reduce((n, r) => n + r.compared, 0)} 题、政治 ${polClean} 个年份 ${polCompared} 题，答案与官方答案页逐题一致，没有需要改的。**`
    )
  } else {
    L.push(`**结论：英语 ${rows.length} 题、政治 ${polRows.length} 题与官方答案页不一致，逐条列出，需回原卷确认后再改。**`)
  }
  L.push('')

  h2('英语 · 逐年核对')
  L.push('| 年份 | 官方答案 | 站内答案 | 实际比对 | 不一致 | 站内缺题 | 判定 |')
  L.push('|:--|--:|--:|--:|--:|:--|:--|')
  const verdictText = {
    clean: '✅ 全对',
    check: '⚠️ 待确认',
    'no-overlap': '— 无重叠',
    'no-site': '— 站内无刷题版',
  }
  for (const r of recs) {
    const miss = r.missingInSite.length ? `${r.missingInSite.length}（${r.missingInSite.slice(0, 6).join(',')}${r.missingInSite.length > 6 ? '…' : ''}）` : '0'
    L.push(
      `| ${r.year} | ${r.sourceCount} | ${r.siteCount} | ${r.compared} | ${r.diffs.length} | ${miss} | ${verdictText[r.verdict] ?? r.verdict}${r.note ? `（${r.note}）` : ''} |`
    )
  }
  L.push('')
  L.push(`**英语合计比对 ${totalCompared} 题，${cleanYears}/${recs.length} 个年份完全一致，共 ${rows.length} 题不一致。**`)
  L.push('')

  if (rows.length) {
    h2('英语 · 答案不一致（需人工确认）')
    L.push('| 年份 | 题号 | 站内 | 官方 | 文件 |')
    L.push('|:--|--:|:--:|:--:|:--|')
    for (const r of rows) L.push(`| ${r.year} | ${r.no} | **${r.site}** | ${r.source} | ${r.file} |`)
    L.push('')
  }

  h2('政治 · 客观题核对')
  L.push('站内政治页只做到 2018 起，所以 2012–2017 的官方答案抽出来了但没有可比对象。')
  L.push('')
  L.push('| 年份 | 官方答案 | 站内答案 | 实际比对 | 不一致 | 判定 |')
  L.push('|:--|--:|--:|--:|--:|:--|')
  for (const r of polRecs) {
    L.push(
      `| ${r.year} | ${r.sourceCount} | ${r.siteCount} | ${r.compared} | ${r.diffs.length} | ${verdictText[r.verdict] ?? r.verdict}${r.note ? `（${r.note}）` : ''} |`
    )
  }
  L.push('')
  L.push(`**政治合计比对 ${polCompared} 题，${polClean}/${polRecs.length} 个年份完全一致，共 ${polRows.length} 题不一致。**`)
  L.push('')
  if (polRows.length) {
    L.push('| 年份 | 题号 | 站内 | 官方 |')
    L.push('|:--|--:|:--:|:--:|')
    for (const r of polRows) L.push(`| ${r.year} | ${r.no} | **${r.site}** | ${r.source} |`)
    L.push('')
  }

  h2('校验源本身的数据问题')
  if (spliced.length) {
    L.push('`历年真题/公共英语/YYYY-ForestDeer完整版.md` 里有文件把两年塞在一起，答案块与卷面块不是同一年。')
    L.push('任何按题号拿它当校验源的工具都会被骗 —— v1/v2 的「题号体系不一致」结论就是这么来的。')
    L.push('')
    L.push('| 文件 | 内含外来年份 | 截断行 |')
    L.push('|:--|:--|--:|')
    for (const s of spliced) L.push(`| ${s.year}-ForestDeer完整版.md | ${s.foreignYears.join('、')} | ${s.stopLine} |`)
    L.push('')
  } else {
    L.push('未发现串年。')
    L.push('')
  }

  h2('能力边界')
  L.push(
    '- **政治只能核到 2018–2019**：站内政治页从 2018 才有，2012–2017 的官方答案虽已抽出（`data/politics-answer-keys.json`），但没有可比对象。'
  )
  L.push(
    '- **政治的年份归属靠结构推断，不是原文标注**：合集里 2019 卷的卷头被裁掉，答案页本身不写年份，所以按「答案组出现顺序 = 2012..2019」推定，再用 2018/2019 的逐题比对结果反证（若错位，正确率会掉到 25% 左右）。'
  )
  L.push(
    '- **2012–2017 的政治答案未经比对验证**：抽出来了（`data/politics-answer-keys.json`），但没有站内页面可比。里面能看到可疑项（如 2012 多选第 24 题只有单个字母 `A`），说明 OCR 在这几年仍有漏字。**这几年当校验源用之前要人工过一遍。**'
  )
  L.push(
    '- **政治视频源抽不出答案**：`p2025-zhengzhi-binge` / `p2025-zhengzhi-zhanghuijia` / `politics2026-dense` 的 OCR 文本里没有任何「解析：X / 答案：X」行，不是题号格式问题，是视频本身只讲题不给答案文字。'
  )
  L.push('- **2024-2026 无官方答案 PDF**：`docs/public/papers/english/` 只到 2023，这三年没有可比对的权威源。')
  L.push('- **只比答案字母**，不比题干。题干是否正确是另一件事。')
  L.push('- **2021 年答案由人工视觉转录**（见 `data/english-answer-keys-manual.json` 的说明）。')
  L.push('')

  const out = L.join('\n')
  if (mdOut) {
    fs.writeFileSync(path.join(ROOT, mdOut), out, 'utf8')
    console.log(`报告已写入 ${mdOut}`)
    console.log(`比对 ${totalCompared} 题，不一致 ${rows.length} 题`)
  } else {
    console.log(out)
  }
}

main()
