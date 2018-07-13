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

## Caylay-Hamilton 定理

### 矩阵的特征值和特征向量

二者以符号 $\lambda, \boldsymbol{\xi}$ 表示.

特征向量非0.

特征值和特征向量满足关系：
$$
\boldsymbol{A\xi} = \lambda \boldsymbol{\xi}
$$

即把矩阵对应的线性变换应用到特征向量上，并不会改变其方向。
$$
\begin{align*}
\boldsymbol{IA\xi} &= \lambda \boldsymbol{I\xi}\\
\boldsymbol{A - I}\lambda &= \bold{0}
\end{align*}
$$
如果矩阵不满秩，其行列式一定为0.