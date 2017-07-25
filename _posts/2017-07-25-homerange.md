---
layout: post
comments: true
title: '[USACO]家的范围'
tags: ['二维平面DP','动态规划']
category: '解题报告'
---

链接：
[Luogu-P2733][1]

## 题意

在正方形的区域内，有一些点有标记，求出边长大于等于2的，内部没有标记的每种不同正方形个数。正方形可以重叠。

## 分析

 - 不同正方形的个数？
   我们知道DP题目的常用方法是“看题说话”。我们可以根据题目信息直接定义状态吗？确定这个区域内的某一个正方形的两个量，分别是右下角（或者左上角等）的位置$$(x,y)$$，以及它的边长。但是，以两者中的任意一个定义状态，都不方便写出转移方程。
怎么办呢？

<!--more-->

 - 考虑将计数问题转化为最优问题。
   计数问题和最优问题是动态规划研究的两类主要问题。其实，它们之间并不是没有关系的。
   考虑与本题相关的一个最优问题：
   以某个位置为右下角，最大的可能的正方形有多大？
   显然可以定义状态$$f(i,j)$$，表示以$$(i,j)$$为右下角的最大可能正方形的边长。
   （这里借用下[yangle61][2]课件里面的几张图）
   ![homerange01][https://panda2134.github.io/img/homerange01.png]
 - 进行状态转移，要对解做出限制
   当**$$(i,j)$$处本身不是障碍**时：

   画出这个可能的最大正方形，把有标记的方块，即障碍块沿着这个正方形的边界移动，试着去寻找它的大小和$$f(i-1,j)$$,$$f(i,j-1)$$之间的联系。
   ![homerange02][https://panda2134.github.io/img/homerange02.png]
   通过画图可以发现，一定有 $$f(i,j) \leq f(i-1,j) + 1$$, $$f(i,j) \leq f(i,j-1) + 1$$。
   这样就完全地限制了$$f(i,j)$$的取值吗？显然没有。如上图中2,4的情况，并没有被$$f(i-1,j)$$，$$f(i,j-1)$$严格地限制。
   ![homerange03][https://panda2134.github.io/img/homerange03.png]
   显然，$$f(i,j)$$还被$$f(i-1,j-1)$$所限制，即须有$$f(i,j) \leq f(i-1,j-1) + 1$$。
   再画画图，发现，这样就完全地限制了$$f(i,j)$$的取值。
 - 当**$$(i,j)$$处本身是障碍时**:显然$$f(i,j)=0$$

   状态转移方程：
   $$
	f(i,j)=\begin{cases}
	\min \begin{cases}
	f(i-1,j)+1  & \text{ 如果 } i \geq 2 \\ 
	f(i,j-1)+1  & \text{ 如果 } j \geq 2\\ 
	f(i-1,j-1)+1  & \text{ 如果 } i \geq 2 \text { 且 } j \geq 2
	\end{cases} \\
	0 \text{ 如果 (i,j) 被挡住 } 
	\end{cases}
   $$

## 代码

注意：为何不需要判断$$f(i,j)$$是否越界呢？

{%highlight cpp linenos%}
#include <cstdio>
#include <cstring>
#include <cctype>
#define min(x,y) (((x)>(y))?(y):(x))
#define max(x,y) (((x)<(y))?(y):(x))
using namespace std;
const int MAXN=250;
int N,Mx,f[MAXN+5][MAXN+5],T[10000010],Map[MAXN+5][MAXN+5];//True for obstacle
char readc(){
    char c=getchar();
    while(!isgraph(c)) c=getchar();
    return c;
}
int main(){
    scanf("%d",&N);
    for(int i=1;i<=N;i++)
        for(int j=1;j<=N;j++)
            Map[i][j]=(readc()=='0');
    for(int i=1;i<=N;i++)
        for(int j=1;j<=N;j++)
            if(!Map[i][j]){
                f[i][j]=min(
                    min(f[i-1][j],f[i][j-1]),
                    f[i-1][j-1]
                )+1;
                T[f[i][j]]++;
                Mx=max(Mx,f[i][j]);
            }
    for(int i=Mx;i>=3;i--)
        T[i-1]+=T[i];
    for(int i=2;i<=Mx;i++)
        if(T[i])
            printf("%d %d\n",i,T[i]);
    return 0;
}
{%endhighlight%}

 [1]:https://www.luogu.org/problem/show?pid=2733
 [2]:blog.csdn.net/yangle61