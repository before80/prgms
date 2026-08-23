+++
title = "8 类型大小"
date = 2026-08-23T13:57:00+08:00
weight = 9
type = "docs"
description = "缩小类型与内存布局"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Rust Performance Book](https://nnethercote.github.io/perf-book/)

# 类型大小 {#type-sizes}


> 原文链接: [https://nnethercote.github.io/perf-book/type-sizes.html](https://nnethercote.github.io/perf-book/type-sizes.html)


缩小经常实例化的类型有助于性能。

例如，如果内存占用较高，像 [DHAT] 这样的堆分析器可以识别热点分配点及相关类型。缩小这些类型可以减少峰值内存占用，并可能通过减少内存流量和缓存压力来改善性能。

[DHAT]: https://www.valgrind.org/docs/manual/dh-manual.html

此外，大于 128 字节的 Rust 类型使用 `memcpy` 复制而非内联代码。如果 `memcpy` 在 profile 中以非平凡的数量出现，DHAT 的「复制分析」模式会准确告诉你热点 `memcpy` 调用的位置及相关类型。将这些类型缩小到 128 字节或更小，可以通过避免 `memcpy` 调用并减少内存流量来使代码更快。

## 测量类型大小

[`std::mem::size_of`] 给出类型的大小（以字节为单位），但你通常还想知道确切的布局。例如，枚举可能因单个过大的变体而出人意料地大。

[`std::mem::size_of`]: https://doc.rust-lang.org/std/mem/fn.size_of.html

`-Zprint-type-sizes` 选项正是为此而设。它在 release 版本的 rustc 上未启用，因此你需要使用 nightly 版本的 rustc。以下是通过 Cargo 的一种可能调用方式：
```text
RUSTFLAGS=-Zprint-type-sizes cargo +nightly build --release
```
以下是 rustc 的一种可能调用方式：
```text
rustc +nightly -Zprint-type-sizes input.rs
```
它将打印所有使用中的类型的大小、布局和对齐方式的详细信息。例如，对于这个类型：
```rust
enum E {
    A,
    B(i32),
    C(u64, u8, u64, u8),
    D(Vec<u32>),
}
```
它会打印以下内容，以及一些内置类型的信息。
```text
print-type-size type: `E`: 32 bytes, alignment: 8 bytes
print-type-size     discriminant: 1 bytes
print-type-size     variant `D`: 31 bytes
print-type-size         padding: 7 bytes
print-type-size         field `.0`: 24 bytes, alignment: 8 bytes
print-type-size     variant `C`: 23 bytes
print-type-size         field `.1`: 1 bytes
print-type-size         field `.3`: 1 bytes
print-type-size         padding: 5 bytes
print-type-size         field `.0`: 8 bytes, alignment: 8 bytes
print-type-size         field `.2`: 8 bytes
print-type-size     variant `B`: 7 bytes
print-type-size         padding: 3 bytes
print-type-size         field `.0`: 4 bytes, alignment: 4 bytes
print-type-size     variant `A`: 0 bytes
```
输出显示以下内容。
- 类型的大小和对齐方式。
- 对于枚举，判别式的大小。
- 对于枚举，每个变体的大小（从大到小排序）。
- 所有字段的大小、对齐方式和顺序。（注意，编译器已重新排列变体 `C` 的字段以最小化 `E` 的大小。）
- 所有填充的大小和位置。

或者，可以使用 [top-type-sizes] crate 以更紧凑的形式显示输出。

[top-type-sizes]: https://crates.io/crates/top-type-sizes

一旦你知道热点类型的布局，有多种方法可以缩小它。

## 字段排序

Rust 编译器会自动对结构体和枚举的字段进行排序以最小化其大小（除非指定了 `#[repr(C)]` 属性），因此你不必担心字段排序。但还有其他方法可以最小化热点类型的大小。

## 缩小枚举

如果枚举有一个过大的变体，考虑将一个或多个字段装箱。例如，你可以将这个类型：
```rust
type LargeType = [u8; 100];
enum A {
    X,
    Y(i32),
    Z(i32, LargeType),
}
```
改为：
```rust
# type LargeType = [u8; 100];
enum A {
    X,
    Y(i32),
    Z(Box<(i32, LargeType)>),
}
```
这以 `A::Z` 变体需要额外堆分配为代价减小了类型大小。如果 `A::Z` 变体相对罕见，这更可能成为净性能收益。`Box` 还会使 `A::Z` 使用起来稍不便捷，尤其是在 `match` 模式中。
[**示例 1**](https://github.com/rust-lang/rust/pull/37445/commits/a920e355ea837a950b484b5791051337cd371f5d)，
[**示例 2**](https://github.com/rust-lang/rust/pull/55346/commits/38d9277a77e982e49df07725b62b21c423b6428e)，
[**示例 3**](https://github.com/rust-lang/rust/pull/64302/commits/b972ac818c98373b6d045956b049dc34932c41be)，
[**示例 4**](https://github.com/rust-lang/rust/pull/64374/commits/2fcd870711ce267c79408ec631f7eba8e0afcdf6)，
[**示例 5**](https://github.com/rust-lang/rust/pull/64394/commits/7f0637da5144c7435e88ea3805021882f077d50c)，
[**示例 6**](https://github.com/rust-lang/rust/pull/71942/commits/27ae2f0d60d9201133e1f9ec7a04c05c8e55e665)。

## 更小的整数

通常可以通过使用更小的整数类型来缩小类型。例如，虽然使用 `usize` 作为索引最自然，但将索引存储为 `u32`、`u16` 甚至 `u8` 通常是合理的，然后在使用点强制转换为 `usize`。
[**示例 1**](https://github.com/rust-lang/rust/pull/49993/commits/4d34bfd00a57f8a8bdb60ec3f908c5d4256f8a9a)，
[**示例 2**](https://github.com/rust-lang/rust/pull/50981/commits/8d0fad5d3832c6c1f14542ea0be038274e454524)。

## 装箱切片

Rust 向量包含三个字：长度、容量和指针。如果你有一个不太可能在未来更改的向量，可以使用 [`Vec::into_boxed_slice`] 将其转换为*装箱切片*。装箱切片只包含两个字：长度和指针。任何多余的元素容量将被丢弃，可能导致重新分配。
```rust
# use std::mem::{size_of, size_of_val};
let v: Vec<u32> = vec![1, 2, 3];
assert_eq!(size_of_val(&v), 3 * size_of::<usize>());

let bs: Box<[u32]> = v.into_boxed_slice();
assert_eq!(size_of_val(&bs), 2 * size_of::<usize>());
```
或者，可以使用 [`Iterator::collect`] 直接从迭代器构造装箱切片。如果事先知道迭代器的长度，这可以避免任何重新分配。
```rust
let bs: Box<[u32]> = (1..3).collect();
```
装箱切片可以使用 [`slice::into_vec`] 转换为向量，无需任何克隆或重新分配。

[`Vec::into_boxed_slice`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.into_boxed_slice
[`Iterator::collect`]: https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.collect
[`slice::into_vec`]: https://doc.rust-lang.org/std/primitive.slice.html#method.into_vec

## `ThinVec`

装箱切片的替代方案是 [`thin_vec`] crate 的 `ThinVec`。它在功能上等同于 `Vec`，但将长度和容量存储在与元素相同的分配中（如果有元素的话）。这意味着 `size_of::<ThinVec<T>>` 只有一个字。

`ThinVec` 是经常实例化的类型中、通常为空向量的良好选择。如果最大变体包含 `Vec`，也可用于缩小枚举的最大变体。

[`thin_vec`]: https://crates.io/crates/thin-vec

## 避免回退

如果某个类型足够热点，其大小可能影响性能，使用静态断言确保它不会意外回退是个好主意。以下示例使用 [`static_assertions`] crate 的宏。
```rust
  // 此类型使用频繁。确保它不会无意中变大。
  #[cfg(target_arch = "x86_64")]
  static_assertions::assert_eq_size!(HotType, [u8; 64]);
```
`cfg` 属性很重要，因为类型大小在不同平台上可能不同。将断言限制在 `x86_64`（通常是最广泛使用的平台）上，在实践中可能足以防止回退。

[`static_assertions`]: https://crates.io/crates/static_assertions
