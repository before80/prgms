+++
title = "24.2-递归"
date = 2026-08-22T19:00:00+08:00
weight = 40
type = "docs"
description = "递归"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 递归 {#recursion}


> 原文链接: [https://rust-lang.github.io/async-book/07_workarounds/04_recursion.html](https://rust-lang.github.io/async-book/07_workarounds/04_recursion.html)


在内部，`async fn` 会创建包含每个被 `.await` 的子 `Future` 的状态机类型。这使得递归 `async fn` 有点棘手，因为生成的状态机类型必须包含自身：

```rust,edition2018
# async fn step_one() { /* ... */ }
# async fn step_two() { /* ... */ }
# struct StepOne;
# struct StepTwo;
// 此函数：
async fn foo() {
    step_one().await;
    step_two().await;
}
// 生成类似这样的类型：
enum Foo {
    First(StepOne),
    Second(StepTwo),
}

// 因此此函数：
async fn recursive() {
    recursive().await;
    recursive().await;
}

// 生成类似这样的类型：
enum Recursive {
    First(Recursive),
    Second(Recursive),
}
```

这行不通——我们创建了无限大小的类型！编译器会报错：

```
error[E0733]: recursion in an async fn requires boxing
 --> src/lib.rs:1:1
  |
1 | async fn recursive() {
  | ^^^^^^^^^^^^^^^^^^^^
  |
  = note: a recursive `async fn` call must introduce indirection such as `Box::pin` to avoid an infinitely sized future
```

要允许这一点，我们必须使用 `Box` 引入间接层。

在 Rust 1.77 之前，由于编译器限制，仅将 `recursive()` 的调用包装在 `Box::pin` 中是不够的。要使其工作，我们必须将 `recursive` 改为返回 `.boxed()` `async` 块的非 `async` 函数：

```rust,edition2018
use futures::future::{BoxFuture, FutureExt};

fn recursive() -> BoxFuture<'static, ()> {
    async move {
        recursive().await;
        recursive().await;
    }.boxed()
}
```

在较新版本的 Rust 中，[该编译器限制已解除]。

自 Rust 1.77 起，带分配间接层的 `async fn` 递归支持[已稳定]，因此只要使用某种形式的间接层以避免函数状态的无限大小，就允许递归调用。

这意味着像这样的代码现在可以工作：

```rust,edition2021
async fn recursive_pinned() {
    Box::pin(recursive_pinned()).await;
    Box::pin(recursive_pinned()).await;
}
```

[becomes stable]: https://blog.rust-lang.org/2024/03/21/Rust-1.77.0.html#support-for-recursion-in-async-fn
[that compiler limitation has been lifted]: https://github.com/rust-lang/rust/pull/117703/
