#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""定位 educity「新标日」各册逐课页面的 ID。

背景：
    目录大纲页 2246769 的正文里列出了 初级上/下、中级上/下、高级上/下 的分册大纲链接，
    但用 `href="/jlpt/N.html"` 正则只能抓到「高级上」那几条。
    ⇒ 说明分册链接的 href 形态不同（可能是相对路径 / 带参数 / 内联 JS）。

本脚本：
    1. 抓 2246769，把**所有 href** 原样打印（含相对路径、query），
    2. 把「中级下册」「高级下册」等锚点附近的原始 HTML 片段打出来，
    3. 便于据此写正确的种子清单。
"""
import re
import time
import urllib.request

HOST = 'https://m.educity.cn'
UAM = ('Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) '
       'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 '
       'Mobile/15E148 Safari/604.1')


def get(url, n=10, timeout=25):
    """带挑战页识别的抓取。挑战页特征是含 __tst_status 或没有 <title>。"""
    for i in range(n):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UAM})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read()
            for enc in ('utf-8', 'gbk', 'gb18030'):
                try:
                    h = raw.decode(enc)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                h = raw.decode('utf-8', 'ignore')
            if '__tst_status' in h or '<title>' not in h:
                time.sleep(2.0 + i * 1.5)
                continue
            return h
        except Exception:
            time.sleep(2.0 + i * 1.5)
    return ''


def main():
    h = get(HOST + '/jlpt/2246769.html')
    print('len =', len(h))
    if not h:
        print('!! 抓取失败（一直拿到挑战页）')
        return

    print('\n===== 全部 href（去重排序） =====')
    for x in sorted(set(re.findall(r'href="([^"]+)"', h))):
        print(' ', x)

    for kw in ('中级下册', '高级下册', '中级上册', '初级下册'):
        i = h.find(kw)
        print(f'\n===== 锚点「{kw}」附近 (idx={i}) =====')
        if i > 0:
            print(repr(h[max(0, i - 500):i + 300]))


if __name__ == '__main__':
    main()
