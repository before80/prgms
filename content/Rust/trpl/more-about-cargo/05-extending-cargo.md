+++
title = "14.5 用自定义命令扩展 Cargo"
date = 2026-08-05T08:44:00+08:00
weight = 66
type = "docs"
description = "通过 cargo-* 可执行文件扩展 Cargo，并小结本章"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用自定义命令扩展 Cargo {#cargo}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch14-05-extending-cargo.html](https://doc.rust-lang.org/stable/book/ch14-05-extending-cargo.html)


## 用自定义命令扩展 Cargo

　　Cargo 的设计允许你在不修改它本身的情况下，用新的子命令扩展它。若 `$PATH` 中有一个名为 `cargo-something` 的二进制，你就可以像使用 Cargo 子命令一样运行 `cargo something`。这类自定义命令也会出现在 `cargo --list` 的列表里。能够用 `cargo install` 安装扩展，再像内置 Cargo 工具一样调用它们，正是 Cargo 设计带来的一大便利！

## 小结

　　借助 Cargo 与 [crates.io](https://crates.io/) 分享代码，是 Rust 生态能胜任众多不同任务的原因之一。Rust 的标准库小而稳定，但 crate 易于分享、使用，并可以按不同于语言本身的节奏持续改进。若某段代码对你有用，不妨大胆把它发布到 [crates.io](https://crates.io/)——它很可能对别人同样有用！
