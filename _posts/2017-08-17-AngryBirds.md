---
layout: post
categories: ["解题报告"]
tags: ["状压DP","数学"]
comments: true
title: "[NOIP2016]愤怒的小鸟"
---

题目链接：

LYOJ:~~[愤怒的南小鸟](https://ly.men.ci/problem/104)~~

Luogu:[愤怒的小鸟](https://www.luogu.org/problem/show?pid=2831)


题目较长，请在OJ上查看

<!--more-->

### 目录
* toc
{:toc}

## 0.题记
还记得去年NOIP赛场上看到这个题就懵了。

当时还剩下30min，写到这道题，发现题目中有了抛物线，以为要用高斯消元法什么的解出函数方程，果断放弃……

后来才发现，完全可以设出抛物线的方程和过抛物线的亮点，用初中知识解出方程。这一步解决后，就是不讲任何技巧的状压DP都能拿75pts以上

果然还是自己太弱了……希望今年不要再这样懵逼了。

## 1.审题
你在玩愤怒的小鸟的一关，可以发射小鸟，小鸟经过猪则猪被消灭。求消灭所有猪需要的小鸟数量。

由 $ 2 \le n \le 18 $ 可知应该使用状压DP。于是考虑设计状态，显然可以把已经打死的猪加入状态之中。

## 2.思路

### 状压动规
设在消灭的猪的集合为 $S$ 的时候，还需要 $f(S)$ 只小鸟可以消灭所有猪。于是有状态转移方程：
$$
f(S)=\begin{cases}
	f(S \cup S')+1 \: | \: S'为这次打下的猪的集合 & \text{ 若 } |S|<n \\ 
    0& \text{ 若 } |S|=n 
\end{cases}
$$
然后考虑如何处理出转移方程中的$S'$，也就是如何计算抛物线。

### 处理抛物线

注意到一定要分两种情况进行讨论：

1. 消灭的猪大于等于2只
2. 消灭的猪为1只

#### 情况1
考虑设出两只猪的坐标 $(x_1,y_1)$ 和 $(x_2,y_2)$ 
由初中知识可以列出方程：

$$\left\{\begin{matrix}
ax_1^2+bx_1=y_1 \\ 
ax_2^2+bx_2=y_2 \\ 
\end{matrix}\right.
$$

联立方程可以解出：

$$
\left\{\begin{matrix}
a=\frac{y_2 x_1 - y_1 x_2}{ x_1 x_2 (x_2-x_1) } & \\ 
b=\frac{y_1 x_2^2 - y_2 x_1^2} {x_1 x_2 (x_2-x_1)} & \\ 
\end{matrix}\right.
$$

涉及到数学表达式，应该关注是否合法！
1. 二次函数：$a \neq 0 \Rightarrow x_1 y_2 - x_2 y_1 \neq 0$ 
2. 分母显然不能为0：$x_1 x_2 (x_1-x_2) \neq 0$。其中 $x_1,x_2$ 题中已经保证了是正数，因此需要特判 $x_1 = x_2$ 的情况。

#### 情况2
显然对于第二种情况，任意作一条过$(0,0)$和猪坐标的抛物线即可达到目的。

### 陷阱和处理

如果你照着上面打出来了，应该是75分左右，最后几组绝对会TLE。

为什么呢？浮点数运算太慢了！

我们应该考虑进行预处理，缓存某两个点和原点确定的抛物线上面有哪些猪，而不是每次要用的时候再计算抛物线，这样就可以AC了。

## 3.代码

``` cpp
#include <cstdio>
#include <cstring>
#include <cstdlib>
#define INF 0x3f3f3f3f
#define eps 1e-9
#define CLEAR(x) memset(x,0,sizeof(x))
#define SETINF(x) memset(x,0x3f,sizeof(x))
#define min(x,y) (x<y?x:y)
#define pow2(x) (x*x)
#define abs(x) ((x-eps)>0?(x):(-(x)))


using namespace std;
const int MAXN = 18;
struct Pt {
    double x,y;
} Point[MAXN+5];
int T,N,M,Mx,Lim,used[(1<<MAXN)+10],opt[(1<<MAXN)+10];
int shoot[MAXN+10][MAXN+10];//Process the points on the parabola
                          //determined by (0,0) and two other points
bool vis[(1<<MAXN)+10];

inline void InitShoot() {
    for(register int i=1; i<=N; i++)
        for(register int j=1; j<=N; j++)
            if( i!=j && abs(Point[i].x-Point[j].x) > eps //分母非0
                    && abs(Point[i].x*Point[j].y-Point[j].x*Point[i].y) > eps ) { //直线不是抛物线
                register double a=(Point[j].x*Point[i].y-Point[i].x*Point[j].y)
                         / (Point[i].x*Point[j].x*(Point[i].x-Point[j].x));
                register double b=(pow2(Point[i].x)*Point[j].y-pow2(Point[j].x)*Point[i].y)
                         / (Point[i].x*Point[j].x*(Point[i].x-Point[j].x));
                if(a>=eps) continue;
                for(register int k=1; k<=N; k++){
                    register double x=Point[k].x,y=Point[k].y;
                    if(abs(y-(a*pow2(x)+b*x))<eps)
                        shoot[i][j]|=(1<<(k-1));
                }        
            }
}
inline void Init() {
    scanf("%d %d",&N,&M);
    for(register int i=1; i<=N; i++)
        scanf("%lf %lf",
              &Point[i].x,&Point[i].y);
    Mx=(1<<N)-1;
    InitShoot();
}
int dfs(int s) {
    if(vis[s]) return opt[s];
    vis[s]=true;
    if(s==Mx) return opt[s]=0; // !!!!!!!
    for(int i=1;i<=N;i++)
        if((s&(1<<(i-1)))==0) {//Not Shoot
            register int m=(s|(1<<(i-1)));
            dfs(m);
            opt[s]=min(opt[s],opt[m]+1);
        }
    for(register int i=1;i<=N;i++)
        for(register int j=i+1;j<=N;j++)
            if((((1<<(i-1))&s)==0) && (((1<<(j-1))&s)==0)) { //Not Shoot
                register int m=shoot[i][j];
                if((s|m)==s) continue;
                else m|=s;
                dfs(m);
                opt[s]=min(opt[s],opt[m]+1);
            }
    return opt[s];
}
inline void Work() {
    printf("%d\n",dfs(0));
}
inline void Clear() {
    N=M=Mx=0;
    SETINF(opt);
    CLEAR(vis);
    CLEAR(used);
    CLEAR(shoot);
}
int main() {
    scanf("%d",&T);
    while(T--) {
        Clear();
        Init();
        Work();
    }
    return 0;
}
```

**UPD:**在uoj会被卡精度。换成long double就好了。