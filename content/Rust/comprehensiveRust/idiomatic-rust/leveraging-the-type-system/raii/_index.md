+++
title = "3.2 RAII"
date = 2026-08-11T11:30:00+08:00
weight = 430
type = "docs"
description = "RAII — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/raii.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/raii.html)

# 3.2 RAII

RAII（**R**esource **A**cquisition **I**s **I**nitialization，资源获取即初始化）将资源的生命周期与值的生命周期绑定在一起。

[Rust 用 RAII 管理内存](https://doc.rust-lang.org/rust-by-example/scope/raii.html)，而 `Drop` trait 允许你把这一机制扩展到其他资源，例如文件描述符或锁。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub struct File(std::os::fd::RawFd);

impl File {
    pub fn open(path: &str) -> Result<Self, std::io::Error> {
        // [...]
        Ok(Self(0))
    }

    pub fn read_to_end(&mut self) -> Result<Vec<u8>, std::io::Error> {
        // [...]
        Ok(b"example".to_vec())
    }

    pub fn close(self) -> Result<(), std::io::Error> {
        // [...]
        Ok(())
    }
}

fn main() -> Result<(), std::io::Error> {
    let mut file = File::open("example.txt")?;
    println!("content: {:?}", file.read_to_end()?);
    Ok(())
}
```

> - 容易忽略：从未调用 `file.close()`。问问全班有没有人注意到。
>
> - 要正确释放文件描述符，必须在最后一次使用之后调用 `file.close()`——出错提前返回的路径上也要调用。
>
> - 与其依赖用户调用 `close()`，不如实现 `Drop` trait 自动释放资源。这样就将清理与 `File` 值的生命周期绑定。
>
>   ```rust
>   // Copyright 2025 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   impl Drop for File {
>       fn drop(&mut self) {
>           // libc::close(...);
>           println!("file descriptor was closed");
>       }
>   }
>   ```
>
> - 注意：`Drop::drop()` 不能返回 `Result`。任何失败都必须在内部处理或忽略。在标准库中，`Drop` 内关闭 FD 时的错误会被静默丢弃。参见实现：
>   <https://doc.rust-lang.org/src/std/os/fd/owned.rs.html#169-196>
>
> - 何时调用 `Drop::drop`？
>
>   通常，当 `main()` 中的 `file` 变量离开作用域时（无论是正常返回还是 panic），会自动调用 `drop()`。
>
>   若文件被移入另一个函数（如本例中的 `File::close()`），则该值在那个函数返回时被 drop——而不是在 `main` 中。
>
>   相比之下，C++ 即使对已移出（moved-from）的值，也会在原作用域运行析构函数。
>
> - 演示：在 `read_to_end()` 开头插入 `panic!("oops")` 并运行。展开（unwinding）期间 `drop()` 仍会执行。
>
> ### 深入探索
>
> `Drop` trait 还有一个重要限制：它不是 `async` 的。
>
> 这意味着你不能在析构函数中 `await`，而清理异步资源时常常需要这样做——例如套接字、数据库连接，或必须向另一系统发出完成信号的任务。
>
> - 了解更多：
>   <https://rust-lang.github.io/async-fundamentals-initiative/roadmap/async_drop.html>
> - nightly 上有实验性的 `AsyncDrop` trait：
>   <https://doc.rust-lang.org/nightly/std/future/trait.AsyncDrop.html>

