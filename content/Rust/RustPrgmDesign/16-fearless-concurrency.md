+++
title = "16-无畏并发"
date = 2026-07-28T14:49:00+08:00
weight = 160
type = "docs"
description = "线程、信道、Mutex/Arc 与 Send/Sync 并发精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第16章

# 无畏并发

Rust 用**所有权 + 类型系统**在**编译时**捕获并发错误 → **无畏并发**（fearless concurrency）。

并发 = 独立执行；并行 = 同时执行。本章聚焦并发。

## 使用线程同时运行代码

- Rust 标准库用 **1:1 线程模型**（每个语言线程 = 一个 OS 线程）。

### 使用 `spawn` 创建新线程

```rust
thread::spawn(|| {
    for i in 1..10 { println!("hi {i} from spawned"); }
});
// 主线程结束 → 所有 spawn 线程也结束
```

### 等待所有线程结束

```rust
let handle = thread::spawn(|| { /* ... */ });
handle.join().unwrap();  // 阻塞直到线程结束
```

- `join()` 位置影响执行顺序：放在循环前 → 子线程先跑完。

### 将 `move` 闭包与线程一同使用

- 传给 `thread::spawn` 的闭包常用 `move` — 取得环境值所有权，避免悬垂引用。

```rust
let v = vec![1, 2, 3];
let handle = thread::spawn(move || {
    println!("{:?}", v);
});
// v 已被 move 进闭包，主线程不能再使用
```

## 使用消息传递在线程间传送数据

> "不要通过共享内存来通讯；而要通过通讯来共享内存。"

### 基本用法

```rust
use std::sync::mpsc;
let (tx, rx) = mpsc::channel();

thread::spawn(move || {
    tx.send(String::from("hi")).unwrap();
});

let received = rx.recv().unwrap();  // 阻塞等待
```

- `mpsc` = **多生产者，单消费者**。
- `tx.clone()` 创建额外发送端。
- `send` **移动**所有权 → 发送后不能再使用值。
- `rx` 当迭代器：`for msg in rx { ... }` — 信道关闭时结束。
- `try_recv()` — 非阻塞，立即返回 `Result`。

## 共享状态并发

### 使用互斥器控制访问

```rust
let m = Mutex::new(5);
{
    let mut num = m.lock().unwrap();  // 获取锁
    *num = 6;
}  // MutexGuard drop → 自动解锁
```

- `Mutex<T>` 是智能指针；`lock()` 返回 `MutexGuard`（实现 `Deref` + `Drop`）。
- 规则：先 lock，用完自动 unlock。

### 给 `Mutex<T>` 共享访问

- 多线程共享 `Mutex` → 需要 `Arc<T>`（**原子引用计数**，线程安全版 `Rc`）。

```rust
use std::sync::{Arc, Mutex};
let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    handles.push(thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    }));
}
// 结果: 10
```

- `Rc<T>` **不能**跨线程（未实现 `Send`）→ 编译错误。
- `Arc<T>` + `Mutex<T>` = 多线程共享可变数据。
- 简单数值运算可用 `AtomicI32` 等（`std::sync::atomic`），比 `Mutex` 更高效。

### 比较 `RefCell<T>`/`Rc<T>` 和 `Mutex<T>`/`Arc<T>`

| 单线程 | 多线程 |
|--------|--------|
| `RefCell<T>` / `Rc<T>` | `Mutex<T>` / `Arc<T>` |

- `Mutex` 提供内部可变性；`Arc<Mutex<T>>` 类似 `Rc<RefCell<T>>` 但线程安全。
- 注意死锁风险（两个线程各持一把锁互相等待）。

## 使用 `Send` 和 `Sync` trait 的可扩展并发

### 在线程间转移所有权 — `Send`

- `Send`：类型所有权可在线程间传送。
- 几乎所有类型都是 `Send`；**例外**：`Rc<T>`（非线程安全引用计数）。

### 多线程访问 — `Sync`

- `Sync`：`&T` 可安全地在多线程间共享（即 `&T` 实现了 `Send`）。
- **例外**：`Rc<T>`、`RefCell<T>`、`Cell<T>` 未实现 `Sync`。
- `Mutex<T>` 实现了 `Sync`。

### 手动实现 `Send` 和 `Sync` 是不安全的

- 标记 trait，无方法。组合类型自动实现。
- 手动实现需 `unsafe` Rust。

## 总结

| 机制 | 用途 |
|------|------|
| `thread::spawn` + `move` | 创建线程 |
| `mpsc::channel` | 消息传递（所有权转移） |
| `Arc<Mutex<T>>` | 共享可变状态 |
| `Send` / `Sync` | 编译时并发安全检查 |

更多并发方案见社区 crate。下一章：async/await。
