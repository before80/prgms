+++
title = "7.2.6 共享枚举"
date = 2026-08-11T11:30:00+08:00
weight = 247
type = "docs"
description = "06-共享枚举 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/cpp/shared-enums.html](https://google.github.io/comprehensive-rust/android/interoperability/cpp/shared-enums.html)

# 7.2.6 共享枚举

```rust,ignore
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[cxx::bridge]
mod ffi {
    enum Suit {
        Clubs,
        Diamonds,
        Hearts,
        Spades,
    }
}
```

生成的 Rust：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Copy, Clone, PartialEq, Eq)]
#[repr(transparent)]
pub struct Suit {
    pub repr: u8,
}

#[allow(non_upper_case_globals)]
impl Suit {
    pub const Clubs: Self = Suit { repr: 0 };
    pub const Diamonds: Self = Suit { repr: 1 };
    pub const Hearts: Self = Suit { repr: 2 };
    pub const Spades: Self = Suit { repr: 3 };
}
```

生成的 C++：

```c++
enum class Suit : uint8_t {
  Clubs = 0,
  Diamonds = 1,
  Hearts = 2,
  Spades = 3,
};
```

> - 在 Rust 一侧，为共享枚举生成的代码实际上是包装数值的结构体。这是因为在 C++ 中，enum class 持有与所有列出变体不同的值并不是 UB，而我们的 Rust 表示需要有相同行为。

