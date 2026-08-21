+++
title = "10-导出"
date = 2026-08-17T22:00:00+08:00
weight = 117
type = "docs"
description = "导出 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/115_zh-cn.html](https://tourofrust.com/115_zh-cn.html)

# 导出

默认情况下，*模块*的成员不能从模块外部访问（甚至它的子模块也不行！）。 我们可以使用 `pub` 关键字使一个模块的成员可以从外部访问。

默认情况下，*crate* 中的成员无法从当前 crate 之外访问。我们可以通过在根模块中 (`lib.rs` 或 `main.rs`)， 将成员标记为 `pub` 使它们可以访问。
