+++
title = "8.8 检入 Chromium 源码"
date = 2026-08-11T11:30:00+08:00
weight = 288
type = "docs"
description = "07-检入 Chromium 源码 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/checking-in.html](https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/checking-in.html)

# 8.8 检入 Chromium 源码

`git status` 应会显示：

- `//third_party/rust/chromium_crates_io` 中的 crate 代码
- `//third_party/rust/<crate>/<version>` 中的元数据（`BUILD.gn` 与 `README.chromium`）

请也在后一位置添加一个 `OWNERS` 文件。

你应把所有这些，连同你的 `Cargo.toml` 与 `gnrt_config.toml` 变更，一起提交进 Chromium 仓库。

**重要：** 你需要使用 `git add -f`，否则 `.gitignore` 文件可能导致一些文件被跳过。

这样做时，你可能发现预提交检查因非包容性语言而失败。这是因为 Rust crate 数据往往包含 git 分支名，而许多项目在那里仍使用非包容术语。因此你可能需要运行：

```shell
infra/update_inclusive_language_presubmit_exempt_dirs.sh > infra/inclusive_language_presubmit_exempt_dirs.txt
git add -p infra/inclusive_language_presubmit_exempt_dirs.txt # 添加属于你的变更
```
