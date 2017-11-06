---
layout: post
comments: true
categories: ['解题报告']
tags: ["最短路","图论","BFS"]
title: '[USACO14DEC]Piggy Back'
---

链接:[Luogu-P3110][1]
## 分析
分两种情况讨论。

1.  $$P \leq B+E$$ 。考虑二者在某个点处相遇。在这个点后两个人如果分别走，一定是沿着到$$N$$的最短路。于是显然背着走更好。
2.  $$P>B+E$$。二者相遇后各自独立地沿着到$$N$$的最短路走（其实是同一条路），比背着走更好。
<!--more-->
## 代码
```cpp
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 40000, MAXM = 40000, INF = 0x3f3f3f3f;
struct Edge {
	int v,next;
};

int N, M, Be, El, Pg, e_ptr, Ans=INF, S[4], head[MAXN+10],
    dist[4][MAXN+10]; Edge E[(MAXM<<1)+10];
void AddEdge(int u, int v) {
	E[++e_ptr] = (Edge){v,head[u]}; head[u]=e_ptr;
}
void AddPair(int u, int v) {
	AddEdge(u,v); AddEdge(v,u);
}

void BFS(int idx) {
	queue<int> Q;
	memset(dist[idx], 0xff, sizeof(int) * (MAXN+10));
	Q.push(S[idx]); dist[idx][S[idx]]=0;
	while(!Q.empty()) {
		int u=Q.front(); Q.pop();
		for(int j=head[u];j;j=E[j].next) {
			int v=E[j].v;
			if(dist[idx][v] == -1) {
				dist[idx][v] = dist[idx][u] + 1;
				Q.push(v);
			}
		}
	}
}

int main() {
	int u, v;
	scanf("%d%d%d%d%d", &Be, &El, &Pg, &N, &M);
	for(int i=1; i<=M; i++) {
		scanf("%d%d", &u, &v);
		AddPair(u,v);
	}
	
	S[1]=1; S[2]=2; S[3]=N;
	for(int i=1; i<=3; i++) BFS(i);
	
	for(int u=1; u<=N; u++) 
		Ans=min(Ans, dist[3][u]*Pg + dist[1][u]*Be + dist[2][u]*El);
	printf("%d", Ans);
	return 0;
}
```

 [1]:https://www.luogu.org/problemnew/show/3110


