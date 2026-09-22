---
title: 站点说明
---

# 站点说明

> ⚠️ **本页是作者自用的仓库说明**，其中的本地路径只在本机有效，读者不必也无法照着执行 —— 看站点本身即可。

本站是广东专升本复习笔记的 **VitePress 网页版**，源内容（Obsidian 库）与站点源码**在同一个仓库里**：

```
<仓库根>/            ← Obsidian 库（历年真题 / 备考计划 / 资料 / 高等数学 / 政治理论 …）
<仓库根>/docs/       ← VitePress 站点源码
```

## 内容从哪来

| 区块 | Obsidian 路径 | 网站路径 |
|:---|:---|:---|
| 高数章节 | `高等数学/` | [/posts/math/notes/](/posts/math/notes/) |
| 计算机知识点 | `计算机程序设计/` | [/posts/computer/notes/](/posts/computer/notes/) |
| 英语笔记 | `编程技能/专升本英语/` | [/posts/english/notes/](/posts/english/notes/) |
| 政治笔记 | `政治理论/` | [/posts/politics/notes/](/posts/politics/notes/) |
| 各科真题 | `历年真题/` | `/posts/{math,computer,english,politics}/` |

重新同步（本地）：

```bash
cd <仓库根>

# ⚠️ sync 已被 guardDeprecated() 阻止：docs/ 侧已分叉，模板会覆盖人工精修内容
node scripts/sync-obsidian-to-blog.mjs --dry-run --force   # 先看影响面，不落盘
node scripts/sync-obsidian-to-blog.mjs --force             # 确认无误再真写
node scripts/build-docs.mjs --no-trash
```

## 阅读建议

- **刷概念**：章节 / 知识点笔记（含闭卷答案块）
- **刷真题**：2024/2026 完整卷优先，再回溯演练页
- **搜索**：顶栏本地搜索可跨页找公式与关键词

## 主题

樱花二次元主题 + Live2D 看板娘。

详见 [资料边界](/guide/sources)。
