#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把「学科知识地图」（data/bili-analyze/_extract/_subject/*.md）落成笔记站页面。

为什么要在仓库外先合并
    语料 728 万字符 → 79 个单元卡片 → 18 份课程大纲 → 3 份学科地图。
    前三步都在 `data/bili-analyze/`（已 gitignore）里做，避免污染笔记库。

为什么拆页
    computer 13.6 万字符、math 14.6 万字符。单页塞进 VitePress 会又慢又难用，
    所以按考纲模块拆成若干页。

用法
    python scripts/bili_build_knowledge_map.py            # 写入 docs/
    python scripts/bili_build_knowledge_map.py --dry-run  # 只看拆分统计
"""
import argparse
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "bili-analyze", "_extract", "_subject")
DST = os.path.join(ROOT, "docs", "guide", "knowledge-map")

# 拆分方案：学科 -> [(输出文件, 页面标题, 区间, 一句话说明)]
#   区间可以是 (lo, hi) 元组（hi 写 None 表示「到图末」，适合尾部只增不改的图），
#   也可以是**主题名字符串**（如 "语法"）—— 由 resolve_ranges() 从章标题的
#   `## <主题> · <章名>` 自动推导。章节会增删的图**必须用主题名**。
PLAN = {
    "computer": [
        ("basics.md", "计算机基础与 Office",
         (1, 9), "计算机基础知识、数制与编码、操作系统、Word / Excel / PPT、多媒体、网络、信息安全"),
        ("c-language.md", "C 语言基础",
         (10, 20), "C 语言概述与程序开发、数据类型与常量变量、运算符与表达式、顺序/选择/循环结构、函数与递归、数组、字符与字符串、数据在内存中的存储"),
        ("c-advanced.md", "C 语言进阶与工程",
         (21, 27), "指针进阶与类型识别、结构体/位段/联合体/枚举、动态内存管理与程序内存区域、文件操作、编译链接与预处理、调试与常见错误、经典例题与项目实践"),
        ("data-structures.md", "数据结构与真题题型",
         (28, 39), "绪论与复杂度、线性表、栈与队列、串、树与二叉树、图、查找、排序、真题题型套路"),
        ("supplement.md", "补充考点（跨课补遗）",
         (40, None), "从 8 门课里补回的缺失章节：按来源课程与父章组织，含数制转换、进制、菜单与窗口约定、URL、调试与版本等"),
    ],
    "math": [
        ("limits-derivatives.md", "极限 · 导数 · 微分学应用",
         (1, 3), "函数极限连续、导数与微分、微分中值定理与导数应用"),
        ("integrals.md", "积分 · 微分方程",
         (4, 6), "不定积分、定积分及其应用、常微分方程"),
        ("advanced.md", "多元微积分 · 级数 · 线代 · 证明",
         (7, 12), "向量代数与空间解析几何、多元函数微分学、二重积分、无穷级数、线性代数、证明专项"),
        ("supplement.md", "补充考点（跨课补遗）",
         (13, None), "从 8 门课里补回的缺失章节：按来源课程与父章组织，含函数判定与复合、极限计算方法、凑微分题型、换元法、特解设法等"),
    ],
    "english": [
        ("grammar.md", "英语语法与题型",
         (1, 12), "句子主干、词法、谓语体系、时态、语态、情态、非谓语、虚拟语气、从句、特殊句式、题型专项"),
        ("supplement.md", "补充考点（跨课补遗）",
         (13, None), "从 3 门课里补回的缺失章节"),
    ],
    # 高考英语：UP主 FREE高考英语 的 16 个合集，与专升本英语不是同一份考纲，单独立图。
    "english-gaokao": [
        ("grammar.md", "语法体系",
         "语法", "词法（名/代/冠/数/形副/介/连）、英语常识与词类总览、构词法、句法基础、动词（谓语判断/时态/语态/情态与虚拟）、非谓语动词、从句（名词性/定语/状语）、特殊句式、语法填空与完形填空的语法侧考点"),
        ("reading.md", "题型与解题方法",
         "题型", "长难句拆解、篇章结构、阅读五大题型（细节/推断/主旨/词义猜测/态度）、高频词汇与难词、七选五、完形填空、语法填空、书面表达、通用应试策略"),
        ("writing.md", "应用文写作",
         "写作", "书信类（申请/建议/感谢/道歉/邀请/投诉/咨询/求助/请求）、倡议书、计划类回信、通知类、演讲稿与发言稿、祝贺类、记叙与描写、推荐与介绍类、议论与观点类、图表作文、通用结构、段落展开、高分表达、主题素材、篇幅控制、常见扣分点"),
        ("vocab-methods.md", "词汇与方法",
         "词汇方法", "词汇分级与备考定位、构词法、高频核心词分类、逻辑连词与功能结构、介词与情态动词考点、近义词与形近词辨析、熟词僻义、固定搭配、写作词汇升级、词汇记忆方法、学习方法论与学习路径规划"),
    ],
}

SUBJECT_CN = {"computer": "计算机", "math": "高数", "english": "英语",
              "english-gaokao": "英语（高考）"}

CH_RE = re.compile(r"^## ", re.M)

# ★ VitePress/Vue 构建隐患：正文里裸的 `<` 会被 Vue 当标签起始。
#   字幕提炼产物里满是数学不等式（`−R<t<R`、`0<x<1`），
#   而检查器的判据是 `/<([A-Z][A-Za-z0-9]*)[\s/>]/` —— 连 `<R ` 这种（大写字母后跟空格）
#   都会被判成未注册组件，构建会挂。
#   所以策略是**代码外所有裸 `<` 一律转义成 `&lt;`**（渲染出来仍是 `<`，视觉无差）。
#   行内代码里不动 —— markdown-it 本来就转义行内代码里的尖括号。
def escape_angle(text):
    """把代码外的裸 `<` 转成 `&lt;`。返回 (新文本, 修了几处)。"""
    n = text.count("<")
    return text.replace("<", "&lt;"), n


# ★ 第二个隐患：LaTeX 下标记法 `_{...}` / `^{...}`。
#   提炼产物里到处是 `lim_{x→0}`、`f_{x}`、`x^{n}`。markdown-it 会把里面的 `_` 当强调定界符，
#   生成的 `<em>` 又带着 `{x→0}` 被 Vue 当**属性绑定**解析 → 生成的 JS 里出现 `{ x→0: "" }`
#   → rollup 报 `Unexpected character '→'`，**构建直接失败**（实测 339 处）。
#   修法：把 `_{...}` / `^{...}` 整段里的 `_ ^ { }` 全部反斜杠转义。
#   markdown-it 会把 `\_` 渲染成 `_`、`\{` 渲染成 `{`，**视觉完全不变**。
def escape_math(text):
    """转义 `_{...}` / `^{...}` 里的 `_ ^ { }`。返回 (新文本, 修了几处)。"""
    out = []
    i = 0
    fixed = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c in "_^" and i + 1 < n and text[i + 1] == "{":
            depth = 0
            j = i + 1
            while j < n:
                if text[j] == "{":
                    depth += 1
                elif text[j] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            if j < n:                          # 找到配对的 }
                seg = text[i:j + 1]
                out.append(seg.replace("_", "\\_").replace("^", "\\^")
                              .replace("{", "\\{").replace("}", "\\}"))
                fixed += 1
                i = j + 1
                continue
        out.append(c)
        i += 1
    return "".join(out), fixed


def sanitize(text):
    """对**行内代码之外**的文本做两项转义（先 LaTeX 后尖括号）。返回 (新文本, 总修改数)。"""
    parts = text.split("`")
    fixed = 0
    for i in range(0, len(parts), 2):          # 偶数下标 = 代码之外
        parts[i], n1 = escape_math(parts[i])
        parts[i], n2 = escape_angle(parts[i])
        fixed += n1 + n2
    return "`".join(parts), fixed


def split_chapters(text):
    """把学科地图按 `## ` 切成 [(标题, 正文)]。"""
    idx = [m.start() for m in CH_RE.finditer(text)]
    if not idx:
        return []
    head = text[:idx[0]]
    out = []
    for i, s in enumerate(idx):
        e = idx[i + 1] if i + 1 < len(idx) else len(text)
        block = text[s:e]
        title = block.split("\n", 1)[0][3:].strip()
        out.append((title, block))
    return head, out


def resolve_ranges(chapters):
    """把 PLAN 里的区间说明解析成真正的 `(lo, hi)`（1-based 闭区间）。

    ★ 为什么不再硬编码序号：高考英语那张图的章节数是会变的
      （补内容 / 删空章都会动），而 `(1, 33)` 这种硬编码序号**一加章就错位**，
      表现为「某个主题页里混进了别的主题的章节」，而且**不会报错**。
      实测 2026-09-25 一天之内手改了三次区间。

    ⇒ 改用**主题名**（章标题 `## <主题> · <章名>` 里 `·` 前面那截）自动推导：
      该主题的所有章连续出现时，区间就是 `[首章序号, 末章序号]`。
      这样加减章只要主题没变，区间自动跟着走。

    返回 {(主题名): (lo, hi)}；主题名不存在时返回 None 由调用方报错。
    """
    rng, multi = {}, set()
    cur, start = None, None
    for i, (title, _) in enumerate(chapters, 1):
        th = title.split("·", 1)[0].strip() if "·" in title else title
        if th != cur:
            if cur is not None:
                if cur in rng:                 # 该主题出现第二段 —— 记下来，别静默吞掉
                    multi.add(cur)
                else:
                    rng[cur] = (start, i - 1)
            cur, start = th, i
    if cur is not None:
        if cur in rng:
            multi.add(cur)
        else:
            rng[cur] = (start, len(chapters))
    return rng, multi


def count_points(block):
    return len(re.findall(r"^### ", block, re.M))


# ── 出处链接化 ────────────────────────────────────────────────────────────────
# 专升本 19 个 BV 与成品里的「课程简称」是**一一对应**的（不像高考英语那样
# 一个简称聚合 8 个 BV），所以可以精确到分P 拼直达链接。
# ★ 只在**生成的页面**上做，不改 `_subject/*.md` 源数据 —— 源里保留纯文本，
#   这样换 UP主、换 BV 只要改这张表，不用重跑整条提炼链路。
BV_OF = {
    # 计算机
    "鹏哥": "BV17a7K64ELH", "逊哥": "BV1tNpbekEht", "H学长": "BV1Ay4y137RA",
    "升本啦": "BV1KU4y167ds", "强哥": "BV1Ye411Y7Ue", "张无忌": "BV1z84y1z7Vp",
    "一灯": "BV1Z4w3znE6h", "强哥·数据结构": "BV1ajMo6TEBm",
    # 高数
    "陈哥": "BV1husGzwEtZ", "石头": "BV18CL26WEJ3", "杰哥": "BV1Up4y1Y76a",
    "ok姐": "BV1vm421s7mv", "米哥": "BV1swAWerEzS", "学士帽": "BV1X4411J792",
    "斌哥": "BV12DdNYzEvy", "帆哥": "BV1xxXZBKENv",
    # 英语
    "阿珂": "BV1brgBzNEbW", "乐贯中西": "BV1jT4y1f7YA", "易易": "BV1Do4y1h7om",
}


def _bv_url(bv, p):
    return "https://www.bilibili.com/video/%s?p=%d" % (bv, p)


def linkify_sources(text):
    """把 `- **出处**：陈哥 P50, P51；杰哥 P28` 里的每个分P 变成直达链接。

    支持的写法（实测这三种覆盖了 100% 的 1590 条）：
        `H学长 P2`                  单课程
        `H学长 P13–P16`             带区间（链到区间起点）
        `H学长 P14；升本啦 P2`        多课程

    ★ 认不出的简称**原样保留**，不猜、不报错 —— 宁可少链，不要链错。
    """
    def one(seg):
        m = re.match(r"^([^\sP][^\s]*)\s+(.+)$", seg.strip())
        if not m:
            return seg
        name, rest = m.group(1), m.group(2)
        bv = BV_OF.get(name)
        if not bv:
            return seg
        out = []
        for i, part in enumerate(re.split(r",\s*", rest)):
            # ★★ 分P 后面**可能带后缀**（画面来源的出处是 `一灯 P1（画面）`）。
            #    第一版正则写死 `$` 结尾 ⇒ 带 `（画面）` 就匹配失败 ⇒ 走兜底
            #    只 append 了 `part`（= `P1（画面）`），**把「一灯」丢了**，
            #    页面上变成光秃秃的 `P1（画面）`。实测漏了 17 条。
            #    ⇒ 正则容忍尾部内容，并把它原样接回去。
            pm = re.match(r"^P(\d+)(?:\s*[–\-]\s*P?(\d+))?\s*(.*)$", part.strip())
            if not pm:
                # 认不出也要**保留简称**（宁可少链，不要丢信息）
                out.append(part if i else ("%s %s" % (name, part)))
                continue
            tail = pm.group(3) or ""
            p0 = int(pm.group(1))
            label = ("%s P%s" % (name, pm.group(1))) if i == 0 else ("P%s" % pm.group(1))
            if pm.group(2):
                label += "–P%s" % pm.group(2)
            out.append("[%s](%s)%s" % (label, _bv_url(bv, p0), tail))
        return "、".join(out)

    def rep(m):
        segs = re.split(r"[；;]", m.group(1))
        return "- **出处**：" + "；".join(one(s) for s in segs)

    out, n = re.subn(r"^- \*\*出处\*\*：(.+)$", rep, text, flags=re.M)
    n_linked = len(re.findall(r"https://www\.bilibili\.com/video/", out))
    return out, n_linked


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    manifest = {}
    for subj, pages in PLAN.items():
        src = os.path.join(SRC, "%s.md" % subj)
        if not os.path.exists(src):
            print("!! 缺源文件 %s" % src)
            return 1
        with io.open(src, encoding="utf-8") as fh:
            text = fh.read()
        head, chapters = split_chapters(text)
        rng, multi = resolve_ranges(chapters)
        if multi:
            print("  ⚠️ 这些主题被拆成多段，只用第一段：%s" % sorted(multi))
        total_pts = sum(count_points(b) for _, b in chapters)
        print("=" * 74)
        print("%s（%s）：%d 章 / %d 知识点 / %d 字符"
              % (SUBJECT_CN[subj], subj, len(chapters), total_pts, len(text)))
        used = 0
        _prev_hi = 0        # ★ 数字区间的连续性游标（见下方边界断言）
        for fname, title, span, desc in pages:
            if isinstance(span, str):              # 主题名 → 自动推导区间
                if span not in rng:
                    print("  ❌ 主题「%s」在图里找不到，跳过 %s" % (span, fname))
                    continue
                lo, hi = rng[span]
            else:
                lo, hi = span
                # ★★ `(lo, None)` = 到图末。专升本那几张图的「补充」页天生
                #    是「主线章节之后的全部」，写死 hi 一加章就漏（实测：
                #    加了 4 章后 supplement 只覆盖到 69/73，页面少 4 章）。
                if hi is None:
                    hi = len(chapters)
            # ★★★ 数字区间的边界断言 —— 2026-10-03 加。
            #    `computer` 那 4 段的标题是 `一、计算机基础知识` 这种中文序号，
            #    **不含 `·`**，所以 resolve_ranges 的主题名机制对它完全无效
            #    （整条标题都会被当成主题名，切成 73 个碎片），
            #    ⇒ 只能用数字区间，这不是偷懒，是唯一可行方式。
            #    但数字区间的**真实风险**是「中段插章导致整体错位」：
            #    在 computer.md 主线段中间插入一章，`(10,20)` 就会把原本的
            #    第 9 章挤到 c-language 页、第 20 章被挤到 c-advanced 页，
            #    而且**不报错**（页面照生成，只是内容串了）。
            #    ⇒ 判据：区间的首章必须接上一段的末章 +1（连续无缝、不重不漏），
            #      且**最后一段必须覆盖到图末**。任何错位都当场硬失败。
            if not isinstance(span, str):
                _exp_lo = _prev_hi + 1 if _prev_hi else 1
                if lo != _exp_lo:
                    raise SystemExit(
                        "❌ %s 的数字区间与上一段不连续：本段 lo=%d，应为 %d。\n"
                        "   通常是**在计算机/高数主线段中间插入了新章**，导致后续区间整体错位。\n"
                        "   改法：重排 PLAN['%s'] 的全部数字区间（或把段落改成主题名，"
                        "若该图章标题含 `·`）。\n"
                        "   历史教训：漏改会让相邻页混进别的章节，且**不会报错**。"
                        % (fname, lo, _exp_lo, subj))
                _prev_hi = hi
            picked = chapters[lo - 1:hi]
            used += len(picked)
            body = "\n".join(b for _, b in picked)
            pts = sum(count_points(b) for _, b in picked)
            chars = len(body)
            print("  → %-22s 章 %2d–%2d（%2d 章）%4d 知识点 %7d 字符  %s"
                  % (fname, lo, hi, len(picked), pts, chars, title))
            manifest.setdefault(subj, []).append(
                (fname, title, desc, len(picked), pts, chars))
            if args.dry_run:
                continue
            outdir = os.path.join(DST, subj) if len(pages) > 1 else DST
            if len(pages) == 1:
                outdir = DST
            if not os.path.isdir(outdir):
                os.makedirs(outdir)
            header = (
                "# %s · %s\n\n"
                "> %s\n\n"
                "> 本页 %d 章 / %d 条知识点。来源与可信度说明见"
                "[知识地图总览](/guide/knowledge-map/)。\n\n"
                % (SUBJECT_CN[subj], title, desc, len(picked), pts)
            )
            out = os.path.join(outdir, fname)
            body, nfix = sanitize(body)
            if nfix:
                print("     ⚠️ 转义 %d 处（裸 `<` + LaTeX 下标）" % nfix)
            body, nlink = linkify_sources(body)
            if nlink:
                print("     🔗 出处链接化 %d 处" % nlink)
            with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(header + body.lstrip("\n") + "\n")
        if used != len(chapters):
            # ★★ 这个警告必须**硬失败**，不能只 print 一句就过。
            #    实测踩过：合并进来的章用了**新主题名**（`应用文写作`，而地图里既有的
            #    写作章主题是 `写作`）⇒ 地图里出现第 5 个主题连续段 ⇒ 生成器的
            #    4 板块切分覆盖不到它 ⇒ **7 章 / 22 条静默地从页面上消失**。
            #    当时只打了 ⚠️ 就继续写文件，页面数字对不上才发现。
            #    ⇒ 章节没被完整消费 = 数据要丢，必须拦住。
            raise SystemExit(
                "❌ 章节覆盖不全：只用了 %d / 共 %d 章。\n"
                "   通常是「新增章用了地图里没有的主题名」，导致主题连续段多出一段。\n"
                "   检查 `_add-*.md` 里的 `## <主题> · ...`，主题名要与地图既有的对齐。"
                % (used, len(chapters)))
    print("=" * 74)
    if args.dry_run:
        print("[dry-run] 未写文件。")
    else:
        print("已写入 %s" % DST)
    return 0


if __name__ == "__main__":
    sys.exit(main())
