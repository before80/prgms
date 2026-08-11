+++
title = "8.6 依赖一个 Crate"
date = 2026-08-11T11:30:00+08:00
weight = 286
type = "docs"
description = "05-依赖一个 Crate — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/depending-on-a-crate.html](https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/depending-on-a-crate.html)

# 8.6 依赖一个 Crate

一旦你添加了第三方 crate 并生成了构建规则，依赖一个 crate 就很简单。找到你的 `rust_static_library` 目标，并添加对你的 crate 内 `:lib` 目标的 `dep`。

具体来说，

```bob
                     +------------+      +----------------------+
"//third_party/rust" | crate name | "/v" | major semver version | ":lib"
                     +------------+      +----------------------+
```

例如，

```gn
rust_static_library("my_rust_lib") {
  crate_root = "lib.rs"
  sources = [ "lib.rs" ]
  deps = [ "//third_party/rust/example_rust_crate/v1:lib" ]
}
```
