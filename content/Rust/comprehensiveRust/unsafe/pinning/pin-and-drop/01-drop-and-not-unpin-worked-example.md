+++
title = "8.8.1 完整示例"
date = 2026-08-11T11:30:00+08:00
weight = 560
type = "docs"
description = "01-完整示例 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/drop-and-not-unpin-worked-example.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/drop-and-not-unpin-worked-example.html)

# 8.8.1 完整示例

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::cell::RefCell;
use std::marker::PhantomPinned;
use std::mem;
use std::pin::Pin;

thread_local! {
    static BATCH_FOR_PROCESSING: RefCell<Vec<String>> = RefCell::new(Vec::new());
}

#[derive(Debug)]
struct CustomString(String);

#[derive(Debug)]
struct SelfRef {
    data: CustomString,
    ptr: *const CustomString,
    _pin: PhantomPinned,
}

impl SelfRef {
    fn new(data: &str) -> Pin<Box<SelfRef>> {
        let mut boxed = Box::pin(SelfRef {
            data: CustomString(data.to_owned()),
            ptr: std::ptr::null(),
            _pin: PhantomPinned,
        });

        let ptr: *const CustomString = &boxed.data;
        unsafe {
            Pin::get_unchecked_mut(Pin::as_mut(&mut boxed)).ptr = ptr;
        }
        boxed
    }
}

impl Drop for SelfRef {
    fn drop(&mut self) {
        // SAFETY: 安全，因为我们从 String 中读取字节
        let payload = unsafe { std::ptr::read(&self.data) };
        BATCH_FOR_PROCESSING.with(|log| log.borrow_mut().push(payload.0));
    }
}

fn main() {
    let pinned = SelfRef::new("Rust 🦀");
    drop(pinned);

    BATCH_FOR_PROCESSING.with(|batch| {
        println!("Batch: {:?}", batch.borrow());
    });
}
```

> 本示例使用 `Drop` trait 添加数据以供后续处理，例如遥测或日志。
>
> **Safety 注释是错误的。** `ptr::read` 创建按位拷贝，使 `self.data` 处于无效状态。`self.data` 会在方法结束时再次被 drop，导致 double free。
>
> 请学员修复代码。
>
> **建议 0：重新设计**
>
> 重新设计后处理系统，使其不依赖 `Drop`。
>
> **建议 1：Clone**
>
> 使用 `.clone()` 是显而易见的首选，但会分配内存。
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> impl Drop for SelfRef {
>     fn drop(&mut self) {
>         let payload = self.data.0.clone();
>         BATCH_FOR_PROCESSING.with(|log| log.borrow_mut().push(payload));
>     }
> }
> ```
>
> **建议 2：ManuallyDrop**
>
> 将 `CustomString` 包装在 `ManuallyDrop` 中，可防止在 `Drop` 实现末尾发生（第二次）自动 drop。
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> struct SelfRef {
>     data: ManuallyDrop<CustomString>,
>     ptr: *const CustomString,
>     _pin: PhantomPinned,
> }
>
> // ...
>
> impl Drop for SelfRef {
>     fn drop(&mut self) {
>         // SAFETY: self.data
>         let payload = unsafe { ManuallyDrop::take(&mut self.data) };
>         BATCH_FOR_PROCESSING.with(|log| log.borrow_mut().push(payload.0));
>     }
> }
> ```

