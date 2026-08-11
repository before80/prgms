+++
title = "02-创建新包"
date = 2026-07-30T14:49:00+08:00
weight = 22
type = "docs"
description = "使用 cargo new / init 创建新包"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 创建新包 {#creating-a-new-package}


> 原文链接: [https://doc.rust-lang.org/cargo/guide/creating-a-new-project.html](https://doc.rust-lang.org/cargo/guide/creating-a-new-project.html)


要用 Cargo 开始一个新[包][def-package]，使用 `cargo new`：

```console
$ cargo new hello_world --bin
```

我们传入 `--bin` 是因为在创建二进制程序：若创建库，则应传入 `--lib`。默认情况下这也会初始化一个新的 `git` 仓库。若不希望如此，请传入 `--vcs none`。

来看看 Cargo 为我们生成了什么：

```console
$ cd hello_world
$ tree .
.
├── Cargo.toml
└── src
    └── main.rs

1 directory, 2 files
```

再仔细看看 `Cargo.toml`：

```toml
[package]
name = "hello_world"
version = "0.1.0"
edition = "2024"

[dependencies]

```

这称为[***清单（manifest）***][def-manifest]，其中包含 Cargo 编译你的包所需的全部元数据。该文件以 [TOML] 格式编写（发音为 /tɑməl/）。

`src/main.rs` 中的内容如下：

```rust
fn main() {
    println!("Hello, world!");
}
```

Cargo 为你生成了一个 “hello world” 程序，也就是一个[*二进制 crate*][def-crate]。来编译它：

```console
$ cargo build
   Compiling hello_world v0.1.0 (file:///path/to/package/hello_world)
```

然后运行它：

```console
$ ./target/debug/hello_world
Hello, world!
```

也可以用 `cargo run` 一步完成编译并运行（若自上次编译后没有任何改动，你不会看到 `Compiling` 那一行）：

```console
$ cargo run
   Compiling hello_world v0.1.0 (file:///path/to/package/hello_world)
     Running `target/debug/hello_world`
Hello, world!
```

现在你会注意到一个新文件 `Cargo.lock`。它包含关于依赖的信息。由于目前还没有任何依赖，它并不太有趣。

准备好发布时，可以使用 `cargo build --release` 打开优化来编译文件：

```console
$ cargo build --release
   Compiling hello_world v0.1.0 (file:///path/to/package/hello_world)
```

`cargo build --release` 会把生成的二进制文件放在 `target/release` 而不是 `target/debug`。

调试模式编译是开发时的默认选择。由于编译器不做优化，编译时间更短，但代码运行更慢。发布模式编译更久，但代码运行更快。

[TOML]: https://toml.io/
[def-crate]:     ../../appendix/01-glossary/#crate     '"crate" (glossary entry)'
[def-manifest]:  ../../appendix/01-glossary/#manifest  '"manifest" (glossary entry)'
[def-package]:   ../../appendix/01-glossary/#package   '"package" (glossary entry)'
