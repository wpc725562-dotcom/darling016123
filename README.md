<p align="center">
  <img src="https://img.shields.io/badge/广东专升本-计算机类-blue?style=for-the-badge&logo=github" alt="Badge">
  <img src="https://img.shields.io/badge/适用-2027届-brightgreen?style=for-the-badge" alt="Year">
  <img src="https://img.shields.io/badge/状态-备考中-yellow?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/笔记-219篇-orange?style=for-the-badge" alt="Notes">
  <img src="https://img.shields.io/badge/真题-77个年份页-red?style=for-the-badge" alt="Exams">
  <img src="https://img.shields.io/github/actions/workflow/status/wpc725562-dotcom/darling016123/deploy.yml?style=for-the-badge&label=Deploy" alt="Deploy">
  <img src="https://img.shields.io/github/stars/wpc725562-dotcom/darling016123?style=for-the-badge&label=Stars" alt="Stars">
</p>

<h1 align="center">📚 广东专升本 · 四科复习笔记库</h1>

<p align="center">
  <strong>VitePress 知识库 · 213 篇实质笔记 · 77 个真题年份页 · 11 套模拟卷</strong><br>
  🎯 目标：公办本科 · 计算机类 · 2027 年 3 月考试
</p>

<p align="center">
  <a href="#-仓库结构">📁 仓库结构</a> •
  <a href="#-学习路线">📖 学习路线</a> •
  <a href="#-笔记使用说明">📝 笔记使用说明</a> •
  <a href="#-在线访问">🌐 在线访问</a>
</p>

---

## 🎯 项目简介

本仓库是**广东普通专升本（专插本）四科全科复习知识库**，覆盖：

| 科目 | 分值 | 笔记 | 真题年份页 | 模拟卷 |
|:---|:---:|:---:|:---:|:---:|
| **政治理论**（公共课） | 100 | 29 篇 | 2012–2026（15 页） | 3 套 |
| **公共英语**（公共课） | 100 | 42 篇 | 2005–2025（39 页） | 2 套 |
| **高等数学**（专业基础课） | 100 | 82 篇 | 2003–2026（10 页，含 2025 OCR 版） | 3 套 |
| **计算机基础与程序设计**（专业综合课） | **200** | 66 篇 | 2018–2027（14 页） | 3 套 |
| | | | | |
| **合计** | **500** | **219 篇** | **77 页** | **11 套** |

> 计算机 66 篇中，含 **6 篇分章专项题库**（按实测考频权重排序）+ 1 篇题库索引。

> **统计口径**（2026-09-17 重算，此前四科数字全部失真，曾导致外部评估误判为"模拟卷缺失"）：
> - 笔记 = `docs/posts/<科>/**/*.md`，排除 `index.md`、模拟卷目录、答案页、正文 < 800 字符的占位页
> - 真题年份页 = `历年真题/<科>/*.md`，排除 `_索引`、`00-` 前缀说明页
> - 模拟卷 = `docs/posts/<科>/模拟卷/卷*.md`（不含配套 `-答案.md`）；高数/计算机各 3 套 20/45 题、政治 3 套 35–37 题、英语 2 套 31/32 题
> - 重算命令：`python scripts/repo_stats.py`
>
> 站点同时是 **Obsidian 双链笔记库**（顶层 `历年真题/`、`政治理论/`、`高等数学/` 等为 Obsidian 导航区）+ **VitePress 站点源**（`docs/posts/`）。

---

## 📁 仓库结构

```
darling016123/
├── docs/                          # 📖 VitePress 站点源（在线发布）
│   ├── posts/
│   │   ├── math/notes/            #   高等数学系统笔记（82 篇）
│   │   ├── computer/notes/        #   计算机基础与程序设计笔记（59 篇）
│   │   ├── computer/专项题库/      #   ✍️ 计算机分章专项题库（6 篇 + 索引）
│   │   ├── politics/notes/        #   政治理论系统笔记（29 篇）
│   │   ├── english/notes/         #   英语笔记（42 篇）
│   │   ├── math|computer|politics|english/   # 各科真题年份页
│   │   ├── 高频考点/              #   高频考点 TOP20
│   │   └── resources/             #   学习资源库
│   ├── guide/                     #   报考指南（考纲/院校/分数线/考频矩阵）
│   │   └── 真题考频矩阵.md         #   📊 2023+2024 两年 90 题逐题实测分值
│   └── public/
│       ├── figs|papers|covers/    #   站点静态资源
│       └── downloads/
│           └── anki-computer.txt  #   🃏 172 张 Anki 卡片（19 分类）
├── 历年真题/                      # 🔗 Obsidian 真题区（双链导航）
│   └── 计算机程序设计/专项题库/    #   ✍️ 专项题库 Obsidian 侧源文件
├── 政治理论/ 高等数学/ 编程技能/   # 🔗 Obsidian 笔记区
├── 资料/ 备考计划/                # 🔗 Obsidian 资料区
├── bencetong/                     # 🖥️ 本科通 Electron 刷题应用
├── knowledge/                     # 📋 知识库辅助（audit 审计报告 / 考点速查）
├── scripts/
│   ├── repo_stats.py              #   笔记数统计
│   ├── health-check.mjs           #   断链 / 格式健康检查
│   ├── sync-专项题库.py            #   专项题库 Obsidian→站点 定向同步
│   └── 考点主清单-计算机.json       #   19 个考点的实测分值主清单
├── tests/                         # 单元测试
└── docs/.vitepress/               # VitePress 站点配置
```

---

## 📊 考频矩阵 · 专项题库 · Anki（2026-09 新增）

这一组是**基于真题原卷实测**的备考工具，不是网传估算。

### 为什么可信

对 **2023 + 2024 两年计算机真题原卷共 90 道题**逐题标注考纲模块，按分值统计，得出实测分布：

| 板块 | 实测分值 | 占卷比 | 网传说法 | 偏差 |
|:---|:---:|:---:|:---:|:---|
| **C 语言程序设计** | **129 / 200** | **64.5%** | 45–50% | ❌ 严重低估 |
| **数据结构** | **71 / 200** | **35.5%** | 50–55% | ❌ 严重高估 |

> 题型结构（原卷核实）：单选 20×3=60 · 判断 10×2=20 · 填空 5×4=20 · 简答 4×10=40 · 计算 3×10=30 · 应用 3×10=30 = **200 分 / 45 小题 / 150 分钟**。

### 三个直接结论

1. **别按网传比例分配时间** —— 数据结构实际只占 1/3 多一点，把一半时间砸在数据结构上是错的。
2. **数组（含字符串）是最大单模块**，35.5 分/卷，比"排序 + 查找 + 图"加起来还多。
3. **排序只有 2 分/卷**，是最容易被高估的模块（旧估算给到 ~10 分，高估 5 倍）。

### 交付物

| 交付物 | 位置 | 说明 |
|:---|:---|:---|
| 📊 **真题考频矩阵** | [在线](https://wpc725562-dotcom.github.io/darling016123/guide/真题考频矩阵) · `docs/guide/真题考频矩阵.md` | 19 模块 × 实测分值 × 占卷比 × 题型分布 |
| ✍️ **分章专项题库** | [在线](https://wpc725562-dotcom.github.io/darling016123/posts/computer/专项题库/) · `历年真题/计算机程序设计/专项题库/` | 6 个文件覆盖 19 模块，共 100+ 题，含折叠答案与扣分坑 |
| 🃏 **Anki 卡片包** | `docs/public/downloads/anki-computer.txt` | 172 张卡片 / 19 分类，制表符分隔，可直接导入 Anki |
| 📋 **考点主清单** | `scripts/考点主清单-计算机.json` | 机器可读，含 `实测分值` / `占卷比` / `题型分布` / `数据来源` |

**专项题库推荐刷题顺序**（按实测权重）：

```
01 数组与字符串（35.5 分）→ 02 循环结构（29.0 分）→ 03 线性表（17.5 分）
→ 04 数据结构基本概念（15.0 分）→ 05 中权重合集（49.0 分）
→ 06 低频速查（53.5 分，只背不刷）
```

> ⚠️ 与 2026-09-12 的模板整改保持一致：笔记正文里**不再写星级评分与预估分值**
> （那批无出处估算已由 `knowledge/removed-考情块存档.md` 存档）。
> 本节的 35.5 / 29.0 等数字**全部来自 90 道真题逐题计数**，可复核、可复现，
> 与"拍脑袋预估"性质不同 —— 这正是当初撤掉笔记内预估分值的理由。

---

## 📖 学习路线

### 阶段一：基础入门（第一轮）

| 顺序 | 内容 | 时间 |
|:---:|:---|:---:|
| 1 | [0.0 计算机基础理论](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/0.0-计算机基础理论) | 1 天 |
| 2 | [1.1 C语言概述](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/1.1-C语言概述与基本概念) → [1.5 循环结构](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/1.5-循环结构程序设计) | 5 天 |
| 3 | [1.6 数组](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/1.6-数组) → [1.7 函数](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/1.7-函数) → [1.8 指针](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/1.8-指针) | 5 天 |
| 4 | [1.9 结构体](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/1.9-结构体与共用体) → [1.10 文件](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/1.10-文件操作) | 2 天 |

### 阶段二：数据结构（第二轮）

| 顺序 | 内容 | 时间 |
|:---:|:---|:---:|
| 1 | [2.1 数据结构概念](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/2.1-数据结构基本概念) → [2.2 线性表](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/2.2-线性表) → [2.3 栈和队列](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/2.3-栈和队列) | 4 天 |
| 2 | [2.4 串/数组/广义表](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/2.4-串、数组和广义表) → [2.5 树和二叉树](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/2.5-树和二叉树) | 3 天 |
| 3 | [2.6 图](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/2.6-图) → [2.7 查找](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/2.7-查找) → [2.8 排序](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/2.8-排序) | 4 天 |

### 阶段三：专项突破 + 模拟（第三轮）

| 顺序 | 内容 | 时间 |
|:---:|:---|:---:|
| 1 | [3.0 改错题专项](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/3.0-改错题专项训练) | 1 天 |
| 2 | [3.3 编程题策略](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/3.3-编程题做题策略) | 1 天 |
| 3 | [高频错题汇总](https://wpc725562-dotcom.github.io/darling016123/posts/computer/notes/高频错题汇总) 复盘 | 1 天 |
| 4 | 卷一 → 卷二 → 卷三 限时模拟 | 3 天 |

---

## 📝 笔记使用说明

笔记**按科目分三套结构**（不是全局单一模板，此前 README 的描述已失真，2026-09-17 修正）：

### 计算机基础与程序设计（6 模块）

| 模块 | 图标 | 内容 |
|:---|:---:|:---|
| 这一章在考试里怎么出现 | ① | **只讲题型**（单选/判断/填空/计算/应用），不写星级评分、不做分值预估 |
| 零基础大白话引入 | ② 🗣️ | 生活化类比（厨师/储物柜/排队等）|
| 正式核心知识点讲解 | ③ 📖 | 考纲要求 + 真题实考内容，禁止超纲 |
| 真题同源例题 | ④ 🧪 | 入门基础题 + 真题改编题，逐变量推演 |
| 历年真题高频扣分坑 | ⑤ ⚠️ | 每章 10 条陷阱表，含出处年份 |
| 课后自测练习题 | ⑥ 📝 | 2-5 题真题风格 + VitePress 折叠答案 |

### 高等数学（6 段）

大白话通俗比喻 → 考点全爆破 → 核心难点 → 考场易错点 → 手把手真题演练 → 闭卷通关训练营

### 政治理论（3 段）

核心知识 → 要点速记 → 闭卷挑战

> 📌 **关于「历年真题考情」模块**（2026-09-12 整改）：
> 原 ① 模块含「出题频次星级 ⭐⭐⭐⭐⭐」「预估分值 10~30 分/200 分」「具体题号统计」，
> 已从 21 篇笔记中整体摘除，原文存档于 `knowledge/removed-考情块存档.md`。
> 原因：星级与预估分值属模板膨胀且无助于理解；部分引用的题号经核对在真题原卷中查无出处。
> **替代方案**：全局只保留一份可复核的 [真题考频矩阵](https://wpc725562-dotcom.github.io/darling016123/guide/真题考频矩阵)，
> 由 90 道真题逐题计数得出，可复现、可追溯。

---

## 🌐 在线访问

**VitePress 站点**：https://wpc725562-dotcom.github.io/darling016123/

> 2026-09-17 实测：首页与内页均返回 **200**，站点正常运行。
> 支持搜索、导航、代码高亮、数学公式渲染、PWA 离线。
>
> ⚠️ 仓库已由 `zhuan-sheng-ben-notes` 改名为 `darling016123`（2026-09-12 前后）。
> 旧地址 `.../zhuan-sheng-ben-notes/` 已失效，站内 base 与所有链接已同步为新名。
> 若在外部笔记或收藏夹里存过旧地址，需要一并更新。

---

## 🛠️ 技术栈

- **框架**：VitePress 1.6 + Vue 3
- **部署**：GitHub Actions → GitHub Pages（`deploy.yml`）
- **数学公式**：markdown-it-mathjax3
- **代码高亮**：highlight.js
- **搜索**：VitePress 本地搜索
- **本地笔记**：Obsidian（双链导航）

---

## 🔧 本地开发

```bash
npm install            # 安装依赖
npm run docs:dev       # 本地预览（热更新）
npm run docs:build     # 构建站点（约 177 秒）
npm run health:check   # 仓库健康检查（断链/BOM/索引/文件大小）
python scripts/repo_stats.py   # 笔记数与真题页数统计
bash scripts/test-patrol-logic.sh   # 巡逻脚本自检（改动 auto-patrol.yml 后必跑）
```

> ⚠️ **不要运行 `npm run docs:sync`**（即 `scripts/sync-obsidian-to-blog.mjs`）。
> 该脚本自身的注释即标注为「危险」：模板已落后于 `docs/` 里的人工精修内容，
> 直接运行会删掉 `config.mts` 的 PWA 配置、日语板块、四科导航等约 290 行。
> 需要把 Obsidian 侧新文件同步到站点时，用定向脚本，例如
> `python scripts/sync-专项题库.py`（只处理专项题库，不动其他配置）。

---

## 🚨 CI 质量门（自动巡逻）

`.github/workflows/auto-patrol.yml` 每天凌晨 3:00 + 每次推送到 `main` 时自动巡检，
共 13 个步骤：

| 级别 | 检查项 | 说明 |
|:---|:---|:---|
| P0 | 🧪 巡逻脚本自检 | 跑 `scripts/test-patrol-logic.sh`，脚本自身有问题立刻红灯 |
| P0 | 🔨 站点构建 | `npm run docs:build` |
| P0 | 🔗 断链检查 | wiki 双链 + markdown 链接 |
| P1 | 📋 质量体检 | 标题跳级 / BOM / 乱码字符 |
| P1 | 📑 索引一致性 | Obsidian 侧 vs 站点侧文件数对照 |
| P2 | 📊 覆盖率分析 | 基线锚定指标，见下方说明 |

```bash
bash scripts/test-patrol-logic.sh   # 本地跑巡逻脚本自检（功能测试 + 防回归扫描）
```

**覆盖率指标的口径**：统计的是「笔记文件数 ÷ 基线期望值」，用于发现
**文件被误删 / 同步失败导致数量回退**，**不是**考纲覆盖百分比。
基线配置在 `scripts/coverage-expectations.json`，笔记数增长后需更新；
报告出现「⚠️超预期」即表示基线过期。

**报告文件**（均在 `knowledge/`）：

| 文件 | 性质 |
|:---|:---|
| `patrol-report-YYYYMMDD.md` | 每日综合报告，自动轮转只保留最近 30 份 |
| `link-report.md` / `quality-report.md` / `index-report.md` | 机器生成，每次覆盖 |
| `coverage-report-auto.md` | 机器生成，每次覆盖 |
| `coverage-report.md` | **人工复核版，不会被脚本覆写**，人工结论写这里 |

> ⚠️ **为什么机器产物与人工产物要分文件**：2026-09-17 审核发现，覆盖率脚本原本
> 直接覆写 `coverage-report.md`，而该文件是 2026-08-18 的人工复核修正版
> （纠正了「按文件大小误判空占位」并如实标注真题来源类型）。只要手动触发一次
> 全量巡逻，那份内容就会被机器统计悄悄替换掉。现已分离，并由自检脚本 7 项
> 防回归扫描守住这条线。

---

## 🛠️ Agent 开发项目

> 本仓库作者也是 **AI Agent 开发者**，以下是相关的 Agent 开发项目：

| 项目 | 说明 | 技术栈 |
|:---|:---|:---|
| 🎓 [本科通 · 学习助手](bencetong/) | 广东专升本桌面学习助手：学习看板 / 笔记阅读 / 刷题练习（对接 Anki）/ 科学学习指南 / GitHub 同步。AI Agent 辅助开发 | Electron + Vue 3 + Vite + Pinia |

> 🔜 更多 Agent 开发项目（如真题检索 MCP 插件）正在建设中，敬请期待！

---

## 📋 更新日志

| 日期 | 更新内容 |
|:---|:---|
| **2026-09-17** | **巡逻工作流全面审核修复（8 项）**：① 覆盖率脚本不再覆写人工复核版报告（拆出 `coverage-report-auto.md`）；② 覆盖率期望值从硬编码改为配置化，修正 `194%/220%/111%` 的荒谬数字为 `100%`；③ 报告轮转，`patrol-report-*.md` 只保留最近 30 份（原已堆积 30 份且无限增长）；④ Issue 去重，此前每天新建重复 Issue（已堆积 13 个未关闭）改为追加评论；⑤ 新增「全绿时自动关闭遗留 Issue」步骤；⑥ `rebase` 冲突后自动回滚，不再残留冲突标记；⑦ 报告「总检查项」不再写死为 4；⑧ 新增 `scripts/test-patrol-logic.sh` 巡逻脚本自检（功能测试 + 防回归扫描），并接入 CI 作为 P0 门禁 |
| **2026-09-17** | **补审剩余两个工作流**：`deploy.yml` 的「通知 ai-learning-assistant 重建 RAG」是**死代码** —— `env` 定义在该 step 自己的 `env:` 里，而 step 级 `if` 在 env 生效前求值，条件恒为假，这步从未执行过；同时 `curl` 未加 `-f`，HTTP 4xx/5xx 也打印「✅ 已通知」（假成功）。已改为在 `run` 内判断并读真实状态码。另补 `scripts/lib/**` 到巡逻触发路径（改共用库原本不会触发自检），并新增「三套链接检查器 SKIP_WIKI 必须一致」的防回归扫描。`test.yml` 审核无问题 |
| **2026-09-17** | **真题考频矩阵实测落地**：对 2023+2024 两年 90 道计算机真题逐题标注，得出 C 语言 **64.5%** / 数据结构 **35.5%** 的实测分布，推翻网传 45-50% / 50-55%。新增 [考频矩阵页](https://wpc725562-dotcom.github.io/darling016123/guide/真题考频矩阵)、**6 篇分章专项题库**（100+ 题）、**172 张 Anki 卡片**；`考点主清单-计算机.json` 的 `score_weight` 由估算值（`~10分`）改为实测值 + `占卷比` / `题型分布` / `数据来源` 字段 |
| **2026-09-17** | **仓库审核修复**：`health-check` 修复 `[[toc]]` 被误判为断链；修复 3 处死链（高频考点 2 篇）；33 个文件剥离 BOM 头；`.gitattributes` 补充 20 种二进制类型声明 + linguist 统计排除规则；`.gitignore` 补 VitePress 构建产物；`docs/guide/index.md` 清除过期外部路径并加入 `docs:sync` 危险警告。健康检查 **6 通过 / 0 警告** |
| **2026-09-17** | **README 账实对齐**：修正笔记数（213→219，含 6 篇专项题库）、真题页数；**修正失真的「6 模块统一模板」描述** —— 实际分三套结构（计算机 6 模块 / 高数 6 段 / 政治 3 段），并说明 2026-09-12 摘除星级与预估分值的原因与替代方案 |
| 2026-09-07 | **知识库完善冲刺**：新增计算机 5 个必杀考点专项（3.4 循环数组 / 3.5 指针 / 3.6 递归 / 2.4a KMP / 2.5a 二叉树建树，26 项答案验证通过）；高数 2025 图片回忆版 OCR 文字化成卷（高置信题详解+低置信待校对）；政治 2025 考情页；高数新增 1.10 极限计算三法决策树；README 账实刷新；新增 .gitattributes 根治 CRLF |
| 2026-08-24 | **仓库同步与升级**：合并远程/本地提交，新增 Agent 开发项目展示区 |
| 2026-08-24 | 仓库四科整合：README 对齐高数/计算机/政治/英语全科结构 |
| 2026-08-24 | 补全政治历年真题 2012-2019 + 2025 高数回忆版（图片） |
| 2026-08-16 | P0-P4 全项目闭环：20+ 篇笔记重制、14 份审计报告、3 套模拟卷、2 份汇总文档 |
| 2026-08-15 | 笔记审计流水线启动，全局 6 模块格式统一，CI 修复 |

---

<p align="center">
  <strong>📚 广东专升本 · 四科复习笔记库</strong><br>
  <a href="https://wpc725562-dotcom.github.io/darling016123/">🌐 在线访问</a> •
  <a href="https://github.com/wpc725562-dotcom/darling016123">📦 GitHub 仓库</a>
</p>
