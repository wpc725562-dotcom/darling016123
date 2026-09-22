#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B站视频「解析」流水线 —— 像豆包那样：给个 BV 号，出结构化解析材料。

    python scripts/bili_analyze.py BV号 [选项]

选项:
    --pages 1-3          只处理第 1~3 个分P（默认全部）
    --chunk 300          音频切片秒数，每片一次 ASR（默认 300）
    --fpm 1              ★ 每分钟抽几帧（默认 1）。讲 PPT 的课 1 够，实操演示调 2~3。
                         （注意不是「每秒」—— ffmpeg 的 fps 滤镜单位是秒，
                          本脚本内部换算成 fps=N/60，所以 1 分钟 1 帧就是 1/60）
    --out DIR            输出目录（默认 data/bili-analyze/<BV>）
    --no-video           只转写音频，不抽帧（省流量、快）

产出（都在 --out 目录）:
    audio/p01.m4s ...    每个分P的音频
    frames/p01_0001.jpg  抽出的画面帧（供多模态模型读取）
    transcript.md        带时间戳的逐字稿
    report.md            ★ 给模型看的解析材料：元数据 + 逐字稿 + 帧清单

设计要点（都是踩过的坑，别改）:
  * 元数据用 x/web-interface/wbi/view —— x/web-interface/view 已被风控稳定 412
  * 流地址必须带 Referer: https://www.bilibili.com/ ，否则 CDN 返 403（且返的是 HTML）
  * 优先取 B站 AI 字幕（need_login_subtitle=true 时才存在），拿不到才走 ASR
  * 零第三方依赖：只用标准库 + ffmpeg + ffprobe
"""
import argparse, base64, json, os, pathlib, random, re, subprocess, sys, time, urllib.request

# ★ A5 残留（2026-09-20）：本文件的 ffmpeg / ffprobe 调用原先没有 timeout ——
#   外部命令一旦挂住（网络源损坏、编解码器卡死），脚本就永远不返回。
#   长视频转码确实要几分钟，所以上限给宽一点，并允许用环境变量覆盖。
SUBPROC_TIMEOUT = int(os.environ.get("ZHENTI_SUBPROC_TIMEOUT", "600"))

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
REFERER = "https://www.bilibili.com/"

# ---- 字幕探测的性能旋钮（详见 probe_subtitle 的注释与 scripts/bili_bench.py）----
# B站 x/player/v2 会随机返回**别的视频**的字幕轨，正确轨的 URL 里含 aid+cid。
# 命中率约 20%，所以「重试」是必需的；但命中率为 0 的分P 会白跑满 retries 次，
# 这是整套流程里最大的单项浪费。这两个常量就是用来压这个尾巴的。
# ★ 2026-09-19 改默认值：原先优化只以 CLI 参数形式存在，默认值仍是慢的那套，
#   结果「不带参数跑 = 等于没优化」，实测慢 12.4 倍（bili_bench_retry.py）。
#   现在默认走快路径。要退回保守值：--probe-retries 40 --probe-sleep 0.3,0.8
PROBE_RETRIES = 12      # 原 40。12 = 尾巴快 3.3 倍；漏掉的分P 靠下一轮 --refresh 补
PROBE_SLEEP = (0.05, 0.15)   # 原 (0.3, 0.8)。实测 jobs<=24 从未触发 412，原 sleep 是纯浪费

# ---------------------------------------------------------------- 基础设施

def find_tool(name):
    """ffmpeg/ffprobe 常常不在 PATH 上，兜底去几个常见捆绑目录找。"""
    from shutil import which
    p = which(name)
    if p:
        return p
    for c in (r"D:/ACLOS/Cross/recorder-release", r"C:/ffmpeg/bin",
              r"C:/Program Files/ffmpeg/bin", os.path.expanduser("~/scoop/shims")):
        exe = pathlib.Path(c) / (name + (".exe" if os.name == "nt" else ""))
        if exe.exists():
            return str(exe)
    return None


FFMPEG = find_tool("ffmpeg")
FFPROBE = find_tool("ffprobe")


def get_key():
    """按优先级找 Gemini key：环境变量 → reasonix 的 .env。"""
    for k in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if os.environ.get(k):
            return os.environ[k]
    for c in (pathlib.Path(os.environ.get("APPDATA", "")) / "reasonix/.env",
              pathlib.Path.home() / ".env"):
        if c.exists():
            m = re.search(r'^GEMINI_API_KEY\s*=\s*(.+)$',
                          c.read_text(encoding="utf-8", errors="ignore"), re.M)
            if m:
                return m.group(1).strip().strip('"').strip("'")
    return None


# ★ B站登录态。有它才能取到「AI 字幕」（need_login_subtitle=True 的那类）。
#   优先级：--sessdata 参数 > 环境变量 BILI_SESSDATA > 同目录 .bili-sessdata 文件
#   ⚠️ 绝不提交进仓库：这是账号最高权限凭证，泄露等于把账号交出去。
COOKIE = ""


def get_sessdata(cli_value=None):
    """找 SESSDATA。返回 (值, 来源说明)。"""
    if cli_value:
        return cli_value, "--sessdata 参数"
    if os.environ.get("BILI_SESSDATA"):
        return os.environ["BILI_SESSDATA"], "环境变量 BILI_SESSDATA"
    for c in (pathlib.Path(".bili-sessdata"), pathlib.Path.home() / ".bili-sessdata"):
        if c.exists():
            v = c.read_text(encoding="utf-8", errors="ignore").strip()
            if v:
                return v, f"文件 {c}"
    return None, ""


def api(url, timeout=30, cookie=None):
    h = {"User-Agent": UA, "Referer": REFERER}
    ck = cookie if cookie is not None else COOKIE
    if ck:
        h["Cookie"] = f"SESSDATA={ck}"
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _open_stream(url, headers, timeout, offset=None):
    h = dict(headers)
    if offset:
        h["Range"] = f"bytes={offset}-"
    return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=timeout)


def download(urls, path, timeout=300, retries=3):
    """把音频/视频流下到 path，返回收到的字节数。

    ★★ 2026-09-22 修（两个叠加的静默缺陷）：

    1. **短读被当成读完了**。原实现 `while True: c = r.read(...); if not c: break`
       无法区分「服务端提前断开」与「正常读完」⇒ 静默留下截断文件。而 B站 m4s 的
       容器头仍写着完整时长，`ffprobe format=duration` 也报完整 ⇒ 一路绿灯，
       直到切片时后半段全空才发现。实测 p71 声明 3563s、实际只有 1561s（44%）。

    2. **只赌一个 URL**。同一段音频有 baseUrl + backupUrl[] 多个镜像，实测**不同
       CDN 节点截断位置不同**（P124：baseUrl 97%、backupUrl 7%）⇒ 必须轮换镜像。

    现在：按 Content-Length 校验 → 缺尾巴就用 HTTP Range 续传补齐 → 不行换下一个
    镜像 → 全都不行就取最长的一份并**显式告警**（绝不静默交半截文件）。
    """
    if isinstance(urls, str):
        urls = [urls]
    h = {"User-Agent": UA, "Referer": REFERER}
    if COOKIE:
        h["Cookie"] = f"SESSDATA={COOKIE}"
    best_n, best_u = 0, None
    for attempt in range(1, retries + 1):
        for u in urls:
            expect, n = None, 0
            try:
                with _open_stream(u, h, timeout) as r, open(path, "wb") as f:
                    cl = r.headers.get("Content-Length")
                    if cl and str(cl).strip().isdigit():
                        expect = int(cl)
                    while True:
                        c = r.read(1 << 20)
                        if not c:
                            break
                        f.write(c)
                        n += len(c)
            except Exception as e:                                # noqa: BLE001
                print(f"  [warn] 下载异常（{e}），换源重试 {attempt}/{retries}")
                continue
            # 缺尾巴 ⇒ 用 Range 续传补齐（B站支持 Range）
            if expect and n < expect:
                try:
                    with _open_stream(u, h, timeout, offset=n) as r2, open(path, "ab") as f2:
                        while True:
                            c = r2.read(1 << 20)
                            if not c:
                                break
                            f2.write(c)
                            n += len(c)
                except Exception as e:                            # noqa: BLE001
                    print(f"  [warn] Range 续传失败（{e}）")
            if n > best_n:
                best_n, best_u = n, u
            if expect is None or n >= expect:
                return best_n
            print(f"  [warn] 下载不完整（{n}/{expect} 字节，{100*n/expect:.0f}%），换源重试")
    print(f"  [warn] !! 全部镜像都不完整，取最长的一份：{best_n} 字节（{best_u}）"
          f"—— 后半段内容拿不到，请重跑")
    return best_n


def ffprobe_dur(path):
    """容器**声明**时长。★ 注意：对截断文件它会谎报完整 —— 要判「数据够不够」用 decoded_dur()。"""
    if not FFPROBE:
        return None
    o = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
                       capture_output=True, text=True,
                       timeout=SUBPROC_TIMEOUT).stdout.strip()
    try:
        return float(o)
    except ValueError:
        return None


def decoded_dur(path):
    """★ 2026-09-22 新增：**真实可解码**时长。

    `ffprobe format=duration` 读的是容器头，截断文件照样报完整（实测 p71：头里 3562.7s，
    实际只有 1561s）。只有把流解一遍才知道到底有多少数据 —— 这是判「下载是否完整」的
    唯一可靠判据。
    """
    if not FFMPEG:
        return None
    try:
        r = subprocess.run([FFMPEG, "-i", str(path), "-f", "null", "-"],
                           capture_output=True, text=True, timeout=SUBPROC_TIMEOUT)
    except Exception:                                             # noqa: BLE001
        return None
    hits = re.findall(r"time=(\d+):(\d\d):(\d\d(?:\.\d+)?)", r.stderr or "")
    if not hits:
        return None
    hh, mm, ss = hits[-1]
    return int(hh) * 3600 + int(mm) * 60 + float(ss)


# ---------------------------------------------------------------- B站取数

def _data(d, what):
    """取 data 字段；code 非 0 时抛出人话错误，而不是 KeyError: 'data'。

    ★ B站「稿件不可见」= code 62002（视频被删/转私密/过审撤回）。
      这种情况直接抛 KeyError 会让调用方以为是自己代码坏了，其实数据是对的。
    """
    if d.get("code") != 0:
        raise RuntimeError(
            f"{what} 失败：code={d.get('code')} {d.get('message')}"
            + ("（稿件不可见 = 视频已下架/转私密，换一个源）"
               if d.get("code") == 62002 else ""))
    if "data" not in d:
        raise RuntimeError(f"{what} 返回体缺 data 字段（接口结构可能变了）")
    return d["data"]


_UNLINK_WARNED = False


def try_unlink(p):
    """删临时文件；删不掉只警告，**绝不中断整轮任务**。

    ★ 真实事故（2026-09-18）：沙箱的安全删除拦截在跑到第 50 次删除时触发
      `SAFE_DELETE_BULK_CONFIRM_REQUIRED`，脚本当场抛异常退出 —— 已经转写完的
      分P 全白费。删临时文件只是省磁盘，不该有这种权力。
    """
    global _UNLINK_WARNED
    try:
        pathlib.Path(p).unlink(missing_ok=True)
    except OSError as e:
        if not _UNLINK_WARNED:
            _UNLINK_WARNED = True
            print(f"  (提示) 临时文件删不掉，不影响结果：{type(e).__name__}: {e}")


def get_meta(bvid):
    d = _data(api(f"https://api.bilibili.com/x/web-interface/wbi/view?bvid={bvid}"),
              f"取 {bvid} 元数据")
    pages = [{"cid": p["cid"], "page": p["page"], "part": p["part"],
              "duration": p["duration"]} for p in d.get("pages", [])]
    return {"bvid": bvid, "title": d["title"], "owner": d["owner"]["name"],
            "desc": (d.get("desc") or "").strip(), "pages": pages,
            "total": d.get("duration", 0)}


def pick_streams(cid, bvid):
    """返回 (音频URL列表, 视频URL列表)。视频可缺。

    ★ 2026-09-22：改成返回**列表**（baseUrl + backupUrl[]）。实测不同 CDN 节点
    截断位置不同，只取 baseUrl 会静默丢后半段音频。
    """
    d = _data(api(f"https://api.bilibili.com/x/player/playurl"
                  f"?bvid={bvid}&cid={cid}&fnval=16&fnver=0&fourk=1"),
              "取播放流地址")
    dash = d.get("dash") or {}
    au = sorted(dash.get("audio") or [], key=lambda x: x.get("bandwidth") or 0)
    vi = sorted(dash.get("video") or [], key=lambda x: x.get("bandwidth") or 0)
    def _urls(x):
        if not x:
            return []
        return [u for u in [x[0].get("baseUrl")] + list(x[0].get("backupUrl") or []) if u]

    return _urls(au), _urls(vi), dash.get("duration")


def probe_subtitle(cid, bvid, retries=None):
    """返回 (字幕轨列表, need_login_subtitle)。★ 判据是这个布尔值，不是空数组。

    ★ 调参入口（性能相关，改前先看 scripts/bili_bench.py 的实测）：
        PROBE_RETRIES      默认 40。命中率约 20% 时，40 次能到 99.9% 把握；
                           但**命中率为 0 的分P 会白跑满 40 次**，实测占「难命中」
                           视频 88% 的耗时。降到 12 次可让尾巴快 3.3 倍，
                           漏掉的分P 留给下一轮 --refresh 补。
        PROBE_SLEEP        默认 (0.3, 0.8) 秒的抖动。实测 jobs=6 时**没有触发 412**，
                           所以这个 sleep 是纯浪费；降到 (0.05, 0.15) 可让重试快 4 倍。

    带 SESSDATA 时才能拿到 need_login_subtitle=True 那类 AI 字幕。

    ★★★ 2026-09-18 第三次修复 —— 前两次都只治了症状，这次才是根因。

    根因：**B站 `x/player/v2` 会返回不属于这个 cid 的字幕轨。**
        同一个 cid 连请求 5 次，`subtitles[0].subtitle_url` 的哈希段**每次都不同**，
        内容分别是火锅探店、篮球解说、iPhone 评测、音乐纯响……只有偶尔一次是对的。
        实测命中率约 15–25%。更坏的是 `code` 恒为 0、`lan` 恒为 `ai-zh`，
        所以**从响应本身完全看不出异常** —— 只有下载下来读内容才发现。

    判据（已验证）：正确轨的 URL 路径 = `prod/{aid}{cid}{hash}`，
        而 `aid` / `cid` 就在同一响应的 `data.aid` / `data.cid` 里。
        所以「URL 里含 `str(aid)+str(cid)`」是可校验的不变量。
        抽 8 个 cid 实测：凡是满足该不变量的轨，内容全部与视频主题一致。

    为什么之前没发现：前两次修复只处理了「空数组 / 空 URL」，而这两种情况
    恰恰是**少数**；大量错误轨是「非空、格式合法、内容完全是别的视频」。

    语义（调用方必须区分）：
      · 命中 aid+cid 不变量        → 返回该轨（唯一可信的「有字幕」）
      · 40 次都没有匹配轨，但有轨   → 返回最后一次拿到的轨（**不可信**，调用方应校验内容）
      · 40 次都是空数组            → 真无轨，返回 ([], need)
      · 全是异常 / code!=0         → raise，调用方计入「失败」而非「无字幕」
    """
    if retries is None:
        retries = PROBE_RETRIES
    lo, hi = PROBE_SLEEP
    last = None
    need = False
    last_was_empty = False
    best_unverified = None       # 有轨但不满足不变量 —— 兜底，标记为不可信
    for attempt in range(retries):
        try:
            # ★★★ 2026-09-19 第四次修复 —— 换端点，这才是根因。
            #
            #   `x/player/v2`（非 wbi 版）返回的字幕轨**基本是坏的**：
            #     实测同一 cid 连打 15 次，只有 5 次命中 aid+cid 不变量，
            #     其余 10 次是别家视频（火锅探店 / 装机 / 明星八卦）。
            #   换成 `x/player/wbi/v2` 后，同一 cid 连打 20 次 **20/20 命中**。
            #
            #   更关键的是「无字幕」这个判断也终于可信了：
            #     · 有轨的视频  → wbi/v2 稳定返回该轨（100%）
            #     · 真无轨的视频 → wbi/v2 稳定返回空数组（19/19、20/20 全空）
            #   而非 wbi 版在「真无轨」时会**凭空编一条别家视频的轨**出来，
            #   于是「无字幕」被误判成「有字幕但串轨」，白白触发昂贵的 ASR。
            #
            #   aid+cid 不变量仍然保留 —— 它现在是安全网，不再是主要判据。
            d = api(f"https://api.bilibili.com/x/player/wbi/v2?bvid={bvid}&cid={cid}")
            if d.get("code") != 0:
                last = RuntimeError("api code=%s msg=%s"
                                    % (d.get("code"), d.get("message")))
                last_was_empty = False
                time.sleep(lo + random.random() * (hi - lo))
                continue
            data = d.get("data") or {}
            st = data.get("subtitle") or {}
            subs = st.get("subtitles") or []
            need = bool(data.get("need_login_subtitle"))

            if not subs:
                last = RuntimeError("subtitles 为空（第 %d 次）" % (attempt + 1))
                last_was_empty = True
                time.sleep(lo + random.random() * (hi - lo))
                continue

            # ★ 核心判据：正确轨的路径里含 aid+cid
            aid, real_cid = data.get("aid"), data.get("cid")
            key = ("%s%s" % (aid, real_cid)) if (aid and real_cid) else None
            if key:
                matched = [s for s in subs
                           if key in (s.get("subtitle_url") or s.get("subtitleUrl") or "")]
                if matched and any((s.get("subtitle_url") or s.get("subtitleUrl"))
                                   for s in matched):
                    for s in matched:
                        s["_verified"] = True     # 通过 aid+cid 不变量校验
                    return matched, need
                if best_unverified is None:
                    best_unverified = subs
                last = RuntimeError("第 %d 次：%d 轨均不含 aid+cid=%s"
                                    % (attempt + 1, len(subs), key))
                last_was_empty = False
                time.sleep(lo + random.random() * (hi - lo))
                continue

            # 拿不到 aid/cid 时退回旧判据（URL 非空即用）
            if any((s.get("subtitle_url") or s.get("subtitleUrl")) for s in subs):
                for s in subs:
                    s["_verified"] = False
                return subs, need
            last = RuntimeError("tracks=%d 但 subtitle_url 全为空" % len(subs))
            last_was_empty = False
            time.sleep(lo + random.random() * (hi - lo))
        except Exception as e:           # HTTP 412 限流、超时、JSON 解析失败…
            last = e
            last_was_empty = False
            time.sleep(lo + random.random() * (hi - lo))

    if best_unverified is not None:
        for s in best_unverified:
            s["_verified"] = False
        return best_unverified, need     # ⚠️ 不可信，调用方必须校验内容
    if last_was_empty:
        return [], need                  # 反复确认为空 —— 这才是「真无轨」
    raise last if last else RuntimeError("probe_subtitle 失败且无异常信息")


# ---------------------------------------------------------------- ASR

ASR_MODELS = ["gemini-3.1-flash-lite", "gemini-flash-lite-latest",
              "gemini-3.1-flash-lite-preview", "gemini-3-flash-preview",
              "gemini-3.5-flash", "gemini-3.8-flash"]

# ★ 2026-09-21 加速项 1：**模型探测结果进程内记忆**。
#   原先每个 chunk 都从 ASR_MODELS 头部开始试；一旦头部模型临时 503/404，
#   每片都要白等一轮（gemini-flash-latest 那次实测每 chunk 白等 21s）。
#   现在第一个成功的模型会被记住并提到队首，后续 chunk 直接命中。
#   ★ 注意：**只在进程内有效**（不落盘）—— 落盘会把「临时故障」固化成长期配置。
_ASR_MODEL_CACHE: list[str] | None = None

ASR_MIME = {"wav": "audio/wav", "aac32": "audio/aac"}


def gemini_asr(wav, key, lang="zh", models=None, mime="audio/wav", remember=True):
    """把音频交给 Gemini 转写。返回 (文本, 用的模型)。

    模型顺序是 2026-09-18 实测排出来的（探活 30s 片段）：
      gemini-3.1-flash-lite    5.7s  ✅ 最快，默认首选
      gemini-flash-lite-latest 5.5s  ✅
      gemini-3.1-flash-lite-preview 6.8s ✅
      gemini-3-flash-preview   6.9s  ✅
      gemini-3.5-flash        11.3s  ✅ 稍慢
      gemini-3.8-flash        89.0s  ⚠️ 极慢，放最后
      gemini-flash-latest      503   ❌ 当前不可用（别放前面，每 chunk 白等 21s）
      gemini-2.5-flash / 2.5-flash-lite  404  ❌ 已下线
    """
    global _ASR_MODEL_CACHE
    if models is None:
        models = list(_ASR_MODEL_CACHE or ASR_MODELS)
    b64 = base64.b64encode(pathlib.Path(wav).read_bytes()).decode()
    body = {"contents": [{"parts": [
        {"text": f"这是一段中文教学视频的音频。请逐字转写为简体中文文本，"
                 f"保留专业术语原样，不要任何解释、不要加标题、不要做总结。"},
        {"inline_data": {"mime_type": mime, "data": b64}}]}]}
    last = ""
    for name in models:
        url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
               f"{name}:generateContent?key={key}")
        for attempt in (1, 2):
            req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=300) as r:
                    d = json.loads(r.read().decode())
                if remember:
                    # 命中者提到队首，其余保持原序做兜底
                    _ASR_MODEL_CACHE = [name] + [m for m in ASR_MODELS if m != name]
                return d["candidates"][0]["content"]["parts"][0]["text"].strip(), name
            except urllib.error.HTTPError as e:
                last = f"HTTP {e.code}"
                if e.code in (503, 429) and attempt == 1:
                    time.sleep(4)
                    continue
                break
            except Exception as e:
                last = f"{type(e).__name__}: {e}"
                break
    raise RuntimeError(f"ASR 全部模型失败（最后错误 {last}）")


def slice_and_transcribe(raw, audio_dir, tag, chunk, act, key,
                         codec="wav", log=print, jobs=1):
    """切片 + 逐片 ASR，**带断点续跑**。返回 (转写文本, 统计 dict)。

    ★ 2026-09-21 加速项 2：**断点续跑**。
      原先每片转写完就 `try_unlink(seg)`，跑完 12 片什么都没留下 ——
      第 11 片网络抖动挂掉，重跑要从第 1 片重新烧 API 额度。
      现在把每片结果落 `{tag}_seg{i:02d}.txt`（几十 KB），重跑时直接复用。
      删掉这些 .txt 即等价于旧行为（`--asr-redo`）。

    ★ 加速项 3：`codec="aac32"` 用 32 kbps AAC 上传（体积 7.5× 小）。
      实测（同段 120s）：wav 5.12 MB/10.3s vs aac32 0.68 MB/6.1s ⇒ **快约 2×**。
      代价：转写文本比 wav 少约 8%（wav 自身两次抖动约 5%）⇒ **默认仍用 wav**，
      只在「先粗筛一遍」的场景显式开 `--asr-codec aac32`。

    ★ 加速项 4（**未采用，附否证**）：并发上传**不会更快**。
      实测 4 片 120s 音频：串行 76.5s vs 4 路并发 70.5s（1.1×），
      且并发下单片延迟从 12–15s 涨到 23–70s ⇒ 瓶颈在服务端/上行带宽，
      不在客户端排队。故 `jobs` 默认 1，>1 时只打印告警。
    """
    if jobs > 1:
        log(f"  [warn] --asr-jobs={jobs} 实测无收益（1.1×），且会拉高单次失败率；"
            f"建议保持 1")
    n = max(1, int((act or 0) // chunk) + 1)
    ext = "aac" if codec == "aac32" else "wav"
    mime = ASR_MIME.get(codec, "audio/wav")
    parts, reused, fresh = [], 0, 0
    for i in range(n):
        seg = audio_dir / f"{tag}_seg{i:02d}.{ext}"
        txtfile = audio_dir / f"{tag}_seg{i:02d}.txt"
        ss = i * chunk
        if txtfile.exists() and txtfile.stat().st_size > 0:
            txt = txtfile.read_text(encoding="utf-8")
            parts.append(f"[{ss//60:02d}:{ss%60:02d}] {txt}")
            reused += 1
            log(f"    seg{i:02d} 复用缓存（{len(txt)} 字）")
            continue
        enc = (["-c:a", "aac", "-b:a", "32k"] if codec == "aac32"
               else ["-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le"])
        if codec != "aac32":
            enc = ["-ar", "16000", "-ac", "1"] + enc
        try:
            subprocess.run([FFMPEG, "-y", "-v", "error", "-ss", str(ss),
                            "-t", str(chunk), "-i", str(raw)] + enc + [str(seg)],
                           check=True, timeout=SUBPROC_TIMEOUT)
        except Exception as e:                                  # noqa: BLE001
            log(f"    seg{i:02d} 切片失败：{e}")
            continue
        if seg.stat().st_size < 2000:
            # ★ 2026-09-22：原来这里**静默** continue，于是「音频被截断 ⇒ 后半段切不出内容」
            #   表现为「transcript 莫名其妙短了一截」而毫无提示。必须留痕。
            log(f"    seg{i:02d} ({ss//60:02d}:{ss%60:02d}) 空切片（{seg.stat().st_size} B）"
                f"—— 音频在该时间点已无数据？")
            try_unlink(seg)
            continue
        t0 = time.time()
        try:
            txt, used = gemini_asr(seg, key, mime=mime)
        except Exception as e:                                  # noqa: BLE001
            log(f"    seg{i:02d} 转写失败: {e}")
            try_unlink(seg)
            continue
        txtfile.write_text(txt, encoding="utf-8", newline="\n")
        parts.append(f"[{ss//60:02d}:{ss%60:02d}] {txt}")
        fresh += 1
        log(f"    seg{i:02d} ({ss//60:02d}:{ss%60:02d}) "
            f"{len(txt)} 字  {time.time()-t0:.1f}s  via {used}")
        try_unlink(seg)
    return ("\n\n".join(parts) if parts else "(转写失败)"), {"reused": reused, "fresh": fresh, "total": n}


def srt_to_text(url):
    """B站字幕 JSON → 纯文本。"""
    d = api(url)
    return "\n".join(x.get("content", "").strip()
                     for x in d.get("body", []) if x.get("content"))


def srt_to_timed_text(url):
    """B站字幕 JSON → 带时间戳的纯文本，每行 `[MM:SS] 内容`。

    ★ 为什么必须另开一个函数而不是改 srt_to_text：
      srt_to_text 的输出已经被 24 个既有产物（data/bili-analyze/）引用，
      改它会静默改变下游所有比对结果。
      而真题解析要求「出处是硬要求」—— 每张真题卡都要能指回**哪一秒**，
      所以这条链路必须保留 from 字段。

    ★ B站字幕的 body 元素长这样（单位：秒，浮点）：
        {"from": 12.345, "to": 15.678, "content": "第一题", "sid": 1, ...}
      `from` 缺省或为 0 时也要输出，不能因为 0 被 falsy 判断吞掉。
    """
    d = api(url)
    out = []
    for x in d.get("body", []):
        txt = (x.get("content") or "").strip()
        if not txt:
            continue
        try:
            sec = int(float(x.get("from") or 0))
        except (TypeError, ValueError):
            sec = 0
        out.append("[%02d:%02d] %s" % (sec // 60, sec % 60, txt))
    return "\n".join(out)


# ---------------------------------------------------------------- 主流程

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bvid")
    ap.add_argument("--pages", default=None, help="如 1-3、或 13,16,18、或 13-18,80；默认全部")
    ap.add_argument("--chunk", type=int, default=300)
    ap.add_argument("--asr-codec", choices=["wav", "aac32"], default="wav",
                    help="ASR 上传编码。wav=无损（默认，逐字稿保真优先）；"
                         "aac32=32kbps AAC，上传体积小 7.5×、实测端到端快约 2×，"
                         "但转写文本比 wav 少约 8%%（wav 自身两次抖动约 5%%）。"
                         "只在「先粗筛一遍」时用。")
    ap.add_argument("--asr-jobs", type=int, default=1,
                    help="ASR 并发数。★ 实测并发**无收益**（4 片 120s：串行 76.5s vs "
                         "4 路 70.5s），瓶颈在服务端与上行带宽；默认 1，别调大。")
    ap.add_argument("--fpm", type=float, default=1.0,
                    help="每分钟抽几帧（默认 1）。注意单位是「分钟」不是「秒」")
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-video", action="store_true")
    ap.add_argument("--no-asr", action="store_true",
                    help="跳过 Gemini ASR，只取画面帧。"
                         "用途：ASR 依赖 Google API，网络不通时会长时间挂起"
                         "（实测 WinError 10060 / 连接超时）；此时仍可用画面帧取证。"
                         "配合 --fpm 控制帧密度。")
    ap.add_argument("--sessdata", default=None,
                    help="B站 SESSDATA（登录态），有它才能取 AI 字幕。"
                         "也可用环境变量 BILI_SESSDATA 或 .bili-sessdata 文件。⚠️ 别提交进仓库")
    a = ap.parse_args()

    global COOKIE
    COOKIE, src = get_sessdata(a.sessdata)

    if not FFMPEG:
        print("!! 找不到 ffmpeg，无法切片/抽帧。装一个或把它加进 PATH。")
        return 1
    key = get_key()
    if not key and not a.no_asr:
        print("!! 找不到 GEMINI_API_KEY（环境变量或 reasonix 的 .env）。"
              "若只想取画面帧，加 --no-asr。")
        return 1

    try:
        m = get_meta(a.bvid)
    except RuntimeError as e:
        print(f"!! {e}")
        return 2
    out = pathlib.Path(a.out or f"data/bili-analyze/{a.bvid}")
    (out / "audio").mkdir(parents=True, exist_ok=True)
    (out / "frames").mkdir(parents=True, exist_ok=True)

    pages = m["pages"]
    if a.pages:
        # ★ 2026-09-22：支持逗号列表（如 13,16,18 或 13-18,80），原来只认单段 lo-hi，
        #   想取几个不连续的分P 就得整段跑，白下载中间那些不需要的分P。
        want: set[int] = set()
        for chunk in a.pages.split(","):
            chunk = chunk.strip()
            if not chunk:
                continue
            lo, _, hi = chunk.partition("-")
            want.update(range(int(lo), int(hi or lo) + 1))
        pages = [p for p in pages if p["page"] in want]

    print(f"标题: {m['title']}")
    print(f"UP: {m['owner']}  |  分P: {len(m['pages'])}  处理: {len(pages)}  "
          f"|  总时长: {m['total']}s")
    print(f"输出: {out}\n")

    sections = []
    for p in pages:
        tag = f"p{p['page']:02d}"
        print(f"--- 第 {p['page']} P: {p['part']} ({p['duration']}s) ---")

        try:
            subs, need_login = probe_subtitle(p["cid"], a.bvid)
        except Exception as e:
            # ★ 别把限流当成「无字幕」——那会白白多跑一路 ASR。
            print(f"  !! 探字幕轨失败（不是「没字幕」）：{e}")
            subs, need_login = [], False
        text = None
        if subs:
            # 有 CC 字幕 → 直接拿，不用 ASR
            url = subs[0].get("subtitle_url") or subs[0].get("subtitleUrl")
            if url:
                if url.startswith("//"):
                    url = "https:" + url
                try:
                    text = srt_to_text(url)
                    print(f"  字幕: 命中 {len(subs)} 轨（{subs[0].get('lan_doc')}），免 ASR")
                except Exception as e:
                    print(f"  字幕: 抓取失败 {e}，回落 ASR")
        if text is None and not subs:
            # ★ 三种情况要分开说，否则「传了失效 SESSDATA」会被误报成「没传」
            if need_login and COOKIE:
                print("  字幕: 需登录的 AI 字幕未取到 —— SESSDATA 多半已失效，本次走 ASR")
            elif need_login:
                print("  字幕: 存在 AI 字幕但需登录 —— 本次走 ASR"
                      "（扫码登录可免 ASR：python scripts/bili_login.py）")
            else:
                print("  字幕: 该视频无字幕轨 —— 直接走 ASR")

        au_url, vi_url, _ = pick_streams(p["cid"], a.bvid)   # 两者都是 URL 列表
        # ★ 无音轨的投稿（纯画面 / 无声讲解）**不应整P跳过** —— 抽帧只要视频流。
        #   旧写法 `if not au_url: continue` 会把「有视频流、无音频流」的源整个丢掉；
        #   而且下面 f"{act:.1f}" 在 act=None 时抛 TypeError，且崩在写 transcript 之前 ⇒ 画面全丢。
        if not au_url and not vi_url:
            print("  跳过：无音频流、也无视频流"); continue
        if not au_url:
            print("  音频: 无音轨 —— 继续处理（画面帧不受影响）")

        act = None
        if au_url:
            raw = out / "audio" / f"{tag}.m4s"
            size = download(au_url, raw)
            act, dec = ffprobe_dur(raw), decoded_dur(raw)
            # ★ 2026-09-22：容器头会谎报完整 ⇒ 用实测可解码时长复核，不一致就重下一次。
            for _try in range(2):
                if act and dec and dec + 5 < act:
                    print(f"  !! 音频截断：容器声明 {act:.0f}s，实际可解码 {dec:.0f}s"
                          f"（{100*dec/act:.0f}%）—— 第 {_try+1} 次重下")
                    size = download(au_url, raw)
                    act, dec = ffprobe_dur(raw), decoded_dur(raw)
                else:
                    break
            if dec:
                act = dec            # 一律按实测时长切片，避免后半段全是空切片
            flag = "OK" if act and abs(act - p["duration"]) <= 5 else "!!时长偏差大"
            # ★ 2026-09-22 修：act 可能为 None（ffprobe 取不到时长），
            #   旧写法 f"{act:.1f}" 抛 TypeError，且崩在下面写 transcript 之前 ⇒ 整段转写白跑。
            act_s = "%.1fs" % act if act else "时长未知"
            print(f"  音频: {size/1e6:.1f} MB  {act_s} / 元数据 {p['duration']}s  {flag}")

        # ---- ASR：按 chunk 切片，逐片转写
        if text is None and (a.no_asr or act is None):
            # ★ 显式声明，别让下游把「没跑 ASR」误读成「转写为空」
            why = "本次以 --no-asr 运行" if a.no_asr else "该投稿无音轨"
            text = f"(未转写：{why}，仅取画面帧)"
            print(f"  转写: 已跳过（{why}）")
        elif text is None:
            # ★ 2026-09-21：切片 + 转写整体下沉到 slice_and_transcribe()，
            #   与 bili_zhenti.py 共用一份实现（带断点续跑 / 模型探测缓存 / 可选 aac 编码）
            text, st = slice_and_transcribe(
                raw, out / "audio", tag, a.chunk, act or p["duration"], key,
                codec=a.asr_codec, jobs=a.asr_jobs)
            if st["reused"]:
                print(f"  转写: 复用缓存 {st['reused']}/{st['total']} 片（本次新转 {st['fresh']} 片）")
        else:
            text = f"[整段] {text}"

        (out / f"transcript_{tag}.md").write_text(
            f"# {m['title']} · 第 {p['page']} P\n\n> {p['part']} · {p['duration']}s\n\n{text}\n",
            encoding="utf-8", newline="\n")

        # ---- 抽帧
        frames = []
        if not a.no_video and vi_url:
            vid = out / "audio" / f"{tag}_video.m4s"
            vsize = download(vi_url, vid)
            print(f"  视频: {vsize/1e6:.1f} MB")
            subprocess.run([FFMPEG, "-y", "-v", "error", "-i", str(vid),
                            "-vf", f"fps={a.fpm}/60,scale=800:-1", "-q:v", "3",
                            str(out / "frames" / f"{tag}_%04d.jpg")],
                           check=True, timeout=SUBPROC_TIMEOUT)
            try_unlink(vid)
            frames = sorted((out / "frames").glob(f"{tag}_*.jpg"))
            print(f"  帧: {len(frames)} 张")
        sections.append({"page": p["page"], "part": p["part"],
                         "duration": p["duration"], "text": text,
                         "frames": [f.name for f in frames]})

    # ---- report.md：给多模态模型看的材料
    L = [f"# {m['title']}", "",
         f"- BV: `{m['bvid']}`", f"- UP: {m['owner']}",
         f"- 分P 总数: {len(m['pages'])}（本次处理 {len(sections)}）",
         f"- 总时长: {m['total']}s", ""]
    if m["desc"]:
        L += ["## UP 主简介", "", m["desc"][:800], ""]
    for s in sections:
        L += [f"## 第 {s['page']} P · {s['part']}", "",
              f"时长 {s['duration']}s · 帧 {len(s['frames'])} 张", "",
              "### 逐字稿", "", s["text"], ""]
        if s["frames"]:
            L += ["### 画面帧（可直接读取以理解板书/PPT）", ""]
            L += [f"- `frames/{f}`" for f in s["frames"]]
            L += [""]
    (out / "report.md").write_text("\n".join(L), encoding="utf-8", newline="\n")

    print(f"\n完成 → {out}")
    print(f"  report.md       解析材料（元数据 + 逐字稿 + 帧清单）")
    print(f"  transcript_*.md 各分P 逐字稿")
    print(f"  frames/         {sum(len(s['frames']) for s in sections)} 张画面帧")
    print("\n下一步：让多模态模型读 report.md 与 frames/ 下的图，即可出摘要/问答/知识点卡片。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
