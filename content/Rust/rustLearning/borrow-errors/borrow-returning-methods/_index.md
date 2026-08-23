+++
title = "2.6 理解返回借用的方法"
date = 2026-08-23T10:16:00+08:00
weight = 19
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Learning Rust](https://quinedot.github.io/rust-learning/)

# 理解返回借用的方法 {#borrow-returning-methods}


> 原文链接: [https://quinedot.github.io/rust-learning/methods.html](https://quinedot.github.io/rust-learning/methods.html)


这里我们看看返回借用的方法是如何工作的。我们的示例将考虑一种典型模式：
```rust
fn method(&mut self) -> &SomeReturnType {}
// 即：
// fn method<'this>(&'this mut self) -> &'this SomeReturnType {}
```

这个签名的含义是：对返回值的任何使用都会让 `*self` 保持独占借用。

这是最需要牢记的一点。以下各小节会深入一些可能有用的细节。
