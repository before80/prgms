+++
title = "2.7 `Drop`"
date = 2026-08-11T11:30:00+08:00
weight = 130
type = "docs"
description = "07-`Drop` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/memory-management/drop.html](https://google.github.io/comprehensive-rust/memory-management/drop.html)

# 2.7 `Drop`

实现了 [`Drop`][1] 的值可以在离开作用域时运行指定代码：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
struct Droppable {
    name: &'static str,
}

impl Drop for Droppable {
    fn drop(&mut self) {
        println!("Dropping {}", self.name);
    }
}

fn main() {
    let a = Droppable { name: "a" };
    {
        let b = Droppable { name: "b" };
        {
            let c = Droppable { name: "c" };
            let d = Droppable { name: "d" };
            println!("Exiting innermost block");
        }
        println!("Exiting next block");
    }
    drop(a);
    println!("Exiting main");
}
```

> - 注意：`std::mem::drop` 与 `std::ops::Drop::drop` 不是一回事。
> - 值在离开作用域时会自动被丢弃。
> - 丢弃值时，若它实现了 `std::ops::Drop`，则会调用其 `Drop::drop` 实现。
> - 随后其所有字段也会被丢弃，无论该类型是否实现了 `Drop`。
> - `std::mem::drop` 只是一个接受任意值的空函数。关键在于它取得该值的所有权，因此在其作用域结束时该值会被丢弃。这使得它成为在值本应离开作用域之前显式提前丢弃的便捷方式。
>   - 对那些在 `drop` 时做清理工作的对象很有用：释放锁、关闭文件等。
>
> 讨论点：
>
> - 为什么 `Drop::drop` 不接受 `self`？
>   - 简短回答：若接受 `self`，块结束时会调用 `std::mem::drop`，从而再次调用 `Drop::drop`，导致栈溢出！
> - 试着用 `a.drop()` 替换 `drop(a)`。


[1]: https://doc.rust-lang.org/std/ops/trait.Drop.html
