#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把已抓到的 educity「新标日」页面按 课次 汇总成一份语法底本。

用途：
    写深度卷的「📖 教材编写」段时，逐课对着这份底本抄准语法点编号、
    接续、用法和例句 —— 而不是凭印象写。

输入：data/snj-lessons/pages.jsonl
输出：data/snj-lessons/digest-中级下.md / digest-高级上.md
"""
import json
import pathlib
import re
from collections import defaultdict

REPO = pathlib.Path(__file__).resolve().parent.parent
SRC = REPO / 'data' / 'snj-lessons' / 'pages.jsonl'
OUT = REPO / 'data' / 'snj-lessons'


def clean(t):
    """剥掉页头页脚，只留正文。"""
    for a, b in (('JLPT资料领取', None), ('【文法】', None), ('解説', None)):
        i = t.find(a)
        if i > 0:
            t = t[i + len(a):]
            break
    j = t.find('相关阅读')
    if j > 0:
        t = t[:j]
    t = re.sub(r'^\s*本文为.*?删除。', '', t)
    return t.strip()


def kind_rank(kind):
    """语法页排前面。"""
    return {'会话': 0, '解说': 0, '课文': 1, '单词': 9, '汇总': 8, '大纲': 9}.get(kind, 5)


def main():
    by = defaultdict(list)
    for line in open(SRC, encoding='utf-8'):
        r = json.loads(line)
        if r['level'] and r['lesson']:
            by[f"{r['level']}{r['lesson']:02d}"].append(r)

    for prefix, fname in (('中级下', 'digest-中级下.md'),
                          ('高级上', 'digest-高级上.md'),
                          ('中级上', 'digest-中级上.md')):
        keys = sorted(k for k in by if k.startswith(prefix))
        buf = [f'# {prefix} 语法底本（自动汇总，勿手改）\n',
               f'> 来源：educity.cn 标日逐课页。覆盖 {len(keys)} 课。\n']
        for k in keys:
            pages = sorted(by[k], key=lambda r: (kind_rank(r['kind']), -r['chars']))
            buf.append(f'\n\n---\n\n## {k}\n')
            for p in pages:
                if p['chars'] < 200:
                    continue
                buf.append(f"\n### [{p['kind']}] {p['title'][:70]}\n")
                buf.append(clean(p['text'])[:6000])
                buf.append('\n')
        (OUT / fname).write_text(''.join(buf), encoding='utf-8')
        print(f'{fname}: {len(keys)} 课, {sum(len(x) for x in buf)} 字符')


if __name__ == '__main__':
    main()
