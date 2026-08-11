+++
title = "9.4 语言差异"
date = 2026-08-11T11:30:00+08:00
weight = 565
type = "docs"
description = "语言差异 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/language-differences.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/language-differences.html)

# 9.4 语言差异

```bob
╭────────────╮          ╭───╮           ╭───╮          ╭────────────╮
│            │          │   │           │   │          │            │
│            │ <----->  │   │ <~~~~~~~> │   │ <------> │            │ 
│            │          │   │           │   │          │            │
╰────────────╯          ╰───╯           ╰───╯          ╰────────────╯
    Rust                  C               C                 "C++"
```

> 以 C 作为最小公倍数意味着 Rust 与 C++ 的许多丰富特性都会丢失。
>
> 每次转换都可能带来语义损失、运行时开销与隐蔽 bug。

