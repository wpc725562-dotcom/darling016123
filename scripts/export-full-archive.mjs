#!/usr/bin/env node
/**
 * 全集合并器 —— 把一科的所有材料合成一个 .md，用于「知识库 / 项目 / 文件上传」
 *
 * 为什么需要它：
 *   对话里贴不下（四科合计 188 万字 ≈ 280 万 token），但 ChatGPT Projects /
 *   Claude Projects / Gemini Gems / Kimi 文件 这类**知识库**是走 RAG 的，
 *   可以一次上传、长期复用。这时候「全给」才是对的。
 *   ⇒ 所以做 4 个科目全集 + 1 个总规则文件，共 5 个文件，上传 5 次就完了。
 *
 * 处理：
 *   1. 各源文件标题整体降一级（文件 H1 → 章 H2），让整本只有一套层级
 *   2. 每份前面插 `<!-- 来源：相对路径 -->` 注释，便于回溯
 *   3. 顶部自动生成目录（文件名清单）
 *
 * 输出：备考计划/网页AI开课包/12-全集-按科/
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.join(__dirname, '..');
const PACK = path.join(REPO, '备考计划', '网页AI开课包');
const OUT = path.join(PACK, '12-全集-按科');

const TODAY = '2026-11-03';

/** 递归列出目录下所有 .md（按文件名自然排序） */
function walkMd(dir) {
  if (!fs.existsSync(dir)) return [];
  const out = [];
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) out.push(...walkMd(p));
    else if (e.name.endsWith('.md')) out.push(p);
  }
  return out.sort((a, b) =>
    path.basename(a).localeCompare(path.basename(b), 'zh-Hans-CN', { numeric: true })
  );
}

/** 标题降一级：`# ` → `## `，最多到 ###### */
function demote(text) {
  return text.replace(/^(#{1,5})(\s)/gm, '#$1$2');
}

/** 去掉文件自带的「用法/来源」抬头块。
 *  这些文件统一是「# 标题 + 若干 > 引用行 + --- 分隔线 + 正文」的结构，
 *  所以只切到**前 25 行内第一条 `---` 分隔线**为止 —— 不能按「凡是 > 行就删」，
 *  那会把正文里的提示框、引言全吃掉（第一版就是这么写的，计算机全集少了 0.25 MB）。 */
function stripUsageHeader(text) {
  const lines = text.split('\n');
  let start = 0;
  while (start < lines.length && lines[start].trim() === '') start++;
  // 保留文件自己的 H1 —— 它说明「这份材料叫什么」，合集里靠它分节
  const h1 = start < lines.length && /^#\s/.test(lines[start]) ? lines[start] : null;
  const limit = Math.min(lines.length, 30);
  for (let i = start; i < limit; i++) {
    if (/^---+\s*$/.test(lines[i])) {
      const body = lines.slice(i + 1).join('\n').trim();
      return h1 ? `${h1}\n\n${body}` : body;
    }
  }
  return text.trim();
}

function buildSubject({ label, title, intro, sources }) {
  const sections = [];
  const toc = [];

  for (const s of sources) {
    let files = s.dir ? walkMd(s.dir) : [s.file];
    if (s.only) files = files.filter((f) => s.only.test(path.basename(f)));
    const parts = [];
    for (const f of files) {
      const rel = path.relative(PACK, f).replace(/\\/g, '/');
      const raw = fs.readFileSync(f, 'utf8').replace(/\r\n/g, '\n');
      const body = demote(stripUsageHeader(raw));
      parts.push(`<!-- 来源：${rel} -->\n\n${body}`);
      toc.push({ group: s.name, file: path.basename(f), rel });
    }
    if (parts.length) {
      sections.push(`# ${s.name}\n\n${parts.join('\n\n---\n\n')}`);
    }
  }

  // 目录按组聚合
  const grouped = new Map();
  for (const t of toc) {
    if (!grouped.has(t.group)) grouped.set(t.group, []);
    grouped.get(t.group).push(t.file);
  }
  let tocMd = '';
  for (const [g, fs_] of grouped) {
    tocMd += `\n**${g}**（${fs_.length} 份）\n\n`;
    tocMd += fs_.map((f) => `- ${f}`).join('\n') + '\n';
  }

  const totalChars = sections.join('\n').length;
  return `# ${title} · 全集

> **这是什么**：${intro}
> **体量**：约 **${totalChars} 字** / ${(Buffer.byteLength(sections.join('\n')) / 1024 / 1024).toFixed(2)} MB。
> **怎么用**：
> - 平台有**项目 / 知识库 / 文件上传** → 把这个文件上传进去，**一次就够**，之后所有对话共享，不用再贴。
> - 平台只能**对话框粘贴** → **别贴这个**（太大，会截断）。改贴 \`6-考点原文-按章贴\` 或 \`10-讲义-按节贴\` 里的单份小文件。
> **导出于**：${TODAY}

---

## 目录
${tocMd}
---

${sections.join('\n\n---\n\n')}
`;
}

function buildRules() {
  const files = [
    '0-教练规则-每个新对话都贴.md',
    '1-C语言-状态卡.md',
    '2-高等数学-状态卡.md',
    '4-英语-状态卡.md',
    '5-政治-状态卡.md',
  ];
  const parts = files.map((f) => {
    const raw = fs.readFileSync(path.join(PACK, f), 'utf8').replace(/\r\n/g, '\n');
    return `<!-- 来源：${f} -->\n\n${demote(stripUsageHeader(raw))}`;
  });
  const totalChars = parts.join('\n').length;
  return `# 总规则与四科状态卡

> **这是什么**：教练规则（13 条）+ 四科状态卡。**这是每次开新对话必贴的那一份**，
> 即使平台有知识库，也建议**把它单独贴进对话**（因为它是「当下的进度」，会变）。
> **体量**：约 **${totalChars} 字** / ${(Buffer.byteLength(parts.join('\n')) / 1024).toFixed(1)} KB —— 任何模型都吃得下。
> **导出于**：${TODAY}

---

${parts.join('\n\n---\n\n')}
`;
}

function main() {
  fs.mkdirSync(OUT, { recursive: true });

  const jobs = [
    {
      file: '00-总规则与状态卡.md',
      content: () => buildRules(),
    },
    {
      file: '计算机-全集.md',
      content: () =>
        buildSubject({
          label: '计算机',
          title: '计算机基础与程序设计（C 语言 + 数据结构）',
          intro: '考点原文（按章）+ 讲义页（按节）+ 错题本 + 真题考点映射表。**200 分，四科里分值最高。**',
          sources: [
            { name: '第一部分　考点原文（按章）', dir: path.join(PACK, '6-考点原文-按章贴', '计算机') },
            { name: '第二部分　讲义（按节）', dir: path.join(PACK, '10-讲义-按节贴', '计算机') },
            { name: '第三部分　错题本', file: path.join(PACK, '7-错题本-按科贴', '计算机错题本.md') },
            { name: '第四部分　真题考点映射表', file: path.join(PACK, '9-真题映射', '计算机-真题考点映射表-2021至2026.md') },
          ],
        }),
    },
    {
      file: '高数-全集.md',
      content: () =>
        buildSubject({
          label: '高数',
          title: '高等数学',
          intro: '考点原文（按章）+ 讲义页（按节）+ 错题本 + 真题映射表与分值分布。',
          sources: [
            { name: '第一部分　考点原文（按章）', dir: path.join(PACK, '6-考点原文-按章贴', '高数') },
            { name: '第二部分　讲义（按节）', dir: path.join(PACK, '10-讲义-按节贴', '高数') },
            { name: '第三部分　错题本', file: path.join(PACK, '7-错题本-按科贴', '高数错题本.md') },
            { name: '第四部分　真题考点映射表', file: path.join(PACK, '9-真题映射', '高数-真题考点映射表-2019至2026.md') },
            { name: '第五部分　真题分值分布', file: path.join(PACK, '9-真题映射', '高数-真题分值分布-2003至2026.md') },
          ],
        }),
    },
    {
      file: '英语-全集.md',
      content: () =>
        buildSubject({
          label: '英语',
          title: '英语',
          intro: '考点原文（按语法组）+ 讲义页（按题型）+ 错题本 + 真题考点分布。**无听力。**',
          sources: [
            { name: '第一部分　考点原文（按语法组）', dir: path.join(PACK, '6-考点原文-按章贴', '英语') },
            { name: '第二部分　讲义（按题型）', dir: path.join(PACK, '10-讲义-按节贴', '英语') },
            { name: '第三部分　错题本', file: path.join(PACK, '7-错题本-按科贴', '英语错题本.md') },
            { name: '第四部分　真题考点分布', file: path.join(PACK, '9-真题映射', '英语-真题考点分布-2008至2025.md') },
          ],
        }),
    },
    {
      file: '政治-全集.md',
      content: () =>
        buildSubject({
          label: '政治',
          title: '政治理论',
          intro:
            '考点原文（按章）+ 讲义（按章）+ **64 篇默写册（默写区+答案区）** + 错题本 + 真题映射表 + 2012–2019 八年原卷。**100 分，0 起点，唯一瓶颈。**',
          sources: [
            { name: '第一部分　考点原文（按章）', dir: path.join(PACK, '6-考点原文-按章贴', '政治') },
            { name: '第二部分　讲义（按章）', dir: path.join(PACK, '10-讲义-按节贴', '政治') },
            { name: '第三部分　A 档默写 64 篇', dir: path.join(PACK, '8-政治默写-按篇贴') },
            { name: '第四部分　错题本', dir: path.join(PACK, '7-错题本-按科贴'), only: /^政治-/ },
            { name: '第五部分　真题考点映射表', file: path.join(PACK, '9-真题映射', '政治-真题考点映射表-2015至2025.md') },
            { name: '第六部分　真题原卷 2012–2019', dir: path.join(PACK, '11-政治真题-按年贴') },
          ],
        }),
    },
  ];

  let total = 0;
  for (const j of jobs) {
    const content = j.content();
    const outFile = path.join(OUT, j.file);
    fs.writeFileSync(outFile, content, 'utf8');
    const mb = Buffer.byteLength(content) / 1024 / 1024;
    total += mb;
    console.log(
      `${j.file.padEnd(22)} ${mb.toFixed(2)} MB · 约 ${[...content].length} 字`
    );
  }
  console.log(`\n合计 ${jobs.length} 个文件 / ${total.toFixed(2)} MB`);
}

main();
