---
layout: post
comments: true
title: "[SDOI2014]重建"
category:
 - 解题报告
tags:
 - 矩阵树定理
 - 期望
 - 高斯消元
---

## 题意

给出一个无向图，每个边有个存在概率 $p_{<u, v>}$ ，求所有存在边恰好组成生成树的概率。

## 思路

第一眼感觉是裸的矩阵树定理，后来发现自己 $\text{Naive}$！

滚去膜拜 dkw 聚聚的题解，学会了一种矩阵树定理的化简技巧。

我们显然可以知道答案是下式：

$$
\sum_{T}\left(\prod_{<u, v> \in T} p_{u, v} \times \prod_{<u, v> \notin T} (1-p_{<u, v>})\right)
$$

而矩阵树定理求的是这个式子：

$$
\sum_T\left(\prod_{<u, v> \in T} A_{<u, v>}\right)
$$

考虑如何变形。上面那个式子里面有 2 个 $\prod$，所以我们考虑在下面这个式子**外面**乘上一个系数，再在化简的时候**分开**。这样就可以**拆出** 2 个 $\prod$.

列个方程：

$$
\sum_{T}\left(\prod_{<u, v> \in T} p_{u, v} \times \prod_{<u, v> \notin T} (1-p_{<u, v>})\right) = \left(\prod_{<u, v>} (1-p_{<u, v>})\right) \times \sum_T\left(\prod_{<u, v> \in T} A_{<u, v>}\right)
$$

于是化简后有

$$
\sum_{T}\left(\prod_{<u, v> \in T} p_{u, v} \times \prod_{<u, v> \notin T} (1-p_{<u, v>})\right) =\sum_T\left(\prod_{<u, v> \in T} (1-p_{<u, v>})A_{<u, v>}\times \prod_{<u, v> \notin T} (1-p_{<u, v>})\right)
$$

那么显然

$$
p_{<u, v>} = (1-p_{<u, v>}) A_{<u, v>}
$$

系数化为1：

$$
A_{<u, v>} = \frac{p_{<u, v>}}{1-p_{<u, v>}}
$$

现在是货真价实的矩阵树定理裸题了。用矩阵树定理算 $\sum_T \left(\prod_{<u, v> \in T} A_{<u, v>}\right)$ ，然后**乘上系数**即可（没乘系数调试了好久……以后记住，数学相关题目，一定要写清楚待求的式子！）。

$p = 1$ 的时候分母为 0 ，怎么办？考虑到 $\mathtt{nan}$ 不能参与运算，设其值为 $\frac{1}{\epsilon}$ 即可。

（其实精度相关处理是最恶心的地方……）

## 代码

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long double ld;

const double eps = 1e-6;
const int MAXN = 50;

int n;
ld mul = 1.0l, A[MAXN + 10][MAXN + 10], G[MAXN + 10][MAXN + 10];

int dcmp(double x) {
	return fabs(x) < eps ? 0 : (x > 0 ? 1 : -1);
}

int main() {
	scanf("%d", &n);
	for(int i = 1; i <= n; i++)
		for(int j = 1; j <= n; j++) {
			scanf("%Lf", &G[i][j]);
			if(dcmp(G[i][j]) == 0) G[i][j] = eps;
			if(dcmp(G[i][j]-1) == 0) G[i][j] = 1-eps;
			if(i < j) mul *= (1 - G[i][j]);
		}
	
	for(int i = 1; i <= n; i++) {
		for(int j = 1; j <= n; j++)
			if(i != j) {
				if(dcmp(G[i][j]-1) != 0)
					A[i][j] -= G[i][j] / (1-G[i][j]);
				else
					A[i][j] -= 1 / eps;
				A[i][i] -= A[i][j];
			}
	}
	
	n--;
	for(int i = 1; i <= n; i++) {
		int k = i;
		for(int j = n; j >= i; j--)
			if(dcmp(A[j][i]) != 0) k = j;
		
		if(k != i) {
			for(int j = 1; j <= n; j++)
				swap(A[i][j], A[k][j]);
			mul *= -1;
		}
		
		if(dcmp(A[i][i]) == 0)
			break;
		
		for(int j = i+1; j <= n; j++) {
			ld t = A[j][i] / A[i][i];
			for(int k = 1; k <= n; k++)
				A[j][k] -= t * A[i][k];
		}
	}
	
	for(int i = 1; i <= n; i++)
		mul = mul * A[i][i];
	
	printf("%Lf", mul);
	
	return 0;
}
```

