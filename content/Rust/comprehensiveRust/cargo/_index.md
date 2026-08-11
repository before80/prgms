+++
title = "使用 Cargo"
date = 2026-08-11T11:30:00+08:00
weight = 6
type = "docs"
description = "使用 Cargo — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/cargo.html](https://google.github.io/comprehensive-rust/cargo.html)

# 使用 Cargo

当你开始了解 Rust 时，很快就会遇到
[Cargo](https://doc.rust-lang.org/cargo/)——Rust 生态中用于构建与运行 Rust 应用的标准工具。这里简要说明 Cargo 是什么、它在更广泛生态中的位置，以及它在本培训中的角色。

## 安装

> **请按 <https://rustup.rs/> 上的说明操作。**

完成后你会得到构建工具 Cargo（`cargo`）与 Rust 编译器（`rustc`）。还会得到 `rustup`，一个可用来安装不同编译器版本的命令行工具。

安装 Rust 后，应配置编辑器或 IDE 以支持 Rust。多数编辑器通过与 [rust-analyzer] 通信来实现这一点，它为 [VS Code]、[Emacs]、[Vim/Neovim] 等提供自动补全与跳转到定义。另有一款不同的 IDE 名为 [RustRover]。

> - 在 Debian/Ubuntu 上，可通过 `apt` 安装 `rustup`：
>
>   ```shell
>   sudo apt install rustup
>   ```
>
> - 在 macOS 上可用 [Homebrew](https://brew.sh/) 安装 Rust，但版本可能偏旧。因此建议从官网安装。


[rust-analyzer]: https://rust-analyzer.github.io/
[VS Code]: https://code.visualstudio.com/
[Emacs]: https://rust-analyzer.github.io/manual.html#emacs
[Vim/Neovim]: https://rust-analyzer.github.io/manual.html#vimneovim
[RustRover]: https://www.jetbrains.com/rust/
[Rust formatter]: https://github.com/rust-lang/rustfmt
