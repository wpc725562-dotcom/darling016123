#!/usr/bin/env node
/**
 * 真题答案交叉核对
 *
 * 为什么需要这个：
 *   站内的真题页是「回忆版 + PDF 文字层重建」两代产物混在一起，答案可能来自
 *   不同来源。而答案错一道，整套刷题就是负收益 —— 这比排版难看严重得多。
 *   原始资料（ForestDeer 抽取的 autotext 合集）里有【答案】标记，
 *   拿它当校验源逐题比对，是唯一能把「答案对不对」这件事变成可验证的办法。
 *
 * 不做什么（写清楚，免得下次误以为它全自动）：
 *   - 不自动改文件。差异只是线索，改不改要看原始解析说的是不是同一个题号。
 *   - 不核对题干文字。autotext 是 OCR 产物，题干本身带噪声，
 *     拿噪声去比对噪声没有意义；答案（单个字母）才是可靠信号。
 *   - 不做模糊匹配。同题号答案不同就报，宁可多报几个让人看一眼。
 *
 * 用法：
 *   node scripts/zhenti-answer-crosscheck.mjs            # 控制台报告
 *   node scripts/zhenti-answer-crosscheck.mjs --json     # 机器可读
 *   node scripts/zhenti-answer-crosscheck.mjs --md out.md  # 写报告
 */
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')

/** 校验源：带【答案】标记的原始抽取文本 */
const SOURCES = [
  { subject: '公共英语', file: '历年真题/公共英语/2008-2022-英语历年真题集-autotext.md' },
  { subject: '政治理论', file: '历年真题/政治理论/2012-2019-政治历年真题合集-autotext.md' },
]

/** 被校验的站内页面 */
const TARGET_DIRS = {
  公共英语: 'docs/posts/english',
  政治理论: 'docs/posts/politics',
}

/** 从 autotext 里抠 { 年份: { 题号: 答案 } }。 */
function parseSource(absPath) {
  const text = fs.readFileSync(absPath, 'utf8')
  const lines = text.split(/\r?\n/)

  const byYear = {}
  let year = null
  let pendingNo = null

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim()

    // 年份标记：只在「像标题」的行里认，避免正文里的「2010年广州将举办亚运会」被误判
    const ym = line.match(/^(?:#\s*)?(?:广东省)?(\d{4})\s*年.{0,20}(?:真题|招生考试|试题)/)
    if (ym) {
      year = ym[1]
      continue
    }

    // 题号独占一行（`28.` / `28．`）
    const nm = line.match(/^(\d{1,3})\s*[.．]\s*$/)
    if (nm) {
      pendingNo = Number(nm[1])
      continue
    }

    if (pendingNo !== null) {
      const am = line.match(/【答案】\s*([A-D])/)
      if (am) {
        if (year) {
          byYear[year] ??= {}
          // 同题号重复出现时保留第一次：后面往往是「同类题」而不是重考
          if (!(pendingNo in byYear[year])) byYear[year][pendingNo] = am[1]
        }
        pendingNo = null
        continue
      }
      // 下一行不是答案，说明这个题号不是答案块，丢弃
      if (line && !line.startsWith('【')) pendingNo = null
    }
  }

  return byYear
}

/** 从站内页面抠答案速查表：`| 1 | C | 2 | D |` 这种两列并排的表格。 */
function parseTarget(absPath) {
  const text = fs.readFileSync(absPath, 'utf8')
  const answers = {}
  for (const line of text.split(/\r?\n/)) {
    if (!line.trim().startsWith('|')) continue
    const cells = line.split('|').map((c) => c.trim())
    // 期望形状：['', 题号, 答案, 题号, 答案, '']
    for (let i = 1; i + 1 < cells.length; i += 2) {
      const no = Number(cells[i])
      const ans = cells[i + 1]
      if (!Number.isInteger(no) || no <= 0 || no > 200) continue
      if (!/^[A-D]$/.test(ans)) continue
      answers[no] = ans
    }
  }
  return answers
}

function yearOfFile(name) {
  const m = name.match(/(\d{4})/)
  return m ? m[1] : null
}

function main() {
  const args = process.argv.slice(2)
  const asJson = args.includes('--json')
  const mdIdx = args.indexOf('--md')
  const mdOut = mdIdx !== -1 ? args[mdIdx + 1] : null

  const rows = []
  const coverage = []

  for (const src of SOURCES) {
    const srcAbs = path.join(ROOT, src.file)
    if (!fs.existsSync(srcAbs)) {
      coverage.push({ subject: src.subject, note: `校验源缺失：${src.file}` })
      continue
    }
    const truth = parseSource(srcAbs)
    const years = Object.keys(truth).sort()
    coverage.push({
      subject: src.subject,
      note: `校验源覆盖年份：${years.join(', ') || '（没解析出年份）'}`,
    })

    const dir = path.join(ROOT, TARGET_DIRS[src.subject])
    if (!fs.existsSync(dir)) continue

    for (const f of fs.readdirSync(dir).filter((x) => x.endsWith('.md'))) {
      const year = yearOfFile(f)
      if (!year || !truth[year]) continue
      const got = parseTarget(path.join(dir, f))
      const want = truth[year]

      const overlap = Object.keys(got).filter((n) => n in want)
      if (overlap.length === 0) {
        coverage.push({
          subject: src.subject,
          note: `${f}：与校验源无重叠题号（源有 ${Object.keys(want).length} 题，页有 ${Object.keys(got).length} 题）`,
        })
        continue
      }

      for (const n of overlap) {
        if (got[n] !== want[n]) {
          rows.push({
            subject: src.subject,
            year,
            file: f,
            no: Number(n),
            page: got[n],
            source: want[n],
          })
        }
      }
      coverage.push({
        subject: src.subject,
        note: `${f}：比对 ${overlap.length} 题，不一致 ${rows.filter((r) => r.file === f).length} 题`,
      })
    }
  }

  if (asJson) {
    console.log(JSON.stringify({ rows, coverage }, null, 2))
    return
  }

  const lines = []
  lines.push('# 真题答案交叉核对')
  lines.push('')
  lines.push(`> 生成：${new Date().toISOString().slice(0, 19).replace('T', ' ')} · scripts/zhenti-answer-crosscheck.mjs`)
  lines.push('> 校验源：ForestDeer 抽取的 autotext 合集（带【答案】标记）')
  lines.push('> **差异只是线索，不是结论。** 改之前要回去看原始解析说的是不是同一个题号。')
  lines.push('')

  lines.push('## 覆盖情况')
  lines.push('')
  for (const c of coverage) lines.push(`- ${c.subject}：${c.note}`)
  lines.push('')

  lines.push(`## 结果`)
  lines.push('')
  if (rows.length === 0) {
    lines.push('无差异。注意：这只说明「有重叠的题号」都对得上，不等于全部题目都核对过。')
  } else {
    // 先把「连续多题不一致」的文件挑出来。这类几乎一定是题号体系不同，
    // 而不是答案批量印错 —— 六道题同时错、还刚好连号，概率上说不通。
    const byFile = {}
    for (const r of rows) (byFile[r.file] ??= []).push(r)
    const misaligned = []
    const realDiff = []
    for (const [file, rs] of Object.entries(byFile)) {
      const nos = rs.map((r) => r.no).sort((a, b) => a - b)
      let run = 1
      let maxRun = 1
      for (let i = 1; i < nos.length; i++) {
        run = nos[i] === nos[i - 1] + 1 ? run + 1 : 1
        maxRun = Math.max(maxRun, run)
      }
      ;(maxRun >= 3 ? misaligned : realDiff).push([file, rs])
    }

    if (misaligned.length) {
      lines.push('### 无法核对：题号体系不一致')
      lines.push('')
      for (const [file, rs] of misaligned) {
        const nos = rs.map((r) => r.no).sort((a, b) => a - b)
        lines.push(
          `- \`${file}\`：第 ${nos.join('、')} 题连续不一致。` +
            `连续三题以上全错，说明两边题号对不上（大题顺序不同 / OCR 重排），` +
            `**这批差异不能当「答案错」处理**。要核对得先人工建题号映射。`
        )
      }
      lines.push('')
      lines.push(
        '已查证的实例（2026-11-11）：2008 英语站内第 28 题是词汇语法题 ' +
          '`The government has lost a great deal of ______`（答案 B），' +
          '而校验源第 28 题是完形 `Think or behave`（答案 D）—— ' +
          '同一题号在两边根本不是同一道题。'
      )
      lines.push('')
    }

    if (realDiff.length) {
      lines.push(`### 待人工确认的答案差异（${realDiff.reduce((n, [, rs]) => n + rs.length, 0)} 题）`)
      lines.push('')
      lines.push('| 科目 | 年份 | 题号 | 站内 | 校验源 | 文件 |')
      lines.push('|:--|:--|--:|:--:|:--:|:--|')
      for (const [, rs] of realDiff) {
        for (const r of rs) {
          lines.push(`| ${r.subject} | ${r.year} | ${r.no} | **${r.page}** | ${r.source} | ${r.file} |`)
        }
      }
      lines.push('')
    }
  }
  lines.push('')

  const out = lines.join('\n')
  if (mdOut) {
    fs.writeFileSync(path.join(ROOT, mdOut), out, 'utf8')
    console.log(`报告已写入 ${mdOut}`)
    console.log(`差异 ${rows.length} 题`)
  } else {
    console.log(out)
  }
}

main()
