---
layout: post
comments: true
title: "NOI知识点总结"
category:
 - 总结
---

NOI 在即，对所有做过的题进行复习，并总结常用算法和数据结构的技巧。

参考了[这个技能树](https://panda2134.github.io/img/技能树.jpg)。原作者不清，但是是在廖哥博客下载的，感谢原作者和廖哥。

## 动态规划

## 数据结构

### 哈夫曼树

- 学会把题目加入的新限制转为数据结构原有的限制！对于 $k$ 叉哈夫曼树，如果 $(n-1)\bmod{k-1} \ne 0$，那么就要补点使得 $(n-1)$ 是 $(k-1)$ 的倍数，这样才能使得深的节点尽可能少。

### 线段树

- 线段树上二分涉及查询某个点向一个方向连续值相同区间的时候，不需要在外面套一个二分。只需要讨论当前区间 $[L, R]$ 是否完整包含查询区间，然后进行转移。

  ```cpp
  int query_same(int o, int l, int r, int ql) { // 假设是向右查询均为 1 的区间
      maintain(o, l, r);
      if(ql <= l) { // 完全包含，直接二分，能返回马上返回
          if(l == r) return andv[o] == FULL ? l : ql - 1;
          
          if(andv[o] == FULL) return r;
          else {
              int ret = ql - 1, mid = (l + r) / 2;
              pushdown(o); // !
              maintain(lc(o), l, mid), maintain(rc(o), mid+1, r);
              if(andv[lc(o)] == FULL) {
                  ret = max(ret, mid);
                  ret = max(ret, query_same(rc(o), mid + 1, r, ql));
              } else {
                  ret = max(ret, query_same(lc(o), l, mid, ql));
              }
              return ret;
          }
      } else { // 不完全包含，找往哪边走
          int ret = ql - 1, mid = (l + r) / 2;
          pushdown(o); //!
          
          if(ql <= mid) {
              ret = max(ret, query_same(lc(o), l, r, ql));
          } else maintain(lc(o), l, mid); // !
          if(ql > mid || ret == mid) {
              ret = max(ret, query_same(rc(o), mid + 1, r, ql));
          } else maintain(rc(o), mid + 1, r); // !
          
          return ret;
      }
  }
  ```

## 数论

- 没有小于等于 $M$ 的质因数 $\Leftrightarrow$ 与 $M!$ 互质
- 

## 线性代数

- 常系数齐次线性递推，在进行多项式取模的时候一定是 $\text{mod }{x^k}$，这样余式的次数才是 $0 \sim k-1$
- 算生成函数的时候，考虑清楚边界情况是否适用递推式！
- 

## 计数，概率和期望

- 计数最重要的是不重不漏
- 计数常用定序的技巧，递推时枚举最小的符合条件元素，以避免重复计算
- 当要考虑 2 种顺序造成的影响时，考虑对第一种排序后再递推
- 数学期望 = 均值 = 概率密度函数的平均值
- 计算期望的常用方法：
  - 结束状态明确时，根据全期望公式逆序递推（绿豆蛙的归宿）
  - 枚举每个部分计算对总期望的贡献（e.g.期望使用次数），用期望线性加总（此时对结束状态无要求）（HNOI游走）
  - 期望不好递推时，分离随机变量，转而递推概率（CF518D、WJMZBMR打OSU）
  - 考虑采用增量的思想，计算到达某个状态的期望步数，可以改为考虑状态发生单位变化的步数
    - e.g. 计算收集 $m$ 个物品的期望步数，可以改为先计算多收集 $1$ 个物品的期望步数
- 式子里面有 $\max$ 的时候可以考虑分类讨论拆掉
- 事后概率

## 错误与不足





