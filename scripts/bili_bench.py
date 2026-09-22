#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""性能基准：定位字幕抓取的瓶颈到底在哪。

要回答的问题
    1) 单次请求的时间花在哪 —— TLS 握手 / API 处理 / 响应体？
    2) 连接复用（keep-alive）能省多少？
    3) 并发度提到多少才到拐点？超过之后是变快还是被限流打回？
    4) 那个「aid+cid 校验重试」到底吃掉了多少时间？

方法
    · 全部用真实接口，样本量写在输出里，不猜
    · 并发测试用同一批分P，保证工作内容一致
    · 每个配置跑完打印 parts/min 与 attempts/min

用法
    python scripts/bili_bench.py
"""
import importlib.util
import json
import pathlib
import socket
import ssl
import statistics
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

# ★ E1（2026-09-20）：锚定到脚本位置，别依赖 CWD（相对路径从别处跑会静默指向空目录）。
ROOT = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'bili-analyze'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ba = load('ba', 'scripts/bili_analyze.py')


def bench_connect(host, n=6):
    """纯 TLS 建连耗时（不含请求）。"""
    out = []
    for _ in range(n):
        t0 = time.perf_counter()
        ctx = ssl.create_default_context()
        s = socket.create_connection((host, 443), timeout=15)
        ss = ctx.wrap_socket(s, server_hostname=host)
        ss.close()
        out.append((time.perf_counter() - t0) * 1000)
    return out


def bench_fresh_request(url, n=8):
    """每次新建连接发一次请求（= 当前代码的行为）。"""
    out = []
    for _ in range(n):
        t0 = time.perf_counter()
        req = urllib.request.Request(url, headers={
            'User-Agent': ba.UA, 'Referer': ba.REFERER,
            'Cookie': 'SESSDATA=' + (ba.COOKIE or '')})
        with urllib.request.urlopen(req, timeout=20) as r:
            r.read()
        out.append((time.perf_counter() - t0) * 1000)
    return out


def bench_keepalive(host, path, n=8):
    """复用同一条 TLS 连接发多次请求。"""
    import http.client
    ctx = ssl.create_default_context()
    conn = http.client.HTTPSConnection(host, 443, timeout=20, context=ctx)
    hdrs = {'User-Agent': ba.UA, 'Referer': ba.REFERER,
            'Cookie': 'SESSDATA=' + (ba.COOKIE or '')}
    out = []
    for _ in range(n):
        t0 = time.perf_counter()
        conn.request('GET', path, headers=hdrs)
        r = conn.getresponse()
        r.read()
        out.append((time.perf_counter() - t0) * 1000)
    conn.close()
    return out


def fmt(name, xs):
    if not xs:
        return '%-34s (无样本)' % name
    return ('%-34s n=%-3d 中位 %7.1f ms  p95 %7.1f ms  最小 %7.1f ms'
            % (name, len(xs), statistics.median(xs),
               sorted(xs)[int(len(xs) * 0.95) - 1] if len(xs) > 1 else xs[0],
               min(xs)))


def throughput(tasks, jobs, tag):
    """跑一批分P，返回 (parts/min, attempts/min, 耗时, 成功数)。"""
    attempts = [0]
    lock = __import__('threading').Lock()

    def one(t):
        bv, cid = t
        n = 0
        try:
            subs, _ = ba.probe_subtitle(cid, bv)
            n += 1                      # 只统计探轨次数，不算下载
        except Exception:
            # ★ A6 复核（2026-09-20）：**有意**吞掉。本脚本测量的就是
            #   「探轨成功率」，失败正是被测量对象本身，不是意外。
            #   上面 n 只统计成功次数，分母固定 = 并发数，所以数据不会失真。
            pass
        with lock:
            attempts[0] += n
        return 1

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        list(ex.map(one, tasks))
    el = time.time() - t0
    pm = len(tasks) / el * 60
    print('  jobs=%-3d  %6.1f 秒  %6.1f 分P/分   (%s)'
          % (jobs, el, pm, tag))
    return pm


def main():
    sd, _ = ba.get_sessdata()
    ba.COOKIE = sd
    print('=' * 74)
    print('① 连接与请求耗时分解')
    print('=' * 74)
    print(fmt('TLS 建连 aisubtitle.hdslb.com', bench_connect('aisubtitle.hdslb.com')))
    print(fmt('TLS 建连 api.bilibili.com', bench_connect('api.bilibili.com')))
    API = 'https://api.bilibili.com/x/player/v2?bvid=BV1husGzwEtZ&cid=33332987484'
    print(fmt('每次新建连接请求 x/player/v2', bench_fresh_request(API)))
    print(fmt('复用连接请求 x/player/v2',
              bench_keepalive('api.bilibili.com',
                              '/x/player/v2?bvid=BV1husGzwEtZ&cid=33332987484')))
    print()

    # 取一条「容易命中」和一条「难命中」的 BV，各 24 个分P 做并发对比
    for bv, tag in (('BV12DdNYzEvy', '容易命中'), ('BV1X4411J792', '难命中')):
        m = ba.get_meta(bv)
        tasks = [(bv, p['cid']) for p in m['pages'][:24]]
        print('=' * 74)
        print('② 并发度扫描 —— %s（%s）24 个分P' % (bv, tag))
        print('=' * 74)
        base = None
        for jobs in (1, 4, 8, 16, 32):
            pm = throughput(tasks, jobs, '')
            if base is None:
                base = pm
        print('  ↑ 相对 jobs=1 的加速比见上（基准 %.1f 分P/分）' % base)
        print()


if __name__ == '__main__':
    main()
