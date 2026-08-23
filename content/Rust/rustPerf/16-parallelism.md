+++
title = "16 并行"
date = 2026-08-23T13:57:00+08:00
weight = 17
type = "docs"
description = "并行与并发"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Rust Performance Book](https://nnethercote.github.io/perf-book/)

# 并行 {#parallelism}


> 原文链接: [https://nnethercote.github.io/perf-book/parallelism.html](https://nnethercote.github.io/perf-book/parallelism.html)


Rust 为安全的并行编程提供了出色支持，可带来显著的性能提升。向程序引入并行有多种方式，对任何程序而言最佳方式都高度依赖其设计。

话虽如此，对并行的深入讨论超出了本书范围。

若对基于线程的并行感兴趣，[`rayon`] 和 [`crossbeam`] crate 的文档是很好的起点。[Rust Atomics and Locks][Atomics] 也是极佳资源。

[`rayon`]: https://crates.io/crates/rayon
[`crossbeam`]: https://crates.io/crates/crossbeam
[Atomics]: https://marabos.nl/atomics/

若对细粒度数据并行感兴趣，这篇[博客文章]是对截至 2025 年 11 月 Rust 中 SIMD 支持状况的良好概述。

[博客文章]: https://shnatsel.medium.com/the-state-of-simd-in-rust-in-2025-32c263e5f53d
