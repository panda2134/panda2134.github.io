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
m \: \mathrm{ox} + n \: e^{-} \rightleftharpoons s \: \mathrm{red}
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

## 参比电极

#### 饱和甘汞电极

$$
\mathrm{Hg_2Cl_2(s) + 2e^{-} \rightleftharpoons 2Hg(l) + 2Cl^- (aq)}
$$

#### 玻璃电极

咕咕
