+++
title = "3-cargo-criterion"
date = 2026-08-22T20:00:00+08:00
weight = 24
type = "docs"
description = "cargo-criterion 子命令简介"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# cargo-criterion {#cargo-criterion}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/cargo_criterion/cargo_criterion.html](https://bheisler.github.io/criterion.rs/book/cargo_criterion/cargo_criterion.html)


cargo-criterion 是一个实验性的 Cargo 扩展，可作为 `cargo bench` 的替代品。cargo-criterion 的长期目标是在单一工具中处理所有统计分析和报告生成。这样，相关代码就可以从 Criterion.rs 中移除（或改为可选），从而减少基准测试的编译和链接时间。由于它管理基准测试运行的整个生命周期，`cargo-criterion` 也处于有利位置，能够提供在 Criterion.rs 本身中难以实现的功能。

目前，`cargo-criterion` 提供与在 `cargo bench` 中运行 Criterion.rs 基准测试时大部分相同的功能，但存在一些差异：
* `cargo-criterion` 目前不支持基线（baselines）
* `cargo-criterion` 比 Criterion.rs 更具可配置性
* `cargo-criterion` 支持使用 `--message-format=json` 输出机器可读格式

`cargo-criterion` 已趋于稳定，你可以使用以下命令安装：

`cargo install cargo-criterion`

安装后，可以使用以下命令运行基准测试：

`cargo criterion`

如果你遇到任何问题，或对未来的功能有建议，请在 [GitHub 仓库](https://github.com/bheisler/cargo-criterion) 提交 issue。
