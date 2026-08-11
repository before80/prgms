+++
title = "3.4.1 Typestate 模式示例"
date = 2026-08-11T11:30:00+08:00
weight = 446
type = "docs"
description = "01-Typestate 模式示例 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/typestate-pattern/typestate-example.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/typestate-pattern/typestate-example.html)

## Typestate 模式：示例

Typestate 模式将值运行时状态的一部分编码进其类型。这使我们能在编译期防止无效或不适用的操作。

```rust
# 3.4.1 Typestate 模式示例
// SPDX-License-Identifier: Apache-2.0
use std::fmt::Write as _;

#[derive(Default)]
struct Serializer {
    output: String,
}

struct SerializeStruct {
    serializer: Serializer,
}

impl Serializer {
    fn serialize_struct(mut self, name: &str) -> SerializeStruct {
        writeln!(&mut self.output, "{name} {{").unwrap();
        SerializeStruct { serializer: self }
    }

    fn finish(self) -> String {
        self.output
    }
}

impl SerializeStruct {
    fn serialize_field(mut self, key: &str, value: &str) -> Self {
        writeln!(&mut self.serializer.output, "  {key}={value};").unwrap();
        self
    }

    fn finish_struct(mut self) -> Serializer {
        self.serializer.output.push_str("}\n");
        self.serializer
    }
}

fn main() {
    let serializer = Serializer::default()
        .serialize_struct("User")
        .serialize_field("id", "42")
        .serialize_field("name", "Alice")
        .finish_struct();

    println!("{}", serializer.finish());
}
```

`Serializer` 使用流程图：

```bob
+------------+  serialize struct   +-----------------+
| Serializer | ------------------> | SerializeStruct | <------+
+------------+                     +-----------------+        |
                                                              |
   |   ^                             |     |                  |
   |   |     finish struct           |     | serialize field  |
   |   +-----------------------------+     +------------------+
   |
   +---> finish
```

> - 本示例受 Serde 的
>   [`Serializer` trait](https://docs.rs/serde/latest/serde/ser/trait.Serializer.html)
>   启发。Serde 在内部使用 typestate 确保序列化遵循有效结构。更多信息见：<https://serde.rs/impl-serializer.html>
>
> - Typestate 的核心思想是：状态转换通过消费一个值并产生一个新值来完成。在每一步，只有对该状态有效的操作才可用。
>
> - 在本例中：
>
>   - 我们从 `Serializer` 开始，它只允许我们开始序列化一个结构体。
>
>   - 一旦调用 `.serialize_struct(...)`，所有权移入 `SerializeStruct` 值。此后我们只能调用与序列化结构体字段相关的方法。
>
>   - 原来的 `Serializer` 不再可访问——防止我们混合模式（例如在结构体中途再开始另一个 _struct_）或过早调用 `finish()`。
>
>   - 只有在调用 `.finish_struct()` 之后，我们才重新得到 `Serializer`。此时可以终结输出或复用。
>
> - 若忘记调用 `finish_struct()` 并提前 drop 掉 `SerializeStruct`，`Serializer` 也会被 drop。这确保不完整输出不会泄漏到系统中。
>
> - 相比之下，若像上一页那样把一切都直接实现在 `Serializer` 上，就无法阻止有人跳过重要步骤或混合序列化流程。

