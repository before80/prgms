+++
title = "8.5 解决问题"
date = 2026-08-11T11:30:00+08:00
weight = 283
type = "docs"
description = "解决问题 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/resolving-problems.html](https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates/resolving-problems.html)

# 8.5 解决问题

若构建失败，可能是因为 `build.rs`：在构建时做任意事情的程序。这从根本上与旨在使用静态、确定性构建规则以最大化并行度与构建可重复性的 `gn` 与 `ninja` 设计相冲突。

某些 `build.rs` 行为会被自动支持；其他则需要采取行动：

| build script 效果                                       | 我们的 gn 模板是否支持 | 你需要做的工作                       |
| ------------------------------------------------------- | ---------------------- | ------------------------------------ |
| 检查 rustc 版本以开关 features                          | 是                     | 无                                   |
| 检查平台或 CPU 以开关 features                          | 是                     | 无                                   |
| 生成代码                                                | 是                     | 是——在 `gnrt_config.toml` 中指定     |
| 构建 C/C++                                              | 否                     | 打补丁绕过                           |
| 任意其他行为                                            | 否                     | 打补丁绕过                           |

幸好，大多数 crate 不包含构建脚本，而且幸好，大多数构建脚本只做前两项。

[0]: https://doc.rust-lang.org/cargo/reference/build-scripts.html
