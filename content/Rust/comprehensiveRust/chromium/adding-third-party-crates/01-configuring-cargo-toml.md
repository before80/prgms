+++
title = "8.1 配置 Cargo.toml"
date = 2026-08-11T11:30:00+08:00
weight = 279
type = "docs"
description = "01-配置 Cargo.toml — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/configuring-cargo-toml.html](https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/configuring-cargo-toml.html)

# 8.1 配置 Cargo.toml

Chromium 有一组集中管理的直接 crate 依赖。它们通过单个 [`Cargo.toml`][0] 管理：

```toml
[dependencies]
bitflags = "1"
cfg-if = "1"
cxx = "1"
# 还有很多……
```

与任何其他 `Cargo.toml` 一样，你可以[指定更多依赖细节][1]——通常，你会想指定希望在 crate 中启用的 `features`。

向 Chromium 添加 crate 时，你经常需要在另一个文件 `gnrt_config.toml` 中提供额外信息，我们接下来会见到它。

[0]: https://source.chromium.org/chromium/chromium/src/+/main:third_party/rust/chromium_crates_io/Cargo.toml
[1]: https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html
