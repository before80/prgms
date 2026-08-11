+++
title = "2.3 其他 repr"
date = 2026-08-06T17:08:00+08:00
weight = 9
type = "docs"
description = "repr(C)、transparent、整数、packed 与 align"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 其他 repr


> 原文链接: [https://doc.rust-lang.org/nomicon/other-reprs.html](https://doc.rust-lang.org/nomicon/other-reprs.html)


　　Rust 允许指定与默认不同的数据布局策略。

## repr(C)

　　这是最重要的 `repr`。意图 fairly 简单：按 C 的方式做。字段顺序、大小与对齐与 C 或 C++ 中预期完全一致。类型跨 `extern "C"` 函数调用边界传递的方式也与 C 传递对应类型相同。任何期望通过 FFI 边界的类型都应有 `repr(C)`，因为 C 是编程世界的 lingua franca。要对数据布局做更 elaborate 的双关（如把值重新解释为不同类型），这也是 soundly 做的必要条件。

　　我们强烈建议用 [rust-bindgen] 和/或 [cbindgen] 管理 FFI 边界。Rust 团队与这些项目紧密合作，确保它们稳健且与类型布局与 `repr` 的当前及未来保证兼容。

　　须牢记 `repr(C)` 与 Rust 更 exotic 数据布局特性的交互。因双重目的「用于 FFI」与「用于布局控制」，`repr(C)` 可用于通过 FFI 边界传递会 nonsensical 或有问题的类型。

* ZST 仍为零大小，虽非 C 标准行为，且明确 contrary 于 C++ 中空类型仍应占一字节。

* DST 指针（宽指针）与 tuple 不是 C 概念，因而 never FFI-safe。

* 带字段的 enum 也不是 C/C++ 概念，但类型的有效桥接[已定义][really-tagged]。

* 若 `T` 是 [FFI-safe 非空指针类型](ffi.html#the-nullable-pointer-optimization)，`Option<T>` 保证与 `T` 布局与 ABI 相同，因而也 FFI-safe。截至本文写作，涵盖 `&`、`&mut` 与函数指针，它们永不为 null。

* 元组 struct 就 `repr(C)` 而言像 struct，唯一区别是字段无命名。

* 对无字段 enum，`repr(C)` 等价于某个 `repr(u*)`（见下一节）。选定的大小与符号是目标平台 C ABI 的默认 enum 大小与符号。注意 C 中 enum 表示由实现定义，故这 really 是「最佳猜测」。尤其当相关 C 代码用特定 flag 编译时可能不正确。

* 带 `repr(C)` 或 `repr(u*)` 的无字段 enum 仍不能设为无对应 variant 的整数值，虽 C/C++ 允许。构造与任一 variant 不匹配的 enum 实例是未定义行为（unsafe 地）。这允许 exhaustive match 照常编写与编译。

## repr(transparent)

　　`#[repr(transparent)]` 只能用于 struct 或只有一个非零大小字段的单 variant enum（可有额外零大小字段）。效果是整 struct/enum 的布局与 ABI 保证与该字段相同。

> 注：有 `transparent_unions` nightly 特性把 `repr(transparent)` 用于 union，但因设计顾虑未稳定。见 [tracking issue][issue-60405]。

　　目标是可在单字段与 struct/enum 之间 transmute。例如 [`UnsafeCell`] 可 transmute 成它包装的类型（[`UnsafeCell`] 还用 unstable [no_niche][no-niche-pull]，嵌于其他类型时 ABI  actually 不保证相同）。

　　此外，通过 FFI 传递 struct/enum 而对方期望内部字段类型，保证可行。尤其 `struct Foo(f32)` 或 `enum Foo { Bar(f32) }` 须始终与 `f32` ABI 相同。

　　仅当单字段为 `pub`，或其布局以 prose 文档化时，此 repr 才视为类型公开 ABI 的一部分。否则其他 crate 不应依赖布局。

　　更多细节见 [RFC 1758][rfc-transparent] 与 [RFC 2645][rfc-transparent-unions-enums]。

## repr(u*)、repr(i*)

　　这些指定无字段 enum 的大小与符号。若判别式溢出须放入的整数，将产生编译期错误。可手动把溢出元素显式设为 0 请求 Rust 允许。但 Rust 不允许两个 variant 判别式相同。

　　「无字段 enum」仅指 enum 各 variant 无数据。无 `repr` 的无字段 enum 仍是 Rust 原生类型，无稳定布局或表示。加 `repr(u*)`/`repr(i*)` 使布局目的上 treated 如同指定整数类型（编译器仍会利用该类型「无效」值的知识优化 enum 布局，例如包在 `Option` 中时）。注意这些类型的函数调用 ABI 一般仍 unspecified，除跨 `extern "C"` 调用时与同符号同大小 C enum ABI 兼容。

　　若 enum 有字段，效果类似 `repr(C)`：类型有定义布局。这可把 enum 传给 C，或访问类型 raw 表示并直接操纵 tag 与字段。见 [RFC][really-tagged]。

　　这些 `repr` 对 struct 无效果。

　　对有字段 enum 加显式 `repr(u*)`、`repr(i*)` 或 `repr(C)` 会 suppress 空指针优化，例如：

```rust
# use std::mem::size_of;
enum MyOption<T> {
    Some(T),
    None,
}

#[repr(u8)]
enum MyReprOption<T> {
    Some(T),
    None,
}

assert_eq!(8, size_of::<MyOption<&u16>>());
assert_eq!(16, size_of::<MyReprOption<&u16>>());
```

　　此优化仍适用于带显式 `repr(u*)`、`repr(i*)` 或 `repr(C)` 的无字段 enum。

## repr(packed)、repr(packed(n))

　　`repr(packed(n))`（`n` 为 2 的幂）强制类型对齐*至多* `n`。最常见无显式 `n` 时，`repr(packed)` 等价于 `repr(packed(1))`，强制 Rust  strip 任意 padding，只对齐到字节。可能改善内存占用，但 likely 有其他负面效果。

　　尤其多数架构*强烈*偏好自然对齐。这可能意味着未对齐 load 受罚（x86），甚至 fault（某些 ARM）。对直接 load/store packed 字段的简单情况，编译器也许能用 shift 与 mask 掩盖对齐问题。但若对 packed 字段取引用，编译器 unlikely 能 emit 避免未对齐 load 的代码。

　　[因可导致未定义行为][ub loads]，lint 已实现并将成为硬错误。

　　`repr(packed)/repr(packed(n))` 不应 lightly 使用。除非有极端需求，不应使用。

　　此 repr 是 `repr(C)` 与 `repr(Rust)` 的修饰。为 FFI 兼容你 most likely 应显式写：`repr(C, packed)`。

## repr(align(n))

　　`repr(align(n))`（`n` 为 2 的幂）强制类型对齐*至少* `n`。

　　这 enable 若干技巧，例如确保数组相邻元素 never 共享同一 cache line（可能加速某些并发代码）。

　　这是 `repr(C)` 与 `repr(Rust)` 的修饰。与 `repr(packed)` 不兼容。

[drop flags]: drop-flags.html
[ub loads]: https://github.com/rust-lang/rust/issues/27060
[issue-60405]: https://github.com/rust-lang/rust/issues/60405
[`UnsafeCell`]: ../std/cell/struct.UnsafeCell.html
[rfc-transparent]: https://github.com/rust-lang/rfcs/blob/master/text/1758-repr-transparent.md
[rfc-transparent-unions-enums]: https://rust-lang.github.io/rfcs/2645-transparent-unions.html
[really-tagged]: https://github.com/rust-lang/rfcs/blob/master/text/2195-really-tagged-unions.md
[rust-bindgen]: https://rust-lang.github.io/rust-bindgen/
[cbindgen]: https://github.com/eqrion/cbindgen
[no-niche-pull]: https://github.com/rust-lang/rust/pull/68491
