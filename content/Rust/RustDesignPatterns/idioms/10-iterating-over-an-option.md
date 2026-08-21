+++
title = "10-遍历 Option"
date = 2026-08-18T22:10:00+08:00
weight = 17
type = "docs"
description = "遍历 Option — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/option-iter.html](https://rust-unofficial.github.io/patterns/idioms/option-iter.html)

# 遍历 Option

## 描述 {#description}

`Option` 可以看作一个包含零个或一个元素的容器。特别是，它实现了 `IntoIterator` trait，因此可以用于需要此类类型的泛型代码。

## 示例 {#examples}

由于 `Option` 实现了 `IntoIterator`，它可以作为
[`.extend()`](https://doc.rust-lang.org/std/iter/trait.Extend.html#tymethod.extend) 的参数：

```rust
let turing = Some("Turing");
let mut logicians = vec!["Curry", "Kleene", "Markov"];

logicians.extend(turing);

// 等价于
if let Some(turing_inner) = turing {
    logicians.push(turing_inner);
}
```

如果需要把一个 `Option` 接到现有迭代器的末尾，可以把它传给
[`.chain()`](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.chain)：

```rust
let turing = Some("Turing");
let logicians = vec!["Curry", "Kleene", "Markov"];

for logician in logicians.iter().chain(turing.iter()) {
    println!("{logician} is a logician");
}
```

注意：如果该 `Option` 总是 `Some`，那么更地道的做法是对该元素使用
[`std::iter::once`](https://doc.rust-lang.org/std/iter/fn.once.html)，而不是用 `Option`。

另外，由于 `Option` 实现了 `IntoIterator`，也可以用 `for` 循环遍历它。这等价于用 `if let Some(..)` 匹配，而且在大多数情况下应优先使用后者。

## 参见 {#see-also}

- [`std::iter::once`](https://doc.rust-lang.org/std/iter/fn.once.html) 是一个恰好产生一个元素的迭代器。它是比 `Some(foo).into_iter()` 更易读的替代方案。

- [`Iterator::filter_map`](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.filter_map)
  是
  [`Iterator::map`](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.map) 的一个版本，专门用于返回 `Option` 的映射函数。

- [`ref_slice`](https://crates.io/crates/ref_slice) crate 提供了把 `Option` 转换成零个或一个元素的切片的函数。

- [`Option<T>` 的文档](https://doc.rust-lang.org/std/option/enum.Option.html)
