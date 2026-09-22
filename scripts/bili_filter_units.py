#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 `_units/*.txt` 过滤成「只含已校验分P」的干净语料，供知识点提炼使用。

为什么必须过滤
--------------
B 站 `x/player/v2` 接口有 ~68% 概率返回**别的视频**的字幕轨（详见
skill `bilibili-video-capture` §3c 与 `docs/guide/bili-subtitle-pipeline-perf.md`）。
`bili_fetch_subs.py` 用 `aid+cid` 不变量校验后，把结论写进 `<BV>/_verify.jsonl`
（每行 `{"p": N, "ok": true|false}`）。

实测分布很不均匀：24 支视频里有 6 支**整支**未校验（含一支 51 分P 的），
另有 1 支只有前半段校验通过。所以「未校验」不是零星撒在各单元里，
而是**整块整块地集中**——这让过滤很有效，但也意味着几个单元会整体报废。

用法
----
    python scripts/bili_filter_units.py                 # 生成 _units_verified/
    python scripts/bili_filter_units.py --min-keep 0.3  # 保留率低于此值的单元直接丢弃
    python scripts/bili_filter_units.py --dry-run       # 只出报告，不写文件
    python scripts/bili_filter_units.py --no-override   # 忽略人工覆写，只看机器判定

判定顺序
--------
    1. `_verify2.jsonl` 有该分P  -> 用它的 ok（`bili_reclassify_unverified.py` 产出）
    2. 否则 `_verify.jsonl` 有   -> 用它的 ok（aid+cid 不变量，确定性但会误杀）
    3. 都没有                    -> 不可信，剔除
    4. 最后叠加 `_manual_verify_override.json` 的人工覆写（**只能置 True**）
"""
import argparse
import collections
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "bili-analyze")
UNITS_DIR = os.path.join(DATA, "_units")
OUT_DIR = os.path.join(DATA, "_units_verified")
OVERRIDE_PATH = os.path.join(DATA, "_manual_verify_override.json")

# 形如：=== P12 | 标题文字 | 158s ===
BLOCK_RE = re.compile(r"^=== P(\d+) \|.*?===\s*$")


def load_overrides():
    """读人工覆写表 -> {bv: {page: int -> 证据说明}}。文件不存在返回 {}。

    表结构见 `_manual_verify_override.json`；以 `_` 开头的键是说明字段，跳过。

    ★ 为什么需要它：`bili_reclassify_unverified.py` 的自动判别拿 `ov >= 0.50`
      （标题词在正文里的重合率）当硬门槛，而这道门槛在**「习题讲解」类分P**上
      系统性失效 —— 标题写「5.9 幂级数练习题讲解」，正文却是口语化的
      「我们来看练习，求这个密集数它的收敛半径」（ASR 把「幂」写成「密」），
      标题词一个都对不上，ov 掉到 0.14。但它的 `cos` 是 0.40，远高于真垃圾
      （多在 0.00–0.33）。2026-09-21 逐页读原文核出 6 个这样的假阴性。

      **只加这个人工入口，不动自动规则** —— 规则注释里已有误捞的标定记录
      （BV1X4411J792 P89，cos=0.551 刚过线，内容是德州靶场），随手放宽门槛
      会把这类页一起放进来，引入新的假阳性。
    """
    if not os.path.exists(OVERRIDE_PATH):
        return {}
    try:
        with io.open(OVERRIDE_PATH, encoding="utf-8") as fh:
            raw = json.load(fh)
    except ValueError as exc:
        print("⚠️  覆写表解析失败，已忽略：%s" % exc, file=sys.stderr)
        return {}
    out = {}
    for bv, pages in raw.items():
        if bv.startswith("_") or not isinstance(pages, dict):
            continue
        try:
            out[bv] = dict((int(p), str(why)) for p, why in pages.items())
        except (TypeError, ValueError):
            print("⚠️  覆写表 %s 的页号非数字，已忽略该视频。" % bv, file=sys.stderr)
    return out


def load_verify(bv):
    """读校验记录 -> {page: bool}。文件不存在返回 {}（= 全部不可信）。

    ★ 优先用 `_verify2.jsonl`（`bili_reclassify_unverified.py` 产出）。
      原因：`_verify.jsonl` 的 ok:false **不等于内容错** —— 实测 BV1X4411J792
      的 P58/P60/P62 内容与该分P标题完全对应，却因 URL 没匹配上不变量而被标 false。
      只按 `_verify.jsonl` 过滤会误删约 19 个正确分P（正好是高数第 3–7 章）。

    ★ 本函数**只读磁盘记录，不含人工覆写**；覆写由 `main()` 叠加，见 `load_overrides()`。
      这样拆开是为了能在报告里如实区分「校验通过」与「人工捞回」两类页。
    """
    for name, key in (("_verify2.jsonl", "ok"), ("_verify.jsonl", "ok")):
        path = os.path.join(DATA, bv, name)
        if not os.path.exists(path):
            continue
        res = {}
        with io.open(path, encoding="utf-8") as fh:
            for ln in fh:
                ln = ln.strip()
                if not ln:
                    continue
                try:
                    rec = json.loads(ln)
                except ValueError:
                    continue
                if "p" in rec:
                    res[int(rec["p"])] = bool(rec.get(key))
        return res
    return {}


def split_blocks(text):
    """把单元文本切成 [(header, body), ...]。header 前的散落行归入前一块。"""
    blocks = []
    cur = None
    for ln in text.split("\n"):
        if BLOCK_RE.match(ln):
            cur = [ln, []]
            blocks.append(cur)
        elif cur is not None:
            cur[1].append(ln)
    return [(h, "\n".join(b)) for h, b in blocks]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-keep", type=float, default=0.30,
                    help="保留率低于此值的单元直接丢弃（默认 0.30）")
    ap.add_argument("--dry-run", action="store_true", help="只出报告不写文件")
    ap.add_argument("--no-override", action="store_true",
                    help="忽略 _manual_verify_override.json 的人工覆写（用于对照/回归）")
    args = ap.parse_args()

    overrides = {} if args.no_override else load_overrides()
    if overrides:
        n_ov = sum(len(v) for v in overrides.values())
        print("人工覆写表：%d 个视频 / %d 个分P（%s）"
              % (len(overrides), n_ov, os.path.basename(OVERRIDE_PATH)))
    elif not args.no_override:
        print("人工覆写表：无（未找到 %s）" % os.path.basename(OVERRIDE_PATH))
    else:
        print("人工覆写表：已按 --no-override 忽略")

    with io.open(os.path.join(UNITS_DIR, "_manifest.json"), encoding="utf-8") as fh:
        manifest = json.load(fh)

    verify_cache = {}
    kept_manifest = []
    dropped = []
    stat = collections.Counter()
    ov_kept_all = []          # [(unit, [page, ...]), ...] 只记真正靠覆写捞回的页

    print("=" * 78)
    print("单元过滤报告（保留 _verify2/_verify 里 ok=true 的分P + 人工覆写）")
    print("=" * 78)
    print("%-22s %-5s %6s %6s %6s %7s  %s" %
          ("unit", "学科", "原P数", "留P数", "丢P数", "字符", "结论"))
    print("-" * 78)

    for u in manifest:
        bv = u["bv"]
        if bv not in verify_cache:
            verify_cache[bv] = load_verify(bv)
        vmap = verify_cache[bv]
        ov_map = overrides.get(bv, {})

        with io.open(os.path.join(UNITS_DIR, os.path.basename(u["file"])),
                     encoding="utf-8") as fh:
            text = fh.read()
        blocks = split_blocks(text)

        kept_blocks = []
        lost = []
        ov_kept = []
        for header, body in blocks:
            page = int(BLOCK_RE.match(header).group(1))
            trusted = bool(vmap.get(page, False))
            if trusted or page in ov_map:
                kept_blocks.append((header, body))
                if not trusted:          # 校验没过、靠人工覆写留下
                    ov_kept.append(page)
            else:
                lost.append(page)

        n_all = len(blocks)
        n_keep = len(kept_blocks)
        ratio = (n_keep / n_all) if n_all else 0.0

        if n_keep == 0 or ratio < args.min_keep:
            dropped.append((u["unit"], u["subject"], n_all, n_keep, sorted(lost)))
            verdict = "丢弃(保留率%.0f%%)" % (ratio * 100)
            print("%-22s %-5s %6d %6d %6d %7s  %s" %
                  (u["unit"], u["subject"], n_all, n_keep, n_all - n_keep,
                   "-", verdict))
            stat["dropped_units"] += 1
            stat["dropped_blocks"] += n_all
            continue

        out_lines = [
            "# unit: %s" % u["unit"],
            "# 学科: %s" % u["subject"],
            "# 视频: %s（%s）" % (u["video_title"], u["owner"]),
            "# 已校验分P: %d/%d（已剔除未校验分P：%s）" %
            (n_keep, n_all, ",".join(map(str, sorted(lost))) or "无"),
            "# ⚠️ 本文件只含 aid+cid 校验通过的分P，内容可信。",
        ]
        if ov_kept:
            out_lines.append(
                "# 人工覆写分P: %s（自动判别判 junk，已逐页读原文核实为正确；"
                "见 _manual_verify_override.json）" % ",".join(map(str, sorted(ov_kept))))
        out_lines.append("")
        for header, body in kept_blocks:
            out_lines.append(header)
            out_lines.append(body)

        kept_text = "\n".join(out_lines)
        kept_pages = [int(BLOCK_RE.match(h).group(1)) for h, _ in kept_blocks]

        if not args.dry_run:
            os.makedirs(OUT_DIR, exist_ok=True)
            with io.open(os.path.join(OUT_DIR, u["unit"] + ".txt"), "w",
                         encoding="utf-8", newline="\n") as fh:
                fh.write(kept_text)

        kept_manifest.append({
            "unit": u["unit"],
            "subject": u["subject"],
            "bv": bv,
            "video_title": u["video_title"],
            "owner": u["owner"],
            "pages": kept_pages,
            "dropped_pages": sorted(lost),
            "override_pages": sorted(ov_kept),
            "chars": len(kept_text),
            "file": "_units_verified/%s.txt" % u["unit"],
        })

        stat["kept_units"] += 1
        stat["kept_blocks"] += n_keep
        stat["override_blocks"] += len(ov_kept)
        stat["kept_chars"] += len(kept_text)
        stat["lost_chars"] += (u["chars"] - len(kept_text))
        if ov_kept:
            ov_kept_all.append((u["unit"], sorted(ov_kept)))
        verdict = "保留 %.0f%%" % (ratio * 100)
        if ov_kept:
            verdict += "（含覆写 %d）" % len(ov_kept)
        print("%-22s %-5s %6d %6d %6d %7d  %s" %
              (u["unit"], u["subject"], n_all, n_keep, n_all - n_keep,
               len(kept_text), verdict))

    if not args.dry_run:
        with io.open(os.path.join(OUT_DIR, "_manifest.json"), "w",
                     encoding="utf-8", newline="\n") as fh:
            json.dump(kept_manifest, fh, ensure_ascii=False, indent=1)

    print("-" * 78)
    print("保留单元 %d 个 / 丢弃 %d 个" % (stat["kept_units"], stat["dropped_units"]))
    print("分P：留 %d / 丢 %d" % (stat["kept_blocks"], stat["dropped_blocks"]))
    if stat["override_blocks"]:
        print("其中人工覆写捞回 %d 个分P：" % stat["override_blocks"])
        for unit, pages in ov_kept_all:
            print("  - %s：%s" % (unit, ",".join(map(str, pages))))
    elif not args.no_override:
        print("人工覆写：本次未捞回任何分P（覆写页可能已被上游判 trusted，或不在任何单元内）")
    print("字符：留 %d / 丢约 %d（%.1f%% 保留）" %
          (stat["kept_chars"], stat["lost_chars"],
           100.0 * stat["kept_chars"] / max(1, stat["kept_chars"] + stat["lost_chars"])))
    by_subj = collections.Counter(u["subject"] for u in kept_manifest)
    print("按学科：%s" % dict(by_subj))
    if dropped:
        print("\n丢弃的单元（整支视频未校验）：")
        for unit, subj, n_all, n_keep, lost in dropped:
            print("  - %s（%s）%d 分P 全丢" % (unit, subj, n_all))
    if args.dry_run:
        print("\n[dry-run] 未写文件。")
    else:
        print("\n已写出 -> %s" % OUT_DIR)
    return 0


if __name__ == "__main__":
    sys.exit(main())
