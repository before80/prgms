+++
title = "4.4 示例"
date = 2026-08-11T11:30:00+08:00
weight = 356
type = "docs"
description = "04-示例 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/send-sync/examples.html](https://google.github.io/comprehensive-rust/concurrency/send-sync/examples.html)

# 4.4 示例

## `Send + Sync`

你遇到的多数类型都是 `Send + Sync`：

- `i8`、`f32`、`bool`、`char`、`&str`、…
- `(T1, T2)`、`[T; N]`、`&[T]`、`struct { x: T }`、…
- `String`、`Option<T>`、`Vec<T>`、`Box<T>`、…
- `Arc<T>`：通过原子引用计数显式线程安全。
- `Mutex<T>`：通过内部加锁显式线程安全。
- `mpsc::Sender<T>`：自 1.72.0 起。
- `AtomicBool`、`AtomicU8`、…：使用特殊的原子指令。

泛型类型通常在类型参数是 `Send + Sync` 时也是 `Send + Sync`。

## `Send + !Sync`

这些类型可以移到其他线程，但不是线程安全的。通常因为内部可变性：

- `mpsc::Receiver<T>`
- `Cell<T>`
- `RefCell<T>`

## `!Send + Sync`

这些类型可以安全地（通过共享引用）从多个线程访问，但不能移到另一线程：

- `MutexGuard<T>`：使用操作系统级原语，必须在创建它们的线程上释放。不过，一把已锁定的互斥锁，其受保护变量可以由任何共享该 guard 的线程读取（除非 `T` 本身是 `!Sync`）。

## `!Send + !Sync`

这些类型不是线程安全的，也不能移到其他线程：

- `Rc<T>`：每个 `Rc<T>` 都引用一个 `RcBox<T>`，其中包含非原子引用计数。
- `*const T`、`*mut T`：Rust 假定原始指针可能有特殊的并发考量。
