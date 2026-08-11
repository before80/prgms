+++
title = "3.2 Traits（特征）"
date = 2026-08-11T11:30:00+08:00
weight = 78
type = "docs"
description = "Traits（特征）— Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/methods-and-traits/traits.html](https://google.github.io/comprehensive-rust/methods-and-traits/traits.html)

# 3.2 Traits（特征）

Rust 允许用 trait 对类型做抽象。它们类似于接口：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
trait Pet {
    /// 返回这只宠物说的一句话。
    fn talk(&self) -> String;

    /// 向终端打印一句问候这只宠物的话。
    fn greet(&self);
}
```

> - Trait 定义了类型要实现该 trait 所必须具备的一组方法。
>
> - 下一节「泛型」中，我们会看到如何编写对所有实现某 trait 的类型通用的功能。

