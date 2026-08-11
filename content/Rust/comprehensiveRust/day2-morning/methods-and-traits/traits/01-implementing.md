+++
title = "3.2.1 实现 Trait"
date = 2026-08-11T11:30:00+08:00
weight = 79
type = "docs"
description = "01-实现 Trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/methods-and-traits/traits/implementing.html](https://google.github.io/comprehensive-rust/methods-and-traits/traits/implementing.html)

# 3.2.1 实现 Trait

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
trait Pet {
    fn talk(&self) -> String;

    fn greet(&self) {
        println!("Oh you're a cutie! What's your name? {}", self.talk());
    }
}

struct Dog {
    name: String,
    age: i8,
}

impl Pet for Dog {
    fn talk(&self) -> String {
        format!("Woof, my name is {}!", self.name)
    }
}

fn main() {
    let fido = Dog { name: String::from("Fido"), age: 5 };
    dbg!(fido.talk());
    fido.greet();
}
```

> - 要为 `Type` 实现 `Trait`，使用 `impl Trait for Type { .. }` 块。
>
> - 与 Go 的接口不同：仅仅方法签名匹配还不够——带 `talk()` 方法的 `Cat` 类型不会自动满足 `Pet`，除非写在 `impl Pet` 块中。
>
> - Trait 可以为部分方法提供默认实现。默认实现可以依赖该 trait 的所有方法。本例中提供了 `greet`，它依赖 `talk`。
>
> - 同一类型允许有多个 `impl` 块，包括固有 `impl` 与 trait `impl`。同样，同一类型也可以实现多个 trait（而且类型常常实现许多 trait！）。`impl` 块甚至可以分散在多个模块/文件中。

