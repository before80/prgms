+++
title = "2 环境准备"
date = 2026-08-11T11:30:00+08:00
weight = 499
type = "docs"
description = "02-环境准备 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/setup.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/setup.html)

# 2 环境准备

## 本地 Rust 安装

你应已安装支持 Rust 2024 edition 的编译器，即任何高于 1.84 的 rustc 版本。

```console
$ rustc --version 
rustc 1.87
```

## （可选）在本地创建课程副本

```console
$ git clone --depth=1 https://github.com/google/comprehensive-rust.git
Cloning into 'comprehensive-rust'...
...
$ cd comprehensive-rust
$ cargo install-tools
...
$ cargo serve # then open http://127.0.0.1:3000/ in a browser
```

> 请确认每位学员都能执行 `rustc`，且版本高于 1.87。
>
> 对于尚未满足条件的人，告知他们我们会在休息期间解决。

