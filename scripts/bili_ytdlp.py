#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B站元数据与「字幕轨声明」探测 —— yt-dlp 补元数据，归属判定仍归自建。

为什么需要它：
    自建管线（`bili_analyze.py` / `bili_fetch_subs.py`）历史上踩过一个大坑：
    **`x/player/v2` 会随机返回别的视频的字幕轨** —— 正确轨的 URL 里含 aid+cid，
    实测命中率只有 15–25%，而 `code` 恒 0、`lan` 恒 `ai-zh`，从响应看不出异常。

    ★ 该坑**已在 2026-09-19 第四次修复时换掉端点**：现在用 `x/player/wbi/v2`，
    同一 cid 连打 20 次 **20/20 命中**，真无轨的视频也稳定返回空数组。
    aid+cid 不变量因此**降级为安全网**（`PROBE_RETRIES = 12` 是兜底，不是主策略）。

    问题剩下两个：
      1. **一条轨都没有的视频也会被重试满 12 次**，全部落空 —— 单项最大浪费；
      2. 历史遗留：`BV1xzBCBFExz` 的磁盘上躺着 6 份「下载成功」的错字幕
         （`_verify.jsonl` 全 false），那是换端点之前留下的。

    yt-dlp 能补上前半个问题：一次请求就拿到「B站声称有哪些轨」，不用赌 12 次。

★★ 但本脚本的价值**不是**「确定性判定字幕有无」—— 那个结论我写错过四次，
   每次都被一个具体的对照实验或源码阅读推翻，全部记录在此
   （详见 subtitle_verdict 的注释）：

     【1】「空 dict = 没有」→ 错。未登录时 B 站不给 AI 字幕，空 dict 只说明没登录。
          （对照：`BV12DdNYzEvy` 本地 200/200 通过，yt-dlp 未登录时却报 `{}`）
     【2】「带上登录态还是空 = 真没有」→ 错。**yt-dlp 默认根本不查字幕**，
          不加 `listsubtitles=True` 时 `subtitles` 恒为 `{}`，
          而日志照样打印 `Extracting subtitle info <cid>` —— 沉默的默认值伪装成否定结论。
     【3】「有 lang key = 有字幕」→ 错，但**错因和我最初的判断不一样**。
          加上开关后 `BV1xzBCBFExz` 报「6/6 有字幕」，我据此写下
          「B站会声称有轨但轨是错的，yt-dlp 也躲不过」—— 这个结论**是错的**。
          真相：yt-dlp 的 `_get_subtitles()` **硬编码**往 `subtitles` 里塞了一条
          `danmaku`（弹幕 XML，`https://comment.bilibili.com/{cid}.xml`），
          见 yt-dlp `extractor/bilibili.py:255-261`。
          ⇒ 它是**弹幕，不是字幕**，且**每个视频都有**，与「有无字幕」毫无关系。
            不剔除它，`claimed_langs` 永远非空 —— 一个把每个视频都判成
            「有字幕」的假阳性。剔除后 `BV1xzBCBFExz` 登录态下**确实无轨**，
            与本地 `_verify.jsonl` 全 false **吻合**。

    ⇒ 最终定位（第五版，源码 + 双向对照支撑）：

        yt-dlp 能回答：**「B站声称这个分P 有哪些语言的字幕轨」**（剔除 danmaku 后）
        yt-dlp 不能回答：**「这些轨是否真的属于这个分P」**

        不能回答的原因有**两条源码级证据**（`extractor/bilibili.py:255-275`）：
          ① yt-dlp 走的是 `x/player/wbi/v2`（`query={'aid','cid'}`）——
             **和自建脚本现在是同一个端点**（自建 2026-09-19 换过来的）；
          ② 它拿到 `subtitle_url` 后直接 `_download_json()` 转 SRT，
             **从不检查该 URL 里是否含 aid+cid**。
        ⇒ 它**没有自建脚本的 aid+cid 安全网**；且 yt-dlp 的 info dict
          **不暴露 cid/aid**（实测顶层与 entries 都没有），想做也做不了。
        ⇒ 两者是**互补**而非替代：yt-dlp 负责「一次请求出声明」，
          自建负责「下载 + aid+cid 校验」。

        所以本脚本把字段命名为 `claimed_langs` 而非 `has_subtitle`，
        并在 `_ytdlp.jsonl` 里恒写 `ownership_verified: false` ——
        **不让下游把「声明」误读成「结论」**。

        另一处实测更正：`ai-zh` 条目**不是空壳轨**。它是
        `{'ext': 'srt', 'data': '<完整 SRT 全文>'}` —— **内联内容、没有 url 字段**
        （yt-dlp 自己把 JSON 转成了 SRT 塞进 `data`）。
        所以「声明有轨」虽然证明不了归属，但**内容确实能直接取到**；
        只是这份内容**未经 aid+cid 校验**，不能直接用于生产。

    两个还能站得住的收益：
      · **确认无轨**（已登录 + 一条声明都没有）→ 可安全跳过，省下 12 次重试/分P；
      · **真实分P 标题**（如「p01 单选题部分」）→ 项目原先的 `part` 字段没这个粒度。

    ★ 收益 1 的消费端已经接好：`bili_fetch_subs.py --ytdlp-skip`
      会读本脚本写的 `_ytdlp.jsonl`，把「已登录且确认无轨」的分P 直接排除在探测之外。
      两边是**配套**的 —— 只跑本脚本不会省下任何重试，要跑下载器时才生效。

用法：
    python scripts/bili_ytdlp.py BV1xzBCBFExz
    python scripts/bili_ytdlp.py BV1xzBCBFExz --out data/bili-analyze
    python scripts/bili_ytdlp.py BV12DdNYzEvy --items 1-2     # 200 分P 只探前两个
    python scripts/bili_ytdlp.py BV1xzBCBFExz --audio         # 顺便下最低码率音频
    python scripts/bili_ytdlp.py --batch bvs.txt              # 每行一个 BV
    python scripts/bili_ytdlp.py BV1xzBCBFExz --json          # 机器可读

    # 先普查、再让下载器用上（推荐流程）
    python scripts/bili_ytdlp.py --batch bvs.txt --items 1 --out data/bili-analyze
    python scripts/bili_fetch_subs.py --refresh --ytdlp-skip

    ★ 想让「确认无轨」可信，必须带登录态：
      `--sessdata <值>` > 环境变量 `BILI_SESSDATA` > 仓库根 `.bili-sessdata` 文件
      （优先级复用 `bili_analyze.get_sessdata()`，不另立一套）

写入：
    <out>/_ytdlp_meta.json 真实分P标题、时长、cid、aid（项目原先没有这份元数据）
                           ★ 刻意**不叫** meta.json —— 管线 bili_zhenti.py 也用那个名字，
                             同目录下会**互相覆盖且看不出异常**
    <out>/_ytdlp.jsonl     每行一个分P 的声明，含 `authenticated` 与
                           `ownership_verified: false`
                           ★ 按 `p` **合并**写（不是截断）—— 只探部分分P 时
                             （`--items`）不会抹掉上次探到的行
    <out>/audio_pNN.m4s    --audio 时才有

    ★ 刻意不写 `_verify.jsonl` —— 那是自建重试链的产物，覆盖它等于把
      「重试命中率」这个观测指标抹掉。两份判定应当并存、互相印证。

退出码：0 = 全部探测成功；1 = 至少一个 BV 失败；2 = 缺 yt-dlp。

依赖：yt-dlp（**可选增强**，缺失时给出安装提示并退出 2）；其余只用标准库。
"""

from __future__ import annotations

import argparse
import contextlib
import datetime
import importlib.util
import json
import os
import pathlib
import sys
import tempfile
import time
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
REFERER = "https://www.bilibili.com/"
DEFAULT_ROOT = pathlib.Path("data/bili-analyze")

# 与 bili_analyze.py 的 PROBE_RETRIES 对齐，用于算「省下多少次重试」
# ★ 输出文件名刻意带下划线前缀 + 专用后缀，避免与管线的 meta.json 撞名：
#   `bili_zhenti.py` 也会写 `meta.json`（字段 schema 完全不同，它有 schema_version/
#   stages/pages，本脚本只有 9 个字段）。两边目录目前不重叠（管线默认 data/bili-zhenti），
#   但一旦有人用 --out 指到同一目录，同名文件会**互相覆盖且看不出异常**。
META_NAME = "_ytdlp_meta.json"
JSONL_NAME = "_ytdlp.jsonl"

LEGACY_RETRIES = 12

# 与 promote/convert 三脚本口径一致：日期可注入，便于回归复现
DATE = os.environ.get("ZHENTI_DATE") or datetime.date.today().isoformat()


# ---------------------------------------------------------------- 基础设施

def _load_analyze():
    """把同目录的 bili_analyze.py 当模块载入（它有自己的 __main__ 保护，导入安全）。

    ★ 为什么要复用而不是重写：SESSDATA 的查找优先级
      （`--sessdata` > 环境变量 `BILI_SESSDATA` > `.bili-sessdata` 文件）
      是**账号凭证的单一事实源**，抄一份出来迟早会两边不一致。
      本脚本只借它的 `get_sessdata()`，不复制任何取数逻辑。
    """
    p = HERE / "bili_analyze.py"
    if not p.exists():
        return None
    spec = importlib.util.spec_from_file_location("bili_analyze", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def get_sessdata(cli_value=None):
    """找 SESSDATA。返回 (值, 来源说明)。找不到返回 (None, "")。"""
    ba = _load_analyze()
    if ba is not None:
        return ba.get_sessdata(cli_value)
    # 兜底：bili_analyze.py 不在时，走同一套优先级（口径见上）
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


def require_ytdlp():
    """yt-dlp 是可选增强：缺了就明确告诉对方怎么装，而不是抛一堆 ImportError。"""
    try:
        import yt_dlp  # noqa: F401
        return yt_dlp
    except ImportError:
        print("!! 缺 yt-dlp（本脚本的唯一可选依赖）。装一个：")
        print("   <venv>/Scripts/pip install yt-dlp")
        print("   或  python -m pip install yt-dlp")
        raise SystemExit(2)


@contextlib.contextmanager
def cookie_file(sessdata):
    """把 SESSDATA 落成一个**临时** Netscape cookiefile，用完即删。

    ★★ 为什么不能图省事走 `http_headers`（2026-09-21 实测）：

        给 yt-dlp 传 `http_headers={'Cookie': 'SESSDATA=...'}` 时，它会打印
        「Deprecated Feature: Passing cookies as a header is a potential security risk」
        —— 而这条警告是**字面意义上的**：Bilibili extractor 的字幕探测**根本不读这个头**。
        实测同一个视频（`BV12DdNYzEvy`，本地 `_verify` 200/200 通过）：

            http_headers 方式  → Available subtitles: danmaku xml        （无 ai-zh）
            cookiefile 方式    → Available subtitles: danmaku xml
                                                    ai-zh   srt          ★ 拿到了

        也就是说：**走 header 会让「已登录」变成一句空话**，脚本以为自己带上了
        登录态、于是把「无字幕」当成可信结论，实际上它看到的是一个未登录的 B 站。
        这正是「假阳性（把有字幕判成没有）最危险」那条注释的又一个实例。

    凭证安全：文件写在系统临时目录（**不在仓库内**），`finally` 里删除；
    绝不打印内容，也绝不写进任何交付物。
    """
    if not sessdata:
        yield None
        return
    fd, path = tempfile.mkstemp(suffix=".txt", prefix="bili-ck-")
    os.close(fd)
    p = pathlib.Path(path)
    exp = int(time.time()) + 86400
    p.write_text(
        "# Netscape HTTP Cookie File\n"
        f".bilibili.com\tTRUE\t/\tFALSE\t{exp}\tSESSDATA\t{sessdata}\n",
        encoding="utf-8")
    try:
        yield str(p)
    finally:
        p.unlink(missing_ok=True)


def api(url, timeout=30, sessdata=None):
    h = {"User-Agent": UA, "Referer": REFERER}
    if sessdata:
        h["Cookie"] = f"SESSDATA={sessdata}"
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def pagelist(bvid, sessdata=None):
    """免登录免签名的分P 列表 —— 拿 cid/aid。

    ★ 为什么必须单独拿：yt-dlp 的 info dict **不暴露 cid/aid**
      （实测顶层与 entries 里都没有这两个字段）。
      而 aid+cid 正是「字幕轨属于谁」的唯一判据，所以这一路不能省。
    """
    d = api(f"https://api.bilibili.com/x/player/pagelist?bvid={bvid}", sessdata=sessdata)
    if d.get("code") != 0:
        raise RuntimeError(f"pagelist code={d.get('code')} msg={d.get('message')}")
    return d["data"]


def probe(bvid, yt_dlp, flat=False, items=None, sessdata=None):
    """用 yt-dlp 取元数据。返回 (标题, [分P dict])，失败返回 (None, [])。

    `items` 透传给 yt-dlp 的 playlist_items（如 "1-2" / "1,3,5"）。
    ★ 为什么必须有：本地最大的一个 BV 有 **200 个分P**，
      全量探测一次要好几分钟；只想核验「这个视频有没有字幕」时，探 2 个分P 就够。

    `sessdata` 是**判定可信度的前提**；必须走 cookiefile，原因见 cookie_file()。

    ★★ `listsubtitles` 不是可选项，是**必需项**（2026-09-21 实测定位）：

        不加这个开关时，yt-dlp 的 info dict 里 `subtitles` 恒为 `{}`，
        而日志里照样打印 `Extracting subtitle info <cid>` —— 看起来像「查过了，没有」。

        同一个视频（`BV12DdNYzEvy` p1）四种选项组合实测：

            baseline（本脚本初版）        subtitles={}                      ← 假的「没有」
            +listsubtitles                subtitles=['danmaku','ai-zh','ai-en']  ★
            +writesubtitles               subtitles=['danmaku','ai-zh','ai-en']
            +writesubtitles+langs=all     subtitles=['danmaku','ai-zh','ai-en']

        ⇒ `{}` 的真实含义是「**yt-dlp 根本没去查**」，不是「B站没有」。
          这是本脚本开发中第二个、也是更隐蔽的坑：**沉默的默认值伪装成否定的结论**。
    """
    opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "ignoreerrors": True,
        "extract_flat": flat,
        # ★ 必需：不加它 subtitles 恒为空，会把「没查」误读成「没有」
        "listsubtitles": True,
    }
    if items:
        opts["playlist_items"] = items
    with cookie_file(sessdata) as ck:
        if ck:
            opts["cookiefile"] = ck
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(
                f"https://www.bilibili.com/video/{bvid}", download=False)
    if not info:
        return None, []
    entries = info.get("entries") or [info]
    return info.get("title"), [e for e in entries if e]


# ★ yt-dlp 硬编码塞进 `subtitles` 的弹幕轨（不是字幕）。
#   见 yt-dlp `extractor/bilibili.py:255-261`：
#       subtitles = {'danmaku': [{'ext': 'xml',
#                                 'url': f'https://comment.bilibili.com/{cid}.xml'}]}
#   ⇒ 每个视频都有，与「有无字幕」无关。不剔除它，`claimed_langs` 永远非空。
SUB_NOISE = frozenset({"danmaku"})


def subtitle_verdict(ent, authed):
    """把 yt-dlp 的字幕字段翻成结论。返回 (claimed_langs, source, note)。

    ★★ 这里有三层坑，全部是 2026-09-21 实测踩出来的，逐层记录：

      【第 1 层】「空 dict = 没有」是错的
          初版据此判定 `BV1xzBCBFExz` 6/6 分P「无字幕」并写进结论。
          正向对照推翻：`BV12DdNYzEvy` 本地 `_verify.jsonl` 是 **200/200 通过**
          （确实有正确字幕），而未登录的 yt-dlp 对它同样报 `subtitles={}`。
          原因：**B 站的 AI 字幕需要登录才可见**（`data.need_login_subtitle`）。

      【第 2 层】带上登录态后依然空 —— 因为**根本没查**
          改用 cookiefile（`http_headers` 传 Cookie 是不生效的，见 cookie_file()）
          之后仍为空，直到加上 `listsubtitles=True` 才拿到：
              baseline            → {}
              +listsubtitles      → ['danmaku','ai-zh','ai-en']
          ⇒ `{}` 的真实含义是「**yt-dlp 没去查**」，不是「B站没有」。
            沉默的默认值伪装成了否定的结论。

      【第 3 层】「有 lang key」也**不等于**「有字幕」—— 但错因不是我以为的那个
          加上 `listsubtitles` 后，`BV1xzBCBFExz` 报「6/6 有字幕」，
          我据此写下「B站声称有轨但轨是错的」—— **这个结论本身是错的**。
          真相：那 6 条全是 `danmaku`。yt-dlp 在 `_get_subtitles()` 里
          **硬编码**塞了一条弹幕 XML 轨进 `subtitles`（源码见 SUB_NOISE 注释），
          所以**任何视频**都会「有字幕」。
          ⇒ 剔除 `danmaku` 后，`BV1xzBCBFExz` 登录态下**确实无轨**，
            与本地 `_verify.jsonl` 全 false 完全吻合；`BV12DdNYzEvy` 则是
            `['ai-en','ai-zh']`，其 `ai-zh` 内联 SRT 与本地 `subtitle_p01.txt`
            **逐字一致**（「好下面我们看那个第一个题 / 他说让你求这个函数的定义域啊」）。

      ⇒ 所以本函数**只输出「B站的声明」**，命名用 `claimed` 而不是 `has`，
        并且在 `_ytdlp.jsonl` 里恒带 `ownership_verified: false`。

      ★ 归属判定为什么**不能**交给 yt-dlp（源码级证据，非推测）：
        yt-dlp `extractor/bilibili.py:255-275` 调的是 `x/player/wbi/v2`
        （`query={'aid','cid'}`）—— **和自建脚本现在是同一个端点**（自建
        2026-09-19 从 `x/player/v2` 换过来的）—— 拿到 `subtitle_url` 后
        直接下载转 SRT，**从不检查 URL 里是否含 aid+cid**。
        ⇒ 它**没有自建脚本的 aid+cid 安全网**；而且 yt-dlp 的 info dict
          **不暴露 cid/aid**（实测顶层与 entries 都没有），想做也做不了。
          归属校验必须由自建脚本用 `x/player/wbi/v2` 的 aid+cid 比对给出
          （见 bili_analyze.py 的 `probe_subtitle`）。

      另一处实测更正：`ai-zh` 条目**不是空壳轨**。它是
      `{'ext': 'srt', 'data': '<完整 SRT 全文>'}` —— **内联内容、没有 url 字段**。
      所以「声明有轨」证明不了归属，但内容确实能直接取到；
      只是这份内容**未经 aid+cid 校验**，不能直接用于生产。
    """
    subs = ent.get("subtitles") or {}
    autos = ent.get("automatic_captions") or {}
    claimed = sorted((set(subs) | set(autos)) - SUB_NOISE)
    if claimed:
        return claimed, "yt-dlp:claimed", ""
    if authed:
        # 已登录 + 一条声明都没有 ⇒ 这才是可信的「确实没有」
        return [], "yt-dlp:no_track_authenticated", ""
    return [], "yt-dlp:unknown_unauthenticated", ""


# ---------------------------------------------------------------- 主流程

def process(bvid, root, yt_dlp, flat=False, audio=False, as_json=False,
            items=None, sessdata=None):
    """探测单个 BV，写 _ytdlp_meta.json + _ytdlp.jsonl。返回结果 dict。"""
    authed = bool(sessdata)
    title, entries = probe(bvid, yt_dlp, flat=flat, items=items, sessdata=sessdata)
    if title is None:
        print(f"[{bvid}] !! yt-dlp 取不到元数据（稿件可能已下架/转私密）")
        return {"bvid": bvid, "ok": False, "reason": "extract_failed", "parts": []}

    pages = []
    try:
        pages = pagelist(bvid, sessdata=sessdata)
    except Exception as e:
        print(f"[{bvid}] !! pagelist 失败({e})，cid 将缺失 —— aid+cid 防线本轮不可用")

    out = pathlib.Path(root) / bvid
    out.mkdir(parents=True, exist_ok=True)

    print(f"[{bvid}] {title}")
    print(f"          分P {len(entries)} 个（pagelist {len(pages)} 个）· "
          f"登录态 {'已带' if authed else '未带'}")

    parts, n_claim, n_none, n_unknown, saved = [], 0, 0, 0, 0
    for ent in entries:
        # ★ 用 playlist_index（真实分P 号）而非枚举序号 ——
        #   `--items 5-6` 时枚举序号是 1/2，会把 p5/p6 标成 p1/p2。
        pno = ent.get("playlist_index") or (len(parts) + 1)
        pg = pages[pno - 1] if 0 < pno <= len(pages) else {}
        claimed, src, _ = subtitle_verdict(ent, authed)
        if claimed:
            n_claim += 1
        elif src == "yt-dlp:no_track_authenticated":
            n_none += 1
            saved += LEGACY_RETRIES
        else:
            n_unknown += 1
        parts.append({
            "p": pno,
            "cid": pg.get("cid"),
            "title": ent.get("title"),
            "duration": round(ent.get("duration") or 0, 1),
            # ★ 字段名刻意用 claimed 而非 has —— 这是 B站的声明，不是归属证明
            "claimed_langs": claimed,
            "subtitle_source": src,
            "authenticated": authed,
            # 归属只能由 aid+cid 校验给出，yt-dlp 这条线给不了
            "ownership_verified": False,
        })
        if claimed:
            mark = "声明有轨"
        elif src == "yt-dlp:no_track_authenticated":
            mark = "确认无轨"
        else:
            mark = "未定(未登录)"
        cid = pg.get("cid") or "?"
        print(f"          p{pno:<3} cid={cid:<12} {mark:<11} {str(ent.get('title'))[:36]}")

    meta = {
        "bvid": bvid,
        "title": title,
        "part_count": len(entries),
        "aid": pages[0].get("aid") if pages else None,
        "authenticated": authed,
        "source": "yt-dlp + x/player/pagelist",
        "probed_at": DATE,
        "note": "claimed_langs 是 B站的声明，非归属证明；归属需 aid+cid 校验",
        "parts": parts,
    }
    (out / META_NAME).write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ★ 按 `p` **合并**写，不是截断写（2026-09-21 修）。
    #   原因：`--items` 常被用来只探几个分P（如 `--items 12,162,195`）。
    #   若用 "w" 截断，这次只写 3 行，**上一次探到的 p1 就被抹掉了** ——
    #   于是「跳过集」凭空变小，而且没有任何报错。
    #   这与本项目 `_verify.jsonl` 的教训同源（清空记录 = 下一轮全部重下）。
    #   合并规则：同一 `p` 以**本次结果为准**，其余保留，按 p 排序。
    jl = out / JSONL_NAME
    rows = {}
    if jl.exists():
        for ln in jl.read_text(encoding="utf-8").splitlines():
            ln = ln.strip()
            if not ln:
                continue
            try:
                o = json.loads(ln)
                rows[o["p"]] = o
            except Exception:
                pass          # 坏行丢弃，不影响本次写入
    for p in parts:
        rows[p["p"]] = {
            "p": p["p"], "cid": p["cid"],
            "claimed_langs": p["claimed_langs"],
            "source": p["subtitle_source"],
            "authenticated": authed,
            "ownership_verified": False,
        }
    with jl.open("w", encoding="utf-8") as f:
        for pno in sorted(rows):
            f.write(json.dumps(rows[pno], ensure_ascii=False) + "\n")

    if audio:
        got = download_audio(bvid, out, yt_dlp, len(entries), sessdata=sessdata)
        print(f"          音频：{got}/{len(entries)} 个分P 已落盘")

    print(f"          → {out}/{META_NAME}   {out}/{JSONL_NAME}")
    if n_claim:
        print(f"          ⚠ {n_claim} 个分P「声明有轨」—— 这只代表 B站声称有，"
              f"**不代表轨属于本视频**")
        print(f"            归属必须再过 aid+cid 校验（bili_analyze.py），"
              f"否则会重演「下到别的视频字幕」")
    if saved:
        print(f"          ★ 已登录且确认无轨，省下约 {saved} 次无用重试"
              f"（{LEGACY_RETRIES} 次/分P × {saved // LEGACY_RETRIES} 分P）")
    if n_unknown:
        print(f"          ⚠ {n_unknown} 个分P 判为「未定」—— 未带登录态时，"
              f"「无轨」不可信（AI 字幕需登录才可见）")

    return {"bvid": bvid, "ok": True, "title": title, "authenticated": authed,
            "parts": parts, "claimed": n_claim, "no_track": n_none,
            "unknown": n_unknown, "retries_saved": saved}


def download_audio(bvid, out, yt_dlp, n_parts, sessdata=None):
    """下最低码率音频。用 yt-dlp 的格式选择器，避免自己拼 playurl。"""
    opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "worstaudio",
        "outtmpl": str(out / "audio_p%(playlist_index)02d.%(ext)s"),
        "ignoreerrors": True,
    }
    with cookie_file(sessdata) as ck:
        if ck:
            opts["cookiefile"] = ck
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([f"https://www.bilibili.com/video/{bvid}"])
    return len(list(out.glob("audio_p*")))


def main():
    ap = argparse.ArgumentParser(
        description="B站元数据与字幕轨声明探测（yt-dlp 出声明，归属仍归 aid/cid 校验）")
    ap.add_argument("bvid", nargs="?", help="BV 号，如 BV1xzBCBFExz")
    ap.add_argument("--batch", metavar="FILE", help="每行一个 BV 号")
    ap.add_argument("--out", default=str(DEFAULT_ROOT),
                    help=f"输出根目录（默认 {DEFAULT_ROOT}/<BV>/）")
    ap.add_argument("--flat", action="store_true",
                    help="快速模式：只取标题，不探字幕轨（省时间，但拿不到 claimed_langs）")
    ap.add_argument("--items", metavar="SPEC",
                    help='只探部分分P，如 "1-2" / "1,3,5"（大分P 视频先验用）')
    ap.add_argument("--sessdata", metavar="VALUE",
                    help="B站 SESSDATA（取 AI 字幕必需）。"
                         "优先级：本参数 > 环境变量 BILI_SESSDATA > .bili-sessdata 文件")
    ap.add_argument("--audio", action="store_true", help="顺便下最低码率音频")
    ap.add_argument("--json", action="store_true", help="stdout 输出 JSON 摘要")
    a = ap.parse_args()

    bvids = []
    if a.batch:
        bvids = [ln.strip() for ln in pathlib.Path(a.batch).read_text(
            encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")]
    elif a.bvid:
        bvids = [a.bvid]
    if not bvids:
        ap.error("需要 bvid 或 --batch")

    yt_dlp = require_ytdlp()
    sessdata, src = get_sessdata(a.sessdata)
    print(f"登录态：{('已带（' + src + '）') if sessdata else '未带 —— AI 字幕不可见，'
          f'「无字幕」将标为「未定」而非结论'}")
    print()

    results, failed = [], 0
    for bv in bvids:
        try:
            r = process(bv, a.out, yt_dlp, flat=a.flat, audio=a.audio,
                        as_json=a.json, items=a.items, sessdata=sessdata)
        except Exception as e:
            print(f"[{bv}] !! 失败：{e}")
            r = {"bvid": bv, "ok": False, "reason": str(e), "parts": []}
        if not r.get("ok"):
            failed += 1
        results.append(r)
        print()

    if a.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        tot = sum(len(r.get("parts") or []) for r in results)
        claim = sum(r.get("claimed", 0) for r in results)
        none = sum(r.get("no_track", 0) for r in results)
        unknown = sum(r.get("unknown", 0) for r in results)
        saved = sum(r.get("retries_saved", 0) for r in results)
        print("=" * 62)
        print(f"BV {len(results)} 个 · 分P {tot} 个")
        print(f"  B站声明有轨 {claim} 个  ← 需 aid+cid 校验才知归属")
        print(f"  确认无轨     {none} 个  ← 可安全跳过")
        print(f"  未定         {unknown} 个  ← 未登录，不可信")
        if saved:
            print(f"确认无轨省下的重试：约 {saved} 次")
        if claim:
            print("⚠ 「声明有轨」不等于「轨属于本视频」—— 本脚本不做归属判定")
        if failed:
            print(f"失败 {failed} 个 BV")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
