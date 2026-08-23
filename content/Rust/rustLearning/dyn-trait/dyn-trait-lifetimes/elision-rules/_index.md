+++
title = "4.5.3 省略规则"
date = 2026-08-23T10:16:00+08:00
weight = 50
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Learning Rust](https://quinedot.github.io/rust-learning/)

# 省略规则 {#elision-rules}


> 原文链接: [https://quinedot.github.io/rust-learning/dyn-elision.html](https://quinedot.github.io/rust-learning/dyn-elision.html)


`dyn Trait` 的生命周期省略规则是 Rust 中分形复杂性的一个实例。一些通用准则能让你理解 95% 的情况，一些高级准则能再覆盖 4%，但越深入就越可能遇到越冷门的特殊情况。不幸的是，目前没有可供参考的正式规范。

好消息是，你可以通过显式指定生命周期来覆盖省略行为，这为大多数复杂性提供了逃生舱。因此，如有疑问，请显式写出生命周期！

在以下小节中，我们分层介绍编译器当前的行为，范围以我们已探索的为准。

我们偶尔会引用[参考手册中关于 trait 对象生命周期省略的文档](https://doc.rust-lang.org/reference/lifetime-elision.html#default-trait-object-lifetimes)。不过，我们的分层方式与参考手册略有不同，因为参考手册并不完全准确。
