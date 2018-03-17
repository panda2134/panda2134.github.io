---
layout: post
comments: true
categories: ['解题报告']
tags: ['序列型DP','动态规划','LCS']
title: '浴谷八连测-R6-A - 不可逆的重启动'
---

## 题意
求两个串$A$,$B$的最长公共子序列。    
对于70%的数据，满足 $|A|,|B| \leq 1000$      
对于100%的数据，满足 $|A| \leq 10^{6},|B| \leq 1000$，所有字符都是小写字母。      
<!--more-->
##思路
首先对于70分的数据直接求LCS就行。     
对于100分的数据呢？         
在DP中，我们常常通过改变状态来进行优化。如果把答案也看成是一维的话，那么可以把“答案”这个维度和其他维度进行对调来转换状态，把最优性问题转为可行性问题。原来的DP是枚举参数计算答案，改变后的状态就是枚举部分参数和答案来计算其他参数。最后只要枚举答案看是否可行即可。       
比如本题。我们都知道通常的LCS的状态是：     
\\[ f(i,j):两个串的第i个和第j个位置往后的LCS长度 \\]
不妨试着把长度和$j$这个维度对调。我们设第一个串比较短。这样的话，状态就是：     
\\[ f(i,j):第一个串的第i个位置待匹配，i之前的LCS长度为j，第二个串上次匹配成功的位置 \\]
注意对于序列DP问题，搞清**当前位置有没有被纳入所求量**是正确转移的关键。如此处的$i$就没有纳入LCS。      
然后刷表即可。用$f(i,j)$去更新$f(i+1,j)$和$f(i+1,To_{f(i,j), A_i})$
其中$To_{i, c}$表示第二个串位置$i$往右最近的一个字符c的位置，可以预处理得到。      
为什么转移到最近的呢？稍微考虑就可以知道，如果有多个位置可以选择，转移到最近的位置，给剩余部分LCS留下的“空间”就越大。也就是说，转移到最近位置，答案不会更坏。       
时间复杂度是$O(26|A|+|B|^2)$。

## 代码
```cpp
#include <bits/stdc++.h>
#define idx(ch) ((ch)-'a')
#define chr(ch) ((ch)+'a')
#define UpMin(x,y) ((x)=min((x),(y)))
using namespace std;
const int LLONG = 1e6, LSHORT = 1e3, INF = 0x3f3f3f3f;
char A[LSHORT+10], B[LLONG+10];
int LA, LB, To[LLONG+5][26], opt[LSHORT+5][LSHORT+5];
void readstr(char* str) {
	char c=getchar(); int p=0;
	while(!isprint(c)) c=getchar();
	while(isprint(c)) {
		str[p++]=c;
		c=getchar();
	}
	str[p]='\0';
}
int main() {
	readstr(B+1); readstr(A+1);
	LA=strlen(A+1); LB=strlen(B+1);
	
	//预处理位置,没有下一个时设置为无穷大
	for(int i=LB; i>=0; i--) 
		for(int j=0; j<26; j++) {
			if(chr(j) == B[i+1]) To[i][j]=i+1;
			else To[i][j]=To[i+1][j];  
			if(To[i][j] == 0) To[i][j]=INF;
		}
		
	memset(opt, 0x3f, sizeof(opt));
	opt[1][0]=0;
	//DP
	for(int i=1; i<=LA; i++)
		for(int j=0; j<=i; j++) 
			if(opt[i][j] < INF) {
				UpMin(opt[i+1][j], opt[i][j]);
				UpMin(opt[i+1][j+1], To[opt[i][j]][idx(A[i])]);
			}
	for(int i=LA; i>=0; i--)
		if(opt[LA+1][i] < INF) {
			printf("%d", i); break;
		}
	return 0;
}

```
