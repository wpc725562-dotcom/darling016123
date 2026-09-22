---
title: "B站/抖音 视频解析 · Agent 项目调研"
description: "B站/抖音视频解析 Agent 项目调研（2026-09-18）· stars / license / 最后提交均经 GitHub API 实测"
---

# B站/抖音 视频解析 · Agent 项目调研

> 调研日期 **2026-09-18**。所有项目的 `stars / archived / license / 最后提交` 均通过 **GitHub API 与仓库页实测**取得，
> 不是抄博客。凡是标注「实测」的结论，都在本机跑过。

## 一句话结论

> **要「像豆包那样解析视频」，现成方案里最对口的是 `like-attract/video-to-note`（VideoToNo）。**
> 它是 Windows 便携 exe，B站/抖音/YouTube 通吃，**已经处理了我们实测到的 HTTP 412 风控**，
> 字幕拿不到时自动回退本地转写，并且同时提供 **MCP** 与 **Agent Skill** 两种接入。
>
> **但它对本机有一个硬前提**：本地转写走 CPU（`int8`）。本机是 **AMD 显卡**，
> CUDA 系方案全部出局，所以「本地转写」会明显慢于视频时长。
>
> ⚠️ **而且在本机，抖音这条路根本走不通** —— 见下一节。别为它调代码。

---

## ★ 零、先测可达性：本机抖音不通（2026-09-18 实测）

在花任何时间研究「怎么解析抖音」之前，先确认目标站**能不能访问**。本机不行：

| 目标 | 实测结果 |
|:---|:---|
| `www.douyin.com` | HTTP 200，但正文只有 **2397 字节**、`lang="en"`、无 `<title>`、只有一个 precollect 埋点脚本 |
| `v.douyin.com`（分享短链） | 同样 2397 字节占位页 |
| `iesdouyin.com/web/api/v2/aweme/iteminfo` | HTTP 200，**零字节** |
| **对照**：`www.bilibili.com` | HTTP 200，**118881 字节**，`lang="zh-CN"`，标题正常 |

**判据**：抖音响应头带 `Via: ens-cache40.l2nm125-7, ens-cache1.hk35` —— 走的是**香港节点**。
即本机出口 IP 被抖音判为**境外**，只返回占位页。

**结论**：这是网络出口问题，**不是代码问题**。换 UA、加 Referer、改请求头都不会有用。
要解析抖音只有两条路：① 走国内出口 IP；② 用抖音开放平台的正规 API（需开发者资质）。

> **方法学**：调研任何「解析某站点」的方案前，**第一步永远是测该站点的可达性**。
> 否则你会花几个小时调一个物理上不可能成功的爬虫。

---

## 一、先看本机硬件 —— 这决定了哪些方案直接出局

| 项目 | 实测值 |
|:---|:---|
| GPU | **AMD Radeon RX 7700 XT，12 GB**（WMI 报 4 GB 是 32 位字段截断的已知 bug，注册表 `qwMemorySize` 才是真值） |
| CPU | AMD Ryzen 5 5600（12 线程） |
| 内存 | 15.9 GB |
| Docker | 29.7.2 ✅ 已装 |
| ffmpeg / ffprobe | ❌ 不在 PATH，在 `D:/ACLOS/Cross/recorder-release/` |
| Python | 3.13（隔离 venv 在 `~/.workbuddy-ai/binaries/python/envs/default`） |

> **★ 这一栏是本页最重要的信息**：主流本地转写方案（faster-whisper GPU、GLM-ASR、Fun-ASR GGUF、
> onnxruntime-gpu）**全部按 CUDA 优化**。AMD 卡在 Windows 上跑这些要么走 ROCm（RDNA3 支持很不完整），
> 要么走 DirectML（生态薄）。所以：
>
> - **需要 NVIDIA + CUDA 的项目 → 直接排除**
> - **纯 CPU 转写 → 可以，但慢**（Ryzen 5 5600 上 `small` 约 3~5 倍实时，`medium` 约 1 倍）
> - **云端 ASR → 本机最优解**（已验证：Gemini 转 60 秒音频只要 16 秒）

---

## 二、候选清单（全部核实过）

### 第一梯队：真能直接用

| 项目 | ★ | 许可 | 最后提交 | 形态 | 为什么推荐 |
|:---|---:|:---|:---|:---|:---|
| **`like-attract/video-to-note`** | 71 | MIT | 2026-09-16 | **Win 便携 exe** + MCP + Skill | ★ 最对口。B站/抖音/YT/本地文件；**已处理 412 回退**；B站凭据扫码导入；CPU 可跑 |
| **`chubbyguan/chubbyskills`** | 683 | MIT | 2026-09-17 | 14 个 Skill + MCP | 平台最全（B站/抖音/小红书/公众号/X/播客/微博/知乎）；知识库 MCP；字幕优先 |
| **`7oMB2006/Bilibili-Video-Research`** | 8 | MIT | 2026-09-16 | MCP（Node） | ★ **最像豆包**：`language`/`vision`/`multimodal` 三模式，视觉模式会**剥掉音轨只看画面** |
| `suonian/vidknot` | 15 | MIT | 2026-09-17 | 桌面 | 11+ 平台一键提取（YouTube/B站/抖音/小红书/快手/TikTok/X/IG/视频号/微博/Vimeo） |
| `Yotsuki2213/BiliBili_VideoRead_MCP` | 30 | MIT | 2026-08-12 | MCP（Python） | **扫码登录**（终端出二维码，手机扫）→ 解掉「AI 字幕需登录」；纯 B站 API，零 yt-dlp |

### 第二梯队：方向对但规模小 / 需自担风险

| 项目 | ★ | 许可 | 最后提交 | 备注 |
|:---|---:|:---|:---|:---|
| `Evil0ctal/Douyin_TikTok_Download_API` | 20170 | Apache-2.0 | 2026-09-15 | 抖音/TikTok 自托管抓取 + MCP。**只做下载，不做理解** |
| `anYuJia/better-douyin` | 462 | NOASSERTION | 2026-09-17 | 抖音客户端增强 + MCP。许可不明 |
| `imlewc/video-to-subtitle-summary-skill` | 199 | MIT | 2026-07-19 | 抖音/小红书/B站 → 字幕+总结；faster-whisper 本地转写 |
| `JazerJu/video-miner` | 28 | **未标注** | 2026-09-16 | 强，但**要 NVIDIA GPU ≥8GB + Docker + CUDA 12.8** ⇒ 本机出局 |
| `ljb1020/video-batch-download` | 54 | MIT | 2026-08-16 | 批量下载+本地转写；抖音/B站/快手/小红书/微博 |
| `xiaohui5206/let-ai-read-video` | 8 | MIT | 2026-07-24 | 纯本地：faster-whisper + 场景感知抽帧，双通道带时间戳。**需 GPU** |
| `guimatheus92/mcp-video-analyzer` | 66 | MIT | 2026-09-13 | 通用视频分析 MCP（YT/IG/TikTok/Loom/X/Vimeo/直链/本地） |
| `Yi-luo-hua/BilibiliCrawler` | 37 | MIT | 2026-09-16 | B站爬虫 + LLM 分析 + MCP + GUI。偏评论/情感分析 |
| `sandraschi/bilibili-mcp` | 1 | MIT | 2026-09-17 | B站内容情报：搜索/热榜/视频情报/字幕摘要 |
| `cgmdeep/video-to-obsidian` | 0 | Apache-2.0 | 2026-09-17 | 抖音+B站 → Kimi 分析 → Obsidian。alpha |

### 已死 / 别用

| 项目 | ★ | 状态 |
|:---|---:|:---|
| `yzfly/douyin-mcp-server` | 1273 | ⚠️ **已归档**（2026-07-02） |
| `nilaoda/BBDown` | 13881 | ⚠️ **已归档，内容已删**（2026-05-14） |
| `SocialSisterYi/bilibili-API-collect` | 20215 | ⚠️ **已归档**（2026-01-30） |
| `n24q02m/imagine-mcp` | 4 | ⚠️ 已归档（2026-09-13） |

---

## 三、为什么推荐 VideoToNo（逐条对着实测说）

`like-attract/video-to-note` v1.4.1，MIT，2026-09-16 仍在提交。它的设计**正好把我们踩到的每个坑都处理了**：

| 我们实测到的坑 | 它怎么处理 |
|:---|:---|
| `x/web-interface/view` 稳定 **412** | README 明写「被风控（HTTP 412）时**自动回退到 `api.bilibili.com` 开放接口**」 |
| AI 字幕**只在登录态返回** | 「除常规字幕外，可在**登录后读取 B 站 AI 字幕**；凭据支持**扫码导入**」 |
| 大多视频**根本没字幕**（实测 0/27） | 无字幕时**自动回退** faster-whisper / paraformer 本地转写 |
| 本机 **AMD 卡无 CUDA** | CPU 模式用 `int8` 降负载；GPU 缺 CUDA 运行库**自动退回 CPU** |
| 中文转写质量 | **中文首选 paraformer**（`paraformer-zh` / `belle-turbo-zh`），不是 whisper |
| 长视频 | v1.4.0 起「长视频逐段完整记录，**3 小时课约 10 分钟**」 |
| 密钥安全 | Key 默认只留内存；落盘走 **Windows DPAPI 加密**，且与接口地址绑定 |
| 模型下载慢 | 默认走 **hf-mirror.com** 镜像，支持断点续传 |
| 怎么给 Agent 用 | **MCP**（`http://127.0.0.1:8000/mcp/sse`）+ **Agent Skill** 双通道 |

**它的 MCP 工具（10 个）**，其中三个是关键：

| 工具 | 说明 |
|:---|:---|
| `transcribe_video` | 只做带时间轴转录，**全程不调大模型 ⇒ 不需要任何 API Key** |
| `get_transcript` | 取转录正文（markdown 或 json 分段）。**任务后来生成笔记失败，转录照样能取** |
| `summarize_video` | 生成笔记；视频链接/Key/模型/B站凭据**均可省略**，自动复用本机已存配置 |

其余：`wait_for_task`（等终态，最长 45 秒，免频繁轮询）、`get_task_status`、`list_whisper_models`、
`save_llm_config`、`save_bilibili_credentials`、`list_llm_keys`、`get_saved_config`。

**安装**：下载 `VideoToNo-1.4.1-portable.exe` 双击即可，**不需要装 Python**。
源码跑则面向 Windows + Python 3.11。

> ⚠️ 注意：三种接入方式**都要先启动 VideoToNo**，任务由本地后端执行。

---

## 四、最像「豆包」的是 `Bilibili-Video-Research`

如果目标是「豆包那种：丢个链接，它看画面 + 听声音 + 出结论」，这个的**设计**最接近：

- 三种模式：
  - `language` → 只吃字幕/ASR，**不看画面**
  - `vision` → **上传前移除音轨**，只把可见文字当视觉证据（旁白和 BGM 不干扰结论）
  - `multimodal` → 都要
- 输出先给一段**确定性的 `VIDEO CONTEXT`**（公开元数据 + 社区语境状态），再给自然语言分析
- 评论默认启用，但明确标注为「**不可信的社区语境**」，不当事实用
- 工具：`analyze_bilibili_video`（可传 `start_seconds`/`end_seconds` 限定区间）、`analyze_video`、`inspect_video_window`
- `media_detail: "low"` 长视频广扫，`"default"` 查小号 UI 文字/代码

**代价**：需要 API Key（默认 StepFun `step-3.7-flash`，**也支持 Gemini** ← 本机已有 `GEMINI_API_KEY`）。
Node.js 24+，`ffmpeg-static` 与 `yt-dlp-exec` 随 npm 装，不用手配。
★ 只有 8，属小项目，得自担维护风险。

---

## 五、⚠️ 现成项目普遍存在的一个 bug

`Yotsuki2213/BiliBili_VideoRead_MCP` 的 `extractor.py` **第 20 行**：

```python
URL_VIEW = "https://api.bilibili.com/x/web-interface/view"   # ← 这个端点现在稳定 412
```

它最后一次提交是 **2026-08-12**，在 B 站加风控之前。**它的字幕逻辑是对的**
（正确读取了 `need_login_subtitle`、正确用了 WBI 签名的 `x/player/wbi/v2`），
只有元数据这一步会挂 —— **改一行就能救**：换成 `x/web-interface/wbi/view`（免签名，实测 200）。

> 本库自己的 `bili-note-mcp`（`D:/deeepseek/bili-note-mcp`，注意不在 `Desktop` 下了）
> 有**同样的问题**，`tools/bili_subtitle.py:92` 也用了这个端点。而且它的 reasonix 配置
> 还指向旧的 `Desktop\deeepseek\bili-note-mcp` 路径 ⇒ **该 MCP 目前根本没加载**。

---

## 六、本库已有的自研方案（不依赖任何第三方）

`scripts/bili_analyze.py` —— 给个 BV 号，产出「元数据 + 逐字稿 + 画面帧」的解析材料。
**已实测跑通**，零第三方依赖（标准库 + ffmpeg + ffprobe）。

```bash
python scripts/bili_analyze.py BV号 [--pages 1-3] [--chunk 300] [--fps 1] [--no-video]
```

| 能力 | 实现 | 实测状态 |
|:---|:---|:---|
| 元数据 | `x/web-interface/wbi/view` | ✅ 30 抽样 27 成功 |
| 字幕 | 优先抓 CC 字幕，免 ASR | ✅ 逻辑就绪（但 0/27 视频有字幕） |
| 转写 | 音频切片 → **Gemini** | ✅ 60 秒音频 16.4 秒出稿，术语准确 |
| 画面 | ffmpeg 抽帧 → **多模态模型直接读图** | ✅ 已实测：能读出 PPT 标题、板书结构、手写批注、水印 |
| 汇总 | 交给 agent（读 `report.md` + `frames/`） | ✅ |

**它和 VideoToNo 的分工**：VideoToNo 强在**本地转写 + 一站式**；本脚本强在**画面理解 + 零安装**。
两者都拿不到字幕时，本脚本用云端 ASR（快），VideoToNo 用本地 ASR（慢但离线）。

### 模型选择（实测探活，别再抄旧的）

| 模型 | 结果 |
|:---|:---|
| `gemini-3.1-flash-lite` | ✅ **5.7s，最快最稳，首选** |
| `gemini-flash-lite-latest` | ✅ 5.5s |
| `gemini-3.1-flash-lite-preview` / `gemini-3-flash-preview` | ✅ 6.8s / 6.9s |
| `gemini-3.5-flash` | ✅ 11.3s |
| `gemini-3.8-flash` | ⚠️ 89.0s，极慢，放最后 |
| `gemini-flash-latest` | ❌ **503 当前不可用**（放前面每片白等 21 秒） |
| `gemini-2.5-flash` / `2.5-flash-lite` | ❌ **404 已下线** |

---

## 七、无论用哪个，这几条边界不变

1. **只做个人学习**：下载下来做笔记、转写、做错题 —— 可以。
2. **不要二次分发**：整段视频、音频、逐字稿上传到**公开仓库/Pages** = 侵犯信息网络传播权。
   本库是公开仓库 ⇒ **只放自己整理的知识点，不放源媒体与逐字稿**。
3. **不要碰付费/大会员内容**（`is_upower_exclusive` / `pay`），不要绕地区限制，不要批量扒全站。
4. **`SESSDATA` 是账号最高权限凭证**：用自己账号读自己本就能看的内容是正常的，
   但**绝不能提交进仓库**（等于把账号交出去）。VideoToNo 用 DPAPI 加密存本机，这是正确做法。
5. 各项目 README 里的免责声明都写明了「接口随时可能变、作者不承诺修复」。**依赖前先自己跑一遍。**

---

## 八、选择建议

| 你的目标 | 选它 |
|:---|:---|
| **要一站式、要省事、要中文转写质量** | **`like-attract/video-to-note`**（便携 exe，先启动再用 MCP） |
| **要平台覆盖最全（小红书/公众号/播客…）** | `chubbyguan/chubbyskills` |
| **要「像豆包那样看画面」** | `7oMB2006/Bilibili-Video-Research`（配已有 Gemini Key） |
| **只要 B站字幕+弹幕+评论，且愿意扫码登录** | `Yotsuki2213/BiliBili_VideoRead_MCP`（**先修 412 那行**） |
| **不想装任何东西、要画面理解** | 本库 `scripts/bili_analyze.py` |
