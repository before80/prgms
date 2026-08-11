+++
title = "14.4 用 cargo install 安装二进制文件"
date = 2026-08-05T08:44:00+08:00
weight = 65
type = "docs"
description = "用 cargo install 从 crates.io 安装并使用二进制 crate"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用 cargo install 安装二进制文件 {#cargo-install}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch14-04-installing-binaries.html](https://doc.rust-lang.org/stable/book/ch14-04-installing-binaries.html)


## 用 `cargo install` 安装二进制文件

　　`cargo install` 命令可以在本地安装并使用二进制 crate。它并不打算取代系统包管理器，而是方便 Rust 开发者安装别人在 [crates.io](https://crates.io/) 上分享的工具。注意：只能安装带有二进制目标（binary target）的包。*二进制目标*是可运行的程序——当 crate 有 *src/main.rs*，或另有文件被指定为二进制时就会生成它；相对地，库目标本身不能单独运行，而是适合被其他程序引入。通常，README 会说明某个 crate 是库、带二进制目标，还是两者都有。

　　用 `cargo install` 安装的所有二进制都会放在安装根目录的 *bin* 文件夹里。若你用 *rustup.rs* 安装 Rust 且没有额外自定义配置，这个目录一般是 *$HOME/.cargo/bin*。请确保该目录在你的 `$PATH` 中，才能运行通过 `cargo install` 安装的程序。

　　例如，第 12 章提到过用 Rust 实现的文件搜索工具 `grep`，名为 `ripgrep`。安装 `ripgrep` 可以这样：


```console
$ cargo install ripgrep
    Updating crates.io index
  Downloaded ripgrep v14.1.1
  Downloaded 1 crate (213.6 KB) in 0.40s
  Installing ripgrep v14.1.1
--snip--
   Compiling grep v0.3.2
    Finished `release` profile [optimized + debuginfo] target(s) in 6.73s
  Installing ~/.cargo/bin/rg
   Installed package `ripgrep v14.1.1` (executable `rg`)
```

　　输出的倒数第二行给出了已安装二进制的位置与名称；对 `ripgrep` 来说就是 `rg`。只要安装目录已在 `$PATH` 中（如前所述），你就可以运行 `rg --help`，开始用这个更快、更有 Rust 味道的文件搜索工具了！
