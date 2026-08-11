+++
title = "5.1 Rust 是健全的"
date = 2026-08-11T11:30:00+08:00
weight = 526
type = "docs"
description = "01-Rust 是健全的 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/rust-is-sound.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/rust-is-sound.html)

# 5.1 Rust 是健全的

- 健全性（soundness）是 Rust 的基础
- 健全性 ≈ 不可能引发内存安全问题
- 健全函数具有一些共同的「形态」

> 「Rust 代码的一项基本原则是：它是健全的。
>
> 「我们很快会给出 soundness 这一术语的正式定义。在此之前，可以把健全代码理解为：不会触发内存安全问题的代码。
>
> 「健全代码由 _健全函数_ 和 _健全操作_ 组成。
>
> 「健全函数是指：无论传入何种可能的输入，都不会引发健全性问题。
>
> 健全函数具有一些共同的形态。
>
> 接下来我们就来看这些形态。
>
> 「先从仅用 Safe Rust 实现的一种形态开始，再看看在不同部分引入 `unsafe` 时会发生什么。

