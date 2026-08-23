+++
title = "4 dyn Trait 概览"
date = 2026-08-23T10:16:00+08:00
weight = 63
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Learning Rust](https://quinedot.github.io/rust-learning/)

# dyn Trait 概览 {#dyn-trait}


> 原文链接: [https://quinedot.github.io/rust-learning/dyn-trait.html](https://quinedot.github.io/rust-learning/dyn-trait.html)


Rust 的类型擦除 `dyn Trait` 提供了一种方式，可以在保持严格、静态（即编译时）类型检查的同时，以统一的方式处理 trait 的不同实现类型。例如：如果你想要一个 `Vec`，其中存放实现了某个 trait 的值，但它们的基础类型可能各不相同，就需要类型擦除，这样才能创建 `Vec<Box<dyn Trait>>` 或类似结构。

`dyn Trait` 在某些不希望使用泛型的场景下也很有用，或者用于将不可命名的类型（如闭包和（大多数）future）擦除为需要命名的类型（例如字段类型或关联类型）。

关于何时以及 `dyn Trait` 如何生效或不生效，以及这与泛型、生命周期和 Rust 类型系统的整体关系，需要了解的内容很多。因此，在学习 Rust 时对 `dyn Trait` 感到有些困惑并不罕见。

在本节中，我们将探讨 `dyn Trait` 是什么、不是什么，使用它的限制，它与泛型和不透明类型的关系，以及更多内容。
