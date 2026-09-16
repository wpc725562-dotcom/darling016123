---
title: 站点说明
---

# 站点说明

本站是广东专升本（专插本）四科复习笔记的 **VitePress 网页版**。
**源内容就在本仓库内**（`历年真题/`、`高等数学/`、`政治理论/`、`docs/posts/` 等），不需要外部 Obsidian 库即可完整构建。

## 内容从哪来

| 区块 | 仓库内源路径 | 网站路径 |
|:---|:---|:---|
| 高数章节 | `高等数学/` | [/posts/math/notes/](/posts/math/notes/) |
| 政治笔记 | `政治理论/` | [/posts/politics/notes/](/posts/politics/notes/) |
| 英语笔记 | `编程技能/专升本英语/` | [/posts/english/notes/](/posts/english/notes/) |
| 计算机知识点 | `docs/posts/computer/notes/`（无 Obsidian 副本） | [/posts/computer/notes/](/posts/computer/notes/) |
| 计算机专项题库 | `历年真题/计算机程序设计/专项题库/` | [/posts/computer/专项题库/](/posts/computer/专项题库/) |
| 各科真题 | `历年真题/` | `/posts/{math,computer,english,politics}/` |
| 真题考频矩阵 | `docs/guide/真题考频矩阵.md` | [/guide/真题考频矩阵](/guide/真题考频矩阵) |
| Anki 卡片包 | `docs/public/downloads/anki-computer.txt` | `/downloads/anki-computer.txt` |

> 站点侧 `docs/posts/` 与 Obsidian 侧顶层目录是**同一份内容的两套视图**：
> 顶层目录用 `[[wiki 双链]]`（Obsidian 导航），`docs/posts/` 用 `/绝对路径`（VitePress 路由）。
> 但计算机知识点与考频矩阵只在站点侧维护，没有 Obsidian 副本。

## 本地构建

```bash
# 安装依赖（首次）
npm install

# 构建站点
npm run docs:build

# 本地预览
npm run docs:dev

# 仓库健康检查（断链 / BOM / 索引 / 文件大小）
npm run health:check
```

> ⚠️ **不要运行 `npm run docs:sync`**（即 `scripts/sync-obsidian-to-blog.mjs`）。
> 该脚本**自身的文件头注释**即标注为「⚠️ 危险（2026-09-04 实测）」：
> 模板已落后于 `docs/` 里的人工精修内容，直接运行会删掉 `config.mts` 的 PWA 配置、
> 日语板块、四科导航等约 290 行。
> 需要把 Obsidian 侧新文件同步到站点时，用定向脚本，例如
> `python scripts/sync-专项题库.py`（只处理专项题库，不动其他配置）。

## 阅读建议

- **刷概念**：章节 / 知识点笔记（含折叠答案块）
- **刷真题**：2024 / 2026 完整卷优先，再回溯演练页
- **查考频**：[真题考频矩阵](/guide/真题考频矩阵) 是 2023+2024 两年 90 道题逐题标注的实测分值表
- **刷专项**：[专项题库](/posts/computer/专项题库/) 按实测权重排序，高权重模块优先
- **搜索**：顶栏本地搜索可跨页找公式与关键词

## 主题

樱花二次元主题 + Live2D，参考开源博客 [a3292334877-star/blog](https://github.com/a3292334877-star/blog)。

详见 [资料边界](/guide/sources)。
