+++
title = "03-Travis CI"
date = 2026-08-22T18:00:00+08:00
weight = 63
type = "docs"
description = "Travis CI 中运行 Clippy"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# Travis CI {#travis-ci}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/continuous_integration/travis.html](https://doc.rust-lang.org/nightly/clippy/continuous_integration/travis.html)


可以像在本地一样将 Clippy 添加到 Travis CI：

```yml
language: rust
rust:
  - stable
  - beta
before_script:
  - rustup component add clippy
script:
  - cargo clippy
  # 若希望构建任务在遇到警告时失败，使用
  - cargo clippy -- -D warnings
  # 若要同时检查测试和非默认 crate 特性，使用
  - cargo clippy --all-targets --all-features -- -D warnings
  - cargo test
  # 等等
```
