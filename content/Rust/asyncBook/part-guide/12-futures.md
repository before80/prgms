+++
title = "12-Future"
date = 2026-08-22T19:00:00+08:00
weight = 14
type = "docs"
description = "Future"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# Future {#futures}


> 原文链接: [https://rust-lang.github.io/async-book/part-guide/futures.html](https://rust-lang.github.io/async-book/part-guide/futures.html)


我们在前面的章节中大量讨论了 future；它们是 Rust async 编程故事的关键部分！在本章中，我们将深入了解 future 是什么、它们如何工作，以及一些直接操作 future 的库。

## `Future` 和 `IntoFuture` traits

- Future
  - Output 关联类型
  - 这里没有真正的细节，轮询在下一节，参考高级章节中的 Pin、执行器/waker
- IntoFuture
  - 用法——通用、在 await 中、async 构建器模式（使用的优缺点）
- 装箱 future，`Box<dyn Future>` 以及它曾经如何常见且必要但现在大多不需要，除了递归等

## 轮询（Polling）

- 它是什么、谁执行它、Poll 类型
  - ready 是最终状态
- 它如何与 await 连接
- drop = 取消
  - 对于 future 以及因此的任务
  - 对 async 编程的一般影响
  - 参考取消安全性章节

### 熔断（Fusing）

## futures-rs crate

- 历史与目的
  - 参见流章节
  - 编写执行器或其他底层 future 内容的辅助工具
    - 固定与装箱
  - 执行器作为部分运行时（参见参考中的替代运行时）
- TryFuture
- 便利 future：pending、ready、ok/err 等
- FutureExt 上的组合器函数
- Tokio 内容的替代方案
  - 函数
  - IO traits

## futures-concurrency crate

https://docs.rs/futures-concurrency/latest/futures_concurrency/
