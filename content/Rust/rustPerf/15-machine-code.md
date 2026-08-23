+++
title = "15 机器码"
date = 2026-08-23T13:57:00+08:00
weight = 16
type = "docs"
description = "查看生成的汇编"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Rust Performance Book](https://nnethercote.github.io/perf-book/)

# 机器码 {#machine-code}


> 原文链接: [https://nnethercote.github.io/perf-book/machine-code.html](https://nnethercote.github.io/perf-book/machine-code.html)


当有一小段非常热点的代码时，值得检查生成的机器码是否存在低效之处，例如可消除的[边界检查]。[Compiler Explorer] 网站是检查小段代码时的极佳资源。[`cargo-show-asm`] 是可用于完整 Rust 项目的替代工具。

[边界检查]: ../11-bounds-checks/
[Compiler Explorer]: https://godbolt.org/
[`cargo-show-asm`]: https://github.com/pacak/cargo-show-asm

相关地，[`core::arch`] 模块提供对架构相关内建函数（intrinsics）的访问，其中许多与 SIMD 指令有关。

[`core::arch`]: https://doc.rust-lang.org/core/arch/index.html
