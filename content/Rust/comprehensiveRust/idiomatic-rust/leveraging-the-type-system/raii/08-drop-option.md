+++
title = "3.2.8 Drop 中的 Option"
date = 2026-08-11T11:30:00+08:00
weight = 438
type = "docs"
description = "08-Drop 中的 Option — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/raii/drop_option.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/raii/drop_option.html)

# 3.2.8 Drop 中的 Option

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
struct File(Option<Handle>);

impl File {
    fn open(path: &'static str) -> std::io::Result<Self> {
        Ok(Self(Some(Handle { path })))
    }

    fn write(&mut self, data: &str) -> std::io::Result<()> {
        // 必须先通过 `Option` 取得 `Handle`
        // 然后才能使用它。
        let handle = self.0.as_ref().unwrap();
        println!("write '{data}' to file '{}'", handle.path);
        Ok(())
    }
}

impl Drop for File {
    fn drop(&mut self) {
        let handle = self.0.take().unwrap();
        handle.close();
    }
}

struct Handle {
    path: &'static str,
}

impl Handle {
    fn close(self) {
        println!("Closing {}", self.path);
    }
}

fn main() -> std::io::Result<()> {
    let mut file = File::open("foo.txt")?;
    file.write("hello")?;
    Ok(())
}
```

> - 本例中我们想在 `Drop` 实现里对内部的 `Handle` 调用 `close`，但 `close` 需要 `Handle` 的所有权。正常情况下做不到：我们在 `drop` 中得不到 `File` 对象的所有权，因此无法移出字段。
>
> - 把 handle 包在 `Option` 中，让我们能通过可变引用移出字段。
>
> - 主要缺点是人体工学。`Option` 迫使我们处理 `Some` 和 `None` 两种情况，即便在逻辑上 `None` 不可能发生的地方也是如此。Rust 的类型系统无法表达 `File` 与其 `Handle` 之间的这种关系，所以我们手动处理两种情况。
>
> ## 深入探索
>
> 除了 `Option`，我们还可以使用
> [`ManuallyDrop`](https://doc.rust-lang.org/std/mem/struct.ManuallyDrop.html)，
> 它通过阻止 Rust 为该值调用 `Drop` 来抑制自动析构；你必须自己处理拆除。
>
> 上一页的
> [_scopeguard_ 示例](./07-scope-guard.md)
> 展示了如何用 `ManuallyDrop` 替代 `Option`，以避免在值应始终存在的地方处理 `None`。
>
> 在这类设计中，我们通常在 `ManuallyDrop<Handle>` 旁用单独的标志跟踪 drop 状态，从而知道 handle 是否已被手动消费。

