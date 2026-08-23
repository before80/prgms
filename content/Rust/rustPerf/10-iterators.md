+++
title = "10 迭代器"
date = 2026-08-23T13:57:00+08:00
weight = 11
type = "docs"
description = "迭代器与性能"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Rust Performance Book](https://nnethercote.github.io/perf-book/)

# 迭代器 {#iterators}


> 原文链接: [https://nnethercote.github.io/perf-book/iterators.html](https://nnethercote.github.io/perf-book/iterators.html)


## `collect` 和 `extend`

[`Iterator::collect`] 将迭代器转换为 `Vec` 等集合，通常需要分配内存。若集合随后仅被再次迭代，应避免调用 `collect`。

[`Iterator::collect`]: https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.collect

因此，函数返回 `impl Iterator<Item=T>` 往往比返回 `Vec<T>` 更好。注意有时这些返回类型需要额外的生命周期参数，[这篇博客文章]有说明。
[**示例**](https://github.com/rust-lang/rust/pull/77990/commits/660d8a6550a126797aa66a417137e39a5639451b)。

[这篇博客文章]: https://blog.katona.me/2019/12/29/Rust-Lifetimes-and-Iterators/

类似地，可以用 [`extend`] 用迭代器扩展现有集合（如 `Vec`），而不是先把迭代器 `collect` 成 `Vec` 再 [`append`]。

[`extend`]: https://doc.rust-lang.org/std/iter/trait.Extend.html#tymethod.extend
[`append`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.append

最后，编写迭代器时，若可能，通常值得实现 [`Iterator::size_hint`] 或 [`ExactSizeIterator::len`] 方法。使用这些迭代器的 `collect` 和 `extend` 调用可能因此减少分配次数，因为它们能提前知道迭代器将产生的元素数量。

[`Iterator::size_hint`]: https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.size_hint
[`ExactSizeIterator::len`]: https://doc.rust-lang.org/std/iter/trait.ExactSizeIterator.html#method.len

## 链式组合

[`chain`] 非常方便，但也可能比单个迭代器更慢。对热点迭代器，若可能，值得避免使用。
[**示例**](https://github.com/rust-lang/rust/pull/64801/commits/5ca99b750e455e9b5e13e83d0d7886486231e48a)。

类似地，[`filter_map`] 可能比先 [`filter`] 再 [`map`] 更快。

[`chain`]: https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.chain
[`filter_map`]: https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.filter_map
[`filter`]: https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.filter
[`map`]: https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.map

## 分块

需要分块迭代器且分块大小已知能整除切片长度时，应使用更快的 [`slice::chunks_exact`]，而不是 [`slice::chunks`]。

当分块大小未知能否整除切片长度时，仍可结合 [`ChunksExact::remainder`] 或手动处理剩余元素来使用 `slice::chunks_exact`，这样往往更快。
[**示例 1**](https://github.com/johannesvollmer/exrs/pull/173/files)，
[**示例 2**](https://github.com/johannesvollmer/exrs/pull/175/files)。

相关迭代器同理：
- [`slice::rchunks`]、[`slice::rchunks_exact`] 和 [`RChunksExact::remainder`]；
- [`slice::chunks_mut`]、[`slice::chunks_exact_mut`] 和 [`ChunksExactMut::into_remainder`]；
- [`slice::rchunks_mut`]、[`slice::rchunks_exact_mut`] 和 [`RChunksExactMut::into_remainder`]。

[`slice::chunks`]: https://doc.rust-lang.org/stable/std/primitive.slice.html#method.chunks
[`slice::chunks_exact`]: https://doc.rust-lang.org/stable/std/primitive.slice.html#method.chunks_exact
[`ChunksExact::remainder`]: https://doc.rust-lang.org/stable/std/slice/struct.ChunksExact.html#method.remainder

[`slice::rchunks`]: https://doc.rust-lang.org/stable/std/primitive.slice.html#method.rchunks
[`slice::rchunks_exact`]: https://doc.rust-lang.org/stable/std/primitive.slice.html#method.rchunks_exact
[`RChunksExact::remainder`]: https://doc.rust-lang.org/stable/std/slice/struct.RChunksExact.html#method.remainder

[`slice::chunks_mut`]: https://doc.rust-lang.org/stable/std/primitive.slice.html#method.chunks_mut
[`slice::chunks_exact_mut`]: https://doc.rust-lang.org/stable/std/primitive.slice.html#method.chunks_exact_mut
[`ChunksExactMut::into_remainder`]: https://doc.rust-lang.org/stable/std/slice/struct.ChunksExactMut.html#method.into_remainder

[`slice::rchunks_mut`]: https://doc.rust-lang.org/stable/std/primitive.slice.html#method.rchunks_mut
[`slice::rchunks_exact_mut`]: https://doc.rust-lang.org/stable/std/primitive.slice.html#method.rchunks_exact_mut
[`RChunksExactMut::into_remainder`]: https://doc.rust-lang.org/stable/std/slice/struct.RChunksExactMut.html#method.into_remainder

## `copied`

迭代小数据类型（如整数）的集合时，使用 `iter().copied()` 可能比 `iter()` 更好。消费该迭代器的代码会按值接收整数而非按引用，LLVM 在此情况下可能生成更优代码。
[**示例 1**](https://github.com/rust-lang/rust/issues/106539)，
[**示例 2**](https://github.com/rust-lang/rust/issues/113789)。

这是进阶技巧。你可能需要检查生成的机器码才能确认是否有效。详见[机器码](../15-machine-code/)一章。
