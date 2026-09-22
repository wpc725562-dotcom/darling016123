#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B站资源清单存活巡检 —— 扫 markdown 里的 BV 号，逐个核验是否还能看。

为什么需要它：
    BV 号是永久标识，但**视频会下架**。`code=62002 稿件不可见` 说明稿件被删、
    转私密或过审撤回。清单页写着「均可在 B站直接播放」，一旦有死链，那句话就是假的
    —— 而读者（包括未来的自己）不会知道，只会点进去看到 404。

用法：
    python scripts/bili_audit_links.py                       # 默认扫 docs/guide/bili-resources.md
    python scripts/bili_audit_links.py docs/guide/*.md       # 扫多个文件
    python scripts/bili_audit_links.py --json out.json       # 顺便落一份机器可读结果
    python scripts/bili_audit_links.py --timeout 40          # 网络慢时放宽

退出码：0 = 全部可访问；1 = 存在失效链接（方便接进 CI/巡检机器人）。

零第三方依赖，只用标准库。请求间隔 0.4s，不打扰人家接口。
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
import time
import urllib.error
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
REFERER = "https://www.bilibili.com/"
VIEW = "https://api.bilibili.com/x/web-interface/wbi/view?bvid={}"

BV_RE = re.compile(r"BV[0-9A-Za-z]{10}")

# 常见业务码 → 人话
CODE_HINT = {
    62002: "稿件不可见（已下架 / 转私密 / 被撤回）",
    62004: "稿件审核中",
    -404: "啥都木有（BV 号不存在或已彻底删除）",
    -403: "访问权限不足（可能需要登录）",
}


def probe(bvid, timeout=25):
    """返回 dict(status, code, message, title, pages, view)。"""
    req = urllib.request.Request(VIEW.format(bvid),
                                 headers={"User-Agent": UA, "Referer": REFERER})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"status": "http_error", "code": e.code,
                "message": f"HTTP {e.code}（412 通常是风控，重试或降速）"}
    except Exception as e:  # noqa: BLE001 — 网络层什么都能抛，统一收敛成一条结果
        return {"status": "exception", "code": None, "message": str(e)}

    if d.get("code") != 0:
        c = d.get("code")
        return {"status": "dead", "code": c,
                "message": f"{d.get('message')}"
                           + (f" —— {CODE_HINT[c]}" if c in CODE_HINT else "")}
    x = d["data"]
    return {"status": "ok", "code": 0, "message": "OK",
            "title": x.get("title", ""),
            "owner": (x.get("owner") or {}).get("name", ""),
            "pages": len(x.get("pages") or [1]),
            "duration": x.get("duration", 0),
            "view": ((x.get("stat") or {}).get("view"))}


def collect(files):
    """从 markdown 里抽 (文件, 行号, 行首单元名, bv)。"""
    out = []
    for f in files:
        try:
            text = open(f, encoding="utf-8").read()
        except OSError as e:
            print(f"!! 读不了 {f}：{e}")
            continue
        for i, line in enumerate(text.splitlines(), 1):
            bvs = BV_RE.findall(line)
            if not bvs:
                continue
            name = ""
            s = line.strip()
            if s.startswith("|"):
                cells = [c.strip() for c in s.strip("|").split("|")]
                name = cells[0] if cells else ""
            for bv in bvs:
                out.append((f, i, name, bv))
    return out


def main():
    ap = argparse.ArgumentParser(description="巡检 markdown 里 B站 BV 号的存活情况")
    ap.add_argument("files", nargs="*",
                    default=["docs/guide/bili-resources.md"],
                    help="要扫的文件（默认 docs/guide/bili-resources.md）")
    ap.add_argument("--json", default=None, help="把结果也写成 JSON")
    ap.add_argument("--timeout", type=int, default=25)
    ap.add_argument("--interval", type=float, default=0.4)
    a = ap.parse_args()

    files = []
    for pat in a.files:
        files.extend(sorted(glob.glob(pat)) or [pat])
    files = list(dict.fromkeys(files))

    items = collect(files)
    if not items:
        print("没找到任何 BV 号。")
        return 0

    print(f"扫描 {len(files)} 个文件，共 {len(items)} 个 BV 号\n")
    results, dead = [], []
    for f, ln, name, bv in items:
        r = probe(bv, a.timeout)
        r.update(file=f, line=ln, name=name, bvid=bv)
        results.append(r)
        if r["status"] == "ok":
            print(f"  ✓ {bv}  {r['title'][:44]}  | {r['pages']}P")
        else:
            print(f"  ✗ {bv}  [{r['code']} {r['message']}]")
            print(f"      {f}:{ln}  {name[:56]}")
            dead.append(r)
        time.sleep(a.interval)

    ok = len(results) - len(dead)
    print(f"\n=== {ok}/{len(results)} 可访问，{len(dead)} 条失效 ===")
    for r in dead:
        print(f"  {r['bvid']}  {r['file']}:{r['line']}  {r['name'][:48]}")

    if a.json:
        with open(a.json, "w", encoding="utf-8", newline="\n") as fh:
            json.dump({"checked": len(results), "ok": ok, "dead": dead,
                       "all": results}, fh, ensure_ascii=False, indent=2)
        print(f"\nJSON → {a.json}")

    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
