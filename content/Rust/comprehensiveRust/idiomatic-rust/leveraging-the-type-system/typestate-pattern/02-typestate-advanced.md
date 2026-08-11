+++
title = "3.4.2 超越简单 Typestate"
date = 2026-08-11T11:30:00+08:00
weight = 447
type = "docs"
description = "02-超越简单 Typestate — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/typestate-pattern/typestate-advanced.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/typestate-pattern/typestate-advanced.html)

## 超越简单 Typestate

如何管理日益复杂、有许多可能状态与转换的配置流程，同时仍防止不兼容的操作？

```rust
# 3.4.2 超越简单 Typestate
// SPDX-License-Identifier: Apache-2.0
struct Serializer {/* [...] */}
struct SerializeStruct {/* [...] */}
struct SerializeStructProperty {/* [...] */}
struct SerializeList {/* [...] */}

impl Serializer {
    // TODO，实现：
    //
    // fn serialize_struct(self, name: &str) -> SerializeStruct
    // fn finish(self) -> String
}

impl SerializeStruct {
    // TODO，实现：
    //
    // fn serialize_property(mut self, name: &str) -> SerializeStructProperty

    // TODO，
    // 我们应如何结束这个结构体？这取决于它出现在何处：
    // - 在根层：返回 `Serializer`
    // - 作为另一结构体内部的属性：返回 `SerializeStruct`
    // - 作为列表内的值：返回 `SerializeList`
    //
    // fn finish(self) -> ???
}

impl SerializeStructProperty {
    // TODO，实现：
    //
    // fn serialize_string(self, value: &str) -> SerializeStruct
    // fn serialize_struct(self, name: &str) -> SerializeStruct
    // fn serialize_list(self) -> SerializeList
    // fn finish(self) -> SerializeStruct
}

impl SerializeList {
    // TODO，实现：
    //
    // fn serialize_string(mut self, value: &str) -> Self
    // fn serialize_struct(mut self, value: &str) -> SerializeStruct
    // fn serialize_list(mut self) -> SerializeList

    // TODO：
    // 与 `SerializeStruct::finish` 类似，返回类型取决于嵌套位置。
    //
    // fn finish(mut self) -> ???
}
```

有效转换示意图：

```bob
    +-----------+   +---------+------------+-----+
    |           |   |         |            |     |
    V           |   V         |            V     |
                +                                |
serializer --> structure --> property --> list +-+

    |           |   ^           |          ^
    V           |   |           |          |
                |   +-----------+          |
  String        |                          |
                +--------------------------+
```

> - 在先前序列化器的基础上，我们现在想支持**嵌套结构**与**列表**。
>
> - 但这同时引入了**重复**与**结构复杂度**。
>
> - 更关键的是，我们现在碰到了**类型系统限制**：若不针对每种嵌套上下文（如根、结构体、列表）复制变体，就无法干净地表达 `finish()` 应返回什么。
>
> - 从有效转换示意图可以观察到：
>   - 转换是递归的
>   - 返回类型取决于子结构或列表出现在_何处_
>   - 每个上下文都需要一条返回其父级的路径
>
> - 仅用具体类型会变得难以管理。当前做法会导致类型爆炸与手工接线。
>
> - 下一章我们将看到，**泛型**如何让我们用更少的样板代码建模递归流程，同时仍在编译期强制有效操作。

