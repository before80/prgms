+++
title = "3.4 Typestate 模式"
date = 2026-08-11T11:30:00+08:00
weight = 445
type = "docs"
description = "Typestate 模式 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/typestate-pattern.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/typestate-pattern.html)

# 3.4 Typestate 模式

如何根据值的当前状态，确保只允许有效操作？

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::fmt::Write as _;

#[derive(Default)]
struct Serializer {
    output: String,
}

impl Serializer {
    fn serialize_struct_start(&mut self, name: &str) {
        let _ = writeln!(&mut self.output, "{name} {{");
    }

    fn serialize_struct_field(&mut self, key: &str, value: &str) {
        let _ = writeln!(&mut self.output, "  {key}={value};");
    }

    fn serialize_struct_end(&mut self) {
        self.output.push_str("}\n");
    }

    fn finish(self) -> String {
        self.output
    }
}

fn main() {
    let mut serializer = Serializer::default();
    serializer.serialize_struct_start("User");
    serializer.serialize_struct_field("id", "42");
    serializer.serialize_struct_field("name", "Alice");

    // serializer.serialize_struct_end(); // ← 糟糕！忘了调用

    println!("{}", serializer.finish());
}
```

> - 这个 `Serializer` 本意是写出结构化的值。
>
> - 但在本例中，我们在 `finish()` 之前忘了调用 `serialize_struct_end()`。结果是序列化输出不完整或语法不正确。
>
> - 一种修复方式是手动跟踪内部状态，并在当前状态无效时从 `serialize_struct_field()` 或 `finish()` 等方法返回 `Result`。
>
> - 但这有缺点：
>
>   - 作为实现者很容易弄错。Rust 的类型系统无法帮助强制状态转换的正确性。
>
>   - 也给用户增加不必要的负担：他们必须为本应在源码层面误用、而非运行时出错的操作处理 `Result`。
>
> - 更好的方案是直接在类型系统中建模有效的状态转换。
>
>   下一页我们将应用 **typestate 模式**，在编译期强制正确用法，使调用不兼容方法或忘记必做动作变得不可能。

