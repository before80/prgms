+++
title = "02-借用检查器"
date = 2026-08-01T10:38:00+08:00
weight = 57
type = "docs"
description = "借用检查器（The Borrow Checker）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 借用检查器 {#the-borrow-checker}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/peripherals/borrowck.html](https://doc.rust-lang.org/stable/embedded-book/peripherals/borrowck.html)


## 可变全局状态 {#mutable-global-state}

不幸的是，硬件基本上就是可变全局状态，这对 Rust 开发者来说可能相当吓人。硬件独立于我们编写的代码结构而存在，并且随时可能被现实世界修改。

## 我们该定什么规则？ {#what-should-our-rules-be}

我们怎样才能可靠地与这些外设交互？

1. 始终使用 `volatile` 方法读写外设内存，因为它随时可能变化
2. 在软件中，我们应当能够共享任意数量的对这些外设的只读访问
3. 若某段软件应对外设拥有读写访问权，它应当持有该外设的唯一引用

## 借用检查器 {#the-borrow-checker-section}

后两条规则听起来可疑地像借用检查器（Borrow Checker）已经在做的事！

想象一下，如果我们能传递这些外设的所有权，或提供对它们的不可变或可变引用？

其实可以，但为了让借用检查器正确处理，每个外设必须恰好有一个实例。幸好在硬件中，任意给定外设本来就只有一个实例，可我们怎样在代码结构中把它表达出来呢？
