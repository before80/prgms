+++
title = "3.4.3.3 Serializer：实现 Property"
date = 2026-08-11T11:30:00+08:00
weight = 451
type = "docs"
description = "03-Serializer：实现 Property — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/typestate-pattern/typestate-generics/property.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/typestate-pattern/typestate-generics/property.html)

## Serializer：实现 Property

```rust
# 3.4.3.3 Serializer：实现 Property
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
struct List<S>(S);

impl<S> Serializer<Property<Struct<S>>> {
    fn serialize_struct(mut self, name: &str) -> Serializer<Struct<Struct<S>>> {
        // [...]
        writeln!(self.buffer, "{name} {{").unwrap();
        Serializer {
            indent: self.indent + 1,
            buffer: self.buffer,
            state: Struct(self.state.0),
        }
    }

    fn serialize_list(mut self) -> Serializer<List<Struct<S>>> {
        // [...]
        writeln!(self.buffer, "[").unwrap();
        Serializer {
            indent: self.indent + 1,
            buffer: self.buffer,
            state: List(self.state.0),
        }
    }

    fn serialize_string(mut self, value: &str) -> Serializer<Struct<S>> {
        // [...]
        writeln!(self.buffer, "{value},").unwrap();
        Serializer { indent: self.indent, buffer: self.buffer, state: self.state.0 }
    }
}
```

加上 Property 状态的方法后，我们的示意图已接近完整：

```bob
                                                     +------+
                                             finish  |      |
                          serialize          struct  V      |
                          struct
+--------------------+ --------------> +-------------------------+ <-----------+
| "Serializer<Root>" |                 | "Serializer<Struct<S>>" |             |
+--------------------+ <-------------- +-------------------------+ <-----------+
                         finish struct                                         |
         |                                     serialize   |                   |
         |                                     property    V        serialize  |
         |                                                          string or  |
finish   |                           +---------------------------+  struct     |
         V                           | "Serializer<Property<S>>" | ------------+
                                     +---------------------------+
     +--------+
     | String |                                serialize   |
     +--------+                                list        V

                                         +-----------------------+
                                         | "Serializer<List<S>>" |
                                         +-----------------------+
```

> - 属性可定义为 `String`、`Struct<S>` 或 `List<S>`，从而能表示嵌套结构。
>
> - 至此分步实现告一段落。包含 `List<S>` 支持的完整实现见下一页。

