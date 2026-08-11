+++
title = "02-Cargo 入门第一步"
date = 2026-07-30T14:49:00+08:00
weight = 12
type = "docs"
description = "用 Cargo 创建、构建与运行第一个包"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# Cargo 入门第一步 {#first-steps-with-cargo}


> 原文链接: [https://doc.rust-lang.org/cargo/getting-started/first-steps.html](https://doc.rust-lang.org/cargo/getting-started/first-steps.html)


本节让你快速感受一下 `cargo` 命令行工具。我们会演示它如何为我们生成一个新的[***包（package）***][def-package]、如何编译包内的 [***crate***][def-crate]，以及如何运行生成的程序。

要用 Cargo 开始一个新包，使用 `cargo new`：

```console
$ cargo new hello_world
```

Cargo 默认使用 `--bin` 来创建二进制程序。若要创建库，则应传入 `--lib`。

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

这些就足以开始了。首先看看 `Cargo.toml`：

```toml
[package]
name = "hello_world"
version = "0.1.0"
edition = "2024"

[dependencies]
```

这称为[***清单（manifest）***][def-manifest]，其中包含 Cargo 编译你的包所需的全部元数据。

`src/main.rs` 中的内容如下：

```rust
fn main() {
    println!("Hello, world!");
}
```

Cargo 为我们生成了一个 “hello world” 程序，也就是一个[***二进制 crate***][def-crate]。来编译它：

```console
$ cargo build
   Compiling hello_world v0.1.0 (file:///path/to/package/hello_world)
```

然后运行它：

```console
$ ./target/debug/hello_world
Hello, world!
```

也可以用 `cargo run` 一步完成编译并运行：

```console
$ cargo run
     Fresh hello_world v0.1.0 (file:///path/to/package/hello_world)
   Running `target/hello_world`
Hello, world!
```

## 进一步了解 {#going-further}
关于使用 Cargo 的更多细节，请参阅 [Cargo 指南](../../cargo-guide/)

[def-crate]:     ../../appendix/01-glossary/#crate     '"crate" (glossary entry)'
[def-manifest]:  ../../appendix/01-glossary/#manifest  '"manifest" (glossary entry)'
[def-package]:   ../../appendix/01-glossary/#package   '"package" (glossary entry)'
