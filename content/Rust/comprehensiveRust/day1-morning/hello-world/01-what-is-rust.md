+++
title = "2.1 什么是 Rust？"
date = 2026-08-11T11:30:00+08:00
weight = 13
type = "docs"
description = "01-什么是 Rust？ — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/hello-world/what-is-rust.html](https://google.github.io/comprehensive-rust/hello-world/what-is-rust.html)

# 2.1 什么是 Rust？

Rust 是一门较新的编程语言，[于 2015 年发布 1.0][1]：

- Rust 是静态编译语言，定位与 C++ 类似
  - `rustc` 以 LLVM 作为后端。
- Rust 支持众多
  [平台与架构](https://doc.rust-lang.org/nightly/rustc/platform-support.html)：
  - x86、ARM、WebAssembly 等
  - Linux、Mac、Windows 等
- Rust 用于广泛的设备：
  - 固件与引导加载程序，
  - 智能显示设备，
  - 手机，
  - 桌面端，
  - 服务器。

> Rust 与 C++ 处于同一领域：
>
> - 高度灵活。
> - 高度可控。
> - 可缩放到微控制器等资源极度受限的设备。
> - 没有运行时或垃圾回收。
> - 在不牺牲性能的前提下，聚焦可靠性与安全性。


[1]: https://blog.rust-lang.org/2015/05/15/Rust-1.0.html
