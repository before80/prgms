+++
title = "01-模块"
date = 2026-08-17T22:00:00+08:00
weight = 108
type = "docs"
description = "模块 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/106_zh-cn.html](https://tourofrust.com/106_zh-cn.html)

# 模块

每个 Rust 程序或者库都叫 *crate*。

每个 crate 都是由*模块*的层次结构组成。

每个 crate 都有一个根模块。

模块里面可以有全局变量、全局函数、全局结构体、全局 Trait 甚至是全局模块！

在 Rust 中，文件与模块树的层次结构并不是一对一的映射关系。我们必须在我们的代码中手动构建模块树。
