+++
title = "8.7 审查与审计"
date = 2026-08-11T11:30:00+08:00
weight = 287
type = "docs"
description = "06-审查与审计 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/reviews-and-audits.html](https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/reviews-and-audits.html)

# 8.7 审查与审计

添加新库须遵守 Chromium 的标准[策略][0]，当然也须经过安全审查。由于你可能带来的不只是单个 crate，还有传递依赖，可能有大量代码需要审查。另一方面，安全的 Rust 代码负面副作用可能有限。你应如何审查它？

随着时间推移，Chromium 旨在转向基于 [cargo vet][1] 的流程。

与此同时，对每次新增 crate，我们在检查以下内容：

- 理解每个 crate 为何被使用。crate 之间是什么关系？若每个 crate 的构建系统包含 `build.rs` 或过程宏，弄清它们的用途。它们是否与 Chromium 通常的构建方式兼容？
- 检查每个 crate 看起来维护得是否合理
- 使用 `cd third-party/rust/chromium_crates_io; cargo audit` 检查已知漏洞（首先你需要 `cargo install cargo-audit`，讽刺的是这涉及从互联网下载大量依赖[2]）
- 确保任何 `unsafe` 代码对 [Rule of Two][3] 来说足够好
- 检查是否有任何对 `fs` 或 `net` API 的使用
- 以足够的层次阅读所有代码，寻找任何可能被恶意插入、看起来不对劲的东西。（你无法现实地追求 100% 完美：代码量往往太大。）

这些只是指南——与 `security@chromium.org` 的审查者合作，找出对 crate 建立信心的正确方法。

[0]: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/rust.md#Third_party-review
[1]: https://mozilla.github.io/cargo-vet/
[2]: ../03-cargo/
[3]: https://chromium.googlesource.com/chromium/src/+/main/docs/security/rule-of-2.md#unsafe-code-in-safe-languages
