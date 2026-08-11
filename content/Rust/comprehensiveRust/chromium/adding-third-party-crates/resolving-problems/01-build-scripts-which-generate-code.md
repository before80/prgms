+++
title = "8.5.1 生成代码的构建脚本"
date = 2026-08-11T11:30:00+08:00
weight = 284
type = "docs"
description = "01-生成代码的构建脚本 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/resolving-problems/build-scripts-which-generate-code.html](https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/resolving-problems/build-scripts-which-generate-code.html)

# 8.5.1 生成代码的构建脚本

若 `ninja` 抱怨缺少文件，检查 `build.rs` 看它是否写入源码文件。

如果是，修改 [`gnrt_config.toml`][1]，为该 crate 添加 `build-script-outputs`。若这是传递依赖，即 Chromium 代码不应直接依赖的依赖，还要添加 `allow-first-party-usage=false`。该文件中已有若干示例：

```toml
[crate.unicode-linebreak]
allow-first-party-usage = false
build-script-outputs = ["tables.rs"]
```

现在重新运行 [`gnrt.py -- gen`][2] 以重新生成 `BUILD.gn` 文件，告知 ninja 该特定输出文件是后续构建步骤的输入。

[1]: ../02-configuring-gnrt-config-toml/
[2]: ../04-generating-gn-build-rules/
