+++
title = "8.4 为何难以使用"
date = 2026-08-11T11:30:00+08:00
weight = 550
type = "docs"
description = "04-为何难以使用 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/why-difficult.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/why-difficult.html)

# 8.4 为何难以使用

- `Pin<Ptr>`「只是」标准库中定义的一个类型
- 这满足了其最初受众——async 运行时作者——的需求，而无需扩展核心语言
- 该受众可以接受一些人体工程学上的缺点，因为 `async` 的使用者很少直接与 `Pin` 交互

> 「你可能会疑惑 Pin 为何如此难用。答案很大程度上是历史原因。」
>
> 「对 Rust 项目而言，`Pin<Ptr>` 比替代方案提供了更简单的实现。」
>
> 「Pin 主要是为世界上大约一百位编写 async 运行时的人设计的。Rust 团队选择了对编译器更简单、但对用户不那么顺手的设计。」
>
> 「存在更用户友好的提案，但因对主要受众过于复杂而被拒绝——他们可以承受这种复杂度。」

