+++
title = "01-项目准备"
date = 2026-08-01T10:33:00+08:00
weight = 11
type = "docs"
description = "用 Cargo 创建 CLI 项目"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Command Line Applications in Rust](https://rust-cli.github.io/book/)

# 项目准备 {#project-setup}


> 原文链接: [https://rust-cli.github.io/book/tutorial/setup.html](https://rust-cli.github.io/book/tutorial/setup.html)


如果还没有，
先在电脑上[安装 Rust][install-rust]
（通常只要几分钟）。
然后打开终端，进入你打算存放
应用代码的目录。

[install-rust]: https://www.rust-lang.org/tools/install

在存放编程项目的目录里运行
`cargo new grrs`。
查看新创建的 `grrs` 目录，
你会看到典型的 Rust 项目布局：

- 一个 `Cargo.toml` 文件，包含项目元数据，
  以及我们使用的依赖/外部库列表。
- 一个 `src/main.rs` 文件，是（主）二进制的入口。

如果能在 `grrs` 目录里执行 `cargo run`
并看到 “Hello World”，就说明环境就绪了。

## 大概会是这样 {#what-it-might-look-like}

```console
$ cargo new grrs
     Created binary (application) `grrs` package
$ cd grrs/
$ cargo run
   Compiling grrs v0.1.0 (/Users/pascal/code/grrs)
    Finished dev [unoptimized + debuginfo] target(s) in 0.70s
     Running `target/debug/grrs`
Hello, world!
```
