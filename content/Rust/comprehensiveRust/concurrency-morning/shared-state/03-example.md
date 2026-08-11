+++
title = "5.3 示例"
date = 2026-08-11T11:30:00+08:00
weight = 360
type = "docs"
description = "03-示例 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/shared-state/example.html](https://google.github.io/comprehensive-rust/concurrency/shared-state/example.html)

# 5.3 示例

来看 `Arc` 与 `Mutex` 的实际用法：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::thread;
// use std::sync::{Arc, Mutex};

fn main() {
    let v = vec![10, 20, 30];
    let mut handles = Vec::new();
    for i in 0..5 {
        handles.push(thread::spawn(|| {
            v.push(10 * i);
            println!("v: {v:?}");
        }));
    }

    handles.into_iter().for_each(|h| h.join().unwrap());
}
```

> 可行解法：
>
> ```rust
> // Copyright 2024 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> use std::sync::{Arc, Mutex};
> use std::thread;
>
> fn main() {
>     let v = Arc::new(Mutex::new(vec![10, 20, 30]));
>     let mut handles = Vec::new();
>     for i in 0..5 {
>         let v = Arc::clone(&v);
>         handles.push(thread::spawn(move || {
>             let mut v = v.lock().unwrap();
>             v.push(10 * i);
>             println!("v: {v:?}");
>         }));
>     }
>
>     handles.into_iter().for_each(|h| h.join().unwrap());
> }
> ```
>
> 要点：
>
> - `v` 同时包在 `Arc` 与 `Mutex` 中，因为它们关注的问题是正交的。
>   - 把 `Mutex` 包在 `Arc` 里是在线程间共享可变状态的常见模式。
> - `v: Arc<_>` 需要克隆，以便为每个新派生的线程提供新引用。注意 lambda 签名中加了 `move`。
> - 引入代码块以尽可能缩小 `LockGuard` 的作用域。

