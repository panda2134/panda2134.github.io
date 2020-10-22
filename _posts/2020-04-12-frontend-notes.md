---
layout: post
comments: true
title: 前端细节小结
categories: 开发
tags: ['javascript', 'css']
---

1. 关于 `Object.defineProperty`，使用方法如下：

   ```javascript
   Object.defineProperty(obj, 'prop', {
     enumerable: true, // 是否可以通过 for ... of ... 枚举
     configurable: true,  // 是否可以再次通过此方法配置
     get() {} // getter
     set() {} // setter
   })
   ```

2. 关于原型链和继承：javascript查找对象属性，是沿着原型链向上找；一个典型例子如下

   ```javascript
   function MyObject() {
     this.prop = 1; // this 绑定到新创建的 {}
     this.func = function() {
       this.prop = 2;
     }
     // 如果这里返回了对象，那么new运算符得到的就是返回的对象；
     // 否则，得到的就是绑定在this的，在函数开始执行前创建的对象
   }
   MyObject.prototype.prop0 = 4;
   a.prop // 1
   a.func() // a.prop = 2， 通过`.`运算符访问成员方法时，绑定成员方法中 this 到当前对象；
   // 方法属于原型链上parent时亦然
   a.prop0 // 4
   ```

   ECMAScript 引入语法糖 `class`，用法如下

   ```javascript
   proto = function() { return {prop0: 4} } // constructor要绑定this,不可为箭头函数
   class MyObject extends proto { // extend的应该是一个ctor函数
     constructor() {
       super() // 和java类似，子类第一行必须为super()
       this.prop = 1
     }
     func() {
       this.prop = 2
     }
   }
   ```

3. 关于 CSS `z-index` [深度好文](https://www.zhangxinxu.com/wordpress/2016/01/understand-css-stacking-context-order-z-index/?shrink=1)

   层叠等级顺序：`层叠上下文background` 

   ​									< `负数z-index` 

   ​												< `block` < `float` < `inline (inline-block)`

   ​															 < `z-index:auto / 0` < `正z-index`

   记忆方法：背景垫在最后，其次是负数 `z-index`；`inline`是文字，比 `float` 边框靠前，而 `float` 作为侧栏又在正文上方；再之后按照 `z-index` 论资排辈

   对于同一等级，则在 DOM 中靠后的排在上面

   [What makes a stacking context](https://developer.mozilla.org/zh-CN/docs/Web/Guide/CSS/Understanding_z_index/The_stacking_context)

   创建层叠上下文常见情况：

   - `position: absolute / relative` 且`z-index` **不是** `auto` （哪怕是写明 `z-index:0`也会创建层叠上下文）
   - `position: fixed / sticky`
   - `display:flex` 且 **子元素** 的`z-index` 不是auto，此时 **子元素** 为层叠上下文

   > IE6/IE7浏览器有个bug，就是`z-index:auto`的定位元素也会创建层叠上下文
   >
   > RIP Internet Explorer

   TO BE CONTINUED

4. `JSON.stringify`: https://juejin.im/post/5decf09de51d45584d238319
5. `<link rel="stylesheet alternate" href="a.css">` 用 `alternate` 做换肤，切换 DOM 的 `disabled` 即可
6. 关于正则匹配。C++ / JS中，匹配结果数组[0] 都是匹配结果，**[1..]开始才是匹配组**！此外，ES6中的匹配返回结构如下：
```typescript
interface RegExpMatchArray extends Array<string> {
	input: string;
  index: number;
  // group: object; // only for NAMED capture groups! e.g. /(?<name>\w+)/
}
```

当正则表达式不含 `g` 标志时，`String.prototype.match(re: RegExp)` 的结果和 `RegExp.prototype.exec(str: string)​`相同。

关于 `global` / `sticky`属性：设置这些属性的时候，RegExp对象是**有状态**的。
7. 关于 `tsconfig.json` 
 - `exclude` 这个选项**根本就不是用来排除文件的！**它只能减少通过`include`包括的文件！官方文档写的很清楚 https://www.typescriptlang.org/v2/en/tsconfig#exclude
 - `"compilerOptions"` 下面有 `"skipLibCheck": true`，会跳过库内部的ts报错
