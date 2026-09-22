#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""字幕内容体检：找出「字幕和视频对不上」的分P。

为什么需要它
    2026-09-18 发现 B站 `x/player/v2` 会返回**别的视频的字幕轨**：同一个 cid 连请求
    5 次，返回的 URL 哈希每次不同，内容分别是火锅探店、篮球解说、iPhone 评测、
    音乐纯响…… 而 `code` 恒为 0、`lan` 恒为 `ai-zh`，**从响应完全看不出异常**。
    首轮下载的 1526 个文件里 1038 个（68%）内容是错的，却全部「下载成功、无报错」。

    所以「文件非空」不等于「内容是对的」，必须有独立的内容校验。

★ 两个判据，谁是主谁是从（这是本脚本最容易搞错的地方）
    主判据：`<BV>/_verify.jsonl` —— 下载时按「URL 路径含 aid+cid」这个不变量校验过，
            是**确定性**的证据（见 bili_analyze.py::probe_subtitle）。
    从判据：学科词密度 —— 只能当**启发式**，因为它对「中英混排的英语课」天然失分：
            英语语法课的正确字幕里混着大量英文（"Welcome back to speak english"），
            纯中文词表会把它打成 0.3 分/千字，**看起来像脏数据，其实是对的**。
            第一版脚本就是踩了这个坑：拿未校准的词表当判据，得出「84% 可疑」的假警报。

用法
    python scripts/bili_audit_subtitle_content.py
产出
    data/bili-analyze/_subtitle_audit.json
    data/bili-analyze/_subtitle_audit.md
"""
import json
import pathlib
import re
import sys

# ★ E1（2026-09-20）：原来是 `pathlib.Path('data/bili-analyze')` —— 相对**当前工作目录**。
#   从仓库根跑没问题，从别处跑就指向一个不存在的目录，然后这个审计脚本会
#   安静地报告「分P 总数 0」，看起来像「没有数据」而不是「路径找错了」。
#   锚定到脚本自身位置，跑在哪都一样。
ROOT = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'bili-analyze'

# 各学科特征词。★ 英语必须带英文词 —— 这是第一版踩过的坑。
KEYWORDS = {
    '计算机': ['函数', '变量', '数组', '指针', '循环', '结构体', '算法', '链表', '节点',
             '二叉树', '遍历', '栈', '队列', '排序', '时间复杂度', '字符串', '返回值',
             '形参', '实参', '编译', '程序', '代码', '内存', '地址', '下标', '递归',
             '顺序表', '哈希', '顶点', '查找', '插入', '删除', '进制', '字节',
             '表达式', '运算符', '类型', 'printf', 'scanf', 'int', 'char', 'float'],
    '高数': ['函数', '极限', '导数', '微分', '积分', '连续', '无穷小', '洛必达',
           '不定积分', '定积分', '微分方程', '中值定理', '拐点', '极值', '单调',
           '原函数', '求导', '复合函数', '偏导', '级数', '收敛', '发散', '区间',
           '定义域', '值域', '切线', '法线', '泰勒', '拉格朗日', '罗尔'],
    '政治': ['社会主义', '矛盾', '实践', '认识', '生产力', '生产关系', '经济基础',
           '上层建筑', '唯物', '辩证', '发展', '人民', '中国共产党', '马克思',
           '毛泽东思想', '邓小平', '新时代', '改革开放', '制度', '法治', '文化',
           '价值', '理想', '信念', '道德', '爱国主义', '本质', '规律',
           '毛概', '思修', '马原', '考点', '辨析', '论述', '单选', '多选'],
    '英语': ['语法', '句子', '从句', '时态', '谓语', '主语', '宾语', '定语', '状语',
           '名词', '动词', '形容词', '副词', '介词', '连词', '代词', '虚拟语气',
           '非谓语', '不定式', '分词', '动名词', '被动', '完成时', '词性', '短语',
           '搭配', '翻译', '写作', '阅读', '词汇',
           # ★ 英语课字幕是中英混排，下面这些英文词是强信号
           'english', 'grammar', 'sentence', 'verb', 'noun', 'adjective', 'adverb',
           'preposition', 'pronoun', 'clause', 'tense', 'subject', 'object',
           'the', 'and', 'is', 'you', 'that', 'we', 'have', 'word'],
}

SUBJECTS = ('计算机', '高数', '政治', '英语')

# ── 被吞掉的异常（2026-09-20，修 A6）────────────────────────────────
#   ★ 原来 read_verify 里是 `except Exception: pass`。这个脚本的**全部职责**
#     就是判「哪些分P 通过了 aid+cid 校验」，而它的输入正是 _verify.jsonl。
#     坏行被吞掉 ⇒ 该分P 落进「未校验」桶 ⇒ 报告说「N 个待复核」，
#     而真相可能是「N-3 个其实已校验，只是记账文件坏了几行」。
#     审计脚本自己吞掉输入错误，是这一类里最讽刺的一种。
_BAD_VERIFY_LINES = []


def load_subject_map():
    """BV → 学科。直接读 fetch 脚本的 CATALOG，避免手工维护第二份映射。"""
    import importlib.util
    # ★ E1（2026-09-20）：原来是 `'scripts/bili_fetch_subs.py'`（相对 CWD）。
    #   从别的目录跑时 exec_module 会抛 FileNotFoundError；更糟的情况是
    #   它抛在 try 之外，整脚本崩掉。改成锚定到本文件旁边。
    spec = importlib.util.spec_from_file_location(
        'fs', str(pathlib.Path(__file__).resolve().with_name('bili_fetch_subs.py')))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = {}
    for subj, bvs in mod.CATALOG.items():
        for bv in bvs:
            out[bv] = subj
    return out


def read_verify(bvdir):
    """读 <BV>/_verify.jsonl → {p: bool}。后写的覆盖先写的。"""
    f = bvdir / '_verify.jsonl'
    if not f.exists():
        return None
    out = {}
    for ln in f.read_text(encoding='utf-8', errors='ignore').splitlines():
        try:
            o = json.loads(ln)
            out[int(o['p'])] = bool(o['ok'])
        except Exception as e:
            # 坏行 ⇒ 该分P 的校验状态未知 ⇒ 会被算进「未校验」，报告虚高。
            n = len(_BAD_VERIFY_LINES)
            _BAD_VERIFY_LINES.append('%s: %s' % (f.parent.name, e))
            if n == 0:
                print('  [警告] %s 有无法解析的行（只报第一条）：%s' % (f, e),
                      file=sys.stderr, flush=True)
    return out or None


def main():
    import collections
    bv2subj = load_subject_map()
    titles = json.loads((ROOT / '_part_titles_all.json').read_text(encoding='utf-8'))

    rows = []
    for bvdir in sorted(ROOT.glob('BV*')):
        if not bvdir.is_dir():
            continue
        bv = bvdir.name
        subj = bv2subj.get(bv)
        if not subj:
            continue
        ver = read_verify(bvdir)
        by_p = {p['p']: p for p in titles.get(bv, {}).get('pages', [])}
        for f in sorted(bvdir.glob('subtitle_p*.txt')):
            pno = int(re.search(r'p(\d+)', f.name).group(1))
            txt = f.read_text(encoding='utf-8', errors='ignore')
            low = txt.lower()
            hit = sum(low.count(k.lower()) for k in KEYWORDS[subj])
            density = hit / len(txt) * 1000 if txt else 0.0
            rows.append({
                'subject': subj, 'bv': bv, 'p': pno,
                'part': by_p.get(pno, {}).get('part', ''),
                'chars': len(txt), 'density': round(density, 1),
                'verified': (ver or {}).get(pno),      # True / False / None(无记录)
            })

    # 学科词密度的中位数 —— 作为「相对低」的基准
    by_subj = collections.defaultdict(list)
    for r in rows:
        by_subj[r['subject']].append(r['density'])
    med = {s: (sorted(v)[len(v) // 2] if v else 0) for s, v in by_subj.items()}
    print('学科词密度中位数（每千字命中）—— 用来定「相对低」的阈值：')
    for s in SUBJECTS:
        print('  %-6s %5.1f   （样本 %d）' % (s, med.get(s, 0), len(by_subj[s])))

    for r in rows:
        m = med.get(r['subject']) or 1
        r['ratio'] = round(r['density'] / m, 3) if m else 0
        flags = []
        if r['chars'] < 60:
            flags.append('几乎无内容')
        if r['verified'] is False:
            flags.append('★未通过 aid+cid 校验')
        if r['ratio'] < 0.2:
            flags.append('学科词密度极低')
        r['flags'] = flags

    bad = [r for r in rows if r['flags']]
    (ROOT / '_subtitle_audit.json').write_text(
        json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8', newline='\n')

    # 两判据的一致性 —— 这是本报告最该看的一张表
    unver = [r for r in rows if r['verified'] is False]
    unver_lowdens = [r for r in unver if '学科词密度极低' in r['flags']]
    lowdens = [r for r in rows if '学科词密度极低' in r['flags']]

    lines = ['# 字幕内容体检报告', '',
             '> 主判据 = `<BV>/_verify.jsonl`（aid+cid 不变量，确定性）；'
             '从判据 = 学科词密度（启发式，仅用于交叉验证）。', '',
             '| 学科 | 分P 总数 | 已校验通过 | 未通过校验 | 密度极低 | 可疑合计 |',
             '|:---|---:|---:|---:|---:|---:|']
    for s in SUBJECTS:
        tot = [r for r in rows if r['subject'] == s]
        nv = [r for r in tot if r['verified'] is True]
        nf = [r for r in tot if r['verified'] is False]
        ld = [r for r in tot if '学科词密度极低' in r['flags']]
        b = [r for r in tot if r['flags']]
        lines.append('| %s | %d | %d | %d | %d | %d |'
                     % (s, len(tot), len(nv), len(nf), len(ld), len(b)))
    lines += ['', '## 两判据一致性', '',
              '| 指标 | 数量 |', '|:---|---:|',
              '| 未通过 aid+cid 校验 | %d |' % len(unver),
              '| 其中「学科词密度也极低」（两判据一致，基本可确认是脏数据） | %d |'
              % len(unver_lowdens),
              '| 学科词密度极低但**校验通过**（多为中英混排等误报） | %d |'
              % len([r for r in lowdens if r['verified'] is True]),
              '| 学科词密度极低且**无校验记录**（老文件，需重下） | %d |'
              % len([r for r in lowdens if r['verified'] is None]),
              '', '## 需要处理的分P（按 BV 汇总）', '',
              '| BV | 学科 | 未通过校验 | 密度极低 |', '|:---|:---|---:|---:|']
    per = collections.defaultdict(lambda: [0, 0, ''])
    for r in bad:
        per[r['bv']][0] += 1 if r['verified'] is False else 0
        per[r['bv']][1] += 1 if '学科词密度极低' in r['flags'] else 0
        per[r['bv']][2] = r['subject']
    for bv, (a, b, s) in sorted(per.items(), key=lambda x: -(x[1][0] + x[1][1])):
        lines.append('| `%s` | %s | %d | %d |' % (bv, s, a, b))

    # ★ A6（2026-09-20）：把「输入本身坏了几行」写进报告。
    #   报告里所有「未通过校验」的数字都建立在 _verify.jsonl 可读的前提上；
    #   这个前提不成立时必须写在纸面上，而不是只往 stderr 丢一行。
    if _BAD_VERIFY_LINES:
        lines += ['', '## ⚠️ 记账完整性', '',
                  '`_verify.jsonl` 里有 **%d** 行无法解析。'
                  % len(_BAD_VERIFY_LINES),
                  '这些分P 的校验状态**未知**，被算进了「未校验」桶 —— '
                  '上表里「未通过校验」的数字因此可能虚高。',
                  '', '| 出处 | 错误 |', '|:---|:---|']
        for item in _BAD_VERIFY_LINES[:20]:
            lines.append('| %s |' % item.replace('|', '\\|'))
    (ROOT / '_subtitle_audit.md').write_text('\n'.join(lines), encoding='utf-8', newline='\n')

    print()
    print('分P 总数 %d' % len(rows))
    print('  未通过 aid+cid 校验            %4d' % len(unver))
    print('  其中密度也极低（两判据一致）    %4d' % len(unver_lowdens))
    print('  密度极低但校验通过（多为误报）  %4d'
          % len([r for r in lowdens if r['verified'] is True]))
    print('  密度极低且无校验记录（需重下）  %4d'
          % len([r for r in lowdens if r['verified'] is None]))
    print()
    print('报告: data/bili-analyze/_subtitle_audit.md')
    if _BAD_VERIFY_LINES:
        print()
        print('⚠️ _verify.jsonl 有 %d 行无法解析 —— 上面的「未通过校验」可能虚高。'
              % len(_BAD_VERIFY_LINES))
        print('   前几条：%s' % '；'.join(_BAD_VERIFY_LINES[:3]))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
