+++
title = "3.4.3 带泛型的 Typestate 模式"
date = 2026-08-11T11:30:00+08:00
weight = 448
type = "docs"
description = "带泛型的 Typestate 模式 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/typestate-pattern/typestate-generics.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/typestate-pattern/typestate-generics.html)

## 带泛型的 Typestate 模式

将 typestate 建模与泛型结合，我们可以表达更广范围的有效状态与转换，而无需重复逻辑。当状态数量增长，或多个状态共享行为但结构不同时，这种方法尤其有用。

```rust
# 3.4.3 带泛型的 Typestate 模式
// SPDX-License-Identifier: Apache-2.0
struct Serializer<S> {
    // [...]
    indent: usize,
    buffer: String,
    state: S,
}

struct Root;
struct Struct<S>(S);
struct Property<S>(S);
struct List<S>(S);
```

我们现在具备了为实现 `Serializer` 及其状态类型定义编写方法所需的全部工具。这确保我们的 API 只允许有效转换，如下图所示：

> - 通过用泛型跟踪父上下文，我们可以构造任意嵌套的序列化器，强制结构体、列表与属性状态之间的有效转换。
>
> - 这使我们能构建递归结构，同时严格控制每个状态下可访问的方法。
>
> - 对所有状态通用的方法可对任意 `S` 定义为 `Serializer<S>` 上的方法。
>
> - 标记类型（如 `List<S>`）不引入内存或运行时开销，因为除可能的零大小类型外它们不含数据。它们的唯一作用是通过类型系统强制正确的 API 用法。

