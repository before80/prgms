+++
title = "8.9 保持 Crate 更新"
date = 2026-08-11T11:30:00+08:00
weight = 289
type = "docs"
description = "08-保持 Crate 更新 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/keeping-up-to-date.html](https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/keeping-up-to-date.html)

# 8.9 保持 Crate 更新

作为任何第三方 Chromium 依赖的 OWNER，你被[要求用任何安全修复保持其更新][0]。希望我们很快能为 Rust crate 自动化这一点，但目前，这仍是你的责任，就像对任何其他第三方依赖一样。

[0]: https://chromium.googlesource.com/chromium/src/+/main/docs/adding_to_third_party.md#add-owners
