+++
title = "24.1-Send 近似"
date = 2026-08-22T19:00:00+08:00
weight = 39
type = "docs"
description = "Send 近似"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# Send 近似 {#send-approximation}


> 原文链接: [https://rust-lang.github.io/async-book/07_workarounds/03_send_approximation.html](https://rust-lang.github.io/async-book/07_workarounds/03_send_approximation.html)


某些 `async fn` 状态机可以安全地在线程间发送，而其他则不行。`async fn` `Future` 是否为 `Send` 取决于是否在 `.await` 点持有非 `Send` 类型。编译器会尽力近似值何时可能在 `.await` 点被持有，但此分析在当今若干地方过于保守。

例如，考虑一个简单的非 `Send` 类型，可能包含 `Rc` 的类型：

```rust
use std::rc::Rc;

#[derive(Default)]
struct NotSend(Rc<()>);
```

`NotSend` 类型的变量可能作为临时值短暂出现在 `async fn` 中，即使 `async fn` 返回的 `Future` 类型必须是 `Send`：

```rust,edition2018
# use std::rc::Rc;
# #[derive(Default)]
# struct NotSend(Rc<()>);
async fn bar() {}
async fn foo() {
    NotSend::default();
    bar().await;
}

fn require_send(_: impl Send) {}

fn main() {
    require_send(foo());
}
```

然而，若我们将 `foo` 改为将 `NotSend` 存储在变量中，此示例将无法编译：

```rust,edition2018
# use std::rc::Rc;
# #[derive(Default)]
# struct NotSend(Rc<()>);
# async fn bar() {}
async fn foo() {
    let x = NotSend::default();
    bar().await;
}
# fn require_send(_: impl Send) {}
# fn main() {
#    require_send(foo());
# }
```

```
error[E0277]: `std::rc::Rc<()>` cannot be sent between threads safely
  --> src/main.rs:15:5
   |
15 |     require_send(foo());
   |     ^^^^^^^^^^^^ `std::rc::Rc<()>` cannot be sent between threads safely
   |
   = help: within `impl std::future::Future`, the trait `std::marker::Send` is not implemented for `std::rc::Rc<()>`
   = note: required because it appears within the type `NotSend`
   = note: required because it appears within the type `{NotSend, impl std::future::Future, ()}`
   = note: required because it appears within the type `[static generator@src/main.rs:7:16: 10:2 {NotSend, impl std::future::Future, ()}]`
   = note: required because it appears within the type `std::future::GenFuture<[static generator@src/main.rs:7:16: 10:2 {NotSend, impl std::future::Future, ()}]>`
   = note: required because it appears within the type `impl std::future::Future`
   = note: required because it appears within the type `impl std::future::Future`
note: required by `require_send`
  --> src/main.rs:12:1
   |
12 | fn require_send(_: impl Send) {}
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

error: aborting due to previous error

For more information about this error, try `rustc --explain E0277`.
```

此错误是正确的。若我们将 `x` 存入变量，它要到 `.await` 之后才会被 drop，此时 `async fn` 可能运行在不同线程上。由于 `Rc` 不是 `Send`，允许其在线程间传递是不安全的。一个简单的解决方案是在 `.await` 之前 `drop` `Rc`，但遗憾的是这在当今行不通。

要成功变通此问题，你可能需要引入块作用域来封装任何非 `Send` 变量。这使编译器更容易判断这些变量不会跨越 `.await` 点存活。

```rust,edition2018
# use std::rc::Rc;
# #[derive(Default)]
# struct NotSend(Rc<()>);
# async fn bar() {}
async fn foo() {
    {
        let x = NotSend::default();
    }
    bar().await;
}
# fn require_send(_: impl Send) {}
# fn main() {
#    require_send(foo());
# }
```
