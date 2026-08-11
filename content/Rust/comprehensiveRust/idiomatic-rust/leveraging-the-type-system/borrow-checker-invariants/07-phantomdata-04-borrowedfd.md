+++
title = "3.5.7 PhantomData：OwnedFd 与 BorrowedFd"
date = 2026-08-11T11:30:00+08:00
weight = 460
type = "docs"
description = "07-PhantomData：OwnedFd 与 BorrowedFd — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/borrow-checker-invariants/phantomdata-04-borrowedfd.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/borrow-checker-invariants/phantomdata-04-borrowedfd.html)

# 3.5.7 PhantomData：OwnedFd 与 BorrowedFd

`BorrowedFd` 是 `PhantomData` 实际应用的典型例子。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::marker::PhantomData;
use std::os::raw::c_int;

mod libc_ffi {
    use std::os::raw::{c_char, c_int};
    pub unsafe fn open(path: *const c_char, oflag: c_int) -> c_int {
        3
    }
    pub unsafe fn close(fd: c_int) {}
}

struct OwnedFd {
    fd: c_int,
}

impl OwnedFd {
    fn try_from_fd(fd: c_int) -> Option<Self> {
        if fd < 0 {
            return None;
        }
        Some(OwnedFd { fd })
    }

    fn as_fd<'a>(&'a self) -> BorrowedFd<'a> {
        BorrowedFd { fd: self.fd, _phantom: PhantomData }
    }
}

impl Drop for OwnedFd {
    fn drop(&mut self) {
        unsafe { libc_ffi::close(self.fd) };
    }
}

struct BorrowedFd<'a> {
    fd: c_int,
    _phantom: PhantomData<&'a ()>,
}

fn main() {
    // 用原始系统调用以只写和创建权限创建文件。
    let fd = unsafe { libc_ffi::open(c"c_str.txt".as_ptr(), 065) };
    // 将整数文件描述符的所有权交给 `OwnedFd`。
    // `OwnedFd::drop()` 关闭文件描述符。
    let owned_fd =
        OwnedFd::try_from_fd(fd).expect("Could not open file with syscall!");

    // 从 `OwnedFd` 创建 `BorrowedFd`。
    // `BorrowedFd::drop()` 不关闭文件，因为它不拥有它！
    let borrowed_fd: BorrowedFd<'_> = owned_fd.as_fd();
    // std::mem::drop(owned_fd); // ❌🔨
    std::mem::drop(borrowed_fd);
    let second_borrowed = owned_fd.as_fd();
    // owned_fd 将在此处被 drop，文件将被关闭。
}
```

> - 文件描述符表示特定进程对文件的访问。
>
>   提醒：在类 Unix 系统上，设备和操作系统特定功能被暴露为仿佛它们是文件。
>
> - [`OwnedFd`](https://rust-lang.github.io/rfcs/3128-io-safety.html#ownedfd-and-borrowedfdfd)
>   是文件描述符的拥有包装类型。它**拥有**文件描述符，并在 drop 时关闭它。
>
>   注意：我们这里有自己的实现，请注意显式的 `Drop` 实现。
>
>   `BorrowedFd` 是其借用对应物，在被 drop 时无需关闭文件。
>
>   注意：我们没有为 `BorrowedFd` 显式实现 `Drop`。
>
> - `BorrowedFd` 用 `PhantomData` 捕获的生命周期强制不变量：「若此文件描述符存在，则操作系统文件描述符仍打开，即便它不负责关闭该文件描述符。」
>
>   `BorrowedFd` 的生命周期参数要求程序中存在另一个值，其存活时间至少与该特定 `BorrowedFd` 一样长或更长（本例中是 `OwnedFd`）。
>
>   演示：取消注释 `std::mem::drop(owned_fd)` 行并尝试编译，以展示 `borrowed_fd` 依赖 `owned_fd` 的生命周期。
>
>   API 设计者将其编码为意味着**是那另一个值保持对文件的访问打开**。
>
>   因为 Rust 的借用检查器强制这种「一个值必须至少与另一个一样长」的关系，此 API 的用户不必自己操心正确处理文件描述符别名与关闭逻辑。

