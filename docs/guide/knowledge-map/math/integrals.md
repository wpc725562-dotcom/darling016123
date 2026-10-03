# 高数 · 积分 · 微分方程

> 不定积分、定积分及其应用、常微分方程

> 本页 3 章 / 205 条知识点。来源与可信度说明见[知识地图总览](/guide/knowledge-map/)。

## 四、不定积分


### 原函数、不定积分与互逆运算
- **要点**：若在区间 I 上 F′(x)=f(x)（或 dF(x)=f(x)dx），则 F(x) 是 f(x) 在 I 上的一个原函数；因常数求导为零，F(x)+C 是全体原函数。f(x) 的全体原函数称为不定积分，记作 ∫f(x)dx=F(x)+C；积分号后的 f(x) 叫被积函数，f(x)dx 叫被积表达式，dx 中的 x 叫积分变量。求导与积分互为逆运算，这是本章全部内容的总纲。见到「某函数是某函数的原函数」要同时反应出求导关系与积分关系。
- **关键概念**：`原函数`、`全体原函数`、`不定积分`、`被积函数`、`被积表达式`、`积分变量`、`互逆运算`
- **相互关系**：不定积分与全体原函数可视为同一概念；积分结果求导即被积函数；积分变量可换字母，∫f(x)dx=∫f(t)dt。
- **出处**：[陈哥 P51](https://www.bilibili.com/video/BV1husGzwEtZ?p=51)、[P52](https://www.bilibili.com/video/BV1husGzwEtZ?p=52)；[杰哥 P52](https://www.bilibili.com/video/BV1Up4y1Y76a?p=52)、[P53](https://www.bilibili.com/video/BV1Up4y1Y76a?p=53)；[米哥 P57](https://www.bilibili.com/video/BV1swAWerEzS?p=57)；[ok姐 P45](https://www.bilibili.com/video/BV1vm421s7mv?p=45)、[P46](https://www.bilibili.com/video/BV1vm421s7mv?p=46)

### 不定积分的记号约定与名称含义
- **要点**：积分号与 dx 配套存在（共存亡），dx 表示积分变量是 x；「不定」指的是积分上下限没有限定。习惯用小 f(x) 表示导函数、用大 F(x) 表示原函数，看到原函数就用大 F(x) 表示是固定切入点。原函数不唯一（x²、x²+1、x²+C 求导都得 2x），F(x) 与 f(x) 是多对一的关系。
- **关键概念**：`积分号`、`dx`、`共存亡`、`不定`、`多对一`、`大 F(x)`
- **相互关系**：原函数与导函数是多对一关系，故不定积分的结果要加上任意常数 C；与求导互为逆运算，是后面全部积分计算的基础。
- **出处**：[学士帽 P54](https://www.bilibili.com/video/BV1X4411J792?p=54)

### 不定积分的性质（可拆性、常数外提与两个口诀）
- **要点**：①∫[f(x)±g(x)]dx=∫f(x)dx±∫g(x)dx（乘除不能拆）；②∫k f(x)dx=k∫f(x)dx（k 为常数，与积分变量无关）。口诀「先积后导为本身」：[∫f(x)dx]′=f(x)、d∫f(x)dx=f(x)dx，「本身」指被积函数。口诀「先导后积为本身加 C」：∫f′(x)dx=f(x)+C、∫dF(x)=F(x)+C，「本身」指未求导前的那个函数。最后一步是积分就加 C，是求导就不加。
- **关键概念**：`可拆性`、`常数外提`、`先积后导`、`先导后积`、`加 C 规则`
- **相互关系**：两个口诀中「本身」含义不同，是主要易错点，也是选填高频考点。
- **出处**：[陈哥 P52](https://www.bilibili.com/video/BV1husGzwEtZ?p=52)；[杰哥 P52](https://www.bilibili.com/video/BV1Up4y1Y76a?p=52)、[P54](https://www.bilibili.com/video/BV1Up4y1Y76a?p=54)；[米哥 P58](https://www.bilibili.com/video/BV1swAWerEzS?p=58)；[ok姐 P48](https://www.bilibili.com/video/BV1vm421s7mv?p=48)、[P49](https://www.bilibili.com/video/BV1vm421s7mv?p=49)

### 由原函数表达式反求被积函数
- **要点**：题给 ∫f(x)dx=φ(x)+C，则 f(x)=φ′(x)；若问 dF(x)，用 dF(x)=F′(x)dx 直接写出。题干给出「f(x) 的原函数是 F(x)」时，必须同时挖出两条信息：一是 ∫f(x)dx=F(x)+C，二是 f(x)=F′(x)，两条缺一不可。求 f 在另一处的取值时，把该处的自变量代入已求出的 f 表达式即可。
- **关键概念**：`原函数`、`先积后导等于被积函数`、`先导后积等于本身`
- **出处**：[陈哥 P62](https://www.bilibili.com/video/BV1husGzwEtZ?p=62)；[杰哥 P53](https://www.bilibili.com/video/BV1Up4y1Y76a?p=53)

### 易错点：dx 与被积函数中的积分变量
- **要点**：①微分形式必须带 dx，如 d(x²)=2x dx，漏写 dx 在填空、大题中直接失分；②被积函数中含有积分变量的因子不能提到积分号外，例如 ∫e^x f(x)dx 中的 e^x 不可提出。与「常数可以外提」的区分点在是否为常数。
- **关键概念**：`dx`、`被积函数中含有积分变量`、`不能提到积分号外`
- **出处**：[陈哥 P52](https://www.bilibili.com/video/BV1husGzwEtZ?p=52)；[杰哥 P52](https://www.bilibili.com/video/BV1Up4y1Y76a?p=52)

### 易错点：导数相同只差一个常数
- **要点**：若 F′(x)=G′(x)，只能推出 F(x)=G(x)+C，即两函数相差一个常数，并不相等。若 F(x)、G(x) 都是 f(x) 的原函数，则 F(x)−G(x)=C——两者函数部分完全相同，只差积分常数。据此可判断选填题中关于「不定积分结果是否相同」的选项。
- **关键概念**：`相差一个常数`、`函数部分`
- **出处**：[陈哥 P52](https://www.bilibili.com/video/BV1husGzwEtZ?p=52)；[杰哥 P53](https://www.bilibili.com/video/BV1Up4y1Y76a?p=53)

### 基本积分公式：幂函数与指数函数
- **要点**：∫k dx=kx+C（被积函数为 1 时可省略）；∫x^a dx=x\^\{a+1\}/(a+1)+C（a≠−1），记忆两步法为「指数加一，再把加一后的指数取倒数作因子」；a=−1 时公式失效，此时 ∫(1/x)dx=ln|x|+C，绝对值不可省。特例 ∫(1/√x)dx=2√x+C、∫(1/x²)dx=−1/x+C。∫a^x dx=a^x/ln a+C，特例 ∫e^x dx=e^x+C。
- **关键概念**：`幂函数积分`、`a≠−1`、`ln|x|+C`、`指数加一`
- **相互关系**：幂函数要先化成幂指数形式（根式写成 x\^\{1/2\}、分式写成负指数）再用公式。
- **出处**：[陈哥 P51](https://www.bilibili.com/video/BV1husGzwEtZ?p=51)、[P53](https://www.bilibili.com/video/BV1husGzwEtZ?p=53)；[杰哥 P55](https://www.bilibili.com/video/BV1Up4y1Y76a?p=55)；[米哥 P58](https://www.bilibili.com/video/BV1swAWerEzS?p=58)；[ok姐 P45](https://www.bilibili.com/video/BV1vm421s7mv?p=45)、[P47](https://www.bilibili.com/video/BV1vm421s7mv?p=47)

### 基本积分公式：三角函数十式
- **要点**：分五组：①∫sin x dx=−cos x+C，∫cos x dx=sin x+C；②∫tan x dx=−ln|cos x|+C，∫cot x dx=ln|sin x|+C；③∫sec x dx=ln|sec x+tan x|+C，∫csc x dx=ln|csc x−cot x|+C；④∫sec²x dx=tan x+C，∫csc²x dx=−cot x+C；⑤∫sec x tan x dx=sec x+C，∫csc x cot x dx=−csc x+C。另有 ∫1/(1+x²)dx=arctan x+C、∫1/√(1−x²)dx=arcsin x+C。
- **关键概念**：`sec`、`csc`、`cot`、`arcsin x`、`arctan x`
- **相互关系**：第三组最难记，可用 S 对应 C、C 对应 S 的开头字母规律辅助记忆；结果可用求导回代检验。
- **出处**：[陈哥 P51](https://www.bilibili.com/video/BV1husGzwEtZ?p=51)、[P53](https://www.bilibili.com/video/BV1husGzwEtZ?p=53)；[杰哥 P55](https://www.bilibili.com/video/BV1Up4y1Y76a?p=55)；[米哥 P58](https://www.bilibili.com/video/BV1swAWerEzS?p=58)；[ok姐 P45](https://www.bilibili.com/video/BV1vm421s7mv?p=45)、[P47](https://www.bilibili.com/video/BV1vm421s7mv?p=47)

### 基本积分公式结果中的负号处理
- **要点**：被积函数中带负号时，负号统一提到积分号外面再做，所以对应 ∫1/√(1−x²)dx=arcsin x+C 与 ∫1/(1+x²)dx=arctan x+C 两条公式，结果是 −arcsin x+C、−arctan x+C，而不是 arccos x、arccot x。
- **关键概念**：`负号外提`、`−arcsin x+C`、`−arctan x+C`、`arccos x`、`arccot x`
- **相互关系**：与求导基本公式互为逆运算；是基本公式法、凑微分法、分部积分法共同的基础。
- **出处**：[学士帽 P55](https://www.bilibili.com/video/BV1X4411J792?p=55)

### 含常数 a 的积分公式（第十组）
- **要点**：∫1/(a²+x²)dx=(1/a)arctan(x/a)+C、∫1/√(a²−x²)dx=arcsin(x/a)+C、∫1/(x²−a²)dx=(1/2a)ln|(x−a)/(x+a)|+C、∫1/(a²−x²)dx=(1/2a)ln|(a+x)/(a−x)|+C、∫1/√(x²±a²)dx=ln|x+√(x²±a²)|+C。
- **关键概念**：`第十组公式`、`arctan`、`arcsin`、`对数型积分`
- **相互关系**：最易混的两条是 1/(x²−a²) 与 1/(a²−x²)（互为相反数，前者积出对数、后者积出反正弦）。
- **出处**：[陈哥 P53](https://www.bilibili.com/video/BV1husGzwEtZ?p=53)；[米哥 P58](https://www.bilibili.com/video/BV1swAWerEzS?p=58)

### 积分公式的验算方法
- **要点**：判断积分结果是否正确，只需把结果求导，看是否等于被积函数；等于则正确，否则错误。对含 ln 的结果，求导时按复合函数逐层求导，可回推出被积函数。
- **关键概念**：`验算`、`积分结果求导`、`复合函数求导`
- **相互关系**：直接依据「求导与积分互逆」；在化简结果、判断两个形式是否等价时也常用。
- **出处**：[陈哥 P53](https://www.bilibili.com/video/BV1husGzwEtZ?p=53)、[P58](https://www.bilibili.com/video/BV1husGzwEtZ?p=58)

### 直接积分法：方法本质与幂指函数型
- **要点**：不做换元，只对被积函数作代数变形，化成基本形式后套公式；常用工具是四则运算、幂指运算、乘法公式（平方差、完全平方、立方和差）、三角公式。适用于被积函数经代数化简能变成基本积分公式形式时。幂指函数型：根式、分式幂相乘除时先统一化为 x 的幂（√[n]{x^a}=x\^\{a/n\}、1/x^a=x\^\{−a\}），用同底数幂相乘（指数相加）、相除（指数相减）整理成单项幂再套公式。指数型：a^x b^x=(ab)^x、a^x/b^x=(a/b)^x，积分用 ∫a^x dx=a^x/ln a+C；加减型分式先按减号拆开再逐项处理。
- **关键概念**：`直接积分法`、`同底数幂运算`、`(ab)^x`、`化简`、`基本积分公式`
- **相互关系**：化简不了时才转向凑微分、换元、分部积分。
- **出处**：[陈哥 P54](https://www.bilibili.com/video/BV1husGzwEtZ?p=54)、[P55](https://www.bilibili.com/video/BV1husGzwEtZ?p=55)、[P56](https://www.bilibili.com/video/BV1husGzwEtZ?p=56)；[杰哥 P55](https://www.bilibili.com/video/BV1Up4y1Y76a?p=55)、[P56](https://www.bilibili.com/video/BV1Up4y1Y76a?p=56)

### 直接积分法：分式型（假分式与部分分式）
- **要点**：①分子分母同次（或含相同项）：分子按分母凑，缺什么补什么、多退少补（分母为 1+x² 而分子含 x² 时，把分子写成 (1+x²)−1 后按加减拆开）；②分子次数高于分母：拆项降次（部分分式思想），用「加一项减一项」拆成整式与真分式之和；③分母为两个因式相乘：拆成「小分之一减大分之一」再补系数，通分验证（分母为 x²(1+x²) 时拆成 1/x²−1/(1+x²) 并通分验证分子恰为 1）。①与②本质都是凑出与分母相同的因式后约分；分子次数低于分母的有理函数积分专升本基本不考。
- **关键概念**：`分子按分母凑`、`降次`、`部分分式`、`拆分`、`通分验证`
- **相互关系**：拆开后分别落入幂函数积分与 arctan x 公式。
- **出处**：[陈哥 P54](https://www.bilibili.com/video/BV1husGzwEtZ?p=54)；[杰哥 P55](https://www.bilibili.com/video/BV1Up4y1Y76a?p=55)

### 直接积分法：三角函数型
- **要点**：分母为 cos x sin x 时用 1=sin²x+cos²x 拆项约分；分子为 cos 2x 时按分母选二倍角形式；遇平方用降幂公式，遇 tan²x 换成 sec²x−1、cot²x 换成 csc²x−1；切化弦；见 2x 用二倍角降倍；数字 1 可写成 sin²x+cos²x。分式型应让分子产生分母的因式以便约分，如 cos2x/(cos x−sin x) 选 cos2x=cos²x−sin²x 分解后约去分母。含「1+三角函数」的用消一：1+cos2x 用 cos2x=2cos²x−1 消去 1；1+sin x 用分子分母同乘 1−sin x 造平方差。
- **关键概念**：`消一`、`平方差`、`分子产生分母`、`降幂公式`、`tan²x=sec²x−1`
- **相互关系**：三类中三角函数型变形最多、难度最高，难点在变形而非积分本身；遇平方型必须用降次而非平方和，否则仍积不出来。
- **出处**：[陈哥 P54](https://www.bilibili.com/video/BV1husGzwEtZ?p=54)；[杰哥 P57](https://www.bilibili.com/video/BV1Up4y1Y76a?p=57)

### 微分的复习与凑微分的本质
- **要点**：微分即 dF(x)=F′(x)dx，由函数求微分只需先求导再乘 dx。凑微分是反过程：已知 f′(x)dx 的形式，反求它是哪个函数的微分 dF(x)，本质就是求原函数（「谁求导等于它」）。由于 dF(x)=d[F(x)+C]，凑微分时不加常数也不影响正确性。凑微分又称第一类换元法。学士帽把凑微分法表述为把一个因子放到 d 的后面（即对它求原函数），使 d 后的表达式与前面某部分形式一致，从而把整体看成基本积分公式中的变量并套用公式；并给出两条操作规则——d 后面可以任意加减常数而不影响结果（d(x²) 与 d(x²+1) 求导都得 2x dx），d 后面也可以乘常数、但要在积分号前乘上相应的倒数配平（如 ∫dx/(2x−1) 写成 ½∫d(2x−1)/(2x−1)）；凑好后把 d 后与前面相同的部分圈起来、想象成最简单的 x 再套基本公式，得 ln|x+1|+C、½ln|2x−1|+C。
- **关键概念**：`微分`、`凑微分`、`反求原函数`、`第一类换元法`
- **相互关系**：与第二类换元法（根式代换）相对。
- **出处**：[陈哥 P55](https://www.bilibili.com/video/BV1husGzwEtZ?p=55)；[学士帽 P57](https://www.bilibili.com/video/BV1X4411J792?p=57)、[P58](https://www.bilibili.com/video/BV1X4411J792?p=58)；[ok姐 P33](https://www.bilibili.com/video/BV1vm421s7mv?p=33)、[P49](https://www.bilibili.com/video/BV1vm421s7mv?p=49)、[P50](https://www.bilibili.com/video/BV1vm421s7mv?p=50)

### 凑微分的数学表达式与核心原理
- **要点**：∫f[g(x)]g′(x)dx=∫f[g(x)]d[g(x)]，再令 u=g(x) 得 ∫f(u)du=F(u)+C，最后回代 u=g(x)。核心是在被积函数中找出导数关系：若两个因子仅相差常数倍，就通过配系数把它写成某个函数的导数。d 后到 d 前是求导、d 前到 d 后是积分；常数可任意乘除后挪动，d 后整体可任意加减常数。解题步骤：找导数关系 → 配系数写导数形式 → 凑微分 → 换元 → 积分 → 回代；找不到导数关系时一般不考虑凑微分。
- **关键概念**：`第一类换元法`、`导数关系`、`配系数`、`回代`、`g′(x)dx=dg(x)`
- **相互关系**：熟练后「令 u」这一步可在心里完成而不写出；成功条件是两部分既满足乘除关系、又存在导数关系；凑微分不成功再考虑分部积分。
- **出处**：[陈哥 P55](https://www.bilibili.com/video/BV1husGzwEtZ?p=55)；[杰哥 P58](https://www.bilibili.com/video/BV1Up4y1Y76a?p=58)；[米哥 P62](https://www.bilibili.com/video/BV1swAWerEzS?p=62)；[ok姐 P49](https://www.bilibili.com/video/BV1vm421s7mv?p=49)、[P50](https://www.bilibili.com/video/BV1vm421s7mv?p=50)

### 凑微分的做题步骤与复杂/简单函数
- **要点**：①把被积函数拆成乘法或除法关系；②定出复杂函数与简单函数；③对复杂函数本身或内层求导，看能否得到简单函数或其倍数；④用求导结果替换简单函数；⑤凑微分并整体换元；⑥回代原变量。第③步找导数是关键，也是命题不直接给出、最难的一步；复杂与简单可以互换试探。
- **关键概念**：`复杂函数`、`简单函数`、`导数关系`
- **出处**：[杰哥 P58](https://www.bilibili.com/video/BV1Up4y1Y76a?p=58)

### 直接凑微分（常见导数关系）
- **要点**：看哪个因子是内层函数的导数：2x dx=d(x²)、x dx=½d(x²)、(1/x)dx=d(ln x)、e^x dx=d(e^x)、cos x dx=d(sin x)、(1/(1+x²))dx=d(arctan x)、(1/√x)dx=2d(√x)、(1/x²)dx=−d(1/x)、sec²x dx=d(tan x)、sin x dx=−d(cos x)（有负号）、csc²x dx=−d(cot x)；挪动后把 d 后整体看作一个字母，套公式再回代。常考结果 ∫e^u du=e^u+C、∫du/u=ln|u|+C、∫du/(1+u²)=arctan u+C、∫du/√u=2√u+C。学士帽给出与对数函数有关的凑微分一般形式 ∫(1/x)f(ln x)dx=∫f(ln x)d(ln x)：被积函数中同时出现 ln x 与单独的 1/x 时，把单独的 1/x 放到 d 后（放过去的是它的原函数 ln x），如 ∫dx/(x ln x)=ln|ln x|+C、∫(ln x/x)dx=½(ln x)²+C；与指数函数有关的凑微分一般形式 ∫e^x f(e^x)dx=∫f(e^x)d(e^x)，如 ∫e^x cos e^x dx=sin e^x+C，若被积函数中没有单独的 e^x（如 ∫dx/(1+e^x)），就让分子构造分母（分子写成 1+e^x−e^x 后按分子拆项）得 x−ln(1+e^x)+C，而 ∫dx/(e^x+e\^\{−x\}) 分子分母同乘 e^x 得 ∫d(e^x)/((e^x)²+1)=arctan e^x+C；三角函数的凑微分：同时含 cos x 与 sin x 时把单独的 cos x 凑成 d(sin x)，单独出现的是 sin x 则凑成 d(cos x) 并把负号提到积分号外，遇 tan x、cot x 先化为 sin x/cos x、cos x/sin x，遇 sin²x 用 sin²x=1−cos²x 转化为含 cos x 的形式。
- **关键概念**：`g′dx=dg`、`d√x`、`d ln x`、`d(arctan x)`
- **出处**：[杰哥 P58](https://www.bilibili.com/video/BV1Up4y1Y76a?p=58)；[米哥 P62](https://www.bilibili.com/video/BV1swAWerEzS?p=62)、[P63](https://www.bilibili.com/video/BV1swAWerEzS?p=63)；[学士帽 P57](https://www.bilibili.com/video/BV1X4411J792?p=57)、[P58](https://www.bilibili.com/video/BV1X4411J792?p=58)、[P69](https://www.bilibili.com/video/BV1X4411J792?p=69)

### 含 e^x 类型的凑微分
- **要点**：把 e^x 凑到 d 后并配常数（e\^\{ax\}dx=(1/a)d(e\^\{ax\})）；无法直接凑时用「加减同一项」拆分或上下同乘 e^x（或 e\^\{−x\}）；遇 e\^\{−x\} 就上下同乘 e^x，把 e\^\{−x\} 化成 1/e^x，使分母出现 1+(e^x)²，再用 arctan 公式，结果含 arctan e^x；有时应凑 d(1+e^x) 整体。
- **关键概念**：`e^x 型`、`同乘因子`、`1+(e^x)²`
- **出处**：[米哥 P63](https://www.bilibili.com/video/BV1swAWerEzS?p=63)；[杰哥 P59](https://www.bilibili.com/video/BV1Up4y1Y76a?p=59)

### 凑微分的六种类型
- **要点**：①内层为 ax+b：凑 d(ax+b) 并在积分号外补系数 1/a（dx=(1/a)d(ax+b)，常数 b 可任意加减），条件是「x 处为一次函数」，如 ∫(3x+1)²dx=⅑(3x+1)³+C、∫e\^\{5t\}dt=⅕e\^\{5t\}+C。②幂函数型：出现 x^a 与 x\^\{a−1\}（幂次相差 1）时把低次幂写成高次幂的导数并补系数 1/a；要有整体思维，优先把「整体」（1−x²、1+x²、1+e^x）作为求导对象，否则换元后会得到难以积分的 √(1−u) 之类形式。③含 e^x 型。④含 √x：(√x)′=1/(2√x)，把 (1/√x)dx 写成 2d√x。⑤含 1/x²：(1/x)′=−1/x²，故 (1/x²)dx=−d(1/x)，补负号抵消。⑥含 ln x：(ln x)′=1/x，遇 1/x 与 ln x 同现即凑 d ln x，必须把含 ln x 的整体作为微分对象。
- **关键概念**：`配系数`、`整体思维`、`负号抵消`、`d√x`、`d ln x`、`直接凑微分法`
- **相互关系**：六类都遵循「找导数关系 → 配系数 → 凑微分 → 换元 → 回代」同一套路；②常有一题多解，不同凑法结果形式不同但可化为同一结果。
- **出处**：[陈哥 P56](https://www.bilibili.com/video/BV1husGzwEtZ?p=56)、[P57](https://www.bilibili.com/video/BV1husGzwEtZ?p=57)；[杰哥 P61](https://www.bilibili.com/video/BV1Up4y1Y76a?p=61)

### 六个基本凑微分方向（三角）
- **要点**：∫f(sin x)cos x dx=∫f(sin x)d sin x；∫f(cos x)sin x dx=−∫f(cos x)d cos x；∫f(tan x)sec²x dx=∫f(tan x)d tan x；∫f(cot x)csc²x dx=−∫f(cot x)d cot x；∫f(sec x)sec x tan x dx=∫f(sec x)d sec x；∫f(csc x)csc x cot x dx=−∫f(csc x)d csc x。后两个方向因求导带负号，前面需补负号抵消。
- **关键概念**：`凑微分`、`sec²x`、`csc²x`、`sec x tan x`
- **相互关系**：多数题实际只用 sin、cos 两个方向。
- **出处**：[陈哥 P58](https://www.bilibili.com/video/BV1husGzwEtZ?p=58)

### 反三角函数与幂函数的凑微分
- **要点**：含 arcsin x 且同时有 1/√(1−x²) 时凑成 d(arcsin x)；含 arccos x 且同时有 1/√(1−x²) 时补负号凑 d(arccos x)；含 arctan x 且同时有 1/(1+x²) 时凑成 d(arctan x)；含 arccot x 时补负号凑 d(arccot x)；幂函数型一般形式 x^a f(x\^\{a+1\})，把低一次的 x^a 凑成 (1/(a+1))d(x\^\{a+1\})。补负号的依据是 arccot x 与 arccos x 的导数本身带负号。
- **关键概念**：`d(arcsin x)`、`d(arctan x)`、`低次幂放 d 后`、`补负号`
- **相互关系**：结构与幂函数型一致，只是内层函数换成反三角函数；解题时要「把分式整体看作一个微分」。
- **出处**：[陈哥 P61](https://www.bilibili.com/video/BV1husGzwEtZ?p=61)；[学士帽 P58](https://www.bilibili.com/video/BV1X4411J792?p=58)

### 抽象函数的凑微分
- **要点**：已知 ∫f(x)dx=F(x)+C，求含 f(φ(x)) 的积分时，先把 φ′(x)dx 凑成 dφ(x)，把积分化为 ∫f(u)du 形式，结果即为 F(u)+C（必要时补负号、系数），最后把 u 回代为 φ(x)。常考形式包括 f(cos x)sin x、f(e\^\{−x\})e\^\{−x\}、f(√x)/√x 等；配系数的方法是先凑再看求导结果与原式的差异，用系数抵消。
- **关键概念**：`抽象函数`、`整体换元`、`系数抵消`
- **出处**：[陈哥 P62](https://www.bilibili.com/video/BV1husGzwEtZ?p=62)

### 必备的三角恒等变形（积分前）
- **要点**：做三角积分前必须熟练三类公式——平方关系 sin²x+cos²x=1、1+tan²x=sec²x、1+cot²x=csc²x；二倍角公式（sin2x 与 cos2x）；降幂公式。遇 tan²x=sec²x−1、cot²x=csc²x−1；切化弦；见 2x 用二倍角降倍；数字 1 可写成 sin²x+cos²x。遇到不熟悉的 tan、sec 一般先化成 sin、cos 再处理。
- **关键概念**：`平方关系`、`二倍角公式`、`降幂公式`
- **相互关系**：积分公式与三角公式要同时掌握，否则无法判断该往哪个方向配。
- **出处**：[陈哥 P58](https://www.bilibili.com/video/BV1husGzwEtZ?p=58)、[P59](https://www.bilibili.com/video/BV1husGzwEtZ?p=59)、[P60](https://www.bilibili.com/video/BV1husGzwEtZ?p=60)；[米哥 P61](https://www.bilibili.com/video/BV1swAWerEzS?p=61)；[杰哥 P57](https://www.bilibili.com/video/BV1Up4y1Y76a?p=57)

### 用凑微分证明基本积分公式
- **要点**：六个基本三角积分公式都能用凑微分反推：∫tan x dx=−ln|cos x|+C、∫cot x dx=ln|sin x|+C、∫sec x tan x dx=sec x+C、∫csc x cot x dx=−csc x cot x（原式见公式表）。较难的两个 ∫sec x dx=ln|sec x+tan x|+C、∫csc x dx=ln|csc x−cot x|+C 需先分子分母同乘共轭，把分母化成平方差，再用 ∫du/(u²−a²)=(1/2a)ln|(u−a)/(u+a)|+C，最后把分子分母的平方提出对数、用绝对值相同来化简。
- **关键概念**：`分子分母同乘共轭`、`平方差公式`、`对数运算法则`
- **相互关系**：属「基本积分公式」与「换元法」的桥梁。
- **出处**：[陈哥 P58](https://www.bilibili.com/video/BV1husGzwEtZ?p=58)

### 三角积分：单项奇次幂与偶次幂
- **要点**：单项奇次幂（cos³x、sin⁵x、tan³x）：把奇次拆成一个偶次乘一个一次，一次项凑到微分号后（cos x dx=d sin x），偶次项用平方关系换成另一函数的形式（cos²x=1−sin²x），再按幂函数积分；tan 的一次项不是任何函数的导数，不能用此法，应先把 tan² 换成 sec²−1 后拆成两个积分。单项偶次幂：首选降幂，拆成两个积分；tan²x 直接换成 sec²x−1；sec⁴x 拆成 sec²x·sec²x，一个平方凑成 d tan x，另一个用 1+tan²x=sec²x 变形。
- **关键概念**：`拆奇次为偶次×一次`、`降幂公式`、`凑 d tan x`、`奇拆偶降`
- **相互关系**：两者同为「单项幂」，区别只在奇次还是偶次；sec 的奇次幂无法用凑微分解决，需留到分部积分。
- **出处**：[陈哥 P59](https://www.bilibili.com/video/BV1husGzwEtZ?p=59)；[杰哥 P60](https://www.bilibili.com/video/BV1Up4y1Y76a?p=60)

### 三角积分：分母为 1±sin x、1±cos x（乘共轭）
- **要点**：分母为 1±sin x 或 1±cos x 时，分子分母同乘其共轭形式，分母化成平方差后成为 sin²x 或 cos²x，再拆开约分。此类型不能把分子 1 换成 sin²+cos²，那样做不出来。
- **关键概念**：`共轭形式`、`平方差`、`拆分约分`
- **相互关系**：判断依据是分母是否为 1±三角函数。
- **出处**：[陈哥 P59](https://www.bilibili.com/video/BV1husGzwEtZ?p=59)

### 三角积分：分子为常数、分母为 sin 与 cos 的组合
- **要点**：形如分子很小、分母很大的「正三角」式被积函数，处理方向是让分子变复杂：把分子 1 写成 sin²x+cos²x，拆成两项后分别与分母约分，得到两个可积的项。若拆开后出现偶次幂，继续用降幂或凑微分。
- **关键概念**：`分子化为 sin²+cos²`、`拆分约分`、`倒三角`
- **相互关系**：若分母出现 1±三角形式则优先用共轭法。
- **出处**：[陈哥 P59](https://www.bilibili.com/video/BV1husGzwEtZ?p=59)

### 三角积分：分子分母同除 cos^n x（配 d tan x）
- **要点**：分子分母幂次之差为偶数时，分子分母同时除以 cos^n x（n 一般按分子分母的幂次差选取），目的是把式子配成含 sec²x dx 的形式，从而凑出 d tan x。除完后常用 1+tan²x=sec²x 化简，再令 u=tan x。除以多少次不是绝对的，若一次替换后仍有四次幂，可再令 u²=t 做第二次换元。
- **关键概念**：`同除 cosⁿx`、`配 d tan x`、`幂次差`
- **出处**：[陈哥 P60](https://www.bilibili.com/video/BV1husGzwEtZ?p=60)

### 三角积分：直接对分母做三角变换
- **要点**：用倍角、半角公式直接改写分母，例如把 1−cos x 写成 2sin²(x/2)，化成 csc² 形式后积分。分母为 sin x cos x 型时先提公因式 sin x，再用二倍角把 x 化为 x/2，最后回归类型五的做法。积分前常把系数直接凑进微分号（如 (1/2)dx=d(x/2)）。
- **关键概念**：`倍角公式`、`半角变形`、`d(x/2)`、`提公因式`
- **相互关系**：与类型五互为衔接——对分母做三角变换后往往就回到类型五的流程。
- **出处**：[陈哥 P60](https://www.bilibili.com/video/BV1husGzwEtZ?p=60)

### 三角积分：高次幂相乘（配微分）
- **要点**：高次幂相乘时，目标是配出某个可凑微分的因子（d sin x、d cos x、d tan x、d sec x、d cot x 都有可能）。做法是把乘积拆出一组「函数 × 其导数」的因子，其余部分用平方关系换成同一变量的多项式，再令整体为 u 积分。
- **关键概念**：`配 d sec x`、`拆出导数因子`、`整体换元`
- **相互关系**：是单项幂类型的推广；能否做出来取决于对基本积分公式的熟练程度。
- **出处**：[陈哥 P60](https://www.bilibili.com/video/BV1husGzwEtZ?p=60)

### 经典题型：分母为 cos x ± sin x 的待定系数法
- **要点**：分母为 cos x±sin x（分子可为 sin x、cos x 或常数）时，解法固定：把分子写成 A·(分母)+B·(分母的导数) 的形式，用待定系数法比较 sin x、cos x 的系数求出 A、B。求完后第一项直接积出（得 Ax），第二项因分子恰为分母的导数，凑微分后得对数。
- **关键概念**：`待定系数法`、`比较系数`、`分母的导数`、`凑微分`
- **出处**：[陈哥 P60](https://www.bilibili.com/video/BV1husGzwEtZ?p=60)

### 简单根式代换的适用条件与换元三部曲
- **要点**：目的是消除根号，前提是根号下为 x 的一次式（如 √[n]{ax+b}）；若根号下是 x 的平方（二次式），须改用三角代换。可代换形式三类：√[n]{ax+b}、√[n]{(ax+b)/(cx+d)}、√[n]{e\^\{ax\}+b}。换元三部曲：①令根式=t；②两边变形解出 x=φ(t)；③求微分 dx=φ′(t)dt——三步必须完整写在试卷上，是核心得分点。之后把被积函数中的 x、根式、dx 全部替换成 t 的表达式（换元要换干净）。若根号下是二次多项式（如 √(x(1−x))）不能整体换元（解不出 x），需拆成两个一次根式之积后只令其中一个为 t。
- **关键概念**：`第二类换元法`、`根式换元`、`消除根号`、`换元三部曲`、`换元要换干净`
- **相互关系**：换元后的积分一定可用直接积分或凑微分完成，不会引入新方法；开 n 次方时两边取 n 次方反解。
- **出处**：[陈哥 P63](https://www.bilibili.com/video/BV1husGzwEtZ?p=63)；[杰哥 P62](https://www.bilibili.com/video/BV1Up4y1Y76a?p=62)；[米哥 P65](https://www.bilibili.com/video/BV1swAWerEzS?p=65)；[ok姐 P53](https://www.bilibili.com/video/BV1vm421s7mv?p=53)、[P51](https://www.bilibili.com/video/BV1vm421s7mv?p=51)

### 多个根式：最小公倍数
- **要点**：同一被积函数中同时出现根指数不同的根式时，令 t=√[p]{ax+b}，其中 p 取各根指数的最小公倍数（2 与 3 取 6）。若根指数以分数指数形式给出（如 1/2 与 2/3），同样取分母的最小公倍数作为 p。
- **关键概念**：`最小公倍数`、`分数指数`、`统一根指数`
- **相互关系**：找最小公倍数是这类题唯一的难点，之后的化简都是常规运算。
- **出处**：[陈哥 P63](https://www.bilibili.com/video/BV1husGzwEtZ?p=63)；[杰哥 P62](https://www.bilibili.com/video/BV1Up4y1Y76a?p=62)；[米哥 P65](https://www.bilibili.com/video/BV1swAWerEzS?p=65)

### 换元后的化简与回代
- **要点**：换元后通常需先化简再积分：约分、分子加 1 减 1 后拆分、通分、用平方差或完全平方分解、利用 e\^\{ln A\}=A 把指数与对数互相消去。积分完成后必须回代，把 t 换回关于 x 的表达式，结果中不能残留 t。
- **关键概念**：`约分`、`加一减一`、`平方差`、`回代`
- **出处**：[陈哥 P63](https://www.bilibili.com/video/BV1husGzwEtZ?p=63)

### 三角代换的三种情形与选择
- **要点**：根号下为二次式时按根号类型选择代换：①√(a²−x²) → 令 x=a sin t，根号化为 a cos t，dx=a cos t dt（用 1−sin²t=cos²t）；②√(a²+x²) → 令 x=a tan t，根号化为 a sec t，dx=a sec²t dt（用 tan²t+1=sec²t）；③√(x²−a²) → 令 x=a sec t，根号化为 a tan t，需分 x>a 与 x&lt;−a 讨论。做题第一步必须先找出 a（如根号下 2−x² 时 a=√2），再写出 x=a·(对应三角函数)；须把所有 x（含 x²、dx）一并换掉。实际考得最多的是 sin 代换。
- **关键概念**：`三角代换`、`a 的确定`、`sin 代换`、`tan 代换`、`sec 代换`、`去根号`
- **相互关系**：与简单根式代换互补，判据是根号下为一次式还是一次以上；情形③因要分类讨论、考查极少；(1−x²)\^\{3/2\} 本质仍是根式。
- **出处**：[陈哥 P64](https://www.bilibili.com/video/BV1husGzwEtZ?p=64)；[杰哥 P63](https://www.bilibili.com/video/BV1Up4y1Y76a?p=63)；[米哥 P66](https://www.bilibili.com/video/BV1swAWerEzS?p=66)；[ok姐 P50](https://www.bilibili.com/video/BV1vm421s7mv?p=50)

### 三角代换的变量范围限定与绝对值
- **要点**：必须限定新变量 t 的范围：sin、tan 代换取 t∈(−π/2,π/2)，sec 代换按 x 的正负取相应区间。限定的目的是让开方后对应的三角函数值恒正，从而去掉绝对值，同时保证变量替换一一对应。若不加限定，开方会带绝对值、出现正负两种情况而无法继续。
- **关键概念**：`限定范围`、`一一对应`、`开方去绝对值`
- **出处**：[陈哥 P64](https://www.bilibili.com/video/BV1husGzwEtZ?p=64)

### 三角代换的回代：画三角形法
- **要点**：万能回代方法是画直角三角形。由最初的令的形式（如 sin t=x/1）确定对边与斜边，用勾股定理求出第三边，再按定义读出所需的 cos t、tan t 等。也可用反三角函数直接解出 t，依据是三角函数与其反函数互为反函数（sin t=x ⇒ t=arcsin x）。结果为单独的 t 时用反三角函数表示（由 x=a sin t 得 t=arcsin(x/a)）。必须回代，不能以 t 结尾，是最易失分的一步。不可把 t 直接代入 sin2t 之类式子。
- **关键概念**：`画三角形法`、`勾股定理`、`反函数互解`、`直角三角形`
- **相互关系**：回代时只看最初令的形式，不依赖中间推导；与三种根号类型一一对应。
- **出处**：[陈哥 P64](https://www.bilibili.com/video/BV1husGzwEtZ?p=64)；[杰哥 P63](https://www.bilibili.com/video/BV1Up4y1Y76a?p=63)；[ok姐 P50](https://www.bilibili.com/video/BV1vm421s7mv?p=50)

### 用三角代换证明积分公式
- **要点**：部分基本积分公式需用三角代换证明，如 ∫dx/√(a²+x²)=ln(x+√(x²+a²))+C：令 x=a tan t 后化为 ∫sec t dt，积出 ln|sec t+tan t|，回代得 ln[(√(x²+a²)+x)/a]，再把常数 ln a 吸收进任意常数 C；另如 ∫dx/√(a²−x²)=arcsin(x/a)+C。根号内为二次三项式时，先配方成完全平方再选用凑微分或三角代换。
- **关键概念**：`d sec t`、`常数吸收进 C`、`配方`、`完全平方`
- **相互关系**：与「用凑微分证明基本积分公式」并列，共同说明基本公式的来源；配方法是三角代换前的常见预处理。
- **出处**：[陈哥 P64](https://www.bilibili.com/video/BV1husGzwEtZ?p=64)

### 分部积分公式、推导与解题三步
- **要点**：∫u dv=uv−∫v du，由乘积求导法则 (uv)′=u′v+uv′ 两边积分、再把 ∫(uv)′dx 还原为 uv 移项即得（推导只作了解）；便于计算的形式 ∫u v′dx=uv−∫v u′dx（推荐记 v′ 形式，因常见积分以 dx 结尾）。解题三步：先判断被积函数是否为两个函数的乘积；①把 f(x) 拆成「一个函数 × 另一个函数的导数」；②把那个导数凑进微分号；③套分部积分公式。真正的新内容是第一步「拆」。
- **关键概念**：`u`、`v`、`dv`、`乘积求导法则`、`拆`
- **相互关系**：是继直接积分、凑微分、根式代换之后的第四种积分方法，学习重点在拆解；化简化不了、凑微分也凑不了（两函数相乘但无导数关系）时用分部积分；定出 v′ 后要积分求出 v（不加 C）。
- **出处**：[陈哥 P65](https://www.bilibili.com/video/BV1husGzwEtZ?p=65)、[P66](https://www.bilibili.com/video/BV1husGzwEtZ?p=66)；[杰哥 P64](https://www.bilibili.com/video/BV1Up4y1Y76a?p=64)

### 分部积分的拆解原则：反对幂指三
- **要点**：按「反三角函数 — 对数函数 — 幂函数 — 指数函数 — 三角函数」排序，排前者取作 u，排后者连同其导数凑到微分号后当 v′；指数与三角（幂指三 / 幂三指）谁前谁后均可。熟练后一眼即可判断谁该往后面凑。
- **关键概念**：`反对幂指三`、`u`、`v′`
- **相互关系**：该排序原则同时也是凑微分的先后原则；选 u 的内在逻辑是让 v 与 du 都变简单，dv 必须能积出来。
- **出处**：[陈哥 P65](https://www.bilibili.com/video/BV1husGzwEtZ?p=65)、[P66](https://www.bilibili.com/video/BV1husGzwEtZ?p=66)；[杰哥 P64](https://www.bilibili.com/video/BV1Up4y1Y76a?p=64)；[米哥 P67](https://www.bilibili.com/video/BV1swAWerEzS?p=67)、[P68](https://www.bilibili.com/video/BV1swAWerEzS?p=68)；[ok姐 P51](https://www.bilibili.com/video/BV1vm421s7mv?p=51)

### 分部积分题型一：积分式只有一个函数
- **要点**：积分式中只有反三角函数或对数函数时，把它看作 u、把 dx 看作 v′（即 v=x），直接套公式，无需再拆、凑。如 ∫ln x dx=x ln x−x+C、∫arcsin x dx=x arcsin x+√(1−x²)+C、∫arctan x dx。套完公式后出现的乘积部分常需再用凑微分处理。复合对数如 ln(1+x²) 求导后与分母约分；ln²x 需连续两次分部积分，两次产生的常数可合并记作一个 C。学士帽指出后续算 ∫v du 时仍需凑微分，如 ∫arcsin x dx 中出现低次幂 x 乘高次幂的结构，把 x 凑成 ½d(x²)，再通过加减常数把 √(1−x²) 整体设为新变量。
- **关键概念**：`∫ln x dx`、`∫arctan x dx`、`v=x`
- **相互关系**：比两个函数相乘的类型简单，第一步「拆」可省略。
- **出处**：[陈哥 P67](https://www.bilibili.com/video/BV1husGzwEtZ?p=67)；[杰哥 P64](https://www.bilibili.com/video/BV1Up4y1Y76a?p=64)；[学士帽 P60](https://www.bilibili.com/video/BV1X4411J792?p=60)

### 分部积分题型二：幂函数 × 三角函数 / 对数函数
- **要点**：幂函数 × 三角函数：幂函数作 u、三角函数凑微分；幂函数次数大于 1 时，一次分部积分后幂次下降，需重复分部积分直到降为一次。幂函数 × 对数函数：对数函数作 u，幂函数凑微分（x dx 凑成 d(x²/2)，x\^\{−2\}dx 凑成 d(−1/x)）；对数求导后化为 1/x，常与分母约分而大幅简化。
- **关键概念**：`降幂`、`多次分部积分`、`d(x²/2)`、`对数函数求导`
- **相互关系**：幂函数 × 三角与「幂函数 × 指数」套路完全一致。
- **出处**：[陈哥 P65](https://www.bilibili.com/video/BV1husGzwEtZ?p=65)、[P66](https://www.bilibili.com/video/BV1husGzwEtZ?p=66)

### 分部积分题型三：幂函数 × 指数函数 / 反三角函数
- **要点**：幂函数 × 指数函数：幂函数作 u、指数函数凑微分（e^x dx=d(e^x)），次数大于 1 时需多次分部积分降幂；遇到 x³e\^\{x²\} 一类，先拆出 x dx 凑成 d(x²)，再换元 u=x² 回到已学题型。幂函数 × 反三角函数：反三角函数作 u，幂函数凑微分；反三角函数求导后化为 1/(1+x²) 或 1/√(1−x²)，常与原有因式约掉。
- **关键概念**：`d(e^x)`、`换元`、`arctan x`、`arcsin x`
- **相互关系**：题型四是「对数/反三角作 u」的同族；题型三是题型一的同构变体。
- **出处**：[陈哥 P66](https://www.bilibili.com/video/BV1husGzwEtZ?p=66)

### 分部积分题型四：三角函数 × 指数函数（循环型）
- **要点**：e^x 与 sin x/cos x 相乘时，因两者求导都不改变函数类型，做两次分部积分后原积分会重新出现，得 I=一坨−I，移项得 2I=一坨，再除以 2，如 ∫e^x cos x dx=½e^x(sin x+cos x)+C；两次必须把同一类函数往后放。速算法：∫e\^\{ax\} sin bx dx 先写系数 1/(a²+b²)，再按二阶行列式「主对角相乘 − 副对角相乘」排列（第一行取导、第二行不取导）。幂函数求导会变零而指数、三角函数不会，是出现循环的根本原因。
- **关键概念**：`循环积分`、`移项`、`二阶行列式`、`两次分部积分`
- **出处**：[陈哥 P66](https://www.bilibili.com/video/BV1husGzwEtZ?p=66)；[杰哥 P64](https://www.bilibili.com/video/BV1Up4y1Y76a?p=64)；[米哥 P68](https://www.bilibili.com/video/BV1swAWerEzS?p=68)；[ok姐 P51](https://www.bilibili.com/video/BV1vm421s7mv?p=51)

### 分部积分题型五：被积函数含根号的复合函数
- **要点**：被积函数是含根号的复合函数（如 e\^\{√x\}）时，先用根式换元化为两类函数的乘积，再用分部积分。
- **关键概念**：`循环型分部积分`、`移项`、`根式换元`
- **相互关系**：是换元法与分部积分的组合。
- **出处**：[ok姐 P51](https://www.bilibili.com/video/BV1vm421s7mv?p=51)

### 分部积分进阶题型：由「原函数」条件反推
- **要点**：题干给「g(x) 是 f(x) 的一个原函数」，可同时得到两条信息：∫f(x)dx=g(x)+C 与 f(x)=g′(x)。再配合 ∫x f′(x)dx=x f(x)−∫f(x)dx 求解；出现 f″(x) 时凑成 d f′(x)，先求导再积分还原为 f′(x)。积分式中含 f′(x) 或 f″(x) 时优先用分部积分：把 f′(x)dx 凑成 df(x)，取 u=x、v=f(x)。
- **关键概念**：`原函数`、`直接函数`、`d f′(x)`、`抽象函数`
- **出处**：[陈哥 P68](https://www.bilibili.com/video/BV1husGzwEtZ?p=68)；[杰哥 P64](https://www.bilibili.com/video/BV1Up4y1Y76a?p=64)

### 积分在线（相消型）
- **要点**：把积分拆两部分，一部分分部展开后出现与另一部分符号相反的相同项，直接抵消。
- **关键概念**：`抵消`
- **出处**：[米哥 P69](https://www.bilibili.com/video/BV1swAWerEzS?p=69)

### 万能公式
- **要点**：令 tan(x/2)=t，则 sin x=2t/(1+t²)、cos x=(1−t²)/(1+t²)、dx=2/(1+t²)dt；超出专升本考纲。
- **关键概念**：`万能公式`
- **出处**：[米哥 P69](https://www.bilibili.com/video/BV1swAWerEzS?p=69)

### 有理函数与真、假分式
- **要点**：形如 P(x)/Q(x)（P,Q 为多项式，Q(x)≠0）的积分。分子最高次 ≥ 分母最高次为假分式，小于则为真分式，两者积分方法不同。假分式用多项式除法化为「多项式 + 真分式」。
- **关键概念**：`有理函数`、`真分式`、`假分式`、`多项式除法`
- **相互关系**：升本阶段分子次数不超过分母次数且不超过二次，故只讨论分母为一次或二次多项式的情形。
- **出处**：[陈哥 P69](https://www.bilibili.com/video/BV1husGzwEtZ?p=69)；[ok姐 P52](https://www.bilibili.com/video/BV1vm421s7mv?p=52)

### 真分式的三种处理
- **要点**：（一）分子恰为分母的导数或只差一个常数倍数时，把分子凑进微分号写成 d(Q(x))，再按 ∫du/u=ln|u| 处理。（二）分母为二次式时配方成 (x+a)²+b² 或 b²−(x−a)²，凑微分后套 arctan、arcsin 公式；含 √x 的分母可把 (1/√x)dx 凑成 2d(√x) 后再看成整体。（三）分母能分解为两个一次因式时拆成 A/(x−a)+B/(x−b)：待定系数法用通分、合并同类项、比较分子系数解方程组；留数法令某因式为零求出该点，代入原式并划掉与之相同的因式项即得对应分子，更快。待定系数法的设定规则：分母一次则分子设常数，分母二次则分子设一次式。
- **关键概念**：`凑微分`、`配完全平方`、`待定系数法`、`留数法`、`列项`
- **相互关系**：留数法是待定系数法的快捷版，仅适用于分母最高次为二次、分子为一次或常数的情形；不可分解的二次分母难度陡增、升本基本不考。
- **出处**：[陈哥 P69](https://www.bilibili.com/video/BV1husGzwEtZ?p=69)；[ok姐 P52](https://www.bilibili.com/video/BV1vm421s7mv?p=52)

### 按分母次数分类的求解套路
- **要点**：分母为一次：分子为常数时直接凑微分；分子也为一次时配凑出分母，拆成「1 + 真分式」再积分。分母为二次：分子为常数、分母可分解时先分解因式再列项（1/((x+a)(x+b)) 拆成两个分式之差，注意验算是否需配常数）；分母不可分解时配完全平方凑成 1/(1+u²) 得反正切；分子为一次时先凑出分母的微分，余下部分按上述两种情形处理。分子分母同为二次时用配凑化为「多项式 + 真分式」再回到上述情形。
- **关键概念**：`分解因式`、`列项`、`配完全平方`、`分母的微分`
- **出处**：[ok姐 P52](https://www.bilibili.com/video/BV1vm421s7mv?p=52)

### 特殊类型 x(x^n+1) 型
- **要点**：分母提出 x 后，分子分母同乘 x\^\{n−1\}，把 x\^\{n−1\}dx 凑成 (1/n)d(x^n)，再换元 u=x^n 化为 ∫du/[u(1+u)]，用留数法拆项积分。
- **关键概念**：`d(x^n)`、`换元`
- **出处**：[陈哥 P69](https://www.bilibili.com/video/BV1husGzwEtZ?p=69)

### 假分式：加一减一 与 多项式除法
- **要点**：假分式首选「加 1 减 1」降幂，拆成整式与真分式；不能直接拆时（如分母 x³+1）先用立方和、平方差公式因式分解再约分。万能方法是多项式除法：被除式 = 除式 × 商 + 余式，可把任意假分式化为多项式加真分式。
- **关键概念**：`加1减1`、`立方和公式`、`多项式除法`、`余式`
- **相互关系**：多项式除法几乎可解决所有假分式积分。
- **出处**：[陈哥 P69](https://www.bilibili.com/video/BV1husGzwEtZ?p=69)


### 原函数的概念与存在定理
- **要点**：若 $F'(x)=f(x)$（等价地 $dF(x)=f(x)dx$），则称 $F(x)$ 是 $f(x)$ 的一个原函数。积分是求导的逆运算，即已知导数求原来的函数。原函数存在定理：若 $f(x)$ 在某区间内连续，则它在该区间上一定有原函数。
- **关键概念**：`原函数`、`$F'(x)=f(x)$`、`$dF(x)=f(x)dx$`、`原函数存在定理`、`连续必有原函数`
- **相互关系**：求导要求曲线连续且光滑，而求原函数只要求连续；不定积分就是「已知导数求原函数」的过程，第三章全部内容都建立在这一概念上。
- **出处**：[石头 P43](https://www.bilibili.com/video/BV18CL26WEJ3?p=43)

### 不定积分的概念与记号
- **要点**：$f(x)$ 的全体原函数称为 $f(x)$ 的不定积分，记作 $\int f(x)dx=F(x)+C$，其中 $C$ 为任意常数。记号中 $\int$ 由 sum 的 $S$ 拉长而来，含求和之意；$f(x)$ 是被积函数，$f(x)dx$ 是被积表达式，$x$ 是积分变量。求不定积分必须加 $C$，否则只是求出了一个原函数。
- **关键概念**：`不定积分`、`$\int f(x)dx=F(x)+C$`、`被积函数`、`被积表达式`、`积分变量`、`任意常数 $C$`
- **相互关系**：原函数不唯一，若有一个原函数 $F(x)$，则 $F(x)+C$ 都是原函数，它们之间只相差一个常数；因 $(\ln(-x))'=\frac1x$，故 $\int\frac1x dx=\ln|x|+C$ 必须带绝对值。
- **出处**：[石头 P43](https://www.bilibili.com/video/BV18CL26WEJ3?p=43)

### 基本积分公式表
- **要点**：需掌握的 12 个基本积分公式：$\int k\,dx=kx+C$；$\int x^a dx=\frac{x\^\{a+1\}}{a+1}+C$（$a\ne-1$）；$\int\frac{1}{x}dx=\ln|x|+C$；$\int e^x dx=e^x+C$；$\int a^x dx=\frac{a^x}{\ln a}+C$；$\int\frac{1}{1+x^2}dx=\arctan x+C$；$\int\frac{1}{\sqrt{1-x^2}}dx=\arcsin x+C$；$\int\cos x\,dx=\sin x+C$；$\int\sin x\,dx=-\cos x+C$；$\int\frac{1}{\cos^2x}dx=\tan x+C$；$\int\frac{1}{\sin^2x}dx=-\cot x+C$；$\int\sec x\tan x\,dx=\sec x+C$。
- **关键概念**：`基本积分公式表`、`$\int x^a dx=\frac{x^{a+1}}{a+1}+C$`、`$\int\frac1x dx=\ln|x|+C$`
- **相互关系**：这些公式就是第二章求导基本公式反过来写，对照记忆即可；幂函数积分是「次数加一再除以新次数」，指数函数 $e^x$ 积分后仍是本身。
- **出处**：[石头 P43](https://www.bilibili.com/video/BV18CL26WEJ3?p=43)

### 不定积分的线性性质与互逆规律
- **要点**：线性性质：$\int[f(x)\pm g(x)]dx=\int f(x)dx\pm\int g(x)dx$；$\int kf(x)dx=k\int f(x)dx$（$k$ 为非零常数，$k=0$ 时不成立，因为左边为 $C$、右边为 $0$）。多个不定积分相加减时最后只写一个 $C$。互逆规律：先积后导、先积后微都等于本身；先导后积、先微后积都等于本身加 $C$。记号规律：最外层是 $d$ 则结果带 $dx$，最外层是积分号则结果带 $C$，最外层是求导则既不带 $dx$ 也不带 $C$。
- **关键概念**：`线性性质`、`$\int kf(x)dx=k\int f(x)dx$`、`先积后导等于本身`、`先导后积加 $C$`、`最外层定结果`
- **相互关系**：这两条规律是解「积分与求导混合」选择题的最快方法，用排除法看有没有 $C$、有没有 $dx$ 即可秒选。
- **出处**：[石头 P43](https://www.bilibili.com/video/BV18CL26WEJ3?p=43)

### 直接积分法与拆字诀
- **要点**：直接积分法就是套用基本积分公式表与不定积分的前两条性质，把被积函数拆成若干个可直接查公式的和或差再逐项积分。核心是一个「拆」字：遇到乘积先乘开，遇到商先化成幂函数或拆项，遇到复杂式子先用恒等变形化简。
- **关键概念**：`直接积分法`、`拆字诀`、`逐项积分`、`基本积分公式表`
- **相互关系**：拆开的每一项都要能查到公式，否则说明拆法不对；常数系数可提到积分号外，最后统一加一个 $C$。
- **出处**：[石头 P44](https://www.bilibili.com/video/BV18CL26WEJ3?p=44)

### 常用恒等变形公式
- **要点**：常用变形工具包括平方差 $a^2-b^2=(a+b)(a-b)$、完全平方 $a^2\pm2ab+b^2=(a\pm b)^2$、立方和差 $a^3\pm b^3=(a\pm b)(a^2\mp ab+b^2)$、二倍角 $\cos2x=\cos^2x-\sin^2x=2\cos^2x-1=1-2\sin^2x$、$\sin2x=2\sin x\cos x$，以及 $\sin^2x+\cos^2x=1$。半角公式不必背，用二倍角公式把 $x$ 换成 $\frac{x}{2}$ 反解即可，如 $\sin^2\frac{x}{2}=\frac{1-\cos x}{2}$。
- **关键概念**：`平方差`、`完全平方`、`二倍角公式`、`$\sin^2x+\cos^2x=1$`、`半角公式由二倍角推出`
- **相互关系**：化 $\tan^2x$ 的积分要用第一章的六边形倒三角关系 $1+\tan^2x=\sec^2x$；$\frac{dx}{x^n}$ 这类题常把 $dx$ 写到分子上，先化成 $x\^\{-n\}$ 再用幂函数公式。
- **出处**：[石头 P44](https://www.bilibili.com/video/BV18CL26WEJ3?p=44)

### 二项式展开与杨辉三角
- **要点**：$(a+b)^2=a^2+2ab+b^2$，$(a+b)^3=a^3+3a^2b+3ab^2+b^3$，$(a+b)^4=a^4+4a^3b+6a^2b^2+4ab^3+b^4$，系数依次为 $121$、$1331$、$14641$。系数可由杨辉三角逐行相加得到（如 $1331$ 相邻两项相加得 $14641$），展开时 $a$ 的次数由高到低、$b$ 的次数由低到高。考试基本只考二次与三次。
- **关键概念**：`二项式展开`、`杨辉三角`、`系数 $1331$`、`系数 $14641$`
- **相互关系**：分子是 $(x\pm a)^n$、分母是幂函数时，先展开再逐项除以分母，即可化为可套公式的幂函数之和。
- **出处**：[石头 P44](https://www.bilibili.com/video/BV18CL26WEJ3?p=44)

### 有理分式拆项与三角变形
- **要点**：有理分式要先因式分解分母，再拆成两个简单分式之差（如 $\frac{1}{x^2-5x+6}=\frac{1}{x-3}-\frac{1}{x-2}$）：设 $\frac{A}{x-a}-\frac{B}{x-b}$ 后通分，令分子与原分子相等，比较 $x$ 的系数与常数项解出 $A$、$B$。三角型的被积函数则先用二倍角等恒等式化简，如 $\frac{\cos2x}{\cos^2x\sin^2x}=\frac{1}{\sin^2x}-\frac{1}{\cos^2x}$，再套公式。
- **关键概念**：`因式分解`、`拆项`、`比较系数`、`$\frac{1}{x-a}-\frac{1}{x-b}$`、`$\int\frac{1}{\cos^2x}dx=\tan x+C$`
- **相互关系**：若分子是常数而分母为 $1+x^2$ 型，可通过加减常数凑成 $\int k\,dx$ 与 $\int\frac{1}{1+x^2}dx$ 之和；拆项时必须朝「能直接查到公式」的方向拆，盲目拆开往往积不出来。
- **出处**：[石头 P44](https://www.bilibili.com/video/BV18CL26WEJ3?p=44)

### 凑微分的原理
- **要点**：被积函数能写成 $f(u)\cdot u'$ 的形式时，把 $u'\,dx$ 凑成 $du$，积分就化为 $\int f(u)du$，可直接套基本公式。如 $\int \sin^2x\cos x\,dx$ 中，$\sin^2x$ 是关于 $\sin x$ 的函数，$\cos x$ 是 $\sin x$ 的导数，把 $\cos x\,dx$ 凑成 $d\sin x$，即得 $\frac13\sin^3x+C$。
- **关键概念**：`第一类换元法`、`凑微分法`、`$f(u)\cdot u'$`、`$u'\,dx=du$`
- **相互关系**：关键在于识别哪一部分是复合函数、哪一部分是内层的导数；换元时被积函数与积分变量必须同时换，漏换一个等式就不成立；只有一部分题目能凑成功，凑不出时要换用第二类换元法。
- **出处**：[石头 P45](https://www.bilibili.com/video/BV18CL26WEJ3?p=45)

### 凑微分三字诀与常用凑微分公式
- **要点**：三字诀「拆、凑、套」：先拆成 $f(u)$ 与 $u'$ 两部分，再把 $u'\,dx$ 凑成 $du$，最后套基本积分公式。常用结论：$\int\frac{1}{ax+b}dx=\frac1a\ln|ax+b|+C$（$a\ne0$）；$\int\frac{1}{a^2+x^2}dx=\frac1a\arctan\frac xa+C$；$\int\frac{1}{x^2-a^2}dx=\frac{1}{2a}\ln\left|\frac{x-a}{x+a}\right|+C$；$\int\frac{1}{\sqrt{a^2-x^2}}dx=\arcsin\frac xa+C$；$\int\tan x\,dx=-\ln|\cos x|+C$；$\int\sec x\,dx=\ln|\sec x+\tan x|+C$。
- **关键概念**：`三字诀 拆凑套`、`$\int\frac{1}{ax+b}dx$`、`$\int\frac{1}{a^2+x^2}dx$`、`$\int\sec x\,dx$`
- **相互关系**：凑微分时允许在积分号外补一个常数系数（如分子分母同乘 $\frac12$ 再乘 $2$）以保证值不变；$\int\sec x\,dx$ 的技巧是分子分母同乘 $\sec x+\tan x$，凑出 $\frac{du}{u}$ 的形式。
- **出处**：[石头 P45](https://www.bilibili.com/video/BV18CL26WEJ3?p=45)

### 分母含一次式与二次式的凑微分
- **要点**：形如 $\int\frac{1}{ax+b}dx$ 的式子把分母整体设为 $u$，因 $u'=a$ 为常数，直接补系数凑成 $du$ 即可。形如 $\int\frac{1}{a^2+x^2}dx$ 的式子则不同，$u'=2x$ 配不出来，须先把分母除以 $a^2$ 写成 $1+(\frac xa)^2$ 的形式，再把 $dx$ 凑成 $d\frac xa$，化为 $\arctan$ 的标准型；平方差型 $\frac{1}{x^2-a^2}$ 则先因式分解再拆项。
- **关键概念**：`$\int\frac{1}{ax+b}dx=\frac1a\ln|ax+b|+C$`、`$1+(\frac xa)^2$`、`平方差因式分解`
- **相互关系**：一次式与二次式的处理方式有本质区别，一次式可直接设分母为 $u$，二次式必须先把常数项化为 $1$；差一个符号（加号与减号）结果就完全不同。
- **出处**：[石头 P45](https://www.bilibili.com/video/BV18CL26WEJ3?p=45)

### 分母复杂时先用换元化简
- **要点**：当分母复杂而分子可以展开时，可令分母整体为新变量（如令 $x+1=t$），反解出 $x=t-1$、$dx=dt$ 后代入，把原积分化为关于 $t$ 的简单积分；分子展开后逐项除以分母，再分别套公式，最后必须把 $t$ 换回 $x$。
- **关键概念**：`换元化简`、`$x+1=t$`、`$dx=dt$`、`变量回代`
- **相互关系**：这是第二类换元法的雏形；换元时必须把被积函数与积分变量一起换干净，回代时所有 $t$ 都要还原为 $x$。
- **出处**：[石头 P45](https://www.bilibili.com/video/BV18CL26WEJ3?p=45)

### 一型根式代换与五步法
- **要点**：被积函数含根号且根号内是一次式（形如 $\sqrt[n]{ax+b}$）时，令整个根式等于 $t$，五步求解：第一步令根式 $=t$；第二步由 $t$ 反解出 $x$；第三步把 $dx$ 换成关于 $t$ 的表达式；第四步解关于 $t$ 的积分（可用凑微分或直接积分法）；第五步把 $t$ 换回 $x$。开几次方不限，根号内必须是一次式。
- **关键概念**：`第二类换元法`、`根式代换`、`一型`、`五步法`、`$\sqrt[n]{ax+b}=t$`
- **相互关系**：与凑微分法相比，根式代换把根号整体消去，步骤固定、套路清晰；换元后若分母为二次、分子为一次，可再凑微分（如 $\int\frac{t}{t^2+1}dt=\frac12\ln|t^2+1|+C$）。
- **出处**：[石头 P46](https://www.bilibili.com/video/BV18CL26WEJ3?p=46)

### 二型根式代换与最小公倍数
- **要点**：被积函数含两个或以上根式（如 $\sqrt{x}$ 与 $\sqrt[4]{x}$、$\sqrt[3]{x}$ 与 $\sqrt{x}$），且各根号内为 $x$ 的幂时，令 $t=\sqrt[m]{x}$，其中 $m$ 为各根号开方次数的最小公倍数，反解出 $x=t^m$、$dx=mt\^\{m-1\}dt$ 后代入，可一次消去所有根号。若换元后仍不易积，可对分母再次换元（如令 $t+1=u$）。
- **关键概念**：`二型根式代换`、`$t=\sqrt[m]{x}$`、`最小公倍数`、`二次换元`
- **相互关系**：一型与二型步骤完全相同，区别只在 $t$ 的设法；最小公倍数取公倍数中最小的一个（如 $2$ 与 $3$ 取 $6$，$2$ 与 $4$ 取 $4$）。变量回代时若根号开偶次方，结果为非负，可省去绝对值。
- **出处**：[石头 P46](https://www.bilibili.com/video/BV18CL26WEJ3?p=46)

### 三角代换的三种类型
- **要点**：被积函数含 $\sqrt{a^2-x^2}$ 时令 $x=a\sin t$（弦代换），含 $\sqrt{a^2+x^2}$ 时令 $x=a\tan t$（切代换），含 $\sqrt{x^2-a^2}$ 时令 $x=a\sec t$（割代换）。三类代换都靠倒三角关系把根号整体去掉：$\sqrt{a^2-x^2}=a\cos t$、$\sqrt{a^2+x^2}=a\sec t$、$\sqrt{x^2-a^2}=a\tan t$。
- **关键概念**：`弦代换`、`切代换`、`割代换`、`$\sqrt{a^2-x^2}\Rightarrow x=a\sin t$`、`$\sqrt{a^2+x^2}\Rightarrow x=a\tan t$`、`$\sqrt{x^2-a^2}\Rightarrow x=a\sec t$`
- **相互关系**：与根式代换的区别在于根号下是 $x$ 的二次式而非一次式；直接令整体等于 $t$ 再反解 $x$ 会出现正负号，故必须改用三角代换。本考点考评最低，但见到这三类根式仍应优先尝试。
- **出处**：[石头 P47](https://www.bilibili.com/video/BV18CL26WEJ3?p=47)

### 三角代换的回代：直角三角形法
- **要点**：代换后得到的是关于 $t$ 的表达式，必须回代成 $x$。由 $\sin t=\frac xa$、$\tan t=\frac xa$、$\sec t=\frac xa$ 画一个直角三角形，用勾股定理求出第三边，再读出 $\cos t$、$\sec t$、$\tan t$ 的比值代回。第三边其实就是原题中的那个根式，可直接抄过来。
- **关键概念**：`回代`、`直角三角形`、`勾股定理`、`$\sin t=\frac xa$`
- **相互关系**：回代是三角代换的第三个难点，与「换元要换干净」的要求一致；专升本可不讨论 $t$ 的取值范围，直接开方取正并假定反三角函数存在。
- **出处**：[石头 P47](https://www.bilibili.com/video/BV18CL26WEJ3?p=47)

### 代换后的三角积分处理
- **要点**：三角代换后常出现 $\int\cos^2t\,dt$ 这类积分，先用降次公式 $\cos^2t=\frac{1+\cos2t}{2}$ 降次升角，再拆成 $\frac14\int\cos2t\,d(2t)$ 与 $\frac12\int dt$ 分别积分。若结果中含 $\sin2t$，再用 $\sin2t=2\sin t\cos t$ 拆成 $\sin t$、$\cos t$ 分别回代。
- **关键概念**：`降次公式`、`$\cos^2t=\frac{1+\cos2t}{2}$`、`$\sin2t=2\sin t\cos t$`、`凑微分`
- **相互关系**：降次与回代分别对应三角代换的第二、第三个难点；$\int\sec t\,dt=\ln|\sec t+\tan t|+C$ 也是本类题必须记住的结果。
- **出处**：[石头 P47](https://www.bilibili.com/video/BV18CL26WEJ3?p=47)

### 分部积分公式
- **要点**：由乘积求导法则 $(uv)'=u'v+uv'$ 两边同时取不定积分，得 $\int uv'\,dx=uv-\int u'v\,dx$，写成微分形式即 $\int u\,dv=uv-\int v\,du$。它的作用是把难积的 $\int u\,dv$ 换成好积的 $\int v\,du$，其中 $uv$ 这一项已经直接积出。
- **关键概念**：`$\int u\,dv=uv-\int v\,du$`、`分部分积分`、`$v$ 取 $v'$ 的不带常数原函数`
- **相互关系**：公式源于第二章的乘积求导法则，是定积分分部积分法的依据；「分部」指把被积表达式分成 $u$ 与 $dv$ 两部分再对调，不是「分步骤积分」。
- **出处**：[石头 P48](https://www.bilibili.com/video/BV18CL26WEJ3?p=48)

### 选 $u$ 的顺序：反对幂指三
- **要点**：按「反三角函数、对数函数、幂函数、指数函数、三角函数」的先后顺序选 $u$，排在前面的优先充当 $u$，剩下的连同 $dx$ 作为 $dv$。指数函数与三角函数之间可颠倒顺序，前三者不能颠倒。被积函数只有一个因子时，把它当作 $u$、把隐藏的 $1$ 当作 $v'$（即用 $dx$ 当 $dv$）。
- **关键概念**：`反对幂指三`、`选 $u$ 的优先权`、`隐藏的因子 $1$`
- **相互关系**：选错 $u$ 会让式子越积越复杂甚至积不出来，是分部积分成败的关键；$x\sin x$ 中幂函数在前，故取 $u=x$，$\ln x$ 型则取 $u=\ln x$。
- **出处**：[石头 P48](https://www.bilibili.com/video/BV18CL26WEJ3?p=48)

### 幂函数型分部积分：逐次降幂
- **要点**：幂函数乘指数函数或三角函数时，每分部一次就把幂函数的次数降低一次。$\int x^2e^xdx$ 第一次分部得 $x^2e^x-2\int xe^xdx$，第二次用 $\int xe^xdx=xe^x-e^x$，最后提取公因式得 $e^x(x^2-2x+2)+C$。$x$ 的三次方需三步，考试最多考到二次。
- **关键概念**：`逐次降幂`、`$\int xe^xdx=xe^x-e^x+C$`、`提取公因式`
- **相互关系**：$x\sin x$、$x\ln x$、$\arcsin x$ 等题都走同一套路；$\int\arcsin x\,dx$ 分部后剩下的 $\int\frac{x}{\sqrt{1-x^2}}dx$ 用凑微分 $x\,dx=\frac12d(x^2)$ 处理，不必动用三角代换。$\int e\^\{\sqrt x\}dx$ 先用根式代换令 $\sqrt x=t$ 化为 $2\int te^t\,dt$，再按幂函数型分部积分，体现两种方法的衔接。
- **出处**：[石头 P48](https://www.bilibili.com/video/BV18CL26WEJ3?p=48)

### 指数×三角函数型：循环后解方程
- **要点**：求 $\int e^x\sin x\,dx$ 时连续分部两次，第二次会重新出现与原式完全相同的不定积分，此时把该积分移项到等号左边，得「二倍的它」等于已算出的部分，两边除以二即得结果 $\frac{e^x}{2}(\sin x-\cos x)+C$。把式子列成方程而不是继续硬积，是这类题的唯一出路。
- **关键概念**：`循环积分`、`移项解方程`、`$\int e^x\sin x\,dx=\frac{e^x}{2}(\sin x-\cos x)+C$`
- **相互关系**：与幂函数型不同，这类题不会越积越简单而是回到原式；等号右边仍带积分号时不加 $C$，化为有限表达式后才补 $C$。
- **出处**：[石头 P48](https://www.bilibili.com/video/BV18CL26WEJ3?p=48)


## 五、定积分及其应用


### 定积分的定义与黎曼和
- **要点**：把 [a,b] 分成 n 个小区间，各区间任取 ξ_i，作和 Σf(ξ_i)Δx_i；令最大区间长度 λ→0 取极限，即得曲边梯形面积。该极限称为黎曼和极限（积分和），记作 ∫_a^b f(x)dx，体现「分割 — 近似 — 求和 — 取极限」的微元法思想。∫_a^b f(x)dx 是求曲边梯形面积的工具：每一小条近似为底 dx、高 f(x) 的小矩形，面积 f(x)dx。
- **关键概念**：`黎曼和`、`λ→0`、`微元法`、`曲边梯形`、`积分和`、`积分上限`、`积分下限`、`积分区间`
- **相互关系**：定积分本质是一个确定的数（与积分变量字母无关），对其求导结果为零；不定积分是含 C 的函数族——这是判断「定积分是不是 f(x) 的原函数」类概念题的依据。
- **出处**：[陈哥 P70](https://www.bilibili.com/video/BV1husGzwEtZ?p=70)；[杰哥 P65](https://www.bilibili.com/video/BV1Up4y1Y76a?p=65)、[P68](https://www.bilibili.com/video/BV1Up4y1Y76a?p=68)；[ok姐 P54](https://www.bilibili.com/video/BV1vm421s7mv?p=54)

### 定积分与不定积分的区别
- **要点**：积分号上下限未限定数值的是不定积分，限定为常数 a、b 的是定积分；定积分多出下限 a（区间左端点）与上限 b（区间右端点），f(x) 仍为被积函数，x 仍为积分变量。定积分的结果是一个确定的数值，只与被积函数和积分区间有关，与积分变量所用字母无关。
- **关键概念**：`定积分`、`不定积分`、`积分上下限`、`积分变量`
- **出处**：[陈哥 P70](https://www.bilibili.com/video/BV1husGzwEtZ?p=70)；[杰哥 P68](https://www.bilibili.com/video/BV1Up4y1Y76a?p=68)；[学士帽 P62](https://www.bilibili.com/video/BV1X4411J792?p=62)

### 定积分的几何意义：面积的代数和
- **要点**：f(x)≥0 时定积分等于曲线 y=f(x)、直线 x=a、x=b 与 x 轴围成的曲边梯形面积（正值）；f(x)≤0 时该面积取负值；f(x) 有正有负时，等于 x 轴上方面积减去下方面积（面积的代数和）。面积恒大于零，曲线在 x 轴下方时须加负号才等于面积。写法是变化量在 x 轴就写 dx，x 的范围由小到大作上下限。学士帽补充：曲线是谁被积函数就是谁；曲线全在 x 轴上方时面积 S=∫_a^b f(x)dx，曲线在 x 轴下方时 S=−∫_a^b f(x)dx（定积分可正可负，面积恒大于零）。
- **关键概念**：`曲边梯形`、`有向面积`、`代数和`、`上方为正、下方为负`
- **相互关系**：是理解全部定积分性质的出发点，也是偶倍奇零成立的原因；遇到独立的 √(a²−x²) 要联想到半圆（y=√(9−x²) 是半径 3 的上半圆），但根式在分母中时不表示圆。
- **出处**：[陈哥 P70](https://www.bilibili.com/video/BV1husGzwEtZ?p=70)；[杰哥 P66](https://www.bilibili.com/video/BV1Up4y1Y76a?p=66)；[学士帽 P62](https://www.bilibili.com/video/BV1X4411J792?p=62)、[P63](https://www.bilibili.com/video/BV1X4411J792?p=63)；[ok姐 P55](https://www.bilibili.com/video/BV1vm421s7mv?p=55)

### 用几何意义求定积分（圆型被积函数）
- **要点**：被积函数含 √(a²−x²) 时平方变形为 x²+y²=a²，判定是半径 a 的圆；根号恒非负取上半圆，再由 x 的范围确定取哪一段，用圆面积公式得结果。∫_0^a √(a²−x²)dx=πa²/4（1/4 圆面积），∫\_\{−a\}\^\{a\}√(a²−x²)dx=πa²/2（1/2 圆面积）。形如 √(2ax−x²) 时先配方成 (x−a)²+y²=a²，半径即 a；∫_0^a 对应 1/4 圆、∫_0\^\{2a\} 对应 1/2 圆。见根号下二次式优先用几何意义，不必硬算。
- **关键概念**：`√(a²−x²)`、`x²+y²=a²`、`上半圆`、`1/4圆面积`、`1/2圆面积`、`配完全平方`
- **相互关系**：与有理函数中「分母配完全平方」同源；常与对称区间上的奇偶性同考。
- **出处**：[陈哥 P70](https://www.bilibili.com/video/BV1husGzwEtZ?p=70)；[杰哥 P73](https://www.bilibili.com/video/BV1Up4y1Y76a?p=73)；[米哥 P74](https://www.bilibili.com/video/BV1swAWerEzS?p=74)；[学士帽 P62](https://www.bilibili.com/video/BV1X4411J792?p=62)

### 定积分是常数，求导为零
- **要点**：d/dx ∫_a^b f(x)dx=0，定积分算完是确定数值；与不定积分 d/dx ∫f(x)dx=f(x) 不同。若被积函数表达式里含自身定积分（如 f(x)=g(x)−∫_0^1 f(x)dx），可把该定积分设为字母 a，代回原式后两边同取相同区间的定积分，解方程求出 a 再写出 f(x)。
- **关键概念**：`定积分为常数`、`求导为零`、`待定字母`、`两边同取定积分`
- **相互关系**：前提是分清定积分（数）与不定积分（函数）；若式中还含极限，极限值也是数，可另设常数，最后解二元一次方程组。
- **出处**：[陈哥 P75](https://www.bilibili.com/video/BV1husGzwEtZ?p=75)；[杰哥 P73](https://www.bilibili.com/video/BV1Up4y1Y76a?p=73)；[学士帽 P63](https://www.bilibili.com/video/BV1X4411J792?p=63)

### 定积分的基本运算性质（线性、可加性与换限）
- **要点**：①∫_a^a f dx=0（上下限相同）；②∫_a^b f=−∫_b^a f（交换上下限加负号）；③∫_a^b f=∫_a^c f+∫_c^b f（区间可加性，是分段函数与绝对值函数积分拆区间的依据）；④∫_a^b 1 dx=b−a，推广 ∫_a^b c dx=c(b−a)；⑤线性性质，常数因子可提出、可逐项积分。
- **关键概念**：`上下限相同为零`、`交换上下限变号`、`可加性`、`线性性质`、`上限减下限`、`矩形面积`
- **相互关系**：后续定积分各种计算方法都要用到，需记得非常熟练；被积表达式相同时，只要两个定积分有一个公共的上下限就能合并。
- **出处**：[陈哥 P70](https://www.bilibili.com/video/BV1husGzwEtZ?p=70)；[杰哥 P68](https://www.bilibili.com/video/BV1Up4y1Y76a?p=68)；[学士帽 P63](https://www.bilibili.com/video/BV1X4411J792?p=63)；[ok姐 P56](https://www.bilibili.com/video/BV1vm421s7mv?p=56)、[P57](https://www.bilibili.com/video/BV1vm421s7mv?p=57)、[P58](https://www.bilibili.com/video/BV1vm421s7mv?p=58)、[P60](https://www.bilibili.com/video/BV1vm421s7mv?p=60)；[米哥 P71](https://www.bilibili.com/video/BV1swAWerEzS?p=71)

### 定积分的保序性与比较大小
- **要点**：保序性：积分区间上 f(x)≥0 则 ∫_a^b f(x)dx≥0，不等号方向不变。推论一（比较大小）：同一区间上若 f(x)≤g(x) 时 ∫_a^b f(x)dx≤∫_a^b g(x)dx，故比较两个定积分转化为比较被积函数的大小；推论二：|∫_a^b f(x)dx|≤∫_a^b|f(x)|dx。熟悉的函数画图比较；不熟悉的可借助单调性（只比较自变量大小）或在区间内取特殊值比较。上下限相同时只比被积函数大小，可借图像或找锚点（如以 e、1 为界判断 ln x 与 ln²x）。
- **关键概念**：`保号性`、`比较大小`、`被积函数大小`、`绝对值不等式`、`特殊值`
- **相互关系**：24 年考过用保号性比较三个定积分大小的选择题。
- **出处**：[陈哥 P70](https://www.bilibili.com/video/BV1husGzwEtZ?p=70)；[杰哥 P67](https://www.bilibili.com/video/BV1Up4y1Y76a?p=67)；[米哥 P72](https://www.bilibili.com/video/BV1swAWerEzS?p=72)；[ok姐 P59](https://www.bilibili.com/video/BV1vm421s7mv?p=59)

### 估值定理与积分中值定理
- **要点**：估值定理：设 M、m 为 f(x) 在 [a,b] 上的最大值与最小值，则 m(b−a)≤∫_a^b f(x)dx≤M(b−a)。积分中值定理：f(x) 在 [a,b] 上连续时存在 ξ 使 ∫_a^b f(x)dx=f(ξ)(b−a)，即总存在一个与该曲边梯形等面积的矩形。两者由几何意义理解即可，升本基本不考。
- **关键概念**：`估值定理`、`积分中值定理`、`等面积矩形`
- **出处**：[陈哥 P70](https://www.bilibili.com/video/BV1husGzwEtZ?p=70)；[米哥 P71](https://www.bilibili.com/video/BV1swAWerEzS?p=71)；[ok姐 P60](https://www.bilibili.com/video/BV1vm421s7mv?p=60)

### 对称区间上的奇偶性简化
- **要点**：区间关于原点对称（如 [−a,a]）时，判断被积函数的奇偶性：奇函数则积分值为 0，偶函数则等于 2∫_0^a f(x)dx。看到上下限互为相反数就应想到此考点。若被积函数是多项加减，奇偶性不能整体判断，需先用可加性拆项后逐项判断。
- **关键概念**：`关于原点对称的区间`、`奇函数`、`偶函数`、`2∫_0^a f dx`
- **相互关系**：依赖奇偶性的定义；偶函数套偶函数仍为偶函数，奇偶相乘除为奇函数；是理解对称区间上奇函数积分为零的铺垫。
- **出处**：[学士帽 P63](https://www.bilibili.com/video/BV1X4411J792?p=63)、[P64](https://www.bilibili.com/video/BV1X4411J792?p=64)

### 牛顿-莱布尼茨公式
- **要点**：∫_a^b f(x)dx=F(x)|_a^b=F(b)−F(a)，F(x) 为 f(x) 的任一原函数；先按不定积分求原函数（不加 C），再杠上上下限，上限代入减下限代入。综合题先看区间是否对称：奇函数项直接为零，偶函数项写成 2∫_0^a 后再套公式。易错点：下限那一坨（尤其含多项或负号时）必须加括号；原函数中的常数因子（如 ∫3x²dx 的 3）不能漏乘。学士帽指出 F(b)、F(a) 均为数值，故定积分结果必为数值。
- **关键概念**：`牛顿-莱布尼茨公式`、`原函数`、`不带常数 C`、`上限函数值`、`下限函数值`
- **相互关系**：求定积分就是求不定积分（不加 C）再代上下限，C 在作差时抵消；求面积题要先由几何意义判断被积函数在该区间上的正负。
- **出处**：[陈哥 P72](https://www.bilibili.com/video/BV1husGzwEtZ?p=72)；[杰哥 P69](https://www.bilibili.com/video/BV1Up4y1Y76a?p=69)；[米哥 P71](https://www.bilibili.com/video/BV1swAWerEzS?p=71)、[P72](https://www.bilibili.com/video/BV1swAWerEzS?p=72)；[学士帽 P64](https://www.bilibili.com/video/BV1X4411J792?p=64)、[P69](https://www.bilibili.com/video/BV1X4411J792?p=69)；[ok姐 P61](https://www.bilibili.com/video/BV1vm421s7mv?p=61)；[帆哥 P1](https://www.bilibili.com/video/BV1xxXZBKENv?p=1)

### 莱布尼兹公式为什么成立
- **要点**：把 [a,b] 分割成 n 个小区间，每个小区间上取微分 dy=f′(x)dx，λ→0 时 Δy 与 dy 等价；各小区间的 Δy_i 是相邻两点函数值之差，全部相加恰好等于 f(x_n)−f(x_1)；另一方面 Σf′(x_i)Δx_i 的极限正是 ∫_a^b f′(x)dx，于是 ∫_a^b f′(x)dx=f(b)−f(a)。
- **关键概念**：`微分`、`高阶无穷小`、`积分和`、`原函数`
- **相互关系**：说明微分与积分互为逆运算，考试不考。
- **出处**：[ok姐 P62](https://www.bilibili.com/video/BV1vm421s7mv?p=62)

### 基本公式法
- **要点**：先按不定积分基本公式求原函数，再代入上下限作差；1/x 的原函数为 ln|x|、sin x 的原函数为 −cos x；结果要化到最简，如 ln4−ln2=ln2。学士帽提醒代入时要准确使用特殊角的函数值，并用 ln a^n=n ln a 把结果化到最简。
- **关键概念**：`基本公式`、`ln|x|`、`−cos x`
- **出处**：[学士帽 P69](https://www.bilibili.com/video/BV1X4411J792?p=69)

### 定积分的凑微分法
- **要点**：与不定积分凑微分完全相同，只是最后多一步代入上下限；关键是识别「某部分恰是另一部分的原函数」并放到微分号后，常见搭配 (1/(2√x))dx=d√x、x dx=½d(x²)、(1/x)dx=d ln x。学士帽补充：低次幂乘高次幂时把低次幂凑进去，凑完把整体圈起来当新变量套基本公式。
- **关键概念**：`凑微分`、`d√x`、`d ln x`
- **出处**：[学士帽 P69](https://www.bilibili.com/video/BV1X4411J792?p=69)；[ok姐 P64](https://www.bilibili.com/video/BV1vm421s7mv?p=64)

### 定积分的换元法
- **要点**：换元过程与不定积分一致，关键区别是换元必须同时换积分上下限（「换元必换线」）：由 x=φ(t)，下限 x=a 对应 t=α、上限 x=b 对应 t=β，积分变为 ∫_α^β f(φ(t))φ′(t)dt；算完不必还原回 x（定积分结果不加 C，而是原函数在上下限处的函数值之差）。两类：无理根式整体代换（令根号等于 t）、三角代换（含 √(1−x²) 令 x=sin t，角取最小正周期内的值）。三角代换后区间常变成 [0,π/2]，衔接点火公式。不换限是最常见错误。
- **关键概念**：`整体换元`、`换元必换线`、`上下限对应`、`三角代换`
- **相互关系**：根式换元后通常化为有理函数积分；换元后若出现分子分母变量次数相同的分式，在分子上加一项再减同一项，拆成 1−1/(t+1) 再逐项积分。
- **出处**：[陈哥 P72](https://www.bilibili.com/video/BV1husGzwEtZ?p=72)；[杰哥 P74](https://www.bilibili.com/video/BV1Up4y1Y76a?p=74)；[米哥 P73](https://www.bilibili.com/video/BV1swAWerEzS?p=73)；[学士帽 P71](https://www.bilibili.com/video/BV1X4411J792?p=71)；[ok姐 P64](https://www.bilibili.com/video/BV1vm421s7mv?p=64)；[帆哥 P1](https://www.bilibili.com/video/BV1xxXZBKENv?p=1)

### 分段函数与含绝对值的定积分
- **要点**：分段函数的积分一定考分段点，必须从分段点处把区间拆开，判断每段取哪个表达式再逐段积分相加；含绝对值时先求绝对值内表达式的零点，用零点拆区间并逐段判号——大于零直接去绝对值、小于零取相反数；√(cos²x) 这类开方结果应写成 |cos x| 再按此流程处理。
- **关键概念**：`分段点`、`零点拆分`、`√(u²)=|u|`
- **相互关系**：若被积函数写成 f(1−x) 这类与题干给的 f(x) 字母不一致的形式，需先换元统一字母（令 1−x=t）；注意前后两个 x 只是名字相同、并非同一变量，取值范围不能混用；换元后上下限倒置时用 ∫_a^b=−∫_b^a 添负号调换。学士帽指出两者同属一类，依据都是定积分的可加性。
- **出处**：[陈哥 P72](https://www.bilibili.com/video/BV1husGzwEtZ?p=72)；[杰哥 P75](https://www.bilibili.com/video/BV1Up4y1Y76a?p=75)；[米哥 P78](https://www.bilibili.com/video/BV1swAWerEzS?p=78)；[学士帽 P71](https://www.bilibili.com/video/BV1X4411J792?p=71)

### 定积分的分部积分法
- **要点**：公式 ∫_a^b u dv=[uv]_a^b−∫_a^b v du，与不定积分相同，区别是每处带上上下限：已算出的 uv 须立刻写成带上下限的 [uv]_a^b，结果不加 C。拆 u、凑 dv 的套路不变（u 按「反对幂指三」优先），最后用牛顿-莱布尼兹公式代入上下限求值。
- **关键概念**：`分部积分公式`、`[uv]_a^b`、`牛顿-莱布尼兹公式`、`u 的选取顺序`
- **相互关系**：去掉上下限即退化为不定积分的分部积分公式；由 dv 求 v 时不加常数。
- **出处**：[陈哥 P72](https://www.bilibili.com/video/BV1husGzwEtZ?p=72)；[杰哥 P69](https://www.bilibili.com/video/BV1Up4y1Y76a?p=69)；[米哥 P73](https://www.bilibili.com/video/BV1swAWerEzS?p=73)；[ok姐 P66](https://www.bilibili.com/video/BV1vm421s7mv?p=66)；[石头 P52](https://www.bilibili.com/video/BV18CL26WEJ3?p=52)

### 定积分综合计算的题型套路
- **要点**：含复合函数又无法凑微分时，先对复合部分换元再分部积分（先换元再分部）；多项式与三角函数、指数函数之积用分部积分；含绝对值时按 x 的取值范围去绝对值；分段函数在积分区间跨分段点时，用积分区域可加性按分段点拆开。定积分换元必须「换元又换线」，用旧变量上下限代入换元式求出新变量上下限；凑微分时补的常数系数与负号属于整个积分，对其使用分部积分时必须加括号带上。
- **关键概念**：`先换元再分部`、`去绝对值`、`积分区域可加性`、`换线`
- **相互关系**：拆分后常出现对称区间积分，可结合奇偶性推论直接得 0，简化计算；考察面广。
- **出处**：[陈哥 P72](https://www.bilibili.com/video/BV1husGzwEtZ?p=72)；[ok姐 P64](https://www.bilibili.com/video/BV1vm421s7mv?p=64)、[P65](https://www.bilibili.com/video/BV1vm421s7mv?p=65)、[P66](https://www.bilibili.com/video/BV1vm421s7mv?p=66)

### 定积分的分部积分法与「三指幂对反」优先顺序
- **要点**：被积函数出现两种不同类型的函数相乘时用分部积分，公式仍是 ∫u dv=uv−∫v du。选谁放到 d 的后面（充当 v）按「三指幂对反」由高到低——三角函数、指数函数、幂函数、对数函数、反三角函数，优先级高的先放到 d 后，放过去时要变成它的原函数。放过去后若与 d 后的变量不一致，须先让 d 后乘一个数、积分号前也乘同一个数把变量凑齐（如把 −x 圈成整体后可直接放到 d 后）。定积分中已经积完的部分要立刻杠上上下限——只要没有积分号就要杠，再减去 ∫v du；整个式子符号较多，要一步一步做、做一步保证一步正确。剩下的积分常需再凑一次微分（e\^\{−x\}、cos2x、sin2x 都要把 d 后的变量凑成一致），并注意「负负得正」的符号处理；单独的对数函数直接充当 u（如 ∫ln x dx，d ln x=(1/x)dx 与前面的 x 约掉后被积函数只剩 1）。
- **关键概念**：`分部积分法`、`三指幂对反`、`凑成与 d 后相同的变量`、`杠上下限`、`再凑一次微分`、`单独的对数函数充当 u`
- **相互关系**：与不定积分分部积分是同一个公式，只多了代入上下限一步；与凑微分法共用「把函数变成原函数放到 d 后」的操作。
- **出处**：[学士帽 P70](https://www.bilibili.com/video/BV1X4411J792?p=70)

### 华里士（点火）公式
- **要点**：∫_0\^\{π/2\} sin^n x dx=∫_0\^\{π/2\} cos^n x dx：n 奇从 n 逐次减 2 连乘到 1（即连乘到 2/3 后乘 1），n 偶同样连乘到 1 再乘 π/2（连乘到 1/2 再乘 π/2）。「点火」指最后那个 π/2——有 1/2 才能点火，奇数次的点不着火。推广：∫_0^π sin^n x dx=2∫_0\^\{π/2\} sin^n x dx，∫_0^π cos^n x dx 奇为 0、偶为二倍。仅限 [0,π/2]，换元后区间若变成 [0,π/2] 即可套用。
- **关键概念**：`点火公式`、`华里士公式`、`奇偶分支`、`拆半翻倍`
- **相互关系**：依据是 sin 在 [0,π] 上关于 π/2 对称，左右两半面积相等，可拆半后翻倍；部分院校会考。
- **出处**：[杰哥 P72](https://www.bilibili.com/video/BV1Up4y1Y76a?p=72)、[P74](https://www.bilibili.com/video/BV1Up4y1Y76a?p=74)；[米哥 P77](https://www.bilibili.com/video/BV1swAWerEzS?p=77)

### 变上限积分的定义与基本求导
- **要点**：上限换成变量、下限为常数即为变上限积分 ∫_a^x f(t)dt（积分变量改用 t 以与 x 区分）；它是 f(x) 的一个原函数，求导时把上限代入被积函数替换 t、去掉积分号与 dt，得 d/dx ∫_a^x f(t)dt=f(x)。∫_x^b f(t)dt 是 −f(x) 的原函数。变下限积分 ∫_x^b f(t)dt=−∫_b^x f(t)dt；上下限都变时插入一个分点，用积分区域可加性拆成两个变限积分之和。闭区间上连续的函数一定可积。学士帽给出推广形式：上限为 φ(x) 时 d/dx ∫_a\^\{φ(x)\} f(t)dt=f(φ(x))·φ′(x)，即代入上限后再乘以上限的导数（漏乘 φ′(x) 是典型错误）；上下限均为变量 φ(x)、ω(x) 时结果为 f(φ(x))φ′(x)−f(ω(x))ω′(x)；变下限（上限为常数）时先用换限变号把负号提到积分号外，化为变上限处理，考频较低。
- **关键概念**：`变上限积分`、`∫_a^x f(t)dt`、`上限代入`、`原函数`、`可积`
- **相互关系**：与「定积分是常数、求导为零」形成对比，是概念判断题的陷阱；被积函数中的积分变量是谁就替换谁（∫_0^t f(x)dx 的积分变量是 x，用上限 t 替换 x）；变下限的复合积分先加负号化成变上限形式，负号当常数因子照抄，不要漏。
- **出处**：[杰哥 P68](https://www.bilibili.com/video/BV1Up4y1Y76a?p=68)；[学士帽 P68](https://www.bilibili.com/video/BV1X4411J792?p=68)；[ok姐 P63](https://www.bilibili.com/video/BV1vm421s7mv?p=63)

### 变限积分与洛必达法则结合求极限
- **要点**：极限式中含变上限积分且为 0/0 型时用洛必达法则上下同时求导，分子按变上限积分求导法则处理；求极限仍按带点、化简、等价代换、洛必达四步走。
- **关键概念**：`洛必达法则`、`零比零型`、`上下同时求导`
- **出处**：[学士帽 P68](https://www.bilibili.com/video/BV1X4411J792?p=68)；[米哥 P75](https://www.bilibili.com/video/BV1swAWerEzS?p=75)

### 积分方程的常数代换法
- **要点**：方程中含未知函数的定积分时，因定积分是一个确定的数，可设为常数 A 代入原式；再在给定区间上两边同时积分，左边同一积分换成 A，解一元一次方程得 A 后回代。
- **关键概念**：`定积分是一个数`、`设为常数 A`、`两边积分`
- **相互关系**：前提是分清定积分（数）与不定积分（函数）。
- **出处**：[陈哥 P75](https://www.bilibili.com/video/BV1husGzwEtZ?p=75)

### 由变限积分方程求函数表达式
- **要点**：含 (1/x)∫_1^x f(t)dt 一类形式时先两边同乘 x 再求导，消去含 f 的项后得 f′(x)，两边积分（先导后积加 C）；常数 C 由原式中令上下限相等（积分为零）所得特值确定。若所求本身是定积分，则先凑微分再用分部积分，边界项按变限积分求导化简。
- **关键概念**：`两边同乘 x`、`先导后积加 C`、`初始条件`、`分部积分`
- **相互关系**：与微分方程题型相通，考试多考大题。
- **出处**：[陈哥 P76](https://www.bilibili.com/video/BV1husGzwEtZ?p=76)

### 变限积分的综合题型
- **要点**：常见考法是求含变限积分的 0/0 型极限（洛必达法则 + 等价无穷小），或由「曲边梯形面积 = 关于 t 的表达式」等条件建立含变限积分的等式，两边求导化为微分方程再解出函数。
- **关键概念**：`洛必达法则`、`等价无穷小`、`微分方程`
- **相互关系**：变限积分常与极限、微分方程、单调性与极值判断结合，多出现在综合题中。
- **出处**：[ok姐 P63](https://www.bilibili.com/video/BV1vm421s7mv?p=63)

### 积分区间在线公式
- **要点**：∫_a^b f(x)dx=∫_a^b f(a+b−x)dx，用法是把自变量 x 换成「上限加下限减 x」，区间不变、其余不动。适用于待证等式两侧积分区间相同的证明题；本质是换元 a+b−x=t。证明：令 a+b−x=t，则 dx=−dt；x=a 时 t=b、x=b 时 t=a，得 ∫_b^a f(t)(−dt)；再用上下限调换添负号把区间倒回 [a,b]，积分变量改名不影响结果，即得证。
- **关键概念**：`区间在线公式`、`上限加下限减 x`、`换元换线`、`上下限调换`
- **出处**：[杰哥 P76](https://www.bilibili.com/video/BV1Up4y1Y76a?p=76)

### 与诱导公式的配合
- **要点**：区间在线把自变量变成 π/2−x、π−x 等形式后，用「奇变偶不变，符号看象限」化简：π/2 的奇数倍则函数名改变（sin↔cos），偶数倍不变；正负号由原角所在象限决定。也用于证 sin 型与 cos 型积分相等。
- **关键概念**：`奇变偶不变`、`符号看象限`
- **出处**：[杰哥 P77](https://www.bilibili.com/video/BV1Up4y1Y76a?p=77)、[P78](https://www.bilibili.com/video/BV1Up4y1Y76a?p=78)

### 证明定积分形式函数的奇偶性
- **要点**：形如 F(x)=∫_a^b g(x,t)dt 的含参积分无法直接算出时，用定义证：写出 F(−x)，对积分变量 t 使用区间在线公式代换，凑出与 F(x) 相同的形式即证得偶函数。易错：把含参的 x 误当积分变量去换。
- **关键概念**：`偶函数定义`、`积分变量是 t 不是 x`
- **出处**：[杰哥 P79](https://www.bilibili.com/video/BV1Up4y1Y76a?p=79)

### 含变限积分的等式证明
- **要点**：证明 ∫_0^x f(x−t)dt=∫_0^x f(t)dt 一类等式时，直接对变限积分求导往往无法推进；此时对复合的被积函数换元（令 u=x−t，dt=−du），换元时上下限同步变换（t=0⇒u=x，t=x⇒u=0），再用负号颠倒上下限即可得证。
- **关键概念**：`换元法`、`积分上下限变换`、`积分变量字母无关性`
- **相互关系**：这是「遇到变限积分先考虑求导」原则失效时的替代思路。
- **出处**：[ok姐 P81](https://www.bilibili.com/video/BV1vm421s7mv?p=81)

### 无穷区间反常积分
- **要点**：把积分区间破坏为无穷（上限 +∞、下限 −∞ 或两者兼有）即为无穷区间反常积分，又称广义积分。求法是把无穷限换成 T 得变上限积分，再求 T→∞ 的极限：代入后极限存在（有限数）则收敛且极限值即积分值，为无穷或不存在则发散。牛顿-莱布尼兹公式代入无穷时必须写成极限形式，不能直接写 e\^\{+∞\}。∫\_\{−∞\}\^\{+∞\} 需拆为两段，两段必须同时收敛才收敛，有一段发散则整体发散。
- **关键概念**：`无穷区间反常积分`、`广义积分`、`写成极限形式`、`收敛`、`发散`、`拆分后同时收敛`
- **相互关系**：本质是「积分 + 极限」的组合；选择、填空题常只问敛散性；求解时先求原函数再取极限，而不是先求导。
- **出处**：[陈哥 P77](https://www.bilibili.com/video/BV1husGzwEtZ?p=77)、[P78](https://www.bilibili.com/video/BV1husGzwEtZ?p=78)；[米哥 P79](https://www.bilibili.com/video/BV1swAWerEzS?p=79)；[ok姐 P67](https://www.bilibili.com/video/BV1vm421s7mv?p=67)；[帆哥 P1](https://www.bilibili.com/video/BV1xxXZBKENv?p=1)

### ∫_a\^\{+∞\} 1/x^p dx 的敛散性
- **要点**：a>0 时，p>1 收敛，p≤1 发散。如 ∫_1\^\{+∞\} 1/√x dx 中 p=1/2&lt;1，发散。
- **关键概念**：`p 积分`、`敛散性判定`
- **相互关系**：先把 1/x^p 化为 x\^\{−p\} 的幂形式再求原函数。
- **出处**：[ok姐 P67](https://www.bilibili.com/video/BV1vm421s7mv?p=67)

### 反常积分的常用计算技巧与结论
- **要点**：1/(1+x²) 型凑 arctan；有限区间上 ∫√(1−x²)dx 用四分之一圆面积；分式对分子加一减一；分母配完全平方凑 arctan；含根号用根式代换；三角代换令 x=tan t 时 t 只能取到 π/2；cos²t 型用点火（华里士）公式。结论 ∫_0\^\{+∞\}x^n e\^\{−x\}dx=n! 可直接套用于选填题。
- **关键概念**：`四分之一圆面积`、`配完全平方`、`根式代换`、`点火公式`
- **出处**：[陈哥 P77](https://www.bilibili.com/video/BV1husGzwEtZ?p=77)

### 无穷区间广义积分的定义与敛散性判断
- **要点**：把变上限积分的上限改成正无穷（或无穷），形如 ∫_a\^\{+∞\} f(x)dx 的积分就叫无穷区间上的广义积分；只要上下限里有无穷就是这种广义积分，它也可以写成极限形式 lim\_\{b→+∞\}∫_a^b f(x)dx，两者意思相同。计算时先把它当定积分处理，按不定积分的方法（必要时凑微分，如把 1/x 凑成 d ln x）求出原函数，再杠上上下限套牛顿-莱布尼茨公式；遇到无穷的那一端不能直接代入，要写成极限形式再按「先带点」求极限。结果分两种情况：极限是确定的常数则极限值存在，称这个广义积分收敛；结果是无穷或极限不存在，则称发散。填空题里问广义积分等于谁时一般结果是收敛的数值，问敛散性时则可能是发散。计算中反复用到几个极限结论：无穷分之一（k/∞）结果为 0，不论正无穷还是负无穷；e\^\{−∞\}=0，即 x→+∞ 时 e\^\{−x\}→0；arctan x 有 π/2 与 −π/2 两条渐近线，x→+∞ 时为 π/2、x→−∞ 时为 −π/2。代入时要带全，如 ln|ln x| 在 x=e 处是 ln1=0，有两层要对准。
- **关键概念**：`无穷区间上的广义积分`、`lim∫f dx`、`化为极限`、`先带点`、`收敛`、`发散`、`k/∞=0`、`e^{−∞}=0`、`arctan(+∞)=π/2`
- **相互关系**：是变上限积分的推广，敛散性由对应极限是否存在决定；把定积分的计算方法与极限的求法串联起来，并与极限部分、arctan x 图像的结论衔接。
- **出处**：[学士帽 P67](https://www.bilibili.com/video/BV1X4411J792?p=67)

### 瑕积分（无界函数的反常积分）
- **要点**：被积函数无定义（无界）的点称为瑕点（无穷间断点），分左端点、右端点、区间内部点三种情形。积出原函数后，代值遇瑕点写成 lim\_\{x→x₀\} 的极限形式；求法是把瑕点换成 C，再求 C 趋于瑕点的单侧极限（瑕点在左侧取左极限，在右侧取右极限）。瑕点在区间内部时必须拆成两个瑕积分分别计算，两段同时收敛才收敛。典型如 ∫_0^1 ln x dx 用分部积分并处理 0·∞ 型，∫\_\{−1\}\^\{1\}(1/x)dx 两端均发散。
- **关键概念**：`瑕积分`、`瑕点`、`无界函数`、`单侧极限`、`拆成两个积分`
- **相互关系**：与无穷区间反常积分只差极限趋近的对象；仅个别省份考纲要求，广东升本基本不考。
- **出处**：[陈哥 P78](https://www.bilibili.com/video/BV1husGzwEtZ?p=78)；[ok姐 P68](https://www.bilibili.com/video/BV1vm421s7mv?p=68)

### 微元法（元素法）
- **要点**：在区间上取宽为 dx 的窄条，窄到可近似看作长方形，面积微元 dS=f(x)dx；积分即把所有微元连续累加。
- **关键概念**：`微元法`、`面积微元`、`累加`
- **相互关系**：是后续旋转体体积、二重积分的基础方法。
- **出处**：[陈哥 P79](https://www.bilibili.com/video/BV1husGzwEtZ?p=79)

### X 型与 Y 型区域及面积公式
- **要点**：X 型：竖线平移时首尾只与上、下边界各交一次，S=∫_a^b(上−下)dx；Y 型：横线上下平移时首尾只与右、左边界各交一次，边界须写成 x=φ(y)，S=∫_c^d(右−左)dy。积分限均由交点坐标确定，两侧可为直线或退化为点。本质都是「大面积减小面积」。
- **关键概念**：`X 型`、`Y 型`、`上减下`、`右减左`、`交点定限`
- **相互关系**：同一图形二者皆可时按计算简便选择；分不清会影响后续二重积分；y 型计算前必须把函数改写成 x= 关于 y 的表达式。
- **出处**：[陈哥 P79](https://www.bilibili.com/video/BV1husGzwEtZ?p=79)；[杰哥 P80](https://www.bilibili.com/video/BV1Up4y1Y76a?p=80)；[米哥 P80](https://www.bilibili.com/video/BV1swAWerEzS?p=80)；[帆哥 P1](https://www.bilibili.com/video/BV1xxXZBKENv?p=1)

### 类型判别与解题流程
- **要点**：用「穿线法」判别——垂直 x 轴画线左右移动，若上方始终只交一个函数、下方也始终只交一个函数则为 x 型；垂直 y 轴画线则为 y 型。解题三步：画图并求交点坐标（交点决定积分上下限）→ 定类型 → 套公式。只画题目给出的曲线，以免围出多格难辨。
- **关键概念**：`穿线法`、`联立求交点`、`画图—定类型—套公式`
- **出处**：[杰哥 P80](https://www.bilibili.com/video/BV1Up4y1Y76a?p=80)、[P81](https://www.bilibili.com/video/BV1Up4y1Y76a?p=81)；[帆哥 P1](https://www.bilibili.com/video/BV1xxXZBKENv?p=1)

### 需拆分的图形
- **要点**：竖线平移时上（或下）边界在两段曲线间切换，则该图形不能整体视为 X 型，应过交点分成两块分别计算再相加；若上下（或左右）方向上有不止一个函数，则既非单纯 x 型也非单纯 y 型，须从函数改变的分界处切开，分段计算后相加。求面积直接用「上减下」，不必考虑符号。被一条竖线分成两块则分别列式；被积函数「上减下」，贴 x 轴部分取上方曲线。
- **关键概念**：`拆分图形`、`分段积分`、`分块列积分`
- **相互关系**：X 型与 Y 型可互相转化；需先把 x=y² 理解为 y=±√x，以判断上边界。
- **出处**：[陈哥 P79](https://www.bilibili.com/video/BV1husGzwEtZ?p=79)；[杰哥 P81](https://www.bilibili.com/video/BV1Up4y1Y76a?p=81)；[帆哥 P1](https://www.bilibili.com/video/BV1xxXZBKENv?p=1)

### 求平面图形面积：以 x 轴为基准（上限减下限）
- **要点**：图形由上面一根曲线 f₁(x) 与下面一根曲线 f₂(x) 连同 x=a、x=b 围成时，用大面积减小面积，把区域相同的两个积分合并得 S=∫_a^b[f₁(x)−f₂(x)]dx；即积分变量是 dx 时用「上限减下限求定积分」——上限是上面这根线、下限是下面这根线。若图形只有一根曲线与 x 轴围成，可把 x 轴当作下限 y=0（代入是 0 不用减），也可理解成只有一根线——这根曲线是谁被积函数就是谁。做题第一步先画图看清区域，再定变量发生在哪个轴上（题中有 x=2 一类竖线时 x 的范围即由它给出）。dx 情形下每根线的表达式都必须先整理成 y=⋯x：x=y² 要开方成 y=±√x，开方要加绝对值、去绝对值加正负号，再按交点所在半轴取正号（交点全在上半轴时只取正的 √x）。
- **关键概念**：`以 x 轴为基准`、`积分变量 dx`、`上限减下限求定积分`、`大面积减小面积`、`先画图`、`x=y² 整理成 y=±√x`
- **相互关系**：是定积分几何意义的直接应用，并把「一根线」推广到「两根线」；与以 y 轴为基准（右线减左线）对称，把上下限换成左右线、把 y=⋯x 换成 x=⋯y。
- **出处**：[学士帽 P66](https://www.bilibili.com/video/BV1X4411J792?p=66)

### 求平面图形面积的第二种类型：以 y 轴为基准（右线减左线）
- **要点**：变化量发生在 y 轴上（y 的范围由常数 c 到常数 d）时，曲线表达式要写成 x=g(y)、积分变量用 dy：只有一根曲线时 S=∫_c^d g(y)dy；两根曲线 g₁(y)、g₂(y) 与 y=c、y=d 围成时用大面积减小面积，S=∫_c^d[g₁(y)−g₂(y)]dy，其中 g₁ 是靠右的那根、g₂ 是靠左的那根，规律记成「右线减左线求定积分」。积分限由联立两曲线求交点得到；右线、左线都必须先整理成 x=⋯y（如直线 x+y=2 写成 x=2−y，xy=1 写成 y=1/x 后再化成 x=1/y）。同一图形若用 dx 要从交点处把图形拆成两个定积分，改用 dy 只需一个表达式，故按计算简便选择。
- **关键概念**：`以 y 轴为基准`、`积分变量 dy`、`表达式写成 x=g(y)`、`右线减左线求定积分`、`联立求交点定限`
- **相互关系**：与第一种类型（以 x 轴为基准）对称；本质仍是「大面积减小面积」。
- **出处**：[学士帽 P66](https://www.bilibili.com/video/BV1X4411J792?p=66)

### 由面积条件反求函数表达式
- **要点**：若题目给出「曲线与直线围成图形面积 = 关于 T 的表达式」，先按面积公式写出上限为 T 的积分上限函数等式，两边对 T 求导即可解出 f。
- **关键概念**：`积分上限函数`、`两边求导`
- **相互关系**：本质是变限积分求导与几何应用的综合。
- **出处**：[ok姐 P69](https://www.bilibili.com/video/BV1vm421s7mv?p=69)

### 面积函数的最值
- **要点**：区域由含参竖直边界线决定时面积是参数的函数；判断导数在定义域内的正负即可定位最小值点；判符号可借图像平移（如 2√a−1 为 2√a 下移一单位）。
- **关键概念**：`面积函数 S(a)`、`驻点`、`单调性`
- **相互关系**：「求面积」与「导数求最值」的串联题型，零点往往是有理数。
- **出处**：[帆哥 P1](https://www.bilibili.com/video/BV1xxXZBKENv?p=1)

### 面积最小问题
- **要点**：设切点→由导数得斜率写切线方程→把面积表为切点参数的函数→求导找驻点并判单调性。
- **关键概念**：`驻点`
- **出处**：[米哥 P80](https://www.bilibili.com/video/BV1swAWerEzS?p=80)、[P81](https://www.bilibili.com/video/BV1swAWerEzS?p=81)

### 旋转体体积：x 型图绕 x 轴
- **要点**：取微元看作薄圆柱体，底面积 πf²(x)、高 dx，故 V=π∫_a^b f²(x)dx（三要素：系数 π、积分上下限、被积函数是曲线函数的平方）。两曲线之间用外侧大体积减内侧小体积，V=π∫_a^b[f上²(x)−f下²(x)]dx。是高数二、高数三的大题考点。题目直接给出 y² 的表达式时可直接代入被积函数。
- **关键概念**：`微元法`、`πr²`、`大体积减小体积`、`圆盘法`
- **相互关系**：体积微元 πf²(x)dx 由薄片近似为圆柱体（底面积 πR² × 高 dx）得到。
- **出处**：[杰哥 P82](https://www.bilibili.com/video/BV1Up4y1Y76a?p=82)；[米哥 P81](https://www.bilibili.com/video/BV1swAWerEzS?p=81)；[ok姐 P70](https://www.bilibili.com/video/BV1vm421s7mv?p=70)

### 旋转体体积：y 型图绕 y 轴
- **要点**：推导与上一种完全相同，只需把 x 换成 y：V=π∫_c^d f²(y)dy；两曲线之间用右侧减左侧。φ(y) 是 x 关于 y 的表达式，绕谁旋转就对谁分割、对谁积分；若题给曲线是 y=f(x) 形式，须先求反函数 x=φ(y)（y=ln x 的反函数为 x=e^y，y=e^x 的反函数为 x=ln y，xy=1 的反函数为 x=1/y）。
- **关键概念**：`绕 y 轴旋转`、`f(y)`、`反函数`、`对 y 积分`
- **出处**：[杰哥 P82](https://www.bilibili.com/video/BV1Up4y1Y76a?p=82)；[米哥 P81](https://www.bilibili.com/video/BV1swAWerEzS?p=81)；[ok姐 P71](https://www.bilibili.com/video/BV1vm421s7mv?p=71)

### 旋转体体积：x 型图绕 y 轴（柱壳法）
- **要点**：图形先与 x 轴围成、再绕 y 轴旋转，微元是展开的薄壳，底面周长 2πx、高 f(x)、厚 dx，故 V=2π∫_a^b x f(x)dx。最易与「y 型绕 y 轴」混淆，判别看题干是否先说「与 x 轴围成」再「绕 y 轴旋转」。与轴相接用圆盘法，与轴有空隙用柱壳法。
- **关键概念**：`柱壳法`、`周长 2πx`
- **出处**：[杰哥 P82](https://www.bilibili.com/video/BV1Up4y1Y76a?p=82)；[米哥 P81](https://www.bilibili.com/video/BV1swAWerEzS?p=81)

### 旋转体体积公式与求解步骤（绕 x 轴、绕 y 轴）
- **要点**：绕哪个轴旋转，积分变量就是谁。绕 x 轴旋转一周：V_x=π∫_a^b(上限²−下限²)dx；绕 y 轴旋转一周：V_y=π∫_c^d(右线²−左线²)dy。与求面积公式相比只差两点——前面多乘一个 π，上限、下限（或右线、左线）各自变成自己的平方，即「上限方减下限方」「右线方减左线方」，这四个公式一定要记清。步骤与求面积一样先把图像画出来；若只有一根曲线绕轴旋转（另一根线是坐标轴，即 y=0 或 x=0），被积函数直接写成这条曲线表达式的平方，不必再减。绕 y 轴旋转时必须注意：表达式一律要整理成 x=⋯y 的形式再平方（如 y=x² 取右半支得 x=√y），考试题一定会标明取哪半支。同一图形求面积、绕 x 轴体积、绕 y 轴体积三个量方法一致，其中绕 y 轴时两根线都要旋转、左线须整理成 x=⋯y（如 y=ln x 写成 x=e^y），遇到 e\^\{2y\} 这类还要凑微分（d 后乘 2、积分号前补 ½）才能套公式。
- **关键概念**：`旋转体体积`、`Vx`、`Vy`、`上限方减下限方`、`右线方减左线方`、`整理成 x=…y`、`右半支取舍`
- **相互关系**：是定积分求面积公式的推广，只需在面积公式上乘 π 并把表达式平方；图形由两根线围成时改用「右线方减左线方」。
- **出处**：[学士帽 P65](https://www.bilibili.com/video/BV1X4411J792?p=65)

### 椭圆绕轴旋转的体积公式
- **要点**：椭圆 x²/a²+y²/b²=1 绕 x 轴旋转 V=4/3πab²；绕 y 轴旋转 V=4/3πa²b。记忆要点：绕 x 轴时平方落在 b 上，绕 y 轴时平方落在 a 上。
- **关键概念**：`椭圆标准方程`、`旋转体体积公式`
- **相互关系**：填空题可直接套公式；也可由 π∫\_\{−a\}\^\{a\}y²dx 推出。
- **出处**：[ok姐 P70](https://www.bilibili.com/video/BV1vm421s7mv?p=70)、[P71](https://www.bilibili.com/video/BV1vm421s7mv?p=71)

### 平面曲线弧长
- **要点**：直角坐标下 s=∫_a^b √(1+y′²)dx；参数方程 x=g(t), y=h(t)（t∈[α,β]）下 s=∫_α^β √(g′²(t)+h′²(t))dt。
- **关键概念**：`弧长`、`弧微分`、`勾股定理`、`参数方程求导`
- **相互关系**：由小直角三角形勾股定理得弧微元 dl=√(dx²+dy²)；套公式前先求导并平方。
- **出处**：[ok姐 P72](https://www.bilibili.com/video/BV1vm421s7mv?p=72)


### 微元思想、曲边梯形与定积分的定义
- **要点**：求不规则图形面积时先切成极窄的竖条，用「底×高」的矩形面积逐条累加，条越窄结果越精确。任意边角小块都可归结为「三条直线边加一条曲线边」的曲边梯形，故只需解决曲边梯形面积。把底边放在 $x$ 轴上、两端为 $x=a$、$x=b$、上方曲线为 $y=f(x)$，面积近似为 $\sum\_\{i=1\}\^\{n\}f(x_i)\Delta x$，令 $\Delta x\to0$（即 $n\to\infty$）取极限得 $\int_a^bf(x)dx$。
- **关键概念**：`微元思想`、`曲边梯形`、`窄矩形`、`$\Delta x$`、`$\int_a^bf(x)dx$`、`积分上限`、`积分下限`、`积分区间`
- **相互关系**：$\int_a^bf(x)dx$ 中拉长的 $S$ 是积分号，$f(x)$ 是被积函数，$f(x)dx$ 是被积表达式，$x$ 是积分变量；与不定积分记号的唯一区别就是多了上下限。专升本只要求理解这一极限思想，不要求用定义式计算。
- **出处**：[石头 P49](https://www.bilibili.com/video/BV18CL26WEJ3?p=49)

### 定积分是带符号的面积
- **要点**：定积分的几何意义是曲线 $y=f(x)$、直线 $x=a$、$x=b$ 与 $x$ 轴围成的「带符号面积」。$f(x)$ 全在 $x$ 轴上方时结果为正，全在下方时为负，上下都有时用上方面积减下方面积，正负可以抵消。
- **关键概念**：`带符号面积`、`线下面积`、`上方面积减下方面积`
- **相互关系**：这是定积分与不定积分的本质区别——不定积分求原函数、结果是一族函数，定积分的结果是一个确定数值；带符号面积也是后面偶倍奇零与瑕积分的判断依据。
- **出处**：[石头 P49](https://www.bilibili.com/video/BV18CL26WEJ3?p=49)

### 积分上下限的规定
- **要点**：定积分不要求上限大于下限。规定 $\int_a^af(x)dx=0$，因为起点与终点相同、扫过的面积为零；又规定 $\int_a^bf(x)dx=-\int_b^af(x)dx$，即上下限对调要添负号，相当于从右往左扫。
- **关键概念**：`$\int_a^af(x)dx=0$`、`$\int_a^bf(x)dx=-\int_b^af(x)dx$`、`上下限对调`
- **相互关系**：这两条规定在后续换元、偶倍奇零、反常积分中反复使用；$f(x)=x^7$ 在 $[1,1]$ 上的积分可直接判为零，无需画图。
- **出处**：[石头 P49](https://www.bilibili.com/video/BV18CL26WEJ3?p=49)

### 牛顿-莱布尼兹公式
- **要点**：若 $F(x)$ 是连续函数 $f(x)$ 在 $[a,b]$ 上的一个原函数，则 $\int_a^bf(x)dx=F(b)-F(a)$，记作 $F(x)\big|_a^b$，即上限代入减去下限代入。有了它求定积分就不必再回到画图求面积的老路，如 $\int\_\{-1\}^1x^2dx=\frac{x^3}{3}\Big|\_\{-1\}^1=\frac23$、$\int_0^1e^xdx=e-1$。它又称微积分基本定理。
- **关键概念**：`牛顿-莱布尼兹公式`、`$\int_a^bf(x)dx=F(x)\big|_a^b$`、`微积分基本定理`
- **相互关系**：公式把定积分计算归结为求原函数，与不定积分彻底打通；原函数取哪一个都行，因为常数在 $F(b)-F(a)$ 中自行抵消，故一律取不带常数的最简形式。
- **出处**：[石头 P50](https://www.bilibili.com/video/BV18CL26WEJ3?p=50)

### 公式的适用前提：被积函数连续
- **要点**：牛顿-莱布尼兹公式要求被积函数 $f(x)$ 在积分区间 $[a,b]$ 上连续。$\frac1x$ 在 $[-1,1]$ 上有无穷间断点 $x=0$，不能直接写成 $\ln|x|\big|\_\{-1\}^1$；分段函数在分段点处断开时，也不能对整个区间一次套用公式，而要借助区间可加性分段后逐段使用。
- **关键概念**：`连续性前提`、`无穷间断点`、`分段函数分段积分`
- **相互关系**：不连续的情形属于反常积分中的瑕积分；这一前提也是后续判断瑕积分能否直接使用公式的标准。
- **出处**：[石头 P50](https://www.bilibili.com/video/BV18CL26WEJ3?p=50)

### 线性性质与区间可加性
- **要点**：性质一：常数因子可外提，$\int_a^bkf(x)dx=k\int_a^bf(x)dx$。性质二：$\int_a^b[f(x)\pm g(x)]dx=\int_a^bf(x)dx\pm\int_a^bg(x)dx$。性质三：$\int_a^bf(x)dx=\int_a^cf(x)dx+\int_c^bf(x)dx$，即区间可加，$c$ 可在区间内也可在区间外。性质四：$\int_a^b1\,dx=b-a$。
- **关键概念**：`常数因子外提`、`和差可拆`、`区间可加性`、`$\int_a^b1\,dx=b-a$`
- **相互关系**：性质三由牛顿-莱布尼兹公式直接验证，是分段函数与瑕积分拆分的依据；性质四也可看作底为 $b-a$、高为 $1$ 的矩形面积，属送分性质。
- **出处**：[石头 P50](https://www.bilibili.com/video/BV18CL26WEJ3?p=50)

### 保号性、比较定理与估值定理
- **要点**：性质五（保号性）：$a&lt;b$ 且 $f(x)\geq0$ 时 $\int_a^bf(x)dx\geq0$。推论一（比较定理）：若 $f(x)\leq g(x)$，则 $\int_a^bf(x)dx\leq\int_a^bg(x)dx$，故比较两个难算的定积分大小时只需比较被积函数。推论二：$\left|\int_a^bf(x)dx\right|\leq\int_a^b|f(x)|dx$。性质六（估值定理）：$m(b-a)\leq\int_a^bf(x)dx\leq M(b-a)$，其中 $m$、$M$ 分别是 $f$ 在 $[a,b]$ 上的最小值与最大值。
- **关键概念**：`保号性`、`比较定理`、`$\left|\int_a^bf\right|\leq\int_a^b|f|$`、`估值定理`、`最小值 $m$、最大值 $M$`
- **相互关系**：推论一由性质五对整体 $g(x)-f(x)$ 使用后拆项证得；估值定理把曲边梯形面积夹在两个矩形之间，如 $f(x)=\sin x+5$ 在 $[1,2]$ 上的积分必在 $4$ 与 $6$ 之间，可直接用于排除选项。
- **出处**：[石头 P50](https://www.bilibili.com/video/BV18CL26WEJ3?p=50)

### 中值定理与偶倍奇零
- **要点**：性质七（中值定理）：$f$ 在 $[a,b]$ 上连续时至少存在一点 $\xi\in[a,b]$ 使 $\int_a^bf(x)dx=f(\xi)(b-a)$，$f(\xi)$ 就是函数在区间上的平均高度。性质八（偶倍奇零）：在对称区间 $[-a,a]$ 上，$f$ 为偶函数时 $\int\_\{-a\}^af(x)dx=2\int_0^af(x)dx$，$f$ 为奇函数时积分等于零。
- **关键概念**：`中值定理（平均值定理）`、`$f(\xi)(b-a)$`、`偶倍奇零`、`对称区间`
- **相互关系**：偶倍奇零要求区间对称且被积函数具备相应奇偶性，常与「奇×偶=奇」等运算性质配合，把复杂被积函数拆成奇、偶两部分后化简；中值定理则给出由平均值反求积分值的思路。
- **出处**：[石头 P50](https://www.bilibili.com/video/BV18CL26WEJ3?p=50)

### 换元必换线
- **要点**：定积分换元时，除了被积函数与积分变量要换，积分上下限也必须换成新变量的范围，即把 $x$ 的上下限代入代换式解出 $t$ 的上下限。口诀是「换元必换线」。若只是凑微分、没有引入新变量，则上下限保持不变。
- **关键概念**：`换元必换线`、`上下限变换`、`凑微分不换线`
- **相互关系**：这是定积分换元与不定积分换元的唯一区别；如令 $\cos x=t$ 时，$x$ 从 $0$ 到 $\frac\pi2$ 对应 $t$ 从 $1$ 到 $0$，此时还可借上下限对调消去负号。
- **出处**：[石头 P51](https://www.bilibili.com/video/BV18CL26WEJ3?p=51)

### 定积分换元的常见代换
- **要点**：凑微分型（如 $\int_0\^\{\frac\pi2\}\cos^5x\sin x\,dx$，把 $\sin x\,dx$ 凑成 $d(-\cos x)$）不换元故不换线；含 $\sqrt{ax+b}$ 用根式代换，令整体为 $t$，如 $\int_0^2\frac{dx}{1+\sqrt x}$ 令 $\sqrt x=t$；含 $\sqrt{a^2-x^2}$ 等用三角代换，如 $\int\_\{\frac\{\sqrt2\}2\}^1\frac{\sqrt{1-x^2}}{x^2}dx$ 令 $x=\sin t$ 后上下限变为 $\frac\pi4$ 与 $\frac\pi2$；被积函数为 $f(x-k)$ 型可令 $x-k=t$，相当于图像与积分区间同步平移。
- **关键概念**：`凑微分`、`根式代换`、`三角代换`、`平移代换`、`$\sqrt x=t$`
- **相互关系**：换元后仍按「先求原函数、再代上下限」计算；分段函数换元后要借助区间可加性分段积分，换元后上下限也随之整体平移。
- **出处**：[石头 P51](https://www.bilibili.com/video/BV18CL26WEJ3?p=51)

### 积分变限函数的定义
- **要点**：定积分的上下限中含自变量时，积分结果随 $x$ 变化，这种函数称积分变限函数，写作 $F(x)=\int\_\{\varphi\_1(x)\}\^\{\varphi\_2(x)\}f(t)dt$。它是关于 $x$ 的函数而不是关于 $t$ 的函数，因为被积曲线 $f(t)$ 固定不动，变动的是上下限。
- **关键概念**：`积分变限函数`、`变上限积分`、`$\int_{\varphi_1(x)}^{\varphi_2(x)}f(t)dt$`、`关于 $x$ 的函数`
- **相互关系**：它把定积分从「一个数值」升级为「一个函数」，体现微分与积分的互逆关系，也是用洛必达处理含积分式极限的前提。个别省份不考本知识点，需对照考试大纲。
- **出处**：[石头 P53](https://www.bilibili.com/video/BV18CL26WEJ3?p=53)

### 积分变限函数的求导公式
- **要点**：$\frac{d}{dx}\int\_\{\varphi\_1(x)\}\^\{\varphi\_2(x)\}f(t)dt=f(\varphi_2(x))\varphi_2'(x)-f(\varphi_1(x))\varphi_1'(x)$，口诀「上限代入上限导，减去下限代入下限导」，由复合函数求导法则导出。下限为常数时后项为零可直接省去；上下限均为常数时结果为 $0$。特例 $\frac{d}{dx}\int_a^xf(t)dt=f(x)$，说明下限为常数、上限为 $x$ 的变限函数就是 $f(x)$ 的一个原函数。
- **关键概念**：`上限代入上限导`、`下限代入下限导`、`$\frac{d}{dx}\int_a^xf(t)dt=f(x)$`
- **相互关系**：凡遇积分变限函数，固定思路就是求导，无论题目问的是求导、求极限还是别的形式；特例把定积分与不定积分重新联系起来。
- **出处**：[石头 P53](https://www.bilibili.com/video/BV18CL26WEJ3?p=53)

### 积分变限函数求极限：洛必达法则
- **要点**：$\frac00$ 型极限中若含积分变限函数，用洛必达法则对分子分母分别求导，求导时套用「上限代入上限导减下限代入下限导」，积分号随之消失，再按普通极限方法（等价无穷小、非零因子直接代入、有理化）继续算。上下限相等（如 $\int_1^1$）时积分为零，可据此先判断是否属于 $\frac00$ 型。
- **关键概念**：`洛必达法则`、`$\frac00$ 型`、`积分号消失`、`等价无穷小`
- **相互关系**：这是积分变限函数最常考的题型；洛必达与等价无穷小不能在同一步混用，须先等价再洛必达或先洛必达再等价。
- **出处**：[石头 P53](https://www.bilibili.com/video/BV18CL26WEJ3?p=53)

### 无穷限反常积分
- **要点**：积分区间无限的反常积分有三种形式 $\int_a\^\{+\infty\}$、$\int\_\{-\infty\}^a$、$\int\_\{-\infty\}\^\{+\infty\}$。计算方法与普通定积分相同，仍用牛顿-莱布尼兹公式，只把无穷限理解为取极限，如 $\int\_\{-\infty\}^0e^xdx=e^x\big|\_\{-\infty\}^0=1-0=1$。
- **关键概念**：`反常积分`、`广义积分`、`无穷限`、`取极限`
- **相互关系**：与定积分的区别只在积分区间是否有限，计算套路完全沿用牛顿-莱布尼兹公式；它是「不正常的」定积分，仍可从面积角度理解。
- **出处**：[石头 P54](https://www.bilibili.com/video/BV18CL26WEJ3?p=54)

### 反常积分的敛散性
- **要点**：算出来是一个确定的数值，则称该反常积分收敛；算出来是无穷或算不出结果，则称发散，作答时必须写明「发散」。如 $\int_0\^\{+\infty\}e^xdx=+\infty$ 发散，而 $\int\_\{-\infty\}\^\{+\infty\}\frac{1}{1+x^2}dx=\arctan x\Big|\_\{-\infty\}\^\{+\infty\}=\pi$ 收敛。
- **关键概念**：`收敛`、`发散`、`$\arctan(+\infty)=\frac\pi2$`、`$\arctan(-\infty)=-\frac\pi2$`
- **相互关系**：判断敛散性就是老老实实算出结果再看它是不是数值；图像上收敛对应有限面积，发散对应面积无限增大。
- **出处**：[石头 P54](https://www.bilibili.com/video/BV18CL26WEJ3?p=54)

### 无界函数的反常积分（瑕积分）
- **要点**：被积函数在积分区间内某点趋于无穷（无穷间断点）时，该点称瑕点，这类积分称瑕积分。瑕点在端点处时可直接用牛顿-莱布尼兹公式计算；瑕点在区间内部时必须从瑕点处把区间拆成两个分别计算，只有两个都收敛整个瑕积分才收敛。如 $\int\_\{-1\}^1\frac1xdx$ 的瑕点是 $x=0$，而 $\int_0^1\frac1xdx=\ln x\big|_0^1=0-(-\infty)$ 发散，故原积分发散。
- **关键概念**：`瑕积分`、`瑕点`、`无穷间断点`、`从瑕点处拆分`、`都收敛才收敛`
- **相互关系**：瑕积分不能套用偶倍奇零，正无穷与负无穷也不能互相抵消；$\int_0^1\frac{1}{\sqrt x}dx=2\sqrt x\big|_0^1=2$ 说明瑕点在端点时仍可能收敛。
- **出处**：[石头 P54](https://www.bilibili.com/video/BV18CL26WEJ3?p=54)

### 求平面图形面积的三步法
- **要点**：第一步在草稿纸上画草图，看清各曲线与所围区域；第二步联立两条曲线方程求交点坐标，目的是确定积分上下限；第三步写出被积函数并列定积分求解。
- **关键概念**：`画草图`、`联立方程求交点`、`列定积分求解`
- **相互关系**：本质仍是微元思想，只是把窄矩形的「高」由 $f(x)$ 换成两条曲线之差；若上下限一眼可看出（如 $x=\pm1$）则可跳过第二步。
- **出处**：[石头 P55](https://www.bilibili.com/video/BV18CL26WEJ3?p=55)

### 积分变量的选择与面积的被积函数
- **要点**：积分变量选 $x$ 还是选 $y$，取决于哪个计算更简单。对 $x$ 积分时从最左端积到最右端，被积函数用上方曲线减下方曲线；对 $y$ 积分时从最下端积到最上端，用右边曲线的 $x$ 值减左边曲线的 $x$ 值，需要先把方程反解成 $x=\varphi(y)$。面积恒为正，故必须用大减小，不能让上下两块互相抵消。
- **关键概念**：`积分变量选择`、`上减下`、`右减左`、`反解 $x=\varphi(y)$`
- **相互关系**：当上（或下）方曲线由多段不同函数组成时，改用另一变量可避免分段；$y=x^3$ 与 $y=4x$ 所围图形上下两块面积相等但不能抵消，须相加。
- **出处**：[石头 P55](https://www.bilibili.com/video/BV18CL26WEJ3?p=55)

### 旋转体的体积
- **要点**：平面图形绕轴旋转一周所得立体称旋转体，仍用微元思想「由面成体」，把立体切成垂直于转轴的一个个截面累加，截面圆的面积为 $\pi R^2$。绕 $x$ 轴旋转时 $V=\pi\int_a^by^2dx$（$y$ 用 $f(x)$ 代入），绕 $y$ 轴旋转时 $V=\pi\int_c^dx^2dy$（$x$ 用 $\varphi(y)$ 代入）。若截面是内有空腔的圆环，被积函数改为大圆面积减小圆面积。
- **关键概念**：`旋转体`、`$V=\pi\int_a^by^2dx$`、`$V=\pi\int_c^dx^2dy$`、`圆环截面`、`$\pi R^2$`
- **相互关系**：绕哪个轴旋转就选哪个变量作积分变量，另一个变量必须用曲线方程换成该变量的函数；$y=x^2$ 与 $y=1$ 围成的区域绕 $y$ 轴旋转得 $V=\frac\pi2$，绕 $x$ 轴旋转则为 $\frac{8\pi}{5}$，两种情形不要混用公式。
- **出处**：[石头 P56](https://www.bilibili.com/video/BV18CL26WEJ3?p=56)


## 六、常微分方程


### 常微分方程的概念、阶、通解与特解
- **要点**：含未知函数及其导数的方程称为微分方程（方程中不一定要出现 y 和 x，但必须出现 y 的导数；没有导数就不是微分方程）；只含一个自变量时叫常微分方程。方程中未知函数导数的最高阶数即为方程的阶；判断时只看「求了几次导」，与幂次无关：y\^\{10\}（10 个 y 相乘）是幂，y\^\{(10)\} 这类带括号的才是十阶导数，y″ 的五次方仍是二阶方程。解中含有独立常数 C 且个数等于方程阶数的式子叫通解（独立常数指不能通过加减乘除互相合并的常数）；把初始条件代入通解定出各常数后得到的、不含任意常数的解叫特解。学士帽补充：专升本主要研究一阶与二阶方程；凡题目中出现「斜率」，一定与导数相关，应把条件翻译成 y′=f(x) 的形式。
- **关键概念**：`常微分方程`、`阶数`、`通解`、`特解`、`独立常数`、`恒等式`
- **相互关系**：判断一个函数是否为通解要同时满足两点——代入后是恒等式，且独立常数个数等于阶数；三阶方程只解出两个独立常数说明算错了；有几个独立常数就需要几个初始条件；是选填题考点。
- **出处**：[陈哥 P108](https://www.bilibili.com/video/BV1husGzwEtZ?p=108)；[杰哥 P137](https://www.bilibili.com/video/BV1Up4y1Y76a?p=137)、[P138](https://www.bilibili.com/video/BV1Up4y1Y76a?p=138)、[P141](https://www.bilibili.com/video/BV1Up4y1Y76a?p=141)；[米哥 P126](https://www.bilibili.com/video/BV1swAWerEzS?p=126)；[学士帽 P97](https://www.bilibili.com/video/BV1X4411J792?p=97)、[P98](https://www.bilibili.com/video/BV1X4411J792?p=98)；[ok姐 P73](https://www.bilibili.com/video/BV1vm421s7mv?p=73)

### 线性微分方程的识别
- **要点**：线性指方程中函数 y 及各阶导数都是一次幂，不能出现 y²、(y′)³、y·y′ 这类乘积或幂次，也不能出现 ln y、cos y 等复合形式；x 前的系数无论多复杂都不影响线性判断，只看 y 这一族。y 相关项均一次且不在复合函数内为线性。与「阶数」是两个独立的判断维度，选择题常要求同时给出「几阶 + 线性/非线性」。
- **关键概念**：`线性`、`一次幂`、`y 及其各阶导数`
- **出处**：[杰哥 P139](https://www.bilibili.com/video/BV1Up4y1Y76a?p=139)；[米哥 P126](https://www.bilibili.com/video/BV1swAWerEzS?p=126)

### 齐次与非齐次的识别
- **要点**：把含 y 及其导数的项全部移到等号左边，把只含 x 的函数（自由项 q(x)）移到右边；右边为零叫齐次，不为零叫非齐次。判断前必须先移项，不能只看表面是否等于零。与「一阶齐次微分方程」（指 x、y 各项次数相同）是含义不同的两个「齐次」，容易混淆。
- **关键概念**：`齐次`、`非齐次`、`自由项`
- **相互关系**：齐次性只由 f(x) 是否为零决定，与系数无关。
- **出处**：[陈哥 P115](https://www.bilibili.com/video/BV1husGzwEtZ?p=115)、[P116](https://www.bilibili.com/video/BV1husGzwEtZ?p=116)；[杰哥 P140](https://www.bilibili.com/video/BV1Up4y1Y76a?p=140)；[米哥 P126](https://www.bilibili.com/video/BV1swAWerEzS?p=126)

### 可直接积分求解的类型
- **要点**：形如「左边是 y 的导数、右边是只含 x 的式子」的方程，两边直接积分即可。y′=f(x) 积一次得通解（含 1 个常数）；y″=f(x) 积两次得通解（含 2 个常数，先积出 y′ 再积出 y）；y\^\{(n)\}=f(x) 型两边连续积分 n 次，每积一次降一阶，注意常数项积分时其原函数是「常数 × x」。积分号去掉后必须补上任意常数 C。学士帽指出这是变量分离法的基础形式，考场上很少直接考这么简单的形式。
- **关键概念**：`左右同时取积分`、`y′=dy/dx`、`逐次积分`、`任意常数 C`、`可降阶`
- **相互关系**：只写右边的常数 C 即可，左边的常数与右边的常数可以合并，不能算作两个独立常数。
- **出处**：[陈哥 P108](https://www.bilibili.com/video/BV1husGzwEtZ?p=108)；[杰哥 P142](https://www.bilibili.com/video/BV1Up4y1Y76a?p=142)；[学士帽 P98](https://www.bilibili.com/video/BV1X4411J792?p=98)；[ok姐 P78](https://www.bilibili.com/video/BV1vm421s7mv?p=78)

### 可分离变量微分方程
- **要点**：标准形式为 dy/dx=f(x)g(y)，即等号左边只有一个 y′，右边能写成「只含 x 的函数 × 只含 y 的函数」；题干通常不直接给标准形式，需靠配凑、移项、变形凑出来。步骤：①y′ 改写为 dy/dx；②变形使一边只含 y、一边只含 x，整理成 g(y)dy=f(x)dx（尽量把 dx 乘过去、避免出现 1/dx）；③两边同时积分；④补上任意常数 C；⑤尽量化简成 y=…，化不出可保留隐式；⑥求特解时代入初始条件定 C。
- **关键概念**：`标准形式`、`f(x)`、`g(y)`、`配凑移项`、`分离变量`、`两边积分`、`隐式通解`、`特解`
- **相互关系**：识别要点是右边能否拆成两个一元函数之积；拆不开就要考虑齐次型或线性型；一阶非线性微分方程一定可分离变量（非线性指方程中出现 y 与 y′ 之间的乘除、乘方、复合，如 y²、y′²、y′/y、cos y、e^y），直接用分离变量法。
- **出处**：[陈哥 P109](https://www.bilibili.com/video/BV1husGzwEtZ?p=109)、[P110](https://www.bilibili.com/video/BV1husGzwEtZ?p=110)；[杰哥 P143](https://www.bilibili.com/video/BV1Up4y1Y76a?p=143)；[米哥 P127](https://www.bilibili.com/video/BV1swAWerEzS?p=127)；[学士帽 P98](https://www.bilibili.com/video/BV1X4411J792?p=98)；[ok姐 P74](https://www.bilibili.com/video/BV1vm421s7mv?p=74)

### 分离变量法的积分常数处理
- **要点**：两边积分时只保留一个任意常数 C（两边各出一个常数，移项后合并成一个）。当另一边是单纯的对数形式时，常把常数写成 ln|C|，以便用对数运算合并真数；若另一边不是单纯对数，则不必如此处理。C 本身代表任意常数，故 e^C 仍可写成任意常数 C；C₁±C₂、C₁C₂、C₁/C₂、±e\^\{C₁\}、ln C₁ 等都可合并为一个任意常数 C。由 ln|y|=… 去绝对值后会出现 ±，可把 ±e\^\{C₁\} 整体记为一个新的任意常数 C；注意 C 必须能取遍全体实数，因此不能写成 e^C 这种只取正值的记号。
- **关键概念**：`任意常数 C`、`ln|C|`、`去绝对值`、`正负号吸收`、`独立常数`
- **相互关系**：易错点——把 C 写成 e^C 会缩小取值范围；这是化简通解、判断独立常数个数的常用手段。
- **出处**：[陈哥 P109](https://www.bilibili.com/video/BV1husGzwEtZ?p=109)、[P110](https://www.bilibili.com/video/BV1husGzwEtZ?p=110)；[杰哥 P143](https://www.bilibili.com/video/BV1Up4y1Y76a?p=143)；[米哥 P127](https://www.bilibili.com/video/BV1swAWerEzS?p=127)；[ok姐 P73](https://www.bilibili.com/video/BV1vm421s7mv?p=73)

### 隐式通解与显式通解
- **要点**：积分后得到的常是隐式通解（y 未单独解出）。原则上隐式通解不扣分，但部分地区阅卷标准要求化为显式 y=…，故能显化时应尽量显化；有些方程（如同时出现 ln y 与 y²）无法显化，保留隐式即可。显化常用取指数的手段把 ln 去掉。
- **关键概念**：`隐式通解`、`显函数`、`显化`
- **出处**：[陈哥 P109](https://www.bilibili.com/video/BV1husGzwEtZ?p=109)、[P110](https://www.bilibili.com/video/BV1husGzwEtZ?p=110)、[P112](https://www.bilibili.com/video/BV1husGzwEtZ?p=112)

### 指数与对数的化简规则（解微分方程时）
- **要点**：整理通解常用 e\^\{a+b\}=e^a e^b、e\^\{a−b\}=e^a/e^b；去 ln 用 e 为底、去 e 用 ln，二者互为逆运算可直接抵消；C 本身代表任意常数，故 e^C 仍可写成任意常数 C；本章默认函数式为正，故 1/y 积分时 ln 后不加绝对值，其它章节仍须加。对数运算只有 ln(ab)=ln a+ln b 与 ln(a/b)=ln a−ln b 两条，ln(a+b) 不可拆。
- **关键概念**：`e^{a+b}=e^a e^b`、`ln 与 e 互消`、`e^C 记为 C`
- **出处**：[学士帽 P98](https://www.bilibili.com/video/BV1X4411J792?p=98)

### 一阶微分方程的三种类型
- **要点**：一阶微分方程只含 y′（也写作 dy/dx），最高阶为一阶。常考三类：一阶可分离变量型、一阶齐次型、一阶线性型；其中可分离变量型与线性型出题频率最高，齐次型只有个别省份考查。判断类型是选方法的前提；dy/dx 与 y′ 必须视为同一记号。
- **关键概念**：`阶数`、`y′`、`dy/dx`、`通解`、`特解`
- **出处**：[陈哥 P109](https://www.bilibili.com/video/BV1husGzwEtZ?p=109)、[P110](https://www.bilibili.com/video/BV1husGzwEtZ?p=110)、[P111](https://www.bilibili.com/video/BV1husGzwEtZ?p=111)

### 一阶齐次微分方程
- **要点**：标准形式为 dy/dx=f(y/x)（或 F(y/x)），即右边出现 x、y 之处都统一以 y/x 整体出现；判断标准是方程中 x、y 各项的次数相同（常考二次）。解法固定：令 u=y/x，即 y=ux，两边对 x 求导得 dy/dx=u+x(du/dx)（或 dy=u dx+x du），与标准形式联立后分离变量求解（化为 du/(F(u)−u)=dx/x），积分完必须把 u=y/x 回代。
- **关键概念**：`y/x 看作整体`、`换元 u=y/x`、`回代`、`各项次数相同`
- **相互关系**：本质是在可分离变量基础上多了一步换元；比可分离变量型多「换元 + 求导 + 联立代入」两步，其余步骤相同；此「齐次」指方程中每一项关于 x,y 的次数相同，与一阶齐次线性方程中的「齐次」（自由项为零）含义不同；广东升本考纲有但从未考过。
- **出处**：[陈哥 P110](https://www.bilibili.com/video/BV1husGzwEtZ?p=110)；[杰哥 P144](https://www.bilibili.com/video/BV1Up4y1Y76a?p=144)；[米哥 P128](https://www.bilibili.com/video/BV1swAWerEzS?p=128)；[ok姐 P75](https://www.bilibili.com/video/BV1vm421s7mv?p=75)

### 齐次型化标准形式的技巧
- **要点**：遇到含 xy、x²、y² 的齐次式，通常把分子分母同时除以 x²，即可整理出只含 y/x 的表达式；若右边是 ln y−ln x，用对数相减化真数相除，凑出 ln(y/x)。
- **关键概念**：`分子分母同除 x²`、`对数相减化相除`
- **出处**：[陈哥 P110](https://www.bilibili.com/video/BV1husGzwEtZ?p=110)

### 一阶线性微分方程的标准形式与通解公式
- **要点**：标准形式为 y′+P(x)y=Q(x)，其中 P(x)、Q(x) 是关于 x 的函数（也可为常数）；用公式前必须先把 y′ 的系数化为一（两边除以系数、再把含 x 的项移到右边）。通解为 y=e\^\{−∫P dx\}(∫Q e\^\{∫P dx\}dx+C)。口诀「EPQEPC」：括号外 e 的指数取负的 ∫Pdx；括号内是「Q 乘 e 的正 ∫Pdx 的不定积分 + C」。计算时先单独算出 ∫P dx 这个小积分。
- **关键概念**：`P(x)`、`Q(x)`、`通解公式`、`积分因子`
- **相互关系**：核心是找准 P、Q；识别标志是 y′ 与 y 都只以一次幂出现；x 无法分离时化为 dx/dy+P(y)x=Q(y) 并互换 x、y；遇到一阶方程应优先考虑一阶线性。
- **出处**：[陈哥 P111](https://www.bilibili.com/video/BV1husGzwEtZ?p=111)、[P112](https://www.bilibili.com/video/BV1husGzwEtZ?p=112)；[杰哥 P145](https://www.bilibili.com/video/BV1Up4y1Y76a?p=145)；[米哥 P129](https://www.bilibili.com/video/BV1swAWerEzS?p=129)；[ok姐 P77](https://www.bilibili.com/video/BV1vm421s7mv?p=77)

### 一阶齐次线性微分方程
- **要点**：标准形 y′+P(x)y=0（自由项为零），通解为 y=Ce\^\{−∫P(x)dx\}；也可直接用分离变量法求解。化标准方程要求 y′ 系数为 1、含 y 项在左、自由项在右，再提取 P(x)；任何一阶齐次线性方程都一定可分离变量。
- **关键概念**：`一阶线性`、`标准方程`、`P(x)`、`自由项`
- **出处**：[ok姐 P76](https://www.bilibili.com/video/BV1vm421s7mv?p=76)

### 一阶线性通解公式的推导
- **要点**：在标准形式两边同乘积分因子 e\^\{∫P dx\}，左边可写成 (e\^\{∫P dx\} y)′（用乘积求导法则与「先积分后求导」的性质验证），两边积分后再乘 e\^\{−∫P dx\} 即得通解公式。推导用于帮助记忆，考试只要求记牢公式并会用。
- **关键概念**：`积分因子`、`乘积求导法则`、`先积分后求导`
- **出处**：[陈哥 P111](https://www.bilibili.com/video/BV1husGzwEtZ?p=111)

### 公式使用中绝对值的省略
- **要点**：当 ∫P dx 积出 ln|·| 时，把对数内层整体取出即可，可不必加绝对值——外层与内层两处正负号同号相乘，结果恒为正；残余的正负号仍可被常数 C 吸收。不省略也不会错，但会增加书写量。一阶线性方程中的 ln 不用加绝对值，最后会被 C 吸收；e\^\{ln□\}=□ 必须熟记。
- **关键概念**：`e^{ln|A|}`、`去绝对值`、`常数吸收`
- **出处**：[陈哥 P111](https://www.bilibili.com/video/BV1husGzwEtZ?p=111)、[P112](https://www.bilibili.com/video/BV1husGzwEtZ?p=112)；[杰哥 P145](https://www.bilibili.com/video/BV1Up4y1Y76a?p=145)

### 一阶线性微分方程的求解流程与例题
- **要点**：解题时先一眼找出 P(x) 与 Q(x)（标准型中间是加号，题目若给减号要看成加上一个负的函数），再套通解公式 y=e\^\{−∫P dx\}[∫Q e\^\{∫P dx\}dx+C]：中括号外是 e 的「负的 P(x) 积分」，中括号里是 Q(x) 乘「P(x) 积分」的 e 次幂再乘 dx，最后加任意常数 C；中括号内外的两个指数部分只差一个负号，记住其中一个即可推出另一个。计算中 e 与 ln 要能互相抵消，ln 前的系数可挪到 x 的指数上（如 ∫(2/x)dx=2ln x，故 e\^\{2ln x\}=x²）；本章 1/x 积分不加绝对值。求出通解后再由初始条件定 C 得特解。
- **关键概念**：`找 P(x)、Q(x)`、`e^{-∫P dx}`、`中括号里的积分`、`e 与 ln 互消`、`特解`
- **相互关系**：与变量分离法并列为常微分方程的两类解法；反复用到指数与对数的运算规则（e^a e^b=e\^\{a+b\}），与变量分离法中的化简同源。
- **出处**：[学士帽 P99](https://www.bilibili.com/video/BV1X4411J792?p=99)

### 二阶可降阶微分方程：两种类型
- **要点**：第一种 y″=f(x,y′)——方程中同时含 x、y′、y″ 但不含 y（缺 y 型）；第二种 y″=f(y,y′)——含 y、y′、y″ 但不含 x（缺 x 型）。判断依据是有没有 y。两类都用 y′=p 降阶，但 y″ 的表示不同，极易混淆。若方程不是显式的 y″=… 形式（如 (1+x²)y″=2xy′），先两边除以系数化为标准形式再判断类型。
- **关键概念**：`可降阶`、`缺 y 型`、`缺 x 型`、`换元降阶`、`y′=p`
- **出处**：[陈哥 P114](https://www.bilibili.com/video/BV1husGzwEtZ?p=114)；[ok姐 P78](https://www.bilibili.com/video/BV1vm421s7mv?p=78)

### 缺 y 型的降阶方法
- **要点**：令 y′=p，则 y″=p′=dp/dx，原方程化为一阶可分离变量方程；解出 p 后再对 dy/dx=p 做一次分离变量积分，共两次分离变量，得两个任意常数。因原式含 x，故 p 视为 x 的函数。
- **关键概念**：`令 y′=p`、`p′=dp/dx`
- **出处**：[陈哥 P114](https://www.bilibili.com/video/BV1husGzwEtZ?p=114)；[ok姐 P78](https://www.bilibili.com/video/BV1vm421s7mv?p=78)

### 缺 x 型的降阶方法
- **要点**：仍令 y′=p，但因原式无 x，需用链式法则改写 y″=dp/dx=(dp/dy)(dy/dx)=p(dp/dy)，代入后同样化为可分离变量方程，再积分两次。
- **关键概念**：`链式法则`、`y″=p·dp/dy`
- **相互关系**：与缺 y 型的关键区别就在这一步，是本节难点；不能直接把 dp/dx 代入（否则出现 x,p,y 三个变量），须乘 dy/dy 变形；广东升本考到的可能性低。
- **出处**：[陈哥 P114](https://www.bilibili.com/video/BV1husGzwEtZ?p=114)；[ok姐 P78](https://www.bilibili.com/video/BV1vm421s7mv?p=78)

### 二阶常系数线性微分方程：常系数与齐次
- **要点**：形如 y″+py′+qy=f(x)（或 ay″+by′+cy=f(x)），y″、y′、y 前面的系数为常数时称常系数；等号右边 f(x)≡0 时称齐次，f(x)≠0 时称非齐次。齐次性只由 f(x) 是否为零决定，与系数无关。标准形要求二阶导系数化为 1。
- **关键概念**：`常系数`、`齐次`、`非齐次`、`自由项 f(x)`
- **出处**：[陈哥 P115](https://www.bilibili.com/video/BV1husGzwEtZ?p=115)、[P116](https://www.bilibili.com/video/BV1husGzwEtZ?p=116)；[杰哥 P146](https://www.bilibili.com/video/BV1Up4y1Y76a?p=146)；[ok姐 P79](https://www.bilibili.com/video/BV1vm421s7mv?p=79)

### 二阶齐次方程通解结构与线性无关
- **要点**：若 y₁,y₂ 是 y″+by′+cy=0 的两个线性无关解，则通解为 y=C₁y₁+C₂y₂。线性相关指两函数仅相差一个常数因子（如 x² 与 2x²），否则线性无关（如 x² 与 x³、e^x 与 e\^\{2x\}）。
- **关键概念**：`线性无关`、`通解结构`
- **出处**：[ok姐 P79](https://www.bilibili.com/video/BV1vm421s7mv?p=79)

### 特征方程与特征根
- **要点**：设 y=e\^\{rx\} 为解代入方程，约去 e\^\{rx\} 得一元二次方程 r²+pr+q=0（或 ar²+br+c=0），称为特征方程；其二次项、一次项、常数项系数分别对应原方程中 y″、y′、y 的系数（y″→r²、y′→r、y→1）。解出的根称特征根。判别式大于零有两个不等实根，等于零有二重根，小于零有一对共轭复根。求根优先用十字相乘，不行再用求根公式。
- **关键概念**：`特征方程`、`特征根`、`y=e^{rx}`、`判别式`
- **相互关系**：微分方程的解与特征方程的解一一对应；特征根的形式直接决定通解的三种写法。
- **出处**：[陈哥 P115](https://www.bilibili.com/video/BV1husGzwEtZ?p=115)；[杰哥 P146](https://www.bilibili.com/video/BV1Up4y1Y76a?p=146)、[P147](https://www.bilibili.com/video/BV1Up4y1Y76a?p=147)；[ok姐 P80](https://www.bilibili.com/video/BV1vm421s7mv?p=80)；[石头 P91](https://www.bilibili.com/video/BV18CL26WEJ3?p=91)

### 二阶齐次方程通解的三种形式
- **要点**：设判别式 Δ。①Δ>0：两个不等实根 r₁≠r₂，y=C₁e\^\{r₁x\}+C₂e\^\{r₂x\}；②Δ=0：二重根 r，y=(C₁+C₂x)e\^\{rx\}（括号中 C₂ 后的 x 不能漏）；③Δ&lt;0：一对共轭复根 α±βi，y=e\^\{αx\}(C₁cos βx+C₂sin βx)。三式写法固定，必须背熟。学士帽给出共轭复根时实部 α=−b/2a、虚部 β=√(4ac−b²)/2a，忘记时可用一元二次方程求根公式现场推导（Δ&lt;0 时根号里换成 4ac−b²，并在后面乘一个 i）。例题：λ²−6λ+9=0 用完全平方写成 (λ−3)²=0 得两个相等的实根 λ=3，通解为 (C₁+C₂x)e\^\{3x\}；y″+y=0 得 λ²=−1，即 λ=±i，写成 0±1·i 故 α=0、β=1，通解为 C₁cos x+C₂sin x（e⁰=1，前面那个因式就是一）。
- **关键概念**：`C₁`、`C₂`、`二重根`、`共轭复根`、`α`、`β`
- **相互关系**：易错点——重根时必须多乘一个 x；复根时 e 的指数取实部 α，三角部分取虚部 β（不带正负号）；C₁、C₂ 与两个根的对应顺序可以互换。
- **出处**：[陈哥 P115](https://www.bilibili.com/video/BV1husGzwEtZ?p=115)；[杰哥 P146](https://www.bilibili.com/video/BV1Up4y1Y76a?p=146)、[P147](https://www.bilibili.com/video/BV1Up4y1Y76a?p=147)；[米哥 P130](https://www.bilibili.com/video/BV1swAWerEzS?p=130)；[学士帽 P98](https://www.bilibili.com/video/BV1X4411J792?p=98)、[P100](https://www.bilibili.com/video/BV1X4411J792?p=100)、[P101](https://www.bilibili.com/video/BV1X4411J792?p=101)；[ok姐 P81](https://www.bilibili.com/video/BV1vm421s7mv?p=81)

### 复数与共轭复根
- **要点**：判别式小于零时引入虚数单位 i，满足 i²=−1，用 i² 替换负号后开方即得复数根（如 √(−16)=4i）。形如 α+βi 与 α−βi 的两个复数称互为共轭复数（实部相同、虚部互为相反数）。
- **关键概念**：`虚数单位 i`、`i²=−1`、`共轭复数`
- **相互关系**：这是专升本高数中唯一用到复数的部分。
- **出处**：[陈哥 P115](https://www.bilibili.com/video/BV1husGzwEtZ?p=115)；[杰哥 P146](https://www.bilibili.com/video/BV1Up4y1Y76a?p=146)；[ok姐 P81](https://www.bilibili.com/video/BV1vm421s7mv?p=81)

### 二阶齐次方程求特解
- **要点**：先求通解，再代入初始条件定常数。二阶方程有两个独立常数，需要两个初始条件；第二个条件通常给的是 y′，因此必须先对通解求导再代入，不能直接把含 y′ 的条件代进通解。含 y′ 的条件需先对通解求导（用乘积求导法则）。
- **关键概念**：`初始条件`、`求导`、`独立常数`
- **相互关系**：易错点——把 y′(0) 的条件代入未求导的通解。
- **出处**：[陈哥 P115](https://www.bilibili.com/video/BV1husGzwEtZ?p=115)；[ok姐 P81](https://www.bilibili.com/video/BV1vm421s7mv?p=81)

### 反问题：由通解求微分方程
- **要点**：给出通解形式反求微分方程时，先看通解属于三种形式中的哪一种，从中读出特征根，再由根反写特征方程 (r−r₁)(r−r₂)=0 并展开，最后把 r²、r、常数分别对应回 y″、y′、y 写出方程。含两个不同指数项说明有两个不等实根。
- **关键概念**：`特征根`、`特征方程`、`反推`
- **相互关系**：常以选择、填空形式出现，是特征根解法的逆用，考得少但需掌握。
- **出处**：[陈哥 P115](https://www.bilibili.com/video/BV1husGzwEtZ?p=115)；[杰哥 P148](https://www.bilibili.com/video/BV1Up4y1Y76a?p=148)

### 非齐次方程的通解结构
- **要点**：二阶常系数非齐次线性方程的通解 = 对应齐次方程的通解 + 该非齐次方程的一个特解 Y*（或 y*）。齐次通解按三种形式求，本节重点只在求 Y*。
- **关键概念**：`齐次通解`、`非齐次特解 Y*`、`通解结构`
- **相互关系**：Y* 与「由初始条件确定的特解」同名但意义不同——Y* 形式唯一，不随初始条件变化；自由项形式任意，升本只要求两类。
- **出处**：[陈哥 P116](https://www.bilibili.com/video/BV1husGzwEtZ?p=116)；[杰哥 P149](https://www.bilibili.com/video/BV1Up4y1Y76a?p=149)；[ok姐 P82](https://www.bilibili.com/video/BV1vm421s7mv?p=82)

### 自由项 f(x) 的形式
- **要点**：重点考查 f(x)=P_m(x)e\^\{λx\}（或 P_n(x)e\^\{αx\}），其中 P_m(x) 为多项式（m 为最高次数），λ 为常数。若题中只出现多项式而没有 e\^\{λx\}，则视为 λ=0。P_m(x) 为三角函数的类型只有极个别省份考查。
- **关键概念**：`P_m(x)`、`多项式`、`λ`、`λ=0`
- **出处**：[陈哥 P116](https://www.bilibili.com/video/BV1husGzwEtZ?p=116)；[杰哥 P149](https://www.bilibili.com/video/BV1Up4y1Y76a?p=149)

### 二阶常系数非齐次线性微分方程的标准型、右端 f(x) 的形式与通解结构
- **要点**：形如 y″+py′+qy=f(x) 的方程叫二阶常系数非齐次线性微分方程：左边与齐次方程完全一样，只是右边换成了与 x 有关的函数 f(x)，带两个撇、属于二阶。考试中 f(x) 无非两种形式：第一类 f(x)=e\^\{λx\}P_m(x)（不含 sin、cos）；第二类 f(x)=e\^\{λx\}P_m(x)cos βx 或 e\^\{λx\}P_m(x)sin βx（含 sin 或 cos）；两类中第一类更好算，考第一种的可能性更大。通解由两部分组成：y=Y+y*，其中 Y 是与之对应的齐次方程的通解（习惯用大 Y 表示），y* 是非齐次方程的一个特解（习惯用带星号的记号表示）。求解分两步：第一步先求齐次方程的通解 Y（与前面方法相同）；第二步找出非齐次方程的一个特解 y*——这是最重要也最复杂的一步。
- **关键概念**：`二阶常系数非齐次线性微分方程`、`标准型 y″+py′+qy=f(x)`、`f(x)=e^{λx}P_m(x)`、`含 sin/cos 的形式`、`通解结构 y=Y+y*`
- **相互关系**：与齐次方程的区别仅在右端，左边相同，所以求解时第一步就是把左边按齐次方程来处理；难点集中在第二步如何设特解。
- **出处**：[学士帽 P102](https://www.bilibili.com/video/BV1X4411J792?p=102)

### 特解 Y* 的设定形式
- **要点**：Y*=Q_m(x)e\^\{λx\}x^k（或 y*=x^k Q_n(x)e\^\{αx\}），三部分分别由 f(x) 决定：Q_m(x) 与 P_m(x) 同次，e\^\{λx\} 原样照抄，x^k 中的 k 由 λ 是否为特征根决定。Q_m(x) 取 P_m(x) 的一般多项式——按最高次数从高到低把所有低次项写全（常数→A；一次→Ax+B；二次→Ax²+Bx+C）。这是选择、填空的高频考点，只要求「设出」形式。易错点——P_m(x)=x² 时不能只写 ax²，必须补上 bx+c。
- **关键概念**：`Q_m(x)`、`x^k`、`待定系数`、`同次一般式`
- **出处**：[陈哥 P116](https://www.bilibili.com/video/BV1husGzwEtZ?p=116)；[杰哥 P149](https://www.bilibili.com/video/BV1Up4y1Y76a?p=149)、[P150](https://www.bilibili.com/video/BV1Up4y1Y76a?p=150)；[ok姐 P82](https://www.bilibili.com/video/BV1vm421s7mv?p=82)

### k 的确定：λ 与特征根的关系
- **要点**：先把非齐次方程对应的齐次特征方程解出 r₁,r₂：若 λ（或 α）不是特征根，k=0；若 λ 等于其中一个单根，k=1；若 λ 等于二重根，k=2。k 相当于「共振次数」，是设 Y* 时最容易出错的一步，故须先解特征方程求根。
- **关键概念**：`λ`、`特征根`、`k=0/1/2`
- **相互关系**：易错点是把它与自由项多项式次数混淆，二者无关。
- **出处**：[陈哥 P116](https://www.bilibili.com/video/BV1husGzwEtZ?p=116)；[杰哥 P150](https://www.bilibili.com/video/BV1Up4y1Y76a?p=150)；[ok姐 P82](https://www.bilibili.com/video/BV1vm421s7mv?p=82)

### 特解的叠加原理
- **要点**：当 f(x) 由多个不同形式相加组成时，可拆成若干单项分别设出各自的 Y_i*，再把它们相加得到总的 Y*；各部分的待定字母要用不同符号以示区分。
- **关键概念**：`叠加原理`、`拆分 f(x)`、`分别设解`
- **相互关系**：是单一项情形的推广，常用于自由项为「多项式 + 指数」的题。
- **出处**：[陈哥 P116](https://www.bilibili.com/video/BV1husGzwEtZ?p=116)

### 待定系数法求参数
- **要点**：把设出的 Y* 及其一阶、二阶导数代回原非齐次方程，约去公共的 e\^\{λx\}，按 x 的幂次从高到低合并同类项，再与原方程右边对比同次幂系数，解出待定常数。整理时先看高次项（常自动消去），再看一次项与常数项。卷面书写规范：把冗长的代入过程写在草稿上，卷面只写「将 y* 代入原方程得 a=…、b=…，故 y*=…」，最后写「非齐次通解 y=ȳ+y*」。
- **关键概念**：`代入`、`对比系数`、`求导`、`卷面书写`
- **相互关系**：易错点——求 Y* 的导数时漏项；Y* 含 x^k 时求导后次数升高，需仔细合并。
- **出处**：[陈哥 P117](https://www.bilibili.com/video/BV1husGzwEtZ?p=117)；[杰哥 P152](https://www.bilibili.com/video/BV1Up4y1Y76a?p=152)

### 非齐次方程特解的设法（第一类）与完整求解流程
- **要点**：当 f(x)=e\^\{λx\}P_m(x) 时，设特解 y*=x^k P_m(x)e\^\{λx\}，三部分各有来源：k 由 λ 是不是特征根决定（λ 不是特征根时 k=0；λ 是特征方程的单根时 k=1；λ 是特征方程的重根时 k=2）；P_m(x) 由原式右端决定（原式里没有含 x 的因子时 m=0、这一部分就用一个常数如 a 代，有 x 倍时 m=1、设成 ax+b 这种与 x 有关的函数）；λ 则取 e 的脑袋上 x 前面的那个系数。做题时要一一对应。设出形式后把 y* 代回原方程定出待定系数：由乘积求导得 y*′、y*″，代入并拆括号合并同类项后，含 x 的项互相抵消，只剩含待定常数的项与右端比较即可解出（如得 4ae\^\{x\}=2e\^\{x\} 故 a=½）。最后写出原方程通解 y=Y+y*=齐次通解+该特解。这类题只写特解形式即可、不必求系数时，也必须先解特征方程定出 k。
- **关键概念**：`y*=x^k P_m(x)e^{λx}`、`k=0,1,2`、`单根`、`重根`、`m=0 或 1`、`代回原方程定系数`、`y=Y+y*`
- **相互关系**：k 由 λ 与特征根的关系决定、P_m(x) 由原式右端是否含 x 决定、λ 从原式读取；完整流程是「求齐次通解 → 设特解 → 代回求系数 → 写出通解」，这种方法叫待定系数法。
- **出处**：[学士帽 P103](https://www.bilibili.com/video/BV1X4411J792?p=103)

### 自由项含三角函数的类型
- **要点**：自由项为 e\^\{αx\}[P_m(x)cos βx+Q_n(x)sin βx] 时，设 y*=x^k e\^\{αx\}[R_l(x)cos βx+S_l(x)sin βx]，取 l=max{m,n}，两个多项式都要写全；k 由 α±βi 是否为特征根决定。计算量极大，属了解性内容。
- **关键概念**：`α±βi`、`l=max{m,n}`
- **出处**：[ok姐 P82](https://www.bilibili.com/video/BV1vm421s7mv?p=82)

### 右端含 sin/cos 时的特解形式与例题
- **要点**：当 f(x)=e\^\{λx\}P_m(x)sin βx（或 cos βx）时，设特解 y*=x^k e\^\{λx\}[R₁(x)cos βx+R₂(x)sin βx]。k 由特征根决定：特征根与 λ+βi 相同时 k=1、不同时 k=0（k=0 就没有 x^k 这一项，相当于乘 1）；λ 看原式右端有没有 e 的幂，没有则 λ=0；β 取 sin、cos 里面的系数；R₁(x)、R₂(x) 由右端是否含 x 决定——右端只有 cos βx（不含 x）时两者都设成常数，右端带 x 时（m=1）设成 ax+b 与 cx+d。代入原方程并合并同类项、按对应项系数相等定出各待定常数（如可定出 a=−1/3、b=0、c=0、d=4/9）。即使只要求特解，也必须先求出齐次方程的特征根来确定 k；求导时注意 cos2x、sin2x 是复合函数，内层还要乘 2。
- **关键概念**：`y*=x^k e^{λx}[R₁cos βx+R₂sin βx]`、`λ+βi 与特征根比较`、`k=0 或 1`、`对应项系数相等`
- **相互关系**：是第一类设法的推广，多了 sin、cos 两项；判断 k 时要先求齐次方程的特征根。
- **出处**：[学士帽 P104](https://www.bilibili.com/video/BV1X4411J792?p=104)

### 解的结构类选择题套路
- **要点**：把「解代入方程右端得到什么」当作记账：得到 f(x) 记一个 f，得到 0 记 0；对解做线性组合后按同样规则相加，看结果等于 f(x) 还是 0 来判定它属于哪个方程的解。常用结论：两个非齐次特解相减＝齐次方程的一个特解；两个解相加对应右端 f₁+f₂；齐次特解的线性组合即为齐次通解；齐次通解加一个非齐次特解构成非齐次通解；求非齐次通解时取一已知特解＋两两相减构造的齐次通解。
- **关键概念**：`解的结构`、`线性组合`、`特解相加`
- **出处**：[陈哥 P132](https://www.bilibili.com/video/BV1husGzwEtZ?p=132)；[杰哥 P151](https://www.bilibili.com/video/BV1Up4y1Y76a?p=151)；[米哥 P132](https://www.bilibili.com/video/BV1swAWerEzS?p=132)

### n 阶常系数齐次线性微分方程
- **要点**：方法同二阶，把各阶导换成 r 的对应次幂写出特征方程并求根：实单根对应 Ce\^\{rx\}；k 重根对应 (C₁+C₂x+…+C_k x\^\{k−1\})e\^\{rx\}；复根对应 e\^\{ax\}(cos bx, sin bx) 的组合。低频考点，偶尔出现在个别省份的卷中。
- **关键概念**：`n 阶`、`单根`、`k 重根`
- **出处**：[杰哥 P153](https://www.bilibili.com/video/BV1Up4y1Y76a?p=153)

### 变限积分函数型方程（一阶）
- **要点**：题干给出含 ∫_0^x f(t)dt 的恒等式时，先两边对 x 求导化为微分方程（变限积分求导法则：上限代入被积函数乘上限导数，减去下限代入乘下限导数）；若被积函数中混有与积分变量无关的 x，必须先用换元 x−t=u 或把 x 提到积分号外，否则不能直接求导。初始条件由令 x 等于积分下限（上下限相同使积分为零）得到。
- **关键概念**：`变限积分函数`、`求导法则`、`换元 x−t=u`、`隐含初始条件`
- **相互关系**：常与一阶线性方程结合，是近年常见的综合题型。
- **出处**：[陈哥 P112](https://www.bilibili.com/video/BV1husGzwEtZ?p=112)、[P117](https://www.bilibili.com/video/BV1husGzwEtZ?p=117)

### 微分方程与变限积分的综合题
- **要点**：给出含变限积分的等式求 f(x)：①对等式两边求导化为一阶微分方程（若一阶导式中仍含变限积分，再求导一次得二阶方程）；②解微分方程求通解；③题目通常不给初值条件，把 x 等于积分下限的值代入原等式及求导后的等式，得初值条件；④代回通解求特解。求特解时注意利用题目条件（如「非负函数」）取舍正负号。与曲线积分结合时，由「积分与路径无关」得到两个偏导相等，从而导出含 f 与 f′ 的微分方程。
- **关键概念**：`两边求导`、`初值条件`、`隐式通解`、`特解`
- **出处**：[ok姐 P74](https://www.bilibili.com/video/BV1vm421s7mv?p=74)、[P81](https://www.bilibili.com/video/BV1vm421s7mv?p=81)；[杰哥 P145](https://www.bilibili.com/video/BV1Up4y1Y76a?p=145)

### 变限积分函数型方程（二阶）
- **要点**：含变限积分的恒等式两边连续求导两次，可化为二阶非齐次线性方程，再按「齐次通解 + Y*」求解。此类题通常隐含两个初始条件：一个由题干中令 x 等于积分下限得到，另一个由第一次求导后的式子令 x 等于下限得到；若被积函数含 x，须先换元或把 x 提出积分号再求导。
- **关键概念**：`两次求导`、`隐含初始条件`、`变限积分`
- **相互关系**：与一阶同类题思路一致，只是多一次求导、多一个初始条件。
- **出处**：[陈哥 P117](https://www.bilibili.com/video/BV1husGzwEtZ?p=117)

### 应用题型：切线斜率与曲线方程
- **要点**：题目给出「曲线上任意点处切线斜率为某式」，即得 y′ 等于该式，从而构成微分方程；「曲线过某点」即初始条件。求出通解后代入该点得特解，即所求曲线方程。
- **关键概念**：`切线斜率`、`导数`、`初始条件`
- **出处**：[陈哥 P112](https://www.bilibili.com/video/BV1husGzwEtZ?p=112)


### 微分方程的概念
- **要点**：含有未知函数的导数或微分的方程叫微分方程。它与普通方程的区别在于：普通方程解出来是一个数值，微分方程解出来是一个函数。速度是路程的一阶导、加速度是路程的二阶导，所以「加速度为定值」这句话本身就是微分方程。
- **关键概念**：`微分方程`、`含导数或微分的方程`、`解出来是函数`
- **相互关系**：微分与导数只是同一个东西的两种写法（乘积形式与商的形式），所以「含微分」与「含导数」是一回事；微分方程是研究函数与导数关系的工具，因为直接找函数关系往往很难。
- **出处**：[石头 P87](https://www.bilibili.com/video/BV18CL26WEJ3?p=87)

### 微分方程的解、通解与特解
- **要点**：代入微分方程后能使方程成立的函数叫微分方程的解。含任意常数 $C$ 的解叫通解，它就是全体原函数；把常数 $C$ 确定下来后得到的那一个函数叫特解。通解中任意常数 $C$ 的个数必须与微分方程的阶数相同。
- **关键概念**：`解`、`通解`、`特解`、`任意常数 $C$ 的个数与阶数相同`
- **相互关系**：只带一个 $C$ 的二阶方程函数既不是通解也不是特解，只能叫「解」；求特解的办法是先求通解再代入初始条件。
- **出处**：[石头 P87](https://www.bilibili.com/video/BV18CL26WEJ3?p=87)

### 微分方程的阶
- **要点**：微分方程的阶就是方程中出现的未知函数最高阶导数的阶数，数出最高阶即可。四阶及以上导数写成 $y\^\{(n)\}$ 的形式，注意 $y'\^\{\,4\}$ 表示一阶导的四次方而不是四阶导，$y'''$ 才是三阶导。
- **关键概念**：`阶`、`最高阶导数`、`$y^{(n)}$`、`$y'^{\,4}$`
- **相互关系**：阶数决定通解中 $C$ 的个数，是判断通解、特解选择题的关键；「几阶导」与「几次方」的写法区别是常见陷阱。
- **出处**：[石头 P87](https://www.bilibili.com/video/BV18CL26WEJ3?p=87)

### 线性与非线性微分方程
- **要点**：判断时只看 $y$、$y'$、$y''$，不看 $x$。若这些量彼此相乘（如 $yy'$、$y'^2$、$y'y''$），或出现关于它们的复合函数（如 $\sin y$、$\cos y'$、$e\^\{y'\}$、$\frac1y$），就是非线性；否则为线性，此时 $y$ 前的系数只能是常数或关于 $x$ 的函数。
- **关键概念**：`线性微分方程`、`非线性微分方程`、`$yy'$`、`$\sin y$`
- **相互关系**：这一区分是判断「二阶线性微分方程」类选择题的必需步骤，要与「二阶」一起检验；含 $x$ 的复合（如 $\sin x$）不影响线性。
- **出处**：[石头 P87](https://www.bilibili.com/video/BV18CL26WEJ3?p=87)

### 可分离变量微分方程的判定
- **要点**：能把含 $y$ 与 $\mathrm{d}y$ 的部分全放到一边、含 $x$ 与 $\mathrm{d}x$ 的部分全放到另一边，这样的方程就是可分离变量微分方程。若某一边出现同时含 $x$ 与 $y$ 的加减式子（如 $(x+2y)\mathrm{d}y$），就一定分离不开；若该因子是乘积形式，可两边同时除以它消掉。
- **关键概念**：`可分离变量`、`分离到两边`、`乘积可除、加减不可除`
- **相互关系**：可分离变量方程必然是一阶，但既可能是线性也可能是非线性，做题时不必判断线性；只看 $x$ 与 $y$ 是否被加减绑在一起。
- **出处**：[石头 P88](https://www.bilibili.com/video/BV18CL26WEJ3?p=88)

### 可分离变量方程的三步解法
- **要点**：第一步分离变量，把方程整理成一边只含 $y$、一边只含 $x$ 的形式；第二步两边同时求不定积分；第三步求出原函数并写通解，两个积分常数合并成一个 $C$。一阶方程的通解中只有一个 $C$。
- **关键概念**：`三步解法`、`分离变量`、`两边同时求不定积分`、`写通解`
- **相互关系**：不要写成两个 $C$，任意常数相减仍是任意常数，合并成一个即可；分离时两边同时除以因子是最常用的操作。
- **出处**：[石头 P88](https://www.bilibili.com/video/BV18CL26WEJ3?p=88)

### 对数结果的化简与两边同时取 e
- **要点**：积分结果出现 $\ln$ 时考试要求化简：先把两个对数合并成 $\ln$ 内相乘，再两边同时取 $e$，用恒等式 $e\^\{\ln M\}=M$ 去掉对数，$e^C$ 仍是任意常数，可再记作 $C$。常用公式为 $\int\frac{1}{\square}\mathrm{d}\square=\ln|\square|+C$、$\ln M+\ln N=\ln(MN)$、$e\^\{M+N\}=e^M\cdot e^N$。
- **关键概念**：`两边同时取 e`、`$e^{\ln M}=M$`、`$\ln M+\ln N=\ln(MN)$`、`$e^C$ 记作 $C$`
- **相互关系**：脱去对数后绝对值符号就可以去掉；这一步不做会被扣分，是微分方程与不定积分题目在格式上的重要差别。
- **出处**：[石头 P88](https://www.bilibili.com/video/BV18CL26WEJ3?p=88)

### 由通解求特解
- **要点**：题目给出初始条件求特解时，先按三步求出通解，再把初始条件代入通解解出 $C$，最后把 $C$ 写回通解即得特解。
- **关键概念**：`特解`、`初始条件`、`先求通解再代值`
- **相互关系**：与微分方程解的概念中通解、特解的区分一致；代值前务必先把通解化到最简，否则解 $C$ 时容易出错。
- **出处**：[石头 P88](https://www.bilibili.com/video/BV18CL26WEJ3?p=88)

### 齐次微分方程的定义与判定
- **要点**：能写成 $\frac{\mathrm{d}y}{\mathrm{d}x}=f\!\left(\frac{y}{x}\right)$ 形式的一阶微分方程叫齐次微分方程，即右端整体可表示为 $\frac{y}{x}$ 的函数，等价于分子分母中 $x$ 与 $y$ 的次数相同。若未写成标准形式，可看 $\mathrm{d}x$、$\mathrm{d}y$ 前的两个多项式是否同为齐次（$x^2$、$y^2$、$xy$ 都是二次）。
- **关键概念**：`齐次微分方程`、`$\frac{\mathrm{d}y}{\mathrm{d}x}=f\!\left(\frac{y}{x}\right)$`、`次数相等`、`齐次多项式`
- **相互关系**：这里的「齐次」指次数齐，与一阶线性微分方程中「自由项为零」的齐次含义完全不同，切勿混淆；齐次方程只能是一阶，且不必判断线性与否。
- **出处**：[石头 P89](https://www.bilibili.com/video/BV18CL26WEJ3?p=89)

### 齐次微分方程的换元解法
- **要点**：令 $u=\frac{y}{x}$，则 $y=xu$，由乘积求导得 $\frac{\mathrm{d}y}{\mathrm{d}x}=u+x\frac{\mathrm{d}u}{\mathrm{d}x}$。把它代回原方程后 $u$ 通常与右端的 $u$ 消掉，剩下可分离变量方程，再按分离变量三步求解，最后把 $u$ 换回 $\frac{y}{x}$。
- **关键概念**：`换元`、`$u=\frac{y}{x}$`、`$\frac{\mathrm{d}y}{\mathrm{d}x}=u+x\frac{\mathrm{d}u}{\mathrm{d}x}$`、`换回 $u=\frac{y}{x}$`
- **相互关系**：换元这一步是固定的，可直接照抄；解完必须把 $u$ 还原成 $\frac{y}{x}$，否则不算完成，它本质上是把齐次方程化为可分离变量方程。
- **出处**：[石头 P89](https://www.bilibili.com/video/BV18CL26WEJ3?p=89)

### 一阶线性微分方程的标准形式与分类
- **要点**：能化成 $y'+P(x)y=Q(x)$ 的方程叫一阶线性微分方程，其中 $P(x)$、$Q(x)$ 只含 $x$，且 $y'$ 前的系数必须是 $1$，不是 $1$ 就先两边同除。$Q(x)$ 称为自由项：$Q(x)\not\equiv0$ 时是非齐次线性方程，$Q(x)\equiv0$ 时是齐次线性方程。
- **关键概念**：`$y'+P(x)y=Q(x)$`、`自由项`、`齐次线性`、`非齐次线性`
- **相互关系**：这里的「齐次」指自由项为零，与齐次微分方程中「次数齐」的含义不同；标准形式中 $y'$ 的系数为 $1$ 是套公式不出错的前提。
- **出处**：[石头 P90](https://www.bilibili.com/video/BV18CL26WEJ3?p=90)

### 一阶线性微分方程的通解公式
- **要点**：直接套公式 $y=e\^\{-\int P(x)\mathrm\{d\}x\}\left[\int Q(x)e\^\{\int P(x)\mathrm\{d\}x\}\mathrm{d}x+C\right]$，式中含三个不定积分号，顺序是「左边负 $P$、中间 $Q$、右边正 $P$」。齐次线性方程（$Q(x)\equiv0$）代入后化为 $y=Ce\^\{-\int P(x)\mathrm\{d\}x\}$。
- **关键概念**：`通解公式`、`$e^{-\int P\mathrm{d}x}$`、`$\int Qe^{\int P\mathrm{d}x}\mathrm{d}x$`、`三个积分号`
- **相互关系**：公式对非齐次与齐次都适用，区别只在 $Q$ 是否为零；套公式前必须先化成标准形式，否则 $P$、$Q$ 都会取错。
- **出处**：[石头 P90](https://www.bilibili.com/video/BV18CL26WEJ3?p=90)

### 一阶微分方程的方法选择
- **要点**：拿到一阶方程先看能否直接分离变量，能就直接用分离变量法；不能直接分离但可先换元再分离，就用齐次方程的换元法（令 $u=\frac{y}{x}$）；若根本无法分离，就直接套一阶线性微分方程的通解公式。
- **关键概念**：`方法选择`、`可分离变量法`、`换元法`、`公式法`
- **相互关系**：同一方程若多种方法都可用，选计算量最小的；公式法虽然万能但计算繁，分离变量法优先。
- **出处**：[石头 P90](https://www.bilibili.com/video/BV18CL26WEJ3?p=90)

### 二阶常系数线性微分方程的形式与分类
- **要点**：形如 $y''+py'+qy=f(x)$ 的方程叫二阶常系数线性微分方程，其中 $y''$ 的系数必须为 $1$，$p$、$q$ 为常数，且 $y''$、$y'$、$y$ 之间不能相乘，也不能出现关于它们的复合函数。$f(x)$ 为自由项，$f(x)\equiv0$ 时为齐次，否则为非齐次。
- **关键概念**：`$y''+py'+qy=f(x)$`、`常系数`、`自由项 $f(x)$`、`齐次与非齐次`
- **相互关系**：限定条件越多、范围越窄、题目越简单；与一阶线性微分方程的唯一区别是「常系数」，即 $y$ 前系数只能是常数而不能是 $x$ 的函数。
- **出处**：[石头 P91](https://www.bilibili.com/video/BV18CL26WEJ3?p=91)

### 齐次方程解的结构与线性无关
- **要点**：若 $y_1$、$y_2$ 是 $y''+py'+qy=0$ 的两个特解，则 $y=C_1y_1+C_2y_2$ 也是解；若 $y_1$、$y_2$ 线性无关，则 $y=C_1y_1+C_2y_2$ 就是通解。判断线性无关看比值 $\frac{y_1}{y_2}$：比值为常数则线性相关，不为常数则线性无关。
- **关键概念**：`解的结构`、`线性相关`、`线性无关`、`$\frac{y_1}{y_2}$ 是否为常数`
- **相互关系**：只有两个线性无关的特解相加才能构成通解，线性相关的两个特解相加后 $C$ 会合并成一个，只能算解；二阶方程的通解必须含两个 $C$。
- **出处**：[石头 P91](https://www.bilibili.com/video/BV18CL26WEJ3?p=91)

### 共轭复根与三种情况下的通解
- **要点**：$\Delta>0$ 时为两个不等实根，通解 $y=C_1e\^\{r\_1x\}+C_2e\^\{r\_2x\}$；$\Delta=0$ 时为两个相等实根 $r$，通解 $y=(C_1+C_2x)e\^\{rx\}$；$\Delta&lt;0$ 时为一对共轭复根 $\alpha\pm\beta i$，通解 $y=e\^\{\alpha x\}(C_1\cos\beta x+C_2\sin\beta x)$。共轭复根处规定虚数单位 $i=\sqrt{-1}$，$\alpha+\beta i$ 与 $\alpha-\beta i$ 关于实轴对称，$\alpha$ 为实部、$\beta$ 为虚部，负数开方写成 $\sqrt{-a}=\sqrt{a}\,i$。
- **关键概念**：`三种情况`、`$e^{\alpha x}(C_1\cos\beta x+C_2\sin\beta x)$`、`共轭复根`、`$i=\sqrt{-1}$`、`实部与虚部`
- **相互关系**：第三种情况最易记错，注意 $\alpha$ 在指数上、$\beta$ 在三角函数里；前两种情况不出现 $\cos$、$\sin$。
- **出处**：[石头 P91](https://www.bilibili.com/video/BV18CL26WEJ3?p=91)

### 非齐次方程解的结构
- **要点**：设 $y^*$ 是 $y''+py'+qy=f(x)$ 的一个特解（非齐特），$Y$ 是它对应的齐次方程 $y''+py'+qy=0$ 的通解（齐通），则非齐次方程的通解为 $y=Y+y^*$，即「非齐通＝齐通＋非齐特」。
- **关键概念**：`非齐通＝齐通＋非齐特`、`非齐特 $y^*$`、`齐通 $Y$`
- **相互关系**：这一结构决定了非齐次题的解题顺序是先求齐通、再求非齐特；它与一阶线性微分方程解的结构是同一思想。
- **出处**：[石头 P92](https://www.bilibili.com/video/BV18CL26WEJ3?p=92)

### 叠加原理
- **要点**：若 $y_1^*$ 是自由项为 $f_1(x)$ 的方程的特解、$y_2^*$ 是自由项为 $f_2(x)$ 的方程的特解，则 $y_1^*+y_2^*$ 是自由项为 $f_1(x)+f_2(x)$ 的方程的特解。自由项是幂函数与三角函数之和（如 $x^2+\sin x$）时，就按叠加原理拆成两个方程分别求特解再相加。
- **关键概念**：`叠加原理`、`$y_1^*+y_2^*$`、`自由项拆分`
- **相互关系**：只适用于两个自由项相加的情形，且两个方程左端系数必须完全相同；它把第一种类型与第二种类型衔接起来。
- **出处**：[石头 P92](https://www.bilibili.com/video/BV18CL26WEJ3?p=92)、[P93](https://www.bilibili.com/video/BV18CL26WEJ3?p=93)

### 自由项的第一种类型与解题步骤
- **要点**：第一种类型为 $f(x)=e\^\{\lambda x\}P_m(x)$，其中 $P_m(x)$ 是 $m$ 次多项式（考试最多二次）。特解设为 $y^*=e\^\{\lambda x\}Q_m(x)x^k$：$e\^\{\lambda x\}$ 照抄；$Q_m(x)$ 是与 $P_m(x)$ 同次的多项式，系数要从最高次往下写满（$P_m$ 为常数设 $A$，一次设 $Ax+B$，二次设 $Ax^2+Bx+C$）；$k$ 由 $\lambda$ 是否为特征根确定，不是特征根取 $k=0$、是单根取 $k=1$、是重根取 $k=2$。四步流程为求特征根、设特解、定 $k$、解待定系数（求出 $y\^\{*\prime\}$、$y\^\{*\prime\prime\}$ 代回原方程，比较 $x$ 的同次幂系数求解）。
- **关键概念**：`$f(x)=e^{\lambda x}P_m(x)$`、`$y^*=e^{\lambda x}Q_m(x)x^k$`、`$Q_m(x)$ 从最高次写满`、`$k=0,1,2$`、`待定系数`
- **相互关系**：多项式必须从最高次写满，原式缺项也要保留待定系数；定 $k$ 只看 $\lambda$ 与特征根的关系，与多项式次数无关。
- **出处**：[石头 P92](https://www.bilibili.com/video/BV18CL26WEJ3?p=92)

### 自由项的第二种类型与解题要点
- **要点**：第二种类型为 $f(x)=e\^\{\lambda x\}[P\cos\omega x+Q\sin\omega x]$，其中 $P$、$Q$ 一般为常数。特解设为 $y^*=e\^\{\lambda x\}(A\cos\omega x+B\sin\omega x)x^k$，$A$、$B$ 为待定系数；即使原式只出现 $\cos$ 或只出现 $\sin$，也要把两项都写全。定 $k$ 改看 $\lambda\pm\omega i$ 是否为特征根：不是特征根取 $k=0$，是特征根取 $k=1$（绝大多数题取 $0$）。若 $\cos$、$\sin$ 前是多项式，则取两者中次数最高的次数，写成两个同次多项式。
- **关键概念**：`$e^{\lambda x}[P\cos\omega x+Q\sin\omega x]$`、`$y^*=e^{\lambda x}(A\cos\omega x+B\sin\omega x)x^k$`、`$\lambda\pm\omega i$`、`sin 与 cos 写全`
- **相互关系**：这里的 $\lambda\pm\omega i$ 与二阶齐次中 $\alpha\pm\beta i$ 的形式一致，是同一套结构；与第一种类型的区别只在特解的第二部分和定 $k$ 的依据，其余四步完全相同。
- **出处**：[石头 P92](https://www.bilibili.com/video/BV18CL26WEJ3?p=92)、[P93](https://www.bilibili.com/video/BV18CL26WEJ3?p=93)

### 特解选择题的反代验证技巧
- **要点**：选择题问「特解可设为什么」时，只需按类型写出特解形式、定出 $k$ 即可判断；问「哪个是特解」时，把选项代入原方程验证比正着求待定系数快得多。还可先按右边多项式的次数推断 $y$ 的次数：右边是二次多项式，则 $y$ 必为三次，据此直接排除两个选项。
- **关键概念**：`反代验证`、`次数推断`、`排除法`、`特解形式`
- **相互关系**：同一道题正着算要写很长的二阶导，反着代往往一步出结果；若选项缺 $\cos$ 或缺 $\sin$，可先按「两项必须写全」排除。
- **出处**：[石头 P92](https://www.bilibili.com/video/BV18CL26WEJ3?p=92)、[P93](https://www.bilibili.com/video/BV18CL26WEJ3?p=93)


