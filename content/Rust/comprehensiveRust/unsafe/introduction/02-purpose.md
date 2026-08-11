+++
title = "3.2 unsafe 关键字的用途"
date = 2026-08-11T11:30:00+08:00
weight = 502
type = "docs"
description = "02-unsafe 关键字的用途 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/purpose.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/purpose.html)

# 3.2 unsafe 关键字的用途

- Rust 保证安全性
- 但编译器能做的事有限
- `unsafe` 关键字让程序员承担维护 Rust 规则的责任

> 「Rust 的一个基本目标是保证内存安全。」
>
> 「但存在局限。有些安全考量无法用编程语言表达。即便可以表达，Rust 编译器能控制的范围也有限。」
>
> 「`unsafe` 关键字将维护 Rust 规则的责任从编译器转移到程序员。」
>
> 「当你看到 `unsafe` 关键字时，就意味着责任从编译器转移到了程序员。」

