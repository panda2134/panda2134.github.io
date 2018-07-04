---
layout: post
comments: true
title: "莫比乌斯反演学习笔记"
categories: "笔记"
catalog: true
tags: ["数论","莫比乌斯反演"]
---


## 莫比乌斯函数

我们定义    
​                
$$
\begin{equation}
\mu(n) = \begin{cases}
	1 & \text{当} n = 1 \\
	(-1)^k & \text{当}n \text{为} k \text{个互异质数的积} \\
	0 & \text{当} n \text{某个质因子次数大于等于} 2
\end{cases}
\end{equation} \label{mobius-func}
$$

为什么这么定义?为了满足性质:      
​                 
$$
\begin{equation} \sum_{d \backslash n} \mu (d) = [n = 1] \end{equation}
$$

下面我们来证明上式.     
​           
当 $n = 1$ 时显然成立.      
​             
当 $n \ge 2$ 时,不妨设 $n = \prod_{i=1}^k p_i^{\alpha_i}$.  $n$ 的恰含有 $r$ 个互异质因数的因子有$\binom{k}{r}$ 个.当它含有奇数个互异质因子时, 对答案贡献为 $-1$ , 含偶数个互异质因子时贡献为 $1$ .于是总的贡献为:           
​              
$$
\begin{align*}
\sum_{d \backslash n} \mu (d) &= \binom{n}{0} - \binom{n}{1} + \binom{n}{2}- \cdots \\
&= \sum_{i=0}^k (-1)^i \binom{n}{i} \\
&= (1 - 1)^k \\
&= 0
\end{align*}
$$

得证.    
​              
从上面的证明过程可以看出, 其实莫比乌斯函数就是在模拟容斥原理, 不过容斥的对象是唯一分解式中的指数罢了. 把不同的质因数看成盒子, 指数看成球, 就转为了经典的球-盒模型.      

## 莫比乌斯反演

### 形式1:枚举约数

$$
\begin{align}
F(n) = \sum_{d \backslash n} f(d) \Leftrightarrow f(n) = \sum_{d \backslash n} \mu(d) F(\frac{n}{d}) \\
\end{align}
$$

证明:       
​                  
⇒:        
​            
$$
\begin{align*}
	\sum_{d \backslash n} \mu(d) F(\frac{n}{d})	&= \sum_{d \backslash n} \mu(d) \sum_{k \backslash (n/d)} f(k) \\
	&= \sum_{d \backslash n} \sum_{k \backslash (n/d)} \mu(d) f(k) \\
	&= \sum_{k \backslash n} \sum_{d \backslash (n/k)} \mu(d) f(k) \\
	&= \sum_{k \backslash n} f(k) \sum_{d \backslash (n/k)} \mu(d) \\
	&= \sum_{k \backslash n} f(k) [n = k] \\
	&= f(n)
	\end{align*}
$$

⇐:    
​           
$$
\begin{align*}
	\sum_{d \backslash n} f(d) &= \sum_{d \backslash n} \sum_{k \backslash d} \mu(k) F(\frac{d}{k}) \\
	&= \sum_{p \backslash n} \sum_{q \backslash (n/p)} \mu(p) F(q) \tag{Rocky Road方法}\\
	&= \sum_{q \backslash n} \sum_{p \backslash (n/q)} \mu(p) F(q) \\
	&= \sum_{q \backslash n} F(q) \sum_{p \backslash (n/q)} \mu(p) \\
	&= \sum_{q \backslash n} F(q) [n = q] \\
	&= F(n)
	\end{align*}
$$

得证.          
​           
### 形式2:枚举倍数

这个形式比较常用.           
​              
我们不妨假设 $n, d \le N$ . 则:  
              
$$
F(n) = \sum_{n \backslash d}f(d) \Leftrightarrow f(n) = \sum_{n \backslash d} \mu(\frac{d}{n})F(d)    
$$

这个比较难证明……想了好久……             
​             
证明:            
​                  
⇒:                        
​                
$$
\begin{align*}
\sum_{n \backslash d} \mu(\frac{d}{n}) F(d) &= \sum_{k=1}^{+\infty}  \mu(k) F(nk) \\
&= \sum_{k=1}^{+\infty}\mu(k)\sum_{nk \backslash t} f(t) \\
&= \sum_{n \backslash t} f(t) \sum_{k \backslash (t / n)} \mu(k) \\
&= \sum_{n \backslash t} f(t) [t = n] \\
&= f(t)
\end{align*}
$$

⇐:            
​                   
$$
\begin{align*}
	\sum_{n \backslash d} f(d)  &= \sum_{k=1}^{+\infty}f(nk) \\
	&= \sum_{k=1}^{+\infty} \sum_{nk \backslash m} \mu(\frac{m}{nk}) F(m) \\	
	&= \sum_{k=1}^{+\infty} \sum_{t=1}^{+\infty} \mu(t) F(nkt) \\	
	&= \sum_{t=1}^{+\infty} \mu(t) \sum_{k=1}^{+\infty} F(nkt) \\
	&= \sum_{k=1}^{+\infty} F(nk) \left(\sum_{p \backslash k} \mu(p)\right) \\
	&= \sum_{k=1}^{+\infty} F(nk) [k = 1] \\
	&= F(n)
	\end{align*}
$$

得证.            

## 一点重要的结论

$$
n = \sum_{d \backslash n}\varphi(d)   \tag{欧拉函数的狄利克雷前缀和}
$$

证明1：利用法里级数    
这是《具体数学》的证明方法。名字很玄乎，其实很直观。

我们考察以 $n$ 为底的所有真分数和1一起组成的集合。不妨假设 $n=12$ . 则这些分数是：    

$$
\frac{1}{12}, \frac{2}{12}, \frac{3}{12}, \frac{4}{12}, \frac{5}{12}, \frac{6}{12}, \frac{7}{12}, \frac{8}{12}, \frac{9}{12}, \frac{10}{12}, \frac{11}{12}, \frac{12}{12}
$$

化简后就变成了：      

$$
\frac{1}{12},\frac{1}{6},\frac{1}{4},\frac{1}{3}, \frac{5}{12}, \frac{1}{2}, \frac{7}{12}, \frac{2}{3}, \frac{3}{4}, \frac{5}{6}, \frac{11}{12}, \frac{1}{1}
$$

按照分母分个组：    

$$
\left(\frac{1}{1}\right),\left(\frac{1}{2}\right), \left(\frac{1}{3}, \frac{2}{3}\right), \left(\frac{1}{4}, \frac{3}{4}\right), \left(\frac{1}{6}, \frac{5}{6}\right),\left( \frac{1}{12}, \frac{5}{12}, \frac{7}{12}, \frac{11}{12}\right)
$$

分母里面出现了 $n$ 的每个约数 $d$ . 对于每个约数 $d$ 对应的分组，分子上出现了 $\varphi(d)$ 个小于等于 $d$ 且与之互质的数。总共又有 $n$ 个分数。也就是说所有约数的 $\varphi(n)$ 之和就是 $n$ . 写成式子就是上式。得证。

证明2：利用 $\mu$ 函数的性质，构造出 $\mu(n)$ ，再使用莫比乌斯反演消去（%Anoxiacxy）

$$
\begin{align*}
\varphi(n) &= \sum_{1 \le i \le n} [i \perp n] \\
&= \sum_{1 \le i \le n} \sum_{d  \backslash \text{gcd}(i, n)} \mu(d) \\
&= \sum_{d \backslash n} \sum_{1 \le i \le n} \mu(d) [d \backslash i] \\
&= \sum_{d \backslash n} \mu(d) \frac{n}{d} \\
&\Rightarrow n = \sum_{d \backslash n} \varphi(n)
\end{align*}
$$

QED.

## 例题

一点感想：做数论题目一定要等忘了题解再做一次！这样才能看出你真正掌握没有！

### BZOJ2440 完全平方数

求小于等于 $n$ 的无平方因子数个数。双倍经验：vijos天真的因数分解。

这个题一开始是看的PoPoQQQ的PPT，当时觉得很简单。今天看到那个双倍经验题，想了好久，甚至想到了杜教筛，却没想到更简单的方法……然而并不会杜教筛……

下面是一种利用容斥的方法：

答案= $n$ $-$ $1$个质数平方倍数的数目 $+$ $2$个不同质数乘积的平方倍数的数目 $-$ $3$个不同质数乘积平方倍数的数目 ……

要求“不同质数”，是为了避免重复统计。（“倍数”可以增加乘积中质因数的指数）有相同质因数的数字对答案贡献为0，这也与 $\mu$ 函数对应。

这个式子和莫比乌斯函数定义的容斥含义是一样的！！！即 $\mu(n) = (-1)^k,\text{当} n= p_1^{\alpha_1} p_2^{\alpha_2} \cdots p_k^{\alpha_k}$ 。

>  奇数个互异质数为负，偶数个互异质数为正，质因子不互异贡献为0.是莫比乌斯函数作为容斥系数的要点。

$\Rightarrow \text{ans} = \sum_{d=1}^{\sqrt{n}} \mu(d) \left\lfloor\frac{n}{d^2}\right\rfloor$ . 可以整除分块求出。复杂度为 $O(n^{1/4})$ （不知道是不是算错了= =）

### BZOJ2301 [HAOI2011]Problem b
莫比乌斯反演+数论分块，达到单组询问 $O(\sqrt{n})$ 的复杂度。

### BZOJ3529 [SDOI2014] 数表

多组数据，直接类似求 $\sum_{i=1}^n\sum_{j=1}^m[\gcd(i, j) = d]$ 的暴力整除分块显然用不了。

考虑化式子，化成整除分块的量与数据无关的形式。

先考虑没有 $a$ 的限制怎么做。设 $n \le m$ ，如果 $n > m$ 将二者交换即可。

注意灵活地在枚举所有约数和所有倍数之间转换。
$$
\begin{align*}
\sum_{i=1}^n \sum_{j=1}^m \sigma\left(\gcd(i, j)\right) &= \sum_{k=1}^n\sigma(k)\sum_{i=1}^n \sum_{j=1}^m[\gcd(i, j) = k] \\
&= \sum_{k=1}^n \sigma(k) \sum_{k \backslash d}\mu\left(\frac{d}{k}\right)\left\lfloor\frac{n}{d}\right\rfloor\left\lfloor\frac{m}{d}\right\rfloor \\
&= \sum_{d=1}^n \sum_{k \backslash d}\sigma(k) \mu\left(\frac{d}{k}\right)\left\lfloor\frac{n}{d}\right\rfloor\left\lfloor\frac{m}{d}\right\rfloor \\
&= \sum_{d=1}^n \left\lfloor\frac{n}{d}\right\rfloor\left\lfloor\frac{m}{d}\right\rfloor \sum_{k \backslash d}\sigma(k) \mu\left(\frac{d}{k}\right) \\
\end{align*}
$$

设 $\gamma = \sigma * \mu$，我们可以筛出 $\sigma, \mu$ 后通过枚举倍数来在 $O(n \log n)$ 的复杂度内求出 $\gamma$ 函数。

于是上式$\:= \sum_{d=1}^n \left\lfloor\frac{n}{d}\right\rfloor\left\lfloor\frac{m}{d}\right\rfloor \gamma(d) $。

当有了 $a$ 的限制后，只有 $\sigma(k) \le a$ 的对答案有贡献。把询问离线，并按照 $a$ 排序，每次加入一部分 $\gamma(n)$ 的函数值，并求出前缀和——这可以用树状数组实现。每次对于一个 $\sigma(k)$ 枚举它的倍数，然后加入树状数组。

---


参考链接:                

**强烈推荐:**
 - [PoPoQQQ的PPT](https://wenku.baidu.com/view/fbec9c63ba1aa8114431d9ac.html)                 
 - [莫比乌斯反演定理证明](http://blog.csdn.net/outer_form/article/details/50588307)              
