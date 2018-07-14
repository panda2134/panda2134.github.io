---
layout: post
comments: true
catalog: true
title: "利用多项式算法优化常系数齐次线性递推"
category: 笔记
tags:
 - FFT
 - 多项式
 - 线性代数
 - 常系数齐次线性递推
---

才听 @Sparky_14145 说这玩意已经是 NOIP 难度辣！为了避免自己没有 NOIP 水平，特来学习。下面若无说明，均有 $n \le 10^9, k \le 10^5$.

强烈推荐 [shadowice1984](https://www.luogu.org/blog/ShadowassIIXVIIIIV/solution-p4723) 的讲解。（老哥稳.jpg）
$$
\newcommand{bm}{\boldsymbol}
$$

## Caylay-Hamilton 定理

### 矩阵的特征值和特征向量

二者以符号 $\lambda, \boldsymbol{\xi}$ 表示. 特征向量一定不是零向量。

特征值和特征向量满足关系：

$$
\boldsymbol{A\xi} = \lambda \boldsymbol{\xi}
$$

即把矩阵对应的线性变换应用到特征向量上，并不会改变其方向。

$$
\begin{align*}
\boldsymbol{IA\xi} &= \lambda \boldsymbol{I\xi}\\
(\boldsymbol{A - I}\lambda) \boldsymbol{\xi} &= \boldsymbol{0}
\end{align*}
$$

如果矩阵不满秩，其行列式一定为0.显然，若要 $\boldsymbol{\xi}​$ 不是 $\boldsymbol{0}​$，系数矩阵必不满秩，则有：

$$
p(\lambda) = \det(\lambda\boldsymbol{I}-\boldsymbol{A}) = 0
$$

上述方程称作特征方程，左式称为特征多项式。

### 定理描述

一个矩阵带入其特征多项式后得到 $\boldsymbol{0}$ 矩阵。

#### 一个例子

考虑矩阵 

$$
\begin{bmatrix}0 & 1 \\ 1 & 1\end{bmatrix}
$$

其特征多项式为 

$$
\det(\lambda\boldsymbol{I}-\boldsymbol{A}) = \det( \begin{bmatrix}\lambda & 0 \\ 0 & \lambda\end{bmatrix}- \begin{bmatrix}0 & 1 \\ 1 & 1\end{bmatrix}) = \begin{vmatrix}\lambda & -1 \\ -1 & \lambda-1\end{vmatrix} = \lambda^2-\lambda-1
$$

把它自己带入其特征多项式有：

$$
\begin{align*}
\begin{bmatrix}0 & 1 \\ 1 & 1\end{bmatrix}^2 - \begin{bmatrix}0 & 1 \\ 1 & 1\end{bmatrix} - \boldsymbol{I} &= \begin{bmatrix}1 & 1 \\ 1 & 2\end{bmatrix} - \begin{bmatrix}0 & 1 \\ 1 & 1\end{bmatrix} - \begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}\\
&= \begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix}
\end{align*}
$$

这就验证了 Caylay-Hamilton 定理。

#### 证明

我们考虑利用特征值的定义式。

如果我们运用算术基本定理，那么就有 $p(x) = \prod (\lambda_i - x)$，其中 $\lambda_i$ 为特征值。

带入矩阵 $\boldsymbol{A}$ 后我们就有 $p(\boldsymbol{A}) = \prod (\lambda_i \boldsymbol{I} - \boldsymbol{A})$.

利用上面所述的特征向量非零性质，转而证明对任意特征向量 $\boldsymbol{\xi_i}$ ，$p(\boldsymbol{A}) \boldsymbol{\xi_i}$ 为零向量。

事实上，有：

$$
\begin{align*}
p(\bm{A}) \bm{\xi_i} &= \left(\prod_{j \ne i} (\lambda_j \bm{I} - \bm{A})\right) \times (\lambda_i \bm{I} - \bm{A}) \bm{\xi_i} \\
&=  \left(\prod_{j \ne i} (\lambda_j \bm{I} - \bm{A})\right) \times (\lambda_i\bm{\xi_i}-\bm{A}\bm{\xi_i})\\
&=  \left(\prod_{j \ne i} (\lambda_j \bm{I} - \bm{A})\right) \times (\bm{A}\bm{\xi_i}-\bm{A}\bm{\xi_i})\\
&= \bm{0}.
\end{align*}
$$

（暴力展开后可以证明这里的括号满足交换律）

于是 $p(\bm{A}) = \bm{0}$，定理立刻得证。

## 优化矩阵快速幂

不妨考虑以下矩阵快速幂的过程：

$$
\begin{bmatrix}g_1 \\ g_2 \\ \vdots \\ g_k\end{bmatrix}^T

\times

\begin{bmatrix}
0 &  &  &  &  & a_1 \\
1 &  &  &  &  & a_2 \\
 & 1 &  &  &  & a_3 \\
 &  & 1 &  &  & a_4 \\
 &  &  &  \ddots &   & \vdots\\
  &  &  &  & 1 & a_k
\end{bmatrix}

= \begin{bmatrix}g_2 \\ g_3 \\ \vdots \\ g_{k+1}\end{bmatrix}^T
$$

我们考察转移用的相伴矩阵的特征多项式：

$$
\begin{align*}
\det(\lambda\bm{I}-\bm{A}) &=
\begin{vmatrix}
\lambda &  &  &  &  & -a_1 \\
-1 & \lambda &  &  &  & -a_2 \\
 & -1 & \lambda &  &  & -a_3 \\
 &  & -1 & \ddots &  & -a_4 \\
 &  &  &  \ddots & \lambda  & \vdots\\
  &  &  &  & -1 & \lambda-a_k
\end{vmatrix}\\
&=
 \begin{vmatrix}
 \lambda &  &  &  &  & -a_1 \\
-1 & \lambda &  &  &  & -a_2 \\
 & -1 & \lambda &  &  & -a_3 \\
 &  & -1 & \ddots &  & -a_4 \\
 &  &  &  \ddots & \lambda  & \vdots\\
  &  &  &  & -1 & \lambda-a_k
\end{vmatrix}^T\\
&= 
\begin{vmatrix}
\lambda - a_k & \cdots & -a_4 & -a_3 & -a_2 & -a_1 \\
-1 & \lambda &  &  &  &  \\
 & -1 & \lambda &  &  &  \\
 &  & -1 & \lambda &  &  \\
 &  &  & \ddots & \ddots &  \\
 &  &  &  & -1 & \lambda \\
\end{vmatrix}\\
&= \lambda^k - \sum_{i=1}^k a_i \lambda^{k-i}.
\end{align*}
$$

最后一步可以考虑把行列式按第一行展开，然后对代数余子式进行化简。化简过程可以考虑高斯消元法。

要优化矩阵快速幂，就是要快速求出 $\bm{A}^n$. 考虑模掉零化多项式，因为显然带入 $\bm{A}$ 后得到零矩阵，对答案没有贡献。

于是可以做一个模特征多项式意义下的矩阵快速幂。这样的复杂度是 $O(k \lg k \lg n)$ 的。

这样就可以把 $\bm{A}^n$ 表示为 $\bm{A}^0 \sim \bm{A}^{k-1}$ 的线性组合，如下（其中 $\bm{V}_0$ 是初始值行向量）：

$$
\begin{align*}
\bm{A}^n &= \sum_{i=0}^{k-1} c_i \bm{A}^i \\
\bm{V}_0\bm{A}^n &= \sum_{i=0}^{k-1}c_i \bm{V}_0 \bm{A}^i
\end{align*}
$$

考虑只取每个行向量的第一项。那么， $g_n = \sum_{i=0}^{k-1}c_i g_i$.

右侧式子中含有 $a_0 \sim a_{k-1}$. 现在唯一的问题就是求出 $a_0 \sim a_{k-1}$. 大多数时候题目都给出了，不过如果题目只给出了 $a_0$，就需要用下面的方法。

问题等价于 $n, k \le 10^5$ 的常系数齐次线性递推。

换个形式：
$$
g_i = \sum_{j=1}^i g_{i-j}a_j
$$
(对于 $j > k$，$a_j = 0$)

考虑 $\{g_n\}, \{a_n\}$ 的生成函数 $G(x), A(x)$，我们发现，只有 $G(x)[x^0]$ 和 $A(x)$ 没有关系，剩余部分都是和 $A(x)$ 的卷积。

也就是说：

$$
G(x) = g_0 + G(x)A(x)
$$

化简后有：

$$
\begin{align*}
(1-A(x))G(x) &= g_0 \\
G(x) &= \frac{g_0}{1-A(x)}\\
G(x) &\equiv g_0 (1-A(x))^{-1} \pmod{x^n}
\end{align*}
$$


用多项式求逆做就可以了。

## 代码

```cpp
#include <bits/stdc++.h>
using namespace std;

namespace polynomial {
	// 多项式大全略
}

using namespace polynomial;

int n, k, ans, a[MAXN + 10], f[MAXN + 10], c[MAXN + 10], mod_poly[MAXN + 10];

inline int readint() {
    int f=1, r=0; char c=getchar();
    while(!isdigit(c)) { if(c=='-')f=-1; c=getchar(); }
    while(isdigit(c)) { r=r*10+c-'0'; c=getchar(); }
    return f*r;
}

void solve(int x, int ret[]) {
    static int a[MAXN + 10], tmp[MAXN + 10];
    memset(a, 0, sizeof(a));
    a[1] = 1;
    memset(ret, 0, sizeof(int)*(MAXN+10));
    ret[0] = 1;
    while(x > 0) {
        if(x & 1) {
            conv(k-1, a, ret, ret);
            poly_div(2*k-1, k, ret, mod_poly, tmp, ret);
        }
        x >>= 1;
        conv(k-1, a, a, a);
        poly_div(2*k-1, k, a, mod_poly, tmp, a);
    }
}

int main() {
    n = readint(), k = readint();
    for(int i = 1; i <= k; i++) f[i] = (readint()%MOD+MOD)%MOD;
    for(int i = 0; i < k; i++) a[i] = (readint()%MOD+MOD)%MOD;
    mod_poly[k] = 1;
    for(int i = 1; i <= k; i++) mod_poly[k-i] = dec(0, f[i]);
    solve(n, c);
    for(int i = 0; i < k; i++) ans = pls(ans, mul(c[i], a[i]));
    cout << ans << '\n';
    return 0;
}
```

