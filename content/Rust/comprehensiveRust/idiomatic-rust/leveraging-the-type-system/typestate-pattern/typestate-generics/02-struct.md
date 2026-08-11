+++
title = "3.4.3.2 Serializer：实现 Struct"
date = 2026-08-11T11:30:00+08:00
weight = 450
type = "docs"
description = "02-Serializer：实现 Struct — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/typestate-pattern/typestate-generics/struct.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/typestate-pattern/typestate-generics/struct.html)

## Serializer：实现 Struct

```rust
# 3.4.3.2 Serializer：实现 Struct
// SPDX-License-Identifier: Apache-2.0
# use std::fmt::Write as _;
struct Serializer<S> {
    // [...]
    indent: usize,
    buffer: String,
    state: S,
}

struct Struct<S>(S);
struct Property<S>(S);

impl<S> Serializer<Struct<S>> {
    fn serialize_property(mut self, name: &str) -> Serializer<Property<Struct<S>>> {
        // [...]
        write!(self.buffer, "{}{name}: ", " ".repeat(self.indent * 2)).unwrap();
        Serializer {
            indent: self.indent,
            buffer: self.buffer,
            state: Property(self.state),
        }
    }

    fn finish_struct(mut self) -> Serializer<S> {
        // [...]
        self.indent -= 1;
        writeln!(self.buffer, "{}}}", " ".repeat(self.indent * 2)).unwrap();
        Serializer { indent: self.indent, buffer: self.buffer, state: self.state.0 }
    }
}
```

示意图现可扩展如下：

```bob
                                                     +------+
                                             finish  |      |
                          serialize          struct  V      |
                          struct
+--------------------+ --------------> +-------------------------+
| "Serializer<Root>" |                 | "Serializer<Struct<S>>" |
+--------------------+ <-------------- +-------------------------+
                         finish struct
         |                                     serialize   |
         |                                     property    V
         |
finish   |                           +-----------------------------------+
         V                           | "Serializer<Property<Struct<S>>>" |
                                     +-----------------------------------+
     +--------+
     | String |
     +--------+
```

> - `Struct` 只能包含 `Property`；
>
> - 结束一个 `Struct` 会把控制权交回其父级；在上一页我们假定父级是 `Root`，但实际上也可以是其他东西，例如嵌套「结构体」时的 `Struct`。

