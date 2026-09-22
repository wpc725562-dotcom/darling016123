#!/usr/bin/env python3
"""把人工读帧得到的真题卡写成 zhenti.jsonl。

★ 为什么单独放一个 .py 而不是在 shell 里 heredoc：
  LaTeX 里全是反斜杠（\\lim \\to \\right），heredoc 会把 `\\\\` 折叠成 `\\`，
  于是 Python 再把 `\\t` / `\\r` / `\\b` 当成转义符 —— 实测 `\\to` 变成了制表符、
  `\\right` 变成了回车、`\\begin` 变成了退格。
  写成文件 + 全用 raw string 才能保证题面一字不差。

★ 卡片字段：
  q_no / q_type / q_text / options / answer / steps / pitfalls /
  t_start / t_end / evidence（硬字段：每项都要能指回哪一帧或哪一秒）
"""
from __future__ import annotations

import json
import pathlib
import sys

# 本脚本依赖同级模块 zhenti_log，显式把 scripts/ 加进 sys.path（理由见 zhenti_lint.py）。
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

# ★ E3（2026-09-20）：诊断走 logging（stderr），print 的题面/答案清单不受影响。
from zhenti_log import get_logger  # noqa: E402

LOG = get_logger(__name__)

ROOT = pathlib.Path(__file__).resolve().parent.parent / "data" / "bili-zhenti"


def write(bvid: str, cards: list[dict]) -> pathlib.Path:
    out = ROOT / bvid / "extract" / "zhenti.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for c in cards:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    return out


# ══════════════════════════════════════════════════════════════════
# BV1Y3L36bEf1 · 孟涛老师 · 2026 广东专升本高数 · P1 单选题
#   画面是**官方真题卷扫描件**（标注「2026年3月4日 16:06」），非回忆版。
# ══════════════════════════════════════════════════════════════════

P1 = dict(
    bvid="BV1Y3L36bEf1", page=1, subject="高数", year=2026,
    paper="广东省专升本 高等数学", up="孟涛老师",
    section="一、单项选择题（本大题共 5 小题，每小题 3 分，共 15 分）",
    source_kind="官方真题卷扫描件",
)

P1_CARDS = [
    dict(P1, q_no=1, q_type="单选", t_start=9, t_end=57,
         q_text=r"$\lim\limits_{n\to\infty}\left(2+\dfrac{1}{n}\right)=$ ______",
         options=["A. 3", "B. 2", "C. 1", "D. 0"], answer="B",
         steps=["极限的四则运算可拆项：$\\lim(a+b)=\\lim a+\\lim b$",
                "常数项 2 直接抄下来",
                r"$\dfrac{1}{n}$ 当 $n\to\infty$ 时是无穷小 $\to 0$",
                "2 + 0 = 2，选 B"],
         pitfalls=[r"把 $\dfrac{1}{\infty}$ 当成「无意义」而不是 0",
                   "不拆项、整体硬代入导致卡住"],
         evidence={"q_text": "frames/p01_0001.jpg",
                   "options": "frames/p01_0001.jpg",
                   "answer": "frames/p01_0001.jpg（红笔标 B）",
                   "steps": "transcript_p01.md 00:00:09~00:00:57"}),

    dict(P1, q_no=2, q_type="单选", t_start=57, t_end=144,
         q_text=r"已知函数 $y=x^3+1$，则 $\left.dy\right|_{x=1}=$ ______",
         options=["A. 5dx", "B. 4dx", "C. 3dx", "D. 2dx"], answer="C",
         steps=[r"由 $y'=\dfrac{dy}{dx}$ 推出 $dy=y'\,dx$",
                r"对 $y$ 求导：$y'=3x^2$（常数 1 的导数为 0）",
                r"★ 先求导再代入：$\left.dy\right|_{x=1}=3\times 1^2\,dx=3dx$"],
         pitfalls=["★ 先代入再求导 —— 对常数求导恒为 0，答案永远是 0",
                   "漏掉 $dx$，只写 3"],
         evidence={"q_text": "frames/p01_0002.jpg",
                   "options": "frames/p01_0002.jpg",
                   "answer": "frames/p01_0002.jpg（红笔 3dx）",
                   "steps": "transcript_p01.md 00:00:57~00:02:24"}),

    dict(P1, q_no=3, q_type="单选", t_start=144, t_end=225,
         q_text=r"定积分 $\displaystyle\int_0^1 (3x^2+2x)\,dx=$ ______",
         options=["A. 5", "B. 4", "C. 3", "D. 2"], answer="D",
         steps=[r"先求原函数：$3x^2\to x^3$，$2x\to x^2$",
                "用牛顿-莱布尼茨公式代入上下限作差",
                r"$(1^3-0^3)+(1^2-0^2)=1+1=2$，选 D"],
         pitfalls=["定积分结果后面加 $+C$ —— 定积分是确定的数，不带常数 C",
                   "上下限代入顺序写反（写成 0-1）"],
         evidence={"q_text": "frames/p01_0003.jpg",
                   "options": "frames/p01_0003.jpg",
                   "answer": "frames/p01_0003.jpg（红笔 =2）",
                   "steps": "transcript_p01.md 00:02:24~00:03:45"}),

    dict(P1, q_no=4, q_type="单选", t_start=225, t_end=458,
         q_text=r"函数 $f(x)=|5x|$ 在 $x=0$ 处 ______",
         options=["A. 左右导数都存在",
                  "B. 左导数存在，右导数不存在",
                  "C. 左导数不存在，右导数存在",
                  "D. 左右导数都不存在"],
         answer="A",
         steps=[r"先把绝对值化为分段函数：$f(x)=\begin{cases}5x,&x\ge 0\\-5x,&x<0\end{cases}$",
                r"按定义求左导数：$f'_-(0)=\lim\limits_{x\to 0^-}\dfrac{-5x-0}{x-0}=-5$",
                r"按定义求右导数：$f'_+(0)=\lim\limits_{x\to 0^+}\dfrac{5x-0}{x-0}=5$",
                "两者都存在 → 选 A"],
         pitfalls=["★ 看到「左右导数不相等」就选 D —— 本题只问是否**存在**，没问是否可导",
                   "把「可导 ⟺ 左右导数存在且相等」套到本题（那是判可导，不是判存在）",
                   "不画图、不化分段，直接对 $|5x|$ 求导"],
         evidence={"q_text": "frames/p01_0005.jpg",
                   "options": "frames/p01_0005.jpg",
                   "answer": "frames/p01_0008.jpg（红笔 ✓ 标在 A）",
                   "steps": "transcript_p01.md 00:03:45~00:07:38",
                   "cross_check": "另一源 BV1xxXZBKENv 也讲同一份卷的第 1、2 题，数值一致"}),

    dict(P1, q_no=5, q_type="单选", t_start=458, t_end=882,
         q_text=r"已知 $D$ 为圆心在原点、$r=2$ 所围成的区域，则 $\displaystyle\iint_D e^{x^2+y^2}\,dxdy=$ ______",
         options=[r"A. $\pi(e^4-1)$", r"B. $\pi(1-e^4)$",
                  r"C. $\pi(e^{-4}-1)$", r"D. $\pi(1-e^{-4})$"],
         answer="A",
         steps=["★ 先画图：区域是半径 2 的圆盘",
                r"化极坐标：$x=r\cos\theta,\;y=r\sin\theta$，面积元 $dxdy=r\,dr\,d\theta$",
                r"定限：$0\le\theta\le 2\pi,\;0\le r\le 2$",
                r"被积函数化为 $e^{r^2}$，原式 $=\displaystyle\int_0^{2\pi}\!d\theta\int_0^2 e^{r^2}r\,dr$",
                r"$=2\pi\cdot\dfrac{1}{2}\displaystyle\int_0^2 e^{r^2}d(r^2)=\pi(e^4-1)$，选 A"],
         pitfalls=["★ 忘乘雅可比因子 $r$",
                   r"被积函数写成 $e^r$ 而不是 $e^{r^2}$",
                   r"换元后误把 $r^2$ 的上限当 2（应为 4）"],
         evidence={"q_text": "frames/p01_0009.jpg",
                   "options": "frames/p01_0009.jpg",
                   "answer": "frames/p01_0009.jpg（红笔 π(e⁴-1)）",
                   "steps": "transcript_p01.md 00:07:38~00:14:42"}),
]


# ══════════════════════════════════════════════════════════════════
# BV1Y3L36bEf1 · P2 填空题
# ══════════════════════════════════════════════════════════════════

P2 = dict(
    bvid="BV1Y3L36bEf1", page=2, subject="高数", year=2026,
    paper="广东省专升本 高等数学", up="孟涛老师",
    section="二、填空题（本大题共 5 小题，每小题 3 分，共 15 分）",
    source_kind="官方真题卷扫描件",
)

P2_CARDS = [
    dict(P2, q_no=6, q_type="填空", t_start=16, t_end=98,
         q_text=r"极限 $\lim\limits_{x\to 0}\dfrac{\sin(4x)}{x}=$ ______",
         options=[], answer="4",
         steps=[r"看到 $\lim$ 趋向 0 且含 $\sin$ → 优先用等价无穷小",
                r"当 $x\to 0$ 时 $\sin(4x)\sim 4x$",
                r"原式 $=\lim\limits_{x\to 0}\dfrac{4x}{x}=4$"],
         pitfalls=[r"等价无穷小只在**乘积/商**里可直接替换，加减里乱换会错",
                   "用洛必达也能做，但比等价无穷小慢，且容易在求导时出错"],
         evidence={"q_text": "frames/p02_0001.jpg",
                   "answer": "frames/p02_0001.jpg（红笔 =4）",
                   "steps": "transcript_p02.md 00:00:16~00:01:38"}),

    dict(P2, q_no=7, q_type="填空", t_start=98, t_end=238,
         q_text=r"已知函数 $f(x)=\sqrt{1+2x}$，则 $f'(0)=$ ______",
         options=[], answer="1",
         steps=[r"改写成幂形式更清楚：$f(x)=(1+2x)^{\frac{1}{2}}$",
                r"复合函数求导 —— **由外向内逐层求导，再连乘**",
                r"外层：$\dfrac{1}{2}(1+2x)^{-\frac{1}{2}}$",
                r"内层：$(1+2x)'=2$",
                r"相乘：$\dfrac{1}{2}(1+2x)^{-\frac{1}{2}}\times 2=\dfrac{1}{\sqrt{1+2x}}$",
                r"★ 先求导再代入：$f'(0)=\dfrac{1}{\sqrt{1}}=1$"],
         pitfalls=["★ 先代入再求导 —— 对常数求导恒为 0",
                   "复合函数只对外层求导，忘了乘内层导数",
                   "把 √(1+2x) 当成 (1+2x)^2 或漏掉根号"],
         evidence={"q_text": "frames/p02_0001.jpg（第 7 题题干）",
                   "steps": "transcript_p02.md 00:01:38~00:03:58",
                   "answer": "transcript_p02.md「最后一步…把它代入进去，结果一看就能看出来是一」"}),

    dict(P2, q_no=8, q_type="填空", t_start=238, t_end=422,
         q_text=r"级数 $\sum\limits_{n=1}^{\infty}\left(\dfrac{2}{3}\right)^{n}$ 的和 $S=$ ______",
         options=[], answer="2",
         steps=["识别出这是**等比级数**（几何级数）",
                r"首项 $a_1=\dfrac{2}{3}$（$n=1$ 代入），公比 $q=\dfrac{2}{3}$",
                r"收敛条件 $|q|<1$ 满足 → 可求和",
                r"用公式 $S=\dfrac{a_1}{1-q}$",
                r"$S=\dfrac{2/3}{1-2/3}=\dfrac{2/3}{1/3}=2$"],
         pitfalls=["真题里级数通常只考**敛散性**，考「求和」很罕见 —— 别看到级数就条件反射判敛散",
                   r"公式记成 $\dfrac{a_1}{1+q}$ 或把 $a_1$ 当成 $n=0$ 时的值",
                   "忘记先确认 $|q|<1$（发散级数不能求和）"],
         evidence={"q_text": "frames/p02_0005.jpg",
                   "answer": "frames/p02_0005.jpg（红笔 S=2）",
                   "steps": "transcript_p02.md 00:03:58~00:07:02"}),

    dict(P2, q_no=9, q_type="填空", t_start=422, t_end=596,
         q_text=r"已知 $L$ 是从 $x$ 轴 $(a,\,0)$ 到 $(-a,\,0)$ 之间的一条直线段，"
                r"求 $\displaystyle\int_L y^2\,dx=$ ______",
         options=[], answer="0",
         steps=[r"★ 先判断类型：被积表达式带 $dx$ → **对坐标的曲线积分**（不是对弧长）",
                r"用第一类公式：$\displaystyle\int_L f(x,y)\,dx=\int_a^b f(x,y(x))\,dx$",
                r"L 是 $x$ 轴上的线段 → 其上 $y\equiv 0$",
                r"被积函数 $y^2=0$ → 原式 $=\displaystyle\int_a^{-a}0\,dx=0$",
                r"★ 定限：下限是起点 $a$，上限是终点 $-a$，**不能写反**"],
         pitfalls=["★ 把上下限写反（写成 $-a$ 到 $a$）",
                   "误判成对弧长的曲线积分，多乘一个 $\\sqrt{1+(y')^2}$（本题 $y'=0$ 结果仍是 0，但思路错）",
                   r"没注意 $L$ 在 $x$ 轴上、$y\equiv 0$，白算一通"],
         evidence={"q_text": "frames/p02_0009.jpg",
                   "answer": "frames/p02_0009.jpg（红笔 ∫_a^{-a} 0dx = 0）",
                   "steps": "transcript_p02.md 00:07:02~00:09:56"}),

    dict(P2, q_no=10, q_type="填空", t_start=596, t_end=949,
         q_text=r"已知积分 $\displaystyle\int_a^{+\infty} xe^{-x}\,dx=0$，求 $a=$ ______",
         options=[], answer="-1",
         steps=[r"看到 $e^{-x}$ 和 $dx$ → 凑微分，把 $dx$ 变 $d(-x)$ 并补一个负号",
                r"原式 $=-\displaystyle\int_a^{+\infty}x\,d(e^{-x})$",
                r"分部积分：$=-\left[x e^{-x}\Big|_a^{+\infty}-\displaystyle\int_a^{+\infty}e^{-x}dx\right]$",
                r"$x e^{-x}\to 0$（$x\to+\infty$ 时），边界项只剩 $a e^{-a}$",
                r"$=a e^{-a}-\left[e^{-x}\right]_a^{+\infty}=a e^{-a}+e^{-a}=0$",
                r"$(a+1)e^{-a}=0$，而 $e^{-a}\neq 0$ → $a=-1$"],
         pitfalls=[r"★ 误以为 $e^{-a}=0$ 而直接得 $a$ 任意 —— $e^{-a}$ 恒不为 0",
                   r"漏掉边界项 $x e^{-x}\big|_a^{+\infty}$ 中 $x\to+\infty$ 的极限（要说明它趋于 0）",
                   "凑微分时忘记补负号"],
         evidence={"q_text": "frames/p02_0011.jpg",
                   "answer": "frames/p02_0011.jpg（红笔 a = -1）",
                   "steps": "transcript_p02.md 00:09:56~00:15:49"}),
]


# ══════════════════════════════════════════════════════════════════
# BV1Y3L36bEf1 · P3 计算题
# ══════════════════════════════════════════════════════════════════

P3 = dict(
    bvid="BV1Y3L36bEf1", page=3, subject="高数", year=2026,
    paper="广东省专升本 高等数学", up="孟涛老师",
    section="三、计算题（本大题共 8 小题，每小题 6 分，共 48 分）",
    source_kind="官方真题卷扫描件",
)

P3_CARDS = [
    dict(P3, q_no=11, q_type="计算", t_start=17, t_end=106,
         q_text=r"求极限 $\lim\limits_{x\to 1}\dfrac{\ln x}{x^{2}-x}$",
         options=[], answer=r"$1$",
         steps=[r"$x\to 1$ 时分子分母都趋于 0 → $\dfrac{0}{0}$ 型",
                "用洛必达法则，分子分母分别求导",
                r"$=\lim\limits_{x\to 1}\dfrac{1/x}{2x-1}$",
                r"$=\dfrac{1}{2\times 1-1}=1$"],
         pitfalls=["直接代入得 0/0 就以为无解，没想到洛必达",
                   r"分母求导写成 $2x$ 而不是 $2x-1$（漏掉 $-x$ 项）"],
         evidence={"q_text": "frames/p03_0001.jpg",
                   "answer": "frames/p03_0001.jpg（红笔 =1）",
                   "steps": "transcript_p03.md 第 11 题段"}),

    dict(P3, q_no=12, q_type="计算", t_start=106, t_end=198,
         q_text=r"设 $f(x)=(x-3)^{5}$，求 $f'''(4)$",
         options=[], answer=r"$60$",
         steps=[r"高阶导数 —— **逐阶求导**",
                r"$f'(x)=5(x-3)^{4}$",
                r"$f''(x)=20(x-3)^{3}$",
                r"$f'''(x)=60(x-3)^{2}$",
                r"$f'''(4)=60(4-3)^{2}=60$"],
         pitfalls=["把 $f'''(4)$ 理解成「先代入 4 再求三阶导」—— 必须先求导后代入",
                   r"逐阶求导时忘记每次乘以上一次的系数（$5\to 20\to 60$）"],
         evidence={"q_text": "frames/p03_0001.jpg（题干）",
                   "answer": "frames/p03_0003.jpg（红笔 f'''(4)=60）",
                   "steps": "transcript_p03.md 第 12 题段"}),

    dict(P3, q_no=13, q_type="计算", t_start=198, t_end=299,
         q_text=r"已知函数 $y=y(x)$ 由参数方程 $\begin{cases}x=e^{t}+t\\ y=t\cos t\end{cases}$ 确定，"
                r"求 $\dfrac{dy}{dx}$",
         options=[], answer=r"$\dfrac{\cos t-t\sin t}{e^{t}+1}$",
         steps=[r"参数方程求导公式：$\dfrac{dy}{dx}=\dfrac{dy/dt}{dx/dt}$",
                r"$\dfrac{dx}{dt}=e^{t}+1$",
                r"$\dfrac{dy}{dt}=\cos t-t\sin t$（乘积求导：$(uv)'=u'v+uv'$）",
                r"相除即得结果"],
         pitfalls=[r"$\dfrac{dy}{dt}$ 求成 $-\sin t$ —— 忘了 $t\cos t$ 是乘积，要两项",
                   r"把结果写成 $\dfrac{dy/dt}{dx/dt}$ 的倒数（分子分母写反）",
                   r"结果里残留 $t$ 是对的，不要去「消掉」它"],
         evidence={"q_text": "frames/p03_0005.jpg",
                   "answer": "frames/p03_0005.jpg（红笔写出最终式）",
                   "steps": "transcript_p03.md 第 13 题段"}),

    dict(P3, q_no=14, q_type="计算", t_start=299, t_end=538,
         q_text=r"求二重积分 $\displaystyle\iint_D (x+y)\,dxdy$，"
                r"其中区域 $D$ 是由直线 $y=x$，$y=2$ 以及 $y$ 轴围成的区域",
         options=[], answer=r"$4$",
         steps=[r"先画图：$D$ 是以 $(0,0),(2,2),(0,2)$ 为顶点的三角形",
                r"选 $X$ 型区域：$0\le x\le 2$，$x\le y\le 2$",
                r"$\displaystyle\int_0^2\!dx\int_x^2 (x+y)\,dy$",
                r"内层 $=\left[xy+\dfrac{y^2}{2}\right]_x^2$",
                r"★ 下限代入：$y=x$ 时 $xy+y^2/2=x^2+\dfrac{x^2}{2}=\dfrac{3x^2}{2}$",
                r"$=\displaystyle\int_0^2\left(2x+2-\dfrac{3x^2}{2}\right)dx=\left[x^2+2x-\dfrac{x^3}{2}\right]_0^2=4$"],
         pitfalls=[r"★ 下限代入时把 $\dfrac{y^2}{2}$ 的 $\dfrac12$ 漏掉（写成 $x^2+x^2=2x^2$）",
                   "上下限顺序写反（写成 $2$ 到 $x$）",
                   "不画图导致 $X$ 型/ $Y$ 型选错，积分限写不出来"],
         evidence={"q_text": "frames/p03_0006.jpg",
                   "answer": "frames/p03_0006.jpg（红笔 =4）",
                   "steps": "transcript_p03.md 第 14 题段"}),

    dict(P3, q_no=15, q_type="计算", t_start=538, t_end=676,
         q_text=r"判断级数 $\sum\limits_{n=1}^{\infty}\dfrac{2^{n}}{n^{2}}$ 的敛散性",
         options=[], answer="发散",
         steps=[r"各项为正 → 正项级数，优先用**比值审敛法**",
                r"$u_n=\dfrac{2^n}{n^2}$，$u_{n+1}=\dfrac{2^{n+1}}{(n+1)^2}$",
                r"$\rho=\lim\limits_{n\to\infty}\dfrac{u_{n+1}}{u_n}"
                r"=\lim\limits_{n\to\infty}\dfrac{2^{n+1}}{(n+1)^2}\cdot\dfrac{n^2}{2^n}=2$",
                r"$\rho=2>1$ → 原级数**发散**"],
         pitfalls=[r"看到 $n^2$ 在分母就以为收敛 —— 指数 $2^n$ 增长远快于 $n^2$",
                   r"$\rho>1$ 判成收敛（比值法：$\rho<1$ 收敛，$\rho>1$ 发散）",
                   r"$\rho=1$ 时比值法失效，要换比较法 —— 本题 $\rho=2$ 不涉及"],
         evidence={"q_text": "frames/p03_0010.jpg",
                   "answer": "frames/p03_0010.jpg（红笔「∴原级数发散」）",
                   "steps": "transcript_p03.md 第 15 题段"}),

    dict(P3, q_no=16, q_type="计算", t_start=676, t_end=878,
         q_text=r"求曲线 $xy+y^{3}+x^{5}-1=0$ 在点 $(0,1)$ 处的切线方程",
         options=[], answer=r"$y=-\dfrac{1}{3}x+1$",
         steps=[r"隐函数求导 —— **方程两端同时对 $x$ 求导**（$y$ 视为 $x$ 的函数）",
                r"$y+xy'+3y^{2}y'+5x^{4}=0$",
                r"解出 $y'=\dfrac{-y-5x^{4}}{x+3y^{2}}$",
                r"代入 $(0,1)$：$k=y'\big|_{(0,1)}=\dfrac{-1-0}{0+3}=-\dfrac{1}{3}$",
                r"点斜式：$y-1=-\dfrac{1}{3}x$，即 $y=-\dfrac{1}{3}x+1$"],
         pitfalls=[r"对 $y^3$ 求导写成 $3y^2$ —— 漏乘 $y'$（链式法则）",
                   r"对 $xy$ 求导写成 $x'y'=y'$ —— 应为 $y+xy'$（乘积法则）",
                   r"求出 $k$ 后忘记写切线方程，只写斜率"],
         evidence={"q_text": "frames/p03_0013.jpg",
                   "answer": "frames/p03_0013.jpg（红笔 y=-1/3x+1）",
                   "steps": "transcript_p03.md 第 16 题段"}),

    dict(P3, q_no=17, q_type="计算", t_start=878, t_end=1104,
         q_text=r"求微分方程 $y'=2xe^{x^{2}-y}$ 满足初始条件 $\left.y\right|_{x=0}=1$ 的特解",
         options=[],
         answer=r"$y=\ln\left(e^{x^{2}}+e-1\right)$",
         steps=[r"把 $e^{x^2-y}$ 拆成 $\dfrac{e^{x^2}}{e^{y}}$，变量即可分离",
                r"分离变量：$e^{y}\,dy=2xe^{x^{2}}\,dx$",
                r"两边积分：$e^{y}=\displaystyle\int e^{x^{2}}d(x^{2})=e^{x^{2}}+C$",
                r"代入 $\left.y\right|_{x=0}=1$：$e=e^{0}+C$ → $C=e-1$",
                r"$e^{y}=e^{x^{2}}+e-1$",
                r"两边取自然对数：$y=\ln\left(e^{x^{2}}+e-1\right)$"],
         pitfalls=[r"★ 取对数时把 $\ln(e^{x^{2}}+e-1)$ 写成 $x^{2}+1$ —— $\ln(A+B)\neq\ln A$，"
                   r"只有 $C=0$ 时才成立",
                   r"分离变量时忘记把 $e^{-y}$ 翻到左边",
                   r"忘记用初始条件求 $C$（题目要的是**特解**，不是通解）"],
         evidence={"q_text": "frames/p03_0016.jpg",
                   "steps": "transcript_p03.md 第 17 题段",
                   "answer": "★ 画面与口播均给出 $y=x^{2}+1$，但那是错的 —— 见 discrepancy"},
         discrepancy={
             "field": "answer",
             "source_claim": r"$y=x^{2}+1$（画面末行 + 口播「LNE的X平方结果就是X方」）",
             "correct": r"$y=\ln(e^{x^{2}}+e-1)$",
             "why": r"老师把 $\ln(e^{x^{2}}+e-1)$ 直接当成 $\ln(e^{x^{2}})=x^{2}$，丢掉了 $+e-1$。"
                    r"验算 $x=1$：正确式 $=\ln(2e-1)\approx 1.49$，老师式 $=2$；"
                    r"只有 $x=0$ 处两者相等（都等于 1），所以代入初始条件检验**查不出**这个错。",
             "action": "落站时以正确式为准，并在该题下标注「本题源讲解有误」"}),

    dict(P3, q_no=18, q_type="证明", t_start=1104, t_end=1205,
         q_text=r"已知函数 $z(x,y)=\sqrt{x^{2}+y^{2}}$，证明："
                r"$\dfrac{\partial^{2}z}{\partial x^{2}}+\dfrac{\partial^{2}z}{\partial y^{2}}=\dfrac{1}{z}$",
         options=[], answer="（证明题，无具体数值）",
         steps=[r"★ 对 $x$ 求偏导时，把 $y$ 当常数",
                r"$\dfrac{\partial z}{\partial x}=\dfrac{2x}{2\sqrt{x^{2}+y^{2}}}"
                r"=\dfrac{x}{\sqrt{x^{2}+y^{2}}}=\dfrac{x}{z}$",
                r"再对 $x$ 求导（商的求导）："
                r"$\dfrac{\partial^{2}z}{\partial x^{2}}=\dfrac{z-x z'_x}{z^{2}}"
                r"=\dfrac{z-\frac{x^{2}}{z}}{z^{2}}=\dfrac{z^{2}-x^{2}}{z^{3}}$",
                r"由 $z(x,y)$ 关于 $x,y$ 的**对称性**，直接写出 "
                r"$\dfrac{\partial^{2}z}{\partial y^{2}}=\dfrac{z^{2}-y^{2}}{z^{3}}$",
                r"相加：$\dfrac{2z^{2}-(x^{2}+y^{2})}{z^{3}}"
                r"=\dfrac{2z^{2}-z^{2}}{z^{3}}=\dfrac{z^{2}}{z^{3}}=\dfrac{1}{z}$，得证"],
         pitfalls=[r"求 $\dfrac{\partial z}{\partial x}$ 时把 $y$ 也当成 $x$ 的函数",
                   r"忘记利用对称性，把 $y$ 方向再硬算一遍（易错且费时）",
                   r"最后一步忘记 $x^{2}+y^{2}=z^{2}$ 这个代换，卡在 $\dfrac{2z^2-x^2-y^2}{z^3}$"],
         evidence={"q_text": "frames/p03_0020.jpg",
                   "answer": "frames/p03_0020.jpg（红笔「成立」）",
                   "steps": "transcript_p03.md 第 18 题段"}),
]


# ══════════════════════════════════════════════════════════════════
# BV1Y3L36bEf1 · P4 综合题
# ══════════════════════════════════════════════════════════════════

P4 = dict(
    bvid="BV1Y3L36bEf1", page=4, subject="高数", year=2026,
    paper="广东省专升本 高等数学", up="孟涛老师",
    section="四、综合题（本大题共 2 小题，19 小题 10 分，20 小题 12 分，共 22 分）",
    source_kind="官方真题卷扫描件",
)

P4_CARDS = [
    dict(P4, q_no=19, q_type="综合", t_start=0, t_end=694,
         q_text=r"已知平面区域 $D$ 是由曲线以及直线 $y=0$，$y=1$，$x=y^{2}$，$x=a$ "
                r"（$0<a<1$，$0<x<1$）围成的区域。" "\n"
                r"(1) 求平面区域 $D$ 的面积 $S(a)$；" "\n"
                r"(2) $a$ 取何值时，$S(a)$ 有最小值，并求出最小值。",
         options=[],
         answer=r"(1) $S(a)=\dfrac{1}{3}-a+\dfrac{4}{3}a^{3/2}$；"
                r"(2) $a=\dfrac{1}{4}$ 时取最小值 $\dfrac{1}{4}$",
         steps=[r"★ 第一步必须画图 —— 四条线围成的区域形状不直观，"
                r"找错区域整题就废",
                r"$x=a$ 代入 $x=y^{2}$ 得交点纵坐标 $y=\sqrt{a}$",
                r"区域拆成两块：$0\le x\le a$ 时 $0\le y\le\sqrt{x}$；"
                r"$a\le x\le 1$ 时 $\sqrt{x}\le y\le 1$",
                r"$S(a)=\displaystyle\int_0^{a}\!\sqrt{x}\,dx+\int_a^{1}\!(1-\sqrt{x})\,dx$",
                r"$=\left[\dfrac{2}{3}x^{3/2}\right]_0^{a}"
                r"+\left[x-\dfrac{2}{3}x^{3/2}\right]_a^{1}"
                r"=\dfrac{1}{3}-a+\dfrac{4}{3}a^{3/2}$",
                r"求导：$S'(a)=-1+2\sqrt{a}=0$ → $\sqrt{a}=\dfrac{1}{2}$ → $a=\dfrac{1}{4}$",
                r"★ 用**极值的第二充分条件**确认是极小："
                r"$S''(a)=\dfrac{1}{\sqrt{a}}>0$",
                r"$S\left(\dfrac{1}{4}\right)=\dfrac{1}{3}-\dfrac{1}{4}"
                r"+\dfrac{4}{3}\cdot\dfrac{1}{8}=\dfrac{1}{4}$"],
         pitfalls=[r"★ 区域找错 —— 它**不是** $x$ 从 $y^2$ 到 $a$ 的那一块，"
                   r"而是「$x<a$ 在抛物线下方 + $x>a$ 在抛物线上方」两块之和",
                   r"求最值时只用 $S'(a)=0$ 就下结论，不验 $S''$ 的符号",
                   r"$a$ 的取值范围是 $0<a<1$，算出的 $a=\dfrac14$ 要回代确认落在区间内"],
         evidence={"q_text": "frames/p04_0001.jpg / frames/p04_0004.jpg",
                   "answer": "frames/p04_0004.jpg（S(a) 展开式）",
                   "steps": "transcript_p04.md 段1 + 段2"}),

    dict(P4, q_no=20, q_type="综合", t_start=694, t_end=919,
         q_text=r"已知 $f(x)$ 在 $[0,+\infty)$ 上连续，$\lim\limits_{x\to+\infty}f(x)=2$，"
                r"且满足方程 $y(x)=e^{-3x}\displaystyle\int_0^{x}e^{3t}f(t)\,dt$，"
                r"证明 $y'+3y=f(x)$，并求极限 $\lim\limits_{x\to+\infty}y(x)$。",
         options=[],
         answer=r"(1) 证明见 steps；(2) $\lim\limits_{x\to+\infty}y(x)=\dfrac{2}{3}$",
         steps=[r"★ 看到「变限积分 + 要证的关系式」→ **方程两边同时对 $x$ 求导**，"
                r"目的是把积分号去掉",
                r"$y(x)=e^{-3x}\displaystyle\int_0^{x}e^{3t}f(t)\,dt$ 是乘积，"
                r"用前导后不导：",
                r"$y'(x)=-3e^{-3x}\displaystyle\int_0^{x}e^{3t}f(t)\,dt"
                r"+e^{-3x}\cdot e^{3x}f(x)$",
                r"第一项 $=-3y(x)$；第二项 $e^{-3x}\cdot e^{3x}=1$，得 $f(x)$",
                r"∴ $y'(x)=-3y(x)+f(x)$，即 $y'+3y=f(x)$，得证",
                r"求极限：$y(x)=\dfrac{\int_0^{x}e^{3t}f(t)\,dt}{e^{3x}}$ 是 $\dfrac{\infty}{\infty}$ 型",
                r"用洛必达：$=\lim\limits_{x\to+\infty}"
                r"\dfrac{e^{3x}f(x)}{3e^{3x}}=\lim\limits_{x\to+\infty}\dfrac{f(x)}{3}$",
                r"$\because\lim\limits_{x\to+\infty}f(x)=2$ ∴ 极限 $=\dfrac{2}{3}$"],
         pitfalls=[r"两边求导时漏掉 $e^{-3x}$ 的导数项（$-3e^{-3x}$）—— 这是乘积不是单项",
                   r"$e^{-3x}\cdot e^{3x}$ 没约掉，导致式子化简不下去",
                   r"洛必达后忘记 $e^{3x}$ 求导要乘 3（分母 $3e^{3x}$）",
                   r"最后把答案写成 2（那是 $\lim f(x)$）而不是 $\dfrac{2}{3}$"],
         evidence={"q_text": "frames/p04_0010.jpg",
                   "answer": "frames/p04_0010.jpg（洛必达链条，末行 f(x)/3）",
                   "steps": "transcript_p04.md 段2 后半"}),
]


if __name__ == "__main__":
    cards = P1_CARDS + P2_CARDS + P3_CARDS + P4_CARDS
    # ★ 文档里写了 evidence 是「硬字段：每项都要能指回哪一帧或哪一秒」，
    #   但代码从来没检查过 —— 漏填就是一张无法溯源的卡，而且没人会发现。
    #   这里补一条告警（不阻断写入：缺证据是内容问题，该由人回看画面补）。
    missing_ev = [c["q_no"] for c in cards
                  if not c.get("evidence") or not isinstance(c.get("evidence"), dict)]
    if missing_ev:
        LOG.warning("有 %d 张卡缺 evidence（无法溯源到帧/秒）：%s", len(missing_ev), missing_ev)
    dup = sorted({c["q_no"] for c in cards if [x["q_no"] for x in cards].count(c["q_no"]) > 1})
    if dup:
        LOG.error("题号重复：%s —— 后写的会覆盖先写的", dup)
    LOG.info("BV1Y3L36bEf1 卡片 %d 张 · 题号 %s", len(cards), [c["q_no"] for c in cards])
    p = write("BV1Y3L36bEf1", cards)
    print("写入 %s · %d 张卡" % (p, len(cards)))
    print("题号 %s" % [c["q_no"] for c in cards])
    print("答案 %s" % [c["answer"] for c in cards])
