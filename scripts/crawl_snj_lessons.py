#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""爬取 educity.cn「新标日」逐课页面，建立 课次 → 页面URL 映射。

为什么需要它：
    站点自带的《标日同步手册》里，中级 / 高级 的逐课语法清单**与教材实际不符**
    （实测：高级上第 1 课教材讲的是「これほど～は、～ない」和说明文写法，
    而站内清单写的是「～を問わず／～ならでは」）。要写 N1 段深度笔记，
    必须先拿到**准确的逐课语法点清单**。

来源：
    educity.cn 的《新标日》逐课「汇总」页 + 「解说/文法」页，
    内容为教材原文解说的转载，含语法点编号，可核对。

用法：
    python scripts/crawl_snj_lessons.py --seed            # 用内置种子爬
    python scripts/crawl_snj_lessons.py --max 400         # 限制页面数

产出：
    data/snj-lessons/pages.jsonl   每行 {url, title, kind, level, lesson, text}
    data/snj-lessons/index.json    课次 → 页面URL 映射
"""
import argparse
import json
import pathlib
import re
import sys
import time
import urllib.request
from collections import defaultdict, deque

REPO = pathlib.Path(__file__).resolve().parent.parent
OUTDIR = REPO / 'data' / 'snj-lessons'
# ★ 2026-09-23：www 站已上间歇性 JS 反爬（__tst_status 挑战页，988 字节）。
#   实测**移动镜像 m.educity.cn 不带挑战**，同一 URL 直接返回完整页。
#   所以统一走移动镜像；www 只在注释里留作备选。
HOST = 'https://m.educity.cn'
UAM = ('Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) '
       'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 '
       'Mobile/15E148 Safari/604.1')
UA = {'User-Agent': UAM}
BASE = HOST + '/jlpt/%s.html'

# 种子：教材大纲分册页（共 10 个，覆盖初级上/下、中级上/下、高级上）
#   ★ 2026-09-23 实测：站点**没有高级下册（第13~24课）**的任何页面。
#   这 10 个 ID 是从目录页 2246769 的正文里逐个核对出来的。
SEEDS = [
    '2241775',   # 初级上（入门单元~第12课）
    '2246170',   # 初级上（第13课~第24课）
    '2246202',   # 初级下（第25课~第36课）
    '2270357',   # 初级下（第37课~第48课）
    '2283233',   # 中级上（第1课~第8课）
    '2283277',   # 中级上（第9课~第16课）
    '2283303',   # 中级下（第17课~第24课）
    '2283411',   # 中级下（第25课~第32课）
    '2292903',   # 高级上（第1课~第7课）
    '2292906',   # 高级上（第8课~第12课）
]

# 只跟进这些类型的页面，避免爬进无关频道
KEEP_KINDS = ('汇总', '解说', '文法', '课文', '单词', '会话', '导入', '目录', '大纲')

LESSON_RE = re.compile(r'(初级|中级|高级)\s*(上|下)?\s*册?\s*第\s*(\d+)\s*课')


def parse_lesson(title):
    """从标题解析 (册别, 课次)。

    ★ 标题形态实测有三种，都必须吃下：
        《新标日》高级上第9课：自然災害（解说2）
        《新版标准日本语》高级上册第10课：資源（解说1）
        新版标准日本语高级上册第1课会话课文单词及语法讲解
    册别统一成「初级上 / 中级下 / 高级上」这种四字形式。
    """
    m = LESSON_RE.search(title)
    if not m:
        return None, None
    lv, half, no = m.group(1), m.group(2), int(m.group(3))
    if not half:
        # 未标上下册时，按课次推断：初级/中级 1-16 属上、17 以上属下；
        # 高级上下册各 12 课，同样按 12 分界。
        if lv == '高级':
            half = '上' if no <= 12 else '下'
        else:
            half = '上' if no <= 16 else '下'
    return lv + half, no


def fetch(num, timeout=25, retries=8):
    """取一页。★ 必须处理间歇性 JS 反爬挑战。

    实测：同一 URL 连续请求，有时返回完整页（约 130KB），
    有时返回一个 988 字节的 `__tst_status` JS 挑战页。
    挑战页**不带 <title>**，如果直接当正常页解析，会得到空标题
    ⇒ 表现为「爬虫跑了但一页都没抓到」，而错误信息为零。
    所以这里显式识别并退避重试。
    """
    last = ''
    for i in range(retries):
        try:
            req = urllib.request.Request(BASE % num, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read()
            html = None
            for enc in ('utf-8', 'gbk', 'gb18030'):
                try:
                    html = raw.decode(enc)
                    break
                except UnicodeDecodeError:
                    continue
            if html is None:
                html = raw.decode('utf-8', 'ignore')
            if '__tst_status' in html or '<title>' not in html:
                last = html
                time.sleep(1.5 + i * 1.2)     # 挑战页：退避后重试
                continue
            return html
        except Exception as e:
            last = repr(e)
            if i == retries - 1:
                raise
            time.sleep(1.5 + i)
    return last or ''


def to_text(html):
    t = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    t = re.sub(r'<style.*?</style>', ' ', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = t.replace('&nbsp;', ' ').replace('&amp;', '&')
    t = t.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
    return re.sub(r'\s+', ' ', t).strip()


def page_title(html):
    m = re.search(r'<title>(.*?)</title>', html, re.S)
    return to_text(m.group(1)) if m else ''


def body_links(html):
    """只取**正文区**的站内链接。

    ★ 2026-09-23 踩坑：整页抓链接会被「相关阅读」侧栏污染 ——
      侧栏永远挂着同几条最新文章（高级上8/9/10 的解说），
      导致 BFS 反复回到那几页，而**真正需要的本课解说页一个都进不来**。
      正文区在「相关阅读」之前，截断后取链接才准。
    """
    i = html.find('相关阅读')
    body = html[:i] if i > 0 else html
    for m in re.finditer(r'<a[^>]+href="([^"]*?/jlpt/(\d+)\.html)"[^>]*>(.*?)</a>',
                         body, re.S):
        yield m.group(2), to_text(m.group(3))


def classify(title):
    for k in KEEP_KINDS:
        if k in title:
            return k
    return 'other'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max', type=int, default=500)
    ap.add_argument('--seeds', default=','.join(SEEDS))
    ap.add_argument('--sleep', type=float, default=0.6)
    args = ap.parse_args()

    OUTDIR.mkdir(parents=True, exist_ok=True)
    seen = set()
    q = deque(args.seeds.split(','))
    records = []
    index = defaultdict(list)

    while q and len(seen) < args.max:
        num = q.popleft()
        if num in seen:
            continue
        seen.add(num)
        try:
            html = fetch(num)
        except Exception as e:
            print(f'  ✗ {num} {type(e).__name__}: {e}', flush=True)
            continue

        title = page_title(html)
        text = to_text(html)
        kind = classify(title)
        lv, lesson = parse_lesson(title)

        # 只保留《新标日》相关的页面
        if '标日' not in title and '标准日本语' not in title:
            continue

        records.append({'url': BASE % num, 'id': num, 'title': title,
                        'kind': kind, 'level': lv, 'lesson': lesson,
                        'chars': len(text), 'text': text})
        if lv and lesson:
            index[f'{lv}{lesson:02d}'].append({'id': num, 'title': title,
                                               'kind': kind, 'chars': len(text)})
        print(f'  ✓ {num} [{kind}] {lv or "-"}{lesson or "-"} :: {title[:60]}',
              flush=True)

        # 跟进正文区链接。★ 不再按锚文本过滤 ——
        #   解说页的锚文本是「1.课文特点 [说明文和条目式写法]…」这种，
        #   不含「标日」二字，按文本过滤会把**最有价值的语法页**全漏掉。
        #   正文区本来就只有本课自己的链接，全跟即可。
        for nid, txt in body_links(html):
            if nid not in seen:
                q.append(nid)

        time.sleep(args.sleep)

    with open(OUTDIR / 'pages.jsonl', 'w', encoding='utf-8', newline='\n') as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    with open(OUTDIR / 'index.json', 'w', encoding='utf-8', newline='\n') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f'\n抓取页面 {len(records)} 个，覆盖课次 {len(index)} 个')
    print('课次清单：', ' '.join(sorted(index.keys())))


if __name__ == '__main__':
    main()
