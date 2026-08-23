+++
title = "23.3-Spawning"
date = 2026-08-22T19:00:00+08:00
weight = 37
type = "docs"
description = "Spawning"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# Spawning {#spawning}


> 原文链接: [https://rust-lang.github.io/async-book/06_multiple_futures/04_spawning.html](https://rust-lang.github.io/async-book/06_multiple_futures/04_spawning.html)


Spawning 允许你在后台运行新的异步任务。这使我们能在其运行的同时继续执行其他代码。

假设我们有一个 Web 服务器，希望在不阻塞主线程的情况下接受连接。为此，我们可以使用 `async_std::task::spawn` 函数创建并运行处理连接的新任务。该函数接收一个 future 并返回 `JoinHandle`，可在任务完成后用于等待任务结果。

```rust,edition2018
use async_std::{task, net::TcpListener, net::TcpStream};
use futures::AsyncWriteExt;

async fn process_request(stream: &mut TcpStream) -> Result<(), std::io::Error>{
    stream.write_all(b"HTTP/1.1 200 OK\r\n\r\n").await?;
    stream.write_all(b"Hello World").await?;
    Ok(())
}

async fn main() {
    let listener = TcpListener::bind("127.0.0.1:8080").await.unwrap();
    loop {
        // 接受新连接
        let (mut stream, _) = listener.accept().await.unwrap();
        // 现在处理此请求，而不阻塞主循环
        task::spawn(async move {process_request(&mut stream).await});
    }
}
```

`spawn` 返回的 `JoinHandle` 实现了 `Future` trait，因此我们可以 `.await` 它以获取任务结果。这会阻塞当前任务直到生成的任务完成。若不对任务进行 await，程序将继续执行而不等待任务；若函数在任务完成前结束，任务会被取消。

```rust,edition2018
use futures::future::join_all;
async fn task_spawner(){
    let tasks = vec![
        task::spawn(my_task(Duration::from_secs(1))),
        task::spawn(my_task(Duration::from_secs(2))),
        task::spawn(my_task(Duration::from_secs(3))),
    ];
    // 若不 await 这些任务且函数结束，它们会被丢弃
    join_all(tasks).await;
}
```

要在主任务与生成任务之间通信，可以使用所用异步运行时提供的通道。
