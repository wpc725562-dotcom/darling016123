# 高数 · 极限 · 导数 · 微分学应用

> 函数极限连续、导数与微分、微分中值定理与导数应用

> 本页 3 章 / 273 条知识点。来源与可信度说明见[知识地图总览](/guide/knowledge-map/)。

## 一、函数、极限与连续


### 函数的概念与构成要素
- **要点**：y=f(x)，自变量 x 经对应法则 f 得因变量 y；三要素为自变量、因变量、对应法则（学士帽另把定义域、值域一并列为「五要素」；米哥作「定义域、对应法则、值域」）。定义域与对应法则定了，值域随之确定。学士帽指出自变量受定义域限制、因变量受值域限制，故二者都不是决定性要素。
- **关键概念**：`自变量`、`因变量`、`对应法则`、`定义域`、`值域`
- **相互关系**：判断同一函数只需比定义域与对应法则。
- **出处**：[陈哥 P1](https://www.bilibili.com/video/BV1husGzwEtZ?p=1)；[杰哥 P2](https://www.bilibili.com/video/BV1Up4y1Y76a?p=2)；[米哥 P2](https://www.bilibili.com/video/BV1swAWerEzS?p=2)；[学士帽 P2](https://www.bilibili.com/video/BV1X4411J792?p=2)；[ok姐 P1](https://www.bilibili.com/video/BV1vm421s7mv?p=1)

### 映射与函数的关系
- **要点**：映射是两个非空集合间使每个元素都有唯一确定元素对应的关系；函数是定义域、值域都为数集的特殊映射。自变量与因变量可用任意字母，y=2x、z=2t、f(t)=2t 是同一个函数。
- **关键概念**：`映射`、`数集`
- **出处**：[ok姐 P1](https://www.bilibili.com/video/BV1vm421s7mv?p=1)

### 两函数相同的判定
- **要点**：定义域相同且对应法则（化简后的表达式）相同才是同一函数，只满足其一即不是；不必单独比值域。陷阱：√(x²)=|x|；√x 的平方只在 x≥0 时等于 x；e\^\{ln x\}=x 要求 x>0；ln x² 只能化为 2ln|x|；(∛x)³ 与 x 是同一函数。学士帽强调判断顺序：先比定义域，定义域不同即可直接判定不是同一函数，无需再看对应法则。
- **关键概念**：`定义域`、`对应法则`、`绝对值`
- **相互关系**：比较定义域常用 A/B>0 ⟺ A·B>0、A/B≥0 ⟺ A·B≥0 且 B≠0，先把分式不等式改写成乘法。
- **出处**：[陈哥 P4](https://www.bilibili.com/video/BV1husGzwEtZ?p=4)；[杰哥 P2](https://www.bilibili.com/video/BV1Up4y1Y76a?p=2)；[米哥 P2](https://www.bilibili.com/video/BV1swAWerEzS?p=2)；[学士帽 P3](https://www.bilibili.com/video/BV1X4411J792?p=3)；[斌哥 P16](https://www.bilibili.com/video/BV12DdNYzEvy?p=16)、[P37–P39](https://www.bilibili.com/video/BV12DdNYzEvy?p=37)

### 常见函数的定义域限制清单
- **要点**：分母不为零；偶次根式被开方数 ≥0，奇次根式不限；x\^\{m/n\} 按「先开 n 次方再取 m 次幂」，n 为偶数时同偶次根式；零次幂底数不为零；log_a x 要求真数 >0、底数 a>0 且 a≠1（lg 底 10，ln 底 e）；tan x 要求 x≠π/2+kπ、cot x≠kπ；arcsin、arccos 定义域 [−1,1]，arctan、arccot 定义域 R。各条分别解出后取交集，写成区间或集合；被抠掉的点用并集（如 (1,3)∪(3,+∞)）。
- **关键概念**：`分母不为零`、`偶次根式`、`分数指数幂`、`真数`、`取交集`、`并集`
- **相互关系**：x\^\{1/4\}、x\^\{3/2\} 一类分数指数幂本质都是开偶次根式；写成不等式链、漏掉被抠掉的点是常见失分点。
- **出处**：[陈哥 P1](https://www.bilibili.com/video/BV1husGzwEtZ?p=1)、[P2](https://www.bilibili.com/video/BV1husGzwEtZ?p=2)、[P9](https://www.bilibili.com/video/BV1husGzwEtZ?p=9)；[杰哥 P3](https://www.bilibili.com/video/BV1Up4y1Y76a?p=3)；[米哥 P11](https://www.bilibili.com/video/BV1swAWerEzS?p=11)；[学士帽 P3](https://www.bilibili.com/video/BV1X4411J792?p=3)、[P26](https://www.bilibili.com/video/BV1X4411J792?p=26)、[P45](https://www.bilibili.com/video/BV1X4411J792?p=45)；[ok姐 P6](https://www.bilibili.com/video/BV1vm421s7mv?p=6)；[斌哥 P1–P7](https://www.bilibili.com/video/BV12DdNYzEvy?p=1)、[P14–P16](https://www.bilibili.com/video/BV12DdNYzEvy?p=14)

### 整体思想（框框）
- **要点**：公式中的 x 可换成任意整体「框框」：1/□ ⇒ □≠0，√□ ⇒ □≥0；定义域是表达式最小单元的取值范围。
- **关键概念**：`整体思想`、`框框`、`最小单元`
- **出处**：[杰哥 P3](https://www.bilibili.com/video/BV1Up4y1Y76a?p=3)；[米哥 P11](https://www.bilibili.com/video/BV1swAWerEzS?p=11)

### 求定义域不能先化简
- **要点**：约分、通分、分子分母同乘同一因式都会改变定义域；必须先按原式列条件、定完定义域再考虑化简。讨论极限时可约分。
- **关键概念**：`等价变形`、`同解`
- **相互关系**：与「解方程可以化简」形成对比，是定义域题最隐蔽的失分点。
- **出处**：[陈哥 P4](https://www.bilibili.com/video/BV1husGzwEtZ?p=4)；[米哥 P34](https://www.bilibili.com/video/BV1swAWerEzS?p=34)；[学士帽 P3](https://www.bilibili.com/video/BV1X4411J792?p=3)；[斌哥 P17](https://www.bilibili.com/video/BV12DdNYzEvy?p=17)

### 绝对值与三角型限制条件
- **要点**：|□|≥0 天然成立，故 |□|>0 等价于 □≠0，|□|≥0 可直接删去；解 |x−a|≤b 借 y=|x−a| 的对勾图像更直观。ln|sin x| 型要求 sin x≠0，即 x≠kπ；sin x≥0 的区间须写成 [2kπ,(2k+1)π]，k∈Z。
- **关键概念**：`绝对值`、`对勾函数`、`x≠kπ`
- **出处**：[陈哥 P1](https://www.bilibili.com/video/BV1husGzwEtZ?p=1)；[斌哥 P6–P8](https://www.bilibili.com/video/BV12DdNYzEvy?p=6)、[P19](https://www.bilibili.com/video/BV12DdNYzEvy?p=19)

### 解不等式的常用手段与易错点
- **要点**：一元二次不等式因式分解后画数轴取区间；两边同乘或同除负数必须变号；a^x≤b 型两边取同底对数。易错：拆错因式、忘变号、把交集写成并集。
- **关键概念**：`因式分解`、`十字相乘`、`变号`
- **出处**：[陈哥 P2](https://www.bilibili.com/video/BV1husGzwEtZ?p=2)

### 二次函数三大工具
- **要点**：求根公式 x=(−b±√(b²−4ac))/(2a)；十字相乘 x²+(a+b)x+ab=(x+a)(x+b)；完全平方 a²±2ab+b²=(a±b)²。分母为二次式须先分解再排除零点。
- **关键概念**：`求根公式`、`十字相乘`、`完全平方`
- **出处**：[杰哥 P3](https://www.bilibili.com/video/BV1Up4y1Y76a?p=3)

### 常用代数公式
- **要点**：平方差 (a+b)(a−b)=a²−b²；完全平方 a²±2ab+b²=(a±b)²；立方和差 a³±b³=(a±b)(a²∓ab+b²)。考试常倒着用。
- **关键概念**：`平方差`、`完全平方`、`立方和差`
- **出处**：[杰哥 P7](https://www.bilibili.com/video/BV1Up4y1Y76a?p=7)

### 抽象函数定义域
- **要点**：外层对应法则相同（都是 f）时，括号内整体的取值范围就相同。已知 f(x) 的定义域即 x 的范围，令新括号内整体落进该范围再反解 x；多个括号分别算后取交集。易错：两个 x 不是同一个。
- **关键概念**：`对应法则`、`抽象函数`、`括号内整体`
- **相互关系**：与具体函数定义域题方向相反；解不等式除以负数要变号；eˣ、2ˣ、ln x 型不等式可两边取对数/取指数，或画图读范围。
- **出处**：[陈哥 P3](https://www.bilibili.com/video/BV1husGzwEtZ?p=3)；[杰哥 P4](https://www.bilibili.com/video/BV1Up4y1Y76a?p=4)；[米哥 P11](https://www.bilibili.com/video/BV1swAWerEzS?p=11)；[ok姐 P5](https://www.bilibili.com/video/BV1vm421s7mv?p=5)；[斌哥 P9–P13](https://www.bilibili.com/video/BV12DdNYzEvy?p=9)、[P18](https://www.bilibili.com/video/BV12DdNYzEvy?p=18)

### 值域与离散取值
- **要点**：值域是 y 的取值范围。符号函数 sgn x 只取 −1,0,1，值域须写成离散集合，不能写成区间 [−1,1]。
- **关键概念**：`值域`、`符号函数 sgn x`
- **出处**：[斌哥 P20](https://www.bilibili.com/video/BV12DdNYzEvy?p=20)

### 求函数表达式：换元法与配凑法
- **要点**：①换元法——令括号内整体=t，反解旧变量后代入，再把 t 换回 x（两边都要换干净）；②配凑法——不动左边、改凑右边，把右侧凑成含括号内整体的形式再整体替换。三角型用配凑（借 cos²x=1−sin²x 统一成 sin x）；分式型 f(x+1/x) 用「分子分母同除以 x² 后配完全平方」（加 2 减 2）。括号内形式复杂（cos²x、x−1/x）时配凑更优。
- **关键概念**：`换元法`、`配凑法`、`完全平方`、`x+1/x`
- **相互关系**：换元法通用但常需反解，配凑法快但要求看出结构；两者结果应一致。求出 f(t) 后可直接把 t 写成 x，因函数表达式与自变量字母无关。
- **出处**：[陈哥 P5](https://www.bilibili.com/video/BV1husGzwEtZ?p=5)；[杰哥 P5](https://www.bilibili.com/video/BV1Up4y1Y76a?p=5)；[米哥 P10](https://www.bilibili.com/video/BV1swAWerEzS?p=10)；[斌哥 P21–P25](https://www.bilibili.com/video/BV12DdNYzEvy?p=21)、[P45](https://www.bilibili.com/video/BV12DdNYzEvy?p=45)、[P52](https://www.bilibili.com/video/BV12DdNYzEvy?p=52)

### 由 f(eˣ)、f[f(x)] 型反求表达式
- **要点**：f(eˣ) 型两边取对数即得 f(x)；f[f(x)] 型把 f(x) 当整体代入后通分约简，常见结果化简回 x；三角型 f(sin x) 两边取 arcsin，并顺手求出定义域。
- **关键概念**：`取对数`、`arcsin`、`反函数记号 f⁻¹`
- **相互关系**：三角型结果必须补定义域，因为 arcsin 有 |□|≤1 的限制。
- **出处**：[陈哥 P5](https://www.bilibili.com/video/BV1husGzwEtZ?p=5)；[斌哥 P25](https://www.bilibili.com/video/BV12DdNYzEvy?p=25)、[P43](https://www.bilibili.com/video/BV12DdNYzEvy?p=43)、[P44](https://www.bilibili.com/video/BV12DdNYzEvy?p=44)

### 由内到外的求值顺序
- **要点**：f[g(a)] 先算最内层 g(a)，再层层往外代。若外层是抽象记号（如已知 f(x+2)=…），必须先换元求出 f(x) 再代值。求 g(½) 而只知 g(f(x)) 时，可令 f(x)=½ 反解 x 直接代入，比先求 g(x) 快得多。
- **关键概念**：`复合函数`、`由内到外`、`整体代入`
- **出处**：[斌哥 P26–P28](https://www.bilibili.com/video/BV12DdNYzEvy?p=26)、[P30](https://www.bilibili.com/video/BV12DdNYzEvy?p=30)、[P32–P35](https://www.bilibili.com/video/BV12DdNYzEvy?p=32)

### 分段函数求值的落段判断
- **要点**：先判断自变量落在哪一段定义区间，再代入对应分支，不要带错分支；比较大小借助已知常数（π/2、1、0）判断。画图一段一段画，分段点按是否取到画空心点或实心点。
- **关键概念**：`分段函数`、`分支`、`落段`、`空心点`、`实心点`
- **出处**：[ok姐 P3](https://www.bilibili.com/video/BV1vm421s7mv?p=3)；[斌哥 P27–P29](https://www.bilibili.com/video/BV12DdNYzEvy?p=27)、[P34](https://www.bilibili.com/video/BV12DdNYzEvy?p=34)

### 比较数值大小与求函数过的定点
- **要点**：比较大小不硬算，用图像与基准数：ln 的自变量小于 1 时函数值为负；底数在 (0,1) 的指数函数递减故值小于 1，底数大于 1 的递增故值大于 1。定点必须是两个确定的数，含参数的 f(0)=a−2 不是定点；方法是取使含参数项恒为零的 x 把参数消掉。
- **关键概念**：`指数函数单调性`、`定点`、`消参数`
- **相互关系**：两题本质都考基本函数图像，而非计算。
- **出处**：[斌哥 P31](https://www.bilibili.com/video/BV12DdNYzEvy?p=31)、[P36](https://www.bilibili.com/video/BV12DdNYzEvy?p=36)

### 由极限定义的函数
- **要点**：极限式中出现下标变量（如 n）时它是极限变量，另一字母（如 x）视为常数。先求出 f(x) 再代入求值，最后用 e^(−ln2)=½ 这类化简收尾。
- **关键概念**：`极限变量`、`常数`、`e^(ln□)=□`
- **相互关系**：与「求导时看对谁求导、谁是变量」是同一套变量视角。
- **出处**：[斌哥 P162](https://www.bilibili.com/video/BV12DdNYzEvy?p=162)

### 函数的四种表达形式与分段点
- **要点**：显函数、隐函数（见「方程」即提示）、参数函数、分段函数；分段点必须是相邻两段共有的点。显函数左边只有 y、右边为关于 x 的式子；隐函数由二元方程 F(x,y)=0 表示，如椭圆方程、sin xy=x ln x+y²；少数可显化（圆方程解出 y=±√(1−x²)，需分段），多数无法显化，只能直接求导。
- **关键概念**：`显函数`、`隐函数`、`参数方程`、`分段点`
- **出处**：[陈哥 P6](https://www.bilibili.com/video/BV1husGzwEtZ?p=6)、[P39](https://www.bilibili.com/video/BV1husGzwEtZ?p=39)；[学士帽 P4](https://www.bilibili.com/video/BV1X4411J792?p=4)

### 参数方程的概念
- **要点**：x=f(t)、y=g(t)，x 与 y 无直接联系，靠中间变量 t 搭桥；一个 t 值同时定出一个 x 与一个 y，即曲线上一点。f、g 本身也可为隐函数形式。
- **关键概念**：`参数方程`、`中间变量`
- **相互关系**：典型例子平摆线方程，专升本不作要求。
- **出处**：[陈哥 P6](https://www.bilibili.com/video/BV1husGzwEtZ?p=6)、[P40](https://www.bilibili.com/video/BV1husGzwEtZ?p=40)

### 分段函数及三类常见形式
- **要点**：定义域分成若干段，每段各有表达式。三类：①y=|x| 在 x=0 处为尖点，不可导；②取整函数 [x] 为不超过 x 的最大整数，满足 x−1&lt;[x]≤x；③符号函数 sgn x 按 x>0、=0、&lt;0 取 1、0、−1。去绝对值即按 x≥0、x&lt;0 写成分段函数，是处理含绝对值函数的通用第一步。
- **关键概念**：`分段函数`、`绝对值函数`、`取整函数`、`符号函数`
- **相互关系**：取整函数图像夹在 y=x−1 与 y=x 之间。
- **出处**：[陈哥 P6](https://www.bilibili.com/video/BV1husGzwEtZ?p=6)；[ok姐 P3](https://www.bilibili.com/video/BV1vm421s7mv?p=3)、[P10](https://www.bilibili.com/video/BV1vm421s7mv?p=10)

### 基本初等函数分类「反对幂指三」
- **要点**：分五类——反三角、对数、幂、指数、三角函数，口诀「反对幂指三」；是后续极限、导数、积分的基础，需牢记图像。米哥作「反对幂三指常」六类（多常函数），并指出该顺序即分部积分选 u 的顺序。
- **关键概念**：`反对幂指三`、`基本初等函数`
- **出处**：[陈哥 P9](https://www.bilibili.com/video/BV1husGzwEtZ?p=9)；[米哥 P5](https://www.bilibili.com/video/BV1swAWerEzS?p=5)；[学士帽 P5](https://www.bilibili.com/video/BV1X4411J792?p=5)；[ok姐 P2](https://www.bilibili.com/video/BV1vm421s7mv?p=2)、[P6](https://www.bilibili.com/video/BV1vm421s7mv?p=6)

### 幂函数
- **要点**：y=x^a 的定义域、单调性、奇偶性均由 a 决定；图像必过 (1,1)，不一定过 (0,0)；无界、非周期。重点掌握 y=1/x、y=x、y=√x、y=x²、y=x³ 五个的图像、定义域、值域与性质（√x 定义域 x≥0）。幂运算：x^a·x^b=x\^\{a+b\}、x^a/x^b=x\^\{a−b\}、x\^\{b/a\}=√[a]{x^b}、x\^\{−a\}=1/x^a。学士帽逐一给出五者图像：x\^\{−1\} 是一三象限双曲线、x\^\{1/2\}=√x 定义域 x≥0、x 是一三象限角平分线、x² 是开口向上的抛物线、x³ 在 x² 基础上把左半支沿 x 轴翻下。
- **关键概念**：`幂函数`、`同底数幂`、`负指数`
- **出处**：[陈哥 P9](https://www.bilibili.com/video/BV1husGzwEtZ?p=9)；[杰哥 P7](https://www.bilibili.com/video/BV1Up4y1Y76a?p=7)；[米哥 P5](https://www.bilibili.com/video/BV1swAWerEzS?p=5)；[学士帽 P5](https://www.bilibili.com/video/BV1X4411J792?p=5)；[ok姐 P2](https://www.bilibili.com/video/BV1vm421s7mv?p=2)；[石头 P7](https://www.bilibili.com/video/BV18CL26WEJ3?p=7)

### 指数函数
- **要点**：y=a^x（a>0,a≠1），定义域 R，值域 (0,+∞)，恒过 (0,1)；a>1 单增，0&lt;a&lt;1 单减；无界（有下界 0 无上界），非奇非偶、无周期。a=e 时即 y=e^x，最常用；e\^\{+∞\}=+∞、e\^\{−∞\}=0。
- **关键概念**：`指数函数`、`底数 a`、`e`
- **相互关系**：x→−∞ 时 e^x→0、x→+∞ 时 e^x→+∞，是求极限时的重要结论。
- **出处**：[陈哥 P9](https://www.bilibili.com/video/BV1husGzwEtZ?p=9)；[杰哥 P7](https://www.bilibili.com/video/BV1Up4y1Y76a?p=7)；[米哥 P6](https://www.bilibili.com/video/BV1swAWerEzS?p=6)；[学士帽 P6](https://www.bilibili.com/video/BV1X4411J792?p=6)；[ok姐 P2](https://www.bilibili.com/video/BV1vm421s7mv?p=2)

### 对数函数
- **要点**：y=log_a x（a>0,a≠1），定义域 (0,+∞)，值域 R，恒过 (1,0)；a>1 单增，0&lt;a&lt;1 单减；无界、非奇非偶、无周期；真数必须恒大于零。ln x 递增，x→+∞ 时 →+∞、x→0⁺ 时 →−∞。公式：log_a(MN)=log_aM+log_aN、log_a(M/N)=log_aM−log_aN、log_aM^n=n log_aM、log_a a=1、log_a 1=0、a\^\{log\_a x\}=x、e\^\{ln x\}=x（须整体化）。学士帽记忆口诀「去 e 用 ln，去 ln 用 e」；易错：ln(a+b) 不能拆、ln(a/b)≠ln a/ln b。
- **关键概念**：`对数函数`、`真数`、`ln`、`lg`
- **相互关系**：与指数函数互为反函数；解指数中的 x 两边取同底对数，解对数中的 x 两边取同底指数，所取底数必须与原底数一致。
- **出处**：[陈哥 P5](https://www.bilibili.com/video/BV1husGzwEtZ?p=5)、[P9](https://www.bilibili.com/video/BV1husGzwEtZ?p=9)；[杰哥 P7](https://www.bilibili.com/video/BV1Up4y1Y76a?p=7)；[米哥 P7](https://www.bilibili.com/video/BV1swAWerEzS?p=7)；[学士帽 P7](https://www.bilibili.com/video/BV1X4411J792?p=7)；[ok姐 P2](https://www.bilibili.com/video/BV1vm421s7mv?p=2)

### 指数函数与对数函数互为反函数
- **要点**：y=a^x 与 y=log_a x 互为反函数，定义域与值域互换，指数函数过 (0,1)、对数函数过 (1,0)；a^x=y 与 log_a y=x 是同一关系的两种表示。
- **关键概念**：`互为反函数`
- **出处**：[杰哥 P7](https://www.bilibili.com/video/BV1Up4y1Y76a?p=7)；[米哥 P6](https://www.bilibili.com/video/BV1swAWerEzS?p=6)、[P7](https://www.bilibili.com/video/BV1swAWerEzS?p=7)；[ok姐 P2](https://www.bilibili.com/video/BV1vm421s7mv?p=2)

### 三角函数与常用数值表
- **要点**：sin x 定义域 R、值域 [−1,1]、奇函数、有界、最小正周期 2π；cos x 定义域 R、值域 [−1,1]、偶函数、有界、周期 2π；tan x 定义域 x≠π/2+kπ、值域 R、奇函数、无界、最小正周期 π，在 (−π/2,π/2) 单增。六函数 sin、cos、tan、cot、sec、csc；sec x=1/cos x、csc x=1/sin x、cot x=cos x/sin x（易错：sec x 是 cos x 的倒数而非 sin x 的倒数）。特殊值：0、π/6、π/4、π/3、π/2 处 sin 为 √0/2、√1/2、√2/2、√3/2、√4/2，cos 倒序，tan=sin÷cos，tan(π/2) 不存在。
- **关键概念**：`sec x`、`csc x`、`cot x`、`特殊角`、`最小正周期`
- **出处**：[陈哥 P9](https://www.bilibili.com/video/BV1husGzwEtZ?p=9)；[杰哥 P7](https://www.bilibili.com/video/BV1Up4y1Y76a?p=7)、[P10](https://www.bilibili.com/video/BV1Up4y1Y76a?p=10)；[米哥 P8](https://www.bilibili.com/video/BV1swAWerEzS?p=8)；[学士帽 P8](https://www.bilibili.com/video/BV1X4411J792?p=8)；[ok姐 P2](https://www.bilibili.com/video/BV1vm421s7mv?p=2)

### 三角恒等变换公式
- **要点**：平方和：sin²x+cos²x=1、1+tan²x=sec²x、1+cot²x=csc²x（六边形记忆法：左「正」右「余」、中心 1，对角线乘积为 1，倒三角形底边平方和等于顶点平方）；和差角：sin(α±β)=sinαcosβ±cosαsinβ、cos(α±β)=cosαcosβ∓sinαsinβ；二倍角：sin2x=2sin x cos x、cos2x=cos²x−sin²x=1−2sin²x=2cos²x−1；降幂：cos²x=(1+cos2x)/2、sin²x=(1−cos2x)/2；立方和差：a³±b³=(a±b)(a²∓ab+b²)。
- **关键概念**：`同角平方关系`、`倍角公式`、`降幂公式`、`六边形记忆法`
- **相互关系**：第三章一元函数积分中大量使用；公式中的 x 都要用整体思想换成任意「框框」。
- **出处**：[陈哥 P9](https://www.bilibili.com/video/BV1husGzwEtZ?p=9)；[杰哥 P7](https://www.bilibili.com/video/BV1Up4y1Y76a?p=7)；[米哥 P8](https://www.bilibili.com/video/BV1swAWerEzS?p=8)；[学士帽 P9](https://www.bilibili.com/video/BV1X4411J792?p=9)

### 反三角函数
- **要点**：只掌握 arcsin x、arccos x、arctan x（米哥另列 arccot）。arctan x 定义域 R、值域 (−π/2,π/2)、单增、有界、奇函数，最重要，有水平渐近线 y=±π/2；arcsin x 定义域 [−1,1]、值域 [−π/2,π/2]、单增、有界、奇函数；arccos x 定义域 [−1,1]、值域 [0,π]、单减、有界、非奇非偶。三组图像均满足定义域值域互换、关于 y=x 对称。求值即反向找角：arctan1=π/4、arcsin1=π/2、arccos0=π/2、arctan0=0、arctan√3=π/3。
- **关键概念**：`arcsin`、`arccos`、`arctan`、`值域`
- **相互关系**：arctan(+∞)=π/2、arctan(−∞)=−π/2，规范写法需用极限符号。
- **出处**：[陈哥 P9](https://www.bilibili.com/video/BV1husGzwEtZ?p=9)、[P11](https://www.bilibili.com/video/BV1husGzwEtZ?p=11)；[杰哥 P7](https://www.bilibili.com/video/BV1Up4y1Y76a?p=7)；[米哥 P9](https://www.bilibili.com/video/BV1swAWerEzS?p=9)；[学士帽 P10](https://www.bilibili.com/video/BV1X4411J792?p=10)；[石头 P7](https://www.bilibili.com/video/BV18CL26WEJ3?p=7)

### 常数函数
- **要点**：y=C 的图像是水平直线（关于 y 轴对称，是偶函数，导数为零），x=C 的图像是竖直直线；x 轴对应 y=0，y 轴对应 x=0，二重积分画图时需写出这些边界表达式。学士帽指出常数函数定义域、值域均为全体实数。
- **关键概念**：`常数函数`、`x 轴`、`y 轴`
- **出处**：[陈哥 P9](https://www.bilibili.com/video/BV1husGzwEtZ?p=9)；[杰哥 P7](https://www.bilibili.com/video/BV1Up4y1Y76a?p=7)；[学士帽 P5](https://www.bilibili.com/video/BV1X4411J792?p=5)

### 复合函数与初等函数
- **要点**：把 y=f(u) 中自变量的位置替换为另一个函数 u=g(x) 即构成复合函数，嵌套可多于两层，要求内层 g(x) 的值域落在外层 f 的定义域内。由常数与基本初等函数经有限次四则运算和有限次复合构成、可用一个式子表示的函数称初等函数；四则运算所得函数的定义域是各部分定义域的交集，分式还须分母不为零。由常数与基本初等函数经四则运算构成的函数称简单函数（如 2+sin x），不是严格的数学概念。
- **关键概念**：`复合函数`、`内层`、`外层`、`简单函数`、`初等函数`
- **相互关系**：分式函数分母为零处是后续间断点的考察对象。
- **出处**：[陈哥 P8](https://www.bilibili.com/video/BV1husGzwEtZ?p=8)、[P10](https://www.bilibili.com/video/BV1husGzwEtZ?p=10)；[杰哥 P8](https://www.bilibili.com/video/BV1Up4y1Y76a?p=8)；[米哥 P10](https://www.bilibili.com/video/BV1swAWerEzS?p=10)；[学士帽 P11](https://www.bilibili.com/video/BV1X4411J792?p=11)；[ok姐 P5](https://www.bilibili.com/video/BV1vm421s7mv?p=5)、[P6](https://www.bilibili.com/video/BV1vm421s7mv?p=6)

### 复合函数的分解
- **要点**：由外向里层层分解，每层定位一个基本初等函数，其余部分整体视为中间变量；分解到基本初等函数或简单函数为止，每层都必须对应一个基本初等函数，每层依次用 u、v、w 表示。如 y=sin(ln√(x²−1)) 分为 y=sin u、u=ln v、v=√w、w=x²−1。ok姐口诀「看谁跟 x 直接接触」——直接接触者作最内层，由内向外层层分解。
- **关键概念**：`由外向内`、`中间变量`、`分层`、`u,v,w`
- **相互关系**：易混 sin²x 与 sin x²（sin²x 外层是平方、sin x² 外层是 sin）；拆分本身不考，但复合函数求导完全依赖它，拆分不彻底会导致求导出错。
- **出处**：[陈哥 P10](https://www.bilibili.com/video/BV1husGzwEtZ?p=10)；[杰哥 P8](https://www.bilibili.com/video/BV1Up4y1Y76a?p=8)；[米哥 P10](https://www.bilibili.com/video/BV1swAWerEzS?p=10)；[学士帽 P11](https://www.bilibili.com/video/BV1X4411J792?p=11)；[ok姐 P5](https://www.bilibili.com/video/BV1vm421s7mv?p=5)

### 复合函数的定义域
- **要点**：由外向内——先由外层函数确定中间变量的取值范围，再解不等式求 x 的范围。
- **关键概念**：`中间变量`
- **出处**：[ok姐 P5](https://www.bilibili.com/video/BV1vm421s7mv?p=5)

### 反函数的概念与求法
- **要点**：把 y=f(x) 的自变量与因变量互换即得反函数，记 x=f⁻¹(y)；f⁻¹ 只是「对应法则」的记号，不是倒数也不是幂。两步——①反解：从 y=f(x) 中解出 x；②对调：把 x 与 y 互换。反解最难，常用取对数、取指数、开方、解方程。定义域可写可不写，写严格些不扣分。本质是定义域与值域互换（y=x²，x∈[0,2] 的反函数定义域 [0,4]、值域 [0,2]）。
- **关键概念**：`反函数`、`f⁻¹`、`反解 x`、`对调 x 与 y`
- **相互关系**：单调函数必有反函数，非单调函数可取单调区间求反函数；原函数与反函数单调性一致；是确定分段函数反函数各段定义域的依据。
- **出处**：[陈哥 P11](https://www.bilibili.com/video/BV1husGzwEtZ?p=11)、[P12](https://www.bilibili.com/video/BV1husGzwEtZ?p=12)；[杰哥 P6](https://www.bilibili.com/video/BV1Up4y1Y76a?p=6)；[米哥 P12](https://www.bilibili.com/video/BV1swAWerEzS?p=12)；[学士帽 P12](https://www.bilibili.com/video/BV1X4411J792?p=12)；[斌哥 P49](https://www.bilibili.com/video/BV12DdNYzEvy?p=49)、[P52](https://www.bilibili.com/video/BV12DdNYzEvy?p=52)、[P55](https://www.bilibili.com/video/BV12DdNYzEvy?p=55)、[P56](https://www.bilibili.com/video/BV12DdNYzEvy?p=56)；[石头 P6](https://www.bilibili.com/video/BV18CL26WEJ3?p=6)

### 反函数的四条基本性质
- **要点**：①反函数的定义域是原函数的值域，反函数的值域是原函数的定义域；②原函数过 (a,b) 则反函数过 (b,a)；③互为反函数的图像关于 y=x 对称；④常见反函数对：sin x 与 arcsin x、tan x 与 arctan x、eˣ 与 ln x。
- **关键概念**：`f⁻¹`、`关于 y=x 对称`、`值域与定义域互换`
- **相互关系**：求 f⁻¹(a) 时用性质②反解更快，不必求出整个反函数；三角函数取单调段求反三角函数即由此而来。
- **出处**：[陈哥 P11](https://www.bilibili.com/video/BV1husGzwEtZ?p=11)、[P12](https://www.bilibili.com/video/BV1husGzwEtZ?p=12)；[杰哥 P6](https://www.bilibili.com/video/BV1Up4y1Y76a?p=6)；[米哥 P12](https://www.bilibili.com/video/BV1swAWerEzS?p=12)；[学士帽 P12](https://www.bilibili.com/video/BV1X4411J792?p=12)；[斌哥 P50–P54](https://www.bilibili.com/video/BV12DdNYzEvy?p=50)

### 反函数的重要关系式
- **要点**：f(f⁻¹(x))=x，f⁻¹(f(x))=x。用它可反解反三角函数值：令 a=arctan 1，两边取 tan 得 tan a=1，故 a=π/4。
- **关键概念**：`f(f⁻¹(x))=x`、`反三角函数求值`
- **相互关系**：使用时必须注意范围——arctan 的结果只能落在 (−π/2,π/2)，arcsin 的自变量只能取 [−1,1]。
- **出处**：[陈哥 P11](https://www.bilibili.com/video/BV1husGzwEtZ?p=11)、[P12](https://www.bilibili.com/video/BV1husGzwEtZ?p=12)

### 分段函数求反函数
- **要点**：逐段反解出 x，逐段对调 x、y；各段定义域由原函数在该段的值域确定，最后用「综上」拼起来。
- **关键概念**：`分段函数`、`分段点`、`用值域定定义域`
- **出处**：[陈哥 P12](https://www.bilibili.com/video/BV1husGzwEtZ?p=12)；[米哥 P12](https://www.bilibili.com/video/BV1swAWerEzS?p=12)

### 复杂反函数的求解套路
- **要点**：分式型先乘开、移项、合并同类项再解出 x；含指数对数型两边取对数或取指数；y=ln(x+√(x²−1)) 型先取指数，再用根式有理化得 x−√(x²−1) 的第二式，两式相加消去根号；y=(e^x−e\^\{−x\})/2 型两边同乘 e^x 化为关于 e^x 的一元二次方程，用求根公式解出 e^x（舍负根）再取对数。
- **关键概念**：`根式有理化`、`取指数`、`求根公式`
- **出处**：[陈哥 P12](https://www.bilibili.com/video/BV1husGzwEtZ?p=12)

### 奇偶性的定义与条件
- **要点**：判断前定义域必须关于原点对称，否则一定非奇非偶。对称定义域内 f(−x)=f(x) 为偶函数（图像关于 y 轴对称），f(−x)=−f(x) 为奇函数（图像关于原点中心对称）；两种关系都不成立即非奇非偶。
- **关键概念**：`定义域关于原点对称`、`偶函数`、`奇函数`、`非奇非偶`
- **相互关系**：如 [−3,0)∪(0,2] 两端不对称，直接判定无奇偶性，可排除奇/偶选项。
- **出处**：[陈哥 P8](https://www.bilibili.com/video/BV1husGzwEtZ?p=8)；[杰哥 P9](https://www.bilibili.com/video/BV1Up4y1Y76a?p=9)；[米哥 P4](https://www.bilibili.com/video/BV1swAWerEzS?p=4)；[学士帽 P13](https://www.bilibili.com/video/BV1X4411J792?p=13)；[ok姐 P7](https://www.bilibili.com/video/BV1vm421s7mv?p=7)；[斌哥 P60](https://www.bilibili.com/video/BV12DdNYzEvy?p=60)、[P62](https://www.bilibili.com/video/BV12DdNYzEvy?p=62)、[P76](https://www.bilibili.com/video/BV12DdNYzEvy?p=76)

### 常见奇偶函数
- **要点**：常见偶函数：cos x、|x|、x\^\{2n\}、常数函数；常见奇函数：sin x、tan x、x\^\{2n−1\}、ln(x+√(x²±1))、arctan x、arcsin x。反函数中 arctan x、arcsin x 为奇，arccos x 无奇偶性；对数函数、指数函数均无奇偶性。
- **关键概念**：`偶次幂`、`奇次幂`、`常见奇偶函数`
- **出处**：[陈哥 P8](https://www.bilibili.com/video/BV1husGzwEtZ?p=8)；[杰哥 P9](https://www.bilibili.com/video/BV1Up4y1Y76a?p=9)；[ok姐 P7](https://www.bilibili.com/video/BV1vm421s7mv?p=7)、[P65](https://www.bilibili.com/video/BV1vm421s7mv?p=65)

### 奇偶性的四则运算规律
- **要点**：奇±奇=奇（两个相同奇函数相减得 0，为偶函数，属特例）；偶±偶=偶；奇±偶=非奇非偶；奇×÷奇=偶；奇×÷偶=奇；偶×÷偶=偶。任何非零常函数（含常数 1）都是偶函数，乘或除一个非零常数不改变奇偶性。
- **关键概念**：`奇偶性四则运算`、`非奇非偶`
- **相互关系**：不必死记，用 x（奇）与 x²（偶）现场推导即可；注意「奇奇相乘」是偶函数。
- **出处**：[陈哥 P8](https://www.bilibili.com/video/BV1husGzwEtZ?p=8)；[杰哥 P9](https://www.bilibili.com/video/BV1Up4y1Y76a?p=9)；[米哥 P4](https://www.bilibili.com/video/BV1swAWerEzS?p=4)；[斌哥 P57–P59](https://www.bilibili.com/video/BV12DdNYzEvy?p=57)、[P61](https://www.bilibili.com/video/BV12DdNYzEvy?p=61)、[P64](https://www.bilibili.com/video/BV12DdNYzEvy?p=64)、[P69–P72](https://www.bilibili.com/video/BV12DdNYzEvy?p=69)、[P75](https://www.bilibili.com/video/BV12DdNYzEvy?p=75)

### 复合函数奇偶性口诀
- **要点**：内偶则偶——最内层为偶函数则整体为偶；最内层为奇函数则整体奇偶性取决于最外层（全奇则奇，内奇同外）。判断最内层时，同一级的加减项（如 1+x²）要整体视为最内层。
- **关键概念**：`内偶则偶`、`全奇则奇`、`内奇同外`
- **出处**：[陈哥 P8](https://www.bilibili.com/video/BV1husGzwEtZ?p=8)；[杰哥 P9](https://www.bilibili.com/video/BV1Up4y1Y76a?p=9)；[斌哥 P57–P59](https://www.bilibili.com/video/BV12DdNYzEvy?p=57)

### 用定义判断奇偶性与构造奇偶函数
- **要点**：任何函数都能用定义判断，口诀只是提速。技巧：含根号的先有理化（ln(x+√(x²+1)) 用根式有理化），含指数的先分子分母同乘 eˣ 之类的因子（(e^x−1)/(e^x+1) 分子分母同乘 e^x），ln((1−x)/(1+x)) 用颠倒相乘，e^x−e\^\{−x\} 提负号。构造：对任意 f(x)，f(x)+f(−x) 必为偶，f(x)−f(−x) 必为奇（具体化为 eˣ 后即 eˣ+e\^\{−x\} 偶、eˣ−e\^\{−x\} 奇）。
- **关键概念**：`根式有理化`、`颠倒相乘`、`f(x)−f(−x)`、`f(x)+f(−x)`
- **相互关系**：这是判断 2ˣ−2\^\{−x\}、2ˣ+2\^\{−x\} 一类题目的快捷依据。
- **出处**：[陈哥 P8](https://www.bilibili.com/video/BV1husGzwEtZ?p=8)；[杰哥 P9](https://www.bilibili.com/video/BV1Up4y1Y76a?p=9)；[斌哥 P60](https://www.bilibili.com/video/BV12DdNYzEvy?p=60)、[P61](https://www.bilibili.com/video/BV12DdNYzEvy?p=61)、[P63](https://www.bilibili.com/video/BV12DdNYzEvy?p=63)

### 有界性
- **要点**：存在 m、M 使恒有 m≤f(x)≤M（或 |f(x)|≤M）则有界，m 为下界、M 为上界；上下界缺一即无界。常见有界函数：sin□、cos□、arctan□、arccot□、arcsin□、arccos□、1/(1+x²)，其中 x 换成任意表达式后仍有界（arctan 取值在 ±π/2 之间）。y=x² 有下界 0 无上界，是无界函数；绝大多数函数无界。闭区间上连续的函数必有界；开区间上连续推不出有界，反例 1/x 在 (0,1)。附加条件：若左端点的右极限与右端点的左极限都存在且有限，则函数在该开区间上有界。
- **关键概念**：`有界`、`上界`、`下界`、`闭区间连续必有界`、`单侧极限`
- **相互关系**：本质是「端点一旦被限制住，函数就有界」；也可用放缩：由 x²≥0 得分母≥1，从而分式≤1，配合非负性得 0≤f≤1；有界函数加减有界函数、加减常数都有界；复合函数的有界性取决于最外层函数。
- **出处**：[陈哥 P7](https://www.bilibili.com/video/BV1husGzwEtZ?p=7)；[杰哥 P10](https://www.bilibili.com/video/BV1Up4y1Y76a?p=10)；[米哥 P3](https://www.bilibili.com/video/BV1swAWerEzS?p=3)；[学士帽 P13](https://www.bilibili.com/video/BV1X4411J792?p=13)；[ok姐 P7](https://www.bilibili.com/video/BV1vm421s7mv?p=7)、[P13](https://www.bilibili.com/video/BV1vm421s7mv?p=13)；[斌哥 P65](https://www.bilibili.com/video/BV12DdNYzEvy?p=65)、[P66](https://www.bilibili.com/video/BV12DdNYzEvy?p=66)、[P71](https://www.bilibili.com/video/BV12DdNYzEvy?p=71)、[P74](https://www.bilibili.com/video/BV12DdNYzEvy?p=74)、[P97](https://www.bilibili.com/video/BV12DdNYzEvy?p=97)

### 无穷大与无界的区别
- **要点**：无穷大量要求「步步高升」，即在该极限过程中函数值趋于无穷；无界只要求找不到两条水平线把它夹住。结论：无穷大一定无界，但无界不一定是无穷大。
- **关键概念**：`无穷大量`、`无界`、`震荡`
- **相互关系**：反例是奇数项递增、偶数项恒为 0 的数列，以及 x sin x——它被 y=±x 夹住，无界但在 x=kπ 处取 0，故不是无穷大。
- **出处**：[斌哥 P102](https://www.bilibili.com/video/BV12DdNYzEvy?p=102)

### 周期性
- **要点**：f(x+T)=f(x) 为周期函数，通常指最小正周期。sin x、cos x 周期 2π，|sin x|、|cos x|、tan x 周期 π；若 f(x) 周期为 T，则 f(ax+b) 的周期为 T/|a|，与 b 无关（sin2x 周期 π，tan2x 周期 π/2）。两个周期函数相加，周期取各自周期的最小公倍数。学士帽另列 cot x 的周期为 π。
- **关键概念**：`周期函数`、`T/|a|`、`最小公倍数`、`最小正周期`
- **相互关系**：−ln x 递减、eˣ 递增，都不是周期函数；仅级数中的傅立叶级数涉及周期，考察不多。
- **出处**：[杰哥 P10](https://www.bilibili.com/video/BV1Up4y1Y76a?p=10)；[米哥 P3](https://www.bilibili.com/video/BV1swAWerEzS?p=3)；[学士帽 P13](https://www.bilibili.com/video/BV1X4411J792?p=13)；[ok姐 P7](https://www.bilibili.com/video/BV1vm421s7mv?p=7)；[斌哥 P67](https://www.bilibili.com/video/BV12DdNYzEvy?p=67)、[P68](https://www.bilibili.com/video/BV12DdNYzEvy?p=68)、[P71](https://www.bilibili.com/video/BV12DdNYzEvy?p=71)、[P77](https://www.bilibili.com/video/BV12DdNYzEvy?p=77)

### 取整函数
- **要点**：[x] 表示不超过 x 的最大整数，即数轴上 x 左侧的整数，故 [−3.2]=−4 而不是 −3。结论：x−[x] 既是有界函数也是周期函数。
- **关键概念**：`取整函数 [x]`、`不超过 x 的最大整数`
- **相互关系**：负数的取整是最常错的地方。
- **出处**：[陈哥 P6](https://www.bilibili.com/video/BV1husGzwEtZ?p=6)；[斌哥 P73](https://www.bilibili.com/video/BV12DdNYzEvy?p=73)

### 单调性
- **要点**：定义域内任取 x₁&lt;x₂，恒有 f(x₁)&lt;f(x₂) 则单增，恒有 f(x₁)>f(x₂) 则单减；整个定义区间内单调的函数叫单调函数。
- **关键概念**：`单调递增`、`单调递减`、`任意性`、`单调区间`
- **相互关系**：易错——y=1/x 在 (−∞,0) 与 (0,+∞) 上分别递减，但不能称其在整个定义域上单调递减。
- **出处**：[陈哥 P7](https://www.bilibili.com/video/BV1husGzwEtZ?p=7)；[杰哥 P10](https://www.bilibili.com/video/BV1Up4y1Y76a?p=10)；[ok姐 P7](https://www.bilibili.com/video/BV1vm421s7mv?p=7)

### 极限的概念与书写形式
- **要点**：描述某个量在一定条件下变化时所趋向的状态，即「趋势」。lim\_\{x→x₀\}f(x)=A，A 必须是确定的常数；数列极限 lim\_\{n→∞\}x_n=b，默认 n→+∞。极限是「无限接近」的过程，不是「等于」。两个基础极限：lim\_\{x→0\} k/x=∞（k≠0），lim\_\{x→∞\} k/x=0；绝大多数极限可直接代入求值。
- **关键概念**：`极限`、`趋势`、`代入求值`
- **相互关系**：数列极限中 n→∞ 特指 +∞，函数极限中 x→∞ 泛指 ±∞。
- **出处**：[陈哥 P14](https://www.bilibili.com/video/BV1husGzwEtZ?p=14)；[杰哥 P11](https://www.bilibili.com/video/BV1Up4y1Y76a?p=11)、[P12](https://www.bilibili.com/video/BV1Up4y1Y76a?p=12)；[米哥 P13](https://www.bilibili.com/video/BV1swAWerEzS?p=13)；[ok姐 P8](https://www.bilibili.com/video/BV1vm421s7mv?p=8)、[P10](https://www.bilibili.com/video/BV1vm421s7mv?p=10)；[学士帽 P14](https://www.bilibili.com/video/BV1X4411J792?p=14)

### 数列极限的定义与 ε-N
- **要点**：严格定义：对任意 ε>0，总存在正整数 N，当 n>N 时 |x_n−A|&lt;ε。存在极限称收敛，不存在称发散。
- **关键概念**：`ε-N`、`收敛`、`发散`
- **出处**：[ok姐 P8](https://www.bilibili.com/video/BV1vm421s7mv?p=8)

### 收敛数列的性质
- **要点**：①唯一性——极限唯一；②有界性——收敛数列一定有界；③保号性——若 A>0（或 A&lt;0），则从某一项起各项都大于零（或小于零）。
- **关键概念**：`唯一性`、`有界性`、`保号性`
- **相互关系**：收敛与「极限存在」是同一意思。
- **出处**：[ok姐 P8](https://www.bilibili.com/video/BV1vm421s7mv?p=8)；[石头 P9](https://www.bilibili.com/video/BV18CL26WEJ3?p=9)

### 数列收敛与有界、子列
- **要点**：收敛必有界；有界不一定收敛；发散不一定无界（反例 (−1)ⁿ）。单调有界准则：单调有界数列必有极限。子列是原数列的一部分，发散数列的子列可能收敛（(−1)ⁿ 的偶数子列恒为 1），收敛数列的任意子列都收敛。
- **关键概念**：`收敛`、`发散`、`单调有界准则`、`子列`
- **出处**：[斌哥 P79–P81](https://www.bilibili.com/video/BV12DdNYzEvy?p=79)

### 极限值与函数值无关
- **要点**：lim\_\{x→x₀\}f(x) 与 f(x) 在 x₀ 处有无定义、f(x₀) 等于多少无关（(x²−1)/(x−1) 在 x=1 无定义但极限存在）。是「0/0 型」可计算的根本原因。
- **关键概念**：`极限值`、`函数值`
- **出处**：[杰哥 P12](https://www.bilibili.com/video/BV1Up4y1Y76a?p=12)；[斌哥 P78](https://www.bilibili.com/video/BV12DdNYzEvy?p=78)、[P79](https://www.bilibili.com/video/BV12DdNYzEvy?p=79)、[P81](https://www.bilibili.com/video/BV12DdNYzEvy?p=81)

### 极限存在的充要条件（左右极限）
- **要点**：lim\_\{x→x₀\}f(x)=A ⟺ 左极限 f(x₀⁻) 与右极限 f(x₀⁺) 都存在且相等；只要不等或其一为无穷，该点极限不存在。计算左右极限时代入的仍是 x₀，正负号只表示从哪一侧趋近。x→∞ 的情形：lim\_\{x→∞\}f(x)=A ⟺ lim\_\{x→+∞\}f(x) 与 lim\_\{x→−∞\}f(x) 都存在且相等。
- **关键概念**：`左极限`、`右极限`、`充要条件`
- **相互关系**：「左右极限都存在」是「极限存在」的必要不充分条件；判断充分/必要就看「左能否推右、右能否推左」。
- **出处**：[陈哥 P14](https://www.bilibili.com/video/BV1husGzwEtZ?p=14)；[杰哥 P12](https://www.bilibili.com/video/BV1Up4y1Y76a?p=12)、[P22](https://www.bilibili.com/video/BV1Up4y1Y76a?p=22)、[P23](https://www.bilibili.com/video/BV1Up4y1Y76a?p=23)；[米哥 P13](https://www.bilibili.com/video/BV1swAWerEzS?p=13)；[学士帽 P15](https://www.bilibili.com/video/BV1X4411J792?p=15)、[P16](https://www.bilibili.com/video/BV1X4411J792?p=16)；[ok姐 P10](https://www.bilibili.com/video/BV1vm421s7mv?p=10)、[P11](https://www.bilibili.com/video/BV1vm421s7mv?p=11)、[P19](https://www.bilibili.com/video/BV1vm421s7mv?p=19)；[斌哥 P80](https://www.bilibili.com/video/BV12DdNYzEvy?p=80)、[P82](https://www.bilibili.com/video/BV12DdNYzEvy?p=82)

### 必须讨论左右极限的情形与典型结果
- **要点**：只有几类必须分开求：①含 e\^\{1/x\}、arctan(1/x)、2\^\{1/x\} 在 x→0 处；②e^x、arctan x 在无穷处；③分段函数在分段点处；④含绝对值（先按 x 正负去绝对值）。典型结果：arctan(+∞)=π/2、arctan(−∞)=−π/2，故 lim\_\{x→∞\}arctan x 不存在；lim\_\{x→+∞\}e^x=+∞、lim\_\{x→−∞\}e^x=0，故 lim\_\{x→∞\}e^x 不存在；lim\_\{x→0⁻\}|x|/x=−1、lim\_\{x→0⁺\}|x|/x=1，故该极限不存在；lim\_\{x→0⁺\}e\^\{1/x\}=+∞、lim\_\{x→0⁻\}e\^\{1/x\}=0；lim\_\{x→0⁺\}arctan(1/x)=π/2、lim\_\{x→0⁻\}arctan(1/x)=−π/2。
- **关键概念**：`e^{1/x}`、`arctan(1/x)`、`分段点`、`极限不存在`
- **相互关系**：若题设「极限存在」，则左右极限相等，可用来求参数；是判断分段点、间断点类型的基础。
- **出处**：[陈哥 P14](https://www.bilibili.com/video/BV1husGzwEtZ?p=14)；[杰哥 P22](https://www.bilibili.com/video/BV1Up4y1Y76a?p=22)、[P23](https://www.bilibili.com/video/BV1Up4y1Y76a?p=23)；[米哥 P14](https://www.bilibili.com/video/BV1swAWerEzS?p=14)；[学士帽 P16](https://www.bilibili.com/video/BV1X4411J792?p=16)；[ok姐 P13](https://www.bilibili.com/video/BV1vm421s7mv?p=13)；[斌哥 P87–P92](https://www.bilibili.com/video/BV12DdNYzEvy?p=87)、[P169](https://www.bilibili.com/video/BV12DdNYzEvy?p=169)、[P200](https://www.bilibili.com/video/BV12DdNYzEvy?p=200)

### 基本初等函数趋于无穷的极限
- **要点**：只有四个存在：lim\_\{x→∞\}1/x=0；0&lt;a&lt;1 时 lim\_\{x→+∞\}a^x=0；lim\_\{x→−∞\}e^x=0；lim\_\{x→±∞\}arctan x=±π/2。其余如 x、√x、x²、x³、ln x、sin x、cos x 趋于无穷时极限都不存在（图像直接读出）。
- **关键概念**：`arctan x`、`无穷大量`
- **出处**：[ok姐 P9](https://www.bilibili.com/video/BV1vm421s7mv?p=9)、[P11](https://www.bilibili.com/video/BV1vm421s7mv?p=11)、[P19](https://www.bilibili.com/video/BV1vm421s7mv?p=19)

### 基本初等函数在定义域内点处的极限
- **要点**：基本初等函数在其定义域内的点 x₀ 处极限等于该点函数值，即 lim\_\{x→x₀\}f(x)=f(x₀)；判断 x₀ 是否在定义域内只需代入看能否算出值。这是代入法的理论依据。
- **关键概念**：`代入法`
- **出处**：[ok姐 P10](https://www.bilibili.com/video/BV1vm421s7mv?p=10)、[P11](https://www.bilibili.com/video/BV1vm421s7mv?p=11)、[P19](https://www.bilibili.com/video/BV1vm421s7mv?p=19)

### 极限的四则运算法则与拆分前提
- **要点**：同一趋向下若 lim f=A、lim g=B 都存在，则 lim(f±g)=A±B，lim(fg)=AB，lim(f/g)=A/B（B≠0），常数因子可提到极限号外。拆成两个极限时必须拆开后两个都存在（等于确定的数）；其中一个为无穷或来回波动则不能拆，否则会得出「∞−∞=0」这类错误。
- **关键概念**：`四则运算`、`极限存在`、`拆项条件`
- **相互关系**：「加 1 减 1 拆项法」（用于 0/0 型与 1^∞ 型）依赖此前提；不能对 0/0、∞−∞ 等极限不存在的情形直接拆分套用。
- **出处**：[陈哥 P15](https://www.bilibili.com/video/BV1husGzwEtZ?p=15)、[P19](https://www.bilibili.com/video/BV1husGzwEtZ?p=19)、[P26](https://www.bilibili.com/video/BV1husGzwEtZ?p=26)；[杰哥 P12](https://www.bilibili.com/video/BV1Up4y1Y76a?p=12)；[米哥 P13](https://www.bilibili.com/video/BV1swAWerEzS?p=13)；[ok姐 P13](https://www.bilibili.com/video/BV1vm421s7mv?p=13)、[P19](https://www.bilibili.com/video/BV1vm421s7mv?p=19)

### 极限四则运算的存在性规则与拼凑法
- **要点**：存在±存在=存在；存在±不存在=不存在；不存在±不存在=不确定；存在×不存在、存在÷不存在都不确定（本质是 0·∞ 未定式）；但存在÷存在且分母极限非零时商一定存在。反向拼凑：f=½[(f+g)+(f−g)]，g=½[(f+g)−(f−g)]，故由 f+g、f−g 都存在可推出 f、g 的极限都存在。
- **关键概念**：`未定式`、`0·∞`、`四则运算`、`拼凑`
- **相互关系**：所有「不确定」情形都要举反例，反例常取 f=x²、g=1/x。做题先浏览选项，正确选项的成立理由通常很直接。
- **出处**：[斌哥 P83–P86](https://www.bilibili.com/video/BV12DdNYzEvy?p=83)

### 极限的保号性、保序性与反例
- **要点**：保号性：f(x)≥0 可推出极限≥0，但 f(x)>0 推不出极限>0（反例 1/n）。保序性：xₙ&lt;yₙ 且都收敛，只能推出 lim xₙ≤lim yₙ，不能推出严格小于。
- **关键概念**：`保号性`、`保序性`、`反例`
- **相互关系**：套路都是「能否反推」，判断题要用反例。
- **出处**：[斌哥 P78](https://www.bilibili.com/video/BV12DdNYzEvy?p=78)、[P79](https://www.bilibili.com/video/BV12DdNYzEvy?p=79)、[P81](https://www.bilibili.com/video/BV12DdNYzEvy?p=81)

### 计算前的通用准备（定型）
- **要点**：先代入看分子分母各趋于什么（定型）再选方法；定型时非零因子先算出；c/∞=0、c/0=∞（c≠0）。定型不是运算。
- **关键概念**：`先定型后定方法`、`非零因子`
- **出处**：[陈哥 P15](https://www.bilibili.com/video/BV1husGzwEtZ?p=15)、[P23](https://www.bilibili.com/video/BV1husGzwEtZ?p=23)；[杰哥 P13](https://www.bilibili.com/video/BV1Up4y1Y76a?p=13)；[米哥 P28](https://www.bilibili.com/video/BV1swAWerEzS?p=28)

### 极限的解题步骤与化简方法
- **要点**：①定型——代入趋近值判断属于哪种未定式；②化简——约分、通分、因式分解、根式有理化、非零因式代入、等价无穷小；③用公式——主要是洛必达法则。若不是未定式（已定式），直接代入求结果，不要拆也不要化。约分中被约因式是否为零都可以，因为它只是趋于零而非等于零；因式分解常用平方差、立方差；根式有理化借助平方差消去根号。学士帽把顺序固定为四步：带点→化简→等价代换→洛必达；高频代换 tan x~x、sin x~x 及 sec²x−1=tan²x~x²。
- **关键概念**：`定型`、`已定式`、`约分`、`通分`、`平方差`、`立方差`
- **相互关系**：定型是第一步，也是选择后续方法的依据。
- **出处**：[陈哥 P15](https://www.bilibili.com/video/BV1husGzwEtZ?p=15)、[P23](https://www.bilibili.com/video/BV1husGzwEtZ?p=23)、[P26](https://www.bilibili.com/video/BV1husGzwEtZ?p=26)、[P27](https://www.bilibili.com/video/BV1husGzwEtZ?p=27)、[P43](https://www.bilibili.com/video/BV1husGzwEtZ?p=43)；[学士帽 P16](https://www.bilibili.com/video/BV1X4411J792?p=16)、[P46](https://www.bilibili.com/video/BV1X4411J792?p=46)、[P72](https://www.bilibili.com/video/BV1X4411J792?p=72)

### 四则运算典型题型
- **要点**：①代入型——非未定式直接代值；②0/0 型——因式分解后约分，或根式有理化后约分；③∞−∞ 型——通分合并为一个分式，再因式分解约分；④数列型——把通项看作等比（等差）数列前 n 项和，用求和公式化成关于 n 的式子再求极限。
- **关键概念**：`等比数列前 n 项和`、`通分`
- **相互关系**：∞−∞ 的通分常与立方差、因式分解配合使用。
- **出处**：[陈哥 P15](https://www.bilibili.com/video/BV1husGzwEtZ?p=15)

### 有理函数与有理分式函数求极限
- **要点**：①代入法：分母极限不为零时直接代入；②因式分解：分母极限为零时对分子或分母因式分解（平方差、提公因式、十字相乘）约去零因子再代入；③抓大头：x（或 n）趋于无穷时分子分母同除以最高次幂。
- **关键概念**：`有理函数`、`代入法`、`因式分解`、`抓大头`
- **相互关系**：因式分解法与抓大头考察最多，代入法几乎不单独考。
- **出处**：[ok姐 P14](https://www.bilibili.com/video/BV1vm421s7mv?p=14)、[P19](https://www.bilibili.com/video/BV1vm421s7mv?p=19)

### 根式函数与含根式的分式函数求极限
- **要点**：含根式的和差且不能直接代入时，先有理化（用平方差公式去根式，分子分母同乘共轭式），再用代入法、抓大头或等价无穷小。√A−√B 型分子分母同乘 √A+√B。出现 1+2+…+n 先按等差数列求和公式化简成 n 的表达式再求极限。
- **关键概念**：`有理化`、`平方差公式`、`等差数列求和`
- **相互关系**：易错——根式抓大头时最高次幂要算上根号（√(x²) 为一次）；x→−∞ 时把 x 放进根号下需加负号，x→+∞ 才可直接放入；化简后常与「同除以最高次方」配合使用。
- **出处**：[ok姐 P15](https://www.bilibili.com/video/BV1vm421s7mv?p=15)、[P19](https://www.bilibili.com/video/BV1vm421s7mv?p=19)；[斌哥 P141–P143](https://www.bilibili.com/video/BV12DdNYzEvy?p=141)、[P192](https://www.bilibili.com/video/BV12DdNYzEvy?p=192)

### 无穷小与无穷大的定义
- **要点**：以 0 为极限的量就是无穷小量，判断时直接看极限是否为 0：cos0=1、e⁰=1、arcsin1=π/2 都不是无穷小，ln1=0 是；常数 0 是任何极限过程的无穷小量。无穷小不是「很小的数」；无穷大是绝对值趋于无穷的函数（趋于正无穷、负无穷都是无穷大）。
- **关键概念**：`无穷小量`、`无穷大量`、`极限为 0`
- **相互关系**：同一变化过程中，无穷大的倒数是无穷小，无穷小的倒数是无穷大（无穷小的倒数为无穷大仅限 x→0 型）；读题要看清问的是无穷小还是无穷大。
- **出处**：[米哥 P15](https://www.bilibili.com/video/BV1swAWerEzS?p=15)；[学士帽 P18](https://www.bilibili.com/video/BV1X4411J792?p=18)、[P19](https://www.bilibili.com/video/BV1X4411J792?p=19)；[ok姐 P12](https://www.bilibili.com/video/BV1vm421s7mv?p=12)、[P19](https://www.bilibili.com/video/BV1vm421s7mv?p=19)；[斌哥 P93](https://www.bilibili.com/video/BV12DdNYzEvy?p=93)、[P94](https://www.bilibili.com/video/BV12DdNYzEvy?p=94)、[P103](https://www.bilibili.com/video/BV12DdNYzEvy?p=103)

### 无穷小的运算定理
- **要点**：①有限个无穷小的和是无穷小；②有界函数与无穷小的乘积是无穷小（「零乘有界」得零）；③常数与无穷小的乘积是无穷小；④有限个无穷小的乘积是无穷小。学士帽指出 sin∞、cos∞ 无确定极限，但与其它函数相乘时一律视为有界变量。
- **关键概念**：`无穷小`、`有界函数`、`零乘有界`
- **相互关系**：定理②是处理 lim\_\{x→∞\}(sin x)/x 这类题的关键；无穷多项不能逐项抓大头，每项都算得 0 再相加得 0 是错误解法。
- **出处**：[杰哥 P16](https://www.bilibili.com/video/BV1Up4y1Y76a?p=16)；[学士帽 P18](https://www.bilibili.com/video/BV1X4411J792?p=18)、[P19](https://www.bilibili.com/video/BV1X4411J792?p=19)；[ok姐 P13](https://www.bilibili.com/video/BV1vm421s7mv?p=13)、[P19](https://www.bilibili.com/video/BV1vm421s7mv?p=19)；[斌哥 P154](https://www.bilibili.com/video/BV12DdNYzEvy?p=154)、[P160](https://www.bilibili.com/video/BV12DdNYzEvy?p=160)

### 无穷小比较的四个层级
- **要点**：设 α、β 都是无穷小，看 α/β 的极限：为 0 则 α 是 β 的高阶无穷小（记 f=o(g)）；为非零常数则同阶；为 1 则等价（记 α~β）；为 ∞ 则低阶。同阶但不等于 1 时不等价（如 ½x² 与 −½x²）。lim α/β^k=c≠0 称 α 是 β 的 k 阶无穷小。学士帽指出阶的本质是无穷小量趋于零的速度，同类型函数（如幂函数）直接看指数大小即可比阶。
- **关键概念**：`高阶无穷小`、`同阶无穷小`、`等价无穷小`、`低阶无穷小`
- **相互关系**：文字表述与极限式要会互译——「f 是 g 的高阶无穷小」与「lim f/g=0」是同一句话。若 f 是 g 的高阶无穷小，则 (f−g)/g→0−1=−1，故 f−g 与 g 是同阶（不是等价）无穷小，不要把 0−1 误算成 1。
- **出处**：[陈哥 P19](https://www.bilibili.com/video/BV1husGzwEtZ?p=19)、[P23](https://www.bilibili.com/video/BV1husGzwEtZ?p=23)、[P26](https://www.bilibili.com/video/BV1husGzwEtZ?p=26)；[米哥 P16](https://www.bilibili.com/video/BV1swAWerEzS?p=16)；[学士帽 P20](https://www.bilibili.com/video/BV1X4411J792?p=20)；[ok姐 P18](https://www.bilibili.com/video/BV1vm421s7mv?p=18)；[斌哥 P107](https://www.bilibili.com/video/BV12DdNYzEvy?p=107)、[P111](https://www.bilibili.com/video/BV12DdNYzEvy?p=111)、[P112](https://www.bilibili.com/video/BV12DdNYzEvy?p=112)、[P118](https://www.bilibili.com/video/BV12DdNYzEvy?p=118)、[P122](https://www.bilibili.com/video/BV12DdNYzEvy?p=122)、[P124](https://www.bilibili.com/video/BV12DdNYzEvy?p=124)

### 由等价公式定阶与求导降阶
- **要点**：把每个无穷小替换成与它等价的 xᵏ，比较次数即可定阶、比阶（比 sin x 低阶就找次数小于 1 的，如 √x 是 x\^\{1/2\}）。xᵐ 开 n 次方等于 x\^\{m/n\}，是化次数的常用手段。若 f(x) 是 n 阶无穷小，则 f′(x) 是 n−1 阶无穷小，可由导数的阶反推原函数的阶。
- **关键概念**：`阶`、`次数`、`求导降阶`
- **相互关系**：求导降阶与定义法（直接做商求极限）互为替代方法，后者更严谨。
- **出处**：[斌哥 P106](https://www.bilibili.com/video/BV12DdNYzEvy?p=106)、[P107](https://www.bilibili.com/video/BV12DdNYzEvy?p=107)、[P109](https://www.bilibili.com/video/BV12DdNYzEvy?p=109)、[P111](https://www.bilibili.com/video/BV12DdNYzEvy?p=111)、[P112](https://www.bilibili.com/video/BV12DdNYzEvy?p=112)、[P121](https://www.bilibili.com/video/BV12DdNYzEvy?p=121)、[P123](https://www.bilibili.com/video/BV12DdNYzEvy?p=123)

### 由阶的关系求参数
- **要点**：设等价或同阶条件，把两边都化成 x 的幂，令次数相等（等价时还须令系数相等）列方程求参数。等价要求系数比为 1，同阶只要求为非零常数。
- **关键概念**：`待定参数`、`次数相等`、`系数相等`
- **相互关系**：这是无穷小比阶参数题的统一套路。
- **出处**：[斌哥 P110](https://www.bilibili.com/video/BV12DdNYzEvy?p=110)、[P112–P114](https://www.bilibili.com/video/BV12DdNYzEvy?p=112)、[P119](https://www.bilibili.com/video/BV12DdNYzEvy?p=119)、[P123](https://www.bilibili.com/video/BV12DdNYzEvy?p=123)、[P134–P137](https://www.bilibili.com/video/BV12DdNYzEvy?p=134)

### 常用等价无穷小清单
- **要点**：一阶：sin x~x，tan x~x，arcsin x~x，arctan x~x，ln(1+x)~x，eˣ−1~x，1−cos x~½x²（即 cos□−1~−½□²），(1+x)^α−1~αx，√(1+□)−1~½□，a^x−1~x ln a。二阶：x−ln(1+x)~½x²，ln(1+x)−x~−½x²。三阶：x−sin x~⅙x³，tan x−x~⅓x³，x−tan x~−⅓x³，arctan x−x~−⅓x³，arcsin x−x~⅙x³，tan x−sin x~½x³，arcsin x−arctan x~½x³。反向：1−e^□~−□。
- **关键概念**：`等价无穷小`、`阶`、`方框`
- **相互关系**：所有公式都要求方框趋于 0，两项交换顺序等价结果变号——ln(1+□)−□~−½□² 就是 □−ln(1+□)~½□² 加负号；带「−1」的都源于 (1+ax)^b−1；等价无穷小由麦克劳林展开式截断高阶项得到。
- **出处**：[陈哥 P20](https://www.bilibili.com/video/BV1husGzwEtZ?p=20)、[P23](https://www.bilibili.com/video/BV1husGzwEtZ?p=23)、[P26–P29](https://www.bilibili.com/video/BV1husGzwEtZ?p=26)；[杰哥 P15](https://www.bilibili.com/video/BV1Up4y1Y76a?p=15)；[米哥 P17](https://www.bilibili.com/video/BV1swAWerEzS?p=17)、[P18](https://www.bilibili.com/video/BV1swAWerEzS?p=18)；[学士帽 P21](https://www.bilibili.com/video/BV1X4411J792?p=21)、[P68](https://www.bilibili.com/video/BV1X4411J792?p=68)；[ok姐 P18](https://www.bilibili.com/video/BV1vm421s7mv?p=18)、[P19](https://www.bilibili.com/video/BV1vm421s7mv?p=19)；[斌哥 P109–P111](https://www.bilibili.com/video/BV12DdNYzEvy?p=109)、[P113](https://www.bilibili.com/video/BV12DdNYzEvy?p=113)、[P115](https://www.bilibili.com/video/BV12DdNYzEvy?p=115)、[P119](https://www.bilibili.com/video/BV12DdNYzEvy?p=119)、[P123](https://www.bilibili.com/video/BV12DdNYzEvy?p=123)、[P143](https://www.bilibili.com/video/BV12DdNYzEvy?p=143)、[P146–P149](https://www.bilibili.com/video/BV12DdNYzEvy?p=146)、[P165](https://www.bilibili.com/video/BV12DdNYzEvy?p=165)、[P180–P182](https://www.bilibili.com/video/BV12DdNYzEvy?p=180)、[P185](https://www.bilibili.com/video/BV12DdNYzEvy?p=185)、[P195](https://www.bilibili.com/video/BV12DdNYzEvy?p=195)

### 等价无穷小替换的适用条件
- **要点**：本质是把复杂因式替换成与之趋于零速度相同的简单因式。两个前提：①被等价的部分必须与其它因式构成乘除关系，不能是加减关系；②被等价出来的整体必须趋近于零（看内层表达式是否趋于 0，与外面趋于多少无关）。x→∞ 时 x·sin(π/x) 中方框趋于 0 可用等价；但 x→0 时 sin(1/x) 的方框趋于无穷，不能用等价。学士帽另给构造法：加减关系中先提公因式构造成乘积再代换，如 tan x−sin x=tan x(1−cos x)。
- **关键概念**：`等价无穷小替换`、`方框趋于零`、`内层`、`乘积关系`
- **相互关系**：不能用等价时改用「无穷小×有界=0」或「无穷大分之有界=0」；遇到加减关系需先拆项或先做变形（如 e^x−1+sin x 中两者相加，不能单独把 e^x−1 换成 x）。
- **出处**：[陈哥 P20](https://www.bilibili.com/video/BV1husGzwEtZ?p=20)、[P21](https://www.bilibili.com/video/BV1husGzwEtZ?p=21)、[P25](https://www.bilibili.com/video/BV1husGzwEtZ?p=25)、[P26](https://www.bilibili.com/video/BV1husGzwEtZ?p=26)；[杰哥 P15](https://www.bilibili.com/video/BV1Up4y1Y76a?p=15)、[P19](https://www.bilibili.com/video/BV1Up4y1Y76a?p=19)、[P21](https://www.bilibili.com/video/BV1Up4y1Y76a?p=21)、[P23](https://www.bilibili.com/video/BV1Up4y1Y76a?p=23)、[P39](https://www.bilibili.com/video/BV1Up4y1Y76a?p=39)；[米哥 P17](https://www.bilibili.com/video/BV1swAWerEzS?p=17)、[P18](https://www.bilibili.com/video/BV1swAWerEzS?p=18)；[学士帽 P21](https://www.bilibili.com/video/BV1X4411J792?p=21)、[P68](https://www.bilibili.com/video/BV1X4411J792?p=68)；[ok姐 P18](https://www.bilibili.com/video/BV1vm421s7mv?p=18)、[P19](https://www.bilibili.com/video/BV1vm421s7mv?p=19)；[斌哥 P92](https://www.bilibili.com/video/BV12DdNYzEvy?p=92)、[P95](https://www.bilibili.com/video/BV12DdNYzEvy?p=95)、[P96](https://www.bilibili.com/video/BV12DdNYzEvy?p=96)、[P105](https://www.bilibili.com/video/BV12DdNYzEvy?p=105)、[P106](https://www.bilibili.com/video/BV12DdNYzEvy?p=106)

### 使用等价无穷小的两个误区
- **要点**：误区一：认为只有 x→0 才能等价。错——x→1 时 sin(x−1)~x−1、x→∞ 时 sin(1/x)~1/x、x→2 时 sin(x²−4)~x²−4。误区二：认为等价随时可用。错——若被等价因式之间是加减关系则不能等价，如求 lim\_\{x→0\}(tan x−sin x)/x³ 时不能把 tan x、sin x 都换成 x（会得 0），应改用 tan x−sin x~x³/2 得 1/2。
- **关键概念**：`误区`、`加减关系不能等价`、`ln a−ln b=ln(a/b)`
- **相互关系**：把两个对数相减化为真数相除、再对 ln(1+□) 做广义化等价，是常见套路。
- **出处**：[陈哥 P21](https://www.bilibili.com/video/BV1husGzwEtZ?p=21)

### 等价无穷小的广义化
- **要点**：把公式中的 x 整体换成任一「方框」（sin x、x²−4、1/x），只要该方框在给定趋向下趋于零，就有相应的等价关系。
- **关键概念**：`广义化`、`整体代换`、`方框趋于零`
- **相互关系**：这是等价无穷小最常用的形式，考试多在此之上做文章。
- **出处**：[陈哥 P20–P23](https://www.bilibili.com/video/BV1husGzwEtZ?p=20)、[P27](https://www.bilibili.com/video/BV1husGzwEtZ?p=27)

### 加减法不能用等价替换（易错）
- **要点**：等价替换只在乘除结构中安全；出现在加减法中直接替换会出错。应拆成两个极限分别算，或改用洛必达。
- **关键概念**：`加减法不可等价`、`拆项`
- **相互关系**：典型错误是把 x−sin3x 中的 sin3x 直接换成 3x 后与前面的 x 相减。
- **出处**：[斌哥 P190](https://www.bilibili.com/video/BV12DdNYzEvy?p=190)

### 非零因子先算，非因子不可先算
- **要点**：只用于 0/0 型。若某因式代入趋近值后不为零，且它与其余（零）因式构成乘积关系，就可先把它的极限值算出来提到极限外；处于加减法中的项不是因子，不能先代入。常见形态：1+cos x 在 x→0 时趋于 2；e\^\{sin x\}、1+sin x、cos x 在 x→0 时趋于 1；根式有理化后出现的「两个根式之和」在 x→0 时趋于 2。典型错误是在 sin x−x cos x 中先把 cos x 算成 1。
- **关键概念**：`非零因子`、`乘积因子`、`加减项`
- **相互关系**：常与「有理化后提出常数括号」等技巧配合。
- **出处**：[陈哥 P22](https://www.bilibili.com/video/BV1husGzwEtZ?p=22)、[P23](https://www.bilibili.com/video/BV1husGzwEtZ?p=23)、[P26](https://www.bilibili.com/video/BV1husGzwEtZ?p=26)、[P28](https://www.bilibili.com/video/BV1husGzwEtZ?p=28)；[杰哥 P13](https://www.bilibili.com/video/BV1Up4y1Y76a?p=13)；[米哥 P28](https://www.bilibili.com/video/BV1swAWerEzS?p=28)、[P29](https://www.bilibili.com/video/BV1swAWerEzS?p=29)；[斌哥 P66](https://www.bilibili.com/video/BV12DdNYzEvy?p=66)、[P91](https://www.bilibili.com/video/BV12DdNYzEvy?p=91)、[P95–P99](https://www.bilibili.com/video/BV12DdNYzEvy?p=95)、[P104](https://www.bilibili.com/video/BV12DdNYzEvy?p=104)、[P115](https://www.bilibili.com/video/BV12DdNYzEvy?p=115)、[P124](https://www.bilibili.com/video/BV12DdNYzEvy?p=124)、[P173](https://www.bilibili.com/video/BV12DdNYzEvy?p=173)、[P178](https://www.bilibili.com/video/BV12DdNYzEvy?p=178)、[P188](https://www.bilibili.com/video/BV12DdNYzEvy?p=188)、[P189](https://www.bilibili.com/video/BV12DdNYzEvy?p=189)、[P192](https://www.bilibili.com/video/BV12DdNYzEvy?p=192)

### 反向使用等价技巧
- **要点**：见「方框 −1」可反向写成 ln(方框)，用对数法则把乘积拆成和再逐个等价。
- **关键概念**：`反向等价`
- **出处**：[米哥 P31](https://www.bilibili.com/video/BV1swAWerEzS?p=31)

### 等价无穷小的坐标法（米格公式一）
- **要点**：按 x→0 时大小排坐标轴、相邻间距固定，求 A−B 等价时判正负后数格乘间距；第一组（间距 ½x²）ln(1+x)→x→eˣ−1，第二组（间距 ⅙x³）arctan x→sin x→x→tan x。
- **关键概念**：`米格公式一`
- **出处**：[米哥 P28–P31](https://www.bilibili.com/video/BV1swAWerEzS?p=28)

### 抓大头与抓小头
- **要点**：x→∞ 抓最高次项（抓大头），常数项可划掉；x→0 抓最低次项（抓小头），xᵐ+xⁿ~x^min(m,n)，如 4x³−3x²+2x 在 x→0 时等价于 2x。分子分母均为多项式时口诀「上大无穷、下大零、相同则为系数比」；分子分母均为指数函数时找最大底数再用同一口诀；若指数不相同（如 5\^\{n+1\} 与 5^n），须先化成相同指数再比系数。含根号或括号时先把低于最高次方的项全部去掉再抓。量级上 x→+∞ 时指数函数≫幂函数≫对数函数；x±sin x 舍有界量。
- **关键概念**：`抓大头`、`抓小头`、`量级`、`同除以最高次方`
- **相互关系**：由「极限等于非零常数」可反推最高次项次数必须相同，从而求参数；选填可直接抓大头，计算题必须写成「分子分母同除以最高次方」再逐项取极限，往根号里放因子时要补平方。
- **出处**：[陈哥 P27](https://www.bilibili.com/video/BV1husGzwEtZ?p=27)；[米哥 P19](https://www.bilibili.com/video/BV1swAWerEzS?p=19)、[P29](https://www.bilibili.com/video/BV1swAWerEzS?p=29)；[学士帽 P14](https://www.bilibili.com/video/BV1X4411J792?p=14)、[P72](https://www.bilibili.com/video/BV1X4411J792?p=72)、[P88](https://www.bilibili.com/video/BV1X4411J792?p=88)；[ok姐 P14](https://www.bilibili.com/video/BV1vm421s7mv?p=14)、[P19](https://www.bilibili.com/video/BV1vm421s7mv?p=19)、[P20](https://www.bilibili.com/video/BV1vm421s7mv?p=20)；[斌哥 P108](https://www.bilibili.com/video/BV12DdNYzEvy?p=108)、[P114](https://www.bilibili.com/video/BV12DdNYzEvy?p=114)、[P132–P137](https://www.bilibili.com/video/BV12DdNYzEvy?p=132)、[P139–P143](https://www.bilibili.com/video/BV12DdNYzEvy?p=139)、[P153](https://www.bilibili.com/video/BV12DdNYzEvy?p=153)、[P161](https://www.bilibili.com/video/BV12DdNYzEvy?p=161)、[P182](https://www.bilibili.com/video/BV12DdNYzEvy?p=182)、[P200](https://www.bilibili.com/video/BV12DdNYzEvy?p=200)

### 洛必达法则
- **要点**：仅当极限类型为 0/0 或 ∞/∞ 时可用；分子分母在变量趋向值的去心邻域内可导。使用时对分子分母同时求导，每次求导后重新定型，若仍是这两种未定式可继续求导。分母趋于零而分子为常数时结果直接为 ∞；分子为零而分母为非零常数时结果直接为 0。课本只讲 0/0 与 ∞/∞ 型可用，实际上只要分母趋于无穷，分子是什么类型都可用洛必达。原则「有等价先等价，能化简先化简，万事不对洛必达」。后验：结果须为零、常数或无穷，震荡则不能用。
- **关键概念**：`洛必达法则`、`同时求导`、`每次求导后定型`、`去心邻域内可导`、`后验条件`
- **相互关系**：求导过程中若出现可等价的形式，应及时做等价替换以简化运算；使用前必须先代入判别类型，若是非未定式，绝不能用洛必达（x→2 时分子分母都非零，直接代入即可，用洛必达会得到错解）。
- **出处**：[陈哥 P25](https://www.bilibili.com/video/BV1husGzwEtZ?p=25)、[P27](https://www.bilibili.com/video/BV1husGzwEtZ?p=27)、[P43](https://www.bilibili.com/video/BV1husGzwEtZ?p=43)；[杰哥 P17](https://www.bilibili.com/video/BV1Up4y1Y76a?p=17)；[米哥 P20](https://www.bilibili.com/video/BV1swAWerEzS?p=20)、[P28](https://www.bilibili.com/video/BV1swAWerEzS?p=28)；[学士帽 P46](https://www.bilibili.com/video/BV1X4411J792?p=46)、[P72](https://www.bilibili.com/video/BV1X4411J792?p=72)；[ok姐 P20](https://www.bilibili.com/video/BV1vm421s7mv?p=20)、[P37](https://www.bilibili.com/video/BV1vm421s7mv?p=37)；[斌哥 P116](https://www.bilibili.com/video/BV12DdNYzEvy?p=116)、[P121](https://www.bilibili.com/video/BV12DdNYzEvy?p=121)、[P125–P131](https://www.bilibili.com/video/BV12DdNYzEvy?p=125)、[P138](https://www.bilibili.com/video/BV12DdNYzEvy?p=138)、[P169](https://www.bilibili.com/video/BV12DdNYzEvy?p=169)

### 洛必达失效
- **要点**：形如 (x+sin x)/(x−cos x) 的 ∞/∞ 型，求导后分子分母出现 cos x、sin x 这类有界振荡项，无法定出结果，此时洛必达失效。正确做法是抓大头（忽略有界项，只留 x）或分子分母同除 x，用「零乘有界」得结果 1。
- **关键概念**：`洛必达失效`、`抓大头`、`零乘有界`
- **相互关系**：识别信号是分子分母中夹带 sin、cos 等有界项；此类题一般只出现在选择、判断中。
- **出处**：[陈哥 P25](https://www.bilibili.com/video/BV1husGzwEtZ?p=25)、[P27](https://www.bilibili.com/video/BV1husGzwEtZ?p=27)

### 七种未定式
- **要点**：0/0、∞/∞、∞−∞、0·∞、1^∞、∞⁰、0⁰ 共七种。核心是前两种，其余五种都能通过通分、有理化、取倒数下放、指数对数化化为 0/0 或 ∞/∞。每种都有对应解法，不能想当然，如 0/0≠1、∞−∞≠0、0·∞≠0。
- **关键概念**：`未定式`、`抓大头`、`洛必达法则`、`万能公式`
- **相互关系**：第一重要极限对应 0/0 型，第二重要极限对应 1^∞ 型。
- **出处**：[陈哥 P15](https://www.bilibili.com/video/BV1husGzwEtZ?p=15)、[P17](https://www.bilibili.com/video/BV1husGzwEtZ?p=17)、[P23](https://www.bilibili.com/video/BV1husGzwEtZ?p=23)、[P26](https://www.bilibili.com/video/BV1husGzwEtZ?p=26)、[P27](https://www.bilibili.com/video/BV1husGzwEtZ?p=27)、[P28](https://www.bilibili.com/video/BV1husGzwEtZ?p=28)；[杰哥 P21](https://www.bilibili.com/video/BV1Up4y1Y76a?p=21)、[P23](https://www.bilibili.com/video/BV1Up4y1Y76a?p=23)；[米哥 P28](https://www.bilibili.com/video/BV1swAWerEzS?p=28)；[ok姐 P20](https://www.bilibili.com/video/BV1vm421s7mv?p=20)、[P37](https://www.bilibili.com/video/BV1vm421s7mv?p=37)

### 0/0 型的处理方法与套路
- **要点**：可用约分（因式分解）、非零因子代入、根式有理化、等价无穷小、洛必达、抓大头（x→0 时低次项是大头）、恒等变形、米格公式一。典型套路：分式约分后直接代值；分子含 e\^\{f(x)\}−e\^\{g(x)\} 时提出一个 e\^\{g(x)\} 再用广义等价；根式相减时乘共轭式有理化；分子为两项之和时加 1 减 1 拆成两个极限；ln cos x 型写成 ln(1+(cos x−1))，等价为 cos x−1，再用 1−cos x~x²/2 得 −1/2；「+1−1」造可等价结构。学士帽补充：已知极限值为常数求参数时，若分母趋于零则分子也必趋于零（否则结果为 ∞，与条件矛盾）。
- **关键概念**：`因式分解`、`提公因子`、`根式有理化`、`加1减1`、`拆项`
- **相互关系**：能用等价替换或约分就优先用，直接多次洛必达通常最繁琐；这些套路均以等价无穷小与非零因子代入为工具。
- **出处**：[陈哥 P22](https://www.bilibili.com/video/BV1husGzwEtZ?p=22)、[P23](https://www.bilibili.com/video/BV1husGzwEtZ?p=23)、[P26](https://www.bilibili.com/video/BV1husGzwEtZ?p=26)；[米哥 P29](https://www.bilibili.com/video/BV1swAWerEzS?p=29)；[学士帽 P22](https://www.bilibili.com/video/BV1X4411J792?p=22)；[斌哥 P168](https://www.bilibili.com/video/BV12DdNYzEvy?p=168)、[P174](https://www.bilibili.com/video/BV12DdNYzEvy?p=174)、[P183](https://www.bilibili.com/video/BV12DdNYzEvy?p=183)、[P186](https://www.bilibili.com/video/BV12DdNYzEvy?p=186)、[P194](https://www.bilibili.com/video/BV12DdNYzEvy?p=194)

### ∞/∞ 型的三种处理方法
- **要点**：（1）有理化——出现根式相减时乘共轭式；（2）抓大头；（3）洛必达法则。实际以有理化与抓大头最常用，洛必达相对少用。
- **关键概念**：`有理化`、`抓大头`、`洛必达法则`
- **相互关系**：与 0/0 型并列为核心类型，是其余五种未定式的转化目标。
- **出处**：[陈哥 P27](https://www.bilibili.com/video/BV1husGzwEtZ?p=27)；[学士帽 P46](https://www.bilibili.com/video/BV1X4411J792?p=46)、[P72](https://www.bilibili.com/video/BV1X4411J792?p=72)

### ∞−∞ 型极限
- **要点**：（1）含分式→通分化为 0/0（最常考，两个分式相减且各自趋于无穷时第一步统一分母）；（2）含根式→根式有理化化为 ∞/∞；（3）倒代换（令 t=1/x）；（4）负代换（x 趋于负无穷时令 x=−t）。前两种是考试重点，后两种频率很低。变形技巧：通分后分子出现平方差时用平方差公式分解；通分后分子常出现 □−ln(1+□) 的结构，可直接用等价公式；根式有理化后用「去掉低于最高次方的项」快速求极限；x²[x−ln(1+1/x)] 型可在括号外提 x²，再对整体用 u−ln(1+u)~u²/2。约分时注意 1−x 与 x−1 相差一个负号。加减中不可对 sin x 单独等价，须先通分后对整体等价。
- **关键概念**：`通分`、`根式有理化`、`倒代换`、`负代换`、`提最高次幂`
- **相互关系**：本章出现频率最高的一类计算题；通分后常配合平方差公式与等价无穷小。
- **出处**：[陈哥 P27](https://www.bilibili.com/video/BV1husGzwEtZ?p=27)、[P43](https://www.bilibili.com/video/BV1husGzwEtZ?p=43)；[杰哥 P19](https://www.bilibili.com/video/BV1Up4y1Y76a?p=19)；[米哥 P21](https://www.bilibili.com/video/BV1swAWerEzS?p=21)、[P22](https://www.bilibili.com/video/BV1swAWerEzS?p=22)、[P30](https://www.bilibili.com/video/BV1swAWerEzS?p=30)；[学士帽 P22](https://www.bilibili.com/video/BV1X4411J792?p=22)、[P46](https://www.bilibili.com/video/BV1X4411J792?p=46)、[P72](https://www.bilibili.com/video/BV1X4411J792?p=72)；[斌哥 P144–P151](https://www.bilibili.com/video/BV12DdNYzEvy?p=144)

### 0·∞ 型极限
- **要点**：基本方法是取倒数下放——把其中一个因式写成倒数的分母形式，化为 ∞/∞ 或 0/0，再用抓大头或洛必达；下放到分母的对象不同，决定化成 ∞/∞ 还是 0/0；下放求导简单的函数，遇 tan、cot 先化为 sin/cos。结果不确定（可为 0、常数或无穷），取决于零与无穷的快慢。结论：幂函数乘对数函数（幂函数部分趋于零）极限必为 0，如 x ln x（x→0⁺）。灵活变形：（1）含 tan x 的式子可直接写成 sin x/cos x，先用非零因子代入（sin(π/2)=1）再洛必达；（2）两个对数相减时先合并为真数相除 ln(a/b)，再用 ln(1+整体)~整体 化简。
- **关键概念**：`取倒数下放`、`切化弦`、`对数真数相除`、`非零因子代入`
- **相互关系**：转化后仍需重新定型，再决定用洛必达、等价无穷小还是抓大头。
- **出处**：[陈哥 P27](https://www.bilibili.com/video/BV1husGzwEtZ?p=27)、[P43](https://www.bilibili.com/video/BV1husGzwEtZ?p=43)；[杰哥 P18](https://www.bilibili.com/video/BV1Up4y1Y76a?p=18)；[米哥 P21](https://www.bilibili.com/video/BV1swAWerEzS?p=21)、[P22](https://www.bilibili.com/video/BV1swAWerEzS?p=22)、[P30](https://www.bilibili.com/video/BV1swAWerEzS?p=30)；[学士帽 P46](https://www.bilibili.com/video/BV1X4411J792?p=46)、[P72](https://www.bilibili.com/video/BV1X4411J792?p=72)；[斌哥 P197](https://www.bilibili.com/video/BV12DdNYzEvy?p=197)、[P198](https://www.bilibili.com/video/BV12DdNYzEvy?p=198)、[P200](https://www.bilibili.com/video/BV12DdNYzEvy?p=200)

### 幂指函数改写 u^v=e\^\{v ln u\}
- **要点**：见到 u^v 形式的幂指函数，一律先改写成 e\^\{v ln u\}，之后只需求指数部分的极限，最后把结果放回 e 的指数上。依据是 ln a^b=b ln a 与 e\^\{ln x\}=x。学士帽指出通项为幂指型时同样先化为整体幂的形式再求极限；若算得极限为 e\^\{−1\} 等非零值，则对应级数发散。
- **关键概念**：`幂指函数`、`u^v=e^{v ln u}`、`指数对数化`
- **相互关系**：是 0·∞、∞⁰、0⁰ 与部分 1^∞ 问题的统一入口；转化后必成 0·∞ 型，再用简单因子下放。
- **出处**：[陈哥 P28](https://www.bilibili.com/video/BV1husGzwEtZ?p=28)、[P43](https://www.bilibili.com/video/BV1husGzwEtZ?p=43)；[杰哥 P20](https://www.bilibili.com/video/BV1Up4y1Y76a?p=20)、[P21](https://www.bilibili.com/video/BV1Up4y1Y76a?p=21)；[米哥 P24](https://www.bilibili.com/video/BV1swAWerEzS?p=24)、[P25](https://www.bilibili.com/video/BV1swAWerEzS?p=25)、[P31](https://www.bilibili.com/video/BV1swAWerEzS?p=31)；[学士帽 P47](https://www.bilibili.com/video/BV1X4411J792?p=47)、[P72](https://www.bilibili.com/video/BV1X4411J792?p=72)、[P88](https://www.bilibili.com/video/BV1X4411J792?p=88)；[斌哥 P154](https://www.bilibili.com/video/BV12DdNYzEvy?p=154)、[P195](https://www.bilibili.com/video/BV12DdNYzEvy?p=195)、[P197](https://www.bilibili.com/video/BV12DdNYzEvy?p=197)

### ∞⁰ 型与 0⁰ 型
- **要点**：底数趋于无穷、指数趋于零（∞⁰），或底数趋于零、指数趋于零（0⁰），绝不能套 1^∞ 公式；改写为 e\^\{v ln u\} 后，把 ln 放到分子做成 ∞/∞ 或 0·∞ 再洛必达。考试出现频率很低，不是侧重点。
- **关键概念**：`∞⁰ 型`、`0⁰ 型`、`洛必达法则`
- **相互关系**：与 1^∞ 型的辨析点——先判别类型再选公式，不能见幂指函数就套 1^∞ 公式。
- **出处**：[陈哥 P28](https://www.bilibili.com/video/BV1husGzwEtZ?p=28)、[P43](https://www.bilibili.com/video/BV1husGzwEtZ?p=43)；[杰哥 P20](https://www.bilibili.com/video/BV1Up4y1Y76a?p=20)、[P21](https://www.bilibili.com/video/BV1Up4y1Y76a?p=21)；[斌哥 P154](https://www.bilibili.com/video/BV12DdNYzEvy?p=154)

### 1^∞ 型万能公式
- **要点**：底数极限为 1、指数极限为无穷即 1^∞ 型。1^∞ 型必可化为 (1+A)^B，且 lim(1+A)^B=e\^\{lim A·B\}，其中 A→0、B→∞，A、B 均为函数而非数；直接套 u^v=e\^\{((u−1)v)\}，即「底数减一，再乘指数」，写成 e\^\{lim (u−1)v\} 后求指数部分的极限。此公式可解决所有 1^∞ 型极限。若括号内不是 1+A，需加 1 减 1 构造，再通分合并出 A；若指数部分极限不是常数，需单独再求一次（常用抓大头）。学士帽凑形技巧：括号内没有「1」时用分子构造分母（如 x+1=x−1+2）造出 1+无穷小，再在指数上乘无穷小的倒数并乘回原指数以保持恒等。
- **关键概念**：`1^∞ 型`、`u^v=e^{((u−1)v)}`、`底数减一`、`加1减1`
- **相互关系**：与第二重要极限同源，比「配倒数关系」简便，可完全替代之；真题多不直接给出 1+A 形式。
- **出处**：[陈哥 P17](https://www.bilibili.com/video/BV1husGzwEtZ?p=17)、[P28](https://www.bilibili.com/video/BV1husGzwEtZ?p=28)；[杰哥 P20](https://www.bilibili.com/video/BV1Up4y1Y76a?p=20)、[P21](https://www.bilibili.com/video/BV1Up4y1Y76a?p=21)；[学士帽 P17](https://www.bilibili.com/video/BV1X4411J792?p=17)；[米哥 P23](https://www.bilibili.com/video/BV1swAWerEzS?p=23)；[ok姐 P17](https://www.bilibili.com/video/BV1vm421s7mv?p=17)、[P19](https://www.bilibili.com/video/BV1vm421s7mv?p=19)；[斌哥 P153](https://www.bilibili.com/video/BV12DdNYzEvy?p=153)、[P155–P157](https://www.bilibili.com/video/BV12DdNYzEvy?p=155)、[P163](https://www.bilibili.com/video/BV12DdNYzEvy?p=163)、[P164](https://www.bilibili.com/video/BV12DdNYzEvy?p=164)

### 1^∞ 型底数减一的化简
- **要点**：底数为分式时 u−1 要先通分；通分后通常化成「常数÷分母」，可与指数中的无穷因子约分。
- **关键概念**：`通分`、`约分`
- **相互关系**：与「抓大头」配合——约分后剩下的无穷比无穷直接看最高次项。
- **出处**：[斌哥 P156](https://www.bilibili.com/video/BV12DdNYzEvy?p=156)、[P161](https://www.bilibili.com/video/BV12DdNYzEvy?p=161)、[P165](https://www.bilibili.com/video/BV12DdNYzEvy?p=165)

### 1^∞ 型公式的适用条件（易错）
- **要点**：只有确为 1^∞ 型才能套公式。若底数极限是 2 等常数，直接代入即可；∞⁰ 型也不是 1^∞，必须改用 u^v=e\^\{v ln u\}。
- **关键概念**：`1^∞ 型`、`∞⁰ 型`、`直接代入`
- **相互关系**：典型陷阱——先判别类型再选公式。
- **出处**：[斌哥 P154](https://www.bilibili.com/video/BV12DdNYzEvy?p=154)

### 1^∞ 型已知极限值反求参数
- **要点**：先用公式把原式化为含参的 e\^\{g(a)\}，与已知值相等后两边取对数解出参数。遇到 ln4 先用 ln b^a=a ln b 化成 2ln2 再约分。用到 ln e^C=C、ln 1=0 等性质。
- **关键概念**：`两边取对数`、`a ln b = ln b^a`
- **出处**：[陈哥 P28](https://www.bilibili.com/video/BV1husGzwEtZ?p=28)；[斌哥 P158–P161](https://www.bilibili.com/video/BV12DdNYzEvy?p=158)

### 第一重要极限及其广义化
- **要点**：lim\_\{x→0\} sin x/x=1（0/0 型）。三要素：x 趋于 0、分子为 sin（某表达式）、分母与 sin 内是同一表达式、结果为 1。广义化：只要某趋向下 f(x)→0，就有 sin f(x)/f(x)→1——被 sin 作用的部分与分母必须形式完全一致；不一致时在分子或分母上乘、除以凑齐，再在整体外补偿。此时也可写作 sin f(x)~f(x)。
- **关键概念**：`第一重要极限`、`sin x/x`、`广义化`、`配凑`
- **相互关系**：与等价无穷小 sin x~x 是同一事实；配合降幂公式可求 (1−cos x)/x²。易错——务必与 lim\_\{x→∞\}(sin x)/x=0（无穷小×有界）区分。
- **出处**：[陈哥 P17](https://www.bilibili.com/video/BV1husGzwEtZ?p=17)；[学士帽 P17](https://www.bilibili.com/video/BV1X4411J792?p=17)；[米哥 P23](https://www.bilibili.com/video/BV1swAWerEzS?p=23)；[ok姐 P16](https://www.bilibili.com/video/BV1vm421s7mv?p=16)、[P19](https://www.bilibili.com/video/BV1vm421s7mv?p=19)

### 第二重要极限及其广义化
- **要点**：lim\_\{x→0\}(1+x)\^\{1/x\}=e，lim\_\{x→∞\}(1+1/x)^x=e。两个关键点：①类型一定是 1^∞；②括号内「加的项」与指数互为倒数。广义化：若 f(x)→0 则 lim(1+f(x))\^\{1/f(x)\}=e；若 f(x)→∞ 则 lim(1+1/f(x))\^\{f(x)\}=e。须拼成固定形式：括号内 1+狗、指数狗分之一、互为倒数。原式没有「1+」时先通分或拆项凑出来。
- **关键概念**：`第二重要极限`、`1^∞`、`互为倒数`、`配凑`
- **相互关系**：对应七种未定式中的 1^∞ 型，考查频率很高；配凑后常需用幂指函数极限法则与抓大头求出剩余指数部分的极限。
- **出处**：[陈哥 P17](https://www.bilibili.com/video/BV1husGzwEtZ?p=17)；[学士帽 P17](https://www.bilibili.com/video/BV1X4411J792?p=17)；[米哥 P23](https://www.bilibili.com/video/BV1swAWerEzS?p=23)；[ok姐 P17](https://www.bilibili.com/video/BV1vm421s7mv?p=17)、[P19](https://www.bilibili.com/video/BV1vm421s7mv?p=19)

### 幂指函数的极限（A^B 法则）
- **要点**：对 u(x)\^\{v(x)\}，若底数极限为 A（A>0）、指数极限为 B，则极限为 A^B。底数与指数都是关于 x 的函数时称幂指函数，既非幂函数也非指数函数的复合。
- **关键概念**：`幂指函数`、`A^B`
- **相互关系**：第二重要极限配凑出的 e 部分与其剩余指数部分结合时即用此法则。
- **出处**：[ok姐 P17](https://www.bilibili.com/video/BV1vm421s7mv?p=17)、[P19](https://www.bilibili.com/video/BV1vm421s7mv?p=19)

### 幂指函数极限例题套路
- **要点**：先定型再套公式；底数含分式先用抓大头求底数极限，再算 u−1 的通分结果乘 v。题目两端各含未知参数时，分别算出两端极限后令其相等。
- **关键概念**：`抓大头`、`通分`
- **出处**：[杰哥 P20](https://www.bilibili.com/video/BV1Up4y1Y76a?p=20)

### 两个 e 相减
- **要点**：把后一项的 e 提到括号外，凑成 e^□−1~□，再用 cos□−1 的等价收尾。
- **关键概念**：`提公因子`、`e^□−1~□`
- **出处**：[斌哥 P185](https://www.bilibili.com/video/BV12DdNYzEvy?p=185)

### 对数运算改写
- **要点**：ln A−ln B=ln(A/B)；a ln b=ln b^a；常数项可写成 ln eˣ 从而并入对数，再拆分成 ln(1+□) 用等价。
- **关键概念**：`对数运算`、`拆项`
- **相互关系**：对数相减合并是「多对数项相加」型题目的突破口。
- **出处**：[斌哥 P196](https://www.bilibili.com/video/BV12DdNYzEvy?p=196)、[P199](https://www.bilibili.com/video/BV12DdNYzEvy?p=199)

### ln□ 的加一减一
- **要点**：见到对数里的方框，可加一减一凑成 ln(1+□)~□；把 ln x 改写为 ln(1+(x−1)) 即可凑出方框。但该改写要求方框趋于 1（此时方框减一趋于 0），若方框本身趋于 0 则不能用。
- **关键概念**：`加一减一`、`方框趋于 1`
- **相互关系**：易错点——套用前必须验证方框的趋向。
- **出处**：[斌哥 P170](https://www.bilibili.com/video/BV12DdNYzEvy?p=170)、[P172](https://www.bilibili.com/video/BV12DdNYzEvy?p=172)、[P187](https://www.bilibili.com/video/BV12DdNYzEvy?p=187)、[P195](https://www.bilibili.com/video/BV12DdNYzEvy?p=195)、[P198](https://www.bilibili.com/video/BV12DdNYzEvy?p=198)

### 因式分解约分
- **要点**：分子分母可作平方差等分解时，先约去零因子再代入，比洛必达快且不易错。
- **关键概念**：`平方差公式`、`约分`
- **出处**：[斌哥 P168](https://www.bilibili.com/video/BV12DdNYzEvy?p=168)、[P169](https://www.bilibili.com/video/BV12DdNYzEvy?p=169)

### 倒代换
- **要点**：式子既无根号（不能有理化）又无分母（不能通分）时，令 t=1/x，把 x→∞ 换成 t→0。倒代换的本质是创造分母，之后照常通分、等价替换。
- **关键概念**：`倒代换`、`创造分母`
- **相互关系**：与「提公因子凑等价」是同一题的两条路，后者只对特定题有效，倒代换是一般方法。
- **出处**：[陈哥 P27](https://www.bilibili.com/video/BV1husGzwEtZ?p=27)；[米哥 P21](https://www.bilibili.com/video/BV1swAWerEzS?p=21)、[P22](https://www.bilibili.com/video/BV1swAWerEzS?p=22)、[P30](https://www.bilibili.com/video/BV1swAWerEzS?p=30)；[斌哥 P152](https://www.bilibili.com/video/BV12DdNYzEvy?p=152)

### 夹逼定理及其放缩技巧
- **要点**：若 a_n≤b_n≤c_n 且 lim a_n=lim c_n=A，则 lim b_n=A。放缩核心是把各项分母统一为第一项或最后一项的分母：分母变大则分式变小（放小），分母变小则分式变大（放大）；统一分母后分子可直接相加求和（常用等差数列求和公式）。步骤：①确定项数 n；②找最小项与最大项（分式型看分母，分母越小值越大）；③各项换最小项得「n 乘最小项」、换最大项得「n 乘最大项」完成放缩；④两端取极限。
- **关键概念**：`夹逼定理`、`放缩`、`统一分母`、`等差数列求和`
- **相互关系**：每次放缩都要对比确认放大还是放小，两端极限必须相同才可使用；无穷项求和时不能因每项趋于零就断定和为零（n 个 1/n 之和为 1），凡遇无穷项求和必须用夹逼定理。
- **出处**：[陈哥 P24](https://www.bilibili.com/video/BV1husGzwEtZ?p=24)；[杰哥 P24](https://www.bilibili.com/video/BV1Up4y1Y76a?p=24)；[米哥 P27](https://www.bilibili.com/video/BV1swAWerEzS?p=27)；[ok姐 P16](https://www.bilibili.com/video/BV1vm421s7mv?p=16)

### 抽象函数具体化（仅限选填）
- **要点**：已知抽象函数 f(x) 与某函数等价时，可令 f(x) 就等于那个函数直接算出极限；或把抽象函数视为 f(x)=x（把 f 去掉）直接做差，谁消失就乘谁的导数。解答题必须用严格的「除一个乘一个」变形往已知极限上靠。
- **关键概念**：`具体化`、`选填技巧`、`去F法`
- **出处**：[米哥 P37](https://www.bilibili.com/video/BV1swAWerEzS?p=37)；[杰哥 P30](https://www.bilibili.com/video/BV1Up4y1Y76a?p=30)；[斌哥 P117](https://www.bilibili.com/video/BV12DdNYzEvy?p=117)

### 连续的定义与充要条件
- **要点**：函数在 x₀ 处连续即 lim\_\{x→x₀\}f(x)=f(x₀)，即「极限值等于函数值」；前提是 x₀ 两边都有定义。充要条件为：左极限等于右极限，且都等于该点函数值。左极限等于函数值称左连续，右极限等于函数值称右连续，两者都满足才是连续。需同时满足 f(x₀) 存在、极限存在、两者相等。
- **关键概念**：`连续`、`左连续`、`右连续`、`且的关系`
- **相互关系**：通常只在分段函数的分段点处考察。
- **出处**：[陈哥 P29](https://www.bilibili.com/video/BV1husGzwEtZ?p=29)；[杰哥 P25](https://www.bilibili.com/video/BV1Up4y1Y76a?p=25)；[米哥 P32](https://www.bilibili.com/video/BV1swAWerEzS?p=32)；[学士帽 P23](https://www.bilibili.com/video/BV1X4411J792?p=23)、[P26](https://www.bilibili.com/video/BV1X4411J792?p=26)；[ok姐 P21](https://www.bilibili.com/video/BV1vm421s7mv?p=21)；[斌哥 P179](https://www.bilibili.com/video/BV12DdNYzEvy?p=179)

### 连续性与复合极限
- **要点**：若内层函数极限存在为 A，且 f 在 A 处连续，则复合函数的极限等于 f(A)，即极限可代入内层极限值。求 lim\_\{x→x₀\}f(g(x)) 时令 u=g(x)，若 lim g(x)=u₀，则原极限等于 lim\_\{u→u₀\}f(u)，即换元法；熟练后可省略换元步骤。
- **关键概念**：`连续`、`复合函数极限`、`换元`、`中间变量`
- **出处**：[ok姐 P13](https://www.bilibili.com/video/BV1vm421s7mv?p=13)、[P19](https://www.bilibili.com/video/BV1vm421s7mv?p=19)；[斌哥 P179](https://www.bilibili.com/video/BV12DdNYzEvy?p=179)

### 讨论分段函数连续性的套路
- **要点**：三步走——求分段点处的左极限、右极限、函数值，再按充要条件比较得出结论。两侧通常都是基本初等函数，故只需讨论分段点。若分段点左右两侧是同一函数表达式，则无需分左右，直接求该点极限即可。学士帽做法：函数值取含该分段点的那一段代入，极限值取含待求未知量的那一段求左右极限，从而解出参数。
- **关键概念**：`分段点`、`分左右极限`、`基本初等函数`
- **相互关系**：极限的求法（等价无穷小、1^∞ 万能公式、零乘有界）在此复用。
- **出处**：[陈哥 P29](https://www.bilibili.com/video/BV1husGzwEtZ?p=29)；[杰哥 P25](https://www.bilibili.com/video/BV1Up4y1Y76a?p=25)；[学士帽 P24](https://www.bilibili.com/video/BV1X4411J792?p=24)

### 间断的定义与间断点分类
- **要点**：不连续即间断，lim\_\{x→x₀\}f(x)≠f(x₀)，x₀ 称间断点。满足任一情形即可：(1) 在 x₀ 处无定义但在其去心邻域内有定义；(2) 有定义但极限不存在；(3) 有定义且极限存在但极限不等于函数值。分类：第一类——左右极限都存在，相等为可去间断点、不相等为跳跃间断点；第二类——左右极限至少有一个不存在（含为无穷），有一个为无穷是无穷间断点，极限值在某区间内振荡是震荡间断点。
- **关键概念**：`间断点`、`可去间断点`、`跳跃间断点`、`无穷间断点`、`震荡间断点`
- **相互关系**：间断点只有两种来源：初等函数的无定义点（主要是分式中分母为零的点）、分段函数的分段点；情形 (1) 中若两边也无定义（如 ln x 在 x=0）则不算间断点；可去间断点补齐该点函数值后即变连续，跳跃与无穷间断点不能；考试以可去、跳跃、无穷三种为主。
- **出处**：[陈哥 P30](https://www.bilibili.com/video/BV1husGzwEtZ?p=30)；[米哥 P33](https://www.bilibili.com/video/BV1swAWerEzS?p=33)；[学士帽 P25](https://www.bilibili.com/video/BV1X4411J792?p=25)；[ok姐 P22](https://www.bilibili.com/video/BV1vm421s7mv?p=22)

### 判断间断点类型的流程与连续区间
- **要点**：三步：找可疑点→算左右极限→归入四类；可疑点＝无定义点（分母零点必为间断点）与分段点（须逐点算）。分式型先因式分解找分母零点；一开始不能约分（改变定义域），讨论极限时可约分；分母零分子非零→无穷，约分后极限为常数但无定义→可去，左右极限不等→跳跃；sin x=0 的解为 x=kπ。一般函数的左右极限天然相等，只有含 arctan(1/x)、e\^\{1/x\} 的函数以及分段函数才需要分左右讨论。求出全部间断点后，把间断点从数轴上剔除，剩下的区间用并集连接即得连续区间。
- **关键概念**：`找间断点`、`连续区间`、`并集`、`因式分解`
- **相互关系**：连续区间是间断点问题的变式考法，常考选择或填空。
- **出处**：[陈哥 P30](https://www.bilibili.com/video/BV1husGzwEtZ?p=30)；[米哥 P33](https://www.bilibili.com/video/BV1swAWerEzS?p=33)、[P34](https://www.bilibili.com/video/BV1swAWerEzS?p=34)；[学士帽 P26](https://www.bilibili.com/video/BV1X4411J792?p=26)、[P27](https://www.bilibili.com/video/BV1X4411J792?p=27)

### 间断点的求法
- **要点**：由「初等函数在定义域内连续」可知，定义不要的点就是间断点，故求间断点即求函数的定义域，把被排除的点列出来（题目问的是点，不写不等号）。分段函数：①各段内按求定义域的方法找间断点并回代检验该点是否落在对应区间内；②分段点单独用三条件逐一验证，若为间断点再按左右极限定类型，最后汇总。
- **关键概念**：`定义域`、`定义不要的点`、`各段内`、`分段点`
- **出处**：[学士帽 P26](https://www.bilibili.com/video/BV1X4411J792?p=26)、[P27](https://www.bilibili.com/video/BV1X4411J792?p=27)；[米哥 P33](https://www.bilibili.com/video/BV1swAWerEzS?p=33)

### 连续函数的四则运算
- **要点**：若 f(x)、g(x) 在 x₀ 处连续，则它们的和、差、积、商（分母不为零）也在 x₀ 处连续；由此构成的函数定义域是各基本初等函数定义域的交集而非并集。
- **关键概念**：`和差积商`、`定义域取交集`
- **相互关系**：是求极限「代入法」的理论依据。
- **出处**：[ok姐 P21](https://www.bilibili.com/video/BV1vm421s7mv?p=21)

### 初等函数的连续性
- **要点**：一切初等函数在其定义区间内都是连续的。
- **关键概念**：`初等函数`、`定义区间`
- **出处**：[ok姐 P23](https://www.bilibili.com/video/BV1vm421s7mv?p=23)；[学士帽 P26](https://www.bilibili.com/video/BV1X4411J792?p=26)；[石头 P15](https://www.bilibili.com/video/BV18CL26WEJ3?p=15)

### 反函数与复合函数的连续性
- **要点**：直接函数与反函数的单调性、连续性一致；内层函数在 x₀ 处连续、外层函数在对应点连续时，复合函数在该点连续，极限可直接代入。
- **关键概念**：`直接函数`、`中间变量`
- **相互关系**：与复合函数求极限法则同源；广东升本中这几个定理不重点考察。
- **出处**：[ok姐 P23](https://www.bilibili.com/video/BV1vm421s7mv?p=23)

### 有界性、最值定理与介值定理
- **要点**：闭区间上连续的函数在该区间上一定有界，且一定能取到最大值和最小值；若还单调，则最值在端点处取得。介值定理：若在 [a,b] 上连续，μ 介于最小值 m 与最大值 M 之间，则至少存在一点 ξ∈[a,b] 使 f(ξ)=μ。
- **关键概念**：`闭区间`、`最大值 M`、`最小值 m`、`介值`、`最值在端点取得`
- **相互关系**：最值定理是「证明不等式」转化为最值问题的依据，也是介值定理的前置知识；使用时关键是把待证的量看成 μ 并验证它落在 [m,M] 内。
- **出处**：[陈哥 P129](https://www.bilibili.com/video/BV1husGzwEtZ?p=129)；[ok姐 P24](https://www.bilibili.com/video/BV1vm421s7mv?p=24)

### 零点定理与证明根的存在性
- **要点**：在闭区间 [a,b] 上连续且 f(a)·f(b)&lt;0，则至少存在一点 ξ∈(a,b) 使 f(ξ)=0；若再加单调条件，则零点有且仅有一个。端点处无定义时，可用两端点处的极限异号代替。证明四步——令 F(x)=方程左端减右端、说明 F(x) 连续、验证端点值乘积小于零、写结论并扣题。
- **关键概念**：`零点定理`、`闭区间连续`、`端点值乘积小于零`、`有且仅有一个`
- **相互关系**：连续条件题目必定给出，做题的关键是找两个端点值异号；「至少存在一点」说明零点可能不止一个；是罗尔定理的基础。
- **出处**：[陈哥 P130](https://www.bilibili.com/video/BV1husGzwEtZ?p=130)；[学士帽 P28](https://www.bilibili.com/video/BV1X4411J792?p=28)；[ok姐 P24](https://www.bilibili.com/video/BV1vm421s7mv?p=24)、[P39](https://www.bilibili.com/video/BV1vm421s7mv?p=39)

### 变限积分求导公式（含复合结构）
- **要点**：(∫_a\^\{g(x)\} f(t)dt)′=f(g(x))·g′(x)——先把上限代入被积函数，再乘上限的导数，上限求导这一步不能漏。上下限均为变量时结果为 f(φ(x))φ′(x)−f(ω(x))ω′(x)；变下限时可先用换限变号把负号提到积分号外化为变上限。积分整体被平方、或外面还套着函数时按复合函数处理：先对外层求导，再乘积分本身求导。被积函数中其他字母对 t 均视为常数。
- **关键概念**：`变限积分`、`上限函数`、`复合求导`、`上限项减下限项`
- **相互关系**：含变上限积分的极限题必用洛必达；上限为 x 的复合形式时结合复合求导。
- **出处**：[陈哥 P76](https://www.bilibili.com/video/BV1husGzwEtZ?p=76)；[杰哥 P43](https://www.bilibili.com/video/BV1Up4y1Y76a?p=43)；[米哥 P75](https://www.bilibili.com/video/BV1swAWerEzS?p=75)；[学士帽 P68](https://www.bilibili.com/video/BV1X4411J792?p=68)；[ok姐 P63](https://www.bilibili.com/video/BV1vm421s7mv?p=63)；[斌哥 P176](https://www.bilibili.com/video/BV12DdNYzEvy?p=176)、[P177](https://www.bilibili.com/video/BV12DdNYzEvy?p=177)、[P188](https://www.bilibili.com/video/BV12DdNYzEvy?p=188)

### 被积函数含上下限变量的处理
- **要点**：求导前提是被积函数中不含上下限的字母。若含 x，可拆出并提到积分号外，再用乘积求导法则；或用换元法，如令 x−t=u（换元必换限、dt=−du、上下限交换变号），对 x²−t² 则先凑微分再令 u=x²−t²。
- **关键概念**：`拆分积分`、`常数提出积分号`、`乘积求导法则`、`换元换线`
- **相互关系**：易错点是直接上限代入得到 x−x=0 的错误结果；经典错误是把积分号内的 x 当作已被求导。
- **出处**：[陈哥 P76](https://www.bilibili.com/video/BV1husGzwEtZ?p=76)；[杰哥 P43](https://www.bilibili.com/video/BV1Up4y1Y76a?p=43)；[米哥 P75](https://www.bilibili.com/video/BV1swAWerEzS?p=75)

### 变限积分参与极限的处理
- **要点**：极限中含变限积分，基本套路是先用等价替换化简分母，再洛必达求导，必要时连续多次。含 √(sin²x) 时开方得 |x|，在 x→0⁺ 时可直接写成 x。变限积分的结果等于非零常数即为同阶，等于 1 为等价。口诀「能等价先等价，再用洛必达」；上下限相等时积分值为零。
- **关键概念**：`洛必达法则`、`等价替换`、`先等价后洛必达`
- **相互关系**：与「非零因子先算」连用，可先把积分前后的常数因子提出；各省几乎每年必考。
- **出处**：[陈哥 P76](https://www.bilibili.com/video/BV1husGzwEtZ?p=76)；[杰哥 P43](https://www.bilibili.com/video/BV1Up4y1Y76a?p=43)；[米哥 P75](https://www.bilibili.com/video/BV1swAWerEzS?p=75)；[学士帽 P68](https://www.bilibili.com/video/BV1X4411J792?p=68)；[ok姐 P63](https://www.bilibili.com/video/BV1vm421s7mv?p=63)；[斌哥 P175](https://www.bilibili.com/video/BV12DdNYzEvy?p=175)、[P178](https://www.bilibili.com/video/BV12DdNYzEvy?p=178)、[P184](https://www.bilibili.com/video/BV12DdNYzEvy?p=184)、[P191](https://www.bilibili.com/video/BV12DdNYzEvy?p=191)


### 高等数学的八章脉络
- **要点**：高等数学以函数为研究对象、以极限为研究方法，共分八章：函数极限与连续、一元函数微分学、一元函数积分学、向量代数与空间解析几何、多元函数微分学、多元函数积分学、微分方程、无穷级数。一元是多元的基础，前三章是根基，微分与积分互为逆运算。
- **关键概念**：`函数`、`极限`、`一元函数微分学`、`一元函数积分学`、`微分方程`、`无穷级数`
- **相互关系**：微分方程由一元微分学与积分学衍生，无穷级数建立在函数与极限之上；广东专升本只考高等数学，不考线性代数与概率论，教材章节划分不同不影响知识相通。
- **出处**：[石头 P1](https://www.bilibili.com/video/BV18CL26WEJ3?p=1)

### 函数的概念与三要素
- **要点**：若自变量 $x$ 按某个对应法则变化时，因变量 $y$ 被唯一确定，则称 $y$ 是 $x$ 的函数，记作 $y=f(x)$。自变量、因变量与对应法则合称函数三要素，自变量的取值范围叫定义域，因变量的取值范围叫值域。判断两个函数是否相同，必须「化简之前看定义域、化简之后看对应法则」，两者同时相同才是同一函数，且与自变量、因变量用什么字母表示无关。
- **关键概念**：`自变量`、`因变量`、`对应法则`、`$y=f(x)$`、`定义域`、`值域`
- **相互关系**：定义域相同且对应法则相同是同一函数的充要条件，此时值域必相同；反之定义域与值域都相同（如 $y=2x$ 与 $y=x^2$ 都取 $[0,2]$）、或值域与对应法则都相同（如 $\sin x$ 分别取一个周期与两个周期）都不足以判定同一函数，选择题用排除法最快。
- **出处**：[石头 P3](https://www.bilibili.com/video/BV18CL26WEJ3?p=3)

### 分段函数
- **要点**：在定义域的不同区间上用不同表达式表示的函数叫分段函数，例如 $x\leq1$ 时取 $x^2$、$1&lt;x&lt;10$ 时取 $2x$、$x\geq10$ 时恒为 $20$。分段函数是一个函数而不是多个函数，画图时把各段图像拼在同一坐标系内。
- **关键概念**：`分段函数`、`不同区间不同表达式`
- **相互关系**：分段点是后续讨论极限、连续性与间断点的关键位置，求分段点处的极限必须分左右两侧分别讨论。
- **出处**：[石头 P4](https://www.bilibili.com/video/BV18CL26WEJ3?p=4)

### 隐函数与参数方程表示的函数
- **要点**：把 $x$、$y$ 写在同一个方程里而不显式解出 $y$ 的函数叫隐函数，如 $4x^2+3y=0$、$e^y+xy-e=0$；由 $x=3t+1$、$y=2t^2$ 这类方程组确定的也是函数，即参数方程表示的函数。不必强求化成 $y=f(x)$ 的显式形式，关键是确认一个 $x$ 对应唯一确定的 $y$。
- **关键概念**：`隐函数`、`参数方程`、`显式形式`
- **相互关系**：这两类形式与抽象函数、复合函数本质相同，区别只在写法；参数方程消去参数 $t$ 即可化为普通函数。
- **出处**：[石头 P4](https://www.bilibili.com/video/BV18CL26WEJ3?p=4)

### 定义域的限制条件与具体函数的定义域
- **要点**：命题人未给出范围、只要求表达式有意义时求出的定义域称自然定义域。常见限制：分式 $\frac{1}{\square}$ 要求 $\square\neq0$；偶次根式 $\sqrt{\square}$ 要求 $\square\geq0$；对数 $\ln\square$ 要求 $\square>0$；$\tan x$ 要求 $x\neq k\pi+\frac{\pi}{2}$；$\arcsin x$、$\arccos x$ 要求 $x\in[-1,1]$。多个条件要同时满足，解出后在数轴上取交集，用区间或集合表示（小括号为开区间、中括号为闭区间）。
- **关键概念**：`自然定义域`、`分母不为零`、`偶次根号下大于等于零`、`真数大于零`、`取交集`
- **相互关系**：此处已出现整体思想的雏形——公式中的 $x$ 可换成任意一「坨」表达式，条件随之整体成立；$y=x$、$y=\sin x$、$y=\cos x$ 的定义域为 $R$，$\frac1x$ 为 $(-\infty,0)\cup(0,+\infty)$，$\sqrt x$ 为 $[0,+\infty)$。
- **出处**：[石头 P3](https://www.bilibili.com/video/BV18CL26WEJ3?p=3)

### 抽象函数与框框思想
- **要点**：只给出符号 $y=f(x)$、$y=g(x)$ 而不给表达式与法则的函数叫抽象函数，$f$ 与 $g$ 一般代表不同法则。核心是「框框思想」：同一个 $f$ 后面括号内的整体范围必须相同。求抽象函数定义域分两步：先由已知函数的定义域求出框框的范围，再令另一函数括号内的整体也落在这个范围内，解不等式即得。
- **关键概念**：`抽象函数`、`框框思想`、`括号内整体范围相同`
- **相互关系**：最易错处是把两个不同函数中的 $x$ 当成同一个 $x$；定义域永远指自变量 $x$ 的范围，而框框的范围才是两式相等的桥梁。
- **出处**：[石头 P4](https://www.bilibili.com/video/BV18CL26WEJ3?p=4)

### 直接代入法（函数表达式的求解）
- **要点**：已知 $f(x)$ 求 $f(\square)$（由简单到复杂）时，直接把括号内的整体代进右边每一处 $x$。例如 $f(x)=x^2+2x$，则 $f(\frac{x}{2}+1)=(\frac{x}{2}+1)^2+2(\frac{x}{2}+1)=\frac14x^2+2x+3$。
- **关键概念**：`直接代入法`、`由简单到复杂`
- **相互关系**：函数与所用字母无关，$f(x)$、$f(t)$、$f(\square)$ 表示同一法则，这是代入法的前提。
- **出处**：[石头 P4](https://www.bilibili.com/video/BV18CL26WEJ3?p=4)

### 换元法与配凑法
- **要点**：已知 $f(\square)=\triangle$ 求 $f(x)$（由复杂到简单）时，令括号内的整体 $\square=t$，反解出用 $t$ 表示的 $x$ 再代回右边，化为 $f(t)$ 后把 $t$ 写成 $x$；也可用配凑法把右边凑成含该整体的形式。若是由复杂到复杂（如已知 $f(\frac{x}{2}+1)$ 求 $f(2x-1)$），分两步走：先用换元法求出 $f(x)$，再用直接代入法求目标表达式。
- **关键概念**：`换元法`、`配凑法`、`反解`、`两步走`
- **相互关系**：换元时左边右边都要换干净，换元后自变量字母不同不影响结果；配凑法计算较繁，一般优先用换元法。
- **出处**：[石头 P4](https://www.bilibili.com/video/BV18CL26WEJ3?p=4)

### 奇偶性及其运算规律
- **要点**：前提是定义域关于原点对称。满足 $f(-x)=f(x)$ 的为偶函数，图像关于 $y$ 轴对称；满足 $f(-x)=-f(x)$ 的为奇函数，图像关于原点对称。判断时写出 $f(-x)$ 与 $f(x)$ 比较即可，不必画图。
- **关键概念**：`偶函数`、`奇函数`、`$f(-x)=f(x)$`、`$f(-x)=-f(x)$`、`定义域关于原点对称`
- **相互关系**：常见奇函数有 $x$ 的奇数次幂、$\sin x$、$\tan x$、$\arcsin x$、$\arctan x$；常见偶函数有 $x$ 的偶数次幂、$\cos x$、$|x|$、常值函数 $y=C$。运算规律：奇±奇=奇，偶±偶=偶，奇±偶为非奇非偶；奇×奇=偶，偶×偶=偶，奇×偶=奇。补充结论：$f(x)+f(-x)$ 为偶函数，$f(x)-f(-x)$ 为奇函数；定义域不对称则直接非奇非偶；奇函数在 $x=0$ 处有定义时必有 $f(0)=0$。
- **出处**：[石头 P5](https://www.bilibili.com/video/BV18CL26WEJ3?p=5)

### 有界性、单调性与周期性
- **要点**：函数值恒大于等于某数 $K_1$ 称有下界，恒小于等于某数 $K_2$ 称有上界，上下界同时存在称有界，等价于存在正数 $M$ 使 $|f(x)|\leq M$，界不唯一、通常取最小的那个。$x_1&lt;x_2$ 时恒有 $f(x_1)&lt;f(x_2)$ 为单调增，恒有 $f(x_1)>f(x_2)$ 为单调减，用定义作差判断符号即可证明。满足 $f(x+T)=f(x)$ 的为周期函数，其中最小的正数叫最小正周期。
- **关键概念**：`有界性`、`上界/下界`、`单调性`、`定义法证明`、`周期 $T$`、`最小正周期`
- **相互关系**：有界性服务于「$0\times$有界$=0$」；$\sin x$、$\cos x$ 有界，$y=x^2$ 只有下界、$\tan x$ 上下都无界。$y=x^3$ 在 $R$ 上单调增，$y=x^2$ 在 $R$ 上不单调须拆区间；$\sin x$、$\cos x$ 的最小正周期为 $2\pi$，$|\cos x|$、$\tan x$ 为 $\pi$，常值函数与狄利克雷函数不存在最小正周期。
- **出处**：[石头 P5](https://www.bilibili.com/video/BV18CL26WEJ3?p=5)

### 反函数存在的条件与三个性质
- **要点**：只有在连续定义域内单调的函数才有反函数，因此 $y=x^2$、$y=\sin x$ 在 $R$ 上没有反函数，只能在单调区间上取反函数。反函数有三个性质：与原函数图像关于直线 $y=x$ 对称；单调性相同；奇偶性相同（奇函数的反函数仍是奇函数，非奇非偶的反函数仍非奇非偶，偶函数没有反函数）。
- **关键概念**：`单调才有反函数`、`关于 $y=x$ 对称`、`单调性相同`、`奇偶性相同`
- **相互关系**：$y=e^x$ 与 $y=\ln x$、$y=\sin x$ 取 $[-\frac\pi2,\frac\pi2]$ 与 $y=\arcsin x$ 是互为反函数的典型；$y=\cos x$ 取 $[0,\pi]$ 后为非奇非偶，其反函数 $y=\arccos x$ 也是非奇非偶。
- **出处**：[石头 P6](https://www.bilibili.com/video/BV18CL26WEJ3?p=6)

### 复合函数的概念、次序与限制
- **要点**：由 $y=f(u)$、$u=g(x)$ 代入得 $y=f[g(x)]$，其中 $u$ 叫中间变量，这样的函数叫复合函数。复合有先后次序，$f[g(x)]$ 与 $g[f(x)]$ 一般不同；并且要求内层函数 $u=g(x)$ 的值域落在外层函数 $y=f(u)$ 的定义域内。
- **关键概念**：`复合函数`、`中间变量 $u$`、`$y=f[g(x)]$`、`内层值域在外层定义域内`
- **相互关系**：内层值域的限制正是框框思想的体现，因此抽象函数定义域问题可转化为复合函数中「已知定义域求值域」或「已知值域求定义域」；复合函数、抽象函数、参数方程本质相同，抓住先内层后外层的顺序即可。
- **出处**：[石头 P6](https://www.bilibili.com/video/BV18CL26WEJ3?p=6)

### 指数函数与对数函数
- **要点**：$y=a^x$（$a>0$、$a\neq1$）与 $y=\log_a x$ 互为反函数，图像关于 $y=x$ 对称，考试以 $y=e^x$（$e\approx2.718$）与 $y=\ln x$ 为主。$e^x$ 的定义域为 $R$、值域为 $(0,+\infty)$、单调增、过 $(0,1)$；$\ln x$ 的定义域为 $(0,+\infty)$、值域为 $R$、单调增、过 $(1,0)$。运算公式：$e^m\cdot e^n=e\^\{m+n\}$、$\frac{e^m}{e^n}=e\^\{m-n\}$、$(e^m)^n=e\^\{mn\}$；$\ln a+\ln b=\ln ab$、$\ln a-\ln b=\ln\frac ab$、$\ln m^n=n\ln m$、$e\^\{\ln x\}=x$。
- **关键概念**：`指数函数`、`对数函数`、`$e\approx2.718$`、`$\ln x$`、`真数大于零`、`$e^{\ln x}=x$`
- **相互关系**：注意区分幂函数 $x^a$ 与指数函数 $a^x$；恒等变形 $x=e\^\{\ln x\}$ 是后续求极限与微分方程的重要工具，可理解为「先取对数再取指数，两个反函数抵消」。
- **出处**：[石头 P7](https://www.bilibili.com/video/BV18CL26WEJ3?p=7)

### 三角函数与同角关系
- **要点**：$\sin x$、$\cos x$ 的定义域为 $R$、值域为 $[-1,1]$、最小正周期为 $2\pi$，前者是奇函数、后者是偶函数；$\tan x$ 的定义域为 $x\neq k\pi+\frac{\pi}{2}$、值域为 $R$、最小正周期为 $\pi$、是奇函数。同角关系可借助三角图记忆：$\sin^2x+\cos^2x=1$、$1+\tan^2x=\sec^2x$、$1+\cot^2x=\csc^2x$；$\tan x=\frac{\sin x}{\cos x}$、$\cot x=\frac{\cos x}{\sin x}$、$\sec x=\frac1{\cos x}$、$\csc x=\frac1{\sin x}$。
- **关键概念**：`三角函数`、`$\sin^2x+\cos^2x=1$`、`$\tan x=\frac{\sin x}{\cos x}$`、`倒数关系`、`最小正周期`
- **相互关系**：$\sec x$、$\csc x$、$\cot x$ 不要求掌握，但出现时要能化为 $\sin$、$\cos$、$\tan$ 处理；三角函数的图像是判断奇偶性、周期性与有界性的依据。
- **出处**：[石头 P7](https://www.bilibili.com/video/BV18CL26WEJ3?p=7)

### 极限的思想与记号
- **要点**：极限刻画「无限趋近」的过程，产生于求曲边图形面积、曲线长度等实际问题的精确解答。庄子「日取半棰」说明无限次取半后棰长趋近于零，刘徽割圆用内接正多边形逼近圆，都是极限思想的体现。极限记作 $\lim$（limit 的缩写），$\to$ 表示趋近，$\lim\_\{x\to x\_0\}f(x)=A$ 中的 $A$ 必须是确定的常数。
- **关键概念**：`极限`、`$\lim$`、`趋近`、`割之弥细，所失弥少`
- **相互关系**：极限是微积分的基础思想，后续导数、积分、级数全部建立在它之上；理解的标准是能用自己的话举生活实例讲清楚，而不是背概念。
- **出处**：[石头 P8](https://www.bilibili.com/video/BV18CL26WEJ3?p=8)

### 数列与数列极限的定义
- **要点**：按正整数 $n$ 的次序排列的一列数 $\{x_n\}$ 叫数列，第 $n$ 项 $x_n$ 叫通项，数列必须有无穷多项。数列极限的定义：对任意给定的正数 $\varepsilon$（无论多小），总存在正整数 $N$，当 $n>N$ 时恒有 $|x_n-A|&lt;\varepsilon$，则称常数 $A$ 是数列的极限，也称数列收敛于 $A$。
- **关键概念**：`数列`、`通项 $x_n$`、`$\varepsilon$-$N$ 语言`、`收敛`、`极限`
- **相互关系**：$\varepsilon$ 是任取的正数、$N$ 的存在性由 $\varepsilon$ 决定；该定义考试不直接考，只需理解，且数列极限只有 $n\to\infty$ 一种变化过程。
- **出处**：[石头 P9](https://www.bilibili.com/video/BV18CL26WEJ3?p=9)

### 单调有界数列必有极限
- **要点**：收敛数列的极限唯一；收敛数列一定有界，但反过来有界数列不一定收敛（如 $1,-1,1,-1,\dots$）；单调且有界的数列必然收敛，即必有极限。此外，数列趋向无穷（如 $x_n=n^2$）属于极限不存在的情形，只是习惯上写作极限为无穷。
- **关键概念**：`极限唯一`、`收敛必有界`、`有界不一定收敛`、`单调有界必有极限`
- **相互关系**：与函数有界性的结论一致，「有界」只是收敛的必要条件而非充分条件；判断收敛要同时看是否有界与是否单调。
- **出处**：[石头 P9](https://www.bilibili.com/video/BV18CL26WEJ3?p=9)

### 夹逼准则及其应用
- **要点**：若三个数列满足 $y_n\leq x_n\leq z_n$（从某一项起）且 $\lim y_n=\lim z_n=A$，则 $\lim x_n=A$。它是求 $n$ 项和形式数列极限的专用方法：分子保持不变，把分母全换成最大的一项得 $y_n$、全换成最小的一项得 $z_n$，再验证两者极限相同。
- **关键概念**：`夹逼准则`、`$y_n\leq x_n\leq z_n$`、`放缩`、`$n$ 项和`
- **相互关系**：放缩的关键是两侧极限必须相等，否则只能得到一个范围；这是求极限的第一种方法，也为函数极限中的函数夹逼准则作铺垫。
- **出处**：[石头 P9](https://www.bilibili.com/video/BV18CL26WEJ3?p=9)

### 函数极限的两种变化过程与去心邻域
- **要点**：函数极限有两种变化过程：$x\to\infty$（含 $x\to+\infty$ 与 $x\to-\infty$）与 $x\to x_0$（含 $x\to x_0^+$ 与 $x\to x_0^-$）。$\lim\_\{x\to x\_0\}f(x)$ 只要求 $f(x)$ 在 $x_0$ 的某去心邻域内有定义，即在 $x_0$ 处可以没有定义。
- **关键概念**：`$x\to\infty$`、`$x\to x_0$`、`去心邻域`、`$\varepsilon$-$X$ 语言`、`$\varepsilon$-$\delta$ 语言`
- **相互关系**：数列极限只有 $n\to\infty$，函数极限多出 $x\to x_0$，原因是数列各项离散、而函数连续可以沿曲线无限靠近；函数极限一般不说「收敛」，「收敛」通常指数列。
- **出处**：[石头 P10](https://www.bilibili.com/video/BV18CL26WEJ3?p=10)

### 左右极限与极限存在的充要条件
- **要点**：从左侧趋近得左极限 $\lim\_\{x\to x\_0\^-\}f(x)$，从右侧趋近得右极限 $\lim\_\{x\to x\_0\^+\}f(x)$，合称单侧极限。函数在 $x_0$ 处极限存在的充要条件是左极限与右极限都存在且相等；求 $x\to\infty$ 时的极限则要求 $x\to+\infty$ 与 $x\to-\infty$ 的极限都存在且相等。例如 $f(x)=\frac1x$，$x\to0^+$ 时为 $+\infty$、$x\to0^-$ 时为 $-\infty$，故 $x\to0$ 时极限不存在。
- **关键概念**：`左极限`、`右极限`、`单侧极限`、`存在且相等`
- **相互关系**：这是判断分段函数在分段点处极限与连续性的基本工具；只要有一侧不存在或两侧不相等，极限就不存在。
- **出处**：[石头 P10](https://www.bilibili.com/video/BV18CL26WEJ3?p=10)

### 极限值与函数值的关系及极限的四则运算
- **要点**：$\lim\_\{x\to x\_0\}f(x)$ 与 $f(x_0)$ 无关：$x_0$ 处无定义、或极限值不等于函数值，极限都可能存在。四则运算：若 $\lim f(x)=A$、$\lim g(x)=B$ 均存在，则 $\lim[f(x)\pm g(x)]=A\pm B$、$\lim[f(x)g(x)]=AB$、$\lim\frac{f(x)}{g(x)}=\frac AB$（$B\neq0$），常数可提出、幂可外提。复合函数极限满足：若 $x\to x_0$ 时 $u=g(x)\to u_0$，且 $u\to u_0$ 时 $f(u)\to A$，则 $\lim\_\{x\to x\_0\}f[g(x)]=A$。
- **关键概念**：`极限值与函数值无关`、`四则运算`、`前提：各部分极限存在`、`趋近过程必须一致`
- **相互关系**：拆开加减的前提是每一部分的极限都存在，某部分极限不存在时不能拆，这是最易错处；参与运算的各部分必须趋于同一过程。
- **出处**：[石头 P10](https://www.bilibili.com/video/BV18CL26WEJ3?p=10)

### 直接代入法（函数极限的计算方法）
- **要点**：若 $f(x)$ 在 $x_0$ 处连续（或代入后分母不为零），直接把 $x_0$ 代入即得极限，如 $\lim\_\{x\to1\}x^2=1$。这是最原始的方法，也是其他方法最后收尾的一步。
- **关键概念**：`直接代入法`、`连续`、`代入后分母不为零`
- **相互关系**：代入后若分母为零则无法直接算出，需先消零因子再代入；消零因子的目的正是为了回到直接代入。
- **出处**：[石头 P10](https://www.bilibili.com/video/BV18CL26WEJ3?p=10)

### 消零因子法（因式分解与根式有理化）
- **要点**：$\frac00$ 型未定式不能直接代入，须先消去使分母为零的因子。分子分母都是多项式时用因式分解，如 $\lim\_\{x\to3\}\frac{x-3}{x^2-9}=\lim\_\{x\to3\}\frac1{x+3}=\frac16$，常用工具是 $x^n-1=(x-1)(1+x+\cdots+x\^\{n-1\})$ 与十字相乘；含根式时上下同乘共轭式、用平方差公式去掉根号，如 $\lim\_\{x\to3\}\frac{\sqrt{1+x}-2}{x-3}=\frac14$。
- **关键概念**：`$\frac00$ 型未定式`、`因式分解`、`十字相乘`、`根式有理化`、`平方差公式`
- **相互关系**：计算时只把平方差因式乘开、其余部分先保留，可大幅简化；有理化不限于分母，分子含根式时同样使用。
- **出处**：[石头 P10](https://www.bilibili.com/video/BV18CL26WEJ3?p=10)

### 抓大头法
- **要点**：$x\to\infty$ 时分子分母同为多项式的 $\frac{\infty}{\infty}$ 型，上下同除以最高次幂即可：最高次在分子则极限为无穷，在分母则为零，上下次数相同则为最高次项系数之比。口诀是「上大无穷，下大零，次数相同系数比」。
- **关键概念**：`$\frac{\infty}{\infty}$ 型`、`抓大头`、`同除以最高次幂`、`系数比`
- **相互关系**：本质是次数较低的项趋于零可以忽略；与数列极限中同除 $n$ 的最高次幂做法完全一致。
- **出处**：[石头 P10](https://www.bilibili.com/video/BV18CL26WEJ3?p=10)

### 第一重要极限
- **要点**：$\lim\_\{x\to0\}\frac{\sin x}{x}=1$，它把三角函数与幂函数联系起来，虽然属于 $\frac00$ 型未定式，极限值却固定为一。用法是把原式拆成 $\frac{\sin\square}{\square}$ 与另一可代入部分的乘积，如 $\lim\_\{x\to0\}\frac{\tan x}{x}=\lim\_\{x\to0\}\frac{\sin x}{x}\cdot\frac1{\cos x}=1$；公式中的 $x$ 可整体替换，只要该整体趋于零。
- **关键概念**：`第一重要极限`、`$\lim_{x\to0}\frac{\sin x}{x}=1$`、`整体替换`、`拆项`
- **相互关系**：证明借助单位圆面积不等式与函数的夹逼准则；由它可直接得到 $\sin x\sim x$、$\tan x\sim x$、$\arcsin x\sim x$、$\arctan x\sim x$，是等价无穷小替换的来源。
- **出处**：[石头 P11](https://www.bilibili.com/video/BV18CL26WEJ3?p=11)

### 第二重要极限与自然常数 e
- **要点**：$\lim\_\{x\to\infty\}(1+\frac1x)^x=e$，等价形式为 $\lim\_\{x\to0\}(1+x)\^\{\frac1x\}=e$，其中 $e$ 是自然常数，约等于 $2.71828$。它处理的是「$1+$ 无穷小」的无穷大次幂（即 $1^\infty$ 型），用银行连续计息时本息和不断增长但最终封顶于 $e$ 可以直观理解。
- **关键概念**：`第二重要极限`、`$e\approx2.71828$`、`$1^\infty$ 型`、`$1+$ 无穷小`
- **相互关系**：与第一重要极限不同，这里自变量趋于无穷而非趋于零；判断时不能只看形式，$x\to0$ 的 $(1+x)\^\{\frac1x\}$ 经换元后与 $x\to\infty$ 的情形完全等价。
- **出处**：[石头 P11](https://www.bilibili.com/video/BV18CL26WEJ3?p=11)

### 先定型后定法与基础十法
- **要点**：做极限题先「定型」，即代入后判断属于哪一类，再选方法。类型分三类：定式（可直接算出，如 $0\times$有界$=0$、两个无穷小之和为零、$\frac{0}{\infty}=0$、同号无穷之和为无穷）、基础未定式（$\frac00$ 型、$\frac{\infty}{\infty}$ 型、$1^\infty$ 型）与其他未定式。基础十法为：夹逼准则、直接代入、因式分解消零因子、根式有理化消零因子、抓大头、第一重要极限、第二重要极限、$0\times$有界$=0$、等价无穷小替换，第十种洛必达法则在学完导数后学习。
- **关键概念**：`先定型后定法`、`定式`、`基础未定式`、`$1^\infty$ 型`、`基础十法`
- **相互关系**：$\frac00$ 型可用消零因子、第一重要极限、等价替换或洛必达；$\frac{\infty}{\infty}$ 型可用抓大头、等价替换或洛必达；$1^\infty$ 型用第二重要极限通式。已知极限值反求参数（如含 $a$、$b$ 的式子极限为常数）时，先抓大头定出参数，再比较系数求解。
- **出处**：[石头 P14](https://www.bilibili.com/video/BV18CL26WEJ3?p=14)

### 无穷小与无穷大的概念
- **要点**：在某个变化过程中极限为零的函数称为该过程下的无穷小，极限为无穷的函数称为无穷大。二者都是函数而不是数：再小的确定正数（如一万亿分之一）都不是无穷小，再大的确定数也不是无穷大。零是唯一的无穷小常数，无穷小包含零但不等于零；无穷大可分为正无穷大与负无穷大，且属于极限不存在的情形。
- **关键概念**：`无穷小`、`无穷大`、`是函数不是数`、`零是无穷小`、`极限不存在`
- **相互关系**：求极限时可以把无穷小当成零来简化计算；无穷小与无穷大互为倒数关系（无穷小分之一为无穷大，反之亦然），改变趋近过程（$x\to0$ 换成 $x\to\infty$）也会使二者互换。
- **出处**：[石头 P8](https://www.bilibili.com/video/BV18CL26WEJ3?p=8)、[P12](https://www.bilibili.com/video/BV18CL26WEJ3?p=12)

### 无穷小的性质
- **要点**：$f(x)$ 以 $A$ 为极限的充要条件是 $f(x)=A+\alpha$，其中 $\alpha$ 为该过程下的无穷小；有限个无穷小的和、积仍是无穷小；有界函数与无穷小的乘积是无穷小，特别地常数与无穷小的乘积仍是无穷小。例如 $\lim\_\{x\to\infty\}\frac{\sin x}{x}=0$，因为 $\sin x$ 有界而 $\frac1x$ 是无穷小。
- **关键概念**：`$f(x)=A+\alpha$`、`有限个无穷小的和/积`、`有界×无穷小=无穷小`、`$0\times$有界$=0$`
- **相互关系**：这条性质本身就是一个求极限的方法。注意与第一重要极限区分：$\lim\_\{x\to\infty\}\frac{\sin x}{x}=0$ 属于「有界×无穷小」，而 $\lim\_\{x\to0\}\frac{\sin x}{x}=1$ 是 $\frac00$ 型，二者不可混用。易混的六个极限还包括：$\lim\_\{x\to0\}x\sin\frac1x=0$（零×有界）、$\lim\_\{x\to\infty\}x\sin\frac1x=1$（等价替换）、$\lim\_\{x\to0\}\frac1x\sin\frac1x$ 不存在（无穷×有界，在正负无穷间震荡）、$\lim\_\{x\to\infty\}\frac1x\sin\frac1x=0$。由有限个推广到无限个时结论不成立，如无限个 $\frac1x$ 之和可以等于任意数。
- **出处**：[石头 P12](https://www.bilibili.com/video/BV18CL26WEJ3?p=12)

### 无穷小的比较
- **要点**：两个无穷小之商反映它们趋近于零的快慢。设 $\alpha$、$\beta$ 为同一过程的无穷小：若 $\lim\frac{\alpha}{\beta}=0$，称 $\alpha$ 是 $\beta$ 的高阶无穷小，记作 $\alpha=o(\beta)$；若 $\lim\frac{\alpha}{\beta}=\infty$，称低阶无穷小；若为非零常数 $C$，称同阶无穷小；若 $\lim\frac{\alpha}{\beta^k}=C\neq0$，称 $\alpha$ 是 $\beta$ 的 $k$ 阶无穷小；若 $\lim\frac{\alpha}{\beta}=1$，称二者等价，记作 $\alpha\sim\beta$。
- **关键概念**：`高阶无穷小`、`低阶无穷小`、`同阶无穷小`、`$k$ 阶无穷小`、`等价无穷小`、`$o(\beta)$`
- **相互关系**：阶数越高趋近于零越快；结论必须说清「谁是分母的高阶」，不能颠倒；常数 $C$ 可正可负，$k$ 可为整数也可为分数。五种比较中只有等价最常考。
- **出处**：[石头 P12](https://www.bilibili.com/video/BV18CL26WEJ3?p=12)

### 等价无穷小替换
- **要点**：若 $\alpha\sim\gamma$、$\beta\sim\theta$，则 $\lim\frac{\alpha}{\beta}=\lim\frac{\gamma}{\theta}$，即乘除关系中的无穷小因子可整体替换。常用公式（$x\to0$）：$\sin x\sim x$、$\tan x\sim x$、$\arcsin x\sim x$、$\arctan x\sim x$、$1-\cos x\sim\frac12x^2$、$\ln(1+x)\sim x$、$e^x-1\sim x$、$(1+x)^\mu-1\sim\mu x$（特别地 $\sqrt[n]{1+x}-1\sim\frac xn$）。公式中的 $x$ 可换成任意趋于零的「框框」，如 $\sin x^2\sim x^2$、$\sin 2x\sim2x$。
- **关键概念**：`等价无穷小替换`、`$\sin x\sim x$`、`$1-\cos x\sim\frac12x^2$`、`$\ln(1+x)\sim x$`、`$e^x-1\sim x$`、`$(1+x)^\mu-1\sim\mu x$`
- **相互关系**：替换只在乘除（因子）关系中可用，加减运算中慎用（如 $\lim\_\{x\to0\}\frac{\sin x-\sin2x}{x}$ 不能各自替换后相减）；等价无穷小具有自反性、对称性、传递性与可替换性。$1-\cos x$、$\ln(1+x)$、$e^x-1$、$(1+x)^\mu-1$ 的公式分别由二倍角公式、第二重要极限、指数与对数互化、恒等变形 $x=e\^\{\ln x\}$ 推出。
- **出处**：[石头 P13](https://www.bilibili.com/video/BV18CL26WEJ3?p=13)

### 连续的概念与充要条件
- **要点**：若函数 $y=f(x)$ 在 $x_0$ 的某邻域内有定义，且 $\lim\_\{x\to x\_0\}f(x)=f(x_0)$，则称 $f(x)$ 在 $x_0$ 处连续；在区间上每一点都连续的函数叫该区间上的连续函数。等价定义是：当 $\Delta x\to0$ 时 $\Delta y\to0$，即自变量有微小变化时因变量也只有微小变化。
- **关键概念**：`连续`、`$\lim_{x\to x_0}f(x)=f(x_0)$`、`$\Delta x\to0\Rightarrow\Delta y\to0$`、`连续函数`
- **相互关系**：连续与「极限值等于函数值」互为充要条件，展开即 $f(x_0^-)=f(x_0^+)=f(x_0)$，这是后续做题的直接依据；左极限存在且等于函数值称左连续，右极限存在且等于函数值称右连续，函数在一点连续必须同时左连续且右连续。
- **出处**：[石头 P15](https://www.bilibili.com/video/BV18CL26WEJ3?p=15)

### 间断点的分类
- **要点**：函数不连续的点叫间断点，分三种情形：在 $x_0$ 处无定义；有定义但极限不存在；有定义且极限存在但极限值不等于函数值。按左右极限分类：左右极限都存在的为第一类间断点，其中左右极限相等的叫可去间断点、不相等的叫跳跃间断点；至少有一个不存在的为第二类间断点，其中出现无穷的叫无穷间断点、出现震荡的叫震荡间断点。
- **关键概念**：`间断点`、`第一类间断点`、`第二类间断点`、`可去间断点`、`跳跃间断点`、`无穷间断点`、`震荡间断点`
- **相互关系**：判断间断点类型只看左右极限，与该点的函数值无关。典型例子：$y=\frac{x^2-1}{x-1}$ 在 $x=1$ 处为可去间断点，分段函数在分段点两侧极限不等为跳跃间断点，$y=\tan x$ 在 $x=\frac\pi2$ 处、$y=\frac1x$ 在 $x=0$ 处为无穷间断点，$y=\sin\frac1x$ 在 $x=0$ 处为震荡间断点。
- **出处**：[石头 P15](https://www.bilibili.com/video/BV18CL26WEJ3?p=15)

### 连续函数的四则、复合与反函数连续性
- **要点**：一切初等函数在其定义区间内都是连续的；两个连续函数的和、差、积、商（分母不为零）仍连续；由连续函数构成的复合函数仍连续；连续函数若有反函数，其反函数也连续。
- **关键概念**：`初等函数`、`定义区间内连续`、`四则运算保持连续`、`复合保持连续`、`反函数保持连续`
- **相互关系**：初等函数的连续性正是「直接代入求极限」的根据——只要 $x_0$ 落在定义区间内，就可以把 $x_0$ 直接代入；五类基本初等函数（反三角、对数、幂、指数、三角）都是初等函数。
- **出处**：[石头 P15](https://www.bilibili.com/video/BV18CL26WEJ3?p=15)

### 闭区间上连续函数的性质
- **要点**：在闭区间上连续的函数一定在该区间上有界，且一定能取到最大值与最小值（有界性与最值定理）；若 $f(x)$ 在 $[a,b]$ 上连续且 $f(a)$ 与 $f(b)$ 异号，则至少存在一点 $\xi\in(a,b)$ 使 $f(\xi)=0$（零点定理）；若 $f(a)=A$、$f(b)=B$，则对 $A$、$B$ 之间的任意数 $C$，至少存在一点 $\xi\in(a,b)$ 使 $f(\xi)=C$（介值定理）。
- **关键概念**：`有界性与最值定理`、`零点定理`、`介值定理`、`闭区间`、`异号`
- **相互关系**：介值定理是零点定理的推广（相当于把 $x$ 轴上下平移）；三者都依赖「闭区间」与「连续」这两个前提，缺一不可。
- **出处**：[石头 P15](https://www.bilibili.com/video/BV18CL26WEJ3?p=15)

### 函数在一点连续的判断
- **要点**：函数在 $x_0$ 处连续的充要条件是左极限、右极限与函数值三者相等，即 $\lim\_\{x\to x\_0\^-\}f(x)=\lim\_\{x\to x\_0\^+\}f(x)=f(x_0)$。判断分段函数在分段点处是否连续，就按左极限、右极限、函数值三项依次算出再比较，三项相同即连续。
- **关键概念**：`左极限`、`右极限`、`函数值`、`连续`、`$\lim_{x\to x_0^-}f(x)=\lim_{x\to x_0^+}f(x)=f(x_0)$`
- **相互关系**：是第二章「可导必连续」的前置结论；算单侧极限时常用等价无穷小（如 $x\to0^+$ 时 $\ln(1+x)\sim x$）与「$0\times$ 有界 $=0$」。
- **出处**：[石头 P16](https://www.bilibili.com/video/BV18CL26WEJ3?p=16)

### 由连续或已知间断点类型确定待定系数
- **要点**：已知分段函数在某点连续，就令左极限 $=$ 右极限 $=$ 函数值，解出待定常数；已知该点是可去间断点，只需令左极限 $=$ 右极限，即该点极限存在且为常数。当分母趋于零而极限要求等于常数时，分子必然也趋于零，由此定出系数。
- **关键概念**：`待定系数`、`可去间断点`、`极限存在`、`$\frac00$ 型`
- **相互关系**：与「间断点类型判断」互为逆向题——那里由函数判断类型，这里由类型反求参数；也是后续罗尔中值定理求参数的常用手法。
- **出处**：[石头 P16](https://www.bilibili.com/video/BV18CL26WEJ3?p=16)

### 间断点的个数判断
- **要点**：考试中数间断点个数，基本只需找使函数无定义的点，通常就是使分母为零的 $x$ 值，逐个列出即为个数。
- **关键概念**：`间断点`、`无定义`、`分母为零`
- **相互关系**：间断点本有三种情形（无定义、极限不存在、极限存在但不等于函数值），做这类题只用到第一种。
- **出处**：[石头 P16](https://www.bilibili.com/video/BV18CL26WEJ3?p=16)

### 间断点的类型判断
- **要点**：间断点分第一类（可去、跳跃）与第二类（无穷、振荡）。左、右极限都存在且相等为可去间断点；都存在但不相等为跳跃间断点；有一侧趋于无穷为无穷间断点；有一侧振荡为振荡间断点。
- **关键概念**：`第一类间断点`、`第二类间断点`、`可去`、`跳跃`、`无穷`、`振荡`
- **相互关系**：必须把左、右极限分开求，尤其 $\frac{1}{0^-}=-\infty$ 与 $\frac{1}{0^+}=+\infty$ 方向相反，很容易误判为相等；本质上是第一章左、右极限的应用。
- **出处**：[石头 P16](https://www.bilibili.com/video/BV18CL26WEJ3?p=16)

### 零点定理与证明方程至少有一个实根
- **要点**：若 $f(x)$ 在闭区间 $[a,b]$ 上连续且 $f(a)\cdot f(b)&lt;0$，则至少存在一点 $\xi\in(a,b)$ 使 $f(\xi)=0$。证明方程有实根分三步：先把方程整理成「某式 $=0$」并令 $f(x)=$ 该式，再求出两端点函数值 $f(a)$、$f(b)$，最后验证 $f(a)f(b)&lt;0$ 并引用零点定理。
- **关键概念**：`零点定理`、`$f(a)\cdot f(b)<0$`、`至少存在一点 $\xi$`、`构造函数`
- **相互关系**：结论形式与罗尔中值定理相似但含义不同——零点定理得 $f(\xi)=0$（函数值为零），罗尔定理得 $f'(\xi)=0$（导数值为零），两者极易混淆。
- **出处**：[石头 P16](https://www.bilibili.com/video/BV18CL26WEJ3?p=16)


## 二、导数与微分


### 导数的定义（两种定义式）
- **要点**：f′(x₀)=lim\_\{Δx→0\}[f(x₀+Δx)−f(x₀)]/Δx（增量式，由「路程对时间的瞬时速度」抽象而来）；定义式二 f′(x₀)=lim\_\{x→x₀\}[f(x)−f(x₀)]/(x−x₀)，其中 x₀ 必为常数（可为具体数字或参数 a、b），由定义式一令 x=x₀+Δx 得到。识别模型：分子是函数值之差、分母是自变量的差且恰为分子中自变量之差。学士帽把自变量变化量记作 Δx、因变量变化量记作 Δy=f(x₀+Δx)−f(x₀)，并指出导数即 Δy/Δx 在 Δx→0 时的极限值。
- **关键概念**：`增量`、`Δx`、`瞬时速度`、`x→x₀`
- **相互关系**：本质仍是求极限；凡分母出现 x−常数 的极限，优先考虑配成定义式二；Δx 可换成 h、t、1/n 等任意趋于零的字母。
- **出处**：[陈哥 P31](https://www.bilibili.com/video/BV1husGzwEtZ?p=31)、[P32](https://www.bilibili.com/video/BV1husGzwEtZ?p=32)；[杰哥 P30](https://www.bilibili.com/video/BV1Up4y1Y76a?p=30)；[米哥 P35](https://www.bilibili.com/video/BV1swAWerEzS?p=35)；[学士帽 P30](https://www.bilibili.com/video/BV1X4411J792?p=30)、[P31](https://www.bilibili.com/video/BV1X4411J792?p=31)、[P72](https://www.bilibili.com/video/BV1X4411J792?p=72)；[ok姐 P25](https://www.bilibili.com/video/BV1vm421s7mv?p=25)、[P26](https://www.bilibili.com/video/BV1vm421s7mv?p=26)

### 导数的记法与导函数
- **要点**：f′(x₀) 有三种等价写法：y′|\_\{x=x₀\}、dy/dx|\_\{x=x₀\}、df(x)/dx|\_\{x=x₀\}；极限存在即该点可导。若函数在开区间内每点可导，则构成的新函数称导函数，记 y′、f′(x)、dy/dx。高阶记法：一阶 y′、f′(x)、dy/dx；二阶 y″、f″(x)、d²y/dx²；n 阶 y\^\{(n)\}、f\^\{(n)\}(x)、dⁿy/dxⁿ。学士帽指出三种记号等价——挂撇形式为求导、带 d 形式为微分，二者含义相同。
- **关键概念**：`f′(x₀)`、`dy/dx`、`y^{(n)}`、`可导`、`导函数`
- **相互关系**：y^n 与 y\^\{(n)\} 含义完全不同——前者是 n 次幂，后者是 n 阶导数。
- **出处**：[陈哥 P31](https://www.bilibili.com/video/BV1husGzwEtZ?p=31)、[P40](https://www.bilibili.com/video/BV1husGzwEtZ?p=40)；[学士帽 P30](https://www.bilibili.com/video/BV1X4411J792?p=30)

### 导数的三个定义式与推广式
- **要点**：第一定义式分子两个 f 相减且含共同点 x₀；第二定义式分母即 x−x₀。推广式：lim\_\{Δx→0\}[f(x₀+AΔx)−f(x₀+BΔx)]/(CΔx)=[(A−B)/C]f′(x₀)，由分子加减 f(x₀) 拆项分别配成定义式一得到；若分子分母颠倒，结果取倒数；无 Δx 项系数取 0。逆用推广式先找共同点，再读系数。学士帽另给逆用形式：lim\_\{Δx→0\}[af(x₀+bΔx)−cf(x₀)]/(dΔx)=[(a−b)/d]f′(x₀)。
- **关键概念**：`第一定义式`、`推广式`、`第二定义式`、`拆项配凑`
- **相互关系**：专治「两个函数值之差」型极限，比逐项配凑快得多；若分子增量与分母增量「绝对相同」且「同时趋近于零」，极限必为 f′(x₀)。
- **出处**：[陈哥 P31](https://www.bilibili.com/video/BV1husGzwEtZ?p=31)、[P32](https://www.bilibili.com/video/BV1husGzwEtZ?p=32)；[杰哥 P30](https://www.bilibili.com/video/BV1Up4y1Y76a?p=30)；[学士帽 P31](https://www.bilibili.com/video/BV1X4411J792?p=31)、[P72](https://www.bilibili.com/video/BV1X4411J792?p=72)

### 一点处导数用定义求
- **要点**：只求一点处导数用定义法，不先求导函数（如 100 项连乘）；先算 f(x₀)（常因含因子零为 0）再约分求极限。连乘形式的多项式求 f′(0)：用定义式，约去 x 后代入，结果化为阶乘（负号个数决定符号）。
- **关键概念**：`定义法`、`阶乘`
- **出处**：[米哥 P35](https://www.bilibili.com/video/BV1swAWerEzS?p=35)；[杰哥 P31](https://www.bilibili.com/video/BV1Up4y1Y76a?p=31)

### 已知极限求导数 / 已知导数求极限
- **要点**：lim\_\{x→0\}f(x)/x=2 时分子必趋零，由连续得 f(0)=0，故 f′(0)=2；极限为无穷则得不出。反向题型拼凑定义式或配平分母系数：括号内一坨当整体框框，配成 f(□)/□。已知极限存在且等于常数求函数值或导数：由分母趋于零推分子趋于零得函数值，再由定义式得导数。
- **关键概念**：`拼凑定义式`、`整体思想`
- **出处**：[米哥 P36](https://www.bilibili.com/video/BV1swAWerEzS?p=36)；[杰哥 P31](https://www.bilibili.com/video/BV1Up4y1Y76a?p=31)

### 左导数、右导数与可导条件
- **要点**：f′_−(x₀)=lim\_\{x→x₀⁻\}[f(x)−f(x₀)]/(x−x₀)，右导数取 x→x₀⁺。函数在 x₀ 处可导 ⟺ 左导数与右导数都存在且相等；只要有一个不存在或二者不等，该点即不可导。只有三类函数在特定点处才需分别求左右导数：分段函数（含绝对值函数）、y=e\^\{1/x\}、y=arctan(1/x)。学士帽补充：分段函数在分段点求 f(x₀) 时，按该点所在的那一段表达式取值。
- **关键概念**：`左导数`、`右导数`、`可导的充要条件`、`分段点`
- **相互关系**：与「极限存在 ⟺ 左右极限存在且相等」完全类比；是判断分段点可导性的唯一手段，求左右导数时要分别选取两侧对应的表达式。
- **出处**：[陈哥 P33](https://www.bilibili.com/video/BV1husGzwEtZ?p=33)、[P42](https://www.bilibili.com/video/BV1husGzwEtZ?p=42)；[杰哥 P32](https://www.bilibili.com/video/BV1Up4y1Y76a?p=32)；[米哥 P38](https://www.bilibili.com/video/BV1swAWerEzS?p=38)；[学士帽 P34](https://www.bilibili.com/video/BV1X4411J792?p=34)、[P72](https://www.bilibili.com/video/BV1X4411J792?p=72)；[ok姐 P25](https://www.bilibili.com/video/BV1vm421s7mv?p=25)、[P26](https://www.bilibili.com/video/BV1vm421s7mv?p=26)

### 判断可导的充要条件（选择题）
- **要点**：看极限分子是否「动静结合」——一个动点 f(a+□) 减一个定点 f(a)；两点都在变化则错；只趋于单侧（如 Δx→0⁺）只是单侧导数，不能推出可导。
- **关键概念**：`动静结合`、`单侧导数`
- **出处**：[杰哥 P33](https://www.bilibili.com/video/BV1Up4y1Y76a?p=33)

### 两类不可导情形
- **要点**：①左导数不等于右导数（图像呈尖点，如 |x| 在 0 点）；②导数为无穷（如 y=x\^\{1/3\} 在 x=0）。几何上导数即切线斜率，尖点处左右斜率不同。
- **关键概念**：`尖点`、`导数为无穷`
- **出处**：[杰哥 P33](https://www.bilibili.com/video/BV1Up4y1Y76a?p=33)

### 可导、可微与连续的关系
- **要点**：可导必连续，连续不能推出可导（如 y=|x| 在 x=0 连续但左右导数不等），不连续一定不可导。可微与可导互为充要条件（一元函数中导数存在即微分存在），二者都能推出连续，连续推不出可微、可导。即可微（可导）是连续的充分条件，连续是可微（可导）的必要条件。证明：导数极限存在且分母趋于零，故分子趋于零，即极限值等于函数值。
- **关键概念**：`可导⇒连续`、`可微`、`充分条件`、`必要条件`
- **相互关系**：三者构成三角关系，是选填常考判断；读到「可导」应同时想到连续与左导=右导。
- **出处**：[陈哥 P33](https://www.bilibili.com/video/BV1husGzwEtZ?p=33)、[P35](https://www.bilibili.com/video/BV1husGzwEtZ?p=35)；[杰哥 P32](https://www.bilibili.com/video/BV1Up4y1Y76a?p=32)；[米哥 P39](https://www.bilibili.com/video/BV1swAWerEzS?p=39)；[学士帽 P35](https://www.bilibili.com/video/BV1X4411J792?p=35)

### 分段函数中求参数
- **要点**：求使分段函数在分段点可导的参数，套路是「先用连续的充要条件（左右极限相等且等于函数值）求出一部分参数，再用可导的充要条件（左右导数相等）求剩余参数」，单用其中一个条件无法解出全部参数。
- **关键概念**：`连续的充要条件`、`左右导数相等`、`分段点`
- **相互关系**：依赖「可导必连续」；过程中会用到复合函数求导与洛必达、等价无穷小（e^□−1~□、ln(1+□)~□）。
- **出处**：[陈哥 P33](https://www.bilibili.com/video/BV1husGzwEtZ?p=33)；[杰哥 P32](https://www.bilibili.com/video/BV1Up4y1Y76a?p=32)；[米哥 P39](https://www.bilibili.com/video/BV1swAWerEzS?p=39)

### 判断函数在某点是否可导
- **要点**：先算函数值与极限值判断连续性；再用定义算 f′(0)，其中 x²sin(1/x) 型借助零乘有界得导数存在且为零。
- **关键概念**：`零乘有界`
- **出处**：[杰哥 P32](https://www.bilibili.com/video/BV1Up4y1Y76a?p=32)

### 导数的几何意义与切线、法线方程
- **要点**：f′(x₀) 就是曲线 y=f(x) 在点 (x₀,f(x₀)) 处切线的斜率，k切=f′(x₀)，须先求一阶导再代入切点横坐标；割线斜率 Δy/Δx=[f(x)−f(x₀)]/(x−x₀)，令 x→x₀ 割线趋近切线。切线用点斜式 y−y₀=f′(x₀)(x−x₀)；法线斜率 k法=−1/f′(x₀)，方程形式相同只换斜率，两斜率乘积为 −1。切线不一定与曲线只有一个交点。学士帽补充：题目未给切点时先把两曲线联立求出切点；两直线平行则斜率相等，可由此反求参数；求斜率时若不会基本求导公式，可回用导数第二定义式求极限（如对 ln(x+1) 在 x=1 处），或直接用洛必达法则。
- **关键概念**：`切线斜率`、`割线`、`切点`、`点斜式`、`法线`
- **出处**：[陈哥 P34](https://www.bilibili.com/video/BV1husGzwEtZ?p=34)；[杰哥 P46](https://www.bilibili.com/video/BV1Up4y1Y76a?p=46)；[米哥 P51](https://www.bilibili.com/video/BV1swAWerEzS?p=51)；[学士帽 P32](https://www.bilibili.com/video/BV1X4411J792?p=32)、[P72](https://www.bilibili.com/video/BV1X4411J792?p=72)；[ok姐 P26](https://www.bilibili.com/video/BV1vm421s7mv?p=26)

### 切线的两种特例与由极限式反求切线
- **要点**：切线平行 x 轴时斜率为 0，切线为 y=f(x₀)、法线为 x=x₀；切线垂直于 x 轴时斜率不存在，切线为 x=x₀、法线为 y=f(x₀)，分别对应导数为 0 与导数不存在。题干只给一个极限式时，先把它配凑成导数定义式的形式求出 f′(x₀)（即斜率），再用点斜式写出切线方程。
- **关键概念**：`斜率为零`、`斜率不存在`、`配凑定义式`
- **出处**：[陈哥 P34](https://www.bilibili.com/video/BV1husGzwEtZ?p=34)

### 切点已知与切点未知两类题型
- **要点**：①切点已知：求导算斜率再套点斜式；曲线以参数方程给出时先由参数值算出切点，再用参数方程求导公式求斜率。②切点未知（只给切线过的点）：设切点为 (a,f(a))，写出含 a 的切线方程，再由题给条件解出 a 回代。点在曲线外时用「外点与切点连线斜率＝该点导数值」列方程。判断所给点是否为切点：切点必在曲线上。
- **关键概念**：`设切点`、`切点必在曲线上`、`回代`
- **相互关系**：设切点时纵坐标用 f(x₀) 表示，未知数越少越好。
- **出处**：[杰哥 P46](https://www.bilibili.com/video/BV1Up4y1Y76a?p=46)；[米哥 P51](https://www.bilibili.com/video/BV1swAWerEzS?p=51)；[ok姐 P26](https://www.bilibili.com/video/BV1vm421s7mv?p=26)

### 两条曲线相切
- **要点**：曲线 y=f(x) 与 y=g(x) 在 x₀ 处相切，等价于两点重合且切线相同，即 f(x₀)=g(x₀) 且 f′(x₀)=g′(x₀)。
- **关键概念**：`相切`、`公共点`、`公共切线`
- **相互关系**：常与隐函数、参数方程结合考综合题。
- **出处**：[陈哥 P34](https://www.bilibili.com/video/BV1husGzwEtZ?p=34)

### 导数的物理意义
- **要点**：运动方程 s=s(t) 时 s′(t₀) 为 t₀ 时刻的瞬时速度，再求一次导的 s″(t₀) 为该时刻加速度；求某时刻速度先求 s′ 再代入 t=t₀。
- **关键概念**：`运动方程`、`瞬时速度`、`加速度`
- **出处**：[学士帽 P33](https://www.bilibili.com/video/BV1X4411J792?p=33)

### 基本初等函数求导公式
- **要点**：共 16 个。常数导数为 0；x^a→ax\^\{a−1\}（最常考 x\^\{−1\}→−1/x²、√x→1/(2√x)）；a^x→a^x ln a，特别 e^x→e^x；log_a x→1/(x ln a)，特别 ln x→1/x；sin x→cos x、cos x→−sin x、tan x→sec²x、cot x→−csc²x、sec x→sec x tan x、csc x→−csc x cot x；arcsin x→1/√(1−x²)、arccos x 差一负号、arctan x→1/(1+x²)、arccot x 差一负号。记忆：含 c 的（cos、cot、csc、arccos、arccot）求导均添负号。
- **关键概念**：`幂函数`、`指数函数`、`三角函数`、`反三角函数`、`含 c 添负号`
- **相互关系**：全部可由导数定义式一配合等价无穷小推导；是后续一切求导与洛必达法则的计算基础；把分式、根式统一写成 x^a 再套幂函数公式。
- **出处**：[陈哥 P25](https://www.bilibili.com/video/BV1husGzwEtZ?p=25)、[P27](https://www.bilibili.com/video/BV1husGzwEtZ?p=27)、[P28](https://www.bilibili.com/video/BV1husGzwEtZ?p=28)、[P36](https://www.bilibili.com/video/BV1husGzwEtZ?p=36)；[杰哥 P34](https://www.bilibili.com/video/BV1Up4y1Y76a?p=34)；[米哥 P40](https://www.bilibili.com/video/BV1swAWerEzS?p=40)；[学士帽 P36](https://www.bilibili.com/video/BV1X4411J792?p=36)；[ok姐 P25](https://www.bilibili.com/video/BV1vm421s7mv?p=25)

### 导数的四则运算法则
- **要点**：(Cu)′=Cu′；(u±v)′=u′±v′；(uv)′=u′v+uv′（前导后不导加后导前不导）；(u/v)′=(u′v−uv′)/v²（上导下不导减下导上不导，分母平方，顺序不能颠倒）；三个函数相乘则轮流求导再相加。乘除不能像加减那样直接拆开。证恒等式常用「导数恒为零 ⇒ 函数恒为常数」。
- **关键概念**：`四则运算`、`前导后不导`、`分母平方`、`商的法则`
- **出处**：[陈哥 P36](https://www.bilibili.com/video/BV1husGzwEtZ?p=36)；[杰哥 P35](https://www.bilibili.com/video/BV1Up4y1Y76a?p=35)；[米哥 P41](https://www.bilibili.com/video/BV1swAWerEzS?p=41)；[学士帽 P37](https://www.bilibili.com/video/BV1X4411J792?p=37)、[P38](https://www.bilibili.com/video/BV1X4411J792?p=38)；[ok姐 P27](https://www.bilibili.com/video/BV1vm421s7mv?p=27)

### 复合函数求导（链式法则与方框法）
- **要点**：先把复合函数由外向内逐层拆成 y=f(u)、u=g(v)、v=φ(x)，各层分别求导后相乘，最后把中间变量替换回原表达式。y′_x=f′(u)g′(x)：外层对中间变量求导，再乘内层对自变量求导。熟练写法是方框法：把内层整体看作「方框」，外层求导后必须再乘方框的导数，层层向内直到最内层，如 ln□ 求导为 (1/□)·□′，√□ 求导为 1/(2√□)·□′；必须求到最里层，漏一层即错。学士帽补充：含乘积项时先用四则运算（前导后不导加前不导后导）拆分，结果要提公因式化简；易错点是分不清 sin x³ 与 (sin x)³ 的层次。
- **关键概念**：`复合函数`、`逐层求导`、`中间变量`、`方框`、`链式法则`
- **相互关系**：依赖第一章的复合函数拆分、基本求导公式与四则运算法则。
- **出处**：[陈哥 P37](https://www.bilibili.com/video/BV1husGzwEtZ?p=37)；[杰哥 P35](https://www.bilibili.com/video/BV1Up4y1Y76a?p=35)、[P37](https://www.bilibili.com/video/BV1Up4y1Y76a?p=37)；[米哥 P42](https://www.bilibili.com/video/BV1swAWerEzS?p=42)；[学士帽 P39](https://www.bilibili.com/video/BV1X4411J792?p=39)、[P72](https://www.bilibili.com/video/BV1X4411J792?p=72)；[ok姐 P28](https://www.bilibili.com/video/BV1vm421s7mv?p=28)

### 复合函数求导的化简技巧
- **要点**：遇到形如 ln(A/B) 的分式复合函数，先用对数性质化为 ln A−ln B 再求导；遇到含根号的分母，先用平方差公式做根式有理化，化为易求导形式后再求导。根号写 ½ 次方提到前面；见 e\^\{−x\} 上下同乘 e^x 化去分式。核心是避免对分式、根式直接求导。书写时把三角函数后面的因子提到前面，避免误看。
- **关键概念**：`对数相减`、`根式有理化`、`平方差公式`、`先化简再求导`
- **出处**：[陈哥 P37](https://www.bilibili.com/video/BV1husGzwEtZ?p=37)；[杰哥 P38](https://www.bilibili.com/video/BV1Up4y1Y76a?p=38)；[米哥 P45](https://www.bilibili.com/video/BV1swAWerEzS?p=45)

### 抽象函数求导
- **要点**：外层用 f′(·) 表示，如 [f(x²)]′=f′(x²)·2x；对 f 求导必须写成 f′（内层照抄），此点最易遗漏；求某点值先代入内层；两抽象函数相乘按乘积法则再各用链式法则。
- **关键概念**：`抽象函数`、`f′(·)`
- **出处**：[米哥 P43](https://www.bilibili.com/video/BV1swAWerEzS?p=43)；[杰哥 P37](https://www.bilibili.com/video/BV1Up4y1Y76a?p=37)

### 高阶导数
- **要点**：y″=d²y/dx²；三阶及以上不再加撇，统一记作 y\^\{(n)\}=dⁿy/dxⁿ（括号不可省）。若函数最高次幂为 n，则 n+1 阶导结果必为 0。通用方法是先求前 3~4 阶导数，观察系数、符号、指数的变化规律再归纳一般式。常见规律：(x e^x)\^\{(n)\}=(x+n)e^x；[ln(1+x)]\^\{(n)\}=(−1)\^\{n−1\}(n−1)!/(1+x)^n；[ln(2x+1)]\^\{(n)\}=(−1)\^\{n−1\}2^n(n−1)!/(2x+1)^n；(x^n)\^\{(n)\}=n!，幂函数求导次数超过其次数结果为 0；(1/x)\^\{(n)\}=(−1)^n n! x\^\{−(n+1)\}；(e^x)\^\{(n)\}=e^x；含 sin、cos 的函数求到 4 阶回归原形，按 4 的倍数归纳；(cos(ax+b))\^\{(n)\}=a^n cos(ax+b+nπ/2)；(1/(ax±b))\^\{(n)\}=(−1)^n a^n n!/(ax±b)\^\{n+1\}。含 cos²x 先用降幂 cos²x=½+½cos2x；含二次分式先用十字相乘分解再拆成两个一次分式之和。幂函数型（含 (x−a)^n）逐阶求导，每阶把指数系数累乘到前面；里层为一次式时导数为 1。
- **关键概念**：`二阶导`、`n 阶导`、`微分形式`、`找规律`、`递推`
- **相互关系**：题干指明求几阶导时逐次求导即可；若表达式由幂函数与指数函数相加构成，可只对能「扛住」这么多次求导的那一项求导，其余早已为 0。江苏一带考得多。
- **出处**：[陈哥 P38](https://www.bilibili.com/video/BV1husGzwEtZ?p=38)、[P40](https://www.bilibili.com/video/BV1husGzwEtZ?p=40)；[杰哥 P44](https://www.bilibili.com/video/BV1Up4y1Y76a?p=44)；[米哥 P50](https://www.bilibili.com/video/BV1swAWerEzS?p=50)；[学士帽 P40](https://www.bilibili.com/video/BV1X4411J792?p=40)；[ok姐 P29](https://www.bilibili.com/video/BV1vm421s7mv?p=29)；[帆哥 P1](https://www.bilibili.com/video/BV1xxXZBKENv?p=1)

### 微分的定义与计算
- **要点**：由 dy/dx=y′ 得 dy=y′dx（或 dy=f′(x)dx），dy 即微分；在 x₀ 处的微分 dy|\_\{x=x₀\}=f′(x₀)dx。求微分本质上就是求导数，结果后面必须带上 dx（自变量为 t 则乘 dt），不能省略；求某点微分则把该点代入导数后乘 dx。推广记 d□=□′dx。几何意义是用切线上纵坐标的增量近似代替函数值增量。可微与可导互为充要条件（一元函数中可微与可导等价）。隐函数求微分先用公式法求出 y′ 再加 dx。
- **关键概念**：`dy`、`dx`、`dy=y′dx`、`可微`、`微商`
- **相互关系**：dy 是 Δy 的线性主部；Δx→0 时 Δy 与 dy 是等价无穷小，故可用 dx 代替 Δx；由 dy=f′(x)dx 得 dy/dx=f′(x)，故导数也称「微商」；与后续积分是互逆过程，也是凑微分的依据。
- **出处**：[陈哥 P35](https://www.bilibili.com/video/BV1husGzwEtZ?p=35)；[杰哥 P45](https://www.bilibili.com/video/BV1Up4y1Y76a?p=45)；[米哥 P44](https://www.bilibili.com/video/BV1swAWerEzS?p=44)；[ok姐 P33](https://www.bilibili.com/video/BV1vm421s7mv?p=33)；[帆哥 P1](https://www.bilibili.com/video/BV1xxXZBKENv?p=1)

### 隐函数求导：公式法与直接求导法
- **要点**：见「方程」「…所确定」即判定为隐函数（口诀「非显即隐」）。公式法三步——①方程移项整理成 F(x,y)=0；②分别对 x、y 求导得 F_x、F_y（对 x 求导时把 y 当常数，对 y 求导时把 x 当常数，此时 x、y 是地位相同的变量）；③y′=−F_x/F_y。直接求导法：方程两边同时对 x 求导，遇到 y 时把 y 视为关于 x 的复合函数（y 求导写成 y′，xy 用乘积求导公式），再用四则运算法则整理，最后解出 y′（结果可同时含 x 与 y）。只求某点导数值时可直接代入 (x₀,y₀)，不必先解出 y′。
- **关键概念**：`F(x,y)`、`F_x`、`F_y`、`y′=−F_x/F_y`、`直接求导法`
- **相互关系**：两法结果必然一致；直接求导法求斜率、求切线时更快；易错：漏负号、上下写反；常考求指定点处导数值（需先代回原方程解出对应 y）。
- **出处**：[陈哥 P39](https://www.bilibili.com/video/BV1husGzwEtZ?p=39)；[杰哥 P40](https://www.bilibili.com/video/BV1Up4y1Y76a?p=40)；[米哥 P47](https://www.bilibili.com/video/BV1swAWerEzS?p=47)；[学士帽 P41](https://www.bilibili.com/video/BV1X4411J792?p=41)、[P72](https://www.bilibili.com/video/BV1X4411J792?p=72)、[P80](https://www.bilibili.com/video/BV1X4411J792?p=80)；[ok姐 P30](https://www.bilibili.com/video/BV1vm421s7mv?p=30)；[帆哥 P1](https://www.bilibili.com/video/BV1xxXZBKENv?p=1)

### 隐函数的切线方程
- **要点**：先用已知横坐标代入方程求出纵坐标确定切点，再求该点处的一阶导数作为切线斜率，最后用点斜式写出切线方程；求解时常直接用直接求导法并代入切点值。
- **关键概念**：`切点`、`切线斜率`、`点斜式`、`代入`
- **相互关系**：综合导数的几何意义与隐函数求导，是各省常考大题；与「导数的几何意义」联用，易错点是求完导函数忘记代点。
- **出处**：[陈哥 P39](https://www.bilibili.com/video/BV1husGzwEtZ?p=39)；[ok姐 P102](https://www.bilibili.com/video/BV1vm421s7mv?p=102)

### 参数方程求导（一阶与二阶）
- **要点**：一阶 dy/dx=(dy/dt)/(dx/dt)=y′(t)/x′(t)，做法是分子分母同除以 dt，把求导对象由 x 换成 t；问某 t=t₀ 处的导数值时先求一阶导再代入 t₀（先把 t 代入可避免化简出错）。二阶 d²y/dx²=[d/dt(y′)]/x′(t)，分子是一阶导再对 t 求一次导，分母仍是 x 对 t 求导，**不是**对 x 或对原函数求导，也不是两个一阶导相乘。
- **关键概念**：`参数方程`、`dy/dt`、`dx/dt`、`二阶导公式`、`上下同除 dt`
- **相互关系**：要求 x(t)、y(t) 可导且分母不为零；常见误区是把 x(t) 连续求两次导当作二阶导，这种做法完全错误；y(t) 为乘积形式时用乘法法则。
- **出处**：[陈哥 P40](https://www.bilibili.com/video/BV1husGzwEtZ?p=40)；[杰哥 P41](https://www.bilibili.com/video/BV1Up4y1Y76a?p=41)；[米哥 P46](https://www.bilibili.com/video/BV1swAWerEzS?p=46)；[学士帽 P42](https://www.bilibili.com/video/BV1X4411J792?p=42)、[P72](https://www.bilibili.com/video/BV1X4411J792?p=72)；[ok姐 P32](https://www.bilibili.com/video/BV1vm421s7mv?p=32)；[帆哥 P1](https://www.bilibili.com/video/BV1xxXZBKENv?p=1)

### 参数方程与隐函数结合的求导
- **要点**：若参数方程中 y 由一个含 y 与 t 的方程确定，则求 dy/dt 时要把 y 看作 t 的函数，按隐函数求导处理（可用直接求导法或公式法得 dy/dt=−F_t/F_y），再代入参数方程一阶导公式；注意上下字母对角对应。求某点处的值前，需先由原方程解出对应的 y₀。
- **关键概念**：`隐函数`、`直接求导法`、`公式法`
- **相互关系**：这类题同时考参数方程与隐函数两个知识点，综合性较强。
- **出处**：[陈哥 P40](https://www.bilibili.com/video/BV1husGzwEtZ?p=40)；[杰哥 P41](https://www.bilibili.com/video/BV1Up4y1Y76a?p=41)

### 参数方程曲线的切线与法线方程
- **要点**：先由给定 t 代入参数方程求出切点，再用参数方程一阶导求出该点处斜率 k，最后用点斜式写切线方程；法线斜率与切线斜率互为负倒数。
- **关键概念**：`切点`、`切线斜率`、`点斜式`、`法线`
- **出处**：[陈哥 P40](https://www.bilibili.com/video/BV1husGzwEtZ?p=40)；[杰哥 P46](https://www.bilibili.com/video/BV1Up4y1Y76a?p=46)

### 幂指函数的识别与两种求导方法
- **要点**：底数与指数都是函数、形如 y=f(x)\^\{g(x)\} 的函数叫幂指函数，既不能当幂函数也不能当指数函数直接套公式（u^v 没有直接求导公式，必须变形）。方法一（公式变形法）：利用 a^b=e\^\{b ln a\} 写成 e\^\{g(x)ln f(x)\}，外层是指数函数、内层是乘积，按复合函数求导，化简时再还原成 f^g。方法二（对数求导法）：两边取对数得 ln y=g(x)ln f(x)，化为乘积结构，再按隐函数的直接求导法求导（左边为 (1/y)y′，勿漏 y′），最后把 y 乘回右边。两法等价。学士帽指出对数求导法同样适用于多因式连乘（含乘除、开方）的函数。
- **关键概念**：`幂指函数`、`u^v`、`e^{b ln a}`、`对数求导法`
- **相互关系**：与幂函数（底为常数）、指数函数（指数为常数）区分开。
- **出处**：[陈哥 P41](https://www.bilibili.com/video/BV1husGzwEtZ?p=41)；[杰哥 P42](https://www.bilibili.com/video/BV1Up4y1Y76a?p=42)；[米哥 P49](https://www.bilibili.com/video/BV1swAWerEzS?p=49)；[学士帽 P43](https://www.bilibili.com/video/BV1X4411J792?p=43)；[ok姐 P31](https://www.bilibili.com/video/BV1vm421s7mv?p=31)

### 幂指函数两种求导方法的选择
- **要点**：①单独的 y=u^v 两法皆可；②单独的 u^v 但含连乘、连除或根式，首选对数求导法（乘变加、除变减）；③u^v 与其它函数加减组合时只能用公式变形法；④与其他函数相乘或相加减时须先把幂指函数「单拎出来」令 z=u^v 单独求导再代回。取对数必须对整边取，不可把 ln[u^v±g(x)] 拆成两项。
- **关键概念**：`连乘连除`、`整体取对数`
- **出处**：[杰哥 P42](https://www.bilibili.com/video/BV1Up4y1Y76a?p=42)；[ok姐 P31](https://www.bilibili.com/video/BV1vm421s7mv?p=31)

### 连乘式（多因子乘除、开方）的求导
- **要点**：形如多个函数相乘相除、带平方或开方的式子，只能用对数求导法：两边取对数 → 用对数三公式把乘除化为加减、把方根化为系数（√[n]{u}=u\^\{1/n\}）→ 两边求导 → 乘回 y。
- **关键概念**：`对数求导法`、`√[n]{u}=u^{1/n}`
- **相互关系**：取对数前先把根号写成 1/n 次方并把幂提到系数位置；拆分减法时要把被减的整体加括号，避免符号错误。
- **出处**：[陈哥 P41](https://www.bilibili.com/video/BV1husGzwEtZ?p=41)

### 分段函数求导的两步法
- **要点**：非分段点用公式求导；分段点处必须用左右导数的定义求导（分别算左右导数）再判是否相等；最后综合写成分段形式。若分段点两侧的表达式相同，则不必分别求左右导数，直接按定义求该点导数即可。
- **关键概念**：`分段点`、`左右导数定义`、`求导法则`
- **相互关系**：此类题中 lim\_\{x→0\}sin(1/x) 属振荡型、极限不存在，故该点不可导；典型如含 x cos(2/x) 的题：极限用零乘有界为零，而右导数因 cos(2/x) 在 x→0 时振荡不存在，故不可导。分段函数综合题的选项常同时涉及极限、连续、可导，需依次算出左极限＝右极限＝函数值（连续），再算左导、右导判断可导。
- **出处**：[陈哥 P42](https://www.bilibili.com/video/BV1husGzwEtZ?p=42)；[杰哥 P39](https://www.bilibili.com/video/BV1Up4y1Y76a?p=39)；[米哥 P48](https://www.bilibili.com/video/BV1swAWerEzS?p=48)


### 导数的定义式
- **要点**：从平均速度 $\frac{\Delta s}{\Delta t}$ 出发，把时间间隔取得越来越短并令其趋于零，所得极限就是瞬时速度；一般化为函数即 $f'(x_0)=\lim\_\{\Delta x\to0\}\frac{f(x_0+\Delta x)-f(x_0)}{\Delta x}$。该极限存在则称函数在 $x_0$ 处可导，极限值即这一点的导数；几何上它是曲线在该点切线的斜率。
- **关键概念**：`平均速度`、`瞬时速度`、`$f'(x_0)$`、`$\lim_{\Delta x\to0}$`、`切线斜率`
- **相互关系**：导数本质是一个极限，第一章的极限理论是本章的前提；导数记作 $f'(x_0)$，撇号位置不能写成 $f(x_0)'$。
- **出处**：[石头 P17](https://www.bilibili.com/video/BV18CL26WEJ3?p=17)

### 导数的三种等价形式
- **要点**：$f'(x_0)=\lim\_\{\Delta x\to0\}\frac{f(x_0+\Delta x)-f(x_0)}{\Delta x}=\lim\_\{x\to x\_0\}\frac{f(x)-f(x_0)}{x-x_0}=\lim\_\{h\to0\}\frac{f(x_0+h)-f(x_0)}{h}$。三种写法只是把增量符号 $\Delta x$ 换成 $x-x_0$ 或 $h$，含义完全相同。
- **关键概念**：`三种等价形式`、`$\Delta x=x-x_0$`、`$h$ 记法`
- **相互关系**：$\Delta x\to0$ 与 $x\to x_0$ 是同一过程的两种写法；做题时先把待求式子往定义式上「靠」，找出不同再逐一改。
- **出处**：[石头 P17](https://www.bilibili.com/video/BV18CL26WEJ3?p=17)

### 定义式中的对应关系与系数规律
- **要点**：定义式有三处必须对应：三个 $x_0$ 要一致，三处增量符号（$\Delta x$、$h$ 或 $x$）也要一致，全部对应时结果就是 $f'(x_0)$。若分子增量前的系数为 $a$、分母为 $b$，则原式等于 $\frac{a}{b}f'(x_0)$；常见特例 $\lim\_\{h\to0\}\frac{f(h)-f(-h)}{h}=2f'(0)$。
- **关键概念**：`三个 $x_0$ 对应`、`增量对应`、`$\frac{a}{b}f'(x_0)$`、`$2f'(0)$`
- **相互关系**：命题常把 $h$ 换成 $x$、$2h$、$3h$ 或把分母换成 $6h$ 来设陷阱；不对应时先凑成对应，再把多出的系数补回来。
- **出处**：[石头 P17](https://www.bilibili.com/video/BV18CL26WEJ3?p=17)

### 导函数的定义与用定义求导
- **要点**：若函数在开区间内每一点都可导，则每点的导数值构成一个新函数，称为导函数，记作 $y'$、$f'(x)$ 或 $\frac{\mathrm{d}y}{\mathrm{d}x}$，只需把定义式中的 $x_0$ 换成 $x$。用定义可算出 $(x^2)'=2x$、$(e^x)'=e^x$。
- **关键概念**：`导函数`、`$f'(x)$`、`$\frac{\mathrm{d}y}{\mathrm{d}x}$`、`$\mathrm{d}$ 表示微观`
- **相互关系**：求极限时变化的是 $h$、$x$ 视为常数，这是理解定义式求导的关键；$\Delta$ 表示宏观增量、$\mathrm{d}$ 表示微观增量。
- **出处**：[石头 P17](https://www.bilibili.com/video/BV18CL26WEJ3?p=17)

### 左导数与右导数
- **要点**：导数作为极限，其左、右极限分别称为左导数 $f'_-(x_0)=\lim\_\{x\to x\_0\^-\}\frac{f(x)-f(x_0)}{x-x_0}$ 与右导数 $f'_+(x_0)=\lim\_\{x\to x\_0\^+\}\frac{f(x)-f(x_0)}{x-x_0}$。求分段函数在分段点处的导数，必须用定义式分左右两侧分别求。
- **关键概念**：`左导数`、`右导数`、`$f'_-(x_0)$`、`$f'_+(x_0)$`、`单侧导数`
- **相互关系**：与第一章的左、右极限完全对应，是判断分段点可导性的唯一严格工具，也是后面分段函数求导一节的基础。
- **出处**：[石头 P18](https://www.bilibili.com/video/BV18CL26WEJ3?p=18)

### 可导的充要条件与分段函数的可导性
- **要点**：$f(x)$ 在 $x_0$ 处可导的充要条件是左导数与右导数都存在且相等，即 $f'_-(x_0)=f'_+(x_0)$。据此判断分段函数：两侧导数都存在且相等则可导，任一侧不存在或二者不等则不可导。
- **关键概念**：`充要条件`、`$f'_-(x_0)=f'_+(x_0)$`、`分段点`
- **相互关系**：如 $y=\sin x\ (x\le0)$ 与 $y=\ln(1+x)\ (x>0)$ 在 $0$ 点两侧导数都为 $1$，故可导；而 $y=|x|$ 在 $0$ 点左导数为 $-1$、右导数为 $1$，故不可导。
- **出处**：[石头 P18](https://www.bilibili.com/video/BV18CL26WEJ3?p=18)

### 可导与连续的关系
- **要点**：可导必连续，连续不一定可导；不连续一定不可导，不可导不一定不连续。几何上可导要求曲线在该点不仅连续而且光滑，出现尖点即不可导。
- **关键概念**：`可导必连续`、`连续不一定可导`、`不连续一定不可导`、`尖点`
- **相互关系**：由原命题与逆否命题同真，得「不连续 $\Rightarrow$ 不可导」成立，而逆命题「连续 $\Rightarrow$ 可导」与否命题「不可导 $\Rightarrow$ 不连续」都不成立；函数在某点不连续时其极限可能存在也可能不存在。
- **出处**：[石头 P18](https://www.bilibili.com/video/BV18CL26WEJ3?p=18)

### 基本导数公式表
- **要点**：必记六个公式：$(C)'=0$、$(x^\mu)'=\mu x\^\{\mu-1\}$（$\mu$ 为任意实数）、$(e^x)'=e^x$、$(\ln x)'=\frac1x$、$(\sin x)'=\cos x$、$(\cos x)'=-\sin x$。第二组建议记：$(\tan x)'=\frac{1}{\cos^2x}=\sec^2x$、$(\cot x)'=-\frac{1}{\sin^2x}=-\csc^2x$、$(\arcsin x)'=\frac{1}{\sqrt{1-x^2}}$、$(\arccos x)'=-\frac{1}{\sqrt{1-x^2}}$。第三组可记可不记：$(\sec x)'=\sec x\tan x$、$(\csc x)'=-\csc x\cot x$、$(\arctan x)'=\frac{1}{1+x^2}$、$(\mathrm{arccot}\,x)'=-\frac{1}{1+x^2}$。
- **关键概念**：`基本导数公式表`、`$(x^\mu)'=\mu x^{\mu-1}$`、`$(\sin x)'=\cos x$`、`$(\tan x)'=\sec^2x$`
- **相互关系**：记忆规律是带「余」字的（$\cos$、$\cot$、$\csc$、$\arccos$、$\mathrm{arccot}$）求导都带负号，带「正」字的不带负号；这些公式也直接决定微分公式表。
- **出处**：[石头 P19](https://www.bilibili.com/video/BV18CL26WEJ3?p=19)

### 四则运算求导法则
- **要点**：$(u\pm v)'=u'\pm v'$，$(Cu)'=Cu'$，$(uv)'=u'v+uv'$（前导后不导加后导前不导），$\left(\frac uv\right)'=\frac{u'v-uv'}{v^2}$（上导下不导减下导上不导，除以分母平方）。四式都以 $u$、$v$ 可导为前提。
- **关键概念**：`四则运算求导法则`、`$(uv)'=u'v+uv'$`、`$\left(\frac uv\right)'=\frac{u'v-uv'}{v^2}$`
- **相互关系**：和差与常数倍相当于「直接去掉括号」；乘积法则可由面积增量法（几何法）证明，除法法则可由乘积法则移项推出，二者也用于证明其他导数公式。
- **出处**：[石头 P19](https://www.bilibili.com/video/BV18CL26WEJ3?p=19)

### 基本初等函数求导
- **要点**：由基本初等函数经加减乘除构成的函数，直接用基本导数公式表加四则运算法则逐项求导即可。特别注意 $\sin\frac\pi2$、$\cos\frac\pi2$ 这类是常数，求导结果为零，不要当成函数再求导。
- **关键概念**：`基本初等函数`、`逐项求导`、`常数求导为零`
- **相互关系**：要区分 $f'(\frac\pi2)$（先求导函数再代点）与 $\left[f(\frac\pi2)\right]'$（先代点得常数，求导为零），撇号位置写错是高频失分点。
- **出处**：[石头 P20](https://www.bilibili.com/video/BV18CL26WEJ3?p=20)

### 反函数求导法则
- **要点**：反函数的导数等于原函数导数的倒数，即 $\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{1}{\frac{\mathrm{d}x}{\mathrm{d}y}}$。用法是先写成 $x=\varphi(y)$ 形式并求出 $\frac{\mathrm{d}x}{\mathrm{d}y}$，取倒数后再把 $y$ 换回用 $x$ 表示；注意不要改写 $x=\sin y$ 这类已定形式。
- **关键概念**：`反函数求导法则`、`$\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{1}{\frac{\mathrm{d}x}{\mathrm{d}y}}$`、`互为倒数`
- **相互关系**：用它可把 $(x^\mu)'=\mu x\^\{\mu-1\}$ 从整数指数推广到分数指数，也可证明 $(\ln x)'=\frac1x$、$(\arcsin x)'=\frac{1}{\sqrt{1-x^2}}$；专升本直接考它的概率很低。
- **出处**：[石头 P21](https://www.bilibili.com/video/BV18CL26WEJ3?p=21)

### 复合函数求导法则
- **要点**：设 $y=f(u)$、$u=g(x)$ 都可导，则 $\frac{\mathrm{d}y}{\mathrm{d}x}=f'(u)\cdot g'(x)$，即外层求导乘以内层求导，顺序由外向内一层层相乘。算完后必须把中间变量 $u$、$v$ 换回用 $x$ 表示的表达式。
- **关键概念**：`复合函数求导法则`、`链式法则`、`外层求导`、`内层求导`、`$\frac{\mathrm{d}y}{\mathrm{d}u}\cdot\frac{\mathrm{d}u}{\mathrm{d}x}$`
- **相互关系**：关键是分清内外层，考试最多考到三层复合；借助 $x^\mu=e\^\{\mu\ln x\}$ 的恒等变形配合本法，可一次性证明 $(x^\mu)'=\mu x\^\{\mu-1\}\ (x>0)$。
- **出处**：[石头 P22](https://www.bilibili.com/video/BV18CL26WEJ3?p=22)

### 分段函数求导
- **要点**：口诀是「分段点两边分别求，中间分段点单独求」——两侧区间内用公式正常求导，分段点处必须用导数定义式求左导数与右导数，二者存在且相等时该点导数才存在，否则结果写「不存在」。
- **关键概念**：`分段点`、`左导数`、`右导数`、`导数不存在`
- **相互关系**：若两侧导函数在分段点代入后不相等，可直接判定该点不可导；若代入后相等，还需先确认原函数在该点连续，才能认定导数存在。
- **出处**：[石头 P23](https://www.bilibili.com/video/BV18CL26WEJ3?p=23)

### 隐函数求导
- **要点**：方程确定的隐函数，方法是对等式两边同时求导，再把 $y'$ 解出来。核心是牢记方程中的 $y$ 是 $x$ 的函数，凡遇含 $y$ 的项都按复合函数求导，如 $(e^y)'=e^y\cdot y'$、$(\ln y)'=\frac{y'}{y}$、$(xy)'=y+xy'$。
- **关键概念**：`隐函数`、`两边同时求导`、`$y$ 是 $x$ 的函数`、`解出 $y'$`
- **相互关系**：求某点处的导数值时，先求整体导函数再代入该点；若结果中仍含 $y$，要用原方程把该点对应的 $y$ 解出来再代入。
- **出处**：[石头 P24](https://www.bilibili.com/video/BV18CL26WEJ3?p=24)

### 参数方程确定的函数求导
- **要点**：由 $\begin{cases}x=\varphi(t)\\y=\psi(t)\end{cases}$ 确定的函数，求导三步：先求 $\frac{\mathrm{d}y}{\mathrm{d}t}$，再求 $\frac{\mathrm{d}x}{\mathrm{d}t}$，最后两者相除得 $\frac{\mathrm{d}y}{\mathrm{d}x}=\dfrac{\mathrm{d}y/\mathrm{d}t}{\mathrm{d}x/\mathrm{d}t}$。求某点处的导数值时，把参数值代入最终表达式。
- **关键概念**：`参数方程`、`$\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{\mathrm{d}y/\mathrm{d}t}{\mathrm{d}x/\mathrm{d}t}$`、`三步法`
- **相互关系**：求导过程中 $t$ 是自变量、$x$ 与 $y$ 都是 $t$ 的函数；结果必须化简，通常能把 $t$ 约掉，是本章考试频次较高的一类。
- **出处**：[石头 P25](https://www.bilibili.com/video/BV18CL26WEJ3?p=25)

### 幂指函数与对数求导法
- **要点**：底数与指数都含自变量的函数称幂指函数（如 $x^x$、$x\^\{\sin x\}$、$(1+2x)\^\{\cos x\}$），用对数求导法：两边取对数，把指数提为系数化为 $\ln y=v(x)\ln u(x)$，再两边求导解出 $y'$，最后把 $y$ 换回原式。多因子积、商、乘方、开方构成的函数也用同一方法，取对数后可化乘除为加减、化乘方开方为系数。
- **关键概念**：`幂指函数`、`对数求导法`、`两边取对数`、`化乘除为加减`、`化乘方开方为系数`
- **相互关系**：取对数后剩下的就是隐函数求导与复合函数求导，相当于只多了一步；题目给出 $x>0$、$y>0$ 之类范围只是为保证取对数合法，不必额外讨论。
- **出处**：[石头 P26](https://www.bilibili.com/video/BV18CL26WEJ3?p=26)、[P27](https://www.bilibili.com/video/BV18CL26WEJ3?p=27)

### 高阶导数的概念与记号
- **要点**：对一阶导数再求导得二阶导数，记作 $y''$、$f''(x)$ 或 $\frac{\mathrm{d}^2y}{\mathrm{d}x^2}$；继续求导得三阶导数 $y'''$。从四阶开始不再打撇，写成 $y\^\{(4)\}$、$y\^\{(n)\}$、$\frac{\mathrm{d}^ny}{\mathrm{d}x^n}$，小括号不能省，否则会与 $y$ 的四次方混淆。
- **关键概念**：`二阶导数`、`$y''$`、`$\frac{\mathrm{d}^2y}{\mathrm{d}x^2}$`、`$y^{(n)}$`、`$n$ 阶导数`
- **相互关系**：求二阶、三阶时逐阶往下求即可；求三阶以上（如 $2025$ 阶）必须用高阶导数公式，不能逐阶硬求。
- **出处**：[石头 P28](https://www.bilibili.com/video/BV18CL26WEJ3?p=28)

### 常用高阶导数公式
- **要点**：$(x^n)\^\{(n)\}=n!$（求导阶数等于幂次时结果为常数），求导阶数大于幂次时结果为 $0$；$(e^x)\^\{(n)\}=e^x$；$(\ln x)\^\{(n)\}=\frac{(-1)\^\{n-1\}(n-1)!}{x^n}$；$\sin x$ 与 $\cos x$ 的 $n$ 阶导数以四阶为一组循环，用阶数除以 $4$ 看余数依次对应 $\sin x$、$\cos x$、$-\sin x$、$-\cos x$。
- **关键概念**：`阶乘`、`$(x^n)^{(n)}=n!$`、`$(e^x)^{(n)}=e^x$`、`四阶循环`
- **相互关系**：这些公式不必死记，能自己推出来即可；幂函数与指数函数的结论可直接用于高阶求导题，如 $x\^\{2000\}+e^x+\cos x$ 的 $2025$ 阶导为 $e^x-\sin x$。
- **出处**：[石头 P28](https://www.bilibili.com/video/BV18CL26WEJ3?p=28)

### 参数方程确定的函数的二阶导数
- **要点**：先用三步法求出 $\frac{\mathrm{d}y}{\mathrm{d}x}$（它是 $t$ 的函数），再把这个结果关于 $t$ 求导得 $\frac{\mathrm{d}y'}{\mathrm{d}t}$，最后除以 $\frac{\mathrm{d}x}{\mathrm{d}t}$，即 $\frac{\mathrm{d}^2y}{\mathrm{d}x^2}=\dfrac{\mathrm{d}y'/\mathrm{d}t}{\mathrm{d}x/\mathrm{d}t}$。
- **关键概念**：`二阶导数`、`$\frac{\mathrm{d}^2y}{\mathrm{d}x^2}=\frac{\mathrm{d}y'/\mathrm{d}t}{\mathrm{d}x/\mathrm{d}t}$`、`三板斧加两步`
- **相互关系**：一阶导函数 $\frac{\mathrm{d}y}{\mathrm{d}x}$ 与 $x=\varphi(t)$ 又构成一个新的参数方程，所以仍用三步法；书上给的长公式不必背。
- **出处**：[石头 P28](https://www.bilibili.com/video/BV18CL26WEJ3?p=28)

### 导数定义式变形与先化简再求导
- **要点**：遇到与定义式结构相近但系数、增量形式不同的极限，按「三处对应」凑出 $f'(x_0)$ 再补系数；遇到分子分母都带根式等复杂分式，先用有理化（平方差公式）化简再求导，可大幅降低计算量；对 $F(\text{某点})$ 整体求导时先判断它是常数，结果为零。
- **关键概念**：`三处对应`、`根式有理化`、`平方差公式`、`常数求导为零`
- **相互关系**：对数求导法只适用于乘除关系，加减关系不能取对数；先看能否化简再决定方法，是本章做题的通用策略。
- **出处**：[石头 P29](https://www.bilibili.com/video/BV18CL26WEJ3?p=29)

### 微分的定义
- **要点**：函数增量可写成 $\Delta y=A\Delta x+o(\Delta x)$，舍去高阶无穷小后得 $\mathrm{d}y=A\mathrm{d}x$，其中 $A=f'(x)$，故 $\mathrm{d}y=f'(x)\mathrm{d}x$。$\mathrm{d}x$ 称自变量的微分，$\mathrm{d}y$ 称函数的微分；微分就是导数的乘积形式，导数也因此被称为微商。
- **关键概念**：`微分`、`$\mathrm{d}y=f'(x)\mathrm{d}x$`、`高阶无穷小`、`微商`
- **相互关系**：用边长 $x$ 的正方形面积增量 $\Delta y=2x\Delta x+(\Delta x)^2$ 可直观看到主部 $2x\Delta x$ 就是微分，高阶项 $(\Delta x)^2$ 被忽略；圆的面积微分为周长 $2\pi R\,\mathrm{d}R$、球的体积微分为表面积 $4\pi R^2\,\mathrm{d}R$ 也是同一道理。
- **出处**：[石头 P30](https://www.bilibili.com/video/BV18CL26WEJ3?p=30)

### 可微与可导的等价
- **要点**：函数在某点可微与可导是等价的，可导必可微、可微必可导，所以不必单独判断可微性，求出导数即可写出微分。
- **关键概念**：`可微`、`可导`、`等价`
- **相互关系**：正因为二者等价，微分公式表与运算法则和导数完全一致，只需在导数后面乘上 $\mathrm{d}x$。
- **出处**：[石头 P30](https://www.bilibili.com/video/BV18CL26WEJ3?p=30)

### 微分公式与运算法则
- **要点**：$\mathrm{d}(u\pm v)=\mathrm{d}u\pm\mathrm{d}v$，$\mathrm{d}(uv)=v\,\mathrm{d}u+u\,\mathrm{d}v$，$\mathrm{d}\left(\frac uv\right)=\frac{v\,\mathrm{d}u-u\,\mathrm{d}v}{v^2}$，复合函数微分为外层导数乘以内层导数再乘 $\mathrm{d}x$。典型计算如 $\mathrm{d}(5x^3)=15x^2\mathrm{d}x$、$\mathrm{d}(\cos 2x)=-\sin 2x\,\mathrm{d}(2x)=-2\sin 2x\,\mathrm{d}x$、$\mathrm{d}(\ln x^2)=\frac{1}{x^2}\mathrm{d}(x^2)=\frac{2}{x}\mathrm{d}x$。
- **关键概念**：`微分公式`、`微分形式不变性`、`$\mathrm{d}(\cos u)=-\sin u\,\mathrm{d}u$`
- **相互关系**：微分形式不变性指无论 $u$ 是自变量还是中间变量，$\mathrm{d}f(u)=f'(u)\mathrm{d}u$ 都成立；反向由微分求原函数已接近积分，是下一章积分的铺垫。
- **出处**：[石头 P30](https://www.bilibili.com/video/BV18CL26WEJ3?p=30)


## 三、微分中值定理与导数应用


### 费马引理（极值的必要条件）
- **要点**：若函数在 x₀ 处可导且在该点取极值，则必有 f′(x₀)=0；几何意义是曲线在极值点处有水平切线。故极值点只可能出现在驻点与不可导点两类点上。
- **关键概念**：`费马引理`、`极值的必要条件`、`可导`、`驻点`、`不可导点`
- **相互关系**：只是必要条件，反之不成立（y=x³ 在 x=0 处导数为零但非极值点）；若该点不可导（如 |x| 的尖点）结论不成立；是罗尔定理的证明工具；已知「某点取极值」求参数时，直接令该点导数为零，注意前提是该点可导。
- **出处**：[陈哥 P46](https://www.bilibili.com/video/BV1husGzwEtZ?p=46)；[ok姐 P34](https://www.bilibili.com/video/BV1vm421s7mv?p=34)、[P42](https://www.bilibili.com/video/BV1vm421s7mv?p=42)

### 罗尔定理
- **要点**：三条件——在 [a,b] 上连续、在 (a,b) 内可导、端点值相等 f(a)=f(b)；结论为至少存在一点 ξ∈(a,b) 使 f′(ξ)=0；几何意义是区间内至少有一条平行于 x 轴的切线。题型一：求满足定理的 ξ——先求导函数，令其为零解出 x，取落在给定开区间内的那个值；题型二：求表达式中的常数——只利用条件 f(a)=f(b)，把端点函数值算出来令其相等求解。
- **关键概念**：`闭区间连续`、`开区间可导`、`端点值相等`、`水平切线`、`ξ`
- **相互关系**：是拉格朗日中值定理的特例；广东升本考频很低，前两个条件一般不必验证。
- **出处**：[陈哥 P131](https://www.bilibili.com/video/BV1husGzwEtZ?p=131)；[学士帽 P44](https://www.bilibili.com/video/BV1X4411J792?p=44)；[ok姐 P34](https://www.bilibili.com/video/BV1vm421s7mv?p=34)

### 拉格朗日中值定理
- **要点**：条件只有两个——在 [a,b] 上连续、在 (a,b) 内可导（不要求端点值相等）；结论为至少存在一点 ξ∈(a,b) 使 f′(ξ)=[f(b)−f(a)]/(b−a)，或写成 f(b)−f(a)=f′(ξ)(b−a)。几何意义：曲线上至少存在一点，其切线平行于弦 AB（弦的斜率即 [f(b)−f(a)]/(b−a)）；若 f(a)=f(b)，弦水平、斜率为零，结论退化为 f′(ξ)=0，即罗尔定理。
- **关键概念**：`闭区间连续`、`开区间可导`、`切线平行于弦`、`弦的斜率`
- **相互关系**：罗尔定理是拉格朗日中值定理在端点函数值相等时的特例，拉格朗日中值定理是罗尔定理的推广。对应题型为求满足定理的 ξ——求导函数与两端点函数值，代入公式解方程。
- **出处**：[陈哥 P134](https://www.bilibili.com/video/BV1husGzwEtZ?p=134)；[学士帽 P45](https://www.bilibili.com/video/BV1X4411J792?p=45)；[ok姐 P35](https://www.bilibili.com/video/BV1vm421s7mv?p=35)

### 中值定理的两种题型（选择题）
- **要点**：选择题用排除法——先验证端点值，再用「使分母为零的点不连续、使绝对值为零的点不可导」，分段函数还需验证分段点处函数值与极限值是否相等；填空题求 ξ：先求一阶导，再把 ξ 代入定理结论的等式解方程，ξ 必须落在开区间内，等于端点的值舍去。学士帽补充：求解 ξ 时常需把常数项化成 ln e 后再用对数运算法则合并。
- **关键概念**：`排除法`、`不连续点`、`不可导点`
- **出处**：[学士帽 P44](https://www.bilibili.com/video/BV1X4411J792?p=44)、[P45](https://www.bilibili.com/video/BV1X4411J792?p=45)

### 常函数定理与证明恒等式
- **要点**：若函数在区间上连续、可导且导数恒为零，则该函数在区间上为常数；反之常函数的导数恒为零。证明「当 x>0 时某含 x 的表达式恒等于常数」时，构造该表达式为新函数 G(x)，求导化简证 G′(x)≡0 得 G(x) 为常函数，再取便于计算的自变量值（如 x=1）算出该常数，最后点题。
- **关键概念**：`导数恒为零`、`构造函数`、`取特殊值`
- **出处**：[ok姐 P36](https://www.bilibili.com/video/BV1vm421s7mv?p=36)

### 一阶导与单调性的判定定理
- **要点**：设 f(x) 在 [a,b] 上连续、在 (a,b) 内可导：f′(x)>0 则单调递增，f′(x)&lt;0 则单调递减，f′(x)=0 则 f(x) 为常数。若 f′(x)≥0（仅有限个点等于零）则单调增加；若 f′(x)≤0（仅有限个点等于零）则单调减少。
- **关键概念**：`一阶导`、`单调性`、`单调增区间`、`单调减区间`
- **相互关系**：由「曲线上升 ⇒ 切线斜率非负 ⇒ 一阶导非负」的几何直观推出，是整个导数应用章节的基础。
- **出处**：[陈哥 P44](https://www.bilibili.com/video/BV1husGzwEtZ?p=44)；[米哥 P52](https://www.bilibili.com/video/BV1swAWerEzS?p=52)；[ok姐 P38](https://www.bilibili.com/video/BV1vm421s7mv?p=38)

### 严格单调递增与单调不减的区分
- **要点**：f′(x)>0 ⇒ 严格单调递增；f′(x)≥0 且 f′(x)=0 的点是孤立的（有限个、不构成区间）时仍是严格单调递增；若 f′(x)=0 在某区间上恒成立，则只能说单调不减（出现水平段）。例：y=x³ 仅在 x=0 处导数为零，仍严格单调递增。考试不考术语辨析。
- **关键概念**：`严格单调递增`、`单调不减`
- **出处**：[陈哥 P44](https://www.bilibili.com/video/BV1husGzwEtZ?p=44)

### 由条件式判定单调性的题型
- **要点**：题干给出 [x f(x)]′ 或 (f(x)/x)′ 的符号条件时，先对该组合函数求导并化到与题干条件一致的形式，由导数符号直接选「严格单增/单减」。注意区分 >0 与 ≥0——前者对应严格单调，后者只能对应单调不减。
- **关键概念**：`乘法求导法则`、`商的求导法则`
- **出处**：[陈哥 P44](https://www.bilibili.com/video/BV1husGzwEtZ?p=44)

### 可疑点：驻点与不可导点
- **要点**：单调区间的分界点只可能是两类：一阶导为零的点（驻点）与一阶导不存在的点（不可导点），统称可疑点。不可导点一般就是一阶导表达式中分母为零的点。
- **关键概念**：`驻点`、`不可导点`、`可疑点`
- **相互关系**：与极值点可能出现的位置完全一致。
- **出处**：[陈哥 P45](https://www.bilibili.com/video/BV1husGzwEtZ?p=45)

### 求单调区间的步骤与写法
- **要点**：①确定定义域；②求一阶导；③求出驻点与不可导点；④用可疑点把定义域分成若干区间（可画数轴辅助）；⑤每区间取代表点代入一阶导判断正负（取特殊值最快，常呈正负交替）；⑥由正负写出单调区间。通常列三行表格（x、y′、y）分析。定义域优先——不在定义域内的点不能作为分界点。多个同向单调区间之间用逗号隔开，不能写成并集（如 y=1/x 在 (−∞,0) 与 (0,+∞) 上分别递减，但不能说它在整体上递减）。
- **关键概念**：`定义域`、`列表法`、`子区间`、`取特殊值定号`
- **出处**：[陈哥 P45](https://www.bilibili.com/video/BV1husGzwEtZ?p=45)；[杰哥 P47](https://www.bilibili.com/video/BV1Up4y1Y76a?p=47)；[米哥 P52](https://www.bilibili.com/video/BV1swAWerEzS?p=52)；[ok姐 P38](https://www.bilibili.com/video/BV1vm421s7mv?p=38)

### 极值的定义与极值点、驻点的区别
- **要点**：若存在 x₀ 的某个去心邻域，使邻域内任意 x 都有 f(x)&lt;f(x₀)，则 x₀ 为极大值点、f(x₀) 为极大值；若都有 f(x)>f(x₀)，则对应极小值点与极小值。极值是局部概念，极大值不一定比极小值大；最值是区间上的整体最大/最小值。极值点与驻点指的都是横坐标 x₀，不是点 (x₀,y₀)，对应的函数值才叫极值；拐点则写坐标。
- **关键概念**：`去心邻域`、`极大值点`、`极小值`、`横坐标`、`极值`、`最值`
- **相互关系**：易混点，常在选择填空中设置陷阱；极值只要求「邻域内最大/最小」，不要求是整个区间的最值；最大值点若两侧都比它小，同时也是极大值点。
- **出处**：[陈哥 P46](https://www.bilibili.com/video/BV1husGzwEtZ?p=46)、[P48](https://www.bilibili.com/video/BV1husGzwEtZ?p=48)；[杰哥 P48](https://www.bilibili.com/video/BV1Up4y1Y76a?p=48)；[米哥 P53](https://www.bilibili.com/video/BV1swAWerEzS?p=53)；[学士帽 P48](https://www.bilibili.com/video/BV1X4411J792?p=48)；[ok姐 P42](https://www.bilibili.com/video/BV1vm421s7mv?p=42)

### 极值点与驻点、不可导点的关系
- **要点**：极值点只可能在驻点或不可导点处取得；但驻点不一定是极值点（如 y=x³ 在 x=0 处导数为零却不是极值点），不可导点也不一定是极值点（如 y=|x| 的尖点）。是否为极值点要看左右两侧单调性是否改变。唯一确定的关系：若在某点可导且取得极值，则该点必为驻点。
- **关键概念**：`驻点`、`不可导点`、`可疑点`、`可导 + 极值 ⟹ 驻点`
- **相互关系**：二元函数求极值只考察驻点这一种情况，不会考偏导不存在的点；这一点与一元函数不同。
- **出处**：[陈哥 P46](https://www.bilibili.com/video/BV1husGzwEtZ?p=46)；[杰哥 P49](https://www.bilibili.com/video/BV1Up4y1Y76a?p=49)；[米哥 P53](https://www.bilibili.com/video/BV1swAWerEzS?p=53)

### 由极限式判断极值
- **要点**：给出 lim\_\{x→x₀\}[f(x)−f(x₀)]/(x−x₀)² 之类的极限，先由分母恒正与极限值的符号推出分子（即 f(x)−f(x₀)）的符号，再结合 x 从左右两侧趋近的取号，判断 f(x₀) 比邻域内函数值大还是小。分子恒正 ⇒ 极小值；分子恒负 ⇒ 极大值。
- **关键概念**：`去心邻域`、`极限的保号性`
- **相互关系**：保号性专升本不作要求，此处只作初步运用。
- **出处**：[陈哥 P46](https://www.bilibili.com/video/BV1husGzwEtZ?p=46)

### 极值的第一、第二充分条件
- **要点**：第一充分条件：f(x) 在 x₀ 处连续、在去心邻域内可导；若左邻域 f′&lt;0、右邻域 f′>0（先减后增）则 x₀ 为极小值点；若左 f′>0、右 f′&lt;0（先增后减）则为极大值点；符号不变则不是极值点。第二充分条件：若 f′(x₀)=0 且 f″(x₀)≠0，则 f″(x₀)&lt;0 取极大值、f″(x₀)>0 取极小值（前提是 x₀ 必须为驻点，二阶导符号与极值类型相反）；若存在不可导点，只能用单调性判断。学士帽补充：二阶导判定与凹凸性一致，凹函数对应极小值。
- **关键概念**：`第一充分条件`、`第二充分条件`、`二阶导`、`先增后减为极大`、`先减再增为极小`
- **相互关系**：第一充分条件把单调性与极值串联，最通用、尤其适用于不可导点；第二充分条件更快，但在不可导点处失效；f″(x₀)=0 时也失效，须回到单调性判断。
- **出处**：[陈哥 P47](https://www.bilibili.com/video/BV1husGzwEtZ?p=47)；[杰哥 P48](https://www.bilibili.com/video/BV1Up4y1Y76a?p=48)；[米哥 P53](https://www.bilibili.com/video/BV1swAWerEzS?p=53)；[学士帽 P50](https://www.bilibili.com/video/BV1X4411J792?p=50)；[ok姐 P42](https://www.bilibili.com/video/BV1vm421s7mv?p=42)、[P43](https://www.bilibili.com/video/BV1vm421s7mv?p=43)

### 求极值与单调区间的步骤
- **要点**：求极值三步——求定义域、求一阶导并令其为零找出驻点与不可导点、判定极值类型；再在单调区间的临界点处求出函数值即得极值（先增后减为极大值，先减后增为极小值）。求单调区间解 f′(x)>0 或 &lt;0，常用穿根法（因式分解求出各根，从右向左、从上往下依次穿过，取数轴上方部分对应大于零的区间）。极大值、极小值是把驻点代入原函数求得的函数值，不是 x 值。
- **关键概念**：`穿根法`、`因式分解`、`单调区间`、`列表法`、`临界点`
- **相互关系**：一阶导是一元二次式时可画抛物线，由开口方向与零点直接判断各区间正负；单调区间与极值通常在同一道大题中一起考；大题可省略表格，但定义域、导数与可疑点必须写出。
- **出处**：[陈哥 P47](https://www.bilibili.com/video/BV1husGzwEtZ?p=47)；[杰哥 P48](https://www.bilibili.com/video/BV1Up4y1Y76a?p=48)；[米哥 P53](https://www.bilibili.com/video/BV1swAWerEzS?p=53)；[学士帽 P51](https://www.bilibili.com/video/BV1X4411J792?p=51)；[ok姐 P42](https://www.bilibili.com/video/BV1vm421s7mv?p=42)、[P43](https://www.bilibili.com/video/BV1vm421s7mv?p=43)

### 已知某点取极值求参数
- **要点**：题干可提取两个信息：①该点的函数值等于已知极值（代入原函数）；②该点处一阶导为零（费马引理）；联立方程组解出参数。若还需判断极大或极小，用第二充分条件看二阶导在该点的符号。
- **关键概念**：`极值的必要条件`、`联立方程组`、`第二充分条件`
- **出处**：[陈哥 P47](https://www.bilibili.com/video/BV1husGzwEtZ?p=47)；[杰哥 P48](https://www.bilibili.com/video/BV1Up4y1Y76a?p=48)

### 最值的定义与求法
- **要点**：最值是闭区间 [a,b] 上的整体概念，区间内函数值最大者为最大值、最小者为最小值；极值是局部概念。极大值可以有多个，最值只有一个。三步法：①按求极值的方法求出区间内所有极值；②求出端点值 f(a)、f(b)；③把所有极值与端点值一起比较，最大者为最大值、最小者为最小值。若某驻点落在给定区间之外，则不必计算其函数值。闭区间连续函数必有最大最小值。
- **关键概念**：`闭区间`、`端点值`、`整体概念`、`比较函数值`
- **相互关系**：专升本阶段最值一定在闭区间上求；最值可能在端点取得，而端点不可能是极值点。
- **出处**：[陈哥 P48](https://www.bilibili.com/video/BV1husGzwEtZ?p=48)；[杰哥 P50](https://www.bilibili.com/video/BV1Up4y1Y76a?p=50)；[米哥 P54](https://www.bilibili.com/video/BV1swAWerEzS?p=54)；[ok姐 P44](https://www.bilibili.com/video/BV1vm421s7mv?p=44)

### 开区间与半开半闭区间上的最值
- **要点**：此类区间不能靠比较端点求解，需借助单调性：半开半闭区间上若函数单调，则在闭的那一端取得最值；两端都是开区间且函数先减后增（或先增后减）时，在极小值点取最小值、极大值点取最大值。
- **关键概念**：`单调性`、`开区间`、`半开半闭区间`
- **出处**：[ok姐 P44](https://www.bilibili.com/video/BV1vm421s7mv?p=44)

### 最值应用题（唯一驻点法）
- **要点**：题型多为「用料最省、面积最小、费用最少」。套路是设自变量 x，用题目约束（如体积 V=64π）消去多余变量（如高 h），写出目标函数（如表面积 = 底面积 + 侧面积），定出自变量范围，再求最值。若由题意可断定该区间内必取最值且内部只有一个驻点，则该驻点处的函数值就是最值，无需判定极大极小。
- **关键概念**：`目标函数`、`约束条件`、`消元`、`唯一驻点`
- **相互关系**：几何体表面积公式（侧面积 = 底面周长 × 高）是建模前置知识。
- **出处**：[杰哥 P50](https://www.bilibili.com/video/BV1Up4y1Y76a?p=50)；[ok姐 P44](https://www.bilibili.com/video/BV1vm421s7mv?p=44)

### 凹凸性的定义与判别法
- **要点**：区间上取两点及其中点，若 [f(x₁)+f(x₂)]/2>f((x₁+x₂)/2)，曲线为凹；反向为凸。图像凹下去（形如坑）的曲线称凹函数，拱起来的称凸函数。判别法：f(x) 二阶可导时，f″(x)>0 曲线为凹，f″(x)&lt;0 曲线为凸。几何上切线逆时针旋转（斜率递增）对应 f″>0 为凹，顺时针旋转对应 f″&lt;0 为凸。记忆口诀「笑脸凹、哭脸凸」「大于零凹」。
- **关键概念**：`凹`、`凸`、`f″(x)>0 凹`、`f″(x)<0 凸`、`凹弧`、`凸弧`
- **相互关系**：与一阶导符号定单调性完全平行，是「升阶版」；与直觉相反，须记牢。
- **出处**：[陈哥 P49](https://www.bilibili.com/video/BV1husGzwEtZ?p=49)；[杰哥 P51](https://www.bilibili.com/video/BV1Up4y1Y76a?p=51)；[米哥 P55](https://www.bilibili.com/video/BV1swAWerEzS?p=55)；[学士帽 P49](https://www.bilibili.com/video/BV1X4411J792?p=49)；[ok姐 P41](https://www.bilibili.com/video/BV1vm421s7mv?p=41)

### 拐点及其必要条件
- **要点**：连续曲线凹与凸的分界点称拐点，即凹凸性发生变化的点；不论由凹变凸还是由凸变凹，只要左右两侧凹凸性不一致该点就是拐点。拐点是一个坐标（点），而驻点、极值点只是横坐标。必要条件：若函数二阶导存在且该点为拐点，则必有该点处二阶导等于零（必要非充分）。拐点来自 f″(x)=0 的点或 f″(x) 不存在的点。
- **关键概念**：`拐点`、`凹凸性的分界点`、`拐点的必要条件`、`f″(x₀)=0`
- **相互关系**：易混点——极值点看一阶导变号、拐点看二阶导变号；拐点写坐标，极值点写横坐标。
- **出处**：[陈哥 P49](https://www.bilibili.com/video/BV1husGzwEtZ?p=49)；[杰哥 P51](https://www.bilibili.com/video/BV1Up4y1Y76a?p=51)；[米哥 P55](https://www.bilibili.com/video/BV1swAWerEzS?p=55)；[学士帽 P49](https://www.bilibili.com/video/BV1X4411J792?p=49)；[ok姐 P41](https://www.bilibili.com/video/BV1vm421s7mv?p=41)

### 拐点的第一充分条件与二阶导不存在的情形
- **要点**：设 f(x) 在 x₀ 处连续、在去心邻域内二阶可导；若 f″(x) 在 x₀ 左右两侧变号（由正变负或由负变正），则 x₀ 是拐点。x₀ 为拐点并不要求该点导数存在，典型例子是 y=∛x，在 x=0 处二阶导不存在（趋于无穷），但左右凹凸性相反，x=0 仍为拐点。
- **关键概念**：`第一充分条件`、`二阶导变号`、`二阶导不存在的点`
- **相互关系**：找可疑点时要同时找二阶导为零的点和不存在的点。
- **出处**：[陈哥 P49](https://www.bilibili.com/video/BV1husGzwEtZ?p=49)

### 拐点与二阶导为零点的关系
- **要点**：三条结论要分清——①拐点不一定是二阶导为零的点（二阶导可不存在）；②若二阶导存在且为拐点，则该点必为二阶导等于零的点（必要条件）；③二阶导为零的点也不一定是拐点，如 y=x⁴ 在 x=0 处二阶导为零但左右同为凹。
- **关键概念**：`必要条件`、`二阶导为零的点`
- **出处**：[陈哥 P49](https://www.bilibili.com/video/BV1husGzwEtZ?p=49)

### 凹凸区间与拐点的求解步骤
- **要点**：①求定义域（确定讨论范围）；②求二阶导；③求可疑点（二阶导为零的点、二阶导不存在的点，通常即分母为零的点）；④用可疑点划分定义域，在各区间上判断二阶导符号定凹凸（列表）；⑤凹凸区间的分界点即拐点，写出拐点坐标。判断符号时可先画二阶导的局部图像。
- **关键概念**：`可疑点`、`列表法`、`凹凸区间`、`拐点坐标`、`二阶不可导点`
- **相互关系**：与求单调区间、极值的步骤一一对应，只是把一阶导换成二阶导。
- **出处**：[陈哥 P49](https://www.bilibili.com/video/BV1husGzwEtZ?p=49)；[杰哥 P51](https://www.bilibili.com/video/BV1Up4y1Y76a?p=51)；[ok姐 P41](https://www.bilibili.com/video/BV1vm421s7mv?p=41)

### 已知某点为拐点求参数
- **要点**：用两个信息：①拐点在曲线上，坐标满足曲线方程；②若在该点二阶可导，则 f″(x₀)=0；由此列出关于参数的方程组求解。升本考查时该点处基本都可导，故两个条件都能用。
- **关键概念**：`拐点`、`二阶导为零`、`联立方程组`
- **出处**：[ok姐 P41](https://www.bilibili.com/video/BV1vm421s7mv?p=41)

### 由一阶导图像判断极值点与拐点个数
- **要点**：给出 f′(x) 图像时，一阶导的零点且变号处为极值点；要判断拐点，需对 f′(x) 再求一次导——f″(x) 的符号决定 f′(x) 的增减，f′(x) 的极值点对应 f″(x) 的零点，该横坐标处即为拐点。核心思想：一个函数导数的正负，一定决定原函数的增减。
- **关键概念**：`f′(x) 的单调性`、`f″(x) 的符号`、`拐点横坐标`
- **出处**：[陈哥 P49](https://www.bilibili.com/video/BV1husGzwEtZ?p=49)

### 渐近线的概念与垂直渐近线
- **要点**：曲线无限靠近某条直线而永不与之相交，该直线即渐近线；分垂直、水平、斜三类。若 x→x₀（或 x→x₀⁺、x→x₀⁻）时 f(x)→∞，则 x=x₀ 为垂直渐近线；左右极限只要有一个为无穷即可。求法：先找无定义点（一般是分母为零的点），再求该点处的极限。遇到 arctan(1/x)、e\^\{1/x\}、分段函数时必须分别求左右极限。
- **关键概念**：`渐近线`、`垂直渐近线`、`无定义点`、`极限为无穷`
- **相互关系**：水平渐近线平行于 x 轴，两者区分；x=0 是 ln x、1/x 的垂直渐近线。
- **出处**：[陈哥 P50](https://www.bilibili.com/video/BV1husGzwEtZ?p=50)；[杰哥 P28](https://www.bilibili.com/video/BV1Up4y1Y76a?p=28)；[米哥 P56](https://www.bilibili.com/video/BV1swAWerEzS?p=56)；[ok姐 P12](https://www.bilibili.com/video/BV1vm421s7mv?p=12)

### 水平渐近线
- **要点**：若 x→+∞ 或 x→−∞ 时 f(x)→Y₁（常数 A），则 y=Y₁ 为水平渐近线（平行于 x 轴）；极限不为常数则无。正负两个方向都要求一次，极限相等则只有一条。y=0 是 1/x、a^x(0&lt;a&lt;1)、e^x 的水平渐近线；arctan x 有 y=±π/2 两条。
- **关键概念**：`水平渐近线`、`平行于 x 轴`、`极限为常数`
- **相互关系**：必须分正负无穷讨论的两类函数是 arctan x（分别趋于 ±π/2）与 e^x（分别趋于 0 与 +∞）。
- **出处**：[陈哥 P50](https://www.bilibili.com/video/BV1husGzwEtZ?p=50)；[杰哥 P28](https://www.bilibili.com/video/BV1Up4y1Y76a?p=28)；[米哥 P56](https://www.bilibili.com/video/BV1swAWerEzS?p=56)；[ok姐 P9](https://www.bilibili.com/video/BV1vm421s7mv?p=9)、[P11](https://www.bilibili.com/video/BV1vm421s7mv?p=11)；[石头 P41](https://www.bilibili.com/video/BV18CL26WEJ3?p=41)

### 斜渐近线及其与水平渐近线的互斥
- **要点**：前提条件是 lim\_\{x→∞\}f(x)=∞；满足前提后设斜渐近线为 y=kx+b（或 y=ax+b），其中 k=lim\_\{x→∞\}f(x)/x，b=lim\_\{x→∞\}[f(x)−kx]；求 b 时常需先通分再用抓大头或洛必达。同一方向上不可能同时出现水平渐近线和斜渐近线，因为该方向 f(x) 的极限要么是常数（水平）、要么是无穷（才可能对应斜）；若函数同时具有水平渐近线与垂直渐近线，则一定没有斜渐近线。
- **关键概念**：`斜渐近线`、`k`、`b`、`互斥`
- **相互关系**：专升本阶段主要考「正负无穷结果相同」这一种情形。
- **出处**：[陈哥 P50](https://www.bilibili.com/video/BV1husGzwEtZ?p=50)；[杰哥 P28](https://www.bilibili.com/video/BV1Up4y1Y76a?p=28)；[米哥 P56](https://www.bilibili.com/video/BV1swAWerEzS?p=56)

### 渐近线条数题型
- **要点**：分别检验是否有水平、垂直、斜渐近线，逐条验证；求 b 时若遇 x(e\^\{1/x\}−1) 型，提公因子后用 e^□−1~□ 等价。
- **关键概念**：`渐近线条数`
- **出处**：[杰哥 P28](https://www.bilibili.com/video/BV1Up4y1Y76a?p=28)


### 罗尔中值定理的条件与结论
- **要点**：三个条件缺一不可：$f(x)$ 在闭区间 $[a,b]$ 上连续、在开区间 $(a,b)$ 内可导、且 $f(a)=f(b)$。结论是至少存在一点 $\xi\in(a,b)$ 使 $f'(\xi)=0$，即曲线至少有一处切线水平，这样的点称为驻点。
- **关键概念**：`罗尔中值定理`、`闭区间连续`、`开区间可导`、`$f(a)=f(b)$`、`$f'(\xi)=0$`、`驻点`
- **相互关系**：可形象理解为「从甲地修一条连续光滑的路到水平等高的乙地，途中至少有一点车头水平朝前」；与零点定理的连续条件相同，但结论一个是 $f'(\xi)=0$、一个是 $f(\xi)=0$。
- **出处**：[石头 P31](https://www.bilibili.com/video/BV18CL26WEJ3?p=31)

### 罗尔中值定理的判断题型
- **要点**：选择题判断某函数在某区间上是否满足罗尔中值定理，用排除法先找软柿子：分段函数先看分段点是否连续，带绝对值的先看尖点是否可导，含分数次幂的先求导函数并写成负指数形式看定义域缺口，例如 $(x-1)\^\{2/3\}$ 的导数含 $\frac{1}{\sqrt[3]{x-1}}$，$x=1$ 处不可导。
- **关键概念**：`排除法`、`分段点`、`尖点`、`导函数定义域`、`不可导`
- **相互关系**：判断可导性的通用做法是先求导函数，再看导函数无定义的点是否落在给定开区间内；这类题的三个条件与可导、连续的关系一节完全一致。
- **出处**：[石头 P31](https://www.bilibili.com/video/BV18CL26WEJ3?p=31)

### 用罗尔中值定理证明方程有实根
- **要点**：证明「方程在某开区间内至少有一个实根」先试零点定理，若两端点函数值无法判定异号，则改用罗尔定理：构造函数 $F(x)$ 使 $F'(x)$ 恰为所证方程的左端，再验证 $F(x)$ 满足三条件（连续、可导、两端点函数值相等），最后由 $F'(\xi)=0$ 得证。
- **关键概念**：`零点定理优先`、`构造 $F'(x)$`、`反求原函数`、`两端点函数值相等`
- **相互关系**：这里构造的是导函数 $F'(x)$，需反推原函数 $F(x)$；与零点定理中直接构造 $f(x)$ 的做法不同，是两种题型的分水岭。
- **出处**：[石头 P31](https://www.bilibili.com/video/BV18CL26WEJ3?p=31)

### 构造辅助函数证明含 $f'(\xi)$ 的等式
- **要点**：要证 $f'(\xi)+k(\xi)f(\xi)=0$ 这类含导数的等式，就把等式左端整体看作辅助函数 $F(x)$ 的导数，令 $F'(x)=f'(x)+k(x)f(x)$，再由乘积法则反推 $F(x)=f(x)v(x)$，其中 $v(x)$ 满足 $v'(x)=k(x)v(x)$。常见对应：$f'(\xi)+f(\xi)=0$ 取 $F=f(x)e^x$；$f'(\xi)+2f(\xi)=0$ 取 $F=f(x)e\^\{2x\}$；$f'(\xi)+2\xi f(\xi)=0$ 取 $F=f(x)e\^\{x\^2\}$；$\frac{\xi}{n}f'(\xi)+f(\xi)=0$ 取 $F=f(x)x^n$。中间是减号时改用商的法则，如 $f'(\xi)-f(\xi)=0$ 取 $F=\frac{f(x)}{e^x}$。
- **关键概念**：`辅助函数`、`$F'(x)=f'(x)+k(x)f(x)$`、`$F=f(x)e^x$`、`$F=f(x)x^n$`、`商的法则`
- **相互关系**：关键在于利用 $e^x$ 求导等于自身这一特性使系数消去；答题按「构造 $F(x)$—验证三条件—由 $F'(\xi)=0$ 化简得证」的固定模板书写即可，是本章难度的天花板。
- **出处**：[石头 P32](https://www.bilibili.com/video/BV18CL26WEJ3?p=32)

### 拉格朗日中值定理的条件与结论
- **要点**：只需两个条件：$f(x)$ 在 $[a,b]$ 上连续、在 $(a,b)$ 内可导（去掉了罗尔定理的端点值相等）。结论是至少存在一点 $\xi\in(a,b)$ 使 $f'(\xi)=\frac{f(b)-f(a)}{b-a}$，右端为两端点连线的斜率，左端为该点切线斜率，即某点切线与两端点连线平行。
- **关键概念**：`拉格朗日中值定理`、`$f'(\xi)=\frac{f(b)-f(a)}{b-a}$`、`两端点连线斜率`、`切线平行`
- **相互关系**：罗尔中值定理是它的特例（当 $f(a)=f(b)$ 时右端为零）；条件少一个、适用面更广，可理解为罗尔定理「旋转一个角度」。
- **出处**：[石头 P33](https://www.bilibili.com/video/BV18CL26WEJ3?p=33)

### 求满足拉格朗日中值定理的 $\xi$ 值
- **要点**：小题求 $\xi$ 就套结论：左边先求导函数 $f'(x)$ 并把 $x$ 换成 $\xi$，右边代入两端点函数值算出 $\frac{f(b)-f(a)}{b-a}$，两边相等解出 $\xi$。例如 $f(x)=\frac12x^2-x$ 在 $[1,2]$ 上得 $\xi-1=\frac12$，即 $\xi=\frac32$。
- **关键概念**：`求 $\xi$`、`$f'(\xi)=\frac{f(b)-f(a)}{b-a}$`、`代点`
- **相互关系**：与判断条件类题互补，一个考条件、一个考结论；解出的 $\xi$ 必须落在开区间 $(a,b)$ 内。
- **出处**：[石头 P33](https://www.bilibili.com/video/BV18CL26WEJ3?p=33)

### 用拉格朗日中值定理证明双边不等式
- **要点**：三步走：由中间那个函数值差构造 $f(x)$（若中间是单项式则减去零，并把零写成该函数的零点值，如 $\ln(1+x)-\ln1$、$\tan x-\tan0$、$\arctan b-\arctan a$）；写出 $f'(\xi)=\frac{f(b)-f(a)}{b-a}$ 并解出两端点函数差 $=f'(\xi)(b-a)$；由 $a&lt;\xi&lt;b$ 比较大小写出不等式链。如 $x>0$ 时 $\frac{x}{1+x}&lt;\ln(1+x)&lt;x$，$x\in(0,\frac\pi2)$ 时 $x&lt;\tan x&lt;\frac{x}{\cos^2x}$。
- **关键概念**：`双边不等式`、`构造 $f(x)$`、`减零变形`、`$a<\xi<b$`、`比较大小`
- **相互关系**：构造 $f$ 时看中间式子的函数类型（$\arctan$ 就取 $\arctan x$，$\ln$ 就取 $\ln x$，$\tan$ 就取 $\tan x$）；比较环节只要写出 $\xi$ 的范围，结论即可直接判断。
- **出处**：[石头 P33](https://www.bilibili.com/video/BV18CL26WEJ3?p=33)

### 洛必达法则及其两个前提
- **要点**：对 $\frac00$ 型或 $\frac{\infty}{\infty}$ 型未定式，有 $\lim\frac{f(x)}{g(x)}=\lim\frac{f'(x)}{g'(x)}$，即分子分母分别求导后再求极限。两个前提：一是原式为 $\frac00$ 或 $\frac{\infty}{\infty}$ 型（自变量趋于何处不限），二是求导后的极限存在或为无穷；不满足就绝不能落。
- **关键概念**：`洛必达法则`、`$\frac00$ 型`、`$\frac{\infty}{\infty}$ 型`、`分子分母分别求导`、`先定型后定法`
- **相互关系**：因为要用求导，所以安排在第二章讲；如 $\lim\_\{x\to0\}\frac{1+x}{x}$ 是 $\frac10$ 型定式，直接得 $\infty$，若强行洛必达会算出 $1$，是典型错误。
- **出处**：[石头 P34](https://www.bilibili.com/video/BV18CL26WEJ3?p=34)

### 洛必达法则的使用技巧与注意事项
- **要点**：一是落完若仍满足条件可一直落，直到不能再落，如 $\lim\_\{x\to+\infty\}\frac{x\^\{100\}}{e^x}$ 落 $100$ 次后分子成常数、极限为 $0$；二是可与等价无穷小交替使用，但同一步中绝不能混用；三是不要一条路走到黑，能化简先化简，如 $\frac{\tan x-x}{x-\sin x}$ 先通分约分直接得 $2$；四是落之前先把非零非无穷的「因子」先行代入；五是落完极限不存在（无穷除外）则法则失效，须换其他方法，如 $\lim\_\{x\to\infty\}\frac{\sin x+x}{x}$ 拆项后用「$0\times$ 有界 $=0$」得 $1$；六是落完陷入循环则失效，如 $\frac{e^x-e\^\{-x\}}{e^x+e\^\{-x\}}$ 改为分子分母同除以 $e^x$ 得 $1$。
- **关键概念**：`一直落到不能落`、`与等价无穷小交替但不混用`、`先化简`、`非零非无穷因子先行代入`、`失效换方法`、`死循环`
- **相互关系**：等价无穷小替换只适用于乘除因子，与洛必达分属两步时才能先后使用；遇到 $e^x$、$\sin\infty$ 等结构要警惕失效与循环。
- **出处**：[石头 P34](https://www.bilibili.com/video/BV18CL26WEJ3?p=34)

### 洛必达法则的证明思路
- **要点**：设 $f(x)$、$g(x)$ 在 $x_0$ 附近可导，取 $x_0$ 与 $x$ 之间的点 $\xi$，由拉格朗日中值定理得 $f'(\xi)=\frac{f(x)-f(x_0)}{x-x_0}$、$g'(\xi)=\frac{g(x)-g(x_0)}{x-x_0}$，两式相除消去分母得 $\frac{f'(\xi)}{g'(\xi)}=\frac{f(x)-f(x_0)}{g(x)-g(x_0)}$。因极限值与 $f(x_0)$、$g(x_0)$ 无关，可令二者都等于零，再把 $\xi\to x_0$ 换成 $x\to x_0$，即得 $\lim\frac{f(x)}{g(x)}=\lim\frac{f'(x)}{g'(x)}$。
- **关键概念**：`拉格朗日中值定理`、`$\frac{f'(\xi)}{g'(\xi)}=\frac{f(x)-f(x_0)}{g(x)-g(x_0)}$`、`令 $f(x_0)=g(x_0)=0$`
- **相互关系**：证明过程中用到了微分中值定理，这正是洛必达法则必须排在导数与中值定理之后讲授的原因；该证明考试不要求，理解即可。
- **出处**：[石头 P35](https://www.bilibili.com/video/BV18CL26WEJ3?p=35)

### 求极限的六字真言
- **要点**：拿到极限先「定型」——把趋近值代入分子分母，判断是定式还是未定式、属于哪一种未定式；再「定法」——按类型选方法。专升本求极限共十种基础方法，前九种在第一章讲完，第十种洛必达法则在第二章补上。
- **关键概念**：`先定型后定法`、`定式`、`未定式`、`十种基础方法`
- **相互关系**：其他未定式（$0\cdot\infty$、$\infty-\infty$、$0^0$、$\infty^0$、$1^\infty$）的统一思路都是先转化为 $\frac00$ 型或 $\frac{\infty}{\infty}$ 型，再用基础方法求解。
- **出处**：[石头 P36](https://www.bilibili.com/video/BV18CL26WEJ3?p=36)

### ∞−∞型与0×∞型未定式的转化
- **要点**：$\infty-\infty$ 型不能想当然认为等于零，例如 $x\to+\infty$ 时 $2x-x\to+\infty$、$x-x\to0$、$x-2x\to-\infty$，结果不确定，故为未定式；解法是通分，以两个分母之积作公分母，化为 $\frac00$ 型。$0\cdot\infty$ 型同样不确定（$x\cdot\frac1x\to1$，$2x\cdot\frac1x\to2$），解法是「下放」：把趋于零的部分取倒数放到分母，或把趋于无穷的部分取倒数放到分母，化为基础未定式。
- **关键概念**：`$\infty-\infty$ 型`、`通分`、`$0\cdot\infty$ 型`、`下放`、`取倒数`
- **相互关系**：下放时优先把求导更简单的部分放到分母上；若两个部分互为倒数（如 $x^2$ 与 $\frac{1}{x^2}$），可先令 $t$ 等于该倒数换元，把式子化简为 $\frac{\infty}{\infty}$ 型再洛必达。
- **出处**：[石头 P36](https://www.bilibili.com/video/BV18CL26WEJ3?p=36)

### 幂指型未定式：$0^0$ 与 $\infty^0$
- **要点**：底数与指数都含未知数的函数称幂指函数，求其极限要先用对数恒等式 $u^v=e\^\{v\ln u\}$ 恒等变形，把指数提到前面做系数，于是 $0^0$ 型与 $\infty^0$ 型都化为 $0\cdot\infty$ 型，再下放为 $\frac00$ 或 $\frac{\infty}{\infty}$ 型。若幂指函数只作为式子的一部分出现，同样先把它单独恒等变形为 $e\^\{\square\}$，再对整体用等价无穷小或洛必达。
- **关键概念**：`幂指函数`、`$u^v=e^{v\ln u}$`、`对数恒等变形`、`$0^0$ 型`、`$\infty^0$ 型`
- **相互关系**：算出的极限只是 $\ln$ 那一部分的极限，最后要放回 $e$ 的指数上，切勿把 $e$ 内部算出的值当成原式的值；这类题结果不一定都等于 $1$，不能凭几道题的结果自行总结规律。
- **出处**：[石头 P36](https://www.bilibili.com/video/BV18CL26WEJ3?p=36)

### $1^\infty$ 型：第二重要极限的两个通式
- **要点**：通式一：若式子能写成 $[1+f(x)]\^\{g(x)\}$ 且 $f(x)\to0$、$g(x)\to\infty$，则极限为 $e\^\{\lim f(x)g(x)\}$，使用时先从中拆出一个 $1$。通式二：若底数本身是一个趋于 $1$ 的整体 $F(x)$，即 $[F(x)]\^\{g(x)\}$，则极限为 $e\^\{\lim[F(x)-1]g(x)\}$，不必再拆 $1$。两式的本质都是把「底数减一」与指数相乘后取 $e$ 的幂。
- **关键概念**：`第二重要极限通式一`、`第二重要极限通式二`、`$e^{\lim[F(x)-1]g(x)}$`
- **相互关系**：数列极限中 $n$ 只能趋于 $+\infty$、不能趋于某个常数，但洛必达法则与两个重要极限都可用；抓大头时分子分母同次，结果取系数比。
- **出处**：[石头 P36](https://www.bilibili.com/video/BV18CL26WEJ3?p=36)

### 三类函数的增长速度
- **要点**：当 $x\to+\infty$ 时，指数函数 $a^x$ 的增长速度远大于幂函数 $x^n$，幂函数又远大于对数函数 $\ln x$。因此 $\lim\_\{x\to+\infty\}\frac{x^n}{e^x}=0$、$\lim\_\{x\to+\infty\}\frac{\ln x}{x^n}=0$，无论 $n$ 多大都成立。这一趋势只作粗略判断用，若复合函数的内层很复杂，结论可能受影响。
- **关键概念**：`指数爆炸`、`指数函数 $\gg$ 幂函数 $\gg$ 对数函数`
- **相互关系**：抓大头只在 $x\to\infty$ 时使用，$x\to0$ 时不可套用；掌握「谁快」可以极大提高做极限题的速度，甚至一眼看出答案。
- **出处**：[石头 P36](https://www.bilibili.com/video/BV18CL26WEJ3?p=36)

### 导数的几何意义与切线斜率
- **要点**：函数在点 $x_0$ 处的导数 $f'(x_0)$ 的几何意义就是曲线在该点处切线的斜率，即 $k\_\{切\}=f'(x_0)=\tan\alpha$（$\alpha$ 为切线与水平方向的夹角）。曲线在某点处的切线，是过该点且与该曲线只有一个交点的直线。
- **关键概念**：`导数的几何意义`、`切线斜率 $k_{切}=f'(x_0)$`、`$\tan\alpha$`
- **相互关系**：把切线斜率看作倾斜方向，可直接反过来判断导数的正负：切线向右上方倾斜则 $f'(x)>0$，向右下方倾斜则 $f'(x)&lt;0$，这是下一节判断单调性的依据。
- **出处**：[石头 P37](https://www.bilibili.com/video/BV18CL26WEJ3?p=37)

### 求切线方程与法线方程的三板斧
- **要点**：过点 $(x_0,y_0)$ 且垂直于切线的直线叫法线，二者斜率之积为 $-1$，故 $k\_\{法\}=-\frac{1}{f'(x_0)}$。求方程共三步：第一步求 $y_0$（题目已给就跳过，只给 $x_0$ 时把 $x_0$ 代入原函数）；第二步求 $f'(x_0)$，推荐先求导函数再代 $x_0$，也可用导数定义；第三步代入点斜式 $y-y_0=k(x-x_0)$。
- **关键概念**：`法线`、`$k_{法}=-\frac{1}{f'(x_0)}$`、`两直线垂直斜率之积为 $-1$`、`点斜式 $y-y_0=k(x-x_0)$`
- **相互关系**：若题目给出「两条曲线在 $x=a$ 处的切线互相垂直」，即令两个导数相乘等于 $-1$ 解出 $a$，这是三板斧的逆用。
- **出处**：[石头 P37](https://www.bilibili.com/video/BV18CL26WEJ3?p=37)

### 隐函数求导求切线
- **要点**：方程 $F(x,y)=0$ 确定的隐函数求导时，等式两边同时对 $x$ 求导，遇到 $y$ 的项按复合函数处理并乘上 $y'$（即 $\frac{dy}{dx}$），再把含 $y'$ 的项移到一边解出 $y'$。求切线时把已知点的横、纵坐标一起代入 $y'$ 的表达式得到斜率，再代入点斜式。
- **关键概念**：`隐函数求导`、`两边对 $x$ 求导`、`$y'=\frac{dy}{dx}$`、`乘积的求导法则`
- **相互关系**：求出的 $y'$ 就是 $f'(x)$，可直接作为三板斧的第二步；乘积项（如 $xy$）要用「前导后不导加后导前不导」。
- **出处**：[石头 P42](https://www.bilibili.com/video/BV18CL26WEJ3?p=42)

### 导数符号与单调性的关系
- **要点**：在区间内若 $f'(x)>0$，则 $f(x)$ 单调增加；若 $f'(x)&lt;0$，则 $f(x)$ 单调减少。推导依据是导数定义 $\frac{\Delta y}{\Delta x}$：单调增加时分子分母同为正，单调减少时分子为负、分母为正，比值的符号就是导数的符号。
- **关键概念**：`$f'(x)>0$ 单调增`、`$f'(x)<0$ 单调减`、`$\frac{\Delta y}{\Delta x}$`
- **相互关系**：$f'(x)=0$ 的点（驻点）两侧单调性可能相同也可能不同，无法判断，命题人常在此设陷阱；$f'(x)$ 不存在的点同理。
- **出处**：[石头 P38](https://www.bilibili.com/video/BV18CL26WEJ3?p=38)

### 求单调区间的四个步骤
- **要点**：第一步求定义域，顺便得到间断点；第二步求一阶导 $f'(x)$；第三步求驻点（$f'(x)=0$ 的点）和不可导点（不满足 $f'(x)$ 定义域的点）；第四步用这些点把定义域分成若干区间，列表用特值法判断各区间内 $f'(x)$ 的正负，从而写出单调区间。
- **关键概念**：`四步法`、`驻点`、`不可导点`、`特值法`、`列表讨论`
- **相互关系**：分区间时可用数轴标点，几个点就把定义域分成几段；单调区间之间用逗号或「和」连接，绝不能用并集，因为并集意味着整个区间单调，而事实是各自区间内单调；端点一律写开区间，避免误把间断点包含进去。
- **出处**：[石头 P38](https://www.bilibili.com/video/BV18CL26WEJ3?p=38)

### 用单调性证明不等式
- **要点**：单边不等式（左式小于右式）可移项作差构造辅助函数 $F(x)=$ 左式 $-$ 右式；求 $F'(x)$ 并判断它在给定区间内的正负，得出 $F(x)$ 单调增或减；再求出区间左端点的函数值（通常为 $0$），由单调性得 $F(x)>F(0)$ 或 $F(x)&lt;F(0)$，即证。双边不等式则用拉格朗日中值定理。
- **关键概念**：`构造函数`、`移项作差`、`$F(x)>F(0)$`、`单边不等式`、`双边不等式`
- **相互关系**：写单调区间时要包含左端点（写成左闭右开），因为要用端点值 $F(0)$ 作比较；若 $F'(x)$ 不易判号，可先通分再判。
- **出处**：[石头 P38](https://www.bilibili.com/video/BV18CL26WEJ3?p=38)、[P42](https://www.bilibili.com/video/BV18CL26WEJ3?p=42)

### 凹凸性的定义与二阶导判定
- **要点**：从上往下看曲线有坑（往下凹）叫凹，往上凸起叫凸；判断时连接曲线两端点作直线，曲线在直线上方为凸，在直线下方为凹。曲线凹时切线斜率递增，即一阶导单调增、二阶导 $f''(x)>0$；曲线凸时切线斜率递减，即 $f''(x)&lt;0$。口诀：一阶导大增小减，二阶导大凹小凸。
- **关键概念**：`凹`、`凸`、`$f''(x)>0$ 为凹`、`$f''(x)<0$ 为凸`、`大凹小凸`
- **相互关系**：凹凸性由二阶导决定、单调性由一阶导决定，两者极易混淆，须对照记忆；凹凸区间描述的是曲线而不是函数。
- **出处**：[石头 P39](https://www.bilibili.com/video/BV18CL26WEJ3?p=39)

### 求凹凸区间与拐点的四个步骤
- **要点**：连续曲线上凹凸性的分界点称拐点。四步与求单调区间雷同：第一步求定义域与间断点；第二步求二阶导 $f''(x)$；第三步求 $f''(x)=0$ 的点与 $f''(x)$ 不存在的点；第四步用这些点分割定义域，列表判断 $f''(x)$ 的正负，写出凹凸区间，再取凹凸性发生改变的点作为拐点并求出纵坐标。
- **关键概念**：`四步法`、`$f''(x)=0$ 的点`、`$f''(x)$ 不存在的点`、`凹凸区间`、`拐点`
- **相互关系**：与求单调区间的差别在于这里求的是二阶导而非一阶导；拐点两侧的二阶导必须异号，否则不是拐点。
- **出处**：[石头 P39](https://www.bilibili.com/video/BV18CL26WEJ3?p=39)

### 拐点的注意事项
- **要点**：拐点一定是曲线上的点，必须写出完整坐标 $(x_0,f(x_0))$，不能只写 $x=x_0$，这与驻点只写横坐标不同。拐点只能在 $f''(x)=0$ 或 $f''(x)$ 不存在的点中去寻找，但反过来这些点不一定是拐点。典型反例：$y=x^4$ 在 $x=0$ 处 $f''(0)=0$，但两侧都是凹，故无拐点；$y=\frac1x$ 在 $x=0$ 处二阶导不存在且两侧凹凸不同，但该点不在曲线上，故也无拐点。
- **关键概念**：`拐点是曲线上的点`、`$(x_0,f(x_0))$`、`两侧二阶导异号`
- **相互关系**：$y=\sqrt[3]{x}$ 的拐点为 $(0,0)$，此处切线竖直、二阶导不存在，说明拐点处的切线可以是水平、倾斜或竖直的；求凹凸区间时同样不能用并集连接两个区间。
- **出处**：[石头 P39](https://www.bilibili.com/video/BV18CL26WEJ3?p=39)、[P42](https://www.bilibili.com/video/BV18CL26WEJ3?p=42)

### 极值与最值的概念
- **要点**：最值指整个区间内最大（小）的函数值，最大值与最小值各唯一；极值是局部区域内的最值，可有多处，也不一定等于最值。极值不能在区间端点处取得，只能在区间内部取得，即该点两侧都要有定义。因此最值可以是极值，也可以不是极值。
- **关键概念**：`极值`、`最值`、`局部最值`、`极值不能在端点取得`
- **相互关系**：极值点必须是两侧都有定义的「山峰」，端点断崖处不能取极值；闭区间上的最值必须比较各极值与两个端点值。
- **出处**：[石头 P40](https://www.bilibili.com/video/BV18CL26WEJ3?p=40)

### 极值的必要条件定理
- **要点**：若 $f(x)$ 在 $x_0$ 处取得极值且在 $x_0$ 处可导，则 $f'(x_0)=0$，即 $x_0$ 是驻点，简记为「极值 $+$ 可导 $\Rightarrow$ 驻点」。反过来只知道是极值、不知道是否可导，推不出它是驻点，例如尖点处取得极值但不可导。
- **关键概念**：`必要条件`、`$f'(x_0)=0$`、`驻点`
- **相互关系**：这是三个极值定理中唯一「由极值推结论」的一个；三个定理都不是充要条件，因为都要求可导，而极值也可能在不可导点取得。
- **出处**：[石头 P40](https://www.bilibili.com/video/BV18CL26WEJ3?p=40)

### 极值的两个充分条件定理
- **要点**：第一充分条件：$f(x)$ 在 $x_0$ 处连续且在 $x_0$ 的某去心邻域内可导，若 $x_0$ 左侧 $f'(x)>0$、右侧 $f'(x)&lt;0$（左增右减），则取极大值；若左减右增，则取极小值；两侧同号则无极值。第二充分条件：若 $f'(x_0)=0$ 且 $f''(x_0)\ne0$，则 $f''(x_0)&lt;0$（凸）时取极大值，$f''(x_0)>0$（凹）时取极小值。
- **关键概念**：`第一充分条件`、`左增右减取极大`、`左减右增取极小`、`第二充分条件`、`驻点 $+$ 凸取极大`
- **相互关系**：不可导点只能用第一充分条件判断，驻点两种方法均可；第一充分条件需要列表看 $f'(x)$ 的符号，第二充分条件只需算一个二阶导的值。
- **出处**：[石头 P40](https://www.bilibili.com/video/BV18CL26WEJ3?p=40)

### 求函数极值的四个步骤
- **要点**：第一步求定义域；第二步求一阶导 $f'(x)$；第三步求驻点（$f'(x)=0$）和不可导点；第四步判断这些点处是否取极值并算出极值。不可导点只能用第一充分条件（列表看左右导数的符号），驻点可用第一或第二充分条件。
- **关键概念**：`四步法`、`驻点`、`不可导点`、`极值`、`尖点`
- **相互关系**：用第二充分条件时先求 $f''(x)$ 再代点判号，比列表更快；用第一充分条件时表的结构与求单调区间的表相同，可同时得到单调区间与极值。
- **出处**：[石头 P40](https://www.bilibili.com/video/BV18CL26WEJ3?p=40)

### 最值的求法
- **要点**：闭区间上求最值三步：第一步求 $f'(x)$（区间已给，不必求定义域）；第二步求所有驻点与不可导点，并算出这些点及两个端点的函数值；第三步比较这些值，最大者为最大值、最小者为最小值。实际问题求最值：先构建目标函数（要最大/最小的量设为 $Y$，可调整的量设为 $x$），由题中尚未使用的条件消去多余变量并确定 $x$ 的取值范围，再求 $Y'=0$ 的驻点；若驻点唯一且为实际问题，该驻点即为所求。
- **关键概念**：`闭区间最值三步`、`端点值`、`目标函数`、`唯一驻点`
- **相互关系**：求最值比求极值简单，不需要判断极大还是极小；实际问题若驻点不唯一，则把各驻点的函数值比较后取优。
- **出处**：[石头 P40](https://www.bilibili.com/video/BV18CL26WEJ3?p=40)、[P42](https://www.bilibili.com/video/BV18CL26WEJ3?p=42)

### 渐近线的定义
- **要点**：若曲线上的点与某条直线的距离随曲线无限延伸而趋近于零，且这个趋势能一直保持到无穷远，则该直线是曲线的渐近线。两个条件缺一不可：距离要趋于零，趋势要保持到无穷远，中途偏离则不是渐近线。
- **关键概念**：`渐近线`、`距离趋近于零`、`趋势保持到无穷远`
- **相互关系**：一条曲线可以有多条渐近线，也可以没有渐近线；按方向分为水平、垂直、斜渐近线，专升本多数省份只考水平与垂直两种，斜渐近线不要求。
- **出处**：[石头 P41](https://www.bilibili.com/video/BV18CL26WEJ3?p=41)

### 垂直渐近线
- **要点**：若 $\lim\_\{x\to x\_0\}f(x)=\infty$（正负无穷均可），则 $x=x_0$ 是曲线的垂直渐近线（也叫铅垂渐近线）。求法是先找不满足定义域的点即间断点，再求该点处的极限；极限为无穷即为无穷间断点，对应一条垂直渐近线，极限为常数则没有。
- **关键概念**：`垂直渐近线 $x=x_0$`、`无穷间断点`、`$\lim_{x\to x_0}f(x)=\infty$`
- **相互关系**：求垂直渐近线实质是找无穷间断点，不用区分左右极限，也不必判断是正无穷还是负无穷；分母为零而分子不为零时极限必为无穷。
- **出处**：[石头 P41](https://www.bilibili.com/video/BV18CL26WEJ3?p=41)


