+++
title = "1.4.1 更多特质"
date = 2026-08-11T11:30:00+08:00
weight = 317
type = "docs"
description = "01-更多特质 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps/uart/traits.html](https://google.github.io/comprehensive-rust/bare-metal/aps/uart/traits.html)

# 1.4.1 更多特质

我们推导出`Debug`特征。实现更多一些特征会很有用
也是。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use core::fmt::{self, Write};

impl Write for Uart {
    fn write_str(&mut self, s: &str) -> fmt::Result {
        for c in s.as_bytes() {
            self.write_byte(*c);
        }
        Ok(())
    }
}

// 安全：`Uart`仅包含一个指向设备内存的指针，可以是
// 从任何上下文访问。
unsafe impl Send for Uart {}
```

> - 实施`Write`让我们使用`write!`和`writeln!`宏与我们的
>   `Uart`类型。
>
> - `Send`是一个自动特征，但不会自动实现，因为它不是
>   为指针实现。

