/**
 * 仓库健康检查脚本
 * 在本地和 CI 中运行，检查仓库健康状况
 * 
 * 用法：
 *   node scripts/health-check.mjs              # 全量检查
 *   node scripts/health-check.mjs --quick       # 快速检查（仅 P0）
 *   node scripts/health-check.mjs --coverage    # 仅覆盖分析
 *   node scripts/health-check.mjs --json        # JSON 格式输出
 */

import { readFileSync, readdirSync, statSync, existsSync, writeFileSync } from 'fs';
import { join, relative } from 'path';
import { fileURLToPath } from 'url';

// 跨平台安全的仓库根目录解析（Windows/Unix 通用）
const ROOT = fileURLToPath(new URL('..', import.meta.url));
const args = process.argv.slice(2);
const isQuick = args.includes('--quick');
const isCoverage = args.includes('--coverage');
const isJson = args.includes('--json');

const results = {
  timestamp: new Date().toISOString(),
  checks: [],
  summary: { passed: 0, warning: 0, failed: 0 }
};

function logCheck(name, status, detail) {
  results.checks.push({ name, status, detail });
  results.summary[status]++;
  const icon = status === 'passed' ? '✅' : status === 'warning' ? '⚠️' : '❌';
  console.log(`${icon} [${status.toUpperCase()}] ${name}: ${detail}`);
}

// ============================================================
// P0: 文件结构检查
// ============================================================
function checkFileStructure() {
  const required = [
    'docs/.vitepress/config.mts',
    'docs/index.md',
    'package.json',
    'README.md',
  ];
  
  let allOk = true;
  for (const file of required) {
    if (!existsSync(join(ROOT, file))) {
      allOk = false;
      logCheck('文件结构', 'failed', `缺少必需文件: ${file}`);
    }
  }
  if (allOk) {
    logCheck('文件结构', 'passed', '所有必需文件存在');
  }
}

// ============================================================
// P0: 目录完整性检查
// ============================================================
function checkDirectoryIntegrity() {
  const requiredDirs = [
    'docs/posts/math/notes',
    'docs/posts/computer/notes',
    'docs/posts/english/notes',
    'docs/posts/politics/notes',
  ];
  
  let allOk = true;
  for (const dir of requiredDirs) {
    if (!existsSync(join(ROOT, dir))) {
      allOk = false;
      logCheck('目录完整性', 'failed', `缺少目录: ${dir}`);
    }
  }
  if (allOk) {
    logCheck('目录完整性', 'passed', '所有必需目录存在');
  }
}

// ============================================================
// P0: 断链检查（基础版）
// ============================================================
function checkBrokenLinks() {
  let brokenCount = 0;
  const brokenLinks = [];

  // 这些 [[...]] 是 Markdown 扩展指令，不是文件双链，需跳过
  const SKIP_WIKI = new Set(['toc', 'tableofcontents']);

  // 只检查 docs/ 目录下的 .md 文件
  const docsDir = join(ROOT, 'docs');
  if (!existsSync(docsDir)) {
    logCheck('断链检查', 'warning', 'docs/ 目录不存在，跳过');
    return;
  }
  
  function walkDir(dir) {
    const entries = readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = join(dir, entry.name);
      if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'node_modules' && entry.name !== 'dist') {
        walkDir(fullPath);
      } else if (entry.isFile() && entry.name.endsWith('.md')) {
        const content = readFileSync(fullPath, 'utf-8');
        // 检查 wiki 双链 [[...]]
        const wikiLinks = content.match(/\[\[([^\]]+)\]\]/g) || [];
        for (const link of wikiLinks) {
          // 去掉 [[ 和 ]]，去掉 |显示文字 和 #锚点；末尾 trim 是必需的 ——
          // 否则 `[[ ]]`（文档里举例说明双链语法时写的空链）会得到 ' '，
          // `!target` 判不出空，被当成文件名去查表从而误报断链（2026-09-17 修）
          const target = link.slice(2, -2).replace(/\|.+$/, '').split('#')[0].trim();
          if (!target) continue;
          // 跳过 Markdown 扩展指令，不是文件链接
          if (SKIP_WIKI.has(target.toLowerCase())) continue;
          // 尝试按 basename 匹配
          const found = findFileByBasename(target, docsDir);
          if (!found) {
            brokenCount++;
            brokenLinks.push(`${relative(ROOT, fullPath)} → [[${target}]]`);
          }
        }
      }
    }
  }
  
  function findFileByBasename(basename, searchDir) {
    // 精确匹配
    const exact = findFile(join(searchDir, `${basename}.md`));
    if (exact) return true;
    // 空格→连字符
    const hyphenated = basename.replace(/ /g, '-');
    const hyphenMatch = findFile(join(searchDir, `${hyphenated}.md`));
    if (hyphenMatch) return true;
    // 递归搜索
    const entries = readdirSync(searchDir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'node_modules') {
        if (findFileByBasename(basename, join(searchDir, entry.name))) return true;
      }
    }
    return false;
  }
  
  function findFile(path) {
    try {
      return statSync(path).isFile();
    } catch { return false; }
  }
  
  walkDir(docsDir);
  
  if (brokenCount === 0) {
    logCheck('断链检查', 'passed', '无断链');
  } else {
    logCheck('断链检查', 'warning', `发现 ${brokenCount} 处断链`);
    // 输出前 10 个
    brokenLinks.slice(0, 10).forEach(l => console.log(`   ${l}`));
    if (brokenLinks.length > 10) {
      console.log(`   ... 还有 ${brokenLinks.length - 10} 处`);
    }
  }
}

// ============================================================
// P1: 文件编码检查
// ============================================================
function checkEncoding() {
  let bomCount = 0;
  
  const docsDir = join(ROOT, 'docs');
  if (!existsSync(docsDir)) return;
  
  function walkDir(dir) {
    const entries = readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = join(dir, entry.name);
      if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'node_modules') {
        walkDir(fullPath);
      } else if (entry.isFile() && entry.name.endsWith('.md')) {
        const buf = readFileSync(fullPath);
        // 检查 UTF-8 BOM (EF BB BF)
        if (buf.length >= 3 && buf[0] === 0xEF && buf[1] === 0xBB && buf[2] === 0xBF) {
          bomCount++;
          console.log(`   BOM: ${relative(ROOT, fullPath)}`);
        }
      }
    }
  }
  
  walkDir(docsDir);
  
  if (bomCount === 0) {
    logCheck('编码检查', 'passed', '所有文件 UTF-8 无 BOM');
  } else {
    logCheck('编码检查', 'warning', `${bomCount} 个文件包含 BOM 头`);
  }
}

// ============================================================
// P1: Index 文件存在性检查
// ============================================================
function checkIndexFiles() {
  const contentDirs = [
    'docs/posts/math/notes',
    'docs/posts/computer/notes',
    'docs/posts/english/notes',
    'docs/posts/politics/notes',
    'docs/posts/math',
    'docs/posts/computer',
    'docs/posts/english',
    'docs/posts/politics',
    'docs/posts/computer/topics',
  ];
  
  let missingCount = 0;
  for (const dir of contentDirs) {
    const fullPath = join(ROOT, dir);
    if (existsSync(fullPath) && !existsSync(join(fullPath, 'index.md'))) {
      missingCount++;
      logCheck('索引文件', 'warning', `${dir}: 缺少 index.md`);
    }
  }
  
  if (missingCount === 0) {
    logCheck('索引文件', 'passed', '所有目录有 index.md');
  }
}

// ============================================================
// P2: 文件大小异常检查
// ============================================================
function checkFileSizes() {
  const minSize = 100; // 最少 100 字节
  let smallFiles = [];
  
  const docsDir = join(ROOT, 'docs/posts');
  if (!existsSync(docsDir)) return;
  
  function walkDir(dir) {
    const entries = readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = join(dir, entry.name);
      if (entry.isDirectory() && !entry.name.startsWith('.')) {
        walkDir(fullPath);
      } else if (entry.isFile() && entry.name.endsWith('.md') && entry.name !== 'index.md') {
        const size = statSync(fullPath).size;
        if (size < minSize) {
          smallFiles.push({ path: relative(ROOT, fullPath), size });
        }
      }
    }
  }
  
  walkDir(docsDir);
  
  if (smallFiles.length === 0) {
    logCheck('文件大小', 'passed', '所有笔记文件大小正常');
  } else {
    logCheck('文件大小', 'warning', `${smallFiles.length} 个文件过小 (< ${minSize} 字节)`);
    smallFiles.forEach(f => console.log(`   ${f.path} (${f.size} 字节)`));
  }
}

// ============================================================
// 执行
// ============================================================
console.log('\n🩺 仓库健康检查\n');
console.log(`时间: ${results.timestamp}`);
console.log(`模式: ${isQuick ? '快速' : isCoverage ? '覆盖分析' : '全量'}\n`);

checkFileStructure();
checkDirectoryIntegrity();

if (!isCoverage) {
  checkBrokenLinks();
  checkEncoding();
  checkIndexFiles();
  checkFileSizes();
}

// 输出摘要
console.log('\n' + '='.repeat(50));
console.log('📊 检查结果摘要');
console.log(`✅ 通过: ${results.summary.passed}`);
console.log(`⚠️  警告: ${results.summary.warning}`);
console.log(`❌ 失败: ${results.summary.failed}`);
console.log('='.repeat(50));

// JSON 输出
if (isJson) {
  const jsonPath = join(ROOT, 'knowledge/health-check-result.json');
  writeFileSync(jsonPath, JSON.stringify(results, null, 2));
  console.log(`\nJSON 结果已保存到: ${jsonPath}`);
}

// 退出码
if (results.summary.failed > 0) {
  process.exit(1);
}