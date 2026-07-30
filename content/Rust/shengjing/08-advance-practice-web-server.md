+++
title = "08-进阶实战1：实现一个web服务器"
date = 2026-07-28T14:49:00+08:00
weight = 80
type = "docs"
description = "《Rust语言圣经》多线程Web服务器实战精要速成"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [Rust语言圣经](https://beatai.org/rust-course/)「进阶实战1: 实现一个 web 服务器」

# 实践应用：多线程Web服务器

**口诀**：TCP 监听 → 读 HTTP → 写响应 → 线程池并发 → Drop 优雅关。

> 多线程非最佳方案；高并发 IO 用 async/tokio（见第 09 章）。

## 构建单线程 Web 服务器

### 监听 TCP 连接

```rust
use std::net::TcpListener;

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    for stream in listener.incoming() {
        let stream = stream.unwrap();
        handle_connection(stream);
    }
}
```

- `7878` 避开 80/8080；`bind` 返回 `Result`；`incoming()` 阻塞迭代连接尝试
- 浏览器可能多次 `Connection established!`（重试 + drop 关连接）

### 读取请求

```rust
use std::io::{prelude::*, BufReader};
use std::net::{TcpListener, TcpStream};

fn handle_connection(mut stream: TcpStream) {
    let http_request: Vec<_> = BufReader::new(&mut stream)
        .lines()
        .map(|r| r.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();
}
```

- 需 `BufRead` 才能用 `lines()`；空行 `\r\n\r\n` 标志请求头结束

### HTTP 请求长啥样

```text
Method Request-URI HTTP-Version\r\n
Header: value\r\n
\r\n
message-body
```

### 请求应答

```rust
let response = "HTTP/1.1 200 OK\r\n\r\n";
stream.write_all(response.as_bytes()).unwrap();
```

```text
HTTP/1.1 200 OK\r\n\r\n
```

### 返回 HTML 页面

```rust
let contents = fs::read_to_string("hello.html").unwrap();
let response = format!(
    "{}\r\nContent-Length: {}\r\n\r\n{}",
    status_line, contents.len(), contents
);
stream.write_all(response.as_bytes()).unwrap();
stream.flush().unwrap();
```

### 验证请求和选择性应答

```rust
let request_line = &http_request[0];
let (status_line, filename) = match &request_line[..] {
    "GET / HTTP/1.1" => ("HTTP/1.1 200 OK", "hello.html"),
    _ => ("HTTP/1.1 404 NOT FOUND", "404.html"),
};
```

## 构建多线程 Web 服务器

### 基于单线程模拟慢请求

```rust
"GET /sleep HTTP/1.1" => {
    thread::sleep(Duration::from_secs(5));
    ("HTTP/1.1 200 OK", "hello.html")
}
```

- 单线程：慢请求阻塞后续连接 → 需并发

### 使用线程池改善吞吐

**口诀**：固定 N 线程 + 任务队列，防 DoS（无限 spawn）。

#### 为每个请求生成一个线程

```rust
thread::spawn(|| handle_connection(stream));
```

- 可行但线程无上限 → 资源耗尽

#### 限制创建线程的数量

```rust
let pool = ThreadPool::new(4);
pool.execute(|| handle_connection(stream));
```

#### 使用编译器驱动的方式开发 ThreadPool

`execute` 签名参考 `thread::spawn`：

```rust
pub fn execute<F>(&self, f: F)
where
    F: FnOnce() + Send + 'static,
{ /* ... */ }
```

#### `new` 还是 `build`

- `new`：简单初始化；`build`：复杂构建（如 `Config::build`）
- 线程池用 `new`；`assert!(size > 0)`

#### 存储线程

```rust
pub struct ThreadPool {
    workers: Vec<Worker>,
}
struct Worker {
    id: usize,
    thread: thread::JoinHandle<()>,
}
```

#### 将代码从 ThreadPool 发送到线程中

Worker 从 channel 取任务，类似服务员→厨房。

#### 将请求发送给线程

```rust
type Job = Box<dyn FnOnce() + Send + 'static>;
let (sender, receiver) = mpsc::channel();
let receiver = Arc::new(Mutex::new(receiver));
```

Worker 循环：

```rust
loop {
    let job = receiver.lock().unwrap().recv().unwrap();
    job();
}
```

#### 实现 execute 方法

```rust
pub fn execute<F>(&self, f: F)
where
    F: FnOnce() + Send + 'static,
{
    self.sender.as_ref().unwrap().send(Box::new(f)).unwrap();
}
```

### while let 的巨大陷阱

```rust
// 错：recv 报错时 panic
while let Ok(job) = receiver.lock().unwrap().recv() { job(); }

// 对：Err 时 break
loop {
    let job = match receiver.lock().unwrap().recv() {
        Ok(job) => job,
        Err(_) => break,
    };
    job();
}
```

## 优雅关闭和资源清理

### 为线程池实现 Drop

```rust
struct Worker {
    id: usize,
    thread: Option<JoinHandle<()>>,
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        drop(self.sender.take()); // 释放 sender
        for w in &mut self.workers {
            if let Some(t) = w.thread.take() { t.join().unwrap(); }
        }
    }
}
```

### 停止工作线程

- `drop(sender)` → `recv()` 返回 `Err` → worker 退出 loop
- `main` 用 `listener.incoming().take(2)` 限制连接数，触发 pool drop

### 完整代码

**main.rs 骨架**：

```rust
use hello::ThreadPool;
use std::{fs, io::prelude::*, net::TcpListener, net::TcpStream, thread, time::Duration};

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    let pool = ThreadPool::new(4);
    for stream in listener.incoming().take(2) {
        pool.execute(|| handle_connection(stream.unwrap()));
    }
    println!("Shutting down.");
}

fn handle_connection(mut stream: TcpStream) { /* 读 buffer → match 路径 → 写响应 */ }
```

**lib.rs 骨架**：

```rust
use std::{sync::{mpsc, Arc, Mutex}, thread};

pub struct ThreadPool {
    workers: Vec<Worker>,
    sender: Option<mpsc::Sender<Job>>,
}
type Job = Box<dyn FnOnce() + Send + 'static>;
// new: channel + Arc<Mutex<receiver>> + N 个 Worker
// execute: send(Box::new(f))
// Drop: take sender + join workers
```

### 可以做的更多

- 增加请求解析、日志、HTTPS、async 重写

### 上一章节的遗留问题

- `while let Ok` 陷阱；`Option<JoinHandle>` + `take()` 解决 drop 所有权
