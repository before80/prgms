+++
title = "3.6 责任转移"
date = 2026-08-11T11:30:00+08:00
weight = 513
type = "docs"
description = "04-责任转移 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/responsibility-shift.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/responsibility-shift.html)

# 3.6 责任转移

|             | 内存是否安全？ | 内存安全的责任方 |
| :---------- | :------------: | :--------------- |
| Safe Rust   |       是       | 编译器           |
| Unsafe Rust |       是       | 程序员           |

> 谁对内存安全负责？
>
> - Safe Rust → 编译器
> - Unsafe Rust → 程序员
>
> 「编写 safe Rust 时，你无法制造内存安全问题。编译器会确保有错误的程序无法通过编译。」
>
> 「`unsafe` 关键字将维护内存安全的责任从编译器转移到程序员。它表明存在必须满足的前置条件。」
>
> 「为履行这一责任，程序员必须确保他们已理解前置条件是什么，并且他们的代码始终能满足这些条件。」
>
> 「在本课程中，我们将用 _safety preconditions（安全前置条件）_ 这一术语来描述这种情况。」

