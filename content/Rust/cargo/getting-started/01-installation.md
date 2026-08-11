+++
title = "01-安装"
date = 2026-07-30T14:49:00+08:00
weight = 11
type = "docs"
description = "使用 rustup 安装 Rust 与 Cargo，或从源码构建"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 安装 {#installation}


> 原文链接: [https://doc.rust-lang.org/cargo/getting-started/installation.html](https://doc.rust-lang.org/cargo/getting-started/installation.html)


## 安装 Rust 与 Cargo {#install-rust-and-cargo}
获取 Cargo 最简单的方式，是通过 [rustup] 安装当前的 [Rust] 稳定版发行版。使用 `rustup` 安装 Rust 时也会一并安装 `cargo`。

在 Linux 与 macOS 系统上，可以这样做：

```console
curl https://sh.rustup.rs -sSf | sh
```

它会下载一个脚本并开始安装。如果一切顺利，你会看到：

```console
Rust is installed now. Great!
```

在 Windows 上，下载并运行 [rustup-init.exe]。它会在控制台中开始安装，成功时会显示上面的消息。

之后，你还可以用 `rustup` 命令安装 Rust 与 Cargo 的 `beta` 或 `nightly` 通道。

关于其他安装选项与更多信息，请访问 Rust 网站的[安装][install-rust]页面。

## 从源码构建并安装 Cargo {#build-and-install-cargo-from-source}
或者，你也可以[从源码构建 Cargo][compiling-from-source]。

[rust]: https://www.rust-lang.org/
[rustup]: https://rustup.rs/
[rustup-init.exe]: https://win.rustup.rs/
[install-rust]: https://www.rust-lang.org/tools/install
[compiling-from-source]: https://github.com/rust-lang/cargo#compiling-from-source
