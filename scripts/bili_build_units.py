#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 `CATALOG`（`bili_fetch_subs.py`）里的视频字幕切片成「提炼工作单元」，供并行子代理消费。

为什么要预拼接
    语料**数百万字符**（专升本四科实测 848 万 / 含高考英语更多），远超单次上下文。
    走「分片提炼 → 合并」，但如果让子代理自己去逐个读**上千个** subtitle_pXX.txt，
    光工具调用就要几十次。所以这里先把每个单元拼成**一个文件**，子代理只读一次。

    ⚠️ 上面刻意**不写具体数字** —— 语料规模随 `CATALOG` 增长（24 → 141 支实测），
    写死数字的 docstring 每次扩课都会过期。要看现状就数一遍：
        ls data/bili-analyze/_extract/BV*.md | wc -l
        python scripts/bili_build_units.py --dry-run   # 会打印单元数与字符数

单元怎么切
    · 按视频切；单个视频超过 --max-chars（默认 100K）就继续拆成多个单元
    · 每个分P 前插一行 `=== P12 | 标题 | 158s ===`，保留结构信息
      —— 这一行很关键：子代理能据此判断「这一段的主题是什么」

产出
    data/bili-analyze/_units/<unit_id>.txt    单元正文
    data/bili-analyze/_units/_manifest.json   单元清单（科目/BV/分P范围/字符数）
    data/bili-analyze/_part_titles_all.json   全部分P 标题缓存

用法
    python scripts/bili_build_units.py
    python scripts/bili_build_units.py --max-chars 120000

    # ★ 导入单条新视频时用这组（别全量重跑，见下）
    python scripts/bili_build_units.py --bv BV18CL26WEJ3 --append

⚠️ 为什么导入新视频要 `--bv ... --append` 而不是全量重跑
    单元 id 是 `<bv>_<seq>`，而 `seq` 是**跨所有 BV 的全局自增序号**。
    往 CATALOG 中间插一条视频，它**之后**所有视频的 id 会整体位移；
    而 `_extract/<id>.md` 是按旧 id 命名的 ⇒ 下一轮提炼会把同一段内容写成新 id
    ⇒ 语料里出现**重复知识点**（旧 md 不会自动消失）。
    `--bv` 模式下序号按 BV 独立起算（`_01`、`_02`…），`--append` 只并进清单、不重写。
    全量模式已有 id 稳定性守卫会拦下位移并 exit 2，`--force` 可强制放行（确认旧产出可废弃时）。
"""
import argparse
import importlib.util
import json
import pathlib

# ★ E1（2026-09-20）：锚定到脚本位置，别依赖 CWD。
ROOT = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'bili-analyze'
UNITS = ROOT / '_units'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fs = load('fs', 'scripts/bili_fetch_subs.py')
ba = load('ba', 'scripts/bili_analyze.py')


def get_titles(bv):
    """取该视频所有分P 的标题。有缓存读缓存。"""
    cache = ROOT / '_part_titles_all.json'
    db = json.loads(cache.read_text(encoding='utf-8')) if cache.exists() else {}
    if bv in db:
        return db[bv]
    m = ba.get_meta(bv)
    db[bv] = {'title': m['title'], 'owner': m.get('owner', ''),
              'pages': [{'p': p['page'], 'part': p['part'],
                         'dur': p['duration']} for p in m['pages']]}
    cache.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding='utf-8', newline='\n')
    return db[bv]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-chars', type=int, default=100000,
                    help='单个单元的字符上限（默认 100K，约 13 万 token）')
    ap.add_argument('--bv', default=None,
                    help='只建这一条（或逗号分隔的多条）BV 的单元。'
                         '★ 与全量模式的关键差别：id 用**该 BV 内独立序号**（_01、_02…），'
                         '不用全局 seq。因为全局 seq 会随 CATALOG 顺序变化 —— '
                         '往 CATALOG 中间插一条视频，它之后所有视频的 unit id 会整体位移，'
                         '而 _extract/*.md 是按旧 id 命名的，'
                         '下一次提炼会把同一段内容写成新 id ⇒ 语料里出现重复知识点。')
    ap.add_argument('--append', action='store_true',
                    help='与 --bv 搭配：把新单元**追加**进 _manifest.json，而不是整体重写。'
                         '整体重写会丢掉本次没重跑的那些视频的条目。')
    ap.add_argument('--force', action='store_true',
                    help='跳过 id 稳定性守卫。★ 只有在你确认「旧 id 的 _extract 产出可以废弃」'
                         '时才用 —— 守卫拦的是「同一段字幕换了 id」，'
                         '放过去就是考点库里多一份重复知识点。')
    a = ap.parse_args()
    only = {x.strip() for x in a.bv.split(',')} if a.bv else None

    UNITS.mkdir(parents=True, exist_ok=True)
    manifest = []
    seq = 0

    for subject, bvs in fs.CATALOG.items():
        for bv in bvs:
            if only and bv not in only:
                continue
            bvdir = ROOT / bv
            if not bvdir.is_dir():
                continue
            try:
                info = get_titles(bv)
            except Exception as e:
                print('!! %s 取标题失败：%s' % (bv, e))
                continue
            by_p = {p['p']: p for p in info['pages']}

            # ★ --bv 模式：序号按 BV 重新起算，避免全局 seq 位移带来的 id 漂移
            if only:
                seq = 0

            buf, buf_pages, buf_chars = [], [], 0

            def flush():
                nonlocal seq, buf, buf_pages, buf_chars
                if not buf:
                    return
                seq += 1
                uid = '%s_%02d' % (bv, seq)
                (UNITS / ('%s.txt' % uid)).write_text(
                    '\n\n'.join(buf), encoding='utf-8', newline='\n')
                manifest.append({
                    'unit': uid, 'subject': subject, 'bv': bv,
                    'video_title': info['title'], 'owner': info.get('owner', ''),
                    'pages': list(buf_pages), 'chars': buf_chars,
                    'file': '_units/%s.txt' % uid,
                })
                buf, buf_pages, buf_chars = [], [], 0

            for p in sorted(by_p):
                f = bvdir / ('subtitle_p%02d.txt' % p)
                if not (f.exists() and f.stat().st_size > 0):
                    continue
                txt = f.read_text(encoding='utf-8', errors='ignore').strip()
                if not txt:
                    continue
                meta = by_p[p]
                head = '=== P%d | %s | %ds ===' % (p, meta['part'], meta['dur'])
                buf.append(head + '\n' + txt)
                buf_pages.append(p)
                buf_chars += len(txt) + len(head)
                if buf_chars >= a.max_chars:
                    flush()
            flush()

    # ── ★ id 稳定性守卫（2026-09-25）────────────────────────────────────
    # 单元 id 里嵌着**全局自增序号**（`<bv>_<seq>`），而 _extract/*.md 是按 id 命名的。
    # 于是往 CATALOG 中间插一条视频，它之后所有视频的 seq 会整体位移：
    # 同一段字幕拿到**新 id**，而旧 id 的 md 还躺在 _extract/ 里 ⇒ 语料里出现重复知识点。
    # 这个故障全程静默（没有报错、没有非零退出），所以在落盘前拦一道：
    # 把「新旧清单里同 id 但分P 区间/所属 BV 不同」的挑出来，默认拒绝写入。
    old_manifest = None
    if (UNITS / '_manifest.json').exists():
        try:
            old_manifest = json.loads((UNITS / '_manifest.json').read_text(encoding='utf-8'))
            if not isinstance(old_manifest, list):
                raise ValueError('manifest 不是 list')
        except Exception as e:
            print('!! 旧 _manifest.json 读取失败（%s），跳过 id 稳定性检查' % e)
            old_manifest = None

    if old_manifest is not None:
        oldmap = {m['unit']: m for m in old_manifest
                  if isinstance(m, dict) and 'unit' in m}
        drift = []
        for m in manifest:
            o = oldmap.get(m['unit'])
            if o and (o.get('pages') != m['pages'] or o.get('bv') != m['bv']):
                drift.append((m['unit'], o.get('bv'), o.get('pages'), m['bv'], m['pages']))
        if drift and not a.force:
            print('❌ 单元 id 位移：%d 个既有 id 被重新分配给了不同的分P 区间' % len(drift))
            for uid, ob, op, nb, nps in drift[:10]:
                print('   %-24s 旧 %s %s   →   新 %s %s' % (uid, ob, op, nb, nps))
            if len(drift) > 10:
                print('   … 另有 %d 个' % (len(drift) - 10))
            print()
            print('   _extract/<id>.md 已按旧编号命名，再提炼一次会把同一段内容写成新 id，')
            print('   ⇒ 考点库里出现重复知识点（旧 md 不会自动消失）。')
            print('   处置：① 用 --bv 逐条建单元（按 BV 独立编号，不影响任何其它视频）；或')
            print('         ② 确认旧 id 的产出可以废弃，再加 --force 强制落盘。')
            raise SystemExit(2)
        if drift:
            print('⚠️ --force：明知 %d 个 id 位移仍继续' % len(drift))
        else:
            print('id 稳定性检查通过：%d 个既有 id 的分P 区间未变'
                  % len(set(oldmap) & {m['unit'] for m in manifest}))

    # ★ --bv --append：只把本次新单元并进清单，保留其它视频已有条目
    if a.append and old_manifest is not None:
        have = {m['unit'] for m in old_manifest}
        added = [m for m in manifest if m['unit'] not in have]
        manifest = old_manifest + added
        print('清单追加：新增 %d 条，原有 %d 条' % (len(added), len(old_manifest)))

    (UNITS / '_manifest.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding='utf-8', newline='\n')

    import collections
    print('单元总数 %d' % len(manifest))
    c = collections.Counter(m['subject'] for m in manifest)
    cc = collections.Counter()
    for m in manifest:
        cc[m['subject']] += m['chars']
    print()
    print('%-6s %6s %12s' % ('科目', '单元数', '字符数'))
    for s in ('计算机', '高数', '政治', '英语'):
        print('%-6s %6d %12d' % (s, c[s], cc[s]))
    print('%-6s %6d %12d' % ('合计', len(manifest), sum(cc.values())))
    print()
    print('=== 单元清单 ===')
    for m in manifest:
        pg = m['pages']
        rng = 'P%d' % pg[0] if len(pg) == 1 else 'P%d–P%d' % (pg[0], pg[-1])
        print('  %-22s %-5s %-10s %7d 字符  %s'
              % (m['unit'], m['subject'], rng, m['chars'], m['video_title'][:26]))


if __name__ == '__main__':
    main()
