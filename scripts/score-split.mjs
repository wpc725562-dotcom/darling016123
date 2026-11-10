#!/usr/bin/env node
/**
 * 计算机卷面分值拆分：C 语言 / 数据结构各多少分
 *
 * 为什么需要这个脚本：
 *   仓库里对「数据结构占多少分」有 3 种说法，散落 12+ 处：
 *     · 约 100 分 —— 按「试卷两半各一半」粗估
 *     · 85 分     —— 考纲模块表行值之和（考纲表本身漏项）
 *     · 71 分     —— 真题逐题标注分值、两年平均
 *   前两个是估算，第三个是实测。差 29 分（29%），足以让复习时间分配错。
 *
 * 数据源：`scripts/考点主清单-计算机.json` 的 `score_weight` 字段。
 *   样本：**2023 真题 + 2024 真题**，各 45 题、共 90 题，逐题标注分值后两年平均。
 *   出处：`docs/guide/真题考频矩阵.md` 的「判断 1」表（C 语言 138/120、数据结构 62/80）。
 *
 * ⚠️ **不要和另一个 90 题样本搞混**：
 *   `资料/高频考点统计/计算机-高频考点TOP20.md` 的样本是 **2021 + 2024**，
 *   那份统计的是「**出现次数**」，不是分值。两个不同的 90 题样本：
 *     · 分值 → 2023+2024（本脚本）
 *     · 次数 → 2021+2024（第八节 TOP15 表）
 *   2026-10-19 就因为只看 TOP20 文件第一行，差点把全站「2023+2024」误改成「2021+2024」。
 *
 * 硬约束：19 个模块的 score_weight 之和必须 == 200（试卷满分）。
 *   不成立就 exit 1 —— 说明清单被改坏了，或某个模块的权重被误改。
 *
 * 用法：
 *   node scripts/score-split.mjs          # 人读
 *   node scripts/score-split.mjs --json   # 机读
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const MANIFEST = path.join(__dirname, '考点主清单-计算机.json');
const FULL_MARK = 200;

/**
 * 模块归类白名单。**不用关键词猜**（「数组」同时出现在 C 语言数组和「串、数组和广义表」里，
 * 靠 includes('数组') 会把两个都算进去）。名字必须精确匹配，对不上就报错。
 */
const SUBJECT_OF = {
  // C 语言（考纲 ①–⑪）
  'C语言基础与数据运算': 'C语言',
  '顺序结构程序设计': 'C语言',
  '选择结构': 'C语言',
  '循环结构': 'C语言',
  '数组': 'C语言',
  '函数': 'C语言',
  '指针': 'C语言',
  '结构体与共用体': 'C语言',
  '文件': 'C语言',
  '程序运行环境与调试': 'C语言',
  // 数据结构（考纲 ⑫–㉑）
  '数据结构基本概念': '数据结构',
  '线性表': '数据结构',
  '栈和队列': '数据结构',
  '串、数组和广义表': '数据结构',
  '树和二叉树': '数据结构',
  '图': '数据结构',
  '查找': '数据结构',
  '排序': '数据结构',
  '算法概念与分析': '数据结构',
};

function loadManifest() {
  const raw = JSON.parse(fs.readFileSync(MANIFEST, 'utf8'));
  return Array.isArray(raw) ? raw : Object.values(raw);
}

function main() {
  const asJson = process.argv.includes('--json');
  const rows = loadManifest();
  const byModule = new Map();
  const unknown = [];

  for (const r of rows) {
    const mod = r.module;
    const w = parseFloat(String(r.score_weight ?? '0').replace(/[^0-9.]/g, '')) || 0;
    if (!SUBJECT_OF[mod]) {
      unknown.push(mod);
      continue;
    }
    const cur = byModule.get(mod) || { n: 0, w: 0 };
    cur.n++;
    cur.w += w;
    byModule.set(mod, cur);
  }

  const problems = [];
  if (unknown.length) {
    problems.push(`清单里有未归类的模块：${[...new Set(unknown)].join('、')}（请在 SUBJECT_OF 里补上）`);
  }

  const modules = [...byModule.entries()]
    .map(([name, v]) => ({ name, n: v.n, weight: v.w, subject: SUBJECT_OF[name] }))
    .sort((a, b) => b.weight - a.weight);

  const total = modules.reduce((s, m) => s + m.weight, 0);
  if (Math.abs(total - FULL_MARK) > 0.05) {
    problems.push(`模块权重合计 ${total.toFixed(1)} ≠ 试卷满分 ${FULL_MARK}（清单被改坏了）`);
  }

  const split = {};
  for (const m of modules) split[m.subject] = (split[m.subject] || 0) + m.weight;

  if (asJson) {
    console.log(JSON.stringify({ sample: '2023+2024 各 45 题，共 90 题', total, split, modules, problems }, null, 2));
    process.exit(problems.length ? 1 : 0);
  }

  console.log('=== 计算机卷面分值拆分（真题逐题标注 · 两年平均）===');
  console.log('样本：2023 真题 45 题 + 2024 真题 45 题 = 90 题');
  console.log('来源：scripts/考点主清单-计算机.json 的 score_weight 字段');
  console.log('⚠️ 与「2021+2024 出现次数榜」是两个不同样本，别混用。\n');
  console.log('模块 | 条目 | 分值/卷 | 归属');
  console.log(':---|:---:|:---:|:---');
  for (const m of modules) {
    console.log(`${m.name} | ${m.n} | ${m.weight.toFixed(1)} | ${m.subject}`);
  }
  console.log(`**合计** | **${modules.reduce((s, m) => s + m.n, 0)}** | **${total.toFixed(1)}** |`);

  console.log('\n=== 分部小计 ===');
  for (const [sub, w] of Object.entries(split).sort((a, b) => b[1] - a[1])) {
    console.log(`${sub}：${w.toFixed(1)} 分（${((w / FULL_MARK) * 100).toFixed(1)}%）`);
  }

  console.log('\n=== 与其它口径的差 ===');
  const ds = split['数据结构'] || 0;
  console.log(`本口径（实测）      数据结构 ${ds.toFixed(1)} 分`);
  console.log(`「试卷两半各一半」   数据结构 100 分  → 比实测多 ${(100 - ds).toFixed(1)} 分（高估 ${(((100 - ds) / ds) * 100).toFixed(0)}%）`);
  console.log(`「考纲模块表行值之和」 数据结构 85 分   → 比实测多 ${(85 - ds).toFixed(1)} 分`);
  console.log('⇒ 复习时间分配请用**实测口径**；估算口径只够判断「量级」。');

  if (problems.length) {
    console.log('\n⚠️ 发现问题：');
    for (const p of problems) console.log('  - ' + p);
  } else {
    console.log('\n✅ 19 个模块权重合计 = 200，与试卷满分一致。');
  }

  process.exit(problems.length ? 1 : 0);
}

main();
