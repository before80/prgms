+++
title = "2.1 repr(Rust)"
date = 2026-08-06T17:08:00+08:00
weight = 7
type = "docs"
description = "默认的 Rust 数据表示"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# repr(Rust)


> 原文链接: [https://doc.rust-lang.org/nomicon/repr-rust.html](https://doc.rust-lang.org/nomicon/repr-rust.html)


　　​	首先，所有类型都有以字节为单位的对齐（alignment）。对齐指定哪些地址可合法存储该值。对齐为 `n` 的值只能存放在 `n` 的倍数地址上。对齐 2 表示必须存在偶地址；对齐 1 表示可存任意处。对齐至少为 1，且恒为 2 的幂。

　　原语通常按自身大小对齐，虽为平台相关行为。例如在 x86 上 `u64` 与 `f64` 常对齐到 4 字节（32 位）。

　　类型大小必须始终为其对齐的倍数（零对任意对齐都是合法大小）。这保证该类型数组总可通过大小倍数偏移索引。注意在[动态大小类型][dst]情况下，大小与对齐可能无法在静态已知。

　　Rust 提供下列复合数据布局方式：

* struct（具名积类型）
* tuple（匿名积类型）
* array（同质积类型）
* enum（具名和类型——带标签的 union）
* union（无标签 union）

　　若 enum 的各 variant 均无关联数据，则称该 enum 为*无字段*（field-less）。

　　默认情况下，复合结构的对齐等于各字段对齐的最大值。Rust 因而会在必要时插入 padding，确保所有字段正确对齐且整体类型大小为对齐的倍数。例如：

```rust
struct A {
    a: u8,
    b: u32,
    c: u16,
}
```

　　在将这些原语按各自大小对齐的目标上，将为 32 位对齐。整个 struct 大小因而是 32 位的倍数。可能变成：

```rust
struct A {
    a: u8,
    _pad1: [u8; 3], // 为对齐 `b`
    b: u32,
    c: u16,
    _pad2: [u8; 2], // 使总大小为 4 的倍数
}
```

　　或也许是：

```rust
struct A {
    b: u32,
    c: u16,
    a: u8,
    _pad: u8,
}
```

　　这些类型*无间接*；所有数据存在 struct 内，与 C 中预期相同。但除数组（密集打包且顺序固定）外，默认不指定数据布局。给定下面两个 struct 定义：

```rust
struct A {
    a: i32,
    b: u64,
}

struct B {
    a: i32,
    b: u64,
}
```

　　Rust *确实*保证两个 A 实例的数据布局完全相同。但 Rust *目前不*保证 A 的实例与 B 的实例字段顺序或 padding 相同。

　　就所写 A 与 B 而言，这点似乎吹毛求疵，但 Rust 若干其他特性使语言以复杂方式摆弄数据布局变得 desirable。

　　例如考虑：

```rust
struct Foo<T, U> {
    count: u16,
    data1: T,
    data2: U,
}
```

　　再考虑 `Foo<u32, u16>` 与 `Foo<u16, u32>` 的单态化。若 Rust 按指定顺序排字段，我们预期会 padding 以满足对齐。故若 Rust 不重排字段，我们预期：

```rust,ignore
struct Foo<u16, u32> {
    count: u16,
    data1: u16,
    data2: u32,
}

struct Foo<u32, u16> {
    count: u16,
    _pad1: u16,
    data1: u32,
    data2: u16,
    _pad2: u16,
}
```

　　后一种情况 simply 浪费空间。最优空间利用要求不同单态化有*不同字段顺序*。

　　enum 使考量更复杂。naively，如下 enum：

```rust
enum Foo {
    A(u32),
    B(u64),
    C(u8),
}
```

　　可能布局为：

```rust
struct FooRepr {
    data: u64, // 根据 `tag` 为 u64、u32 或 u8
    tag: u8,   // 0 = A, 1 = B, 2 = C
}
```

　　 indeed 大致如此布局（`tag` 的大小与位置 modulo）。

　　然而若干情况下这种表示低效。经典例子是 Rust 的「空指针优化」：由单个外层 unit variant（如 `None`）与（可能嵌套的）非空指针 variant（如 `Some(&T)`）组成的 enum 使 tag 多余。空指针可安全解释为 unit（`None`）variant。结果例如 `size_of::<Option<&T>>() == size_of::<&T>()`。

　　Rust 中许多类型是或包含非空指针，如 `Box<T>`、`Vec<T>`、`String`、`&T`、`&mut T`。类似地，可想象嵌套 enum 将 tag 合并为单一判别式，因按定义其有效值范围有限。原则上 enum 可用相当 elaborate 的算法在嵌套类型的 forbidden 值中存储比特。因此*尤其* desirable 是今天 leave enum 布局 unspecified。

[dst]: exotic-sizes.html#dynamically-sized-types-dsts
