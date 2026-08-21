+++
title = "10-静态项"
date = 2026-08-18T08:45:00+08:00
weight = 27
type = "docs"
description = "静态项 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/items/static-items.html](https://doc.rust-lang.org/reference/items/static-items.html)

r[items.static]
# 静态项

r[items.static.syntax]
```grammar,items
StaticItem ->
    ItemSafety?[^extern-safety] `static` `mut`? IDENTIFIER `:` Type ( `=` Expression )? `;`
```

[^extern-safety]: `safe` 和 `unsafe` 函数限定符在语义上只允许出现在 `extern` 块内。

r[items.static.intro]
*静态项*类似于[常量][constant]，不同之处在于它表示程序中的一块分配，该分配用初始化表达式进行初始化。所有指向该静态项的引用和原始指针都指向同一块分配。

r[items.static.lifetime]
静态项具有 `static` 生命周期，它长于 Rust 程序中的所有其他生命周期。静态项在程序结束时不会调用 [`drop`]。

r[items.static.storage-disjointness]
若该 `static` 的大小至少为 1 字节，则此分配与所有其他此类 `static` 分配以及堆分配和栈分配变量都不相交。不过，不可变 `static` 项的存储可以与本身不具有唯一地址的分配重叠，例如[被提升的值][promoteds]和 [`const` 项][constant]。

r[items.static.namespace]
静态声明在其所在模块或块的[值命名空间][value namespace]中定义静态值。

r[items.static.init]
静态初始化器是在编译期求值的[常量表达式][constant expression]。静态初始化器可以引用并读取其他静态项。在读取可变静态项时，它们读取的是该静态项的初始值。

r[items.static.read-only]
包含非[内部可变][interior mutable]类型的非 `mut` 静态项可以被放入只读内存。

r[items.static.safety]
对静态项的所有访问都是安全的，但对静态项有若干限制：

r[items.static.sync]
* 类型必须具有 [`Sync`](std::marker::Sync) trait 约束，以允许线程安全访问。

r[items.static.init.omission]
在[外部块][external block]中必须省略初始化表达式，而对自由静态项则必须提供。

r[items.static.safety-qualifiers]
`safe` 和 `unsafe` 限定符在语义上只允许在[外部块][external block]中使用。

r[items.static.generics]
## 静态项与泛型

在泛型作用域中定义的静态项（例如在 blanket 或默认实现中）会导致恰好定义一个静态项，就好像该静态定义被从当前作用域抽到模块中一样。*不会*为每次单态化各生成一项。

这段代码：

```rust
use std::sync::atomic::{AtomicUsize, Ordering};

trait Tr {
    fn default_impl() {
        static COUNTER: AtomicUsize = AtomicUsize::new(0);
        println!("default_impl: counter was {}", COUNTER.fetch_add(1, Ordering::Relaxed));
    }

    fn blanket_impl();
}

struct Ty1 {}
struct Ty2 {}

impl<T> Tr for T {
    fn blanket_impl() {
        static COUNTER: AtomicUsize = AtomicUsize::new(0);
        println!("blanket_impl: counter was {}", COUNTER.fetch_add(1, Ordering::Relaxed));
    }
}

fn main() {
    <Ty1 as Tr>::default_impl();
    <Ty2 as Tr>::default_impl();
    <Ty1 as Tr>::blanket_impl();
    <Ty2 as Tr>::blanket_impl();
}
```

会打印

```text
default_impl: counter was 0
default_impl: counter was 1
blanket_impl: counter was 0
blanket_impl: counter was 1
```

r[items.static.mut]
## 可变静态项

r[items.static.mut.intro]
若静态项用 `mut` 关键字声明，则程序允许修改它。Rust 的目标之一是让并发缺陷难以碰上，而这显然是竞态条件或其他缺陷的一个很大来源。

r[items.static.mut.safety]
因此，读取或写入可变静态变量都需要 `unsafe` 块。应当小心确保对可变静态项的修改相对于同一进程中运行的其他线程是安全的。

r[items.static.mut.extern]
不过，可变静态项仍然非常有用。它们可以与 C 库一起使用，也可以在 `extern` 块中从 C 库绑定。

```rust
## fn atomic_add(_: *mut u32, _: u32) -> u32 { 2 }

static mut LEVELS: u32 = 0;

// 这违反了“没有共享状态”的理念，并且内部并不
// 防止竞态，因此此函数是 `unsafe` 的
unsafe fn bump_levels_unsafe() -> u32 {
    unsafe {
        let ret = LEVELS;
        LEVELS += 1;
        return ret;
    }
}

// 作为 `bump_levels_unsafe` 的替代，此函数是安全的，前提是我们
// 有一个返回旧值的 atomic_add 函数。此函数仅在没有其他代码以
// 非原子方式访问该静态项时才是安全的。若可能存在此类访问
// （例如在 `bump_levels_unsafe` 中），则这需要是 `unsafe` 的，
// 以向调用者表明他们仍须防范并发访问。
fn bump_levels_safe() -> u32 {
    unsafe {
        return atomic_add(&raw mut LEVELS, 1);
    }
}
```

r[items.static.mut.sync]
可变静态项与普通静态项具有相同的限制，只不过类型不必实现 `Sync` trait。

r[items.static.alternate]
## 使用静态项还是常量

应该使用常量项还是静态项可能会令人困惑。一般来说，应优先选择常量而非静态项，除非下列情况之一为真：

* 存储了大量数据。
* 需要静态项的“单一地址”性质。
* 需要内部可变性。

[constant]: constant-items.md
[`drop`]: ../destructors.md
[constant expression]: ../const_eval.md#constant-expressions
[external block]: external-blocks.md
[interior mutable]: ../interior-mutability.md
[value namespace]: ../names/namespaces.md
[promoteds]: ../destructors.md#constant-promotion
