#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""课程级**全量**分P字幕普查：一次跑多门课，产出可写进文档的汇总表。

与 `bili_probe_parts.py` 的分工
------------------------------
`bili_probe_parts.py` 探**一个** BV 的**指定**分P范围（做抽样 / 复核单点）。
本脚本探**一组**课程，且默认**全量**（该 BV 的所有分P），并把结果汇总成表。

为什么要「全量」而不是抽样
--------------------------
抽样只能证明「抽到的那些没有」，证不出「全都没有」。一门 100P 的课抽 6 个
返回 0，完全可能是那 6 个恰好落在没做字幕的章节 —— 这种「0」写进文档就是
**不可证伪的结论**。要么全量，要么在文档里明确写「抽样，未定」。
（同一条教训见 skill `bilibili-video-capture` 的阳性对照一节。）

自动重跑
--------
`unknown`（异常 / code!=0 / 串轨）不是结论。全部跑完后，脚本会把这些分P
**单独再跑一轮**（间隔更长），仍为 unknown 的才如实保留。

用法
----
  # 课程清单写在 JSON 里（见 --list 的格式说明）
  python scripts/bili_probe_courses.py --list courses.json --out result.json

  # 或临时用命令行给几门
  python scripts/bili_probe_courses.py --bv BV1hK4y1S7hz:小昊子 --bv BV1j741167og:周业繁

  # 只探指定范围（复用本脚本的重跑与汇总能力）
  python scripts/bili_probe_courses.py --bv BV14T4y1Y78G:研习社 --pages 169-184

清单 JSON 格式：
  [{"label": "小昊子", "bv": "BV1hK4y1S7hz"}, ...]
"""
import argparse
import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import bili_probe_parts as B          # noqa: E402  （复用凭据 / 登录校验 / probe）


def load_courses(args):
    out = []
    if args.list:
        data = json.loads(pathlib.Path(args.list).read_text(encoding="utf-8"))
        for it in data:
            out.append((it.get("label") or it["bv"], it["bv"]))
    for spec in args.bv or []:
        if ":" in spec:
            bv, label = spec.split(":", 1)
            out.append((label, bv))
        else:
            out.append((spec, spec))
    return out


def probe_all(bv, pages_spec, total):
    """返回 rows。unknown 项不在这里重跑，交给 main 统一处理。"""
    wanted = B.parse_pages(pages_spec, total)
    rows = []
    for pno in wanted:
        rows.append({"p": pno})
    return wanted


def main():
    # 行缓冲：本脚本要跑十几分钟，若输出被重定向到文件，Python 默认块缓冲（8KB）
    # 会让进度**完全不可见**（实测：19 分钟的普查全程 0 字节日志）。
    # 在这里强制行缓冲，就不必要求调用方记得加 -u。
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--list", help="课程清单 JSON")
    ap.add_argument("--bv", action="append", help="BV 或 BV:标签，可重复")
    ap.add_argument("--pages", default="1-9999",
                    help="分P范围，默认全量（1-9999，超出部分自动丢弃）")
    ap.add_argument("--out", help="汇总结果写到这个 JSON 路径")
    ap.add_argument("--attempts", type=int, default=4)
    args = ap.parse_args()

    courses = load_courses(args)
    if not courses:
        print("没有课程。用 --list 或 --bv 指定。")
        return 2

    print("凭据来源: %s" % B.SRC)
    print("凭据长度: %d" % len(B.SESSDATA or ""))
    if not B.SESSDATA:
        print("✗ 没有凭据 —— AI 字幕是登录门控的，本次结果无意义。中止。")
        return 2
    ok, uname = B.check_login()
    print("登录态: isLogin=%s uname=%s" % (ok, uname))
    if not ok:
        print("✗ 未登录 —— 空结果会伪装成「没字幕」。中止，别下结论。")
        return 2

    report = []
    for label, bv in courses:
        print("\n" + "=" * 78)
        try:
            title, owner, pages = B.get_pages(bv)
        except SystemExit as e:
            print("✗ %s (%s) 元数据失败: %s" % (label, bv, e))
            report.append({"label": label, "bv": bv, "error": str(e)})
            continue

        total = len(pages)
        wanted = B.parse_pages(args.pages, total)
        by_page = {p["page"]: p for p in pages}
        print("%s  |  %s  |  %s" % (label, bv, title[:44]))
        print("UP主: %s   总分P: %d   本次探: %d" % (owner, total, len(wanted)))

        rows = []
        for pno in wanted:
            pg = by_page.get(pno)
            if not pg:
                continue
            state, detail = B.probe(pg["cid"], bv, args.attempts)
            mark = {"has": "✓", "none": "✗", "unknown": "?"}[state]
            print("  P%-5d %s %-40s %s" % (pno, mark, (pg.get("part") or "")[:40], detail))
            rows.append({"p": pno, "part": pg.get("part"),
                         "cid": pg["cid"], "state": state, "detail": detail})
            time.sleep(0.3)

        # ---- 未定项单独重跑一轮（更长间隔）----
        retry = [r for r in rows if r["state"] == "unknown"]
        if retry:
            print("  ↻ 重跑 %d 个未定项…" % len(retry))
            for r in retry:
                time.sleep(1.2)
                state, detail = B.probe(r["cid"], bv, attempts=5)
                if state != "unknown":
                    print("    P%-5d 重跑后 → %s  %s" % (r["p"], state, detail))
                    r["state"], r["detail"] = state, detail
                    r["retried"] = True

        n = {s: sum(1 for r in rows if r["state"] == s) for s in ("has", "none", "unknown")}
        has_pages = [r["p"] for r in rows if r["state"] == "has"]
        unk_pages = [r["p"] for r in rows if r["state"] == "unknown"]
        print("  ── 有轨 %d / 无轨 %d / 未定 %d  （共探 %d）" % (n["has"], n["none"], n["unknown"], len(rows)))
        report.append({
            "label": label, "bv": bv, "title": title, "owner": owner,
            "totalPages": total, "probed": len(rows),
            "has": n["has"], "none": n["none"], "unknown": n["unknown"],
            "hasPages": has_pages, "unknownPages": unk_pages,
            "full": len(rows) == total,
            "rows": rows,
        })

    print("\n" + "=" * 78)
    print("汇总（has = 有字幕轨的分P数）")
    print("%-14s %-6s %6s %6s %6s %6s %s" % ("课程", "分P", "探到", "有轨", "无轨", "未定", "是否全量"))
    for r in report:
        if r.get("error"):
            print("%-14s  ERROR %s" % (r["label"], r["error"]))
            continue
        print("%-14s %-6d %6d %6d %6d %6d %s" % (
            r["label"], r["totalPages"], r["probed"], r["has"], r["none"], r["unknown"],
            "全量" if r["full"] else "⚠ 部分"))

    bad = sum(1 for r in report if not r.get("error") and r["unknown"])
    if bad:
        print("\n⚠ 有 %d 门课存在未定项 —— 未定不等于无轨，别写进结论。" % bad)

    if args.out:
        pathlib.Path(args.out).write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print("结果已写入 %s" % args.out)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
