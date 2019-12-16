---
layout: post
comments: true
title: "电化学"
categories: "化学"
---

### 标准电极电势

#### 氢标准电极

3个条件缺一不可：$298 \mathrm{K}, p(\mathrm{H}_2) = 100 \mathrm{kPa}, c(\mathrm{H}^{+}) = 1 \mathrm{mol / L}$ 

向涂有铂黑（极细的Pt粉）的铂电极上面持续通入氢气，这样的电极叫做氢标准电极

产生的还原电位定为标准电位0V
并不是不发生反应，只是相对值

标准电极电势的代数值：越大则氧化性越强，越小则还原性越强
记住两端：$\mathrm{Li^{+} / Li}$ 最负，$\mathrm{F_2 / F^{-}}$ 最正

#### 和平衡常数的关系

van't Hoff 等温方程：$\Delta G - \Delta G^{\Theta} = RT \ln Q$

恒温恒压条件下，体系吉布斯自由能降低等于体系能做的最大非体积功。
由于 

$$
W' = \Delta G = -n N_A e E = -nFE
$$

（系统对外做功，取负号）

$$
-nEF + nE^{\Theta}F = RT \ln Q
$$

由此我们得到 Nernst 方程：

$$
E = E^{\Theta} - \frac{RT \ln Q}{nF}
$$

用标准电极电势求平衡常数：$E = 0, Q = K^{\Theta} \Rightarrow K^{\Theta} = \exp \left(\frac{nFE^{\Theta}}{RT}\right) $

$\mathrm{E_{池}} \geq 0.2 \mathrm{V} \Leftrightarrow K^{\Theta} \geq 10^{7} \Leftrightarrow \text{反应较为完全}$

由上式可知

- 标准电极电势对于分步反应不满足加和性质，不能进行类似盖斯定律的处理
  
  （但是 $n\mathrm{E}$ 满足！）

- 反应式加倍，标准电极电势不变

- $E_{池} = E_+ - E_-$ 可以用来判断氧化还原反应的自发性
  
  - $\geq 0$ 自发
  
  - $=0$ 平衡
  
  - $\leq 0$ 非自发（逆反应自发）

#### 电极电势的 Nernst 方程式

考虑反应：

$$
m \; \mathrm{ox} + n \; e^{-} \rightleftharpoons s \; \mathrm{red}
$$

则根据上述方程有：

$$
E = E^{\Theta} - \frac{RT \ln Q}{nF}\\
= E^{\Theta} - \frac{RT}{nF} \ln \frac{\mathrm{(red)}^s}{\mathrm{(ox)}^m}
$$

注意：red -> reducing state, ox -> oxidizing state

### $\mathrm{H^{+}}$ 浓差电池

$$
(+)\mathrm{Pt} \mid \mathrm{H_2} (p^\Theta) \mid \mathrm{H^+} (c_1) \parallel \mathrm{H^+} (c_2) \mid \mathrm{H_2}(p^\Theta) | \mathrm{Pt} (-)
$$

 其中 $c_1$ 为已知。则可以根据 Nernst 方程推算出待测溶液中的 $c_2$.

### 标准电极电势与氧化还原反应条件

对于同一种物质，酸碱性条件不同，标准电极电势不同，氧化还原能力亦有差异。

### 参比电极

#### 饱和甘汞电极

$$
\mathrm{Hg_2Cl_2(s) + 2e^{-} \rightleftharpoons 2Hg(l) + 2Cl^- (aq)}
$$

$E^{\ominus} = 0.2415 \text{V}$

#### 玻璃电极

另一种参比电极。采用只能透过 $\mathrm{H^{+}}$ 的玻璃制成。



### 应用

#### 以电极电势判断还原性

标准电极电势：标准状态（ $p^{\ominus},c^{\ominus}$ ）下，相应电对和氢标准电极组成原电池，由此列出 $E_{池}=E_+ - E_-$，进而根据已知的一个电极电势计算未知电极的电极电势。显然计算的时候应该适当选择正负极，使得电池电动势非负。

标准电极电势可以用于还原性的判断。根据其含义，其代指的是还原电势。标准电极电势大于0，说明其与氢电极组成电池后做正极，其还原性弱于氢电极，极端的例子是 $\mathrm{F_2 / F^-}$；标准电极电势小于0，说明其与氢电极组成电池后做负极，其还原性强于氢电极，极端的例子是 $\mathrm{Li^+ / Li}$.

用平衡移动的观点可以进行电极电势定性比较。考虑反应 $\mathrm{H^+ + e^- \rightarrow \frac{1}{2}H_2}$. 如果增大氢离子的量，则平衡向右移动，夺取电子能力增强，还原性减弱，标准电极电势上升；减少氢离子的量，则平衡向左移动，夺取电子能力减弱，失去电子的能力即相应增强，还原性增强，标准电极电势下降。

#### Nernst方程的应用

对于单个电极的反应，一般不转为自由能（因为式子中有电子，以自由能加以计算很不方便），而是采用 Nernst 方程进行标准状态和实际状态之间电极电势的计算。计算时要明确反应的方向。由于电极电势几乎都是由还原电势的形式给出，一律要使用得电子的反应式进行计算。切不可把浓度商 $Q$ 求成其倒数。同时，反应式和方程中转移电子数目要对应。

### 与 Gibbs 自由能 / 标准平衡常数的关系

对于*完整的原电池*，适宜使用 $\Delta G^\ominus = -NEF$，其中 $N$ 为总反应式中转移电子数目，$E$ 为原电池的电动势。注意一定要有负号！

### 例题

来源：普通化学原理

- 生物中常常以 $\mathrm{pH=7}$ 为标准状态，并用 $\Delta G^{\ominus'}, E^{\ominus'}$ 代替 $\Delta G^{\ominus}, E^{\ominus}$ 等。

  $\mathrm{NAD^+ + H^+ + 2e \rightarrow NADH \;\;\; E^{\ominus} = -0.11V}$  求对应的 $E^{\ominus'}$.

  分析：对象是电极反应，而非原电池；如果我们选定化学里的标准状态，则生物的标准状态实质上是氢离子浓度发生了变化。直接采用 Nernst 方程。

- 实验测得 $\mathrm{0.10 \; mol\cdot dm^{-3} \; HX}$ 的氢电极（$p^{\ominus}$）与饱和甘汞电极组成电池，电势为 $\mathrm{0.48 \; V}$，求该酸电离常数。


  分析：可以采用分类讨论正负极的方法。但是，如果可以的话，最好把正负极确定下来。溶液中的氢离子浓度显然小于标准态；浓度小，氢离子被还原的反应平衡左移，难夺取电子，还原性增强，电极电势降低，故其电极电势为负数；而饱和甘汞电极电极电势为正。由此可确定正负极。再利用 Nernst 方程列式算出对应氢离子浓度即可。

- 向 $\mathrm{0.200\; mmol \; AgCl(cr)}$ 中加入少量水和过量锌粉，使得总体积为 $2 \mathrm{\;mL}$. 计算说明，锌粉能否把氯化银全部还原成银单质。
  分析：所谓完全反应，实际上还是要看标准平衡常数，而不是计算平衡状态。首先，反应是绝对的，不反应是相对的；完全性，自然也是相对而言的。而要看 $\mathrm{K^{\ominus}}$，就要看相应的标准 Gibbs 自由能，以及相应的标准电动势。查表找出 $\mathrm{AgCl/Ag}$ 以及 $\mathrm{Zn^{2+}/Zn}$ 之标准电极电势，相减即可。

- 电解 $\mathrm{[H^+] = 1 \; mol \cdot L^{-1}}$ 的 $\mathrm{H_2 SO_4}$ 溶液，阳极放出 $\mathrm{O_2}(p^{\ominus})$，阴极放出 $\mathrm{H_2}(p^{\ominus})$.

  利用以下资料计算理论分解电势。
$$
  \begin{align*}
  \mathrm{2H^{+} + 2e }&\rightarrow\mathrm{H_2} &\mathrm{ E^{\ominus}} &= \mathrm{0.00\; V}\\
  \mathrm{H_2 O + \frac{1}{2}O_2 + 2e} &\rightarrow \mathrm{2 OH^-} &\mathrm{ E^{\ominus}} &= \mathrm{+0.40\; V}
  \end{align*}
$$

分析：并不需要把氧气的还原产物换算成 $\mathrm{H^+}$！只需要使用水的离子积算出硫酸中的 $\mathrm{[OH^-]}$ 即可。

 

  