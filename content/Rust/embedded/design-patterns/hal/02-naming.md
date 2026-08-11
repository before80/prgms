+++
title = "02-命名"
date = 2026-08-01T10:38:00+08:00
weight = 124
type = "docs"
description = "命名（Naming）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 命名 {#naming}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/design-patterns/hal/naming.html](https://doc.rust-lang.org/stable/embedded-book/design-patterns/hal/naming.html)


<a id="c-crate-name"></a>
## crate 命名恰当（C-CRATE-NAME） {#the-crate-is-named-appropriately-c-crate-name}

HAL crate 应以其所支持的芯片或芯片系列命名。名称应以 `-hal` 结尾，以便与寄存器访问 crate 区分。名称中不应包含下划线（请改用连字符）。
