+++
title = "1 Rust 生态"
date = 2026-08-11T11:30:00+08:00
weight = 7
type = "docs"
description = "01-Rust 生态 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/cargo/rust-ecosystem.html](https://google.github.io/comprehensive-rust/cargo/rust-ecosystem.html)

# 1 Rust 生态

Rust 生态由多种工具组成，其中主要有：

- `rustc`：Rust 编译器，把 `.rs` 文件变成二进制以及其他中间格式。

- `cargo`：Rust 依赖管理与构建工具。Cargo 知道如何下载依赖（通常托管在 <https://crates.io>），并在构建项目时把它们交给 `rustc`。Cargo 还内置测试运行器，用于执行单元测试。

- `rustup`：Rust 工具链安装与更新器。新版本 Rust 发布时，用它安装并更新 `rustc` 与 `cargo`。此外，`rustup` 也能下载标准库文档。你可以同时安装多个 Rust 版本，并按需用 `rustup` 切换。

> 要点：
>
> - Rust 发布节奏很快，约每六周一个新版本。新版本对旧版本保持向后兼容——同时引入新功能。
>
> - 有三个发布通道（release channel）：「stable」「beta」和「nightly」。
>
> - 新功能在「nightly」上试验；「beta」每六周会成为「stable」。
>
> - 依赖也可从备用[注册表（registries）][registries]、git、本地目录等解析。
>
> - Rust 还有[版本（editions）][editions]：当前版本是 Rust 2024。此前有 Rust 2015、Rust 2018 和 Rust 2021。
>
>   - 版本允许对语言做向后不兼容的变更。
>
>   - 为避免破坏现有代码，版本采用显式选择：通过 `Cargo.toml` 为你的 crate 指定版本。
>
>   - 为避免撕裂生态，Rust 编译器可以混用为不同版本编写的代码。
>
>   - 说明：不经过 `cargo` 而直接使用编译器相当少见（多数用户从不这样做）。
>
>   - 不妨提一下：Cargo 本身极为强大且全面，支持许多高级能力，包括但不限于：
>     - 项目/包结构
>     - [工作区（workspaces）][workspaces]
>     - 开发依赖与运行时依赖的管理/缓存
>     - [构建脚本（build scripting）][build scripting]
>     - [全局安装][global installation]
>     - 还可通过子命令插件扩展（例如
>       [cargo clippy]）。
>   - 更多内容见[官方 Cargo Book][official Cargo Book]
>
> [editions]: https://doc.rust-lang.org/edition-guide/
> [workspaces]: https://doc.rust-lang.org/cargo/reference/workspaces.html
> [build scripting]: https://doc.rust-lang.org/cargo/reference/build-scripts.html
> [global installation]: https://doc.rust-lang.org/cargo/commands/cargo-install.html
> [cargo clippy]: https://github.com/rust-lang/rust-clippy
> [official Cargo Book]: https://doc.rust-lang.org/cargo/
> [registries]: https://doc.rust-lang.org/cargo/reference/registries.html

