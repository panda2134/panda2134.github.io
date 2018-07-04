---
layout: post
comments: true
title: "湖南省队雅礼集训Day3题解"
category:
  - 解题报告
tags:
  - 贪心
  - 数列
  - FFT
  - 分治
  - 多项式
---

## circular

### 题意

有一个长度为 $M$ 的环，环上有 $M$ 个等距离的点，按顺时针顺序依次标号为 $0, 1, 2, \dots, n$.
环上有 $N$ 个线段 $(a_i, b_i) (1 \le i \le n)$. 需要注意的是 $(a_i, b_i)$ 所指的线段是从点 $a_i$ 顺时针延伸
到 $b_i$ 的线段。
小 c 希望知道最多能选多少个不重叠的线段（线段的端点允许重合）。（$n \le 10^5$）

### 思路

考虑贪心。对于链的情况怎么做？以左端点为第一关键字，右端点为第二关键字，从左往右扫。同时维护当前线段右边的所有线段中右端点的最小值。每次转移到右端点最小的线段。

现在把问题放在了环上面，又要如何处理呢？从最短的线段开始断开，往后贪心即可。

（如果能 Hack 掉请评论，谢谢qaq）



## admirable

根号分治+分治 $\text{FFT}$ ，也坑着。

## illustrious

### 题意

$$
\begin{array}{l}
f(n) = \begin{cases}
1 & n = 1 \\
f(n-f(f(n-1)))+1 & n > 1
\end{cases} \\
g(n) = \sum_{i=1}^n f(i) \\
h(n) = h(g(f(n))) - f(f(n)) + g(g(n))
\end{array}
$$

求 $h(n)$. $1 \le n \le 10^9$.

### 思路

神TM OEIS题。$f(n), g(n)$ 在 OEIS 都有。

打表后发现 $f(n)$ 表示 $n$ 这个数字在 $\{f_n\}$ 这一数列中出现几次。

前面几项大概是这样：

$$
1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6,\cdots
$$

这启发我们解读每个函数的组合意义。

$g(n)$ 是 $f(n)$ 的前缀和，表示最后一个 $n$ 在数列中的下标。

$h(n)$ 有点难办，但是我们可以分开看：显然 $g(f(n)) - f(f(n))$ 表示 $f(n)-1$ 这个数字的最后一次出现位置。

于是 $h(n)$ 就是对于数列 $\{f_n\}$ 内的每种数字计算一次贡献。也就是说：

$$
h(n) = g(g(n)) + \sum_{i\text{ is end of a segment in } \{f_n\}, i < n} g(g(i))
$$

再冷静分析一下 $g(g(i))$ 是什么。在连续数学中我们遇到问题常常求导 + 积分解决。显然这个函数是离散的，考虑离散微积分。如何差分？利用 $g(n)$ 的**定义**！

（注意，离散导数定义是 $\Delta f = f(n+1) - f(n)$！类比导数的 $\frac{\mathrm{d}y}{\mathrm{d}x} = \lim\limits_{\Delta x \to 0} \frac{f(x+\Delta x)-f(x)}{\Delta x}$ ！）

$$
\begin{align*}
\Delta \left(g(g(n-1))\right) &= g(g(n)) - g(g(n-1)) \\
&= \sum_{i = g(n-1) + 1}^{g(n)} f_i \\
&= n \times f_n
\end{align*}
\Rightarrow
g(g(n)) =  \sum\nolimits_0^n \Delta(g(g(i))) = \sum\nolimits_0^ni \times f_i
$$

于是 $\{h_n\}$ 就可以递推了。注意处理边界。

直接暴力 $O(n)$ 算只有 50pts. 正解先坑着，明天或者后天更。