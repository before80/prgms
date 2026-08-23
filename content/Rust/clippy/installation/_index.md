+++
title = "01-安装"
date = 2026-08-22T18:00:00+08:00
weight = 10
type = "docs"
description = "安装 Clippy（rustup 或源码）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 安装 {#installation}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/installation.html](https://doc.rust-lang.org/nightly/clippy/installation.html)


如果你使用 `rustup` 安装和管理 Rust 工具链，Clippy 通常**已经安装**。此时可跳过本章，直接阅读[用法](/clippy/usage/)一章。

> 注意：若安装 Rust 工具链时使用了 `minimal` profile，Clippy 不会自动安装。

## 使用 Rustup

若某工具链未安装 Clippy，可用以下命令安装：

```
$ rustup component add clippy [--toolchain=<name>]
```

## 从源码安装

请参阅 Clippy 开发者指南中的[基础](/clippy/development/01-basics/#install-from-source)一章，按步骤从源码构建并安装 Clippy。

[基础]: /clippy/development/01-basics/#install-from-source
[用法]: /clippy/usage/