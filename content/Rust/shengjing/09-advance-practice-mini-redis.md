+++
title = "09-进阶实战2：实现一个简单Redis"
date = 2026-07-28T14:49:00+08:00
weight = 90
type = "docs"
description = "《Rust语言圣经》tokio与mini-redis实战精要速成"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [Rust语言圣经](https://beatai.org/rust-course/)「进阶实战2: 实现一个简单 Redis」

# 进阶实战: 实现一个简单 redis

**骨架**：`#[tokio::main]` → `TcpListener` → `spawn` 处理连接 → `Connection` 读写帧 → 共享 `Db` → channel 客户端。

## tokio 概览

### 异步运行时

- **reactor**：订阅 IO/定时器等事件
- **executor**：调度执行 `Future`
- 主流：`tokio`（生态全）、`async-std`（贴近 std）、`smol`（轻量）

### tokio 简介

- 多线程 async 运行时；提供 `async` 版阻塞 API（如 `tokio::time::sleep`）
- API 名与 std 对齐，同步 `fn` → 异步 `async fn` + `.await`

#### 优势

高性能、行为一致、灵活（单/多线程 runtime）

#### 劣势

学习曲线；需选 runtime；协作式调度下 CPU 密集任务会饿死其它任务 → 用 `spawn_blocking`

## tokio 初印象

### 专题目标

边学边练，最终实现 mini-redis 客户端 + 服务端（非完整 redis）。

### 环境配置

```shell
cargo install mini-redis
mini-redis-server   # 6379
mini-redis-cli set foo 1
```

### Hello Tokio

```toml
[dependencies]
tokio = { version = "1", features = ["full"] }
mini-redis = "0.4"
```

```rust
use mini_redis::{client, Result};

#[tokio::main]
async fn main() -> Result<()> {
    let mut client = client::connect("127.0.0.1:6379").await?;
    client.set("hello", "world".into()).await?;
    let result = client.get("hello").await?;
    println!("{:?}", result); // Some("world")
    Ok(())
}
```

### 原理解释

- `#[tokio::main]` 展开为创建 runtime + `block_on`
- `.await` 挂起当前任务，不阻塞 OS 线程
- `?` 在 async 中传播 `Result`

### cargo feature

```toml
tokio = { version = "1", features = ["full"] }
# 或按需：rt-multi-thread, net, io-util, sync, time, macros
```

## 创建异步任务

客户端示例移入 `examples/hello-redis.rs`；`src/main.rs` 写服务端。

### 接收 sockets

```rust
use tokio::net::{TcpListener, TcpStream};
use mini_redis::{Connection, Frame};

#[tokio::main]
async fn main() {
    let listener = TcpListener::bind("127.0.0.1:6379").await.unwrap();
    loop {
        let (socket, _) = listener.accept().await.unwrap();
        process(socket).await; // 串行：一次一条连接
    }
}

async fn process(socket: TcpStream) {
    let mut conn = Connection::new(socket);
    if let Some(frame) = conn.read_frame().await.unwrap() {
        let response = Frame::Error("unimplemented".to_string());
        conn.write_frame(&response).await.unwrap();
    }
}
```

### 生成任务

```rust
loop {
    let (socket, _) = listener.accept().await.unwrap();
    tokio::spawn(async move { process(socket).await; });
}
```

- `loop` 内 `.await` 会阻塞当前任务；spawn 后 listener 可继续 accept

### 使用 HashMap 存储数据

```rust
use std::collections::HashMap;
use bytes::Bytes;

#[derive(Clone)]
struct Db {
    inner: Arc<Mutex<HashMap<String, Bytes>>>,
}
// SET/GET 命令解析 Frame::Array → 读写 HashMap
```

## 共享状态

### 解决方法

多连接共享 `Db`：`Arc<Mutex<HashMap<...>>>` 或 `tokio::sync::Mutex`

### 添加 `bytes` 依赖包

```toml
bytes = "1"
```

### 初始化 HashMap

```rust
let db = Db { inner: Arc::new(Mutex::new(HashMap::new())) };
tokio::spawn(async move { process(socket, db.clone()).await; });
```

### 更新 `process()`

```rust
async fn process(socket: TcpStream, db: Db) {
    let mut conn = Connection::new(socket);
    while let Some(frame) = conn.read_frame().await.unwrap() {
        // 解析命令，操作 db，write_frame 响应
    }
}
```

### 任务、线程和锁竞争

- tokio 多 worker 线程；`Mutex` 竞争影响吞吐

### 在 `.await` 期间持有锁

```rust
// 错：持锁跨越 await，可能死锁
let mut db = db.inner.lock().await;
some_async().await;

// 对：缩小锁作用域
{
    let mut db = db.inner.lock().await;
    db.insert(k, v);
} // 锁释放后再 await
```

- **口诀**：`.await` 前必须 drop 锁；优先 `tokio::sync::Mutex`（async 场景）

## 消息传递

### 错误的实现

```rust
// 错：client 非 Copy，两任务不能同时 &mut client
let t1 = tokio::spawn(async { client.get("hello").await; });
let t2 = tokio::spawn(async { client.set("foo", "bar".into()).await; });
```

- `std::sync::Mutex` 不能跨 `.await`

### 消息传递

Producer 发 `Command` → 单 Consumer 任务独占 `client` → `oneshot` 回传结果。

### Tokio 的消息通道( channel )

| 类型 | 模式 |
|------|------|
| `mpsc` | 多生产者，单消费者 |
| `oneshot` | 单发单收，一次 |
| `broadcast` | 多生产者多消费者，广播 |
| `watch` | 单生产者多消费者，只保留最新值 |

async 用 `tokio::sync::*`；阻塞线程用 `std::sync::mpsc` / `crossbeam`

### 定义消息类型

```rust
enum Command {
    Get { key: String, resp: Responder<Option<Bytes>> },
    Set { key: String, val: Bytes, resp: Responder<()> },
}
type Responder<T> = oneshot::Sender<T>;
```

### 创建消息通道

```rust
let (tx, mut rx) = mpsc::channel(32);
let manager = tokio::spawn(async move {
    let mut client = client::connect("127.0.0.1:6379").await.unwrap();
    while let Some(cmd) = rx.recv().await {
        match cmd { /* 处理并 oneshot 回复 */ }
    }
});
```

### 生成管理任务

Client API：`tx.send(Command::Get { ... }).await` + `rx.await` 等响应

### 接收响应消息

```rust
let (resp_tx, resp_rx) = oneshot::channel();
tx.send(Command::Get { key, resp: resp_tx }).await.unwrap();
let val = resp_rx.await.unwrap();
```

### 对消息通道进行限制

`mpsc::channel(32)` 有界缓冲，背压控制

## I/O

### AsyncRead 和 AsyncWrite

```rust
use tokio::io::{AsyncReadExt, AsyncWriteExt};
stream.read(&mut buf).await?;
stream.write_all(&buf).await?;
```

### 实用函数

`copy`、`copy_bidirectional`、`read_exact`、`read_to_end`

### 回声服务( Echo )

```rust
loop {
    let n = socket.read(&mut buf).await?;
    if n == 0 { return; }
    socket.write_all(&buf[..n]).await?;
}
```

## 解析数据帧

```rust
enum Frame {
    Simple(String), Error(String), Integer(u64),
    Bulk(Bytes), Null, Array(Vec<Frame>),
}
```

Redis 协议：[RESP](https://redis.io/docs/reference/protocol-spec/)

### 缓冲读取(Buffered Reads)

```rust
pub struct Connection {
    stream: TcpStream,
    buffer: BytesMut, // with_capacity(4096)
}
```

- `read` 可能返回部分/多帧；缓冲 + `parse_frame` 循环

### 帧解析

```rust
fn parse_frame(&mut self) -> Result<Option<Frame>> {
    // 检查 buffer 是否够解析一帧；不够返回 Ok(None)
}
```

### 缓冲写入(Buffered writes)

`write_frame` 序列化帧 → `stream.write_all` / `flush`

## 深入 async

### Future

```rust
trait Future {
    type Output;
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

- 惰性：不 poll 不执行；`async fn` 编译为状态机

### 执行器( Excecutor )

`block_on` / tokio runtime 循环 poll ready 的任务

### Waker

`poll` 返回 `Pending` 时注册 waker；IO 就绪后 wake → 重新 poll

## select

### tokio::select!

```rust
tokio::select! {
    _ = signal.recv() => { /* 关闭 */ }
    res = socket.read(&mut buf) => { /* 处理 IO */ }
}
```

- 多分支竞速，**只执行第一个完成的**

### 语法

每个分支：`pattern = async_expr => { ... }`

### 返回值

select 块整体有返回值（最后执行分支的值）

### 错误传播

分支内可用 `?`（需在返回 `Result` 的 async 块中）

### 模式匹配

```rust
select! {
    Ok(n) = socket.read(&mut buf) => { ... }
    _ = sleep(Duration::from_secs(1)) => { ... }
}
```

### 借用

select 会多次执行分支表达式 → 需 `&mut` 或 move 进分支

### 循环

```rust
loop {
    tokio::select! {
        _ = shutdown.recv() => break,
        frame = conn.read_frame() => { /* ... */ }
    }
}
```

### spawn 和 select! 的一些不同

- `JoinHandle` 也是 Future；可与 IO 一起 select

## Stream

类似 `Iterator`，异步版：

```rust
trait Stream {
    type Item;
    fn poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>>;
}
```

- `StreamExt::next().await`；适配器 `map`/`filter`/`take`
- `while let Some(x) = stream.next().await { }`

## 优雅的关闭

### 找出合适的关闭时机

- Ctrl+C / 信号 / 管理端口 / 空闲超时

### 通知程序的每一个部分开始关闭

```rust
let (shutdown_tx, mut shutdown_rx) = broadcast::channel(1);
// 各任务 select! 监听 shutdown_rx
```

### 等待各个部分的结束

```rust
let mut handles = vec![];
handles.push(tokio::spawn(/* ... */));
for h in handles { h.await.unwrap(); }
```

- 先 broadcast shutdown → 等 spawn 任务 join → 再退出 main

## 异步跟同步共存

### `#[tokio::main]` 的展开

```rust
fn main() {
    tokio::runtime::Builder::new_multi_thread()
        .enable_all().build().unwrap()
        .block_on(async { /* 你的 main */ })
}
```

### mini-redis 的同步接口

```rust
// 阻塞式客户端：内部 block_on
let rt = tokio::runtime::Runtime::new()?;
rt.block_on(async { client.get("k").await })
```

### 其它方法

- `Handle::current().block_on(...)`（已在 runtime 内时慎用）
- CPU 密集：`tokio::task::spawn_blocking(|| { ... }).await`
- 目录：`src/bin/server.rs`、`src/bin/client.rs`、`examples/hello-redis.rs`
