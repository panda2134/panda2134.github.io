---
layout: post
comments: true
catalog: true
title: 利用单调性优化动态规划
categories: 笔记
tags:
  - 动态规划
  - 单调栈
  - 单调队列
  - 斜率优化
  - 四边形不等式
  - 凸壳
---

参考了[这个题解](http://www.cnblogs.com/ka200812/archive/2012/08/03/2621345.html)，虽然有错误，但是讲的还不错= =。

## 斜率优化

### HDU3507

#### 题意

把一个序列 $C_i​$ 划分成若干份，每份的代价为 $\left( \sum c_i \right)^2 + M​$. 最小化总代价和。

#### 思路

$f(i)$ 表示前 $i$ 个的最小总代价和。

于是 $f(i) = \min_{0 \le j \le i-1} \\{ f(j) + \left(\sum_{j+1 \le k \le i} c_i\right)^2 + M \\}$.  边界为 $f(0) = 0$.
但是复杂度太高，无法胜任题中数据范围。考虑进行优化。看到 $\min$ ，联想到单调性。

假设在 $j = \alpha$ 时取值优于 $j = \beta$ ，且 $\alpha > \beta$ ， 而 $\\{c_n\\}$ 前缀和为 $\text{sum}(i)$ ，就有：
$$
\newcommand{sumc}{\text{sum}}
\begin{align*}
f(\alpha) + \sumc^2(\alpha) - 2\sumc(\alpha) \sumc(i) + \sumc^2(i) + M &< f(\beta) + \sumc^2(i) - 2 \sumc(\beta) \sumc(i)+ \sumc^2(\beta) + M \\
f(\alpha) + \sumc^2(\alpha) - 2\sumc(\alpha)\sumc(i) &< f(\beta) + \sumc^2(\beta) - 2\sumc(\beta)\sumc(i) \\
\end{align*}
$$

令 $ y_{\alpha} = f(\alpha) + \sumc^2(\alpha), y_{\beta} = f(\beta) + \sumc^2(\beta), x_{\alpha} = 2\cdot \sumc(\alpha), x_{\beta} = 2 \cdot\sumc(\beta)$ ，则有：

$$
\begin{equation*}
y_{\alpha} - y_{\beta} < (x_{\alpha} - x_{\beta}) \cdot \sumc(i)
\end{equation*}
$$

显然，$\sumc(x)$ 关于 $x$ 单调递增，于是当 $\alpha > \beta$ 时，$\sumc(\alpha) \ge \sumc(\beta)$ ，斜率存在时，有:   

$$
\frac{y_{\alpha} - y_{\beta}}{x_{\alpha} - x_{\beta}} < \sumc(i)
$$

上面的式子为斜率形式，我们可以在坐标系中画出对应的点。

不妨记左侧为 $K(\alpha, \beta)$.  同理可得，上式取 $\ge$ 时，满足在 $j=\beta$ 时取值优于 $j=\alpha$.

我们下面就证明，假如 $\alpha < \beta < \gamma$ ，而且 $K(\beta,\alpha) \ge K(\gamma, \beta)$ ，那么在求 $f(i)$ 时，一定不会在 $j = \beta$ 处取得最小值。

1. 当 $K(\gamma, \beta) < \sumc(i)$ 时：由上式定义知，取得 $j = \gamma$ 优于 $j = \beta$ . 所以不会在 $j = \beta$ 取得最小值。
2. 当 $K(\gamma, \beta) \ge \sumc(i)$ 时：取得 $j=\beta$ 优于 $j = \gamma$ ，但是取得 $j=\alpha$ 优于 $j = \beta$ ，所以仍然不会取得 $j = \beta$ .

综上所述，一定不会在 $j = \beta$ 处取得最小值，命题得证。因此可以移除 $j = \beta$ 对应的点。于是可行的决策点一定满足斜率逐渐增大，即形成上凸壳。如图。

![slope](https://panda2134.tk/img/slope.png)

用单调队列维护凸壳。维护单调队列相邻元素之间的斜率单调递增，即：对于任意 2 个相邻元素（自然，也就是 $c_i$ 中的下标）$A, B$ ，如果队列中 $A$ 在 $B$ 前面，一定有从队首到队尾 $K(B, A)$ 单调递增。求解的时候首先检查队首的斜率是否小于 $\sumc(i)$ ，大于的话，说明队首比它后面的所有元素更优，于是队首为决策点，求解 $f(i)$，反之队首出队，因为由上述转移方程，如果这时候队首不是最优决策点，以后 $\sumc(i) - \sumc(j)$ 越来越大，更不可能是最优决策点。当然，对于一般的斜率优化 DP，如果当前非最优的决策点，以后可能最优，就不能出队，每次应该在凸包上二分。

#### 代码

注意避免除法。就算是队列末尾的 2 个元素对应斜率等于带插入元素和最后一个元素的斜率，也要继续弹出。

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 5e5;

int N, M, Sum[MAXN+10], opt[MAXN+10];

inline int readint() {
	int f=1, r=0; char c=getchar();
	while(!isdigit(c)) { if(c=='-')f=-1; c=getchar(); }
	while(isdigit(c)) { r=r*10+c-'0'; c=getchar(); }
	return f*r;
}

inline bool Init() {
	if(scanf("%d%d", &N, &M) == EOF)
		return false;
	for(int i = 1; i <= N; i++)
		Sum[i] = readint() + Sum[i-1];
	return true;
}

int Hd = 1, Tl = 0, Q[(MAXN+10)<<1];

inline int GetY(int i) { return opt[i] + Sum[i] * Sum[i]; }
inline int GetX(int i) { return 2 * Sum[i]; }

inline void Work() {	
	Hd = 1, Tl = 0;
	opt[0] = 0; Q[++Tl] = 0;
	for(int i = 1; i <= N; i++) {
		while(Tl - Hd + 1 >= 2 &&
			(GetY(Q[Hd+1]) - GetY(Q[Hd])) < Sum[i] * (GetX(Q[Hd+1]) - GetX(Q[Hd])))
			++Hd;
		int j = Q[Hd];
		opt[i] = opt[j] + (Sum[i] - Sum[j]) * (Sum[i] - Sum[j]) + M;
		while(Tl - Hd + 1 >= 2 && 
			(GetY(Q[Tl]) - GetY(Q[Tl-1])) * (GetX(i) - GetX(Q[Tl])) >= 
			(GetY(i) - GetY(Q[Tl])) * (GetX(Q[Tl]) - GetX(Q[Tl-1])))
			--Tl;
		Q[++Tl] = i;
	}
	printf("%d\n", opt[N]);
}

int main() {
	while(Init())
		Work();
	return 0;
}
```

### BZOJ1010
DP方程：$f(i) = \min\\{f(j) + \left(i - (j+1)+\sum_{j+1 \le k \le i}c_k - L\right)^2 \vert 0 \le j \le i-1\\}$




## 四边形不等式





