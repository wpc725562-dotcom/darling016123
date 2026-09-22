#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把语法底本压缩成「每点 1~2 句」的浓缩版，供逐课核对用。

为什么需要：
    digest-*.md 是教材原文全文（每课 2 万字），整读会吃掉大量上下文。
    写笔记时真正要核对的是：**语法点编号、名称、接续、核心释义、教材交叉引用**。
    例句和翻译可以只留一句。

输出：data/snj-lessons/condensed-<册>.md
"""
import json
import pathlib
import re
from collections import defaultdict

REPO = pathlib.Path(__file__).resolve().parent.parent
SRC = REPO / 'data' / 'snj-lessons' / 'pages.jsonl'
OUT = REPO / 'data' / 'snj-lessons'


def clean(t):
    for a in ('JLPT资料领取', '【文法】', '解説'):
        i = t.find(a)
        if i > 0:
            t = t[i + len(a):]
            break
    j = t.find('相关阅读')
    if j > 0:
        t = t[:j]
    t = re.sub(r'^\s*本文为.*?删除。', '', t)
    return t.strip()


def main():
    by = defaultdict(list)
    for line in open(SRC, encoding='utf-8'):
        r = json.loads(line)
        if r['level'] and r['lesson'] and r['kind'] in ('会话', '解说', '课文'):
            by[f"{r['level']}{r['lesson']:02d}"].append(r)

    for prefix in ('中级下', '高级上'):
        keys = sorted(k for k in by if k.startswith(prefix))
        buf = []
        for k in keys:
            pages = sorted(by[k], key=lambda r: -r['chars'])
            merged = clean('\n'.join(p['text'] for p in pages))
            # 按「数字.」切分语法点
            parts = re.split(r'(?=(?:^|\s)\d{1,2}[.．](?=[^\d]))', merged)
            buf.append(f'\n\n## {k}\n')
            seen = set()
            for p in parts:
                p = p.strip()
                m = re.match(r'^(\d{1,2})[.．]\s*(.{1,30}?)(?=[\s(（]|。|，|$)', p)
                if not m:
                    continue
                n = m.group(1)
                if n in seen or int(n) > 25:
                    continue
                seen.add(n)
                body = re.sub(r'\s+', ' ', p)[:430]
                buf.append(f'\n**{n}. {m.group(2).strip()}** — {body}\n')
        (OUT / f'condensed-{prefix}.md').write_text(''.join(buf), encoding='utf-8')
        print(f'condensed-{prefix}.md: {len(keys)} 课, '
              f'{sum(len(x) for x in buf)} 字符')


if __name__ == '__main__':
    main()
