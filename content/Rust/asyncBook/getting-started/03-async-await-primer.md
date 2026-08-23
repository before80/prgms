+++
title = "19.3-async/.await 入门"
date = 2026-08-22T19:00:00+08:00
weight = 25
type = "docs"
description = "async/.await 入门"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# async/.await 入门 {#async-await-primer}


> 原文链接: [https://rust-lang.github.io/async-book/01_getting_started/04_async_await_primer.html](https://rust-lang.github.io/async-book/01_getting_started/04_async_await_primer.html)


`async`/`.await` 是 Rust 内置的、用于编写看起来像同步代码的异步函数的工具。`async` 将一段代码转换为实现名为 `Future` 的 trait 的状态机。在同步方法中调用阻塞函数会阻塞整个线程，而被阻塞的 `Future` 会让出线程控制权，允许其他 `Future` 运行。

让我们在 `Cargo.toml` 文件中添加一些依赖：

```toml
[dependencies]
futures = "0.3"
```

要创建异步函数，可以使用 `async fn` 语法：

```rust,edition2018
async fn do_something() { /* ... */ }
```

`async fn` 返回的值是一个 `Future`。要发生任何事情，该 `Future` 需要在执行器上运行。

```rust,edition2018
// `block_on` blocks the current thread until the provided future has run to
// completion. Other executors provide more complex behavior, like scheduling
// multiple futures onto the same thread.
use futures::executor::block_on;

async fn hello_world() {
    println!("hello, world!");
}

fn main() {
    let future = hello_world(); // Nothing is printed
    block_on(future); // `future` is run and "hello, world!" is printed
}
```

在 `async fn` 内部，可以使用 `.await` 等待实现 `Future` trait 的另一种类型的完成，例如另一个 `async fn` 的输出。与 `block_on` 不同，`.await` 不会阻塞当前线程，而是异步等待 future 完成；若该 future 当前无法推进，则允许其他任务运行。

例如，假设我们有三个 `async fn`：`learn_song`、`sing_song` 和 `dance`：

```rust,ignore
async fn learn_song() -> Song { /* ... */ }
async fn sing_song(song: Song) { /* ... */ }
async fn dance() { /* ... */ }
```

一种学习、唱歌和跳舞的方式是分别阻塞等待每一个：

```rust,ignore
fn main() {
    let song = block_on(learn_song());
    block_on(sing_song(song));
    block_on(dance());
}
```

然而，这样无法获得最佳性能——我们一次只做一件事！显然必须先学会歌曲才能唱，但可以在学习和唱歌的同时跳舞。为此，我们可以创建两个可并发运行的独立 `async fn`：

```rust,ignore
async fn learn_and_sing() {
    // Wait until the song has been learned before singing it.
    // We use `.await` here rather than `block_on` to prevent blocking the
    // thread, which makes it possible to `dance` at the same time.
    let song = learn_song().await;
    sing_song(song).await;
}

async fn async_main() {
    let f1 = learn_and_sing();
    let f2 = dance();

    // `join!` is like `.await` but can wait for multiple futures concurrently.
    // If we're temporarily blocked in the `learn_and_sing` future, the `dance`
    // future will take over the current thread. If `dance` becomes blocked,
    // `learn_and_sing` can take back over. If both futures are blocked, then
    // `async_main` is blocked and will yield to the executor.
    futures::join!(f1, f2);
}

fn main() {
    block_on(async_main());
}
```

在本示例中，学习歌曲必须在唱歌之前完成，但学习和唱歌可以与跳舞同时进行。若在 `learn_and_sing` 中使用 `block_on(learn_song())` 而非 `learn_song().await`，在 `learn_song` 运行期间线程将无法做其他事，也就无法同时跳舞。通过对 `learn_song` future 使用 `.await`，若 `learn_song` 被阻塞，我们允许其他任务接管当前线程。这使得在同一线程上并发运行多个 future 直至完成成为可能。
