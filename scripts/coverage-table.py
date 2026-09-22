#!/usr/bin/env python3
"""《考纲覆盖 × 练习对照表》的复算脚本。

背景：`docs/guide/考纲覆盖与练习对照表.md` 曾声称「数字由脚本从笔记文件实算」，
但仓库里一直没有这个脚本（该页 2026-09-19 订正里记录了这一点）。本脚本补上它。

用法
----
    python scripts/coverage-table.py           # 只复算 + 对比，不改任何文件
    python scripts/coverage-table.py --write   # 把复算结果写回页面

口径（与页面「口径」一节一致）
------------------------------
    独立练习 = 标题含 闭卷/自检/小测/测验/随堂/作业 的章节下，形如 `1.` 或 `**1.**` 的条目数
    带做例题 = 标题含 手把手/真题演练/例题精讲 的章节下的同类条目数
    行数     = wc -l（换行符个数）

注意：这是**估算**，不是精确题数。正则数不清「手把手真题演练」这类边界，
换个口径数字能差一半。请当量级参考用。
"""
import argparse
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'docs/guide/考纲覆盖与练习对照表.md')

SEC_EX = re.compile(r'闭卷|自检|小测|测验|随堂|作业')
SEC_DEMO = re.compile(r'手把手|真题演练|例题精讲')
HEAD = re.compile(r'^#{2,6}\s')
ITEM = re.compile(r'^(?:\*\*)?\d+[.、)]')
ROW = re.compile(r'^\|\s*([①-⑳㉑])\s*\|\s*([^|]+?)\s*\|\s*\[([^\]]+)\]\(([^)]+)\)\s*'
                 r'\|\s*(\d+)\s*\|\s*(\d+)\s*([^|]*)\|\s*(\d+)\s*\|$')
TOTAL = re.compile(r'^\| \| \*\*合计\*\* \| \| \| \*\*(\d+)\*\* \| \*\*(\d+)\*\* \|$')


def count_items(text, sec_re):
    """标题命中 sec_re 的章节下，形如 `1.` / `**1.**` 的编号条目数。"""
    n, in_sec = 0, False
    for line in text.split('\n'):
        if HEAD.match(line):
            in_sec = bool(sec_re.search(line))
        elif in_sec and ITEM.match(line.strip()):
            n += 1
    return n


def wc_l(path):
    with io.open(path, 'rb') as f:
        return f.read().count(b'\n')


def measure():
    """返回 [(编号, 模块, 路径, 行数, 练习, 例题), ...]，按页面表格顺序。"""
    text = io.open(PAGE, encoding='utf-8').read()
    out = []
    for line in text.split('\n'):
        m = ROW.match(line)
        if not m:
            continue
        f = os.path.join(ROOT, 'docs' + m.group(4) + '.md')
        if not os.path.exists(f):
            print('!! 文件不存在: %s' % m.group(4), file=sys.stderr)
            continue
        body = io.open(f, encoding='utf-8').read()
        out.append((m.group(1), m.group(2), m.group(4), wc_l(f),
                    count_items(body, SEC_EX), count_items(body, SEC_DEMO)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true', help='把复算结果写回页面')
    args = ap.parse_args()

    rows = measure()
    if len(rows) != 21:
        print('!! 只解析到 %d 行，预期 21 行；页面表格结构可能变了' % len(rows),
              file=sys.stderr)
        return 1

    page = io.open(PAGE, encoding='utf-8').read()
    lines = page.split('\n')
    stale_l = stale_e = 0
    for i, line in enumerate(lines):
        m = ROW.match(line)
        if not m:
            continue
        hit = [r for r in rows if r[0] == m.group(1)]
        if not hit:
            continue
        no, mod, path, rl, rex, rdemo = hit[0]
        if rl != int(m.group(5)):
            stale_l += 1
        if rex != int(m.group(6)):
            stale_e += 1
        if args.write:
            warn = ' ⚠️' if rex < 10 else ''
            lines[i] = '| %s | %s | [%s](%s) | %d | %d%s | %d |' % (
                no, mod, m.group(3), path, rl, rex, warn, rdemo)

    tot = sum(r[4] for r in rows)
    uniq = {r[2] for r in rows}
    uniq_tot = sum(count_items(
        io.open(os.path.join(ROOT, 'docs' + p + '.md'), encoding='utf-8').read(),
        SEC_EX) for p in uniq)

    print('解析 %d 行 | 行数过期 %d | 练习过期 %d' % (len(rows), stale_l, stale_e))
    print('练习逐行之和 %d | 唯一讲义 %d 篇 ⇒ 去重后 %d' % (tot, len(uniq), uniq_tot))

    if not args.write:
        print('（未写盘。加 --write 写回页面。）')
        return 0

    # 合计行 + 去重脚注
    idx = [i for i, l in enumerate(lines) if TOTAL.match(l)]
    if len(idx) == 1:
        lines[idx[0]] = '| | **合计** | | | **%d** | **0** |' % tot
    note = ('> 📌 **合计 %d 是逐行相加**；⑳ 与 ㉑ 共用同一篇 `2.9-算法基本概念与分析`，'
            '**去重后为 %d 道**。' % (tot, uniq_tot))
    ni = [i for i, l in enumerate(lines) if l.startswith('> 📌 **合计 ')]
    if ni:
        lines[ni[0]] = note
    else:
        ai = [i for i, l in enumerate(lines) if '= 独立练习少于 10 道' in l]
        if len(ai) == 1:
            lines[ai[0] + 1:ai[0] + 1] = [note]

    out = '\n'.join(lines).encode('utf-8')
    crlf = io.open(PAGE, 'rb').read().count(b'\r') > 0
    if crlf:
        out = out.replace(b'\n', b'\r\n')
    io.open(PAGE, 'wb').write(out)
    print('已写回 %s（%d 字节）' % (PAGE, len(out)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
