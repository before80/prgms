+++
title = "8.3 下载 Crate"
date = 2026-08-11T11:30:00+08:00
weight = 281
type = "docs"
description = "03-下载 Crate — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/downloading-crates.html](https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/downloading-crates.html)

# 8.3 下载 Crate

名为 `gnrt` 的工具知道如何下载 crate 以及如何生成 `BUILD.gn` 规则。

首先，像这样下载你想要的 crate：

```shell
cd chromium/src
vpython3 tools/crates/run_gnrt.py -- vendor
```

> 虽然 `gnrt` 工具是 Chromium 源码的一部分，但运行此命令会从 `crates.io` 下载并运行其依赖。见[前面讨论这一安全决策的章节][0]。

该 `vendor` 命令可能下载：

- 你的 crate
- 直接与传递依赖
- 其他 crate 的新版本，这是 `cargo` 为解析 Chromium 所需的完整 crate 集合所要求的。

Chromium 为某些 crate 维护补丁，保存在 `//third_party/rust/chromium_crates_io/patches`。这些会自动重新应用，但若打补丁失败，你可能需要手工处理。

[0]: ../03-cargo/
