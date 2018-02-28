---
layout: post
comments: true
title: "莫队笔记"
categories: "笔记"
tags: ["分块","莫队"]
---



莫队是一种**离线**解决区间查询问题的算法。

记得 NOIP 之前那段时间，见到一道查询区间颜色种类数目的题目，标签是树状数组。想了很久也没有想出来怎么用树状数组做，看题解才知道有莫队这种逆天的东西……srOOrz

## 普通莫队

以查询区间颜色种类数目为例。为了方便，假定元素个数为 $$n$$ ，查询数目为 $$q$$ .

暴力开桶扫一遍，复杂度是 $$O(qn)$$ 的。有没有更高效的算法呢？

如果已经扫描到区间 $$[L,R]$$ ，那么转移到 $$[L, R+1]$$，  $$[L+1, R]$$，  $$[L, R-1]$$，  $$[L-1, R]$$， 都可以在 $$O(1)$$ 的复杂度内完成。既然是离线做，也许可以以某种顺序处理所有询问，利用相邻询问的共同信息，来达到较优化的复杂度。

如何利用呢？

<!--more-->

我们设 $$BlkSize = \sqrt{n}$$ ，并且以左端点**所在块的序号**为第一关键字，右端点为第二关键字，对所有询问进行排序。可以证明，当 $$n, q$$ 同阶时，这样的复杂度为 $$O(n^{\frac{3}{2}}) = O(n\sqrt{n})$$ 。

**证明**： 

> - 左端点在同一个块内时，由于此时右端点升序排序，所有的转移总共是 $$O(n)$$ 的。
>
> - 总共有 $$\sqrt{n}$$ 个块
>
> - 相邻块之间转移，左端点最多移动 $$2\sqrt{n}$$
>
>   $$\Rightarrow$$ 复杂度为 $$O(n\sqrt{n})$$

**总结**：只要在  $$[L, R+1]$$，  $$[L+1, R]$$，  $$[L, R-1]$$，  $$[L-1, R]$$ 之间转移可以 $$O(1)$$ / $$O(\lg{n})$$ 地进行，就可以使用莫队。

**代码**： [[SDOI2009]HH的项链][4]

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 5e4, MAXQ = 2e5, MAXC = 1e6;
int N, Q, BlkSize, L, R, NowAns, A[MAXN+10], M[MAXC+10], Ans[MAXQ+10];

struct Query {
    int L, R, id;
    Query() {}
    Query(int l, int r, int i): L(l),R(r),id(i) {}
    inline bool operator<(const Query& rhs) const {
        return L/BlkSize == rhs.L/BlkSize ? 
            R < rhs.R : L/BlkSize < rhs.L/BlkSize;
    }
} q[MAXQ+10];

template<typename T>
inline void readint(T& x) {
    T f=1, r=0; char c=getchar();
    while(!isdigit(c)){ if(c=='-')f=-1; c=getchar(); }
    while(isdigit(c)){ r=r*10+c-'0'; c=getchar(); }
    x = f*r;
}

inline char readc() { 
    char c=getchar();
    while(!isalnum(c) && !ispunct(c)) 
        c=getchar();
    return c;
}

inline void readstr(char *str) {
    char c=getchar(); int p=0;
    while(!isalnum(c) && !ispunct(c)) c=getchar();
    while(isalnum(c) || ispunct(c)) {
        str[p++]=c;
        c=getchar();
    }
    str[p]='\0';
}

void Init() {
    int u, v;
    readint(N); BlkSize = ceil(sqrt(N));
    for(int i=1; i<=N; i++) 
        readint(A[i]);
    readint(Q);
    for(int i=1; i<=Q; i++) {
        readint(u); readint(v);
        q[i] = Query(u, v, i);
    }
    sort(q+1, q+Q+1);
}

inline void Add(int Clr) {
    if(M[Clr]++ == 0) NowAns++;
}

inline void Sub(int Clr) {
    if(--M[Clr] == 0) NowAns--;
}

void Work() {
    L=1, R=0; NowAns=0;
    for(int i=1; i<=Q; i++) {
        while(R < q[i].R) Add(A[++R]);
        while(L > q[i].L) Add(A[--L]);
        while(R > q[i].R) Sub(A[R--]);
        while(L < q[i].L) Sub(A[L++]);
        Ans[q[i].id] = NowAns;
    }
    for(int i=1; i<=Q; i++)
        printf("%d\n", Ans[i]);
}

int main() {
    Init(); Work();
    return 0;
}
```



## 带修改莫队

其实就是给莫队加上了“时间”这个维度，自然我们可以想到把 $$L,R$$ 都分块，再排序处理。

若取分块大小 $$BlkSize = n ^ {\frac{2}{3}}$$ ，可以证明复杂度是 $$O(n^{\frac{5}{3}})$$ 的。

证明略。（其实是我不会证……）

注意实现上面的细节：先移动时间轴再调整 $$L,R$$ 。 因为在调整时间轴的时候，会先调整 $$L,R$$ 来把修改点纳入当前区间，所以在调整完时间后一定要把区间重新调整为查询区间。

代码：[[国家集训队]数颜色][5]

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1e4, MAXC = 1e6;
int N, Q, Q1, Q2, L, R, T, BlkSize, NowAns, M[MAXC+10], A[MAXN+10], B[MAXN+10], Ans[MAXN+10];

struct Query {
    int L, R, T, id;
    Query() {}
    Query(int l, int r, int t, int id_): L(l), R(r), T(t), id(id_) {}
    bool operator<(const Query& rhs) const {
        if(L/BlkSize == rhs.L/BlkSize) {
            if(R/BlkSize == rhs.R/BlkSize) 
                return T < rhs.T;
            else return R/BlkSize < rhs.R/BlkSize;
        } else return L/BlkSize < rhs.L/BlkSize;
    }
} q[MAXN+10];

struct Modify {
    int p, val, orig, id;
    Modify() {}
    Modify(int p_, int val_, int orig_, int id_): p(p_), val(val_), orig(orig_), id(id_) {}
} mod[MAXN+10];

template<typename T>
inline void readint(T& x) {
    T f=1, r=0; char c=getchar();
    while(!isdigit(c)){ if(c=='-')f=-1; c=getchar(); }
    while(isdigit(c)){ r=r*10+c-'0'; c=getchar(); }
    x = f*r;
}

inline char readc() { 
    char c=getchar(); 
    while(!isalnum(c) && !ispunct(c)) 
        c=getchar(); 
    return c; 
}

void Init() {
    static int u, v; char op;
    readint(N); readint(Q);
    BlkSize = ceil(pow(N, 0.67));
    for(int i=1; i<=N; i++) {
        readint(A[i]); B[i] = A[i];
    }
    for(int i=1; i<=Q; i++) {
        op = readc(); readint(u); readint(v);
        switch(op) {
            case 'Q':
                q[++Q1] = Query(u, v, Q2, i);
                break;
            case 'R':
                mod[++Q2] = Modify(u, v, B[u], i); 
                B[u] = v;
                break;
        }
    }
    sort(q+1, q+Q1+1);
}

inline void add(int Clr) {
    if(M[Clr]++ == 0) NowAns++;
}

inline void sub(int Clr) {
    if(--M[Clr] == 0) NowAns--;
}

inline void goforth(int t) {
    //先把修改点纳入当前区间！ 
    while(L > mod[t].p) add(A[--L]);
    while(R < mod[t].p) add(A[++R]);
    A[mod[t].p] = mod[t].val;
    sub(mod[t].orig); add(mod[t].val);
}

inline void goback(int t) {
    while(L > mod[t].p) add(A[--L]);
    while(R < mod[t].p) add(A[++R]);
    A[mod[t].p] = mod[t].orig; //改回去！
    sub(mod[t].val); add(mod[t].orig);
}

void Work() {
    L=1, R=0, T=0;
    for(int i=1; i<=Q1; i++) {
        while(T < q[i].T) goforth(++T);
        while(T > q[i].T) goback(T--); //先调整时间后调整区间
        while(R < q[i].R) add(A[++R]);
        while(L > q[i].L) add(A[--L]);
        while(R > q[i].R) sub(A[R--]);
        while(L < q[i].L) sub(A[L++]);
        Ans[q[i].id] = NowAns;
    }
    for(int i=1; i<=Q; i++) 
        if(Ans[i]) {
            printf("%d\n", Ans[i]);
        }
}

int main() {
    Init(); Work();
    return 0;
}
```



## 树上莫队

待填坑QAQ



## 参考链接

[传说中能解决一切区间处理问题的莫队算法是什么？][1]

[莫队算法学习笔记][2]

[莫队算法][3]



[1]: https://www.zhihu.com/question/27316467/answer/130423804
[2]: https://blog.sengxian.com/algorithms/mo-s-algorithm
[3]: https://zhuanlan.zhihu.com/p/25017840
[4]: https://www.luogu.org/problemnew/show/P1972
[5]: https://www.luogu.org/problemnew/show/P1903
