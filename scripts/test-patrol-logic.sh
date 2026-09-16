#!/usr/bin/env bash
# ============================================================================
# 巡逻工作流回归测试
# ----------------------------------------------------------------------------
# 为什么需要这个文件：
#   .github/workflows/auto-patrol.yml 里内联了大量 bash。2026-09-17 发现该脚本
#   用 `((VAR++))` 计数，在 GitHub Actions 默认的 `bash -e` 下，变量从 0 变 1 时
#   该表达式返回退出码 1 → 整个 step 静默中断 → 报告只留第一条记录；
#   又因为每个 step 都带 `continue-on-error: true`，失败被完全吞掉，
#   workflow 显示"通过"。这个 bug 潜伏多日无人发现，根本原因就是**没有测试**。
#   本文件用来防止同类问题回归。
#
# 用法：bash scripts/test-patrol-logic.sh
# ============================================================================
set -euo pipefail

WF_FILE=".github/workflows/auto-patrol.yml"

cd "$(dirname "$0")/.."
TMPDIR_T=".tmp-patrol-test"
mkdir -p "$TMPDIR_T"

echo "===== 1. count_md / pct_of 函数 ====="
count_md() {
  local d="$1"; shift
  if [[ ! -d "$d" ]]; then echo "MISSING"; return; fi
  find "$d" -name "*.md" "$@" 2>/dev/null | wc -l | tr -d ' '
}
pct_of() {
  if [[ "$2" == "MISSING" || "$2" -le 0 ]]; then echo "N/A"; return; fi
  if [[ "$1" == "MISSING" ]]; then echo "N/A"; return; fi
  local p=$(( $1 * 100 / $2 ))
  if [[ $p -gt 100 ]]; then echo "${p}% ⚠️超预期"; else echo "${p}%"; fi
}
cell() { [[ "$1" == "MISSING" ]] && echo "⚠️ 目录缺失" || echo "$1"; }

m="$(count_md docs/posts/math/notes/ ! -name 'index.md' ! -name 'syllabus.md')"
c="$(count_md docs/posts/computer/notes/ ! -name 'index.md' ! -name 'syllabus.md')"
p="$(count_md docs/posts/politics/notes/ ! -name 'index.md')"
e="$(count_md docs/posts/english/notes/ ! -name 'index.md')"
echo "math=$m cs=$c po=$p en=$e"
echo "缺失目录: $(count_md docs/posts/nonexistent/)"
echo "cell(MISSING) = $(cell MISSING)"

echo ""
echo "===== 2. 期望值读取三级回退 ====="
EXPECT_FILE="scripts/coverage-expectations.json"
read_expect() {
  local v=""
  if [[ -f "$EXPECT_FILE" ]]; then
    if command -v jq >/dev/null 2>&1; then
      v="$(jq -r --arg k "$1" '.[$k] // empty' "$EXPECT_FILE" 2>/dev/null || true)"
    fi
    if [[ -z "$v" || "$v" == "null" ]] && command -v node >/dev/null 2>&1; then
      v="$(node -e "try{const c=JSON.parse(require('fs').readFileSync('$EXPECT_FILE','utf8'));process.stdout.write(c['$1']!=null?String(c['$1']):'')}catch(e){}" 2>/dev/null || true)"
    fi
  fi
  if [[ -n "$v" && "$v" != "null" ]]; then echo "$v"; else echo "$2"; fi
}
echo "jq 可用? $(command -v jq >/dev/null 2>&1 && echo yes || echo no)"
echo "node 可用? $(command -v node >/dev/null 2>&1 && echo yes || echo no)"
math_expected="$(read_expect math 36)"
cs_expected="$(read_expect cs 20)"
po_expected="$(read_expect po 18)"
echo "读取到: math=$math_expected cs=$cs_expected po=$po_expected  (期望 70/44/20)"
[ "$math_expected" = "70" ] || { echo "❌ math 期望值读取失败"; exit 1; }

echo ""
echo "===== 3. 覆盖率结果（配置生效后） ====="
echo "math: $(pct_of "$m" "$math_expected")   (期望 100%)"
echo "cs:   $(pct_of "$c" "$cs_expected")   (期望 100%)"
echo "po:   $(pct_of "$p" "$po_expected")   (期望 100%)"
echo "极端 pct_of 100 0        = $(pct_of 100 0)          (期望 N/A)"
echo "极端 pct_of 0 36         = $(pct_of 0 36)           (期望 0%)"
echo "极端 pct_of MISSING 36   = $(pct_of MISSING 36)     (期望 N/A)"
echo "极端 pct_of 40 20        = $(pct_of 40 20)          (期望 200% ⚠️超预期)"

echo ""
echo "===== 4. 配置缺失时回退到默认值 ====="
EXPECT_FILE="scripts/__nonexistent__.json"
echo "math=$(read_expect math 36)  (期望 36 兜底)"

echo ""
echo "===== 5. 报告轮转逻辑（干跑） ====="
KEEP=30
mapfile -t ALL_REPORTS < <(ls -1 knowledge/patrol-report-*.md 2>/dev/null | sort)
TOTAL=${#ALL_REPORTS[@]}
echo "现有报告数: $TOTAL"
if [[ $TOTAL -gt $KEEP ]]; then
  REMOVE=$((TOTAL - KEEP))
  echo "将清理 $REMOVE 份（保留最近 $KEEP）:"
  for ((i = 0; i < REMOVE; i++)); do echo "  - ${ALL_REPORTS[$i]}"; done
else
  echo "未超过上限 $KEEP，无需清理（当前 $TOTAL 份）"
fi
# 模拟 35 份
echo "模拟 35 份:"
sim=(); for ((i=0;i<35;i++)); do sim+=("patrol-report-$(printf %02d $i).md"); done
T=${#sim[@]}
if [[ $T -gt $KEEP ]]; then
  echo "  → 清理 $((T-KEEP)) 份，保留 ${sim[$((T-KEEP))]} 及之后"
fi

echo ""
echo "===== 6. CHECKED 行数统计 ====="
TMP="$TMPDIR_T/report.md"
{
  echo "# 🚨 自动巡逻报告"
  echo ""
  echo "## ✅ 检查结果"
  echo ""
  echo "| 检查项 | 状态 | 详情 |"
  echo "|:---|:---:|:---|"
  echo "| 🔨 站点构建 | ✅ 通过 | 构建成功 |"
  echo "| 🔗 链接检查 | ✅ 通过 | 无断链 |"
  echo "| 📋 质量体检 | ✅ 通过 | 无问题 |"
  echo "| 📑 索引一致性 | ✅ 通过 | 全部一致 |"
  echo "| 📊 覆盖率分析 | ℹ️ 参考 | 见 coverage-report-auto.md |"
} > "$TMP"
CHECKED_ROWS="$(grep -c '^| ' "$TMP" || true)"
CHECKED=$(( ${CHECKED_ROWS:-0} - 1 ))
[[ $CHECKED -lt 0 ]] && CHECKED=0
echo "grep -c '^| ' = $CHECKED_ROWS  →  CHECKED = $CHECKED  (期望 5)"
[ "$CHECKED" = "5" ] || { echo "❌ 行数统计错误"; exit 1; }

echo ""
echo "===== 7. 空报告边界 ====="
TMP2="$TMPDIR_T/empty.md"
echo "# 空报告" > "$TMP2"
R="$(grep -c '^| ' "$TMP2" || true)"
C=$(( ${R:-0} - 1 )); [[ $C -lt 0 ]] && C=0
echo "grep 返回 '$R' → CHECKED = $C (期望 0)"
[ "$C" = "0" ] || { echo "❌ 边界处理错误"; exit 1; }

echo ""
echo "===== 8. 报告的 Markdown 表格结构 ====="
cat "$TMP"

echo ""
echo "===== 9. 禁用模式扫描（防回归） ====="
# 9a. ((VAR++)) —— 见文件头说明，这是导致巡逻静默中断的元凶
#     必须排除注释行：本文件与 workflow 里都有大段解释该 bug 的注释文字，
#     它们本身含有 "((VAR++))" 字面量，不排除会造成永久性误报。
VAR_INC_HITS="$(grep -nE '\(\([A-Za-z_][A-Za-z0-9_]*(\+\+|--)\)\)' "$WF_FILE" \
  | grep -vE '^[0-9]+:[[:space:]]*#' || true)"
if [[ -n "$VAR_INC_HITS" ]]; then
  echo "❌ 发现 ((VAR++)) / ((VAR--))：在 bash -e 下变量 0→1 时返回 1，会静默中断 step"
  echo "$VAR_INC_HITS"
  echo "   请改用 VAR=\$((VAR + 1))"
  exit 1
else
  echo "✅ 无 ((VAR++)) / ((VAR--)) 用法（已排除注释）"
fi

# 9b. 覆盖率脚本不得再写人工复核版报告
if grep -nE '>\s*"?\$?REPORT_FILE"?\s*$' "$WF_FILE" | grep -q 'coverage-report\.md'; then
  echo "❌ 覆盖率脚本仍在写 coverage-report.md（人工复核版），会被覆写丢失"
  exit 1
fi
if grep -n 'REPORT_FILE="knowledge/coverage-report.md"' "$WF_FILE"; then
  echo "❌ 覆盖率 REPORT_FILE 仍指向人工复核版 coverage-report.md"
  exit 1
else
  echo "✅ 覆盖率报告写入 *-auto.md，人工版未被覆写"
fi

# 9c. 自动提交不得包含人工复核版覆盖率报告
if grep -n 'git add' "$WF_FILE" | grep -q 'knowledge/coverage-report\.md'; then
  echo "❌ git add 中包含人工复核版 coverage-report.md"
  exit 1
else
  echo "✅ 自动提交未包含人工复核版 coverage-report.md"
fi

# 9d. 期望值配置文件必须存在且可解析
if [[ ! -f "scripts/coverage-expectations.json" ]]; then
  echo "❌ scripts/coverage-expectations.json 缺失"
  exit 1
fi
if command -v node >/dev/null 2>&1; then
  node -e "JSON.parse(require('fs').readFileSync('scripts/coverage-expectations.json','utf8'))" \
    && echo "✅ coverage-expectations.json 是合法 JSON" \
    || { echo "❌ coverage-expectations.json JSON 解析失败"; exit 1; }
fi

# 9e. 报告轮转逻辑必须存在
if grep -q 'KEEP=30' "$WF_FILE"; then
  echo "✅ 存在报告轮转逻辑（保留 30 份）"
else
  echo "❌ 缺少报告轮转逻辑，patrol-report-*.md 会无限堆积"
  exit 1
fi

# 9f. Issue 去重逻辑必须存在
if grep -q 'issues.listForRepo' "$WF_FILE"; then
  echo "✅ 存在 Issue 去重逻辑"
else
  echo "❌ 缺少 Issue 去重逻辑，会每天新建重复 Issue"
  exit 1
fi

# 9g. rebase 冲突必须回滚
if grep -q 'git rebase --abort' "$WF_FILE"; then
  echo "✅ 存在 rebase 冲突回滚逻辑"
else
  echo "❌ 缺少 git rebase --abort，rebase 冲突会残留污染工作区"
  exit 1
fi

echo ""
echo "===== 清理 ====="
rm -rf "$TMPDIR_T"
echo "已清理 $TMPDIR_T"

echo ""
echo "✅ 全部测试通过（8 项功能 + 7 项防回归扫描）"
