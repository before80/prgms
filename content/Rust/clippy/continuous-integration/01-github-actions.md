+++
title = "01-GitHub Actions"
date = 2026-08-22T18:00:00+08:00
weight = 61
type = "docs"
description = "GitHub Actions 中运行 Clippy"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# GitHub Actions {#github-actions}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/continuous_integration/github_actions.html](https://doc.rust-lang.org/nightly/clippy/continuous_integration/github_actions.html)


使用最新稳定版 Rust 的 GitHub 托管 runner 已预装 Clippy。
只需运行 `cargo clippy` 即可对代码库运行 lint。

```yml
on: push
name: Clippy check

# 确保 CI 在所有警告（包括 Clippy lint）上失败
env:
  RUSTFLAGS: "-Dwarnings"

jobs:
  clippy_check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - name: Run Clippy
        run: cargo clippy --all-targets --all-features
```
