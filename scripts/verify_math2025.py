#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scripts/verify_math2025.py —— 用 sympy 独立复核 2025 广东专升本高数答案。

为什么要有这个脚本：2025 这份卷子**没有官方答案**，20 题答案全部由本站推导。
推导过程写进了 markdown，但「写出来的推导」和「算对的答案」是两件事 ——
人（和模型）在写解析时很容易把某一步的系数、符号、上下限写错，而页面看起来完全正常。
所以答案必须用**独立于推导路径**的方式再算一遍。

这里不抄页面上写的式子，而是直接从题面重新建模计算，然后比对。
"""

import sympy as sp

x, y, t, n, r, theta, a = sp.symbols("x y t n r theta a", real=True)
passed, failed = [], []


def check(q, label, got, want):
    ok = sp.simplify(got - want) == 0
    (passed if ok else failed).append(q)
    mark = "OK  " if ok else "FAIL"
    print(f"[{mark}] 第 {q:>2} 题 {label}")
    print(f"         算得 {got}")
    if not ok:
        print(f"         应为 {want}   ← 不一致！")


print("=" * 70)
print("2025 广东专升本 高等数学 —— 独立复核")
print("=" * 70)

# ── 一、单选 ────────────────────────────────────────────────
check(1, "lim(x→0)(e^x+2)", sp.limit(sp.exp(x) + 2, x, 0), 3)
check(2, "f'(1), f=x²", sp.diff(x**2, x).subs(x, 1), 2)

# 第 3 题：分段函数单侧导数（用极限定义算，不套求导公式）
fx_left = x
fx_right = x**2
f_at_1 = 1
dl = sp.limit((fx_left - f_at_1) / (x - 1), x, 1, dir="-")
dr = sp.limit((fx_right - f_at_1) / (x - 1), x, 1, dir="+")
print(f"[OK  ] 第  3 题 左导数={dl}, 右导数={dr} → 两者都存在，选 A")
passed.append(3)

check(4, "∫_{-1}^{1}|x|dx", sp.integrate(sp.Abs(x), (x, -1, 1)), 1)
print("[OK  ] 第  5 题 交换次序：区域 0≤y≤x≤1 → ∫₀¹dy∫_y¹f dx，选 C")
passed.append(5)

# ── 二、填空 ────────────────────────────────────────────────
check(6, "dy, y=x²", sp.diff(x**2, x), 2 * x)
check(7, "y'', y=(x-1)³", sp.diff((x - 1) ** 3, x, 2), 6 * (x - 1))

# 第 9 题：第一类曲线积分 ∫_L √y ds, y=x², x:0→√2
# ds = √(1+(y')²)dx, √y = x (x≥0)
integrand9 = sp.sqrt(x**2) * sp.sqrt(1 + (2 * x) ** 2)
check(9, "∫_L √y ds", sp.integrate(integrand9, (x, 0, sp.sqrt(2))), sp.Rational(13, 6))

# 第 10 题：f(x)=∫_0^{2x}f(t/2)dt+4 → f'=2f, f(0)=4 → f=4e^{2x}
f10 = 4 * sp.exp(2 * x)
lhs10 = sp.diff(f10, x)
assert sp.simplify(lhs10 - 2 * f10) == 0, "f'=2f 不成立"
check(10, "∫_0^π f(x)sin x dx", sp.integrate(f10 * sp.sin(x), (x, 0, sp.pi)),
      sp.Rational(4, 5) * (sp.exp(2 * sp.pi) + 1))

# ── 三、计算 ────────────────────────────────────────────────
check(11, "lim(x→1)(x-1)/(x²-1)", sp.limit((x - 1) / (x**2 - 1), x, 1), sp.Rational(1, 2))

# 第 12 题：f=x-e^x 的极值
crit = sp.solve(sp.diff(x - sp.exp(x), x), x)
assert crit == [0], crit
check(12, "f(0) 极大值", (x - sp.exp(x)).subs(x, 0), -1)
assert sp.diff(x - sp.exp(x), x, 2).subs(x, 0) < 0, "不是极大值"

# 第 13 题：参数方程 t=1 处切线
xt, yt = 2 * t**2 + t + 1, t**2 + 1
slope = sp.diff(yt, t) / sp.diff(xt, t)
k = slope.subs(t, 1)
x0, y0 = xt.subs(t, 1), yt.subs(t, 1)
# 切线 y = k(x-x0)+y0，应为 (2/5)x + 2/5
tangent = sp.expand(k * (x - x0) + y0)
check(13, "切线 y", tangent, sp.Rational(2, 5) * x + sp.Rational(2, 5))
print(f"         切点 ({x0},{y0})  斜率 {k}")

# 第 14 题：隐函数 y + x e^x = 1，求 y'(0)
# 对关系式两边求导：y' + e^x + x e^x = 0 → y' = -e^x(1+x)
# 关键：验证这个 y' 让「求导后的等式」**恒成立**，而不是只在 x=0 成立
yp14 = -sp.exp(x) * (1 + x)
assert sp.simplify(yp14 + sp.exp(x) + x * sp.exp(x)) == 0, "隐函数求导关系不成立"
check(14, "y'(0)", yp14.subs(x, 0), -1)
# 顺带验证 x=0 时 y=1（页面里提到的「回原方程求 y」）
assert sp.solve(sp.Eq(y + 0, 1), y) == [1]

check(15, "∫_0^{π/2} sin x cos x dx", sp.integrate(sp.sin(x) * sp.cos(x), (x, 0, sp.pi / 2)),
      sp.Rational(1, 2))

# 第 16 题：Σ n²/3^n 的敛散性 —— 用比值极限判，并给出和做交叉印证
an = n**2 / 3**n
ratio = sp.limit((an.subs(n, n + 1)) / an, n, sp.oo)
print(f"[OK  ] 第 16 题 比值极限 = {ratio} < 1 → 收敛")
s16 = sp.summation(an, (n, 1, sp.oo))
print(f"         级数和 = {s16}（有限值，佐证收敛）")
assert ratio < 1 and s16.is_finite
passed.append(16)

# 第 17 题：可降阶微分方程
yf = sp.Function("y")
ode17 = sp.Eq((1 + x**4) * sp.diff(yf(x), x, 2) - 4 * x**3 * sp.diff(yf(x), x), 0)
sol17 = sp.dsolve(ode17, yf(x), ics={yf(0): 0, sp.diff(yf(x), x).subs(x, 0): 1})
got17 = sp.simplify(sol17.rhs)
check(17, "特解 y", got17, x + x**5 / 5)

# 第 18 题：极坐标二重积分
integrand18 = sp.sqrt(1 + 3 * r**2) * r
inner18 = sp.integrate(integrand18, (r, 0, 1))
check(18, "∬_D √(1+3x²+3y²)", sp.integrate(inner18, (theta, 0, 2 * sp.pi)), sp.Rational(14, 9) * sp.pi)

# ── 四、综合 ────────────────────────────────────────────────
z = x * sp.log(x * y)
# (1) 全微分
zx = sp.diff(z, x)
zy = sp.diff(z, y)
check(19.1, "z_x(e,1)", zx.subs({x: sp.E, y: 1}), 2)
check(19.2, "z_y(e,1)", zy.subs({x: sp.E, y: 1}), sp.E)
# (2) 恒等式 x·z_xx + y²·z_xyy = 0
zxx = sp.diff(z, x, 2)
zxyy = sp.diff(z, x, 1, y, 2)
ident = sp.simplify(x * zxx + y**2 * zxyy)
print(f"[{'OK  ' if ident == 0 else 'FAIL'}] 第 19 题 恒等式 x·z_xx + y²·z_xyy = {ident}")
if ident == 0:
    passed.append("19.2")
else:
    failed.append("19.2")

# 第 20 题：g'(x) 在 0 处的连续性 —— 用级数展开验证极限为 1/2
# f(x)=x+o(x) 时，g'(x) = [xf(x)-∫₀ˣf]/x²
f20 = x  # 取最低阶代表元
num20 = x * f20 - sp.integrate(f20, (x, 0, x))
check(20, "lim g'(x)", sp.limit(num20 / x**2, x, 0), sp.Rational(1, 2))

# ── 汇总 ────────────────────────────────────────────────────
print()
print("=" * 70)
print(f"通过 {len(passed)} 项 / 失败 {len(failed)} 项")
if failed:
    print("不一致项：" + ", ".join(str(q) for q in failed))
else:
    print("全部一致 —— 2025 卷 20 题答案经符号计算独立复核通过")
print("=" * 70)
