+++
title = "09-已弃用特性"
date = 2026-08-01T07:35:00+08:00
weight = 90
type = "docs"
description = "rustdoc 中已弃用的特性"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The rustdoc book](https://doc.rust-lang.org/rustdoc/)

# 已弃用特性 {#deprecated-features}


> 原文链接: [https://doc.rust-lang.org/rustdoc/deprecated-features.html](https://doc.rust-lang.org/rustdoc/deprecated-features.html)


## Passes {#passes}

Rustdoc 有一个称为 “passes” 的概念。它们是 `rustdoc` 在生成最终输出之前对文档执行的变换。

自定义 passes **已弃用**。可用的 passes 不视为稳定，可能在任何发行版中变更。

过去，自定义 passes 最常见的用途是省略 `strip-private` pass。
现在可以更简单地做到这一点，且不必担心 pass 变更，方法是传入 [`--document-private-items`](02-command-line-arguments/#--document-private-items-show-items-that-are-not-public)。
