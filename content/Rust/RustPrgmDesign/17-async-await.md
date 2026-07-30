+++
title = "17-异步编程基础：Async、Await、Future与Stream"
date = 2026-07-28T14:49:00+08:00
weight = 170
type = "docs"
description = "Future、async/await、运行时、Stream 与 Pin 精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第17章

# 异步编程基础：Async、Await、Future 与 Stream

**异步** = 操作可能暂停、稍后恢复；**运行时**管理执行。**CPU 密集型** → 线程；**I/O 密集型** → async。

- **并发**：单核切换任务（交替推进）。
- **并行**：多核同时执行。

## Future 与 async 语法

- **Future**：将来某时刻就绪的值（实现 `Future` trait）。
- `async fn` / `async { }` → 编译为返回 future 的函数/块。
- `await` 是**后缀关键字**：`future.await`（Rust 特有）。
- Future **惰性**：不 `await` 就不执行（编译器警告未使用 future）。

```rust
async fn page_title(url: &str) -> Option<String> {
    let text = trpl::get(url).await.text().await;
    Html::parse(&text).select_first("title").map(|t| t.inner_html())
}
// 等价于：
fn page_title(url: &str) -> impl Future<Output = Option<String>> {
    async move { /* ... */ }
}
```

### 使用运行时执行异步函数

- `main` **不能**是 `async fn` — 需要运行时初始化。
- Rust **无内置运行时**，需选第三方（如 tokio）。

```rust
fn main() {
    trpl::block_on(async {
        let title = page_title(url).await;
        // ...
    });
}
```

- 每个 `await` 点 = 可能暂停并交还控制权给运行时。
- 编译器自动生成**状态机**管理暂停/恢复。

### 让两个 URL 并发竞争

```rust
let (url, page_title) = match trpl::select(title_fut_1, title_fut_2).await {
    trpl::Either::Left(left) => left,
    trpl::Either::Right(right) => right,
};
```

## 使用 async 实现并发

### 使用 `spawn_task` 创建新任务

```rust
trpl::spawn_task(async { /* ... */ });
// 类似 thread::spawn，但由运行时管理，非 OS 线程
```

- 任务句柄是 future → `handle.await.unwrap()` 等待完成。
- `trpl::join(fut1, fut2).await` — 两个 future 都完成（公平交替）。

### 通过消息传递在两个任务之间发送数据

```rust
let (tx, rx) = trpl::channel();
// tx.send(msg) — 不阻塞
// rx.recv().await — 异步等待
```

- **关键**：单个 `async` 块内代码**线性执行**，无并发。
- 要并发 → 分成多个 `async` 块 + `trpl::join` / `join!`。
- `async move` — 将所有权移入块，块结束时 drop（关闭信道发送端）。

```rust
let tx_fut = async move { /* send */ };
let rx_fut = async { /* recv */ };
trpl::join(tx_fut, rx_fut).await;
```

- `while let Some(msg) = rx.recv().await { ... }` — 接收直到信道关闭。
- `join!` 宏 — 等待编译期已知数量的 future。

### 将控制权交还给运行时

- await 点之间全是**同步**执行 → 长计算会**饿死**其他 future。
- 主动交出：`trpl::yield_now().await`（比 `sleep` 更轻量）。
- 协作式多任务：每个 future 负责在适当时交出控制权。

### 构建我们自己的异步抽象

```rust
async fn timeout<F: Future>(future_to_try: F, max_time: Duration) -> Result<F::Output, Duration> {
    match trpl::select(future_to_try, trpl::sleep(max_time)).await {
        trpl::Either::Left(output) => Ok(output),
        trpl::Either::Right(_) => Err(max_time),
    }
}
```

## Stream：按顺序出现的 Future

- **Stream** = 异步版迭代器（条目随时间到达）。
- 需 `use trpl::StreamExt` 才能用 `.next().await`。

```rust
let stream = trpl::stream_from_iter(iter);
while let Some(value) = stream.next().await {
    println!("{value}");
}
```

- `Stream` trait 提供 `poll_next`；`StreamExt` 提供 `next` 等高层 API。

## 深入理解 async 相关的 trait

### `Future` trait

```rust
pub trait Future {
    type Output;
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}

pub enum Poll<T> { Ready(T), Pending }
```

- `poll` → `Ready(值)` 或 `Pending`（稍后重试）。
- `await` 底层 = 循环 poll + 运行时调度。

### `Pin` 类型与 `Unpin` trait

- async 状态机可能**自引用** → 移动不安全。
- `Pin` 保证被 pin 的值不移动。
- `Unpin` — 标记 trait，表示可以安全移动（大多数类型）。
- `!Unpin` — 特殊标记，不能移动（async 生成的 future）。
- 动态 future 集合：`pin!(fut)` 或 `Box::pin(fut)`。

### `Stream` trait

```rust
trait Stream {
    type Item;
    fn poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>>;
}
```

- 合并 `Iterator::next` + `Future::poll` 语义。

## 结合起来看：Future、任务与线程

| 层级 | 类比 | 管理 |
|------|------|------|
| 线程 | OS 级并发边界 | 操作系统 |
| 任务 | async 并发边界 | 运行时 |
| Future | 最细粒度并发单位 | 运行时 executor |

选择指南：
- **CPU 密集型**（并行计算）→ 线程
- **I/O 密集型**（高并发网络/文件）→ async
- 常组合使用：线程做计算 + async 信道通知 UI

```rust
// 线程发送 + async 接收
thread::spawn(move || { tx.send(i).unwrap(); });
trpl::block_on(async { while let Some(n) = rx.recv().await { ... } });
```

## 总结

- `async/await` + 运行时 = Rust 异步模型。
- 单 async 块线性执行；并发需多 future + join/select。
- `move` 关闭信道；`yield_now` 交出控制权。
- `Pin`/`Unpin` 保证自引用 future 安全。
- 线程与 async 互补，非二选一。
