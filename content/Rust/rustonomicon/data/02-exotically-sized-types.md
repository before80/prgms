+++
title = "2.2 奇异大小的类型"
date = 2026-08-06T17:08:00+08:00
weight = 8
type = "docs"
description = "DST、ZST、空类型与外部类型"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 奇异大小的类型


> 原文链接: [https://doc.rust-lang.org/nomicon/exotic-sizes.html](https://doc.rust-lang.org/nomicon/exotic-sizes.html)


　　多数时候，我们期望类型有静态已知且为正的大小。在 Rust 中并非总是如此。

## 动态大小类型（DST）

　　Rust 支持动态大小类型（Dynamically Sized Types，DST）：无静态已知大小或对齐的类型。表面上有悖常理：Rust *必须*知道某物的大小与对齐才能正确操作！就此而言，DST 不是普通类型。因缺乏静态已知大小，这些类型只能存在于指针之后。指向 DST 的任意指针因而成为*宽指针*，由指针与「补全」它的信息组成（下文详述）。

　　语言暴露的两大 DST：

* trait 对象：`dyn MyTrait`
* slice：[`[T]`][slice]、[`str`] 等

　　trait 对象表示实现其指定 trait 的某类型。确切原始类型被*擦除*，代之以运行时反射与包含使用该类型所需一切信息的 vtable。补全 trait 对象指针的信息是 vtable 指针。pointee 的运行时大小可从 vtable 动态请求。

　　slice  simply 是对某连续存储的视图——通常是数组或 `Vec`。补全 slice 指针的信息只是它指向的元素个数。pointee 的运行时大小只是元素静态已知大小乘以元素个数。

　　struct 实际上可将单个 DST 直接存为最后一个字段，但这也会使 struct 本身成为 DST：

```rust
// 无法直接放在栈上
struct MySuperSlice {
    info: u32,
    data: [u8],
}
```

　　遗憾的是，若无构造方式，这种类型 largely 无用。目前唯一 properly 支持创建自定义 DST 的方式是让类型泛化并做* unsizing 强制转换*：

```rust
struct MySuperSliceable<T: ?Sized> {
    info: u32,
    data: T,
}

fn main() {
    let sized: MySuperSliceable<[u8; 8]> = MySuperSliceable {
        info: 17,
        data: [0; 8],
    };

    let dynamic: &MySuperSliceable<[u8]> = &sized;

    // 打印: "17 [0, 0, 0, 0, 0, 0, 0, 0]"
    println!("{} {:?}", dynamic.info, &dynamic.data);
}
```

　　（是的，自定义 DST 目前 largely 是半成品特性。）

## 零大小类型（ZST）

　　Rust 也允许指定不占空间的类型：

```rust
struct Nothing; // 无字段 = 无大小

// 所有字段都无大小 = 无大小
struct LotsOfNothing {
    foo: Nothing,
    qux: (),      // 空元组无大小
    baz: [u8; 0], // 空数组无大小
}
```

　　就其本身，零大小类型（Zero Sized Types，ZST）显然几乎无用。但与 Rust 中许多 curious 布局选择一样，潜力在泛型上下文中显现：Rust largely 理解产生或存储 ZST 的任意操作可化为 no-op。首先，存储它无意义——不占空间。且该类型只有一个值，任何加载它的操作都可凭空产生——也是 no-op，因为不占空间。

　　极端例子之一是 Set 与 Map。给定 `Map<Key, Value>`，常见用 `Map<Key, UselessJunk>` 的薄包装实现 `Set<Key>`。在许多语言中，这 necessitates 为 UselessJunk 分配空间并做存取工作只为丢弃。对编译器证明这多余是困难分析。

　　然而在 Rust，我们可直接说 `Set<Key> = Map<Key, ()>`。Rust 静态知道每次 load/store 无用，且任何分配都无大小。结果单态化代码 basically 是 HashSet 的定制实现，却没有 HashMap 为支持 value 的开销。

　　Safe 代码不必操心 ZST，但 *unsafe* 代码必须注意无大小类型的后果。尤其指针偏移是 no-op，分配器通常[要求非零大小][alloc]。

　　注意对 ZST 的引用（含空 slice）与所有其他引用一样，必须非 null 且 suitably 对齐。然而，通过指向 ZST 的 null 指针 load/store 不是[未定义行为][ub]，与其他类型指针不同。

[alloc]: ../std/alloc/trait.GlobalAlloc.html#tymethod.alloc
[ub]: what-unsafe-does.html

## 空类型

　　Rust 还允许声明*甚至无法实例化*的类型。这些类型只能在类型层面谈论，永不能在值层面。空类型可通过声明无 variant 的 enum 声明：

```rust
enum Void {} // 无 variant = 空
```

　　空类型比 ZST 更 marginal。主要动机例子是类型级不可达。例如 suppose API 一般须返回 `Result`，但某具体情况 actually 不会失败。可在类型层面用 `Result<T, Void>` 表达。API 消费者可放心 unwrap，因为*静态不可能*该值为 `Err`——那需要提供 `Void` 类型的值。

　　原则上 Rust 可基于此做有趣分析与优化。例如 `Result<T, Void>` 表示为 just `T`，因为 `Err` case actually 不存在（严格说这只是优化、非保证，故例如 transmute 彼此仍是未定义行为）。

　　下列也能编译：

```rust
enum Void {}

let res: Result<u32, Void> = Ok(0);

// Err 已不存在，故 Ok  actually 不可反驳。
let Ok(num) = res;
```

　　空类型最后一个 subtle 细节：指向它们的裸指针 actually 可合法构造，但解引用是未定义行为，因为无意义。

　　不建议用 `*const Void` 建模 C 的 `void*`。很多人这样做但很快遇 trouble，因为 Rust 对用 unsafe 实例化空类型几乎没有安全 guard，若做了就是未定义行为。尤其 problematic 的是开发者习惯把裸指针转成引用，而构造 `&Void` *也*是未定义行为。

　　`*const ()`（或等价物）对 `void*`  reasonably 可用，可变成引用而无安全问题。仍无法阻止读写值，但至少编译为 no-op 而非未定义行为。

## 外部类型（Extern Types）

　　[已接受的 RFC][extern-types] 要加入大小未知的 proper 类型，称* extern types*，让 Rust 开发者更准确建模 C 的 `void*` 等「声明但从未定义」的类型。但截至 Rust 2018，[`size_of_val::<MyExternType>()` 应如何行为][extern-types-issue] 使特性 stuck in limbo。

[extern-types]: https://github.com/rust-lang/rfcs/blob/master/text/1861-extern-types.md
[extern-types-issue]: https://github.com/rust-lang/rust/issues/43467
[`str`]: ../std/primitive.str.html
[slice]: ../std/primitive.slice.html
