+++
title = "8.2 配置 `gnrt_config.toml`"
date = 2026-08-11T11:30:00+08:00
weight = 280
type = "docs"
description = "02-配置 `gnrt_config.toml` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/configuring-gnrt-config-toml.html](https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/configuring-gnrt-config-toml.html)

# 8.2 配置 `gnrt_config.toml`

与 `Cargo.toml` 并列的是 [`gnrt_config.toml`][0]。它包含 Chromium 特有的 crate 处理扩展。

若你添加新 crate，至少应指定 `group`。它是以下之一：

```toml
#   'safe': 该库满足 rule-of-2，可在任何进程中使用。
#   'sandbox': 该库不满足 rule-of-2，必须在沙箱进程中使用，
#              例如渲染器或 utility 进程。
#   'test': 该库仅用于测试。
```

例如，

```toml
[crate.my-new-crate]
group = 'test' # 仅用于测试代码
```

取决于 crate 源码布局，你可能还需要用该文件指定在哪里可以找到其 `LICENSE` 文件。

稍后，我们会看到为解决一些问题，你需要在此文件中配置的其他事项。

[0]: https://source.chromium.org/chromium/chromium/src/+/main:third_party/rust/chromium_crates_io/gnrt_config.toml
