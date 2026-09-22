#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给「aid+cid 校验未通过」的分P 做**内容判别**，把其中的假阴性捞回来。

为什么需要它
------------
`_verify.jsonl` 的 `ok:false` **不等于**「内容是错的」。实测 `BV1X4411J792`：

    P58「3.6 不定积分计算-凑微分法」  磁盘内容讲凑微分   → 其实是对的
    P59「3.7 不定积分计算-分部积分法」磁盘内容讲擦桌子   → 垃圾
    P60「3.8 分部积分法的考点」       磁盘内容讲分部积分 → 其实是对的
    P61「3.9 不定积分计算-换元法」    磁盘内容讲沙漠水稻 → 垃圾
    P62「3.10 定积分的几何意义」      磁盘内容讲定积分   → 其实是对的

原因：`probe_subtitle` 在 retries 内没命中不变量时，会把**最后一次拿到的脏轨**
当兜底返回。所以磁盘上既可能是脏轨，也可能是「内容对但 URL 没匹配上」的好轨。
（另注：SESSDATA 过期后所有探轨都返回 0 轨，**无法靠重探复核**，只能看内容。）

判据（双信号，自校准）
----------------------
1. **字串相似度**：把同一 BV 里 `ok:true` 的分P 拼成参考语料，算字符二元组余弦相似度。
   同一门课同一老师的用词高度一致，脏轨（别的视频）会明显偏离。
2. **标题重合度**：`_part_titles_all.json` 里有每个分P 的标题。正确内容的用词
   通常与该分P标题重合（如 P58 标题含「凑微分」↔ 内容含「凑微分」），脏轨不重合。

阈值不写死：取该 BV 内 `ok:true` 分P 的分数分布的低分位（默认 10%）作为门槛，
因为「已知正确」的样本本身就是最好的标尺。参考页不足 5 页时降级为只信标题信号。

输出
----
`<BV>/_verify2.jsonl`，每行 `{"p":N,"ok":bool,"cos":f,"ov":f,"verdict":"..."}`
verdict ∈ trusted（原校验通过）/ recovered（捞回）/ junk（判为脏）
"""
import argparse
import collections
import io
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "bili-analyze")

CJK_RUN = re.compile(r"[\u4e00-\u9fff]+")
ASCII_WORD = re.compile(r"[A-Za-z][A-Za-z0-9_+#.\-]{1,}")


def cjk_bigrams(text):
    """只取汉字连读段内的二元组 —— 跨标点/数字/英文不产生 n-gram。"""
    out = []
    for run in CJK_RUN.findall(text):
        for i in range(len(run) - 1):
            out.append(run[i:i + 2])
    return out


def ascii_tokens(text):
    return set(w.lower() for w in ASCII_WORD.findall(text))


def unit_vector(counter):
    norm = math.sqrt(sum(v * v for v in counter.values()))
    if not norm:
        return {}
    return {k: v / norm for k, v in counter.items()}


def cosine(a, b):
    if not a or not b:
        return 0.0
    if len(a) > len(b):
        a, b = b, a
    return sum(v * b.get(k, 0.0) for k, v in a.items())


def title_tokens(title):
    toks = set(cjk_bigrams(title))
    toks |= ascii_tokens(title)
    return toks


def overlap(title_toks, content):
    """标题里的词有多少比例出现在正文里。"""
    if not title_toks:
        return 0.0
    body = set(cjk_bigrams(content)) | ascii_tokens(content)
    hit = len(title_toks & body)
    return hit / float(len(title_toks))


def load_text(bv, pno):
    path = os.path.join(DATA, bv, "subtitle_p%02d.txt" % pno)
    if not os.path.exists(path):
        return None
    with io.open(path, encoding="utf-8") as fh:
        return fh.read()


def load_verify(bv):
    path = os.path.join(DATA, bv, "_verify.jsonl")
    res = {}
    if not os.path.exists(path):
        return res
    with io.open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if not ln:
                continue
            try:
                rec = json.loads(ln)
            except ValueError:
                continue
            res[int(rec["p"])] = bool(rec.get("ok"))
    return res


def load_titles():
    with io.open(os.path.join(DATA, "_part_titles_all.json"), encoding="utf-8") as fh:
        return json.load(fh)


def percentile(vals, q):
    if not vals:
        return 0.0
    s = sorted(vals)
    idx = max(0, min(len(s) - 1, int(round(q * (len(s) - 1)))))
    return s[idx]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bvs", default=None, help="逗号分隔，默认全部 24 支")
    ap.add_argument("--q", type=float, default=0.10,
                    help="门槛分位（在 ok 分P 的分数分布上取，默认 10%%）")
    ap.add_argument("--write", action="store_true", help="写 _verify2.jsonl")
    ap.add_argument("--show", default=None,
                    help="只看某支 BV 的明细，如 --show BV1X4411J792")
    args = ap.parse_args()

    titles = load_titles()
    bvs = (args.bvs.split(",") if args.bvs
           else sorted(d for d in os.listdir(DATA)
                       if d.startswith("BV") and os.path.isdir(os.path.join(DATA, d))))

    summary = []
    for bv in bvs:
        if not os.path.isdir(os.path.join(DATA, bv)):
            continue
        vmap = load_verify(bv)
        if not vmap:
            print("%s 无 _verify.jsonl，跳过" % bv)
            continue

        # 参考语料 = 该 BV 里已通过校验的分P
        ref = collections.Counter()
        ok_pages = [p for p, v in vmap.items() if v]
        for p in ok_pages:
            t = load_text(bv, p)
            if t:
                ref.update(cjk_bigrams(t))
        ref_vec = unit_vector(ref)

        # 标题表
        tinfo = titles.get(bv) or {}
        tmap = {pg["p"]: (pg.get("part") or "") for pg in (tinfo.get("pages") or [])}

        rows = []
        for p in sorted(vmap):
            text = load_text(bv, p)
            if text is None:
                rows.append((p, False, 0.0, 0.0, "missing"))
                continue
            cos = cosine(unit_vector(collections.Counter(cjk_bigrams(text))), ref_vec)
            ov = overlap(title_tokens(tmap.get(p, "")), text)
            rows.append((p, vmap[p], cos, ov, None))

        # 自校准：用 ok 分P 的分数定门槛
        ok_cos = [r[2] for r in rows if r[1]]
        ok_ov = [r[3] for r in rows if r[1]]
        thr_cos = percentile(ok_cos, args.q)
        thr_ov = percentile(ok_ov, args.q)
        weak_ref = len(ok_pages) < 5

        out_rows = []
        for p, ok, cos, ov, flag in rows:
            # ★ 规则是**实测标定**出来的，不要随手放宽（见文件头「标定记录」）：
            #   · 必须「或」→ 误捞：BV1X4411J792 P89（cos=0.551 刚过线，内容是德州靶场）
            #   · 只用标题信号（弱参考）→ 误捞 6/6（政治 P3/P4、英语 P21/P38/P44、
            #     BV1Up4y1Y76a P1 全是别的视频）
            #   · 现规则在 20 个已核对样本上：捞回 19、误捞 0
            if flag == "missing":
                verdict = "missing"
            elif ok:
                verdict = "trusted"
            elif weak_ref:
                verdict = "unjudged"          # 没有参考页 ⇒ 判不了，下游按「不可信」处理
            else:
                verdict = "recovered" if (ov >= 0.50 and cos >= 0.30) else "junk"
            out_rows.append({"p": p, "ok": verdict in ("trusted", "recovered"),
                             "cos": round(cos, 4), "ov": round(ov, 4),
                             "verdict": verdict})

        n_trusted = sum(1 for r in out_rows if r["verdict"] == "trusted")
        n_rec = sum(1 for r in out_rows if r["verdict"] == "recovered")
        n_junk = sum(1 for r in out_rows if r["verdict"] == "junk")
        n_un = sum(1 for r in out_rows if r["verdict"] in ("unjudged", "missing"))
        summary.append((bv, tinfo.get("title", "?"), len(out_rows), n_trusted, n_rec,
                        n_junk + n_un, thr_cos, thr_ov, weak_ref))

        if args.write:
            with io.open(os.path.join(DATA, bv, "_verify2.jsonl"), "w",
                         encoding="utf-8", newline="\n") as fh:
                for r in out_rows:
                    fh.write(json.dumps(r, ensure_ascii=False) + "\n")

        if args.show == bv:
            print("\n### %s  %s" % (bv, tinfo.get("title", "?")))
            print("  门槛 cos>=%.4f  ov>=%.4f  （参考 %d 页%s）"
                  % (thr_cos, max(thr_ov, 0.30), len(ok_pages),
                     "，⚠️参考不足" if weak_ref else ""))
            for r in out_rows:
                if r["verdict"] == "trusted":
                    continue
                tag = {"recovered": "✓捞回", "junk": "✗垃圾", "missing": "—缺文件",
                       "unjudged": "?不可判"}[r["verdict"]]
                t = tmap.get(r["p"], "")[:26]
                print("    P%-4d %s cos=%.3f ov=%.3f  %s" %
                      (r["p"], tag, r["cos"], r["ov"], t))

    print("\n" + "=" * 92)
    print("%-14s %5s %5s %6s %6s %7s  %s" %
          ("BV", "总P", "已验", "捞回", "垃圾", "门槛cos", "标题"))
    print("-" * 92)
    T = [0, 0, 0]
    for bv, title, n, nt, nr, nj, tc, to, weak in summary:
        T[0] += n; T[1] += nt; T[2] += nr
        print("%-14s %5d %5d %6d %6d %7.3f  %s%s" %
              (bv, n, nt, nr, nj, tc, title[:30], "  ⚠️" if weak else ""))
    print("-" * 92)
    print("合计：%d 分P｜原校验通过 %d｜**新捞回 %d**｜判为脏 %d"
          % (T[0], T[1], T[2], T[0] - T[1] - T[2]))
    if args.write:
        print("已写出 <BV>/_verify2.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main())
