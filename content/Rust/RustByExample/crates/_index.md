+++
title = "第11章 crate"
date = 2026-08-20T21:20:00+08:00
weight = 74
type = "docs"
description = "crate — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/crates.html](https://doc.rust-lang.org/stable/rust-by-example/crates.html)

# crate

crate（中文有 “包，包装箱” 之意）是 Rust 的编译单元。当调用 `rustc some_file.rs`
 时，`some_file.rs` 被当作 **crate 文件**。如果 `some_file.rs` 里面含有 `mod`
 声明，那么模块文件的内容将在编译之前被插入 crate 文件的相应声明处。换句话说，模块**不会**单独被编译，只有 crate 才会被编译。

crate 可以编译成二进制可执行文件（binary）或库文件（library）。默认情况下，`rustc` 将从 crate 产生二进制可执行文件。这种行为可以通过 `rustc` 的选项 `--crate-type`
 重载。
