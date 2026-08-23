+++
title = "26-最终项目：HTTP 服务器"
date = 2026-08-22T19:00:00+08:00
weight = 47
type = "docs"
description = "最终项目：HTTP 服务器"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 最终项目：HTTP 服务器 {#final-project-http-server}


> 原文链接: [https://rust-lang.github.io/async-book/09_example/00_intro.html](https://rust-lang.github.io/async-book/09_example/00_intro.html)


本章我们将使用异步 Rust 修改 Rust 书中的[单线程 Web 服务器](https://doc.rust-lang.org/book/ch20-01-single-threaded.html)，以并发地服务请求。

## 回顾

以下是课程结束时代码的样子。

`src/main.rs`：

```rust
use std::fs;
use std::io::prelude::*;
use std::net::TcpListener;
use std::net::TcpStream;

fn main() {
    // 在 localhost 7878 端口监听传入的 TCP 连接
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    // 永久阻塞，处理到达此 IP 地址的每个请求
    for stream in listener.incoming() {
        let stream = stream.unwrap();

        handle_connection(stream);
    }
}

fn handle_connection(mut stream: TcpStream) {
    // 从流中读取前 1024 字节数据
    let mut buffer = [0; 1024];
    stream.read(&mut buffer).unwrap();

    let get = b"GET / HTTP/1.1\r\n";

    // 根据请求数据回复问候或 404，
    // 取决于请求中的数据
    let (status_line, filename) = if buffer.starts_with(get) {
        ("HTTP/1.1 200 OK\r\n\r\n", "hello.html")
    } else {
        ("HTTP/1.1 404 NOT FOUND\r\n\r\n", "404.html")
    };
    let contents = fs::read_to_string(filename).unwrap();

    // 将响应写回流，
    // 并刷新流以确保响应发回客户端
    let response = format!("{status_line}{contents}");
    stream.write_all(response.as_bytes()).unwrap();
    stream.flush().unwrap();
}
```

`hello.html`：

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Hello!</title>
  </head>
  <body>
    <h1>Hello!</h1>
    <p>Hi from Rust</p>
  </body>
</html>
```

`404.html`：

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Hello!</title>
  </head>
  <body>
    <h1>Oops!</h1>
    <p>Sorry, I don't know what you're asking for.</p>
  </body>
</html>
```

若用 `cargo run` 运行服务器并在浏览器中访问 `127.0.0.1:7878`，你会收到 Ferris 的友好问候！
