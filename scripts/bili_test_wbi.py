#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试：`x/player/wbi/v2`（WBI 签名版）能不能绕开「返回别的视频字幕轨」的问题。

背景
    实测 `x/player/v2` 对同一个 cid 会随机返回**别的视频**的字幕轨，命中率约 20%。
    加 `aid+cid` 不变量校验后能把正确轨挑出来，但**约 9% 的分P 反复试也拿不到**
    （BV1rg411h7Z1 的 51 个、BV1X4411J792 的 45 个）。

    怀疑：不带 WBI 签名的请求走的是另一条（可能被缓存污染的）代码路径。
    B站 对 `x/web-interface/view` 就要求必须用 `wbi/view`，否则 412。

    WBI 签名算法（公开、稳定）：
        img_key + sub_key  →  按固定置换表重排  →  取前 32 位 = mixin_key
        w_rid = md5(按 key 排序后的 query 串 + mixin_key)
        请求要带 wts=<当前秒级时间戳>

用法
    python scripts/bili_test_wbi.py
"""
import hashlib
import importlib.util
import json
import pathlib
import random
import sys
import time
import urllib.parse

MIXIN_TAB = [46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43,
             5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16,
             24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59,
             6, 63, 57, 62, 11, 36, 20, 34, 44, 52]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ba = load('ba', 'scripts/bili_analyze.py')


def get_mixin_key():
    """取 wbi 的 mixin_key。缓存到 data/bili-analyze/_wbi_key.json（当天有效）。"""
    cache = pathlib.Path('data/bili-analyze/_wbi_key.json')
    if cache.exists():
        o = json.loads(cache.read_text(encoding='utf-8'))
        if o.get('date') == time.strftime('%Y-%m-%d'):
            return o['mixin']
    nav = ba.api('https://api.bilibili.com/x/web-interface/nav')
    wbi = (nav.get('data') or {}).get('wbi_img') or {}
    img = (wbi.get('img_url') or '').rsplit('/', 1)[-1].split('.')[0]
    sub = (wbi.get('sub_url') or '').rsplit('/', 1)[-1].split('.')[0]
    raw = img + sub
    mixin = ''.join(raw[i] for i in MIXIN_TAB)[:32]
    cache.write_text(json.dumps({'date': time.strftime('%Y-%m-%d'),
                                 'mixin': mixin}, ensure_ascii=False),
                     encoding='utf-8', newline='\n')
    return mixin


def wbi_sign(params, mixin):
    """给参数表加上 wts 与 w_rid。"""
    p = dict(params)
    p['wts'] = int(time.time())
    # 过滤 !'()* 这几个字符，然后按 key 排序拼 query
    items = sorted((k, ''.join(c for c in str(v) if c not in "!'()*"))
                   for k, v in p.items())
    q = urllib.parse.urlencode(items)
    p['w_rid'] = hashlib.md5((q + mixin).encode()).hexdigest()
    return p


def probe_wbi(cid, bvid, mixin):
    """用 WBI 签名请求 x/player/wbi/v2，返回 (aid, cid, [轨])。"""
    p = wbi_sign({'bvid': bvid, 'cid': cid}, mixin)
    url = 'https://api.bilibili.com/x/player/wbi/v2?' + urllib.parse.urlencode(p)
    d = ba.api(url)
    if d.get('code') != 0:
        raise RuntimeError('code=%s msg=%s' % (d.get('code'), d.get('message')))
    data = d.get('data') or {}
    return (data.get('aid'), data.get('cid'),
            ((data.get('subtitle') or {}).get('subtitles')) or [])


def main():
    sd, _ = ba.get_sessdata()
    ba.COOKIE = sd
    mixin = get_mixin_key()
    print('mixin_key 取到（%d 位）' % len(mixin))
    print()

    # 这 6 个 cid 是用旧端点反复试都拿不到正确轨的
    CASES = [('BV1rg411h7Z1', 1), ('BV1rg411h7Z1', 3), ('BV1rg411h7Z1', 5),
             ('BV1X4411J792', 52), ('BV1X4411J792', 60), ('BV1X4411J792', 90),
             ('BV1PRM26hEbk', 1), ('BV1xzBCBFExz', 1), ('BV1husGzwEtZ', 13)]
    print('=' * 78)
    print('%-16s %5s %10s %10s %8s' % ('BV', 'P', 'wbi 命中', '旧端点命中', '结论'))
    print('=' * 78)
    total_err = [0]      # ★ A6：探测抛异常的次数（≠ 未命中）
    for bv, pno in CASES:
        m = ba.get_meta(bv)
        pg = [p for p in m['pages'] if p['page'] == pno][0]
        cid = pg['cid']
        # wbi 端点试 8 次
        wbi_ok = 0
        wbi_err = 0
        old_err = 0
        aid_ok = None
        for _ in range(8):
            try:
                aid, rc, subs = probe_wbi(cid, bv, mixin)
            except Exception:
                wbi_err += 1          # ★ A6：原来静默 continue，见下方注释
                continue
            key = '%s%s' % (aid, rc)
            if subs and any(key in (s.get('subtitle_url') or '') for s in subs):
                wbi_ok += 1
                aid_ok = aid
        # 旧端点试 8 次
        old_ok = 0
        for _ in range(8):
            try:
                d = ba.api('https://api.bilibili.com/x/player/v2?bvid=%s&cid=%s' % (bv, cid))
            except Exception:
                old_err += 1
                continue
            data = d.get('data') or {}
            key = '%s%s' % (data.get('aid'), data.get('cid'))
            subs = ((data.get('subtitle') or {}).get('subtitles')) or []
            if subs and any(key in (s.get('subtitle_url') or '') for s in subs):
                old_ok += 1
        verdict = ('★ wbi 明显更好' if wbi_ok > old_ok else
                   'wbi 更好' if wbi_ok > 0 and old_ok == 0 else
                   '两者差不多' if wbi_ok == old_ok else '旧端点更好')
        # ★ A6（2026-09-20）：这两个 err 计数是**结论的前提**。
        #   本脚本的结论形如「wbi 命中 7/8、旧端点 0/8 ⇒ wbi 更好」——
        #   分母 8 是「试了 8 次」，但如果失败是因为**抛异常**而不是「没命中」，
        #   那 0/8 的含义就完全不同（接口挂了 vs 接口没返回轨）。
        #   原来两处 `except: continue` 把它们混为一谈，verdict 就建在沙子上。
        verdict += '（异常 wbi %d / 旧 %d）' % (wbi_err, old_err) if (wbi_err or old_err) else ''
        total_err[0] += wbi_err + old_err
        print('%-16s %5d %7d/8 %10d/8 %10s' % (bv, pno, wbi_ok, old_ok, verdict))
    print()
    print('注：命中 = 返回的轨满足 aid+cid 不变量（已验证该不变量等价于「内容正确」）')
    if total_err[0]:
        print('⚠️ 有 %d 次探测以**异常**收场（不是「没命中」）—— 上面的命中率分母'
              '因此偏小，结论需打折。' % total_err[0])
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
