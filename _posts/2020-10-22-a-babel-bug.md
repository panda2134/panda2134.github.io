---
layout: post
comments: true
title: 记一个Babel相关bug的调试经历
categories: 开发
tags: ['javascript', 'babel']
---

> All abstraction layers are leaking. -- a random guru

# 起因

引起问题的，是如下的一段vue jsx代码：

```jsx

export default {
  // ... data等省略，在data中声明了blanks和submitted
  render () {
    // ... 前面代码省略，声明res为字符串数组
    const descriptionNodes = []
    let blankCount = 0
    res.forEach((value, index, { length }) => {
      if (/* 省略 */) {
      blankCount++
      descriptionNodes.push(<el-input vModel={this.blanks[index]} disabled={this.submitted} />)
      }
    })
    // ... return等省略
  }
}

```

这段代码在本机无论以development模式构建，还是以production模式构建，都没有任何问题；但是，在推送到预生产环境后，控制台出现奇怪的报错称 `d` 未定义。

# 排查过程

看到代码中并没有 `d` 变量，第一反应是 source-map 不全导致调试信息是babel编译以后的代码，于是设置预生产环境亦使用 eval-source-map，然后再次调试。

问题变为 `this` 未定义，于是怀疑是闭包导致的问题。按照通常的套路，把jsx中引用this的地方去掉，相应变量 `blank, submitted` 全部在箭头函数闭包外存储进入 render 时的值，问题依旧，报错仍然为 `this` 未定义。

冷静分析一下，闭包不应该是导致问题发生的原因。首先，这里的forEach内的函数是箭头函数，箭头函数没有词法作用域，应该会直接继承外层的 `this`；其次，箭头函数内代码同步执行，不会有其他地方对 `this` 作更改。

先保留提取 `blank, submitted` 后的代码如下不变。按理说，箭头函数内不再有对于 `this` 的引用，为什么还会出现相关错误呢？

```jsx

export default {
  // ... data等省略，在data中声明了blanks和submitted
  render () {
    // ... 前面代码省略，声明res为字符串数组
    const descriptionNodes = []
    let blankCount = 0
    const { blanks, submitted } = this
    res.forEach((value, index, { length }) => {
      if (/* 省略 */) {
      blankCount++
      descriptionNodes.push(<el-input vModel={blanks} disabled={submitted} />)
      }
    })
    // ... return等省略
  }
}

```

打开调试器的源代码选项卡，右键选择查看映射前的代码，这即为真正执行于浏览器中的代码。我们知道，jsx 在转译过程中，会被转为对 `$createElement` 的调用。而对 Vue 2.x，这一函数中描述 vModel 的方式是初始值+更新回调函数，那么唯一可能用到 `this` 的就是回调函数了。

原始代码大致如下：

```js
render () {
  // ... 无关部分省略
  var _this = this;
  res.forEach(function(value, index, arg) {
    var length = arg.length;
    var _this2 = this;
    if (/* blahblahblah */) {
      blankCount++
      descriptionNodes.push(_this.$createElement("el-input",{ // h 为注入的
        class: "fill-blank__input",
        attrs: { disabled: submitted },
        model: {
          value:blanks[blankCount],
          callback: function(e) {
            _this2.$set(blanks, blankCount, e)
          }
        }
      }))
    }
  })
  // ... 无关部分省略
}
```

这里问题就很显然了，ci中，babel转译的时候引用了错误的 `this`!

修复方法也显然，既然转译出错，把不带词法作用域的箭头函数强行翻译成了带词法作用域的 `function` （这应该是因为Vue JSX 中对 `this` 的引用没有被 babel 检测到)，那就索性将箭头函数改为 `function`，然后手动绑定外层的 `this` !

# 小结

Babel, Webpack, Minifier, 抽象越多，出问题时隐藏的也越深，当今前端架构的致命弱点莫过于此。


