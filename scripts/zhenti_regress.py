#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""真题页转换器 · 幂等性回归验证

目的
----
`zhenti_convert.py --apply` 会原地覆盖真题页。一旦转换器本身被改动
（新增折叠合并、新增答案形态……），已转换的页面可能就不再是「当前
转换器对该页面输出」了 —— 也就是说转换器变得不可重放。

这个脚本验证的正是这件事：拿页面**转换前的原件**（`.bak-*`），
用**当前**转换器重跑一遍，跟**线上文件**逐字节比对。

  ✓ = 复现一致（转换器对这份页面是幂等的、可重放的）
  ✗ = 有差异（要么转换器行为变了需要重新 --apply，要么真出了 bug）
  △ = 基线退化（.bak 全是转换产物，只证明了幂等，证明不了可重放）
  ◆ = 已声明的手工编辑（线上文件被人手改过，不是转换器行为变化）
  ! = 没跑成（文件不存在 / 找不到原件 / 转换器报错 / 没产出文件）

★ 退出码：只有 ✓ 和 ◆ 算通过。✗ △ ! 全部计入未通过，退出码 1。
  · ◆ 的判据见 `check_manual_edit()` —— 只放行「线上多出内容」这一个方向，
    而且必须能在差异里找到声明的特征串。它**永远会打印出来**，不静默。
  · 另一个例外是 `--allow-degraded` —— 它把 △ 降级为「已知并接受」。

用法
----
    python scripts/zhenti_regress.py                 # 全部
    python scripts/zhenti_regress.py math2018        # 指定配置
    python scripts/zhenti_regress.py --diff math2018 # 附差异详情
    python scripts/zhenti_regress.py --idem          # 幂等探针（见下）
    python scripts/zhenti_regress.py --allow-degraded  # 放行 △（见下）

基线从哪来（2026-09-20 起）
--------------------------
`.bak-*` / `.orig-*` 原先被 `.gitignore` 排除，只留在本机。后果：
**换机器或重新克隆之后，24 份页面全部走 NOBAK，而当时 NOBAK 被统计进
「复现一致」** —— 于是回归报「24/24 复现一致 · 退出码 0」，一次比对都没做。
现在 `.gitignore` 对 `docs/posts/**` 开了例外，这两类文件必须入库。
（`scripts/*.bak-*` 之类的脚本本地备份仍然不入库。）

两种检查的区别
--------------
`--idem` 是**另一种**检查，不是同一种的加强版：

  · 默认检查（原件重跑）：输入 `.bak`（转换前原件），期望输出 == 线上。
    这验证的是「转换器可重放」，是**交付质量的判据**。

  · `--idem`（幂等探针）：输入**线上文件本身**，期望输出 == 输入。
    这验证的是「对着已转换的页面再跑一次不会改坏它」。
    ★ 这条**不是**管线契约。2026-09-19 实测：24 份里只有 8 份成立
      （english2019、english2020jingxi、math2021–math2026）。
      另外 16 份会改动，归成三类，**都不是 bug**：
        ① 空白行累积（9 份：computer2021/2022/2025、english2020–2024、
          politics2024）—— 转换器在 `## 大题` 标题后固定补一条空行，
          却不消费源文件里原有的那条；线上文件本身带双空行，再跑一次变三条。
          ★ 试过改成「消费」，正向回归立刻从 24/24 掉到 12/24 —— 因为线上文件
            是**更早一版转换器**的产物，两边对不上。要么不改，要么把 12 份
            全部重新落盘；后者会让回归退化成「自己跟自己比」的同义反复。
            双空行在 markdown 里不可见，所以选择不改，换取回归链路的可信度。
        ② 题号偏移重复施加（3 份：computer2023/2024/2025huiyi）—— 这些页面
          配了 `section_qno_base`（源文件每节从 1 重新编号）；线上文件已经是
          **全局**编号，再跑会又加一次偏移（第 21 题 → 第 41 题）。
        ③ 裸答案被再包一层折叠块（4 份：math2018/2019/2020、politics2023）——
          这些页面里有「没有 `>` 前缀的裸文本答案」，线上文件里它们本该是
          折叠块却被留成了裸行，于是 `wrap_raw_answers` 再跑一次会包上去。
    所以 `--idem` 的用途是**诊断**，不是验收标准：改转换器之前先跑一次，
    知道哪些页面不能直接 `--apply` 重跑（得先从 `.bak` 还原）。
    判据是「24 份全 ✓」的是 `run_one()`（默认模式），不是它。

★ 比对前会把 frontmatter 里的 `date:` 值归一化掉
（`norm_dates()`）。原因：转换器每次都把 `date` 写成**当天**日期，
于是这份回归跨过午夜就必然全红 —— 2026-09-19 23:5x 跑是 24/24 ✓，
2026-09-20 00:0x 再跑就变成 0/24，而逐份看差异只有 `date:` 那一行。
这种「假红」会让验证链失去可信度，所以归一化。正文一个字节都不放过。

实现细节
--------
不直接改 `zhenti_cfg/*.json`。做法是：把配置读进来，`file` 字段改成
临时目录里的 `.bak` 副本，落成一份临时配置跑转换器，再把产物跟线上
文件 diff。这样线上配置一个字节都不会被动到。
"""
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# 本脚本依赖同级模块 zhenti_log，显式把 scripts/ 加进 sys.path（理由见 zhenti_lint.py）。
sys.path.insert(0, str(Path(__file__).resolve().parent))

# ★ E3（2026-09-20）：诊断走 logging（stderr），正式输出仍走 print（stdout）。
#   本脚本手写 sys.argv 解析（不是 argparse），所以没有 `-v` 开关 ——
#   级别用 `ZHENTI_LOG=INFO` / `ZHENTI_LOG=DEBUG` 环境变量控制。
from zhenti_log import get_logger, setup  # noqa: E402

LOG = get_logger(__name__)

ROOT = Path(__file__).resolve().parent.parent
CFG_DIR = ROOT / "scripts" / "zhenti_cfg"
PY = sys.executable

# ★ 子进程超时（2026-09-20，修 A5）。
#   三处 subprocess.run 原来都没有 timeout —— 转换器一旦卡住（主循环不前进、
#   等 stdin、网络挂起），回归就**永久阻塞**，在 CI 上表现为「一直转」，
#   比报错难查得多。用环境变量可覆盖，方便大仓库临时放宽。
SUBPROC_TIMEOUT = int(os.environ.get("ZHENTI_SUBPROC_TIMEOUT", "120"))

DATE_LINE_RE = re.compile(r"^(date:[ \t]*).*$", re.M)


def run_tool(cmd, timeout=None):
    """跑一个外部脚本，**必须带超时**。返回 `(rc, stdout, stderr)`。

    超时返回 `rc = -1` 并把原因写进 stderr，调用方按 ERROR 处理 ——
    这样「卡死」会变成一个明确的失败，而不是无限等待。
    """
    t = SUBPROC_TIMEOUT if timeout is None else timeout
    try:
        p = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=t)
        return p.returncode, p.stdout or "", p.stderr or ""
    except subprocess.TimeoutExpired:
        return -1, "", f"超时（>{t}s）：{' '.join(str(c) for c in cmd)}"


def norm_dates(text: str) -> str:
    """把 frontmatter 里的 `date:` 值抹成占位符，再拿去比对。

    ★ 为什么必须这么做：`zhenti_convert.py` 的 `DATE = date.today()`，
      每次转换都把 frontmatter 的 `date` 写成**当天**。
      于是这份回归在跨过午夜之后必然全红 —— 实测踩过：
        2026-09-19 23:5x  跑出 24 份 · 复现一致 24
        2026-09-20 00:0x  再跑  24 份 · 复现一致 0（24 份全是「9 行差异」）
      而逐份 diff 看下来，差异只有一行 `date: 2026-09-19` → `date: 2026-09-20`。
      这种「假红」最伤验证链 —— 真出 bug 时没人会再看它。

    ★ 归一化只碰最前面那段 frontmatter 里的 `date:` 行，正文一个字节不动；
      正文里任何真实差异照样会报出来。想核对日期本身，看线上文件的 frontmatter。
    """
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    return DATE_LINE_RE.sub(r"\g<1><归一化>", text[:end]) + text[end:]


def read_norm(path: Path):
    return norm_dates(path.read_text(encoding="utf-8")).splitlines(keepends=True)


def load_cfgs():
    """转换器配置 = zhenti_cfg/*.json，但排除 `promote*.json`（那是前置提升的清单）。"""
    out = {}
    for p in sorted(CFG_DIR.glob("*.json")):
        if p.name.startswith("promote"):
            continue
        out[p.stem] = p
    return out


def find_bak(doc_path: Path):
    """找 doc_path 旁边**还没被转换过**的那份 `.bak-*` 原件。

    返回 `(path, status, msg)`：找到时 status/msg 为 None；找不到时 path 为 None，
    status 是 `NOBAK`（一份都没有）或 `BAKCONV`（有的全都是转换产物）。

    ★ 两道防线，缺一不可：

    ① 只认「不含 `## 题目一览`」的那一份。
       判据与 `zhenti_convert.py --apply` 的防重复转换**完全一致**。
       以前是「取字典序第一个」—— 一旦最老那份被删掉，就会静默拿到一份
       **已经转换过**的中间产物，回归于是退化成「自己跟自己比」：永远 ✓，
       什么都没验证。2026-09-19 审计实测：`math2025` 就是这种情况（见 ②）。

    ② 一个可用原件都没有时，明确报 `BAKCONV`，**不拿中间产物顶上**。
       实测 `docs/posts/math/2025.md.bak-2026-09-19` 是一份已转换的页面
       （含 `## 题目一览`，677 行，而线上 679 行）。它过去被当成原件用，
       于是 math2025 那个 ✓ 的含义与其它 23 份不同 —— 它只证明了「幂等」，
       没有证明「可重放」。现在会被单独标出来。
    """
    cands = sorted(doc_path.parent.glob(doc_path.name + ".bak-*"))
    if not cands:
        return None, "NOBAK", f"找不到 .bak 原件：{doc_path.name}.bak-*"
    for c in cands:
        if "## 题目一览" not in c.read_text(encoding="utf-8", errors="replace"):
            return c, None, None
    return None, "BAKCONV", (
        f"{len(cands)} 份 .bak-* 全是已转换的产物（都含 `## 题目一览`），没有可用的原件。"
        f"这一份的回归只能证明幂等，证明不了可重放。"
    )


def run_one(name, cfg_path, workdir: Path, show_diff: bool):
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    doc_rel = cfg["file"]
    doc_path = ROOT / doc_rel
    LOG.debug("[%s] 开始：%s", name, doc_rel)
    if not doc_path.exists():
        LOG.error("[%s] 线上文件不存在：%s", name, doc_rel)
        return name, "MISSING", f"线上文件不存在：{doc_rel}", None

    bak, st, why = find_bak(doc_path)
    if not bak:
        LOG.error("[%s] 找不到可用基线：%s（%s）", name, st, why)
        return name, st, why, None
    # ★ 这条日志是**排查回归假绿的关键**：find_bak 是按 glob 取「第一份不含
    #   `## 题目一览` 的 .bak-*」，一旦目录里多出一份更早的备份，
    #   拿到的那份就会变。把实际选中的文件名打出来，这类问题才看得见。
    LOG.debug("[%s] 基线 → %s", name, bak.name)

    # 临时目录里放一份原件副本 + 一份改写 file 的配置
    bak_copy = workdir / (name + "_bak.md")
    shutil.copy2(bak, bak_copy)

    # ── 若有前置搬运（紧凑形态 → 模板形态），先跑它 ──
    #   2023 计算机的判断题原本是一张表、英语刷题版原本是 HTML `<details>`，
    #   都必须先 promote 再 convert。把 promote 也算进「管线」，
    #   回归验证的才是端到端可重放，而不只是转换器。
    #   ★ 清单命名优先 `promote_<配置名>.json`，回退到 `promote<年份>.json`。
    #     早期只有 `promote<年份>.json`（一年一份，够用）；英语进来之后
    #     同一个年份会有两份源文件（2020 刷题版 / 2020 精析版），
    #     按年份命名就撞车了，所以改成按配置名。
    promote_spec = CFG_DIR / f"promote_{name}.json"
    if not promote_spec.exists():
        promote_spec = CFG_DIR / f"promote{cfg.get('year')}.json"
    if promote_spec.exists():
        p2 = workdir / (name + "_promote.json")
        pspec = json.loads(promote_spec.read_text(encoding="utf-8"))
        if pspec.get("file") == doc_rel:  # 只认指向同一份页面的 spec
            pspec["file"] = str(bak_copy).replace("\\", "/")
            p2.write_text(json.dumps(pspec, ensure_ascii=False, indent=2), encoding="utf-8",
                          newline="\n")
            rc0, _o0, err0 = run_tool(
                [PY, str(ROOT / "scripts" / pspec.get("script", "zhenti_promote_compact.py")),
                 "--spec", str(p2), "--out", str(bak_copy)])
            if rc0 != 0:
                LOG.error("[%s] 前置搬运失败 rc=%d：%s", name, rc0, err0[-200:])
                return name, "ERROR", "promote 失败：" + err0[-400:], None
            LOG.debug("[%s] 前置搬运 OK：%s", name,
                      pspec.get("script", "zhenti_promote_compact.py"))
        else:
            LOG.debug("[%s] 有 promote spec 但 file 指向别的页面，跳过", name)
    else:
        LOG.debug("[%s] 无 promote spec（该页面不需要前置搬运）", name)

    cfg2 = dict(cfg)
    cfg2["file"] = str(bak_copy).replace("\\", "/")
    cfg2_path = workdir / (name + "_cfg.json")
    cfg2_path.write_text(json.dumps(cfg2, ensure_ascii=False, indent=2), encoding="utf-8",
                         newline="\n")

    # 产物落到临时目录，文件名沿用线上文件名，方便跟线上文件对齐
    want = workdir / doc_path.name
    rc, so, se = run_tool(
        [PY, str(ROOT / "scripts" / "zhenti_convert.py"),
         "--config", str(cfg2_path), "--out", str(want)])
    if rc != 0:
        return name, "ERROR", so[-800:] + se[-800:], None
    if not want.exists():
        return name, "NOPROD", "转换器没有产出文件", None
    produced = want

    a = read_norm(doc_path)
    b = read_norm(produced)
    if a == b:
        return name, "OK", "", None

    d = list(difflib.unified_diff(a, b, fromfile="线上 " + doc_rel, tofile="重跑", n=2))
    # * 先问一句「这是不是已声明的人工编辑」，再决定算不算失败。
    ok_me, why_me = check_manual_edit(name, d)
    if ok_me:
        return name, "ACK", "已声明的手工编辑：" + why_me, d
    return name, "DIFF", f"{len(d)} 行差异", d


def run_idem(name, cfg_path, workdir: Path, show_diff: bool):
    """幂等探针：把**线上文件**当输入喂给转换器，期望输出跟输入逐字节一致。

    跟 run_one() 的区别只在于输入取哪一份 —— 这里不碰 `.bak`。
    单独写一个函数而不是给 run_one 加开关，是因为两者的**结论含义不同**
    （见模块 docstring），混在一起容易把「设计使然」误读成「回归失败」。
    """
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    doc_rel = cfg["file"]
    doc_path = ROOT / doc_rel
    if not doc_path.exists():
        return name, "MISSING", f"线上文件不存在：{doc_rel}", None

    src_copy = workdir / (name + "_idem_in.md")
    shutil.copy2(doc_path, src_copy)
    cfg2 = dict(cfg)
    cfg2["file"] = str(src_copy).replace("\\", "/")
    cfg2_path = workdir / (name + "_idem_cfg.json")
    cfg2_path.write_text(json.dumps(cfg2, ensure_ascii=False, indent=2), encoding="utf-8",
                         newline="\n")

    want = workdir / ("idem_" + doc_path.name)
    rc, so, se = run_tool(
        [PY, str(ROOT / "scripts" / "zhenti_convert.py"),
         "--config", str(cfg2_path), "--out", str(want)])
    if rc != 0:
        return name, "ERROR", so[-800:] + se[-800:], None

    a = read_norm(doc_path)
    b = read_norm(want)
    if a == b:
        return name, "OK", "", None
    d = list(difflib.unified_diff(a, b, fromfile="线上 " + doc_rel, tofile="再跑一次", n=1))
    return name, "DIFF", f"{len(d)} 行差异", d


# 「没跑成 / 跑不成有效比对」的状态。这些状态**不是**「通过」，必须计入失败。
#
# ★ 为什么单列一个集合：`run_one()` 在这些情况下都返回 `d=None`，
#   而 2026-09-19 之前的 main() 是 `if d: bad.append(nm)` ——
#   于是「线上文件不存在 / 找不到 .bak / 转换器报错 / 转换器没产出文件」
#   四种「根本没比过」的情况全部被统计进「复现一致」。
#   实测（修复前）：
#       指向一个不存在的页面 → 打印「合计 1 份 · 复现一致 1 · 有差异 0」，退出码 0
#   叠加 `.gitignore` 里的 `*.bak-*`（回归基线不入库）之后更致命：
#       **在一个新克隆上跑，24 份全走 NOBAK，回归会报「24/24 复现一致」，
#         而实际上一次字节比对都没做。**
#
#   BAKCONV = 有 .bak，但全是已转换的产物 → 比对有效但含义被削弱（只证明幂等）。
#             默认也算失败：没验证到位 ≠ 验证通过。确知并接受时加 --allow-degraded。
# ======================================================================
# 已声明的手工编辑（2026-09-20 新增）
#
# 问题：回归验证的是「用当前转换器重跑 .bak 能不能复现线上文件」。
#       但线上文件**是可以被人手工编辑的** —— 加一个保真度警示块、补一句说明。
#       这类编辑转换器当然产出不来，于是报 DIFF。
#       结果是二选一：要么人习惯性忽略红色（回归失去意义），
#       要么被迫把手工内容也写进 .bak（污染基线语义，见审计 F1 就是这么来的）。
#
# 解法：允许显式声明「这一份的差异是人工加的」，但**必须绑定内容特征**，
#       而且只放行一个方向 —— 见 check_manual_edit()。
# ======================================================================
MANUAL_EDITS = {
    # ★ english2021 于 2026-09-20 退场。
    #   原先它在这里豁免一个手工加的「保真度警示块」（::: danger + 来源说明的 ⚠ 行）——
    #   因为那 19 道题（5、6、8、9、11、12、16、17、19、20、21、22、23、24、25、27、28、29、30）
    #   的题干/选项被改写成了别的词，页面必须警告读者「别当真题刷」。
    #   现在这批题已按官方卷面（`2021-paper.pdf`）+ 官方答案（`2021-answers.pdf`）改回原卷措辞，
    #   并经 B 站 `BV1jT4y1f7YA` 画面逐帧独立复核，警示块随之删除 ——
    #   页面重新等于 `convert(promote(.bak))`，不再需要豁免。
    #   ★ 注意：豁免机制只该用于「生成器表达不了的手工装饰」。
    #     拿它去盖住「内容不对」是错的 —— 红灯变绿了，雷还在。
    "math2026": {
        "why": "手工添加的「源讲解有误」纠错批注（2 行块引用）",
        "marker": "本题源讲解有误",
        # ★ 这一份曾经被「把批注也写进 .bak」的方式掩盖过（审计 F1）：
        #   .bak 从 9684 B 涨到 10090 B，不再是「B站补全前的原始页」。
        #   2026-09-20 已把 .bak 换回真原件，差异改为在这里显式声明。
        "ref": "审计 F1 · B站 BV1Y3L36bEf1（孟涛）画面与口播均给出错误解",
    },
}


def check_manual_edit(name, diff_lines):
    """这处 DIFF 能不能算「已声明的手工编辑」？

    * 只放行一个方向：**线上比重跑多出内容，而重跑没有多出任何内容**。

        手工在页面上加东西  -> 线上多出内容 -> diff 里只有 `-` 行
        转换器行为变了      -> 重跑多出内容 -> diff 里出现 `+` 行

    两者方向相反，所以「出现 `+` 内容行」一定是真回归，绝不能豁免。
    另外还要求差异里能找到声明的特征串 —— 声明过期（比如警示块被删掉）
    会立刻失效，而不是变成一张永久通行证。

    返回 (是否放行, 原因)。
    """
    spec = MANUAL_EDITS.get(name)
    if not spec:
        return False, "该配置未声明手工编辑"
    added = [l for l in diff_lines if l.startswith("+") and not l.startswith("+++")]
    if added:
        return False, ("重跑多出 %d 行内容 —— 这是转换器行为变化，"
                       "不是手工编辑，不能豁免" % len(added))
    removed = [l for l in diff_lines if l.startswith("-") and not l.startswith("---")]
    if not any(spec["marker"] in l for l in removed):
        return False, ("差异里找不到声明的特征串 %r —— "
                       "声明可能已过期，请核对 MANUAL_EDITS" % spec["marker"])
    return True, spec["why"]


HARD_FAIL = {"MISSING", "NOBAK", "ERROR", "NOPROD", "BAKCONV"}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    show_diff = "--diff" in sys.argv
    idem = "--idem" in sys.argv
    allow_degraded = "--allow-degraded" in sys.argv
    # ── 结构化输出（2026-09-20，修 E3）──────────────────────────────
    #   E3 的要害不是「没有 logging」，而是**没有任何地方能把
    #   「跑了什么、结果如何」汇总成机器可判定的东西** ——
    #   于是 A1/A2/A4 那三种「跑了、没比对、退出码 0」的假绿能长期存活。
    #   退出码修好之后只解决了「通过/不通过」这一个比特；
    #   `--json` 补上的是**逐项明细**，让上层能聚合「哪几份退化、退化成什么」。
    #
    #   ★ 实现方式：`--json` 时把**整个 stdout 重定向到 stderr**，
    #     跑完再把真 stdout 换回来、只打印一个 JSON。
    #     为什么不把每处 `print` 逐个改成 `say()`：那样以后谁新加一行
    #     print 就会污染 JSON，而且看不出错在哪。整体重定向是**结构性**的，
    #     不存在漏网。人看的文本仍然完整保留在 stderr，调试不受影响。
    as_json = "--json" in sys.argv
    real_stdout = sys.stdout
    if as_json:
        sys.stdout = sys.stderr
    cfgs = load_cfgs()
    names = args or list(cfgs)
    LOG.info("regress 启动：%d 份配置 · 模式=%s · show_diff=%s · allow_degraded=%s",
             len(names), "idem" if idem else "replay", show_diff, allow_degraded)
    results = []      # (name, status, msg, diff)
    unknown = []      # 命令行点名的配置根本不存在 —— 也是失败，不能静默跳过
    with tempfile.TemporaryDirectory(prefix="zhenti_reg_") as td:
        wd = Path(td)
        for nm in names:
            if nm not in cfgs:
                LOG.error("命令行点名的配置不存在：%s", nm)
                print(f"  {nm:18s} ?  配置不存在")
                unknown.append(nm)
                continue
            fn = run_idem if idem else run_one
            name, status, msg, d = fn(nm, cfgs[nm], wd, show_diff)
            mark = {"OK": "✓", "DIFF": "✗", "BAKCONV": "△", "ACK": "◆"}.get(status, "!")
            if status in HARD_FAIL:
                LOG.warning("[%s] %s —— %s", name, status, msg)
            elif status == "ACK":
                # msg 本身已经带「已声明的手工编辑：」前缀（run_one 拼的），别再拼一次
                LOG.info("[%s] %s", name, msg)
            else:
                LOG.debug("[%s] %s", name, status)
            print(f"  {nm:18s} {mark}  {msg}")
            if d and show_diff:
                sys.stdout.writelines(d[:400])
                print()
            results.append((nm, status, msg, d))

    if idem:
        # 幂等探针是**诊断**不是验收（见模块 docstring）：
        #   · DIFF   = 设计使然，只报告，不算失败；
        #   · 没跑成 = 仍然必须算失败，否则和修复前一样是假绿。
        failed = [r for r in results if r[1] in HARD_FAIL]
        acked = []   # 幂等探针不参与豁免（它本来就是诊断，不是验收）
        changed = [r for r in results if r[1] == "DIFF"]
        ok = len(results) - len(failed) - len(changed)
        print(f"\n幂等探针：合计 {len(results)} 份 · 幂等 {ok} · 会改动 {len(changed)} · 没跑成 {len(failed)}")
        print("  （'会改动' 不等于 bug —— 多数是设计使然，见脚本 docstring）")
    else:
        # ★ 唯一判据：status == "OK"。任何其它状态都是未通过。
        #   △ BAKCONV（基线是转换产物、只证明幂等）**默认也算未通过** ——
        #   想放行必须显式加 --allow-degraded，让这个让步留在命令行历史里，
        #   而不是又一次悄悄混进「复现一致」。
        degraded = [r for r in results if r[1] == "BAKCONV"]
        # ◆ ACK = 已声明的人工编辑。不计失败，但**必须打印出来** ——
        #   豁免机制一旦静默，就变成了新的假绿，跟 A2 的病是同一个。
        acked = [r for r in results if r[1] == "ACK"]
        if allow_degraded:
            failed = [r for r in results if r[1] not in ("OK", "BAKCONV", "ACK")]
        else:
            failed = [r for r in results if r[1] not in ("OK", "ACK")]
        ok_n = sum(1 for r in results if r[1] == "OK")
        line = f"\n合计 {len(results)} 份 · 复现一致 {ok_n} · 未通过 {len(failed)}"
        if acked:
            line += f"（另已声明手工编辑 {len(acked)} 份）"
        if allow_degraded and degraded:
            line += f"（另放行基线退化 {len(degraded)} 份）"
        print(line)
        if failed:
            print("  未通过明细：")
            for nm, st, msg, _ in failed:
                print(f"    {nm:18s} {st:8s} {msg}")
        if acked:
            print("  已声明的手工编辑（不计失败，但必须可见）：")
            for nm, st, msg, _ in acked:
                print(f"    {nm:18s} ◆  {msg}")
        if degraded and allow_degraded:
            print("  已放行的基线退化：")
            for nm, st, msg, _ in degraded:
                print(f"    {nm:18s} △  {msg}")

    if unknown:
        print(f"\n★ {len(unknown)} 个配置名不存在：{'、'.join(unknown)}")

    rc = 1 if (failed or unknown) else 0
    LOG.info("regress 汇总：合计 %d · 复现一致 %d · 未通过 %d · 已声明手工编辑 %d → rc=%d",
             len(results), sum(1 for r in results if r[1] == "OK"),
             len(failed), len(acked), rc)
    if failed:
        LOG.warning("regress 未通过的页面：%s",
                    "、".join(f"{nm}({st})" for nm, st, _m, _d in failed))
    if unknown:
        LOG.error("命令行点名的配置不存在：%s", "、".join(unknown))
    if rc:
        print("\n退出码 1 —— 有页面没通过（含「压根没跑成」）。")

    if as_json:
        sys.stdout = real_stdout
        payload = {
            "tool": "zhenti_regress",
            "mode": "idem" if idem else "replay",
            "allow_degraded": allow_degraded,
            # 判据与退出码一一对应，别让读 JSON 的人自己猜口径
            "pass_criterion": ("status == 'OK'（BAKCONV 也放行）" if allow_degraded
                               else "status == 'OK'"),
            "total": len(results),
            "ok": sum(1 for r in results if r[1] == "OK"),
            "failed": len(failed),
            "degraded": len([r for r in results if r[1] == "BAKCONV"]),
            # ◆ 已声明的人工编辑：不计入 failed，但必须让读 JSON 的人看得见
            "acknowledged": len(acked),
            "acknowledged_items": [{"name": nm, "reason": msg}
                                   for nm, st, msg, _ in acked],
            "unknown_configs": unknown,
            "exit_code": rc,
            "items": [{"name": nm, "status": st, "message": msg}
                      for nm, st, msg, _ in results],
        }
        json.dump(payload, real_stdout, ensure_ascii=False, indent=2)
        real_stdout.write("\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
