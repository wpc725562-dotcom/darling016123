// ── 受控标签词表（2026-10-05 建立）────────────────────────────────────────
// 背景：全站原有 251 个标签、其中 202 个只出现 1 次 ⇒ 长尾对导航零贡献。
// 收敛为 4 个维度、共 40 个词；`check-tags.mjs` 会在白名单外**直接 exit 1**。
//
// 抄的是 mkdocs-material tags 插件的 `tags_allowed` 设计：
// 「若某页面引用了不在白名单内的标签，插件会停止构建」—— 硬失败，不是 warning。

export const VOCAB = {
  科目: ['高等数学', '计算机程序设计', '公共英语', '政治理论', '日语', '雅思'],
  类型: ['真题', '题库', '模拟卷', '学习手册', '章节笔记', '高频考点', '考点总析', '备考资料'],
  用途: ['零基础', '易错', '答题模板', '时政'],
}

// 年份轴单独一维（天然较宽，2005–2026 共 22 个）
export const YEARS = Array.from({ length: 22 }, (_, i) => String(2005 + i))

export const ALLOWED = new Set([
  ...Object.values(VOCAB).flat(),
  ...YEARS,
])

// ── 目录级打标（抄 mkdocs-material meta 插件的 `.meta.yml` 递归继承）──────
// 与其逐页手写，不如按路径前缀批量注入「科目」。**先匹配的规则优先**。
export const SUBJECT_RULES = [
  [/^posts\/math\//, '高等数学'],
  [/^posts\/computer\//, '计算机程序设计'],
  [/^posts\/english\//, '公共英语'],
  [/^posts\/politics\//, '政治理论'],
  [/^posts\/resources\//, null],            // 通用资料，不挂科目
  [/^posts\/题库\//, null],
  [/^posts\/模拟卷\//, null],
  [/^posts\/高频考点\//, null],
  [/^course\/japanese\//, '日语'],
  [/^learn\/standard-japanese\//, '日语'],
  [/^learn\/(zero-baseline|systematic-japanese-learning-guide|japanese-)/, '日语'],
  [/^learn\/bili-japanese/, '日语'],
  [/^learn\/ielts-/, '雅思'],
  [/^learn\/bili-ielts/, '雅思'],
]

// 文件名以年份开头 ⇒ 自动补年份标签（如 `2024-英语-刷题版.md`）
export const YEAR_RE = /^((?:19|20)\d\d)[-_]/

// ── 按路径注入「类型」────────────────────────────────────────────────────
// 只对**目录语义明确**的区块打，不猜。先匹配的规则优先。
export const TYPE_RULES = [
  [/^posts\/题库\//, '题库'],
  [/^posts\/模拟卷\//, '模拟卷'],
  [/\/模拟卷\//, '模拟卷'],
  [/^posts\/高频考点\//, '高频考点'],
  [/^posts\/resources\//, '备考资料'],
  [/^posts\/真题索引/, '真题'],
  [/^posts\/\w+\/(?:19|20)\d\d[-_]/, '真题'],   // 各科 `2024-xxx` 真题页
  [/^posts\/\w+\/学习手册/, '学习手册'],
]
