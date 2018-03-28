---
title: "[NOI2014]魔法森林"
categories: '解题报告'
tags: ['Link-Cut Tree', '并查集', '生成树']
comments: true
---

链接：[Luogu-P2387][1]

这是我做的第一道非模板LCT题目……自己并没有想出来，看题解也看了好久，于是总结下做这个题目的思路。

## 题意	

给出一个$n$个点，$m$条边的无向图，每条边都有权值$a_i,b_i$，求一条从点$1$到点$n$的路径，使得这条路径上边的$a_i,b_i$最大值之和最小。$2 \leq n \leq 5 \times 10^4, 0 \leq m \leq 1 \times 10^5$。	

<!--more-->

## 思路	

### 二分？	

看到*最大值最小*，想到二分。怎么二分呢？如果是只有一种权值的情况，可以二分+BFS，不过我们有更好的方法，也就是瓶颈生成树。也就是说这里要求出2个参数的瓶颈生成树。对于有2种权值的情况，是否也可以类似地直接贪心呢？比如说，按照$a_i+b_i$排序？听上去就不靠谱。或者说先二分$a_i$，对每个$a_i$的值去二分$b_i$？ 这也不符合“和的最大值最小”这个要求。	

### 生成树！	

不过，这个做法倒是提供了一些思路。我们也许可以枚举$\max\\{a_i\\}$，对每个枚举出来的$\max\\{a_i\\}$去判断如何加边。 暴力枚举复杂度太高。考虑效仿Kruskal算法，把边按照$a_i$排序，然后再枚举当前考虑第几条边。这样的话每次判断是否加入当前边即可。判断的依据是什么？是否成环，环中最大边是哪条。根据生成树的回路性质，某个回路中的权值最大边恰好有一条不在最小生成树中。于是每次加边（相当于枚举了$a_i$），同时对$b_i$做动态加边最小生成树，再用$a_i$与当前的$1 \rightarrow n$路径上的$\max\\{b_i\\}$之和更新答案。显然对于每个给定的$a_i$，$b_i$满足最小生成树性质时一定最优。而我们枚举了$a_i$的取值，这样一定可以遍历所有的可能情况。

### 细节的处理	

上面的方法似乎很正确，不过好像有点问题：加入的边一定在$1 \rightarrow n$的路径上吗？	

稍微想想就会发现，就算加的边和这条路径无关，也没有关系：由于这时$a_i$大于$1 \rightarrow n$的路径上$a_i$最大值，而$1 \rightarrow n$的路径上$b_i$最大值又不变，于是在考虑$1 \rightarrow n$的路径上$a_i$最大值时，答案已经松弛过了，此时不能再松弛答案！如果当前边与$1 \rightarrow n$的路径上某个边构成环，那么这次松弛也是有用的，因为对于不同的$\max\\{a_i\\}$，$b_i$取值也相应不同。

## 实现

考虑下求出“生成树路径边权最大值”怎么做到：用Link-Cut Tree即可。通过一次$\text{MakeRoot}$和一次$\text{Access}$，就可以把路径弄到一条$\text{Preferred Path}$上。然后在Splay里面打标记就好了。注意边权的处理：给每条边单独建一个点就好了。

代码如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 5e4, MAXM = 1e5;

//----------------LCT--------------------
struct Node *null, *nd[MAXN+10];
struct Node {
	int v, s, maxv; bool flip;
	Node *fa, *ch[2];
	Node() { v = maxv = 0; s = 1; flip = false; fa = ch[0] = ch[1] = null; }
	Node(int v_) { v = maxv = v_; s = 1; flip = false; fa = ch[0] = ch[1] = null; }
	bool splayrt() { return fa->ch[0]!=this && fa->ch[1]!=this; }
	int rel() { return splayrt() ? -1 : (fa->ch[0]==this ? 0 : 1); }
	void rev() { flip^=1; }
	int cmp(int k) { return k == ch[0]->s + 1 ? -1 : (k > ch[0]->s + 1 ? 1 : 0); }
	void pushdown() {
		if(flip) {
			flip^=1; ch[0]->flip^=1; ch[1]->flip^=1;
			swap(ch[0], ch[1]);
		}
	}
	void maintain() {
		maxv = max(max(ch[0]->maxv, ch[1]->maxv), v);
		s = ch[0]->s + ch[1]->s + 1;
	}
};

void init_null() {
	null = new Node(0); null->s = 0;
}

void rotate(Node* o) {
	Node *x, *y, *k; int d, d2;
	if(o->splayrt()) return;
	x = o->fa; y = x->fa;
	d = o->rel(); d2 = x->rel();
	k = o->ch[d^1];
	if(!x->splayrt()) y->ch[d2] = o;
	o->fa = y;
	o->ch[d^1] = x; x->fa = o;
	x->ch[d] = k; k->fa = x;
	x->maintain(); o->maintain();
}

void Splay(Node* o) {
	static Node *x, *S[(MAXN<<1)+10]; int p, d, d2;
	for(p=1, S[p] = o; !S[p]->splayrt(); p++)
		S[p+1] = S[p]->fa;
	for(; p; p--) S[p]->pushdown();
	while(!o->splayrt()) {
		x = o->fa; 
		d = o->rel(); d2 = x->rel();
		if(!x->splayrt()) {
			if(d == d2) rotate(x);
			else rotate(o);
		}
		rotate(o);
	}
}

Node* FindMax(Node* o) {
	if(o->v == o->maxv) //!!
		return o;
	else return o->ch[0]->maxv == o->maxv ? 
		FindMax(o->ch[0]) : FindMax(o->ch[1]);
}

Node* Kth(Node* o, int k) {
	if(o == null) return o;
	int d = o->cmp(k);
	if(d==-1) return o;
	return Kth(o->ch[d], k - d*(o->ch[0]->s + 1));
}

void Access(Node* o) {
	for(Node *t=null; o!=null; t=o, o=o->fa) {
		Splay(o); o->ch[1] = t; o->maintain();
	}
}

void MakeRoot(Node* o) {
	Access(o); Splay(o); o->rev();
}

Node* GetRoot(Node* o) {
	Access(o); Splay(o);
	while(o->ch[0] != null) o = o->ch[0];
	return o;
}

void Link(Node* u, Node* v) {
	if(GetRoot(u) == GetRoot(v)) return;
	MakeRoot(u); Splay(u); u->fa = v;
}

void Cut(Node* u, Node* v) {
	if(GetRoot(u) != GetRoot(v)) return;
	MakeRoot(u); Access(v); Splay(u);
	if(u->ch[1] == v) {
		u->ch[1] = null; v->fa = null;
		u->maintain();
	}
}

//-----------------------------------------

struct Edge {
	int u, v, a, b;
	Edge() {}
	Edge(int u_, int v_, int a_, int b_):
		u(u_), v(v_), a(a_), b(b_) {}
	inline bool operator<(const Edge& rhs) const
	{ return a < rhs.a; }
} E[MAXM+10];
int N, M, Ans, fa[MAXN+10];

int GetFather(int x) { return fa[x] == x ? x : fa[x] = GetFather(fa[x]); }
inline void Union(int x, int y) { fa[GetFather(x)] = GetFather(y); }

template<typename T>
inline void readint(T& x) {
	T f=1, r=0; char c=getchar();
	while(!isdigit(c)){ if(c=='-')f=-1; c=getchar(); }
	while(isdigit(c)){ r=r*10+c-'0'; c=getchar(); }
	x = f*r;
}

void Init() {
	int u, v, a, b;
	init_null(); 
	readint(N); readint(M);
	for(int i=1; i<=N; i++) {
		nd[i] = new Node(0);
		fa[i] = i;
	}
	for(int i=1; i<=M; i++) {
		readint(u); readint(v);
		readint(a); readint(b);
		E[i] = Edge(u, v, a, b);
	}
	sort(E+1, E+M+1);
}

inline void AddTreeEdge(int u, int v, int b) {
	Node* w = new Node(b);
	Link(nd[u], w); Link(nd[v], w);
	if(GetFather(u) != GetFather(v)) 
		Union(u, v);
}

inline Node* GetMaxEdge(int u, int v) {
	Node* w;
	MakeRoot(nd[u]); Access(nd[v]); Splay(nd[u]);
	w = FindMax(nd[u]); 
	Splay(w);
	return w;
}

inline void CutMaxEdge(int u, int v) {
	Node *w, *x, *y; int k;
	w = GetMaxEdge(u, v); k = w->ch[0]->s + 1;
	x = Kth(w, k-1); y = Kth(w, k+1);
	if(x == null || y == null) return;
	Cut(w, x); Cut(w, y);
}

void Work() {
	int u, v, a, b; bool add = false;
	Ans = INT_MAX;
	for(int t=1; t<=M; t++) {
		u = E[t].u, v = E[t].v, a = E[t].a, b = E[t].b;
		add = false;
		if(GetFather(u) != GetFather(v)) 
			add = true, AddTreeEdge(u, v, b);
		else if(b < GetMaxEdge(u, v)->v) {
			add = true;
			CutMaxEdge(u, v);
			AddTreeEdge(u, v, b);
		}
		//更新答案
		if(add && GetFather(1) == GetFather(N)) 
			Ans = min(Ans, a + GetMaxEdge(1, N)->v);
	}
	if(Ans < INT_MAX)
		printf("%d", Ans);
	else puts("-1");
}

int main() {
	Init(); Work();
	return 0;
}
```



[1]: https://www.luogu.org/problemnew/show/P2387	"Luogu-P2387"
