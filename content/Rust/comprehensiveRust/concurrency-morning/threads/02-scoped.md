+++
title = "2.2 作用域线程"
date = 2026-08-11T11:30:00+08:00
weight = 347
type = "docs"
description = "02-作用域线程 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/threads/scoped.html](https://google.github.io/comprehensive-rust/concurrency/threads/scoped.html)

# 2.2 作用域线程

普通线程无法从环境中借用：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::thread;

fn foo() {
    let s = String::from("Hello");
    thread::spawn(|| {
        dbg!(s.len());
    });
}

fn main() {
    foo();
}
```

不过可以使用[作用域线程][1]做到这一点：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::thread;

fn foo() {
    let s = String::from("Hello");
    thread::scope(|scope| {
        scope.spawn(|| {
            dbg!(s.len());
        });
    });
}

fn main() {
    foo();
}
```

[1]: https://doc.rust-lang.org/std/thread/fn.scope.html

> - 原因是：当 `thread::scope` 函数完成时，所有线程都保证已 join，因此它们可以返回借用的数据。
> - 普通的 Rust 借用规则仍然适用：要么由一个线程可变借用，要么由任意数量的线程不可变借用。

