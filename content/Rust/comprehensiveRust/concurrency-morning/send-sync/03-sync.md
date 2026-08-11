+++
title = "4.3 `Sync`"
date = 2026-08-11T11:30:00+08:00
weight = 355
type = "docs"
description = "03-`Sync` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/send-sync/sync.html](https://google.github.io/comprehensive-rust/concurrency/send-sync/sync.html)

# 4.3 `Sync`

> 若同时从多个线程访问 `T` 值是安全的，则类型 `T` 是 [`Sync`][1]。

更精确的定义是：

> `T` 是 `Sync`，当且仅当 `&T` 是 `Send`

[1]: https://doc.rust-lang.org/std/marker/trait.Sync.html

> 这句话本质上是在简短说明：若某类型对共享使用是线程安全的，那么跨线程传递它的引用也是线程安全的。
>
> 因为若类型是 Sync，意味着它可以在多个线程间共享而不会有数据竞争或其他同步问题，因此把它移到另一线程是安全的。对该类型的引用也可以安全地移到另一线程，因为它所引用的数据可以从任何线程安全访问。

