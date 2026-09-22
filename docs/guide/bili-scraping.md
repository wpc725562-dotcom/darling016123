---
title: "B站爬取笔记（实测 2026-08 / 2026-09-18 复测修订）"
description: "B站接口风控实测与换用方案 · x/web-interface/view 失效 → 改用 wbi/view（免登录免签名）"
---

# B站爬取笔记（实测 2026-08 / 2026-09-18 复测修订）

> **2026-09-18 复测：本文原第 13 行「`x/web-interface/view` ✅」已失效。**
> B站对该端点加了风控，**稳定返回 HTTP 412**（4/4 个 BV 全中，无 cookie / 带 `buvid3` cookie / 加完整浏览器头均无效）。
> 已换用 `x/web-interface/wbi/view`，**免登录免签名**，30 抽样 27 成功（3 个失败是 BV 号本身无效，返回 `code:-400`）。
> 脚本 `scripts/bili_fetch.py` 已同步修复（含 pagelist 兜底）。

## 核心结论一句话

> **B站元数据 + 播放流 + 整段视频，全部可免登录走官方 API 拿到，唯一门槛是 CDN 防盗链（必须带 Referer）。**
> **但字幕拿不到** —— 专升本类教学视频几乎不传 CC 字幕，AI 字幕需登录。**想要文字稿只能自己上 ASR。**

## 一、能力矩阵（2026-09-18 实测）

| 环节 | 端点 / 方式 | 结果 | 备注 |
|:---|:---|:---:|:---|
| 元数据 | `x/web-interface/view?bvid=` | ❌ **412** | **已失效，别再用** |
| 元数据 | `x/web-interface/wbi/view?bvid=` | ✅ 200 | **免签名**，标题/UP/分P/cid/时长/封面 |
| 分P + cid | `x/player/pagelist?bvid=` | ✅ 200 | 只需 UA，连 Referer 都不用 |
| 字幕轨 | `x/player/v2?bvid=&cid=` | ✅ 200 但**轨数 0** | 27/27 抽样无 CC 字幕 |
| 弹幕 | yt-dlp `--list-subs` | ✅ 只有 `danmaku` | 弹幕≠字幕 |
| 播放流 | `x/player/playurl?bvid=&cid=&fnval=16` | ✅ 200，DASH 全量 | 免登录 |
| 下载 m4s | 直拉流地址 **+ Referer** | ✅ 206 | **无 Referer = 403** |
| 合流 | `ffmpeg -c copy` | ✅ 11MB 可播放 mp4 | 不转码 |
| 时长校验 | ffprobe vs 元数据 | ✅ 差 0.9s | 阈值 ±5s |

### 抽样统计（仓库内 158 个 BV，取前 30）

```
wbi/view 成功 27/30  失败 3（均为 code:-400，BV 号无效，非限流）
有字幕轨 0 / 无字幕 27      ← 字幕路线的死刑判决
耗时 93.5s  平均 3.12s/条   ← 单线程 + 0.35s 间隔，有限流
```

## 二、坑（按踩到的顺序）

1. **`x/web-interface/view` 已 412** —— 老脚本会在这里直接抛 `HTTPError: 412`。换 `wbi/view`。
2. **CDN 防盗链**：流地址**不带 `Referer: https://www.bilibili.com/` 就是 403**，带了才 206。
   实测魔数：403 返回 `<HTML><HEAD><TIT`；206 返回 `00 00 00 20 66 74 79 70 69 73 6f 35`（`ftypiso5`，合法 fMP4）。
3. **别用 `api/playurl`**（无 `x/` 前缀那个），会被反爬。必须 `x/player/playurl`。
4. **分P 视频的时长**：逐 P 用 `pages[].duration` 比对，别用整体 `duration`（分P 总长 ≠ 单段音频）。
5. **`need_login_subtitle: false` ≠ 有字幕** —— 它只表示「没有需要登录才能看的字幕」，实际 `subtitles` 数组是空的。

## 三、两条路线，选一条

### 路线 A：自己写（可控、零依赖、已跑通）

```bash
# ① 一条龙：元数据 + 逐字稿 + 画面帧（推荐）
python scripts/bili_analyze.py BV号 --pages 1-3 --fpm 1

# ② 只要音频（自己接 ASR）
python scripts/bili_fetch.py BV号 [输出.m4s]

# ③ 扫码登录，拿 SESSDATA 以便跳过 ASR（可选）
python scripts/bili_login.py
```

- `bili_analyze.py`：元数据 → 字幕探测 → 命中则下字幕，否则下最小音频走 ASR → 抽帧 → 出 `report.md`。
  `--fpm` 是**每分钟**抽几帧（不是每秒，见 §二 的坑）。
- `bili_fetch.py`：只下音频，自动做 ffprobe 时长校验。
- `bili_login.py`：扫码登录，产物 `.bili-sessdata`（已 gitignore）。
- **外部依赖 = `ffprobe` + `ffmpeg`**（本机在 `D:/ACLOS/Cross/recorder-release/`，未进 PATH）。
  `bili_login.py` 需要 `qrcode` 库（仅用于画二维码，没装会退化为打印链接）。

### 路线 B：yt-dlp（省事、功能全、推荐默认）

```bash
# 列出全部格式（含 1080P）
python -m yt_dlp -F "https://www.bilibili.com/video/BV号"
# 只要最小音频
python -m yt_dlp -f 30216 -o "%(title)s.%(ext)s" "https://www.bilibili.com/video/BV号"
# 视频+音频自动合流（需 ffmpeg 在 PATH）
python -m yt_dlp -f "bv*+ba/b" --merge-output-format mp4 "URL"
```

**2026-09-18 实测**：venv 里装 `yt-dlp==2026.08.19` 即可，**无需任何配置**。
3 秒下完 3.58MiB 音频；ffprobe 校验 aac / 453.115s / 3749143B 全对。
1080P 免登录可下，只有「**1080P 高码率**」需大会员（yt-dlp 会打印提示，不影响普通 1080P）。

适用：要**视频本体**、要番剧/合集、不想维护脚本。

## 四、想要「文字稿」怎么办（关键结论）

字幕路线实测**走不通**（0/27 有 CC 字幕）。但有一个**例外通道**：

### ★ 4.1 `need_login_subtitle` —— 决定「值不值得去登录」

`x/player/v2` 返回的这个布尔值才是关键：

| 值 | 含义 | 对策 |
|:---|:---|:---|
| `false` + `subtitles: []` | **该视频根本没字幕** —— ⚠️ 前提是这次请求真的成功了，见 §4.1.1 | 死路，只能自己 ASR |
| `true` + `subtitles: []` | **有 AI 字幕，但要登录才给** | 带 `SESSDATA` 再请求即可 |

**实测两例（差别很大，别一刀切）**：
- `BV176gY6nEb3`（政治辨析题）→ `need_login_subtitle=false` → **真没字幕**，只能 ASR
- `BV117UMBXEhj`（**专升本C语言速成课 2027版，82 分P / 10.3 小时**）→ `need_login_subtitle=true`
  → **有 AI 字幕，登录就能拿** ← 这个视频直接对着考纲的 C 语言空白章

#### 4.1.1 ★ 别用一次探测就给视频判死刑 —— `subtitle_url` 会偶发为空

`x/player/v2` 有约 **20% 概率**返回「轨道列表非空、但 `subtitle_url` 是空串」，
`code` 仍是 `0`、`is_lock` 仍是 `false`。这是**瞬时状态**，同一个 `cid` 复探就能拿到。

危险在于：如果把探测包成 `try/except: return []`，那么**限流（HTTP 412）会被吞成
「这个视频没字幕」** —— 一个假的、看起来永久成立的结论。1526 个分P 的实测损失：

| 单次运行的判定 | 数量 | 复探后真相 |
|:---|:---:|:---|
| 下载失败（`unknown url type: ''`） | 271 | **241 个复探即好** |
| 有轨但 URL 空 | 65 | **65/65 在 2 轮内恢复** |
| 完全无轨 | 32 | **30/32 在 4 轮内恢复** |
| 剩下 2 个「确定无轨」 | 2 | **带重试探测后也有轨** |

⇒ 真正的 ASR 缺口是 **0 个分P**，不是 338。所以：

1. **探测函数绝不能在异常时返回 `([], False)`**。三种状态必须分开：`code:0` + 空数组 =
   真无轨；有轨但 URL 全空 = 瞬时，重试；异常 / `code != 0` = 限流或故障，重试后
   **抛异常**，由调用方计入「失败」而不是「无字幕」。
2. **「哪些视频没有字幕」无法用一次探测回答**。探 P1 拿到 `false`，就会得出
   「这条 47 小时的课要跑 ASR」—— 错的。**给负面结论留 3–4 次带抖动的重试预算。**

> 教训可以推广：**任何「把异常吞成默认值」的探测函数，都会把基础设施故障伪装成业务结论。**
> 判据要能区分「我查了，答案是没有」和「我没查成」。

`x/player/v2` 还带 `asr_language` / `ocr_language` 两个键，是 AI 字幕的语种标记。

### 4.2 三条出路

| 方案 | 可行性 | 说明 |
|:---|:---|:---|
| 扒 CC 字幕 | ❌ | 抽样 0/27，教学 UP 主基本不传 |
| **AI 字幕（登录）** | ✅ **优先试** | 用自己的 B 站账号 cookie（`SESSDATA`），只读自己有权看的内容 |
| 本地 ASR | ✅ 兜底 | 下最小音频（3.6MB/7分钟）→ 本地转写 |

**顺序建议：先看 `need_login_subtitle`，为 `true` 才值得去登录；为 `false` 直接走 ASR，别浪费时间。**

> ⚠️ 用 `SESSDATA` 是**拿自己账号的权限**读自己本来就能看的东西 —— 这是正常的。
> 但**别把它提交进仓库**（等于把账号交出去），也别拿它去碰付费/大会员内容。

#### 怎么拿 `SESSDATA`：扫码，30 秒

别去 DevTools 里手抄 cookie（容易抄错、抄漏，也容易顺手贴进聊天记录）。用官方扫码接口：

```bash
python scripts/bili_login.py                 # 终端直接出二维码，用「哔哩哔哩」App 扫
python scripts/bili_login.py --html qr.html  # 终端乱码时落一份网页版二维码
python scripts/bili_login.py --verify        # 事后校验存下来的 SESSDATA 还有没有效
```

成功后写入仓库根 `.bili-sessdata`（已被 `.gitignore` 挡掉）。之后 `bili_analyze.py` 会自动读取，
`need_login_subtitle=true` 的视频就能**直接下现成字幕、跳过 ASR**。

读取优先级：`--sessdata` 参数 > 环境变量 `BILI_SESSDATA` > `./.bili-sessdata` > `~/.bili-sessdata`。

> 实测记录（2026-09-18）：二维码生成接口 `x/passport-login/web/qrcode/generate` 正常返回
> `qrcode_key`(32 位) + 跳转 URL；轮询接口内层状态码为 `86101` 未扫码 / `86090` 已扫码待确认 /
> `86038` 已失效 / `0` 成功。**扫码那一步需要手机，脚本作者无法代跑** —— 该环节属未实测。

### 4.3 下音频比下视频划算

7 分钟视频：音频 3.6MB / 视频 6.6MB（合流后 11MB）。**转写只需要音频**。

## 五、边界（必须知道）

- **自己看 / 自己学** → 可以。下载下来做笔记、转文字、做错题，属于个人使用。
- **传到公开站** → 不行。整段视频、整篇文字稿上传到公开仓库/Pages，是**侵犯信息网络传播权**。
  本站是公开仓库 ⇒ **只放「自己整理的知识点」，不放原文/原视频/原字幕**。
- 别碰**付费课程**（`is_upower_exclusive` / `pay` 为真）、别绕**地区限制**、别做**批量扒全站**。
- 请求间隔 ≥0.35s，别打人家接口。抽样 30 条耗时 93.5s，已经是温和速度。

## 六、GitHub 可选项（2026-09-18 核实的活跃度）

| 项目 | Stars | 状态 | 许可 | 说明 |
|:---|---:|:---|:---|:---|
| `yt-dlp/yt-dlp` | 191837 | ✅ 活跃 | Unlicense | **首选**。已实测跑通，B站 extractor 内置 |
| `the1812/Bilibili-Evolved` | 30507 | ✅ 活跃 | NOASSERTION | 油猴脚本，网页端增强（非下载器） |
| `nexmoe/VidBee` | 10658 | ✅ 活跃 | MIT | 通用视频下载 |
| `ScottSloan/Bili23-Downloader` | 7504 | ✅ 活跃 | GPL-3.0 | GUI，B站专用，功能全 |
| `lanyeeee/bilibili-video-downloader` | 2051 | ✅ 活跃 | MIT | 轻量 GUI |
| `nilaoda/BBDown` | 13881 | ⚠️ **已归档** | MIT | 2026-05-14 归档，内容已删。**别用** |
| `LOVAHE/BBDownT` | 40 | ✅ 活跃 | MIT | BBDown 接手方，功能全但社区小 |
| `crazysmile-PhD/downkyicore` | 329 | ✅ 活跃 | GPL-3.0 | 跨平台 GUI（.NET） |
| `SocialSisterYi/bilibili-API-collect` | 20215 | ⚠️ 已归档 | 无 | API 文档，2026-01 停更 |

> **结论：不用装第三方 B 站下载器。`yt-dlp` 一个就够，且是唯一实测跑通的。**

## 七、本机现状

- `ffmpeg` / `ffprobe`：**不在 PATH**，实现在 `D:/ACLOS/Cross/recorder-release/`（n5.1.3）。
  临时用：`export PATH="/d/ACLOS/Cross/recorder-release:$PATH"`
- `yt-dlp`：装在隔离 venv `~/.workbuddy-ai/binaries/python/envs/default/`，
  调用 `~/.workbuddy-ai/binaries/python/envs/default/Scripts/python.exe -m yt_dlp`
- `qrcode`：同一个 venv 里（`qrcode 8.2`），仅供 `bili_login.py` 画二维码。**系统 python 没装**，
  所以扫码登录要用 venv 的 python 跑：
  `~/.workbuddy-ai/binaries/python/envs/default/Scripts/python.exe scripts/bili_login.py`
  （用系统 python 跑也行，只是终端不出图，会退化成打印链接）
- `winget` 可用，需要的话可 `winget install Gyan.FFmpeg` 把 ffmpeg 装进 PATH。

## 八、其他

- B站教学视频大多**无官方 chapters**，转写后按文本结构拆章仍是正确兜底。
- 本机到部分中国站点（百度/知乎/文库）出口被限，GitHub/B站 可达 —— 资源优先走这两通道。
