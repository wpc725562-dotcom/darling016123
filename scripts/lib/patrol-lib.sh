#!/usr/bin/env bash
# ============================================================================
# 巡逻共用函数库
# ----------------------------------------------------------------------------
# 为什么要有这个文件：
#   这些函数原本内联在 .github/workflows/auto-patrol.yml 的 run: 块里，
#   而 scripts/test-patrol-logic.sh 为了测试它们只能**抄一份副本**。
#   副本会漂移 —— 改了工作流里的实现，测试仍对着旧副本跑并报「通过」，
#   属于典型的「假信心测试」：测试通过不代表被测代码正确。
#
#   所以把实现抽到这里，工作流与测试**同源 source**，测试才真正有意义。
#
# 使用方式（工作流里）：
#   source scripts/lib/patrol-lib.sh
#   math_expected="$(read_expect "$EXPECT_FILE" math 36)"
#   actual="$(count_md docs/posts/math/notes/ ! -name 'index.md')"
#   pct="$(pct_of "$actual" "$math_expected")"
#
# 注意：本库只定义函数，不在 source 时执行任何动作。
# ============================================================================

# count_md <dir> [额外的 find 参数...]
#   统计目录下 .md 文件数。
#   目录不存在时返回字面量 MISSING —— 绝不能返回 0：
#   `find <不存在的目录> ... | wc -l` 会打印 0，而 find 的报错被管道吞掉，
#   于是「目录缺失」被静默伪装成「一个文件都没有」，检查彻底失效。
count_md() {
  local d="$1"; shift
  if [[ ! -d "$d" ]]; then echo "MISSING"; return 0; fi
  find "$d" -name "*.md" "$@" 2>/dev/null | wc -l | tr -d ' '
}

# pct_of <actual> <expected>
#   计算百分比。超出 100% 时显式标注「超预期」而不是输出荒谬数字：
#   期望值一旦过期（例如实际 70 篇而期望写 36），194% 这种数字没人会当真，
#   数字失真等于检查不存在。分母 <= 0 或 actual 缺失时返回 N/A。
pct_of() {
  local actual="$1" expected="$2"
  if [[ "$expected" == "MISSING" || -z "$expected" || "$expected" -le 0 ]]; then
    echo "N/A"; return 0
  fi
  if [[ "$actual" == "MISSING" || -z "$actual" ]]; then echo "N/A"; return 0; fi
  local p=$(( actual * 100 / expected ))
  if [[ $p -gt 100 ]]; then echo "${p}% ⚠️超预期"; else echo "${p}%"; fi
}

# cell <value>  把 MISSING 渲染成可读告警，其余原样返回
cell() {
  if [[ "$1" == "MISSING" ]]; then echo "⚠️ 目录缺失"; else echo "$1"; fi
}

# read_expect <config_file> <key> <default>
#   从 JSON 配置读期望值，三级回退：jq → node → default。
#   为什么不能只用 jq：开发机（Windows Git Bash）常常没有 jq。
#   为什么不能用 node 之外还有 default：node 是 workflow 必然存在的
#   （setup-node + npm ci），但本库也可能被别处 source，所以要能兜底。
#   注意 default 必须是**当前有效**的值 —— 若兜底值是过期常量，
#   读不到配置时又会退回荒谬百分比，等于把 bug 藏起来。
read_expect() {
  local file="$1" key="$2" default="$3" v=""
  if [[ -f "$file" ]]; then
    if command -v jq >/dev/null 2>&1; then
      v="$(jq -r --arg k "$key" '.[$k] // empty' "$file" 2>/dev/null || true)"
    fi
    if [[ -z "$v" || "$v" == "null" ]] && command -v node >/dev/null 2>&1; then
      v="$(node -e "try{const c=JSON.parse(require('fs').readFileSync('$file','utf8'));process.stdout.write(c['$key']!=null?String(c['$key']):'')}catch(e){}" 2>/dev/null || true)"
    fi
  fi
  if [[ -n "$v" && "$v" != "null" ]]; then echo "$v"; else echo "$default"; fi
}

# rotate_reports <keep> <glob-prefix>
#   报告轮转：按文件名排序，只保留最新 N 份，返回将被删除的路径列表（每行一个）。
#   只**计算**不删除，便于调用方打印日志、也便于测试干跑。
#   每天新增一份 patrol-report-YYYYMMDD.md 而从不清理，一年就是 365 份噪声。
rotate_reports() {
  local keep="$1" prefix="$2"
  local -a all
  mapfile -t all < <(ls -1 ${prefix}* 2>/dev/null | sort)
  local total=${#all[@]}
  if [[ $total -le $keep ]]; then return 0; fi
  local remove=$((total - keep))
  local i
  for ((i = 0; i < remove; i++)); do
    echo "${all[$i]}"
  done
}
