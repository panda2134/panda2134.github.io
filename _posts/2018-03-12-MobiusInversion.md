---
layout: post
comments: true
title: "莫比乌斯反演学习笔记"
categories: "笔记"
tags: ["数论","莫比乌斯反演"]
---


## 莫比乌斯函数
            
我们定义    
              
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
                 
$$
\begin{equation} \sum_{d \backslash n} \mu (d) = [n = 1] \end{equation}
$$
              
下面我们来证明上式.     
           
当 $$n = 1$$ 时显然成立.      
             
当 $$n \ge 2$$ 时,不妨设 $$n = \prod_{i=1}^k p_i^{\alpha_i}$$.  $$n$$ 的恰含有 $$r$$ 个互异质因数的因子有$$\binom{k}{r}$$ 个.当它含有奇数个互异质因子时, 对答案贡献为 $$-1$$ , 含偶数个互异质因子时贡献为 $$1$$ .于是总的贡献为:           
              
$$
\begin{align*}
\sum_{d \backslash n} \mu (d) &= \binom{n}{0} - \binom{n}{1} + \binom{n}{2}- \cdots \\
&= \sum_{i=0}^k (-1)^i \binom{n}{i} \\
&= (1 - 1)^k \\
&= 0
\end{align*}
$$
                 
得证.    
              
从上面的证明过程可以看出, 其实莫比乌斯函数就是在模拟容斥原理, 不过容斥的对象是唯一分解式中的指数罢了. 把不同的质因数看成盒子, 指数看成球, 就转为了经典的球-盒模型.      

## 莫比乌斯反演
             
### 形式1:枚举约数
                   
$$
\begin{align}
F(n) = \sum_{d \backslash n} f(d) \Leftrightarrow f(n) = \sum_{d \backslash n} \mu(d) F(\frac{n}{d}) \\
\end{align}
$$
                    
证明:       
                  
$$\Rightarrow:$$           
            
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
          
$$\Leftarrow:$$    
           
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
           
### 形式2:枚举倍数
                
这个形式比较常用.           
              
我们不妨假设 $$n, d \le N$$ . 则:  
              
$$
F(n) = \sum_{n \backslash d}f(d) \Leftrightarrow f(n) = \sum_{n \backslash d} \mu(\frac{d}{n})F(d)
$$
             
这个比较难证明……想了好久……            
             
证明:            
                  
$$\Rightarrow:$$                        
                
$$
\begin{align*}
\sum_{n \backslash d} \mu(\frac{d}{n}) F(d) &= \sum_{k=1}^{+\infty}  \mu(k) F(nk) \\
&= \sum_{k=1}^{+\infty}\mu(k)\sum_{nk \backslash t} f(t) \\
&= \sum_{n \backslash t} f(t) \sum_{k \backslash (t / n)} \mu(k) \\
&= \sum_{n \backslash t} f(t) [t = n] \\
&= f(t)
\end{align*}
$$
                
$$\Leftarrow:$$              
                   
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







-----------------------------

参考链接:                

**强烈推荐:**[PoPoQQQ的PPT](https://wenku.baidu.com/view/fbec9c63ba1aa8114431d9ac.html)                 

[莫比乌斯反演定理证明](http://blog.csdn.net/outer_form/article/details/50588307)              

