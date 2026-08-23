+++
title = "Rust Fuzz Book"
date = 2026-08-23T13:50:00+08:00
weight = 1
type = "docs"
description = "Rust 模糊测试简介"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Rust Fuzz Book](https://rust-fuzz.github.io/book/)

> 原文链接: [https://rust-fuzz.github.io/book/](https://rust-fuzz.github.io/book/)

[模糊测试][Fuzz testing]是一种软件测试技术，通过向程序提供伪随机数据作为输入，以发现安全性和稳定性问题。

[Rust][] 是一门高性能、安全、通用的编程语言。

本书演示如何对用 Rust 编写的软件进行模糊测试。

本书记录了两种用于模糊测试 Rust 代码的工具：**[afl.rs]** 和 **[cargo-fuzz]**。

本书源码可在 GitHub 获取：<https://github.com/rust-fuzz/book>。

[Fuzz testing]: https://en.wikipedia.org/wiki/Fuzz_testing
[Rust]: https://www.rust-lang.org/
[cargo-fuzz]: cargo-fuzz/
[afl.rs]: afl/