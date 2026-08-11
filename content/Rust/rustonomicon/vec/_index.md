+++
title = "第9章 实现 Vec"
date = 2026-08-06T17:08:00+08:00
weight = 42
type = "docs"
description = "从零实现 Vec 的教程"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 实现 Vec


> 原文链接: [https://doc.rust-lang.org/nomicon/vec/vec.html](https://doc.rust-lang.org/nomicon/vec/vec.html)


　　为把一切串联起来，我们将从零编写 `std::Vec`。我们限定在稳定 Rust 内。尤其不会使用任何本可让代码略好或更高效的 intrinsics，因为 intrinsics 永久不稳定。尽管许多 intrinsics 会在别处稳定（`std::ptr` 和 `std::mem` 就包含许多 intrinsics）。

　　最终这意味着我们的实现可能无法利用所有可能的优化，但绝不算*幼稚*。我们肯定会深入细枝末节，即便问题*并不*真的需要如此。

　　你想要进阶内容。我们就来进阶。
