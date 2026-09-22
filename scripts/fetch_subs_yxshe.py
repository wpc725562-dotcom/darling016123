#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""定向抓取「研习社-小李来了 · 日语0-N1全套」(BV14T4y1Y78G) 的字幕。

为什么单独写一个：
    该视频不在 scripts/bili_fetch_subs.py 的 CATALOG（那是专升本四科的清单）。
    而它**是本站唯一含 N1 精讲的日语视频源** —— 阿飞老师那条止于中级第 21 课。
    所以 N1 阶段要「从视频提炼」，只能靠这一条。

抓取范围（默认）：
    143-168  饼干老师《标日中上》第 1-16 课
    169-176  N2 精讲 8 次课
    177-184  N1 精讲 8 次课

用法：
    python scripts/fetch_subs_yxshe.py --pages 143-184
    python scripts/fetch_subs_yxshe.py --pages 177-184 --jobs 4

★ 坑：bili_analyze 的模块级 COOKIE 只在它自己的 main() 里赋值。
   import 后不设置它 ⇒ probe_subtitle 不带 cookie ⇒ 全部误报「无字幕」。
"""
import argparse
import importlib.util
import pathlib
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
OUT_ROOT = REPO / 'data' / 'bili-analyze'
BV = 'BV14T4y1Y78G'


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ba = _load('ba', HERE / 'bili_analyze.py')
bfs = _load('bfs', HERE / 'bili_fetch_subs.py')
bfs.ba = ba                      # 让 fetch_one 用的是同一个 ba 实例

ck, src = ba.get_sessdata(None)
if not ck:
    sys.exit('✗ 没有 SESSDATA，无法取 AI 字幕。先跑 scripts/bili_login.py')
ba.COOKIE = ck                   # ★ 关键：不加这行，探测全部返回「无字幕」
print(f'SESSDATA 已加载（{src}）')


def parse_pages(spec_str, total):
    want = set()
    for chunk in spec_str.split(','):
        chunk = chunk.strip()
        if not chunk:
            continue
        if '-' in chunk:
            a, b = chunk.split('-', 1)
            want.update(range(int(a), int(b) + 1))
        else:
            want.add(int(chunk))
    return [p for p in sorted(want) if 1 <= p <= total]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pages', default='143-184')
    ap.add_argument('--jobs', type=int, default=4)
    ap.add_argument('--sleep', type=float, default=0.15)
    args = ap.parse_args()

    meta = ba.get_meta(BV) or {}
    pages = meta.get('pages') or []
    if not pages:
        sys.exit('✗ 拿不到分P 列表')
    by_no = {p['page']: p for p in pages}
    target = parse_pages(args.pages, len(pages))
    outdir = OUT_ROOT / BV
    outdir.mkdir(parents=True, exist_ok=True)

    todo = []
    for pno in target:
        p = by_no.get(pno)
        if not p:
            continue
        outfile = outdir / f'subtitle_p{pno:02d}.txt'
        if outfile.exists() and outfile.stat().st_size > 200:
            continue                      # 已有且非空 —— 跳过（幂等）
        todo.append((p, outfile))

    print(f'目标分P {len(target)} 个，其中待下载 {len(todo)} 个，并发 {args.jobs}\n')
    if not todo:
        print('没有待下载的分P。')
        return

    lock = threading.Lock()
    done = 0

    def work(item):
        nonlocal done
        p, outfile = item
        r = bfs.fetch_one('日语', BV, p, outfile, args.sleep)
        with lock:
            done += 1
            mark = {'hit': '✓', 'miss': '－', 'fail': '✗'}.get(r, '?')
            print(f'[{done}/{len(todo)}] {mark} P{p["page"]:>3} '
                  f'{r:<4} :: {p.get("part")}', flush=True)
        return r

    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs = [ex.submit(work, it) for it in todo]
        for f in as_completed(futs):
            f.result()

    print('\n=== 汇总 ===')
    print(f'命中 {bfs._HIT} / 无字幕 {bfs._MISS} / 失败 {bfs._FAIL} / 可疑 {bfs._SUSPECT}')
    if bfs._MISS_LIST:
        print('无字幕分P：', ' '.join(sorted(bfs._MISS_LIST)))
    if bfs._FAIL_LIST:
        print('失败分P：')
        for x in bfs._FAIL_LIST:
            print('  ', x)
    if bfs._SUSPECT_LIST:
        print('⚠️ 可疑（未通过 aid+cid 不变量）：', ' '.join(bfs._SUSPECT_LIST))


if __name__ == '__main__':
    main()
