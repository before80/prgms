+++
title = "07-集合"
date = 2026-08-01T10:38:00+08:00
weight = 102
type = "docs"
description = "集合（Collections）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 集合 {#collections}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/collections/](https://doc.rust-lang.org/stable/embedded-book/collections/)


最终你会想在程序中使用动态数据结构（也就是集合）。`std` 提供了一组常见集合：[`Vec`]、[`String`]、[`HashMap`] 等。`std` 中实现的所有集合都使用全局动态内存分配器（也就是堆）。

[`Vec`]: https://doc.rust-lang.org/std/vec/struct.Vec.html
[`String`]: https://doc.rust-lang.org/std/string/struct.String.html
[`HashMap`]: https://doc.rust-lang.org/std/collections/struct.HashMap.html

由于 `core` 按定义不包含内存分配，这些实现在那里不可用，但可以在随编译器一起提供的 `alloc` crate 中找到。

如果你需要集合，基于堆分配的实现并非唯一选择。你也可以使用*固定容量*集合；[`heapless`] crate 中就有这样一种实现。

[`heapless`]: https://crates.io/crates/heapless

在本节中，我们将探索并比较这两种实现。

## 使用 `alloc` {#using-alloc}

`alloc` crate 随标准 Rust 发行版一起提供。要导入该 crate，你可以直接 `use` 它，*无需*在 `Cargo.toml` 文件中声明为依赖。

``` rust,ignore
#![feature(alloc)]

extern crate alloc;

use alloc::vec::Vec;
```

要使用任何集合，你首先需要用 `global_allocator` 属性声明程序将使用的全局分配器。你选择的分配器必须实现 [`GlobalAlloc`] trait。

[`GlobalAlloc`]: https://doc.rust-lang.org/core/alloc/trait.GlobalAlloc.html

为了完整起见，并让本节尽可能自成一体，我们将实现一个简单的 bump pointer 分配器，并用它作为全局分配器。不过，我们*强烈*建议你在程序中使用 crates.io 上久经考验的分配器，而不是这个分配器。

``` rust,ignore
// 指针碰撞（bump pointer）分配器实现

use core::alloc::{GlobalAlloc, Layout};
use core::cell::UnsafeCell;
use core::ptr;

use cortex_m::interrupt;

// 用于*单*核系统的 bump pointer 分配器
struct BumpPointerAlloc {
    head: UnsafeCell<usize>,
    end: usize,
}

unsafe impl Sync for BumpPointerAlloc {}

unsafe impl GlobalAlloc for BumpPointerAlloc {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        // `interrupt::free` 是临界区，使我们的分配器
        // 可从中断中安全使用
        interrupt::free(|_| {
            let head = self.head.get();
            let size = layout.size();
            let align = layout.align();
            let align_mask = !(align - 1);

            // 把 start 上移到下一个对齐边界
            let start = (*head + align - 1) & align_mask;

            if start + size > self.end {
                // 空指针表示内存不足（Out Of Memory）
                ptr::null_mut()
            } else {
                *head = start + size;
                start as *mut u8
            }
        })
    }

    unsafe fn dealloc(&self, _: *mut u8, _: Layout) {
        // 此分配器从不释放内存
    }
}

// 声明全局内存分配器
// 注意：用户必须确保内存区域 `[0x2000_0100, 0x2000_0200]`
// 不被程序其他部分使用
#[global_allocator]
static HEAP: BumpPointerAlloc = BumpPointerAlloc {
    head: UnsafeCell::new(0x2000_0100),
    end: 0x2000_0200,
};
```

除了选择全局分配器外，用户还必须用*不稳定*的 `alloc_error_handler` 属性定义如何处理内存不足（OOM）错误。

``` rust,ignore
#![feature(alloc_error_handler)]

use cortex_m::asm;

#[alloc_error_handler]
fn on_oom(_layout: Layout) -> ! {
    asm::bkpt();

    loop {}
}
```

一旦这些都就绪，用户终于可以使用 `alloc` 中的集合了。

```rust,ignore
#[entry]
fn main() -> ! {
    let mut xs = Vec::new();

    xs.push(42);
    assert!(xs.pop(), Some(42));

    loop {
        // ..
    }
}
```

如果你用过 `std` crate 中的集合，这些会很熟悉，因为它们是完全相同的实现。

## 使用 `heapless` {#using-heapless}

`heapless` 无需设置，因为它的集合不依赖全局内存分配器。只需 `use` 其集合并着手实例化它们：

```rust,ignore
// heapless 版本：v0.4.x
use heapless::Vec;
use heapless::consts::*;

#[entry]
fn main() -> ! {
    let mut xs: Vec<_, U8> = Vec::new();

    xs.push(42).unwrap();
    assert_eq!(xs.pop(), Some(42));
    loop {}
}
```

你会注意到这些集合与 `alloc` 中的集合有两处不同。

首先，你必须事先声明集合的容量。`heapless` 集合从不重新分配，且容量固定；该容量是集合类型签名的一部分。在本例中我们声明 `xs` 的容量为 8 个元素，即该向量最多可容纳 8 个元素。这由类型签名中的 `U8`（见 [`typenum`]）表示。

[`typenum`]: https://crates.io/crates/typenum

其次，`push` 方法以及许多其他方法会返回 `Result`。由于 `heapless` 集合容量固定，所有向集合插入元素的操作都可能失败。API 通过返回 `Result` 来反映这一问题，以表明操作是否成功。相比之下，`alloc` 集合会在堆上重新分配自身以增大容量。

截至 v0.4.x 版本，所有 `heapless` 集合都内联存储其全部元素。这意味着像 `let x = heapless::Vec::new();` 这样的操作会在栈上分配集合，但也可以把集合分配在 `static` 变量上，甚至在堆上（`Box<Vec<_, _>>`）。

## 权衡 {#trade-offs}

在堆分配、可重定位的集合与固定容量集合之间做选择时，请牢记以下几点。

### 内存不足与错误处理 {#out-of-memory-and-error-handling}

使用堆分配时，内存不足始终可能发生，并且可能出现在集合可能需要增长的任何地方：例如，所有 `alloc::Vec.push` 调用都可能产生 OOM 条件。因此某些操作可能*隐式*失败。一些 `alloc` 集合暴露了 `try_reserve` 方法，让你在增长集合时检查潜在的 OOM 条件，但你需要主动使用它们。

若你只使用 `heapless` 集合，并且不为其他任何事情使用内存分配器，则不可能出现 OOM 条件。相反，你必须逐个处理集合容量耗尽的情况。也就是说，你必须处理像 `Vec.push` 这类方法返回的*所有* `Result`。

OOM 失败可能比说对 `heapless::Vec.push` 返回的所有 `Result` 做 `unwrap` 更难调试，因为观察到的失败位置可能*并不*与问题原因的位置一致。例如，即使 `vec.reserve(1)` 也可能在分配器接近耗尽时触发 OOM，原因是某个其他集合在泄漏内存（安全 Rust 中也可能发生内存泄漏）。

### 内存使用 {#memory-usage}

推理堆分配集合的内存使用很难，因为长生命周期集合的容量可能在运行时变化。某些操作可能隐式重新分配集合从而增加其内存使用，有些集合还暴露了像 `shrink_to_fit` 这样可能减少集合所用内存的方法 —— 最终是否真的缩小内存分配取决于分配器。此外，分配器可能还要处理内存碎片，这会增加*表观*内存使用量。

另一方面，若你只使用固定容量集合，把它们大多存放在 `static` 变量中，并为调用栈设置最大大小，那么如果你试图使用超过物理可用的内存，链接器就会检测出来。

此外，分配在栈上的固定容量集合会由 [`-Z emit-stack-sizes`] 标志报告，这意味着分析栈使用的工具（如 [`stack-sizes`]）会把它们纳入分析。

[`-Z emit-stack-sizes`]: https://doc.rust-lang.org/beta/unstable-book/compiler-flags/emit-stack-sizes.html
[`stack-sizes`]: https://crates.io/crates/stack-sizes

不过，固定容量集合*不能*缩小，这可能导致装载因子（集合大小与其容量之比）低于可重定位集合所能达到的水平。

### 最坏情况执行时间（WCET） {#worst-case-execution-time-wcet}

若你在构建时间敏感的应用或硬实时应用，那么你关心 —— 或许非常关心 —— 程序不同部分的最坏情况执行时间。

`alloc` 集合可以重新分配，因此可能增长集合的操作的 WCET 还会包含重新分配集合所花的时间，而这本身又取决于集合的*运行时*容量。这使得很难确定例如 `alloc::Vec.push` 操作的 WCET，因为它既取决于所用的分配器，也取决于其运行时容量。

另一方面，固定容量集合从不重新分配，因此所有操作都有可预测的执行时间。例如，`heapless::Vec.push` 以常数时间执行。

### 易用性 {#ease-of-use}

`alloc` 需要设置全局分配器，而 `heapless` 不需要。不过，`heapless` 要求你为实例化的每个集合选择容量。

`alloc` API 对几乎每一位 Rust 开发者都是熟悉的。`heapless` API 试图紧密模仿 `alloc` API，但由于其显式错误处理，永远不会完全相同 —— 有些开发者可能觉得显式错误处理过度或过于繁琐。
