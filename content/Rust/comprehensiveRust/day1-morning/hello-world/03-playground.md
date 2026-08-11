+++
title = "2.3 在线演练场"
date = 2026-08-11T11:30:00+08:00
weight = 15
type = "docs"
description = "03-在线演练场 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/hello-world/playground.html](https://google.github.io/comprehensive-rust/hello-world/playground.html)

# 2.3 在线演练场

[Rust Playground](https://play.rust-lang.org/) 提供了便捷方式运行短小的 Rust 程序，
也是本课程示例与练习的基础。试着运行它默认打开的 “hello-world” 程序。它还带有一些实用功能：

- 在 “Tools”（工具）下，用 `rustfmt` 选项按“标准”方式格式化代码。

- Rust 生成代码有两个主要“配置文件”：Debug（额外运行时检查、较少优化）与
  Release（较少运行时检查、大量优化）。可在顶部的 “Debug” 处切换。

- 若感兴趣，可在 “...” 下用 “ASM” 查看生成的汇编代码。

> 学员进入休息时，鼓励他们打开 Playground 稍作尝试。鼓励他们把标签页开着，在课程其余时间
> 继续试验。这对想进一步了解 Rust 优化或生成汇编的进阶学员尤其有帮助。

