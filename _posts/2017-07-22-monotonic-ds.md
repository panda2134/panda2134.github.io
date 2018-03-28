---
layout: post
title: '单调数据结构学习笔记'
category: ["笔记"]
tags: ["单调栈","单调队列"]
comments: true
---

这里的“单调数据结构”，指的就是单调栈和单调队列。

## 单调栈

### 特点

先进的元素后出，求前/后缀最值。

### 实现

使用一个栈（~~这不是废话么233~~），每次在加入栈时维护单调性。不断弹出栈顶元素，直到栈顶元素大于将要加入
的元素，此时再将要加入的元素推入栈中。具体地讲，由于需要随机访问单调栈中的元素，
以便充分利用其单调的特性，常用一个数组来模拟栈。
<!--more-->
设`s[0]`为栈中元素个数，`s[1]~s[ s[0] ]`为栈中各个元素，于是可以简单地实现：

入栈:`s[++s[0]]=x;`

出栈:`s[0]--;`

取栈顶：`x=s[s[0]];`

用数组模拟栈实现单调栈的代码如下。此处实现的是自底向顶单调递减的单调栈。注意，我
们在栈中通常存储元素的下标/地址，以便于进行与元素顺序有关的统计。

```cpp
void insert(int* val,int* s,int idx){ //val为存放序列值的数组，s为单调栈，idx
                                      //为将要加入元素在val数组中的下标
  while(s[0]!=0 && val[s[s[0]]] < val[idx]) s[0]--;
  s[++s[0]]=x;
}
```
例题：[BZOJ-1012][1]
代码：
注意输入一个字符的实现，不然有的OJ会报错

```cpp
//BZOJ 1012
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cctype>
#include <cassert>
#include <deque>
#include <utility>
using namespace std;
const int MAXM = 200000;
int M,D,T,N;
int s[MAXM+10],val[MAXM+10];//st[0]->size
inline int readint(){

	int f=1,r=0;char c=getchar();
	while(!isdigit(c)){if(c=='-')f=-1;c=getchar();}
	while(isdigit(c)){r=r*10+c-'0';c=getchar();}
	return f*r;
} 
inline char readc(){
	char c=getchar();
	while(!isgraph(c)) //!
		c=getchar();
	return c;
}
int main(){
	M=readint();D=readint();
	while(M--){
		char c;int x;
		c=readc();x=readint();
		switch(c){
			case 'A':
				x=((1ll*x)%D+T%D)%D;
				val[++N]=x;
				while(s[0]!=0 && val[ s[s[0]] ] < x) s[0]--; //自底向顶单调递减
				s[++s[0]]=N;
				break;
			case 'Q':
				x=N-x+1;
				printf("%d\n",T=val[*lower_bound(s+1,s+s[0]+1,x)]);
				break;
		}
	}
}
```

## 单调队列

特点：先进队列的元素先出，维护某个滑动窗口的单调性。

怎么实现？求最大值，就保证队首是最大值，于是维护队首到队尾单调递减。求最小值，就保证队首是最小值，于是维护队首到队尾单调递增。

和单调栈一样，我们在单调队列中也一般保留元素的下标/地址。

滑动窗口。在 $O(n)$ 复杂度内求出区间内每一段长为 $W$ 的区间的最大或最小值。 直接用单调队列实现。不妨假设求最大值。元素入队时，弹出队尾所有小于等于它的元素，再插入。窗口向右边滑动的时候，检查队首元素下标是否等于离开窗口元素下标，如果是的话就弹出队首，否则什么都不做。要取窗口最大值的时候，检查队首元素即可。

例题：[Luogu-1886][2]

代码：

```cpp
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 1e6;
int N, K, A[MAXN+10], AnsMin[MAXN+10], AnsMax[MAXN+10];
deque<int> Q;
inline int readint() {
    int f=1,r=0; char c=getchar();
    while(!isdigit(c)) { if(c=='-')f=-1; c=getchar(); }
    while(isdigit(c)) { r=r*10+c-'0'; c=getchar(); }
    return f*r;
}
int main() {
    scanf("%d%d", &N, &K);
    for(int i=1; i<=N; i++) A[i]=readint();
    Q.clear();
    //Process Min
    for(int i=1; i<=K; i++) {
        while(!Q.empty() && A[Q.back()] > A[i]) Q.pop_back();
        Q.push_back(i);
    }
    AnsMin[K]=A[Q.front()];
    for(int i=K+1; i<=N; i++) {
        //Clear front
        while(!Q.empty() && Q.front() < i-K+1) Q.pop_front();
        //Clear end
        while(!Q.empty() && A[Q.back()] > A[i]) Q.pop_back();
        Q.push_back(i); AnsMin[i]=A[Q.front()];
    }
    Q.clear();
    //Process Max
    for(int i=1; i<=K; i++) {
        while(!Q.empty() && A[Q.back()] < A[i]) Q.pop_back();
        Q.push_back(i);
    }
    AnsMax[K]=A[Q.front()];
    for(int i=K+1; i<=N; i++) {
        //Clear front
        while(!Q.empty() && Q.front() < i-K+1) Q.pop_front();
        //Clear end
        while(!Q.empty() && A[Q.back()] < A[i]) Q.pop_back();
        Q.push_back(i); AnsMax[i]=A[Q.front()];
    }
    for(int i=K; i<=N; i++) printf("%d%c", AnsMin[i], " \n"[i==N]);
    for(int i=K; i<=N; i++) printf("%d%c", AnsMax[i], " \n"[i==N]);
    return 0;
}
```



[1]:http://www.lydsy.com/JudgeOnline/problem.php?id=1012
[2]:https://www.luogu.org/problemnew/show/P1886