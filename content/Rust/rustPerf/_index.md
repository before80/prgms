+++
title = "The Rust Performance Book"
date = 2026-08-23T13:57:00+08:00
weight = 1
type = "docs"
description = "本书范围与读者"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Rust Performance Book](https://nnethercote.github.io/perf-book/)

> 原文链接: [https://nnethercote.github.io/perf-book/](https://nnethercote.github.io/perf-book/)

性能对许多 Rust 程序都很重要。

本书包含可改善 Rust 程序性能相关特性的技术，例如运行时速度、内存占用和二进制体积。[编译时间]一节还包含可缩短 Rust 程序编译时间的技术。有些技术只需更改构建配置，但许多技术需要修改代码。

[编译时间]: 18-compile-times/
有些技术完全是 Rust 特有的，有些则涉及可（经修改后）应用于其他语言程序的想法。[通用技巧]一节还包含一些适用于任何编程语言的通用原则。尽管如此，本书主要关注 Rust 程序的性能，不能替代通用的性能分析与优化指南。

[通用技巧]: 17-general-tips/
本书还侧重于实用且经过验证的技术：许多技术附有拉取请求或其他资源的链接，展示该技术如何应用于真实的 Rust 程序。本书反映了主要作者的背景，在编译器开发方面有所偏重，而在科学计算等其他领域则相对薄弱。

本书刻意保持简洁，以广度优先于深度，便于快速阅读。在适当时会链接到外部资料以提供更深入的内容。

本书面向中级和高级 Rust 用户。初学者 Rust 用户需要学习的内容已经很多，这些技术可能会分散他们的注意力，反而不利于学习。
