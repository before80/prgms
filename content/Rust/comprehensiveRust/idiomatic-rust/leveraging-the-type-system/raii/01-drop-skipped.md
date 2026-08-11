+++
title = "3.2.1 跳过 Drop"
date = 2026-08-11T11:30:00+08:00
weight = 431
type = "docs"
description = "01-跳过 Drop — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/raii/drop_skipped.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/raii/drop_skipped.html)

# 3.2.1 跳过 Drop

存在析构函数不会运行的情况。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug)]
struct OwnedFd(i32);

impl Drop for OwnedFd {
    fn drop(&mut self) {
        println!("OwnedFd::drop() called with raw fd: {:?}", self.0);
    }
}

impl Drop for TmpFile {
    fn drop(&mut self) {
        println!("TmpFile::drop() called with owned fd: {:?}", self.0);
        // libc::unlink("/tmp/file")
        // panic!("TmpFile::drop() panics");
    }
}

#[derive(Debug)]
struct TmpFile(OwnedFd);

impl TmpFile {
    fn open() -> Self {
        Self(OwnedFd(2))
    }

    fn close(&self) {
        panic!("TmpFile::close(): not implemented yet");
    }
}

fn main() {
    let owned_fd = OwnedFd(1);

    let file = TmpFile::open();

    std::process::exit(0);

    // std::mem::forget(file);

    // file.close();

    let _ = owned_fd;
}
```

> - Drop 并不保证总会运行。有多种情况会跳过 drop：程序崩溃或退出、带有 drop 实现的值被泄漏等。
>
> - 在调用
>   [`std::process::exit`](https://doc.rust-lang.org/std/process/fn.exit.html)
>   的版本中，`TmpFile::drop()` 永远不会运行，因为 `exit()` 会立即终止进程，没有机会调用任何 `drop()` 方法。
>
>   - 可通过拒绝
>     [`clippy::exit`](https://rust-lang.github.io/rust-clippy/stable/index.html#exit)
>     lint 来防止误用 `exit`。
>
> - 若去掉 `std::process::exit(0)` 这一行，在这个简单例子中每个 `drop()` 方法都会依次运行。
>
> - 试着取消注释
>   [`std::mem::forget`](https://doc.rust-lang.org/std/mem/fn.forget.html)
>   调用。你认为会发生什么？
>
>   `mem::forget()` 取得所有权并「忘记」值 `file`，而不运行其**析构函数** `Drop::drop()`。`owned_fd` 的析构函数仍会运行。
>
> - 去掉 `mem::forget()` 调用，再取消注释下面的 `file.close()`。现在你期望怎样？
>
>   在默认的 `panic = "unwind"` 设置下，即使 panic 从 `main` 开始，栈仍会展开，析构函数仍会运行。
>
>   - 使用
>     [`panic = "abort"`](https://doc.rust-lang.org/cargo/reference/profiles.html#panic)
>     时，不会运行任何析构函数。
>
> - 最后一步：取消注释 `TmpFile::drop()` 内的 `panic!` 并运行。问全班：abort 之前哪些析构函数会运行？
>
>   双重 panic 之后，Rust 不再保证剩余析构函数会运行：
>
>   - 某些已在进行中的清理仍可能完成（例如，当前正在被 drop 的值的字段析构函数），
>   - 但在展开路径中稍后安排的清理可能被完全跳过。
>   - 因此我们说：不能仅依赖 `drop()` 做关键外部清理，也不能假设双重 panic 会 abort 且不再运行任何后续析构函数。
>
> - 有些语言禁止或限制在析构函数中抛异常。Rust 允许在 `Drop::drop` 中 panic，但这几乎从来不是好主意，因为它会干扰展开并导致不可预测的清理。除非有非常具体的需求（例如 **drop bomb**），最好避免。
>
> - Drop 适合清理进程范围内的资源，但不适合为进程外发生的事情提供硬保证（例如本地磁盘，或分布式系统中的另一服务）。
>
> - 例如，在 `drop()` 中删除临时文件在玩具示例中没问题，但在真实程序中仍需要外部清理机制，例如临时文件回收器（reaper）。
>
> - 相比之下，我们可以依赖 `drop()` 解锁互斥锁，因为它是进程本地资源。若跳过 `drop()` 且互斥锁保持锁定，进程外不会有持久影响。

