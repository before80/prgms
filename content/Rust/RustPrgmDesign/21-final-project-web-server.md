+++
title = "21-最后的项目：构建多线程web server"
date = 2026-07-28T14:49:00+08:00
weight = 210
type = "docs"
description = "手写 TCP/HTTP 单线程 server、线程池并发与优雅停机实现精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第21章

# 最后的项目：构建多线程 web server

综合复习项目：手写基础 HTTP server + 线程池。非生产最佳实践（可用 crates.io 现成库），目的是理解底层机制；本章不用 async/await。

## 构建单线程 web server

### 监听 TCP 连接

```rust
let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
for stream in listener.incoming() {
    let stream = stream.unwrap();
    handle_connection(stream);
}
```

- **`std::net::TcpListener`**：`bind` 绑定端口（7878 ≈ "rust"）；`incoming()` 迭代连接尝试。
- 浏览器可能多连接（favicon、预连接等）；无响应时连接 drop 关闭，浏览器或重连。

### 读取请求

```rust
fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let http_request: Vec<_> = buf_reader
        .lines()
        .map(|l| l.unwrap())
        .take_while(|l| !l.is_empty())
        .collect();
}
```

- **`BufReader`** + `lines()` 按行读；连续两个 `\r\n`（空行）标志请求头结束。
- 请求行格式：`Method Request-URI HTTP-Version CRLF`

### 更仔细地观察 HTTP 请求

```text
GET / HTTP/1.1
Host: 127.0.0.1:7878
...
（空行）
```

- 第一行：方法（GET/POST）、URI（如 `/`）、HTTP 版本。
- 后续为 header；GET 通常无 body。

### 编写响应

```text
HTTP/1.1 200 OK\r\n\r\n
```

- 状态行 + headers + 空行 + body。
- `stream.write_all(response.as_bytes())`

### 返回真正的 HTML

- 读 `hello.html`；响应加 `Content-Length` header。
- `format!` 拼状态行、header、body。

### 验证请求并有选择的进行响应

- 只匹配 `GET / HTTP/1.1` → 200 + `hello.html`。
- 其他 → 404 + `404.html`。
- **重构**：`let (status_line, filename) = if ... else ...;` + `let` 解构，消除重复读写逻辑。

## 将单线程 server 变为多线程 server

### 模拟慢请求

- `/sleep` 分支 `thread::sleep(Duration::from_secs(5))`。
- 单线程下慢请求阻塞后续请求 → 需并发。

### 使用线程池改善吞吐量

**线程池**：固定数量 worker 线程 + 任务队列；限制并发防 DoS。

#### 为每一个请求分配线程

`thread::spawn(|| handle_connection(stream))` — 简单但可无限创建线程。

#### 创建有限数量的线程

目标 API：

```rust
let pool = ThreadPool::new(4);
pool.execute(|| { handle_connection(stream); });
```

#### 采用编译器驱动开发构建 `ThreadPool`

1. 定义 `ThreadPool` 结构体（`src/lib.rs` 库 crate）。
2. `new(size: usize) -> Self`；`size == 0` 时 `assert!` panic。
3. `execute<F>(&self, f: F) where F: FnOnce() + Send + 'static`（对齐 `thread::spawn` 约束）。

#### 在 `new` 中验证线程池的线程数量

- `assert!(size > 0, "Number of threads must be greater than 0");`

#### 分配空间以存储线程

- 存 `Vec<Worker>` 而非裸 `JoinHandle`；`with_capacity(size)` 预分配。

#### 将代码从 `ThreadPool` 发送给线程

- **`Worker`** 结构体：`id` + `JoinHandle<()>`；启动时空闭包占位。

#### 使用信道向线程发送请求

1. `ThreadPool` 持有 `mpsc::Sender<Job>`。
2. 每个 `Worker` 共享 `Arc<Mutex<Receiver<Job>>>`（多生产者单消费者 → 共享接收端）。
3. `type Job = Box<dyn FnOnce() + Send + 'static>;`
4. `execute`：`sender.send(Box::new(f))`。
5. Worker 循环：`while let Ok(job) = receiver.lock().unwrap().recv() { job(); }`

> **`while let` 陷阱**：`while let Ok(job) = receiver.lock().unwrap().recv()` 会在整个循环体持有锁；应 `let job = receiver.lock().unwrap().recv().unwrap();` 让锁在 `let` 结束时释放。

## 优雅停机与清理

### 为 `ThreadPool` 实现 `Drop` Trait

- `drop` 中对每个 worker 调用 `thread.join()`。
- 用 `self.workers.drain(..)` 取出所有 `Worker` 再 join（避免借用冲突）。

### 向线程发出信号，让它们停止接收任务

1. `sender` 改为 `Option<Sender<Job>>`；`drop` 时 `drop(sender)` 关闭信道。
2. Worker 中 `recv` 返回 `Err` 时 `break` 退出循环。
3. 演示：`for stream in listener.incoming().take(2)` 处理两请求后退出，`ThreadPool` drop 触发清理。

## 总结

完整路径：**TcpListener → 解析 HTTP → 响应 → ThreadPool（Worker + mpsc + Arc/Mutex）→ Drop 优雅停机**。生产环境请用成熟 web 框架与线程池 crate。
