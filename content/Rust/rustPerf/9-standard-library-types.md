+++
title = "9 标准库类型"
date = 2026-08-23T13:57:00+08:00
weight = 10
type = "docs"
description = "选用高效标准库类型"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Rust Performance Book](https://nnethercote.github.io/perf-book/)

# 标准库类型 {#standard-library-types}


> 原文链接: [https://nnethercote.github.io/perf-book/standard-library-types.html](https://nnethercote.github.io/perf-book/standard-library-types.html)


值得通读常见标准库类型的文档——例如 [`Vec`]、[`Option`]、[`Result`] 以及 [`Rc`]/[`Arc`]——以发现有时能提升性能的实用函数。

[`Vec`]: https://doc.rust-lang.org/std/vec/struct.Vec.html
[`Option`]: https://doc.rust-lang.org/std/option/enum.Option.html
[`Result`]: https://doc.rust-lang.org/std/result/enum.Result.html
[`Rc`]: https://doc.rust-lang.org/std/rc/struct.Rc.html
[`Arc`]: https://doc.rust-lang.org/std/sync/struct.Arc.html

同样值得了解标准库类型的高性能替代方案，例如 [`Mutex`]、[`RwLock`]、[`Condvar`] 和 [`Once`]。

[`Mutex`]: https://doc.rust-lang.org/std/sync/struct.Mutex.html
[`RwLock`]: https://doc.rust-lang.org/std/sync/struct.RwLock.html
[`Condvar`]: https://doc.rust-lang.org/std/sync/struct.Condvar.html
[`Once`]: https://doc.rust-lang.org/std/sync/struct.Once.html

## `Vec`

创建长度为 `n` 的零填充 `Vec` 的最佳方式是 `vec![0; n]`。这很简单，而且可能比使用 `resize`、`extend` 或任何涉及 `unsafe` 的替代方案[同样快或更快]，因为它可以利用操作系统协助。

[同样快或更快]: https://github.com/rust-lang/rust/issues/54628

[`Vec::remove`] 会移除指定索引处的元素，并将后续所有元素左移一位，因此是 O(n)。[`Vec::swap_remove`] 会用最后一个元素替换指定索引处的元素，不保持顺序，但是 O(1)。

[`Vec::retain`] 能高效地从 `Vec` 中移除多个元素。其他集合类型（如 `String`、`HashSet` 和 `HashMap`）也有等价方法。

[`Vec::remove`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.remove
[`Vec::swap_remove`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.swap_remove
[`Vec::retain`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.retain

## `Option` 和 `Result`

[`Option::ok_or`] 将 `Option` 转换为 `Result`，并传入一个 `err` 参数，当 `Option` 值为 `None` 时使用。`err` 会被**立即**求值。若其计算开销很大，应改用 [`Option::ok_or_else`]，通过闭包惰性计算错误值。例如，应把下面这段代码：
```rust
# fn expensive() {}
# let o: Option<u32> = None;
let r = o.ok_or(expensive()); // 总是会求值 `expensive()`
```
改成：
```rust
# fn expensive() {}
# let o: Option<u32> = None;
let r = o.ok_or_else(|| expensive()); // 仅在需要时才求值 `expensive()`
```
[**示例**](https://github.com/rust-lang/rust/pull/50051/commits/5070dea2366104fb0b5c344ce7f2a5cf8af176b0)。

[`Option::ok_or`]: https://doc.rust-lang.org/std/option/enum.Option.html#method.ok_or
[`Option::ok_or_else`]: https://doc.rust-lang.org/std/option/enum.Option.html#method.ok_or_else

[`Option::map_or`]、[`Option::unwrap_or`]、[`Result::or`]、[`Result::map_or`] 和 [`Result::unwrap_or`] 也有类似的惰性替代方法。

[`Option::map_or`]: https://doc.rust-lang.org/std/option/enum.Option.html#method.map_or
[`Option::unwrap_or`]: https://doc.rust-lang.org/std/option/enum.Option.html#method.unwrap_or
[`Result::or`]: https://doc.rust-lang.org/std/result/enum.Result.html#method.or
[`Result::map_or`]: https://doc.rust-lang.org/std/result/enum.Result.html#method.map_or
[`Result::unwrap_or`]: https://doc.rust-lang.org/std/result/enum.Result.html#method.unwrap_or

## `Rc`/`Arc`

[`Rc::make_mut`]/[`Arc::make_mut`] 提供写时复制（clone-on-write）语义。它们会返回 `Rc`/`Arc` 的可变引用。若引用计数大于 1，会 `clone` 内部值以确保唯一所有权；否则直接修改原值。虽不常用，但偶尔极其有用。
[**示例 1**](https://github.com/rust-lang/rust/pull/65198/commits/3832a634d3aa6a7c60448906e6656a22f7e35628)，
[**示例 2**](https://github.com/rust-lang/rust/pull/65198/commits/75e0078a1703448a19e25eac85daaa5a4e6e68ac)。

[`Rc::make_mut`]: https://doc.rust-lang.org/std/rc/struct.Rc.html#method.make_mut
[`Arc::make_mut`]: https://doc.rust-lang.org/std/sync/struct.Arc.html#method.make_mut

## `Mutex`、`RwLock`、`Condvar` 和 `Once`

[`parking_lot`] crate 提供了这些同步类型的替代实现。`parking_lot` 类型的 API 和语义与标准库中对应类型相似，但不完全相同。

`parking_lot` 版本过去在某些平台上通常比标准库版本更小、更快、更灵活，但标准库版本已在部分平台上大幅改进。因此切换到 `parking_lot` 之前应先测量。

[`parking_lot`]: https://crates.io/crates/parking_lot

若决定全面使用 `parking_lot` 类型，很容易在某些地方误用标准库等价类型。可以[使用 Clippy] 来避免这一问题。

[使用 Clippy]: ../3-linting/#disallowing-types