#!/usr/bin/env node
// 双轨合并报告：易错点地图 × 章节审计报告 join
// 产出：按 chapter_id 聚合的「易错点 + 真题覆盖」联合视图
// 用法：node scripts/_join-errormap-audit.mjs

import {readFileSync, readdirSync, writeFileSync} from 'node:fs';
import {join} from 'node:path';

const ROOT = process.cwd();
const ERRORMAP = join(ROOT, '备考计划/易错点地图.json');
const AUDIT_DIR = join(ROOT, 'docs/posts/computer/notes');
const OUTPUT = join(ROOT, '备考计划/易错点地图-章节审计-联合报告-2026-10-04.md');

// ---------- 读 errormap ----------
const emRaw = readFileSync(ERRORMAP, 'utf8');
const em = JSON.parse(emRaw);

// 按 chapter_id 分组 cats
const emByChapter = {};
for (const cat of em.cats) {
  const k = cat.chapter_id || '_unmapped';
  if (!emByChapter[k]) emByChapter[k] = [];
  emByChapter[k].push(cat);
}

// ---------- 读 audit-*.md ----------
const auditFiles = readdirSync(AUDIT_DIR)
  .filter(f => /^audit-/.test(f) && f.endsWith('.md'));

const audits = [];
for (const f of auditFiles) {
  const content = readFileSync(join(AUDIT_DIR, f), 'utf8');
  const fmMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
  const fm = fmMatch ? fmMatch[1] : '';
  const titleMatch = fm.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  const tagsMatch = fm.match(/^tags:\r?\n((?:\s+-\s+.+\r?\n?)+)/m);
  const tags = tagsMatch ? tagsMatch[1].split(/\r?\n/).map(l => l.replace(/^\s+-\s+/, '').trim()).filter(Boolean) : [];

  // 提取历年真题关联矩阵行
  const yearStats = {};
  const lines = content.split(/\r?\n/);
  let inMatrix = false;
  for (const line of lines) {
    if (/^##\s+一、历年真题关联矩阵/.test(line)) { inMatrix = true; continue; }
    if (inMatrix && /^##\s+/.test(line)) break;  // 进入下一节
    if (!inMatrix) continue;
    // 表格行: | 2021 | 单选11 | 选择 | ... |
    const m = line.match(/^\|\s*(20\d{2})\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|/);
    if (m) {
      const [, year, tihao, tixing, kaodian, fenzhi, nandu] = m;
      if (!yearStats[year]) yearStats[year] = { count: 0, fen: 0 };
      yearStats[year].count++;
      const fz = parseFloat(fenzhi.replace(/[^\d.]/g, ''));
      if (!isNaN(fz)) yearStats[year].fen += fz;
    }
  }

  // 提取 4 年合计那句
  const totalMatch = content.match(/\*\*4年合计：(\d+)题，年均([\d.]+)题，估分约(\d+)分\*\*/);
  const totalQuestions = totalMatch ? parseInt(totalMatch[1]) : 0;
  const perYear = totalMatch ? parseFloat(totalMatch[2]) : 0;
  const totalScore = totalMatch ? parseInt(totalMatch[3]) : 0;

  // 提取 chapter_id
  const chapMatch = titleMatch ? titleMatch[1].match(/(\d+\.\d+)/) : null;
  const chapterId = chapMatch ? chapMatch[1] : null;

  audits.push({
    file: f,
    title: titleMatch ? titleMatch[1] : f,
    tags,
    chapterId,
    yearStats,
    totalQuestions,
    perYear,
    totalScore,
  });
}

// ---------- 生成报告 ----------
const lines = [];
lines.push('# 易错点地图 × 章节审计 联合报告');
lines.push('');
lines.push(`> 生成时间：2026-10-04`);
lines.push(`> 数据源：备考计划/易错点地图.json (9 个 cat) + docs/posts/computer/notes/audit-*.md (${audits.length} 篇)`);
lines.push(`> 目的：把两条独立维护的错误追踪轨统一到一个视图，方便「哪个章节错最多 + 真题最多 + 缺口在哪」一句话说清`);
lines.push('');
lines.push('## 一、易错点 × 真题 按章节覆盖矩阵');
lines.push('');
lines.push('| chapter_id | 易错点 cat | 真题覆盖 | 4年合计 | 缺口 |');
lines.push('|:---:|:---|:---|---:|:---|');

const allChapterIds = new Set([...Object.keys(emByChapter), ...audits.map(a => a.chapterId).filter(Boolean)]);
const sorted = [...allChapterIds].sort();

for (const cid of sorted) {
  const cats = emByChapter[cid] || [];
  const audit = audits.find(a => a.chapterId === cid);
  const catNames = cats.map(c => `${c.id}(${c.items.length})`).join('+') || '-';
  const realQuestions = audit ? `${audit.totalQuestions}题/${audit.totalScore}分` : '-';
  const covered = (cats.length > 0 ? '✓' : '✗') + (audit ? '✓' : '✗');
  const gap = !audit ? '**无审计**' : (cats.length === 0 ? '**易错点未映射**' : '-');
  lines.push(`| ${cid || '?'} | ${catNames} | ${realQuestions} | ${audit ? audit.totalQuestions : '-'} | ${gap} |`);
}

lines.push('');
lines.push('**图例**：✓ = 已有；✗ = 缺失；粗体 = 缺口');
lines.push('');

// ---------- 二、按 cat 详表 ----------
lines.push('## 二、易错点 cat 详表');
lines.push('');
for (const cat of em.cats) {
  lines.push(`### ${cat.name}（${cat.id}）`);
  lines.push(`- 章节：${cat.chapter || '?'}（chapter_id=${cat.chapter_id || '?'}）`);
  lines.push(`- 学科：${cat.subject || '?'}`);
  lines.push(`- 易错点数：${cat.items.length}`);
  // 关联审计（如果 chapter_id 匹配）
  const matched = cat.chapter_id ? audits.filter(a => a.chapterId === cat.chapter_id) : [];
  if (matched.length > 0) {
    lines.push(`- 关联审计：${matched.map(m => m.title).join('、')}`);
    for (const m of matched) {
      lines.push(`  - ${m.totalQuestions}题 / ${m.totalScore}分（4年合计）`);
    }
  } else {
    lines.push(`- 关联审计：**未匹配**（该 cat 在审计章节中无对应）`);
  }
  lines.push('');
}

lines.push('## 三、缺口清单');
lines.push('');
const gaps = [];
for (const cat of em.cats) {
  if (!cat.chapter_id) gaps.push(`- 易错点 cat ${cat.id} (${cat.name}) 未映射 chapter_id`);
  else if (!audits.find(a => a.chapterId === cat.chapter_id)) {
    gaps.push(`- 易错点 cat ${cat.id} (${cat.name}) 映射到 chapter_id=${cat.chapter_id}, 但该章节无 audit 报告`);
  }
}
for (const a of audits) {
  if (!a.chapterId) gaps.push(`- 审计 ${a.file} 标题无章节号，无法 join`);
}
if (gaps.length === 0) lines.push('无缺口。');
else gaps.forEach(g => lines.push(g));

lines.push('');
lines.push('---');
lines.push('');
lines.push(`## 附：脚本 + 元数据`);
lines.push('');
lines.push(`- 脚本路径：\`scripts/_join-errormap-audit.mjs\``);
lines.push(`- errormap 字段：cats / chapter / chapter_id / subject（来自 commit 825a2ac）`);
lines.push(`- audit 字段：tags / chapterId / yearStats / totalQuestions / totalScore（解析自历年真题关联矩阵节）`);
lines.push(`- join key：chapter_id（如 '1.5'）`);
lines.push(`- 输出：\`备考计划/易错点地图-章节审计-联合报告-2026-10-04.md\``);

writeFileSync(OUTPUT, lines.join('\n'), 'utf8');
console.log(`已生成：${OUTPUT}`);
console.log(`- 易错点 cat: ${em.cats.length}`);
console.log(`- audit 文件: ${audits.length}`);
console.log(`- join 上的 chapter: ${sorted.filter(s => emByChapter[s] && audits.find(a => a.chapterId === s)).length} 个`);
console.log(`- 缺口: ${gaps.length} 条`);
