---
title: "[NOI2009]变换序列"
layout: post
comments: true
categories: "解题报告"
tags: ["二分图","匈牙利算法","贪心","字典序"]
---



链接：[Luogu-P1963][1]

## 思路
这个题目可以看出你真正理解了匈牙利算法没有。

首先我们可以建立二分图的模型：每个位置可以有2种取值，于是我们把位置作为左边的点，取值作为右边的点。然后进行二分图匹配，只要有完美匹配，完美匹配就是一个可行解。

<!--more-->

再考虑题面中最优性的要求。对于字典序问题，我们常常按照字典序枚举。于是这里也可以枚举：从上往下枚举左边的点，按照字典序枚举和右边的哪个点匹配，再看除开匹配了的两个点剩下的那个图中有没有完美匹配。举个例子：不妨设左边的点$u_i$和右边的点$v_i,v_i'$连了边。首先尝试匹配$(u_i, v_i)$。在除开了这条边以及这条边之前以及匹配的子图后，看剩下的图有无完美匹配。如果有，就选定$(u_i,v_i)$，否则尝试选定$(u_i, v_i')$。如果$(u_i, v_i')$还不行的话就说明无解。
由于枚举左边的点是$O(n)$的，匈牙利算法是$O(nm)=O(n^2)$的（边数是$O(n)$的），这个方法复杂度是$O(n^3)$的，有些高。

这时就要追寻匈牙利算法的本质了。不妨设左边点集为X，右边的为Y，那么匈牙利算法是后面的X点把Y点以前匹配的X点“挤掉”的过程，因为每次从某个X点$u$开始增广，都会试着让`mat[v] = u`。如果我们让字典序小的“挤掉”字典序大的，不就刚刚好可以满足题意了么？我们把邻接表按照字典序排序，每次再倒着扫描，并且增广即可。复杂度为$O(n^2)$，但是上界比较松，可以通过。

## 代码
```cpp
#include <bits/stdc++.h>
using namespace std; 

const int MAXN = 20000, MAXM = 4e4, INF = 0x3f3f3f3f;

int n, match_cnt, e_ptr, vis[MAXN+10], mat[MAXN+10];

vector<int> G[MAXN+10];

inline void AddPair(int u, int v){ 
	G[u].push_back(v); G[v].push_back(u);
}

bool augment(int u) {
	for(int i=0; i<G[u].size(); i++) {
		int v = G[u][i];
		if(vis[v] == match_cnt) continue;
		vis[v] = match_cnt; //数据范围比较大，不清空数组，打时间戳
		if(mat[v] == -1 || augment(mat[v])) {
			mat[v] = u; 
			return true;
		}
	}
	return false;
}

int Hungary() {
	memset(mat, 0xff, sizeof(mat));
	int ret = 0;
	for(int u=n-1; u>=0; u--) { //!!
		++match_cnt;
		if(augment(u)) ++ret;
	}
	return ret;
}

template<typename T>
inline void readint(T& x) {
	T f=1, r=0; char c=getchar();
	while(!isdigit(c)) { if(c=='-')f=-1; c=getchar(); }
	while(isdigit(c)) { r=r*10+c-'0'; c=getchar(); }
	x = f*r;
}

int main() {
	int d, a, b, Ans;
	readint(n);
	for(int i=0; i<n; i++) {
		readint(d);
		a = (i-d+n)%n;
		b = (i+d)%n;
		AddPair(i, a+n);
		AddPair(i, b+n);
	}
	for(int i=0; i<2*n; i++)
		sort(G[i].begin(), G[i].end());
	Ans = Hungary();
	if(Ans != n) puts("No Answer");
	else {
		for(int i=0; i<n; i++)
			mat[mat[i+n]]=i;
		for(int i=0; i<n; i++) {
			printf("%d", mat[i]);
			if(i!=n-1) putchar(' '); 
		}
	}
	return 0;
}
/*
附赠数据一组：
16
4 5 6 8 5 3 4 6 7 7 4 6 7 4 7 3 
*/ 
```

## 还有别的做法吗？

考虑贪心。

（待填坑）

参考：[Byvoid神犇的Blog][2]（%%%%%%%）

[1]: https://www.luogu.org/problemnew/show/P1963
[2]: https://www.byvoid.com/zhs/blog/noi-2009-transform