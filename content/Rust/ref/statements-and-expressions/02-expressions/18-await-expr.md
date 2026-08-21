+++
title = "18-await 表达式"
date = 2026-08-18T08:45:00+08:00
weight = 61
type = "docs"
description = "await 表达式 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/expressions/await-expr.html](https://doc.rust-lang.org/reference/expressions/await-expr.html)

r[expr.await]
# await 表达式

r[expr.await.syntax]
```grammar,expressions
AwaitExpression -> Expression `.` `await`
```

r[expr.await.intro]
`await` 表达式是一种语法构造，用于挂起由 `std::future::IntoFuture` 的实现所提供的计算，直到给定的 future 准备好产生一个值。

r[expr.await.construct]
await 表达式的语法是：一个类型实现了 [`IntoFuture`] trait 的表达式（称为 *future 操作数*），然后是词法单元 `.`，然后是 `await` 关键字。

r[expr.await.allowed-positions]
await 表达式只在[异步上下文][async context]中合法，例如 [`async fn`]、[`async` 闭包][`async` closure]或 [`async` 块][`async` block]。

r[expr.await.effects]
更具体地说，await 表达式具有以下效果。

1. 对 future 操作数调用 [`IntoFuture::into_future`] 以创建一个 future。
2. 将该 future 求值为 [future] `tmp`；
3. 使用 [`Pin::new_unchecked`] 固定 `tmp`；
4. 然后通过调用 [`Future::poll`] 方法并传入当前[任务上下文](#task-context)来轮询这个被固定的 future；
5. 若对 `poll` 的调用返回 [`Poll::Pending`]，则该 future 返回 `Poll::Pending`，并挂起其状态，使得外围异步上下文再次被轮询时，执行从第 3 步继续；
6. 否则对 `poll` 的调用必定已返回 [`Poll::Ready`]，此时 [`Poll::Ready`] 变体中包含的值就是该 `await` 表达式本身的结果。

r[expr.await.edition2018]
> [!EDITION-2018]
> await 表达式从 Rust 2018 起才可用。

r[expr.await.task]
## 任务上下文

任务上下文指的是当前[异步上下文][async context]自身被轮询时提供给它的 [`Context`]。因为 `await` 表达式只在异步上下文中合法，所以必定存在某个可用的任务上下文。

r[expr.await.desugar]
## 近似脱糖

实际上，await 表达式大致等价于以下非规范性脱糖：

<!-- ignore: example expansion -->
```rust
match operand.into_future() {
    mut pinned => loop {
        let mut pin = unsafe { Pin::new_unchecked(&mut pinned) };
        match Pin::future::poll(Pin::borrow(&mut pin), &mut current_context) {
            Poll::Ready(r) => break r,
            Poll::Pending => yield Poll::Pending,
        }
    }
}
```

其中 `yield` 伪代码返回 `Poll::Pending`，并在再次被调用时从该点恢复执行。变量 `current_context` 指的是从异步环境中取得的上下文。

[`async fn`]: ../items/functions.md#async-functions
[`async` closure]: closure-expr.md#async-closures
[`async` block]: block-expr.md#async-blocks
[`Context`]: std::task::Context
[`future::poll`]: std::future::Future::poll
[`pin::new_unchecked`]: std::pin::Pin::new_unchecked
[`poll::Pending`]: std::task::Poll::Pending
[`poll::Ready`]: std::task::Poll::Ready
[async context]: ../expressions/block-expr.md#async-context
[future]: std::future::Future
[`IntoFuture`]: std::future::IntoFuture
[`IntoFuture::into_future`]: std::future::IntoFuture::into_future
