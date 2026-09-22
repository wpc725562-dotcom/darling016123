# flyingmouse-format 对照评估与升级方向

> **结论先行**
> 1. **不引入** —— 上一轮已判定（能力重叠、1.41 GiB 安装包、非商用许可 + PyMuPDF AGPL 摩擦），本轮复核后维持不变。
> 2. 但**它确实比我们多两块东西**，且**都在我们现有依赖里就能实现**：
>    - **PDF 表格结构化提取**（我们完全没有；`pymupdf 1.28.2` 已自带 `find_tables()`，**零新增依赖**）
>    - **低置信度批注**（我们的 OCR 早就产出了置信度字段，**却从来没有任何脚本消费它**）
> 3. 另有两条**工程约定**值得抄：`capabilities` / `targets` 自描述子命令、`--json` 契约补全。
> 4. 其余 7 类能力（图片/音频/视频/RAW/电子书/GUI/AES 加密）与我们场景无关，**明确不学**。
>
> 本文所有「我方现状」结论均来自本轮对仓库的实际检索；所有「可行」判断均来自**在本仓库真原卷上跑过的实测**，不是推断。

---

## 一、被测对象：flyingmouse-format 的真实能力清单

| 项 | 实测值 |
|:---|:---|
| 仓库 | `LaoFeng-mouse/flyingmouse-format`（另有镜像 `shenpipi/flyingmouse-format2pp`） |
| 版本 | 0.7.10（Windows 公开版） |
| 形态 | Electron 桌面应用 + Node CLI（`cli.js`），可向 `~/.codex/skills`、`~/.claude/skills`、`~/.agents/skills` 一键装 skill |
| 内置引擎 | FFmpeg、LibreOffice、Poppler、Tesseract、Pandoc、dcraw、docengine（含 PyMuPDF） |
| 体积 | 安装包 **1,515,803,399 字节（≈1.41 GiB）**，完整展开 **≈3.76 GiB** |
| 平台 | Windows 10/11 x64；**macOS / Win7 / Store 版本轮未发布**；安装包**未签名**（SmartScreen 会拦） |
| 许可 | **非商用许可**；禁止售卖/转卖/套壳换皮；二次开发须标注原作者；内置 PyMuPDF 为 **AGPL-3.0** |
| 本地状态 | **未安装**（本轮复核确认） |

### 支持的转换（9 类）

| 类别 | 输入 | 输出 |
|:---|:---|:---|
| 图片 | jpg/png/webp/avif/tiff/gif/bmp/heic/heif + 21 种相机 RAW | png/jpg/webp/avif/tiff/gif/pdf/txt(OCR)/mp4/webm |
| 文本 | txt/md/html/json/csv/log/xml/yaml | txt/md/html/json/csv/pdf/docx/epub |
| 电子书 | epub/mobi | txt/md/epub（mobi→epub 实验性） |
| Word/WPS/OFD | doc/docx/odt/rtf/wps/wpt/wpd/ofd | pdf/docx/odt/rtf/txt/html/md |
| Excel/WPS | xls/xlsx/xlsm/ods/csv/tsv/et/ett | pdf/xlsx/xls/ods/csv/html |
| PPT/WPS | ppt/pptx/odp/dps/dpt | pdf/pptx/odp/html/png/jpg（逐页转图 zip） |
| PDF | pdf | xlsx/docx/txt/html/png/jpg/split/加解密 |
| 音频 | mp3/wav/flac/m4a/aac/ogg/opus/wma | 同左（**不支持 NCM/KGG/mflac/kgma/kwm 等平台加密格式**） |
| 视频 | mp4/mov/mkv/webm/avi/m4v/wmv/flv | mp4/webm/mkv/mov/gif + 音频轨；编码可选 H.264/H.265/AV1 |
| 任意文件 | any | zip |

### 真正值得看的两块细节

- **PDF → Excel（智能表格提取）**：电子文字坐标 / 扫描页 OCR / 有框与无框表格 / 多表 / 跨页续接 / 合并单元格 / **低置信度批注**。
- **CLI 契约**：每个子命令都吃 `--json`，且有两个**自描述**子命令：
  ```
  node cli.js capabilities --json          # 我能做什么
  node cli.js targets example.pdf --json   # 这个文件能转成什么
  node cli.js convert input.docx --to pdf --output output.pdf --json
  node cli.js images-to-pdf 1.jpg 2.jpg --output album.pdf --json
  node cli.js merge-pdfs a.pdf b.pdf --output merged.pdf --json
  ```
- **已知精度边界**（作者自己写的）：PDF→Word「复杂多栏、图片定位和扫描标点**不能保证**与原 PDF 完全一致」；高级表格识别限 500 页 / 单页 5000 万像素 / 每批 8 页且累计 1 亿像素（144 DPI），且**要求至少 5 GiB 可用物理内存**。

---

## 二、我方现状盘点

| 项 | 实测值 |
|:---|:---|
| 脚本数 | `scripts/` 下 **67 个 `.py` + 24 个 `.mjs` = 91 个**（另有 `.bak-*` 备份） |
| 体积 | **2.7 MB**（对比 3.76 GiB） |
| 支持 `--json` | **13 个**（`zhenti_lint` / `zhenti_regress` / `zhenti_log` / `check-links` / `check-md-hazards` / `check-session-ledger` / `health-check` / `mistake-stats` / `bili_search` / `bili_ytdlp` / `bili_audit_links` / `bili_zhenti_diff` / `bili_merge_extract`） |
| 第三方依赖 | 9 个，全部声明在 `requirements.txt`（2026-09-20 补） |
| 关键依赖 | `PyMuPDF==1.28.2`、`Pillow`、`python-docx`、`matplotlib`、`numpy`、`rapidocr-onnxruntime`、`sympy`、`qrcode`、`yt-dlp` |
| 真题配置 | `scripts/zhenti_cfg/*.json` 共 **43 份** |

### 现有管线（按职责）

| 环节 | 脚本 |
|:---|:---|
| PDF → 文本 | `pdf_to_md.py`（文字层直抽，跳过「去水印后 <50 字」页）、`pdf_vision_ocr.py`（视觉模型 OCR，**分页渲染 / 断点续跑 / 余额守卫 / 失败重试**）、`pdf_fill_image_pages.py`（补「图片排版页」）、`pdf_pipeline.py`（PDF/DOCX 分流） |
| 真题页生成 | `zhenti_promote_english.py` → `zhenti_convert.py`（**配置驱动**） |
| 真题页校验 | `zhenti_lint.py`（`--all-configs` 才查「配置↔页面」一致性）、`zhenti_regress.py`（复现比对） |
| B 站语料 | `bili_*` 共 **25 个**（字幕、视频、抽帧、OCR、**判色**、校验、知识地图） |
| 考点统计 | `extract_topics.py` → `map_chapters.py` |
| 站点质量闸门 | `check-md-hazards.mjs`、`check-links.mjs`、`sync-home-stats.mjs`、`build-docs.mjs` |
| 产物 | VitePress 静态站（385 html） |

---

## 三、能力矩阵对照

| 能力 | flyingmouse | 我方 | 判定 |
|:---|:---:|:---|:---|
| PDF 文字层直抽 | ✅ | ✅ `pdf_to_md.py` | 打平（我们的**跳过规则可配置**，更贴合） |
| 扫描页 OCR | ✅ Tesseract | ✅ 视觉模型 + `rapidocr` | **我方更强**（视觉模型对中文排版更好；有断点续跑） |
| **PDF 表格 → 结构化** | ✅ 一整套 | ❌ **完全没有** | **★ 真差距** |
| **低置信度批注** | ✅ | ❌ 字段有、**从未消费** | **★ 真差距** |
| **自描述 capabilities/targets** | ✅ | ❌ | **★ 真差距** |
| `--json` 输出 | ✅ 全量 | ⚠️ 13/91 | **★ 部分差距** |
| PDF 拆分 / 加解密 | ✅ AES-256 | ❌ | 无场景，不学 |
| Markdown → Word/PDF | ✅（可编辑公式 OMML） | ✅ `md-to-printable.py` + MathJax 预渲染 SVG | **方向不同**，我方更贴合（离线可看） |
| HTML → PDF | ✅ | ✅ `html-to-pdf.mjs` | 打平 |
| 图片 / 音频 / 视频 / RAW / 电子书 | ✅ 9 类 | ❌ | 无场景，不学 |
| GUI | ✅ Electron | ❌（CLI + 静态站） | 不需要 |
| 真实进度与耗时 | ✅ | ⚠️ 有进度落盘，无耗时冻结 | 低优先 |
| 操作记忆 / 路径记忆 | ✅ | ❌ | 不需要（脚本无状态更可复现） |
| 全本地离线 | ✅ | ✅ | 打平 |

---

## 四、真正的差距 —— 4 条，按价值排序

### D1 ★★★ PDF 表格结构化提取（最高价值，且**已验证零成本可行**）

**问题**：`scripts/pdf_to_md.py` 里 `table` / `find_tables` / `表格` **出现 0 次**。表格进了文字流就被压平——我们的「试卷结构」表（**必须 5 列**）、分值分布表、答案区**全靠手敲**。

**实测证据**（本轮在本仓库真原卷上跑的）：

```
=== english/2013-full.pdf ===
  p9 strategy=lines 表数=0
  p9 strategy=text  表数=1  [63x11 bbox=(62, 102, 482, 741)]
=== english/2014-full.pdf ===
  p9 strategy=text  表数=1  [57x10 bbox=(75, 102, 535, 654)]
=== english/2015-full.pdf ===
  p9 strategy=text  表数=1  [53x8  bbox=(62, 129, 511, 683)]
```

抽取质量（2013 第 9 页答案区）：

```
r4: ['1. B', None, None, '2. D', None, '3. B', None, '4. C', None, None, '5. B']
r6: ['6. A', None, None, '7. D', None, '8. A', None, '9. A', None, None, '10. C']
```

⇒ **答案键被干净地抽成了 `题号. 字母` 单元格**。逐词碎片（`I Voca` / `bulary`）说明它**不适合抽散文**，但抽**答案键**恰好完美。

**为什么这条价值最高**：它给答案**多出第三条独立来源**。MEMORY 里记着一条血债 ——
> 「答案有两个独立来源，**互不校验、各自沉默出错**」——`english2022.json` 速查表与官方 31/45 不符，而正文 45/45 全对。

现在两条来源都走**同一个文字流**。`find_tables(strategy="text")` 走的是**坐标聚类**，与 `re.finditer(r"^(\d{1,2})\.\s*([A-D])\s*$")` 的**行序假设完全独立**。三条路径互校，才能真正堵住「静默出错」。

**实现要点**
- 新建 `scripts/pdf_tables.py`（**零新增依赖**，`pymupdf 1.28.2` 已具备）
- 接口：`--pdf <路径> [--pages 1-3] [--strategy lines|text|auto] [--json] [--out <md>]`
- **`auto` 策略必须做**：先 `lines`，表数为 0 再退 `text` —— 实测我们的原卷**全部走 `text`**（答案区无框线），只有 `lines` 会 0 命中
- 跨页续接：比对相邻页**首行 / 末行表头是否逐字相同**，相同才合并（不要按「页相邻」就合并）
- 低置信度：单元格 bbox 非空但 `extract()` 为 `None`/空串 ⇒ 标 `⚠️`（见 D2）
- 表格输出：markdown 管道表；**列数必须由表头决定，不允许补空格凑数**（对应 MEMORY 里「试卷结构表写成 6 列 ⇒ 整卷权重被压到 42%」那次事故）

**验收判据**（可复算）
```bash
python scripts/pdf_tables.py --pdf docs/public/papers/english/2013-full.pdf --pages 9 --json
# 必须：tables>=1，且解析出的 (题号,字母) 对 == _build2013.py 的 extract_answers() 结果（65 对，逐对相等）
```

---

### D2 ★★ 低置信度字段消费（字段早已产出，**从未被读**）

**问题**：`scripts/bili_ocr_frames.py:114` 每行都写了 `"s": round(float(score), 3)`，schema 是
```json
{"frame": "p01_0001.jpg", "lines": [{"t": "文本", "s": 0.987, "box": [[x,y]×4]}]}
```
但 `_ocr.jsonl` 的三个消费方（`bili_color_answers.py` / `bili_ocr_answers.py` / `bili_ocr_frames.py` 自身）**没有任何一处读过 `s`**（全仓检索 `.get("s")` / `["s"]` 在消费侧 0 命中）。

**为什么值得补**：MEMORY 里有一整类教训是「**我看到的文字是 OCR 猜的，不是原卷印的**」——
- 政治 2026 用 `--fpm 3.0` 抽帧，整屏落在两次采样之间 ⇒ 误记「A/B/C 画面未捕获」
- 完形第 27 题 C/D 被 OCR 并成一行 ⇒ 一度判错答案

这两次都是**事后靠人眼回看原卷**才发现的。有了置信度阈值，这类行**在流水线里就能自己举旗**。

**实现要点**
- 在 `bili_ocr_frames.py` 的 `_ocr.jsonl` 之外，**另写一份 `_ocr_lowconf.jsonl`**（不破坏既有 schema，向后兼容）
- 阈值走参数：`--min-conf 0.85`（默认值写进 `--help`，不硬编码在函数里）
- 汇总打印：`[低置信] 528 帧 / 14320 行 → 低置信 213 行（1.49%），涉及帧 97 个`
- **消费侧**：`bili_color_answers.py` 判色前，先把低置信行标 `?` 并**排除出投票**（宁可少投一票，不要投错一票）
- 判据：**低置信率**本身是「这版抽帧够不够」的量化指标 —— 比 MEMORY 里「抽帧率与内容停留时长匹配吗」这种定性判断更硬

**验收判据**
```bash
python scripts/bili_ocr_frames.py --help        # 必须能看到 --min-conf 及其默认值
# 对已有 _ocr.jsonl 跑一次汇总：输出「总行数 / 低置信行数 / 占比 / 涉及帧数」四个数
```

---

### D3 ★★ 管线自描述：`capabilities` / `targets`

**问题**：91 个脚本，**没有一处能回答「这个文件能跑哪些脚本」**。所有前置条件都写在**人脑和 MEMORY.md 里**。

**为什么这条对我们特别值**：MEMORY 里最贵的一类事故全是「**入口条件没接住**」——
- 「凡改用 `## Part N` + 选项表格的真题页（英语 2026）**整页静默剔除**」
- 「一个页面『变成有结构』就会**静默进入统计**」
- 「`zhenti_lint.py` **没有 `--config`**：只传页面路径就静默只查页面、看着全绿」

这些都是**脚本能自描述、就不会发生**的事故。

**实现要点**
- 新建 `scripts/zhenti_pipeline.py`（**纯读取，不写任何产物**）
- `capabilities --json` ⇒ 逐脚本：`{path, role, reads, writes, requires, exit_codes, silent_fail_modes}`
  - `silent_fail_modes` 是**关键字段** —— 直接抄 MEMORY 里的判例（如 `zhenti_lint.py` 的「只传页面路径 ⇒ 只查页面」）
- `targets <file> --json` ⇒ 按文件路径匹配可跑的脚本 + **必须先跑哪个**
- `preflight <脚本> --json` ⇒ 跑之前检查前置文件是否存在（把「先备份 `analysis.json`」这类口头规矩变成断言）

**验收判据**
```bash
python scripts/zhenti_pipeline.py capabilities --json | python -m json.tool > /dev/null && echo OK
# 必须：>=10 个脚本条目，且每个都有非空 silent_fail_modes
```

---

### D4 ★ `--json` 契约补全（13/91 → 优先补 5 个）

**现状**：13 个有 `--json`，且 `zhenti_lint.py` 的实现**质量很高**（逐项明细 + 把 stdout 重定向到 stderr 再只打一个 JSON）。缺的不是机制，是覆盖面。

**优先补这 5 个**（理由：它们是**既读也写**的脚本，没有 `--json` 就没法在临时路径下安全断言）：

| 脚本 | 为什么急 |
|:---|:---|
| `extract_topics.py` | `main()` **既读 `topics.json` 也写 `analysis.json`** —— MEMORY 记着「只替换输入路径会让**假标签写进真实产物**」。有 `--json` 才能把 `unmatched` 当成断言而不是打印 |
| `map_chapters.py` | 同上，未命中标签必须为 0 |
| `zhenti_promote_english.py` | 「题号 66 / 选项 260 / Passage 4」这些数字现在只能靠人眼看 stdout |
| `zhenti_convert.py` | 「选项行 0 是正常值」这种反直觉判据必须机器可判 |
| `pdf_to_md.py` | 「跳过 N 页」现在只打印，上层拿不到 |

**关键约定（抄 `zhenti_lint.py` 的）**：`--json` 时把人类可读输出**整体重定向到 stderr**，stdout **只留一个 JSON** —— 否则 `| jq` 会被日志污染。

**验收判据**
```bash
python data/zhenti-extract/extract_topics.py --json 2>/dev/null | python -m json.tool > /dev/null
# 且 JSON 里必须有 unmatched 字段（数组），并断言为空
```

---

## 五、明确**不该学**的（附理由，避免下次重新纠结）

| 项 | 为什么不该学 |
|:---|:---|
| 图片 / 音频 / 视频 / RAW / 电子书 转换 | 与本项目零交集。为它付 **3.76 GiB** 展开体积，换来的能力一行都用不上 |
| Electron GUI | 我们是 **CLI + VitePress 静态站**。加 GUI 等于把可 diff、可进 Git、可断点续跑的管线，换成不可审计的二进制 |
| Markdown → Word 的**可编辑公式（OMML）** | 我们的场景是「**离线能看**」⇒ 已用 MathJax **构建期预渲染成内联 SVG**（`offline-mathjax-html` skill）。OMML 是「可编辑」，SVG 是「可阅读」——**方向不同，不是落后** |
| PDF AES-256 加解密 | 无场景（我们的 PDF 是公开原卷，站点上直接发） |
| 操作记忆 / 路径记忆 | 脚本**无状态**才可复现。记住「上次选了哪个格式」在 GUI 里是体贴，在管线里是**隐藏输入** |
| 非商用许可 + AGPL-3.0 docengine | 许可摩擦。我们已用 PyMuPDF（**上游 AGPL**），但走的是「内部工具、不外发二进制」这条兼容路径；引入一个**禁止商用**的整包只会把边界弄浑 |

---

## 六、硬约束（引用前必读）

1. **体积**：flyingmouse 3.76 GiB 展开 vs 我方 2.7 MB ⇒ 引入即**膨胀 1400 倍**。
2. **平台**：本轮只发 Windows 10/11 x64；macOS 无包；安装包**未签名**。
3. **许可**：非商用；**禁止套壳换皮重新发布**；二次开发公开发布须标注原作者并沿用非商用限制。
4. **内存门槛**：高级表格识别**要求 ≥5 GiB 可用物理内存** —— 我们的构站机同时跑 VitePress，这条会撞。
5. **我方硬约束不变**：只做本地修改，**不 `git commit` / 不 `git push` / 不建 PR**，HEAD 保持 `4930f93`。

---

## 七、落地顺序

| 序 | 动作 | 改动 | 成本 | 验收 |
|:--:|:---|:---|:---:|:---|
| 1 | **D2 置信度消费** | `bili_ocr_frames.py` +2 个消费方 | 低 | `--min-conf` 可见；汇总四数可打印 |
| 2 | **D1 PDF 表格提取** | 新建 `scripts/pdf_tables.py` | 中 | 2013 第 9 页答案键 **65 对逐对相等** |
| 3 | **D4 `--json` 补 5 个** | 5 个脚本各加一个分支 | 中 | `\| python -m json.tool` 不报错 |
| 4 | **D3 管线自描述** | 新建 `scripts/zhenti_pipeline.py` | 中 | `capabilities --json` ≥10 条且字段齐 |

**为什么 D2 排在 D1 前面**：D2 是**加一个参数 + 一个汇总函数**，半天的活；但它立刻把「OCR 猜的」变成**可量化**。而 D1 虽然价值最高，要处理跨页续接、`lines`/`text` 回退、列数一致性三件事，属于「要一次性做对」的活。

> ★ 两条都不要现在动。**当前手上还有 2013/2014 两卷真题在重建**（`_build2013.py` 尚未开写），先把内容批次闭环，再回来做工具链升级 —— 否则改了 `pdf_to_md.py` 会**污染正在跑的批次**。

---

## 附：本轮实测的原始证据

```
$ ls scripts/*.py | grep -vc '\.bak-'          → 67
$ ls scripts/*.mjs | wc -l                      → 24
$ grep -rl -- '--json' scripts/*.py scripts/*.mjs | wc -l   → 13
$ grep -nE 'table|find_tables|表格' scripts/pdf_to_md.py    → （空）
$ grep -rnE '\[.s.\]|\.get\(.s.\)' scripts/*.py | grep -v bili_ocr_frames  → （空）
$ python -c "import pymupdf; print(pymupdf.__version__, hasattr(pymupdf.Page,'find_tables'))"
                                                → 1.28.2 True
$ python scripts/_tmp/_probe_tables.py          → 见 §四 D1 输出
```

报告日期：2026-09-21 ｜ 作者：02
