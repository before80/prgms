+++
title = "8.4 生成 `gn` 构建规则"
date = 2026-08-11T11:30:00+08:00
weight = 282
type = "docs"
description = "04-生成 `gn` 构建规则 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/generating-gn-build-rules.html](https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/generating-gn-build-rules.html)

# 8.4 生成 `gn` 构建规则

下载 crate 后，像这样生成 `BUILD.gn` 文件：

```shell
vpython3 tools/crates/run_gnrt.py -- gen
```

现在运行 `git status`。你应会发现：

- 在 `third_party/rust/chromium_crates_io/vendor` 中至少有一个新的 crate 源码
- 在 `third_party/rust/<crate name>/v<major semver version>` 中至少有一个新的 `BUILD.gn`
- 一个合适的 `README.chromium`

“major semver version” 是一个 [Rust “semver” 版本号][0]。

仔细查看，尤其是 `third_party/rust` 中生成的内容。

> 稍微讲一下 semver——具体来说，在 Chromium 中它是为了允许多个不兼容版本的 crate，这在 Cargo 生态中不鼓励但有时必要。


[0]: https://doc.rust-lang.org/cargo/reference/semver.html
