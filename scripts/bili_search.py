#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B站搜索（视频）—— 现有 bili_* 工具链缺的一环。

为什么需要它：`x/web-interface/search/type` 现在**必须带设备指纹**，否则 HTTP 412
（不是限流，也不是端点死了）。修法不是 wbi 签名，而是两个 cookie：buvid3 / buvid4，
从 `x/frontend/finger/spi` 免费拿，不需要登录。

用法：
    python bili_search.py "2021 广东专升本 英语 真题"
    python bili_search.py "关键词" --pages 1-3 --json out.json
    python bili_search.py "关键词" --check-login      # 顺带验证 SESSDATA

退出码：0 成功 / 2 需要登录（SESSDATA 无效）/ 3 被 412 拦（指纹没生效）/ 5 参数错
"""
from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
SESS_FILE = ROOT / ".bili-sessdata"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def load_sessdata() -> str:
    if not SESS_FILE.exists():
        return ""
    return SESS_FILE.read_text(encoding="utf-8").strip()


def api(url: str, cookie: str = "") -> dict:
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Referer": "https://www.bilibili.com/",
        "Accept": "application/json, text/plain, */*",
        **({"Cookie": cookie} if cookie else {}),
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def build_cookie(sess: str) -> tuple[str, str]:
    """返回 (cookie, 说明)。指纹拿不到就退化为只用 SESSDATA。"""
    try:
        spi = api("https://api.bilibili.com/x/frontend/finger/spi").get("data") or {}
        b3, b4 = spi.get("b_3", ""), spi.get("b_4", "")
    except Exception as e:
        b3 = b4 = ""
        note = f"指纹获取失败({e})，仅用 SESSDATA"
    else:
        note = f"指纹 OK (buvid3={b3[:8]}… buvid4={b4[:8]}…)"
    parts = []
    if sess:
        parts.append(f"SESSDATA={sess}")
    if b3:
        parts.append(f"buvid3={b3}")
    if b4:
        parts.append(f"buvid4={b4}")
    parts.append(f"b_nut={int(time.time())}")
    return "; ".join(parts), note


def check_login(cookie: str) -> tuple[bool, str]:
    try:
        d = api("https://api.bilibili.com/x/web-interface/nav", cookie)
    except Exception as e:
        return False, f"nav 调用失败: {e}"
    if d.get("code") != 0:
        return False, f"nav code={d.get('code')} {d.get('message')}"
    data = d.get("data") or {}
    return bool(data.get("isLogin")), (f"已登录 as {data.get('uname')}" if data.get("isLogin")
                                       else "未登录（SESSDATA 可能过期）")


def strip_tags(s: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def search(keyword: str, page: int, cookie: str) -> tuple[int, list[dict], str]:
    q = urllib.parse.urlencode({
        "search_type": "video", "keyword": keyword, "page": page, "page_size": 20,
    })
    url = f"https://api.bilibili.com/x/web-interface/search/type?{q}"
    try:
        d = api(url, cookie)
    except urllib.error.HTTPError as e:
        return e.code, [], f"HTTP {e.code}"
    if d.get("code") != 0:
        return d.get("code", -1), [], str(d.get("message"))
    out = []
    for it in ((d.get("data") or {}).get("result") or []):
        out.append({
            "bvid": it.get("bvid"),
            "title": strip_tags(it.get("title")),
            "author": it.get("author"),
            "play": it.get("play"),
            "favorites": it.get("favorites"),
            "duration": it.get("duration"),
            "pubdate": it.get("pubdate"),
            "description": strip_tags(it.get("description"))[:120],
        })
    return 0, out, ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("keyword")
    ap.add_argument("--pages", default="1", help="如 1 / 1-3")
    ap.add_argument("--json", help="把结果写到该路径")
    ap.add_argument("--check-login", action="store_true")
    a = ap.parse_args()

    if a.pages == "1":
        pages = [1]
    else:
        m = re.fullmatch(r"(\d+)-(\d+)", a.pages)
        if not m:
            print("--pages 格式应为 1 或 1-3", file=sys.stderr)
            return 5
        pages = list(range(int(m.group(1)), int(m.group(2)) + 1))

    sess = load_sessdata()
    cookie, note = build_cookie(sess)
    print(f"[cookie] {note}")
    if a.check_login:
        ok, msg = check_login(cookie)
        print(f"[login ] {msg}")

    all_hits: list[dict] = []
    for p in pages:
        code, hits, msg = search(a.keyword, p, cookie)
        if code == 412:
            print(f"[p{p}] HTTP 412 —— 指纹没生效（不是限流）", file=sys.stderr)
            return 3
        if code != 0:
            print(f"[p{p}] code={code} {msg}", file=sys.stderr)
            if code == -101:
                return 2
            continue
        all_hits.extend(hits)
        print(f"[p{p}] {len(hits)} 条")
        time.sleep(0.5)

    print(f"\n共 {len(all_hits)} 条：\n")
    for h in all_hits:
        print(f"  {h['bvid']}  {h['play']:>9} 播放  {h['duration']:>7}  "
              f"{(h['author'] or '')[:14]:<14}  {h['title'][:70]}")

    if a.json:
        pathlib.Path(a.json).write_text(
            json.dumps(all_hits, ensure_ascii=False, indent=2), encoding="utf-8",
            newline="\n")
        print(f"\n已写入 {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
