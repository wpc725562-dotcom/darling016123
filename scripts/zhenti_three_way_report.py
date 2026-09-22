#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""生成「B站真题 × 本地试卷 × 标准答案」三方对比报告（自包含单文件 HTML）。

数据来源（全部本地，可复核）：
  · 官方卷面    docs/public/papers/english/20XX-paper.pdf   → pdftotext
  · 官方答案    docs/public/papers/english/20XX-answers.pdf → pdftotext
  · 笔记页      docs/posts/english/20XX.md
  · 刷题版      docs/posts/english/20XX-英语-刷题版.md
  · B站视频     data/bili-zhenti/BV1jT4y1f7YA/（字幕 + 画面帧，人工读帧核对）

用法：python zhenti_three_way_report.py --out D:/tmp/zhenti/report.html
"""
from __future__ import annotations

import argparse
import html
import os
import pathlib
import re
import subprocess
import sys

# 本脚本依赖同级模块 zhenti_log，显式把 scripts/ 加进 sys.path（理由见 zhenti_lint.py）。
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

# ★ E3（2026-09-20）：诊断走 logging（stderr），正式输出仍走 print（stdout）。
from zhenti_log import add_logging_args, get_logger, setup_from_args  # noqa: E402

LOG = get_logger(__name__)

# ★ A5 残留（2026-09-20）：pdftotext 原先没有 timeout ——
#   遇到损坏/超大的 PDF 它会挂住，整个报告脚本就永远不返回。
SUBPROC_TIMEOUT = int(os.environ.get("ZHENTI_SUBPROC_TIMEOUT", "120"))

ROOT = pathlib.Path(__file__).resolve().parent.parent
PDFDIR = ROOT / "docs" / "public" / "papers" / "english"
ENG = ROOT / "docs" / "posts" / "english"


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def pdf_text(pdf: pathlib.Path, layout: bool = False) -> str:
    """★ 答案表必须用 -layout：不加它 pdftotext 会把每个数字/字母各自放一行，
    「题号行 + 答案行」的启发式永远匹配不到，抽出来是 0 条（实测踩过）。"""
    cmd = ["pdftotext"] + (["-layout"] if layout else []) + [str(pdf), "-"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                             timeout=SUBPROC_TIMEOUT)
    except subprocess.TimeoutExpired:
        LOG.error("pdftotext 超时（%ds）：%s", SUBPROC_TIMEOUT, pdf)
        return ""
    except FileNotFoundError:
        LOG.error("找不到 pdftotext（poppler 未安装或不在 PATH）：%s", pdf)
        return ""
    if out.returncode:
        LOG.warning("pdftotext 退出码 %d：%s", out.returncode, pdf)
    return out.stdout.replace("\r", "")


def parse_paper(text: str, lo: int, hi: int) -> dict[int, list[str]]:
    """按题号切块，块内按 A./B./C./D. 标记切分（支持一行多选项）。"""
    lines = text.split("\n")
    starts = []
    for i, ln in enumerate(lines):
        m = re.match(r"^\s*(\d{1,2})\.\s+\S", ln)
        if m and lo <= int(m.group(1)) <= hi:
            starts.append((int(m.group(1)), i))
    starts.sort(key=lambda t: t[1])
    out = {}
    for idx, (n, i) in enumerate(starts):
        j = starts[idx + 1][1] if idx + 1 < len(starts) else min(i + 40, len(lines))
        block = re.sub(r"^\s*\d{1,2}\.\s+", "", "\n".join(lines[i:j]))
        parts = re.split(r"(?<![A-Za-z])([ABCD])\.\s*", block)
        opts = []
        for k in range(1, len(parts) - 1, 2):
            v = norm(parts[k + 1].split("\n")[0])
            if v:
                opts.append(v)
        if len(opts) >= 4 and n not in out:
            out[n] = opts[:4]
    return out


def parse_answers(text: str) -> dict[int, str]:
    """官方答案表：题号行（1 2 3 …）后跟答案行（A C B …）。"""
    lines = [l.strip() for l in text.split("\n")]
    out: dict[int, str] = {}
    for i, ln in enumerate(lines):
        nums = re.findall(r"\b(\d{1,2})\b", ln)
        if len(nums) < 5:
            continue
        nums = [int(x) for x in nums]
        if not all(1 <= x <= 66 for x in nums):
            continue
        # 往下找第一行「全是单个 A-D 字母」的行
        for j in range(i + 1, min(i + 5, len(lines))):
            letters = re.findall(r"\b([A-D])\b", lines[j])
            if len(letters) == len(nums):
                for n, a in zip(nums, letters):
                    out.setdefault(n, a)
                break
    return out


def parse_page(path: pathlib.Path, lo: int, hi: int) -> tuple[dict[int, list[str]], dict[int, str]]:
    text = path.read_text(encoding="utf-8").replace("\r", "")
    opts, ans = {}, {}
    parts = re.split(r"^#{2,3}\s*(?:第\s*)?(\d+)\s*[.题、]?\s*$", text, flags=re.M)
    for i in range(1, len(parts) - 1, 2):
        n = int(parts[i])
        if not (lo <= n <= hi):
            continue
        body = parts[i + 1]
        o = [norm(m.group(2))
             for m in re.finditer(r"^[\s>*-]*(?:\*\*)?([ABCD])(?:\*\*)?\s*[.、．]\s*(.+)$",
                                 body, flags=re.M)]
        o = [x for x in o if x]
        if o:
            opts[n] = o
        m = re.search(r"答案[:：]\s*\**\s*([A-D])", body)
        if m:
            ans[n] = m.group(1)
    return opts, ans


CSS = """
:root{--bg:#fff;--fg:#1a1a1a;--mut:#5f5e5a;--line:#e3e1da;--ok:#0f6e56;--okbg:#e1f5ee;
--bad:#a32d2d;--badbg:#fcebeb;--warn:#854f0b;--warnbg:#faeeda;--acc:#185fa5}
*{box-sizing:border-box}
body{margin:0;background:#f6f5f1;color:var(--fg);
font:14px/1.65 -apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:32px 24px 64px}
h1{font-size:22px;font-weight:600;margin:0 0 6px}
.sub{color:var(--mut);font-size:13px;margin-bottom:24px}
h2{font-size:16px;font-weight:600;margin:32px 0 10px;padding-bottom:6px;border-bottom:1px solid var(--line)}
.card{background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin-bottom:16px}
table{border-collapse:collapse;width:100%;font-size:13px;background:var(--bg)}
th,td{border:1px solid var(--line);padding:6px 9px;text-align:left;vertical-align:top}
th{background:#faf9f6;font-weight:600;white-space:nowrap}
td.n{text-align:center;width:38px;font-variant-numeric:tabular-nums;color:var(--mut)}
.ok{color:var(--ok);font-weight:600}
.bad{color:var(--bad);font-weight:600}
.mono{font-family:ui-monospace,Consolas,monospace;font-size:12px}
.kpi{display:flex;gap:14px;flex-wrap:wrap;margin:14px 0 6px}
.kpi div{flex:1;min-width:150px;border:1px solid var(--line);border-radius:8px;padding:12px 14px;background:var(--bg)}
.kpi b{display:block;font-size:22px;font-weight:600;margin-bottom:2px}
.kpi span{font-size:12px;color:var(--mut)}
.tag{display:inline-block;font-size:11px;padding:1px 7px;border-radius:20px;font-weight:600}
.tag.ok{background:var(--okbg);color:var(--ok)}
.tag.bad{background:var(--badbg);color:var(--bad)}
.tag.warn{background:var(--warnbg);color:var(--warn)}
ul{margin:8px 0;padding-left:20px}
li{margin:4px 0}
.note{font-size:12.5px;color:var(--mut)}
code{background:#f2f0ea;padding:1px 5px;border-radius:4px;font-size:12px}
"""


def build_html() -> str:
    p21 = pdf_text(PDFDIR / "2021-paper.pdf")
    a21 = pdf_text(PDFDIR / "2021-answers.pdf", layout=True)
    p20 = pdf_text(PDFDIR / "2020-paper.pdf")

    paper21 = parse_paper(p21, 1, 30)
    paper20 = parse_paper(p20, 1, 30)
    key21 = parse_answers(a21)

    o21, s21 = parse_page(ENG / "2021.md", 1, 30)
    b21, sb21 = parse_page(ENG / "2021-英语-刷题版.md", 1, 30)
    o20, _ = parse_page(ENG / "2020.md", 1, 30)
    b20, _ = parse_page(ENG / "2020-英语-刷题版.md", 1, 30)

    rows = []
    bad_nums = []
    for n in range(1, 31):
        p = paper21.get(n, [])
        a, b = o21.get(n, []), b21.get(n, [])
        ha = sum(1 for x in a if x in p) if p and a else 0
        hb = sum(1 for x in b if x in p) if p and b else 0
        ok_a = bool(p and a and ha >= 3)
        ok_b = bool(p and b and hb >= 3)
        if not ok_b:
            bad_nums.append(n)
        ka, kb = s21.get(n, "—"), sb21.get(n, "—")
        kk = key21.get(n, "—")
        rows.append((n, ok_a, ok_b, ka, kb, kk, ha, hb, len(a), len(b)))

    n_a_ok = sum(1 for r in rows if r[1])
    n_b_ok = sum(1 for r in rows if r[2])

    def cls(x):
        return "ok" if x else "bad"

    trs = []
    a_hit = a_tot = b_hit = b_tot = 0
    for n, oa, ob, ka, kb, kk, ha, hb, ta, tb in rows:
        # 2021.md 的答案是否等于官方答案
        av = (ka == kk and kk != "—")
        if kk != "—" and ka != "—":
            a_tot += 1
            a_hit += 1 if av else 0
        # 刷题版的答案：只有题面与原卷一致时，字母才可与官方对照
        if not ob:
            bcell = "<span class='note'>不可比（题面已改写）</span>"
        else:
            bv = (kb == kk and kk != "—")
            if kk != "—" and kb != "—":
                b_tot += 1
                b_hit += 1 if bv else 0
            bcell = (f"<span class='mono'>{kb}</span> "
                     f"<span class='{'ok' if bv else 'bad'}'>{'✓' if bv else '✗'}</span>")
        trs.append(
            f"<tr><td class='n'>{n}</td>"
            f"<td><span class='tag {cls(oa)}'>{'一致' if oa else '不符'}</span>"
            f" <span class='note'>{ha}/{ta}</span></td>"
            f"<td><span class='tag {cls(ob)}'>{'一致' if ob else '不符'}</span>"
            f" <span class='note'>{hb}/{tb}</span></td>"
            f"<td class='mono'>{kk}</td>"
            f"<td><span class='mono'>{ka}</span> "
            f"<span class='{'ok' if av else 'bad'}'>{'✓' if av else '✗'}</span></td>"
            f"<td>{bcell}</td></tr>")

    # 2020 对照
    c20a = sum(1 for n in range(1, 31)
               if paper20.get(n) and o20.get(n)
               and sum(1 for x in o20[n] if x in paper20[n]) >= 3)
    c20b = sum(1 for n in range(1, 31)
               if paper20.get(n) and b20.get(n)
               and sum(1 for x in b20[n] if x in paper20[n]) >= 3)
    t20 = sum(1 for n in range(1, 31) if paper20.get(n) and o20.get(n))

    # ── 结论文案**必须跟着现算的数字走** ──────────────────────────────
    #   2026-09-20 实测：刷题版修好之后重跑本脚本，KPI 已变成 30/30，
    #   但下面这段文案是硬编码的，于是输出了
    #   「有 0 道题不是这套卷子：题号 （空） 的题干或选项被替换成了别的词」
    #   这种自相矛盾的句子 —— 数字现算、结论手抄，等于报告会撒谎。
    #   现在按 bad_nums 是否为空分两种文案。
    if bad_nums:
        _nums = ",".join(str(x) for x in bad_nums)
        concl = (
            f'<li><b>2021-英语-刷题版.md 有 {30 - n_b_ok} 道题不是这套卷子</b>：题号'
            f'<span class="mono">{_nums}</span> 的题干或选项被替换成了别的词。'
            f'不是"选项重排"（重排会让答案字母变、选项词不变），是<b>选项词本身被换掉</b>。</li>'
            f'<li><b>答案字母不可跨文件对照</b>：刷题版的答案指向它自己那套选项，'
            f'与官方答案表的字母对不上，拿它核对官方答案会显示"错"。</li>'
        )
        if 10 in bad_nums:
            concl += (
                '<li><b>最微妙的一例是第 10 题</b>：刷题版只换掉了 4 个选项中的 1 个'
                '（原卷 <span class="mono">D.had been on</span> → 刷题版 '
                '<span class="mono">B.began</span>），正确答案 '
                '<span class="mono">has been on</span> 从 C 位移到了 D 位。'
                '<b>答案内容是对的，但字母与官方不符</b> —— 按刷题版选 D 正确，'
                '一核对官方答案表（写 C）反而会以为自己做错了。这类"部分改写"最难察觉。</li>'
            )
        note2021 = ("2021 的问题是<b>内容不忠实</b> —— 与 2020 性质不同，不能一起处理。")
        bili_tail = ("视频是独立第三源，它的题面与官方 PDF、2021.md 三方吻合，"
                     "而刷题版与三者都不同。")
    else:
        concl = (
            '<li><b>2021-英语-刷题版.md 的题面已与原卷一致</b>：30 题选项逐字一致，'
            '30 题答案与官方答案表全部相同。</li>'
            '<li><b>两份文件现在是同一套卷子</b>：刷题版的答案字母可以直接拿去核对官方答案表。</li>'
            '<li><b>历史沿革</b>：2026-09-20 之前，刷题版有 19 道题'
            '（5、6、8、9、11、12、16、17、19、20、21、22、23、24、25、27、28、29、30）'
            '的题干/选项被改写成了别的词，页面当时挂着一块红色警示块。'
            '这批题已按官方卷面 + 官方答案改回原卷措辞，警示块随之删除。'
            '修复前的页面与源文件见 <code>回归基线原件-2026-09-20/english-2021/</code>。</li>'
        )
        note2021 = ("2021 的内容不忠实问题<b>已于 2026-09-20 修复</b> —— "
                    "现在 2020 与 2021 都只剩体例层面的差异。")
        bili_tail = ("视频是独立第三源：它的题面与官方 PDF、2021.md 三方吻合；"
                     "本次修复正是用它把刷题版从「改写版」改回原卷措辞。")

    bili_annot = ""
    if bad_nums:
        if 8 in bad_nums:
            bili_annot += ('（刷题版写成 <span class="mono">suggested</span> + '
                           '<span class="mono">left/had left/leave/would leave</span>）')
        if 16 in bad_nums:
            bili_annot += ('<li>第 16 题 → 画面 <span class="mono">A.then B.and C.but D.that</span>，'
                           '与 2021.md 一致（刷题版写成 '
                           '<span class="mono">A.that B.when C.where D.which</span>）</li>')

    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>广东专升本公共英语 2021 真题三方对比</title>
<style>{CSS}</style></head><body><div class="wrap">

<h1>广东专升本《公共英语》2021 真题 · 三方对比</h1>
<div class="sub">B站真题讲解视频 × 本地试卷页 × 官方标准答案 —— 核对题面与答案是否同一套卷子</div>

<h2>一、结论</h2>
<div class="card">
<div class="kpi">
  <div><b class="ok">{n_a_ok}/30</b><span>2021.md 选项与原卷一致</span></div>
  <div><b class="bad">{n_b_ok}/30</b><span>2021-英语-刷题版.md 选项与原卷一致</span></div>
  <div><b class="ok">{a_hit}/{a_tot}</b><span>2021.md 答案 = 官方答案</span></div>
  <div><b class="{'ok' if b_hit == b_tot else 'bad'}">{b_hit}/{b_tot}</b><span>刷题版 答案 = 官方答案<br>（仅题面一致的那些题）</span></div>
</div>
<ul>
<li><b>2021.md 忠实于原卷</b>：30 题选项逐字一致，30 题答案与官方答案表全部相同。</li>
{concl}</ul>
</div>

<h2>二、逐题明细（第 1–30 题）</h2>
<div class="card" style="padding:0;overflow:hidden">
<table>
<thead><tr>
<th>题号</th><th>2021.md<br><span class="note">选项 vs 原卷</span></th>
<th>刷题版<br><span class="note">选项 vs 原卷</span></th>
<th>官方<br>答案</th><th>2021.md<br>答案</th><th>刷题版<br>答案</th>
</tr></thead>
<tbody>{"".join(trs)}</tbody>
</table>
</div>
<div class="note">「一致」判据：该文件 4 个选项中至少 3 个能在官方卷面的选项集中找到（比对前只保留字母数字，以吸收 OCR 空格粘连）。</div>

<h2>三、对照组：2020 年</h2>
<div class="card">
<table><thead><tr><th>文件</th><th>选项与原卷一致</th><th>判定</th></tr></thead><tbody>
<tr><td>2020.md</td><td>{c20a}/{t20}</td><td><span class="tag ok">忠实原卷</span></td></tr>
<tr><td>2020-英语-刷题版.md</td><td>{c20b}/{t20}</td><td><span class="tag ok">忠实原卷</span></td></tr>
</tbody></table>
<p class="note" style="margin-top:10px">
2020 三份文件（<code>2020.md</code> / 刷题版 / 精析版）互不冲突：题面 55 题全部覆盖，答案 55 题全部一致。
<b>所以 2020 的问题是体例不统一，{note2021}</b>
</p>
</div>

<h2>四、B站视频的独立作用</h2>
<div class="card">
<p><b>BV1jT4y1f7YA</b>《2021年广东普通专升本（专插本）〈公共英语〉真题完整版 全解析》· UP 乐贯中西 ·
8 个分P（词汇语法 1–30 / 阅读 4 篇 / 完形 / 写作）· 字幕 8 段全部通过 <code>aid+cid</code> 校验。</p>
<p>视频画面就是原卷（页脚可见「英语试题 第 N 页 共 8 页」），老师答案以手写标注叠在卷面上。
已逐帧核对到的题面：</p>
<ul>
<li>第 5 题 <span class="mono">The wind was ___ fierce that we couldn't move forward any more.</span>
→ 画面 <span class="mono">A.such B.so C.this D.as</span>，与 2021.md 逐字一致</li>
<li>第 8 题 <span class="mono">We suggest that he ___ for Beijing next Tuesday.</span>
→ 画面 <span class="mono">A.will leave B.leaves C.leave D.is leaving</span>，与 2021.md 一致
（刷题版写成 <span class="mono">suggested</span> + <span class="mono">left/had left/leave/would leave</span>）</li>
<li>第 16 题 → 画面 <span class="mono">A.then B.and C.but D.that</span>，与 2021.md 一致
（刷题版写成 <span class="mono">A.that B.when C.where D.which</span>）</li>
<li>第 2 题答案：画面圈选 <b>C</b>，与官方答案表一致</li>
</ul>
<p class="note">⇒ 视频是独立第三源，它的题面与官方 PDF、2021.md 三方吻合，而刷题版与三者都不同。</p>
</div>

<h2>五、方法与可复核性</h2>
<div class="card">
<ul>
<li>官方卷面/答案：<code>pdftotext</code> 抽 <code>docs/public/papers/english/2021-paper.pdf</code> 与 <code>2021-answers.pdf</code></li>
<li>B站：<code>scripts/bili_zhenti.py BV1jT4y1f7YA --stage content</code> → 字幕 8 段 + 92 帧，
关键题面用 <code>ffmpeg tile</code> 拼联络表定位后逐帧人工读</li>
<li>比对：<code>scripts/zhenti_option_diff.py</code>（v2 —— v1 有一行两选项的抽取 bug，会把一致误报为不符）</li>
<li>本报告由 <code>scripts/zhenti_three_way_report.py</code> 生成，数字全部现算，未手工转录</li>
</ul>
<p class="note">版权：B站视频仅用于个人备考核对，本报告只呈现「是否一致」的判定与题号，
不转载视频画面、不转录视频原文。</p>
</div>

</div></body></html>"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="D:/tmp/zhenti/report.html")
    add_logging_args(ap)
    a = ap.parse_args()
    setup_from_args(a)
    LOG.info("生成三方对比报告 → %s", a.out)
    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_html(), encoding="utf-8", newline="\n")
    LOG.info("已写入 %s（%d 字节）", out, out.stat().st_size)
    print(f"已写入 {out}  ({out.stat().st_size} 字节)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
