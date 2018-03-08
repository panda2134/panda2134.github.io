---
layout: post
comments: true
title: "[六省联考2017]寿司餐厅"
categories: "解题报告"
tags: ["最大权闭合子图","最小割"]
---

省选提前到 4 月 6 日了，慌的要命，赶紧找找去年的题目做一做。

[Luogu-3749][1]

这个题目似乎又是zhx出的？

## 思路

Kiana的美食评判标准的“记忆性”说明选择了多个区间，影响不会扩大。“选择即有对应的影响，选择了多个物品，影响不会扩大，求最大权和……” 不就是最大权闭合子图吗？

每个区间建 1 个点，每个代号建 1 个点，分别赋相应的权值，再找出最大权闭合子图即可。

## 代码

```cpp
#include <bits/stdc++.h>
#define rep(i, x) for(int i = 1 ; i <= (x); i++)
using namespace std;

const int MAXN = 1e4, MAXM = 1e5, MAXL = 100, MAXA = 1000, INF = 0x3f3f3f3f;

int idx, N, M, PosSum, A[MAXL+10], W[MAXN+10], D[MAXL+10][MAXL+10], ID[MAXL+10][MAXL+10];

namespace Maxflow {
    struct Edge {
        int u, v, flow, cap, next;
    };
    int n, s, t, e_ptr = 1, head[MAXN+10]; Edge E[(MAXM+10)<<1];
    int vis[MAXN+10], d[MAXN+10], num[MAXN+10], p[MAXN+10], cur[MAXN+10];
    
    void AddEdge(int u, int v, int cap) {
        E[++e_ptr] = (Edge) { u, v, 0, cap, head[u] }; head[u] = e_ptr;
        E[++e_ptr] = (Edge) { v, u, 0,   0, head[v] }; head[v] = e_ptr;
    }
    
    void BFS() {
        queue<int> Q;
        memset(d, 0, sizeof(d));
        memset(vis, 0, sizeof(vis));
        vis[t] = true; Q.push(t);
        while(!Q.empty()) {
            int u = Q.front(); Q.pop();
            for(int j=head[u]; j; j=E[j].next) {
                int v = E[j].v, f = E[j^1].flow, c = E[j^1].cap;
                if(f < c && !vis[v]) {
                    vis[v] = true; d[v] = d[u] + 1;
                    Q.push(v);
                }
            }
        }
    }
    
    int Augment() {
        int aug = INF;
        for(int u = t; u != s; u = E[p[u]].u)
            aug = min(aug, E[p[u]].cap - E[p[u]].flow);
        for(int u = t; u != s; u = E[p[u]].u) {
            E[p[u]].flow += aug;
            E[p[u]^1].flow -= aug;
        }
        return aug;
    }
    
    int ISAP() {
        int u = s, flow = 0;
        BFS(); memcpy(cur, head, sizeof(head));
        for(int i = 1; i <= n; i++) ++num[d[i]];
        while(d[s] < n) {
            bool ok = false;
            if(u == t) {
                flow += Augment();
                u = s;
                continue;
            }
            for(int &j=cur[u]; j; j=E[j].next) {
                int v = E[j].v, f = E[j].flow, c = E[j].cap;
                if(f < c && d[v] == d[u] - 1) {
                    ok = true;
                    p[v] = j; u = v; // 最后再走
                    break;
                }
            }
            if(!ok) {
                int slk = n-1;
                for(int j=head[u]; j; j=E[j].next) {
                    int v = E[j].v, f = E[j].flow, c = E[j].cap;
                    if(f < c) slk = min(slk, d[v]);
                }
                if(--num[d[u]] == 0) break;
                ++num[d[u] = slk + 1];
                cur[u] = head[u];
                if(u != s) u = E[p[u]].u;
            }
        }
        return flow;
    }
}

inline int readint() {
    int f=1, r=0; char c=getchar();
    while(!isdigit(c)) { if(c=='-')f=-1; c=getchar(); }
    while(isdigit(c)) { r=r*10+c-'0'; c=getchar(); }
    return f*r;
}

void Init() {
    N = readint(); M = readint();
    rep(i, N) A[i] = readint();
    rep(i, N) rep(j, N-i+1) {
        D[i][i+j-1] = readint();
        ID[i][i+j-1] = ++idx;
    }
    rep(i, MAXA)
        W[idx + i] = -M*i*i;
    for(int i = 1; i <= N; i++)
        for(int j = i; j <= N; j++) {
            if(i == j) {
                W[ID[i][i]] = D[i][i] - A[i];
                Maxflow::AddEdge(ID[i][i], idx + A[i], INF);
            } else {
                W[ID[i][j]] = D[i][j];
                Maxflow::AddEdge(ID[i][j], ID[i][j-1], INF);
                Maxflow::AddEdge(ID[i][j], ID[i+1][j], INF);
            }
        }
    Maxflow::n = idx + MAXA + 2;
    Maxflow::s = idx + MAXA + 1, Maxflow::t = idx + MAXA + 2;
    for(int i = 1; i <= idx + MAXA; i++) {
        if(W[i] > 0) {
            PosSum += W[i];
            Maxflow::AddEdge(Maxflow::s, i, W[i]);
        }
        if(W[i] < 0)
            Maxflow::AddEdge(i, Maxflow::t, -W[i]);
    }
}

void Work() {
    cout << PosSum - Maxflow::ISAP();
}

int main() {
    Init(); Work();
    return 0;
}
```



[1]: https://www.luogu.org/problemnew/show/P3749