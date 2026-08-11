+++
title = "8 Pinning（固定）"
date = 2026-08-11T11:30:00+08:00
weight = 546
type = "docs"
description = "Pinning（固定） — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning.html)

# 8 Pinning（固定）

本课程本节涵盖：

- 什么是「pinning（固定）」
- 为何需要它
- Rust 如何实现它
- 它如何与 unsafe 和 FFI 交互

## 大纲

本小节约需 1 小时 20 分钟。内容包括：

| 内容 | 时长 |
| --- | --- |
| 什么是 pinning | 5 分钟 |
| Pin<Ptr> 的定义 | 5 分钟 |
| `PhantomPinned` 标记类型 | 5 分钟 |
| 自引用缓冲区示例 | 50 分钟 |
| `Pin<Ptr>` 与 `Drop` | 15 分钟 |


> 「Pinning，即让某个值的内存地址保持在固定位置，是 Rust 中较难理解的概念之一。」
>
> 「它通常只在 async 代码中出现，例如 [`poll(self: Pin<&mut Self>)`][poll]，但 pinning 的适用范围更广。」
>
> 有些数据结构若不使用 `unsafe` 关键字则难以或无法编写，包括自引用结构体和侵入式数据结构。
>
> 与 C++ 的 FFI 是一个与此相关的重要用例。Rust 必须假设任何带引用的 C++ 代码都可能是自引用数据结构。
>
> 「要更详细地理解这一冲突，我们首先需要确保对 Rust 的移动语义有扎实的理解。」

[poll]: https://doc.rust-lang.org/std/future/trait.Future.html#tymethod.poll
