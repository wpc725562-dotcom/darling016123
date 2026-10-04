#!/usr/bin/env node
// 把工作室的 inbox 事件沉淀回笔记库主仓
// 用法：node scripts/studio-receiver.mjs [--watch]
//   一次性模式（默认）：处理 inbox 所有事件，写入 学习日志.jsonl
//   --watch：每 60s 跑一次，可由 systemd / Task Scheduler / WorkBuddy 自动化驱动

import {readFileSync, appendFileSync, existsSync, mkdirSync, renameSync, statSync} from 'node:fs';
import {dirname, join} from 'node:path';

const ROOT = process.cwd();
const INBOX = join(ROOT, '备考计划/_inbox/studio-events.jsonl');
const STUDY_LOG = join(ROOT, '备考计划/学习日志.jsonl');

function processInbox() {
  if (!existsSync(INBOX)) {
    return { ok: true, processed: 0, reason: 'inbox 不存在' };
  }

  const content = readFileSync(INBOX, 'utf8');
  const lines = content.split('\n').filter(Boolean);
  if (lines.length === 0) {
    // 空文件直接归档
    renameSync(INBOX, INBOX + '.processed-' + Date.now());
    return { ok: true, processed: 0, reason: 'inbox 空' };
  }

  let okCount = 0, badCount = 0;
  let studyAppend = 0;

  mkdirSync(dirname(STUDY_LOG), { recursive: true });

  for (const line of lines) {
    let ev;
    try {
      ev = JSON.parse(line);
    } catch (e) {
      badCount++;
      continue;
    }

    // 只把学习轨迹写到 学习日志.jsonl
    // inbox 事件当前两种 type：
    //   - progress: { keys, patch } —— 今日勾选 / 番茄钟累计
    //   - mastery:  { kp, ok, src } —— 知识点判分
    //   错题目前没有 POST 入站（走 mistake-stats 反向计算）
    if (ev.type === 'progress' || ev.type === 'mastery') {
      const entry = {
        ts: ev.ts,
        type: ev.type,
        ...ev.payload,
      };
      appendFileSync(STUDY_LOG, JSON.stringify(entry) + '\n');
      studyAppend++;
    }
    okCount++;
  }

  // 原子清理：rename 而非 unlink，避免处理中途被中断留下半截
  const archivePath = INBOX + '.processed-' + Date.now();
  renameSync(INBOX, archivePath);

  return {
    ok: true,
    processed: okCount,
    badLines: badCount,
    studyAppended: studyAppend,
    archivedTo: archivePath,
  };
}

function main() {
  const watch = process.argv.includes('--watch');
  if (watch) {
    console.log('[studio-receiver] watch mode, polling every 60s...');
    const tick = () => {
      const r = processInbox();
      if (r.processed > 0) console.log(JSON.stringify(r));
    };
    tick();
    setInterval(tick, 60000);
  } else {
    const r = processInbox();
    console.log(JSON.stringify(r, null, 2));
  }
}

main();
