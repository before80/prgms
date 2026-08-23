+++
title = "26.3-测试服务器"
date = 2026-08-22T19:00:00+08:00
weight = 46
type = "docs"
description = "测试服务器"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 测试服务器 {#testing-the-server}


> 原文链接: [https://rust-lang.github.io/async-book/09_example/03_tests.html](https://rust-lang.github.io/async-book/09_example/03_tests.html)


让我们继续测试 `handle_connection` 函数。

首先，我们需要一个可用的 `TcpStream`。在端到端或集成测试中，我们可能希望建立真实的 TCP 连接来测试代码。一种策略是在 `localhost` 端口 0 上启动监听器。端口 0 不是有效的 UNIX 端口，但用于测试可以。操作系统会为我们选择一个开放的 TCP 端口。

在本示例中，我们将为连接处理程序编写单元测试，检查对相应输入是否返回正确响应。为保持单元测试隔离且确定，我们将用 mock 替换 `TcpStream`。

首先，我们将修改 `handle_connection` 的签名以便于测试。`handle_connection` 实际上不需要 `async_std::net::TcpStream`；它需要任何实现 `async_std::io::Read`、`async_std::io::Write` 和 `marker::Unpin` 的结构。将类型签名改为反映这一点，使我们能在测试时传入 mock。

```rust,ignore
use async_std::io::{Read, Write};

async fn handle_connection(mut stream: impl Read + Write + Unpin) {
```

接下来，让我们构建实现这些 trait 的 mock `TcpStream`。首先实现 `Read` trait，有一个方法 `poll_read`。我们的 mock `TcpStream` 将包含一些被复制到读取缓冲区的数据，我们将返回 `Poll::Ready` 表示读取完成。

```rust,ignore
    use super::*;
    use futures::io::Error;
    use futures::task::{Context, Poll};

    use std::cmp::min;
    use std::pin::Pin;

    struct MockTcpStream {
        read_data: Vec<u8>,
        write_data: Vec<u8>,
    }

    impl Read for MockTcpStream {
        fn poll_read(
            self: Pin<&mut Self>,
            _: &mut Context,
            buf: &mut [u8],
        ) -> Poll<Result<usize, Error>> {
            let size: usize = min(self.read_data.len(), buf.len());
            buf[..size].copy_from_slice(&self.read_data[..size]);
            Poll::Ready(Ok(size))
        }
    }
```

我们的 `Write` 实现非常类似，但需要编写三个方法：`poll_write`、`poll_flush` 和 `poll_close`。`poll_write` 会将任何输入数据复制到 mock `TcpStream`，完成时返回 `Poll::Ready`。mock `TcpStream` 无需执行刷新或关闭操作，因此 `poll_flush` 和 `poll_close` 只需返回 `Poll::Ready`。

```rust,ignore
    impl Write for MockTcpStream {
        fn poll_write(
            mut self: Pin<&mut Self>,
            _: &mut Context,
            buf: &[u8],
        ) -> Poll<Result<usize, Error>> {
            self.write_data = Vec::from(buf);

            Poll::Ready(Ok(buf.len()))
        }

        fn poll_flush(self: Pin<&mut Self>, _: &mut Context) -> Poll<Result<(), Error>> {
            Poll::Ready(Ok(()))
        }

        fn poll_close(self: Pin<&mut Self>, _: &mut Context) -> Poll<Result<(), Error>> {
            Poll::Ready(Ok(()))
        }
    }
```

最后，我们的 mock 需要实现 `Unpin`，表示其在内存中的位置可以安全移动。有关 pinning 和 `Unpin` trait 的更多信息，请参阅 pinning 一节。

```rust,ignore
    impl Unpin for MockTcpStream {}
```

现在我们可以测试 `handle_connection` 函数了。在设置包含一些初始数据的 `MockTcpStream` 之后，我们可以使用属性 `#[async_std::test]` 运行 `handle_connection`，类似于我们使用 `#[async_std::main]` 的方式。为确保 `handle_connection` 按预期工作，我们将根据其初始内容检查是否正确数据被写入 `MockTcpStream`。

```rust,ignore
    use std::fs;

    #[async_std::test]
    async fn test_handle_connection() {
        let input_bytes = b"GET / HTTP/1.1\r\n";
        let mut contents = vec![0u8; 1024];
        contents[..input_bytes.len()].clone_from_slice(input_bytes);
        let mut stream = MockTcpStream {
            read_data: contents,
            write_data: Vec::new(),
        };

        handle_connection(&mut stream).await;

        let expected_contents = fs::read_to_string("hello.html").unwrap();
        let expected_response = format!("HTTP/1.1 200 OK\r\n\r\n{}", expected_contents);
        assert!(stream.write_data.starts_with(expected_response.as_bytes()));
    }
```
