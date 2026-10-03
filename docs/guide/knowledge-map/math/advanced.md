# 高数 · 多元微积分 · 级数 · 线代 · 证明

> 向量代数与空间解析几何、多元函数微分学、二重积分、无穷级数、线性代数、证明专项

> 本页 6 章 / 362 条知识点。来源与可信度说明见[知识地图总览](/guide/knowledge-map/)。

## 七、向量代数与空间解析几何


### 向量的概念、坐标表示、模长与单位向量
- **要点**：向量是既有大小又有方向的量（物理上称矢量），几何上是带方向的线段（有向线段），只有大小的量叫标量；空间中的向量没有具体位置，只有大小和方向；由起点 A 指向终点 B 的向量 AB 用「终点坐标减起点坐标」表示，即 {x₂−x₁, y₂−y₁, z₂−z₁}，相当于把向量平移到原点；注意向量用大括号、点的坐标用小括号，另可写作 x i + y j + z k（i、j、k 为三轴正方向的单位向量）。向量的模（长度）就是起点到终点的距离：|AB|=√((x₂−x₁)²+(y₂−y₁)²+(z₂−z₁)²)；若已写成 {x,y,z}，则 |a|=√(x²+y²+z²)。模长为 1 的向量称为单位向量，记作 a⁰ 或 e，求法是把向量各坐标分别除以该向量的模，即 a⁰={x/|a|, y/|a|, z/|a|}，其模长恒为 1；反向的单位向量再在前面加负号。模长为 0 的向量叫零向量，起点终点重合、方向任意。
- **关键概念**：`向量`、`标量`、`终点减起点`、`模`、`单位向量`、`零向量`、`i,j,k`
- **相互关系**：模长是单位向量、点乘、叉乘的定义基础；这是向量加减、点乘、叉乘、方向向量的统一入口；与两点间距离公式同源，结果常需分母有理化。
- **出处**：[陈哥 P81](https://www.bilibili.com/video/BV1husGzwEtZ?p=81)；[杰哥 P93](https://www.bilibili.com/video/BV1Up4y1Y76a?p=93)、[P95](https://www.bilibili.com/video/BV1Up4y1Y76a?p=95)、[P96](https://www.bilibili.com/video/BV1Up4y1Y76a?p=96)；[米哥 P82](https://www.bilibili.com/video/BV1swAWerEzS?p=82)；[学士帽 P105](https://www.bilibili.com/video/BV1X4411J792?p=105)；[ok姐 P83](https://www.bilibili.com/video/BV1vm421s7mv?p=83)、[P85](https://www.bilibili.com/video/BV1vm421s7mv?p=85)、[P86](https://www.bilibili.com/video/BV1vm421s7mv?p=86)

### 相等、负向量、夹角与位置关系
- **要点**：大小相等且方向相同则相等；大小相等方向相反则为负向量。两向量夹角 φ 是平移到共起点后所夹的不超过 π 的角，0≤φ≤π；φ=0 或 π 为平行（同向为 0、反向为 π），φ=π/2 为垂直。零向量与任何向量既平行又垂直。
- **关键概念**：`负向量`、`夹角`、`平行`、`垂直`
- **出处**：[ok姐 P83](https://www.bilibili.com/video/BV1vm421s7mv?p=83)；[陈哥 P81](https://www.bilibili.com/video/BV1husGzwEtZ?p=81)

### 向量的加减与数乘
- **要点**：两向量相加减就是对应坐标相加减（满足交换律与结合律）；加法口诀「首尾相接，从首指向尾」（平行四边形或三角形法则）；减法口诀「连起点，指被减」，即平移到共起点后由减向量终点指向被减向量终点（a−b 的方向由 b 终点指向 a 终点）。数 k 与 a={x₁,y₁,z₁} 相乘即把 k 乘到每一个坐标上得 {kx₁,ky₁,kz₁}，|λa|=|λ||a|，k>0 时同向、k&lt;0 时反向，两者始终平行；λ=0 得零向量，数值为零但仍带方向。向量没有除法。
- **关键概念**：`对应坐标相加减`、`数乘`、`零向量`、`三角形法则`、`首尾相接`、`连起点指被减`
- **出处**：[陈哥 P81](https://www.bilibili.com/video/BV1husGzwEtZ?p=81)、[P84](https://www.bilibili.com/video/BV1husGzwEtZ?p=84)；[杰哥 P97](https://www.bilibili.com/video/BV1Up4y1Y76a?p=97)；[米哥 P84](https://www.bilibili.com/video/BV1swAWerEzS?p=84)；[学士帽 P106](https://www.bilibili.com/video/BV1X4411J792?p=106)；[ok姐 P84](https://www.bilibili.com/video/BV1vm421s7mv?p=84)、[P85](https://www.bilibili.com/video/BV1vm421s7mv?p=85)

### 两向量平行的充要条件
- **要点**：非零向量 a 与 b 平行的充要条件是存在唯一实数 λ 使 b=λa；坐标形式即对应坐标成比例 b_x/a_x=b_y/a_y=b_z/a_z（也可写作叉乘为零向量），可据此求未知参数。实际计算一律用比值法而不用叉乘。
- **关键概念**：`b=λa`、`对应坐标成比例`
- **相互关系**：这两个结论会直接平移到平面与平面、直线与直线的位置关系判断。
- **出处**：[陈哥 P81](https://www.bilibili.com/video/BV1husGzwEtZ?p=81)；[杰哥 P101](https://www.bilibili.com/video/BV1Up4y1Y76a?p=101)；[ok姐 P84](https://www.bilibili.com/video/BV1vm421s7mv?p=84)、[P85](https://www.bilibili.com/video/BV1vm421s7mv?p=85)

### 方向角与方向余弦
- **要点**：非零向量与三条坐标轴的夹角 α、β、γ 称方向角，范围均为 [0,π]；向量 a={x,y,z} 与 x、y、z 轴正方向的夹角分别为 α、β、γ，则 cos α=x/|a|、cos β=y/|a|、cos γ=z/|a|，且满足恒等式 cos²α+cos²β+cos²γ=1。由余弦值结合范围与诱导公式反求角，如 cos α=−½ 得 α=2π/3。以三个方向余弦为坐标的向量就是单位向量，故单位化后的坐标就是方向余弦。
- **关键概念**：`方向角`、`方向余弦`、`cos²α+cos²β+cos²γ=1`、`诱导公式`
- **出处**：[陈哥 P81](https://www.bilibili.com/video/BV1husGzwEtZ?p=81)；[学士帽 P105](https://www.bilibili.com/video/BV1X4411J792?p=105)；[ok姐 P87](https://www.bilibili.com/video/BV1vm421s7mv?p=87)；[石头 P59](https://www.bilibili.com/video/BV18CL26WEJ3?p=59)

### 数量积（点乘）
- **要点**：数量积又称点积、内积，记作 a·b，结果是一个数值；几何式为 |a||b|cos θ（即 a 在 b 方向上的投影长度乘 b 的模长），坐标式为 x₁x₂+y₁y₂+z₁z₂（对应坐标相乘再相加）；满足交换律、分配律、结合律。a·a=|a|²（自身与自身夹角为 0，cos0=1）。特别地 a⊥b ⟺ a·b=0 ⟺ x₁x₂+y₁y₂+z₁z₂=0，是充要条件（因 cos90°=0，投影为零）。计算用坐标式，判断位置关系用几何式。由垂直关系可反求向量中的未知参数：按对应坐标之积的和列方程即可（如 1×2+2×5+3l=0 解得 l=−4）。
- **关键概念**：`数量积`、`点乘`、`结果是数`、`|a||b|cosθ`、`投影`、`垂直`
- **相互关系**：与向量积极易混淆，点乘得数、叉乘得向量；这两条在判断垂直与化简向量表达式时最常用，垂直判断也是后续平面、直线位置关系的基础。
- **出处**：[陈哥 P81](https://www.bilibili.com/video/BV1husGzwEtZ?p=81)；[杰哥 P97](https://www.bilibili.com/video/BV1Up4y1Y76a?p=97)、[P98](https://www.bilibili.com/video/BV1Up4y1Y76a?p=98)；[米哥 P84](https://www.bilibili.com/video/BV1swAWerEzS?p=84)、[P85](https://www.bilibili.com/video/BV1swAWerEzS?p=85)、[P86](https://www.bilibili.com/video/BV1swAWerEzS?p=86)；[学士帽 P106](https://www.bilibili.com/video/BV1X4411J792?p=106)、[P107](https://www.bilibili.com/video/BV1X4411J792?p=107)；[ok姐 P88](https://www.bilibili.com/video/BV1vm421s7mv?p=88)

### 向量的夹角与投影
- **要点**：由数量积公式反解即得 cos θ=a·b/(|a||b|)，再取反三角函数得 θ=arccos(a·b/(|a||b|))（夹角在 [0,π] 内）；只需知道两向量坐标即可求夹角。a 在 b 上的投影长度等于 |a|cos θ，计算式为 (a·b)/|b|；反过来 b 在 a 上的投影为 (a·b)/|a|。
- **关键概念**：`夹角`、`cosθ=(a·b)/(|a||b|)`、`投影`、`除以被投影向量的模`
- **相互关系**：求角问题通法——先写出两向量坐标，再用坐标点积与模反解余弦。
- **出处**：[陈哥 P81](https://www.bilibili.com/video/BV1husGzwEtZ?p=81)；[杰哥 P97](https://www.bilibili.com/video/BV1Up4y1Y76a?p=97)、[P98](https://www.bilibili.com/video/BV1Up4y1Y76a?p=98)；[学士帽 P106](https://www.bilibili.com/video/BV1X4411J792?p=106)；[ok姐 P88](https://www.bilibili.com/video/BV1vm421s7mv?p=88)

### 向量积（叉乘）与三阶行列式
- **要点**：向量积又称叉乘、外积，记作 a×b，结果是一个向量：大小 |a||b|sin θ（等于以 a、b 为邻边的平行四边形面积，取一半即对应三角形的面积，即 S=½|a×b|），方向由右手法则（右手螺旋法则）确定（右手四指从 a 转向 b，大拇指指向即结果方向），故 b×a=−a×b（反交换律，顺序不能颠倒）；新向量同时垂直于 a 与 b，凡遇「求同时垂直于两个向量的向量」或求法向量必用叉乘。计算用三阶行列式：第一行写 i、j、k，第二、三行分别写 a、b 的坐标，按主对角线元素相乘之和减副对角线元素相乘之和展开（或按第一行展开），展开符号固定为「一正、二负、三正」（中间项为减号），每个二阶行列式按「右对角线减左对角线」计算；书写务必按 i、j、k 顺序，因其分别对应 x、y、z 坐标。a×a=0；a×b=0 与 a∥b 互为充要条件；垂直时模等于两模之积。
- **关键概念**：`向量积`、`叉乘`、`右手法则`、`三阶行列式`、`反交换律`、`平行四边形面积`、`法向量`
- **相互关系**：与点积结论对照：点积为零对应垂直，叉乘为零向量对应平行；求三角形面积、求与两向量都垂直的法向量都依赖这一结论。
- **出处**：[陈哥 P81](https://www.bilibili.com/video/BV1husGzwEtZ?p=81)；[杰哥 P97](https://www.bilibili.com/video/BV1Up4y1Y76a?p=97)、[P99](https://www.bilibili.com/video/BV1Up4y1Y76a?p=99)、[P100](https://www.bilibili.com/video/BV1Up4y1Y76a?p=100)；[米哥 P84](https://www.bilibili.com/video/BV1swAWerEzS?p=84)、[P85](https://www.bilibili.com/video/BV1swAWerEzS?p=85)、[P87](https://www.bilibili.com/video/BV1swAWerEzS?p=87)、[P88](https://www.bilibili.com/video/BV1swAWerEzS?p=88)；[学士帽 P106](https://www.bilibili.com/video/BV1X4411J792?p=106)、[P107](https://www.bilibili.com/video/BV1X4411J792?p=107)；[ok姐 P89](https://www.bilibili.com/video/BV1vm421s7mv?p=89)

### 平面的法向量与点法式、一般式方程
- **要点**：垂直于平面的非零向量称为法向量，记 n=(A,B,C)，同一平面有无穷多个且互相平行，法向量垂直于平面内任意一条直线（平面没有方向向量，直线没有法向量）。由 n⊥M₀M 得点法式 A(x−x₀)+B(y−y₀)+C(z−z₀)=0，即一个点加一个法向量唯一确定一个平面，只给点或只给法向量都定不下一个平面；展开得一般式 Ax+By+Cz+D=0，系数即法向量（看 x、y、z 的系数），结果应化为一般式。截距式为 x/a+y/b+z/c=1。求平面方程优先考虑点法式。
- **关键概念**：`法向量`、`点法式方程`、`一般式方程`、`系数即法向量`、`截距式`
- **相互关系**：两式可互相转化；求平面方程的通法是「找一个点 + 求法向量」。
- **出处**：[陈哥 P82](https://www.bilibili.com/video/BV1husGzwEtZ?p=82)；[杰哥 P102](https://www.bilibili.com/video/BV1Up4y1Y76a?p=102)；[米哥 P89](https://www.bilibili.com/video/BV1swAWerEzS?p=89)；[学士帽 P108](https://www.bilibili.com/video/BV1X4411J792?p=108)、[P110](https://www.bilibili.com/video/BV1X4411J792?p=110)；[ok姐 P90](https://www.bilibili.com/video/BV1vm421s7mv?p=90)

### 三点确定平面与叉乘求法向量
- **要点**：三点确定一个平面。取两点构成两个不共线向量（如 M₁M₂ 与 M₁M₃），叉乘得法向量 n=M₁M₂×M₁M₃，任取一点写点法式再化一般式。依据是「直线垂直于平面内两条相交直线则垂直于该平面」。
- **关键概念**：`三点确定一个平面`、`叉乘求法向量`、`相交向量定平面`
- **出处**：[陈哥 P82](https://www.bilibili.com/video/BV1husGzwEtZ?p=82)；[米哥 P90](https://www.bilibili.com/video/BV1swAWerEzS?p=90)；[ok姐 P90](https://www.bilibili.com/video/BV1vm421s7mv?p=90)

### 缺变量与剩变量的几何意义（特殊平面方程）
- **要点**：一般式中 D=0 表示平面过原点；缺某个变量（系数为零），平面平行于对应坐标轴（因为该变量取值不影响方程）或与该轴重合（缺字母且 D=0 则平面经过该坐标轴）；只剩一个变量（两个系数为零），平面垂直于对应坐标轴，即平行于相应的坐标平面。属超纲内容，过坐标轴的题可直接设简化方程。
- **关键概念**：`过原点`、`缺变量→平行于轴`、`剩变量→垂直于轴`、`过坐标轴`
- **相互关系**：两条结论方向相反，容易混淆。
- **出处**：[陈哥 P82](https://www.bilibili.com/video/BV1husGzwEtZ?p=82)；[杰哥 P107](https://www.bilibili.com/video/BV1Up4y1Y76a?p=107)；[米哥 P94](https://www.bilibili.com/video/BV1swAWerEzS?p=94)

### 求平面方程的综合题型
- **要点**：套路是先凑齐一个点和法向量，再套点法式。点常由「过某点」或两点连线给出；法向量最难求，当题给「平面过两点且垂直于某已知平面」时，待求法向量同时垂直于 AB 向量和已知平面的法向量，故用两者叉乘求出（n₁=M₁M₂×n₂，向量可平移）。难点不在公式，而在从题干中提炼出「点 + 法向量」两个条件。
- **关键概念**：`点法式`、`叉乘求法向量`、`平移不变性`、`抽取题干信息`
- **出处**：[杰哥 P105](https://www.bilibili.com/video/BV1Up4y1Y76a?p=105)；[ok姐 P91](https://www.bilibili.com/video/BV1vm421s7mv?p=91)

### 平面的夹角与点到平面的距离
- **要点**：两平面的夹角定义为各自垂直于交线的两条直线的夹角，范围 [0,π/2]，等于两法向量的夹角，用 cos θ=|n₁·n₂|/(|n₁||n₂|) 算出余弦后反推角度（取锐角故加绝对值；不取绝对值时得到的是两法向量夹角，可为钝角）。两平面垂直的充要条件是 n₁·n₂=0；平行或重合的充要条件是法向量对应坐标成比例（若连 D 的比值也相等则重合）。点 (x₀,y₀,z₀) 到平面 Ax+By+Cz+D=0 的距离为 d=|Ax₀+By₀+Cz₀+D|/√(A²+B²+C²)，即点代入平面方程取绝对值再除以法向量的模。平行平面距离 d=|D₂−D₁|/√(A²+B²+C²)（只有 D 不同时两平面才平行）。均为低频考点。判断两平面关系时按「先看系数是否成比例，再验证点积是否为零」的顺序做。
- **关键概念**：`n₁,n₂`、`取绝对值`、`点到平面的距离`、`法向量的模`
- **相互关系**：垂直的情况计算量最大，考得最多；分母是模长相乘，不是绝对值。
- **出处**：[陈哥 P86](https://www.bilibili.com/video/BV1husGzwEtZ?p=86)；[杰哥 P103](https://www.bilibili.com/video/BV1Up4y1Y76a?p=103)、[P104](https://www.bilibili.com/video/BV1Up4y1Y76a?p=104)、[P106](https://www.bilibili.com/video/BV1Up4y1Y76a?p=106)；[米哥 P91](https://www.bilibili.com/video/BV1swAWerEzS?p=91)、[P92](https://www.bilibili.com/video/BV1swAWerEzS?p=92)、[P93](https://www.bilibili.com/video/BV1swAWerEzS?p=93)；[学士帽 P109](https://www.bilibili.com/video/BV1X4411J792?p=109)、[P112](https://www.bilibili.com/video/BV1X4411J792?p=112)；[ok姐 P91](https://www.bilibili.com/video/BV1vm421s7mv?p=91)、[P92](https://www.bilibili.com/video/BV1vm421s7mv?p=92)

### 直线的点向式方程与参数式方程
- **要点**：平行于直线的非零向量称为方向向量，记为 s=(m,n,p)，有无穷多条且互相平行（直线无法向量）。已知直线上一点 M(x₀,y₀,z₀) 及方向向量 s，则点向式方程为 (x−x₀)/m=(y−y₀)/n=(z−z₀)/p，分子中被减的数为直线上一点，分母为方向向量；令该比值等于参数 t 即得参数式 x=x₀+mt、y=y₀+nt、z=z₀+pt，t 的系数即方向向量；确定直线只需求出「一个点 + 一个方向向量」。看分母得方向向量，看分子得直线所过的点。
- **关键概念**：`点向式`、`方向向量 s`、`参数式`
- **相互关系**：与点法式对偶——直线用「点 + 方向向量」，平面用「点 + 法向量」；点向式与参数式可直接互化；求交点类问题一律化为参数方程，因只剩一个变量 t，计算最简。
- **出处**：[陈哥 P83](https://www.bilibili.com/video/BV1husGzwEtZ?p=83)；[杰哥 P108](https://www.bilibili.com/video/BV1Up4y1Y76a?p=108)；[米哥 P95](https://www.bilibili.com/video/BV1swAWerEzS?p=95)、[P96](https://www.bilibili.com/video/BV1swAWerEzS?p=96)；[学士帽 P110](https://www.bilibili.com/video/BV1X4411J792?p=110)；[ok姐 P93](https://www.bilibili.com/video/BV1vm421s7mv?p=93)

### 点向式的分母为零与直线的一般式方程
- **要点**：方向向量的某坐标为零时，该零照写到分母位置，不适用「分母不能为零」的限制。任意空间直线可视为两不平行平面的交线，由两平面方程联立表示（一般式/交面式）；两平面的法向量都垂直交线，故直线的方向向量 S=N₁×N₂；求点时可令点向式分子为零或令某坐标取特值。平行直线的方程可直接借用已知直线的方向向量。
- **关键概念**：`分母为零`、`交线`、`S=N₁×N₂`
- **相互关系**：一般式最易出考题，因为方向向量需要计算。
- **出处**：[陈哥 P83](https://www.bilibili.com/video/BV1husGzwEtZ?p=83)；[杰哥 P108](https://www.bilibili.com/video/BV1Up4y1Y76a?p=108)；[米哥 P95](https://www.bilibili.com/video/BV1swAWerEzS?p=95)、[P96](https://www.bilibili.com/video/BV1swAWerEzS?p=96)；[ok姐 P93](https://www.bilibili.com/video/BV1vm421s7mv?p=93)

### 两直线与两平面的位置关系
- **要点**：设两直线方向向量为 s₁={l₁,m₁,n₁}、s₂={l₂,m₂,n₂}：平行的充要条件是分量成比例 l₁/l₂=m₁/m₂=n₁/n₂；垂直的充要条件是点积为零 l₁l₂+m₁m₂+n₁n₂=0。两平面法向量平行则平行（或重合），垂直则垂直。若两直线平行且有公共点则重合——判出平行后必须验证是否有公共点，否则会把重合误判为平行，是常见陷阱。考试给出两条直线时，先看分量是否成比例、再看点积是否为零即可判定位置关系。
- **关键概念**：`方向向量`、`成比例`、`点积为零`、`重合`
- **相互关系**：所有位置关系都归结为向量关系的判断；垂直的情况计算量最大，考得最多。
- **出处**：[陈哥 P84](https://www.bilibili.com/video/BV1husGzwEtZ?p=84)；[杰哥 P109](https://www.bilibili.com/video/BV1Up4y1Y76a?p=109)、[P111](https://www.bilibili.com/video/BV1Up4y1Y76a?p=111)；[米哥 P92](https://www.bilibili.com/video/BV1swAWerEzS?p=92)、[P97](https://www.bilibili.com/video/BV1swAWerEzS?p=97)、[P98](https://www.bilibili.com/video/BV1swAWerEzS?p=98)；[学士帽 P109](https://www.bilibili.com/video/BV1X4411J792?p=109)、[P111](https://www.bilibili.com/video/BV1X4411J792?p=111)；[ok姐 P94](https://www.bilibili.com/video/BV1vm421s7mv?p=94)

### 直线与平面的位置关系
- **要点**：设直线方向向量 s={l,m,n}、平面法向量 n={a,b,c}：直线与平面平行的充要条件是 s⊥n，即 la+mb+nc=0，若在此基础上还有公共点（取直线上一点代入平面方程成立）则直线落在平面上（重合）；直线与平面垂直的充要条件是 s∥n，即 l/a=m/b=n/c。注意「平行对应点积为零、垂直对应分量成比例」与直觉相反，是易错点，考得最多。斜交一般不考。
- **关键概念**：`法向量 n`、`la+mb+nc=0`、`分量成比例`、`S⊥N → 线面平行`、`S∥N → 线面垂直`
- **相互关系**：判出平行后同样要带回直线上一点验证。
- **出处**：[陈哥 P84](https://www.bilibili.com/video/BV1husGzwEtZ?p=84)；[杰哥 P110](https://www.bilibili.com/video/BV1Up4y1Y76a?p=110)、[P111](https://www.bilibili.com/video/BV1Up4y1Y76a?p=111)；[米哥 P92](https://www.bilibili.com/video/BV1swAWerEzS?p=92)、[P97](https://www.bilibili.com/video/BV1swAWerEzS?p=97)、[P98](https://www.bilibili.com/video/BV1swAWerEzS?p=98)；[学士帽 P112](https://www.bilibili.com/video/BV1X4411J792?p=112)；[ok姐 P95](https://www.bilibili.com/video/BV1vm421s7mv?p=95)

### 三类夹角公式
- **要点**：向量夹角范围是 [0,π]，而线线、面面夹角都取锐角，故余弦公式分子须加绝对值：cos θ=|s₁·s₂|/(|s₁||s₂|)（线线）、cos θ=|n₁·n₂|/(|n₁||n₂|)（面面）；线面夹角定义为直线与其在平面上投影的夹角，范围 [0,π/2]，取正弦：sin θ=|s·n|/(|s||n|)。三者都归结为向量运算。
- **关键概念**：`数量积`、`模长`、`cos θ`、`sin θ`、`线面角`
- **相互关系**：易错：分母是模长相乘，不是绝对值；与两平面夹角公式混用（此处用正弦）。
- **出处**：[陈哥 P86](https://www.bilibili.com/video/BV1husGzwEtZ?p=86)；[杰哥 P106](https://www.bilibili.com/video/BV1Up4y1Y76a?p=106)、[P112](https://www.bilibili.com/video/BV1Up4y1Y76a?p=112)；[米哥 P91](https://www.bilibili.com/video/BV1swAWerEzS?p=91)；[学士帽 P109](https://www.bilibili.com/video/BV1X4411J792?p=109)、[P112](https://www.bilibili.com/video/BV1X4411J792?p=112)；[ok姐 P91](https://www.bilibili.com/video/BV1vm421s7mv?p=91)、[P94](https://www.bilibili.com/video/BV1vm421s7mv?p=94)、[P95](https://www.bilibili.com/video/BV1vm421s7mv?p=95)

### 直线与平面的交点、过点作垂线及垂足
- **要点**：直线方程与平面方程直接联立无法求解，须先把点向式化为参数式（引入参数 t 作公共比值），使交点坐标都只含 t；再把参数式代入平面方程解出 t，回代即得交点。过点作平面的垂线时，因直线与平面垂直时方向向量与法向量平行，可直接取平面法向量作为垂线的方向向量，写出点向式后化为参数式，代入平面方程解出参数即得垂足。求投影点（垂足）的题可转化为「以平面法向量为方向向量、过已知点的直线与平面的交点」。这是直线与平面部分最可能出大题的类型。
- **关键概念**：`点向式方程`、`参数式方程`、`法向量`、`垂足`、`联立求交点`
- **相互关系**：两问方法一致，只是向量来源不同。
- **出处**：[陈哥 P85](https://www.bilibili.com/video/BV1husGzwEtZ?p=85)；[杰哥 P111](https://www.bilibili.com/video/BV1Up4y1Y76a?p=111)

### 位置关系题的通用解法（画图—标向量—叉乘）
- **要点**：求平面或直线方程的大题只有两步：先按题干画出所求对象与已知平面/直线的空间位置图，理清谁与谁平行、谁与谁垂直；再由位置关系确定向量关系，缺的向量用叉乘补出。求直线需「一点 + 方向向量 S」，求平面需「一点 + 法向量 N」。
- **关键概念**：`方向向量 S`、`法向量 N`、`叉乘`、`三阶行列式`
- **相互关系**：线线垂直 ⇔ 方向向量垂直，线面平行 ⇔ S⊥N，面面垂直 ⇔ 两法向量垂直。易错点：空间图中看似垂直的关系必须靠向量判断，不能凭图。
- **出处**：[陈哥 P85](https://www.bilibili.com/video/BV1husGzwEtZ?p=85)

### 综合题型套路
- **要点**：过一点且与已知平面垂直的直线，方向向量取平面法向量；与两平面平行的直线取两法向量叉乘；与已知直线垂直的平面，法向量取该直线方向向量。
- **关键概念**：`叉乘求方向向量`
- **出处**：[米哥 P96](https://www.bilibili.com/video/BV1swAWerEzS?p=96)、[P98](https://www.bilibili.com/video/BV1swAWerEzS?p=98)


### 向量的概念、表示与相等
- **要点**：既有大小又有方向的量称向量，又称矢量，力、位移都是向量。用两个字母表示时写作 $\vec{AB}$，前一字母是起点、后一字母是终点；也可用一个字母如 $\vec a$、$\vec F$ 表示，书写时必须加箭头。大小相等且方向相同的两个向量相等，与所在位置无关。
- **关键概念**：`向量`、`矢量`、`$\vec{AB}$`、`起点与终点`、`相等向量`
- **相互关系**：向量只有大小与方向两个要素，因此向量可以自由平移，这是「起点平移到同一点」定义夹角、以及后面加减法作图的前提。
- **出处**：[石头 P57](https://www.bilibili.com/video/BV18CL26WEJ3?p=57)

### 向量的模、单位向量与零向量
- **要点**：向量的模 $|\vec a|$ 就是向量的大小（长度）。模等于 $1$ 的向量称单位向量；模等于 $0$ 的向量称零向量，其方向是任意的而不是没有方向。与 $\vec a$ 同方向的单位向量为 $\vec e_a=\frac{\vec a}{|\vec a|}$，即把向量除以它自己的模。
- **关键概念**：`向量的模 $|\vec a|$`、`单位向量`、`零向量`、`$\vec e_a=\frac{\vec a}{|\vec a|}$`
- **相互关系**：零向量方向任意这一规定正是「零向量平行于任意向量」的前提；单位向量在方向余弦与投影中还会反复用到。
- **出处**：[石头 P57](https://www.bilibili.com/video/BV18CL26WEJ3?p=57)

### 向量的加减法及其运算律
- **要点**：加法有两种作图法：两向量首尾相接时用三角形法则，起点重合时用平行四边形法则，对角线即和向量。$\vec{AB}+\vec{BC}=\vec{AC}$（尾首相连、首尾连、方向指向后），$\vec{AB}-\vec{AC}=\vec{CB}$（首首相连、尾尾连、方向指向前）。运算满足交换律 $\vec a+\vec b=\vec b+\vec a$、结合律 $(\vec a+\vec b)+\vec c=\vec a+(\vec b+\vec c)$，且 $\vec a-\vec b=\vec a+(-\vec b)$。
- **关键概念**：`三角形法则`、`平行四边形法则`、`$\vec{AB}+\vec{BC}=\vec{AC}$`、`交换律`、`结合律`
- **相互关系**：加减法与物理中的受力分析一致；多个向量首尾相接时可直接连写，如 $\vec{AB}+\vec{BC}+\vec{CD}+\vec{DE}=\vec{AE}$，中间字母全部消去。减法不必单记，一律化成加法处理。
- **出处**：[石头 P57](https://www.bilibili.com/video/BV18CL26WEJ3?p=57)

### 向量与数的乘积及平行的充要条件
- **要点**：实数 $\lambda$ 与向量 $\vec a$ 的乘积 $\lambda\vec a$ 仍是向量：$\lambda>0$ 时方向相同、$\lambda&lt;0$ 时方向相反，大小为 $|\lambda|\,|\vec a|$；$\lambda=0$ 时得零向量。非零向量 $\vec b$ 平行于 $\vec a$ 的充要条件是存在唯一实数 $\lambda$ 使 $\vec b=\lambda\vec a$。数乘满足 $\lambda(\mu\vec a)=(\lambda\mu)\vec a$、$(\lambda+\mu)\vec a=\lambda\vec a+\mu\vec a$、$\lambda(\vec a+\vec b)=\lambda\vec a+\lambda\vec b$。
- **关键概念**：`$\lambda\vec a$`、`平行的充要条件`、`$\vec b=\lambda\vec a$`、`零向量平行于任意向量`
- **相互关系**：$\lambda>0$ 是同向平行、$\lambda&lt;0$ 是反向平行，两种都算平行；平行关系是后续判断两向量共线的基础，也是把向量分解到坐标轴上的依据。
- **出处**：[石头 P57](https://www.bilibili.com/video/BV18CL26WEJ3?p=57)

### 空间直角坐标系与八个卦限
- **要点**：在 $x$ 轴、$y$ 轴的基础上再增加一条与二者都垂直的 $z$ 轴，即得空间直角坐标系，三条坐标轴互相垂直，原点 $O$ 的三个坐标均为零。沿 $x$、$y$、$z$ 轴正方向的三个单位向量习惯记作 $\vec i$、$\vec j$、$\vec k$。每两个坐标轴确定一个坐标面：$xOy$ 面上 $z=0$，$yOz$ 面上 $x=0$，$zOx$ 面上 $y=0$。
- **关键概念**：`空间直角坐标系`、`$\vec i,\vec j,\vec k$`、`三个坐标面`、`八个卦限`、`第一卦限`
- **相互关系**：三个坐标面把空间分成八个卦限（对应平面的四个象限），第一卦限内三个坐标全为正；考试常把「某点在第二卦限」作为已知条件，隐含 $y>0$、$z>0$、$x&lt;0$ 的符号信息。
- **出处**：[石头 P58](https://www.bilibili.com/video/BV18CL26WEJ3?p=58)

### 向量的坐标分解式与坐标表示
- **要点**：以向量 $\vec{OM}$ 为对角线、三条坐标轴为棱作长方体，由首尾相连的加法得 $\vec{OM}=\vec{OP}+\vec{OQ}+\vec{OR}$，即把向量分解到三个坐标轴上。再由平行充要条件写成 $\vec{OM}=x\vec i+y\vec j+z\vec k$，简记为 $\vec{OM}=(x,y,z)$，这就是向量的坐标分解式。
- **关键概念**：`坐标分解式`、`$\vec r=x\vec i+y\vec j+z\vec k$`、`$(x,y,z)$`、`分向量`
- **相互关系**：$(x,y,z)$ 既可表示点 $M$ 的坐标，也可表示从原点出发的向量 $\vec{OM}$，二者形式相同、含义由上下文区分；分解思想与物理中把力分解到水平、竖直方向完全一致。
- **出处**：[石头 P58](https://www.bilibili.com/video/BV18CL26WEJ3?p=58)

### 坐标形式下的线性运算
- **要点**：设 $\vec a=(a_x,a_y,a_z)$、$\vec b=(b_x,b_y,b_z)$，则 $\vec a+\vec b=(a_x+b_x,\ a_y+b_y,\ a_z+b_z)$，$\vec a-\vec b=(a_x-b_x,\ a_y-b_y,\ a_z-b_z)$，$\lambda\vec a=(\lambda a_x,\lambda a_y,\lambda a_z)$，即对应坐标分别相加、相减、相乘。
- **关键概念**：`坐标形式的加法`、`坐标形式的减法`、`数乘`
- **相互关系**：运算结果仍是向量，若算得 $(0,0,0)$ 必须写成零向量或坐标形式，直接写数字 $0$ 是错的；平行条件 $\vec b=\lambda\vec a$ 在坐标形式下就是对应坐标成比例。
- **出处**：[石头 P58](https://www.bilibili.com/video/BV18CL26WEJ3?p=58)

### 向量的模与两点间距离公式
- **要点**：由分解式与勾股定理得 $\vec r=(x,y,z)$ 的模 $|\vec r|=\sqrt{x^2+y^2+z^2}$。对任意两点 $A(x_1,y_1,z_1)$、$B(x_2,y_2,z_2)$，$\vec{AB}=(x_2-x_1,\ y_2-y_1,\ z_2-z_1)$，故两点距离 $|\vec{AB}|=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2+(z_2-z_1)^2}$。
- **关键概念**：`$|\vec r|=\sqrt{x^2+y^2+z^2}$`、`两点间距离公式`、`$\vec{AB}=\vec{OB}-\vec{OA}$`
- **相互关系**：$\vec{AB}$ 由终点坐标减起点坐标得到，可由 $\vec{OB}-\vec{OA}$ 的减法法则（首首相连、尾尾连、方向指向前）解释；从原点出发的模公式只是两点距离公式在 $A=O(0,0,0)$ 时的特例，记一个即可。
- **出处**：[石头 P59](https://www.bilibili.com/video/BV18CL26WEJ3?p=59)

### 向量在轴上的投影
- **要点**：把 $x=|\vec r|\cos\alpha$、$y=|\vec r|\cos\beta$、$z=|\vec r|\cos\gamma$ 定义为 $\vec r$ 在三条坐标轴上的投影，记作 $\mathrm{prj}_x\vec r$、$\mathrm{prj}_y\vec r$、$\mathrm{prj}_z\vec r$（$\mathrm{prj}$ 是 projection 的缩写），几何上就是向量在轴上投下的影子长度。投影不是向量，也不是长度，它只是一个可正、可负、可为零的数值。
- **关键概念**：`投影`、`$\mathrm{prj}_x\vec r=|\vec r|\cos\alpha$`、`投影是数值`、`projection`
- **相互关系**：投影与坐标的关系是 $\mathrm{prj}_x\vec r=x$、$\mathrm{prj}_y\vec r=y$、$\mathrm{prj}_z\vec r=z$，因此已知三个投影就等于已知向量的坐标，可直接得点坐标或反解起点坐标；方向角为钝角时投影取负值，正午太阳当顶时投影为零。
- **出处**：[石头 P59](https://www.bilibili.com/video/BV18CL26WEJ3?p=59)

### 数量积的定义
- **要点**：两个向量的数量积等于它们模的乘积再乘以夹角余弦，即 $\vec a\cdot\vec b=|\vec a||\vec b|\cos\theta$，记作 $\vec a\cdot\vec b$（中间是一个点）。它的原型是恒力做功 $W=|\vec F||\vec s|\cos\theta$：只有沿位移方向的那部分力才真正做功。因为 $|\vec a|$、$|\vec b|$、$\cos\theta$ 都是数，所以点乘的结果是一个数，这才叫「数量积」。
- **关键概念**：`数量积`、`点乘`、`$\vec a\cdot\vec b=|\vec a||\vec b|\cos\theta$`、`$W=|\vec F||\vec s|\cos\theta$`
- **相互关系**：点乘的符号不能写成叉号，$\vec a\cdot\vec b$ 与 $\vec a\times\vec b$ 是两种完全不同的运算；只有数字与数字之间的乘号写点或写叉才没有区别。
- **出处**：[石头 P60](https://www.bilibili.com/video/BV18CL26WEJ3?p=60)

### 数量积的坐标表达式
- **要点**：设 $\vec a=(a_x,a_y,a_z)$、$\vec b=(b_x,b_y,b_z)$，则 $\vec a\cdot\vec b=a_xb_x+a_yb_y+a_zb_z$，即同名坐标分别相乘再相加。题目给出坐标形式时求数量积一律用这个公式，比用模与夹角更快。
- **关键概念**：`坐标表达式`、`$a_xb_x+a_yb_y+a_zb_z$`
- **相互关系**：与模长公式 $|\vec a|=\sqrt{a_x^2+a_y^2+a_z^2}$ 配合，就构成求夹角余弦的完整工具；数量积满足交换律、分配律与结合律，且 $\vec a\cdot\vec a=|\vec a|^2$。
- **出处**：[石头 P60](https://www.bilibili.com/video/BV18CL26WEJ3?p=60)

### 求两向量的夹角
- **要点**：由定义式反解得 $\cos\theta=\dfrac{\vec a\cdot\vec b}{|\vec a||\vec b|}$，先用坐标式求分子，再用模长公式求分母，最后按特殊角写出 $\theta$。若算出 $\cos\theta=0$ 则 $\theta=\frac{\pi}{2}$，算出 $\cos\theta=\frac12$ 则 $\theta=\frac{\pi}{3}$。
- **关键概念**：`夹角余弦公式`、`$\cos\theta=\frac{\vec a\cdot\vec b}{|\vec a||\vec b|}$`、`特殊角反查`
- **相互关系**：三角形中求内角（如 $\angle ABC$）时，先把它翻译成两个向量 $\overrightarrow{BA}$ 与 $\overrightarrow{BC}$ 的夹角，其中向量用「终点坐标减起点坐标」得到。
- **出处**：[石头 P60](https://www.bilibili.com/video/BV18CL26WEJ3?p=60)

### 求投影
- **要点**：$\vec a$ 在 $\vec b$ 上的投影等于 $|\vec a|\cos\theta$，也就是 $\dfrac{\vec a\cdot\vec b}{|\vec b|}$，口诀是「在谁上投影就除以谁的模」。$\vec b$ 在 $\vec a$ 上的投影则为 $\dfrac{\vec a\cdot\vec b}{|\vec a|}$。
- **关键概念**：`投影`、`$\mathrm{Prj}_{\vec b}\vec a=\frac{\vec a\cdot\vec b}{|\vec b|}$`、`在谁上投影除以谁的模`
- **相互关系**：最易错的是把两个投影写反，务必先看清「谁在谁上」；数量积定义式也可改写成「一个向量的模乘以另一个向量在它方向上的投影」。
- **出处**：[石头 P60](https://www.bilibili.com/video/BV18CL26WEJ3?p=60)

### 向量积的定义与右手法则
- **要点**：两个向量叉乘的结果仍是一个向量，其模为 $|\vec a\times\vec b|=|\vec a||\vec b|\sin\theta$，方向由右手法则确定：右手四指从第一个向量以不超过 $\pi$ 的角度转向第二个向量，大拇指所指即为结果向量的方向。该向量同时垂直于 $\vec a$ 与 $\vec b$，即垂直于两者所在的平面。
- **关键概念**：`向量积`、`叉乘`、`$|\vec a\times\vec b|=|\vec a||\vec b|\sin\theta$`、`右手法则`
- **相互关系**：与数量积对照记忆——点乘取 $\cos\theta$ 得数，叉乘取 $\sin\theta$ 得向量；转向必须从前者转到后者，转反就错。
- **出处**：[石头 P61](https://www.bilibili.com/video/BV18CL26WEJ3?p=61)

### 反交换律与向量积的性质
- **要点**：$\vec a\times\vec b=-\vec b\times\vec a$，大小相同、方向相反，这是向量积最需要记牢的一条性质。此外 $\vec a\times\vec a=\vec 0$；两个非零向量平行（同向或反向）时 $\vec a\times\vec b=\vec 0$，反之叉乘为零向量也能推出两向量平行；分配律与结合律则与普通运算一致。
- **关键概念**：`反交换律`、`$\vec a\times\vec b=-\vec b\times\vec a$`、`平行 $\Leftrightarrow$ 叉乘为零向量`
- **相互关系**：由 $\sin0=\sin\pi=0$ 可推出平行时叉乘为零向量，而 $\vec a\times\vec a=\vec 0$ 正是「平行」中的特例；用坐标式分别算 $\vec a\times\vec b$ 与 $\vec b\times\vec a$ 只差一个负号，可用来验证反交换律。
- **出处**：[石头 P61](https://www.bilibili.com/video/BV18CL26WEJ3?p=61)

### 向量积的坐标表达式
- **要点**：把 $\vec a=a_x\vec i+a_y\vec j+a_z\vec k$、$\vec b=b_x\vec i+b_y\vec j+b_z\vec k$ 展开，利用 $\vec i\times\vec j=\vec k$、$\vec j\times\vec k=\vec i$、$\vec k\times\vec i=\vec j$ 化简，可得 $\vec a\times\vec b=\begin{vmatrix}\vec i&\vec j&\vec k\\a_x&a_y&a_z\\b_x&b_y&b_z\end{vmatrix}$。按第一行展开：把每个基向量所在的行与列划掉，剩下四个数交叉相乘再相减，注意中间 $\vec j$ 那一项前面带负号。
- **关键概念**：`三阶行列式`、`$\vec i\times\vec j=\vec k$`、`中间项取负号`
- **相互关系**：把叉乘写成行列式后，交换两行行列式变号，正好对应反交换律；计算时先写出行列式框架再逐项填空，可避免符号出错。
- **出处**：[石头 P61](https://www.bilibili.com/video/BV18CL26WEJ3?p=61)

### 向量积的模的几何意义
- **要点**：$|\vec a\times\vec b|$ 等于以 $\vec a$、$\vec b$ 为邻边的平行四边形的面积（底乘高，高为 $|\vec b|\sin\theta$），因而以两向量为邻边的三角形面积等于 $\frac12|\vec a\times\vec b|$。求三角形面积的三步：先取相邻两边构成的向量，再求这两个向量的叉乘的模，最后除以 2。
- **关键概念**：`平行四边形面积`、`三角形面积`、`$\frac12|\vec a\times\vec b|$`
- **相互关系**：取向量时用「大数减小数」可避免出现负坐标、减少算错；用 $\overrightarrow{BA}$、$\overrightarrow{BC}$ 或 $\overrightarrow{AB}$、$\overrightarrow{AC}$ 算出的面积相同。
- **出处**：[石头 P61](https://www.bilibili.com/video/BV18CL26WEJ3?p=61)

### 向量平行的充要条件
- **要点**：两个非零向量平行时夹角只能是 $0$ 或 $\pi$（同向或反向）。充要条件是存在唯一实数 $\lambda$ 使 $\vec a=\lambda\vec b$，写成坐标即 $\frac{a_x}{b_x}=\frac{a_y}{b_y}=\frac{a_z}{b_z}=\lambda$（$\lambda$ 可正、可负、可为零）；等价地也有 $\vec a\times\vec b=\vec 0$。另外务必记住零向量平行于任意向量。
- **关键概念**：`向量平行`、`$\vec a=\lambda\vec b$`、`坐标成比例`、`$\vec a\times\vec b=\vec 0$`
- **相互关系**：平行的四条结论要与垂直的两条对照记忆；已知平行求未知参数时，用「坐标成比例」列等式最方便。
- **出处**：[石头 P62](https://www.bilibili.com/video/BV18CL26WEJ3?p=62)

### 向量垂直的充要条件
- **要点**：两个向量垂直时夹角为 $\frac{\pi}{2}$，充要条件是数量积为零，即 $\vec a\cdot\vec b=0$，坐标形式为 $a_xb_x+a_yb_y+a_zb_z=0$。注意这里的零是数字零，而平行条件里的零是零向量。
- **关键概念**：`向量垂直`、`$\vec a\cdot\vec b=0$`、`$a_xb_x+a_yb_y+a_zb_z=0$`
- **相互关系**：判断两向量关系时先看是否成比例（平行），再看数量积是否为零（垂直）；「零向量与任意向量垂直」不成立。
- **出处**：[石头 P62](https://www.bilibili.com/video/BV18CL26WEJ3?p=62)

### 平行与垂直的常见题型
- **要点**：求与已知向量垂直的单位向量，要同时满足「在指定平面内」「与已知向量垂直」「模长为 1」三个条件，先设坐标，再用数量积为零与模长等于 1 联立，开方后正负两个解都要保留。求与已知向量平行的单位向量，先写成 $\lambda\vec a$，再由 $|\lambda\vec a|=1$ 得 $\lambda=\pm\frac{1}{|\vec a|}$。已知平行或垂直关系求参数，直接套成比例或数量积为零即可。
- **关键概念**：`单位向量`、`$\pm\frac{1}{|\vec a|}\vec a$`、`开方取正负`
- **相互关系**：含叉乘的式子（如 $(\vec a+\vec b)\times(\vec a-\vec b)$）展开时 $\vec a\times\vec a$、$\vec b\times\vec b$ 都是零向量可去掉，剩下的 $-\vec a\times\vec b+\vec b\times\vec a$ 由反交换律等于 $2\vec b\times\vec a$，绝不能当成零。
- **出处**：[石头 P62](https://www.bilibili.com/video/BV18CL26WEJ3?p=62)

### 平面的法线向量与点法式方程
- **要点**：垂直于平面的非零向量叫该平面的法线向量，一个平面的法线向量有无穷多条，它们彼此平行（同向或反向）。已知平面上一点 $M_0(x_0,y_0,z_0)$ 与法向量 $\vec n=(A,B,C)$，即得点法式方程 $A(x-x_0)+B(y-y_0)+C(z-z_0)=0$。
- **关键概念**：`法线向量`、`点法式方程`、`$A(x-x_0)+B(y-y_0)+C(z-z_0)=0$`
- **相互关系**：点法式与直线的点向式对照记忆：平面用「点＋法向量」，直线用「点＋方向向量」；法向量垂直于平面，方向向量平行于直线。
- **出处**：[石头 P63](https://www.bilibili.com/video/BV18CL26WEJ3?p=63)

### 平面的一般式方程
- **要点**：把点法式展开，令常数项为 $D$，得一般式 $Ax+By+Cz+D=0$，其中 $(A,B,C)$ 仍是法向量。特殊情况归纳为两句口诀：经过原点则没有常数项 $D$；平行于哪个坐标轴则方程中不含哪个自变量（$C=0$ 平行于 $z$ 轴，$A=0$ 平行于 $x$ 轴，$B=0$ 平行于 $y$ 轴）。经过某轴则两条同时成立，如 $C=D=0$ 表示平面经过 $z$ 轴，$A=B=0$ 表示平面平行于 $xOy$ 面。
- **关键概念**：`一般式方程`、`$Ax+By+Cz+D=0$`、`经过原点则没常数`、`平行于哪个轴则没哪个自变量`
- **相互关系**：一般式的十条特殊情况不必死记，由口诀即可推出；求过某轴或平行于某轴的平面时，先按口诀设出缺项的一般式，再代点求解。
- **出处**：[石头 P63](https://www.bilibili.com/video/BV18CL26WEJ3?p=63)

### 平面的截距式方程
- **要点**：若平面在 $x$、$y$、$z$ 三轴上的截距分别为 $a$、$b$、$c$（均不为零），则方程为 $\frac xa+\frac yb+\frac zc=1$，注意右边是 $1$ 而不是 $0$。小写 $a,b,c$ 表示截距，大写 $A,B,C$ 表示法向量的分量，两者不要混淆。
- **关键概念**：`截距式方程`、`$\frac xa+\frac yb+\frac zc=1$`、`截距`
- **相互关系**：把截距式化为一般式 $\frac1a x+\frac1b y+\frac1c z-1=0$，即可看出法向量为 $\left(\frac1a,\frac1b,\frac1c\right)$、常数项为 $-1$；考试时若时间允许，建议把结果化成一般式。
- **出处**：[石头 P63](https://www.bilibili.com/video/BV18CL26WEJ3?p=63)

### 平行与重合的充要条件
- **要点**：两平面 $\pi_1:A_1x+B_1y+C_1z+D_1=0$、$\pi_2:A_2x+B_2y+C_2z+D_2=0$ 平行或重合时法向量必平行，即 $\frac{A_1}{A_2}=\frac{B_1}{B_2}=\frac{C_1}{C_2}$。再比较常数项：系数比与 $\frac{D_1}{D_2}$ 不相等时两平面平行但不重合；系数比与 $\frac{D_1}{D_2}$ 全部相等时两平面重合，此时两方程化简后完全相同。
- **关键概念**：`法向量成比例`、`$\frac{A_1}{A_2}=\frac{B_1}{B_2}=\frac{C_1}{C_2}$`、`$\frac{D_1}{D_2}$ 不成比例`
- **相互关系**：判断位置关系的第一步永远是把两平面的法向量写出来，再比成比例关系；只要系数比中有一个不成立，两平面就必然相交。
- **出处**：[石头 P64](https://www.bilibili.com/video/BV18CL26WEJ3?p=64)

### 两平面的夹角
- **要点**：两平面的夹角规定取锐角或直角，即 $\theta\in\left(0,\frac{\pi}{2}\right]$，它等于两法向量的夹角或其补角。公式为 $\cos\theta=\dfrac{|A_1A_2+B_1B_2+C_1C_2|}{\sqrt{A_1^2+B_1^2+C_1^2}\sqrt{A_2^2+B_2^2+C_2^2}}$，分子必须加绝对值以保证结果非负，再由 $\theta=\arccos(\cdot)$ 写出答案。
- **关键概念**：`两平面夹角`、`$\cos\theta=\frac{|\vec n_1\cdot\vec n_2|}{|\vec n_1||\vec n_2|}$`、`分子加绝对值`
- **相互关系**：漏写绝对值会得到钝角而失分；当 $\cos\theta=0$ 时夹角为 $\frac{\pi}{2}$，正好对应两平面垂直。
- **出处**：[石头 P64](https://www.bilibili.com/video/BV18CL26WEJ3?p=64)

### 两平面垂直的充要条件
- **要点**：两平面垂直即夹角为 $\frac{\pi}{2}$，等价于两法向量垂直，充要条件是 $A_1A_2+B_1B_2+C_1C_2=0$。
- **关键概念**：`两平面垂直`、`$A_1A_2+B_1B_2+C_1C_2=0$`
- **相互关系**：判断两平面位置关系的完整流程是：先求两法向量，看是否成比例——成比例再比常数项定平行或重合；不成比例再求数量积，为零则垂直，不为零则一般相交。
- **出处**：[石头 P64](https://www.bilibili.com/video/BV18CL26WEJ3?p=64)

### 方向向量与点向式方程
- **要点**：平行于直线的非零向量叫直线的方向向量，通常记作 $\vec s=(m,n,p)$。已知直线上一点 $M_0(x_0,y_0,z_0)$ 与方向向量 $\vec s$，即得点向式方程 $\frac{x-x_0}{m}=\frac{y-y_0}{n}=\frac{z-z_0}{p}$，它又称标准式、对称式。
- **关键概念**：`方向向量`、`点向式方程`、`$\frac{x-x_0}{m}=\frac{y-y_0}{n}=\frac{z-z_0}{p}$`
- **相互关系**：点向式与平面的点法式对照记忆，法向量垂直于平面、方向向量平行于直线；分母允许为零，某个分母为零就表示直线上该坐标恒为定值。
- **出处**：[石头 P65](https://www.bilibili.com/video/BV18CL26WEJ3?p=65)

### 一般式方程及其方向向量的求法
- **要点**：直线的一般式（交面式）方程是两个平面方程联立的方程组 $\begin{cases}A_1x+B_1y+C_1z+D_1=0\\A_2x+B_2y+C_2z+D_2=0\end{cases}$，表示两平面的交线。由于过同一条直线的平面有无穷多个，一般式的表示不唯一。求该直线的方向向量时，取两平面的法向量 $\vec n_1$、$\vec n_2$，令 $\vec s=\vec n_1\times\vec n_2$ 即可。
- **关键概念**：`一般式方程`、`交面式`、`$\vec s=\vec n_1\times\vec n_2$`
- **相互关系**：这一步把一般式与点向式联系起来，也是判断两直线关系、直线与平面关系时的关键技巧；方向向量乘任意非零常数仍是同一条直线的方向向量。
- **出处**：[石头 P65](https://www.bilibili.com/video/BV18CL26WEJ3?p=65)

### 参数式方程与直线和平面的交点
- **要点**：令点向式中的连比等于 $t$，反解出 $x=x_0+mt$、$y=y_0+nt$、$z=z_0+pt$，即得参数式方程（准确说是参数方程组）。求直线与平面的交点时，把参数式代入平面方程，得到一个关于 $t$ 的一元方程，解出 $t$ 后再回代即得交点坐标。
- **关键概念**：`参数式方程`、`$x=x_0+mt$`、`联立求交点`
- **相互关系**：分母为零时由 $0\cdot t=0$ 可知相应坐标仍为常数，这正是参数式的便利之处；两点式方程 $\frac{x-x_1}{x_2-x_1}=\frac{y-y_1}{y_2-y_1}=\frac{z-z_1}{z_2-z_1}$ 只需了解，考得较少。
- **出处**：[石头 P65](https://www.bilibili.com/video/BV18CL26WEJ3?p=65)

### 平行或重合的条件
- **要点**：两直线平行或重合，等价于它们的方向向量平行，即 $\frac{m_1}{m_2}=\frac{n_1}{n_2}=\frac{p_1}{p_2}$。
- **关键概念**：`方向向量平行`、`$\frac{m_1}{m_2}=\frac{n_1}{n_2}=\frac{p_1}{p_2}$`
- **相互关系**：空间中两直线垂直不一定相交，可能异面垂直；相交也不一定垂直，因此垂直与相交要分开判断。
- **出处**：[石头 P66](https://www.bilibili.com/video/BV18CL26WEJ3?p=66)

### 垂直的条件
- **要点**：两直线垂直等价于方向向量垂直，充要条件为 $m_1m_2+n_1n_2+p_1p_2=0$。
- **关键概念**：`方向向量垂直`、`$m_1m_2+n_1n_2+p_1p_2=0$`
- **相互关系**：若直线给的是参数方程，可直接把 $t$ 前面的三个系数抄下来作为方向向量（前提是 $x,y,z$ 前没有别的系数）；若给的是一般式方程，则先由两个法向量叉乘求出方向向量。
- **出处**：[石头 P66](https://www.bilibili.com/video/BV18CL26WEJ3?p=66)

### 两直线的夹角
- **要点**：两直线的夹角取锐角或直角，等于两方向向量的夹角或其补角，公式为 $\cos\theta=\dfrac{|m_1m_2+n_1n_2+p_1p_2|}{\sqrt{m_1^2+n_1^2+p_1^2}\sqrt{m_2^2+n_2^2+p_2^2}}$，分子加绝对值，最后 $\theta=\arccos(\cdot)$。
- **关键概念**：`两直线夹角`、`$\cos\theta=\frac{|\vec s_1\cdot\vec s_2|}{|\vec s_1||\vec s_2|}$`
- **相互关系**：求夹角前必须先找到两直线的方向向量，一般式方程要先做叉乘；题目已知平行或垂直时，直接套对应条件解参数即可。
- **出处**：[石头 P66](https://www.bilibili.com/video/BV18CL26WEJ3?p=66)

### 直线与平面的四种位置关系及判定
- **要点**：直线与平面共有四种位置关系：直线在平面上、直线与平面平行、直线与平面垂直、直线与平面斜交。判定用直线的方向向量 $\vec s$ 与平面的法向量 $\vec n$：直线在平面上要求 $\vec s\cdot\vec n=0$ 且直线上一点满足平面方程；直线与平面平行要求 $\vec s\cdot\vec n=0$ 且直线上一点不满足平面方程；直线与平面垂直要求 $\vec s$ 与 $\vec n$ 平行，即 $\frac Am=\frac Bn=\frac Cp$。
- **关键概念**：`$\vec s\cdot\vec n=0$`、`$\vec s\parallel\vec n$`、`直线在平面上`
- **相互关系**：「在平面上」与「平行」只差一个条件——把直线上那个已知点代入平面方程，成立即在平面上，不成立即平行；这里「垂直对应平行、平行对应垂直」极易记混。
- **出处**：[石头 P67](https://www.bilibili.com/video/BV18CL26WEJ3?p=67)

### 直线与平面的夹角
- **要点**：直线与平面的夹角 $\theta$ 取锐角或直角，它与 $\vec s$、$\vec n$ 的夹角 $\alpha$ 互余，因此 $\sin\theta=\dfrac{|\vec s\cdot\vec n|}{|\vec s||\vec n|}$，分子要加绝对值，最后 $\theta=\arcsin(\cdot)$。
- **关键概念**：`直线与平面的夹角`、`$\sin\theta=\frac{|\vec s\cdot\vec n|}{|\vec s||\vec n|}$`、`$\theta=\arcsin(\cdot)$`
- **相互关系**：三种夹角要对照记忆——直线与直线、平面与平面求夹角的余弦，直线与平面求夹角的正弦，弄混正余弦是最常见的失分点。
- **出处**：[石头 P67](https://www.bilibili.com/video/BV18CL26WEJ3?p=67)

### 点到平面的距离与两平行平面间的距离
- **要点**：点 $P_0(x_0,y_0,z_0)$ 到平面 $Ax+By+Cz+D=0$ 的距离为 $d=\dfrac{|Ax_0+By_0+Cz_0+D|}{\sqrt{A^2+B^2+C^2}}$，即把点代入平面方程取绝对值作分子、法向量模长作分母。两平行平面 $Ax+By+Cz+D_1=0$ 与 $Ax+By+Cz+D_2=0$ 之间的距离为 $d=\dfrac{|D_1-D_2|}{\sqrt{A^2+B^2+C^2}}$。
- **关键概念**：`点到平面的距离`、`$d=\frac{|Ax_0+By_0+Cz_0+D|}{\sqrt{A^2+B^2+C^2}}$`、`$d=\frac{|D_1-D_2|}{\sqrt{A^2+B^2+C^2}}$`
- **相互关系**：用两平行平面距离公式前必须先把两方程的 $A,B,C$ 化为完全相同的系数；点 $(x_0,y_0,z_0)$ 到 $xOy$ 面、$yOz$ 面、$zOx$ 面的距离分别是 $|z_0|$、$|x_0|$、$|y_0|$（三面方程分别为 $z=0$、$x=0$、$y=0$）。
- **出处**：[石头 P68](https://www.bilibili.com/video/BV18CL26WEJ3?p=68)


## 八、多元函数微分学


### 多元函数的概念与定义域
- **要点**：二元函数 z=f(x,y) 是在一元函数基础上多一个自变量：x,y 为自变量（定义域），z 为因变量（值域），f 为对应关系（映射）；自变量个数即元数，超过两个统称多元函数（两个变量确定的是二元函数，三个变量确定的是三元函数）。定义域写 D={(x,y)|…}，条件为联立不等式组（分母非零、根号内非负、真数为正、反三角函数内部绝对值 ≤1），多个限制条件共同决定定义域；不能用区间表示，几何上是一个平面区域（点集）；严格不等号时边界不在集合内，画图用虚线。
- **关键概念**：`z=f(x,y)`、`自变量`、`因变量`、`映射`、`平面点集`、`定义域 D`、`积分区域`
- **相互关系**：与一元函数类比：一元函数定义域是数集，二元函数定义域是点集；与一元函数定义域规则一致，只是从区间变为区域，为二重积分作准备。
- **出处**：[陈哥 P87](https://www.bilibili.com/video/BV1husGzwEtZ?p=87)、[P88](https://www.bilibili.com/video/BV1husGzwEtZ?p=88)；[杰哥 P113](https://www.bilibili.com/video/BV1Up4y1Y76a?p=113)；[米哥 P99](https://www.bilibili.com/video/BV1swAWerEzS?p=99)；[ok姐 P96](https://www.bilibili.com/video/BV1vm421s7mv?p=96)

### 二元函数的图像
- **要点**：在空间直角坐标系中，定义域是 xOy 平面上的区域，所有点对应的函数值连成一张曲面，曲面上每点坐标为 (x,y,f(x,y))；若定义域是一条曲线，则对应图像是一条空间曲线。
- **关键概念**：`曲面`、`空间曲线`
- **出处**：[ok姐 P96](https://www.bilibili.com/video/BV1vm421s7mv?p=96)

### 二元函数求表达式
- **要点**：已知 f(x,y) 求复合函数直接代入；已知复合形式的表达式求 f(x,y) 用配方法或换元法：换元法先令两个括号分别为 u,v，反解出 x,y 用 u,v 表示，代回右端整理，最后把 u,v 换回 x,y；当换元后反解繁琐时改用配凑法——先对右端用完全平方、平方差公式因式分解并约分，凑出与括号相同的结构再换元（常见做法是把右侧式子凑成与括号内整体一致的形式，如用平方差公式分解为两式相乘）。属低频考点。
- **关键概念**：`换元法`、`配凑法`、`完全平方公式`、`平方差公式`、`整体思想`
- **相互关系**：自变量用什么字母不影响函数表达式；配凑法易错点是约分后剩余的是 x/y 还是 y/x。
- **出处**：[陈哥 P87](https://www.bilibili.com/video/BV1husGzwEtZ?p=87)；[杰哥 P114](https://www.bilibili.com/video/BV1Up4y1Y76a?p=114)；[米哥 P100](https://www.bilibili.com/video/BV1swAWerEzS?p=100)

### 二元函数的极限与方向性
- **要点**：二元极限要求 (x,y) 以任意方式（沿任意方向）趋近 (x₀,y₀) 时函数都趋近同一常数 A；与一元只有左右两个方向不同，二元从四面八方趋近，方向不确定。关键在「任意方式」：只要找到一种趋近方式使极限值不同，极限就不存在。计算时先代入定型，必要时用等价无穷小（把组合式如 x²+y²、xy 整体看成等价无穷小公式中的自变量，套用 1−cos□~□²/2、ln(1+□)~□、(1+α□)^β−1~αβ□ 等，再约分求值）。连续只需极限等于函数值，不能用洛必达。
- **关键概念**：`邻域`、`趋近路径`、`二重极限`、`等价无穷小`、`整体代换`
- **相互关系**：正因为方向不确定，一元函数的洛必达法则在二元极限中不适用；专升本二元极限九成靠等价无穷小。
- **出处**：[陈哥 P88](https://www.bilibili.com/video/BV1husGzwEtZ?p=88)；[杰哥 P115](https://www.bilibili.com/video/BV1Up4y1Y76a?p=115)；[米哥 P101](https://www.bilibili.com/video/BV1swAWerEzS?p=101)

### 路径法判定极限不存在
- **要点**：沿两条不同路径（常取直线 y=x、y=kx 与抛物线 y=x²）趋近同一点，若所得极限值不同，则原极限不存在。证明不存在取 y=kx 代入看是否随 k 变化。
- **关键概念**：`特殊路径`、`直线`、`抛物线`、`y=kx`、`极限不存在`
- **相互关系**：是真题中的高频难题型。
- **出处**：[陈哥 P88](https://www.bilibili.com/video/BV1husGzwEtZ?p=88)；[米哥 P101](https://www.bilibili.com/video/BV1swAWerEzS?p=101)

### 偏导数的定义与记号
- **要点**：二元函数有两个变量，求导须指明对谁求，「偏」即偏向某一变量。在 (x₀,y₀) 处对 x 的偏导数是固定 y=y₀ 后取的极限 lim\_\{x→x₀\}[f(x,y₀)−f(x₀,y₀)]/(x−x₀)，对 y 对称定义；定义式由一元导数定义式补上另一变量（如 y₀）得到。书写有四种：f′_x、z′_x、∂z/∂x、∂f/∂x（读作「z 对 x 的偏导」），右下角的下标必须写。形如 lim\_\{x→0\}[f(x,0)−f(0,0)]/x 的极限可直接识别为 f_x(0,0)。分段函数分界点的偏导须用定义求。
- **关键概念**：`偏导数`、`∂`、`z_x`、`f_x`、`视为常数`
- **相互关系**：特征与一元导数一致——分子为函数值之差、分母为对应自变量之差；概念与定义部分考纲多要求为了解，重点是计算；定义曾作为真题考点。
- **出处**：[陈哥 P89](https://www.bilibili.com/video/BV1husGzwEtZ?p=89)；[杰哥 P116](https://www.bilibili.com/video/BV1Up4y1Y76a?p=116)、[P117](https://www.bilibili.com/video/BV1Up4y1Y76a?p=117)；[米哥 P102](https://www.bilibili.com/video/BV1swAWerEzS?p=102)；[ok姐 P97](https://www.bilibili.com/video/BV1vm421s7mv?p=97)

### 一阶偏导数的求法
- **要点**：对 x 求偏导时把 y 看作常数（可想象替换为常数 A 再换回），对 y 求偏导时把 x 看作常数，之后完全沿用一元函数的求导法则（乘积、商、复合）；含被求导变量的项若不含该变量则导数为 0。求某点偏导先求偏导函数再代点。
- **关键概念**：`求导变量`、`常数化`、`乘法求导法则`、`偏导函数`
- **相互关系**：是整个多元微分学的核心方法，二阶偏导、复合函数与隐函数求导都建立在它之上。
- **出处**：[陈哥 P89](https://www.bilibili.com/video/BV1husGzwEtZ?p=89)；[杰哥 P116](https://www.bilibili.com/video/BV1Up4y1Y76a?p=116)、[P117](https://www.bilibili.com/video/BV1Up4y1Y76a?p=117)；[米哥 P102](https://www.bilibili.com/video/BV1swAWerEzS?p=102)；[ok姐 P98](https://www.bilibili.com/video/BV1vm421s7mv?p=98)

### 幂指函数的偏导
- **要点**：形如 z=x^y 或 z=y\^\{2x\} 的幂指函数：对 x 求偏导时底数 y 为常数，套 a^u 形式得 y\^\{2x\} ln y 再乘内层 2x 的导数 2（此 2 极易漏），也可先做指数对数化写成 z=e\^\{y ln x\}，再用复合函数求导得 z_x=y x\^\{y−1\}；对 y 求偏导时指数为常数，套 y^a 形式得 2x y\^\{2x−1\}（或 z_y=x^y ln x）。切勿整体当作幂指函数。
- **关键概念**：`幂指函数`、`指数对数化`、`e^{y ln x}`、`a^x 求导`、`x^a 求导`、`内层导数`
- **出处**：[陈哥 P89](https://www.bilibili.com/video/BV1husGzwEtZ?p=89)；[学士帽 P76](https://www.bilibili.com/video/BV1X4411J792?p=76)；[ok姐 P100](https://www.bilibili.com/video/BV1vm421s7mv?p=100)

### 「先代后求」求某点偏导
- **要点**：求 f_x(x₀,y₀) 时，因对 x 求导时 y 不参与运算，可先把 y=y₀ 代入函数化简，再对 x 求导，最后代 x=x₀；即代入非求导变量的值。易错点是不能把求导变量的值提前代入。
- **关键概念**：`先代后求`、`非求导变量`
- **出处**：[陈哥 P89](https://www.bilibili.com/video/BV1husGzwEtZ?p=89)

### 二阶偏导数与混合偏导相等
- **要点**：二阶偏导是在一阶偏导（仍是 x,y 的二元函数）基础上再求一次偏导，共四个 z\_\{xx\}, z\_\{xy\}, z\_\{yx\}, z\_\{yy\}；记号按求导先后写，∂²z/∂x∂y 表示先 x 后 y（分母中写在前的变量对应先求）。当二阶混合偏导连续时 z\_\{xy\}=z\_\{yx\}，专升本题目恒满足，故实际只有三个不同结果。每一步仍只关注求导变量、其余变量当常数。求偏导时把另一变量看作常数，逐次求导；对 x 求偏导且分子分母都含 x 时用除法法则，对 y 求偏导只有分母含 y 则不用。
- **关键概念**：`二阶偏导`、`z_{xy}`、`混合偏导`、`连续性`、`对称性`
- **相互关系**：利用 x、y 互换的对称性可直接写出另一个二阶偏导；结果常需同乘一因子去根式再整理；易错点是二元函数中 x,y 地位平等，不能写成「乘以内层导数」的一元复合形式。
- **出处**：[陈哥 P91](https://www.bilibili.com/video/BV1husGzwEtZ?p=91)；[杰哥 P121](https://www.bilibili.com/video/BV1Up4y1Y76a?p=121)；[米哥 P103](https://www.bilibili.com/video/BV1swAWerEzS?p=103)；[ok姐 P99](https://www.bilibili.com/video/BV1vm421s7mv?p=99)；[帆哥 P1](https://www.bilibili.com/video/BV1xxXZBKENv?p=1)

### 全微分
- **要点**：二元函数全微分 dz=z_x dx+z_y dy（∂z/∂x dx+∂z/∂y dy），即各偏导乘对应自变量微分再相加，是一元微分 dy=f′dx 的推广；三元函数 du=u_x dx+u_y dy+u_z dz。求某点全微分时先把点坐标代入两个偏导再乘 dx、dy；若方程中隐式含 z，需先由方程解出该点的 z。dx、dy 只当后缀理解、不需要计算，形式一定要对——偏导求对了但没抓上 dx、dy 不得分；常见错误是把两个偏导值直接相加。反之，若题给 dz=P dx+Q dy，则 P 即 ∂z/∂x、Q 即 ∂z/∂y（反读偏导，是常考变形）。
- **关键概念**：`全微分`、`dz`、`dx`、`dy`、`反读偏导`
- **相互关系**：与一元函数 dy=f′(x)dx 结构一致；与隐函数求导、空间曲线切向量共用「求偏导」这一步。
- **出处**：[陈哥 P90](https://www.bilibili.com/video/BV1husGzwEtZ?p=90)、[P93](https://www.bilibili.com/video/BV1husGzwEtZ?p=93)；[杰哥 P118](https://www.bilibili.com/video/BV1Up4y1Y76a?p=118)；[米哥 P104](https://www.bilibili.com/video/BV1swAWerEzS?p=104)；[学士帽 P79](https://www.bilibili.com/video/BV1X4411J792?p=79)、[P80](https://www.bilibili.com/video/BV1X4411J792?p=80)；[ok姐 P100](https://www.bilibili.com/video/BV1vm421s7mv?p=100)

### 可微、偏导存在与连续的关系
- **要点**：偏导连续 ⇒ 可微 ⇒ 连续、偏导存在，反之均不成立；一元可微与可导等价，多元不等价。仅「偏导存在」推不出可微，也推不出连续，因为偏导只保证 x 方向与 y 方向上的性质，其余方向的情况未知。这是选择题的高频陷阱，命题人常只给「偏导存在」而不给「连续」。
- **关键概念**：`可微`、`偏导存在`、`偏导连续`、`连续`
- **相互关系**：可微的实质是用该点处的切线（线性增量）近似代替曲线（全增量），前提是两者之差为自变量增量的高阶无穷小：一元情形 Δy−f′(x₀)Δx 是 Δx 的高阶无穷小；二元情形 Δz 与线性增量 AΔx+BΔy（A=∂z/∂x、B=∂z/∂y）之差是 √(Δx²+Δy²) 的高阶无穷小。
- **出处**：[杰哥 P119](https://www.bilibili.com/video/BV1Up4y1Y76a?p=119)、[P120](https://www.bilibili.com/video/BV1Up4y1Y76a?p=120)；[米哥 P105](https://www.bilibili.com/video/BV1swAWerEzS?p=105)

### 链式求导法则（多元复合）
- **要点**：z=f(u,v) 而 u,v 均为 x,y（或 t）的函数时，z 与 x,y 无直接联系，须经中间变量搭桥。画出链式结构图后 z_x=(∂z/∂u)(∂u/∂x)+(∂z/∂v)(∂v/∂x)，口诀「连线相乘，分线相加」（或「同链相乘，异链相加」）；u=u(t),v=v(t) 时 dz/dt=(∂z/∂u)(du/dt)+(∂z/∂v)(dv/dt)。若某中间变量只含一个自变量（如 v=v(x)），该处须写成一元导数 dv/dx 而非偏导；被求导变量与函数是一元关系用 d，多元关系用 ∂。使用前先画变量关系链，找出所有指向被求导变量的链再逐条相加；外层一元、内层二元的复合（如 f(4x²−y²)）用一元链式法则即可。
- **关键概念**：`链式求导法则`、`中间变量`、`结构图`、`树状图`、`连线相乘，分线相加`
- **相互关系**：是多元复合与隐函数求导的总纲；实际做题更推荐直接代入法或下标法，链式法则只需理解结构；外层含 x 的因子时先按乘积法则拆。
- **出处**：[陈哥 P92](https://www.bilibili.com/video/BV1husGzwEtZ?p=92)；[杰哥 P124](https://www.bilibili.com/video/BV1Up4y1Y76a?p=124)；[米哥 P108](https://www.bilibili.com/video/BV1swAWerEzS?p=108)；[ok姐 P100](https://www.bilibili.com/video/BV1vm421s7mv?p=100)、[P101](https://www.bilibili.com/video/BV1vm421s7mv?p=101)

### 具体复合函数的求导（直接代入法）
- **要点**：已知 x、y 关于 u、v 的具体表达式时，直接把 x、y 代入原式，化为 z 关于 u、v 的函数再求导，此法称直接代入法。注意外层为乘积时要使用乘法求导法则。
- **关键概念**：`直接代入法`、`乘法求导`
- **出处**：[杰哥 P125](https://www.bilibili.com/video/BV1Up4y1Y76a?p=125)

### 抽象复合函数的记号与一阶偏导
- **要点**：f 括号内第 i 个整体（逗号分隔）记作下标 i，对第 i 个部分求导记 f_i′；如 f(x²+y², xy) 有 z_x=f₁′·2x+f₂′·y。若两个位置都含所求变量，则两条路径相加，每条路径上依次相乘；最终结果中的括号内容可省略不写。抽象函数括号内的内容在求导中不变。也可先换元：令逗号前整体为 u、逗号后整体为 v，化为 z=f(u,v) 后用链式法则求导，结果用 f_u,f_v 表示，换元步骤须写在卷面上。
- **关键概念**：`抽象函数`、`f₁′`、`f₂′`、`一阶偏导`、`位置下标`、`换元`
- **相互关系**：一阶偏导是专升本必考题型。
- **出处**：[陈哥 P92](https://www.bilibili.com/video/BV1husGzwEtZ?p=92)；[杰哥 P126](https://www.bilibili.com/video/BV1Up4y1Y76a?p=126)；[ok姐 P101](https://www.bilibili.com/video/BV1vm421s7mv?p=101)

### 抽象复合函数的二阶偏导
- **要点**：f_i′ 与原函数结构相同，仍含相同的两个部分，故求二阶偏导时要继续对这两个部分分别求导，产生 f₁₁″、f₁₂″、f₂₁″、f₂₂″；再利用 f₁₂″=f₂₁″ 合并同类项。求二阶导时外层已有 f₁′，再求导要写 f″₁₁、f″₁₂，此时括号不能省略。
- **关键概念**：`f₁₁″`、`f₁₂″`、`二阶偏导`
- **相互关系**：属难点题型，部分省份不考，需对照本省考纲。
- **出处**：[陈哥 P92](https://www.bilibili.com/video/BV1husGzwEtZ?p=92)；[杰哥 P126](https://www.bilibili.com/video/BV1Up4y1Y76a?p=126)

### 三元函数与隐函数结合的求导
- **要点**：求 u=f(x,y,z) 而 z 又由 F(x,y,z)=0 确定的偏导时，x 会出现在两处：显含的 x 和隐藏在 z 中的 x。对含 z 的项求导要按复合函数处理并乘上 ∂z/∂x，而 ∂z/∂x 再用隐函数公式求出后回代。易错点在于漏掉 z 中隐含的 x。
- **关键概念**：`三元函数`、`隐函数`、`∂z/∂x`、`回代`
- **出处**：[杰哥 P127](https://www.bilibili.com/video/BV1Up4y1Y76a?p=127)

### 二元隐函数求导：公式法与直接求导法
- **要点**：公式法——由 F(x,y,z)=0 确定 z=f(x,y) 时，先把方程移项整理为 F(x,y,z)=0（先把方程一边化为零构造 F），再对 x,y,z 分别求偏导（求某个变量的偏导时另外两个当常数），则 z_x=−F_x/F_z、z_y=−F_y/F_z（口诀「对角线原则加负号」；因变量的偏导恒在分母位置）；由 F(x,y)=0 确定 y=y(x) 时 dy/dx=−F_x/F_y。直接求导法——方程两边同时对 x（或 y）求导，此时另一自变量当常数，而 z 要当作 x,y 的复合函数处理，凡遇 z 一律带出 z_x（或 z_y），再移项合并同类项解出。
- **关键概念**：`隐函数`、`F_x, F_y, F_z`、`z_x`、`−F_x/F_z`、`直接求导法`
- **相互关系**：两法殊途同归、结果一致；直接求导法求斜率、求切线时更快；抽象函数型隐函数（如 F(xy, x+z)=0）需结合 f₁′、f₂′ 记号使用；求出偏导后可写全微分 dz=(∂z/∂x)dx+(∂z/∂y)dy。
- **出处**：[陈哥 P93](https://www.bilibili.com/video/BV1husGzwEtZ?p=93)；[杰哥 P122](https://www.bilibili.com/video/BV1Up4y1Y76a?p=122)；[米哥 P106](https://www.bilibili.com/video/BV1swAWerEzS?p=106)；[学士帽 P80](https://www.bilibili.com/video/BV1X4411J792?p=80)；[ok姐 P102](https://www.bilibili.com/video/BV1vm421s7mv?p=102)

### 隐函数求二阶偏导
- **要点**：一阶偏导再求一次（不再套公式）；二阶时 z 仍是 x,y 的函数，凡含 z 的项要再乘 ∂z/∂x（链式关系），此点易漏。
- **关键概念**：`链式法则`、`z 是 x,y 的函数`、`分式求导`
- **出处**：[杰哥 P123](https://www.bilibili.com/video/BV1Up4y1Y76a?p=123)；[米哥 P107](https://www.bilibili.com/video/BV1swAWerEzS?p=107)

### 隐函数求导与切线方程
- **要点**：求曲线在某点处的切线方程时，斜率 k 等于该点处的 dy/dx，用公式法或两边对 x 求导求出导函数后代点，再用点斜式写出切线方程。与「导数的几何意义」联用；易错点是求完导函数忘记代点。
- **关键概念**：`切线方程`、`斜率`、`点斜式`
- **出处**：[ok姐 P102](https://www.bilibili.com/video/BV1vm421s7mv?p=102)

### 空间曲线的参数式表示
- **要点**：空间曲线由三个参数方程 x=x(t)、y=y(t)、z=z(t) 给出；若只给出两个方程（如 y=6x²、z=12x²），可令 x=t 补齐为参数式（选谁作参数没有硬性规定，以计算量最小为原则）。只取前两个方程即为平面曲线。若曲线由 y=y(x), z=z(x) 给出，可取 x 为参数，切向量为 (1,y′(x),z′(x))。
- **关键概念**：`参数方程`、`空间曲线`、`平面曲线`、`参数化`
- **出处**：[陈哥 P94](https://www.bilibili.com/video/BV1husGzwEtZ?p=94)；[杰哥 P128](https://www.bilibili.com/video/BV1Up4y1Y76a?p=128)；[ok姐 P103](https://www.bilibili.com/video/BV1vm421s7mv?p=103)

### 空间曲线的切线方程与法平面方程
- **要点**：给定 t₀ 先由曲线方程求出切点（由点 (x₀,y₀,z₀) 反求 t₀）；对三个参数方程分别关于 t 求导并代入 t₀ 得切向量，该向量同时充当切线的方向向量与法平面的法向量：切线写成点向式（「线除」），法平面写成点法式（「面乘」，系数与切线分母相同）。口诀「线除面乘」是为区分线与面的书写形式，不是新公式。
- **关键概念**：`切向量`、`切线方程`、`法平面`、`t₀`、`点向式`、`点法式`
- **相互关系**：与直线、平面方程写法直接衔接；变限积分型参数方程求导需用变限积分求导法则。
- **出处**：[陈哥 P94](https://www.bilibili.com/video/BV1husGzwEtZ?p=94)；[杰哥 P128](https://www.bilibili.com/video/BV1Up4y1Y76a?p=128)；[米哥 P109](https://www.bilibili.com/video/BV1swAWerEzS?p=109)；[ok姐 P103](https://www.bilibili.com/video/BV1vm421s7mv?p=103)

### 由位置关系反求切点
- **要点**：题目说「切线平行于某平面」时，要利用「线与面的位置关系与向量关系相反」这一点：线面平行等价于切向量与平面法向量垂直，即两者点乘为零，由此得到关于参数 t₀ 的方程，解出切点。线面位置关系与向量关系的「相反」对应是本节最易错处。
- **关键概念**：`方向向量`、`法向量`、`点乘为零`
- **出处**：[杰哥 P128](https://www.bilibili.com/video/BV1Up4y1Y76a?p=128)

### 空间曲面与切平面、法线的概念
- **要点**：空间曲面由三元方程 F(x,y,z)=0 表示（或由 z=f(x,y) 给出）。曲面上过某点的所有曲线在该点的切线都落在同一平面上，这个平面叫曲面在该点的切平面；过该点且垂直于切平面的唯一一条直线叫该点的法线；切平面与法线互相垂直。
- **关键概念**：`三元方程`、`切平面`、`法线`
- **相互关系**：与空间曲线的切线、法平面并列且易混；求切平面用平面的点法式、求法线用直线的点向式。
- **出处**：[陈哥 P95](https://www.bilibili.com/video/BV1husGzwEtZ?p=95)；[杰哥 P129](https://www.bilibili.com/video/BV1Up4y1Y76a?p=129)；[ok姐 P104](https://www.bilibili.com/video/BV1vm421s7mv?p=104)

### 法线方向向量与切平面法向量是同一个向量
- **要点**：把曲面方程所有项移到一边，构造三元函数 F(x,y,z)（方程整理成 F(x,y,z)=0），则曲面在点 (x₀,y₀,z₀) 处的法向量就是 (F_x,F_y,F_z) 在该点取值构成的向量；它同时是切平面的法向量与法线的方向向量（可合并为同一个向量 n=(F_x,F_y,F_z)|_M）。点已给定，只需求出这一个向量。由 z=f(x,y) 给出时移项成 z−f(x,y)=0（或 f(x,y)−z=0，两种取法结果等价），再按三元方程的方法处理。
- **关键概念**：`方向向量`、`法向量`、`点法式`、`三元函数`、`显示二元函数`
- **相互关系**：把平面方程与直线方程两套旧知识统一到同一向量上，是本知识点的核心；前提是多元函数的偏导数计算。
- **出处**：[陈哥 P95](https://www.bilibili.com/video/BV1husGzwEtZ?p=95)；[杰哥 P129](https://www.bilibili.com/video/BV1Up4y1Y76a?p=129)；[ok姐 P104](https://www.bilibili.com/video/BV1vm421s7mv?p=104)

### 切平面与法线的求解步骤与两个方程
- **要点**：①把曲面方程移项写成 F(x,y,z)=0，求三个一阶偏导（对某变量求导时其余视为常数）；②把切点代入三个偏导得向量分量。切点为 M(x₀,y₀,z₀) 时，切平面为 F_x(x−x₀)+F_y(y−y₀)+F_z(z−z₀)=0，法线为 (x−x₀)/F_x=(y−y₀)/F_y=(z−z₀)/F_z。忘记先移项成 F=0、三个分量有公因数不约简，是两个常见错误。面面平行求点时，两个法向量平行即对应坐标成比例，据此列方程组解出切点坐标；要求平行于已知平面时设切点并令偏导成比例。
- **关键概念**：`一阶偏导`、`代入切点`、`法向量平行`、`坐标成比例`
- **相互关系**：两式共用同一组系数；法线方程由切平面「相加改相除」得到。
- **出处**：[陈哥 P95](https://www.bilibili.com/video/BV1husGzwEtZ?p=95)；[杰哥 P129](https://www.bilibili.com/video/BV1Up4y1Y76a?p=129)

### 方向导数
- **要点**：偏导数是二元函数沿平行于 x 轴、y 轴两个特殊方向的变化率；方向导数是二元函数在一点沿任意指定方向的变化率，方向以向量形式给出。计算公式：设方向向量的方向余弦为 cos α、cos β（等于向量的坐标比上向量的模），则 ∂z/∂l=f_x cos α+f_y cos β；两个方向余弦构成的向量就是该方向上的单位向量。偏导数是方向导数的两个特例。
- **关键概念**：`方向导数`、`变化率`、`方向余弦`、`单位向量`
- **相互关系**：二维向量的方向余弦公式与三维形式相同，向量的模都是各坐标平方和开根号。
- **出处**：[ok姐 P105](https://www.bilibili.com/video/BV1vm421s7mv?p=105)、[P106](https://www.bilibili.com/video/BV1vm421s7mv?p=106)

### 梯度
- **要点**：二元函数在一点处的两个偏导数值构成的向量就是该点的梯度，记为 grad f 或 ∇f，也可写成 f_x i+f_y j 或坐标形式。梯度由偏导数构造，与方向无关，是确定向量。书写时加箭头，避免加粗后阅卷看不清。
- **关键概念**：`梯度`、`grad`、`倒三角`
- **出处**：[ok姐 P106](https://www.bilibili.com/video/BV1vm421s7mv?p=106)

### 方向导数与梯度的关系
- **要点**：方向导数等于梯度与该方向单位向量的点积，即 |grad f|cos θ（θ 为梯度与方向向量的夹角）。θ=0（方向与梯度同向）时方向导数最大且等于梯度的模，函数值增加最快；θ=π（反向）时方向导数最小、等于模的负值，函数值减少最快；θ=π/2（垂直）时方向导数为零。
- **关键概念**：`点积`、`夹角余弦`
- **相互关系**：由方向导数公式与梯度定义联合推出。
- **出处**：[ok姐 P106](https://www.bilibili.com/video/BV1vm421s7mv?p=106)

### 多元函数的极值与极值点
- **要点**：若点 (x₀,y₀) 的某邻域内所有点的函数值都大于 f(x₀,y₀)（或都小于），则该点为极小值点（极大值点）、函数值为极小值（极大值）。二元函数与一元函数的概念完全一致，只是几何上由平面曲线变为空间曲面；只需在邻域内比较，不要求在整个区域上最大或最小。
- **关键概念**：`邻域`、`极小值`、`极大值`、`极值点`
- **相互关系**：邻域思想在条件极值的判定中还要再用。
- **出处**：[陈哥 P96](https://www.bilibili.com/video/BV1husGzwEtZ?p=96)；[ok姐 P107](https://www.bilibili.com/video/BV1vm421s7mv?p=107)

### 多元函数的驻点与极值点
- **要点**：使两个一阶偏导 f_x、f_y 同时为零的点称驻点（可偏导的极值点处，两个一阶偏导都为零）。极值点分两类：驻点与不可偏导点（曲面尖点处一阶偏导不存在）。
- **关键概念**：`驻点`、`一阶偏导`、`不可偏导点`
- **相互关系**：二元函数求极值只考察驻点这一种情况，不会考偏导不存在的点；这一点与一元函数不同。
- **出处**：[陈哥 P96](https://www.bilibili.com/video/BV1husGzwEtZ?p=96)；[ok姐 P107](https://www.bilibili.com/video/BV1vm421s7mv?p=107)

### 多元函数极值的四步求解法与判别准则
- **要点**：①求两个一阶偏导并令其为零，联立解出全部驻点；②求二阶偏导 f\_\{xx\},f\_\{xy\},f\_\{yy\}；③把驻点代入二阶偏导，记作 A,B,C（A=f\_\{xx\}, B=f\_\{xy\}, C=f\_\{yy\}，必须是驻点处的二阶偏导值）；④判断：AC−B²>0 有极值，此时 A>0 取极小、A&lt;0 取极大；AC−B²&lt;0 无极值；AC−B²=0 失效、需另作讨论（升本不要求）。判出极值点后还须把驻点代回原函数求出极值。部分教材用 B²−AC，符号正好相反，做题时统一用其中一种即可。
- **关键概念**：`二阶偏导`、`A、B、C`、`AC−B²`
- **相互关系**：只针对驻点；判断完所有驻点后再统一求各极值点的函数值。
- **出处**：[陈哥 P96](https://www.bilibili.com/video/BV1husGzwEtZ?p=96)；[杰哥 P130](https://www.bilibili.com/video/BV1Up4y1Y76a?p=130)；[米哥 P111](https://www.bilibili.com/video/BV1swAWerEzS?p=111)；[ok姐 P107](https://www.bilibili.com/video/BV1vm421s7mv?p=107)

### 多元函数极值的题型与易错点
- **要点**：若二阶偏导解出来直接是常数，则 A,B,C 已确定、无需再代驻点；若是表达式则必须代入。解驻点用加减消元或代入消元；出现两个驻点须逐个讨论，可能一个有极值、另一个无极值。难度递进的三种考法——直接得常数、需代入表达式、多驻点分情况。
- **关键概念**：`联立消元`、`分类讨论`
- **出处**：[陈哥 P96](https://www.bilibili.com/video/BV1husGzwEtZ?p=96)

### 二元函数的最值
- **要点**：闭区域上连续的二元函数必取得最大值与最小值；由于边界点有无穷多个，不能照搬一元函数「比较驻点与端点函数值」的做法。升本中若由题意可知最值一定在区域内部取得、且区域内只有一个驻点，则该驻点的函数值即为所求最值。
- **关键概念**：`闭区域`、`最值定理`、`驻点`
- **相互关系**：与一元闭区间上的最值定理类比。
- **出处**：[ok姐 P108](https://www.bilibili.com/video/BV1vm421s7mv?p=108)

### 条件极值：目标函数与条件函数
- **要点**：自变量被约束方程限制时的极值称条件极值，约束限制的始终是 x,y 两个自变量。目标函数即「求谁的极值」中的那个函数；条件函数须把约束方程右边移到左边写成 φ(x,y)=0，不能只写「x+y」这种半截形式。题干有时不直接给出这两个函数（如「表面积固定求最大体积」），需自己提炼，这是第一个难点。
- **关键概念**：`条件极值`、`目标函数`、`条件函数`
- **出处**：[陈哥 P97](https://www.bilibili.com/video/BV1husGzwEtZ?p=97)；[杰哥 P131](https://www.bilibili.com/video/BV1Up4y1Y76a?p=131)、[P132](https://www.bilibili.com/video/BV1Up4y1Y76a?p=132)

### 拉格朗日函数与方程组
- **要点**：构造 L(x,y)=f(x,y)+λφ(x,y)（φ 为约束，须右边化为零），对 x,y,λ 求偏导令零（L_x=L_y=L_λ=0），再补上条件函数为零；解法核心是由前两式消去 λ 得 x,y 的关系（用「移项后两式相除」消 λ，比直接消元更快），再代入条件函数解出 x,y，所得点即可能极值点，最后代入目标函数比较大小。λ 是自变量不能当常数，难点在解方程组，靠观察化简；目标函数与条件函数找错是最常见的失分点。
- **关键概念**：`拉格朗日函数`、`拉格朗日乘数`、`λ`、`消元`
- **出处**：[陈哥 P97](https://www.bilibili.com/video/BV1husGzwEtZ?p=97)；[杰哥 P131](https://www.bilibili.com/video/BV1Up4y1Y76a?p=131)、[P132](https://www.bilibili.com/video/BV1Up4y1Y76a?p=132)；[米哥 P112](https://www.bilibili.com/video/BV1swAWerEzS?p=112)

### 条件极值的极值判定
- **要点**：条件极值没有 AC−B² 判别法，改用极值定义：在驻点附近另取一个满足条件函数的点代入目标函数，与该驻点处的函数值比较，更大则为极小值点、更小则为极大值点。取点不落在约束曲线上则判断无效。也可结合实际意义判断极大或极小。
- **关键概念**：`邻域取值比较`、`满足约束`
- **出处**：[陈哥 P97](https://www.bilibili.com/video/BV1husGzwEtZ?p=97)；[杰哥 P131](https://www.bilibili.com/video/BV1Up4y1Y76a?p=131)

### 条件极值的两类常考应用题型
- **要点**：一是实际应用型，如「表面积固定求最大体积」，需自设长宽高为 x,y,z，以 V=xyz 为目标、以表面积表达式减定值为约束；其偏导方程组含三个方程，可将各方程分别乘 x、乘 y、乘 z 后两两相减消去 λ，推出 x=y=z 之类的对称关系。二是距离型，以点到直线距离公式为目标、曲线方程为约束，因含绝对值通常先对距离的平方求极值，最后开根号还原；距离公式的分母是常数，真正决定最值的是分子，因此可只取分子（线性式）作目标函数，把椭圆等约束作条件函数；求出驻点后逐个代入距离公式比较，取最小（大）者。取分子的做法只在分母为常数时成立，是简化运算的技巧而非公式变形。
- **关键概念**：`V=xyz`、`乘系数相减`、`平方去绝对值`、`点到直线的距离公式`、`分子决定最值`
- **相互关系**：实际应用型的方程组消元是压轴难点。
- **出处**：[陈哥 P97](https://www.bilibili.com/video/BV1husGzwEtZ?p=97)；[杰哥 P132](https://www.bilibili.com/video/BV1Up4y1Y76a?p=132)

### 极值在实际问题中的应用（建模）
- **要点**：把实际条件翻译成目标函数与约束条件，写出拉格朗日函数后按条件极值流程求解。
- **关键概念**：`目标函数`
- **出处**：[米哥 P113](https://www.bilibili.com/video/BV1swAWerEzS?p=113)


### 二元函数的概念
- **要点**：有两个自变量 $x$、$y$ 的函数叫二元函数，记作 $z=f(x,y)$；有几个自变量就叫几元函数，两个及以上统称多元函数。二元函数中 $x$ 与 $y$ 相互独立，各自变化共同引起 $z$ 的变化。
- **关键概念**：`二元函数`、`$z=f(x,y)$`、`多元函数`
- **相互关系**：考试中绝大多数是二元函数，偶尔考三元函数，四元及以上不会考。
- **出处**：[石头 P69](https://www.bilibili.com/video/BV18CL26WEJ3?p=69)

### 二元函数的几何意义与定义域
- **要点**：一元函数 $y=f(x)$ 的图像是平面上的曲线，二元函数 $z=f(x,y)$ 的图像是空间直角坐标系中的一张曲面（如 $z=x^2+y^2$ 是旋转抛物面）。把自变量的一对值 $(x,y)$ 看作 $xOy$ 面上的点 $P(x,y)$，二元函数的定义域就是曲面在 $xOy$ 面上的投影区域。
- **关键概念**：`曲面`、`投影区域`、`定义域`
- **相互关系**：定义域的几何意义（投影区域）在第六章二重积分中会直接用到，需要会画；一元函数求定义域只解出 $x$ 的范围，二元函数则得到一个平面区域。
- **出处**：[石头 P69](https://www.bilibili.com/video/BV18CL26WEJ3?p=69)

### 求二元函数的定义域
- **要点**：求法与一元函数一致，仍是「三把斧」：根号下大于等于零、分母不等于零、对数的真数大于零，偶尔涉及反三角函数要求整体落在 $[-1,1]$ 内；把各限制联立后解出 $x$ 与 $y$ 的关系式即可，不必分别解出 $x$、$y$ 各自的范围。最终结果必须写成集合或区间形式，如 $\{(x,y)\mid 4&lt;x^2+y^2\leq 9\}$。
- **关键概念**：`三把斧`、`联立不等式组`、`$\{(x,y)\mid\cdots\}$`
- **相互关系**：不等式组在 $xOy$ 面上对应一个区域（如 $4&lt;x^2+y^2\leq 9$ 是圆环），画图时实线表示包含边界、虚线表示不包含；若一时化不到最简，直接写原始不等式组也能得分。
- **出处**：[石头 P69](https://www.bilibili.com/video/BV18CL26WEJ3?p=69)

### 二元函数极限的定义
- **要点**：当点 $(x,y)$ 以任意方式趋近于 $(x_0,y_0)$ 时 $f(x,y)$ 都趋近于同一个常数 $A$，才称 $\lim\limits\_\{(x,y)\to(x\_0,y\_0)\}f(x,y)=A$ 存在。因为二元函数的图像是曲面，趋近的路径有无穷多条，必须所有路径的极限都相同才算有极限。
- **关键概念**：`二元函数极限`、`路径无关`、`$\lim\limits_{(x,y)\to(x_0,y_0)}f(x,y)=A$`
- **相互关系**：只要有一条路径的极限不存在或与其他路径不同，就可判定极限不存在，这为「取路径证伪」提供了依据。
- **出处**：[石头 P70](https://www.bilibili.com/video/BV18CL26WEJ3?p=70)

### 求二元函数极限的整体思想
- **要点**：把趋于零或趋于无穷的那一「坨」表达式整体换元为新变量（如令 $t=x^2+y^2$），二元极限就化为一元函数的极限，再用重要极限、等价无穷小、抓大头等一元方法求解；定型时要把 $x$、$y$ 的值同时代入看趋势。
- **关键概念**：`整体思想`、`换元法`、`先定型后定法`、`$\sin\square\sim\square$`、`$1^\infty$ 型用第二重要极限`
- **相互关系**：二元函数本身不能直接用洛必达法则（对谁求导都不合适），但换元成一元函数之后就可以洛必达。
- **出处**：[石头 P70](https://www.bilibili.com/video/BV18CL26WEJ3?p=70)

### 极限不存在的判断与二元函数的连续性
- **要点**：证明极限不存在的方法是取特殊路径（通常令 $y=kx$），若化得的极限值随 $k$ 变化而不同，则极限不存在；需记住三个极限不存在的典型式：$\frac{y}{x+y}$、$\frac{x^2-y^2}{x^2+y^2}$、$\frac{xy}{x^2+y^2}$（均为 $(x,y)\to(0,0)$）。二元函数在一点连续的定义是极限值等于该点的函数值。常用工具还有 $0\times$ 有界 $=0$，以及夹逼准则（典型题为 $\frac{x^2y}{x^2+y^2}$，先上下同除 $x^2$ 再夹逼）。
- **关键概念**：`路径法`、`$y=kx$`、`极限不存在`、`极限值等于函数值`、`$0\times$ 有界 $=0$`
- **相互关系**：判断连续本质上仍是求极限；连续函数经四则运算、复合后仍连续，有界闭区域上的多元连续函数必取到最大值与最小值，并可取到介于两者之间的任何值。
- **出处**：[石头 P70](https://www.bilibili.com/video/BV18CL26WEJ3?p=70)

### 偏导数的概念与求法
- **要点**：二元函数 $z=f(x,y)$ 对 $x$ 求偏导时把 $y$ 视为常数，记作 $\frac{\partial z}{\partial x}$ 或 $f_x$；对 $y$ 求偏导时把 $x$ 视为常数，记作 $\frac{\partial z}{\partial y}$ 或 $f_y$。求法就是回到一元函数求导，把另一个变量当成字母系数处理。若式子复杂看不清，可先在草稿上把另一个变量写成 $A$，算完再换回来。
- **关键概念**：`偏导数`、`$\frac{\partial z}{\partial x}$`、`$f_x$`、`把另一变量视为常数`
- **相互关系**：幂指函数（底数与指数都含 $x$，如 $(x+2y)\^\{x\^2\}$）对 $x$ 求偏导要先用恒等式 $u^v=e\^\{v\ln u\}$ 化成复合函数；它对 $y$ 求偏导时已退化为普通幂函数，直接按幂函数法则求。
- **出处**：[石头 P71](https://www.bilibili.com/video/BV18CL26WEJ3?p=71)

### 高阶偏导数
- **要点**：一阶偏导仍是二元函数，可继续求偏导，共得到四个二阶偏导 $f\_\{xx\}$、$f\_\{xy\}$、$f\_\{yx\}$、$f\_\{yy\}$，下标按求导的先后顺序排列。其中 $f\_\{xy\}$ 与 $f\_\{yx\}$ 称混合偏导数，当二者都连续时相等，否则不保证相等，所以求 $f\_\{xy\}$ 就按先 $x$ 后 $y$ 的顺序算，不要随意调换。
- **关键概念**：`二阶偏导数`、`$f_{xy}$`、`$f_{yx}$`、`混合偏导数`、`连续则相等`
- **相互关系**：三元函数求偏导同理，对某个自变量求偏导时把另外两个都视为常数；考到三元函数时题目一般更简单，知道怎么求即可。
- **出处**：[石头 P71](https://www.bilibili.com/video/BV18CL26WEJ3?p=71)

### 全微分与可微的条件
- **要点**：二元函数的全微分等于两个偏微分之和，$dz=\frac{\partial z}{\partial x}dx+\frac{\partial z}{\partial y}dy$；求 $dz$ 的步骤是先求两个偏导数再代入该式，若要求某点的全微分，最后把点的坐标代入系数（$dx$、$dy$ 保留不代）。三元函数则为 $du=\frac{\partial u}{\partial x}dx+\frac{\partial u}{\partial y}dy+\frac{\partial u}{\partial z}dz$。可微的必要条件：可微可推出可偏导，也可推出连续；充分条件：两个偏导数连续可推出可微。
- **关键概念**：`全微分`、`$dz=\frac{\partial z}{\partial x}dx+\frac{\partial z}{\partial y}dy$`、`偏微分`、`可微 $\Rightarrow$ 可偏导`
- **相互关系**：一元函数中可导与可微等价，二元函数中可偏导推不出可微（必须偏导数连续才行）；连续与可偏导都推不出对方，也都推不出可微，这是与一元函数最大的区别。
- **出处**：[石头 P72](https://www.bilibili.com/video/BV18CL26WEJ3?p=72)

### 复合求导链式图与口诀
- **要点**：求多元复合函数的偏导分两步：第一步画复合求导链式图，理清外层函数与中间变量的复合关系；第二步按口诀「竖向同一条线上的相乘，横向同一自变量的相加」写出结果。画图时外层括号里有几个逗号就分成几支（一个逗号两支，两个逗号三支），每个中间变量有几个自变量就向下分几支。
- **关键概念**：`链式图`、`竖向相乘`、`横向相加`、`逗号定支数`
- **相互关系**：该口诀对二元复合二元、三个中间变量、二元复合一元、一元复合一元等各种模型都通用，学完模型后应把它们忘掉，只留这两步。
- **出处**：[石头 P73](https://www.bilibili.com/video/BV18CL26WEJ3?p=73)

### 抽象函数求偏导
- **要点**：题目只给 $z=f(\square,\triangle)$ 而不给具体表达式时，用 $f_1'$、$f_2'$ 表示外层函数对第一、第二个中间变量的偏导数，再乘以内层中间变量对该自变量的偏导数，按口诀相加。若外层括号里只有一项（如 $f(2x+y)$），则只用 $f'$，不必写 $f_1'$、$f_2'$。
- **关键概念**：`抽象函数`、`$f_1'$`、`$f_2'$`、`$f'$`
- **相互关系**：结果中可以保留 $f_1'$、$f_2'$，因为它们代表外层的运算规则；若中间变量是自己设的（如设 $u=xy$），最后最好换回原自变量。
- **出处**：[石头 P73](https://www.bilibili.com/video/BV18CL26WEJ3?p=73)

### 全导数
- **要点**：若 $z=f(u,v)$ 而 $u$、$v$ 都只是 $x$ 的一元函数，则复合后本质上仍是一元函数，此时求导不再是偏导而是全导数 $\frac{dz}{dx}=\frac{\partial z}{\partial u}\cdot\frac{du}{dx}+\frac{\partial z}{\partial v}\cdot\frac{dv}{dx}$，即外层用偏导、内层用普通导数，再相加。
- **关键概念**：`全导数`、`$\frac{dz}{dx}$`、`外层偏导、内层导数`
- **相互关系**：这类题也可直接把 $u$、$v$ 代入化为关于 $x$ 的一元函数再逐层求导，两种方法结果相同；把一元问题「升维」成多元问题处理的思想，在多元隐函数求偏导中更常用。
- **出处**：[石头 P73](https://www.bilibili.com/video/BV18CL26WEJ3?p=73)

### 一元隐函数的两边求导法
- **要点**：方程 $F(x,y)=0$ 确定的隐函数 $y=y(x)$，把方程两边同时对 $x$ 求导，求导时 $y$ 是 $x$ 的复合函数，凡是含 $y$ 的项都要再乘 $y'$（即 $\frac{dy}{dx}$）。例如 $e^y+xy-1=0$ 两边求导得 $e^yy'+y+xy'=0$，解出 $y'$ 即可。
- **关键概念**：`隐函数`、`两边分别求导`、`$y$ 是 $x$ 的复合函数`、`$y'$`
- **相互关系**：最易漏的是含 $y$ 的项忘了再乘 $y'$；乘积项 $xy$ 要用「前导后不导加后导前不导」的乘法法则，常数项求导为零。此法结果与公式法完全一致。
- **出处**：[石头 P74](https://www.bilibili.com/video/BV18CL26WEJ3?p=74)

### 一元隐函数的公式法
- **要点**：把方程所有项移到一边、使右边为零，设左边这一整块为二元函数 $F(x,y)$，此时 $x$ 与 $y$ 都是独立自变量。分别求出 $F_x$、$F_y$，则 $\frac{dy}{dx}=-\frac{F_x}{F_y}$。
- **关键概念**：`$F(x,y)$`、`$\frac{dy}{dx}=-\frac{F_x}{F_y}$`、`上下颠倒加负号`
- **相互关系**：口诀是「上下颠倒加负号」，负号极易丢掉。公式的来源是把一元隐函数升维成二元函数后两边对 $x$ 求偏导，再解出 $\frac{dy}{dx}$。
- **出处**：[石头 P74](https://www.bilibili.com/video/BV18CL26WEJ3?p=74)

### 二元隐函数求偏导的两边求导法
- **要点**：方程 $F(x,y,z)=0$ 确定 $z=z(x,y)$，对 $x$ 求偏导时把 $y$ 当常数、$z$ 当 $x$ 的函数（含 $z$ 的项都要再乘 $\frac{\partial z}{\partial x}$）；对 $y$ 求偏导时把 $x$ 当常数、$z$ 当 $y$ 的函数。求完把含偏导的项合并，再解出来。
- **关键概念**：`隐函数 $z=z(x,y)$`、`$\frac{\partial z}{\partial x}$`、`$\frac{\partial z}{\partial y}$`
- **相互关系**：与一元情形的区别在于这里 $x$、$y$ 相互独立，求 $\frac{\partial z}{\partial x}$ 时 $y$ 是常数而不再是 $x$ 的函数；过程繁琐易错，通常改用公式法。
- **出处**：[石头 P74](https://www.bilibili.com/video/BV18CL26WEJ3?p=74)

### 二元隐函数求偏导的公式法
- **要点**：把方程整理成右边为零，设左边为三元函数 $F(x,y,z)$，此时 $x$、$y$、$z$ 地位平等、互不相关。分别求出 $F_x$、$F_y$、$F_z$，则 $\frac{\partial z}{\partial x}=-\frac{F_x}{F_z}$，$\frac{\partial z}{\partial y}=-\frac{F_y}{F_z}$。
- **关键概念**：`$F(x,y,z)$`、`$\frac{\partial z}{\partial x}=-\frac{F_x}{F_z}$`、`$\frac{\partial z}{\partial y}=-\frac{F_y}{F_z}$`
- **相互关系**：同样遵循「上下颠倒加负号」，分母永远是 $F_z$；求 $F_x$ 时 $y$、$z$ 都视为常数，大量项直接为零，比两边求导法省力得多。
- **出处**：[石头 P74](https://www.bilibili.com/video/BV18CL26WEJ3?p=74)

### 无条件极值的概念
- **要点**：若二元函数 $z=f(x,y)$ 在点 $M_0$ 的某个邻域内，$M_0$ 处函数值比邻域内所有其他点都大（都小），则 $M_0$ 为极大值点（极小值点），该函数值称极大值（极小值），统称极值。它对自变量不加任何限制条件，故称无条件极值。
- **关键概念**：`无条件极值`、`极值点`、`邻域`、`极大值`、`极小值`
- **相互关系**：与一元函数极值对照记忆：一元只看左右两侧，二元要看四面八方；极值不一定是最大（小）值，只是局部最大（小）。
- **出处**：[石头 P75](https://www.bilibili.com/video/BV18CL26WEJ3?p=75)

### 无条件极值的必要条件
- **要点**：若 $f(x,y)$ 在点 $(x_0,y_0)$ 取得极值且两个一阶偏导数都存在，则必有 $f_x(x_0,y_0)=0$ 且 $f_y(x_0,y_0)=0$。两个一阶偏导同时为零的点称为驻点。
- **关键概念**：`必要条件`、`驻点`、`$f_x=0$ 且 $f_y=0$`
- **相互关系**：与一元函数「极值点＋可导 $\Rightarrow$ 驻点」完全一致；反过来驻点不一定是极值点，必须用充分条件进一步判断。
- **出处**：[石头 P75](https://www.bilibili.com/video/BV18CL26WEJ3?p=75)

### 无条件极值的充分条件与 Δ 判别法
- **要点**：在驻点处算出 $A=f\_\{xx\}$、$B=f\_\{xy\}$、$C=f\_\{yy\}$，记 $\Delta=B^2-AC$。当 $\Delta&lt;0$ 时该点必为极值点：$A&lt;0$ 为极大值点，$A>0$ 为极小值点；当 $\Delta>0$ 时不是极值点；当 $\Delta=0$ 时结论不确定。
- **关键概念**：`$A=f_{xx}$`、`$B=f_{xy}$`、`$C=f_{yy}$`、`$\Delta=B^2-AC$`、`小小大、小大小、大不是、等不定`
- **相互关系**：口诀「小小大、小大小、大不是、等不定」依次对应 $\Delta&lt;0$ 且 $A&lt;0$、$\Delta&lt;0$ 且 $A>0$、$\Delta>0$、$\Delta=0$ 四种情形；有的教材把判别式写成 $AC-B^2$，此时所有符号判断都要反过来。
- **出处**：[石头 P75](https://www.bilibili.com/video/BV18CL26WEJ3?p=75)

### 求无条件极值的解题步骤
- **要点**：第一步求一阶偏导 $f_x$、$f_y$ 并令它们同时为零，联立解出全部驻点；第二步求三个二阶偏导 $f\_\{xx\}$、$f\_\{xy\}$、$f\_\{yy\}$，把每个驻点分别代入求出 $A$、$B$、$C$ 与 $\Delta$；第三步按判别法逐个判断该驻点是否为极值点、是极大还是极小。
- **关键概念**：`三步套路`、`联立解方程组求驻点`、`逐点判断`
- **相互关系**：驻点往往不止一个，必须逐个判断不能只算一个；若题目要求极值，最后还要把极值点代回原函数算出函数值。
- **出处**：[石头 P75](https://www.bilibili.com/video/BV18CL26WEJ3?p=75)

### 无条件极值的应用题
- **要点**：实际问题（如把正数 $A$ 表示为三个正数之和使其乘积最大）先设两个自变量，第三个用约束式表示，把目标量写成二元函数，再用无条件极值求驻点。若符合题意的驻点唯一，可直接断定它取到所求最值，无需再判极大极小。
- **关键概念**：`唯一驻点即最值点`、`目标量化为二元函数`、`实际问题最值必存在`
- **相互关系**：同一题也可设三个自变量用条件极值求解，两种方法结果一致；答句必须回答题目所问（求最值还是求各变量的值），否则答非所问。
- **出处**：[石头 P75](https://www.bilibili.com/video/BV18CL26WEJ3?p=75)

### 条件极值的概念
- **要点**：求二元函数 $z=f(x,y)$ 在约束条件 $\varphi(x,y)=0$ 下的极值，称为条件极值。它不要求该点在四面八方都最高，只要求在满足约束的那条曲线上比邻近点高（低）。
- **关键概念**：`条件极值`、`约束条件`、`$\varphi(x,y)=0$`
- **相互关系**：与无条件极值的唯一区别就是多了一个等式约束；约束条件必须整理成右边为零的标准形式 $\varphi(x,y)=0$ 才能使用后续方法。
- **出处**：[石头 P76](https://www.bilibili.com/video/BV18CL26WEJ3?p=76)

### 目标函数、约束条件与决策变量
- **要点**：应用题要先把文字翻译成数学模型：题目中要求「最大/最小/最高/最低」的那个量是目标函数；「在什么前提下、什么要求下、什么是定值」给出的是约束条件；可以自由取值、需要决策的自变量是决策变量。
- **关键概念**：`目标函数`、`约束条件`、`决策变量`、`找关键词`
- **相互关系**：这三者找对，题目就完成了一大半；决策变量的设法可以不同（如铁丝题既设两段长为变量，也可设正方形边长与圆半径为变量），设法一变，目标函数与约束条件都要相应改写。
- **出处**：[石头 P76](https://www.bilibili.com/video/BV18CL26WEJ3?p=76)

### 拉格朗日乘数法的步骤
- **要点**：第一步设拉格朗日函数 $L(x,y)=f(x,y)+\lambda\varphi(x,y)$，其中 $\lambda$ 称拉格朗日乘子；第二步对 $x$、$y$、$\lambda$ 分别求一阶偏导；第三步令这三个偏导都等于零，联立解出 $x$、$y$（$\lambda$ 可不解）；第四步按实际问题说明最值在唯一驻点处取得。
- **关键概念**：`拉格朗日函数`、`$L=f+\lambda\varphi$`、`拉格朗日乘子`、`四步流程`
- **相互关系**：对 $\lambda$ 求偏导得到的永远是约束条件本身；三元情形做法完全一样，只是多一个自变量就多一个偏导方程。
- **出处**：[石头 P76](https://www.bilibili.com/video/BV18CL26WEJ3?p=76)

### 拉格朗日乘数法解应用题的套路
- **要点**：先读题定出目标函数与约束条件，再设拉格朗日函数、求三个偏导、联立求解，最后把解出的变量值代回目标函数得最值，并写出完整答句。解方程组时可用两式相减先消掉 $\lambda$，能显著减少计算量。
- **关键概念**：`建模—设函数—求偏导—联立求解—作答`
- **相互关系**：这类题一般出大题或应用题，难点在读懂题意与写答句而非计算步骤；约束式中含根号、$\pi$ 时通常能在消元过程中约简。
- **出处**：[石头 P76](https://www.bilibili.com/video/BV18CL26WEJ3?p=76)

### 轮换对称性
- **要点**：若把目标函数与约束条件中的 $x$、$y$（或 $x$、$y$、$z$）任意对调后表达式不变，则这些变量地位等价，必然有 $x=y$（或 $x=y=z$），直接代入约束条件即可求出驻点，省去大量计算。
- **关键概念**：`轮换对称性`、`$x=y$`、`$x=y=z$`
- **相互关系**：用它几秒就能看出变量相等，但专升本不把轮换对称性列为已知结论，答题时仍应把拉格朗日乘数法的步骤写全，以免被判步骤缺失而失分。
- **出处**：[石头 P76](https://www.bilibili.com/video/BV18CL26WEJ3?p=76)

### 条件极值与无条件极值的相互转化
- **要点**：由约束条件解出其中一个变量（如 $z=z(x,y)$）代入目标函数，条件极值就化为一元或二元函数的无条件极值；反之把 $n$ 元无条件极值添一个约束条件升为 $(n+1)$ 元，与原来的问题等价。
- **关键概念**：`自由度`、`代入消元`、`升维与降维`
- **相互关系**：二元无约束（自由度 $2+0$）与三元加一个约束（自由度 $3-1$）等价；同一道应用题用两种方法都能做，一般选计算量小的那种。
- **出处**：[石头 P76](https://www.bilibili.com/video/BV18CL26WEJ3?p=76)


## 九、二重积分与曲线积分


### 二重积分的概念与几何意义
- **要点**：把积分区域 D 分成许多小块，每块取一点算函数值当高、小块面积当底得到小柱体，把这些柱体体积求和取极限，就是二重积分 ∬_D f(x,y)dσ。故其几何意义是曲顶柱体的体积：顶为曲面 z=f(x,y)，底为 xOy 平面上的有界区域 D（D 是积分区域，即曲面在 xOy 面上的投影）；直角坐标系下面积元素 dσ 写成 dx dy。f≥0 时等于曲顶柱体体积；f 有正有负时等于平面上方体积减去下方体积；f≡1 时等于区域 D 的面积。定积分求面积、二重积分求体积是升维关系。
- **关键概念**：`积分区域 D`、`被积函数`、`曲顶柱体`、`dσ=dx dy`、`面积微元`
- **相互关系**：由一元定积分（曲边梯形面积）升维而来，思想一致（分割—近似—求和—取极限）。
- **出处**：[陈哥 P98](https://www.bilibili.com/video/BV1husGzwEtZ?p=98)；[杰哥 P83](https://www.bilibili.com/video/BV1Up4y1Y76a?p=83)；[米哥 P114](https://www.bilibili.com/video/BV1swAWerEzS?p=114)；[学士帽 P82](https://www.bilibili.com/video/BV1X4411J792?p=82)；[ok姐 P109](https://www.bilibili.com/video/BV1vm421s7mv?p=109)

### 二重积分的性质
- **要点**：常数因子 k 可提到积分号外；被积函数为两函数加减时可拆开分别积分；区域可加（∬_D=∬\_\{D₁\}+∬\_\{D₂\}，两块须正好拼成 D）；被积函数为 1 时 ∬_D 1 dσ=S_D 等于区域 D 的面积（柱体高为 1，体积等于底面积），推广 ∬_D K dσ=K S_D。比大小：区域同则被积函数大者大（比较定理），被积函数同则区域大者大；具体比较时常取特殊值（如令 x²+y²=¼）判断，并结合函数图像。
- **关键概念**：`常数倍`、`可加性`、`∬_D 1 dσ=S_D`、`比较定理`
- **相互关系**：最后一条常与「已知积分值反求区域」的选择题结合。
- **出处**：[陈哥 P98](https://www.bilibili.com/video/BV1husGzwEtZ?p=98)；[杰哥 P83](https://www.bilibili.com/video/BV1Up4y1Y76a?p=83)、[P85](https://www.bilibili.com/video/BV1Up4y1Y76a?p=85)；[米哥 P114](https://www.bilibili.com/video/BV1swAWerEzS?p=114)、[P115](https://www.bilibili.com/video/BV1swAWerEzS?p=115)；[学士帽 P82](https://www.bilibili.com/video/BV1X4411J792?p=82)；[ok姐 P110](https://www.bilibili.com/video/BV1vm421s7mv?p=110)

### 估值定理与常数二重积分
- **要点**：设 m≤f(x,y)≤M，则 m S_D≤∬_D f dσ≤M S_D。∬_D k dσ=k S_D 用于反推区域参数。矩形区域上求 f 的最值只需在端点处取。易错：x²+y²≤A 的半径为 √A。考频很低，一般只考填空。
- **关键概念**：`估值定理`、`最大值最小值`、`底面积`、`圆域半径`
- **相互关系**：两者由几何意义理解即可。
- **出处**：[杰哥 P83](https://www.bilibili.com/video/BV1Up4y1Y76a?p=83)、[P86](https://www.bilibili.com/video/BV1Up4y1Y76a?p=86)；[米哥 P115](https://www.bilibili.com/video/BV1swAWerEzS?p=115)

### 常见平面图形面积
- **要点**：圆 x²+y²=R² 面积 πR²；椭圆 x²/a²+y²/b²=1 面积 πab（长半轴与短半轴相乘再乘 π）；圆环用大圆减小圆；半圆、扇形、圆环的面积需熟记。椭圆面积常在大题中间步骤用到，容易被忽略。
- **关键概念**：`椭圆面积 πab`、`圆环`
- **出处**：[杰哥 P84](https://www.bilibili.com/video/BV1Up4y1Y76a?p=84)

### 平面区域的代数表示
- **要点**：y≥kx+b 表示直线之上方、y≤kx+b 表示下方；x²+y²≤R² 表示圆内、≥ 表示圆外；|x|+|y|≤1 表示对角顶点在坐标轴上的菱形（正方形），边长为 √2、面积为 2。
- **关键概念**：`直线的上下方`、`圆内圆外`、`|x|+|y|≤1`
- **相互关系**：|x|+|y|≤1 这个区域在后续计算中反复出现，必须记住。
- **出处**：[陈哥 P98](https://www.bilibili.com/video/BV1husGzwEtZ?p=98)

### 题型：由积分值反求积分区域
- **要点**：题目问「∬_D 1 dσ=k 时 D 是哪一个」，实质是问哪个选项的区域面积等于 k，逐个画图算面积比对即可。遇绝对值不等式按 x,y 正负分四种情况去绝对值，得到四条边界线后围出区域。
- **关键概念**：`去绝对值分类`、`区域面积`
- **出处**：[陈哥 P98](https://www.bilibili.com/video/BV1husGzwEtZ?p=98)

### 二重积分的 X 型与 Y 型区域
- **要点**：X 型区域「上下为曲线、左右为直线（或退化为点）」，即 D={(x,y)|a≤x≤b, y₁(x)≤y≤y₂(x)}；Y 型区域「左右为关于 y 的曲线、上下为直线」。判断类型是一切计算的起点；同一区域常常两型通用。
- **关键概念**：`X 型`、`Y 型`
- **出处**：[陈哥 P99](https://www.bilibili.com/video/BV1husGzwEtZ?p=99)

### 化二重积分为二次积分
- **要点**：D 为 X 型时 ∬_D f dxdy=∫_a^b dx ∫\_\{y₁(x)\}\^\{y₂(x)\} f dy（先对 y 后对 x，dx 在前、dy 在后）；Y 型时 ∬_D f dxdy=∫_c^d dy ∫\_\{x₁(y)\}\^\{x₂(y)\} f dx（dy 在前、dx 在后）。这种写法只是把内层结果「挪到后面」的简写，两个积分号不是乘积关系。计算时先算内层（写在后面的那个），再算外层；内层积分变量为 y 时，被积函数中的 x 全部当常数。
- **关键概念**：`二次积分`、`累次积分`、`dx 在前`、`dy 在前`、`从右向左`
- **相互关系**：与偏导数「对一个变量求导、其余视为常数」逻辑一致。
- **出处**：[陈哥 P99](https://www.bilibili.com/video/BV1husGzwEtZ?p=99)、[P100](https://www.bilibili.com/video/BV1husGzwEtZ?p=100)；[杰哥 P87](https://www.bilibili.com/video/BV1Up4y1Y76a?p=87)；[米哥 P116](https://www.bilibili.com/video/BV1swAWerEzS?p=116)；[ok姐 P111](https://www.bilibili.com/video/BV1vm421s7mv?p=111)

### 定限口诀
- **要点**：「后积先定线，线内画条线，先交写下限，后交写上限」。后积分变量对应的上下限一定是常数（即区域在该轴上的取值范围，取该变量在区域中的最小与最大值）；另一变量的上下限由箭头线穿过区域时先交、后交的边界决定。X 型从下往上画箭头线，Y 型从左往右画，方向不能搞反。先画出积分区域 D 并求出关键交点；对 y 积分时画从左到右的竖直穿越线，先穿过的曲线为下限、后穿过的为上限，表达式整理成 y=…x；对 x 积分时改画水平穿越线，上下限须整理成 x=…y，开方出现正负号时按图形位置舍去不合理分支。
- **关键概念**：`后积先定线`、`先交写下限`、`后交写上限`、`穿越线`、`箭头法定限`
- **出处**：[陈哥 P99](https://www.bilibili.com/video/BV1husGzwEtZ?p=99)；[杰哥 P87](https://www.bilibili.com/video/BV1Up4y1Y76a?p=87)；[米哥 P116](https://www.bilibili.com/video/BV1swAWerEzS?p=116)；[学士帽 P83](https://www.bilibili.com/video/BV1X4411J792?p=83)；[帆哥 P1](https://www.bilibili.com/video/BV1xxXZBKENv?p=1)

### Y 型的表达式变形
- **要点**：Y 型的左右边界必须写成 x=ψ(y) 的形式，不能写成 y=…。例如 y=x² 在 Y 型中要改写成 x=√y（只取所需半支），y=x 改写成 x=y。
- **关键概念**：`x 关于 y 的函数`、`反解表达式`
- **相互关系**：这是 Y 型计算最常见的出错点，也是交换积分次序必须掌握的变形。
- **出处**：[陈哥 P99](https://www.bilibili.com/video/BV1husGzwEtZ?p=99)

### 圆域上下限的推导
- **要点**：由 y=√(2x−x²) 两边平方配方得 (x−1)²+y²=1，是圆心 (1,0)、半径 1 的上半圆；由 y=√(1−x²) 可得 x=±√(1−y²)，正号对应右半圆、负号对应左半圆。规律是根号前带正号取圆的上半部分、带负号取下部分；x=1±√(…) 中加号取右半、减号取左半。
- **关键概念**：`配方`、`上半圆`、`左半圆/右半圆`
- **出处**：[陈哥 P101](https://www.bilibili.com/video/BV1husGzwEtZ?p=101)

### 二重积分计算的题型与易错点
- **要点**：第一步永远是画积分区域图。同一区域用 X 型与 Y 型算出的结果必然相同；若 Y 型下区域需拆成上下（或左右）两块，则写成两个二次积分再相加。若图形既能当 x 型又能当 y 型，优先选 x 型（不必改函数）。只有一条边界曲线（圆、半圆）通常改用极坐标；两条边界曲线：上下合抱用 X 型，左右合抱用 Y 型；三条及以上边界曲线：比较垂直于坐标轴的边界曲线数量，垂直于 x 轴的多用 X 型、垂直于 y 轴的多用 Y 型，数量相等则两者皆可，此时看被积函数先积谁更容易。某些区域只适合一种类型，需先判断再动笔。
- **关键概念**：`画图`、`区域拆分`、`优先 x 型`、`边界曲线`
- **相互关系**：与定积分求面积的流程相同（画图—定类型—套公式）。
- **出处**：[陈哥 P99](https://www.bilibili.com/video/BV1husGzwEtZ?p=99)、[P100](https://www.bilibili.com/video/BV1husGzwEtZ?p=100)；[杰哥 P88](https://www.bilibili.com/video/BV1Up4y1Y76a?p=88)；[ok姐 P112](https://www.bilibili.com/video/BV1vm421s7mv?p=112)、[P113](https://www.bilibili.com/video/BV1vm421s7mv?p=113)

### 题型：由 y=x²、y=1/x、x=2 围成区域的积分次序选择
- **要点**：D 由 y=x²（开口朝上的抛物线）、y=1/x（一、三象限的双曲线，第三象限不用画）、x=2（垂直于 x 轴的直线）围成，关键交点是 y=x² 与 y=1/x 联立的解 (1,1)。选积分次序先看被积函数 x²/y²，两者难易差不多、看不出结果；再看区域中的穿越线：d 后是 x 就画从左到右的穿越线，d 后是 y 就画从下到上的穿越线。本题横着画穿越线要以交点为界分成上下两块、得列两个式子，竖着画则始终「先穿 y=1/x、后穿 y=x²」，只画一次即可，故选择先对 y 积分。定限：x 的范围 1∼2，y 的范围 1/x∼x²，计算 ∫₁²x²dx∫\_\{1/x\}\^\{x²\}(1/y²)dy=∫₁²x²·(−1/y)|\_\{1/x\}\^\{x²\}dx=∫₁²(x³−1)dx=11/4。
- **关键概念**：`穿越线少的先积分`、`横穿（d 后是 x）`、`竖穿（d 后是 y）`、`列式个数`、`11/4`
- **相互关系**：是「积分次序选择」两条原则的具体运用。
- **出处**：[学士帽 P84](https://www.bilibili.com/video/BV1X4411J792?p=84)

### 题型：四分之一圆域的二重积分与上下限整理
- **要点**：D 为 x²+y²≤1 在第一象限的部分，即以原点为圆心、半径 1 的四分之一圆。看被积函数后决定先对 x 积分（d 后是 x），则外层是 dy：y 的范围 0∼1。内层画从左到右的穿越线，先穿过 y 轴即 x=0 为下限，后穿过圆为上限，须把圆的表达式整理成 x=±√(1−y²)，再按「第一象限中 x 恒大于零」舍去负号。计算时内层把 y² 当常数提到积分号外，x 的原函数为 ½x²，代入上下限时根号与平方抵消，得 ½∫₀¹(y²−y⁴)dy=½(⅓−⅕)=1/15。遇到圆域或椭圆域时直角坐标系往往不便，应考虑改用极坐标。
- **关键概念**：`圆域 D`、`上限整理成 x=…y`、`开方后按象限取舍`、`常数倍提到积分号外`
- **相互关系**：引出极坐标系下二重积分的计算。
- **出处**：[学士帽 P84](https://www.bilibili.com/video/BV1X4411J792?p=84)

### 非初等函数的积分（超越积分）
- **要点**：e\^\{x²\}、sin x/x、cos x/x、sin x²、cos x²、arctan x、e\^\{−x²\} 等函数的原函数不能用初等函数表示，称非初等函数的积分（俗称超越积分），积不出来，结果不必记忆。
- **关键概念**：`非初等函数积分`、`超越积分`、`无初等原函数`
- **相互关系**：这类函数出现在被积函数中时，直接决定积分区域该选 X 型还是 Y 型。
- **出处**：[陈哥 P100](https://www.bilibili.com/video/BV1husGzwEtZ?p=100)；[杰哥 P89](https://www.bilibili.com/video/BV1Up4y1Y76a?p=89)

### 由被积函数反推积分类型
- **要点**：被积函数含只含 x 的「积不出来」的式子时，x 不能作内层积分变量，故内层只能是 dy、dx 在前，必须选 X 型；含只含 y 的此类式子（如 sin y/y、cos y²）时，内层只能是 dx、dy 在前，必须选 Y 型；一种顺序算不下去就换另一种。被积函数含复合函数时，先看剩余部分能否凑成内层函数的微分（只差一个常数因子即可）。
- **关键概念**：`内层积分变量`、`选取合适的积分类型`、`换顺序`、`凑微分`
- **相互关系**：与「先看区域像什么型」是两条不同的思路。
- **出处**：[陈哥 P100](https://www.bilibili.com/video/BV1husGzwEtZ?p=100)；[杰哥 P89](https://www.bilibili.com/video/BV1Up4y1Y76a?p=89)；[ok姐 P113](https://www.bilibili.com/video/BV1vm421s7mv?p=113)

### 交换积分次序：含义与步骤
- **要点**：研究对象是二次积分，把 X 型二次积分化为 Y 型（或反向），原因常是原次序下内层积不出来（被积函数对某变量是超越积分时必须先交换次序）。步骤：①由上下限写出四条边界曲线（外层上下限给出两条常数直线，内层上下限给出两条曲线）；②画出积分区域；③按新类型重新定限，若区域需拆分则拆开分别写再相加。
- **关键概念**：`交换积分次序`、`四条边界曲线`、`重新定限`、`超越积分`
- **相互关系**：是「非初等函数积分」问题的通用解法，属选择题、填空题高频考点；本质是「二次积分 ↔ 积分区域」的双向转换。
- **出处**：[陈哥 P101](https://www.bilibili.com/video/BV1husGzwEtZ?p=101)；[杰哥 P90](https://www.bilibili.com/video/BV1Up4y1Y76a?p=90)；[米哥 P117](https://www.bilibili.com/video/BV1swAWerEzS?p=117)；[ok姐 P113](https://www.bilibili.com/video/BV1vm421s7mv?p=113)

### 交换积分次序的易错点
- **要点**：交换积分次序绝不是把上下限位置直接对调（不能直接照搬），必须经过画区域、重定限的完整过程。若题目只说「计算」而内层含积不出来的函数，要主动想到先交换次序再计算。上下限都被题目定好往往是「坑」，提示需要交换次序。
- **关键概念**：`不能直接对调上下限`、`先换序再计算`
- **出处**：[陈哥 P101](https://www.bilibili.com/video/BV1husGzwEtZ?p=101)；[杰哥 P90](https://www.bilibili.com/video/BV1Up4y1Y76a?p=90)

### 极坐标的两个要素与极角的正负约定
- **要点**：极坐标用「极径 + 极角」两个量确定平面上一点的位置。极径 r（或 ρ）是点到极点（原点）的距离，恒有 r≥0；极角 θ 是极径与极轴（x 轴正半轴）所成的角，通常取 0 到 2π。逆时针量得的角为正角；极轴下方的点按顺时针量角时记作负角，也可改用 2π 减去该角表示，两种取法对应不同的积分上下限。是区域跨越极轴时 θ 下限写负值还是写大角度的依据。
- **关键概念**：`极点`、`极轴`、`极径 r`、`极角 θ`、`负角`
- **出处**：[陈哥 P102](https://www.bilibili.com/video/BV1husGzwEtZ?p=102)、[P103](https://www.bilibili.com/video/BV1husGzwEtZ?p=103)；[杰哥 P91](https://www.bilibili.com/video/BV1Up4y1Y76a?p=91)；[ok姐 P114](https://www.bilibili.com/video/BV1vm421s7mv?p=114)

### 直角坐标与极坐标的互化公式
- **要点**：由直角三角形「邻边比斜边」「对边比斜边」得 x=r cos θ、y=r sin θ；两式平方相加得 x²+y²=r²。这三条是极坐标二重积分「换被积函数」一步的依据；反向也可由 r cos θ、r sin θ 配出 x、y。极坐标下面积元素为 dσ=r dr dθ（或 ρ dρ dθ），这个 r 不能漏。
- **关键概念**：`x=r cosθ`、`y=r sinθ`、`x²+y²=r²`、`dxdy=r dr dθ`、`面积元素`
- **相互关系**：本质是换元。
- **出处**：[陈哥 P102](https://www.bilibili.com/video/BV1husGzwEtZ?p=102)、[P103](https://www.bilibili.com/video/BV1husGzwEtZ?p=103)；[杰哥 P91](https://www.bilibili.com/video/BV1Up4y1Y76a?p=91)；[米哥 P119](https://www.bilibili.com/video/BV1swAWerEzS?p=119)、[P120](https://www.bilibili.com/video/BV1swAWerEzS?p=120)；[ok姐 P114](https://www.bilibili.com/video/BV1vm421s7mv?p=114)

### 圆的极坐标方程
- **要点**：把圆的直角坐标方程中的 x²+y² 换成 r²、x 换成 r cos θ、y 换成 r sin θ，两边约去 r 即得。三种常用结果：圆心在原点、半径 a 的圆为 r=a（x²+y²≤a² 时 r∈[0,a]）；圆心在 x 轴上且过原点的圆（(x−a)²+y²=a²）为 r=2a cos θ、θ∈[−π/2,π/2]；圆心在 y 轴上且过原点的圆（x²+(y−a)²=a²）为 r=2a sin θ、θ∈[0,π]；圆环域 θ∈[0,2π]。写成等号表示边界曲线，改成「小于等于」表示圆内区域；专升本考圆的化极坐标占绝大多数。
- **关键概念**：`r=a`、`r=2a cosθ`、`r=2a sinθ`
- **相互关系**：是极坐标题的难点；r 的上限常常就是圆的极坐标方程（如 2cos θ、2sin θ），所以圆化极坐标必须先练熟。
- **出处**：[陈哥 P102](https://www.bilibili.com/video/BV1husGzwEtZ?p=102)、[P103](https://www.bilibili.com/video/BV1husGzwEtZ?p=103)；[杰哥 P91](https://www.bilibili.com/video/BV1Up4y1Y76a?p=91)；[米哥 P119](https://www.bilibili.com/video/BV1swAWerEzS?p=119)；[ok姐 P114](https://www.bilibili.com/video/BV1vm421s7mv?p=114)、[P115](https://www.bilibili.com/video/BV1vm421s7mv?p=115)

### 直线的极坐标方程
- **要点**：同样代入互化公式化简即可，例如 y=x+1 化为 r=1/(sin θ−cos θ)，y=1−x 化为 r=1/(sin θ+cos θ)。专升本很少考直线化极坐标，但补线题里会用到。
- **关键概念**：`r=1/(sinθ+cosθ)`
- **出处**：[陈哥 P102](https://www.bilibili.com/video/BV1husGzwEtZ?p=102)、[P103](https://www.bilibili.com/video/BV1husGzwEtZ?p=103)

### 直角坐标二重积分化为极坐标的「三换」
- **要点**：换三处——①积分区域 D 换成极坐标表示；②被积函数中的 x、y 换成 r cos θ、r sin θ；③面积元素 dxdy 换成 r dr dθ（或 r dθ dr）。多出来的那个 r 是固定写法，绝不能丢。
- **关键概念**：`三换`、`dxdy=r dθ dr`、`面积元素`
- **出处**：[陈哥 P102](https://www.bilibili.com/video/BV1husGzwEtZ?p=102)

### 极坐标二重积分的二次积分框架
- **要点**：框架唯一固定——外层 dθ 在前，内层 r dr 在后：∬_D f dxdy=∫_α^β dθ ∫\_\{r₁(θ)\}\^\{r₂(θ)\} f(r cos θ, r sin θ) r dr。与直角坐标下 X 型、Y 型各有各的框架不同。计算时先对 r 积分，此时 θ 视为常数；积出的结果再放入外层对 θ 积分。若 θ 与 r 的四个上下限全是常数，且被积函数能分离为「只含 θ」与「只含 r」两部分之积，可把二次积分拆成两个定积分相乘，分别算出后相乘，能大幅省算；只要有一个上下限含变量（如上限为 2cos θ）就不能拆。
- **关键概念**：`dθ 在前`、`r dr 在后`、`二次积分框架`、`常数上下限`、`两个定积分相乘`
- **出处**：[陈哥 P102](https://www.bilibili.com/video/BV1husGzwEtZ?p=102)、[P103](https://www.bilibili.com/video/BV1husGzwEtZ?p=103)；[杰哥 P91](https://www.bilibili.com/video/BV1Up4y1Y76a?p=91)；[ok姐 P114](https://www.bilibili.com/video/BV1vm421s7mv?p=114)

### θ 的上下限：扫描法
- **要点**：把极轴绕极点逆时针旋转，刚接触积分区域时的角为下限，刚要离开区域时的角为上限（角度由原点出发作积分区域的两条切线确定）。θ 的上下限一定是常数，不能写成含 θ 的式子。区域要绕极点转满一整圈才扫完时取 0 到 2π；只占半圈时取 α 到 β；边界落在极轴下方时用负角作下限。极点在区域内时 θ 为 0→2π。
- **关键概念**：`扫描法`、`α 到 β`、`两条切线定角度`
- **出处**：[陈哥 P102](https://www.bilibili.com/video/BV1husGzwEtZ?p=102)、[P103](https://www.bilibili.com/video/BV1husGzwEtZ?p=103)；[杰哥 P91](https://www.bilibili.com/video/BV1Up4y1Y76a?p=91)；[ok姐 P114](https://www.bilibili.com/video/BV1vm421s7mv?p=114)

### r 的上下限：射线穿出法
- **要点**：从极点引一条射线穿过区域，先交到的边界曲线表达式写下限，后交到的写上限，口诀「先交写下限，后交写上限」；若射线起点已在区域内，下限为 0。可靠算法是把 x=r cos θ、y=r sin θ、x²+y²=r² 代入区域边界函数式解出 r。半径恒非负。当 r 上限不是常数时，要找同时含 r 与 θ 的直角三角形求两者关系，如半圆由「直径所对圆周角为直角」得 r=2cos θ。
- **关键概念**：`先交写下限`、`后交写上限`、`射线穿出`、`代入边界函数求 r`
- **出处**：[陈哥 P102](https://www.bilibili.com/video/BV1husGzwEtZ?p=102)；[杰哥 P91](https://www.bilibili.com/video/BV1Up4y1Y76a?p=91)；[ok姐 P114](https://www.bilibili.com/video/BV1vm421s7mv?p=114)、[P115](https://www.bilibili.com/video/BV1vm421s7mv?p=115)

### 极坐标二重积分按极点位置的三种类型
- **要点**：极坐标下二重积分的形式是固定的，先对 r 积分再对 θ 积分，写作 ∫dθ∫f(r cos θ, r sin θ) r dr，被积函数中多乘一个 r、后面是 dr。r 的范围统一按「从极点向外发一根射线，先经过的为下限、后经过的为上限」来定，不管属于哪一种形式都一样——从极点出发时先经过极点本身，所以 r 最小是 0，后经过的那条边界线就是 r 的上限；θ 的范围由积分区域内任意点与极点连线同极轴的夹角的最小值、最大值决定。按极点位置分三种类型：一是极点在积分区域 D 内部（如极点就是圆心），θ 取 0∼2π，r 从 0 到半径（正规圆的上限就是半径）；二是极点在积分区域 D 的边界上（小扇形），θ 从最小角 α 到最大角 β，r 从 0 到圆域表达式 r(θ)；三是极点在积分区域 D 的外部（考得少，作简单了解），θ 仍取 α∼β，r 的下限、上限分别是射线先穿、后穿的两段圆弧表达式 r₁(θ)、r₂(θ)。求 r 的上限要由边界方程反解出 r：如由 x²+y²=2y 得 r²=2r sin θ，两边消去一个 r，得 r=2sin θ；上下限必须写成 r= 谁的形式。
- **关键概念**：`先对 r 后对 θ`、`向外发射线`、`r 的下限为 0`、`极点在区域内部/边界/外部`、`r(θ)`
- **相互关系**：三种类型判定 r 的思路完全一样，只是 θ 与 r 上下限的具体形式不同。
- **出处**：[学士帽 P85](https://www.bilibili.com/video/BV1X4411J792?p=85)、[P86](https://www.bilibili.com/video/BV1X4411J792?p=86)

### 极坐标二重积分的适用类型
- **要点**：两种情形优先考虑极坐标：①积分区域是圆或圆的一部分（半圆、扇形、圆环、弧线）；②被积函数含 x²+y² 或 √(x²+y²)、y/x 等结构。两者只要满足其一即可考虑。圆、圆环、扇形等区域用极坐标远比直角坐标简单。
- **关键概念**：`圆或圆的一部分`、`x²+y²`、`与圆相关的区域`
- **出处**：[陈哥 P102](https://www.bilibili.com/video/BV1husGzwEtZ?p=102)、[P103](https://www.bilibili.com/video/BV1husGzwEtZ?p=103)；[杰哥 P91](https://www.bilibili.com/video/BV1Up4y1Y76a?p=91)；[ok姐 P114](https://www.bilibili.com/video/BV1vm421s7mv?p=114)

### 题型：圆环域上的计算
- **要点**：两同心圆围成的圆环，θ 取 0 到 2π（绕极点一整圈才扫完），r 取内圆到外圆。内层积分常出现 r³ 一类幂函数，外层多为 cos²θ，用降幂公式 cos²θ=(1+cos2θ)/2 后再积分。
- **关键概念**：`圆环`、`降幂公式`、`r³`
- **出处**：[陈哥 P103](https://www.bilibili.com/video/BV1husGzwEtZ?p=103)

### 题型：被积函数含 arctan(y/x)
- **要点**：把 arctan(y/x) 中的 y、x 分别换成 r sin θ、r cos θ，约去 r 后化为 arctan(tan θ)，反三角函数套三角函数的结果就是 θ，被积函数由繁变简。换完后积分区域由两条直线夹出，θ 的下限、上限就是两条直线的倾斜角（由斜率反查 tan 值确定）。
- **关键概念**：`arctan(y/x)`、`arctan(tanθ)=θ`
- **出处**：[陈哥 P103](https://www.bilibili.com/video/BV1husGzwEtZ?p=103)

### 题型：极坐标二次积分反化为直角坐标二次积分
- **要点**：先把 r 的范围两边同乘 r，凑出 r cos θ、r sin θ，从而把 r 的不等式翻译回 x、y 的不等式；配方后认出圆（如 r≤cos θ 对应 x²+y²≤x，即圆心 (½,0)、半径 ½ 的圆），再按 X 型或 Y 型写二次积分。区域所在象限决定取上半圆还是整圆；写上限时要写成含 x 的表达式，如 √(x−x²)。
- **关键概念**：`两边乘 r`、`配方`、`X 型 / Y 型`
- **出处**：[陈哥 P103](https://www.bilibili.com/video/BV1husGzwEtZ?p=103)

### 题型：区域由「圆 + 直线」围成
- **要点**：先画图确定区域落在哪一象限，再定 θ。若区域是圆上被两条直线切出的一块，θ 由两条直线的倾斜角给出；r 的下限多为 0，上限是圆的极坐标方程。若射线起点不在区域内则需分段，分段麻烦时改用负角起算，把 θ 写成一个连续区间。
- **关键概念**：`倾斜角`、`负角起算`、`连续区间`
- **出处**：[陈哥 P103](https://www.bilibili.com/video/BV1husGzwEtZ?p=103)

### 题型：被积函数含定值常数的二重积分
- **要点**：形如被积函数中带一个待求的常数 A（A 就是整个二重积分的值）时，令该二重积分等于 A，两边同时再取一次二重积分，利用「对 1 作二重积分等于区域面积」的性质，得到关于 A 的方程解出 A。
- **关键概念**：`设 A`、`二重积分是常数`、`区域面积`
- **出处**：[陈哥 P103](https://www.bilibili.com/video/BV1husGzwEtZ?p=103)

### 极坐标计算二重积分的题型与套路
- **要点**：常见题型是「把直角坐标的二次积分化为极坐标形式」与「直接在圆、圆环区域上用极坐标计算」。前者先由上下限反推边界曲线并画图；后者常需先用 x²+y²=ρ² 等关系化简被积函数。区域为「正方形挖去圆」一类时，用积分区域可加性拆成两个积分，正方形部分用直角坐标、圆部分用极坐标。
- **关键概念**：`区域可加性`、`x²+y²=ρ²`
- **出处**：[ok姐 P115](https://www.bilibili.com/video/BV1vm421s7mv?p=115)

### 极坐标二重积分的常见易错点
- **要点**：①忘记写那个 r；②区域只在上半平面却按整圆取 θ（如已知 y≥0 时不能取 −π/2 到 π/2，应取 0 到 π/2）；③上下限含变量时误用「两个定积分相乘」；④化极坐标后没有把圆的边界曲线也一起换掉。
- **关键概念**：`区域范围`、`r 的遗漏`、`常数上下限`
- **出处**：[陈哥 P103](https://www.bilibili.com/video/BV1husGzwEtZ?p=103)

### sin 的奇次幂积分（凑微分）
- **要点**：算到 (8/3)∫_0\^\{π/2\} sin³θ dθ 时，把 sin³θ 写成 sinθ·sin²θ，再把 sinθ 调到 d 后面（∫sinθ dθ=−cosθ，负号提到积分号外），并用 sin²θ=1−cos²θ 把被积函数整理成只含 cosθ 的形式，最后按 ∫(1−cos²θ)d(cosθ) 积出。本题最终结果为 16/9。
- **关键概念**：`凑微分`、`sin²θ=1−cos²θ`、`奇次幂`、`16/9`
- **相互关系**：被积函数只有一个 sinθ 或一个 sin²θ 都能直接积，sinθ·sin²θ 才需要先整理成既有 sin 又有 cos 的形式。
- **出处**：[学士帽 P86](https://www.bilibili.com/video/BV1X4411J792?p=86)

### 二重积分的对称性（偶倍奇零）
- **要点**：若积分区域 D 关于 x 轴对称，则看被积函数 f(x,y) 关于 y 的奇偶性：关于 y 为奇函数时二重积分直接等于 0；关于 y 为偶函数时，等于在对称的一半区域上积分的 2 倍。若 D 关于 y 轴对称，则看 f(x,y) 关于 x 的奇偶性：关于 x 为奇函数时积分等于 0；为偶函数时等于一半区域上积分的 2 倍（取左半或右半均可）。关于哪个轴对称，就判断另一个变量的奇偶性，这是固定套路。
- **关键概念**：`关于 X 轴对称`、`关于 Y 轴对称`、`关于 y 的奇函数`、`偶倍奇零`
- **相互关系**：与一元定积分的「偶倍奇零」本质相同。
- **出处**：[陈哥 P104](https://www.bilibili.com/video/BV1husGzwEtZ?p=104)；[杰哥 P92](https://www.bilibili.com/video/BV1Up4y1Y76a?p=92)；[米哥 P118](https://www.bilibili.com/video/BV1swAWerEzS?p=118)

### 判断二元函数奇偶性的操作要点
- **要点**：判断关于 y 的奇偶性时，把 x 当作常数（可随手代成 1）；判断关于 x 的奇偶性时，把 y 当作常数。与求偏导、求极限时「对一个变量操作，其余视为常数」是同一个思想。二元函数没有绝对的「奇函数 / 偶函数」，必须说清是关于哪个变量。
- **关键概念**：`其余变量视为常数`、`内偶则偶`、`奇×奇=偶`
- **出处**：[陈哥 P104](https://www.bilibili.com/video/BV1husGzwEtZ?p=104)

### 对称性的解题流程
- **要点**：①画积分区域图；②看区域关于哪条轴对称；③判断被积函数关于另一变量的奇偶性；④奇函数项直接舍去写 0，剩下的偶函数项用「区域取一半 ×2」简化；⑤再按直角坐标或极坐标算出结果。被积函数为常数时，二重积分等于该常数乘区域面积，这一条常与对称性连用（如右半圆上对 1 积分即 ½ 圆面积）。被积函数为加减形式时必须拆成单项逐个判断；化简后只算一半区域时极易漏乘 2。
- **关键概念**：`拆项`、`区域取一半`、`被积函数为 1 时等于区域面积`
- **出处**：[陈哥 P104](https://www.bilibili.com/video/BV1husGzwEtZ?p=104)；[杰哥 P92](https://www.bilibili.com/video/BV1Up4y1Y76a?p=92)

### 三重积分的概念
- **要点**：三重积分求空间立体的质量。密度不均匀且为三元函数 f(x,y,z) 时，把立体同时沿 x、y、z 三向分割成小立方体，分割足够细时小块密度视为均匀，质量微元为 f(x,y,z)dv，累加取极限即得三重积分；可化为三次积分计算，积分次序可以调换。
- **关键概念**：`三重积分`、`质量微元`、`体积微元`、`三次积分`
- **相互关系**：与定积分求面积、二重积分求体积同属「分割求和取极限」。
- **出处**：[ok姐 P116](https://www.bilibili.com/video/BV1vm421s7mv?p=116)

### 第一类曲线积分（对弧长）
- **要点**：积分号位置出现 L 即曲线积分；ds 为第一类，dx（或 dy）为第二类。第一类曲线积分求曲边柱面面积（或曲线的质量）：曲线密度是单位长度的质量，称线密度；把曲线分割成小弧段，弧长微元为 ds，质量微元为 f(x,y)ds，累加取极限得 ∫_L f(x,y)ds；积分曲线闭合时在积分号上加圆圈。由勾股定理得 ds=√(dx²+dy²)；若曲线由参数方程 x=g(t)、y=h(t)（t∈[α,β]）给出，则 ∫_L f ds=∫_α^β f(g(t),h(t))√(g′²+h′²)dt；曲线由 y=y(x) 给出就取 x 为参数（ds=√(1+y′²)dx，上限取 x 范围），由 x=x(y) 给出就取 y 为参数；上下限一定下限小于上限。f≡k 时等于 k×曲线长。具有线性性质与积分区域可加性。圆用 x=R cos θ、y=R sin θ，由路径定 θ 范围。
- **关键概念**：`L`、`ds`、`弧长微元`、`线密度`、`第一类曲线积分`、`下限小于上限`
- **相互关系**：核心区别在方向性——第一类无方向，上下限必须由小到大；与定积分、二重积分、三重积分的定义思想一致；关键在于把曲线 L 表示成参数方程。
- **出处**：[杰哥 P133](https://www.bilibili.com/video/BV1Up4y1Y76a?p=133)；[米哥 P121](https://www.bilibili.com/video/BV1swAWerEzS?p=121)；[ok姐 P117](https://www.bilibili.com/video/BV1vm421s7mv?p=117)、[P118](https://www.bilibili.com/video/BV1vm421s7mv?p=118)、[P119](https://www.bilibili.com/video/BV1vm421s7mv?p=119)；[帆哥 P1](https://www.bilibili.com/video/BV1xxXZBKENv?p=1)

### 第二类曲线积分（对坐标）
- **要点**：求变力 F 沿曲线 L 对物体做功。把力分解为水平与竖直分量 F₁、F₂（或写作 F=P(x,y)i+Q(x,y)j），对应位移 dx、dy，微功为 P dx+Q dy；沿整条曲线累加即得对坐标的曲线积分 ∫_L P dx+Q dy（P 为 dx 前、Q 为 dy 前），物理意义是「变力沿曲线做功」。计算时把曲线 L 写成参数方程：若 x=g(t)、y=h(t)，则化为 ∫_α^β[P g′(t)+Q h′(t)]dt，上下限由路径方向决定（严格按起点到终点书写）；曲线由 y=g(x) 给出就取 x 为参数（把 y 换成 g(x)、dy 换成 g′dx），由 x=f(y) 给出就取 y 为参数；有向折线用积分区域可加性拆成几段分别计算。普通函数型换 y=g(x)、dy=g′dx，上下限按起点到终点；交换起点终点变号。
- **关键概念**：`第二型曲线积分`、`变力做功`、`P dx+Q dy`、`方向性`、`可加性`、`起点与终点`
- **相互关系**：与第一类（对弧长）曲线积分并列，区别在于被积表达式是 dx、dy 而非 ds，且与方向有关，方向相反时结果互为相反数，上下限没有大小限制；用区域可加性拆分时方向必须保持一致；第一类还需乘 √(1+y′²)。
- **出处**：[杰哥 P133](https://www.bilibili.com/video/BV1Up4y1Y76a?p=133)、[P134](https://www.bilibili.com/video/BV1Up4y1Y76a?p=134)；[米哥 P122](https://www.bilibili.com/video/BV1swAWerEzS?p=122)；[ok姐 P120](https://www.bilibili.com/video/BV1vm421s7mv?p=120)、[P121](https://www.bilibili.com/video/BV1vm421s7mv?p=121)；[帆哥 P1](https://www.bilibili.com/video/BV1xxXZBKENv?p=1)

### 曲线积分的直接代入法
- **要点**：当曲线方程非常简单时，把曲线关系代入被积式，连同 dx 一起换元（由 x=g(y) 求微分得到 dx），使被积式只剩一个变量，化为定积分，积分限由曲线起点终点的坐标范围确定。若曲线是圆等带根号的形式，代入后会更复杂，此时应改用格林公式；判断标准是「代进去能不能让式子变简单」。
- **关键概念**：`换元`、`化为定积分`、`积分限`
- **出处**：[杰哥 P134](https://www.bilibili.com/video/BV1Up4y1Y76a?p=134)

### 格林公式与成立条件
- **要点**：设 L 是封闭的正向边界曲线（记 ∮_L），围成平面区域 D 且所围区域内无「洞」，P、Q 在 D 上有一阶连续偏导数，则 ∮_L P dx+Q dy=∬_D(∂Q/∂x−∂P/∂y)dxdy。它是把曲线积分转化为二重积分的桥梁。方向人为规定逆时针为正（沿 L 行走时区域 D 始终在左手边：外边界逆时针、内边界顺时针）；若题给顺时针，须在二重积分前添一个负号。∬_D dxdy 就是区域面积，圆域用极坐标算最快。记忆要点：P 配 dx 却对 y 求偏导，Q 配 dy 却对 x 求偏导，是交错的；被积函数顺序不能颠倒。
- **关键概念**：`格林公式`、`正向边界（逆时针）`、`∂Q/∂x−∂P/∂y`、`逆正顺负`
- **相互关系**：考这一章必然连考二重积分；易错点是顺时针忘添负号、把 P 与 Q 认错（P 是 dx 前的函数）、漏 P 的负号。
- **出处**：[陈哥 P107](https://www.bilibili.com/video/BV1husGzwEtZ?p=107)；[杰哥 P135](https://www.bilibili.com/video/BV1Up4y1Y76a?p=135)；[米哥 P123](https://www.bilibili.com/video/BV1swAWerEzS?p=123)；[ok姐 P122](https://www.bilibili.com/video/BV1vm421s7mv?p=122)

### 格林公式题型一：L 本身封闭
- **要点**：区域为整圆一类封闭曲线时直接用格林公式：求两个偏导、作差、把二重积分化成「常数 × 区域面积」或转极坐标算出结果。
- **关键概念**：`封闭区域`、`区域面积`
- **相互关系**：被积函数为常数时二重积分等于该常数乘 D 的面积，是这类题最省事的一步。
- **出处**：[陈哥 P107](https://www.bilibili.com/video/BV1husGzwEtZ?p=107)

### 不封闭曲线的补线法
- **要点**：L 只是半圆周等不封闭曲线、直接代入又难算时，补一条直线使其封闭（补一条辅助线段与 L 一起围成封闭区域）再用格林公式；补上的直线最后必须减去其积分（「有借有还」，∫_L=∮\_\{L+BA\}−∫\_\{BA\}，前项用格林公式，后项用对坐标积分，真题常为零）。补线方向要与原曲线合成逆时针；补线前先写出该直线上的 x 范围、y 的取值以及 dy（常数的微分为零），后续计算会大幅简化。只能补直线；补曲线会使区域描述与回减都变得极难。补线段通常取坐标轴上的直线段，其 dy=0（或 dx=0），积分很容易算。
- **关键概念**：`补线`、`封闭区域`、`减去补线积分`、`逆时针方向`
- **相互关系**：补线后整体方向必须是逆时针（正向），否则格林公式要变号。
- **出处**：[陈哥 P107](https://www.bilibili.com/video/BV1husGzwEtZ?p=107)；[杰哥 P135](https://www.bilibili.com/video/BV1Up4y1Y76a?p=135)；[米哥 P124](https://www.bilibili.com/video/BV1swAWerEzS?p=124)

### 积分与路径无关
- **要点**：对 ∫_L P dx+Q dy，若 ∂P/∂y=∂Q/∂x（且偏导连续），则积分与路径无关，只与起点、终点有关。此时可改取便于计算的路径——通常取「先水平后竖直」的折线或起点到终点的直线；折线中有一段 y（或 x）为常数，则该段 dy（或 dx）为零，被积式中大量项直接消失。解题套路：①写清 P、Q；②分别求 ∂P/∂y、∂Q/∂x（另一变量视为常数）；③相等则改取折线路径（一段 y=0 的水平线 + 一段 x=1 的竖直线）；④水平段 dy=0、竖直段 dx=0，代入后各化为定积分相加。证明「积分与路径无关」就是验证这两个偏导相等。
- **关键概念**：`∂P/∂y=∂Q/∂x`、`折线路径`、`起点与终点`、`路径无关`
- **相互关系**：格林公式的被积函数正是 ∂Q/∂x−∂P/∂y；偏导相等时该二重积分为 0，正好呼应路径无关。
- **出处**：[陈哥 P107](https://www.bilibili.com/video/BV1husGzwEtZ?p=107)；[杰哥 P136](https://www.bilibili.com/video/BV1Up4y1Y76a?p=136)；[米哥 P125](https://www.bilibili.com/video/BV1swAWerEzS?p=125)；[ok姐 P123](https://www.bilibili.com/video/BV1vm421s7mv?p=123)


### 从一重积分到二重积分
- **要点**：一重积分即定积分，是对一元函数 $y=f(x)$ 积分，几何上求曲边梯形的面积；二重积分是对二元函数 $z=f(x,y)$ 积分，几何上求曲顶柱体的体积。曲顶柱体的底是积分区域在 $xOy$ 面上的投影，侧面垂直于底面，顶是一张曲面。
- **关键概念**：`一重积分`、`定积分`、`曲边梯形`、`曲顶柱体`、`投影`
- **相互关系**：一重积分求「曲线下方的面积」，二重积分求「曲面下方的体积」，多了一维但思想一致；曲顶柱体的底面在二重积分中称为积分区域 $D$。
- **出处**：[石头 P77](https://www.bilibili.com/video/BV18CL26WEJ3?p=77)

### 二重积分的定义、记号与面积元素
- **要点**：把积分区域分成 $n$ 个小块，第 $i$ 块面积记 $\Delta\sigma_i$，以块内任一点的函数值为高作和 $\sum\_\{i=1\}\^\{n\}f(\xi_i,\eta_i)\Delta\sigma_i$，再令各小块直径的最大值 $\lambda\to0$ 取极限，所得极限即二重积分 $\iint_D f(x,y)\,d\sigma$。其中 $f(x,y)$ 是被积函数，$D$ 是积分区域，$d\sigma$ 是面积元素，在直角坐标系下 $d\sigma=dx\,dy$。
- **关键概念**：`分割、近似、求和、取极限`、`$\iint_D f(x,y)\,d\sigma$`、`$d\sigma=dx\,dy$`
- **相互关系**：与定积分「分割—近似—求和—取极限」完全同构，只是把区间换成平面区域、把 $\Delta x$ 换成 $\Delta\sigma$；用两个积分号是因为要在两个方向上累加。
- **出处**：[石头 P77](https://www.bilibili.com/video/BV18CL26WEJ3?p=77)

### 二重积分的几何意义
- **要点**：当 $f(x,y)\ge0$ 时二重积分等于曲顶柱体的体积；当 $f(x,y)\le0$ 时等于体积的相反数；有正有负时等于上方部分体积减去下方部分体积，即所谓「数字体积」。计算时不必理会几何意义，算出正就是正、算出负就是负。
- **关键概念**：`数字体积`、`正体积与负体积`
- **相互关系**：与定积分的「数字面积」一一对应——$x$ 轴上方为正、下方为负；考试一般只考计算，几何意义了解即可。
- **出处**：[石头 P77](https://www.bilibili.com/video/BV18CL26WEJ3?p=77)

### 二重积分的七条性质
- **要点**：常数因子可提到积分号外；和与差的积分等于积分的和与差；积分区域可加（$D=D_1+D_2$ 时可拆成两块相加）；$f\equiv1$ 时积分等于区域面积；若 $f\le g$ 则积分也满足 $\le$；估值定理给出积分介于「区域面积乘最小值」与「区域面积乘最大值」之间；中值定理说存在一点使积分等于该点函数值乘区域面积。
- **关键概念**：`线性性质`、`区域可加性`、`保号性`、`估值定理`、`中值定理`
- **相互关系**：这七条与定积分的性质一一对应，原理相同不必死记；其中「被积函数为 $1$ 求面积」与「比较大小」两条最常出题。
- **出处**：[石头 P78](https://www.bilibili.com/video/BV18CL26WEJ3?p=78)

### 被积函数为 1 时求区域面积
- **要点**：$\iint_D 1\,dx\,dy$ 在数值上等于积分区域 $D$ 的面积。遇到被积函数是常数（尤其是 $1$）的题目，先想是不是在求面积，再把 $D$ 画出来按几何公式（圆环面积、矩形面积等）算出结果。
- **关键概念**：`$S_D=\iint_D dx\,dy$`、`高为 1 的平顶柱体`
- **相互关系**：这是「高为 $1$ 的平顶柱体体积在数值上等于底面积」的直接推论；求面积的题不一定用定积分，也可能用二重积分。
- **出处**：[石头 P78](https://www.bilibili.com/video/BV18CL26WEJ3?p=78)

### 比较两个二重积分的大小
- **要点**：同一积分区域上比较两个二重积分的大小，只需比较被积函数的大小。做选择题时可先找出三个被积函数中最「基础」的那个（另两个都由它变形而来），它必居中间；再在区域范围内取一个特殊值代入，即可判断大小顺序。
- **关键概念**：`比较被积函数`、`找中间值`、`取特殊值`
- **相互关系**：比较函数大小也可用做差判单调性、拉格朗日中值定理等方法，但选择题用特值法最快；验证出两端的大小关系后，中间那个无需再证。
- **出处**：[石头 P78](https://www.bilibili.com/video/BV18CL26WEJ3?p=78)

### 二重积分化为两次定积分
- **要点**：把曲顶柱体沿一个方向切成无数薄片，每一片的截面积是一个定积分（内层），再把所有截面积沿垂直方向累加即得体积（外层），于是 $\iint_D f(x,y)\,dx\,dy=\int_a^b\left(\int\_\{\varphi\_1(x)\}\^\{\varphi\_2(x)\}f(x,y)\,dy\right)dx$。内层积分上下限是函数、积出来仍是函数，外层积分上下限是常数、积出来才是数值。
- **关键概念**：`两次定积分`、`先一后二`、`内层积分`、`外层积分`
- **相互关系**：两次积分的积分变量相互垂直；内层上下限含外层变量，因此计算时必须先算内层再算外层，顺序不能颠倒。
- **出处**：[石头 P79](https://www.bilibili.com/video/BV18CL26WEJ3?p=79)

### X 型积分区域及其定限
- **要点**：若区域的左右两侧是竖直线或交点（边界在 $x$ 轴方向上取常数值），称 X 型区域，先对 $y$ 积、后对 $x$ 积。定限时先定 $x$ 的上下限（左边界到右边界，是常数），再沿 $y$ 轴方向穿过区域，先穿过的边界线 $y=\varphi_1(x)$ 为下限、后穿过的 $y=\varphi_2(x)$ 为上限，二者都是 $x$ 的函数。
- **关键概念**：`X 型区域`、`先对 $y$ 积`、`$x\in[a,b]$`、`$y\in[\varphi_1(x),\varphi_2(x)]$`
- **相互关系**：X 型与 Y 型的区别只是「切片方向」不同；可 X 可 Y 时优先选 X 型，因为不必把边界曲线改写成反函数。
- **出处**：[石头 P79](https://www.bilibili.com/video/BV18CL26WEJ3?p=79)

### Y 型积分区域及其定限
- **要点**：若区域的上下两侧是水平线或交点（边界在 $y$ 轴方向上取常数值），称 Y 型区域，先对 $x$ 积、后对 $y$ 积。先定 $y$ 的上下限（下边界到上边界，是常数），再沿 $x$ 轴方向穿过区域定出 $x$ 的上下限，二者都是 $y$ 的函数。
- **关键概念**：`Y 型区域`、`先对 $x$ 积`、`$y\in[c,d]$`、`$x\in[\psi_1(y),\psi_2(y)]$`
- **相互关系**：对 $x$ 积分时上下限必须是 $y$ 的函数，对 $y$ 积分时上下限必须是 $x$ 的函数，写反即错；区域若上下换边，需拆成两块分别积分。
- **出处**：[石头 P79](https://www.bilibili.com/video/BV18CL26WEJ3?p=79)

### 计算三步走与定限口诀
- **要点**：三步为「画图—定型—求解」：先画出积分区域 $D$，再根据边界有无水平线、竖直线以及交点在左右还是上下判断是 X 型还是 Y 型，最后化为两次定积分并逐次计算。定限口诀是「后积的先定线、先积的后定线」，且都按坐标轴从负方向到正方向确定下限与上限。
- **关键概念**：`画图`、`定型`、`求解`、`后积先定线`
- **相互关系**：判断类型时若找不出水平线或竖直线，就看两个交点在哪两侧——在左右为 X 型，在上下为 Y 型；区域不封闭或需拆分时，要先联立两曲线方程求出交点坐标。
- **出处**：[石头 P79](https://www.bilibili.com/video/BV18CL26WEJ3?p=79)

### 画积分区域的常考图形
- **要点**：一次函数 $y=kx+b$ 先找 $y$ 轴截距 $b$ 再按斜率作直线；水平线 $y=a$ 与竖直线 $x=a$ 直接在坐标轴上找点；二次曲线常考 $y=x^2$、$y=-x^2$、$x=y^2$、$y=\sqrt x$，注意 $y=\sqrt x$ 只取上半支；圆常考 $x^2+y^2=a^2$、$(x-a)^2+y^2=a^2$（展开即 $x^2+y^2=2ax$）以及上半圆 $y=\sqrt{a^2-x^2}$。
- **关键概念**：`斜率与截距`、`$x=y^2$`、`$y=\sqrt x$`、`$x^2+y^2=2ax$`、`上半圆`
- **相互关系**：开方时若不能确定正负，要写出 $y=\pm\sqrt x$ 两支；积分区域是圆或圆环时一般改用极坐标计算，画图时圆心必在坐标轴上。
- **出处**：[石头 P79](https://www.bilibili.com/video/BV18CL26WEJ3?p=79)

### 交换积分次序的方法
- **要点**：题目给出的二次积分若内层积不出来（如被积函数含 $e\^\{-y\^2\}$），就要交换积分次序。做法是先由内层积分的上下限还原出边界曲线、必要时用外层上下限补足，画出积分区域 $D$；再按新的积分顺序重新定限。
- **关键概念**：`交换积分次序`、`由上下限还原区域`、`重新定限`
- **相互关系**：还原区域时先看内层（后面那个积分）的上下限确定曲线，不够再用外层上下限补；图画得不准会导致区域判断错误，比例要画得大致准确。
- **出处**：[石头 P80](https://www.bilibili.com/video/BV18CL26WEJ3?p=80)

### 可 X 可 Y 时的选型技巧
- **要点**：区域既可看作 X 型也可看作 Y 型时，看被积函数：若它是关于 $y$ 的复杂函数，选 Y 型（先对 $x$ 积，此时复杂部分视为常数），若关于 $x$ 复杂则选 X 型（先对 $y$ 积）；若被积函数很简单，默认选 X 型即可。
- **关键概念**：`选型技巧`、`先积的变量视为常数`、`默认选 X 型`
- **相互关系**：选型的目的是让内层积分能积出来或变得更简单；若某个型必须把区域拆成两块，说明它不是最佳选择。
- **出处**：[石头 P80](https://www.bilibili.com/video/BV18CL26WEJ3?p=80)

### 极坐标与直角坐标的转换
- **要点**：极坐标用「角度 $\theta$ 加距离 $r$」定位点，与直角坐标共用原点、以 $x$ 轴正方向为极轴。三组基本关系是 $x=r\cos\theta$、$y=r\sin\theta$、$r^2=x^2+y^2$，三者互为补充，转换时按需取用。
- **关键概念**：`极坐标`、`极轴`、`$x=r\cos\theta$`、`$y=r\sin\theta$`、`$r^2=x^2+y^2$`
- **相互关系**：极坐标与直角坐标下的点一一对应；把区域边界曲线化为极坐标时，目标是把它写成 $r=r(\theta)$ 的形式，且 $r\ge0$ 恒成立。
- **出处**：[石头 P81](https://www.bilibili.com/video/BV18CL26WEJ3?p=81)

### 极坐标下的面积元素
- **要点**：用等角度射线与等半径圆弧把小区域切成细网格，网格两条边长分别是 $dr$ 与 $r\,d\theta$，故面积元素 $d\sigma=r\,dr\,d\theta$，即 $dx\,dy=r\,dr\,d\theta$。于是极坐标下的二重积分写为 $\iint_D f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta$。
- **关键概念**：`面积元素`、`$d\sigma=r\,dr\,d\theta$`、`$dx\,dy=r\,dr\,d\theta$`
- **相互关系**：式中多出来的 $r$ 来自弧长公式 $l=r\theta$，是最容易漏写的地方，一旦漏掉整个结果全错。
- **出处**：[石头 P81](https://www.bilibili.com/video/BV18CL26WEJ3?p=81)

### 极坐标下 θ 与 r 的定限规则
- **要点**：$\theta$ 的上下限由射线从极轴出发逆时针旋转确定：进入积分区域时的角度为下限，离开时的角度为上限。$r$ 的上下限由从极点发出的射线确定：先穿过的边界曲线 $r=\varphi_1(\theta)$ 为下限，后穿过的 $r=\varphi_2(\theta)$ 为上限；若射线一出发就进入区域，则下限为 $0$。
- **关键概念**：`$\theta$ 的定限`、`$r$ 的定限`、`进入定下限、离开定上限`
- **相互关系**：按极点位置分三种情况——极点在区域外、在区域边界上、在区域内，前两种 $\theta\in[\alpha,\beta]$，第三种 $\theta\in[0,2\pi]$ 且 $r$ 的下限为 $0$；边界曲线必须先写成 $r=r(\theta)$ 才能代入。
- **出处**：[石头 P81](https://www.bilibili.com/video/BV18CL26WEJ3?p=81)

### 极坐标的适用情形与积分次序
- **要点**：积分区域是圆、圆环、扇形（或它们的一部分），或被积函数中含有 $x^2+y^2$、$\frac yx$ 时，用极坐标最方便。极坐标下永远先对 $r$ 积、后对 $\theta$ 积，不涉及交换积分次序。
- **关键概念**：`圆与圆环`、`扇形`、`$x^2+y^2$`、`$\frac yx$`、`先 $r$ 后 $\theta$`
- **相互关系**：按「后积先定线」原则，$\theta$ 写在前面的积分号上、要最先定限，$r$ 的上下限后定；边界是直线时 $r$ 的下限往往很复杂，这类题一般只要求列式。
- **出处**：[石头 P81](https://www.bilibili.com/video/BV18CL26WEJ3?p=81)

### 直角坐标二次积分化为极坐标形式
- **要点**：给出直角坐标下的二次积分要求化为极坐标形式时，先由内层上下限还原边界曲线、外层上下限补足，画出积分区域；再按极坐标定限规则写出 $\theta$、$r$ 的范围，并把被积函数与 $dx\,dy$ 分别换成极坐标表达式与 $r\,dr\,d\theta$。
- **关键概念**：`还原积分区域`、`逐项替换`、`$r\,dr\,d\theta$`
- **相互关系**：当区域边界含直线时，$r$ 的下限常化为 $\frac{1}{\sin\theta+\cos\theta}$ 这类复杂式子，题目通常只要求列出式子（填空或选择），不要求算出最终数值。
- **出处**：[石头 P81](https://www.bilibili.com/video/BV18CL26WEJ3?p=81)

### 对弧长的曲线积分的概念
- **要点**：对弧长的曲线积分 $\int_L f(x,y)\,ds$ 是把曲线 $L$ 分成 $n$ 小段，每段长度 $\Delta s_i$ 与段上密度 $f(\xi_i,\eta_i)$ 相乘求和后取极限，物理意义是求一段不均匀细曲线的质量，故又称第一类曲线积分。
- **关键概念**：`对弧长的曲线积分`、`第一类曲线积分`、`$\int_L f(x,y)\,ds$`、`积分弧段 $L$`
- **相互关系**：$f(x,y)$ 是被积函数、$L$ 是积分弧段、$ds$ 是弧长元素，「密度乘弧长」即质量；曲线封闭时积分号上要加一个圆圈。
- **出处**：[石头 P82](https://www.bilibili.com/video/BV18CL26WEJ3?p=82)

### 对弧长曲线积分的性质
- **要点**：与定积分、二重积分类似：常数因子可提出；和与差的积分可拆开；弧段可加（$L=L_1+L_2$ 时拆成两段相加）；被积函数大则积分大，且 $\left|\int_L f\,ds\right|\le\int_L|f|\,ds$；最重要的一条是 $\int\_\{AB\}f\,ds=\int\_\{BA\}f\,ds$，即对弧长的曲线积分与弧的方向无关。
- **关键概念**：`线性性质`、`弧段可加性`、`保号性`、`与方向无关`
- **相互关系**：与方向无关是对弧长曲线积分区别于对坐标曲线积分的本质特征；正因如此，计算时上下限永远保持「下限小于上限」。
- **出处**：[石头 P82](https://www.bilibili.com/video/BV18CL26WEJ3?p=82)

### 对称性与偶倍奇零
- **要点**：若曲线 $L$ 关于 $x$ 轴对称，则只看被积函数中 $y$ 的奇偶性：$y$ 为奇函数时积分为零，$y$ 为偶函数时等于在右半部分 $L_1$ 上积分的二倍；若 $L$ 关于 $y$ 轴对称，则看 $x$ 的奇偶性，规则相同。
- **关键概念**：`偶倍奇零`、`关于 $x$ 轴对称看 $y$`、`关于 $y$ 轴对称看 $x$`
- **相互关系**：与定积分、二重积分的对称性结论一致；专升本中二重积分的对称性很少考，但对弧长的曲线积分常用它化简，判断时先把被积函数中不含对称变量的部分视为常数。
- **出处**：[石头 P82](https://www.bilibili.com/video/BV18CL26WEJ3?p=82)

### 参数方程形式的计算公式
- **要点**：若 $L$ 由参数方程 $x=\varphi(t)$、$y=\psi(t)$（$\alpha\le t\le\beta$）给出，则 $\int_L f(x,y)\,ds=\int_\alpha^\beta f(\varphi(t),\psi(t))\sqrt{\varphi'^2(t)+\psi'^2(t)}\,dt$。计算时被积函数中的 $x$、$y$ 与弧长元素要全部换成 $t$ 的表达式。
- **关键概念**：`参数方程`、`$ds=\sqrt{\varphi'^2+\psi'^2}\,dt$`、`换元要彻底`
- **相互关系**：圆 $x^2+y^2=R^2$ 常用参数方程 $x=R\cos t$、$y=R\sin t$，此时 $ds=R\,dt$；把曲线参数化与用极坐标描述圆是同一思想的两种表现。
- **出处**：[石头 P82](https://www.bilibili.com/video/BV18CL26WEJ3?p=82)

### y=y(x) 与 x=x(y) 形式的计算公式
- **要点**：若 $L$ 由 $y=y(x)$（$a\le x\le b$）给出，则 $ds=\sqrt{1+y'^2(x)}\,dx$，积分化为对 $x$ 的定积分；若 $L$ 由 $x=x(y)$（$c\le y\le d$）给出，则 $ds=\sqrt{1+x'^2(y)}\,dy$，积分化为对 $y$ 的定积分。判断用哪条公式只看自变量是谁，并把另一变量全部替换掉。
- **关键概念**：`$ds=\sqrt{1+y'^2}\,dx$`、`$ds=\sqrt{1+x'^2}\,dy$`、`下限小于上限`
- **相互关系**：自变量为 $x$ 时隐含 $x=x$，故根号内出现 $1^2+y'^2$；只给两点而未给方程时，先用两点式求出直线方程再套公式，含根号的积分常用凑微分处理。
- **出处**：[石头 P82](https://www.bilibili.com/video/BV18CL26WEJ3?p=82)

### 对坐标的曲线积分的概念与记号
- **要点**：对坐标的曲线积分（第二类曲线积分）研究的是变力沿曲线做功的问题，被积函数有两个：$P(x,y)$ 与 $Q(x,y)$，分别对应 $x$ 方向与 $y$ 方向上的分量。一般形式写作 $\int_L P(x,y)\,\mathrm{d}x+Q(x,y)\,\mathrm{d}y$，两段积分弧相同，可共用一个 $\int_L$。记号对应关系是 $x$ 配 $P$、$y$ 配 $Q$，按字母表顺序记作「前前组合、后后组合」。
- **关键概念**：`第二类曲线积分`、`$\int_L P\,\mathrm{d}x+Q\,\mathrm{d}y$`、`被积函数 $P$、$Q$`、`前前组合后后组合`
- **相互关系**：与对弧长的曲线积分同属曲线积分，区别在于对弧长「求质量」、对坐标「求做功」；二者是整个第六章后续格林公式与路径无关的基础。
- **出处**：[石头 P83](https://www.bilibili.com/video/BV18CL26WEJ3?p=83)

### 两类曲线积分的区分
- **要点**：拿到题先看积分号后的微分符号：出现 $\mathrm{d}s$ 就是对弧长的曲线积分，出现 $\mathrm{d}x$、$\mathrm{d}y$ 就是对坐标的曲线积分。对坐标的曲线积分有方向，写上下限时起点作下限、终点作上限，与两端数值大小无关；若曲线取反向，只需在最前面添一个负号。
- **关键概念**：`$\mathrm{d}s$`、`$\mathrm{d}x$、$\mathrm{d}y$`、`起点作下限、终点作上限`、`反向添负号`
- **相互关系**：对弧长是「下小上大」，对坐标是「起点到终点」，这是两者最容易混的地方；分清 $\mathrm{d}s$ 与 $\mathrm{d}x\mathrm{d}y$ 是选择解题方法的第一步。
- **出处**：[石头 P83](https://www.bilibili.com/video/BV18CL26WEJ3?p=83)

### 对坐标的曲线积分的计算方法
- **要点**：核心口诀是「自变量是谁，就转化为谁的定积分」。曲线由参数方程 $x=\varphi(t)$、$y=\psi(t)$ 给出时，把 $x$、$y$ 全部换成 $t$ 的表达式，$\mathrm{d}x=\varphi'(t)\mathrm{d}t$、$\mathrm{d}y=\psi'(t)\mathrm{d}t$，上下限取 $t$ 的范围；由 $y=f(x)$ 给出时把 $y$ 换成 $f(x)$、$\mathrm{d}y=f'(x)\mathrm{d}x$，化为对 $x$ 的定积分；由 $x=f(y)$ 给出时化为对 $y$ 的定积分。
- **关键概念**：`自变量是谁就转化为谁的定积分`、`参数方程法`、`$\mathrm{d}y=f'(x)\mathrm{d}x$`
- **相互关系**：展开式不必死记，认准自变量与微分关系即可推出来；曲线分段给出（如折线 $OAB$）时要分成两段分别化为关于 $x$、关于 $y$ 的定积分再相加。
- **出处**：[石头 P83](https://www.bilibili.com/video/BV18CL26WEJ3?p=83)

### 单连通区域与复连通区域
- **要点**：只由一条封闭曲线围成的区域叫单连通区域；由两条或两条以上封闭曲线围成的区域叫复连通区域，它围成的区域是两条曲线之间的那一部分。
- **关键概念**：`单连通区域`、`复连通区域`、`封闭曲线`
- **相互关系**：区分这两类区域是为了确定边界正向，复连通区域的内外边界方向正好相反。
- **出处**：[石头 P84](https://www.bilibili.com/video/BV18CL26WEJ3?p=84)

### 边界正向的规定
- **要点**：格林公式要求曲线封闭且取正向。判定标准是：人沿边界行走时，左手边始终靠近被围区域的方向为正向。口诀为「外逆内顺」——外边界以逆时针为正向，内边界以顺时针为正向。
- **关键概念**：`正向`、`左手边靠近区域`、`外逆内顺`
- **相互关系**：若曲线取负向，在格林公式算出的二重积分前添一个负号即可；方向判错会导致最终结果差一个符号。
- **出处**：[石头 P84](https://www.bilibili.com/video/BV18CL26WEJ3?p=84)

### 格林公式的条件与形式
- **要点**：当 $L$ 为封闭正向曲线，且 $P(x,y)$、$Q(x,y)$ 在区域 $D$ 上具有一阶连续偏导数时，$\oint_L P\,\mathrm{d}x+Q\,\mathrm{d}y=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\mathrm{d}x\,\mathrm{d}y$。找准函数的原则是 $\mathrm{d}x$ 前面的是 $P$、$\mathrm{d}y$ 前面的是 $Q$，且 $P$ 对 $y$ 求偏导、$Q$ 对 $x$ 求偏导，相减顺序不能颠倒。
- **关键概念**：`格林公式`、`$\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}$`、`一阶连续偏导数`、`$\mathrm{d}x$ 前是 $P$、$\mathrm{d}y$ 前是 $Q$`
- **相互关系**：命题人常把 $\mathrm{d}y$ 项写在前面，或把负号藏在 $P$、$Q$ 里，取函数时必须连符号一起取；格林公式把曲线积分化为二重积分，与对坐标曲线积分「化为定积分」形成两条不同的路。
- **出处**：[石头 P84](https://www.bilibili.com/video/BV18CL26WEJ3?p=84)

### 格林公式的应用与割补法
- **要点**：看到 $\mathrm{d}x$、$\mathrm{d}y$ 且曲线封闭，直接用格林公式；化为二重积分后，被积函数或区域与圆有关就用极坐标，与圆无关就用直角坐标。若曲线不封闭，用割补法补上一段使它封闭，再减去补上那一段的积分，补的那段不一定为零，要按题计算。当 $\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}$ 为常数 $k$ 时，二重积分等于 $k$ 倍区域面积；当它恒等于零时被积函数为零，积分值直接为 $0$。
- **关键概念**：`割补法`、`补封闭`、`极坐标`、`$\iint_D \mathrm{d}x\mathrm{d}y$ 表示区域面积`、`被积函数为零`
- **相互关系**：补出来的直线段用对坐标的曲线积分算（如 $y=0$ 时该段常为零）；含分式函数求偏导时按商的求导法则「上导下不导减上不导下导，比上分母的平方」计算，负号不能丢，否则会误判被积函数是否为零。
- **出处**：[石头 P84](https://www.bilibili.com/video/BV18CL26WEJ3?p=84)、[P86](https://www.bilibili.com/video/BV18CL26WEJ3?p=86)

### 积分与路径无关的充要条件
- **要点**：在单连通区域内，若 $P$、$Q$ 具有一阶连续偏导数，则曲线积分与路径无关的充要条件是 $\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}$ 处处成立。此时从起点到终点无论走直线、折线还是绕圈，积分值都相同。
- **关键概念**：`积分与路径无关`、`$\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}$`、`单连通区域`
- **相互关系**：题目含抽象函数（如 $Q=yf(x)$）时，可由这个等式反解出该函数；一旦两个偏导不相等，路径无关立刻排除。
- **出处**：[石头 P85](https://www.bilibili.com/video/BV18CL26WEJ3?p=85)

### 路径无关时的折线法与封闭情形
- **要点**：路径无关时取平行于坐标轴的折线计算最省事，先竖后横或先横后竖都可以，各段分别化为对 $y$、对 $x$ 的定积分再相加。若曲线本身封闭且偏导相等，用格林公式后二重积分的被积函数为零，积分值直接为 $0$。
- **关键概念**：`折线法`、`平行于坐标轴`、`被积函数为零`
- **相互关系**：封闭时优先用格林公式，不封闭才用折线法，这是两类题目的分界；折线法要与「给定曲线方程、按曲线走」的对坐标曲线积分区分开。
- **出处**：[石头 P85](https://www.bilibili.com/video/BV18CL26WEJ3?p=85)、[P86](https://www.bilibili.com/video/BV18CL26WEJ3?p=86)

### 曲线积分的类型判别流程
- **要点**：先看微分符号：是 $\mathrm{d}s$ 就是对弧长；是 $\mathrm{d}x$、$\mathrm{d}y$ 再看是否封闭，封闭就用格林公式（不封闭可割补），不封闭则检验 $\frac{\partial P}{\partial y}$ 与 $\frac{\partial Q}{\partial x}$ 是否相等，相等用路径无关的折线法，不相等才回到对坐标的曲线积分。能用定积分解决的就不绕道二重积分。
- **关键概念**：`类型判别流程`、`对弧长`、`对坐标`、`格林公式`、`路径无关`
- **相互关系**：四个知识点共用同一套 $P$、$Q$ 记号，判断顺序错了会白算一次二重积分，或把负向曲线当成正向。
- **出处**：[石头 P85](https://www.bilibili.com/video/BV18CL26WEJ3?p=85)、[P86](https://www.bilibili.com/video/BV18CL26WEJ3?p=86)

### 与圆有关的曲线积分
- **要点**：积分曲线是圆 $x^2+y^2=a^2$ 或表达式中含 $x^2+y^2$ 时，优先用参数方程 $x=a\cos\theta$、$y=a\sin\theta$，或转极坐标。化为二重积分时 $\theta$ 的范围由射线扫过的角度决定（整圆为 $0$ 到 $2\pi$，上半圆为 $0$ 到 $\pi$），$r$ 的范围由代入曲线方程确定，面积元为 $r\,\mathrm{d}r\,\mathrm{d}\theta$。
- **关键概念**：`参数方程`、`$x=a\cos\theta$`、`$y=a\sin\theta$`、`$r\,\mathrm{d}r\,\mathrm{d}\theta$`
- **相互关系**：整圆且被积函数简单时用格林公式最快；只是半圆、四分之一圆时补封闭再减补段反而繁琐，此时直接用对坐标的曲线积分。
- **出处**：[石头 P84](https://www.bilibili.com/video/BV18CL26WEJ3?p=84)、[P86](https://www.bilibili.com/video/BV18CL26WEJ3?p=86)


## 十、无穷级数


### 级数与部分和数列
- **要点**：把无穷数列的各项用加号连接，记作 Σu_n，称无穷级数；u_n 叫通项（一般项）。级数不是「逐项相加」的结果，而是定义为部分和数列的极限：Σu_n=lim S_n，其中 S_n=u₁+u₂+…+u_n（前 n 项之和）。这一等式把不熟悉的求和运算转化为熟悉的极限运算，是整章的基石。Σu_n 中，下方的 n=1 是下标（表示从第几项开始累加），上方的 ∞ 是上标（表示累加到哪一项）。若 u_n 为常数，则该级数叫常数项级数。
- **关键概念**：`通项`、`一般项`、`部分和数列`、`Σ 求和符号`、`常数项级数`
- **出处**：[陈哥 P118](https://www.bilibili.com/video/BV1husGzwEtZ?p=118)；[杰哥 P154](https://www.bilibili.com/video/BV1Up4y1Y76a?p=154)、[P155](https://www.bilibili.com/video/BV1Up4y1Y76a?p=155)；[米哥 P133](https://www.bilibili.com/video/BV1swAWerEzS?p=133)；[ok姐 P124](https://www.bilibili.com/video/BV1vm421s7mv?p=124)

### 级数的收敛与发散（定义法）
- **要点**：若 lim S_n=S（常数），称级数收敛于 S，S 称为级数的和；若该极限不存在或为无穷（摆动不定），称级数发散。这是判别敛散性的第一种方法（定义法），做题时必须先写出通项对应的前 n 项和。求级数的和关键在于求部分和数列的极限。
- **关键概念**：`收敛`、`发散`、`级数的和`、`定义法`
- **相互关系**：是后续所有判别方法（比值、比较、根值、莱布尼兹）的出发点；实际判敛散很少靠求和。
- **出处**：[陈哥 P118](https://www.bilibili.com/video/BV1husGzwEtZ?p=118)、[P120](https://www.bilibili.com/video/BV1husGzwEtZ?p=120)；[杰哥 P154](https://www.bilibili.com/video/BV1Up4y1Y76a?p=154)、[P155](https://www.bilibili.com/video/BV1Up4y1Y76a?p=155)；[米哥 P134](https://www.bilibili.com/video/BV1swAWerEzS?p=134)；[ok姐 P124](https://www.bilibili.com/video/BV1vm421s7mv?p=124)

### 无穷级数的分类
- **要点**：级数分成两大类：数项级数与函数项级数。数项级数中最常考的三种是——正项级数（每一项都是正数，即 u_n≥0 的 Σ\_\{n=1\}^∞ u_n）、交错级数、任意项级数（也叫一般项级数）。函数项级数中专升本只涉及幂级数，其他不会涉及。
- **关键概念**：`数项级数`、`函数项级数`、`正项级数`、`交错级数`、`任意项级数`、`幂级数`
- **相互关系**：考试重点是正项级数；交错级数在专升本不是重点（考研才是重点），任意项级数了解即可。
- **出处**：[学士帽 P89](https://www.bilibili.com/video/BV1X4411J792?p=89)

### 常见数列求和
- **要点**：等差数列通项 a_n=a₁+(n−1)d，和 S_n=n(a₁+a_n)/2；等比数列通项 a_n=a₁q\^\{n−1\}，q≠1 时 S_n=a₁(1−q^n)/(1−q)，特别地 |q|&lt;1 时 q^n→0，得无穷等比级数和 a₁/(1−q)；裂项相消如 1/(n(n+1))=1/n−1/(n+1)，展开后中间项两两抵消，只剩首尾（分式裂项的口诀是「大减小分之小 减 大分之一」）。能直接求和的数列种类很有限。
- **关键概念**：`等差数列`、`等比数列`、`公比`、`裂项相消`、`首尾相消`
- **相互关系**：是定义法的核心计算手段。
- **出处**：[陈哥 P118](https://www.bilibili.com/video/BV1husGzwEtZ?p=118)、[P120](https://www.bilibili.com/video/BV1husGzwEtZ?p=120)；[杰哥 P154](https://www.bilibili.com/video/BV1Up4y1Y76a?p=154)；[米哥 P133](https://www.bilibili.com/video/BV1swAWerEzS?p=133)

### 级数的线性运算性质
- **要点**：性质一：若 Σu_n 收敛于 S，则 Σk u_n 收敛于 kS（常数 k 可提到求和号外），k≠0 时 Σu_n 与 Σk u_n 同敛散。性质二：若 Σu_n 收敛于 S、Σv_n 收敛于 T，则 Σ(au_n+bv_n) 收敛于 aS+bT。添加或去掉有限项也不改变敛散性（去掉前几项后下标顺延即可），注意去掉的必须是有限项，不能去掉无穷多项。收敛级数任意加括号后仍收敛，且和不变。
- **关键概念**：`常数倍`、`线性组合`、`同敛散`、`有限项`、`加括号`
- **出处**：[陈哥 P119](https://www.bilibili.com/video/BV1husGzwEtZ?p=119)；[杰哥 P155](https://www.bilibili.com/video/BV1Up4y1Y76a?p=155)；[米哥 P134](https://www.bilibili.com/video/BV1swAWerEzS?p=134)；[学士帽 P88](https://www.bilibili.com/video/BV1X4411J792?p=88)；[ok姐 P126](https://www.bilibili.com/video/BV1vm421s7mv?p=126)、[P130](https://www.bilibili.com/video/BV1vm421s7mv?p=130)

### 收敛与发散的组合规律
- **要点**：收敛±收敛=收敛；收敛±发散=发散；发散±发散=敛散性不确定（只有限定为正项级数时结果才一定发散；发散±发散之所以不定，是因为正无穷与负无穷相加可能得常数）。除前两条外，其余组合结果均不一定，是选择题的高频陷阱。
- **关键概念**：`收敛加发散等于发散`、`发散±发散不定`
- **相互关系**：常与「把复杂级数拆成两个基本级数」配合使用。
- **出处**：[陈哥 P119](https://www.bilibili.com/video/BV1husGzwEtZ?p=119)；[杰哥 P155](https://www.bilibili.com/video/BV1Up4y1Y76a?p=155)；[米哥 P134](https://www.bilibili.com/video/BV1swAWerEzS?p=134)；[学士帽 P88](https://www.bilibili.com/video/BV1X4411J792?p=88)

### 级数收敛的必要条件及其逆否命题
- **要点**：若级数收敛，则必定有 lim u_n=0。其逆否命题（第 n 项判别法/通项判别法）：若 lim u_n≠0 或极限不存在，则级数必定发散。这是判别敛散性的第二种方法，但只能判定发散、不能判定收敛。判断敛散性的基础方法就是看 lim u_n 是否为零，或看前 n 项和 S_n 的极限是否存在。
- **关键概念**：`必要条件`、`一般项的极限`、`逆否命题`、`第 n 项判别法`、`通项判别法`
- **相互关系**：易错点——不能反向推，即 lim u_n=0 推不出级数收敛（调和级数 Σ1/n 就是反例）；拿到任何级数的第一步都是用它先判断是否发散，再决定后续方法。
- **出处**：[陈哥 P119](https://www.bilibili.com/video/BV1husGzwEtZ?p=119)、[P120](https://www.bilibili.com/video/BV1husGzwEtZ?p=120)；[杰哥 P155](https://www.bilibili.com/video/BV1Up4y1Y76a?p=155)、[P162](https://www.bilibili.com/video/BV1Up4y1Y76a?p=162)；[米哥 P134](https://www.bilibili.com/video/BV1swAWerEzS?p=134)；[学士帽 P87](https://www.bilibili.com/video/BV1X4411J792?p=87)、[P88](https://www.bilibili.com/video/BV1X4411J792?p=88)；[ok姐 P126](https://www.bilibili.com/video/BV1vm421s7mv?p=126)、[P130](https://www.bilibili.com/video/BV1vm421s7mv?p=130)

### 与无穷区间广义积分的类比
- **要点**：把 Σ\_\{n=1\}^∞ u_n 与积分上限为正无穷的广义积分 ∫_1\^\{+∞\} f(x)dx 对照着理解：积分号对应求和符号，被积函数 f(x) 对应 u_n，积分代表围成图形的面积。图形底部长度是无穷，只有当 f(x) 的取值一直趋近于 x 轴、不断趋近于零时，面积才是一个确定的常数；对应地，u_n 必须足够小、趋近于零，级数才可能收敛。
- **关键概念**：`无穷区间上的广义积分`、`图形面积`、`f(x)→0`、`对应关系`
- **相互关系**：是理解「u_n→0 为必要条件」的直观来源；与广义积分、极限内容相关联。
- **出处**：[学士帽 P87](https://www.bilibili.com/video/BV1X4411J792?p=87)

### 通项判别法的典型题型
- **要点**：对通项直接取极限：sin(1/n) 型先等价为 1/n 再判；cos(1/n)→1、(1+1/n)^n→e、√[n]n→1 三种极限都不为零，故均发散。含根号的通项先化为幂函数形式 n\^\{1/n\}，再用 u^v=e\^\{v ln u\} 处理 1^∞、∞⁰ 型。数列不能直接洛必达，须先把 n 改为 x。
- **关键概念**：`等价无穷小`、`1^∞ 型`、`u^v=e^{v ln u}`
- **出处**：[杰哥 P155](https://www.bilibili.com/video/BV1Up4y1Y76a?p=155)、[P162](https://www.bilibili.com/video/BV1Up4y1Y76a?p=162)

### 等比级数（几何级数）
- **要点**：标准形式 Σa q^n（或 Σ\_\{n=0\}^∞ A q^n），q 为公比（后一项比前一项恒为常数）。部分和 S_n=A(1−q^n)/(1−q)，判别只看 |q|：|q|&lt;1 时收敛且和为 a₁/(1−q)（首项除以 1−q），|q|≥1 时发散。推导依据是 lim q^n=0（|q|&lt;1）；只有收敛的等比级数才能用此公式求和。q=1 时级数为 A+A+…，S_n=nA→∞，发散；q=−1 时级数为 A−A+A−A+…，S_n 在 A 与 0 之间跳动，极限不存在，也发散。
- **关键概念**：`等比级数`、`几何级数`、`公比 q`、`首项`、`一减公比分之首项`
- **相互关系**：识别时先定出首项与公比，公比由相邻两项之比确定；是极限比较判别法最终归结的两类目标级数之一；是后面幂级数求和的前置公式；与 p 级数的判别条件恰好相反，是本章最容易混淆的一对。
- **出处**：[陈哥 P120](https://www.bilibili.com/video/BV1husGzwEtZ?p=120)；[杰哥 P156](https://www.bilibili.com/video/BV1Up4y1Y76a?p=156)；[米哥 P135](https://www.bilibili.com/video/BV1swAWerEzS?p=135)；[学士帽 P89](https://www.bilibili.com/video/BV1X4411J792?p=89)、[P90](https://www.bilibili.com/video/BV1X4411J792?p=90)；[ok姐 P125](https://www.bilibili.com/video/BV1vm421s7mv?p=125)、[P130](https://www.bilibili.com/video/BV1vm421s7mv?p=130)；[帆哥 P1](https://www.bilibili.com/video/BV1xxXZBKENv?p=1)

### 从通项识别等比级数
- **要点**：看通项里有没有「某数的 n 次方」；把同次方因子合并成 (·)^n 后取公比。不好看时写出 n=1,2,3 的前三项，用「后项除以前项」定公比。含 (−1)^n、(−1)\^\{n−1\} 时把负号提到求和号外，化为负公比的等比级数（(−1)\^\{n−1\}=(−1)^n/(−1)）。与「收敛±收敛=收敛」配合使用，可把多个等比级数的加减拆开分别判。
- **关键概念**：`公比`、`提公因子`、`(−1)^{n−1}=(−1)^n/(−1)`
- **出处**：[杰哥 P156](https://www.bilibili.com/video/BV1Up4y1Y76a?p=156)

### p 级数与调和级数
- **要点**：形如 Σ\_\{n=1\}^∞ 1/n^p 的级数称为 p 级数（p>0 为常数）：p>1 时收敛、0&lt;p≤1 时发散；p=1 的情形 Σ1/n 即调和级数，是最典型的发散级数——虽然 1/n→0，但它「不够小」所以发散，1/n² 这类才足够小从而收敛。使用前必须化为 1/n^p 的分式形式（分母为根式时先化为分数指数幂，如 √(N³)=N\^\{3/2\} 再读出 p）。分母次数越高值越小、越收敛。
- **关键概念**：`p 级数`、`p 判别法`、`调和级数`、`分数指数幂`
- **相互关系**：常作为比较判别法中的「标尺级数」；与等比级数极易混——p 级数中 N 在底数、指数为常数，等比级数底数为常数、N 在指数，判据方向也相反（p>1 收敛 vs |q|&lt;1 收敛），务必区分。
- **出处**：[陈哥 P120](https://www.bilibili.com/video/BV1husGzwEtZ?p=120)；[杰哥 P157](https://www.bilibili.com/video/BV1Up4y1Y76a?p=157)；[米哥 P135](https://www.bilibili.com/video/BV1swAWerEzS?p=135)；[学士帽 P90](https://www.bilibili.com/video/BV1X4411J792?p=90)；[ok姐 P125](https://www.bilibili.com/video/BV1vm421s7mv?p=125)、[P130](https://www.bilibili.com/video/BV1vm421s7mv?p=130)

### 一般项为常数的级数
- **要点**：Σ\_\{n=1\}^∞ K，K 为非零常数时发散（S_n=nK→∞）；K=0 时收敛于 0。K=0 是特例，与「一般项极限为 0 不一定收敛」相呼应，不可由 K=0 收敛推广到 K≠0。
- **关键概念**：`一般项为常数`
- **出处**：[ok姐 P126](https://www.bilibili.com/video/BV1vm421s7mv?p=126)、[P127](https://www.bilibili.com/video/BV1vm421s7mv?p=127)、[P130](https://www.bilibili.com/video/BV1vm421s7mv?p=130)

### 拆项相消法求收敛性
- **要点**：通项是分式（如 1/[n(n+1)]）或根式差（如 √(n+1)−√n）时，先用裂项把每一项拆成两项之差，累加时中间项两两抵消，只剩首项与末项，再对剩下的式子求极限判断敛散性。
- **关键概念**：`拆项相消`、`裂项`、`首尾相消`
- **相互关系**：是定义法的核心计算手段。
- **出处**：[米哥 P136](https://www.bilibili.com/video/BV1swAWerEzS?p=136)；[陈哥 P118](https://www.bilibili.com/video/BV1husGzwEtZ?p=118)、[P120](https://www.bilibili.com/video/BV1husGzwEtZ?p=120)

### 正项级数与判别方法体系
- **要点**：每一项都为正（u_n>0）的级数称正项级数。正项级数的敛散性判别在考题中出现频率极高，是选择填空的主要考点。其判别法分三大方向：比值判别法（自己比自己）、比较判别法（与别人比，含等价、抓大头、放缩三种找 v_n 的手段）、根值判别法。三大判别法是幂级数求收敛半径的基础工具；交错级数与任意项级数需另用方法。
- **关键概念**：`正项级数`、`比值判别法`、`比较判别法`、`根值判别法`
- **出处**：[陈哥 P121](https://www.bilibili.com/video/BV1husGzwEtZ?p=121)；[杰哥 P158](https://www.bilibili.com/video/BV1Up4y1Y76a?p=158)、[P159](https://www.bilibili.com/video/BV1Up4y1Y76a?p=159)

### 比值判别法（达朗贝尔判别法）
- **要点**：令 ρ=lim|u\_\{n+1\}/u_n|（计算时把分式相除化为乘以倒数，再约分、抓大头）。ρ&lt;1 时级数收敛，ρ>1 时级数发散，ρ=1 时判别法失效（需改用比较判别法；专升本基本不考这种情况）。写出 u_n 与 u\_\{n+1\}（把所有 n 换成 n+1），作商取绝对值，把同类项（2^n 与 2\^\{n+1\}、n! 与 (n+1)!、n^n 与 (n+1)\^\{n+1\}）分组约简，最后对残式取极限；残留的 (n/(n+1))^n 型用第二重要极限（1^∞ 型公式 e\^\{((u−1)v)\}）求值；结论仍与 1 比较大小定敛散。
- **关键概念**：`比值判别法`、`达朗贝尔判别法`、`ρ`、`失效`、`后项比前项`、`同项分组`
- **相互关系**：适用条件是通项 u_n 中含有三种形式之一：a^n（指数形式）、n^n（幂指形式）、n!（阶乘）——即「三大金刚」；优势是不需另找比较级数，与自身比较；阶乘约分要用 (n+1)!=(n+1)·n!。
- **出处**：[陈哥 P121](https://www.bilibili.com/video/BV1husGzwEtZ?p=121)；[杰哥 P158](https://www.bilibili.com/video/BV1Up4y1Y76a?p=158)、[P159](https://www.bilibili.com/video/BV1Up4y1Y76a?p=159)；[米哥 P138](https://www.bilibili.com/video/BV1swAWerEzS?p=138)；[学士帽 P91](https://www.bilibili.com/video/BV1X4411J792?p=91)、[P92](https://www.bilibili.com/video/BV1X4411J792?p=92)；[ok姐 P128](https://www.bilibili.com/video/BV1vm421s7mv?p=128)、[P130](https://www.bilibili.com/video/BV1vm421s7mv?p=130)；[帆哥 P1](https://www.bilibili.com/video/BV1xxXZBKENv?p=1)

### 阶乘
- **要点**：n!=n·(n−1)·(n−2)…3·2·1，即从 1 连乘到该数。常用变形是 (n+1)!=(n+1)·n!，用于比值法中的约分。
- **关键概念**：`n!`、`阶乘`
- **出处**：[陈哥 P121](https://www.bilibili.com/video/BV1husGzwEtZ?p=121)；[杰哥 P158](https://www.bilibili.com/video/BV1Up4y1Y76a?p=158)

### 题型：含 n! 的比值判别法
- **要点**：级数中含有 n 的阶乘时，要直接想到试比值判别法。例题 Σ4^n n!/n^n：把原式中所有 n 换成 n+1 后与原项相除（即乘以原项的倒数），利用 (n+1)!/n!=n+1 约分，整理得 4·n^n/(n+1)^n；再把括号内凑成 1+□ 的形式、指数凑成无穷小分之一，用第二重要极限得 ρ=4e\^\{−1\}=4/e。因 e≈2.7，4>e，故 ρ>1，原级数发散。
- **关键概念**：`n 的阶乘`、`第二重要极限`、`ρ=4/e`、`发散`
- **相互关系**：计算中又用到了数列极限（上下同次幂看系数之比）与幂指函数求极限的方法。
- **出处**：[学士帽 P91](https://www.bilibili.com/video/BV1X4411J792?p=91)

### 根值判别法
- **要点**：令 ρ=lim √[n]{u_n}（运算时把开 n 次根式写成 u_n\^\{1/n\} 更便于化简）。ρ&lt;1 收敛，ρ>1 发散，ρ=1 时不能确定。适用条件是通项中含有整体的 n 次方（如 (n/(2n+1))^n、(1+1/n)\^\{n²\}）。参考教材中标星号，权重低。
- **关键概念**：`根值判别法`、`开 n 次根式`、`ρ`
- **相互关系**：结论形式与比值判别法相同，只是所求极限不同。
- **出处**：[陈哥 P121](https://www.bilibili.com/video/BV1husGzwEtZ?p=121)；[ok姐 P129](https://www.bilibili.com/video/BV1vm421s7mv?p=129)、[P130](https://www.bilibili.com/video/BV1vm421s7mv?p=130)

### 比较判别法——比较形式
- **要点**：设 u_n≤v_n。若大的级数 Σv_n 收敛，则小的级数 Σu_n 必定收敛；若小的级数 Σu_n 发散，则大的级数 Σv_n 必定发散。口诀：大收则小收，小发则大发。推导方向不可颠倒，没有「大发则小发」「小收则大收」。判断 Σu_n 时另找敛散性已知的 Σv_n 作参照（比较基准「因地制宜」，优先选 p 级数或等比级数），v_n 必须比原通项更大或更小，只是形式更简单；找不到 v_n 口诀就无从下手。本法考得不多，多在选择题里直接选答案，是极限形式的基础。
- **关键概念**：`比较判别法`、`参照级数`、`大收则小收`、`小发则大发`、`比较基准`
- **相互关系**：遇到 sin、cos 时通常放大到 1（有界函数 |sin x|≤1），遇到 ln n 时用 ln n&lt;n 放缩；一般项含三角函数时，用其值域（如 0≤|sin n|≤1）放缩出大小关系再用本法。
- **出处**：[陈哥 P121](https://www.bilibili.com/video/BV1husGzwEtZ?p=121)；[杰哥 P159](https://www.bilibili.com/video/BV1Up4y1Y76a?p=159)；[米哥 P137](https://www.bilibili.com/video/BV1swAWerEzS?p=137)；[学士帽 P89](https://www.bilibili.com/video/BV1X4411J792?p=89)、[P90](https://www.bilibili.com/video/BV1X4411J792?p=90)、[P92](https://www.bilibili.com/video/BV1X4411J792?p=92)；[ok姐 P127](https://www.bilibili.com/video/BV1vm421s7mv?p=127)、[P130](https://www.bilibili.com/video/BV1vm421s7mv?p=130)

### 比较判别法——极限形式
- **要点**：找辅助级数 Σv_n，令 lim(u_n/v_n)=A。当 A 为非零常数时，两级数同敛散；A=0 说明 v_n 更大，用「大收则小收」；A=+∞ 说明 v_n 更小，用「小发则大发」；A=0 或 A=∞ 的情形几乎不考。这是考得最多的一种形式。使用前必须保证 Σv_n 是已会判断的等比级数或 p 级数。本质仍是比大小；两个发散的级数相减，结果不确定，不能直接下结论。
- **关键概念**：`极限形式`、`同敛散`、`非零常数`、`比值的极限`
- **相互关系**：免去直接比较大小（如 1/(3^n−1) 无法用原法）。
- **出处**：[陈哥 P121](https://www.bilibili.com/video/BV1husGzwEtZ?p=121)；[杰哥 P159](https://www.bilibili.com/video/BV1Up4y1Y76a?p=159)、[P160](https://www.bilibili.com/video/BV1Up4y1Y76a?p=160)；[学士帽 P89](https://www.bilibili.com/video/BV1X4411J792?p=89)、[P90](https://www.bilibili.com/video/BV1X4411J792?p=90)、[P92](https://www.bilibili.com/video/BV1X4411J792?p=92)；[ok姐 P127](https://www.bilibili.com/video/BV1vm421s7mv?p=127)、[P130](https://www.bilibili.com/video/BV1vm421s7mv?p=130)

### 由极限形式得到的常用结论
- **要点**：分子为常数、分母为 N 的 k 次多项式的级数，与 Σ1/N^k 同敛散，即分母次数 >1 收敛、≤1 发散；此类题可先看分母最高次直接下结论。比较基准一般取同次 p 级数。
- **关键概念**：`分母次数`、`同次 p 级数`
- **相互关系**：极限形式的直接应用，常作为选择题快速判据。
- **出处**：[ok姐 P127](https://www.bilibili.com/video/BV1vm421s7mv?p=127)

### 用等价代换构造比较级数
- **要点**：通项中含三角函数、指数等不易直接比较的因子时，先用等价代换把 u_n 化简（在 n→∞ 下若通项可等价替换，如 sin x~x、ln(1+x)~x、x−sin x 等），再据此反推出参照级数 v_n，两级数的敛散性相同；常用代换（方块趋于 0）为 1−cos□~½□²、sin□~□、□−sin□~⅙□³，构造时把 1/n 整体当作方块。等价后的目标几乎总是等比级数或 p 级数，直接套用两者的判敛结论。□−sin□~⅙□³ 可由洛必达法则与 1−cos□~½□² 推出，也可直接当结论记忆。
- **关键概念**：`等价代换`、`方块整体代换`、`极限比较判别法`、`同敛散`
- **相互关系**：常见组合：sin(1/2^n)~1/2^n（归为等比，收敛）；ln(1+1/n)~1/n（归为调和，发散）；(1/√n)ln(1+1/n) 化成 n\^\{−3/2\}（p 级数，收敛）；sin(π/3^n)/2^n 提常数后归为等比。两数之差（如 √(n+1)−√(n−1)）先有理化，再在极限状态下忽略常数项。
- **出处**：[杰哥 P160](https://www.bilibili.com/video/BV1Up4y1Y76a?p=160)；[学士帽 P90](https://www.bilibili.com/video/BV1X4411J792?p=90)

### 抓大头定 v_n
- **要点**：通项是分式（幂函数或有理根式）时，把分子、分母各自的最大项留下、其余低次项舍去，得到的新级数即为 v_n。抓大头不是求极限，而是为了化简出更简单的比较对象；它本身隐含着放缩（分母去掉低次项后变小，值变大），因此仍受「大收则小收」约束。也可用等价无穷小化简通项（无分母用等价、有分母用抓大头）。
- **关键概念**：`抓大头`、`保留最大项`、`有理分式`、`构造 v_n`
- **相互关系**：典型：(n+1)/(n(n+2)) 抓成 1/n（调和，发散）；1/(2^n+4) 抓成 1/2^n（等比，收敛）；1/√(4n³+5) 抓成 1/(2n\^\{3/2\})（p 级数 p=3/2，收敛）；2n²/(n³+1) 抓成 2/n（发散）。写成解答时先构造 Σv_n，再用 lim(u_n/v_n)=非零常数说明同敛散；分式形通项若被拆成两项相减，先按「加减运算可分开」拆成两个级数分别判，再用「发散±收敛=发散」合结论。
- **出处**：[杰哥 P161](https://www.bilibili.com/video/BV1Up4y1Y76a?p=161)；[米哥 P137](https://www.bilibili.com/video/BV1swAWerEzS?p=137)

### 放缩思想
- **要点**：两类常用放缩：①sin∞、cos∞、(−1)^n 这类通项一律放大为 1（有界性 |sin|≤1）；②均值不等式 a²+b²≥2ab，即 2ab≤a²+b²，用于把两项乘积拆成平方和（由完全平方 (a−b)²≥0 推出），或用 a+b≥2√(ab)。考得较少；含 sin nx 的题放缩后归为 Σ1/n²（p 级数，收敛）。
- **关键概念**：`放缩`、`有界性`、`均值不等式`
- **出处**：[杰哥 P162](https://www.bilibili.com/video/BV1Up4y1Y76a?p=162)；[米哥 P137](https://www.bilibili.com/video/BV1swAWerEzS?p=137)

### 正项级数判敛的三部曲
- **要点**：①先对通项取极限，不为零直接判发散；②通项趋于零且含 n!、a^n、n^n 时用比值判别法；③通项是有理分式、含 sin、ln(1+·) 等可等价形式时，用等价替换或抓大头定出 v_n，再用比较判别法。等比级数与 p 级数是最终判定的落点。
- **关键概念**：`三部曲`、`优先选择顺序`
- **出处**：[杰哥 P162](https://www.bilibili.com/video/BV1Up4y1Y76a?p=162)

### 交错级数
- **要点**：各项正负交错的级数，形如 Σ(−1)\^\{n−1\}u_n 或 Σ(−1)^n u_n（其中 u_n>0），用 (−1) 的幂决定各项的符号：首项为正时用 (−1)\^\{n−1\}，首项为负时用 (−1)^n。前提是撇开符号后 u_n>0。
- **关键概念**：`交错级数`、`(−1)^{n−1}u_n`、`正负交错`
- **相互关系**：与正项级数审敛法适用范围不同。
- **出处**：[陈哥 P122](https://www.bilibili.com/video/BV1husGzwEtZ?p=122)；[杰哥 P163](https://www.bilibili.com/video/BV1Up4y1Y76a?p=163)；[米哥 P139](https://www.bilibili.com/video/BV1swAWerEzS?p=139)；[学士帽 P92](https://www.bilibili.com/video/BV1X4411J792?p=92)；[ok姐 P131](https://www.bilibili.com/video/BV1vm421s7mv?p=131)

### 莱布尼兹判别法
- **要点**：交错级数 Σ(−1)\^\{n−1\}u_n 若同时满足①u\_\{n+1\}≤u_n（各项绝对值单调不增）②lim u_n=0，则该交错级数收敛，两条缺一不可。单调性等价于 u_n−u\_\{n+1\}≥0 或 u\_\{n+1\}/u_n≤1；判定 u_n 与 u\_\{n+1\} 大小有三种方法——直接解不等式、做差、做商，专升本阶段一般用解不等式即可。
- **关键概念**：`莱布尼兹判别法`、`单调递减`、`通项趋于零`、`单调不增`
- **相互关系**：易错点——判断时 u_n 不包含 (−1) 的幂因子，必须把符号部分单独拿出来；它是判定条件收敛的关键工具。
- **出处**：[陈哥 P122](https://www.bilibili.com/video/BV1husGzwEtZ?p=122)；[杰哥 P163](https://www.bilibili.com/video/BV1Up4y1Y76a?p=163)、[P164](https://www.bilibili.com/video/BV1Up4y1Y76a?p=164)；[米哥 P139](https://www.bilibili.com/video/BV1swAWerEzS?p=139)；[学士帽 P92](https://www.bilibili.com/video/BV1X4411J792?p=92)；[ok姐 P131](https://www.bilibili.com/video/BV1vm421s7mv?p=131)、[P132](https://www.bilibili.com/video/BV1vm421s7mv?p=132)

### 交错级数判别的注意事项
- **要点**：①若通项极限不为零，直接判发散，不必再看单调性；②判单调性需要求导时，必须先把 n 换成 x，对函数 f(x) 求 f′(x)，由 f′(x)&lt;0 得单减——数列是离散点，不能直接求导（海涅定理）。只需在 x→∞ 时导数小于零即可，前有限项是否单调不影响结论。
- **关键概念**：`海涅定理`、`n 换成 x`、`f′(x)<0`
- **出处**：[杰哥 P163](https://www.bilibili.com/video/BV1Up4y1Y76a?p=163)、[P164](https://www.bilibili.com/video/BV1Up4y1Y76a?p=164)

### 交错级数典型题型
- **要点**：含 1/n!、1/n² 的题通项显然趋于零且单减，直接由莱布尼兹定理得收敛。含 n/3\^\{n−1\} 的题需先把 n 改成 x 用洛必达求通项极限，再用商的求导法则判单调性（通分后提出 3\^\{x−1\}，由 1−x ln3&lt;0 得导数小于零）。含 n/(n+1) 的题通项极限为 1，直接判发散。sin(1/√n) 这类通项在判 Σu_n² 时，平方后等价为 1/n（调和，发散）。
- **关键概念**：`莱布尼兹定理`、`商的求导法则`、`抓大头`
- **出处**：[杰哥 P164](https://www.bilibili.com/video/BV1Up4y1Y76a?p=164)

### 任意项级数与加绝对值的处理方法
- **要点**：各项可正可负、形式任意的级数称任意项级数，它包含了正项级数与交错级数。处理方法是对通项取绝对值，把 Σu_n 变成正项级数 Σ|u_n|，再用正项级数的三种判别法处理。加绝对值本质是放大，因此「大收则小收」适用：Σ|u_n| 收敛可推出 Σu_n 收敛；反之不成立。这里求和号后的整体才是 u_n，与交错级数中「只把非符号部分看作 u_n」不同。
- **关键概念**：`任意项级数`、`加绝对值`、`放大过程`
- **出处**：[陈哥 P122](https://www.bilibili.com/video/BV1husGzwEtZ?p=122)；[杰哥 P165](https://www.bilibili.com/video/BV1Up4y1Y76a?p=165)

### 绝对收敛与条件收敛
- **要点**：若 Σ|u_n| 收敛，称 Σu_n 绝对收敛（此时原级数必收敛）；若 Σu_n 收敛而 Σ|u_n| 发散，称 Σu_n 条件收敛。加绝对值发散不能推出原级数发散。绝对收敛必收敛，反之不一定；条件收敛是介于两者之间的情形。典型例子——Σ(−1)\^\{n−1\}/n² 绝对收敛；Σ(−1)\^\{n−1\}/n 条件收敛（绝对值后为调和级数发散，但原级数由莱布尼兹定理收敛）。（学士帽 P93 把条件收敛表述为「若 Σ|u_n| 发散则原级数称为条件收敛」——口径不一致，以「Σu_n 收敛而 Σ|u_n| 发散」为准）
- **关键概念**：`绝对收敛`、`条件收敛`
- **相互关系**：把「收敛」进一步细分为两类，是选择题常考的区分点。
- **出处**：[陈哥 P122](https://www.bilibili.com/video/BV1husGzwEtZ?p=122)；[杰哥 P165](https://www.bilibili.com/video/BV1Up4y1Y76a?p=165)；[米哥 P140](https://www.bilibili.com/video/BV1swAWerEzS?p=140)；[学士帽 P92](https://www.bilibili.com/video/BV1X4411J792?p=92)、[P93](https://www.bilibili.com/video/BV1X4411J792?p=93)；[ok姐 P132](https://www.bilibili.com/video/BV1vm421s7mv?p=132)

### 任意项级数敛散性的两步判定法
- **要点**：第一步加绝对值，判断 Σ|u_n| 的敛散性；若收敛则为绝对收敛。第二步：若 Σ|u_n| 发散，再判断原级数 Σu_n 本身的敛散性（此时它极大概率是交错级数，用莱布尼兹定理）；若收敛则为条件收敛，若发散则级数发散。
- **关键概念**：`加绝对值`、`正项级数审敛法`、`先本身后绝对值`
- **相互关系**：把交错级数、莱布尼兹定理、正项级数各判别法全部串联起来，是比较审敛法「大收则小收」的延伸应用。
- **出处**：[陈哥 P122](https://www.bilibili.com/video/BV1husGzwEtZ?p=122)；[杰哥 P166](https://www.bilibili.com/video/BV1Up4y1Y76a?p=166)；[ok姐 P132](https://www.bilibili.com/video/BV1vm421s7mv?p=132)

### 绝对收敛与条件收敛典型题型
- **要点**：判断步骤为「先看本身、再加绝对值」。本身含 (−1)^n 时用莱布尼兹判别法判收敛；再加绝对值化为 Σ1/(n²+n)（抓大头成 1/n²，p 级数收敛）或 Σ1/n（调和，发散），据此区分绝对收敛与条件收敛。另一类考点是「由 Σu_n 收敛能推出什么」：只有通项趋于零、收敛±收敛、收敛±发散三条成立，Σu_n² 是否收敛不能确定（反例：Σ(−1)^n/√n 收敛，其平方为调和级数发散）。条件收敛加发散仍为发散。
- **关键概念**：`先本身后绝对值`、`反例`、`收敛平方不确定`
- **出处**：[杰哥 P166](https://www.bilibili.com/video/BV1Up4y1Y76a?p=166)

### 函数项级数与幂级数
- **要点**：把常数项级数通项中的常数换成函数，就得到函数项级数 Σu_n(x)（每一项都是关于 x 的函数，定义在区间 I 上）。若 u_n(x) 的底数是幂函数、指数是 n 次方（或其变形），则该函数项级数称为幂级数，一般形式为 Σa_n(x−x₀)^n 或 Σ\_\{n=0\}^∞ a_n x^n，其中 a_n 是与 x 无关的系数项（常数部分）；含 x 的部分为函数部分。当 x 取定一个数值时，函数项级数就退化为常数项级数。
- **关键概念**：`函数项级数`、`幂级数`、`系数项`、`系数 a_n`、`常数项级数`
- **相互关系**：幂级数是函数项级数的特例，同样有收敛点、收敛域、和函数等概念；敛散性取决于 x 的取值，故讨论的对象由「级数」转为「x 的范围」。
- **出处**：[陈哥 P123](https://www.bilibili.com/video/BV1husGzwEtZ?p=123)；[杰哥 P167](https://www.bilibili.com/video/BV1Up4y1Y76a?p=167)；[ok姐 P133](https://www.bilibili.com/video/BV1vm421s7mv?p=133)、[P134](https://www.bilibili.com/video/BV1vm421s7mv?p=134)

### 收敛点、发散点、收敛域与和函数
- **要点**：幂级数中 x 取不同值时，对应的常数项级数敛散性可能不同。若 x=x₁ 时对应的常数项级数收敛，则称 x₁ 为收敛点；若发散则称 x₁ 为发散点。收敛点全体为收敛域（或收敛点构成的集合即为收敛区间），发散点全体为发散域。收敛域 D 中每个 x 对应唯一一个收敛常数项级数的和，这种一一对应构成函数 S(x)，称为函数项级数的和函数，其定义域即收敛域，即 S(x)=Σu_n(x)=lim S_n(x)。求某点处常数项级数的和，可直接把该点代入和函数。
- **关键概念**：`收敛点`、`发散点`、`收敛域`、`发散域`、`和函数 S(x)`、`部分和 S_n(x)`
- **相互关系**：引出收敛域的概念——所有收敛点的集合；把函数项级数逐点化为常数项级数，即可沿用前面的判敛工具。
- **出处**：[陈哥 P123](https://www.bilibili.com/video/BV1husGzwEtZ?p=123)；[杰哥 P167](https://www.bilibili.com/video/BV1Up4y1Y76a?p=167)；[ok姐 P133](https://www.bilibili.com/video/BV1vm421s7mv?p=133)

### 收敛区间与收敛半径
- **要点**：令 ρ(x)=lim|u\_\{n+1\}(x)/u_n(x)|，解不等式 ρ(x)&lt;1 得到 x 的范围，即为收敛区间；收敛区间一定是开区间 (a,b)。收敛半径 R 等于收敛区间长度的一半，即 R=(b−a)/2。标准形 Σa_n x^n 时，收敛半径 R=lim|a_n/a\_\{n+1\}|（即用 x^n 前的系数除以 n+1 次项的系数再取绝对值）。特例：R=+∞ 时收敛区间为 (−∞,+∞)（ρ=0 时），R=0 时退化为单点 x=0（ρ=+∞ 时）。求极限时 x 视为常数（类比求偏导中「每次只关注一个变量」），极限算完后 x 才转为自变量；含绝对值不能丢。
- **关键概念**：`收敛区间`、`收敛半径 R`、`开区间`、`系数之比`
- **相互关系**：知道收敛区间即可求半径与收敛域，因此核心问题归结为「如何求收敛区间」；级数从 n=0 还是 n=1 起始会影响 a_n 的写法，也可直接用「后一项系数比前一项系数」避开。
- **出处**：[陈哥 P123](https://www.bilibili.com/video/BV1husGzwEtZ?p=123)；[杰哥 P167](https://www.bilibili.com/video/BV1Up4y1Y76a?p=167)；[学士帽 P94](https://www.bilibili.com/video/BV1X4411J792?p=94)；[ok姐 P134](https://www.bilibili.com/video/BV1vm421s7mv?p=134)、[P135](https://www.bilibili.com/video/BV1vm421s7mv?p=135)

### 收敛域端点的判断
- **要点**：收敛半径只给出开区间 (−R,R)，端点 x=±R 处可能收敛也可能发散，必须把两个端点分别代回原级数用数项级数的方法判断——得到调和级数（或其差一个负号）则发散，得到交错级数则用莱布尼兹判别法；常用第 n 项判别法（如 Σn、Σ(−1)^n n 通项不为零即发散）快速定端点。最终收敛域由开区间加上收敛的端点组成，可写成半开半闭区间。共有四种组合：两端都发散为开区间、两端都收敛为闭区间、一端收敛一端发散为半开半闭。收敛域是收敛区间与端点的并集，在专升本阶段一定是连续的范围。
- **关键概念**：`收敛域`、`端点`、`代入原级数`、`闭区间`
- **出处**：[陈哥 P123](https://www.bilibili.com/video/BV1husGzwEtZ?p=123)；[杰哥 P169](https://www.bilibili.com/video/BV1Up4y1Y76a?p=169)；[学士帽 P94](https://www.bilibili.com/video/BV1X4411J792?p=94)；[ok姐 P135](https://www.bilibili.com/video/BV1vm421s7mv?p=135)

### 求收敛域的完整步骤
- **要点**：①求收敛半径 R（必要时先换元）；②写出收敛区间；③把两个端点分别代入，得到常数项级数并判定其敛散性（常用 p 级数、等比级数、莱布尼兹定理）；④写出收敛域。端点判定要调用前面所有判敛工具，是级数知识的综合应用点。
- **关键概念**：`端点判定`、`收敛域`
- **出处**：[ok姐 P135](https://www.bilibili.com/video/BV1vm421s7mv?p=135)

### 求收敛区间的方法一：比值判别法
- **要点**：把 Σu_n(x) 视为正项级数并加绝对值，强行令 lim|u\_\{n+1\}/u_n|&lt;1，解此不等式所得 x 的范围就是收敛区间；再讨论端点得收敛域。根值判别法 lim √[n]{|u_n|}&lt;1 同理（遇到 (1+1/n)\^\{n²\} 这类含第二重要极限的式子时，用此法可快速得到 ρ=e|x|），但考题中比值法最常用。
- **关键概念**：`强行令小于一`、`解不等式`、`端点讨论`、`根值法`
- **相互关系**：与正项级数的根值判别法同源。
- **出处**：[杰哥 P168](https://www.bilibili.com/video/BV1Up4y1Y76a?p=168)；[陈哥 P123](https://www.bilibili.com/video/BV1husGzwEtZ?p=123)

### 求收敛区间的方法二：公式法
- **要点**：对标准形 Σa_n x^n，先算 ρ=lim|a\_\{n+1\}/a_n|，则收敛半径 R=1/ρ，收敛区间为 (−1/ρ, 1/ρ)。ρ=0 时 R=+∞（整个数轴收敛），ρ=+∞ 时 R=0。只适用于 x 的 n 次这种标准形（不缺项），由比值判别法推导而来，优点是只看系数 a_n。
- **关键概念**：`公式法`、`ρ`、`R=1/ρ`、`不缺项`
- **出处**：[杰哥 P168](https://www.bilibili.com/video/BV1Up4y1Y76a?p=168)

### 具体型幂级数求收敛区间
- **要点**：题干直接给出 a_n 的具体表达式。两条路径：用比值判别法带 x 整体运算，或只用系数套公式法，两者结果一致。求出 x 范围后取一半得半径，再代 x=±R 讨论端点敛散性得收敛域。
- **关键概念**：`具体型`、`端点代入`、`通项判别法判端点`
- **出处**：[杰哥 P169](https://www.bilibili.com/video/BV1Up4y1Y76a?p=169)

### 抽象型幂级数求收敛区间
- **要点**：题干只给 Σa_n(x−x₀)^n 而不给 a_n。三条储备结论：①对称中心为使 x−x₀=0 的点 x=x₀；②收敛区间内部绝对收敛，外部发散，条件收敛只能出现在端点；③系数相同的级数（如 Σa_n(x−1)^n 与 Σa_n x^n）只是自变量平移，收敛半径相同、两端敛散性相同。解题靠画数轴：由已知点的敛散性向中心对称过去，定出半径与另一侧端点，再判断所求点落在区间内部（绝对收敛）、端点（需讨论）还是外部（发散）。
- **关键概念**：`抽象型`、`对称中心`、`内部绝对收敛`、`条件收敛只在端点`
- **出处**：[杰哥 P170](https://www.bilibili.com/video/BV1Up4y1Y76a?p=170)

### 复合型幂函数的换元
- **要点**：若幂函数部分不是单纯的 x^n（如 (x−1)^n、(x²)^n），先令 t=x−1 等换元，求出关于 t 的收敛区间 −R&lt;t&lt;R，再解不等式还原为 x 的收敛区间。公式求出的 −R&lt;R 是「整体」的范围而非 x 的范围，漏换元会直接把区间写错；注意 (2x)^n 可写成 2^n x^n 归入系数，不属复合。
- **关键概念**：`换元`、`复合幂函数`
- **出处**：[ok姐 P135](https://www.bilibili.com/video/BV1vm421s7mv?p=135)

### 阿贝尔定理
- **要点**：若幂级数在 x₀ 处收敛，则满足 |x|&lt;|x₀| 的一切 x 都使幂级数绝对收敛；若在 x₀ 处发散，则满足 |x|>|x₀| 的一切 x 都使幂级数发散；几何上表现为以原点为中心的对称区间。它是收敛半径与收敛区间存在的理论依据。由此可得：在收敛区间内部，对应的常数项级数一定绝对收敛；在收敛区间的两个端点上，若对应的常数项级数收敛，则必定是条件收敛。
- **关键概念**：`阿贝尔定理`、`绝对收敛`、`对称区间`、`条件收敛`
- **相互关系**：可用来验证端点处的收敛类型，与任意项级数的两步判定法互相印证。
- **出处**：[陈哥 P123](https://www.bilibili.com/video/BV1husGzwEtZ?p=123)；[ok姐 P134](https://www.bilibili.com/video/BV1vm421s7mv?p=134)

### 多个幂级数相加时收敛区间的取法
- **要点**：若一个幂级数由两个幂级数相加而成，需分别求出各自收敛区间，再取二者的交集作为整体收敛区间，收敛半径取较小者。
- **关键概念**：`交集`、`取小半径`
- **出处**：[陈哥 P123](https://www.bilibili.com/video/BV1husGzwEtZ?p=123)

### 幂级数的连续性、逐项积分与逐项求导
- **要点**：幂级数的和函数 S(x) 在其收敛域上连续（收敛域内一点处的极限等于该点的函数值）。和函数在收敛域上可积，且可逐项积分：∫_0^T S(x)dx=Σ∫_0^T a_n x^n dx=Σ a_n T\^\{n+1\}/(n+1)；和函数在收敛区间内可导，且可逐项求导：S′(x)=Σ(a_n x^n)′=Σ n a_n x\^\{n−1\}。逐项积分与逐项求导后的幂级数与原级数收敛半径相同（但两个端点的收敛性可能改变，必须单独代入端点判断）。
- **关键概念**：`和函数连续性`、`逐项积分`、`逐项求导`、`收敛半径不变`
- **相互关系**：逐项积分后的新级数常是等比级数，可直接求和，是求和方法的核心步骤；逐项积分与逐项求导互为逆操作。
- **出处**：[ok姐 P136](https://www.bilibili.com/video/BV1vm421s7mv?p=136)；[陈哥 P127](https://www.bilibili.com/video/BV1husGzwEtZ?p=127)

### 幂级数和函数：先积分后求导型
- **要点**：当幂级数的系数 a_n 为整式（无分数线，如 n、n²、n(n+1)）时用此法。步骤：求收敛域 → 令级数为 S(x)，两边取变上限积分 ∫\_\{x₀\}\^\{x\}，把被积式里的 x 换成 t、dx 换成 dt → 对积分结果求导还原。配凑原则：使用前必须把级数凑成「x 的指数恰为前面整式因式减一」，否则积分后系数消不掉（如 ∫4x⁴dx=4x⁵/5，系数仍残留）；若指数是因式加一，则外提 x² 之类的公因子调整。
- **关键概念**：`整式`、`分式`、`变上限函数`、`收敛区间中心`、`配凑`
- **相互关系**：与「先导后积」互为对照——a_n 为分式用先导后积，为整式用先积分后求导；目的都是消掉系数 a_n；与先导后积的配凑要求相反（那里要求指数与分母相同）。
- **出处**：[陈哥 P126](https://www.bilibili.com/video/BV1husGzwEtZ?p=126)

### 幂级数求和函数的两条通用手段
- **要点**：积分或求导后得到的级数用「一减公比分之首项」化为 x 的函数；再用变上限函数求导还原（上限代入乘以上限导数，减去下限代入乘以下限导数）。无论先导后积还是先积后导，中间结果必是 x 的函数。
- **关键概念**：`一减公比分之首项`、`公比`、`首项`、`变上限函数求导`
- **出处**：[陈哥 P126](https://www.bilibili.com/video/BV1husGzwEtZ?p=126)

### 求幂级数和函数的步骤
- **要点**：①求收敛域，作为和函数的定义域；②在收敛域上写出 S(x)=Σa_n x^n；③两端积分，右边逐项积分并求和（多为等比级数，用 A(1−q^n)/(1−q) 取极限）；④把结果视为积分上限函数，对 T 求导得 S(x)。如 Σ\_\{n=0\}^∞(n+1)x^n=1/(1−x)²，即积分得 T/(1−T) 后求导；注意积分变量用 T、最后把 T 换回 x。
- **关键概念**：`和函数`、`逐项积分`、`积分上限函数求导`
- **出处**：[ok姐 P136](https://www.bilibili.com/video/BV1vm421s7mv?p=136)

### 逐项求导 + 微分方程求 Σx^n/n!
- **要点**：无法用先导后积/先积后导的特殊题型只能逐项求导。对 Σx^n/n! 逐项求导后结果与原级数完全相同，得 S′(x)=S(x)，即一阶线性微分方程，用通解公式并由初始条件 S(0)=1 定常数，得 S(x)=e^x。
- **关键概念**：`逐项求导`、`阶乘`、`一阶线性微分方程`、`初始条件`
- **相互关系**：结论 e^x=Σx^n/n! 即后面必背的麦克劳林展开式。
- **出处**：[陈哥 P126](https://www.bilibili.com/video/BV1husGzwEtZ?p=126)

### 数项级数求和
- **要点**：把待求数项级数配凑成已知和函数的形式，使该级数恰为 S(x) 在某个具体 x 值处的取值，再代入和函数求值。常用手法：提公因子、拆项、把 3^n 写成 (√3)\^\{2n\} 以对齐结构。
- **关键概念**：`配凑`、`和函数取值`
- **出处**：[陈哥 P126](https://www.bilibili.com/video/BV1husGzwEtZ?p=126)、[P127](https://www.bilibili.com/video/BV1husGzwEtZ?p=127)

### 六个麦克劳林展开式（基础框架）
- **要点**：1/(1−x)、1/(1+x)、e^x、ln(1+x)、sin x、cos x 六个展开式必须背熟，前四个是绝大多数省份的考查范围。1/(1±x) 的范围是 (−1,1)，e^x 无限制，ln(1+x) 的范围是 (−1,1] 且 n 从 1 开始（其余从 0 开始）。
- **关键概念**：`麦克劳林展开式`、`基础框架`、`收敛范围`
- **相互关系**：是幂级数展开一切题目的基础；其逆过程就是求和函数。
- **出处**：[陈哥 P127](https://www.bilibili.com/video/BV1husGzwEtZ?p=127)

### 等价无穷小源于麦克劳林展开
- **要点**：等价无穷小由麦克劳林展开式截断高阶项得到。例如 e^x=1+x+… 舍去二次以上项得 e^x−1~x；ln(1+x) 保留到二次项得 x−ln(1+x)~x²/2；(1+x)^α−1~αx。用不到高阶精度时就按需要截断。
- **关键概念**：`等价无穷小`、`截断高阶项`、`阶`
- **出处**：[陈哥 P127](https://www.bilibili.com/video/BV1husGzwEtZ?p=127)

### 框架替换与配框架
- **要点**：六个框架中的 x 可整体替换为任意「方框」表达式（与等价无穷小的整体替换同理）。展开时先配出目标整体并绑定不可拆，再选框架、提系数把式子配成框架标准形，最后把方框整体代入展开式。
- **关键概念**：`框架`、`整体替换`、`配框架`
- **出处**：[陈哥 P127](https://www.bilibili.com/video/BV1husGzwEtZ?p=127)

### 展开成 (x−a) 幂级数的步骤
- **要点**：①在函数中配出目标整体 (x−a) 并绑定；②选对应框架；③提公因子配成框架标准形；④代入框架展开式；⑤整理成含 (x−a)^n 的形式；⑥由方框范围 −1&lt;方框&lt;1 反解 x 的范围。
- **关键概念**：`配整体`、`基础框架`、`收敛范围反解`
- **出处**：[陈哥 P127](https://www.bilibili.com/video/BV1husGzwEtZ?p=127)

### 有理分式函数的展开
- **要点**：分母为二次多项式时，先因式分解，再用待定系数法拆成两个简单分式之和（通分后比较 x 项系数与常数项求 A,B），然后逐项提系数、配框架展开，最后合并同类项并把两个收敛范围取交集。
- **关键概念**：`因式分解`、`待定系数法`、`拆项`、`收敛范围取交集`
- **出处**：[陈哥 P127](https://www.bilibili.com/video/BV1husGzwEtZ?p=127)

### 幂指函数与对数函数的展开
- **要点**：底数不是 e 的指数函数用指数对数化 a\^\{g(x)\}=e\^\{g(x)ln a\}，再按 e^x 框架展开。ln 函数要在真数中提公因子凑成 1+方框，并把真数的乘积拆成对数相加。两者都属于「配框架」的具体手法。
- **关键概念**：`指数对数化`、`对数运算法则`
- **出处**：[陈哥 P127](https://www.bilibili.com/video/BV1husGzwEtZ?p=127)

### 通过求导/积分求非标准函数的展开
- **要点**：函数本身不便直接展开时从导数或积分入手。arctan x 先求导得 1/(1+x²)，按 1/(1+x) 框架把 x² 当整体展开，再两边取 [0,x] 上的变上限积分还原；1/x² 则先展开 1/x 再两边求导。
- **关键概念**：`先求导后积分`、`变上限积分`、`(arctan x)′=1/(1+x²)`
- **相互关系**：与「先积分后求导」是互逆的操作思路。
- **出处**：[陈哥 P127](https://www.bilibili.com/video/BV1husGzwEtZ?p=127)

### 求导/积分后端点的收敛性变化
- **要点**：对幂级数求导或积分后收敛半径不变，但两个端点的收敛性可能改变，必须单独代入端点判断。例如 arctan x 展开后在 x=±1 处化为交错级数，由莱布尼兹定理判定为条件收敛，故范围要写成 −1≤x≤1。
- **关键概念**：`收敛半径不变`、`端点收敛性`、`莱布尼兹定理`、`条件收敛`
- **出处**：[陈哥 P127](https://www.bilibili.com/video/BV1husGzwEtZ?p=127)

### 泰勒展开式
- **要点**：若 f(x) 在 x₀ 的某邻域可展开为幂级数，则 f(x)=Σ\_\{n=0\}^∞ a_n(x−x₀)^n，系数由 a_n=f\^\{(n)\}(x₀)/n! 给出（即 a₀=f(x₀)、a₁=f′(x₀)、a₂=f″(x₀)/2! 等）；(x−x₀)^n 部分照搬，只需逐项求各阶导数算系数。
- **关键概念**：`泰勒展开式`、`各阶导数`、`系数公式`
- **相互关系**：与「求幂级数和函数」是同一等式的两个方向（求和 ↔ 展开）。
- **出处**：[ok姐 P137](https://www.bilibili.com/video/BV1vm421s7mv?p=137)

### 麦克劳林展开式
- **要点**：泰勒展开式中取 x₀=0，得 f(x)=Σ\_\{n=0\}^∞ f\^\{(n)\}(0)/n! x^n；例如 e^x=Σ\_\{n=0\}^∞ x^n/n!（e^x 各阶导数恒为自身，在 0 处均为 1，故 a_n=1/n!）。
- **关键概念**：`麦克劳林展开式`、`指数函数展开式`
- **相互关系**：是泰勒展开式的特例；常见函数的展开式（e^x、sin x、1/(1+x) 等）了解即可。
- **出处**：[ok姐 P137](https://www.bilibili.com/video/BV1vm421s7mv?p=137)

### 傅里叶级数
- **要点**：又称三角级数，各项为「常数×三角函数」，形式为 a₀/2+Σ\_\{n=1\}^∞(a_n cos nx+b_n sin nx)；系数由 a_n=(1/π)∫\_\{−π\}\^\{π\}f(x)cos nx dx、b_n=(1/π)∫\_\{−π\}\^\{π\}f(x)sin nx dx 求出，称为傅里叶系数；代入三角级数所得的级数才叫傅里叶级数。
- **关键概念**：`三角级数`、`傅里叶系数`、`a_n`、`b_n`
- **相互关系**：与幂级数并列的另一类函数项级数（常数×幂函数 vs 常数×三角函数）；系数必须按上述积分公式求得，并非所有三角级数都是傅里叶级数。
- **出处**：[ok姐 P138](https://www.bilibili.com/video/BV1vm421s7mv?p=138)


### 常数项级数的定义与一般项
- **要点**：给定无穷数列 $u_1,u_2,\cdots,u_n,\cdots$，把它的所有项相加就叫做常数项无穷级数，简称常数项级数，记作 $\sum\_\{n=1\}\^\{\infty\}u_n$，其中 $u_n$ 叫一般项（通项）。级数是一个数，不是一个数列。
- **关键概念**：`常数项级数`、`$\sum_{n=1}^{\infty}u_n$`、`一般项 $u_n$`、`级数是一个数`
- **相互关系**：给级数写通项靠观察分母、分子与 $n$ 的关系，正负交替用 $(-1)^n$ 或 $(-1)\^\{n-1\}$ 表示；一般项是后续所有敛散性判定的入口。
- **出处**：[石头 P94](https://www.bilibili.com/video/BV18CL26WEJ3?p=94)

### 级数的收敛与发散
- **要点**：级数的和等于前 $n$ 项和 $S_n$ 当 $n\to\infty$ 时的极限，即 $\sum\_\{n=1\}\^\{\infty\}u_n=\lim\_\{n\to\infty\}S_n$。该极限存在则称级数收敛，极限不存在（趋于无穷或来回摆动）则称级数发散。因此求级数的和就是先求前 $n$ 项和再取极限。
- **关键概念**：`前 $n$ 项和 $S_n$`、`$\lim_{n\to\infty}S_n$`、`收敛`、`发散`
- **相互关系**：与数列极限中「收敛即极限存在」的概念一致；判断敛散性有时不必求出具体的和，收敛与「和为多少」是两件事。
- **出处**：[石头 P94](https://www.bilibili.com/video/BV18CL26WEJ3?p=94)

### 用定义判断级数的敛散性
- **要点**：先用定义法写出前 $n$ 项和 $S_n$，再求 $n\to\infty$ 的极限。通项形如 $\frac{1}{n(n+1)}$ 时用裂项 $\frac{1}{n(n+1)}=\frac1n-\frac{1}{n+1}$，求和时中间项全部相消，只剩首尾两项，$S_n=1-\frac{1}{n+1}$，极限为 $1$，故收敛；通项形如 $\sqrt{n+1}-\sqrt{n}$ 时也逐项相消，只剩 $\sqrt{n+1}-1$，极限为无穷，故发散。
- **关键概念**：`定义法`、`裂项相消`、`$\frac{1}{n(n+1)}=\frac1n-\frac{1}{n+1}$`、`$\sqrt{n+1}-\sqrt{n}$`
- **相互关系**：等差数列型通项（如 $u_n=n$）的前 $n$ 项和为 $\frac{n(1+n)}{2}$，极限为无穷，故发散；裂项相消的关键是看清哪些项互相抵消。
- **出处**：[石头 P94](https://www.bilibili.com/video/BV18CL26WEJ3?p=94)

### 收敛级数的性质
- **要点**：若 $\sum u_n$ 收敛于 $S$，则 $\sum ku_n$ 也收敛且和为 $kS$（$k\neq0$ 时两者敛散性相同）；若 $\sum u_n$、$\sum v_n$ 分别收敛于 $S$、$\sigma$，则 $\sum(u_n\pm v_n)$ 收敛于 $S\pm\sigma$。推论是收敛级数加减发散级数必发散，两个发散级数相加减敛散性不确定。去掉、加上或改变级数的有限项不改变敛散性；收敛级数任意加括号后仍收敛且和不变。
- **关键概念**：`$k$ 倍级数`、`收加减收等于收`、`收加减发等于发`、`发加减发不确定`、`有限项不影响敛散性`、`加括号和不变`
- **相互关系**：这几条性质都很直观，考试很少单独出题；性质三讲「有限项」、性质五讲「通项」，分别对应局部与整体。
- **出处**：[石头 P94](https://www.bilibili.com/video/BV18CL26WEJ3?p=94)

### 收敛的必要条件与发散判定
- **要点**：级数收敛的必要条件是 $\lim\_\{n\to\infty\}u_n=0$。其逆否命题是判断发散的重要工具：若 $\lim\_\{n\to\infty\}u_n\neq0$，则级数一定发散。但逆命题不成立——通项极限为 $0$ 推不出收敛（如 $\sum\frac{1}{n}$、$\sum\sin\frac1n$ 都发散），这时需要后续课程的其他方法。
- **关键概念**：`必要条件`、`$\lim_{n\to\infty}u_n=0$`、`逆否命题`、`通项极限不为零则发散`
- **相互关系**：用这一条判断发散时先求通项极限，不为零立即发散，不必算前 $n$ 项和；若极限为零则此路不通，不能据此断定收敛。
- **出处**：[石头 P94](https://www.bilibili.com/video/BV18CL26WEJ3?p=94)

### 等比级数的定义与首项公比
- **要点**：各项构成等比数列的级数叫等比级数，也叫几何级数，通项为 $u_n=aq\^\{n-1\}$，其中首项 $a\neq0$、公比 $q$ 为常数，展开即 $a+aq+aq^2+\cdots+aq\^\{n-1\}+\cdots$。识别特征是通项写成「常数的 $n$ 次方」，这个常数就是公比 $q$，把 $n$ 的起点代入即可定出首项。
- **关键概念**：`等比级数`、`几何级数`、`$u_n=aq^{n-1}$`、`首项 $a$`、`公比 $q$`
- **相互关系**：必须与 P 级数 $\sum\frac{1}{n^p}$ 区分——$\sum\frac{1}{2^n}$ 是等比级数，$\sum\frac{1}{n^2}$ 是 P 级数；含负指数时（如 $\sum3\^\{-n\}$）先化成 $\sum\frac{1}{3^n}$ 再看公比。
- **出处**：[石头 P95](https://www.bilibili.com/video/BV18CL26WEJ3?p=95)

### 等比级数的审敛法与求和公式
- **要点**：只比较 $\lvert q\rvert$ 与 $1$：$\lvert q\rvert&lt;1$ 时级数收敛且和为 $S=\frac{a}{1-q}$；$\lvert q\rvert\geq1$ 时级数发散。推导由等比数列前 $n$ 项和 $S_n=\frac{a(1-q^n)}{1-q}$ 取 $\lim\_\{n\to\infty\}S_n$ 得到，$\lvert q\rvert&lt;1$ 时 $q^n\to0$；$q=1$ 时分母为零需单独讨论，此时 $S_n=na\to\infty$。
- **关键概念**：`$\lvert q\rvert<1$ 收敛`、`$\lvert q\rvert\geq1$ 发散`、`$S=\frac{a}{1-q}$`、`$S_n=\frac{a(1-q^n)}{1-q}$`
- **相互关系**：与 P 级数的判据方向正好相反（P 级数是 $p>1$ 收敛），最容易记混；题目中出现「若收敛求其和」时，基本可以断定它就是等比级数。
- **出处**：[石头 P95](https://www.bilibili.com/video/BV18CL26WEJ3?p=95)

### 等比级数的识别与拆分求和应用
- **要点**：见到 $\sum a^nb^n$ 要先合并为 $\sum(ab)^n$ 再读公比，如 $\sum\frac{(-5)^n}{6^n}=\sum\left(-\frac56\right)^n$。遇到 $\sum(a^n\pm b^n)$ 不能合并成 $(a\pm b)^n$（没有这个公式），须拆成两个级数分别判断：两者都收敛时原级数收敛，和等于两个和相加减。
- **关键概念**：`$a^nb^n=(ab)^n$`、`拆分求和`、`收敛级数的线性性质`
- **相互关系**：拆分的前提是各部分都收敛，与后文比较审敛法中「发散部分不能拆」相呼应；求和时先定首项（代入 $n$ 的起点）再套 $\frac{a}{1-q}$。
- **出处**：[石头 P95](https://www.bilibili.com/video/BV18CL26WEJ3?p=95)

### P级数的定义与通项
- **要点**：通项为 $\frac{1}{n^p}$（$p>0$ 为常数）的级数叫 P 级数，展开为 $1+\frac{1}{2^p}+\frac{1}{3^p}+\cdots+\frac{1}{n^p}+\cdots$，首项恒为 $1$。只要 $p>0$ 就属于 P 级数，$p$ 可以是 $\frac12$、$\frac14$ 这类分数。
- **关键概念**：`P 级数`、`$\sum\frac{1}{n^p}$`、`$p>0$`
- **相互关系**：与等比级数形式互为对照——$\sum\frac{1}{n^2}$ 是 P 级数，$\sum\frac{1}{2^n}$ 是等比级数，二者把「底数变」和「指数变」对调了。
- **出处**：[石头 P96](https://www.bilibili.com/video/BV18CL26WEJ3?p=96)

### 调和级数
- **要点**：当 $p=1$ 时级数 $\sum\frac{1}{n}$ 称为调和级数，它是 P 级数的特例，且恒为发散。
- **关键概念**：`调和级数`、`$\sum\frac{1}{n}$`、`发散`
- **相互关系**：调和级数是比较审敛法中最常用的「发散参照物」，也常出现在幂级数端点代入后的敛散性判断里。
- **出处**：[石头 P96](https://www.bilibili.com/video/BV18CL26WEJ3?p=96)

### P级数的审敛法与参数范围
- **要点**：判据是看 $p$：$p>1$ 时收敛，$p\leq1$ 时发散，与等比级数的判据方向相反。若已知级数收敛而 $p$ 中含参数（如 $p=x^2-1$），由 $p>1$ 解不等式，答案必须写成区间或集合形式，如 $(-\infty,-\sqrt2)\cup(\sqrt2,+\infty)$。
- **关键概念**：`$p>1$ 收敛`、`$p\leq1$ 发散`、`参数范围`、`区间形式作答`
- **相互关系**：易错点是把两个判据记混；等号归入发散一侧，所以调和级数发散；只写不等式而不写区间会扣分。
- **出处**：[石头 P96](https://www.bilibili.com/video/BV18CL26WEJ3?p=96)

### 正项级数的概念
- **要点**：每一项都大于零的级数叫正项级数。它不是一个与等比、P 级数并列的分类，同一个级数可以既是正项级数又是等比级数或 P 级数；此时优先用等比或 P 级数的判据，因为只需看 $q$ 或 $p$，最简单。
- **关键概念**：`正项级数`、`$u_n>0$`、`分类不互斥`
- **相互关系**：只有正项级数才能用比值、比较、根值三种审敛法，因此判断任意项级数时通常先加绝对值把它化为正项级数。
- **出处**：[石头 P97](https://www.bilibili.com/video/BV18CL26WEJ3?p=97)

### 比值审敛法
- **要点**：计算 $\rho=\lim\_\{n\to\infty\}\frac{u\_\{n+1\}}{u_n}$，即后一项比前一项再取极限。$\rho&lt;1$ 时级数收敛，$\rho>1$ 或为 $+\infty$ 时发散，$\rho=1$ 时方法失效需改用其他方法。直观理解：后项比前项小则各项越来越靠近零、可能收敛，越来越大则发散。
- **关键概念**：`比值审敛法`、`达朗贝尔判别法`、`$\rho=\lim\frac{u_{n+1}}{u_n}$`
- **相互关系**：与等比级数判据本质一致（$\rho$ 就是公比），可用来验证等比级数结论；极限为无穷虽属「极限不存在」，但按 $\rho>1$ 直接判发散。
- **出处**：[石头 P97](https://www.bilibili.com/video/BV18CL26WEJ3?p=97)

### 比值审敛法的适用题型与常用化简
- **要点**：通项含 $a^n$、$n^n$ 或 $n!$ 时优先用比值审敛法，因为后项比前项能大量约分。三个常用化简：$\frac{a\^\{n+1\}}{a^n}=a$；$\frac{(n+1)\^\{n+1\}}{n^n}=(n+1)\left(1+\frac1n\right)^n$；$\frac{(n+1)!}{n!}=n+1$。写 $u\_\{n+1\}$ 时把通项中所有 $n$ 都换成 $n+1$。
- **关键概念**：`$a^n$`、`$n^n$`、`$n!$`、`$(n+1)!=n!(n+1)$`
- **相互关系**：化简后若出现 $\left(1+\frac1n\right)^n$ 这类「$1$ 的无穷次方」型，要用第二重要极限处理；通项是多项式时最后用抓大头得系数比。
- **出处**：[石头 P97](https://www.bilibili.com/video/BV18CL26WEJ3?p=97)

### 比较审敛法的一般形式
- **要点**：设 $\sum u_n$、$\sum v_n$ 都是正项级数且 $u_n\leq v_n$：若大的 $\sum v_n$ 收敛，则小的 $\sum u_n$ 收敛；若小的 $\sum u_n$ 发散，则大的 $\sum v_n$ 发散。口诀「大收则小收，小发则大发」。
- **关键概念**：`比较审敛法`、`$u_n\leq v_n$`、`大收则小收`、`小发则大发`
- **相互关系**：参照级数必须选得合适——想证收敛要与收敛级数比且自己更小，想证发散要与发散级数比且自己更大，方向弄反得不到任何结论。
- **出处**：[石头 P98](https://www.bilibili.com/video/BV18CL26WEJ3?p=98)

### 参照级数的选取与放缩
- **要点**：找参照物常靠放缩：舍掉分子中的因子会放大，如 $\frac{1}{n\cdot2^n}\leq\frac{1}{2^n}$，于是可与已知敛散性的等比级数比较。含 $\lvert\sin n\rvert$、$\lvert\cos n\rvert$ 时，因 $\lvert\sin n\rvert\leq1$、$\lvert\cos n\rvert\leq1$，把因子换成 $1$ 即得参照级数。
- **关键概念**：`放缩`、`舍项`、`$\lvert\sin n\rvert\leq1$`、`$\lvert\cos n\rvert\leq1$`
- **相互关系**：$\lvert\sin n\rvert$、$\lvert\cos n\rvert$ 型在判断绝对收敛时会反复用到；放缩只能向一个方向走，舍项是放大、补项是缩小，先判断目标再决定取舍。
- **出处**：[石头 P98](https://www.bilibili.com/video/BV18CL26WEJ3?p=98)

### 比较审敛法的极限形式与找 $v_n$ 的两种思路
- **要点**：极限形式：取 $\lim\_\{n\to\infty\}\frac{u_n}{v_n}=l$，参照级数 $v_n$ 必须放在分母。$l=0$ 时 $v_n$ 大，$\sum v_n$ 收敛则 $\sum u_n$ 收敛；$l=+\infty$ 时 $u_n$ 大，$\sum v_n$ 发散则 $\sum u_n$ 发散；$l$ 为非零常数时二者敛散性相同。找 $v_n$ 有两条路：$u_n$ 是无穷小时取它的等价无穷小，如 $\sin\frac1n\sim\frac1n$、$e\^\{1/n\^2\}-1\sim\frac{1}{n^2}$、$\ln\left(1+\frac1n\right)\sim\frac1n$；$u_n$ 是多项式时用抓大头取分子分母的最高次。
- **关键概念**：`极限形式`、`等价无穷小`、`抓大头`、`二者敛散性相同`
- **相互关系**：与求极限的抓大头口诀「上大无穷下大零、同次系数比」完全对应；极限形式的思路比一般形式更机械，不必凭空猜放缩方向，因此是首选做法。
- **出处**：[石头 P98](https://www.bilibili.com/video/BV18CL26WEJ3?p=98)

### 根值审敛法及其适用题型
- **要点**：计算 $\rho=\lim\_\{n\to\infty\}\sqrt[n]{u_n}$，$\rho&lt;1$ 时收敛，$\rho>1$ 时发散，$\rho=1$ 时失效。适用于通项整体含 $n$ 次方的形式，因为 $\sqrt[n]{u_n}=u_n\^\{\frac1n\}$ 会把原有的 $n$ 次方抵消，式子立刻变简单，例如 $\sqrt[n]{n^n}=n\to\infty$ 判发散、$\sqrt[n]{\left(\frac1n\right)^n}=\frac1n\to0$ 判收敛。
- **关键概念**：`根值审敛法`、`$\rho=\lim\sqrt[n]{u_n}$`、`整体 $n$ 次方`
- **相互关系**：与比值审敛法判据形式相同，只是取极限对象不同；开方后若出现有界量（如 $(-1)^n$）除以 $n$，用「有界乘无穷小仍为无穷小」得极限为零。
- **出处**：[石头 P99](https://www.bilibili.com/video/BV18CL26WEJ3?p=99)

### 三种正项级数审敛法的总结
- **要点**：比值法问「谁比谁」——后一项比前一项；比较法问「跟谁比」——找一个已知敛散性的等比或 P 级数作参照；根值法是开 $n$ 次方后求极限。三种方法的临界值都是 $1$，等于 $1$ 时全部失效。
- **关键概念**：`比值审敛法`、`比较审敛法`、`根值审敛法`、`临界值为 1`
- **相互关系**：通项含 $a^n$、$n^n$、$n!$ 想比值，通项是无穷小或多项式想比较，通项整体是 $n$ 次方想根值；选错方法会算不出来，做题前先看特征。
- **出处**：[石头 P99](https://www.bilibili.com/video/BV18CL26WEJ3?p=99)

### 交错级数的定义与标准形式
- **要点**：正负项交替出现的级数叫交错级数，标准形式为 $\sum(-1)\^\{n-1\}u_n$ 或 $\sum(-1)^nu_n$（其中 $u_n>0$），负号全部由 $(-1)$ 的幂承担。首项为正用 $(-1)\^\{n-1\}$，首项为负用 $(-1)^n$，展开即 $u_1-u_2+u_3-u_4+\cdots$ 或 $-u_1+u_2-u_3+u_4-\cdots$。
- **关键概念**：`交错级数`、`$\sum(-1)^{n-1}u_n$`、`$u_n>0$`
- **相互关系**：只有 $(-1)^n$ 与 $u_n$ 相乘才是交错级数；若写成 $\frac{1}{\sqrt n}+(-1)^n\frac{1}{\sqrt n}$ 这种相加形式，整体不是交错级数，需拆项处理。
- **出处**：[石头 P100](https://www.bilibili.com/video/BV18CL26WEJ3?p=100)

### 莱布尼茨审敛法
- **要点**：交错级数若同时满足两个条件——(1) $u_n\geq u\_\{n+1\}$，即各项绝对值单调不增；(2) $\lim\_\{n\to\infty\}u_n=0$——则级数收敛。几何上表现为各项逐次逼近数轴、最终紧贴数轴，级数整体收敛到数轴附近。
- **关键概念**：`莱布尼茨审敛法`、`莱布尼茨定理`、`$u_n\geq u_{n+1}$`、`$\lim u_n=0$`
- **相互关系**：与收敛的必要条件 $\lim\_\{n\to\infty\}u_n=0$ 直接挂钩：若该极限不为零，由性质五的推论立判发散，所以第二个条件失效时可跳过第一个条件。
- **出处**：[石头 P100](https://www.bilibili.com/video/BV18CL26WEJ3?p=100)

### 判断 $u_n\geq u\_\{n+1\}$ 的三种思路
- **要点**：一是作商，$\frac{u_n}{u\_\{n+1\}}\geq1$；二是作差，$u_n-u\_\{n+1\}\geq0$；三是构造 $f(x)=u_x$，用单调递减说明 $u_n\geq u\_\{n+1\}$。也可借具体函数的单调性，如 $0&lt;\frac{1}{n+1}&lt;\frac1n\leq1$ 且 $\sin x$ 在 $(0,1]$ 上单调增，故 $\sin\frac1n>\sin\frac{1}{n+1}$。
- **关键概念**：`作商`、`作差`、`构造单调函数`、`单调性`
- **相互关系**：涉及根式差（如 $\sqrt{n+1}-\sqrt n$）时先分子有理化化为 $\frac{1}{\sqrt{n+1}+\sqrt n}$，分母越大值越小，大小关系一目了然；用单调性时注意 $u_x$ 应是 $\sin\frac1x$ 这类复合形式，不可与 $\sin x$ 递增混淆。
- **出处**：[石头 P100](https://www.bilibili.com/video/BV18CL26WEJ3?p=100)

### 交错级数的拆项与展开重组合
- **要点**：遇到「非纯交错」的级数可先拆项，如把 $\frac{1}{\sqrt n}+(-1)^n\frac{1}{\sqrt n}$ 拆成 P 级数（$p=\frac12&lt;1$，发散）与交错级数（收敛）之和，由「发散＋收敛＝发散」判定原级数发散。也可把级数逐项展开，把等于零的项划掉重新组合，如奇数项全为零时只剩偶数项构成的新级数 $\sum\frac{2}{\sqrt{2n}}$，再化为已知级数判断。
- **关键概念**：`拆项`、`发散＋收敛＝发散`、`展开重组合`
- **相互关系**：拆项依据的是收敛级数的性质，故必须先确认各部分敛散性；重组合的关键是重新找通项，不能沿用原通项。
- **出处**：[石头 P100](https://www.bilibili.com/video/BV18CL26WEJ3?p=100)

### 绝对收敛与条件收敛的定义
- **要点**：每项为任意实数的级数叫任意项级数，它包含正项级数、交错级数等全部常数项级数。若 $\sum\lvert u_n\rvert$ 收敛，称 $\sum u_n$ 绝对收敛；若 $\sum\lvert u_n\rvert$ 发散而 $\sum u_n$ 本身收敛，称 $\sum u_n$ 条件收敛。二者都是收敛，区别只在加绝对值后是否仍收敛。
- **关键概念**：`任意项级数`、`绝对收敛`、`条件收敛`、`$\sum\lvert u_n\rvert$`
- **相互关系**：加上绝对值后级数变成正项级数，比值、比较、根值三种审敛法随即全部可用，这是判断时必须先加绝对值的根本原因。
- **出处**：[石头 P101](https://www.bilibili.com/video/BV18CL26WEJ3?p=101)

### 绝收则本收、本散则决散
- **要点**：若 $\sum u_n$ 绝对收敛，则 $\sum u_n$ 本身一定收敛；若 $\sum u_n$ 本身发散，则 $\sum\lvert u_n\rvert$ 一定发散。口诀为「绝收则本收，本散则决散」。
- **关键概念**：`绝收则本收`、`本散则决散`
- **相互关系**：这两条可直接当定理使用，是「先判绝对值」这一解题顺序成立的理论依据。
- **出处**：[石头 P101](https://www.bilibili.com/video/BV18CL26WEJ3?p=101)

### 判断绝对收敛与条件收敛的标准步骤
- **要点**：先判断 $\sum\lvert u_n\rvert$：若收敛，则原级数收敛且绝对收敛，题目即做完。若发散，再判断原级数本身——多数是交错级数，用莱布尼茨定理；本身收敛则为条件收敛，本身发散则原级数发散。实测约六成题目一步即可判为绝对收敛。
- **关键概念**：`先判绝对值`、`再判本身`、`莱布尼茨定理`
- **相互关系**：顺序不能颠倒，先判本身会因可用方法少、步骤多而变难；含 $\cos n\alpha$ 这类有界因子时，加绝对值后用比较审敛法把因子换成 $1$，再对化简后的级数用比值审敛法。
- **出处**：[石头 P101](https://www.bilibili.com/video/BV18CL26WEJ3?p=101)

### 函数项级数、收敛点、收敛域与和函数
- **要点**：各项都由含自变量 $x$ 的函数构成的级数叫函数项级数。把 $x$ 取定值 $x_0$ 代入后它变成常数项级数：收敛则称 $x_0$ 为收敛点，发散则称发散点；全体收敛点构成收敛域，全体发散点构成发散域。在收敛域上每个收敛点对应一个和 $S(x)$，由此定义的函数叫和函数，即 $S(x)=\lim\_\{n\to\infty\}S_n(x)$。
- **关键概念**：`函数项级数`、`收敛点`、`收敛域`、`发散域`、`和函数 $S(x)$`
- **相互关系**：和函数的定义域就是级数的收敛域，因此求收敛域是求和函数、展开幂级数的前提；这与一元函数「一个 $x$ 对应唯一一个 $y$」的结构相同。
- **出处**：[石头 P102](https://www.bilibili.com/video/BV18CL26WEJ3?p=102)

### 幂级数的标准形式与中心
- **要点**：幂级数的一般形式为 $\sum\_\{n=0\}\^\{\infty\}a_n(x-x_0)^n$，其中 $x=x_0$ 称为中心；当 $x_0=0$ 时简化为 $\sum\_\{n=0\}\^\{\infty\}a_nx^n$，即以零为中心。求收敛半径与收敛域时，真正要抓的是 $x$ 的幂前面的常系数 $a_n$。
- **关键概念**：`幂级数`、`$\sum a_n(x-x_0)^n$`、`中心 $x_0$`、`常系数 $a_n$`
- **相互关系**：分清 $a_n$ 与整个通项 $u_n$ 是解题第一步，$a_n$ 只含 $n$、不含 $x$；带 $(x-x_0)$ 的幂级数相当于把标准幂级数平移了中心。
- **出处**：[石头 P102](https://www.bilibili.com/video/BV18CL26WEJ3?p=102)

### 阿贝尔定理与收敛半径、收敛区间、收敛域
- **要点**：阿贝尔定理指出：幂级数在 $x=x_0$ 处收敛，则在 $\lvert x\rvert&lt;\lvert x_0\rvert$ 内处处收敛；在 $x=x_0$ 处发散，则在 $\lvert x\rvert>\lvert x_0\rvert$ 外处处发散。由此存在非负数 $R$，使 $\lvert x\rvert&lt;R$ 内收敛、$\lvert x\rvert>R$ 外发散：$R$ 叫收敛半径，$(-R,R)$ 叫收敛区间，再讨论两个端点后得到的区间叫收敛域。
- **关键概念**：`阿贝尔定理`、`收敛半径 $R$`、`收敛区间`、`收敛域`
- **相互关系**：三者顺序不可颠倒——先求 $R$，再写收敛区间，最后代端点定收敛域；收敛区间永远是以 $R$ 为半长的开区间，收敛域才有可能是半开半闭或闭区间。
- **出处**：[石头 P102](https://www.bilibili.com/video/BV18CL26WEJ3?p=102)

### 收敛半径的求法与收敛域的端点讨论
- **要点**：按比值判别法只比系数，取 $\rho=\lim\_\{n\to\infty\}\left\lvert\frac{a\_\{n+1\}}{a_n}\right\rvert$（$x$ 的幂会自行约掉），则 $R=\frac1\rho$。若级数缺项，即以 $x\^\{2n\}$、$x\^\{2n\pm1\}$ 开头，则 $R=\sqrt{\frac1\rho}$；以 $3n$ 次方开头就开三次方，以此类推。求收敛域要把 $x=\pm R$ 代入化为常数项级数判断：端点收敛取闭区间、发散取开区间，共有四种情形。若 $R=0$ 或 $R=+\infty$，收敛区间与收敛域相同（分别为 $\{0\}$ 与 $(-\infty,+\infty)$），此时不必讨论端点。
- **关键概念**：`$\rho=\lim\left\lvert\frac{a_{n+1}}{a_n}\right\rvert$`、`$R=\frac1\rho$`、`缺项开根号`、`端点讨论`
- **相互关系**：$\rho=0$ 对应 $R=+\infty$，$\rho=+\infty$ 对应 $R=0$；遇到 $x-x_0$ 型可令 $x-x_0=t$，半径不变而区间要平移，如 $x-3$ 的收敛区间 $(-1,1)$ 平移后为 $(2,4)$。
- **出处**：[石头 P102](https://www.bilibili.com/video/BV18CL26WEJ3?p=102)、[P103](https://www.bilibili.com/video/BV18CL26WEJ3?p=103)

### 平移型与缺项型幂级数的收敛域实例
- **要点**：对 $\sum a_n(x-x_0)^n$ 先令 $x-x_0=t$ 化为标准幂级数，求出 $t$ 的收敛半径与区间后再回代平移得 $x$ 的范围；若同时缺项，半径还要开根号。端点代回原级数时要注意 $(-1)\^\{2n\}=1$，此时交错级数会退化为同号级数。
- **关键概念**：`换元 $t=x-x_0$`、`区间平移`、`$(-1)^{2n}=1$`
- **相互关系**：以 $2n$ 开头的 $(-1)\^\{2n-1\}$ 不是交错级数标志，由调和级数演变来的这种级数通常发散；以 $n$ 开头的 $(-1)\^\{n-1\}$ 才是交错级数标志，由调和级数演变来的交错级数收敛。
- **出处**：[石头 P103](https://www.bilibili.com/video/BV18CL26WEJ3?p=103)

### 幂级数的加减运算
- **要点**：两个幂级数相加减，其收敛半径取二者中较小的一个，记为 $\min\{R_1,R_2\}$。例如收敛半径分别为 $3$ 和 $4$ 的两个幂级数相加，和的收敛半径为 $3$。
- **关键概念**：`幂级数的加减`、`$\min\{R_1,R_2\}$`
- **相互关系**：只有在两个级数都收敛的点上才能逐项加减，所以半径只能取小；这与常数项级数中「发散部分不能拆」的性质同源。
- **出处**：[石头 P104](https://www.bilibili.com/video/BV18CL26WEJ3?p=104)

### 等比幂级数与消系数思想
- **要点**：$\sum\_\{n=0\}\^\{\infty\}x^n$ 叫等比幂级数，$\lvert x\rvert&lt;1$ 时收敛于 $\frac{1}{1-x}$，即「一减公比分之首项」。对一般幂级数 $\sum a_nx^n$ 求和的思路是消系数：设法去掉 $a_n$，把它化成等比幂级数再套公式。
- **关键概念**：`等比幂级数`、`$\sum_{n=0}^{\infty}x^n=\frac{1}{1-x}$`、`消系数`、`一减公比分之首项`
- **相互关系**：与常数项等比级数求和公式形式一致，可视为把公比换成任意「框框」的推广；$a_n$ 只与 $n$ 有关，求导、积分时一律当常数处理。
- **出处**：[石头 P104](https://www.bilibili.com/video/BV18CL26WEJ3?p=104)

### 逐项求导与逐项积分
- **要点**：和函数在收敛区间内连续、可导、可积，可逐项求导与逐项积分，且收敛半径不变。逐项积分取固定下限 $0$：$\int_0^x\sum a_nt^n\,dt=\sum\frac{a_n}{n+1}x\^\{n+1\}$；逐项求导为 $\left(\sum a_nx^n\right)'=\sum na_nx\^\{n-1\}$。消系数的口诀是「除先导、乘先积」——$a_n$ 含 $\frac1n$ 时先求导，$a_n$ 含 $n$ 时先积分。
- **关键概念**：`逐项求导`、`逐项积分`、`收敛半径不变`、`除先导乘先积`
- **相互关系**：先导的要后积、先积的要后导，才能还原出原级数的和函数；积分上下限固定为 $0$ 到 $x$，为与上限区分可把积分变量写成 $t$。
- **出处**：[石头 P104](https://www.bilibili.com/video/BV18CL26WEJ3?p=104)

### 求和函数的标准步骤
- **要点**：三步走——第一步求收敛域（没有收敛域和函数无意义）；第二步令 $S(x)=\sum a_nx^n$，按「除先导、乘先积」消去系数并套用等比幂级数公式；第三步作相应的积分或求导还原。典型结果：$\sum\_\{n=1\}\^\{\infty\}nx\^\{n-1\}=\frac{1}{(1-x)^2}$（$\lvert x\rvert&lt;1$），$\sum\_\{n=1\}\^\{\infty\}\frac{x^n}{n}=-\ln(1-x)$（$-1\leq x&lt;1$）。
- **关键概念**：`先求收敛域`、`消系数`、`先积后导`、`先导后积`
- **相互关系**：还原时用到的商的求导法则与凑微分是前几章内容，容易在此卡壳；最终答案必须附上收敛域，否则扣分。
- **出处**：[石头 P104](https://www.bilibili.com/video/BV18CL26WEJ3?p=104)

### 泰勒级数与麦克劳林级数
- **要点**：把函数 $f(x)$ 表示成 $\sum\_\{n=0\}\^\{\infty\}a_n(x-x_0)^n$ 的过程叫函数展开成幂级数。以 $x_0$ 为中心展开时，系数由 $a_n=\frac{f\^\{(n)\}(x_0)}{n!}$ 给出，所得级数叫泰勒级数；当 $x_0=0$ 时叫麦克劳林级数。系数公式由逐项求导后取 $x=x_0$ 推出，了解即可、不必死记。
- **关键概念**：`函数展开成幂级数`、`泰勒级数`、`麦克劳林级数`、`$a_n=\frac{f^{(n)}(x_0)}{n!}$`
- **相互关系**：与求和函数互为逆过程——求和函数是由级数求函数，函数展开是由函数求级数。
- **出处**：[石头 P105](https://www.bilibili.com/video/BV18CL26WEJ3?p=105)

### 常用函数的幂级数展开式
- **要点**：必记五个展开式：$e^x=\sum\_\{n=0\}\^\{\infty\}\frac{x^n}{n!}$（$x\in R$）；$\frac{1}{1-x}=\sum\_\{n=0\}\^\{\infty\}x^n$（$\lvert x\rvert&lt;1$）；$\ln(1+x)=\sum\_\{n=1\}\^\{\infty\}(-1)\^\{n-1\}\frac{x^n}{n}$（$-1&lt;x\leq1$）；$\sin x=\sum\_\{n=0\}\^\{\infty\}(-1)^n\frac{x\^\{2n+1\}}{(2n+1)!}$（$x\in R$）；$\cos x=\sum\_\{n=0\}\^\{\infty\}(-1)^n\frac{x\^\{2n\}}{(2n)!}$（$x\in R$）。不记住这些公式就无法做题。
- **关键概念**：`$e^x$`、`$\frac{1}{1-x}$`、`$\ln(1+x)$`、`$\sin x$`、`$\cos x$`
- **相互关系**：$\sin x$、$\cos x$ 的展开式只含奇次项或偶次项，正是它们为奇函数、偶函数的体现；$\frac{1}{1-x}$ 与 $\ln(1+x)$ 的展开式可由等比幂级数逐项积分互推。
- **出处**：[石头 P105](https://www.bilibili.com/video/BV18CL26WEJ3?p=105)

### 展开式的推广与凑框框
- **要点**：把公式中的 $x$ 换成任意整体「框框」仍成立，如 $\frac{1}{1-\square}=\sum\_\{n=0\}\^\{\infty\}\square^n$、$\ln(1+\square)=\sum\_\{n=1\}\^\{\infty\}(-1)\^\{n-1\}\frac{\square^n}{n}$，条件为 $\lvert\square\rvert&lt;1$。展开成 $x$ 的幂级数要把函数凑成 $1-\square$ 的形式，如 $\frac{1}{1+2x}=\sum\_\{n=0\}\^\{\infty\}(-1)^n2^nx^n$（$\lvert x\rvert&lt;\frac12$）；展开成 $x-x_0$ 的幂级数时框框取 $x-x_0$，如 $\frac1x=\sum\_\{n=0\}\^\{\infty\}(-1)^n(x-1)^n$（$0&lt;x&lt;2$）。
- **关键概念**：`框框`、`$\frac{1}{1-\square}$`、`凑 $x-x_0$`、`$\lvert\square\rvert<1$`
- **相互关系**：收敛条件约束的是框框而不是 $x$，因此最后必须解出 $x$ 的范围；凑形时提取负号、补项配平，注意除以负数要改变不等号方向。
- **出处**：[石头 P105](https://www.bilibili.com/video/BV18CL26WEJ3?p=105)

### 收敛半径与收敛区间的综合计算
- **要点**：含阶乘的幂级数先写出 $a_n$ 与 $a\_\{n+1\}$ 再作比，$a\_\{n+1\}$ 中的多项式务必加括号（如 $2(n+1)$ 要写全）以防约分出错；化简后常出现 $\left(\frac{n}{n+1}\right)^n$ 型，用第二重要极限得 $\rho=\frac1e$，故 $R=e$。缺项型（如含 $\frac{(2n)!}{(n!)^2}$、$x\^\{2n\}$ 的级数）最后要记得开根号，例如 $\rho=4$ 时 $R=\frac12$。
- **关键概念**：`$a_{n+1}$ 加括号`、`第二重要极限`、`缺项开根号`、`$R=\frac1\rho$`
- **相互关系**：常见答案为 $\frac12$、$\frac13$、$2$、$e$ 等，与系数比值、是否开根号一一对应；题目只要求收敛域时仍须先求收敛半径与收敛区间，三者顺序不可跳过。
- **出处**：[石头 P106](https://www.bilibili.com/video/BV18CL26WEJ3?p=106)

### 级数概念体系梳理
- **要点**：判别敛散性的定义是前 $n$ 项和 $S_n$ 取极限；级数收敛的必要条件是 $\lim\_\{n\to\infty\}u_n=0$，反之不成立；正项级数收敛的充要条件是前 $n$ 项和序列有界。等比级数 $\lvert q\rvert&lt;1$ 收敛、$\lvert q\rvert\geq1$ 发散；P 级数 $p>1$ 收敛、$p\leq1$ 发散。正项级数三种审敛法为比较（含极限形式，大收小收、小发大发）、比值、根值；比值或根值判别中 $\rho>1$ 时级数必发散。
- **关键概念**：`前 $n$ 项和 $S_n$`、`必要条件 $\lim u_n=0$`、`正项级数有界充要条件`、`三种审敛法`
- **相互关系**：这些结论是整章判断的总纲，做题时先识别级数类型再选方法；绝对收敛与条件收敛都要求本身收敛，差别只在加绝对值后是否收敛。
- **出处**：[石头 P106](https://www.bilibili.com/video/BV18CL26WEJ3?p=106)


## 十一、线性代数


### 线性代数的学科特点与章节构成
- **要点**：知识点多而杂、单个简单、关联性强；主要学行列式、矩阵、方程组（向量的运算多归入方程组）。
- **关键概念**：`行列式`
- **出处**：[米哥 P141](https://www.bilibili.com/video/BV1swAWerEzS?p=141)、[P142](https://www.bilibili.com/video/BV1swAWerEzS?p=142)

### 行列式的定义与记号
- **要点**：方程组系数外加两条竖线即为行列式，表示一个数；n 阶记 D_n，元素 a\_\{ij\} 中 i 行 j 列；行数＝列数。
- **关键概念**：`a_{ij}`
- **出处**：[米哥 P143](https://www.bilibili.com/video/BV1swAWerEzS?p=143)

### 二阶与三阶行列式：对角线法则
- **要点**：二阶＝主对角乘积减副对角乘积；三阶把前两列抄右侧，三条主对角串之和减三条副对角串之和；只适用二阶、三阶。
- **关键概念**：`对角线法则`
- **出处**：[米哥 P144](https://www.bilibili.com/video/BV1swAWerEzS?p=144)

### 三角行列式
- **要点**：上三角＝主对角线元素之积；下三角＝(−1)\^\{n(n−1)/2\} × 副对角线元素之积。
- **关键概念**：`副对角线`
- **出处**：[米哥 P144](https://www.bilibili.com/video/BV1swAWerEzS?p=144)

### 行列式的三个基本性质
- **要点**：①某行（列）公因子可提出；②交换两行（列）变号；③某行的 k 倍加到另一行值不变。
- **关键概念**：`倍加不变`
- **出处**：[米哥 P145](https://www.bilibili.com/video/BV1swAWerEzS?p=145)

### 化为三角形行列式
- **要点**：用性质③把主对角线下方消成零；尽量让第一行（列）首元为 1，必要时先交换行。
- **关键概念**：`首元化一`
- **出处**：[米哥 P145](https://www.bilibili.com/video/BV1swAWerEzS?p=145)

### 余子式、代数余子式与拉普拉斯展开
- **要点**：M\_\{ij\} 为划去第 i 行第 j 列的行列式；A\_\{ij\}=(−1)\^\{i+j\}M\_\{ij\}；行列式＝任一行（列）各元素乘其代数余子式之和。
- **关键概念**：`拉普拉斯展开`
- **出处**：[米哥 P146](https://www.bilibili.com/video/BV1swAWerEzS?p=146)

### 爪型行列式与行（列）和相等行列式
- **要点**：爪型用某列（行）倍数加到另一列（行）把「爪」消零；行（列）和相等先把各列（行）加到第一列（行），提公因子构全 1 列再化三角。
- **关键概念**：`爪型行列式`
- **出处**：[米哥 P147](https://www.bilibili.com/video/BV1swAWerEzS?p=147)

### 矩阵的概念与特殊矩阵
- **要点**：矩阵是信息表（用括号），本身算不出数值，行数列数任意，记 A\_\{m×n\}；特殊矩阵有行/列矩阵、零矩阵、单位矩阵 E（主对角线为 1）。转置 A^T 是把第 i 行写成第 i 列。
- **关键概念**：`单位矩阵 E`、`A^T`
- **出处**：[米哥 P148](https://www.bilibili.com/video/BV1swAWerEzS?p=148)

### 矩阵的加减法与数乘
- **要点**：加减须同型、对应元素相加减；kA 把 k 乘到每个元素；矩阵没有除法。
- **关键概念**：`同型矩阵`
- **出处**：[米哥 P149](https://www.bilibili.com/video/BV1swAWerEzS?p=149)

### 矩阵的乘法
- **要点**：A 的列数＝B 的行数才能乘，结果取 A 的行数、B 的列数；元素为左行 × 右列的对应乘积之和；一般 AB≠BA。
- **关键概念**：`不可交换`
- **出处**：[米哥 P149](https://www.bilibili.com/video/BV1swAWerEzS?p=149)

### 矩阵运算的注意点与方阵行列式公式
- **要点**：AB=AC 不能约去 A，AB=O 推不出 A=O 或 B=O；|A^T|=|A|、|kA|=k^n|A|、|AB|=|A||B|、|A+B|≠|A|+|B|。
- **关键概念**：`|AB|=|A||B|`
- **出处**：[米哥 P150](https://www.bilibili.com/video/BV1swAWerEzS?p=150)

### 初等行变换与两种标准形
- **要点**：三条：换行不变号、某行乘非零常数、某行 k 倍加到另一行；行阶梯形台阶首元非零、下方全零，行最简形首元为 1 且所在列其余为零。
- **关键概念**：`初等行变换`
- **出处**：[米哥 P151](https://www.bilibili.com/video/BV1swAWerEzS?p=151)

### 矩阵的秩
- **要点**：化为行阶梯形后阶梯层数即 r(A)；求秩不必化到最简形。
- **关键概念**：`秩 r(A)`
- **出处**：[米哥 P151](https://www.bilibili.com/video/BV1swAWerEzS?p=151)

### 逆矩阵的概念与性质
- **要点**：AB=E 则 A\^\{−1\}=B；(A\^\{−1\})\^\{−1\}=A、(kA)\^\{−1\}=(1/k)A\^\{−1\}、(AB)\^\{−1\}=B\^\{−1\}A\^\{−1\}、(AB)^T=B^T A^T、|A\^\{−1\}|=1/|A|。
- **关键概念**：`反序律`
- **出处**：[米哥 P152](https://www.bilibili.com/video/BV1swAWerEzS?p=152)

### 伴随矩阵
- **要点**：元素换成代数余子式再转置得 A*；A\^\{−1\}=A*/|A|，故 |A|≠0 ⟺ 可逆；|A*|=|A|\^\{n−1\}。
- **关键概念**：`伴随矩阵 A*`
- **出处**：[米哥 P152](https://www.bilibili.com/video/BV1swAWerEzS?p=152)

### 求逆矩阵：公式法与初等行变换法
- **要点**：公式法仅二阶：主对角线互换、副对角线变号再除以 |A|=ad−bc；任意阶：(A|E) 经行变换化为 (E|B) 则 A\^\{−1\}=B。
- **关键概念**：`(A|E)→(E|B)`
- **出处**：[米哥 P153](https://www.bilibili.com/video/BV1swAWerEzS?p=153)

### 抽象型矩阵求逆
- **要点**：核心是「凑 □·△=E」，用十字相乘法、完全平方、恒等变形，注意 E^n=E；AX=B 时 X=A\^\{−1\}B。
- **关键概念**：`十字相乘法`
- **出处**：[米哥 P153](https://www.bilibili.com/video/BV1swAWerEzS?p=153)、[P154](https://www.bilibili.com/video/BV1swAWerEzS?p=154)

### 向量与向量组
- **要点**：行向量写一横排、列向量写一竖列；若干向量构成向量组，写成矩阵形式即矩阵。
- **关键概念**：`向量组`
- **出处**：[米哥 P155](https://www.bilibili.com/video/BV1swAWerEzS?p=155)

### 线性组合与线性表出
- **要点**：k₁α₁+…+k_nα_n 为线性组合；β 能这样写出则可由该组线性表出；表出关系是相互的。
- **关键概念**：`线性表出`
- **出处**：[米哥 P155](https://www.bilibili.com/video/BV1swAWerEzS?p=155)

### 线性相关与线性无关
- **要点**：存在不全为零的 k_i 使 Σk_iα_i=0 则线性相关，只有全零才成立则线性无关；等价说法：某向量可由其余表出即线性相关。
- **关键概念**：`线性相关`
- **出处**：[米哥 P155](https://www.bilibili.com/video/BV1swAWerEzS?p=155)

### 极大线性无关组
- **要点**：化行阶梯形后每台阶取一个向量即极大线性无关组；能表出其余向量，个数＝向量组的秩；求表示用行最简形。
- **关键概念**：`极大线性无关组`
- **出处**：[米哥 P155](https://www.bilibili.com/video/BV1swAWerEzS?p=155)

### 齐次方程组与基础解系
- **要点**：AX=O 一定有解；r(A)=n 只有零解，r(A)&lt;n 有无穷多解，为基础解系的线性组合，个数 n−r(A)。
- **关键概念**：`n−r(A)`
- **出处**：[米哥 P156](https://www.bilibili.com/video/BV1swAWerEzS?p=156)

### 非齐次方程组解的判定与结构
- **要点**：r(A)≠r(A,b) 无解，=n 唯一解，&lt;n 无穷多解；解＝齐次通解＋非齐次特解；步骤：增广矩阵→行最简形→还原方程→自由未知量设 k₁,k₂→写通解。
- **关键概念**：`增广矩阵`
- **出处**：[米哥 P157](https://www.bilibili.com/video/BV1swAWerEzS?p=157)

### 含参数方程组的讨论
- **要点**：方阵先算 |A|；|A|≠0 唯一解，|A|=0 代回用秩判断：r(A)≠r(A,b) 无解，r(A)=r(A,b)&lt;n 无穷多解。
- **关键概念**：`分类讨论`
- **出处**：[米哥 P158](https://www.bilibili.com/video/BV1swAWerEzS?p=158)


## 十二、证明专项


### 证明专项的定理分布
- **要点**：按考查频率，单调性、零点定理、罗尔定理、拉格朗日中值定理为高频（四星），最值定理与介值定理、积分中值定理、柯西中值定理、泰勒公式、积分等式证明为低频。约 90% 的证明题集中在前四类。
- **关键概念**：`罗尔定理`、`拉格朗日中值定理`、`拉氏定理`
- **相互关系**：罗尔定理的辅助函数构造要用到积分学知识，故统一放在最后一章；题干出现「一撇」（导数）就考虑中值定理，不出现导数则用最值、介值或零点定理。
- **出处**：[陈哥 P128](https://www.bilibili.com/video/BV1husGzwEtZ?p=128)、[P136](https://www.bilibili.com/video/BV1husGzwEtZ?p=136)

### 单调性证不等式的基本步骤
- **要点**：证明 f(x)>g(x) 类不等式时作差构造辅助函数 F(x)=f(x)−g(x)，求导判断 F′(x) 符号得单调性，再取区间端点（或极限点）求最小值/最大值，由最值符号推出不等式。含分式的先两边乘去分母（须确认分母为正）化为整式。步骤：①构造函数并确定讨论范围；②说明连续；③求导证单调；④求最值（一般在端点取得）。
- **关键概念**：`辅助函数`、`单调性`、`最值`、`作差法`、`构造函数`
- **相互关系**：讨论范围不一定等于定义域——若端点处函数有定义应取闭区间以便直接代入；若一阶导先增后减，需借助「极值」内容求最值；是罗尔定理辅助函数构造的基础。
- **出处**：[陈哥 P128](https://www.bilibili.com/video/BV1husGzwEtZ?p=128)；[ok姐 P40](https://www.bilibili.com/video/BV1vm421s7mv?p=40)

### 二次求导法
- **要点**：一阶导符号无法直接判断时再求二阶导：由 F″(x)>0 推 F′(x) 单调递增，取端点得一阶导最小值；若该最小值非负则 F′(x)≥0，原函数单调递增，再由原函数最小值推出结论。整条链是「二阶导 → 一阶导单调 → 一阶导符号 → 原函数单调 → 原函数最值」。
- **关键概念**：`二阶导数`、`一阶导单调性`、`最值链`
- **出处**：[陈哥 P128](https://www.bilibili.com/video/BV1husGzwEtZ?p=128)；[ok姐 P40](https://www.bilibili.com/video/BV1vm421s7mv?p=40)

### 最值定理与介值定理结合的证明题
- **要点**：题干给出若干函数值之和的等式（如 f(1)+f(2)+f(3)=3f(4)）时，先由可导推连续、用最值定理得每个函数值都在 [m,M] 内；把若干不等式相加再除以个数，得平均值仍介于 m 与 M 之间，把它当作 μ 用介值定理，得存在 ξ 使 f(ξ) 等于该平均值，代入题干条件化简即得结论。
- **关键概念**：`可导必连续`、`不等式相加`、`平均值作为 μ`
- **出处**：[陈哥 P129](https://www.bilibili.com/video/BV1husGzwEtZ?p=129)

### 零点定理题型一：方程根的存在性
- **要点**：把方程移项归到一边构造 F(x)，将「方程有根」转化为「函数有零点」，再验证零点定理的两个条件。两曲线交点问题同样处理：交点 ⟺ 联立方程 f(x)=g(x) 有根 ⟺ F(x)=f(x)−g(x) 有零点。
- **关键概念**：`方程与函数互化`、`零点问题`、`交点问题`
- **出处**：[陈哥 P130](https://www.bilibili.com/video/BV1husGzwEtZ?p=130)

### 零点定理题型二：有且仅有一个根
- **要点**：分两步——用零点定理证存在性，用单调性证唯一性。求导判断 F′(x) 在区间上恒正或恒负，说明 F(x) 单调，单调函数至多一个零点，结合存在性即得「有且仅有一个」。
- **关键概念**：`存在性`、`唯一性`、`单调性`
- **出处**：[陈哥 P130](https://www.bilibili.com/video/BV1husGzwEtZ?p=130)；[ok姐 P39](https://www.bilibili.com/video/BV1vm421s7mv?p=39)

### 证明方程根的个数（完整步骤）
- **要点**：把方程根的个数问题转化为函数零点问题（构造 G(x)=方程左端）。步骤：①构造函数；②说明它在区间上连续；③证明端点值异号（端点无定义时改为两端点处极限异号）；④求导证明单调，即可得「有且仅有一个零点」。升本中遇到的几乎都是只有一个根。
- **关键概念**：`零点定理`、`构造函数`、`端点异号`、`单调`
- **出处**：[ok姐 P39](https://www.bilibili.com/video/BV1vm421s7mv?p=39)

### 零点定理题型三：等式中含 f(ξ)
- **要点**：把待证等式中的 ξ 全部换成 x，右边移到左边构造 F(x)，验证 F 在闭区间连续，再算两端点值（常用题干给的 f(0)、f(1) 等），若异号则由零点定理得存在 ξ 使 F(ξ)=0，回代即得待证等式。
- **关键概念**：`ξ 换成 x`、`存在符号 ∃`
- **相互关系**：此类题常作为大题第一问，第二问多用罗尔定理。
- **出处**：[陈哥 P130](https://www.bilibili.com/video/BV1husGzwEtZ?p=130)

### 辅助函数的构造是罗尔定理的核心
- **要点**：题目不会直接给出 f(a)=f(b)，故不能对题干中的 f(x) 直接用罗尔定理，必须先构造含 f(x) 的辅助函数 F(x) 使两端点值相等。四种题型本质上是四种构造辅助函数的方法。
- **关键概念**：`辅助函数 F(x)`、`端点值相等`
- **相互关系**：是罗尔定理所有题型的统一点。
- **出处**：[陈哥 P131](https://www.bilibili.com/video/BV1husGzwEtZ?p=131)

### 罗尔定理题型一：根的存在性
- **要点**：构造辅助函数的方法是对移项后的方程直接积分（移项 → 积分两步）。求出 F(x) 后验证 F(a)=F(b)，由罗尔定理得 F′(ξ)=0，而 F′(x) 恰为原方程左边的函数，即证得方程在区间上至少有一个根。积分时不必加常数 C。
- **关键概念**：`移项`、`直接积分`、`不加 C`
- **相互关系**：特征是被证函数恰为某函数的导数。
- **出处**：[陈哥 P131](https://www.bilibili.com/video/BV1husGzwEtZ?p=131)

### 罗尔定理题型二：含 f′(ξ) 与 ξ 的等式
- **要点**：被证等式中同时含 f′(ξ) 与 ξ（如 f′(ξ)+g(ξ)=0 或 f′(ξ)f(ξ)+g(ξ)=0）时，三步构造辅助函数：ξ 换成 x → 全部移到等号左边 → 直接积分。积分时 f(x)f′(x) 用凑微分写成 f²(x)/2；等式含分式时先交叉相乘去分母化为整式再积分，之后照常验证罗尔定理三条件。
- **关键概念**：`ξ 换成 x`、`凑微分`、`交叉相乘去分母`
- **相互关系**：易混点——若 f′(ξ) 与 f(ξ) 是相加减关系则不能直接积分，属第三种题型；只有相乘关系才能用此法。
- **出处**：[陈哥 P131](https://www.bilibili.com/video/BV1husGzwEtZ?p=131)

### 罗尔定理题型三：标准形式与辅助函数公式
- **要点**：要证等式中同时含 f′(ξ) 与 f(ξ)（形如 f′(ξ)+g(ξ)f(ξ)=0）时，不能再用积分法找辅助函数。先把 ξ 换成 x 化为标准形式（f′(x) 前的系数必须化为 1，不为 1 时在等式两边同除该系数；系数为 g(x) 时除以它后变成 1/g(x)），再取辅助函数 F(x)=e\^\{∫g(x)dx\}f(x)：g(x) 积分后写在 e 的指数上，f(x) 原样照写。
- **关键概念**：`标准形式`、`辅助函数`、`e^{∫g(x)dx}f(x)`、`系数为一`、`两边同除`
- **相互关系**：与「f′(x)±f(x)=0 用积分法」的题型相区别；绝大部分此类题都可化为标准形式；系数归一化是写辅助函数前的必做步骤，题干常故意给不唯一的系数。
- **出处**：[陈哥 P132](https://www.bilibili.com/video/BV1husGzwEtZ?p=132)

### 罗尔定理题型三：辅助函数的来源（一阶线性微分方程）
- **要点**：f′(x)+g(x)f(x)=0 是一阶齐次线性微分方程，用公式 y=e\^\{−∫P dx\}(∫Q e\^\{∫P dx\}dx+C)，取 P=g、Q=0 得 f(x)=Ce\^\{−∫g dx\}，两边同乘 e\^\{∫g dx\} 即 C=e\^\{∫g dx\}f(x)；C 求导为零，正是罗尔定理所需的 F′(ξ)=0。辅助函数本质就是微分方程通解中的常数 C。
- **关键概念**：`一阶线性微分方程`、`齐次`、`常数 C`
- **出处**：[陈哥 P132](https://www.bilibili.com/video/BV1husGzwEtZ?p=132)

### 罗尔定理题型三：进阶形式一（复合函数型）
- **要点**：标准形式中的 f(x) 不一定是单纯的 f(x)，可能是 f(x)+x、f′(x)−1 等复合整体。把该整体看作一个方框，它与自身的导数仍构成导数关系，公式照用；关键是把待证等式配成「复合整体的导数 + g(x)×该整体 = 0」。
- **关键概念**：`复合函数`、`导数关系`、`整体代换`
- **相互关系**：由基础形式推广而来，是考查重点；配形无固定技巧，只能多练题摸索。
- **出处**：[陈哥 P132](https://www.bilibili.com/video/BV1husGzwEtZ?p=132)

### 罗尔定理题型三：进阶形式二（非齐次型）
- **要点**：形如 f′(ξ)+g(ξ)f(ξ)=Q(ξ)（右端非零）时，辅助函数为 e\^\{∫g dx\}[f(x)−∫Q e\^\{∫g dx\}dx]；Q=0 时退化为齐次型，说明形式二是形式一的一般情形。
- **关键概念**：`非齐次`、`Q(x)`、`特解`
- **相互关系**：考到的概率较小，仅个别省份出现过。
- **出处**：[陈哥 P132](https://www.bilibili.com/video/BV1husGzwEtZ?p=132)

### 罗尔定理题型三的解题套路
- **要点**：流程固定为「化标准形式 → 定出 g(x) → 写出 F(x)」，找到 F 后其余全是套话：说明 F 在闭区间连续、开区间可导，算出两端点函数值相等，由罗尔定理得 F′(ξ)=0，再求导验证它等价于待证等式。
- **关键概念**：`罗尔定理三条件`、`端点函数值相等`、`F′(ξ)=0`
- **相互关系**：题干常故意给 f(a)=f(b)=0、f(1)=2f(0) 之类的条件，正是为凑出第三个条件。
- **出处**：[陈哥 P132](https://www.bilibili.com/video/BV1husGzwEtZ?p=132)

### 罗尔定理题型四：反证法的适用特征与思路
- **要点**：题干出现「至多」「不可能」「最多」这类描述时用反证法：先否定结论（把「至多一个零点」否定为「有两个零点」）并当作假设条件，再用罗尔定理推出与题干矛盾的结论，从而说明假设错误、原结论成立。
- **关键概念**：`反证法`、`否定结论`、`与题干矛盾`
- **相互关系**：与「至少存在一点」的题型互为反面；反证法不限于罗尔定理。
- **出处**：[陈哥 P133](https://www.bilibili.com/video/BV1husGzwEtZ?p=133)

### 罗尔定理题型四：至多一个零点型
- **要点**：假设 f(x) 在 [a,b] 上有两个零点 x₀,x₁，作辅助函数 F(x)=e\^\{−g(x)\}f(x)，由 F(x₀)=F(x₁)=0 用罗尔定理得某点导数为零，整理后所得等式与题干「该式恒不为零」矛盾。
- **关键概念**：`两个零点`、`e^{−g(x)}f(x)`、`矛盾`
- **出处**：[陈哥 P133](https://www.bilibili.com/video/BV1husGzwEtZ?p=133)

### 罗尔定理题型四：不可能有三个根 / 至多两个根型
- **要点**：假设方程有三个根 x₀&lt;x₁&lt;x₂，在 [x₀,x₁]、[x₁,x₂] 上各用一次罗尔定理得 f′(ξ₁)=f′(ξ₂)=0；再把 f′(x) 看作函数，在 [ξ₁,ξ₂] 上再用一次罗尔定理得 f″(ξ)=0，与题干（如 f″(x)&lt;0）矛盾。
- **关键概念**：`三个根`、`连续两次罗尔定理`、`f″(ξ)=0`
- **相互关系**：这一「多次使用罗尔定理」的思想在拉格朗日中值定理题型二中再次出现。
- **出处**：[陈哥 P133](https://www.bilibili.com/video/BV1husGzwEtZ?p=133)

### 拉格朗日中值定理题型一：识别特征与配形
- **要点**：出现「两个函数相减 ÷ 对应自变量相减」的形式（如 (sin b−sin a)/(b−a)、(ln b−ln a)/(b−a)、(e^b−e^a)/(b−a)）就考虑用拉格朗日中值定理。题目不会直接给出该形式，需从中间的函数入手，用对数运算（ln(b/a)=ln b−ln a）或通分把它配出来。约六成的拉格朗日中值定理题属此类。
- **关键概念**：`函数相减`、`自变量相减`、`配形`
- **出处**：[陈哥 P134](https://www.bilibili.com/video/BV1husGzwEtZ?p=134)

### 拉格朗日中值定理题型一：解题套路（三步）
- **要点**：①把不等式配成 [f(b)−f(a)]/(b−a) 形式（常在两边同除以正数 b−a，不等号不变向）；②令 f(t) 为相应函数（ln t、arctan t、t^n 等），说明其连续可导后由拉格朗日中值定理得 f′(ξ)=[f(b)−f(a)]/(b−a)；③由 ξ 落在区间内定出 f′(ξ) 的上下界，代回原式即得。三步中只有第二步的求导代换不是套话。
- **关键概念**：`套话部分`、`代入具体函数求导`、`ξ 的范围`
- **出处**：[陈哥 P134](https://www.bilibili.com/video/BV1husGzwEtZ?p=134)

### 拉格朗日中值定理题型一：常见配形变式
- **要点**：①对数型如 ln(1+x)−ln x 可写成 [ln(1+x)−ln x]/[(1+x)−x]，令 f(t)=ln t、t∈[x,x+1]，此时 x 视为参数、t 才是自变量；②单独的 ln(1+x) 可配上 ln 1=0 凑成两对数相减；③幂函数型把 b−a 除到中间得 (b^n−a^n)/(b−a)，令 f(x)=x^n；④出现 ∫_a^x f(t)dt 时，利用它与其导数 f(x) 的导数关系，把 f(x) 写成 (∫_a^x f(t)dt)′ 再配标准形式。
- **关键概念**：`参数与自变量`、`ln 1=0`、`变上限积分`
- **相互关系**：这些变式的后续步骤与基本套路完全一致，只换函数与区间。
- **出处**：[陈哥 P132](https://www.bilibili.com/video/BV1husGzwEtZ?p=132)、[P134](https://www.bilibili.com/video/BV1husGzwEtZ?p=134)

### 拉格朗日中值定理题型二：总思路（从题干条件找突破口）
- **要点**：此类题无固定形式，需从附加条件（有零点、取极值、端点异号、二阶导有界等）找突破口，定出区间内的一个分点，再在两个子区间上各用一次拉格朗日中值定理，最后通过加绝对值与放缩凑出待证不等式。
- **关键概念**：`突破口`、`分点`、`加绝对值放缩`
- **出处**：[陈哥 P135](https://www.bilibili.com/video/BV1husGzwEtZ?p=135)

### 拉格朗日中值定理题型二：与零点定理结合
- **要点**：题干说 f(x) 在区间上至少有一个零点，就设零点为 x₀ 把区间分成两段，分别得 f(x₀)−f(a)=f′(ξ₁)(x₀−a) 与 f(b)−f(x₀)=f′(ξ₂)(b−x₀)，代入 f(x₀)=0 后加绝对值。
- **关键概念**：`零点`、`分区间`、`f(x₀)=0`
- **相互关系**：与反证法中的「至多一个零点」题型形成对照。
- **出处**：[陈哥 P135](https://www.bilibili.com/video/BV1husGzwEtZ?p=135)

### 拉格朗日中值定理题型二：与极值必要条件（费马引理）结合
- **要点**：题干说 f(x) 在区间内取到极值，由极值必要条件（费马引理）知存在 x₀ 使 f′(x₀)=0；此时应对 f′(x) 这个函数使用拉格朗日中值定理，所得结论中出现二阶导 f″(ξ)。
- **关键概念**：`费马引理`、`极值必要条件`、`对 f′(x) 用中值定理`
- **相互关系**：结构与上一类型相同，只是把 f(x₀)=0 换成 f′(x₀)=0，作用对象由 f 变为 f′。
- **出处**：[陈哥 P135](https://www.bilibili.com/video/BV1husGzwEtZ?p=135)

### 拉格朗日中值定理题型二：与端点异号结合及放缩处理
- **要点**：题干给出 f(a)f(b)&lt;0，由零点定理得 f(x₀)=0；对区间内任一点 x 写 f(x)−f(x₀)=f′(ξ)(x−x₀)，加绝对值后用 |x−x₀|&lt;1 与 |f′(ξ)|≤M 两次放缩，得 |f(x)|≤M。处理绝对值时：等式两边可同取绝对值，乘积的绝对值可拆成绝对值之积（|ab|=|a||b|），端点差为正时可直接去绝对值，最后把两个不等式相加、中间项相消得到目标常数。
- **关键概念**：`端点异号`、`两次放缩`、`|ab|=|a||b|`
- **相互关系**：|f′(x)|≤M 表示导数有界，是放缩的依据。
- **出处**：[陈哥 P135](https://www.bilibili.com/video/BV1husGzwEtZ?p=135)

### 拉格朗日中值定理题型二：与罗尔定理结合（二阶导问题）
- **要点**：证存在 ξ 使 f″(ξ)=0，关键是先找出两个一阶导为零的点：把题干等式拆项移项，配成 [f(2)−f(1)]/(2−1)=[f(4)−f(2)]/(4−2) 的形式，在 [1,2]、[2,4] 上分别用拉格朗日中值定理得 f′(ξ₁)=f′(ξ₂)，再对 f′(x) 在 [ξ₁,ξ₂] 上用罗尔定理。
- **关键概念**：`两个一阶导为零`、`配成中值定理等式`、`再对 f′ 用罗尔定理`
- **相互关系**：综合考查拉格朗日中值定理与罗尔定理，是压轴难度题。
- **出处**：[陈哥 P135](https://www.bilibili.com/video/BV1husGzwEtZ?p=135)

### 拉格朗日中值定理题型三：总思路与分点选取
- **要点**：结论中出现两个中值（ξ、η）时，把区间分成两段，每段各用一次拉格朗日中值定理得到两个等式，再通过相加、相乘或取倒数凑出待证结论。分点的选取是最难的一步：最简单时直接取区间中点（如 [0,1] 取 1/2），较难时用第一小问的结论、最值定理得到的 x₀、或介值定理得到的 c 作为分点。
- **关键概念**：`双中值`、`分两段`、`分点`
- **相互关系**：是题型二的延伸；多问题目中第一问常为第二问铺路。
- **出处**：[陈哥 P136](https://www.bilibili.com/video/BV1husGzwEtZ?p=136)

### 拉格朗日中值定理题型三：基础型与乘积型
- **要点**：①已知 f(0)=f(1) 证 f′(ξ)+f′(η)=0：取中点 1/2 分两段，两式相加后 f(0) 与 f(1) 相消、f(1/2) 项互为相反数，即得。②证 f′(η)f′(ξ)=1：先由第一问得 f(c)=1−c，以 c 为分点，两式整理为 (1−c)/c 与 c/(1−c)，相乘得 1。
- **关键概念**：`中点分区间`、`两式相加`、`两式相乘`
- **出处**：[陈哥 P136](https://www.bilibili.com/video/BV1husGzwEtZ?p=136)

### 拉格朗日中值定理题型三：用最值定理与介值定理找分点
- **要点**：①题干给 f(x) 在 [0,1] 上有最大值 M>0，由最值定理存在 x₀ 使 f(x₀)=M，以 x₀ 为分点得 f′(ξ)=M/x₀、f′(η)=−M/(1−x₀)，取绝对值相加后用分母 x₀(1−x₀)≤1/4（令 g(x)=x(1−x) 求最值）放缩，得 ≥4M。②先由最值定理得 m≤f(0)≤M、m≤f(1)≤M，相加得 m≤[f(0)+f(1)]/2=1/2≤M，再由介值定理存在 c 使 f(c)=1/2；以 c 为分点用两次中值定理，取倒数后相加消去 2c 项得 2。
- **关键概念**：`最值定理`、`介值定理`、`x₀(1−x₀)≤1/4`、`取倒数相加`
- **相互关系**：分别为 2025 年山东、黑龙江真题；把最值定理的结论当作介值定理的条件是关键一步。
- **出处**：[陈哥 P136](https://www.bilibili.com/video/BV1husGzwEtZ?p=136)

### 中值定理体系与考试范围
- **要点**：专升本证明题的核心是闭区间上连续函数的性质（最值定理、介值定理、零点定理）与中值定理（罗尔定理、拉格朗日中值定理）。题干出现「一撇」（导数）就考虑中值定理，不出现导数则用最值、介值或零点定理。柯西中值定理、泰勒公式、积分中值定理仅要求了解，一般不作为考点。
- **关键概念**：`最值定理`、`介值定理`、`零点定理`、`罗尔定理`、`拉格朗日中值定理`
- **出处**：[陈哥 P136](https://www.bilibili.com/video/BV1husGzwEtZ?p=136)


