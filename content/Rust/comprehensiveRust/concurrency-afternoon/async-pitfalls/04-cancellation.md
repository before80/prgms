+++
title = "4.4 取消"
date = 2026-08-11T11:30:00+08:00
weight = 382
type = "docs"
description = "04-取消 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/async-pitfalls/cancellation.html](https://google.github.io/comprehensive-rust/concurrency/async-pitfalls/cancellation.html)

# 4.4 取消

丢弃 future 意味着它再也不能被轮询。这称为*取消*（cancellation），可以发生在任意 `await` 点。需要小心确保即使 future 被取消，系统仍能正确工作。例如，不应死锁或丢失数据。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::io;
use std::time::Duration;
use tokio::io::{AsyncReadExt, AsyncWriteExt, DuplexStream};

struct LinesReader {
    stream: DuplexStream,
}

impl LinesReader {
    fn new(stream: DuplexStream) -> Self {
        Self { stream }
    }

    async fn next(&mut self) -> io::Result<Option<String>> {
        let mut bytes = Vec::new();
        let mut buf = [0];
        while self.stream.read(&mut buf[..]).await? != 0 {
            bytes.push(buf[0]);
            if buf[0] == b'\n' {
                break;
            }
        }
        if bytes.is_empty() {
            return Ok(None);
        }
        let s = String::from_utf8(bytes)
            .map_err(|_| io::Error::new(io::ErrorKind::InvalidData, "not UTF-8"))?;
        Ok(Some(s))
    }
}

async fn slow_copy(source: String, mut dest: DuplexStream) -> io::Result<()> {
    for b in source.bytes() {
        dest.write_u8(b).await?;
        tokio::time::sleep(Duration::from_millis(10)).await
    }
    Ok(())
}

#[tokio::main]
async fn main() -> io::Result<()> {
    let (client, server) = tokio::io::duplex(5);
    let handle = tokio::spawn(slow_copy("hi\nthere\n".to_owned(), client));

    let mut lines = LinesReader::new(server);
    let mut interval = tokio::time::interval(Duration::from_millis(60));
    loop {
        tokio::select! {
            _ = interval.tick() => println!("tick!"),
            line = lines.next() => if let Some(l) = line? {
                print!("{}", l)
            } else {
                break
            },
        }
    }
    handle.await.unwrap()?;
    Ok(())
}
```

> - 编译器不会帮你保证取消安全。你需要阅读 API 文档，并考虑你的 `async fn` 持有什么状态。
>
> - 与 `panic` 和 `?` 不同，取消是正常控制流的一部分（相对于错误处理）。
>
> - 本示例会丢失字符串的部分内容。
>
>   - 每当 `tick()` 分支先完成时，`next()` 及其 `buf` 就会被丢弃。
>
>   - 可通过把 `buf` 作为结构体的一部分，使 `LinesReader` 取消安全：
>     ```rust
>     // Copyright 2024 Google LLC
>     // SPDX-License-Identifier: Apache-2.0
>     #
>     struct LinesReader {
>         stream: DuplexStream,
>         bytes: Vec<u8>,
>         buf: [u8; 1],
>     }
>
>     impl LinesReader {
>         fn new(stream: DuplexStream) -> Self {
>             Self { stream, bytes: Vec::new(), buf: [0] }
>         }
>         async fn next(&mut self) -> io::Result<Option<String>> {
>             // 给 buf 和 bytes 加上 self. 前缀。
>             // ...
>             let raw = std::mem::take(&mut self.bytes);
>             let s = String::from_utf8(raw)
>                 .map_err(|_| io::Error::new(io::ErrorKind::InvalidData, "not UTF-8"))?;
>             // ...
>         }
>     }
>     ```
>
> - [`Interval::tick`](https://docs.rs/tokio/latest/tokio/time/struct.Interval.html#method.tick)
>   是取消安全的，因为它会跟踪某个 tick 是否已被「交付」。
>
> - [`AsyncReadExt::read`](https://docs.rs/tokio/latest/tokio/io/trait.AsyncReadExt.html#method.read)
>   是取消安全的，因为它要么返回，要么不读取数据。
>
> - [`AsyncBufReadExt::read_line`](https://docs.rs/tokio/latest/tokio/io/trait.AsyncBufReadExt.html#method.read_line)
>   与本示例类似，*不是*取消安全的。详见其文档及替代方案。

