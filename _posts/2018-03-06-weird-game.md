---
layout: post
comments: true
title: "[SCOI2012]奇怪的游戏"
categories: "解题报告"
tags: ["网络流","二分答案","数学"]
---

[BZOJ2756][1]

## 题意

给出一个 $$n \times m$$ 的矩阵，初始每个格子有一个正整数。每次可以给相邻两个格子加1，求最少操作多少次使得矩阵里面数字相同。

<!--more-->

## 思路

就差一点点就想出来了QAQ
先转化为判定性问题。显然我们可以把“+1”的操作看成网络流的增广操作，黑白染色后建图。
设每个格子都变成了 $$x$$ ，连s->黑点边，容量 $$x-w_{ij}$$ ；白点->t边，容量 $$x-w_{ij}$$ ；黑白相邻连边，容量无穷大。
找出最大流后看s出发，t结束边是否都满流即可。
解决了判定性问题我们自然就想到了二分。看看是否满足可二分性。对于一般的情况，是不满足可二分性的。
我们考虑行数列数至少一个是偶数的情况。显然这种特殊情况是满足单调的，因为只要 $$x$$ 是一个答案，我们可以构造使得 $$x+1$$ 也是一个答案。这时可以二分。
对于行数列数都是奇数的情况呢？（我想到这一步就懵逼了= =）其实可以利用每次加相邻2个点列方程。设黑点和为 $$s_1$$ , 点数为 $$n_1$$ , 白点相应为 $$s_2$$ , $$n_2$$ , 由于每次加的2个点相邻，就一定有 $$x \cdot n_1 - s_1 = x \cdot n_2 - s_2$$，解得 $$\large{x = \frac{s_1 - s_2}{n_1-n_2}}$$。显然此时满足分母非0。这时候 $$x$$ 是唯一的。如果 $$x$$ 不是整数，无解。否则直接建图，网络流check即可。

总结：对于不同性质的数据可能有不同的思路。如果不满足二分所需要的单调性，说不定解是唯一的，可以尝试按照题意列方程。

## 代码

二分边界小了WA，边界大了TLE，有没有什么好的解决办法呢？

```cpp
#include <bits/stdc++.h>
#define CLEAR(x) memset((x), 0, sizeof(x))
#define rep(i, x) for(int i = 1; i <= (x); i++)
using namespace std;

typedef long long int64;

const int MAXN = 2000, MAXM = 100000;
const int di[] = { -1, 1, 0, 0 }, dj[] = { 0, 0, -1, 1 };
const int64 LL_INF = 0x3f3f3f3f3f3f3f3fLL;

struct Edge {
	int v;
	int64 flow, cap;
	int next;
};

int T, r, c, s, t, n1, n2, e_ptr = 1, head[MAXN+10]; Edge E[(MAXM+10)<<1];
int64 Mx, s1, s2, A[MAXN+10][MAXN+10];

inline void AddEdge(int u, int v, int64 cap) {
	E[++e_ptr] = (Edge) { v, 0, cap, head[u] }; head[u] = e_ptr;
	E[++e_ptr] = (Edge) { u, 0,   0, head[v] }; head[v] = e_ptr;
}

int cur[MAXN+10], d[MAXN+10];
bool BFS() {
	queue<int> Q;
	memset(d, 0xff, sizeof(d));
	Q.push(s); d[s] = 0;
	while(!Q.empty()) {	
		int u = Q.front(); Q.pop();
		for(int j=head[u]; j; j=E[j].next) {
			int v = E[j].v; int64 f = E[j].flow, c = E[j].cap;
			if(f < c && d[v] == -1) {
				d[v] = d[u] + 1;
				if(v == t) return true;
				else Q.push(v);
			}
		}
	}
	return false;
}

int64 DFS(int u, int64 flow) {
	if(u == t || flow == 0) return flow;
	int64 res = flow;
	for(int& j=cur[u]; j; j=E[j].next) {
		int v = E[j].v; int64 f = E[j].flow, c = E[j].cap;
		if(d[v] == d[u] + 1) {
			int64 aug = DFS(v, min(res, c-f));
			E[j].flow += aug; E[j^1].flow -= aug;
			res -= aug;
		}
	}
	return flow - res;
}

int64 Dinic() {
	int64 MaxFlow = 0, CurFlow = 0;
	while(BFS()) {
		memcpy(cur, head, sizeof(head));
		while( (CurFlow = DFS(s, LL_INF)) )
			MaxFlow += CurFlow;
	}
	return MaxFlow;
}

void Init() {
	s = MAXN - 1, t = MAXN;
	scanf("%d%d", &r, &c);
	rep(i, r) rep(j, c) {
		scanf("%lld", &A[i][j]);
		Mx = max(Mx, A[i][j]);
		if((i^j)&1) {
			++n1; s1 += A[i][j];
		} else {
			++n2; s2 += A[i][j];
		}
	}
}

inline bool valid(int i, int j) { return i >= 1  && i <= r && j >= 1 && j <= c; }
inline int idx(int i, int j) { return (i-1) * c + j; }

bool judge(int64 x) {
	if(x < Mx) return false;
	e_ptr = 1; CLEAR(head);
	rep(i, r) rep(j, c) {
		if((i^j)&1) 
			AddEdge(s, idx(i, j), x - A[i][j]); // >=0
		else
			AddEdge(idx(i, j), t, x - A[i][j]);
		if((i^j)&1) {
			for(int dir = 0; dir < 4; dir++) {
				int ni = i + di[dir], nj = j + dj[dir];
				if(!valid(ni, nj)) continue;
				AddEdge(idx(i, j), idx(ni, nj), LL_INF);
			}
		}
	}
	Dinic();
	for(int j=head[s]; j; j=E[j].next)
		if(E[j].flow != E[j].cap)
			return false;
	for(int j=head[t]; j; j=E[j].next) 
		if(E[j^1].flow != E[j^1].cap)
			return false;
	return true;
}

void Work1() {
	int64 L = Mx, R = Mx + (1LL<<30), Mid; 
	if(!judge(LL_INF)) { cout << -1 << endl; return; }
	while(L < R) {
		Mid = ((L + R) >> 1);
		if(judge(Mid)) 
			R = Mid;
		else 
			L = Mid + 1;
	}
	cout << (r*c*L - s1 - s2) / 2 << endl;
}

void Work2() {
	if((s1-s2) % (n1-n2) != 0)
		cout << -1 << endl;
	else {
		int64 x = (s1-s2) / (n1-n2);
		if(judge(x)) {
			cout << (r*c*x - s1 - s2) / 2 << endl;
		} else 
			cout << -1 << endl;
	}
}

void Clear() {
	r = c = s = t = n1 = n2 = 0; 
	e_ptr = 1; CLEAR(head); Mx = s1 = s2 = 0; 
}

int main() {
	scanf("%d", &T);
	while(T--) {
		Init(); 
		if(n1 == n2) 
			Work1(); 
		else 
			Work2();
		Clear();
	}
}
```



[1]:http://www.lydsy.com/JudgeOnline/problem.php?id=2756