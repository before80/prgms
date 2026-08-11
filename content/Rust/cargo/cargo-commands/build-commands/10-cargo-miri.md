+++
title = "10-cargo miri"
date = 2026-07-30T14:49:00+08:00
weight = 55
type = "docs"
description = "cargo-miri(1) 用 Miri 解释执行"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-miri(1) {#cargo-miri1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-miri.html](https://doc.rust-lang.org/cargo/commands/cargo-miri.html)


## 名称 {#name}
cargo-miri --- 在 Miri 中运行二进制 crate 与测试

## 描述 {#description}
这是随 Rust 工具链分发的可选组件中的外部命令。
它并非内置于 Cargo，可能需要额外安装。

此命令仅在 [nightly](https://doc.rust-lang.org/book/appendix-07-nightly-rust.html) 通道可用。

关于用法与安装，请参阅 <https://github.com/rust-lang/miri>。

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/)、
[cargo-run(1)](../11-cargo-run/)、
[cargo-test(1)](../14-cargo-test/)、
[自定义子命令](../../../cargo-reference/11-external-tools/#custom-subcommands)
