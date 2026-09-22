#!/usr/bin/env bash
# ============================================================================
# 巡逻工作流回归测试
# ----------------------------------------------------------------------------
# 为什么需要这个文件：
#   .github/workflows/auto-patrol.yml 里内联了大量 bash。2026-09-17 发现该脚本
#   用 `((VAR++))` 计数，在 GitHub Actions 默认的 `bash -e` 下，变量从 0 变 1 时
#   该表达式返回退出码 1 → 整个 step 静默中断 → 报告只留第一条记录；
#   又因为每个 step 都带 `continue-on-error: true`，失败被完全吞掉，
#   workflow 显示「通过」。这个 bug 潜伏多日无人发现，根本原因就是**没有测试**。
#
# 关键设计：函数实现从 scripts/lib/patrol-lib.sh **同源 source**，不抄副本。
#   抄副本的测试会漂移 —— 工作流里的实现改了，测试仍对着旧副本报「通过」，
#   那是假信心，比没有测试更危险。
#
# 用法：bash scripts/test-patrol-logic.sh
# ============================================================================
set -euo pipefail

cd "$(dirname "$0")/.."

WF_FILE=".github/workflows/auto-patrol.yml"
LIB_FILE="scripts/lib/patrol-lib.sh"
EXPECT_FILE="scripts/coverage-expectations.json"
TMPDIR_T=".tmp-patrol-test"

FAILED=0
pass() { echo "  ✅ $1"; }
fail() { echo "  ❌ $1"; FAILED=$((FAILED + 1)); }
check_eq() { # <actual> <expected> <label>
  if [[ "$1" == "$2" ]]; then pass "$3"; else fail "$3 —— 实际 '$1'，期望 '$2'"; fi
}

mkdir -p "$TMPDIR_T"

# 同源加载被测实现
# shellcheck source=scripts/lib/patrol-lib.sh
source "$LIB_FILE"

echo "===== 1. count_md：目录计数与缺失告警 ====="
m="$(count_md docs/posts/math/notes/ ! -name 'index.md' ! -name 'syllabus.md')"
c="$(count_md docs/posts/computer/notes/ ! -name 'index.md' ! -name 'syllabus.md')"
p="$(count_md docs/posts/politics/notes/ ! -name 'index.md')"
e="$(count_md docs/posts/english/notes/ ! -name 'index.md')"
echo "  math=$m cs=$c po=$p en=$e"
[[ "$m" =~ ^[0-9]+$ ]] && pass "math 返回数字" || fail "math 未返回数字: '$m'"
check_eq "$(count_md docs/posts/nonexistent-dir/)" "MISSING" "缺失目录返回 MISSING（而非静默 0）"
# 目录缺失时绝不能返回 0 —— 那会把「目录没了」伪装成「一个文件都没有」
[[ "$(count_md docs/posts/nonexistent-dir/)" != "0" ]] \
  && pass "缺失目录未伪装成 0" || fail "缺失目录被伪装成 0"

echo ""
echo "===== 2. pct_of：百分比与超预期告警 ====="
check_eq "$(pct_of 70 70)" "100%" "70/70 = 100%"
check_eq "$(pct_of 40 20)" "200% ⚠️超预期" "40/20 标注超预期（不输出裸 200%）"
check_eq "$(pct_of 0 36)" "0%" "0/36 = 0%"
check_eq "$(pct_of 100 0)" "N/A" "分母为 0 → N/A"
check_eq "$(pct_of MISSING 36)" "N/A" "实际缺失 → N/A"
check_eq "$(pct_of 70 MISSING)" "N/A" "期望缺失 → N/A"

echo ""
echo "===== 3. cell：MISSING 渲染 ====="
check_eq "$(cell MISSING)" "⚠️ 目录缺失" "MISSING 渲染为告警"
check_eq "$(cell 42)" "42" "正常值原样返回"

echo ""
echo "===== 4. read_expect：三级回退（jq → node → default） ====="
echo "  jq 可用? $(command -v jq >/dev/null 2>&1 && echo yes || echo no)    node 可用? $(command -v node >/dev/null 2>&1 && echo yes || echo no)"
check_eq "$(read_expect "$EXPECT_FILE" math 70)" "70" "读取 math"
check_eq "$(read_expect "$EXPECT_FILE" cs 51)" "51" "读取 cs"
check_eq "$(read_expect "$EXPECT_FILE" po 20)" "20" "读取 po"
check_eq "$(read_expect "$EXPECT_FILE" notakey 999)" "999" "键不存在 → default"
check_eq "$(read_expect scripts/__nope__.json math 70)" "70" "文件不存在 → default"

echo ""
echo "===== 5. 配置与实测一致性（防漂移） ====="
if [[ -f "$EXPECT_FILE" ]] && command -v node >/dev/null 2>&1; then
  node -e "JSON.parse(require('fs').readFileSync('$EXPECT_FILE','utf8'))" 2>/dev/null \
    && pass "coverage-expectations.json 是合法 JSON" || fail "JSON 解析失败"
  # 配置值必须与实测文件数一致，否则报告又会输出荒谬百分比
  check_eq "$(read_expect "$EXPECT_FILE" math 0)" "$m" "配置 math 期望值 == 实测文件数"
  check_eq "$(read_expect "$EXPECT_FILE" cs 0)" "$c" "配置 cs 期望值 == 实测文件数"
  check_eq "$(read_expect "$EXPECT_FILE" po 0)" "$p" "配置 po 期望值 == 实测文件数"
fi

echo ""
echo "===== 6. rotate_reports：轮转只算不删 ====="
# 对真实仓库干跑：待删数应恒等于 max(0, 实际份数 - 30)，且不得真的删掉东西
real_reports="$(ls -1 knowledge/patrol-report-*.md 2>/dev/null | wc -l | tr -d ' ')"
real_expected=$(( real_reports > 30 ? real_reports - 30 : 0 ))
check_eq "$(rotate_reports 30 knowledge/patrol-report- | wc -l | tr -d ' ')" \
  "$real_expected" "真实仓库 $real_reports 份 → 待删 $real_expected 份"
check_eq "$(ls -1 knowledge/patrol-report-*.md 2>/dev/null | wc -l | tr -d ' ')" \
  "$real_reports" "干跑未删除任何真实报告"
mkdir -p "$TMPDIR_T/rot"
for i in $(seq -w 1 35); do : > "$TMPDIR_T/rot/report-$i.md"; done
check_eq "$(rotate_reports 30 "$TMPDIR_T/rot/report-" | wc -l | tr -d ' ')" "5" "构造 35 份、保留 30 → 待删 5 份"
check_eq "$(rotate_reports 30 "$TMPDIR_T/rot/report-" | head -1)" "$TMPDIR_T/rot/report-01.md" "先删最旧的"
check_eq "$(rotate_reports 40 "$TMPDIR_T/rot/report-" | wc -l | tr -d ' ')" "0" "未超上限 → 待删 0"
check_eq "$(ls -1 "$TMPDIR_T/rot/" | wc -l | tr -d ' ')" "35" "干跑未实际删除文件"

echo ""
echo "===== 7. CHECKED 行数统计（综合报告） ====="
TMP="$TMPDIR_T/report.md"
{
  echo "# 🚨 自动巡逻报告"
  echo ""
  echo "## ✅ 检查结果"
  echo ""
  echo "| 检查项 | 状态 | 详情 |"
  echo "|:---|:---:|:---|"
  echo "| 🧪 巡逻脚本自检 | ✅ 通过 | 功能测试 + 防回归扫描全部通过 |"
  echo "| 🔨 站点构建 | ✅ 通过 | 构建成功 |"
  echo "| 🔗 链接检查 | ✅ 通过 | 无断链 |"
  echo "| 📋 质量体检 | ✅ 通过 | 无问题 |"
  echo "| 📑 索引一致性 | ✅ 通过 | 全部一致 |"
  echo "| 📊 覆盖率分析 | ℹ️ 参考 | 见 coverage-report-auto.md |"
} > "$TMP"
CHECKED_ROWS="$(grep -c '^| ' "$TMP" || true)"
CHECKED=$(( ${CHECKED_ROWS:-0} - 1 ))
[[ $CHECKED -lt 0 ]] && CHECKED=0
check_eq "$CHECKED" "6" "6 行正文（表头不计、分隔行不匹配）"
TMP2="$TMPDIR_T/empty.md"
echo "# 空报告" > "$TMP2"
R="$(grep -c '^| ' "$TMP2" || true)"
C=$(( ${R:-0} - 1 )); [[ $C -lt 0 ]] && C=0
check_eq "$C" "0" "空报告 → 0（不为负）"

echo ""
echo "===== 8. 禁用模式扫描（防回归） ====="
# 8a. ((VAR++)) —— 见文件头说明，这是导致巡逻静默中断的元凶
#     必须排除注释行：workflow 里有大段解释该 bug 的注释含此字面量
VAR_INC_HITS="$(grep -nE '\(\([A-Za-z_][A-Za-z0-9_]*(\+\+|--)\)\)' "$WF_FILE" \
  | grep -vE '^[0-9]+:[[:space:]]*#' || true)"
if [[ -n "$VAR_INC_HITS" ]]; then
  fail "发现 ((VAR++)) / ((VAR--))，bash -e 下会静默中断 step"
  echo "$VAR_INC_HITS"
else
  pass "无 ((VAR++)) / ((VAR--)) 用法（已排除注释）"
fi

# 8b. 覆盖率脚本不得写人工复核版报告
if grep -q 'REPORT_FILE="knowledge/coverage-report.md"' "$WF_FILE"; then
  fail "覆盖率 REPORT_FILE 仍指向人工复核版 coverage-report.md"
else
  pass "覆盖率报告写入 *-auto.md，人工版未被覆写"
fi
if grep -n 'git add' "$WF_FILE" | grep -q 'knowledge/coverage-report\.md'; then
  fail "git add 中包含人工复核版 coverage-report.md"
else
  pass "自动提交未包含人工复核版 coverage-report.md"
fi

# 8c. 关键逻辑必须存在
grep -q 'KEEP=30' "$WF_FILE" && pass "存在报告轮转" || fail "缺少报告轮转逻辑"
grep -q 'issues.listForRepo' "$WF_FILE" && pass "存在 Issue 去重" || fail "缺少 Issue 去重逻辑"
grep -q 'git rebase --abort' "$WF_FILE" && pass "存在 rebase 冲突回滚" || fail "缺少 git rebase --abort"
grep -q 'source scripts/lib/patrol-lib.sh' "$WF_FILE" \
  && pass "工作流引用共用库（未内联副本）" || fail "工作流未 source 共用库"

# 8c+. 改了共用库必须能触发巡逻，否则自检永远跑不到新实现
grep -q "scripts/lib/\*\*" "$WF_FILE" \
  && pass "触发路径含 scripts/lib/**" || fail "触发路径缺 scripts/lib/**（改库不触发自检）"

# 8c++. 三套链接检查器的 [[toc]] 跳过集合必须一致
#   仓库里存在三套独立的 wiki 双链检查器（health-check.mjs / check-links.mjs /
#   workflow 内联 bash），它们各自维护一份 SKIP_WIKI。2026-09-17 就是因为只修了
#   前两套、漏了第三套，导致 [[toc]] 误报持续存在。这条扫描守住一致性。
extract_skip() {
  grep -oE "[\"'](toc|tableofcontents)[\"']" "$1" 2>/dev/null | tr -d "\"'" | sort -u | tr '\n' ','
}
hc_skip="$(extract_skip scripts/health-check.mjs)"
cl_skip="$(extract_skip scripts/check-links.mjs)"
wf_skip="$(extract_skip "$WF_FILE")"
echo "  health-check.mjs: $hc_skip"
echo "  check-links.mjs:  $cl_skip"
echo "  workflow 内联:     $wf_skip"
if [[ -n "$hc_skip" && "$hc_skip" == "$cl_skip" && "$cl_skip" == "$wf_skip" ]]; then
  pass "三套链接检查器 SKIP_WIKI 一致"
else
  fail "三套链接检查器 SKIP_WIKI 不一致（漏改某一套会导致误报）"
fi

# 8c+++. 三套链接检查器都必须「先剥行内代码，再抽双链」（2026-09-23 加）
#   与 8c++ 完全同构的失效模式，只是换了个维度：SKIP_WIKI 守住了「跳过扩展指令」，
#   但没人守「跳过反引号里的示例」。实测 workflow 内联那套没剥，
#   于是 `docs/posts/computer/notes/*.md` 里那句「只统计带标签 `[[1.1 …]]` 的题」
#   被当成真链接，10 篇笔记各报 1 处，加 1 处 `[[...]]` 语法示例共 20 处假阳性 ——
#   断链检查因此长期停在 ⚠️，真出问题时反而看不出来。
#   这里只断言「剥代码这段存在」，不比对具体写法（mjs 用 replace 正则，
#   bash 用 sed，形式本来就不同，强行比对会变成脆弱测试）。
extract_strip() {
  if grep -qF '.replace(/`[^`\n]*`/g' "$1" 2>/dev/null; then echo "replace"
  elif grep -qF 's/`[^`]*`//g' "$1" 2>/dev/null; then echo "sed"
  else echo "none"; fi
}
hc_strip="$(extract_strip scripts/health-check.mjs)"
cl_strip="$(extract_strip scripts/check-links.mjs)"
wf_strip="$(extract_strip "$WF_FILE")"
echo "  health-check.mjs 剥行内代码: $hc_strip"
echo "  check-links.mjs  剥行内代码: $cl_strip"
echo "  workflow 内联    剥行内代码: $wf_strip"
if [[ "$hc_strip" != "none" && "$cl_strip" != "none" && "$wf_strip" != "none" ]]; then
  pass "三套链接检查器都剥离了行内代码"
else
  fail "有检查器未剥离行内代码（会把反引号里的示例当成真链接，稳定误报）"
fi

# 8d. 工作流内不得再内联这些函数定义（否则又与库漂移）
for fn in count_md pct_of read_expect rotate_reports; do
  if grep -qE "^[[:space:]]*${fn}\(\)[[:space:]]*\{" "$WF_FILE"; then
    fail "工作流内联了 ${fn}()，会与 $LIB_FILE 漂移"
  else
    pass "工作流未内联 ${fn}()"
  fi
done

echo ""
echo "===== 清理 ====="
# 清理必须**容忍失败**：本机沙箱会拦截批量删除（35 个文件即触发
# safe-delete 保护），若无条件 `rm -rf` + set -e，测试会因清理失败而
# 报错退出 —— 明明是全部通过却返回退出码 1，比不清理更糟。
# CI 上（Linux）能正常删除；本机删不掉时只提示，不影响测试结论。
if rm -rf "$TMPDIR_T" 2>/dev/null; then
  echo "  已清理 $TMPDIR_T"
else
  echo "  ⚠️ 无法清理 $TMPDIR_T（本机沙箱拦截批量删除），已忽略"
  echo "     该目录已在 .gitignore 中，不会污染仓库"
fi

echo ""
if [[ $FAILED -eq 0 ]]; then
  echo "✅ 全部测试通过"
  exit 0
else
  echo "❌ 有 $FAILED 项失败"
  exit 1
fi
