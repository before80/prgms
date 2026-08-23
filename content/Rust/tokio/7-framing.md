+++
title = "7 分帧"
date = 2026-08-23T16:54:00+08:00
weight = 8
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tokio.rs/tokio/tutorial/framing](https://tokio.rs/tokio/tutorial/framing)

现在我们将把刚学到的 I/O 知识应用到 Mini-Redis 的分帧层实现上。分帧（framing）是将字节流转换为帧流的过程。帧是两个对等方之间传输的数据单元。Redis 协议帧定义如下：

```rust
use bytes::Bytes;

enum Frame {
    Simple(String),
    Error(String),
    Integer(u64),
    Bulk(Bytes),
    Null,
    Array(Vec<Frame>),
}
```

注意，帧只包含数据，不包含任何语义。命令解析和实现在更高层进行。

对于 HTTP，一帧可能如下所示：

```rust
# type Method = ();
# type Uri = ();
# type Version = ();
# type HeaderMap = ();
# type StatusCode = ();
enum HttpFrame {
    RequestHead {
        method: Method,
        uri: Uri,
        version: Version,
        headers: HeaderMap,
    },
    ResponseHead {
        status: StatusCode,
        version: Version,
        headers: HeaderMap,
    },
    BodyChunk {
        chunk: Bytes,
    },
}
```

要为 Mini-Redis 实现分帧，我们将实现一个 `Connection` 结构体，它包装 `TcpStream` 并读写 `mini_redis::Frame` 值。

```rust
use tokio::net::TcpStream;
use mini_redis::{Frame, Result};

struct Connection {
    stream: TcpStream,
    // ... 其他字段
}

impl Connection {
    /// 从连接读取一帧。
    /// 
    /// 如果到达 EOF，返回 `None`
    pub async fn read_frame(&mut self)
        -> Result<Option<Frame>>
    {
        // 实现放在这里
# unimplemented!();
    }

    /// 向连接写入一帧。
    pub async fn write_frame(&mut self, frame: &Frame)
        -> Result<()>
    {
        // 实现放在这里
# unimplemented!();
    }
}
```

Redis 线路协议的详细信息见[这里][proto]。完整的 `Connection` 代码见[这里][full]。

[proto]: https://redis.io/topics/protocol
[full]: https://github.com/tokio-rs/mini-redis/blob/tutorial/src/connection.rs

# 缓冲读取

`read_frame` 方法会等待收到完整一帧后才返回。单次调用 `TcpStream::read()` 可能返回任意数量的数据。可能包含完整一帧、部分帧或多帧。如果只收到部分帧，数据会被缓冲，并从套接字继续读取更多数据。如果收到多帧，则返回第一帧，其余数据缓冲到下次调用 `read_frame`。

如果还没有创建，请新建一个名为 `connection.rs` 的文件。

```bash
touch src/connection.rs
```

要实现这一点，`Connection` 需要一个读缓冲区字段。数据从套接字读入读缓冲区。解析出一帧后，相应数据会从缓冲区移除。

我们将使用 [`BytesMut`][BytesMutStruct] 作为缓冲区类型。这是 [`Bytes`][BytesStruct] 的可变版本。

```rust
use bytes::BytesMut;
use tokio::net::TcpStream;

pub struct Connection {
    stream: TcpStream,
    buffer: BytesMut,
}

impl Connection {
    pub fn new(stream: TcpStream) -> Connection {
        Connection {
            stream,
            // 分配 4kb 容量的缓冲区
            buffer: BytesMut::with_capacity(4096),
        }
    }
}
```

接下来，我们实现 `read_frame()` 方法。

```rust
use tokio::io::AsyncReadExt;
use bytes::Buf;
use mini_redis::Result;

# struct Connection {
#   stream: tokio::net::TcpStream,
#   buffer: bytes::BytesMut,
# }
# struct Frame {}
# impl Connection {
pub async fn read_frame(&mut self)
    -> Result<Option<Frame>>
{
    loop {
        // 尝试从已缓冲数据中解析一帧。如果
        // 已缓冲足够数据，则返回该帧。
        if let Some(frame) = self.parse_frame()? {
            return Ok(Some(frame));
        }

        // 已缓冲数据不足以读取一帧。
        // 尝试从套接字读取更多数据。
        //
        // 成功时返回读取的字节数。`0`
        // 表示「流结束」。
        if 0 == self.stream.read_buf(&mut self.buffer).await? {
            // 远端关闭了连接。若要干净关闭，
            // 读缓冲区中不应再有数据。若仍有数据，
            // 表示对端在发送帧的过程中关闭了套接字。
            if self.buffer.is_empty() {
                return Ok(None);
            } else {
                return Err("connection reset by peer".into());
            }
        }
    }
}
# fn parse_frame(&self) -> Result<Option<Frame>> { unimplemented!() }
# }
```

让我们逐步分析。`read_frame` 方法在循环中运行。首先调用 `self.parse_frame()`，尝试从 `self.buffer` 解析 redis 帧。如果有足够数据解析出一帧，就将该帧返回给 `read_frame()` 的调用者。否则，我们尝试从套接字向缓冲区读取更多数据。读取更多数据后，再次调用 `parse_frame()`。此时如果已收到足够数据，解析可能成功。

从流读取时，返回值为 `0` 表示不会再从对端收到数据。如果读缓冲区中仍有数据，说明收到了部分帧且连接被突然终止。这是错误情况，返回 `Err`。

[BytesMutStruct]: https://docs.rs/bytes/1/bytes/struct.BytesMut.html
[BytesStruct]: https://docs.rs/bytes/1/bytes/struct.Bytes.html

## `Buf` trait

从流读取时，调用的是 `read_buf`。这个版本的读取函数接受一个实现 [`BufMut`] 的值，来自 [`bytes`] crate。

首先，考虑如何用 `read()` 实现同样的读循环。可以用 `Vec<u8>` 代替 `BytesMut`。

```rust
use tokio::net::TcpStream;

pub struct Connection {
    stream: TcpStream,
    buffer: Vec<u8>,
    cursor: usize,
}

impl Connection {
    pub fn new(stream: TcpStream) -> Connection {
        Connection {
            stream,
            // 分配 4kb 容量的缓冲区
            buffer: vec![0; 4096],
            cursor: 0,
        }
    }
}
```

`Connection` 上的 `read_frame()` 函数：

```rust
use mini_redis::{Frame, Result};

# use tokio::io::AsyncReadExt;
# pub struct Connection {
#     stream: tokio::net::TcpStream,
#     buffer: Vec<u8>,
#     cursor: usize,
# }
# impl Connection {
pub async fn read_frame(&mut self)
    -> Result<Option<Frame>>
{
    loop {
        if let Some(frame) = self.parse_frame()? {
            return Ok(Some(frame));
        }

        // 确保缓冲区有容量
        if self.buffer.len() == self.cursor {
            // 扩大缓冲区
            self.buffer.resize(self.cursor * 2, 0);
        }

        // 读入缓冲区，并跟踪读取的
        // 字节数
        let n = self.stream.read(
            &mut self.buffer[self.cursor..]).await?;

        if 0 == n {
            if self.cursor == 0 {
                return Ok(None);
            } else {
                return Err("connection reset by peer".into());
            }
        } else {
            // 更新游标
            self.cursor += n;
        }
    }
}
# fn parse_frame(&mut self) -> Result<Option<Frame>> { unimplemented!() }
# }
```

使用字节数组和 `read` 时，还必须维护一个游标来跟踪已缓冲多少数据。必须将缓冲区的空部分传给 `read()`，否则会覆盖已缓冲数据。如果缓冲区满了，必须扩大缓冲区才能继续读取。在 `parse_frame()`（未包含）中，需要解析 `self.buffer[..self.cursor]` 中的数据。

因为「字节数组 + 游标」的组合非常常见，`bytes` crate 提供了表示字节数组和游标的抽象。`Buf` trait 由可从中读取数据的类型实现。`BufMut` trait 由可向其写入数据的类型实现。将 `T: BufMut` 传给 `read_buf()` 时，缓冲区的内部游标会被 `read_buf` 自动更新。因此，在我们版本的 `read_frame` 中，不需要自己管理游标。

此外，使用 `Vec<u8>` 时，缓冲区必须**初始化**。`vec![0; 4096]` 会分配 4096 字节的数组并向每个条目写入零。调整缓冲区大小时，新容量也必须用零初始化。初始化不是免费的。使用 `BytesMut` 和 `BufMut` 时，容量是**未初始化**的。`BytesMut` 抽象防止我们读取未初始化的内存，从而避免初始化步骤。

[`BufMut`]: https://docs.rs/bytes/1/bytes/buf/trait.BufMut.html
[`bytes`]: https://docs.rs/bytes/

# 解析

现在来看 `parse_frame()` 函数。解析分两步：

1. 确保已缓冲完整一帧，并找到该帧的结束索引。
2. 解析该帧。

`mini-redis` crate 为这两步都提供了函数：

1. [`Frame::check`](https://docs.rs/mini-redis/0.4/mini_redis/frame/enum.Frame.html#method.check)
2. [`Frame::parse`](https://docs.rs/mini-redis/0.4/mini_redis/frame/enum.Frame.html#method.parse)

我们还会复用 `Buf` 抽象。`Frame::check` 接受一个 `Buf`。当 `check` 遍历传入的缓冲区时，内部游标会前进。`check` 返回后，缓冲区的内部游标指向帧的末尾。

对于 `Buf` 类型，我们使用 [`std::io::Cursor<&[u8]>`][`Cursor`]。

```rust
use mini_redis::{Frame, Result};
use mini_redis::frame::Error::Incomplete;
use bytes::Buf;
use std::io::Cursor;

# pub struct Connection {
#     stream: tokio::net::TcpStream,
#     buffer: bytes::BytesMut,
# }
# impl Connection {
fn parse_frame(&mut self)
    -> Result<Option<Frame>>
{
    // 创建 `T: Buf` 类型
    let mut buf = Cursor::new(&self.buffer[..]);

    // 检查是否有完整帧可用
    match Frame::check(&mut buf) {
        Ok(_) => {
            // 获取帧的字节长度
            let len = buf.position() as usize;

            // 为调用 `parse` 重置
            // 内部游标
            buf.set_position(0);

            // 解析帧
            let frame = Frame::parse(&mut buf)?;

            // 从缓冲区丢弃该帧
            self.buffer.advance(len);

            // 将帧返回给调用者
            Ok(Some(frame))
        }
        // 已缓冲数据不足
        Err(Incomplete) => Ok(None),
        // 遇到错误
        Err(e) => Err(e.into()),
    }
}
# }
```

完整的 [`Frame::check`][check] 函数见[这里][check]。我们不会完整讲解它。

值得注意的是，这里使用了 `Buf` 的「字节迭代器」风格 API。这些 API 会取数据并推进内部游标。例如，解析一帧时，会检查第一个字节以确定帧类型。使用的函数是 [`Buf::get_u8`]。它会取当前游标位置的字节，并将游标前进一位。

[`Buf`] trait 上还有更多有用方法。详见 [API 文档][`Buf`]。

[check]: https://github.com/tokio-rs/mini-redis/blob/tutorial/src/frame.rs#L65-L103
[`Buf::get_u8`]: https://docs.rs/bytes/1/bytes/buf/trait.Buf.html#method.get_u8
[`Buf`]: https://docs.rs/bytes/1/bytes/buf/trait.Buf.html
[`Cursor`]: https://doc.rust-lang.org/stable/std/io/struct.Cursor.html

# 缓冲写入

分帧 API 的另一半是 `write_frame(frame)` 函数。该函数将整帧写入套接字。为尽量减少 `write` 系统调用，写入会被缓冲。维护一个写缓冲区，帧先编码到该缓冲区再写入套接字。但与 `read_frame()` 不同，并非总是先把整帧缓冲到字节数组再写入套接字。

考虑一个 bulk 流帧。要写入的值是 `Frame::Bulk(Bytes)`。bulk 帧的线路格式由帧头组成，即 `$` 字符后跟数据长度（字节）。帧的大部分是 `Bytes` 值的内容。如果数据很大，复制到中间缓冲区代价很高。

要实现缓冲写入，我们使用 [`BufWriter` 结构体][buf-writer]。该结构体用 `T: AsyncWrite` 初始化，并自身实现 `AsyncWrite`。对 `BufWriter` 调用 `write` 时，写入不会直接进入内部 writer，而是进入缓冲区。缓冲区满时，内容会刷新到内部 writer，内部缓冲区被清空。某些情况下还有绕过缓冲区的优化。

本教程不会完整实现 `write_frame()`。完整实现见[这里][write-frame]。

首先更新 `Connection` 结构体：

```rust
use tokio::io::BufWriter;
use tokio::net::TcpStream;
use bytes::BytesMut;

pub struct Connection {
    stream: BufWriter<TcpStream>,
    buffer: BytesMut,
}

impl Connection {
    pub fn new(stream: TcpStream) -> Connection {
        Connection {
            stream: BufWriter::new(stream),
            buffer: BytesMut::with_capacity(4096),
        }
    }
}
```

接下来实现 `write_frame()`。

```rust
use tokio::io::{self, AsyncWriteExt};
use mini_redis::Frame;

# struct Connection {
#   stream: tokio::io::BufWriter<tokio::net::TcpStream>,
#   buffer: bytes::BytesMut,
# }
# impl Connection {
async fn write_frame(&mut self, frame: &Frame)
    -> io::Result<()>
{
    match frame {
        Frame::Simple(val) => {
            self.stream.write_u8(b'+').await?;
            self.stream.write_all(val.as_bytes()).await?;
            self.stream.write_all(b"\r\n").await?;
        }
        Frame::Error(val) => {
            self.stream.write_u8(b'-').await?;
            self.stream.write_all(val.as_bytes()).await?;
            self.stream.write_all(b"\r\n").await?;
        }
        Frame::Integer(val) => {
            self.stream.write_u8(b':').await?;
            self.write_decimal(*val).await?;
        }
        Frame::Null => {
            self.stream.write_all(b"$-1\r\n").await?;
        }
        Frame::Bulk(val) => {
            let len = val.len();

            self.stream.write_u8(b'$').await?;
            self.write_decimal(len as u64).await?;
            self.stream.write_all(val).await?;
            self.stream.write_all(b"\r\n").await?;
        }
        Frame::Array(_val) => unimplemented!(),
    }

    self.stream.flush().await;

    Ok(())
}
# async fn write_decimal(&mut self, val: u64) -> io::Result<()> { unimplemented!() }
# }
```

这里使用的函数由 [`AsyncWriteExt`] 提供。`TcpStream` 上也有，但没有中间缓冲区就不宜进行单字节写入。

* [`write_u8`] 向 writer 写入单个字节。
* [`write_all`] 将整个切片写入 writer。
* [`write_decimal`] 由 mini-redis 实现。

函数末尾调用 `self.stream.flush().await`。因为 `BufWriter` 将写入存放在中间缓冲区，`write` 调用不保证数据已写入套接字。返回前，我们希望帧已写入套接字。`flush()` 会将缓冲区中待写的数据写入套接字。

另一种做法是在 `write_frame()` 中**不**调用 `flush()`，而是在 `Connection` 上提供 `flush()` 函数。这样调用者可以在写缓冲区中排队多个小帧，然后用一次 `write` 系统调用全部写入套接字。但这会使 `Connection` API 更复杂。简洁是 Mini-Redis 的目标之一，因此我们决定在 `fn write_frame()` 中包含 `flush().await` 调用。

[buf-writer]: https://docs.rs/tokio/1/tokio/io/struct.BufWriter.html
[write-frame]: https://github.com/tokio-rs/mini-redis/blob/tutorial/src/connection.rs#L159-L184
[`AsyncWriteExt`]: https://docs.rs/tokio/1/tokio/io/trait.AsyncWriteExt.html
[`write_u8`]: https://docs.rs/tokio/1/tokio/io/trait.AsyncWriteExt.html#method.write_u8
[`write_all`]: https://docs.rs/tokio/1/tokio/io/trait.AsyncWriteExt.html#method.write_all
[`write_decimal`]: https://github.com/tokio-rs/mini-redis/blob/tutorial/src/connection.rs#L225-L238
