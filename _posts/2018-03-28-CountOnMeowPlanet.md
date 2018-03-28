---
title: "[SCOI2012]喵星球上的点名"
layout: post
categories:
  - 解题报告
tags:
  - 后缀数组
  - 莫队
  - 树状数组
  - 字符串
comments: true
---

这个题最开始只会做第一问……（其实也不完全是自己做出来的，因为是在试炼场里面看到的）

后来去膜拜各路神犇的题解，想知道第二问怎么做，发现没几个看的懂的，全是什么后缀自动机/乱搞/暴力什么的……最无语的是据说 $O(nm)$ 暴力碾压正解……

>  暴力碾标算，$n^2$ 过十万

2333333

直到找到了雅礼的[dy神的题解](https://blog.csdn.net/dy0607/article/details/69053701)，才发现一个第二问的我看的懂的做法= =

太神辣！

## 题意

给定 $n$ 个名字和 $m$ 个串，问这 $m$ 个串中的每个在多少名字里面作为子串出现，以及每个人被点名多少次。

## 思路

子串显然可以想到LCP。我们进行后缀排序后求出`Height` 数组，然后对于每个串在后缀数组中二分找出出现的连续一段，这样就转为了多次询问区间颜色数量，直接上莫队模板。

第二问就比较妙了。第二问的等价表达方式是：给出一个序列 $\\{a_n\\}$ 上的 $m$ 个区间，求每种数字在多少个区间内出现过。

用莫队并不能做。直接差分然后乱搞的复杂度不对。我们不妨用扫描线，对每个位置分别计算相应的答案。

我们用容斥原理的思想：假设当前在点 $i$ ，那么这个位置的数对于答案贡献就等于 $a_i$ 和它上次出现的位置 $x$ 之间夹着的询问区间左端点数目（只有在这些区间内是第一次出现，也只有在某个区间内第一次出现才对答案有贡献），这等价于 $a_i$ 左侧的左端点数目减去 $x$ 左侧的左端点数目。为了快速维护这个信息，需要统计小于某个数字的值的和。同时，在扫描线向右边扫的时候，要相应地打开/关闭区间，即单点加。单点加，查前缀和，可以用权值树状数组维护。

复杂度 $O\left(n (\sqrt{n} + \lg n)\right)$ ，比暴力靠谱多了。

## 代码

有必要注意下后缀数组的写法：虽然字符串是 0-indexed 的，但是由于把最后的 `\0` 也纳入了字符串做结尾，后缀数组和`height` 数组都是 1-indexed 的。（当然输入字符串的时候也可以 1-indexed，不过传入`build_sa`的时候就需要给指针 +1）

```cpp
#include <bits/stdc++.h>
using namespace std;

extern int BlkSize;
struct Query {
    int idx, l, r;
    inline bool operator<(const Query &rhs) const {
        return (l / BlkSize == rhs.l / BlkSize) ? 
                r < rhs.r : l / BlkSize < rhs.l / BlkSize;
    }
};
struct Diff {
    int l, pos, val;
    inline bool operator<(const Diff &rhs) const {
        return pos < rhs.pos;
    }
};

const int MAXN = 2e5, SIGMA = 1e4+10;
int N, Q, BlkSize, len, nowans, s[MAXN+10], buf[3][MAXN+10], c[MAXN+10], belong[MAXN+10],
    sa[MAXN+10], rk[MAXN+10], height[MAXN+10], cnt[MAXN+10], ans[MAXN+10];
Query qry[MAXN+10];

void build_sa() {
    int p, m = SIGMA + 10, n = len + 1, *x = buf[0], *y = buf[1];
    for(int i = 0; i < m; i++) c[i] = 0;
    for(int i = 0; i < n; i++) ++c[x[i] = s[i]];
    for(int i = 1; i < m; i++) c[i] += c[i-1];
    for(int i = n-1; i >= 0; i--) sa[--c[x[i]]] = i;
    for(int k = 1; k <= n; k <<= 1) {
        p = 0;
        for(int i = n-k; i < n; i++) y[p++] = i;
        for(int i = 0; i < n; i++)
            if(sa[i] >= k) y[p++] = sa[i] - k;
        for(int i = 0; i < m; i++) c[i] = 0;
        for(int i = 0; i < n; i++) ++c[x[y[i]]];
        for(int i = 1; i < m; i++) c[i] += c[i-1];
        for(int i = n-1; i >= 0; i--) sa[--c[x[y[i]]]] = y[i];
        swap(x, y);
        p = 1, x[sa[0]] = 0;
        for(int i = 1; i < n; i++)
            x[sa[i]] = (y[sa[i]] == y[sa[i-1]] && y[sa[i]+k] == y[sa[i-1]+k] ? p-1 : p++);
        if(p >= n) break;
        m = p;
    }
    memcpy(rk, x, sizeof(rk));
    int k = 0;
    for(int i = 0; i < n; i++) {
        if(!rk[i]) continue;
        if(k) k--;
        int j = sa[rk[i]-1];
        while(s[i+k] == s[j+k]) k++;
        height[rk[i]] = k;
    }
}

inline int readint() {
    int f=1, r=0; char c=getchar();
    while(!isdigit(c)) { if(c=='-')f=-1; c=getchar(); }
    while(isdigit(c)) { r=r*10+c-'0'; c=getchar(); }
    return f*r;
}

void init() {
    int L1, L2;
    N = readint(); Q = readint();
    for(int i = 1; i <= N; i++) {
        L1 = readint();
        for(int j = 0; j < L1; j++) {
            s[len] = readint() + 1;
            belong[len] = i;
            len++;
        }
        s[len++] = SIGMA;
        L2 = readint();
        for(int j = L1; j < L1+L2; j++) {
            s[len] = readint() + 1;
            belong[len] = i;
            len++;
        }
        s[len++] = SIGMA;
    }
    BlkSize = sqrt(len); 
    build_sa();
}

int cmp_suffix(int *str, int p, int qrylen) {
    for(int i = 0; i < qrylen; i++)
        if(str[i] != s[sa[p]+i])
            return str[i] - s[sa[p]+i];
    return 0;
}

int sa_lbound(int *str, int qrylen) {
    int l = 1, r = len+1, mid;
    while(l < r) {
        mid = l + (r-l) / 2;
        if(cmp_suffix(str, mid, qrylen) <= 0)
            r = mid;
        else
            l = mid + 1;
    }
    return l;
}

int sa_ubound(int *str, int qrylen) {
    int l = 1, r = len+1, mid;
    while(l < r) {
        mid = l + (r-l) / 2;
        if(cmp_suffix(str, mid, qrylen) < 0)
            r = mid;
        else
            l = mid + 1;
    }
    return l;
}

void add(int x) {
    int clr = belong[sa[x]];
    if(cnt[clr]++ == 0) nowans++;
}

void sub(int x) {
    int clr = belong[sa[x]];
    if(--cnt[clr] == 0) nowans--;
}

void work1() {
    static int l, r, QryLen, str[MAXN+10], mark[MAXN+10];
    for(int i = 1; i <= Q; i++) {
        QryLen = readint();
        for(int j = 0; j < QryLen; j++)
            str[j] = readint() + 1;
        qry[i].idx = i;
        qry[i].l = sa_lbound(str, QryLen);
        qry[i].r = sa_ubound(str, QryLen) - 1;
        if(qry[i].l <= len) {
            mark[qry[i].l]++; mark[qry[i].r+1]--;
        }
    }
    sort(qry + 1, qry + Q + 1);
    l = 1, r = 0; nowans = 0;
    for(int i = 1; i <= Q; i++) {
        if(qry[i].l > len) {
            ans[qry[i].idx] = 0;
            continue;
        } else {
            while(r < qry[i].r) add(++r);
            while(l > qry[i].l) add(--l);
            while(r > qry[i].r) sub(r--);
            while(l < qry[i].l) sub(l++);
            ans[qry[i].idx] = nowans;
        }
    }
    for(int i = 1; i <= Q; i++)
        printf("%d\n", ans[i]);
}

int bit[MAXN+10], prv[MAXN+10]; Diff D[(MAXN+10)<<1];
inline int lowbit(int x) { return x & (-x); }
inline int sum(int p) {
    int ret = 0;
    while(p > 0) {
        ret += bit[p];
        p -= lowbit(p);
    }
    return ret;
}
inline void add(int p, int val) {
    while(p <= len) {
        bit[p] += val;
        p += lowbit(p);
    }
}

void work2() {
    int p = 1;
    memset(ans, 0, sizeof(ans));
    for(int i = 1; i <= Q; i++) {
        D[i] = (Diff){ qry[i].l, qry[i].l, 1 };
        D[i+Q] = (Diff){ qry[i].l, qry[i].r+1, -1 };
    }
    sort(D+1, D+2*Q+1);
    for(int i = 1; i <= len; i++) {
        while(p <= 2*Q && D[p].pos <= i)
            add(D[p].l, D[p].val), p++;
        int &x = prv[belong[sa[i]]];
        ans[belong[sa[i]]] += sum(i) - sum(x);
        x = i;
    }
    for(int i = 1; i <= N; i++) printf("%d%c", ans[i], " \n"[i==N]);
}

int main() {
    init(); 
    work1(); work2();
    return 0;
}
```



## 后记

不会使用搜索引擎对学OI真是有不小的障碍呢……查各种题解都查了半个下午……
