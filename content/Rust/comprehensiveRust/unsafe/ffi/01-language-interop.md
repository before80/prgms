+++
title = "9.1 语言互操作"
date = 2026-08-11T11:30:00+08:00
weight = 562
type = "docs"
description = "01-语言互操作 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/language-interop.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/language-interop.html)

# 9.1 语言互操作

理想场景：

```bob
╭────────────╮                                          ╭────────────╮
│            │                                          │            │
│            │ <--------------------------------------> │            │
│            │                                          │            │
╰────────────╯                                          ╰────────────╯
     Rust                                                    "C++"
```

> 本课程本节介绍如何通过 Rust 的外部函数接口（FFI）与外部语言交互，并特别关注与 C++ 的互操作。
>
> 理想情况下，Rust 与外部语言（此处为 C++）的用户应能直接调用彼此的方法。
>
> 这一理想场景很难实现：
>
> 不同语言具有不同语义，在它们之间映射意味着需要权衡。Rust 与 C++ 都不提供 ABI 稳定性[^1]，难以在稳定基础上构建。
>
> [^1]: 部分 C++ 编译器厂商在其工具链内提供 ABI 稳定性支持。

