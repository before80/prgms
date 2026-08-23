+++
title = "02-GitLab CI"
date = 2026-08-22T18:00:00+08:00
weight = 62
type = "docs"
description = "GitLab CI 中运行 Clippy"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# GitLab CI {#gitlab-ci}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/continuous_integration/gitlab.html](https://doc.rust-lang.org/nightly/clippy/continuous_integration/gitlab.html)


可通过使用最新稳定版 [rust docker 镜像](https://hub.docker.com/_/rust) 将 Clippy 添加到 GitLab CI，
如下方 `.gitlab-ci.yml` CI 配置文件所示：

```yml
# 确保 CI 在所有警告（包括 Clippy lint）上失败
variables:
  RUSTFLAGS: "-Dwarnings"

clippy_check:
  image: rust:latest
  script:
    - rustup component add clippy
    - cargo clippy --all-targets --all-features
```
