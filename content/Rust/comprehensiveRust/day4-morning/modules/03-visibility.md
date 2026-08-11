+++
title = "3.3 可见性"
date = 2026-08-11T11:30:00+08:00
weight = 173
type = "docs"
description = "03-可见性 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/modules/visibility.html](https://google.github.io/comprehensive-rust/modules/visibility.html)

# 3.3 可见性

模块是一道隐私边界：

- 模块中的项默认是私有的（隐藏实现细节）。
- 父模块与兄弟模块中的项始终可见。
- 换言之，若某个项在模块 `foo` 中可见，则在 `foo` 的所有后代模块中也可见。

```rust
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
mod outer {
    fn private() {
        println!("outer::private");
    }

    pub fn public() {
        println!("outer::public");
    }

    mod inner {
        fn private() {
            println!("outer::inner::private");
        }

        pub fn public() {
            println!("outer::inner::public");
            super::private();
        }
    }
}

fn main() {
    outer::public();
}
```

> - 使用 `pub` 关键字让模块变为公开。
>
> 此外，还有更高级的 `pub(...)` 说明符，可限制公开可见性的范围。
>
> - 参见
>   [Rust Reference](https://doc.rust-lang.org/reference/visibility-and-privacy.html#pubin-path-pubcrate-pubsuper-and-pubself)。
> - 配置 `pub(crate)` 可见性是常见模式。
> - 较少见地，也可以把可见性授予某个具体路径。
> - 无论如何，可见性必须授予某个祖先模块（及其所有后代）。

