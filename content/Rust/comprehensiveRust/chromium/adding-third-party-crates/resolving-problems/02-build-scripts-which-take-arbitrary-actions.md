+++
title = "8.5.2 构建 C++ 或执行任意操作的构建脚本"
date = 2026-08-11T11:30:00+08:00
weight = 285
type = "docs"
description = "02-构建 C++ 或执行任意操作的构建脚本 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/resolving-problems/build-scripts-which-take-arbitrary-actions.html](https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/resolving-problems/build-scripts-which-take-arbitrary-actions.html)

# 8.5.2 构建 C++ 或执行任意操作的构建脚本

有些 crate 使用 [`cc`][1] crate 来构建并链接 C/C++ 库。其他 crate 在其构建脚本中使用 [`bindgen`][2] 解析 C/C++。这些行为在 Chromium 环境中无法得到支持——我们的 gn、ninja 与 LLVM 构建系统在表达构建动作之间的关系方面非常具体。

因此，你的选项是：

- 避免这些 crate
- 对该 crate 打补丁。

补丁应保存在 `third_party/rust/chromium_crates_io/patches/<crate>`——例如见[对 `cxx` crate 的补丁][3]——并且每次 `gnrt` 升级该 crate 时会自动应用。

[1]: https://crates.io/crates/cc
[2]: https://crates.io/crates/bindgen
[3]: https://source.chromium.org/chromium/chromium/src/+/main:third_party/rust/chromium_crates_io/patches/cxx/
