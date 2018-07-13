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

才听 @Sparky_14145 说这玩意已经是 NOIP 难度辣！为了避免自己没有 NOIP 水平，特来学习。
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

如果矩阵不满秩，其行列式一定为0.显然，若要 $\boldsymbol{\xi}$ 不是 $\boldsymbol{0}$，系数矩阵必不满秩，则有：

$$
p(\lambda) = \det(\lambda\boldsymbol{I}-\boldsymbol{A}) = 0
$$

上述方程称作特征方程，左式称为特征多项式。

### 定理描述

一个矩阵带入其特征多项式后得到 $\boldsymbol{0}$ 矩阵。

#### 一个例子

考虑矩阵 $\begin{bmatrix}0 & 1 \\ 1 & 1\end{bmatrix}$.

其特征多项式为 $\det(\lambda\boldsymbol{I}-\boldsymbol{A}) = \det( \begin{bmatrix}\lambda & 0 \\ 0 & \lambda\end{bmatrix}- \begin{bmatrix}0 & 1 \\ 1 & 1\end{bmatrix}) = \begin{vmatrix}\lambda & -1 \\ -1 & \lambda-1\end{vmatrix} = \lambda^2-\lambda-1$.

把它自己带入其特征多项式有：

$$
\begin{align*}
\begin{bmatrix}0 & 1 \\ 1 & 1\end{bmatrix}^2 - \begin{bmatrix}0 & 1 \\ 1 & 1\end{bmatrix} - \boldsymbol{I} &= \begin{bmatrix}1 & 1 \\ 1 & 2\end{bmatrix} - \begin{bmatrix}0 & 1 \\ 1 & 1\end{bmatrix} - \begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}\\
&= \begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix}.
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

= \begin{bmatrix}g_2 \\ g_3 \\ \cdots \\ g_{k+1}\end{bmatrix}^T
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

使用数学归纳法即可证明，$\bm{A}^n$ 只和 $\bm{A}^0\sim \bm{A}^{k-1}$ 有关。在此略去（其实是太晚了撑不住了QAQ）。

于是可以做一个模特征多项式意义下的矩阵快速幂。这样的复杂度是 $O(k \lg k \lg n)$ 的。

## 代码

咕咕咕。