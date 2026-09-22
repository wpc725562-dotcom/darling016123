# 项目维基 · 模块文档

> 仓库各模块的职责、依赖、调用链、已知坑点。
> 依赖全景图见 [dependency-graph](../dependency-graph.md)；报错排查见 [agent-troubleshoot](https://github.com/wpc725562-dotcom/darling016123/tree/main/agent-troubleshoot)。

---

## 模块总览

| 模块 | 路径 | 职责 | 语言 |
|:---|:---|:---|:---|
| 学习库本体 | `历年真题/` `政治理论/` `高等数学/` `编程技能/` `资料/` | Obsidian 笔记源 | Markdown |
| 知识库流水线 | `knowledge/` `skills/` | PDF→标准试卷→知识库 | YAML + Markdown |
| 网页站 | `docs/` | VitePress 站点（GitHub Pages） | TS + Vue + MD |
| 脚本 | `scripts/` | 数据抓取/同步/填充 | Python + Node |
| 运维 | `.github/workflows/` | CI 自动部署 | YAML |
| 排障库 | `agent-troubleshoot/` | Agent 报错排查 | Markdown |
| 考点速查 | `computer-kb/` | 计算机考点对照/图谱 | Markdown |
| Agent 技能 | `agent-skills/` `skills/` | 可复用 Agent 技能 | YAML |
| 测试 | `tests/` | 单元测试 | Python |

---

## 1. scripts/ — 数据处理脚本

**依赖关系**（详见 dependency-graph.md）：
- Python 脚本：`pdf_pipeline.py`（PDF/DOCX 分流提取）、`fill_*.py`（真题补全）、`embed_video_links*.py`（B站视频嵌入）、`bili_fetch.py`（B站抓取）
- Node 脚本：`sync-obsidian-to-blog.mjs`（Obsidian→站点同步）、`export-english-embedded.mjs`、`fill-gaps-from-web.mjs`、`fill-more-exams.mjs`

**调用链**：
```
PDF真题 → pdf_pipeline.py → 历年真题/*.md
Obsidian笔记 → sync-obsidian-to-blog.mjs → docs/posts/*
考点笔记 → embed_video_links*.py → 笔记尾部嵌入B站视频
```

**已知坑点**：
- `pdf_pipeline.parse_pages('2-')` 开放区间会抛 ValueError（见 tests/）
- 扫描件需 OCR（rapidocr / tesseract），引擎参数 `--engine rapid|tesseract`
- PDF 中文字体 Identity-H 无 ToUnicode 时提取乱码（见排障库 E-03）

---

## 2. knowledge/ + skills/ — 知识库流水线

**流程**：
```
PDF试卷 → pdf-to-knowledge 技能 → knowledge/exam_papers/*.md（标准排版）
                ↓ 原始备份
        knowledge/exam_papers/raw_backup/
                ↓
        自动调用 knowledge-formatter 技能 → 统一排版
                ↓
        self-optimizer 技能定期复盘 → optimization-report.md
```

**技能清单**：
- `skills/pdf-to-knowledge.yaml` — PDF 提取清洗（v1.1.0）
- `skills/knowledge-formatter.yaml` — 知识库统一排版（v1.0.0）
- `skills/self-optimizer.yaml` — 质量复盘迭代（v1.0.0）
- `agent-skills/broken-link-repair.yaml` — 断链批量修复
- `agent-skills/anki-card-export.yaml` — Anki 卡片导出
- `agent-skills/official-source-verifier.yaml` — 官方来源核实
- `agent-skills/knowledge-base-integrity-check.yaml` — 知识库体检

---

## 3. docs/ — VitePress 站点

- 入口：`docs/index.md`（首页）+ `docs/.vitepress/config.mts`（导航/主题）
- 内容：`docs/posts/{math,computer,english,politics}/`（系统笔记 + 历年真题网页版）
- 主题组件：`docs/.vitepress/theme/components/`（樱花、Live2D、播放器等）
- 部署：GitHub Actions `deploy.yml` → Pages

**已知问题**：
- 构建有 500kB chunk 警告（非致命，见排障库 E-06）
- `docs/guide/index.md` 仍引用旧路径 `D:/专升本/专升本`（待更新）

---

## 4. .github/workflows/ — CI/CD

- `deploy.yml`：push 到 main → `npm ci` + `docs:build` → 上传 Pages artifact → 部署
- ⚠️ 最近 run 61-69 失败（build job），lockfile registry 已修复推送（见排障库 E-01）

---

## 5. computer-kb/ + agent-troubleshoot/ + tests/（本次新增）

- `computer-kb/`：计算机考点速查（易错点对照表 / 知识图谱 / 题型速览）
- `agent-troubleshoot/`：Agent 真实报错排查库（8 个 E-0x 条目）
- `tests/`：`pdf_pipeline.py` 单元测试（16 例全通过）
