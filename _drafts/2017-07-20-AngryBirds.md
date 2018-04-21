---
layout: post
categories: ["解题报告"]
tags: ["状压DP","数学"]
comments: true
title: "[NOIP2016]愤怒的小鸟"
---

题目链接：

LYOJ:~~[愤怒的南小鸟](https://ly.men.ci/problem/104)~~

Luogu:[愤怒的小鸟](https://www.luogu.org/problem/show?pid=2831)


题目较长，请在OJ上查看

- 目录
* toc
{:toc}

## 0.题记
还记得去年NOIP赛场上看到这个题就懵了
当时还剩下30min，写到这道题，发现题目中有了抛物线，以为要用高斯消元法什么的解出函数方程，果断放弃……
后来才发现，完全可以设出抛物线的方程和过抛物线的亮点，用初中知识解出方程。这一步解决后，就是不讲任何技巧的状压DP都能拿75pts以上
果然还是自己太弱了……希望今年不要再这样懵逼了。

<!--more-->

## 1.审题
作过原点的抛物线，经过猪则猪被消灭。求消灭所有猪需要的小鸟数量。
由 $$ 2 \le n \le 18 $$
To Be Done