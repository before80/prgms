+++
title = "01-为什么需要 Cargo"
date = 2026-07-30T14:49:00+08:00
weight = 21
type = "docs"
description = "Cargo 解决的问题与存在的理由"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 为什么需要 Cargo {#why-cargo-exists}


> 原文链接: [https://doc.rust-lang.org/cargo/guide/why-cargo-exists.html](https://doc.rust-lang.org/cargo/guide/why-cargo-exists.html)


## 预备知识 {#preliminaries}
在 Rust 中，你可能已经知道，库或可执行程序称为 [*crate*][def-crate]。Crate 由 Rust 编译器 `rustc` 编译。刚开始学 Rust 时，大多数人最先接触到的源码是经典的 “hello world” 程序，并直接调用 `rustc` 来编译：

```console
$ rustc hello.rs
$ ./hello
Hello, world!
```

请注意，上面的命令要求你显式指定文件名。若要用 `rustc` 直接编译另一个程序，就需要不同的命令行调用。若还需要指定特定的编译器标志或引入外部依赖，所需命令会更加具体（也更复杂）。

此外，大多数非平凡程序很可能依赖外部库，因而也会传递依赖那些库的依赖。若手工获取所有必要依赖的正确版本并保持更新，既困难又容易出错。

与其只跟 crate 和 `rustc` 打交道，你可以通过引入更高层的[“*包（package）*”][def-package]抽象，并使用[包管理器（package manager）][def-package-manager]，来避免上述任务带来的困难。

## 登场：Cargo {#enter-cargo}
*Cargo* 是 Rust 的包管理器。它是一个工具，让 Rust [*包*][def-package]能够声明各自的各种依赖，并确保你总能得到可重复的构建。

为实现这一目标，Cargo 做四件事：

* 引入两个包含各类包信息的元数据文件。
* 获取并构建包的依赖。
* 以正确的参数调用 `rustc` 或其他构建工具来构建你的包。
* 引入约定，让使用 Rust 包更轻松。

在很大程度上，Cargo 规范化了构建给定程序或库所需的命令；这正是上述约定的一个方面。如后文所示，同一条命令可用于构建不同的 [*产物（artifact）*][def-artifact]，而不论其名称如何。与其直接调用 `rustc`，你可以调用诸如 `cargo build` 这样的通用命令，让 Cargo 去构造正确的 `rustc` 调用。此外，Cargo 会自动从[*注册表（registry）*][def-registry]获取你为产物定义的任何依赖，并在需要时把它们加入构建。

可以说，一旦你知道如何构建一个基于 Cargo 的项目，你就知道如何构建*所有*这类项目——这并不夸张多少。

[def-artifact]:         ../../appendix/01-glossary/#artifact         '"artifact" (glossary entry)'
[def-crate]:            ../../appendix/01-glossary/#crate            '"crate" (glossary entry)'
[def-package]:          ../../appendix/01-glossary/#package          '"package" (glossary entry)'
[def-package-manager]:  ../../appendix/01-glossary/#package-manager  '"package manager" (glossary entry)'
[def-registry]:         ../../appendix/01-glossary/#registry         '"registry" (glossary entry)'
