+++
title = "03-在已有包上工作"
date = 2026-07-30T14:49:00+08:00
weight = 23
type = "docs"
description = "检出、构建与运行已有 Cargo 项目"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 在已有 Cargo 包上工作 {#working-on-an-existing-cargo-package}


> 原文链接: [https://doc.rust-lang.org/cargo/guide/working-on-an-existing-project.html](https://doc.rust-lang.org/cargo/guide/working-on-an-existing-project.html)


如果你下载了一个使用 Cargo 的已有[包][def-package]，上手非常容易。

首先，从某处获取该包。本例中我们使用从 GitHub 仓库克隆的 `regex`：

```console
$ git clone https://github.com/rust-lang/regex.git
$ cd regex
```

要构建，使用 `cargo build`：

```console
$ cargo build
   Compiling regex v1.5.0 (file:///path/to/package/regex)
```

这会获取所有依赖，然后连同该包一起构建它们。

[def-package]:  ../../appendix/01-glossary/#package  '"package" (glossary entry)'
