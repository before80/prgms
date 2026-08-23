+++
title = "4.7 dyn Trait 示例"
date = 2026-08-23T10:16:00+08:00
weight = 61
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Learning Rust](https://quinedot.github.io/rust-learning/)

# dyn Trait 示例 {#dyn-trait-examples}


> 原文链接: [https://quinedot.github.io/rust-learning/dyn-trait-examples.html](https://quinedot.github.io/rust-learning/dyn-trait-examples.html)


此处提供一些常见 `dyn Trait` 实现模式的「配方」。

在示例中，为简洁起见，我们通常使用 `dyn Trait`、`Box<dyn Trait>` 等。但请注意，在更实际的代码中，你很可能还需要为 `Box<dyn Trait + Send + Sync>` 或其他跨自动 trait 的变体提供实现。这可能替代对 `dyn Trait` 的实现（若你总是需要自动 trait 约束），也可能与之并存（以提供最大灵活性）。
