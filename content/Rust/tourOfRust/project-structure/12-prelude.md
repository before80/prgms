+++
title = "12-Prelude"
date = 2026-08-17T22:00:00+08:00
weight = 119
type = "docs"
description = "Prelude — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/117_zh-cn.html](https://tourofrust.com/117_zh-cn.html)

# Prelude

你可能很好奇，为什么我们在没用 `use` 导入 `Vec` 或 `Box` 的情况下却可以到处使用它们。
这是因为标准库中有一个叫 `prelude` 的模块。

要知道，在 Rust 标准库中，以 `std::prelude::*` 导出的任何东西都会自动提供给 Rust 的各个部分。
`Vec` 和 `Box` 便是如此，并且其他东西（Option、Copy 等）也是如此。
