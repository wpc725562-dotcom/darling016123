#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 `bili_probe_parts` / `bili_probe_courses` 留下的 `unknown` 分P**二次定性**。

为什么需要这个脚本
------------------
`probe()` 判 `has` 用的不变量是「`subtitle_url` 里含 `str(aid)+str(cid)`」。
但 B站 的字幕 URL 有**三种形态**，只有第一种满足该不变量：

  A  `//aisubtitle.hdslb.com/bfs/ai_subtitle/prod/{aid}{cid}{hash}`
        → 命中不变量 → `has`。**正常情况。**

  B  `//aisubtitle.hdslb.com/bfs/ai_subtitle/prod/{32位hash}`
        → 裸 hash，不含 aid+cid ⇒ 探针判 `unknown`。
        但 `ai_status=2`、`lan=ai-zh`，**多半是它自己的 AI 轨**，只是命名不合规。
        ⇒ **不能当无字幕用**，必须取正文验证。（2026-09-24 实测：阿飞 P5 = 5198 字，
          内容与标题「日语的声调」严丝合缝；同 aid 的 P8 正文 md5 与之不同，
          证明不是「同 aid 别的分P」的串轨。）

  C  `//aisubtitle.hdslb.com/bfs/subtitle/{40位hash}.json`
        → 旧轨，`ai_status=0`，通常只有 **1 条空句**（0 字）或几个乱码字符。
        ⇒ 占位空轨，**等同无可用字幕**。（实测：阿飞 P11 = 0 字、P45 = 6 字、周业繁 P74 = 32 字。）

也就是说 `unknown` 把「真字幕被漏掉」和「空壳轨」混成了一类。
本脚本按形态分流，再**取正文按字数定夺**，把 `unknown` 收敛成 has / none。

判据
----
  形态 A / B + 正文 ≥ MIN_CHARS  → has   （有可用字幕）
  形态 A / B + 正文 <  MIN_CHARS  → none  （残缺轨 / 只够开头几秒）
  形态 C                          → none  （占位空轨，无论字数）
  取正文失败 / 无轨列表为空        → 保持 unknown（不臆断）

用法
----
  # 直接给分P
  python scripts/bili_resolve_unknown.py --bv BV1Bp4y1D747 --pages 5,11,45,109

  # 从普查 JSON 里自动读出所有 unknown 分P
  python scripts/bili_resolve_unknown.py --from-census jp-census.json --out resolved.json

  # 带阳性对照（强烈建议：证明这一轮的登录态与取正文链路是好的）
  python scripts/bili_resolve_unknown.py --bv BV1Bp4y1D747 --pages 5 --control BV1Bp4y1D747:3
"""
import argparse
import json
import pathlib
import random
import sys
import time
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import bili_probe_parts as P  # noqa: E402

MIN_CHARS = 200  # 低于此字数视为「残缺轨」，等同无可用字幕


def url_form(url):
    """返回 (形态代号, 说明)。"""
    if "/ai_subtitle/prod/" in url:
        seg = url.split("/ai_subtitle/prod/")[1].split("?")[0]
        # A 形态的 path 以 aid+cid 开头（纯数字），B 形态是 32 位裸 hash
        if len(seg) >= 32 and seg[:9].isdigit():
            return "A", "ai_subtitle/prod/{aid}{cid}{hash}（命中不变量）"
        return "B", "ai_subtitle/prod/{hash}（裸 hash，需取正文定夺）"
    if "/bfs/subtitle/" in url:
        return "C", "bfs/subtitle/{hash}.json（旧轨，多为占位空壳）"
    return "?", "未识别的 URL 形态"


def fetch_body(url, timeout=25, attempts=3):
    """取字幕正文。**必须带重试** —— 实测 hdslb 会偶发
    `SSL: UNEXPECTED_EOF_WHILE_READING`，一次失败就把分P 留成「未定」是不必要的。"""
    if url.startswith("//"):
        url = "https:" + url
    h = {"User-Agent": P.UA, "Referer": "https://www.bilibili.com/"}
    if P.SESSDATA:
        h["Cookie"] = "SESSDATA=%s" % P.SESSDATA
    last = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers=h)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:
            last = e
            time.sleep(0.8 + random.random() * 1.2)
    raise last


def resolve_one(bv, pno, cid):
    """返回 dict。state ∈ {has, none, unknown}。"""
    d = P.api("https://api.bilibili.com/x/player/wbi/v2?bvid=%s&cid=%s" % (bv, cid))
    data = d.get("data") or {}
    subs = ((data.get("subtitle") or {}).get("subtitles")) or []
    if not subs:
        return {"state": "unknown", "detail": "轨列表为空（应由 probe 判 none，不该走到这里）"}

    out = []
    for s in subs:
        u = s.get("subtitle_url") or ""
        form, note = url_form(u)
        rec = {"form": form, "form_note": note, "lan": s.get("lan"),
               "ai_status": s.get("ai_status")}
        if not u:
            rec.update({"state": "unknown", "detail": "subtitle_url 为空（瞬时故障）"})
            out.append(rec)
            continue
        try:
            raw = fetch_body(u)
            cues = (json.loads(raw.decode("utf-8")).get("body")) or []
            text = "".join(c.get("content", "") for c in cues)
            rec.update({"bytes": len(raw), "cues": len(cues), "chars": len(text),
                        "first": (cues[0].get("content") if cues else "")[:60]})
            if form == "C":
                rec.update({"state": "none",
                            "detail": "占位空轨（旧轨形态），正文 %d 字" % len(text)})
            elif len(text) >= MIN_CHARS:
                rec.update({"state": "has", "detail": "有可用字幕，正文 %d 字" % len(text)})
            else:
                rec.update({"state": "none",
                            "detail": "残缺轨，正文仅 %d 字（< %d）" % (len(text), MIN_CHARS)})
        except Exception as e:
            rec.update({"state": "unknown",
                        "detail": "取正文失败: %s: %s" % (type(e).__name__, e)})
        out.append(rec)

    # 任一条可用即算 has
    states = [r["state"] for r in out]
    state = "has" if "has" in states else ("none" if all(s == "none" for s in states) else "unknown")
    return {"state": state, "tracks": out}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bv")
    ap.add_argument("--pages", help="如 5,11,45-47")
    ap.add_argument("--from-census", help="普查 JSON；自动读出其中所有 unknown 分P")
    ap.add_argument("--control", help="阳性对照，形如 BV1Bp4y1D747:3")
    ap.add_argument("--out", default="resolved-unknown.json")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

    ok, uname = P.check_login()
    print("登录: %s  uname=%s" % (ok, uname))
    print("凭据来源: %s" % P.SRC)
    if not ok:
        raise SystemExit("未登录 —— 结果无意义，直接中止（不要把它当成「没字幕」）")

    # 组装任务：[(label, bv, [pages])]
    tasks = []
    if args.from_census:
        data = json.load(open(args.from_census, encoding="utf-8"))
        for c in data:
            pgs = c.get("unknownPages") or []
            if pgs:
                tasks.append((c["label"], c["bv"], pgs))
    elif args.bv:
        if not args.pages:
            raise SystemExit("给了 --bv 就必须给 --pages")
        tasks.append((args.bv, args.bv, P.parse_pages(args.pages, 10 ** 6)))
    else:
        raise SystemExit("需要 --bv 或 --from-census")

    if args.control:
        cbv, cpno = args.control.split(":")
        tasks.insert(0, ("阳性对照", cbv, [int(cpno)]))

    results = []
    for label, bv, pgs in tasks:
        _, _, pages = P.get_pages(bv)
        by = {pg["page"]: pg for pg in pages}
        print("\n" + "=" * 80)
        print("%s  %s" % (label, bv))
        print("=" * 80)
        for pno in pgs:
            pg = by.get(pno)
            if not pg:
                print("P%-5s 分P不存在" % pno)
                continue
            r = resolve_one(bv, pno, pg["cid"])
            head = {"has": "✓ 有可用", "none": "✗ 无可用", "unknown": "? 仍未定"}[r["state"]]
            print("P%-5s %-9s %s" % (pno, head, pg.get("part", "")[:34]))
            for t in r.get("tracks", []):
                print("        形态%s  lan=%-8s ai_status=%-3s %s" % (
                    t["form"], t.get("lan"), t.get("ai_status"), t["form_note"]))
                if "chars" in t:
                    print("        正文 %6d 字节 / %4d 条 / %5d 字  首句=%r"
                          % (t["bytes"], t["cues"], t["chars"], t.get("first", "")))
                print("        → %s" % t["detail"])
            results.append({"label": label, "bv": bv, "p": pno,
                            "part": pg.get("part"), "state": r["state"],
                            "tracks": r.get("tracks", [])})

    print("\n" + "=" * 80)
    n = {s: sum(1 for r in results if r["state"] == s) for s in ("has", "none", "unknown")}
    print("小结: has=%d  none=%d  unknown=%d" % (n["has"], n["none"], n["unknown"]))
    if n["unknown"]:
        print("仍未定（需人工看）: " + ", ".join(
            "%s P%s" % (r["label"], r["p"]) for r in results if r["state"] == "unknown"))
    json.dump(results, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("已写入 %s" % args.out)


if __name__ == "__main__":
    main()
