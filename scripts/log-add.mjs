#!/usr/bin/env node
/**
 * 学习日志写入器 —— 在写的那一刻就拦住「没有考点编号」的记录
 *
 * 为什么需要它：
 *   掌握度引擎（`mastery-core.js`）要求**同一个 key 至少出现 3 次**才可能判过关。
 *   2026-10-19 实测：328 个自由文本考点名里只有 2 个出现过第二次（0.6%），
 *   而 5 个 `#Cxxx` 稳定编号里有 4 个出现过第二次（80%）—— 差 130 倍。
 *   引擎已经在 2026-10-19 改成「编号优先」，但**写入侧没跟上**：
 *   91 条 quiz 里只有 7 条带编号（7.7%），所以引擎基本还在空转。
 *
 *   「规范写在 AI路由表 里」这件事已经证明不够 —— 规范写了 15 天，执行率 7.7%。
 *   所以把它做成一个**绕不过去的入口**：想写日志，就走这个脚本。
 *
 * 校验（任一不过就 exit 1，不写盘）：
 *   · kind 在 log-schema 白名单里
 *   · subject 在 log-schema 白名单里（别名会自动纠正并提示）
 *   · quiz 必须有 mastery
 *   · **quiz 的 title 或 weak 必须含 `#C数字` / `#M数字` / `#E数字`**
 *     （除非显式传 `--no-id`，用于「整章综合测」这类确实没有单一考点的场景）
 *
 * 用法：
 *   node scripts/log-add.mjs --date 2026-10-19 --subject C语言 --kind quiz \
 *     --title "1.7 函数关口题 8 题 #C002 #C007" --mastery passed --score 7/8 \
 *     --weak "第3题作用域-同名" --dry
 *
 *   去掉 --dry 才会真正追加。建议先 --dry 看一眼。
 *
 * 退出码：0 写入成功（或 dry 通过）；1 校验失败，未写盘
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { KINDS, SUBJECTS, ALIASES, MASTERY, DATE_RE, RE_KP_ID } from './lib/log-schema.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const LOG = path.join(__dirname, '..', '备考计划', '学习日志.jsonl');

/** 考点编号正则：`#C002`（C语言）/ `#D001`（数据结构）/ `#M013`（高数）/ `#E007`（英语）
 *  ⚠️ 2026-10-19 补 D：`考点主清单-计算机.json` 里数据结构用的是 `D01`–`D09`，
 *  原来只认 C/M/E，写 `#D01` 会被判成「没有编号」—— 报错信息还会指错方向。
 *  ⚠️ 2026-10-25 抽到 `lib/log-schema.mjs`：本文件和 `check-study-log.mjs` 各写一份，
 *  两份已经漂了（校验器那份没补 D）⇒ 写进去的记录会被校验器判成无编号。现统一从 lib 引。 */

function parseArgs(argv) {
  const out = { dry: false, noId: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--dry') { out.dry = true; continue; }
    if (a === '--no-id') { out.noId = true; continue; }
    if (!a.startsWith('--')) continue;
    const key = a.slice(2);
    const val = argv[i + 1];
    if (val === undefined || val.startsWith('--')) {
      out[key] = true;
    } else {
      out[key] = val;
      i++;
    }
  }
  return out;
}

function fail(msg, hint) {
  console.error('❌ ' + msg);
  if (hint) console.error('   ⇒ ' + hint);
  process.exit(1);
}

function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.date || !args.subject || !args.kind || !args.title) {
    fail(
      '缺必填参数（date / subject / kind / title）',
      '例：node scripts/log-add.mjs --date 2026-10-19 --subject C语言 --kind quiz --title "… #C002" --mastery passed --dry'
    );
  }

  if (!DATE_RE.test(args.date)) {
    fail(`date 格式不对：${args.date}`, '要 YYYY-MM-DD，如 2026-10-19');
  }

  if (!KINDS.includes(args.kind)) {
    fail(`kind 不在白名单：${args.kind}`, `允许：${KINDS.join(' / ')}`);
  }

  let subject = args.subject;
  if (!SUBJECTS.includes(subject)) {
    const fixed = ALIASES[subject];
    if (fixed) {
      console.error(`⚠️ 科目名「${subject}」是别名，已按规范名「${fixed}」写入。`);
      subject = fixed;
    } else {
      fail(`subject 不在白名单：${args.subject}`, `允许：${SUBJECTS.join(' / ')}`);
    }
  }

  if (args.mastery && !MASTERY.includes(args.mastery)) {
    fail(`mastery 不在白名单：${args.mastery}`, `允许：${MASTERY.join(' / ')}`);
  }

  // quiz 必须有 mastery —— 引擎以它为准，缺了就只能靠 score 猜，而 score 是过程叙述
  if (args.kind === 'quiz' && !args.mastery) {
    fail(
      'quiz 必须带 --mastery（引擎以它为准，不靠 score 判对错）',
      `例：--mastery passed　允许：${MASTERY.join(' / ')}`
    );
  }

  // 核心闸门：quiz 必须带考点编号
  const idText = `${args.title} ${args.weak || ''}`;
  if (args.kind === 'quiz' && !RE_KP_ID.test(idText) && !args.noId) {
    fail(
      'quiz 的 title 里没有考点编号 —— 引擎攒不起来，这条记录等于白写',
      '在 title 里加 `#C006`（C语言）/ `#D001`（数据结构）/ `#M013`（高数）/ `#E007`（英语）这类稳定编号；\n' +
        '     引擎会把 `#C6` / `#C06` / `#C006` 都归一到 `#C006`，写成 3 位最省事；\n' +
        '     确实没有单一考点的整章综合测，显式加 `--no-id` 豁免。'
    );
  }
  if (args.kind === 'quiz' && args.noId) {
    console.error('⚠️ 用了 --no-id：这条 quiz 不会进掌握度累积，只作学习量记录。');
  }

  const record = { date: args.date, subject, kind: args.kind, title: args.title };
  if (args.score) record.score = args.score;
  if (args.mastery) record.mastery = args.mastery;
  if (args.weak) record.weak = args.weak;
  if (args.note) record.note = args.note;

  const line = JSON.stringify(record);

  if (args.dry) {
    console.log('=== dry run · 不会写盘 ===');
    console.log(line);
    console.log('\n✅ 校验通过。去掉 --dry 再跑一次才会真正追加。');
    return;
  }

  fs.appendFileSync(LOG, line + '\n', 'utf8');
  console.log('✅ 已追加到 ' + path.relative(path.join(__dirname, '..'), LOG));
  console.log(line);

  if (args.kind === 'quiz' && !args.noId) {
    /* 2026-11-03：原来这里硬编码 `[CDME]` + `\d{1,3}`，与 RE_KP_ID（`[CDMEP]` + `\d{1,4}`）
       不是同一个正则。后果有两个：政治 `#P122` 校验能过、提示里的记账编号却是空的；
       `#P1211` 这种 4 位编号还会被截成 3 位。改为从 RE_KP_ID.source 派生，
       以后改 lib 里的正则，这里自动跟上，不会再漂。 */
    const RE_KP_ID_G = new RegExp(RE_KP_ID.source, 'g');
    const ids = [...idText.matchAll(RE_KP_ID_G)].map((m) => {
      const digits = m[0].replace(/[^\d]/g, '');
      return '#' + m[1].toUpperCase() + String(parseInt(digits, 10)).padStart(3, '0');
    });
    console.log(`\n📌 记账编号：${[...new Set(ids)].join('、')}　（引擎按这些编号累积次数）`);
  }
}

main();
