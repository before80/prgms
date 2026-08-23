+++
title = "24.3-Trait 中的 async"
date = 2026-08-22T19:00:00+08:00
weight = 41
type = "docs"
description = "Trait 中的 async"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# Trait 中的 async {#async-in-traits}


> 原文链接: [https://rust-lang.github.io/async-book/07_workarounds/05_async_in_traits.html](https://rust-lang.github.io/async-book/07_workarounds/05_async_in_traits.html)


目前，在 Rust 稳定版中不能在 trait 中使用 `async fn`。自 2022 年 11 月 17 日起，nightly 工具链上提供了 async-fn-in-trait 的 MVP，[详见此处](https://blog.rust-lang.org/inside-rust/2022/11/17/async-fn-in-trait-nightly.html)。

与此同时，稳定工具链上可使用 [crates.io 上的 async-trait crate](https://github.com/dtolnay/async-trait) 作为变通方法。

请注意，使用这些 trait 方法会导致每次函数调用进行一次堆分配。对绝大多数应用这不是显著成本，但在决定是否在低层函数（预期每秒被调用数百万次）的公开 API 中使用此功能时应予以考虑。

最新更新：https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits.html
