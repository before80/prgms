+++
title = "26.1-运行异步代码"
date = 2026-08-22T19:00:00+08:00
weight = 44
type = "docs"
description = "运行异步代码"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 运行异步代码 {#running-asynchronous-code}


> 原文链接: [https://rust-lang.github.io/async-book/09_example/01_running_async_code.html](https://rust-lang.github.io/async-book/09_example/01_running_async_code.html)


HTTP 服务器应能并发服务多个客户端；也就是说，在处理当前请求时不应等待先前请求完成。书中通过[创建线程池](https://doc.rust-lang.org/book/ch20-02-multithreaded.html#turning-our-single-threaded-server-into-a-multithreaded-server)解决此问题，每个连接在独立线程上处理。此处我们不通过添加线程提高吞吐量，而是用异步代码达到同样效果。

让我们将 `handle_connection` 修改为通过声明为 `async fn` 来返回 future：

```rust,ignore
async fn handle_connection(mut stream: TcpStream) {
    //<-- snip -->
}
```

在函数声明中添加 `async` 会将其返回类型从单元类型 `()` 改为实现 `Future<Output=()>` 的类型。

若尝试编译，编译器会警告这不会工作：

```console
$ cargo check
    Checking async-rust v0.1.0 (file:///projects/async-rust)
warning: unused implementer of `std::future::Future` that must be used
  --> src/main.rs:12:9
   |
12 |         handle_connection(stream);
   |         ^^^^^^^^^^^^^^^^^^^^^^^^^^
   |
   = note: `#[warn(unused_must_use)]` on by default
   = note: futures do nothing unless you `.await` or poll them
```

因为我们没有 `await` 或 `poll` `handle_connection` 的结果，它永远不会运行。若运行服务器并在浏览器中访问 `127.0.0.1:7878`，你会看到连接被拒绝；我们的服务器没有处理请求。

我们不能在同步代码中单独 `await` 或 `poll` future。我们需要异步运行时来处理调度和将 future 运行至完成。有关异步运行时、执行器和反应器的更多信息，请参阅[选择运行时一节](../../ecosystem/)。列出的任何运行时都可用于本项目，但在这些示例中，我们选择使用 `async-std` crate。

## 添加异步运行时

以下示例演示将同步代码重构为使用异步运行时；此处为 `async-std`。`async-std` 的 `#[async_std::main]` 属性允许我们编写异步 main 函数。要使用它，请在 `Cargo.toml` 中为 `async-std` 启用 `attributes` 功能：

```toml
[dependencies.async-std]
version = "1.6"
features = ["attributes"]
```

作为第一步，我们将切换到异步 main 函数，并 `await` 异步版 `handle_connection` 返回的 future。然后，我们测试服务器的响应。

大致如下：

```rust
#[async_std::main]
async fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    for stream in listener.incoming() {
        let stream = stream.unwrap();
        // 警告：这不是并发的！
        handle_connection(stream).await;
    }
}
```

现在，让我们测试服务器是否能并发处理连接。仅将 `handle_connection` 改为异步并不意味着服务器能同时处理多个连接，我们很快会看到原因。

为说明这一点，让我们模拟慢请求。当客户端请求 `127.0.0.1:7878/sleep` 时，我们的服务器将休眠 5 秒：

```rust,ignore
use std::time::Duration;
use async_std::task;

async fn handle_connection(mut stream: TcpStream) {
    let mut buffer = [0; 1024];
    stream.read(&mut buffer).unwrap();

    let get = b"GET / HTTP/1.1\r\n";
    let sleep = b"GET /sleep HTTP/1.1\r\n";

    let (status_line, filename) = if buffer.starts_with(get) {
        ("HTTP/1.1 200 OK\r\n\r\n", "hello.html")
    } else if buffer.starts_with(sleep) {
        task::sleep(Duration::from_secs(5)).await;
        ("HTTP/1.1 200 OK\r\n\r\n", "hello.html")
    } else {
        ("HTTP/1.1 404 NOT FOUND\r\n\r\n", "404.html")
    };
    let contents = fs::read_to_string(filename).unwrap();

    let response = format!("{status_line}{contents}");
    stream.write(response.as_bytes()).unwrap();
    stream.flush().unwrap();
}
```

这与书中[模拟慢请求](https://doc.rust-lang.org/book/ch20-02-multithreaded.html#simulating-a-slow-request-in-the-current-server-implementation)非常相似，但有一个重要区别：我们使用非阻塞函数 `async_std::task::sleep` 而非阻塞函数 `std::thread::sleep`。请记住，即使某段代码在 `async fn` 内运行并被 `await`，它仍可能阻塞。要测试服务器是否并发处理连接，我们需要确保 `handle_connection` 是非阻塞的。

若运行服务器，你会看到对 `127.0.0.1:7878/sleep` 的请求会阻塞任何其他传入请求 5 秒！这是因为在 `await` `handle_connection` 的结果时没有其他并发任务可以推进。在下一节中，我们将看到如何使用异步代码并发处理连接。
