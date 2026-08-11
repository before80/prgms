+++
title = "1.1 Safe 与 Unsafe 如何交互"
date = 2026-08-06T17:08:00+08:00
weight = 3
type = "docs"
description = "Safe 与 Unsafe 如何划分责任并协同工作"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# Safe 与 Unsafe 如何交互


> 原文链接: [https://doc.rust-lang.org/nomicon/safe-unsafe-meaning.html](https://doc.rust-lang.org/nomicon/safe-unsafe-meaning.html)


　　Safe Rust 与 Unsafe Rust 是什么关系？它们如何交互？

　　Safe 与 Unsafe 的分界由 `unsafe` 关键字控制，它充当二者之间的接口。因此我们说 Safe Rust 是安全语言：所有 unsafe 部分都严格关在 `unsafe` 边界之后。若愿意，你甚至可以在代码库中加入 `#![forbid(unsafe_code)]`，静态保证只写 Safe Rust。

　　`unsafe` 有两个用途：声明编译器无法检查的契约存在；声明程序员已检查这些契约得到满足。

　　可用 `unsafe` 在*函数*与*trait 声明*上标明存在未检查的契约。对函数，`unsafe` 表示调用者须查阅文档，确保用法满足函数要求的契约。对 trait 声明，`unsafe` 表示实现者须查阅 trait 文档，确保实现满足 trait 要求的契约。

　　可用 `unsafe` 块声明块内所有 unsafe 操作均已验证满足相应契约。例如，传给 [`slice::get_unchecked`][get_unchecked] 的索引在界内。

　　可用 `unsafe` 在 trait 实现上声明实现满足 trait 契约。例如，实现 [`Send`] 的类型确实可安全移到另一线程。

　　标准库有许多 unsafe 函数，包括：

* [`slice::get_unchecked`][get_unchecked]：无界检查索引，可随意破坏内存安全。
* [`mem::transmute`][transmute]：把某值按给定类型重新解释，以任意方式绕过类型安全（详见 [conversions]）。
* 每个指向有大小类型的裸指针都有 [`offset`][ptr_offset] 方法；若偏移不在 ["界内"][ptr_offset] 则触发未定义行为。
* 所有 FFI（Foreign Function Interface，外部函数接口）调用都是 `unsafe` 的，因为另一语言可做编译器无法检查的任意操作。

　　截至 Rust 1.29.2，标准库定义了以下 unsafe trait（还有其他，但尚未稳定，有些可能永远不会）：

* [`Send`]：标记 trait（无 API），承诺实现者可安全发送到（move 到）另一线程。
* [`Sync`]：标记 trait，承诺线程可通过共享引用安全共享实现者。
* [`GlobalAlloc`]：允许自定义整个程序的内存分配器。

　　Rust 标准库内部也大量使用 Unsafe Rust。这些实现通常经过严格人工审查，因此建立在它们之上的 Safe Rust 接口可假定是安全的。

　　这种分离的根本原因在于 Safe Rust 的一个基本性质——*健全性（soundness）*：

　　**无论如何，Safe Rust 的调用者都不能导致未定义行为。**

　　safe/unsafe 划分的设计意味着 Safe 与 Unsafe Rust 之间存在不对称的信任关系。Safe Rust 本质上必须信任它接触到的任何 Unsafe Rust 写得正确；而 Unsafe Rust 不能不经考虑就信任 Safe Rust。它可以信任作为*客户端*的 Safe Rust，但不能信任由*其客户端*选择或提供的 Safe Rust。

　　例如，Rust 有 [`PartialOrd`] 与 [`Ord`] trait，区分「仅仅可比较」的类型与提供「全序」（total ordering，即比较行为合理）的类型。

　　[`BTreeMap`] 对部分有序类型意义不大，因此要求键实现 `Ord`。但 `BTreeMap` 实现内含 Unsafe Rust。若草率的 `Ord` 实现（写它是 Safe 的）导致未定义行为，就不可接受；因此 BTreeMap 内的 unsafe 代码必须能抵御并非真正全序的 `Ord` 实现——尽管要求 `Ord` 的本意正是全序。

　　Unsafe Rust 代码就是不能信任 Safe Rust 一定写得正确。话虽如此，若你传入没有全序的值，`BTreeMap` 仍会行为完全错乱；只是不会导致未定义行为。

　　有人可能问：若 `BTreeMap` 因 `Ord` 是 Safe 的而不能信任它，为何能信任*任何* Safe 代码？例如 `BTreeMap` 依赖整数与 slice 实现正确——它们也是 safe 的，对吧？

　　区别在于范围。当 `BTreeMap` 依赖整数与 slice 时，它依赖的是*非常具体*的实现。这是可权衡收益的风险。此处风险基本为零：若整数与 slice 坏了，*所有人*都坏了；且它们与 `BTreeMap` 由同一批人维护，便于跟踪。

　　crate 边界也可如此：若 crate `foo` 依赖 crate `bar`，则 `foo` 中的 Unsafe Rust 可信任 `bar` 中的 Safe Rust——因为 `foo` 选择依赖 `bar`，即信任 `bar` 实现正确。

　　另一方面，`BTreeMap` 的键类型是泛型的。信任其 `Ord` 实现意味着信任*任意*客户端的 `Ord` 实现。此处风险高：某处有人会搞错 `Ord`，甚至因「看起来能用」而谎称提供全序。那时 `BTreeMap` 必须有所准备。

　　对传给你的闭包行为正确的信任，逻辑相同。

　　这种无界泛型信任的问题，正是 `unsafe` trait 要解决的。理论上 `BTreeMap` 可要求键实现名为 `UnsafeOrd` 的新 trait 而非 `Ord`，可能如下：

```rust
use std::cmp::Ordering;

unsafe trait UnsafeOrd {
    fn cmp(&self, other: &Self) -> Ordering;
}
```

　　然后类型用 `unsafe` 实现 `UnsafeOrd`，表示已确保实现满足 trait 期望的契约。此时 `BTreeMap` 内部的 Unsafe Rust 有理由信任键类型的 `UnsafeOrd` 实现正确；若不对，错在 unsafe trait 实现，与 Rust 安全保证一致。

　　是否将 trait 标为 `unsafe` 是 API 设计选择。safe trait 更易实现，但依赖它的 unsafe 代码必须防御错误行为。标为 `unsafe` 则把责任转给实现者。Rust 传统上避免把 trait 标为 `unsafe`，因为会让 Unsafe Rust 无处不在，并不可取。

　　`Send` 与 `Sync` 标为 unsafe，因为线程安全是 unsafe 代码*无法*像防御有 bug 的 `Ord` 那样防御的*基本性质*。类似地，`GlobalAlloc` 掌管程序中所有内存，`Box`、`Vec` 等建立其上；若它行为怪异（例如仍在使用时把同一块内存再给另一请求），几乎无法检测并处理。

　　是否把自己的 trait 标为 `unsafe` 取决于同类考量：若 unsafe 代码无法合理期望防御 trait 的错误实现，标为 `unsafe` 是合理选择。

　　顺带一提，虽 `Send` 与 `Sync` 是 `unsafe` trait，当可证明安全时也会*自动*为类型实现。`Send` 自动为仅由也实现 `Send` 的类型组成的类型推导；`Sync` 同理。这减小了把二者标为 unsafe 带来的普遍 unsafety。且很少有人会*实现*内存分配器（或直接用它）。

　　这就是 Safe 与 Unsafe Rust 之间的平衡。分离旨在让 Safe Rust 尽可能好用，而写 Unsafe Rust 则需额外努力与谨慎。本书其余部分主要讨论必须注意的方面，以及 Unsafe Rust 必须遵守的契约。

[`Send`]: ../std/marker/trait.Send.html
[`Sync`]: ../std/marker/trait.Sync.html
[`GlobalAlloc`]: ../std/alloc/trait.GlobalAlloc.html
[conversions]: conversions.html
[ptr_offset]: ../std/primitive.pointer.html#method.offset
[get_unchecked]: ../std/primitive.slice.html#method.get_unchecked
[transmute]: ../std/mem/fn.transmute.html
[`PartialOrd`]: ../std/cmp/trait.PartialOrd.html
[`Ord`]: ../std/cmp/trait.Ord.html
[`BTreeMap`]: ../std/collections/struct.BTreeMap.html
