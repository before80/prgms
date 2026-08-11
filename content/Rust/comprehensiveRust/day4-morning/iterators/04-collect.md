+++
title = "2.4 `collect`"
date = 2026-08-11T11:30:00+08:00
weight = 166
type = "docs"
description = "04-`collect` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/iterators/collect.html](https://google.github.io/comprehensive-rust/iterators/collect.html)

# 2.4 `collect`

[`collect`][3] 方法可以让你从 [`Iterator`][2] 构建一个集合。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let primes = vec![2, 3, 5, 7];
    let prime_squares = primes.into_iter().map(|p| p * p).collect::<Vec<_>>();
    println!("prime_squares: {prime_squares:?}");
}
```

> - 任意迭代器都可以收集（collect）到 `Vec`、`VecDeque` 或 `HashSet`。产出键值对（即二元组）的迭代器还可以收集到 `HashMap` 和 `BTreeMap`。
>
> 向学员展示标准库文档中 `collect` 的定义。指定该方法的泛型类型 `B` 有两种方式：
>
> - 使用「涡轮鱼」（turbofish）语法：`some_iterator.collect::<COLLECTION_TYPE>()`，如示例所示。这里的 `_` 简写让 Rust 推断 `Vec` 元素的类型。
> - 使用类型推断：`let prime_squares: Vec<_> = some_iterator.collect()`。可以把示例改写成这种形式。
>
> ## 更多探索
>
> - 若学员好奇其工作原理，可以提到 [`FromIterator`][1] trait，它定义了每种集合类型如何从迭代器构建。
> - 除了 `Vec`、`HashMap` 等的基本 `FromIterator` 实现外，还有更专门的实现，例如可以把 `Iterator<Item = Result<V, E>>` 转换成 `Result<Vec<V>, E>`。
> - 使用 `collect` 时经常需要类型标注，因为它对返回类型是泛型的，这会让编译器在许多情况下更难推断出正确类型。


[1]: https://doc.rust-lang.org/std/iter/trait.FromIterator.html
[2]: https://doc.rust-lang.org/std/iter/trait.Iterator.html
[3]: https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.collect
