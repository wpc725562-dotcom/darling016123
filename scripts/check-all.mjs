#!/usr/bin/env node
/**
 * 全站检查总入口（2026-10-05 新增）
 *
 * 为什么需要它：
 *   本库到 2026-10-05 已经有 **13 个独立检查器**（config / tags / nav / links / md / health /
 *   search / kanban / ledger / study-log / 三个生成器 --check）。但它们是**散装**的 ——
 *   每次要靠人记得逐个跑。
 *   ⚠️ 其中 `ledger:check` 与 `study-log:check` 是 2026-10-05 才补收进来的：
 *     它们**一直存在、却谁都没跑**（不在本清单、也不在任何 workflow）——
 *     正是本段描述的病本身。
 *   实测代价：`home:stats:check` 逻辑早就对，只是**没人跑**，首页两处数字（高数篇数、英语篇数）
 *   烂了半个月；`updates:gen:check` 同理。
 *   ⇒ **纪律写在文档里靠不住，要变成一条命令。**
 *
 * 它还额外盯一件散装跑法看不见的事：**dist 是否比源文件旧**。
 *   产物层检查（`search:check`）跑在**过期产物**上会给出**假绿** —— 这正是本库踩过的坑：
 *   「构建通过 + 检查器全绿」而功能其实没生效。所以本脚本会把「dist 过期」单独报出来，
 *   并且**默认不让它算作全绿**（用 `--allow-stale` 可降级为警告）。
 *
 * 用法：
 *   node scripts/check-all.mjs                 # 跑全部；dist 过期则退出码 2
 *   node scripts/check-all.mjs --allow-stale   # dist 过期只警告，退出码看检查结果
 *   node scripts/check-all.mjs --only=link:check,md:check
 *   node scripts/check-all.mjs --json
 *
 * 退出码：0 全绿 · 1 有检查失败 · 2 检查都过但 dist 过期（产物层结论不可信）
 */
import { spawnSync } from 'node:child_process'
import { readdirSync, statSync, existsSync } from 'node:fs'
import { join, dirname, resolve, relative } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const DOCS = join(ROOT, 'docs')
const DIST = join(DOCS, '.vitepress', 'dist')
const DIST_INDEX = join(DIST, 'index.html')

const args = process.argv.slice(2)
const JSON_OUT = args.includes('--json')
const ALLOW_STALE = args.includes('--allow-stale')
const onlyRaw = (args.find((a) => a.startsWith('--only=')) || '').slice('--only='.length)
const onlySet = onlyRaw
  ? new Set(onlyRaw.split(',').map((s) => s.trim()).filter(Boolean))
  : null

/**
 * 检查清单 —— 单一事实源。
 * 新增检查器时**只改这里**（以及 package.json 里对应的一条 script）。
 */
const CHECKS = [
  { name: 'config:check',      script: 'check-config-eval.mjs',   argv: [],          desc: 'nav/sidebar 真求值 + 结构约束' },
  { name: 'tags:check',        script: 'check-tags.mjs',          argv: [],          desc: '标签白名单（受控词表 40）' },
  { name: 'tags:gen:check',    script: 'gen-tags.mjs',            argv: ['--check'], desc: '标签索引页是否最新' },
  { name: 'updates:gen:check', script: 'gen-updates.mjs',         argv: ['--check'], desc: '/updates/ 与 feed.xml 是否最新' },
  { name: 'home:stats:check',  script: 'sync-home-stats.mjs',     argv: ['--check'], desc: '首页统计与横幅日期是否最新' },
  { name: 'nav:check',         script: 'check-nav-coverage.mjs',  argv: [],          desc: '导航覆盖 / 孤页 / 分区可达性' },
  { name: 'link:check',        script: 'check-links.mjs',         argv: [],          desc: '死链（含 srcExclude 口径）' },
  { name: 'md:check',          script: 'check-md-hazards.mjs',    argv: [],          desc: 'md / Vue 模板构建风险' },
  { name: 'health:check',      script: 'health-check.mjs',        argv: [],          desc: '文件结构 / 编码 / 大小（6 项）' },
  { name: 'kanban:check',      script: 'check-kanban-tables.mjs', argv: [],          desc: '看板表格行列一致' },
  // ★ 2026-10-05 补收：这两个检查器**一直存在、却谁都没跑**（不在本清单、也不在任何 workflow）。
  //   正是本清单开头那段说的病 —— 「检查器不跑等于不存在」。
  //   ledger 用 `--no-freshness`：它的「3 天内有新条目」是**学习节奏**问题、不是仓库缺陷；
  //   而本清单**也跑在 CI 里**，带上新鲜度会让 CI 因为「这几天没学习」变红并自动开 Issue（假警报）。
  //   结构性部分（日志字段 / 错题编号 / 开场卡）照常查；新鲜度留作人工收工仪式：`npm run ledger:check`。
  { name: 'ledger:check',      script: 'check-session-ledger.mjs', argv: ['--no-freshness'], desc: '学习落账：日志字段 / 错题编号 / 开场卡（不含新鲜度）' },
  { name: 'study-log:check',   script: 'check-study-log.mjs',      argv: [],          desc: '学习日志结构与科目名一致性' },
  { name: 'politics-paper:check', script: 'check-politics-papers.mjs', argv: [],     desc: '政治卷面：多选题必须 A–D 四选项' },
  { name: 'score:split',          script: 'score-split.mjs',           argv: [],     desc: '计算机分值拆分：19 模块权重合计 = 200' },
  { name: 'search:check',      script: 'check-search-tags.mjs',   argv: [],          desc: '产物层：标签真的进了搜索索引', needsDist: true },
]

/** 递归取「最新的源文件 mtime」——用于判断 dist 是否过期。 */
function newestSource(dir, acc) {
  let entries
  try {
    entries = readdirSync(dir, { withFileTypes: true })
  } catch {
    return acc
  }
  for (const e of entries) {
    // 跳过构建产物与缓存：它们不是「源」，且 dist 自己会不断变新（自指）
    if (e.isDirectory()) {
      if (['node_modules', 'dist', 'cache', '.git'].includes(e.name)) continue
      newestSource(join(dir, e.name), acc)
    } else if (/\.(md|mts|ts|vue|json|xml|css)$/i.test(e.name)) {
      const p = join(dir, e.name)
      try {
        const m = statSync(p).mtimeMs
        if (m > acc.t) { acc.t = m; acc.f = p }
      } catch { /* ignore */ }
    }
  }
  return acc
}

const distExists = existsSync(DIST_INDEX)
const newest = newestSource(DOCS, { t: 0, f: null })
const distMtime = distExists ? statSync(DIST_INDEX).mtimeMs : 0
const stale = distExists && newest.t > distMtime

function runOne(c) {
  const t0 = Date.now()
  const r = spawnSync(
    process.execPath,
    [join(ROOT, 'scripts', c.script), ...c.argv],
    { cwd: ROOT, encoding: 'utf8', timeout: 300000, maxBuffer: 64 * 1024 * 1024 },
  )
  const ms = Date.now() - t0
  const out = `${r.stdout || ''}${r.stderr || ''}`
  return { ...c, status: r.status === 0 ? 'pass' : 'fail', ms, code: r.status, out }
}

/** 从检查器输出里挑一行最能代表结论的（带 ✅ / ❌ / 数字的）。 */
function clean(s) {
  return s.replace(/[✅❌⚠️🟠🔴🟡🔵⏭️]\s*/g, '').trim()
}
function digest(out) {
  const lines = out.split(/\r?\n/).map((s) => s.trim()).filter(Boolean)
  // 1) 优先「通过 N」这类汇总行（health-check 的结论在汇总里，不在最后一行）
  const summary = lines.find((l) => /通过\s*[:：]\s*\d/.test(l))
  if (summary) return clean(summary)
  // 2) 退而取最后一条「只含 ✅、不含 ❌」的行（避免抓到「❌ 失败: 0」这种）
  for (let i = lines.length - 1; i >= 0; i--) {
    if (lines[i].includes('✅') && !lines[i].includes('❌')) return clean(lines[i])
  }
  return clean(lines[lines.length - 1] || '')
}

const results = []
for (const c of CHECKS) {
  if (onlySet && !onlySet.has(c.name)) continue
  if (c.needsDist && !distExists) {
    results.push({ ...c, status: 'skip', ms: 0, code: null, out: '', note: '未找到 dist ⇒ 先跑 npm run docs:build:sandbox' })
    continue
  }
  results.push(runOne(c))
}

const failed = results.filter((r) => r.status === 'fail')
const skipped = results.filter((r) => r.status === 'skip')
const passed = results.filter((r) => r.status === 'pass')
const staleMatters = stale && passed.some((r) => r.needsDist) && !ALLOW_STALE

const exitCode = failed.length > 0 ? 1 : staleMatters ? 2 : 0

if (JSON_OUT) {
  console.log(JSON.stringify({
    exitCode,
    dist: {
      exists: distExists,
      stale,
      newestSource: newest.f ? relative(ROOT, newest.f) : null,
      newestSourceMtime: newest.t ? new Date(newest.t).toISOString() : null,
      distIndexMtime: distExists ? new Date(distMtime).toISOString() : null,
    },
    passed: passed.length,
    failed: failed.length,
    skipped: skipped.length,
    results: results.map((r) => ({
      name: r.name, status: r.status, ms: r.ms, code: r.code,
      digest: digest(r.out), note: r.note || null,
    })),
  }, null, 2))
  process.exit(exitCode)
}

const total = results.length
console.log(`\n=== 全站检查（${total} 项）===`)
const nameW = Math.max(...results.map((r) => r.name.length))
for (let i = 0; i < results.length; i++) {
  const r = results[i]
  const icon = r.status === 'pass' ? '✅' : r.status === 'fail' ? '❌' : '⏭️'
  const secs = `${(r.ms / 1000).toFixed(1)}s`.padStart(6)
  console.log(`${String(i + 1).padStart(2)}/${total} ${r.name.padEnd(nameW)}  ${icon} ${secs}  ${r.status === 'pass' ? digest(r.out) : ''}`)
  if (r.status === 'fail') {
    const tail = r.out.split(/\r?\n/).map((s) => s.trimEnd()).filter(Boolean).slice(-8)
    for (const line of tail) console.log(`        │ ${line}`)
  }
  if (r.status === 'skip' && r.note) console.log(`        │ ${r.note}`)
}

console.log('\n--- 摘要 ---')
console.log(`✅ 通过 ${passed.length} · ⏭️ 跳过 ${skipped.length} · ❌ 失败 ${failed.length}`)

if (stale) {
  const src = newest.f ? relative(ROOT, newest.f) : '?'
  console.log(`\n⚠️ dist 比源文件旧 —— 产物层检查可能基于**过期构建**（这就是「假绿」的来源）。`)
  console.log(`   最新源文件：${src}（${new Date(newest.t).toLocaleString('zh-CN')}）`)
  console.log(`   dist/index.html：${new Date(distMtime).toLocaleString('zh-CN')}`)
  console.log(`   ⇒ 先跑 npm run docs:build:sandbox，再重跑本命令。${ALLOW_STALE ? '（--allow-stale 已降级为警告）' : ''}`)
}

process.exit(exitCode)
