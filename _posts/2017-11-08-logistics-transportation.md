---
layout: post
comments: true
categories: ['解题报告']
tags: ["最短路","图论","动态规划","序列型DP"]
title: '[ZJOI2006]物流运输'
---
链接:[Luogu-P1772][1]
## 分析
在输入时对每个码头的不可用时间进行差分。假设某一段连续的时间$$[t_1,t_2]$$选择同一条运输路线，则可以通过Dijkstra求出这段时间的$$s \rightarrow t$$最短路长度，记作$$cost[t_1][t_2]$$。总时间是$$t$$，点数目是$$n$$，那么预处理每个时间段内选择同一条路的代价的时间复杂度是$$O(n) \cdot O(t^2) \cdot O(n \log n) = O(n^2 t^2 \log n)$$。显然是可以承受的。 
<!--more-->    
我们再来考虑一段时间内是用同一条路径更优，还是改变路线更优。注意到总代价=运输路线长度和+K$$\cdot$$改变路线次数。也就是说总代价和改变次数成线性关系。而时间又是个有序的量，就可以考虑进行DP。
状态为$$f(i,j):$$在时间段$$[i,j]$$的最小总代价。
于是就可以转移了：
$$f(i,j)=\min \begin{cases} cost[i][j], \\ f(i,p)+f(p,j)+K \; (p=i,i+1, \dots , j-1) \end{cases}$$
复杂度是$$O(t^3)$$的，也同样可以承受。
## 代码
```cpp
#include <bits/stdc++.h>
using namespace std;
typedef pair<int,int> pii;
struct Edge {
    int v, len, next;
};


const int MAXT = 100, MAXN = 20, MAXM = 400, INF = 0x3f3f3f3f;
int T, N, K, M, e_ptr, head[MAXN+10], dist[MAXN+10], dif[MAXN+10][MAXT+10], 
    cost[MAXT+10][MAXT+10], opt[MAXT+10][MAXT+10];
bool done[MAXN+10], del[MAXN+10];  Edge E[(MAXM<<1)+10];


void AddEdge(int u, int v, int len) {
    E[++e_ptr]=(Edge){v,len,head[u]}; head[u]=e_ptr;
}
void AddPair(int u, int v, int len) {
    AddEdge(u,v,len); AddEdge(v,u,len);
}


void Dijkstra() {
    priority_queue<pii, vector<pii>, greater<pii> > pq;
    memset(dist, 0x3f, sizeof(dist));
    memset(done, 0, sizeof(done));
    
    if(del[1]) return;
    
    pq.push(make_pair(0,1)); dist[1]=0;
    while(!pq.empty()) {
        pii cur=pq.top(); pq.pop();
        int u=cur.second;
        if(done[u]) continue;
        done[u]=true;
        for(int j=head[u];j;j=E[j].next) {
            int v=E[j].v, len=E[j].len;
            if(!del[v] && dist[v] > dist[u] + len) {
                dist[v] = dist[u] + len;
                pq.push(make_pair(dist[v],v));
            }
        }
    }
}
void Init() {
    int u,v,c,p,a,b,d;
    scanf("%d%d%d%d", &T, &N, &K, &M);
    for(int i=1; i<=M; i++) {
        scanf("%d%d%d", &u, &v, &c);
        AddPair(u,v,c);
    }
    scanf("%d", &d);
    while(d--) {
        scanf("%d%d%d", &p, &a, &b);
        dif[p][a]++; dif[p][b+1]--;
    }
    
    //差分数组+前缀和 
    for(int u=1; u<=N; u++) {
        for(int i=1; i<=T; i++)
            dif[u][i]+=dif[u][i-1];
        for(int i=1; i<=T; i++)
            dif[u][i]+=dif[u][i-1];
    }
    
    //Dijkstra
    for(int t1=1; t1<=T; t1++)
        for(int t2=t1; t2<=T; t2++) {
            memset(del, 0, sizeof(del));
            for(int u=1; u<=N; u++)
                if(dif[u][t2]-dif[u][t1-1] != 0) { //disabled
                    del[u]=true;
                }
            Dijkstra();
            cost[t1][t2]=dist[N];
        }
}
void Work() {
    //DP
    //len=1 边界
    for(int len=1; len<=T; len++)
        for(int i=1; i+len-1<=T; i++) {
            int j=i+len-1;
            if(cost[i][j] != INF) //注意防止溢出！
                opt[i][j]=cost[i][j]*len; //一条路径代价*天数 
            else opt[i][j]=INF;
            for(int p=i; p<=j-1; p++)
                opt[i][j] = min(opt[i][j], opt[i][p] + opt[p+1][j] + K);
        } 
    printf("%d", opt[1][T]);
}
int main() {
    Init(); Work();
    return 0;
}
```

 [1]:https://www.luogu.org/problemnew/show/1772