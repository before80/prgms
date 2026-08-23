+++
title = "26.2-并发处理连接"
date = 2026-08-22T19:00:00+08:00
weight = 45
type = "docs"
description = "并发处理连接"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 并发处理连接 {#handling-connections-concurrently}


> 原文链接: [https://rust-lang.github.io/async-book/09_example/02_handling_connections_concurrently.html](https://rust-lang.github.io/async-book/09_example/02_handling_connections_concurrently.html)


我们目前代码的问题在于 `listener.incoming()` 是阻塞迭代器。当 `listener` 等待传入连接时，执行器无法运行其他 future，在处理完前一个连接之前也无法处理新连接。

要修复此问题，我们将把 `listener.incoming()` 从阻塞 Iterator 转换为非阻塞 Stream。Stream 与 Iterator 类似，但可以异步消费。更多信息请参阅[关于 Stream 的章节](../../streams/)。

让我们用非阻塞的 `async_std::net::TcpListener` 替换阻塞的 `std::net::TcpListener`，并更新连接处理程序以接受 `async_std::net::TcpStream`：

```rust,ignore
use async_std::prelude::*;

async fn handle_connection(mut stream: TcpStream) {
    let mut buffer = [0; 1024];
    stream.read(&mut buffer).await.unwrap();

    //<-- snip -->
    stream.write(response.as_bytes()).await.unwrap();
    stream.flush().await.unwrap();
}
```

异步版 `TcpListener` 为 `listener.incoming()` 实现了 `Stream` trait，这一改变带来两个好处。

第一是 `listener.incoming()` 不再阻塞执行器。当没有待处理的传入 TCP 连接时，执行器现在可以让出给其他挂起的 future。

第二是 Stream 的元素可以选择并发处理，使用 Stream 的 `for_each_concurrent` 方法。此处我们将利用此方法并发处理每个传入请求。我们需要从 `futures` crate 导入 `Stream` trait，因此我们的 Cargo.toml 现在如下：

```diff
+[dependencies]
+futures = "0.3"

 [dependencies.async-std]
 version = "1.6"
 features = ["attributes"]
```

现在，我们可以通过闭包函数传入 `handle_connection` 来并发处理每个连接。闭包函数取得每个 `TcpStream` 的所有权，并在新的 `TcpStream` 可用时立即运行。只要 `handle_connection` 不阻塞，慢请求将不再阻止其他请求完成。

```rust,ignore
use async_std::net::TcpListener;
use async_std::net::TcpStream;
use futures::stream::StreamExt;

#[async_std::main]
async fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").await.unwrap();
    listener
        .incoming()
        .for_each_concurrent(/* limit */ None, |tcpstream| async move {
            let tcpstream = tcpstream.unwrap();
            handle_connection(tcpstream).await;
        })
        .await;
}
```

# 并行服务请求

我们目前的示例主要将协作式多任务并发（使用异步代码）呈现为抢占式多任务（使用线程）的替代方案。然而，异步代码和线程并不互斥。在我们的示例中，`for_each_concurrent` 并发处理每个连接，但在同一线程上。`async-std` crate 也允许我们将任务生成到单独线程上。由于 `handle_connection` 既是 `Send` 又是非阻塞的，与 `async_std::task::spawn` 一起使用是安全的。大致如下：

```rust
use async_std::task::spawn;

#[async_std::main]
async fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").await.unwrap();
    listener
        .incoming()
        .for_each_concurrent(/* limit */ None, |stream| async move {
            let stream = stream.unwrap();
            spawn(handle_connection(stream));
        })
        .await;
}
```

现在我们同时使用协作式多任务并发和抢占式多任务来处理多个请求！更多信息请参阅[多线程执行器一节](../../ecosystem/#single-threading-vs-multithreading)。
