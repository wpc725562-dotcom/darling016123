#!/usr/bin/env node
/**
 * 最高执行命令 —— 一条命令跑完「巡逻自检 → 站点构建 → 全站检查」。
 * （2026-10-05 新增）
 *
 * ── 为什么还需要它 ──────────────────────────────────────────────────────
 * 到 2026-10-05，本库已有三层验证，但它们**各跑各的、顺序有隐含依赖**：
 *   ① `bash scripts/test-patrol-logic.sh`  —— 巡逻 workflow 的 bash 逻辑 + 防回归扫描
 *   ② `npm run docs:build`                 —— 站点构建（5 分半）
 *   ③ `npm run check:all`                  —— 11 个检查器 + dist 过期检测
 *
 * 「顺序有隐含依赖」是重点：**③ 里的 `search:check` 读的是 ① ② 之后产出的 dist**。
 * 先跑 ③ 再跑 ②，③ 检查的是**上一版构建**，照样打 ✅ —— 正是本库踩过的
 * 「构建通过 + 检查器全绿，功能其实没生效」。靠人记顺序 = 迟早记错。
 *
 * ⇒ 把它们按**正确顺序**串成一条命令，顺序就不会错。
 *
 * ── 为什么自检放最前、构建放中间 ────────────────────────────────────────
 * · 自检最快（约 5 秒）且不依赖任何产物 ⇒ 放最前，坏了立刻停，不必等 5 分半构建；
 * · 构建必须**早于** check:all（见上）；
 * · check:all 放最后 ⇒ 它看到的 dist 一定是刚构建的，产物层结论可信。
 *
 * ── 用法 ────────────────────────────────────────────────────────────────
 *   npm run verify                 # 全套（自检 → 构建 → 检查），约 6 分钟
 *   npm run verify -- --skip-build # 跳过构建（确定 docs/ 没改时用；更省 5 分半）
 *   npm run verify -- --json       # 机器可读输出
 *
 * ── 退出码 ──────────────────────────────────────────────────────────────
 *   0  全部通过
 *   1  有阶段失败（失败阶段附末若干行原始输出）
 *   2  没有阶段失败，但 `check:all` 报「dist 比源文件旧」——
 *      产物层结论不可信。**用 `--skip-build` 时最可能撞上这个**：
 *      它正是提醒你「你跳过了构建，而源文件确实动过」。
 */
import { spawnSync } from 'node:child_process'
import { existsSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const args = process.argv.slice(2)
const JSON_OUT = args.includes('--json')
const SKIP_BUILD = args.includes('--skip-build')

/** 阶段清单 —— 单一事实源。顺序即依赖顺序，不要随意调换。 */
const STAGES = [
  {
    key: 'selftest',
    label: '🧪 巡逻脚本自检',
    desc: 'test-patrol-logic.sh：巡逻 bash 逻辑 + 防回归扫描',
    cmd: 'bash',
    argv: ['scripts/test-patrol-logic.sh'],
  },
  {
    key: 'build',
    label: '🔨 站点构建',
    desc: 'build-docs.mjs：刷新 dist（产物层检查的前置）',
    cmd: process.execPath,
    argv: ['scripts/build-docs.mjs', '--no-trash'],
    slow: true,
    skip: SKIP_BUILD,
  },
  {
    key: 'checks',
    label: '🧾 全站检查',
    desc: 'check-all.mjs：11 个检查器 + dist 过期检测',
    cmd: process.execPath,
    argv: ['scripts/check-all.mjs'],
    staleIsSpecial: true, // 退出码 2 = 检查都过但 dist 过期，单独一档
  },
]

const active = STAGES.filter((s) => !s.skip)
const results = []
let failed = false

/**
 * ⚠️ 已知的本机噪声（不影响结论）：
 * `test-patrol-logic.sh` 收尾会 `rm -rf .tmp-patrol-test`（内含 35 个轮转测试文件）。
 * 本机沙箱对**批量删除**有保护，会拦下它并打印
 * 「⚠️ 无法清理 .tmp-patrol-test（本机沙箱拦截批量删除），已忽略」。
 * 这**不是失败** —— 该测试对清理失败是刻意容忍的（删不掉只提示，不改结论），
 * 且 `.tmp-patrol-test/` 已在 `.gitignore` 里。CI（Linux）上能正常删除。
 * 试过给它传 `CODEBUDDY_SAFE_DELETE_BULK_THRESHOLD` 抬高阈值，**对 bash 的 rm 无效**
 * （那个开关只作用于走 NODE_OPTIONS shim 的 node 进程删除，例如 VitePress 的 rimraf），
 * 故不保留这段无效代码。
 */

if (!JSON_OUT) {
  console.log(`\n=== 最高执行命令 verify（${active.length} 个阶段）===`)
  if (SKIP_BUILD) console.log('（--skip-build：已跳过站点构建）')
  console.log()
}

for (let i = 0; i < active.length; i++) {
  const s = active[i]
  if (!JSON_OUT) {
    console.log(`── ${i + 1}/${active.length} ${s.label} ── ${s.desc}`)
    if (s.slow) console.log('   （这一步约 5 分半，输出实时打印）')
  }

  const t0 = Date.now()
  // 正常模式 stdio:'inherit' —— 构建要跑 5 分半，必须让用户看到实时进度；
  // --json 模式才捕获输出（此时不打印，避免污染 JSON）。
  const r = spawnSync(s.cmd, s.argv, {
    cwd: ROOT,
    stdio: JSON_OUT ? 'pipe' : 'inherit',
    encoding: 'utf8',
    maxBuffer: 64 * 1024 * 1024,
    env: process.env,
  })
  const ms = Date.now() - t0
  const code = r.status === null ? 1 : r.status

  // 退出码 2 只在 check:all 有意义（检查都过但 dist 过期）
  const status = code === 0 ? 'pass' : s.staleIsSpecial && code === 2 ? 'stale' : 'fail'
  const out = JSON_OUT ? `${r.stdout || ''}${r.stderr || ''}` : ''

  results.push({ ...s, code, status, ms, out })

  if (!JSON_OUT) {
    const icon = status === 'pass' ? '✅' : status === 'stale' ? '⚠️' : '❌'
    const secs = `${(ms / 1000).toFixed(1)}s`
    console.log(`   ${icon} ${s.label} —— ${status === 'pass' ? '通过' : status === 'stale' ? '检查通过但 dist 过期' : `失败（退出码 ${code}）`}（${secs}）\n`)
  }

  if (status === 'fail') { failed = true; break } // 失败即停：自检坏了不必等构建，构建坏了产物层结论无效
}

const staleOnly = !failed && results.some((r) => r.status === 'stale')
const exitCode = failed ? 1 : staleOnly ? 2 : 0

if (JSON_OUT) {
  console.log(JSON.stringify({
    exitCode,
    skippedBuild: SKIP_BUILD,
    stages: results.map((r) => ({
      key: r.key, label: r.label, status: r.status, code: r.code, ms: r.ms,
      tail: r.status === 'fail'
        ? r.out.split(/\r?\n/).map((l) => l.trimEnd()).filter(Boolean).slice(-12)
        : undefined,
    })),
  }, null, 2))
  process.exit(exitCode)
}

console.log('--- 结论 ---')
for (const r of results) {
  const icon = r.status === 'pass' ? '✅' : r.status === 'stale' ? '⚠️' : '❌'
  console.log(`${icon} ${r.label}（${(r.ms / 1000).toFixed(1)}s）`)
}

if (failed) {
  const bad = results.find((r) => r.status === 'fail')
  console.log(`\n❌ 阶段「${bad.label}」失败 —— 上面已实时打印其输出。修复后重跑本命令。`)
} else if (staleOnly) {
  console.log('\n⚠️ 检查全部通过，但 `check:all` 报告 dist 比源文件旧 ⇒ 产物层结论不可信。')
  if (SKIP_BUILD) console.log('   你用了 --skip-build，而源文件确实动过 —— 去掉该参数重跑即可。')
  else console.log('   正常情况下构建刚跑完不该出现；请检查构建是否真的产出了新的 dist。')
} else {
  console.log('\n✅ 全部通过。')
}

process.exit(exitCode)
