# -*- coding: utf-8 -*-
"""绘图风格依赖的统一入口（外部技能 scipilot-figure-skill 的 `setup_style`）。

★ 为什么要有这个文件（2026-09-20，修 E1）
    9 个 `gen-*-figs.py` 原来各自硬编码一行：

        sys.path.insert(0, r'C:\\Users\\Administrator\\.dsh\\skills\\scipilot-figure-skill\\scripts')
        from setup_style import setup_style
        OUT = r'C:\\Users\\Administrator\\Desktop\\deeepseek\\zhuan-sheng-ben-notes\\docs\\public\\figs'

    两个路径**都死了**：
      · 技能被搬到 `D:\\deeepseek\\dsh-agent-kit\\skills\\scipilot-figure-skill\\scripts\\`
        ⇒ 9 个脚本全部在 import 阶段 `ModuleNotFoundError: No module named 'setup_style'`。
        实测：gen-core-figs / gen-math-figs / gen-p1-figs / gen-ds-figs 退出码全为 1。
      · `C:\\Users\\...\\Desktop\\deeepseek\\...` 是仓库搬家前的旧位置 ⇒ 即使依赖找回来，
        图也会写到那个不存在的目录（savefig 直接抛 FileNotFoundError）。

    修法**不是**「把路径改成新的硬编码」—— 那样下次再搬一次，9 个脚本同时再挂一次。
    而是：候选列表 + 环境变量覆盖 + 找不到时**说清楚缺什么、怎么补**。

用法（各脚本头部）
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from _figstyle import setup_style, FIGS_DIR      # noqa: E402
    setup_style(journal='nature', lang='zh')
    OUT = FIGS_DIR
"""
import os
import pathlib
import sys

# 候选顺序：环境变量 → 技能当前位置 → 旧位置 → 仓库内 vendor（留的扩展位）
CANDIDATES = [
    os.environ.get("SCIPILOT_SCRIPTS"),
    r"D:\deeepseek\dsh-agent-kit\skills\scipilot-figure-skill\scripts",
    str(pathlib.Path.home() / ".dsh" / "skills" / "scipilot-figure-skill" / "scripts"),
    str(pathlib.Path(__file__).resolve().parent / "_vendor" / "scipilot"),
]

# 产物目录：docs/public/figs。**相对本文件定位**，不看当前工作目录 ——
# 原来用绝对路径时，从别的目录跑会把图写丢。
# ★ 可用环境变量 `FIGS_DIR` 覆盖：做「改样式前后对比」时输出到临时目录，
#   就不用动仓库里已跟踪的 53 张图（否则一次试验会污染整片 git status）。
FIGS_DIR = (os.environ.get("FIGS_DIR")
            or str(pathlib.Path(__file__).resolve().parent.parent
                   / "docs" / "public" / "figs"))


def _find_scripts_dir():
    for c in CANDIDATES:
        if not c:
            continue
        p = pathlib.Path(c)
        if (p / "setup_style.py").is_file():
            return p
    return None


_dir = _find_scripts_dir()
if _dir is None:
    sys.stderr.write(
        "\n✗ 找不到 setup_style.py —— 这 9 个绘图脚本依赖外部技能 scipilot-figure-skill。\n"
        "  已按顺序试过这些位置：\n"
        + "".join("    · %s\n" % c for c in CANDIDATES if c)
        + "\n  修法（任选其一）：\n"
        "    · 设环境变量指向该技能的 scripts 目录：\n"
        "        SCIPILOT_SCRIPTS=/path/to/scipilot-figure-skill/scripts \\\n"
        "          python scripts/gen-core-figs.py\n"
        "    · 或把 setup_style.py 放进 scripts/_vendor/scipilot/（仓库内自包含）\n"
    )
    raise SystemExit(2)

sys.path.insert(0, str(_dir))

from setup_style import setup_style  # noqa: E402,F401

# 产物目录随依赖一起建好：原来没有这一步，目录不存在时 savefig 会抛
# FileNotFoundError，报错信息里只有文件路径，看不出是「产物目录没建」。
pathlib.Path(FIGS_DIR).mkdir(parents=True, exist_ok=True)
