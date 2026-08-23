+++
title = "2.10-已知限制"
date = 2026-08-22T20:00:00+08:00
weight = 12
type = "docs"
description = "Criterion.rs 已知限制"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 已知限制 {#known-limitations}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/user_guide/known_limitations.html](https://bheisler.github.io/criterion.rs/book/user_guide/known_limitations.html)


## 已知限制

目前，相对于标准基准测试 harness，Criterion.rs 的使用存在若干限制。

首先，Criterion.rs 必须使用 `criterion_main` 宏提供自己的 `main` 函数。这带来以下限制：

* 无法像常规基准测试 harness 那样在 `src/` 目录的代码中包含基准测试。
* 无法对非 `pub` 函数进行基准测试。外部基准测试（包括使用 Criterion.rs 的）作为独立 crate 编译，非 `pub` 函数对基准测试不可见。
* 无法对二进制 crate 中的函数进行基准测试。二进制 crate 不能作为其他 crate 的依赖，这包括外部测试和基准测试（更多细节[见此处](https://github.com/rust-lang/cargo/issues/4316)）。
* 无法对不提供 `rlib` 的 crate 中的函数进行基准测试。

Criterion.rs 目前无法解决这些问题。正在实现一项[实验性 RFC](https://github.com/rust-lang/rust/issues/50297)，以支持自定义测试与基准测试框架。
