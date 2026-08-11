+++
title = "第14章 深入 Cargo 与 Crates.io"
date = 2026-08-05T08:44:00+08:00
weight = 61
type = "docs"
description = "介绍 Cargo 的发布配置、发布到 crates.io、工作空间、安装二进制与自定义命令"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 深入 Cargo 与 Crates.io {#more-about-cargo-and-crates-io}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch14-00-more-about-cargo.html](https://doc.rust-lang.org/stable/book/ch14-00-more-about-cargo.html)


　　到目前为止，我们只用了 Cargo 最基础的功能来构建、运行和测试代码，但它还能做更多事。本章会介绍一些更进阶的特性，帮助你完成这些工作：

- 通过发布配置（release profiles）自定义构建。
- 在 [crates.io](https://crates.io/) 上发布库。
- 用工作空间（workspaces）组织大型项目。
- 从 [crates.io](https://crates.io/) 安装二进制程序。
- 用自定义命令扩展 Cargo。

　　Cargo 能做的事比本章覆盖的还多；若要全面了解所有功能，请参阅 [Cargo 文档](https://doc.rust-lang.org/cargo/)。
