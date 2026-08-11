+++
title = "01-HAL"
date = 2026-08-01T10:38:00+08:00
weight = 122
type = "docs"
description = "HAL（HALs）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# HAL 设计模式 {#hal-design-patterns}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/design-patterns/hal/](https://doc.rust-lang.org/stable/embedded-book/design-patterns/hal/)


这是一套在 Rust 中为微控制器编写硬件抽象层（HAL，Hardware Abstraction Layers）时常见且推荐的模式。编写微控制器 HAL 时，这些模式应作为现有 [Rust API 指南] 的补充使用。

[Rust API 指南]: https://rust-lang.github.io/api-guidelines/

[检查清单](01-checklist/)

- [命名](02-naming/)
- [互操作性](03-interoperability/)
- [可预测性](04-predictability/)
- [GPIO](05-gpio/)
