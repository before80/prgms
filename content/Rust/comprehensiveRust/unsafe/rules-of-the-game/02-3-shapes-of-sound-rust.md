+++
title = "5.3 健全 Rust 的三种形态"
date = 2026-08-11T11:30:00+08:00
weight = 533
type = "docs"
description = "02-健全 Rust 的三种形态 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/3-shapes-of-sound-rust.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/3-shapes-of-sound-rust.html)

# 5.3 健全 Rust 的三种形态

- 完全用 Safe Rust 编写的函数
- 包含不可能被误用的 `unsafe` 块的函数
- 已记录安全前置条件的不安全（unsafe）函数

> - 我们要编写健全代码。
> - 健全代码只能有以下形态：
>   - 不含 `unsafe` 块的安全函数
>   - 完全封装 `unsafe` 块的安全函数，即调用方无需了解其中的 `unsafe`
>   - 包含 `unsafe` 块但未将其封装、把证明责任转嫁给调用方的不安全函数
> - 证明责任
>   - 仅含 Safe Rust 的安全函数 → 编译器
>   - 含 `unsafe` 块的安全函数 → 函数作者
>   - 不安全函数 → 函数调用方

