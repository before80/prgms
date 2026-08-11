+++
title = "第6章 枚举与模式匹配"
date = 2026-08-05T08:44:00+08:00
weight = 23
type = "docs"
description = "枚举与模式匹配：用枚举表达一组可能取值并用 match 处理"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 枚举与模式匹配 {#enums-and-pattern-matching}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch06-00-enums.html](https://doc.rust-lang.org/stable/book/ch06-00-enums.html)


　　本章我们来看枚举（enumeration），通常简称为 *enum*。枚举允许你通过列出所有可能的变体（variant）来定义一个类型。首先，我们会定义并使用一个枚举，展示它如何把含义与数据编码在一起。接着会探讨特别有用的 `Option` 枚举，它表示一个值可能有、也可能没有。然后会看 `match` 表达式中的模式匹配如何让你为枚举的不同取值轻松运行不同代码。最后会介绍 `if let` 语法，它是处理枚举时另一种便捷、简洁的惯用法。
