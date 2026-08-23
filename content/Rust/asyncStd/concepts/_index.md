+++
title = "2 使用 async-std 的异步概念"
date = 2026-08-23T16:35:00+08:00
weight = 10
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://book.async.rs/concepts.html](https://book.async.rs/concepts.html)

[Rust Future][futures] 以难以掌握著称。我们不这么认为。在我们看来，它们是最容易理解的并发概念之一，并且有直观的解释。

然而，这种印象也有其合理原因。Future 基于三个概念，而这些概念似乎一直是困惑的来源：延迟计算、异步性，以及执行策略的独立性。

这些概念本身并不难，只是许多人并不习惯。这种基础性的困惑，又因许多面向实现细节的实现而被放大。大多数对这些实现的解释也面向高级用户，初学者可能难以理解。我们力求既提供易于理解的原语，也提供平易近人的概念概览。

Future 是一种对代码运行方式进行抽象的概念。它们本身什么也不做。这在命令式语言中是一个奇怪的概念——在命令式语言中，通常一件事接一件事地发生——而且就是现在发生。

那么 Future 如何运行？由你决定！Future 如果没有_执行_它们的代码，就什么也不做。这部分称为_执行器_（executor）。_执行器_决定_何时_以及_如何_执行你的 future。`async-std::task` 模块为你提供了与这类执行器交互的接口。

不过，让我们先从一点动机说起。

[futures]: https://en.wikipedia.org/wiki/Futures_and_promises
