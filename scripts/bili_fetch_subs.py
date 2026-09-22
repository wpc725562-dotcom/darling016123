#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量下载 B站 AI 字幕 —— 免 ASR 建字幕库。

为什么需要它
    24 条备考视频合计 1526 个分P / 470 小时。走 ASR 要 56.7 小时机器时间。
    但普查发现其中 84%（397 小时）的视频带 AI 字幕，登录后可直接下载。
    本脚本把这部分一次拉下来存盘；后续所有 Q&A 提炼都基于字幕，不再跑 ASR。

前置
    先扫码登录：python scripts/bili_login.py --html qr.html

用法
    python scripts/bili_fetch_subs.py                  # 全部 24 条（默认 6 线程）
    python scripts/bili_fetch_subs.py --only 政治       # 只跑一科
    python scripts/bili_fetch_subs.py --bv BV1Z4w3znE6h
    python scripts/bili_fetch_subs.py --jobs 1         # 退回串行（被限流时用）
    python scripts/bili_fetch_subs.py --jobs 24        # 实测未触发 412，但属显式选择
    python scripts/bili_fetch_subs.py --refresh        # 只补缺失/未校验的（推荐长任务）
    python scripts/bili_fetch_subs.py --force --yes    # 全量重下（覆盖已校验文件需 --yes）

产出
    data/bili-analyze/<BV>/subtitle_pXX.txt    每个分P 一份
    末尾打印汇总：新增 / 跳过 / 无字幕 / 失败

★ 为什么默认并行
    串行实测 ≈ 11 个分P/分钟 ⇒ 1526 个要 2 小时以上。
    瓶颈是每个分P 两次网络往返（探字幕轨 + 下字幕），不是带宽。
    改成线程池后同等工作量约 20-30 分钟。
    每个分P 内部仍保留 jitter 小睡，避免触发 B站限流（412）。
"""
import argparse
import importlib.util
import json
import pathlib
import random
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

SPEC = pathlib.Path(__file__).resolve().with_name('bili_analyze.py')
_spec = importlib.util.spec_from_file_location('ba', str(SPEC))
ba = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ba)

CATALOG = {
    '计算机': ['BV1Ye411Y7Ue', 'BV1Ay4y137RA', 'BV1KU4y167ds', 'BV1tNpbekEht',
             'BV1z84y1z7Vp', 'BV1ajMo6TEBm', 'BV17a7K64ELH', 'BV1Z4w3znE6h'],
    '高数': ['BV1Up4y1Y76a', 'BV1husGzwEtZ', 'BV1swAWerEzS', 'BV1X4411J792',
           'BV1vm421s7mv', 'BV12DdNYzEvy', 'BV1xxXZBKENv'],
    '政治': ['BV1PRM26hEbk', 'BV1TDj36dEdc', 'BV176gY6nEb3', 'BV1xzBCBFExz',
           'BV1gh9MBkEEC'],
    '英语': ['BV1rg411h7Z1', 'BV1brgBzNEbW', 'BV1Do4y1h7om', 'BV1jT4y1f7YA'],
}

# ★ E1（2026-09-20）：原来是相对路径 `Path('data/bili-analyze')`。
#   这个脚本常以「长任务」形式被从任意目录拉起（甚至被别的脚本 subprocess 调用），
#   相对路径下它会往一个**新建的空目录**里下载 1526 个分P，然后报告「全部成功」。
#   锚定到脚本位置：产出永远落在仓库的 data/bili-analyze/。
ROOT = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'bili-analyze'

_LOCK = threading.Lock()
_HIT = 0      # 新下载成功
_SKIP = 0     # 本地已有，跳过
_MISS = 0     # 该分P 无字幕轨
_FAIL = 0     # 下载/写盘失败
_SUSPECT = 0  # 下到了，但轨道没过 aid+cid 不变量校验（内容可能不是这个视频的）
_MISS_LIST = []
_FAIL_LIST = []
_SUSPECT_LIST = []
_SKIP_NOTRACK = 0   # 被 yt-dlp 普查判为「已登录且确认无轨」而**未做探测**的分P（--ytdlp-skip）
_SKIP_RECOVERED = 0  # 被 _verify2.jsonl 判为 recovered 而**未重下**的分P（保护好数据）

# ── 被吞掉的异常（2026-09-20，修 A6）────────────────────────────────
#   ★ 本文件原来有 4 处 `except Exception: pass`，而且**全是数据级的**：
#     _verify.jsonl 写不进去 / 读不出来 / 压缩失败 —— 后果是「已通过 aid+cid
#     校验」的记录静默丢失，下一轮把全部分P 重下。
#     「跑完了、看着成功、其实白干」是这类静默失败最贵的地方。
#   不改成 raise：这是 24 线程的长任务，单个分P 的落盘失败不该终止整轮。
#   但必须让人看见 —— 打印 + 计数，跑完在汇总里体现。
#   同一条消息只打第一次（并发下同一故障会重复几千次，刷屏等于没有告警）。
_WARN = {}
_WARN_LOCK = threading.Lock()


def _warn(msg):
    """报告一处被吞掉的异常。返回累计次数。"""
    with _WARN_LOCK:
        n = _WARN.get(msg, 0) + 1
        _WARN[msg] = n
        first = (n == 1)
    if first:
        print('  [警告] %s' % msg, file=sys.stderr, flush=True)
    return n


def _mark_verified(outfile, verified):
    """把「这条字幕有没有通过 aid+cid 校验」记到 <BV>/_verify.jsonl。

    为什么要落盘：B站 会返回**别的视频的字幕轨**，所以「文件非空」完全不能说明
    「内容是对的」。这份记录让后续可以定向重试未校验的分P，而不是全量重跑。

    格式是「追加」的 JSONL，同一个 p 可能出现多行，**后写的覆盖先写的**。
    跑完由 _compact_verify() 压缩成一行一个 p。
    """
    try:
        line = json.dumps({'p': int(re.search(r'p(\d+)', outfile.name).group(1)),
                           'ok': bool(verified)}, ensure_ascii=False)
        with _LOCK:
            with (outfile.parent / '_verify.jsonl').open('a', encoding='utf-8') as fh:
                fh.write(line + '\n')
    except Exception as e:
        # 校验状态没落盘 ⇒ 下一轮会把这个分P 当「未校验」重下。必须可见。
        _warn('写 _verify.jsonl 失败（%s，p 无法从 %r 解析或磁盘不可写）：%s'
              % (outfile.parent.name, outfile.name, e))


def _compact_verify(bvdir):
    """把 <BV>/_verify.jsonl 压缩成「一个分P 一行」的最终状态。"""
    f = bvdir / '_verify.jsonl'
    if not f.exists():
        return
    try:
        state = {}
        for ln in f.read_text(encoding='utf-8', errors='ignore').splitlines():
            try:
                o = json.loads(ln)
                state[int(o['p'])] = bool(o['ok'])
            except Exception as e:
                # 坏行 = 这个分P 的校验状态丢了 ⇒ 下一轮会重下它。
                # 原来 `pass` 掉，于是「压缩成功」和「压缩时丢了 20 条」看起来一样。
                _warn('_verify.jsonl 有无法解析的行（%s）：%s' % (f, e))
        with f.open('w', encoding='utf-8') as fh:
            for p in sorted(state):
                fh.write(json.dumps({'p': p, 'ok': state[p]}, ensure_ascii=False) + '\n')
    except Exception as e:
        # ★ 最危险的一处：`f.open('w')` 已经**截断了文件**，若随后写入失败，
        #   原记录就没了。这里至少要吼出来，别让它静默。
        _warn('压缩 _verify.jsonl 失败（%s，文件可能已被截断）：%s' % (f, e))


def _load_ytdlp_notrack(bvdir):
    """读 `<BV>/_ytdlp.jsonl`，返回「已登录且确认无轨」的分P 号集合。

    由 `scripts/bili_ytdlp.py` 生成（yt-dlp 的字幕轨**声明**普查）。

    ★ 为什么值得读：`probe_subtitle` 对**真无轨**的分P 会重试满 `PROBE_RETRIES`（12 次）
      才认输 —— 实测全库有 144 个 not-ok 分P，最坏就是 1728 次纯浪费的请求。
      yt-dlp 一次请求就能给出「这个分P 一条轨都没有」，于是可以直接跳过探测。

    ★ 只接受 `yt-dlp:no_track_authenticated` 这一种 source，**别的一律不跳过**：
      · `yt-dlp:claimed`                 → 有轨，必须走原探测（要拿 subtitle_url）
      · `yt-dlp:unknown_unauthenticated` → **未登录**，空结果不可信
      漏掉这条判断，就会把「没登录所以看不到」当成「确实没有」，**永久跳过有字幕的分P** ——
      正是本项目最贵的那类 bug（把「没查成」当「没有」）。
      所以判定条件写成「source 精确匹配 **且** claimed_langs 为空」，两重都不放松。

    ★ 未覆盖的分P 一律不跳过：返回集合只含普查**明确覆盖到**的分P。
      因此只探过 p1 的 BV，就只会跳过 p1 —— 不会因为「没数据」而误跳过。
    """
    f = pathlib.Path(bvdir) / '_ytdlp.jsonl'
    if not f.exists():
        return set()
    notrack = set()
    for ln in f.read_text(encoding='utf-8', errors='ignore').splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            o = json.loads(ln)
        except Exception as e:
            _warn('读取 _ytdlp.jsonl 行失败（%s）：%s' % (f, e))
            continue
        if (o.get('source') == 'yt-dlp:no_track_authenticated'
                and not o.get('claimed_langs')):
            notrack.add(o.get('p'))
    return notrack


def _load_verify2(bvdir):
    """读 `<BV>/_verify2.jsonl`（`bili_reclassify_unverified.py` 的产物），返回 {p: verdict}。

    verdict ∈ trusted / recovered / junk / unjudged。

    ★ 为什么下载器要关心它：`_verify.jsonl` 的 `ok:false` **不等于「内容是错的」**。
      实测 144 个 not-ok 分P 里，**19 个其实是好数据**（内容与同课程参考语料高度相似、
      且与本分P标题重合），只是当初探轨时 URL 没匹配上 aid+cid 不变量。
      `--refresh` 只看 `_verify.jsonl`，会把这 19 个**重下并覆盖** ——
      而新下到的很可能正是当初让它们失败的脏轨。**这是「用好数据换坏数据」。**

    ⇒ 所以 `--refresh` 默认**不碰** recovered 的分P；要重下得显式给 `--recheck-recovered`。
      （判据是启发式的，所以不写进 `_verify.jsonl` —— 那个文件只放确定性证据。）
    """
    f = pathlib.Path(bvdir) / '_verify2.jsonl'
    out = {}
    if not f.exists():
        return out
    for ln in f.read_text(encoding='utf-8', errors='ignore').splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            o = json.loads(ln)
            out[o['p']] = o.get('verdict')
        except Exception as e:
            _warn('读取 _verify2.jsonl 行失败（%s）：%s' % (f, e))
    return out


def fetch_one(subject, bv, page, outfile, sleep):
    """下载单个分P 的字幕。返回 'hit' / 'miss' / 'fail'。

    ★ 2026-09-18 修复两处，都源于「把瞬时故障当终态」：
      1) 原来只重试「下载」，不重试「探轨」。而 B站 的 subtitle_url 约 20% 概率
         返回空串（轨道在、URL 空），报错是 urllib 的 unknown url type: ''。
         实测 65 个这样失败的分P，复探 1-2 轮全部拿到 URL，**0 个真需 ASR**。
      2) probe_subtitle 现在内部已重试并会对持续故障 raise；这里接住后计入
         fail（不是 miss），保证「无字幕」这个数字只统计真无轨的分P。
    """
    global _HIT, _SKIP, _MISS, _FAIL, _SUSPECT
    cid, pno = page['cid'], page['page']

    # 探字幕轨。probe_subtitle 内部已做 4 次退避重试，这里再包一层兜底。
    subs = []
    try:
        subs, _need = ba.probe_subtitle(cid, bv)
    except Exception as e:
        with _LOCK:
            _FAIL += 1
            _FAIL_LIST.append('%s P%d 探轨失败:%s' % (bv, pno, e))
        return 'fail'

    if not subs:
        with _LOCK:
            _MISS += 1
            _MISS_LIST.append('%s P%d' % (bv, pno))
        return 'miss'

    url = subs[0].get('subtitle_url') or subs[0].get('subtitleUrl') or ''
    if url.startswith('//'):
        url = 'https:' + url
    if not url:
        # 走到这里说明 probe_subtitle 的判据失效了，别静默跳过。
        with _LOCK:
            _FAIL += 1
            _FAIL_LIST.append('%s P%d 轨道存在但 URL 为空' % (bv, pno))
        return 'fail'

    if not subs[0].get('_verified'):
        # probe_subtitle 没能拿到通过 aid+cid 不变量校验的轨 —— 内容可能不是这个视频的。
        with _LOCK:
            _SUSPECT += 1
            _SUSPECT_LIST.append('%s P%d' % (bv, pno))
    _mark_verified(outfile, bool(subs[0].get('_verified')))

    for attempt in (1, 2, 3):
        try:
            txt = ba.srt_to_text(url)
            # 先写临时文件再改名 —— 避免中断留下半截文件被误判为「已有」
            tmp = outfile.with_suffix('.part')
            tmp.write_text(txt, encoding='utf-8', newline='\n')
            tmp.replace(outfile)
            with _LOCK:
                _HIT += 1
            if sleep:
                time.sleep(sleep * (0.5 + random.random()))
            return 'hit'
        except Exception as e:
            if attempt == 3:
                with _LOCK:
                    _FAIL += 1
                    _FAIL_LIST.append('%s P%d 下载失败:%s' % (bv, pno, e))
                return 'fail'
            time.sleep(1.0 + random.random())
    return 'fail'


def main():
    global _SKIP, _SKIP_NOTRACK, _SKIP_RECOVERED
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default=None, help='只跑一科：计算机 / 高数 / 政治 / 英语')
    ap.add_argument('--bv', default=None, help='只跑某一条 BV（也可给逗号分隔的多条）')
    ap.add_argument('--sessdata', default=None)
    ap.add_argument('--jobs', type=int, default=6,
                    help='并发线程数。**默认 6**（保守，与脚本文档一致）。'
                         '实测 24 未触发 412，但那是单机单次的结果 —— '
                         '风控是按账号判的，所以把 24 留成显式选项：--jobs 24。'
                         '被限流就降到 1（退回串行）。')
    ap.add_argument('--sleep', type=float, default=0.15, help='每个分P 的抖动间隔基准秒数')
    ap.add_argument('--force', action='store_true',
                    help='忽略本地已有文件，全部重下。'
                         '★ 2026-09-18 必须用它一次：当时发现 B站 x/player/v2 会返回'
                         '**别的视频的字幕轨**，导致 1526 个文件里 1038 个内容是错的'
                         '（文件非空、格式合法、无报错）。修好判据后必须全量重下。'
                         '⚠️ 若待重下里存在**已通过 aid+cid 校验**的文件，'
                         '本脚本会拒绝执行并要求加 --yes 二次确认（见 D5 说明）。')
    ap.add_argument('--yes', action='store_true',
                    help='配合 --force：确认「用新下载覆盖已校验通过的文件」。'
                         '★ 只在确实要全量重下时用 —— 已校验的文件是好数据，'
                         '而 --force 不备份、直接覆盖。')
    ap.add_argument('--refresh', action='store_true',
                    help='只重下「缺失」或「未通过 aid+cid 校验」的分P（读 <BV>/_verify.jsonl）。'
                         '★ 长任务请用这个而不是 --force —— 它可断点续传：'
                         '跑一半被中断，重跑只会补没做完的，不会重头再来。')
    ap.add_argument('--probe-retries', type=int, default=None,
                    help='覆盖 ba.PROBE_RETRIES（★ 默认已改为 12）。'
                         '退回保守值用 40：把握更高，但尾巴慢 3.3 倍'
                         '（见 scripts/bili_bench_retry.py 实测）')
    ap.add_argument('--probe-sleep', default=None,
                    help='覆盖 ba.PROBE_SLEEP，格式 "lo,hi" 秒（★ 默认已改为 "0.05,0.15"）。'
                         '退回旧值用 "0.3,0.8"')
    ap.add_argument('--ytdlp-skip', action='store_true',
                    help='用 yt-dlp 普查（<BV>/_ytdlp.jsonl）跳过「已登录且确认无轨」的分P，'
                         '不做探测。省掉每个分P 的 12 次无用重试。'
                         '★ 先跑 scripts/bili_ytdlp.py 生成普查；'
                         '只读 yt-dlp:no_track_authenticated 这一种结论，未登录的空结果不会跳过。')
    ap.add_argument('--recheck-recovered', action='store_true',
                    help='允许 --refresh 重下「_verify2.jsonl 判为 recovered」的分P。'
                         '★ 默认不重下：那些文件的内容其实是对的（只是当初 URL 没匹配上不变量），'
                         '重下很可能拿回脏轨 —— 等于用好数据换坏数据。')
    ap.add_argument('--dry-run', action='store_true',
                    help='只打印本次会下载哪些分P，不实际下载。'
                         '★ 长任务起跑前先看一眼 —— 尤其确认 --force 的覆盖范围。')
    a = ap.parse_args()

    if a.probe_retries is not None:
        ba.PROBE_RETRIES = a.probe_retries
    if a.probe_sleep:
        lo, hi = [float(x) for x in a.probe_sleep.split(',')]
        ba.PROBE_SLEEP = (lo, hi)
    overridden = a.probe_retries is not None or a.probe_sleep
    print('探测参数：retries=%d sleep=%s%s'
          % (ba.PROBE_RETRIES, ba.PROBE_SLEEP,
             '' if overridden else '  ← 默认快路径（2026-09-19 起）'))

    sd, src = ba.get_sessdata(a.sessdata)
    if not sd:
        raise SystemExit('!! 没有 SESSDATA。先跑：python scripts/bili_login.py --html qr.html')
    ba.COOKIE = sd
    print('SESSDATA: 已加载（来源 %s）' % src)
    print('并发：%d 线程' % a.jobs)
    print()

    # 1) 收集任务
    tasks = []
    # ★ D5（2026-09-20）：`--force` 会把「已校验通过」的文件也重下 —— 不备份、直接覆盖。
    #   原来它无条件 `need = True`，于是「想补几个缺的」误传 --force 就会
    #   **用好数据换坏数据**（新下载可能失败/拿到错轨，而旧的已经校验过）。
    #   这里先数出「会被覆盖且已校验」的分P 数量，>0 且没给 --yes 就拒绝执行。
    #   不写成交互式提问：这个脚本常在无人值守的长任务里跑，input() 会把它挂住。
    risk_overwrite = 0
    for subject, bvs in CATALOG.items():
        if a.only and a.only != subject:
            continue
        for bv in bvs:
            if a.bv and bv not in [x.strip() for x in a.bv.split(',')]:
                continue
            try:
                m = ba.get_meta(bv)
            except Exception as e:
                print('%s 取元数据失败：%s' % (bv, e))
                continue
            outdir = ROOT / bv
            outdir.mkdir(parents=True, exist_ok=True)
            # 读已校验记录：{p: bool}
            verified = {}
            vf = outdir / '_verify.jsonl'
            if vf.exists():
                for ln in vf.read_text(encoding='utf-8', errors='ignore').splitlines():
                    try:
                        o = json.loads(ln)
                        verified[o['p']] = o['ok']   # 后写的覆盖先写的
                    except Exception as e:
                        # 这一行读不出来 ⇒ 该分P 的校验状态未知 ⇒ 会被当「未校验」重下。
                        _warn('读取 _verify.jsonl 行失败（%s）：%s' % (vf, e))
            if a.refresh:
                # ★ 不要清空 _verify.jsonl！清空会让下一轮把「已校验通过」的分P
                #   当成「无记录」重新下载。实测代价：第二轮白下了 1468 个分P。
                #   正确做法是继续追加（read_verify 里「后写的覆盖先写的」），
                #   跑完后由 _compact_verify() 去重压缩。
                pass
            # ★ 可选（--ytdlp-skip）：yt-dlp 普查里「已登录且确认无轨」的分P
            #   直接**不进任务队列**。在收集阶段过滤，不动 fetch_one 的热路径
            #   （那里是 24 线程并发，改动风险高得多）。
            notrack = _load_ytdlp_notrack(outdir) if a.ytdlp_skip else set()
            v2 = _load_verify2(outdir)
            n_new = 0
            n_nt = 0
            n_rc = 0
            for p in m['pages']:
                f = outdir / ('subtitle_p%02d.txt' % p['page'])
                exists = f.exists() and f.stat().st_size > 0
                pno = p['page']
                is_rec = (v2.get(pno) == 'recovered')
                if a.refresh:
                    need = (not exists) or (not verified.get(pno, False))
                elif a.force:
                    need = True
                    # ★ 判 recovered 的也是好数据，--force 覆盖它们同样要过 --yes
                    if exists and (verified.get(pno, False) or is_rec):
                        risk_overwrite += 1
                else:
                    need = not exists
                if not need:
                    _SKIP += 1
                    continue
                # ★ 内容已判「其实是对的」→ --refresh 默认不重下（详见 _load_verify2 注释）
                if a.refresh and is_rec and not a.recheck_recovered:
                    _SKIP_RECOVERED += 1
                    n_rc += 1
                    continue
                if notrack and pno in notrack:
                    _SKIP_NOTRACK += 1
                    n_nt += 1
                    continue
                tasks.append((subject, bv, p, f))
                n_new += 1
            extra = ''
            if n_nt:
                extra += '，yt-dlp 确认无轨跳过 %d P' % n_nt
            if n_rc:
                extra += '，recovered 保护 %d P' % n_rc
            print('[%s] %-14s 共 %3d P，待下载 %3d  P%s  %s'
                  % (subject, bv, len(m['pages']), n_new, extra, m['title'][:32]))

    # ★ 2026-09-21：`--dry-run` —— 任务收集完成后立刻短路，只打印计划、不发请求。
    #   刻意放在 D5 护栏**之前**：预览不具破坏性，不该被护栏拦下；但真要覆盖
    #   已校验文件时，把护栏那句结论照打出来（让用户先看到「真跑会被拒」）。
    #   放在 D5 之后则相反 —— 预览被拦掉、看不到覆盖范围，工具就白加了。
    if a.dry_run:
        print()
        print('（--dry-run：只预览，不下载）')
        if not tasks:
            print('没有待下载的分P —— 真跑不会发出任何下载请求。')
        else:
            by_bv = {}
            for subject, bv, p, f in tasks:
                by_bv.setdefault((subject, bv), []).append(p['page'])
            print('将下载 %d 个分P，涉及 %d 条 BV：' % (len(tasks), len(by_bv)))
            for (subject, bv), pages in sorted(by_bv.items()):
                pages = sorted(pages)
                shown = ', '.join('p%d' % x for x in pages[:24])
                if len(pages) > 24:
                    shown += ' …'
                print('  [%s] %-14s %3d P：%s' % (subject, bv, len(pages), shown))
        if a.force:
            print()
            print('⚠️ --force：本次将覆盖 %d 个文件，其中 %d 个**已通过 aid+cid 校验**。'
                  % (len(tasks), risk_overwrite))
            if risk_overwrite and not a.yes:
                print('   ✗ 真跑会被 D5 护栏拒绝 —— 要么改用 --refresh，要么显式加 --yes。')
        print()
        print('（预览结束，未发出任何下载请求）')
        return 0

    # ★ D5 护栏：`--force` 要覆盖「已校验通过」的文件时，必须显式二次确认。
    if a.force and risk_overwrite and not a.yes:
        print('✗ 拒绝执行：--force 会覆盖 %d 个**已通过 aid+cid 校验**的分P。' % risk_overwrite)
        print('  这些是好数据，而 --force 不备份、直接覆盖 —— 下载失败或再拿到错轨，')
        print('  就变成「用好数据换坏数据」，且旧文件已经没了。')
        print()
        print('  通常你要的是「只补缺失/未校验的」，那是另一个开关：')
        print('      python scripts/bili_fetch_subs.py --refresh')
        print('  确实要全量重下，就显式确认：')
        print('      python scripts/bili_fetch_subs.py --force --yes')
        return 1

    print()
    if not tasks:
        bits = []
        if _SKIP:
            bits.append('已有 %d 个' % _SKIP)
        if _SKIP_RECOVERED:
            bits.append('%d 个已判 recovered（内容是对的，受保护未重下）' % _SKIP_RECOVERED)
        if _SKIP_NOTRACK:
            bits.append('%d 个由 yt-dlp 判为「确认无轨」（仍需 ASR）' % _SKIP_NOTRACK)
        if bits:
            print('没有待下载的分P —— ' + '，'.join(bits) + '。')
        else:
            print('没有待下载的分P —— 全部已就绪。')
    else:
        if a.force:
            print('⚠️ --force 全量重下：本次将覆盖 %d 个文件（其中已校验 %d 个）'
                  % (len(tasks), risk_overwrite))
        print('开始下载 %d 个分P…' % len(tasks))
        done = 0
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=a.jobs) as ex:
            futs = [ex.submit(fetch_one, s, b, p, f, a.sleep) for s, b, p, f in tasks]
            for fu in as_completed(futs):
                fu.result()
                done += 1
                if done % 50 == 0 or done == len(tasks):
                    el = time.time() - t0
                    rate = done / el * 60 if el else 0
                    eta = (len(tasks) - done) / rate if rate else 0
                    print('  进度 %d/%d  已用 %.1f 分  速度 %.0f 个/分  预计剩余 %.1f 分'
                          % (done, len(tasks), el / 60, rate, eta))

    # 压缩校验记录：一个分P 一行
    for d in ROOT.iterdir():
        if d.is_dir() and d.name.startswith('BV'):
            _compact_verify(d)

    print()
    print('=' * 58)
    print('新增 %d | 已有跳过 %d | 无字幕轨 %d | 失败 %d | 未校验 %d'
          % (_HIT, _SKIP, _MISS, _FAIL, _SUSPECT))
    if _SKIP_NOTRACK:
        print('★ 另有 %d 个分P 由 yt-dlp 普查判为「确认无轨」，未做探测（--ytdlp-skip）'
              % _SKIP_NOTRACK)
        print('  省下约 %d 次探测请求（%d 次/分P）—— 但它们**仍计入「无字幕」，需走 ASR**'
              % (_SKIP_NOTRACK * ba.PROBE_RETRIES, ba.PROBE_RETRIES))
    if _SKIP_RECOVERED:
        print('★ 另有 %d 个分P 已判 recovered，受保护未重下（_verify2.jsonl）' % _SKIP_RECOVERED)
        print('  这些文件内容其实是对的（当初只是 URL 没匹配上 aid+cid 不变量）；'
              '要重下用 --recheck-recovered')
    if _MISS_LIST:
        print('无字幕的分P（必须走 ASR）：%d 个' % len(_MISS_LIST))
        print('  ' + ', '.join(_MISS_LIST[:20]) + (' …' if len(_MISS_LIST) > 20 else ''))
    if _FAIL_LIST:
        print('失败的分P（重跑本脚本会自动重试）：%d 个' % len(_FAIL_LIST))
        print('  ' + ', '.join(_FAIL_LIST[:10]) + (' …' if len(_FAIL_LIST) > 10 else ''))
    if _SUSPECT_LIST:
        print()
        print('⚠️ 未通过 aid+cid 校验的分P：%d 个 —— 内容可能不是这个视频的，'
              '必须跑 bili_audit_subtitle_content.py 复核' % len(_SUSPECT_LIST))
        print('  ' + ', '.join(_SUSPECT_LIST[:20]) + (' …' if len(_SUSPECT_LIST) > 20 else ''))

    # ★ A6（2026-09-20）：把「被吞掉的异常」摆到汇总里。
    #   放在最末、带退出码 —— 上面那些计数只说明「下载结果」，
    #   这一节说明「记账本身可不可信」。两者缺一不可：
    #   _verify.jsonl 写失败时，上面的「已有跳过」会虚低，而没人会知道。
    if _WARN:
        print()
        print('⚠️ 有 %d 类异常被吞掉（详见上方 [警告] 行）—— 记账可能不完整：'
              % len(_WARN))
        for msg, n in sorted(_WARN.items(), key=lambda kv: -kv[1]):
            print('   %4d 次  %s' % (n, msg))
        print('   影响：_verify.jsonl 缺失会让下一轮把已校验的分P 当未校验重下。')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
