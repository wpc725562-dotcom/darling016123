#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bili_tag_kaodian.py —— 用免费模型给网课字幕逐集打「考点标签」。

为什么需要它
    `B站网课资源总索引` 只能做到「BV → 集数 → 分P标题」，
    但学生卡在某个考点时，真正想知道的是「这个考点在第几集」。
    字幕是纯文本、**没有时间戳**，所以做不到「第几分钟」；
    但做到「第几集」是可行的 —— 只要知道每集讲什么。

怎么做（★ 批量，不是逐集）
    把 N 集（默认 8）的字幕开头拼成一段，一次调用让模型逐集判定。
    逐集调用会被免费额度限流（实测 42 集跑 10 分钟没跑完），
    批量后 42 集只要 6 次调用，1 分钟内完成。

用法
    python scripts/bili_tag_kaodian.py --subject 政治
    python scripts/bili_tag_kaodian.py --subject 政治 --dry-run
    python scripts/bili_tag_kaodian.py --subject 高数 --batch 10 --jobs 2

产出
    备考计划/网课考点索引-<学科>.md
    控制台打印：成功 / 失败 / 低置信度 计数

★ 模型选择
    OpenRouter 免费线（gemma-4-26b 等）本机直连失败（EOF），只有 Groq 那条通。
    Groq 免费额度按「每分钟请求数」限，批量调用正好绕开这个限制。
"""
import argparse
import json
import pathlib
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = pathlib.Path('D:/deeepseek/zhuan-sheng-ben-notes')
BILI = ROOT / 'data' / 'bili-analyze'
EXE = r'D:\agenttttt\Reasonix\reasonix-cli.exe'
EXE_CWD = r'D:\agenttttt\Reasonix'
DEFAULT_MODEL = 'groq/openai/gpt-oss-120b'

SUBJECT_SPEC = {
    '政治': (
        '【毛中特】00导论 01毛泽东思想及其历史地位 02新民主主义革命理论 03社会主义改造理论 '
        '04初步探索的理论成果 05理论体系的形成发展 06邓小平理论 07三个代表重要思想 08科学发展观\n'
        '【习概】00导论 01新时代坚持和发展中国特色社会主义 02中国式现代化 03坚持党的全面领导 '
        '04坚持以人民为中心 05全面深化改革开放 06推动高质量发展 07教育科技人才战略 '
        '08全过程人民民主 09全面依法治国 10文化强国 11民生与社会建设 12生态文明 '
        '13国家安全 14国防和军队 15一国两制与祖国统一 16大国外交 17全面从严治党',
        '政治',
    ),
    '高数': (
        '01函数极限连续 02导数与微分 03微分中值定理与导数应用 04不定积分 '
        '05定积分 06定积分应用 07微分方程 08向量代数与空间解析几何 '
        '09多元函数微分法 10重积分 11曲线积分与曲面积分 12无穷级数',
        '高数',
    ),
    '计算机': (
        '【C语言】C1概述 C2数据类型运算输入输出 C3选择结构 C4循环结构 C5函数 C6数组 '
        'C7指针 C8结构体共用体 C9预处理 C10文件\n'
        '【数据结构】D1基本概念 D2线性表 D3栈和队列 D4串 D5数组与广义表 D6树与二叉树 '
        'D7图 D8查找 D9排序',
        '计算机',
    ),
    '英语': (
        'E01名词 E02代词 E03冠词 E04数词 E05形容词副词 E06介词 E07动词时态 E08被动语态 '
        'E09情态动词 E10非谓语动词 E11虚拟语气 E12定语从句 E13名词性从句 E14状语从句 '
        'E15主谓一致 E16倒装 E17强调 E18反义疑问\n'
        '题型：阅读理解 完形填空 语法填空 短文造句匹配 写作',
        '英语',
    ),
}


def sample_text(f, n):
    """取字幕的「正文段」，不是开头段。

    踩过的坑：一集 60 分钟的课，前 300 字几乎全是开场白
    （「同学们好，今天我们讲…」「先回顾一下上节课」），
    按开头采样会把《毛概》导论判成「课程介绍」。
    所以从 15% 位置开始取，避开寒暄，落进正文。
    """
    t = f.read_text(encoding='utf-8', errors='replace')
    if len(t) <= n:
        return t
    start = int(len(t) * 0.15)
    return t[start:start + n]


def build_batch_prompt(subject, items, chars):
    """items: [(p, part, file)] —— 一次判 N 集。"""
    spec = SUBJECT_SPEC[subject][0]
    parts = [
        f'你是广东专升本{subject}老师。下面有 {len(items)} 段网课字幕的正文片段，'
        f'每段以【P编号】开头。请对每一段判断它主要讲哪个考点。',
        f'可选考点清单：\n{spec}',
        '输出要求：只输出 ' + str(len(items)) + ' 行，每行格式严格为',
        'P编号|考点编号|考点名|置信度(高/中/低)',
        '考点名控制在 12 字以内。不要表头、不要解释、不要空行。',
        '若某段确实是课程介绍/广告/闲聊/试听说明，该行考点编号写「无」、考点名写「课程介绍」。',
        '',
        '===== 字幕 =====',
    ]
    for p, part, f in items:
        text = sample_text(f, chars)
        parts.append(f'【P{p}】{text}')
        parts.append('')
    return '\n'.join(parts)


def call_model(prompt, model, timeout=240, retries=3):
    """调 Reasonix CLI。空输出＝被限流，重试。"""
    last_err = ''
    for attempt in range(retries):
        try:
            r = subprocess.run(
                [EXE, '-p', '--model', model, prompt],
                cwd=EXE_CWD, capture_output=True, text=True,
                encoding='utf-8', errors='replace', timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            last_err = 'timeout'
            time.sleep(3 * (attempt + 1))
            continue
        out_lines = [l.strip() for l in (r.stdout or '').splitlines()
                     if l.strip() and not l.strip().startswith('warning:')]
        if out_lines:
            return out_lines, None
        err_lines = [l.strip() for l in (r.stderr or '').splitlines()
                     if l.strip() and not l.strip().startswith('warning:')]
        last_err = (err_lines[-1] if err_lines else '空输出（疑似限流）')[:120]
        time.sleep(3 * (attempt + 1))
    return None, last_err


LINE_RE = re.compile(
    r'P?\s*(\d{1,3})\s*[|｜]\s*([0-9A-Za-z第章无]{1,8})\s*[|｜]\s*([^|｜]{1,40})\s*[|｜]\s*(高|中|低)')


def parse_batch(lines):
    """返回 {p: (编号, 考点名, 置信度)}"""
    got = {}
    for ln in lines or []:
        m = LINE_RE.search(ln)
        if m:
            got[int(m.group(1))] = (m.group(2), m.group(3).strip(), m.group(4))
    return got


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--subject', required=True, choices=list(SUBJECT_SPEC))
    ap.add_argument('--bv', action='append', help='只跑指定 BV，可重复')
    ap.add_argument('--batch', type=int, default=4, help='每次调用判几集')
    ap.add_argument('--jobs', type=int, default=1, help='并发批次数（免费额度建议 1）')
    ap.add_argument('--chars', type=int, default=300, help='每集送前多少字')
    ap.add_argument('--sleep', type=float, default=2.0, help='批次间隔秒数，防限流')
    ap.add_argument('--model', default=DEFAULT_MODEL)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--no-cache', action='store_true', help='忽略已缓存的标注结果')
    ap.add_argument('--limit', type=int, default=0)
    a = ap.parse_args()

    smap = json.loads((BILI / '_subject-map.json').read_text(encoding='utf-8'))
    ptitles = json.loads((BILI / '_part_titles_all.json').read_text(encoding='utf-8'))

    # 缓存：key = "BV|p"，value = [编号, 考点名, 置信度]
    cache_path = BILI / '_kaodian_tags.json'
    cache = {}
    if cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text(encoding='utf-8'))
        except Exception:
            cache = {}

    tasks = []
    for bv, subj in smap.items():
        if subj != a.subject:
            continue
        if a.bv and bv not in a.bv:
            continue
        d = BILI / bv
        if not d.is_dir():
            continue
        pages = {p['p']: p.get('part', '') for p in ptitles.get(bv, {}).get('pages', [])}
        title = ptitles.get(bv, {}).get('title', bv)
        for f in sorted(d.glob('subtitle_p*.txt')):
            m = re.search(r'p(\d+)', f.name)
            if not m:
                continue
            p = int(m.group(1))
            tasks.append((bv, p, title, pages.get(p, ''), f))
    if a.limit:
        tasks = tasks[:a.limit]

    # 命中缓存的不再调用模型
    tagged = {}
    todo = []
    for t in tasks:
        key = f'{t[0]}|{t[1]}'
        if not a.no_cache and key in cache:
            v = cache[key]
            tagged[(t[0], t[1])] = (v[0], v[1], v[2])
        else:
            todo.append(t)

    # 按 BV 分组，再按 batch 切
    by_bv = {}
    for t in todo:
        by_bv.setdefault(t[0], []).append(t)
    batches = []
    for bv, ts in by_bv.items():
        ts.sort(key=lambda x: x[1])
        for i in range(0, len(ts), a.batch):
            batches.append((bv, ts[i:i + a.batch]))

    print(f'[{a.subject}] 共 {len(tasks)} 集：缓存命中 {len(tagged)}，待标注 {len(todo)} '
          f'→ {len(batches)} 批（每批 ≤{a.batch} 集，每集前 {a.chars} 字）')
    print(f'模型 {a.model}，并发 {a.jobs}，批次间隔 {a.sleep}s')
    if a.dry_run:
        for bv, ts in batches:
            print(f'  {bv}: P{ts[0][1]}–P{ts[-1][1]}（{len(ts)} 集）')
        return

    failed = []
    t0 = time.time()

    def work(batch):
        bv, ts = batch
        items = [(t[1], t[3], t[4]) for t in ts]
        prompt = build_batch_prompt(a.subject, items, a.chars)
        lines, err = call_model(prompt, a.model)
        if lines is None:
            return bv, ts, None, err
        return bv, ts, parse_batch(lines), None

    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        futs = {pool.submit(work, b): b for b in batches}
        done = 0
        for fu in as_completed(futs):
            bv, ts, got, err = fu.result()
            done += 1
            if got is None:
                failed.append((bv, ts, err))
            else:
                for p, v in got.items():
                    tagged[(bv, p)] = v
                    cache[f'{bv}|{p}'] = list(v)
            # 每批落盘，中断不丢进度
            cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding='utf-8')
            el = time.time() - t0
            print(f'  批次 {done}/{len(batches)}  已标注 {len(tagged)}/{len(tasks)} 集  {el:.0f}s')
            if a.sleep and done < len(batches):
                time.sleep(a.sleep)

    miss = [(t[0], t[1]) for t in tasks if (t[0], t[1]) not in tagged]
    low = [k for k, v in tagged.items() if v[2] == '低']
    print(f'\n成功 {len(tagged)}/{len(tasks)} | 未标 {len(miss)} | 低置信度 {len(low)}')
    for bv, ts, err in failed:
        print(f'  ✗ 批次失败 {bv} P{ts[0][1]}-P{ts[-1][1]}: {(err or "")[:80]}')

    # 写索引
    out_path = ROOT / '备考计划' / f'网课考点索引-{SUBJECT_SPEC[a.subject][1]}.md'
    lines_out = [
        f'# 📺 网课考点索引 · {a.subject}',
        '',
        f'> 生成：{time.strftime("%Y-%m-%d %H:%M")}　｜　模型：`{a.model}`（Reasonix 免费线）',
        f'> 覆盖：**{len(tagged)} 集**（总 {len(tasks)} 集，未标 {len(miss)}）',
        f'> 方法：每批 {a.batch} 集，取每集字幕前 {a.chars} 字让模型判定主要考点。',
        '> ⚠️ 字幕无时间戳，**只能定位到「集」，不能到「第几分钟」**。',
        '> ⚠️ 置信度「低」的条目建议人工扫一眼再用。',
        '',
        '---',
        '',
        '## 按 BV 排列（看课时用）',
        '',
    ]
    meta = {(t[0], t[1]): t for t in tasks}
    per_bv = {}
    for (bv, p), v in tagged.items():
        per_bv.setdefault(bv, []).append((p, v))
    for bv in sorted(per_bv):
        title = meta[(bv, per_bv[bv][0][0])][2]
        lines_out.append(f'### `{bv}` {title}')
        lines_out.append('')
        lines_out.append('| 集 | 分P标题 | 考点编号 | 考点 | 置信度 |')
        lines_out.append('|:--:|:--|:--:|:--|:--:|')
        for p, (num, name, conf) in sorted(per_bv[bv]):
            part = meta[(bv, p)][3]
            lines_out.append(f'| P{p} | {part[:30]} | **{num}** | {name} | {conf} |')
        lines_out.append('')

    lines_out += ['---', '', '## 按考点反查（卡住时用）', '',
                  '| 考点编号 | 考点 | 在哪些集 |', '|:--:|:--|:--|']
    by_kp = {}
    for (bv, p), (num, name, conf) in tagged.items():
        if num == '无':
            continue
        by_kp.setdefault((num, name), []).append((bv, p))
    for (num, name), locs in sorted(by_kp.items()):
        locs.sort()
        s = '、'.join(f'{b} P{p}' for b, p in locs[:8]) + ('…' if len(locs) > 8 else '')
        lines_out.append(f'| **{num}** | {name} | {s} |')
    lines_out.append('')

    out_path.write_text('\n'.join(lines_out) + '\n', encoding='utf-8')
    print(f'✅ 已写入：{out_path}')
    print(f'   总耗时 {(time.time()-t0)/60:.1f} 分钟')


if __name__ == '__main__':
    main()
