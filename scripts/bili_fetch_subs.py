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
             'BV1z84y1z7Vp', 'BV1ajMo6TEBm', 'BV17a7K64ELH', 'BV1Z4w3znE6h',
             # ★ 2026-10-04 新增：严蔚敏《数据结构》清华 C 语言版全视频（92P / 63:12:28）。
             #   加它的原因：数据结构 2.1–2.9 笔记把它当**系统课**引用了 11 处
             #   （P2~P3 / P4~P6 / P7~P18 / P19~P27 / P25 / P28~P32 / P33~P36 /
             #    P37~P40 / P41~P44 / P46~P60），但字幕一直没下 ⇒ 引用悬空、无法回查。
             #   ⚠️ 它**不在** 141 总索引里（索引是从本 CATALOG 生成的），
             #   补进 CATALOG 后索引应同步 +1（见备考计划/B站资源利用率评估-2026-10-04.md §6 动作 5）。
             'BV11T411q7Qw',
             # ★ 2026-10-04 新增（第 2 批）：两个**被笔记引用但本地无字幕**的悬空源。
             #   ① `BV1dr4y1n7vA` 浙大翁恺《C 语言程序设计》—— 被 **10 处**笔记引用
             #      （1.7 函数 P68~74 · 1.8 指针 P81~P87/P84 · 1.9 结构体 P85 ·
             #       1.11 运行环境 P1~P10/P19 · 3.3 编程题 P25~P40 · 资源图谱），
             #      评级 ⭐⭐⭐⭐⭐「最严谨，作用域/传参讲透」，但**字幕一直没下** ⇒ 引用悬空、无法回查。
             #   ② `BV1sz4y1a7cP` 易懂C「联合 union 共用体」15 分钟 —— 1.9 结构体与共用体 引用 1 处。
             'BV1dr4y1n7vA', 'BV1sz4y1a7cP',
             # ★ 2026-10-22：D 盘音频库新增源（第 4 批），均实测有 AI 字幕：
             #   BV1RwXvBpE7q 一灯computer《广东省计算机专升插本精讲课》34 集 / 15.5h
             #   BV1QN411B7Qo 专升本老唐《计算机历年真题详解》3 集 —— 真题类，P1 口径
             #   注意 `BV1QN411B7Qo` **不在** `D:/专升本资料/_manifest/survey.json` 里
             #   （目录存在但 survey 漏登记），集数以实际 3 个 m4a 为准。
             'BV1RwXvBpE7q', 'BV1QN411B7Qo'],
    '高数': ['BV1Up4y1Y76a', 'BV1husGzwEtZ', 'BV1swAWerEzS', 'BV1X4411J792',
           'BV1vm421s7mv', 'BV12DdNYzEvy', 'BV1xxXZBKENv',
           # ★ 2026-09-25 新增：之了专升本《2027年广东专升本高等数学零基础全套课程》
           #   106 分P / 53:44:20 / 稿件 pubdate 2026-05-20，已完结，非付费稿件
           #   （rights.pay=0、is_upower_exclusive=None）。
           #   ⚠️ `--bv` 只在本 CATALOG 内做过滤，不在清单里的 BV 会被**静默跳过** ——
           #   这正是「明明给了 BV 却什么都没下」的原因，必须登记在这里。
           'BV18CL26WEJ3',
           # ★ 2026-10-22：D 盘音频库新增源（见下方第 4 批说明）
           #   BV1je41157EL 阿廖呀《专升本2022数学真题讲解》1 集 —— 真题类，P1 口径
           #   BV1SnYF6eEcC 米哥《专升本高等数学全程班27年》60 集 —— 有轨，但属
           #   **第 4 门同质高数全程班**，`_LOCAL-ASSETS-AUDIT.md` §2.3 判定「不提炼」。
           #   登记它的唯一目的是留档（字幕可下，将来查漏时才用），不占 P0/P1 提炼队列。
           'BV1je41157EL', 'BV1SnYF6eEcC'],
    '政治': ['BV1PRM26hEbk', 'BV1TDj36dEdc', 'BV176gY6nEb3', 'BV1xzBCBFExz',
           'BV1gh9MBkEEC',
           # ★ 2026-10-22（第 4 批续）：D 盘音频库的两门政治课。
           #   ⚠️ 更正一条旧结论：此前记的「政治 5 源全部无字幕轨、B 站这条路走死」
           #   **是错的**。那次探测打在 `x/player/wbi/v2` 的降级窗口上（该端点会把
           #   subtitle 置 null 而 code 仍为 0）。修好双端点兜底后重探：
           #     BV1YJM46XEud 阿来 58 集 → **28 集有轨**（48%）
           #     BV1FWiLeFECK 郑多分 19 集 → 待复测
           #   所以政治不是 0 供给，是「部分有轨 + 部分要 ASR」。
           'BV1YJM46XEud', 'BV1FWiLeFECK'],
    # ★ 2026-10-22 新增（第 4 批）：D 盘音频库 `D:/专升本资料/` 里 8 个本地字幕库没有的 BV。
    #   背景：见 `data/bili-analyze/_extract/_LOCAL-ASSETS-AUDIT.md` §2.2 / §4。
    #   逐个探过轨，只有下面 6 个有 AI 字幕；郑多分 BV1FWiLeFECK（19 集）与
    #   阿来 BV1YJM46XEud（58 集）**逐分P 全量探完 0/58 有轨**，不登记（政治只能走 ASR）。
    #   ⚠️ `--bv` 只在本 CATALOG 内做过滤，不在清单里的 BV 会被**静默跳过**。
    # ★ 2026-10-04 新增（第 3 批）：**广东专插本英语源** —— 修「英语栏 120 个 BV 全是高考口径」的结构错位。
    #   背景：总索引 §3.1 实查发现 119/120 个英语 BV 来自 `FREE高考英语` 一个 UP 主（高考口径），
    #   唯一真·广东源 `BV11dHvz7Epz` 反而只在正文里提过、**从未登记进 CATALOG** ⇒ 引用悬空。
    #   本批 5 个：4 个广东真题 + 1 个广东适用语法课（均为 `bili_search.py` 实搜所得，非猜）。
    '英语': ['BV1rg411h7Z1', 'BV1brgBzNEbW', 'BV1Do4y1h7om', 'BV1jT4y1f7YA',
           # ① 真·广东真题（2025）—— 唯一被正文点名「比 120 个高考 BV 都更贴近考试」的源，补登记
           'BV11dHvz7Epz',
           # ② 真·广东真题（2026）· 简言英语-提分Studio · 44 分钟
           'BV1Z7Nc67E8V',
           # ③ 真·广东真题（2022-2024 三年详解）· 阳哥英语 · 238 分钟
           'BV1cxrzY9Ea5',
           # ④ 广东省 2025 真题讲解 · 小豚专升本英语 · 125 分钟
           'BV1yEen6nEEY',
           # ⑤ 广东适用语法精讲（广东/江西/福建）· 专插本英语Nana · 1430 分钟
           'BV1QKbZ6xEea',
           # ★ 2026-10-22：D 盘音频库新增源（第 4 批），两门都是真·广东口径且有 AI 字幕：
           #   BV17b7664EZL 秦天《27年专升本英语零基础系统课》125 集 / 40.1h
           #   BV1UXdhBCEkb 刘晓艳《专升本英语语法精讲》21 集 / 11.7h
           #   合计 146 集 —— 与 `D:/专升本资料/02_英语/` 的集数完全对上，无重复。
           'BV17b7664EZL', 'BV1UXdhBCEkb'],
    # ★ 2026-09-24 新增：B站「FREE高考英语」(mid 2742391) 全频道。
    #   普查产出见 out/free-up.json（合集结构）+ out/free-census.json（分P/时长）。
    #   合计 116 个 BV / 1072 个分P / 623 小时。
    #   分成两组：广东专升本英语不考听力/续写/口语，那 105 小时单独成组，
    #   方便 --only 高考英语 跳过，需要时再补 --only 高考英语-不考。
    '高考英语': [
        'BV1MWhJ67EkY', 'BV1rBe66MEZU', 'BV1FXec6xEJT', 'BV1dnY76tEEq',
        'BV1xgbM6zE5i', 'BV192t663Esq', 'BV1Phtd6qE4h', 'BV1gRtJ6LE6P',
        'BV1F2hG6EEUq', 'BV1oFth6DE28', 'BV1rRGG6TEqE', 'BV17HTi6JErn',
        'BV12dGnzUEFN', 'BV1MY4y1P7Jj', 'BV1rXuzzXEsm', 'BV1vb421H71y',
        'BV1UM4m127xY', 'BV1S4421U7wT', 'BV1ni421h7Vm', 'BV1aU411U7SG',
        'BV1H4421S7Tg', 'BV1Yr421M76r', 'BV1waU3YaE5X', 'BV1TKeE6DEr4',
        'BV1zc411y7p9', 'BV14g4y1Q753', 'BV1vWgezcE7M', 'BV1He4y1r7fc',
        'BV1y3xweeEnJ', 'BV1nxun6JECX', 'BV138411V7uR', 'BV1pMm2BnE3u',
        'BV1SUqpBBE7d', 'BV1z4BKBkEjG', 'BV1dWgezcEYS', 'BV1xj411R75q',
        'BV1w14y117wg', 'BV1Mz4y157dP', 'BV1aG41117RC', 'BV17M411D7kh',
        'BV1ru4y1j7Z1', 'BV1eC4y1R7Bp', 'BV1jyKQ6dEDs', 'BV1FFM36HEJM',
        'BV13wrLBaE2t', 'BV1EyMVzuExP', 'BV1RAMFzfEoJ', 'BV1yVNzzyEsK',
        'BV1KmwJe8E7a', 'BV1DJ4m1M7Zj', 'BV1US411P7Fi', 'BV1Bb421n7re',
        'BV1WV411R7UU', 'BV1cQ4y1L7Hq', 'BV1wQ4y1L7iD', 'BV1CN4y1H78q',
        'BV1Bg4y1S7rg', 'BV1Zc411x7eZ', 'BV1eW4y1A7aK', 'BV1ne411v7Fe',
        'BV1W1RABDEKv', 'BV1DK411v7do', 'BV1F94y1M7cr', 'BV1Ka4y117hH',
        'BV177Vz63EHv', 'BV1k3Mh6yEJD', 'BV13B4y1B7un', 'BV1QvtC6LE8e',
        'BV1LQbE6HEFF', 'BV1VTbx6vEhm', 'BV1BqYE6iEz3', 'BV1b5Yt6VEHT',
        'BV1ujY86SExR', 'BV17QYV6DEV3', 'BV1BZY76AEme', 'BV15bY96fE8g',
        'BV1S6Y96nEJC', 'BV1vNYr6dEuN', 'BV1zoY66wEx4', 'BV1xaY16REU4',
        'BV14bY16dESb', 'BV1iheE6eEm9', 'BV1nHeE66ErW', 'BV1pshi6DEps',
        'BV17BhB6SEex', 'BV1N8hk6rE3p', 'BV1mnh766Eq3', 'BV17r8F6gE2u',
        'BV1544y1L74x', 'BV1Uq4y1B7F8', 'BV1X64y1e71c', 'BV1tP4y1p7zd',
        'BV16q4y1M7jZ', 'BV13M4y1V7nx', 'BV1744y1C7wh', 'BV1JM4y1M7ju',
        'BV1Wh411h7q3'
    ],
    '高考英语-不考': [
        'BV1V84y1v7PU', 'BV1T27V6cEtV', 'BV1eSu6zCEJT', 'BV1H1gt6kELg',
        'BV1aogZ61ECz', 'BV1sB316PEQv', 'BV1tg8j6vEJD', 'BV1TY876zEUU',
        'BV18EuMz1Ejp', 'BV13iGNz7ExF', 'BV1dtGNzQEKo', 'BV1ufGPzkEyQ',
        'BV1MwGNz6EMf', 'BV1GXGPz2EMU', 'BV1r1Ggz1Eem', 'BV14vGgzpEK4',
        'BV1LZGgzqEbT', 'BV1zuGgzgEux', 'BV1fuGgzgEeq'
    ],

    # ================================================================ 日语
    # ★ 2026-10-22 新增。背景：`D:/学习资料/08-Study/japanese-kb/` 已有 3.1 GB
    #   官方素材库（Irodori 四册 + Tadoku 分级读物 + JLPT 官方样题 + Tae Kim 语法），
    #   骨架是**标日 104 课**，但**没有任何视频课、没有字幕、没有中文讲解**。
    #   所以日语这边的缺口不是「教材」，是「讲解」——本组就是补这一块。
    #
    # 分级依据与筛选理由见 `data/bili-analyze/_extract/_JP-TARGET-VIDEOS.md`。
    # 下面只登记**抽样确认有 AI 字幕轨**的，无轨的单独列在注释里（要 ASR，不进本组）。
    #
    #   ── J0 体系主线（N5→N1 全程）──
    #   BV1m7411B7eK  lk_qhd《N5~N2日语语法详解》375P / 31h / 206万播放
    #                 纯语法，375 个短分P，粒度和标日 104 课最贴，抽样 3/3 有轨
    #   BV1v34y1Z7rQ  言趣日语木子老师《0-N1全套合集》144P / 95.8h / 137万播放
    #                 抽样 3/3 有轨，是**免费全程最长**的一套
    #   BV1j741167og  周业繁《大家的日本语 零基础课程》150P / 37.3h / 334万播放
    #                 【合集】【完】，N5–N4 段最扎实
    #
    #   ── J1 分级专项（蓝宝书 / 新完全掌握 / 日本語の森）──
    #   BV1bB4y1u78T  いねい《蓝宝书 N3 语法 1–20 单元》20P / 9.4h  【完结】抽样 3/3
    #   BV1xA411b7ri  周业繁《免费 N3 语法课程》41P / 11.3h / 138万播放  抽样 3/3
    #   BV1464y1U7RL  和洋外语私塾《N1 蓝宝书语法精讲》33P / 14.8h（更新完毕）抽样 2/3
    #   BV1L54y1Q7fj  无良骚年a《日本人为你讲解 N1 语法 日本語の森》144P / 20.8h 抽样 1/3
    #
    #   ── J2 口语会话（「怎么说日语」）──
    #   BV133411L7st  皆传日语《新影子跟读法 日本語を話そう 初~中級》19P / 3.8h / 72万播放 抽样 2/3
    #   BV1AP411t7cS  不给量就捣蛋《日语口语全面精讲》81P / 29h  抽样 1/3
    #   BV1k14y1M7yV  awaoo0o0《NHK WORLD 商务日语 中日双语》30P / 7.5h  抽样 1/3
    #
    #   ── J3 发音 / 声调 ──
    #   BV1zh411v7DW  日语老师林梓岸《日语声调轻松搞定》4P / 25min  抽样 3/3
    #
    #   ⛔ 抽样 0/3 无轨（要 ASR，不进本组，避免白抓）：
    #   BV1Ti4y1X7yZ 圆圆 新标日初级上 83P｜BV1c7wuzSEYz 谷安 N2语法 170P
    #   BV1He4y1q7ys Sinn桑 新完全掌握N1语法 19P｜BV1g64y1t7k9 肥喵 アクセント 43P
    #   ⛔ 标题党搬运（「全400集」「允许白嫖」「整理成动画片」同一套模板）：
    #   BV1WTnozqEd3 BV1PM9YBvEQs BV1BRevzwE3w BV1qDtKe3EMA BV1oeWw6cEtT BV14T4y1Y78G
    '日语': [
        'BV1m7411B7eK', 'BV1v34y1Z7rQ', 'BV1j741167og',
        'BV1bB4y1u78T', 'BV1xA411b7ri', 'BV1464y1U7RL', 'BV1L54y1Q7fj',
        'BV133411L7st', 'BV1AP411t7cS', 'BV1k14y1M7yV',
        'BV1zh411v7DW',
    ],
}

# ★ E1（2026-09-20）：原来是相对路径 `Path('data/bili-analyze')`。
#   这个脚本常以「长任务」形式被从任意目录拉起（甚至被别的脚本 subprocess 调用），
#   相对路径下它会往一个**新建的空目录**里下载 1526 个分P，然后报告「全部成功」。
#   锚定到脚本位置：产出永远落在仓库的 data/bili-analyze/。
ROOT = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'bili-analyze'

# ★ 2026-09-24：元数据写回缓存。
#   原来本脚本在收集阶段调 `ba.get_meta(bv)`（每个 BV 一次），但**不写**
#   `_part_titles_all.json`；而 `bili_build_units.py` 的 `get_titles()` 只认那个
#   缓存，读不到就**再调一次** get_meta。于是同一批元数据被付了两遍。
#   实测（2026-09-24，97 个 BV）：元数据单次中位 869 ms ⇒ 白花 84 s，
#   而当时整个抓取段（元数据+下载+切片+过滤）合计才 364 s —— **46% 是重复劳动**。
#   详见 docs/guide/bili-subtitle-pipeline-perf.md §八。
TITLE_CACHE = ROOT / '_part_titles_all.json'


def _load_title_cache() -> dict:
    try:
        return json.loads(TITLE_CACHE.read_text(encoding='utf-8'))
    except Exception:
        return {}


def _save_title_cache(db: dict) -> None:
    """写回缓存。

    ★ 刻意吞掉异常：这是**非承重**步骤。缓存写失败不该让一个已经跑了几十分钟的
      下载任务整体失败（同 skill 里「cleanup must never fail the job」那条）。
    """
    try:
        TITLE_CACHE.parent.mkdir(parents=True, exist_ok=True)
        TITLE_CACHE.write_text(json.dumps(db, ensure_ascii=False, indent=1),
                               encoding='utf-8', newline='\n')
    except Exception as e:
        print('  (warn) 标题缓存写回失败，不影响本次下载：%s' % e)


def _cache_entry(m: dict) -> dict:
    """与 `bili_build_units.get_titles()` 的读法保持一致（title/owner/pages）。"""
    return {
        'title': m['title'],
        'owner': m.get('owner', ''),
        'pages': [{'p': p['page'], 'part': p['part'], 'dur': p['duration']}
                  for p in m['pages']],
    }


# ★ 2026-09-24：元数据也要重试。
#   事故：抓「FREE高考英语」时 `BV1MY4y1P7Jj`（零基础训练，20 个分P / 43.8 小时）
#   的 get_meta 撞上一次瞬时 SSL 错误
#   （`SSL: UNEXPECTED_EOF_WHILE_READING`），收集循环 `continue` 掉了整支视频 ——
#   **20 个分P 一个没下，目录都没建，而且日志里只有一行，混在 97 行里看不出来。**
#   重跑时单独调 get_meta 是成功的（code 0 / 20 分P），确认是瞬时故障。
#
#   教训与探轨那边完全同构：**一个 BV 的元数据失败 = 整支视频被静默丢弃**，
#   代价远大于一次重试。宁可慢 1.6 秒，不可丢 43.8 小时。
META_RETRIES = 3
_META_FAILED: list[str] = []

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
    # ★ 2026-09-24：本阶段已经取过元数据，顺手写回缓存，供 build_units 复用。
    _title_db = _load_title_cache()
    for subject, bvs in CATALOG.items():
        if a.only and a.only != subject:
            continue
        for bv in bvs:
            if a.bv and bv not in [x.strip() for x in a.bv.split(',')]:
                continue
            m = None
            last_err = None
            for attempt in range(META_RETRIES):
                try:
                    m = ba.get_meta(bv)
                    break
                except Exception as e:
                    last_err = e
                    if attempt + 1 < META_RETRIES:
                        time.sleep(0.8 + attempt * 0.8)
            if m is None:
                # ★ 不要静默丢弃：见 META_RETRIES 的注释（丢一支 = 丢几十个分P）
                _META_FAILED.append('%s（重试 %d 次仍失败）：%s'
                                    % (bv, META_RETRIES, last_err))
                print('[%s] %-14s ✗ 取元数据失败（重试 %d 次）：%s'
                      % (subject, bv, META_RETRIES, last_err))
                continue
            _title_db[bv] = _cache_entry(m)     # ★ 见 TITLE_CACHE 注释
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

    # ★ 2026-09-24：收集阶段结束，把本阶段取得的元数据一次性写回缓存。
    #   放在这里而不是每个 BV 后立即写：97 次重写整个 JSON 是纯 I/O 浪费，
    #   而这一阶段总耗时只有百来秒，中途崩了重跑代价可接受。
    _save_title_cache(_title_db)

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
    if _META_FAILED:
        print()
        print('⚠️ 整支视频被跳过：%d 个 BV（元数据重试 %d 次仍失败）'
              % (len(_META_FAILED), META_RETRIES))
        for line in _META_FAILED:
            print('  ' + line)
        print('  这些 BV 的**所有分P**都没进任务队列，不计入上面的任何数字。'
              '重跑本脚本会自动补。')
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
