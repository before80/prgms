+++
title = "11 边界检查"
date = 2026-08-23T13:57:00+08:00
weight = 12
type = "docs"
description = "减少边界检查开销"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Rust Performance Book](https://nnethercote.github.io/perf-book/)

# 边界检查 {#bounds-checks}


> 原文链接: [https://nnethercote.github.io/perf-book/bounds-checks.html](https://nnethercote.github.io/perf-book/bounds-checks.html)


默认情况下，Rust 中对切片、向量等容器类型的访问会进行边界检查。这可能影响性能，例如在热点循环中，不过往往没有想象中那么频繁。

有几种安全方式可以改写代码，让编译器了解容器长度并优化掉边界检查。

- 在循环中用迭代替代直接元素访问。
- 不要在循环内对 `Vec` 做索引，而是在循环前把 `Vec` 转成切片，再在循环内对切片索引。
- 为索引变量的范围添加断言。
[**示例 1**](https://github.com/rust-random/rand/pull/960/commits/de9dfdd86851032d942eb583d8d438e06085867b)，
[**示例 2**](https://github.com/image-rs/jpeg-decoder/pull/167/files)。

要让这些技巧生效可能比较棘手。[Bounds Check Cookbook] 对此有更详细的说明。

[Bounds Check Cookbook]: https://github.com/Shnatsel/bounds-check-cookbook/

作为最后手段，还有不安全的 [`get_unchecked`] 和 [`get_unchecked_mut`] 方法。

[`get_unchecked`]: https://doc.rust-lang.org/std/primitive.slice.html#method.get_unchecked
[`get_unchecked_mut`]: https://doc.rust-lang.org/std/primitive.slice.html#method.get_unchecked_mut
