+++
title = "3.3 派生"
date = 2026-08-11T11:30:00+08:00
weight = 82
type = "docs"
description = "02-派生 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/methods-and-traits/deriving.html](https://google.github.io/comprehensive-rust/methods-and-traits/deriving.html)

# 3.3 派生

对受支持的 trait，可以自动为自定义类型实现，如下：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug, Clone, Default)]
struct Player {
    name: String,
    strength: u8,
    hit_points: u8,
}

fn main() {
    let p1 = Player::default(); // Default trait 增加 `default` 构造函数。
    let mut p2 = p1.clone(); // Clone trait 增加 `clone` 方法。
    p2.name = String::from("EldurScrollz");
    // Debug trait 增加用 `{:?}` 打印的支持。
    println!("{p1:?} vs. {p2:?}");
}
```

> - 派生通过宏实现，许多 crate 提供有用的 derive 宏来增加实用功能。例如，`serde` 可用 `#[derive(Serialize)]` 为结构体派生序列化支持。
>
> - 派生通常用于那些有常见样板实现、且在大多数情况下正确的 trait。例如，演示手动实现 `Clone` 相比派生有多啰嗦：
>
>   ```rust
>   // Copyright 2023 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   impl Clone for Player {
>       fn clone(&self) -> Self {
>           Player {
>               name: self.name.clone(),
>               strength: self.strength.clone(),
>               hit_points: self.hit_points.clone(),
>           }
>       }
>   }
>   ```
>
>   本例中并非所有 `.clone()` 都必要，但这演示了手动实现通常会遵循的样板模式，有助于让学员理解为何使用 `derive`。

