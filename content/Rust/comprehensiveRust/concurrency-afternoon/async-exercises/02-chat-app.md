+++
title = "5.2 广播聊天应用程序"
date = 2026-08-11T11:30:00+08:00
weight = 385
type = "docs"
description = "02-广播聊天应用程序 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/async-exercises/chat-app.html](https://google.github.io/comprehensive-rust/concurrency/async-exercises/chat-app.html)

# 5.2 广播聊天应用程序

在本练习中，我们希望使用新知识来实现广播聊天
应用程序。我们有一个聊天服务器，客户端可以连接到该服务器并发布他们的信息
消息。客户端从标准输入读取用户消息，并将其发送
到服务器。聊天服务器将其收到的每条消息广播给所有人
客户。

为此，我们在服务器上使用[广播通道][1]，并且
[`tokio_websockets`][2]用于客户端和服务器之间的通信。

创建一个新的 Cargo 项目并添加以下依赖项：

_Cargo.toml_：

```toml
[package]
name = "chat-async"
version = "0.1.0"
edition = "2024"

[dependencies]
futures-util = { version = "0.3.32", features = ["sink"] }
http = "1.4.1"
tokio = { version = "1.52.3", features = ["full"] }
tokio-websockets = { version = "0.13.2", features = ["client", "fastrand", "server", "sha1_smol"] }
```

## 所需的 API

您将需要以下功能`tokio`和
[`tokio_websockets`][2]。花一些时间熟悉 API。

- [StreamExt::next()][3] 实现者`WebSocketStream`: 对于异步
  从 Websocket 流读取消息。
- [SinkExt::send()][4] 实现者`WebSocketStream`: 对于异步
  在 Websocket 流上发送消息。
- [Lines::next_line()][5]：用于异步读取用户消息
  标准输入。
- [Sender::subscribe()][6]：用于订阅广播频道。

## 两个二进制文件

通常在 Cargo 项目中，您只能拥有一个二进制文件，并且一个`src/main.rs`文件。在这个项目中，我们需要两个二进制文件。一份给客户，一份给客户
服务器。您可以将它们设为两个独立的 Cargo 项目，但我们
将它们放入具有两个二进制文件的单个 Cargo 项目中。为了做到这一点，
客户端和服务器代码应该放在下面`src/bin`（参见
[文档][7]）。

将以下服务器和客户端代码复制到`src/bin/server.rs`和`src/bin/client.rs`， 分别。您的任务是完成这些文件
如下所述。

_src/bin/server.rs_：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use futures_util::sink::SinkExt;
use futures_util::stream::StreamExt;
use std::error::Error;
use std::net::SocketAddr;
use tokio::net::{TcpListener, TcpStream};
use tokio::sync::broadcast::{Sender, channel};
use tokio_websockets::{Message, ServerBuilder, WebSocketStream};


async fn handle_connection(
    addr: SocketAddr,
    mut ws_stream: WebSocketStream<TcpStream>,
    bcast_tx: Sender<String>,
) -> Result<(), Box<dyn Error + Send + Sync>> {


    // TODO：有关提示，请参阅下面的任务描述。

}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error + Send + Sync>> {
    let (bcast_tx, _) = channel(16);

    let listener = TcpListener::bind("127.0.0.1:2000").await?;
    println!("listening on port 2000");

    loop {
        let (socket, addr) = listener.accept().await?;
        println!("New connection from {addr:?}");
        let bcast_tx = bcast_tx.clone();
        tokio::spawn(async move {
            // 将原始 TCP 流包装到 websocket 中。
            let (_req, ws_stream) = ServerBuilder::new().accept(socket).await?;

            handle_connection(addr, ws_stream, bcast_tx).await
        });
    }
}
```

_src/bin/client.rs_：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use futures_util::SinkExt;
use futures_util::stream::StreamExt;
use http::Uri;
use tokio::io::{AsyncBufReadExt, BufReader};
use tokio_websockets::{ClientBuilder, Message};

#[tokio::main]
async fn main() -> Result<(), tokio_websockets::Error> {
    let (mut ws_stream, _) =
        ClientBuilder::from_uri(Uri::from_static("ws://127.0.0.1:2000"))
            .connect()
            .await?;

    let stdin = tokio::io::stdin();
    let mut stdin = BufReader::new(stdin).lines();


    // TODO：有关提示，请参阅下面的任务描述。

}
```

## 运行二进制文件

使用以下命令运行服务器：

```shell
cargo run --bin server
```

和客户：

```shell
cargo run --bin client
```

## 任务

- 实施`handle_connection`函数于`src/bin/server.rs`.
  - 提示：使用`tokio::select!`用于同时执行两个任务
    连续循环。一个任务接收来自客户端的消息并广播
    他们。另一个将服务器收到的消息发送给客户端。
- 完成主要功能`src/bin/client.rs`.
  - 提示：和以前一样，使用`tokio::select!`在连续循环中同时进行
    执行两个任务：（1）从标准输入读取用户消息和
    将它们发送到服务器，以及 (2) 从服务器接收消息，以及
    为用户显示它们。
- 可选：完成后，更改代码以向所有人广播消息
  客户端，而是消息的发送者。

[1]: https://docs.rs/tokio/latest/tokio/sync/broadcast/fn.channel.html
[2]: https://docs.rs/tokio-websockets/
[3]: https://docs.rs/futures-util/0.3.28/futures_util/stream/trait.StreamExt.html#method.next
[4]: https://docs.rs/futures-util/0.3.28/futures_util/sink/trait.SinkExt.html#method.send
[5]: https://docs.rs/tokio/latest/tokio/io/struct.Lines.html#method.next_line
[6]: https://docs.rs/tokio/latest/tokio/sync/broadcast/struct.Sender.html#method.subscribe
[7]: https://doc.rust-lang.org/cargo/reference/cargo-targets.html#binaries
