+++
title = "3 在本地运行 Cargo"
date = 2026-08-11T11:30:00+08:00
weight = 9
type = "docs"
description = "03-在本地运行 Cargo — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/cargo/running-locally.html](https://google.github.io/comprehensive-rust/cargo/running-locally.html)

# 3 在本地运行 Cargo

若想在自己的系统上试验代码，需要先安装 Rust。请按
[《The Rust Book》中的说明][1] 操作。完成后应能使用 `rustc` 与
`cargo`。撰写本文时，最新稳定版 Rust 的版本号如下：

```shell
% rustc --version
rustc 1.69.0 (84c898d65 2023-04-16)
% cargo --version
cargo 1.69.0 (6e9a83356 2023-04-12)
```

也可以使用之后的任意版本，因为 Rust 保持向后兼容。

准备好后，按下列步骤把本培训中的示例构建为 Rust 二进制：

1. 在要复制的示例上点击「Copy to clipboard」按钮。

2. 用 `cargo new exercise` 创建新的 `exercise/` 目录存放代码：

   ```shell
   $ cargo new exercise
        Created binary (application) `exercise` package
   ```

3. 进入 `exercise/`，用 `cargo run` 构建并运行二进制：

   ```shell
   $ cd exercise
   $ cargo run
      Compiling exercise v0.1.0 (/home/mgeisler/tmp/exercise)
       Finished dev [unoptimized + debuginfo] target(s) in 0.75s
        Running `target/debug/exercise`
   Hello, world!
   ```

4. 用你自己的代码替换 `src/main.rs` 中的样板。例如，使用上一页的示例，让 `src/main.rs` 如下所示：

   ```rust
   // Copyright 2022 Google LLC
   // SPDX-License-Identifier: Apache-2.0
   #
   fn main() {
       println!("Edit me!");
   }
   ```

5. 用 `cargo run` 构建并运行更新后的二进制：

   ```shell
   $ cargo run
      Compiling exercise v0.1.0 (/home/mgeisler/tmp/exercise)
       Finished dev [unoptimized + debuginfo] target(s) in 0.24s
        Running `target/debug/exercise`
   Edit me!
   ```

6. 用 `cargo check` 快速检查项目错误，用 `cargo build`
   编译但不运行。普通 debug 构建的输出在 `target/debug/`。用 `cargo build --release` 可在 `target/release/` 生成优化后的 release 构建。

7. 可通过编辑 `Cargo.toml` 为项目添加依赖。运行 `cargo` 命令时，它会自动下载并编译缺失的依赖。

[1]: https://doc.rust-lang.org/book/ch01-01-installation.html

> 尽量鼓励学员安装 Cargo 并使用本地编辑器。这样他们会有正常的开发环境，使用更方便。

