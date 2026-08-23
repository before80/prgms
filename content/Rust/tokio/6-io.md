+++
title = "6 I/O"
date = 2026-08-23T16:54:00+08:00
weight = 7
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tokio.rs/tokio/tutorial/io](https://tokio.rs/tokio/tutorial/io)

Tokio 中的 I/O 与 `std` 中的工作方式大致相同，但是异步的。有一个用于读取的 trait（[`AsyncRead`]）和一个用于写入的 trait（[`AsyncWrite`]。特定类型会视情况实现这些 trait（[`TcpStream`]、[`File`]、[`Stdout`]）。许多数据结构也实现了 [`AsyncRead`] 和 [`AsyncWrite`]，例如 `Vec<u8>` 和 `&[u8]`。这样就可以在需要 reader 或 writer 的地方使用字节数组。

本页将介绍 Tokio 中基本的 I/O 读写，并通过几个示例进行说明。下一页将深入一个更高级的 I/O 示例。


这两个 trait 提供了从字节流异步读取和向字节流异步写入的能力。这些 trait 上的方法通常不会直接调用，就像你不会手动调用 `Future` trait 的 `poll` 方法一样。相反，你会通过 [`AsyncReadExt`] 和 [`AsyncWriteExt`] 提供的工具方法来使用它们。

让我们简要看看其中几个方法。这些函数都是 `async` 的，必须与 `.await` 一起使用。

## `async fn read()`

[`AsyncReadExt::read`][read] 提供了一个异步方法，用于将数据读入缓冲区，并返回读取的字节数。

**注意：** 当 `read()` 返回 `Ok(0)` 时，表示流已关闭。此后任何对 `read()` 的调用都会立即以 `Ok(0)` 完成。对于 [`TcpStream`] 实例，这表示套接字的读端已关闭。

```rust
use tokio::fs::File;
use tokio::io::{self, AsyncReadExt};

# fn dox() {
#[tokio::main]
async fn main() -> io::Result<()> {
    let mut f = File::open("foo.txt").await?;
    let mut buffer = [0; 10];

    // 最多读取 10 个字节
    let n = f.read(&mut buffer[..]).await?;

    println!("The bytes: {:?}", &buffer[..n]);
    Ok(())
}
# }
```

## `async fn read_to_end()`

[`AsyncReadExt::read_to_end`][read_to_end] 从流中读取所有字节，直到 EOF。

```rust
use tokio::io::{self, AsyncReadExt};
use tokio::fs::File;

# fn dox() {
#[tokio::main]
async fn main() -> io::Result<()> {
    let mut f = File::open("foo.txt").await?;
    let mut buffer = Vec::new();

    // 读取整个文件
    f.read_to_end(&mut buffer).await?;
    Ok(())
}
# }
```

## `async fn write()`

[`AsyncWriteExt::write`][write] 将缓冲区写入 writer，并返回实际写入的字节数。

```rust
use tokio::io::{self, AsyncWriteExt};
use tokio::fs::File;

# fn dox() {
#[tokio::main]
async fn main() -> io::Result<()> {
    let mut file = File::create("foo.txt").await?;

    // 写入字节串的某个前缀，但不一定是全部
    let n = file.write(b"some bytes").await?;

    println!("Wrote the first {} bytes of 'some bytes'.", n);
    Ok(())
}
# }
```

## `async fn write_all()`

[`AsyncWriteExt::write_all`][write_all] 将整个缓冲区写入 writer。

```rust
use tokio::io::{self, AsyncWriteExt};
use tokio::fs::File;

# fn dox() {
#[tokio::main]
async fn main() -> io::Result<()> {
    let mut file = File::create("foo.txt").await?;

    file.write_all(b"some bytes").await?;
    Ok(())
}
# }
```

这两个 trait 还包含许多其他有用的方法。完整列表请参阅 API 文档。

# 辅助函数

此外，与 `std` 一样，[`tokio::io`] 模块也包含许多有用的工具函数，以及用于处理[标准输入][stdin]、[标准输出][stdout]和[标准错误][stderr]的 API。例如，[`tokio::io::copy`][copy] 会异步地将 reader 的全部内容复制到 writer。

```rust
use tokio::fs::File;
use tokio::io;

# fn dox() {
#[tokio::main]
async fn main() -> io::Result<()> {
    let mut reader: &[u8] = b"hello";
    let mut file = File::create("foo.txt").await?;

    io::copy(&mut reader, &mut file).await?;
    Ok(())
}
# }
```

注意，这里利用了字节数组也实现了 `AsyncRead` 这一事实。

# Echo 服务器

让我们通过一些异步 I/O 来练习。我们将编写一个 echo 服务器。

echo 服务器会绑定一个 `TcpListener`，并在循环中接受入站连接。对于每个入站连接，从套接字读取数据并立即写回套接字。客户端向服务器发送数据，并收到完全相同的数据。

我们将用两种略有不同的策略来实现 echo 服务器。

## 使用 `io::copy()`

首先，我们使用 [`io::copy`][copy] 工具来实现 echo 逻辑。

你可以在一个新的二进制文件中编写这段代码：

```bash
$ touch src/bin/echo-server-copy.rs
```

然后可以这样启动（或仅检查编译）：

```bash
$ cargo run --bin echo-server-copy
```

你可以使用 `telnet` 等标准命令行工具来测试服务器，也可以编写一个简单的客户端，例如 [`tokio::net::TcpStream`][tcp_example] 文档中的示例。

这是一个 TCP 服务器，需要一个 accept 循环。每接受一个套接字，就 spawn 一个新任务来处理。

```rust
use tokio::io;
use tokio::net::TcpListener;

# fn dox() {
#[tokio::main]
async fn main() -> io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:6142").await?;

    loop {
        let (mut socket, _) = listener.accept().await?;

        tokio::spawn(async move {
            // 在这里复制数据
        });
    }
}
# }
```

如前所述，这个工具函数接受一个 reader 和一个 writer，并将数据从一方复制到另一方。然而，我们只有一个 `TcpStream`。这个单一值**同时**实现了 `AsyncRead` 和 `AsyncWrite`。由于 `io::copy` 要求 reader 和 writer 都传入 `&mut`，套接字不能同时用作两个参数。

```rust
// 这无法编译
io::copy(&mut socket, &mut socket).await
```

## 拆分 reader + writer

为了解决这个问题，我们必须将套接字拆分为一个 reader 句柄和一个 writer 句柄。拆分 reader/writer 组合的最佳方式取决于具体类型。

任何 reader + writer 类型都可以使用 [`io::split`][split] 工具来拆分。该函数接受单个值，并返回独立的 reader 和 writer 句柄。这两个句柄可以独立使用，包括从不同任务中使用。

例如，echo 客户端可以这样并发处理读写：

```rust
use tokio::io::{self, AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpStream;

# fn dox() {
#[tokio::main]
async fn main() -> io::Result<()> {
    let socket = TcpStream::connect("127.0.0.1:6142").await?;
    let (mut rd, mut wr) = io::split(socket);

    // 在后台写入数据
    tokio::spawn(async move {
        wr.write_all(b"hello\r\n").await?;
        wr.write_all(b"world\r\n").await?;

        // 显式关闭写端，向对端发出 EOF 信号；
        // `io::split` 在 drop 时不会关闭连接。
        wr.shutdown().await?;

        // 有时 Rust 类型推断器需要一点帮助
        Ok::<_, io::Error>(())
    });

    let mut buf = vec![0; 128];

    loop {
        let n = rd.read(&mut buf).await?;

        if n == 0 {
            break;
        }

        println!("GOT {:?}", &buf[..n]);
    }

    Ok(())
}
# }
```

由于 `io::split` 支持**任何**实现了 `AsyncRead + AsyncWrite` 的值，并返回独立句柄，其内部使用了 `Arc` 和 `Mutex`。对于 `TcpStream`，可以避免这种开销。`TcpStream` 提供了两个专用的拆分函数。

[`TcpStream::split`] 接受流的**引用**，并返回 reader 和 writer 句柄。由于使用的是引用，两个句柄必须留在调用 `split()` 的**同一**任务上。这种专用 `split` 是零成本的，不需要 `Arc` 或 `Mutex`。`TcpStream` 还提供 [`into_split`]，支持可跨任务移动的句柄，代价是仅增加一个 `Arc`。

由于 `io::copy()` 是在拥有 `TcpStream` 的同一任务上调用的，我们可以使用 [`TcpStream::split`]。服务器中处理 echo 逻辑的任务变为：

```rust
# use tokio::io;
# use tokio::net::TcpStream;
# fn dox(mut socket: TcpStream) {
tokio::spawn(async move {
    let (mut rd, mut wr) = socket.split();
    
    if io::copy(&mut rd, &mut wr).await.is_err() {
        eprintln!("failed to copy");
    }
});
# }
```

完整代码见[这里][full_copy]。

## 手动复制

现在让我们看看如何手动复制数据来编写 echo 服务器。为此，我们使用 [`AsyncReadExt::read`][read] 和 [`AsyncWriteExt::write_all`][write_all]。

完整的 echo 服务器如下：

```rust
use tokio::io::{self, AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpListener;

# fn dox() {
#[tokio::main]
async fn main() -> io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:6142").await?;

    loop {
        let (mut socket, _) = listener.accept().await?;

        tokio::spawn(async move {
            let mut buf = vec![0; 1024];

            loop {
                match socket.read(&mut buf).await {
                    // 返回 `Ok(0)` 表示远端已关闭
                    Ok(0) => return,
                    Ok(n) => {
                        // 将数据复制回套接字
                        if socket.write_all(&buf[..n]).await.is_err() {
                            // 意外的套接字错误。这里能做的很少，
                            // 所以直接停止处理。
                            return;
                        }
                    }
                    Err(_) => {
                        // 意外的套接字错误。这里能做的很少，
                        // 所以直接停止处理。
                        return;
                    }
                }
            }
        });
    }
}
# }
```

（你可以将这段代码放入 `src/bin/echo-server.rs`，并用 `cargo run --bin echo-server` 启动）。

让我们逐步分析。首先，由于使用了 `AsyncRead` 和 `AsyncWrite` 工具，必须将扩展 trait 引入作用域。

```rust
use tokio::io::{self, AsyncReadExt, AsyncWriteExt};
```

## 分配缓冲区

策略是从套接字读取一些数据到缓冲区，然后将缓冲区内容写回套接字。

```rust
let mut buf = vec![0; 1024];
```

这里明确避免使用栈缓冲区。[前面][send]我们提到过，所有跨越 `.await` 调用的任务数据都必须由任务存储。在本例中，`buf` 会跨越 `.await` 调用。所有任务数据都存储在单一分配中。你可以把它想象成一个 `enum`，每个变体对应某次 `.await` 调用需要存储的数据。

如果缓冲区用栈数组表示，每个已接受套接字 spawn 的任务内部结构可能类似：

```rust
struct Task {
    // 内部任务字段
    task: enum {
        AwaitingRead {
            socket: TcpStream,
            buf: [BufferType],
        },
        AwaitingWriteAll {
            socket: TcpStream,
            buf: [BufferType],
        }

    }
}
```

如果使用栈数组作为缓冲区类型，它会*内联*存储在任务结构中。这会使任务结构变得非常大。此外，缓冲区大小通常是页大小。这反过来会使 `Task` 的尺寸变得尴尬：`$page-size + a-few-bytes`。

编译器对 async 块的布局优化远超基本的 `enum`。实践中，变量不会像 `enum` 那样在变体之间移动。然而，任务结构的大小至少与最大变量一样大。

因此，通常为缓冲区使用独立分配会更高效。

## 处理 EOF

当 TCP 流的读端关闭时，调用 `read()` 会返回 `Ok(0)`。此时退出读循环非常重要。忘记在 EOF 时跳出读循环是常见的 bug 来源。

```rust
# use tokio::io::AsyncReadExt;
# use tokio::net::TcpStream;
# async fn dox(mut socket: TcpStream) {
# let mut buf = vec![0_u8; 1024];
loop {
    match socket.read(&mut buf).await {
        // 返回 `Ok(0)` 表示远端已关闭
        Ok(0) => return,
        // ... 其他情况在这里处理
# _ => unreachable!(),
    }
}
# }
```

忘记在读循环中处理 EOF 通常会导致 100% CPU 的无限循环。由于套接字已关闭，`socket.read()` 会立即返回，然后循环永远重复。

完整代码见[这里][full_manual]。

[full_manual]: https://github.com/tokio-rs/website/blob/master/tutorial-code/io/src/echo-server.rs
[full_copy]: https://github.com/tokio-rs/website/blob/master/tutorial-code/io/src/echo-server-copy.rs

[send]: ../3-spawning/#send-bound
[`AsyncRead`]: https://docs.rs/tokio/1/tokio/io/trait.AsyncRead.html
[`AsyncWrite`]: https://docs.rs/tokio/1/tokio/io/trait.AsyncWrite.html
[`AsyncReadExt`]: https://docs.rs/tokio/1/tokio/io/trait.AsyncReadExt.html
[`AsyncWriteExt`]: https://docs.rs/tokio/1/tokio/io/trait.AsyncWriteExt.html
[`TcpStream`]: https://docs.rs/tokio/1/tokio/net/struct.TcpStream.html
[`File`]: https://docs.rs/tokio/1/tokio/fs/struct.File.html
[`Stdout`]: https://docs.rs/tokio/1/tokio/io/struct.Stdout.html
[read]: https://docs.rs/tokio/1/tokio/io/trait.AsyncReadExt.html#method.read
[read_to_end]: https://docs.rs/tokio/1/tokio/io/trait.AsyncReadExt.html#method.read_to_end
[write]: https://docs.rs/tokio/1/tokio/io/trait.AsyncWriteExt.html#method.write
[write_all]: https://docs.rs/tokio/1/tokio/io/trait.AsyncWriteExt.html#method.write_all
[`tokio::io`]: https://docs.rs/tokio/1/tokio/io/index.html
[stdin]: https://docs.rs/tokio/1/tokio/io/fn.stdin.html
[stdout]: https://docs.rs/tokio/1/tokio/io/fn.stdout.html
[stderr]: https://docs.rs/tokio/1/tokio/io/fn.stderr.html
[copy]: https://docs.rs/tokio/1/tokio/io/fn.copy.html
[split]: https://docs.rs/tokio/1/tokio/io/fn.split.html
[`TcpStream::split`]: https://docs.rs/tokio/1/tokio/net/struct.TcpStream.html#method.split
[`into_split`]: https://docs.rs/tokio/1/tokio/net/struct.TcpStream.html#method.into_split
[tcp_example]: https://docs.rs/tokio/1/tokio/net/struct.TcpStream.html#examples
