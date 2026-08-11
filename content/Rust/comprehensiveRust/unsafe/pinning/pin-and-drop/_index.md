+++
title = "8.8 `Pin<Ptr>` 与 `Drop`"
date = 2026-08-11T11:30:00+08:00
weight = 559
type = "docs"
description = "`Pin<Ptr>` 与 `Drop` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/pin-and-drop.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/pin-and-drop.html)

# 8.8 `Pin<Ptr>` 与 `Drop`

对已固定、`!Unpin` 类型而言，实现 `Drop` trait 是一个关键挑战。`drop` 方法接受 `&mut self`，这允许移动该值。然而，被固定的值绝不能移动。

## 错误的 `Drop` 实现

在 `drop` 内很容易意外移动值。赋值、`ptr::read` 和 `mem::replace` 等操作会在不知不觉中破坏 pinning 保证。

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
struct SelfRef {
    data: String,
    ptr: *const String,
}

impl Drop for SelfRef {
    fn drop(&mut self) {
        // 错误：`ptr::read` 将 `self.data` 移出 `self`。
        // 当 `_dupe` 在函数结束时被 drop，会导致 double free！
        let _dupe = unsafe { std::ptr::read(&self.data) };
    }
}
```

> `!Unpin` 类型可能使安全实现 `Drop` 变得困难。实现绝不能移动已固定的值。
>
> 已固定类型对内存稳定性做出保证。`ptr::read` 和 `mem::replace` 等操作会通过移动或复制数据在不知不觉中破坏这些保证，在类型系统不知情的情况下使内部指针失效。
>
> 在此 `drop()` 方法中，`_dupe` 是 `self.data` 的按位拷贝。方法结束时，它会与 `self` 一起被 drop。这种 double drop 是未定义行为。


## 正确的 `Drop` 实现

要为 `!Unpin` 类型正确实现 `Drop`，必须确保值不被移动。常见模式是创建一个在 `Pin<&mut T>` 上操作的辅助函数。

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::marker::PhantomPinned;
use std::pin::Pin;

struct SelfRef {
    data: String,
    ptr: *const String,
    _pin: PhantomPinned,
}

impl SelfRef {
    fn new(data: impl Into<String>) -> Pin<Box<SelfRef>> {
        let mut this = Box::pin(SelfRef {
            data: data.into(),
            ptr: std::ptr::null(),
            _pin: PhantomPinned,
        });
        let ptr: *const String = &this.data;
        // SAFETY: 在创建自引用之前，`this` 已被固定。
        unsafe {
            Pin::as_mut(&mut this).get_unchecked_mut().ptr = ptr;
        }
        this
    }

    // 此函数只能在已固定的 `SelfRef` 上调用。
    unsafe fn drop_pinned(self: Pin<&mut SelfRef>) {
        // `self` 已被固定，因此不能从中移出。
        println!("dropping {}", self.data);
    }
}

impl Drop for SelfRef {
    fn drop(&mut self) {
        // 可以安全调用 `drop_pinned`，因为 `drop` 是该值最后一次被使用。
        // 我们使用 `new_unchecked`，因为我们知道 `self` 不会再被移动。
        unsafe {
            SelfRef::drop_pinned(Pin::new_unchecked(self));
        }
    }
}

fn main() {
    let _pinned = SelfRef::new("Hello, ");
} // `Drop` 运行时不移动已固定的值
```
