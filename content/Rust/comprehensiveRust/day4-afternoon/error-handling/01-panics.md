+++
title = "2.1 Panic"
date = 2026-08-11T11:30:00+08:00
weight = 187
type = "docs"
description = "01-Panic — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/error-handling/panics.html](https://google.github.io/comprehensive-rust/error-handling/panics.html)

# 2.1 Panic

遇到致命的运行时错误时，Rust 会触发 panic（恐慌）：

```rust
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let v = vec![10, 20, 30];
    dbg!(v[100]);
}
```

- Panic 用于不可恢复、出乎意料的错误。
  - Panic 往往是程序中存在 bug 的症状。
  - 运行时失败（例如边界检查失败）可能触发 panic。
  - 断言（如 `assert!`）失败时会 panic。
  - 针对特定场景可用 `panic!` 宏主动触发。
- Panic 会“展开”（unwind）调用栈，并像函数正常返回一样丢弃（drop）值。
- 若不能接受进程崩溃，请改用不会 panic 的 API（例如 `Vec::get`）。

> <summary>讲师备注</summary>
>
> 默认情况下，panic 会展开调用栈。这种展开可以被捕获：
>
> ```rust
> // Copyright 2022 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> use std::panic;
>
> fn main() {
>     let result = panic::catch_unwind(|| "No problem here!");
>     dbg!(result);
>
>     let result = panic::catch_unwind(|| {
>         panic!("oh no!");
>     });
>     dbg!(result);
> }
> ```
>
> - 捕获 panic 并不常见；不要试图用 `catch_unwind` 实现类似异常的机制！
> - 在服务器场景中可能有用：即使单个请求崩溃，服务整体仍应继续运行。
> - 若在 `Cargo.toml` 中设置了 `panic = 'abort'`，则无法用这种方式捕获。

