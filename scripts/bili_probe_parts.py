#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""探测某个 BV 指定分P范围**到底有没有字幕轨**，并区分三种状态。

为什么要单独写一个
------------------
`bili_fetch_subs.py` 是「有轨就下载」，本脚本是「先问有没有轨」。
两者解决不同问题：给一门课排期前，需要先知道哪些分P**真的**没轨（只能走 ASR），
哪些只是**这次没探到**（重探就好）。把后者当成前者，会凭空多出一大批 ASR 工作。

三条硬规矩（都踩过坑，见 skill `bilibili-video-capture`）
--------------------------------------------------------
1. **端点必须是 `x/player/wbi/v2`**，不是 `x/player/v2`。
   后者会**凭空编出别的视频的字幕轨**（真无轨的视频也能返回一条），
   于是「有轨但内容不对」和「根本没轨」被混成同一类。
2. **凭据按绝对路径解析，并打印实际加载了哪个文件。**
   `bili_analyze.get_sessdata()` 找的是 `Path(".bili-sessdata")`——**相对当前工作目录**。
   从别处运行就静默变成「未登录」，而 `need_login_subtitle` 仍是 true，
   于是每个分P 都返回空数组 —— 看起来和「这门课没字幕」一模一样。
   本脚本绕过它，直接读仓库根的绝对路径。
3. **先证明查询成功，再相信空结果。** 一次 `x/web-interface/nav` 就够：
   `data.isLogin` 为假时直接退出，免得「没登录」伪装成「没字幕」。

三态定义
--------
  has     —— 有轨，且 URL 命中 aid+cid 不变量
  none    —— 端点正常返回 code:0 且轨列表为空  → **真无轨，可信**
  unknown —— 异常 / code!=0 / 有轨但 URL 全空   → **不算结论，只算失败**

只有 `none` 可以写进结论。`unknown` 必须重跑。

用法
----
  python scripts/bili_probe_parts.py --bv BV14T4y1Y78G --pages 169-184
  python scripts/bili_probe_parts.py --bv BV14T4y1Y78G --pages 177-184 --attempts 4
"""
import argparse
import json
import os
import pathlib
import random
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
SESSDATA_FILE = ROOT / ".bili-sessdata"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


def load_sessdata(explicit=None):
    """返回 (值, 来源说明)。绝对路径，不依赖 CWD。"""
    if explicit:
        return explicit, "--sessdata 参数"
    if os.environ.get("BILI_SESSDATA"):
        return os.environ["BILI_SESSDATA"], "环境变量 BILI_SESSDATA"
    if SESSDATA_FILE.exists():
        return SESSDATA_FILE.read_text(encoding="utf-8").strip(), str(SESSDATA_FILE)
    return None, "(未找到)"


SESSDATA, SRC = load_sessdata()


def api(url, timeout=25):
    h = {"User-Agent": UA, "Referer": "https://www.bilibili.com/"}
    if SESSDATA:
        h["Cookie"] = "SESSDATA=%s" % SESSDATA
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def check_login():
    """没有这一步，'未登录' 会伪装成 '没字幕'。"""
    d = api("https://api.bilibili.com/x/web-interface/nav")
    data = d.get("data") or {}
    return bool(data.get("isLogin")), data.get("uname") or ""


def get_pages(bvid):
    d = api("https://api.bilibili.com/x/web-interface/wbi/view?bvid=%s" % bvid)
    if d.get("code") != 0:
        raise SystemExit("元数据失败 code=%s msg=%s" % (d.get("code"), d.get("message")))
    dd = d["data"]
    return dd["title"], dd["owner"]["name"], dd["pages"]


def probe(cid, bvid, attempts=4):
    """返回 (state, detail)。state ∈ {has, none, unknown}"""
    last = "未开始"
    for i in range(attempts):
        try:
            d = api("https://api.bilibili.com/x/player/wbi/v2?bvid=%s&cid=%s" % (bvid, cid))
            if d.get("code") != 0:
                last = "code=%s" % d.get("code")
            else:
                data = d.get("data") or {}
                subs = ((data.get("subtitle") or {}).get("subtitles")) or []
                key = "%s%s" % (data.get("aid"), data.get("cid"))
                if not subs:
                    # 端点正常 + 空列表 = 真无轨。这一条是唯一可信的否定结论。
                    return "none", "code:0 轨列表为空 need_login=%s" % data.get("need_login_subtitle")
                if any(s.get("subtitle_url") for s in subs):
                    hit = [s for s in subs if key in (s.get("subtitle_url") or "")]
                    if hit:
                        return "has", "轨=%d 命中aid+cid lan=%s" % (len(subs), hit[0].get("lan"))
                    last = "轨=%d 但都不含 aid+cid（端点串轨）" % len(subs)
                else:
                    last = "轨=%d 但 URL 全空（瞬时故障）" % len(subs)
        except Exception as e:
            last = "%s: %s" % (type(e).__name__, e)
        time.sleep(0.8 + random.random() * 1.4)
    return "unknown", last


def parse_pages(spec, total):
    out = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            a, b = chunk.split("-", 1)
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(chunk))
    return [p for p in out if 1 <= p <= total]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bv", required=True)
    ap.add_argument("--pages", required=True, help="如 169-184 或 1,5,9")
    ap.add_argument("--attempts", type=int, default=4)
    ap.add_argument("--json", help="把结果写到这个路径")
    args = ap.parse_args()

    print("凭据来源: %s" % SRC)
    print("凭据长度: %d" % len(SESSDATA or ""))
    if not SESSDATA:
        print("✗ 没有凭据，AI 字幕是登录门控的，本次结果无意义。中止。")
        return 2
    ok, uname = check_login()
    print("登录态: isLogin=%s uname=%s" % (ok, uname))
    if not ok:
        print("✗ 未登录 —— 空结果会伪装成「没字幕」。中止，别下结论。")
        return 2

    title, owner, pages = get_pages(args.bv)
    print("视频: %s" % title)
    print("UP主: %s   总分P: %d" % (owner, len(pages)))
    wanted = parse_pages(args.pages, len(pages))
    by_page = {p["page"]: p for p in pages}
    print("=" * 78)

    rows = []
    for pno in wanted:
        pg = by_page.get(pno)
        if not pg:
            continue
        state, detail = probe(pg["cid"], args.bv, args.attempts)
        mark = {"has": "✓ 有轨", "none": "✗ 无轨", "unknown": "? 未定"}[state]
        print("P%-4d %-8s %-34s %s" % (pno, mark, (pg.get("part") or "")[:34], detail))
        rows.append({"p": pno, "part": pg.get("part"), "state": state, "detail": detail})
        time.sleep(0.3)          # wbi/v2 并发会 RemoteDisconnected，串行 + 间隔

    print("=" * 78)
    n = {s: sum(1 for r in rows if r["state"] == s) for s in ("has", "none", "unknown")}
    print("有轨 %d / 无轨 %d / 未定 %d" % (n["has"], n["none"], n["unknown"]))
    if n["unknown"]:
        print("⚠ 有未定项 —— 必须重跑这些分P，未定不等于无轨。")

    if args.json:
        pathlib.Path(args.json).write_text(
            json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
        print("结果已写入 %s" % args.json)
    return 0 if n["unknown"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
