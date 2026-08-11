+++
title = "8.1 竞态"
date = 2026-08-06T17:08:00+08:00
weight = 39
type = "docs"
description = "数据竞争与竞态条件"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 竞态


> 原文链接: [https://doc.rust-lang.org/nomicon/races.html](https://doc.rust-lang.org/nomicon/races.html)


　　Safe Rust 保证不存在数据竞争（data race），其定义为：

* 两个或多个线程并发访问同一内存位置
* 其中至少一个是写
* 其中至少一个是未同步的

　　数据竞争具有未定义行为，因此在 Safe Rust 中不可能发生。数据竞争*主要*通过 Rust 的所有权系统 alone 来防止：不可能别名可变引用，因此不可能发生数据竞争。内部可变性（interior mutability）使情况更复杂，这也是我们有 `Send` 和 `Sync` trait 的重要原因（下一节详述）。

　　**然而 Rust 并不阻止一般的竞态条件（race condition）。**

　　在你无法控制调度器的场景下，这在数学上不可能——对普通 OS 环境确实如此。若你控制抢占，*可以*阻止一般竞态——[RTIC](https://github.com/rtic-rs/rtic) 等框架就采用这种技术。然而实际上控制调度非常罕见。

　　因此，Rust 因错误同步而死锁或做出荒谬行为，被认为仍是「safe」的：这称为一般竞态条件或资源竞态。显然这样的程序并不好，但 Rust 当然无法阻止所有逻辑错误。

　　无论如何，竞态条件 alone 无法在 Rust 程序中违反内存安全。只有与其他 unsafe 代码结合时，竞态条件才可能真正违反内存安全。例如，一个正确的程序如下：

```rust,no_run
use std::thread;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;

let data = vec![1, 2, 3, 4];
// 使用 Arc，以便 AtomicUsize 所在内存在另一线程递增时仍存在，
// 即使我们在它之前完全执行完毕。没有 Arc Rust 不会编译通过，
// 因为 thread::spawn 的 lifetime 要求！
let idx = Arc::new(AtomicUsize::new(0));
let other_idx = idx.clone();

// `move` 按值捕获 other_idx，移入此线程
thread::spawn(move || {
    // 可以 mutate idx，因为该值是 atomic，
    // 不会造成 Data Race。
    other_idx.fetch_add(10, Ordering::SeqCst);
});

// 用从 atomic 加载的值索引。这是安全的，因为我们只读一次 atomic 内存，
// 然后把该值的副本传给 Vec 的索引实现。此索引会正确做边界检查，
// 且值不会在中间被改变。然而若我们 spawn 的线程在此运行前已递增，
// 程序可能 panic。这是竞态条件，因为正确执行（panic 很少是正确行为）
// 取决于线程执行顺序。
println!("{}", data[idx.load(Ordering::SeqCst)]);
```

　　若我们提前做边界检查，然后用未检查的值 unsafe 访问数据，竞态条件可能违反内存安全：

```rust,no_run
use std::thread;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;

let data = vec![1, 2, 3, 4];

let idx = Arc::new(AtomicUsize::new(0));
let other_idx = idx.clone();

// `move` 按值捕获 other_idx，移入此线程
thread::spawn(move || {
    // 可以 mutate idx，因为该值是 atomic，
    // 不会造成 Data Race。
    other_idx.fetch_add(10, Ordering::SeqCst);
});

if idx.load(Ordering::SeqCst) < data.len() {
    unsafe {
        // 边界检查后又错误地加载 idx。
        // 它可能已改变。这是竞态条件，*且危险*，
        // 因为我们决定用 `get_unchecked`，它是 `unsafe`。
        println!("{}", data.get_unchecked(idx.load(Ordering::SeqCst)));
    }
}
```
