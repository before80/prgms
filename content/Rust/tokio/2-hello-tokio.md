+++
title = "2 Hello Tokio"
date = 2026-08-23T16:54:00+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tokio.rs/tokio/tutorial/hello-tokio](https://tokio.rs/tokio/tutorial/hello-tokio)

我们将从一个非常基础的 Tokio 应用开始。它会连接到 Mini-Redis 服务器，将键 `hello` 的值设置为 `world`，然后读回该键。这将使用 Mini-Redis 客户端库来完成。


## 创建新 crate

首先，创建一个新的 Rust 应用：

```bash
$ cargo new my-redis
$ cd my-redis
```

## 添加依赖

接下来，打开 `Cargo.toml`，在 `[dependencies]` 下方添加以下内容：

```toml
tokio = { version = "1", features = ["full"] }
mini-redis = "0.4"
```

## 编写代码

然后，打开 `main.rs`，将文件内容替换为：

```rust
use mini_redis::{client, Result};

# fn dox() {
#[tokio::main]
async fn main() -> Result<()> {
    // 打开到 mini-redis 地址的连接。
    let mut client = client::connect("127.0.0.1:6379").await?;

    // 将键 "hello" 的值设置为 "world"
    client.set("hello", "world".into()).await?;

    // 获取键 "hello"
    let result = client.get("hello").await?;

    println!("got value from the server; result={:?}", result);

    Ok(())
}
# }
```

确保 Mini-Redis 服务器正在运行。在另一个终端窗口中运行：

```bash
$ mini-redis-server
```

如果尚未安装 mini-redis，可以使用以下命令安装：

```bash
$ cargo install mini-redis
```

现在，运行 `my-redis` 应用：

```bash
$ cargo run
got value from the server; result=Some(b"world")
```

成功！

你可以在[这里][full]找到完整代码。

[full]: https://github.com/tokio-rs/website/blob/master/tutorial-code/hello-tokio/src/main.rs

# 逐步解析

我们来花点时间回顾一下刚才做了什么。代码不多，但发生了很多事情。

```rust
# use mini_redis::client;
# async fn dox() -> mini_redis::Result<()> {
let mut client = client::connect("127.0.0.1:6379").await?;
# Ok(())
# }
```

[`client::connect`] 函数由 `mini-redis` crate 提供。它会异步建立与指定远程地址的 TCP 连接。连接建立后，会返回一个 `client` 句柄。尽管操作是异步执行的，我们编写的代码**看起来**却是同步的。唯一能表明操作是异步的，就是 `.await` 运算符。

[`client::connect`]: https://docs.rs/mini-redis/0.4/mini_redis/client/fn.connect.html

## 什么是异步编程？

大多数计算机程序按照编写的顺序执行。先执行第一行，再执行下一行，依此类推。在同步编程中，当程序遇到无法立即完成的操作时，它会阻塞直到操作完成。例如，建立 TCP 连接需要与对端通过网络进行交互，这可能需要相当长的时间。在此期间，线程会被阻塞。

在异步编程中，无法立即完成的操作会被挂起到后台。线程不会被阻塞，可以继续运行其他任务。操作完成后，任务会恢复执行，从挂起处继续处理。我们之前的示例只有一个任务，因此挂起时不会发生其他事情，但异步程序通常有许多这样的任务。

尽管异步编程可以使应用更快，但它往往会使程序复杂得多。程序员必须跟踪恢复工作所需的所有状态，以便在异步操作完成后继续执行。从历史上看，这是一项繁琐且容易出错的工作。

## 编译期绿色线程

Rust 使用名为 [`async/await`] 的特性来实现异步编程。执行异步操作的函数用 `async` 关键字标记。在我们的示例中，`connect` 函数定义如下：

```rust
use mini_redis::Result;
use mini_redis::client::Client;
use tokio::net::ToSocketAddrs;

pub async fn connect<T: ToSocketAddrs>(addr: T) -> Result<Client> {
    // ...
# unimplemented!()
}
```

`async fn` 定义看起来就像普通的同步函数，但实际上是异步运行的。Rust 在**编译**时将 `async fn` 转换为异步执行的例程。`async fn` 内对 `.await` 的任何调用都会将控制权交还给线程。操作在后台处理时，线程可以执行其他工作。

> **warning**
> 尽管其他语言也实现了 [`async/await`]，但 Rust 采用了独特的方式。主要区别在于，Rust 的异步操作是**惰性的**。这会导致与其他语言不同的运行时语义。

[`async/await`]: https://en.wikipedia.org/wiki/Async/await

如果这还不太清楚，别担心。我们将在本指南中进一步探讨 `async/await`。

## 使用 `async/await`

异步函数的调用方式与其他 Rust 函数相同。然而，调用这些函数并不会执行函数体。相反，调用 `async fn` 会返回一个表示该操作的值。从概念上讲，这类似于零参数闭包。要真正运行该操作，应对返回值使用 `.await` 运算符。

例如，给定程序

```rust
async fn say_world() {
    println!("world");
}

#[tokio::main]
async fn main() {
    // 调用 `say_world()` 不会执行 `say_world()` 的函数体。
    let op = say_world();

    // 这条 println! 会先执行
    println!("hello");

    // 对 `op` 调用 `.await` 会开始执行 `say_world`。
    op.await;
}
```

输出：

```text
hello
world
```

`async fn` 的返回值是一个实现了 [`Future`] trait 的匿名类型。

[`Future`]: https://doc.rust-lang.org/std/future/trait.Future.html

## 异步 `main` 函数

用于启动应用的 main 函数与大多数 Rust crate 中常见的不同。

1. 它是一个 `async fn`
2. 它带有 `#[tokio::main]` 注解

使用 `async fn` 是因为我们要进入异步上下文。然而，异步函数必须由[运行时]执行。运行时包含异步任务调度器，提供事件驱动的 I/O、定时器等。运行时不会自动启动，因此 main 函数需要启动它。

`#[tokio::main]` 是一个宏。它将 `async fn main()` 转换为同步的 `fn main()`，该函数会初始化运行时实例并执行异步 main 函数。

例如，以下代码：

```rust
#[tokio::main]
async fn main() {
    println!("hello");
}
```

会被转换为：

```rust
fn main() {
    let mut rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async {
        println!("hello");
    })
}
```

Tokio 运行时的细节将在后面介绍。

[runtime]: https://docs.rs/tokio/1/tokio/runtime/index.html

## Cargo features

在本教程中依赖 Tokio 时，启用了 `full` feature 标志：

```toml
tokio = { version = "1", features = ["full"] }
```

Tokio 拥有大量功能（TCP、UDP、Unix 套接字、定时器、同步工具、多种调度器类型等）。并非所有应用都需要全部功能。在尝试优化编译时间或最终应用体积时，应用可以选择**仅**启用它使用的功能。
