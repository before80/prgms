+++
title = "6 测试"
date = 2026-08-11T11:30:00+08:00
weight = 265
type = "docs"
description = "测试 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/testing.html](https://google.github.io/comprehensive-rust/chromium/testing.html)

# 6 测试

Rust 社区通常把单元测试写在与被测代码同一源文件中的模块里。课程[前面](../../testing/)已介绍过，看起来像这样：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[cfg(test)]
mod tests {
    #[test]
    fn my_test() {
        todo!()
    }
}
```

在 Chromium 中我们把单元测试放在单独的源文件里，对 Rust 也继续遵循这一做法——这使测试能被一致地发现，并有助于避免以 `test` 配置第二次重建 `.rs` 文件。

因此在 Chromium 中测试 Rust 代码有以下选项：

- 原生 Rust 测试（即 `#[test]`）。除 `//third_party/rust` 外不鼓励使用。
- 用 C++ 编写并通过 FFI 调用行使 Rust 的 `gtest` 测试。当 Rust 代码只是薄 FFI 层、且现有单元测试已为该功能提供足够覆盖时足够。
- 用 Rust 编写并通过被测 crate 的公共 API 使用它的 `gtest` 测试（需要时使用 `pub mod for_testing { ... }`）。这是接下来几页的主题。

> 提到第三方 crate 的原生 Rust 测试最终应由 Chromium bot 运行。（这种测试很少需要——只在添加或更新第三方 crate 之后。）
>
> 一些例子可能有助于说明何时应使用 C++ `gtest` 与何时应使用 Rust `gtest`：
>
> - QR 在第一方 Rust 层几乎没有功能（只是薄 FFI 胶水），因此使用现有的 C++ 单元测试同时测试 C++ 与 Rust 实现（对测试参数化，以便用 `ScopedFeatureList` 启用或禁用 Rust）。
>
> - 假设/进行中的 PNG 集成可能需要 `libpng` 提供、但 `png` crate 缺失的内存安全像素变换实现——例如 RGBA => BGRA，或伽马校正。这类功能可能受益于用 Rust 编写的单独测试。

