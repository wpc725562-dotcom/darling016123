#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A/B 实测：重试次数与重试抖动对「难命中」视频耗时的影响。

为什么单独做这个实验
    真实运行数据里，吞吐完全由「未校验率」决定：
        未校验 1%  → 76 分P/分
        未校验 19% → 32 分P/分
        未校验 54% → 15 分P/分
    说明瓶颈是**重试尾巴**：命中率为 0 的分P 会跑满 PROBE_RETRIES 次，
    每次还要睡 PROBE_SLEEP 秒。**旧默认**（40 次 × 0.3–0.8 秒）下一个「没字幕」
    的分P 要花 ~26 秒，而正常分P 只要 ~0.25 秒 —— 差 100 倍。
    ★ 2026-09-19 默认值已改为 12 / (0.05,0.15)，单分P 实测降到 2.50 秒。

    所以这里在同一批「已知难命中」的分P 上跑三组配置，量出真实差距。

用法
    python scripts/bili_bench_retry.py
"""
import importlib.util
import pathlib
import statistics
import time
from concurrent.futures import ThreadPoolExecutor

# ★ E1（2026-09-20）：锚定到脚本位置，别依赖 CWD。
ROOT = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'bili-analyze'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ba = load('ba', 'scripts/bili_analyze.py')

# 这批分P 是实测「未通过 aid+cid 校验」的（BV1X4411J792 P52–P91），
# 也就是最坏情况：有轨但拿不到正确的那个。
HARD_BV = 'BV1X4411J792'
HARD_PAGES = [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 65, 66, 67, 68, 69,
              70, 71, 72, 73, 74, 75, 77, 78, 80, 88, 89, 90, 91, 109]


def run(tasks, retries, sleep, jobs, tag):
    ba.PROBE_RETRIES = retries
    ba.PROBE_SLEEP = sleep
    hits = [0]
    import threading
    lk = threading.Lock()

    def one(t):
        try:
            subs, _ = ba.probe_subtitle(t[1], t[0], retries=retries)
        except Exception:
            # ★ A6 复核（2026-09-20）：**有意**吞掉。本脚本比较的是
            #   「不同 retries 下的成功率」，失败即被测量对象。
            return
        if subs and subs[0].get('_verified'):
            with lk:
                hits[0] += 1

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        list(ex.map(one, tasks))
    el = time.time() - t0
    print('  %-40s %6.1f 秒   校验通过 %2d/%d   每分P %5.2f 秒'
          % (tag, el, hits[0], len(tasks), el / len(tasks)))
    return el, hits[0]


def main():
    sd, _ = ba.get_sessdata()
    ba.COOKIE = sd
    m = ba.get_meta(HARD_BV)
    by = {p['page']: p['cid'] for p in m['pages']}
    tasks = [(HARD_BV, by[p]) for p in HARD_PAGES if p in by]
    print('样本：%s 的 %d 个「难命中」分P（全部实测过未通过校验）' % (HARD_BV, len(tasks)))
    print()
    print('=' * 82)
    print('%-42s %8s %12s %12s' % ('配置', '耗时', '通过', '每分P'))
    print('=' * 82)
    base = None
    rows = []
    # ★ 2026-09-19：bili_analyze.py 的默认值已改为 12 / (0.05,0.15)，
    #   所以 A / D 组现在是「历史对照」，不再代表现状。
    #   保留它们，是为了让这张表可复现地分离出每个变量的单独贡献。
    for retries, sleep, jobs, tag in [
        (40, (0.30, 0.80), 6, 'A 旧默认：retries=40 sleep=0.3-0.8 jobs=6'),
        (12, (0.05, 0.15), 6, 'B 只调参：retries=12 sleep=0.05-0.15 jobs=6'),
        (12, (0.05, 0.15), 24, 'C 再提并发：retries=12 jobs=24'),
        (40, (0.05, 0.15), 6, 'D 只去睡：retries=40 sleep=0.05-0.15 jobs=6'),
    ]:
        el, h = run(tasks, retries, sleep, jobs, tag)
        rows.append((tag, el, h))
        if base is None:
            base = el
    print()
    print('相对 A 的加速：')
    for tag, el, h in rows[1:]:
        print('  %-42s %.1fx' % (tag[:42], base / el))
    print()
    print('注：B/C 会漏掉一些分P（本轮拿不到正确轨），漏的靠下一轮 --refresh 补；')
    print('    这里的取舍是「一轮跑快 3-15 倍、多跑一两轮」vs「一轮就尽量收全但很慢」。')


if __name__ == '__main__':
    main()
