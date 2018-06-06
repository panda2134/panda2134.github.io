---
layout: post
comments: true
title: "最长回文子串"
categories:
  - 解题报告
tags:
  - 哈希
  - 字符串
  - 二分
  - 线段树
  - 数据结构
  - 标记永久化
---

[Luogu-P4555](https://www.luogu.org/problemnew/solution/P4555)

## 题意

标题即题意。注意两个子串不能重复。

## 思路

并不会 $\text{Manacher}$ ，所以脑补了一种 $O(n \lg n)$ 的做法。

首先考虑转化所有偶数长度回文串。每个字符之间以及开头结尾插入 `#` 即可全部转为奇数长度。

然后可以维护正反串 Hash，每次枚举回文中心并且枚举回文串一半的长度。但是这样是 $O(n^2)$ 的。这个长度显然满足单调和有界性，类似求 $\text{LCP}$ ，可以二分它。于是我们就处理出了以每个点为回文中心的最长回文串。

类似 \[NOI2016\] 优秀的拆分，考虑用 `pre[], suf[]` 表示某个点往左，往右的最长回文串。显然，最长双回文串由两个极长回文串拼接而成。

如何求出这两个数组呢？实际上求出每个回文中心的回文串长后，可以注意到这个回文串以及它的同回文中心的子串对左右的贡献成等差数列，以对于 `pre[] `的贡献为例，如图：

![eg](/img/doublepalindrome.jpg)

于是问题就变成了：

1. 区间加 $a_0 = 1, d = 1$ 的等差数列
2. 单点求值。

我们用线段树实现。（感谢Claris神犇和Anoxiacxy同学）

考虑维护数组 $b_i$，$b_i = a_i - i$，所以初始时 $b_i = -i$。于是操作1就变为 $\{b_n\}$ 的区间 chkmax ，也就是对于 $[l, r]$ 的区间加等差数列，转为了在 $\{b_n\}$ 中 $[l, r]$ 对于 $-i+1$ 去 chkmax。

考虑 chkmax 的实现。可以采取标记永久化，不下放线段树标记，在查询单点的时候返回树上所有祖先和叶子的 $\max$ 即可。

最后统计答案的时候，只需在 `#` 处加以统计。

## 代码

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef unsigned long long ull;

const int MAXN = 3e5, INF = 0x3f3f3f3f;
const ull base = 1313;
int n, ans, pre[MAXN + 10], suf[MAXN + 10];
char s0[MAXN + 10], s[MAXN + 10], *ptr = &s[1];
ull powbase[MAXN + 10], hval[MAXN + 10], hrev[MAXN + 10];

struct SegTree {
#define lc(o) ((o) << 1)
#define rc(o) ((o) << 1 | 1)
    int sumv[(MAXN + 10) << 2], setv[(MAXN + 10) << 2];

    SegTree() { fill(setv, setv + ((MAXN + 10) << 2), -INF); }

    void maintain(int o, int l, int r) {
        if(l != r) sumv[o] = sumv[lc(o)] + sumv[rc(o)];
        if(setv[o] != -INF) sumv[o] = setv[o] * (r - l + 1);
    }

    void build_tree(int o, int l, int r) {
        if(l == r)
            setv[o] = -l;
        else {
            int mid = (l + r) >> 1;
            build_tree(lc(o), l, mid);
            build_tree(rc(o), mid + 1, r);
        }
        maintain(o, l, r);
    }

    void cover(int o, int l, int r, int ql, int qr, int val) {
        if(ql > qr) return;
        if(ql <= l && r <= qr)
            setv[o] = max(setv[o], val);
        else {
            int mid = (l + r) >> 1;
            if(ql <= mid) cover(lc(o), l, mid, ql, qr, val);
            if(qr >= mid + 1) cover(rc(o), mid + 1, r, ql, qr, val);
        }
        maintain(o, l, r);
    }

    int query(int o, int l, int r, int p) {
        maintain(o, l, r);
        if(l == r)
            return sumv[o];
        else {
            int mid = (l + r) >> 1;
            if(p <= mid)
                return max(setv[o], query(lc(o), l, mid, p));
            else
                return max(setv[o], query(rc(o), mid + 1, r, p));
        }
    }
#undef lc
#undef rc
} seg1, seg2;

inline ull get_hash(ull h[], int l, int r) {
    return h[r] - h[l - 1] * powbase[r - l + 1];
}

inline int odd_palindrome(int p) {  // p是回文中心
    int l = 1, r = n + 1;
    while(l < r) {
        int mid = (l + r) >> 1;
        if(mid <= max(p, n - p + 1) &&
           get_hash(hval, p, p + mid - 1) ==
               get_hash(hrev, n - p + 1, n - p + mid))
            l = mid + 1;
        else
            r = mid;
    }
    return l - 1;
}

int main() {
    scanf("%s", &s0[1]);
    n = strlen(s0 + 1);
    *(ptr++) = '#';
    for(int i = 1; i <= n; i++) {
        *(ptr++) = s0[i];
        *(ptr++) = '#';
    }
    n = strlen(s + 1);

    powbase[0] = 1;
    for(int i = 1; i <= MAXN; i++) powbase[i] = powbase[i - 1] * base;
    for(int i = 1; i <= n; i++) hval[i] = hval[i - 1] * base + s[i];
    for(int i = 1; i <= n; i++) hrev[i] = hrev[i - 1] * base + s[n - i + 1];

    seg1.build_tree(1, 1, n);
    seg2.build_tree(1, 1, n);

    for(int i = 1; i <= n; i++) {
        int len;
        len = odd_palindrome(i);
        seg1.cover(1, 1, n, i, i + len - 1, -i + 1);
        seg2.cover(1, 1, n, n - i + 1, n - i + len, -n + i);
    }
    for(int i = 1; i <= n; i++) pre[i] = i + seg1.query(1, 1, n, i);
    for(int i = 1; i <= n; i++) suf[i] = i + seg2.query(1, 1, n, i);
    reverse(suf + 1, suf + n + 1);
    for(int i = 2; i <= n - 1; i++)
        if(s[i] == '#') ans = max(ans, pre[i - 1] + suf[i + 1]);
    printf("%d\n", ans);
    return 0;
}
```

