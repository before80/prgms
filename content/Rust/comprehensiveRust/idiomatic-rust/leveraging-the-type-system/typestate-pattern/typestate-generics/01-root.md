+++
title = "3.4.3.1 Serializer：实现 Root"
date = 2026-08-11T11:30:00+08:00
weight = 449
type = "docs"
description = "01-Serializer：实现 Root — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/typestate-pattern/typestate-generics/root.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/typestate-pattern/typestate-generics/root.html)

## Serializer：实现 Root

```rust
# 3.4.3.1 Serializer：实现 Root
// SPDX-License-Identifier: Apache-2.0
# use std::fmt::Write as _;
struct Serializer<S> {
    // [...]
    indent: usize,
    buffer: String,
    state: S,
}

struct Root;
struct Struct<S>(S);

impl Serializer<Root> {
    fn new() -> Self {
        // [...]
        Self { indent: 0, buffer: String::new(), state: Root }
    }

    fn serialize_struct(mut self, name: &str) -> Serializer<Struct<Root>> {
        // [...]
        writeln!(self.buffer, "{name} {{").unwrap();
        Serializer {
            indent: self.indent + 1,
            buffer: self.buffer,
            state: Struct(self.state),
        }
    }

    fn finish(self) -> String {
        // [...]
        self.buffer
    }
}
```

回到最初的有效转换示意图，可将实现的开端可视化如下：

```bob
                          serialize
                          struct
+--------------------+ --------------> +----------------------------+
| "Serializer<Root>" |                 | "Serializer<Struct<Root>>" |
+--------------------+ <-------------- +----------------------------+
                         finish struct
         |
         |
         |
finish   |
         V

     +--------+
     | String |
     +--------+
```

> - 在我们的 `Serializer`「根」处，唯一允许的构造是 `Struct`。
>
> - `Serializer` 只能在该根层终结为 `String`。

