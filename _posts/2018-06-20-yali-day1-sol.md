---
layout: post
comments: true
title: "湖南省队雅礼集训Day1题解"
category:
  - 解题报告
tags:
  - 倍增LCA
  - 树链剖分
  - 多项式
  - FFT
  - 倍增
  - 凸包
  - 单调栈
  - 斜率优化
---

风格有点像 NOI2017，有送分题，但是并不很好写（不过似乎比去年 day2 游戏好写？）

今天发挥还不错，争取把分数稳定下来。

## Tree

对于操作 1 ，用一个变量记录。

对于操作 2 ，对两点在原树上 $\text{lca}$ 的位置进行讨论。不妨设之为 $\text{lca_0}$ 。

分为以下情况：

1. $\text{lca}$ 在新根 $\text{rt}$ 与 $1$ 的路径上
2. $\text{lca}$ 在新根的子树里
3. $\text{lca}$ 在除了上述之外的地方

对于 $1$ 我们**可以用 $\textbf{lca(rt, lca}_0 \textbf{)= lca_o}$ 加以判定** ；

对于 $2$ 可以直接用 $\text{dfs}$ 序判断。

注意：

1. 初始根为 $1$
2. 注意特判 $\text{rt, lca}_0$ 是否重合

## Or

有一个显然的DP就是，如果设状态 $dp[i][j]$ 表示考虑长度为 $i$ 的序列 $B_i$ 含有 $j$ 个 $1$ ，那么就有：

$$
\begin{equation*}
dp[i][j] = j! \cdot \sum_{k=1}^j \frac{1}{k!} \cdot \frac{\sum_{p=0}^{j-k}\binom{j-k}{p} \cdot dp[i-1][j-k]}{(j-k)!}
\end{equation*}
$$

而由 $\sum_{i=1}^n \binom{n}{i} = 2^n$ 这个结论可以立刻知道：
$$
\begin{equation*}
dp[i][j]
= j! \cdot \sum_{k=1}^j \frac{1}{k!} \cdot \frac{2^{j-k} \cdot dp[i-1][j-k]}{(j-k)!}
\end{equation*}
$$
考场写的暴力 NTT 是 $O(nk\lg k)$ 的，可以获得 $59$ 分。

考虑使用指数生成函数：
$$
\begin{align*}
F_i(x)[j] = \frac{dp[i][j]}{j!}
&= \sum_{k=1}^j \frac{1}{k!} \cdot \frac{2^{j-k} \cdot dp[i-1][j-k]}{(j-k)!} \\
F_i(x) &= F_{i-1}(2x) \times (e^x - 1)\\
F_n(x) &= F_{n-1}(2x) \times (e^x - 1) \\
&= F_{n-2}(4x) \times (e^{2x}-1) \times (e^x - 1) \\
&= \dots \\
&= F_{n-n}(2^n x) \times \prod_{i=0}^{n-1} (e^{2^i x} - 1) \\
&= \prod_{i=0}^{n-1} (e^{2^i x} - 1)
\end{align*}
$$
这可以用类似普通快速幂的倍增方法求出。即：
$$
F_n(x) = F_{ n/2 }(x) \times F_{ n/2 } (2^{ n/2 } x) \:\:\:(x \text{ even})
$$
对于 $n$ 为奇数的情况暴力算一次就好了。

这样递归为什么就可以解决问题呢？$e^{2^i x}-1$ 到哪儿去了？在递归边界 $n = 1$ 里！

时间复杂度为 $O(k \lg n \lg k)$，可以通过。