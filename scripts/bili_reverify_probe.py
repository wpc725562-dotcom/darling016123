#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""决定性实验：`_verify.jsonl` 标 ok=false 的分P，内容到底是不是这个视频的？

背景
----
`bili_fetch_subs.py` 用「subtitle_url 里含 str(aid)+str(cid)」当不变量，
通过则写 `{"p":N,"ok":true}`，否则 `ok:false`。
但抽查 `BV1X4411J792`（学士帽 专升本高数）发现 **ok=false 的页里混着正确内容**：
  p58 凑微分 ✓ / p59 擦桌子 ✗ / p60 分部积分 ✓ / p61 沙漠种水稻 ✗ / p62 定积分 ✓
所以「ok=false」不等于「内容错」——需要量化假阴性率。

本脚本做什么
------------
对指定分P **重复探轨 N 次**，每次都打印：
  · 请求的 cid vs 响应里的 data.cid / data.aid
  · 每条纹的 URL 尾部（含 aid+cid 的那段）
  · 不变量是否命中
一旦命中，就**下载该轨并与磁盘上的 subtitle_pNN.txt 对比**（长度 + 前 80 字）。
若命中轨的内容 == 磁盘内容 → 磁盘文件其实是对的，是**假阴性**。
"""
import argparse
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bili_analyze as ba  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "bili-analyze")


def tail(url, n=46):
    if not url:
        return "(空)"
    return "…" + url[-n:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bv", required=True)
    ap.add_argument("--pages", required=True, help="逗号分隔，如 58,59,60,61,62")
    ap.add_argument("--probes", type=int, default=8, help="每页探轨次数（默认 8）")
    ap.add_argument("--no-download", action="store_true")
    args = ap.parse_args()

    pages_wanted = [int(x) for x in args.pages.split(",") if x.strip()]
    meta = ba.get_meta(args.bv)
    by_page = {p["page"]: p for p in meta["pages"]}

    print("视频：%s" % meta.get("title"))
    print("aid=%s  分P数=%d" % (meta.get("aid"), len(meta["pages"])))
    print("=" * 78)

    for pno in pages_wanted:
        pg = by_page.get(pno)
        if not pg:
            print("P%d 不存在，跳过" % pno)
            continue
        cid = pg["cid"]
        disk = os.path.join(DATA, args.bv, "subtitle_p%02d.txt" % pno)
        disk_txt = ""
        if os.path.exists(disk):
            with io.open(disk, encoding="utf-8") as fh:
                disk_txt = fh.read()
        print("\n### P%d  「%s」  cid=%s" % (pno, pg.get("part", ""), cid))
        print("    磁盘文件：%s  %d 字" %
              ("存在" if disk_txt else "缺失", len(disk_txt)))
        print("    磁盘开头：%s" % disk_txt[:70].replace("\n", " / "))

        hit_url = None
        for i in range(args.probes):
            try:
                d = ba.api("https://api.bilibili.com/x/player/v2?bvid=%s&cid=%s"
                           % (args.bv, cid))
            except Exception as e:
                print("    探%d 异常：%s" % (i + 1, e))
                continue
            if d.get("code") != 0:
                print("    探%d code=%s" % (i + 1, d.get("code")))
                continue
            data = d.get("data") or {}
            subs = ((data.get("subtitle") or {}).get("subtitles")) or []
            r_aid, r_cid = data.get("aid"), data.get("cid")
            key = "%s%s" % (r_aid, r_cid)
            mark = []
            for s in subs:
                u = s.get("subtitle_url") or s.get("subtitleUrl") or ""
                ok = bool(u) and (key in u)
                mark.append("命中" if ok else "未中")
                if ok and hit_url is None:
                    hit_url = u
            print("    探%d aid=%s cid=%s(请求%s) 轨=%d [%s] %s" %
                  (i + 1, r_aid, r_cid, cid, len(subs), ",".join(mark),
                   tail(subs[0].get("subtitle_url") if subs else "")))
            if hit_url:
                break

        if hit_url and not args.no_download:
            try:
                txt = ba.srt_to_text(hit_url)
            except Exception as e:
                print("    下载命中轨失败：%s" % e)
                continue
            same = txt.strip() == disk_txt.strip()
            print("    ★ 命中轨 %d 字；与磁盘内容 %s" %
                  (len(txt), "【完全一致 → 假阴性！】" if same else "【不同】"))
            print("      命中轨开头：%s" % txt[:70].replace("\n", " / "))
        elif not hit_url:
            print("    ✗ %d 次探测都没命中 aid+cid 不变量" % args.probes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
