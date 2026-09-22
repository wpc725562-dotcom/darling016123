#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bili_zhenti.py —— 真题讲解抓取 · 编排入口（阶段 0：只探测，不下载）

用法：
    python scripts/bili_zhenti.py https://www.bilibili.com/video/BV1JmLP6DEtp
    python scripts/bili_zhenti.py BV1JmLP6DEtp --pages 1-3
    python scripts/bili_zhenti.py BV1JmLP6DEtp --dry-run      # 只探测，落 meta.json

设计要点（与启动提示词一致）：

  · **不重写已有链**。元信息 / 字幕探测 / 登录态全部复用 bili_analyze.py，
    本文件只做「编排 + 真题判定 + 落盘」，不复制任何取数逻辑。
  · **可中断、可检查**。每段产物独立落盘（meta.json），单段可重跑。
    阶段 ① 跑完就能看到结论，不需要等全流程。
  · **失败可见**。四种失败各有独立退出码，绝不静默返回 0。
  · **幂等**。meta.json 已存在则跳过，除非 --force。

退出码：
    0  成功
    1  未知错误
    2  需要登录（存在 AI 字幕轨，但没给 SESSDATA）
    3  稿件不可见 / BV 无效
    4  该视频无任何可用字幕轨
    5  参数错误
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys
import time

# ★ A5 残留（2026-09-20）：ffmpeg 切片/抽帧原先没有 timeout —— 外部命令挂住脚本就不返回。
SUBPROC_TIMEOUT = int(os.environ.get("ZHENTI_SUBPROC_TIMEOUT", "600"))

# ------------------------------------------------------------------ 载入复用模块

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
DEFAULT_OUT = ROOT / "data" / "bili-zhenti"

SCHEMA_VERSION = 1

# 退出码（与文件头文档一致）
EX_OK, EX_ERR, EX_NEED_LOGIN, EX_GONE, EX_NO_SUB, EX_USAGE = 0, 1, 2, 3, 4, 5


def die(msg: str, code: int = EX_USAGE):
    """打印人话错误到 stderr 并带**指定**退出码退出。

    ★ 不能用 `sys.exit("字符串")` —— 那样只会得到退出码 1，
      调用方（比如巡逻脚本）就没法区分「参数写错」和「网络挂了」。
    """
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def _load_analyze():
    """把同目录的 bili_analyze.py 当模块载入（它有自己的 __main__ 保护，导入安全）。

    ★ 为什么不用 `import bili_analyze`：脚本目录不一定在 sys.path 上，
      而且本文件常被从仓库根目录调用。显式按路径载入最稳。
    """
    p = HERE / "bili_analyze.py"
    if not p.exists():
        die(f"!! 找不到 {p}（本工具依赖它取数，不复制其逻辑）")
    spec = importlib.util.spec_from_file_location("bili_analyze", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ba = _load_analyze()

# ------------------------------------------------------------------ 真题判定

# 强信号：出现在标题 / 分P 名里，基本可以直接判真题
STRONG_TITLE = re.compile(
    r"真题|历年|押题|模拟卷|试卷|原卷|考题|真题解析|真题讲解|逐题|密训")

# 强信号：分P 名就是题型名（真题卷的结构特征，课程视频不会这么分P）
STRONG_PART = re.compile(
    r"^\s*[【\[(]?\d{4}[】\])]?\s*[一二三四五六七八九十\d]+[、.．]"   # 2025 一、选择题
    r"|^\s*[一二三四五六七八九十]+[、.．]\s*(选择|判断|填空|简答|计算|编程|应用|综合|辨析|论述|材料)"
    r"|(单选|多选|判断题|填空题|简答题|编程题|综合分析|应用题|辨析题|论述题|材料分析题)")

# 弱信号：简介里提到真题
WEAK_DESC = re.compile(r"真题|历年|押题|试卷")


def classify_zhenti(meta: dict) -> dict:
    """判定一个视频是不是「真题讲解」。多信号投票，返回结论 + 命中证据。

    ★ 为什么不只看标题：实测有课程标题写「紧扣考纲」却 100% 超纲
      （BV1Ay4y137RA，内容是计算机等级考试的 Office/Windows，与广东考纲零交集）。
      标题是 UP 主的声明，不是事实，必须与分P 结构交叉验证。
    """
    title = meta.get("title") or ""
    desc = meta.get("desc") or ""
    parts = [p.get("part") or "" for p in meta.get("pages", [])]

    signals = []
    if STRONG_TITLE.search(title):
        signals.append({"kind": "title", "hit": STRONG_TITLE.search(title).group(0)})

    part_hits = [p for p in parts if STRONG_PART.search(p)]
    if part_hits:
        signals.append({"kind": "part_structure",
                        "count": len(part_hits),
                        "ratio": round(len(part_hits) / max(len(parts), 1), 3),
                        "samples": part_hits[:5]})

    if WEAK_DESC.search(desc):
        signals.append({"kind": "desc", "hit": WEAK_DESC.search(desc).group(0)})

    strong = any(s["kind"] in ("title", "part_structure") for s in signals)
    # 分P 结构命中率 > 50% 时，即使标题没写真题也判为真题（纯题型分P 只可能是讲卷子）
    struct_ratio = next((s["ratio"] for s in signals
                         if s["kind"] == "part_structure"), 0)
    if strong or struct_ratio >= 0.5:
        verdict = "zhenti"
    elif signals:
        verdict = "likely"
    else:
        verdict = "course"

    return {"verdict": verdict, "signals": signals}


# ------------------------------------------------------------------ 输入解析

BV_RE = re.compile(r"(BV[0-9A-Za-z]{10})")


def parse_target(raw: str) -> dict:
    """接受 BV 号、完整链接、带 ?p= 的链接。返回 {bvid, page}。"""
    raw = (raw or "").strip()
    m = BV_RE.search(raw)
    if not m:
        die(f"!! 解析不出 BV 号：{raw!r}\n"
            f"   支持：BV1JmLP6DEtp / https://www.bilibili.com/video/BV1JmLP6DEtp / 带 ?p=2 的链接")
    page = None
    pm = re.search(r"[?&]p=(\d+)", raw)
    if pm:
        page = int(pm.group(1))
    return {"bvid": m.group(1), "page": page}


def parse_pages(spec: str | None, total: int) -> list[int]:
    """'1-3,5' → [1,2,3,5]；None → 全部。"""
    if not spec:
        return list(range(1, total + 1))
    out: list[int] = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            a, _, b = chunk.partition("-")
            try:
                lo, hi = int(a), int(b)
            except ValueError:
                die(f"!! --pages 区间写错了：{chunk!r}")
            out.extend(range(lo, hi + 1))
        else:
            try:
                out.append(int(chunk))
            except ValueError:
                die(f"!! --pages 不是数字：{chunk!r}")
    bad = [p for p in out if p < 1 or p > total]
    if bad:
        die(f"!! --pages 超出范围（该视频共 {total} 个分P）：{bad}")
    return sorted(set(out))


# ------------------------------------------------------------------ 日志

class Log:
    def __init__(self, path: pathlib.Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.f = path.open("a", encoding="utf-8")

    def __call__(self, msg: str):
        line = f"[{dt.datetime.now():%H:%M:%S}] {msg}"
        print(line)
        self.f.write(line + "\n")
        self.f.flush()

    def close(self):
        self.f.close()


def redact(s: str) -> str:
    """日志脱敏：绝不把 SESSDATA 明文写进日志。"""
    return re.sub(r"(SESSDATA=)[^;\s,]+", r"\1<REDACTED>", s or "")


def _atomic_write(path: pathlib.Path, text: str) -> None:
    """先写 .part 再改名。

    ★ 不能直接写目标文件：中途崩了会留下一个「短但非空」的文件，
      而续跑判断恰恰是「存在且非空」——于是它会被永久当成已完成。
      真实教训（2026-09-18）：一次崩溃把 133 个待重下的分P 变成了「已完成」。
    """
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    tmp.replace(path)


def _record_quarantine(bvdir: pathlib.Path, entry: dict) -> None:
    """把隔离记录追加进 <BV>/_quarantine.json。

    ★ 为什么要留记录而不是直接删：串轨是 B 站接口的**系统性**问题，
      隔离数量本身就是「这个账号 / 这个接口当前可信度」的指标。
      删掉就没法回答「我到底有多少条字幕是不可信的」。
    """
    p = bvdir / "_quarantine.json"
    items = []
    if p.exists():
        try:
            items = json.loads(p.read_text(encoding="utf-8"))
            if not isinstance(items, list):
                raise ValueError("顶层不是数组（是 %s）" % type(items).__name__)
        except Exception as e:
            # ★ A6（2026-09-20）：原来是 `except Exception: items = []` —— 静默清零，
            #   紧接着 `_atomic_write` 就把整个文件覆盖成「只有新的一条」。
            #   而这份记录的用途恰恰是「数一数到底有多少条轨不可信」，
            #   清掉它等于把账本烧了再记一笔。
            #   现在：改名留证，再从空开始；**改名失败就放弃写入**（宁可不记，
            #   也不能覆盖掉可能还能人工抢救的原文）。
            bak = p.with_suffix(p.suffix + ".corrupt-%s"
                                % dt.datetime.now().strftime("%Y%m%d-%H%M%S"))
            try:
                p.replace(bak)
            except OSError as e2:
                print("  [警告] %s 无法解析（%s），且改名留证也失败（%s）—— "
                      "为避免覆盖原文，本次不写隔离记录。"
                      % (p, e, e2), file=sys.stderr, flush=True)
                return
            print("  [警告] %s 无法解析（%s）—— 已改名保留为 %s，隔离记录从空开始。"
                  % (p.name, e, bak.name), file=sys.stderr, flush=True)
            items = []
    entry = dict(entry)
    entry["at"] = dt.datetime.now().isoformat(timespec="seconds")
    # ★ 去重：同一个 (page, lan, head) 反复隔离只留一条。
    #   重跑 stage_content 时会再隔离一次，不去重的话记录会线性膨胀，
    #   而这条记录的用途恰恰是「数一数到底有多少条轨不可信」。
    key = (entry.get("page"), entry.get("lan"), entry.get("head"))
    if any((i.get("page"), i.get("lan"), i.get("head")) == key for i in items):
        return
    items.append(entry)
    _atomic_write(p, json.dumps(items, ensure_ascii=False, indent=1) + "\n")


# ------------------------------------------------------------------ ② 取内容

def stage_content(bvid: str, meta: dict, bvdir: pathlib.Path, pages: list[int],
                  log, a) -> dict:
    """② 取内容：字幕轨（优先）+ 抽帧。

    ★ 为什么必须抽帧：真题讲解的**题面在画面里**（板书 / PPT），字幕只有口播。
      只抓字幕会得到「这个选 C 因为…」却永远不知道题是什么。

    ★ 抽帧的 fpm 单位是「每分钟几帧」，不是「每秒」。ffmpeg 的 -vf fps=N 是每秒，
      两者差 60 倍 —— 曾把一个 454 秒的视频抽出 453 张帧。
    """
    subs_dir = bvdir / "subs"
    frames_dir = bvdir / "frames"
    audio_dir = bvdir / "audio"
    for d in (subs_dir, frames_dir, audio_dir):
        d.mkdir(parents=True, exist_ok=True)

    by_page = {p["page"]: p for p in meta["pages"]}
    gem_key = ba.get_key()
    stat = {"subtitle": 0, "asr": 0, "skipped": 0, "no_text": 0,
            "quarantined": 0, "frames": 0, "pages_done": 0}

    for pno in pages:
        p = by_page.get(pno)
        if not p:
            continue
        cid, dur = p["cid"], p["duration"]
        log(f"--- P{pno} {p['part'][:44]} ({dur}s) ---")
        transcript = bvdir / f"transcript_p{pno:02d}.md"
        text = None

        # ---- 文字：字幕轨优先
        if transcript.exists() and transcript.stat().st_size > 0 and not a.force:
            text = transcript.read_text(encoding="utf-8")
            stat["skipped"] += 1
            log("  文字：已存在，跳过")
        else:
            try:
                subs, need_login = ba.probe_subtitle(cid, bvid)
            except Exception as e:
                # ★ 限流不是「没字幕」。混淆两者会白跑一路 ASR。
                log(f"  !! 探字幕轨失败（不是「没字幕」）：{redact(str(e))[:90]}")
                subs, need_login = [], False

            verified = [s for s in subs if s.get("_verified")]
            # ★★ 未过 aid+cid 校验的轨**绝不当字幕用**。
            #   实测 x/player/v2 有 68% 的概率返回**别的视频**的字幕轨，且报 HTTP 200 + code:0。
            #   两个实证：BV1LfXaBmEbN「政治真题回忆版」的轨是分体水冷装机，
            #            BV1gh9MBkEEC「政治真题解析」的轨是珍妮·古道尔儿童故事。
            #   所以这里只做两件事：① 有已验证轨就用它；② 没有就隔离留档 + 回落 ASR。
            #   早期版本写的 `(verified or subs)[0]` 会把串轨内容当正文写进 subs/，
            #   而 subs/ 是下游解析器的输入 —— 等于让污染直接进笔记。已修。
            if verified:
                pick = verified[0]
                url = pick.get("subtitle_url") or pick.get("subtitleUrl") or ""
                if url.startswith("//"):
                    url = "https:" + url
                if url:
                    try:
                        # ★ 用带时间戳的版本：阶段 ③ 的真题卡要求「出处指回哪一秒」，
                        #   而 srt_to_text 会丢掉 from 字段。
                        text = ba.srt_to_timed_text(url)
                        log(f"  文字：字幕轨命中（{pick.get('lan_doc') or pick.get('lan')}）"
                            f" {len(text)} 字 · 已过 aid+cid 校验")
                        # 原始轨留档，供事后核对
                        _atomic_write(subs_dir / f"P{pno:02d}.{pick.get('lan', 'x')}.txt", text)
                        stat["subtitle"] += 1
                    except Exception as e:
                        log(f"  文字：字幕抓取失败 {redact(str(e))[:70]}，回落 ASR")
            elif subs:
                # 有轨但全未过校验 → 隔离，留证据但不喂给下游
                bad_dir = subs_dir / ".bad"
                bad_dir.mkdir(parents=True, exist_ok=True)
                for s in subs:
                    lan = s.get("lan", "x")
                    u = s.get("subtitle_url") or s.get("subtitleUrl") or ""
                    if u.startswith("//"):
                        u = "https:" + u
                    if not u:
                        continue
                    try:
                        raw = ba.srt_to_text(u)
                    except Exception as e:
                        log(f"  隔离：轨 {lan} 抓取失败 {redact(str(e))[:50]}")
                        continue
                    _atomic_write(bad_dir / f"P{pno:02d}.{lan}.txt", raw)
                    _record_quarantine(
                        bvdir, {"page": pno, "cid": cid, "lan": lan,
                                "lan_doc": s.get("lan_doc"),
                                "reason": "aid+cid 校验未通过 —— 该轨极可能属于别的视频",
                                "chars": len(raw),
                                "head": raw.strip().replace("\n", " ")[:80]})
                    log(f"  隔离：轨 {lan}（{len(raw)} 字）→ subs/.bad/，"
                        f"不进笔记。开头：「{raw.strip()[:40]}」")
                log("  文字：无可用字幕轨（全部未过校验）—— 回落 ASR 取真实口播")
                stat["quarantined"] = stat.get("quarantined", 0) + len(subs)

            # ---- 回落 ASR
            if text is None:
                if a.no_asr:
                    log("  文字：无可用字幕轨，且已指定 --no-asr，跳过")
                    stat["no_text"] += 1
                elif not gem_key:
                    log("  文字：无可用字幕轨，且找不到 GEMINI_API_KEY，跳过")
                    stat["no_text"] += 1
                else:
                    if need_login and ba.COOKIE:
                        log("  文字：需登录的字幕没取到 —— SESSDATA 多半已失效，走 ASR")
                    elif need_login:
                        log("  文字：存在 AI 字幕但需登录 —— 走 ASR"
                            "（扫码可免 ASR：python scripts/bili_login.py）")
                    else:
                        log("  文字：无字幕轨 —— 走 ASR")
                    text = _asr_page(bvid, cid, pno, dur, audio_dir, gem_key, a, log)
                    if text:
                        stat["asr"] += 1
                    else:
                        stat["no_text"] += 1

            if text:
                _atomic_write(transcript,
                              f"# {meta['title']} · 第 {pno} P\n\n"
                              f"> {p['part']} · {dur}s\n\n{text}\n")

        # ---- 抽帧
        if a.no_video:
            log("  抽帧：已指定 --no-video，跳过")
        else:
            n = _grab_frames(bvid, cid, pno, frames_dir, a.fpm, log)
            stat["frames"] += n

        stat["pages_done"] += 1

    return stat


def _asr_page(bvid, cid, pno, dur, audio_dir, gem_key, a, log) -> str | None:
    """音频下载 + 按 chunk 切片 + Gemini 转写。返回逐字稿或 None。"""
    tag = f"p{pno:02d}"
    try:
        au_url, _vi, _d = ba.pick_streams(cid, bvid)
    except Exception as e:
        log(f"  取流地址失败：{redact(str(e))[:80]}")
        return None
    if not au_url:
        log("  跳过：无音频流")
        return None

    raw = audio_dir / f"{tag}.m4s"
    try:
        size = ba.download(au_url, raw)
    except Exception as e:
        log(f"  音频下载失败：{redact(str(e))[:80]}")
        return None
    act = ba.ffprobe_dur(raw)
    # ★ 校验时长：对不上说明流截断或拿错了
    flag = "OK" if act and abs(act - dur) <= 5 else "!!时长偏差大"
    log(f"  音频：{size/1e6:.1f} MB · {act or '?'}s / 元数据 {dur}s · {flag}")

    # ★ 2026-09-21：与 bili_analyze.py 共用 slice_and_transcribe()，
    #   从而同时获得「断点续跑」「模型探测缓存」「可选 aac 编码」三项加速。
    text, st = ba.slice_and_transcribe(raw, audio_dir, tag, a.chunk, act or dur,
                                       gem_key, codec=a.asr_codec, log=log)
    ba.try_unlink(raw)          # ★ 删临时文件绝不能拖垮任务，try_unlink 内部已吞异常
    if st["reused"]:
        log(f"  复用缓存 {st['reused']}/{st['total']} 片（本次新转 {st['fresh']} 片）")
    return text if text and not text.startswith("(转写失败") else None


def _write_frame_index(frames_dir, tag, fpm) -> None:
    """写 frames/_index.json：帧文件名 → 该帧在视频里的秒数。

    ★ 为什么必须落这个索引：阶段 ③ 的真题卡要求「出处是硬要求」——
      每张卡的题面都要能指回**哪一帧、哪一秒**。
      靠文件名反推（p01_0005 → 第 5 张 → 240s）只在 fpm 恒为 1 时成立，
      换个 --fpm 就全错。所以这里把映射关系显式存下来。

    ★ ffmpeg `fps=N/60` 取的是 t = 0, 60/N, 2*60/N … 处的帧，
      所以第 i 张（1-based）对应 t = (i-1) * 60 / fpm。
    """
    idx = {}
    interval = 60.0 / fpm if fpm else 60.0
    for f in sorted(frames_dir.glob(f"{tag}_*.jpg")):
        try:
            i = int(f.stem.rsplit("_", 1)[1])
        except (IndexError, ValueError):
            continue
        idx[f.name] = round((i - 1) * interval, 1)
    p = frames_dir / "_index.json"
    old = {}
    if p.exists():
        try:
            old = json.loads(p.read_text(encoding="utf-8"))
            if not isinstance(old, dict):
                raise ValueError("顶层不是对象（是 %s）" % type(old).__name__)
        except Exception as e:
            # ★ A6（2026-09-20）：这个函数**每个分P 调一次**，而 `_index.json`
            #   是**所有分P 共用**的一张表。原来坏掉就 `old = {}`，
            #   于是这一页的写入会把别的分P 的帧→秒映射全部抹掉，
            #   而且是在「一切正常」的表象下完成的。
            bak = p.with_suffix(p.suffix + ".corrupt-%s"
                                % dt.datetime.now().strftime("%Y%m%d-%H%M%S"))
            try:
                p.replace(bak)
            except OSError as e2:
                print("  [警告] %s 无法解析（%s），且改名留证也失败（%s）—— "
                      "为避免抹掉其它分P 的映射，本次不写帧索引。"
                      % (p, e, e2), file=sys.stderr, flush=True)
                return
            print("  [警告] %s 无法解析（%s）—— 已改名保留为 %s，"
                  "本页之前的其它分P 映射已随之失效（需重跑抽帧）。"
                  % (p.name, e, bak.name), file=sys.stderr, flush=True)
            old = {}
    old.update(idx)
    _atomic_write(p, json.dumps(old, ensure_ascii=False, indent=0,
                                 sort_keys=True) + "\n")


def _grab_frames(bvid, cid, pno, frames_dir, fpm, log) -> int:
    """抽帧。返回张数。已存在则跳过（幂等）。"""
    tag = f"p{pno:02d}"
    existing = sorted(frames_dir.glob(f"{tag}_*.jpg"))
    if existing:
        _write_frame_index(frames_dir, tag, fpm)
        log(f"  抽帧：已存在 {len(existing)} 张，跳过")
        return len(existing)

    try:
        _au, vi_url, _d = ba.pick_streams(cid, bvid)
    except Exception as e:
        log(f"  抽帧：取视频流失败 {redact(str(e))[:70]}")
        return 0
    if not vi_url:
        log("  抽帧：无视频流")
        return 0

    tmp = frames_dir / f"{tag}_video.m4s"
    try:
        size = ba.download(vi_url, tmp)
    except Exception as e:
        log(f"  抽帧：视频下载失败 {redact(str(e))[:70]}")
        return 0
    try:
        # ★ fpm 是「每分钟几帧」；ffmpeg 的 fps= 是「每秒几帧」，所以要 /60
        subprocess.run([ba.FFMPEG, "-y", "-v", "error", "-i", str(tmp),
                        "-vf", f"fps={fpm}/60,scale=800:-1", "-q:v", "3",
                        str(frames_dir / f"{tag}_%04d.jpg")],
                       check=True, timeout=SUBPROC_TIMEOUT)
    except Exception as e:
        log(f"  抽帧：ffmpeg 失败 {e}")
        return 0
    finally:
        ba.try_unlink(tmp)

    n = len(sorted(frames_dir.glob(f"{tag}_*.jpg")))
    _write_frame_index(frames_dir, tag, fpm)
    log(f"  抽帧：{n} 张（{size/1e6:.1f} MB 视频 · {fpm}/分钟）")
    return n


# ------------------------------------------------------------------ 主流程

def run(a) -> int:
    tgt = parse_target(a.target)
    bvid = tgt["bvid"]

    out_root = pathlib.Path(a.out).resolve() if a.out else DEFAULT_OUT
    bvdir = out_root / bvid
    meta_path = bvdir / "meta.json"
    log = Log(out_root / "logs" / f"{dt.date.today():%Y-%m-%d}.log")

    log(f"=== bili_zhenti · {bvid} · {'dry-run' if a.dry_run else 'probe'} ===")

    # ---- 登录态
    sessdata, src = ba.get_sessdata(a.sessdata)
    ba.COOKIE = sessdata or ""
    if sessdata:
        log(f"登录态：来自 {src}（值已脱敏，长度 {len(sessdata)}）")
    else:
        log("登录态：无。need_login_subtitle=True 的字幕轨将取不到")

    # ---- ① 元信息
    try:
        meta = ba.get_meta(bvid)
    except RuntimeError as e:
        msg = redact(str(e))
        log(f"取元信息失败：{msg}")
        if "62002" in msg:
            log("→ 稿件不可见（已删除 / 转私密 / 审核下架）。BV 号永久有效，视频不是。")
            return 3
        log("→ BV 号可能无效，或接口结构变了")
        return 3

    log(f"标题：{meta['title']}")
    log(f"UP：{meta['owner']} · 分P {len(meta['pages'])} · 总时长 {meta['total']}s")

    # ---- ① 真题判定
    verdict = classify_zhenti(meta)
    label = {"zhenti": "真题讲解", "likely": "疑似真题", "course": "课程（非真题）"}
    log(f"真题判定：{label[verdict['verdict']]}")
    for s in verdict["signals"]:
        if s["kind"] == "part_structure":
            log(f"  · 分P 结构命中 {s['count']} 个（占比 {s['ratio']:.0%}）"
                f" 例：{' / '.join(s['samples'][:3])}")
        else:
            log(f"  · {s['kind']} 命中「{s['hit']}」")

    # ---- 读旧记录，做增量探测
    #   ★ 跳过判断必须放在 get_meta 之后：只有拿到 page_count 才能判断
    #     「旧记录是否覆盖了本次要探的全部分P」。
    #     早期版本把跳过判断放在 get_meta 之前，于是 `--pages 1` 留下的
    #     单页 meta.json 会让后续全量跑被误判成「已完成」而整段跳过。
    old = None
    if meta_path.exists() and not a.force:
        try:
            old = json.loads(meta_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            log("已存在的 meta.json 读不动，当作不存在，重新探测")

    done_by_page: dict[int, dict] = {}
    if old:
        for r in old.get("pages") or []:
            if isinstance(r, dict) and r.get("page"):
                done_by_page[r["page"]] = r

    pages = parse_pages(a.pages, len(meta["pages"]))
    todo = [p for p in pages if p not in done_by_page]

    if not todo:
        # ★ 探测已完成 ≠ 任务结束。--stage content/all 还要往下走 ②。
        #   早期版本在这里无条件 return 0，于是「先 probe 后 content」的两步跑法
        #   在第二步会被静默跳过 —— 看起来成功，其实什么都没做。
        log(f"这 {len(pages)} 个分P 已探测过，无需重新探测")
        if a.stage == "probe":
            _print_summary(old)
            return 0
    elif done_by_page:
        log(f"增量：已有 {len(done_by_page)} 个分P 的记录，本次补探 {len(todo)} 个")

    # ---- ① 逐分P 字幕探测
    log(f"探测 {len(todo)} 个分P 的字幕可用性…")

    for p in meta["pages"]:
        if p["page"] not in todo:
            continue
        try:
            subs, need_login = ba.probe_subtitle(p["cid"], bvid)
        except Exception as e:
            state, detail = "probe_failed", redact(f"{type(e).__name__}: {e}")[:160]
        else:
            verified = [s for s in subs if s.get("_verified")]
            if verified:
                state, detail = "ok", f"{verified[0].get('lan', '?')}（已过 aid+cid 校验）"
            elif subs:
                state = "unverified"
                detail = f"{len(subs)} 轨但均未过 aid+cid 校验，内容可能串了别的视频"
            elif need_login:
                state, detail = "need_login", "有 AI 字幕，但需登录才可见"
            else:
                state, detail = "no_track", "确认无字幕轨，需走 ASR 兜底"

        done_by_page[p["page"]] = {
            "page": p["page"], "part": p["part"], "duration": p["duration"],
            "cid": p["cid"], "state": state, "detail": detail,
        }
        mark = {"ok": "OK", "unverified": "??", "need_login": "LOCK",
                "no_track": "--", "probe_failed": "ERR"}[state]
        log(f"  [{mark:4}] P{p['page']:<3} {detail[:70]}  | {p['part'][:36]}")

    probe_results = [done_by_page[k] for k in sorted(done_by_page)]
    tally = {"ok": 0, "need_login": 0, "no_track": 0, "probe_failed": 0}
    for r in probe_results:
        tally[r["state"]] = tally.get(r["state"], 0) + 1
    n_ok, n_login = tally["ok"], tally["need_login"]
    n_none, n_fail = tally["no_track"], tally["probe_failed"]

    # ---- 落 meta.json
    record = {
        "schema_version": SCHEMA_VERSION,
        "bvid": bvid,
        "url": f"https://www.bilibili.com/video/{bvid}",
        "title": meta["title"],
        "owner": meta["owner"],
        "desc": meta["desc"][:500],
        "total_duration_s": meta["total"],
        "page_count": len(meta["pages"]),
        "fetched_at": dt.datetime.now().isoformat(timespec="seconds"),
        "api": "x/web-interface/wbi/view + x/player/v2",
        "logged_in": bool(sessdata),
        "zhenti": verdict,
        "probed_pages": [r["page"] for r in probe_results],
        "subtitle_summary": {"ok": n_ok, "need_login": n_login,
                             "no_track": n_none, "probe_failed": n_fail},
        "pages": probe_results,
        "stages": {"probe": "done", "content": "todo",
                   "extract": "todo", "publish": "todo"},
    }
    bvdir.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(json.dumps(record, ensure_ascii=False, indent=1),
                         encoding="utf-8", newline="\n")
    log(f"→ {meta_path}")

    _print_summary(record)

    # ---- ② 取内容（可选）
    if a.stage in ("content", "all"):
        if verdict["verdict"] == "course" and not a.force:
            log("!! 该视频被判为「课程（非真题）」，默认不取内容。"
                "确实要跑加 --force")
            return 0
        log("")
        log("=== ② 取内容：字幕轨 + 抽帧 ===")
        # ★ 2026-09-20 修：原先直接传 [r["page"] for r in probe_results]，
        #   而 probe_results 来自**已有 meta.json 的全部历史分P** —— 于是
        #   `--pages 1-3 --stage content` 会把 8 个分P 全取一遍（实测踩到：
        #   只想取语法 1-30 的三个分P，结果下载+抽帧了整卷 92 帧）。
        #   probe_results 保留全量（要写回 meta.json），取内容时按 --pages 过滤。
        want = [r["page"] for r in probe_results if r["page"] in set(pages)]
        if not want:
            log("!! --pages 指定的分P 没有可用记录，跳过取内容")
            return 0
        log(f"取内容分P：{want}（--pages 共 {len(pages)} 个，历史记录 {len(probe_results)} 个）")
        stat = stage_content(bvid, meta, bvdir, want,
                             log, a)
        record["content_summary"] = stat
        record["stages"]["content"] = "done"
        meta_path.write_text(json.dumps(record, ensure_ascii=False, indent=1),
                             encoding="utf-8", newline="\n")
        log("")
        log(f"② 完成：字幕 {stat['subtitle']} · ASR {stat['asr']} · "
            f"跳过 {stat['skipped']} · 无文字 {stat['no_text']} · "
            f"帧 {stat['frames']} 张")
        if stat["no_text"]:
            log(f"!! {stat['no_text']} 个分P 没拿到文字，后续真题解析会缺这些分P")
            return 4
        log("下一步（未实现）：③ 真题解析 → ④ 落站")
        return 0

    # ---- 退出码
    if n_ok:
        log("阶段 ① 完成。加 --stage content 继续取字幕与抽帧。")
        return 0
    if n_login:
        log("!! 全部可用字幕都需要登录。给 SESSDATA 后重跑（--sessdata 或 BILI_SESSDATA 或 ~/.bili-sessdata）")
        return 2
    if n_none:
        log("!! 该视频没有任何字幕轨。只能走 ASR 兜底（阶段 ② 实现）。")
        return 4
    log("!! 所有分P 探测失败，多半是限流或接口变更。稍后重试或看日志。")
    return 1


def _print_summary(r: dict) -> None:
    s = r.get("subtitle_summary", {})
    label = {"zhenti": "真题讲解", "likely": "疑似真题", "course": "课程"}
    print()
    print("─" * 74)
    print(f"  {r['bvid']}  {r['title'][:48]}")
    print(f"  UP：{r['owner']} · 分P {r['page_count']} · "
          f"判定：{label.get((r.get('zhenti') or {}).get('verdict'), '?')}")
    print(f"  字幕：可用 {s.get('ok', 0)} · 需登录 {s.get('need_login', 0)} · "
          f"无轨 {s.get('no_track', 0)} · 失败 {s.get('probe_failed', 0)}")
    print("─" * 74)


# ------------------------------------------------------------------ CLI

def main() -> int:
    ap = argparse.ArgumentParser(
        prog="bili_zhenti.py",
        description="真题讲解抓取 · 编排入口（阶段 0：只探测，不下载）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例：
  %(prog)s https://www.bilibili.com/video/BV1JmLP6DEtp
  %(prog)s BV1JmLP6DEtp --pages 1-3
  %(prog)s BV1JmLP6DEtp --dry-run --force

退出码：0 成功 / 2 需登录 / 3 稿件不可见 / 4 无字幕 / 5 参数错误 / 1 其他""")
    ap.add_argument("target", help="BV 号或完整视频链接（可带 ?p=）")
    ap.add_argument("--dry-run", action="store_true",
                    help="只探测不下载（阶段 0 唯一模式，暂为默认行为）")
    ap.add_argument("--pages", default=None, help="只探测部分分P，如 1-3,5；默认全部")
    ap.add_argument("--subject", default=None,
                    help="学科标签（计算机/高数/政治/英语）；不给则从标题猜")
    ap.add_argument("--sessdata", default=None,
                    help="B站 SESSDATA。也可用环境变量 BILI_SESSDATA 或 ~/.bili-sessdata。"
                         "⚠️ 这是账号凭证，绝不提交进仓库")
    ap.add_argument("--out", default=None, help=f"产物根目录，默认 {DEFAULT_OUT}")
    ap.add_argument("--force", action="store_true", help="已探测过也重跑")
    ap.add_argument("--stage", default="probe", choices=["probe", "content", "all"],
                    help="probe=只探测（默认）；content=探测+取字幕抽帧；all=全流程")
    ap.add_argument("--fpm", type=float, default=1.0,
                    help="抽帧密度：每分钟几帧（默认 1）。★ 单位是「分钟」不是「秒」")
    ap.add_argument("--chunk", type=int, default=300,
                    help="ASR 切片长度秒数（默认 300）")
    ap.add_argument("--no-video", action="store_true", help="不抽帧（省带宽，但真题题面就在画面里）")
    ap.add_argument("--no-asr", action="store_true", help="无字幕轨时不用 ASR 兜底")
    ap.add_argument("--asr-codec", choices=["wav", "aac32"], default="wav",
                    help="ASR 上传编码。wav=默认（保真）；aac32 上传小 7.5×、"
                         "实测端到端快约 2×，但转写少约 8%% 字，只用于粗筛。")
    a = ap.parse_args()
    try:
        return run(a)
    except KeyboardInterrupt:
        print("\n已中断。已落盘的产物可复用，重跑即可。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
