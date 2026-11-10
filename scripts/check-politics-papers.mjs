#!/usr/bin/env node
/**
 * 政治卷面结构检查：多选题必须是 A–D 四选项
 *
 * 为什么需要这个检查：
 *   广东专升本政治多选题是**固定四选项**（A/B/C/D），历年真题无一例外。
 *   但「中国式现代化的五个特色」「新发展理念的五个理念」这类知识点天然是 5 项，
 *   出题时很容易顺手加个 E 选项 —— 一旦出现，学生练的就是**考场不存在的题型**，
 *   而且会让「全选 ABCD」这条策略失效（变成全选 ABCDE）。
 *   2026-10-19 实测卷一第 21、23 题就是这种情况，已改。
 *
 * 检查范围：
 *   docs/posts/politics/*.md（真题）与 docs/posts/politics/模拟卷/*.md（模拟卷）
 *
 * 判定：
 *   在「多项选择题」区段内出现行首 `E.` / `E、`，或答案里出现 E，即报错。
 *
 * 用法：node scripts/check-politics-papers.mjs [--json]
 * 退出码：0 通过；1 发现问题
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const POLITICS = path.join(__dirname, '..', 'docs', 'posts', 'politics');

const RE_MC_HEAD = /^#{2,3}\s*二、多项选择/m;
const RE_NEXT_HEAD = /^#{2,3}\s*三、[辨简问论材]/m;

/**
 * 选项行：`E. xxx` / `E、xxx` / `- E. xxx` / `- **E.** xxx`
 * 最后一种（`- **E.**`）是真题正文格式，必须覆盖，否则会漏。
 */
const RE_E_OPTION = /^\s*[-*]?\s*\*{0,2}E\*{0,2}\s*[.、．]\s*\S/m;

/**
 * 答案行有**两种格式**，必须都覆盖（这是本检查第一次写时的漏洞）：
 *   ① 真题：`**答案：ABCD**`
 *   ② 模拟卷答案页：表格 `| 23 | **ABCDE** | 新发展理念 | 解析 |`
 * 只写 ① 会漏掉全部模拟卷答案页。
 *
 * 另外必须用 matchAll **扫全部**，不能只取第一个 —— 第二次踩的坑：
 * 表格里第 21 题是 `| 21 | **ABC** |`，match 只返回它，第 23 题的 ABCDE 永远看不到。
 */
const ANSWER_PATTERNS = [
  ['答案含 E（内联）', /答案\s*[:：]\s*\**\s*([A-E]{2,6})/g],
  ['答案含 E（表格）', /^\|\s*\d+\s*\|\s*\**\s*([A-E]{2,6})\s*\**\s*\|/gm],
];

function collectPapers() {
  const out = [];
  for (const name of fs.readdirSync(POLITICS)) {
    if (name.endsWith('.md') && /^\d{4}/.test(name)) out.push(path.join(POLITICS, name));
  }
  const mockDir = path.join(POLITICS, '模拟卷');
  if (fs.existsSync(mockDir)) {
    for (const name of fs.readdirSync(mockDir)) {
      if (name.endsWith('.md')) out.push(path.join(mockDir, name));
    }
  }
  return out.sort();
}

function mcSegment(text) {
  const head = text.search(RE_MC_HEAD);
  if (head < 0) return null;
  let seg = text.slice(head);
  const nextRel = seg.slice(5).search(RE_NEXT_HEAD);
  if (nextRel > 0) seg = seg.slice(0, nextRel + 5);
  return seg;
}

function main() {
  const asJson = process.argv.includes('--json');
  const papers = collectPapers();
  const problems = [];
  let checked = 0;

  for (const f of papers) {
    const rel = path.relative(path.join(__dirname, '..'), f).replace(/\\/g, '/');
    const seg = mcSegment(fs.readFileSync(f, 'utf8'));
    if (seg === null) continue; // 没有多选章节（如纯答案页），跳过
    checked++;
    if (RE_E_OPTION.test(seg)) {
      const line = seg.split('\n').find((l) => RE_E_OPTION.test(l));
      problems.push({ file: rel, type: 'E 选项', detail: line.trim() });
    }
    // 两种答案格式都扫全部匹配；答案里只要出现 E 就算问题
    for (const [label, re] of ANSWER_PATTERNS) {
      for (const m of seg.matchAll(re)) {
        if (m[1] && m[1].includes('E')) {
          problems.push({ file: rel, type: label, detail: m[0].trim() });
          break; // 同一文件同类问题只报一次，避免刷屏
        }
      }
    }
  }

  if (asJson) {
    console.log(JSON.stringify({ checked, problems }, null, 2));
  } else {
    console.log('=== 政治卷面结构检查 · 多选题必须 A–D 四选项 ===');
    console.log(`已检查 ${checked} 份卷子的多选区段\n`);
    if (problems.length === 0) {
      console.log('✅ 未发现 E 选项，全部为四选项结构。');
    } else {
      console.log(`❌ 发现 ${problems.length} 处问题：`);
      for (const p of problems) console.log(`  · [${p.type}] ${p.file}\n      ${p.detail}`);
      console.log('\n⇒ 真题多选题只有 A/B/C/D。若知识点是 5 项，请只列其中 4 项（或 3 对 1 错），');
      console.log('  并在解析里注明「第 5 项是什么」，不要加 E 选项。');
    }
  }

  process.exit(problems.length ? 1 : 0);
}

main();
