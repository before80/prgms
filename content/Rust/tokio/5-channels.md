+++
title = "5 通道"
date = 2026-08-23T16:54:00+08:00
weight = 6
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tokio.rs/tokio/tutorial/channels](https://tokio.rs/tokio/tutorial/channels)

既然我们已经了解了 Tokio 中的并发，让我们在客户端应用这些知识。将我们之前编写的服务器代码放入一个显式的二进制文件中：

```bash
$ mkdir src/bin
$ mv src/main.rs src/bin/server.rs
```

然后创建一个新的二进制文件，其中包含客户端代码：

```bash
$ touch src/bin/client.rs
```

你将在此文件中编写本页的代码。每当你想运行它时，你必须先在另一个终端窗口中启动服务器：

```bash
$ cargo run --bin server
```

然后**单独**运行客户端：

```bash
$ cargo run --bin client
```

话虽如此，让我们开始编码吧！

假设我们想并发运行两个 Redis 命令。我们可以为每个命令生成一个任务。这样两个命令就会并发执行。

起初，我们可能会尝试类似这样的代码：

```rust
use mini_redis::client;

#[tokio::main]
async fn main() {
    // 建立与服务器的连接
    let mut client = client::connect("127.0.0.1:6379").await.unwrap();

    // 生成两个任务，一个获取键，另一个设置键
    let t1 = tokio::spawn(async {
        let res = client.get("foo").await;
    });

    let t2 = tokio::spawn(async {
        client.set("foo", "bar".into()).await;
    });

    t1.await.unwrap();
    t2.await.unwrap();
}
```

这无法编译，因为两个任务都需要以某种方式访问 `client`。由于 `Client` 没有实现 `Copy`，没有一些促进共享的代码就无法编译。此外，`Client::set` 接受 `&mut self`，这意味着调用它需要独占访问。我们可以为每个任务打开一个连接，但这不是理想的。我们不能使用 `std::sync::Mutex`，因为需要在持有锁时调用 `.await`。我们可以使用 `tokio::sync::Mutex`，但这只允许一个正在进行的请求。如果客户端实现了[管道][pipelining]（简而言之，发送许多命令而不等待每个先前命令的响应），异步互斥锁会导致连接利用不足。

[pipelining]: https://redis.io/topics/pipelining


答案是使用消息传递。该模式涉及生成一个专用任务来管理 `client` 资源。任何希望发出请求的任务都会向 `client` 任务发送消息。`client` 任务代表发送者发出请求，响应被发送回发送者。

使用这种策略，只建立一个连接。管理 `client` 的任务能够获得独占访问以调用 `get` 和 `set`。此外，通道充当缓冲区。当 `client` 任务忙碌时，操作可以发送到 `client` 任务。一旦 `client` 任务可以处理新请求，它就会从通道中取出下一个请求。这可以提高吞吐量，并扩展以支持连接池。

# Tokio 的通道原语

Tokio 提供了[多种通道][channels]，每种服务于不同的目的。

- [mpsc]：多生产者、单消费者通道。可以发送许多值。
- [oneshot]：单生产者、单消费者通道。只能发送单个值。
- [broadcast]：多生产者、多消费者。可以发送许多值。每个接收者都会看到每个值。
- [watch]：多生产者、多消费者。可以发送许多值，但不保留历史记录。接收者只看到最新的值。

如果你需要一个多生产者多消费者通道，且每个消息只有一个消费者看到，你可以使用 [`async-channel`] crate。还有一些用于异步 Rust 之外的通道，例如 [`std::sync::mpsc`] 和 [`crossbeam::channel`]。这些通道通过阻塞线程来等待消息，这在异步代码中是不允许的。

在本节中，我们将使用 [mpsc] 和 [oneshot]。其他类型的消息传递通道将在后面的章节中探讨。本节的完整代码可在[这里][full]找到。

[channels]: https://docs.rs/tokio/1/tokio/sync/index.html
[mpsc]: https://docs.rs/tokio/1/tokio/sync/mpsc/index.html
[oneshot]: https://docs.rs/tokio/1/tokio/sync/oneshot/index.html
[broadcast]: https://docs.rs/tokio/1/tokio/sync/broadcast/index.html
[watch]: https://docs.rs/tokio/1/tokio/sync/watch/index.html
[`async-channel`]: https://docs.rs/async-channel/
[`std::sync::mpsc`]: https://doc.rust-lang.org/stable/std/sync/mpsc/index.html
[`crossbeam::channel`]: https://docs.rs/crossbeam/latest/crossbeam/channel/index.html

# 定义消息类型

在大多数情况下，使用消息传递时，接收消息的任务会响应多个命令。在我们的情况下，任务将响应 `GET` 和 `SET` 命令。为此建模，我们首先定义一个 `Command` 枚举，并为每种命令类型包含一个变体。

```rust
use bytes::Bytes;

#[derive(Debug)]
enum Command {
    Get {
        key: String,
    },
    Set {
        key: String,
        val: Bytes,
    }
}
```

# 创建通道

在 `main` 函数中，创建一个 `mpsc` 通道。

```rust
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    // 创建一个容量最多为 32 的新通道。
    let (tx, mut rx) = mpsc::channel(32);
# tx.send(()).await.unwrap();

    // ... 其余内容在此
}
```

`mpsc` 通道用于**发送**命令到管理 redis 连接的任务。多生产者能力允许从许多任务发送消息。创建通道返回两个值：一个发送者和一个接收者。这两个句柄分开使用。它们可以被移动到不同的任务。

通道以 32 的容量创建。如果消息发送速度比接收速度快，通道会存储它们。一旦通道中存储了 32 条消息，调用 `send(...).await` 将进入睡眠，直到接收者移除一条消息。

从多个任务发送是通过**克隆** `Sender` 完成的。例如：

```rust
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel(32);
    let tx2 = tx.clone();

    tokio::spawn(async move {
        tx.send("sending from first handle").await.unwrap();
    });

    tokio::spawn(async move {
        tx2.send("sending from second handle").await.unwrap();
    });

    while let Some(message) = rx.recv().await {
        println!("GOT = {}", message);
    }
}
```

两条消息都发送到单个 `Receiver` 句柄。无法克隆 `mpsc` 通道的接收者。

当每个 `Sender` 都离开作用域或以其他方式被 drop 时，就无法再向通道发送更多消息。此时，`Receiver` 上的 `recv` 调用将返回 `None`，这意味着所有发送者都已消失，通道已关闭。

在我们管理 Redis 连接的任务的情况下，它知道一旦通道关闭就可以关闭 Redis 连接，因为该连接不会再被使用。

# 生成管理器任务

接下来，生成一个处理来自通道的消息的任务。首先，建立到 Redis 的客户端连接。然后，通过 Redis 连接发出接收到的命令。

```rust
use mini_redis::client;
# enum Command {
#    Get { key: String },
#    Set { key: String, val: bytes::Bytes }
# }
# async fn dox() {
# let (_, mut rx) = tokio::sync::mpsc::channel(10);
// `move` 关键字用于将 `rx` 的所有权**移动**到任务中。
let manager = tokio::spawn(async move {
    // 建立与服务器的连接
    let mut client = client::connect("127.0.0.1:6379").await.unwrap();

    // 开始接收消息
    while let Some(cmd) = rx.recv().await {
        use Command::*;

        match cmd {
            Get { key } => {
                client.get(&key).await;
            }
            Set { key, val } => {
                client.set(&key, val).await;
            }
        }
    }
});
# }
```

现在，更新两个任务，通过通道发送命令，而不是直接在 Redis 连接上发出命令。

```rust
# #[derive(Debug)]
# enum Command {
#    Get { key: String },
#    Set { key: String, val: bytes::Bytes }
# }
# async fn dox() {
# let (mut tx, _) = tokio::sync::mpsc::channel(10);
// `Sender` 句柄被移动到任务中。由于有两个
// 任务，我们需要第二个 `Sender`。
let tx2 = tx.clone();

// 生成两个任务，一个获取键，另一个设置键
let t1 = tokio::spawn(async move {
    let cmd = Command::Get {
        key: "foo".to_string(),
    };

    tx.send(cmd).await.unwrap();
});

let t2 = tokio::spawn(async move {
    let cmd = Command::Set {
        key: "foo".to_string(),
        val: "bar".into(),
    };

    tx2.send(cmd).await.unwrap();
});
# }
```

在 `main` 函数的底部，我们 `.await` join handle，以确保在进程退出之前命令完全完成。

```rust
# type Jh = tokio::task::JoinHandle<()>;
# async fn dox(t1: Jh, t2: Jh, manager: Jh) {
t1.await.unwrap();
t2.await.unwrap();
manager.await.unwrap();
# }
```

# 接收响应

最后一步是从管理器任务接收响应。`GET` 命令需要获取值，`SET` 命令需要知道操作是否成功完成。

要传递响应，使用 `oneshot` 通道。`oneshot` 通道是一种针对发送单个值优化的单生产者、单消费者通道。在我们的情况下，单个值就是响应。

与 `mpsc` 类似，`oneshot::channel()` 返回一个发送者和接收者句柄。

```rust
use tokio::sync::oneshot;

# async fn dox() {
let (tx, rx) = oneshot::channel();
# tx.send(()).unwrap();
# }
```

与 `mpsc` 不同，不指定容量，因为容量始终为一。此外，两个句柄都不能被克隆。

要从管理器任务接收响应，在发送命令之前，创建一个 `oneshot` 通道。通道的 `Sender` 半部分包含在发送给管理器任务的命令中。接收半部分用于接收响应。

首先，更新 `Command` 以包含 `Sender`。为了方便，使用类型别名来引用 `Sender`。

```rust
use tokio::sync::oneshot;
use bytes::Bytes;

/// 多种不同的命令通过单个通道进行多路复用。
#[derive(Debug)]
enum Command {
    Get {
        key: String,
        resp: Responder<Option<Bytes>>,
    },
    Set {
        key: String,
        val: Bytes,
        resp: Responder<()>,
    },
}

/// 由请求者提供，由管理器任务用于将命令响应发送回请求者。
type Responder<T> = oneshot::Sender<mini_redis::Result<T>>;
```

现在，更新发出命令的任务以包含 `oneshot::Sender`。

```rust
# use tokio::sync::{oneshot, mpsc};
# use bytes::Bytes;
# #[derive(Debug)]
# enum Command {
#     Get { key: String, resp: Responder<Option<bytes::Bytes>> },
#     Set { key: String, val: Bytes, resp: Responder<()> },
# }
# type Responder<T> = oneshot::Sender<mini_redis::Result<T>>;
# fn dox() {
# let (mut tx, mut rx) = mpsc::channel(10);
# let mut tx2 = tx.clone();
let t1 = tokio::spawn(async move {
    let (resp_tx, resp_rx) = oneshot::channel();
    let cmd = Command::Get {
        key: "foo".to_string(),
        resp: resp_tx,
    };

    // 发送 GET 请求
    tx.send(cmd).await.unwrap();

    // 等待响应
    let res = resp_rx.await;
    println!("GOT = {:?}", res);
});

let t2 = tokio::spawn(async move {
    let (resp_tx, resp_rx) = oneshot::channel();
    let cmd = Command::Set {
        key: "foo".to_string(),
        val: "bar".into(),
        resp: resp_tx,
    };

    // 发送 SET 请求
    tx2.send(cmd).await.unwrap();

    // 等待响应
    let res = resp_rx.await;
    println!("GOT = {:?}", res);
});
# }
```

最后，更新管理器任务以通过 `oneshot` 通道发送响应。

```rust
# use tokio::sync::{oneshot, mpsc};
# use bytes::Bytes;
# #[derive(Debug)]
# enum Command {
#     Get { key: String, resp: Responder<Option<bytes::Bytes>> },
#     Set { key: String, val: Bytes, resp: Responder<()> },
# }
# type Responder<T> = oneshot::Sender<mini_redis::Result<T>>;
# async fn dox(mut client: mini_redis::client::Client) {
# let (_, mut rx) = mpsc::channel::<Command>(10);
while let Some(cmd) = rx.recv().await {
    match cmd {
        Command::Get { key, resp } => {
            let res = client.get(&key).await;
            // 忽略错误
            let _ = resp.send(res);
        }
        Command::Set { key, val, resp } => {
            let res = client.set(&key, val).await;
            // 忽略错误
            let _ = resp.send(res);
        }
    }
}
# }
```

在 `oneshot::Sender` 上调用 `send` 会立即完成，**不需要** `.await`。这是因为 `oneshot` 通道上的 `send` 总是会立即失败或成功，无需任何形式的等待。

当接收者半部分已被 drop 时，在 oneshot 通道上发送值会返回 `Err`。这表示接收者不再对响应感兴趣。在我们的场景中，接收者取消兴趣是可以接受的事件。`resp.send(...)` 返回的 `Err` 不需要处理。

你可以在[这里][full]找到完整代码。

# 背压和有界通道

每当引入并发或排队时，确保排队是有界的并且系统能够优雅地处理负载是很重要的。无界队列最终会填满所有可用内存，并以不可预测的方式导致系统失败。

Tokio 小心避免隐式排队。这很大一部分是因为异步操作是惰性的。考虑以下代码：

```rust
# fn async_op() {}
# fn dox() {
loop {
    async_op();
}
# }
# fn main() {}
```

如果异步操作急切地运行，循环会反复将新的 `async_op` 排队运行，而不确保前一个操作已完成。这会导致隐式无界排队。基于回调的系统和**急切**的 future 系统特别容易受到这种情况的影响。

然而，使用 Tokio 和异步 Rust，上面的代码片段**不会**导致 `async_op` 运行。这是因为从未调用 `.await`。如果代码片段更新为使用 `.await`，则循环会等待操作完成后再重新开始。

```rust
# async fn async_op() {}
# async fn dox() {
loop {
    // 在 `async_op` 完成之前不会重复
    async_op().await;
}
# }
# fn main() {}
```

并发和排队必须显式引入。实现方式包括：

* `tokio::spawn`
* `select!`
* `join!`
* `mpsc::channel`

这样做时，请注意确保并发总量是有界的。例如，编写 TCP accept 循环时，确保打开的套接字总数是有界的。使用 `mpsc::channel` 时，选择一个可管理的通道容量。具体的边界值将因应用程序而异。

谨慎选择合理的边界是编写可靠的 Tokio 应用程序的重要组成部分。

[full]: https://github.com/tokio-rs/website/blob/master/tutorial-code/channels/src/main.rs
