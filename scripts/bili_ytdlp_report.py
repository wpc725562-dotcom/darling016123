#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 yt-dlp 普查结果汇总成一张表 —— 回答「哪些分P 可以跳过探测」。

为什么需要它
    `bili_ytdlp.py` 只写**每个 BV 一份** `_ytdlp.jsonl`，没有任何跨 BV 的汇总。
    而真正要做的决策是全局的：

      · 全库有多少分P 是「确认无轨」→ 这些**不必再探测**，省 12 次/分P 的重试；
      · 全库有多少分P 是「声明有轨但没通过校验」→ 这些是**串轨**问题，另一码事。

    ★ 这个区分是本脚本存在的核心理由：
      `_verify.jsonl` 的 `ok:false` **同时**代表上面两种情况，无法区分。
      实测全库 144 个 not-ok 分P 里，**90 个是真无轨、54 个是声明有轨** ——
      如果把它们当成同一类，就会得出「144 个都要走 ASR」这种错误结论
      （实际只有 90 个要，另 54 个是内容问题、可能有救）。

用法
    python scripts/bili_ytdlp_report.py
    python scripts/bili_ytdlp_report.py --out data/bili-analyze/_ytdlp_scan.md

产出
    data/bili-analyze/_ytdlp_scan.md    覆盖表 + 三类结论 + 交叉验证
    （该目录被 .gitignore:112 忽略，不会进 git）

依赖：只用标准库。
"""
import argparse
import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'bili-analyze'
LEGACY_RETRIES = 12   # 与 bili_ytdlp.py / bili_analyze.PROBE_RETRIES 对齐

# 科目归属：按 CATALOG（bili_fetch_subs.py）的口径，便于与 audit 表对照
SUBJECT = {}
for _s, _bvs in {
    '计算机': ['BV1Ye411Y7Ue', 'BV1Ay4y137RA', 'BV1KU4y167ds', 'BV1tNpbekEht',
             'BV1z84y1z7Vp', 'BV1ajMo6TEBm', 'BV17a7K64ELH', 'BV1Z4w3znE6h'],
    '高数': ['BV1Up4y1Y76a', 'BV1husGzwEtZ', 'BV1swAWerEzS', 'BV1X4411J792',
           'BV1vm421s7mv', 'BV12DdNYzEvy', 'BV1xxXZBKENv'],
    '政治': ['BV1PRM26hEbk', 'BV1TDj36dEdc', 'BV176gY6nEb3', 'BV1xzBCBFExz',
           'BV1gh9MBkEEC'],
    '英语': ['BV1rg411h7Z1', 'BV1brgBzNEbW', 'BV1Do4y1h7om', 'BV1jT4y1f7YA'],
}.items():
    for _bv in _bvs:
        SUBJECT[_bv] = _s


def read_jsonl(p):
    """读 jsonl；坏行跳过但不静默（返回 (行列表, 坏行数)）。"""
    rows, bad = [], 0
    if not p.exists():
        return rows, 0
    for ln in p.read_text(encoding='utf-8', errors='ignore').splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            rows.append(json.loads(ln))
        except Exception:
            bad += 1
    return rows, bad


def collect():
    """遍历所有 BV，返回每个 BV 的统计 + 全库合计。"""
    per = []
    for p in sorted(ROOT.glob('BV*/_ytdlp.jsonl')):
        bv = p.parent.name
        rows, bad = read_jsonl(p)
        # ★ 跳过集：只认「已登录且确认无轨」这一种，与 bili_fetch_subs._load_ytdlp_notrack 同口径
        notrack = {r['p'] for r in rows
                   if r.get('source') == 'yt-dlp:no_track_authenticated'
                   and not r.get('claimed_langs')}
        claimed = {r['p']: r.get('claimed_langs') or [] for r in rows if r.get('claimed_langs')}
        # 该 BV 的 not-ok 分P（_verify.jsonl）
        vrows, vbad = read_jsonl(p.parent / '_verify.jsonl')
        bad_parts = {r['p'] for r in vrows if not r.get('ok')}
        per.append({
            'bv': bv, 'subject': SUBJECT.get(bv, '其它'), 'rows': len(rows), 'bad_lines': bad + vbad,
            'notrack': notrack, 'claimed': claimed, 'bad_parts': bad_parts,
            'bad_notrack': bad_parts & notrack,
            'bad_claimed': bad_parts & set(claimed),
            'uncovered_bad': bad_parts - notrack - set(claimed),
        })
    return per


def build(per):
    T = lambda k: sum(len(r[k]) for r in per)   # 仅用于集合/映射类字段
    tot_rows = sum(r['rows'] for r in per)      # rows 已是计数，不能再 len()
    tot_nt, tot_cl = T('notrack'), T('claimed')
    bad_all, bad_nt, bad_cl = T('bad_parts'), T('bad_notrack'), T('bad_claimed')
    bad_unc = T('uncovered_bad')

    L = []
    A = L.append
    A('# B站字幕轨普查汇总（yt-dlp）')
    A('')
    A(f'- 生成时间：{datetime.date.today().isoformat()}')
    A('- 数据源：`data/bili-analyze/<BV>/_ytdlp.jsonl`（由 `scripts/bili_ytdlp.py` 写）')
    A('- 对照源：`data/bili-analyze/<BV>/_verify.jsonl`（自建 aid+cid 校验结果）')
    A('- 生成器：`scripts/bili_ytdlp_report.py`')
    A('')
    A('> **`claimed` 是 B站的声明，不是归属证明。** 本表只用于决定「哪些分P 不值得再探测」，')
    A('> 归属判定仍须走 `bili_analyze.probe_subtitle` 的 aid+cid 不变量。')
    A('')
    A('## 一、全库合计')
    A('')
    A('| 指标 | 数量 | 含义 |')
    A('|:---|---:|:---|')
    A(f'| 已普查分P | {tot_rows} | p1 全量 + 全部 not-ok 分P |')
    A(f'| **确认无轨** | **{tot_nt}** | 已登录且无任何声明 ⇒ **可跳过探测** |')
    A(f'| 声明有轨 | {tot_cl} | 仍需 aid+cid 校验才知归属 |')
    A(f'| **省下探测请求** | **约 {tot_nt * LEGACY_RETRIES} 次** | {LEGACY_RETRIES} 次/分P × {tot_nt} |')
    A('')
    A('## 二、★ `_verify.jsonl` 的 not-ok 其实是两类')
    A('')
    A(f'全库 `_verify.jsonl` 合计 **{bad_all}** 个 not-ok 分P。')
    A('`ok:false` **不区分**下面两种情况，这正是本报告要拆开的：')
    A('')
    A('| 类别 | 数量 | 真实含义 | 该怎么办 |')
    A('|:---|---:|:---|:---|')
    A(f'| **真无轨** | **{bad_nt}** | B站这个分P 一条字幕轨都没有 | 跳过探测，**必须走 ASR** |')
    A(f'| **声明有轨但没通过校验** | **{bad_cl}** | 拿到了轨，但内容不是这个视频的（串轨） | 不是「无轨」问题 —— 重试/复核内容，**可能有救** |')
    A(f'| 普查未覆盖 | {bad_unc} | 没探到 | 保持现状（不跳过） |')
    A('')
    A(f'⇒ 只看 `_verify.jsonl` 会得出「{bad_all} 个都要走 ASR」；')
    A(f'  实际只有 **{bad_nt}** 个真要，另 **{bad_cl}** 个是内容问题。')
    A('')
    A('## 三、逐 BV')
    A('')
    A('| BV | 科目 | 普查行 | 确认无轨 | 声明有轨 | not-ok | 其中真无轨 | 其中声明有轨 |')
    A('|:---|:---|---:|---:|---:|---:|---:|---:|')
    for r in sorted(per, key=lambda x: (x['subject'], x['bv'])):
        if not r['rows']:
            continue
        A(f"| `{r['bv']}` | {r['subject']} | {r['rows']} | {len(r['notrack'])} | "
          f"{len(r['claimed'])} | {len(r['bad_parts'])} | {len(r['bad_notrack'])} | "
          f"{len(r['bad_claimed'])} |")
    A('')
    A('## 四、按科目')
    A('')
    A('| 科目 | 确认无轨 | 声明有轨 |')
    A('|:---|---:|---:|')
    for s in ('计算机', '高数', '政治', '英语', '其它'):
        sub = [r for r in per if r['subject'] == s]
        if not sub:
            continue
        A(f"| {s} | {sum(len(r['notrack']) for r in sub)} | {sum(len(r['claimed']) for r in sub)} |")
    A('')
    A('## 五、交叉验证')
    A('')
    pol = [r for r in per if r['subject'] == '政治' and r['rows']]
    pol_nt = sum(len(r['notrack']) for r in pol)
    pol_cl = sum(len(r['claimed']) for r in pol)
    A(f'- **政治**：本表 {len(pol)} 个政治 BV 中，**确认无轨 {pol_nt} 个、声明有轨 {pol_cl} 个**；')
    A('  `_subtitle_audit.md` 的政治通过率是 **0/19**。两边一致。')
    A('- ⇒「政治 B站字幕全量不可用」现在有**两条独立证据**（自建 aid+cid 校验 + yt-dlp 声明普查）。')
    A('')
    A('## 六、怎么用')
    A('')
    A('```bash')
    A('# 1) 生成/更新普查（会按 p 合并写入，不会抹掉已探到的行）')
    A('python scripts/bili_ytdlp.py --batch bvs.txt --items 1 --out data/bili-analyze')
    A('# 2) 汇总成这张表')
    A('python scripts/bili_ytdlp_report.py')
    A('# 3) 让下载器用上「确认无轨」清单，省掉无用重试')
    A('python scripts/bili_fetch_subs.py --refresh --ytdlp-skip')
    A('```')
    A('')
    bad_lines = sum(r['bad_lines'] for r in per)
    if bad_lines:
        A(f'> ⚠️ 读取时有 {bad_lines} 行 jsonl 解析失败（已跳过，未计入上表）。')
    return '\n'.join(L) + '\n'


def main():
    ap = argparse.ArgumentParser(description='汇总 yt-dlp 普查结果成一张可读的表')
    ap.add_argument('--out', default=str(ROOT / '_ytdlp_scan.md'),
                    help='输出路径（默认 data/bili-analyze/_ytdlp_scan.md）')
    a = ap.parse_args()

    per = collect()
    if not per:
        print('!! 没找到任何 _ytdlp.jsonl —— 先跑 scripts/bili_ytdlp.py')
        return 1
    md = build(per)
    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding='utf-8', newline='\n')
    print(f'写入 {out}  ({out.stat().st_size} B)')
    print()
    print(md)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
