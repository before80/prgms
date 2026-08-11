+++
title = "7.1 包与 Crate"
date = 2026-08-05T08:44:00+08:00
weight = 28
type = "docs"
description = "理解 Cargo 包与二进制/库 crate 的关系与约定"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 包与 Crate {#crate}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch07-01-packages-and-crates.html](https://doc.rust-lang.org/stable/book/ch07-01-packages-and-crates.html)


## 包与 Crate

　　模块系统里我们先讲的部分是包（package）和 crate。

　　*Crate* 是 Rust 编译器一次会纳入考虑的最小代码量。即便你不用 `cargo` 而直接运行 `rustc`，并只传入一个源文件（就像我们在第 1 章[「Rust 程序基础」][basics]里做的那样），编译器也会把那个文件当作一个 crate。Crate 可以包含模块，这些模块也可以定义在其他会与该 crate 一同编译的文件里——后面几节会看到。

　　Crate 有两种形态：二进制 crate 或库 crate。*二进制 crate*（binary crate）可编译成能运行的可执行文件，例如命令行程序或服务器。每个二进制 crate 都必须有一个名为 `main` 的函数，定义可执行文件启动时发生什么。迄今为止我们创建的 crate 都是二进制 crate。

　　*库 crate*（library crate）没有 `main` 函数，也不会编译成可执行文件。它们定义的是供多个项目共享的功能。例如，我们在[第 2 章][rand]用过的 `rand` crate，就提供了生成随机数的能力。多数时候，Rustacean 说起「crate」时指的是库 crate，并且会把「crate」与一般编程概念里的「库（library）」互换使用。

　　*Crate 根*（crate root）是 Rust 编译器开始编译的源文件，也构成你这个 crate 的根模块（我们会在[「用模块控制作用域与私有性」][modules]中深入讲解模块）。

　　*包*（package）是一个或多个 crate 的集合，共同提供一组功能。包里包含一个描述如何构建这些 crate 的 *Cargo.toml* 文件。Cargo 本身其实也是一个包：它包含你一直用来构建代码的那个命令行工具的二进制 crate；同时，这个包还包含二进制 crate 所依赖的库 crate。其他项目也可以依赖 Cargo 的库 crate，从而复用与 Cargo 命令行工具相同的逻辑。

　　一个包可以包含任意数量的二进制 crate，但库 crate 最多只能有一个。包必须至少包含一个 crate，无论是库还是二进制 crate。

　　我们来走一遍创建包时会发生什么。首先输入命令 `cargo new my-project`：

```console
$ cargo new my-project
     Created binary (application) `my-project` package
$ ls my-project
Cargo.toml
src
$ ls my-project/src
main.rs
```

　　运行 `cargo new my-project` 之后，我们用 `ls` 查看 Cargo 创建了什么。在 *my-project* 目录里有一个 *Cargo.toml* 文件，这就给了我们一个包。还有一个 *src* 目录，其中有 *main.rs*。用编辑器打开 *Cargo.toml*，会发现里面并没有提到 *src/main.rs*。Cargo 遵循约定：*src/main.rs* 是与包同名的二进制 crate 的 crate 根。同样，若包目录里有 *src/lib.rs*，Cargo 就知道这个包包含一个与包同名的库 crate，且 *src/lib.rs* 是它的 crate 根。Cargo 会把这些 crate 根文件传给 `rustc` 来构建库或二进制程序。

　　这里，我们的包只有 *src/main.rs*，因此只包含一个名为 `my-project` 的二进制 crate。若一个包同时有 *src/main.rs* 和 *src/lib.rs*，它就有两个 crate：一个二进制、一个库，二者都与包同名。若要有多个二进制 crate，可以把文件放在 *src/bin* 目录下：每个文件都会成为一个独立的二进制 crate。

[basics]: /trpl/getting-started/02-hello-world/#rust-program-basics
[modules]: /trpl/modules/02-defining-modules-to-control-scope-and-privacy/
[rand]: /trpl/guessing-game/#generating-a-random-number
