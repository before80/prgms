+++
title = "13.4 循环与迭代器的性能比较"
date = 2026-08-05T08:44:00+08:00
weight = 60
type = "docs"
description = "对比 for 循环与迭代器实现的性能，说明零成本抽象"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 循环与迭代器的性能比较


> 原文链接: [https://doc.rust-lang.org/stable/book/ch13-04-performance.html](https://doc.rust-lang.org/stable/book/ch13-04-performance.html)


## 循环与迭代器的性能

　　要决定用循环还是迭代器，需要知道哪种实现更快：带显式 `for` 循环的 `search`，还是使用迭代器的版本。

　　我们做了一次基准测试：把阿瑟·柯南·道尔爵士（Sir Arthur Conan Doyle）的《福尔摩斯探案集》全文加载进一个 `String`，并在内容中搜索单词 *the*。使用 `for` 循环的 `search` 与使用迭代器的版本结果如下：

```text
test bench_search_for  ... bench:  19,620,300 ns/iter (+/- 915,700)
test bench_search_iter ... bench:  19,234,900 ns/iter (+/- 657,200)
```

　　两种实现性能相近！这里不解释基准代码本身——重点不是证明两者完全等价，而是大致感受这两种实现在性能上的对比。

　　更全面的基准还应换用不同篇幅的文本作为 `contents`、不同单词与不同长度作为 `query`，以及各种其他变化。关键在于：迭代器虽是高层抽象，编译后大致会变成你亲手写底层代码时会得到的那种代码。迭代器是 Rust 的*零成本抽象*（zero-cost abstraction）之一，意思是使用该抽象不会带来额外的运行时开销。这与 C++ 的最初设计者兼实现者 Bjarne Stroustrup 在 2012 年 ETAPS 主题演讲 “Foundations of C++” 中对零开销的定义类似：

> 一般而言，C++ 的实现遵循零开销原则：你不用的，就不必付出代价。更进一步：你用到的，也不可能手写得更好。

　　在许多情况下，使用迭代器的 Rust 代码会编译成与你手写汇编同等的结果。循环展开、消除数组访问的边界检查等优化会生效，使最终代码极为高效。既然知道了这一点，就可以放心使用迭代器与闭包了！它们让代码看起来更高层，却不会为此付出运行时性能代价。

## 小结

　　闭包和迭代器是受函数式编程语言思想启发的 Rust 特性。它们帮助 Rust 以底层性能清晰表达高层思想。闭包与迭代器的实现方式使得运行时性能不受影响。这体现了 Rust 力求提供零成本抽象的目标。

　　既然已经提升了 I/O 项目的表达力，接下来看看 `cargo` 的更多功能，帮助我们把项目分享给世界。
