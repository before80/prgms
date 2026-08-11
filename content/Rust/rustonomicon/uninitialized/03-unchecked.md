+++
title = "5.3 未受检的未初始化"
date = 2026-08-06T17:08:00+08:00
weight = 30
type = "docs"
description = "未受检地处理未初始化内存"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 未受检的未初始化


> 原文链接: [https://doc.rust-lang.org/nomicon/unchecked-uninit.html](https://doc.rust-lang.org/nomicon/unchecked-uninit.html)


　　此规则的一个有趣例外是处理数组。Safe Rust 不允许部分初始化数组。初始化数组时，要么用 `let x = [val; N]` 把所有元素设为同一值，要么用 `let x = [val1, val2, val3]` 逐个指定。遗憾的是这相当死板，尤其需要更渐进或动态方式初始化数组时。

　　Unsafe Rust 提供强大工具：[`MaybeUninit`]。此类型可处理尚未完全初始化的内存。

　　用 `MaybeUninit` 可逐元素初始化数组：

```rust
use std::mem::{self, MaybeUninit};

// 数组大小硬编码但易改（只改常量即可）。因此不能用 [a, b, c] 语法初始化，
// 否则须与 `SIZE` 保持同步！
const SIZE: usize = 10;

let x = {
    // 创建 `MaybeUninit` 的未初始化数组。
    let mut x = [const { MaybeUninit::uninit() }; SIZE];

    // drop `MaybeUninit` 什么都不做。因此用裸指针赋值而非 `ptr::write`
    // 不会导致旧的未初始化值被 drop。
    // 异常安全不是问题，因为 Box 不会 panic
    for i in 0..SIZE {
        x[i] = MaybeUninit::new(Box::new(i as u32));
    }

    // 一切已初始化。transmute 数组为已初始化类型。
    unsafe { mem::transmute::<_, [Box<u32>; SIZE]>(x) }
};

println!("{x:?}");
```

　　此代码分三步：

1. 创建 `MaybeUninit<T>` 数组。

2. 初始化数组。微妙之处在于：通常用 `=` 赋给 Rust 类型检查器认为已初始化的值（如 `x[i]`）时，左侧旧值会被 drop。那会是灾难。但此例左侧类型是 `MaybeUninit<Box<u32>>`，drop 它什么都不做！见下文关于此 `drop` 问题的更多讨论。

3. 最后须改变数组类型以移除 `MaybeUninit`。当前 stable Rust 需要 `transmute`。
　　   此 transmute 合法，因为在内存中 `MaybeUninit<T>` 与 `T` 看起来相同。

　　    但注意，一般而言 `Container<MaybeUninit<T>>` *不*与 `Container<T>` 相同！想象 `Container` 是 `Option`，`T` 是 `bool`，则 `Option<bool>` 利用 `bool` 只有两个有效值，但 `Option<MaybeUninit<bool>>` 不能，因为 `bool` 不必已初始化。

　　    因此能否 transmute 掉 `MaybeUninit` 取决于 `Container`。对数组可以（标准库最终会提供相应方法）。

　　值得多花点时间看中间循环，以及赋值运算符与 `drop` 的交互。若写成：

```rust,ignore
*x[i].as_mut_ptr() = Box::new(i as u32); // 错误！
```

　　会实际覆盖 `Box<u32>`，导致 drop 未初始化数据，造成巨大痛苦。

　　正确替代（若因某种原因不能用 `MaybeUninit::new`）是使用 [`ptr`] 模块。它提供三个函数，可在不 drop 旧值的情况下向内存位置写入字节：[`write`]、[`copy`]、[`copy_nonoverlapping`]。

* `ptr::write(ptr, val)` 取 `val` 并 move 到 `ptr` 指向的地址。
* `ptr::copy(src, dest, count)` 复制 `count` 个 `T` 项占用的比特从 src 到 dest。（等价于 C 的 memmove——注意参数顺序相反！）
* `ptr::copy_nonoverlapping(src, dest, count)` 与 `copy` 相同，但在假设两段内存不重叠时稍快。（等价于 C 的 memcpy——注意参数顺序相反！）

　　不用说，误用这些函数会导致严重灾难或直接未定义行为。这些函数*本身*的唯一要求是读写的位置已分配且正确对齐。然而向内存任意位置写入任意比特破坏事物的方式简直不可计数！

　　值得注意的是，对不实现 `Drop` 或不包含 `Drop` 类型的类型，不必担心 `ptr::write` 式花招，因为 Rust 知道不要尝试 drop 它们。上面例子正是依赖这一点。

　　但处理未初始化内存时，须时刻警惕 Rust 在完全初始化前 drop 你构造的值。若值有析构函数，该变量作用域的每条控制路径在结束前必须初始化它。
　　*[这包括代码 panic](../unwinding/_index.html)*。`MaybeUninit` 略有帮助，因为它不隐式 drop 内容——但 panic 时这意味着不是 double-free 未初始化部分，而是已初始化部分的内存泄漏。

　　注意，要使用 `ptr` 方法，须先获得要初始化数据的*裸指针*。构造*引用*指向未初始化数据是非法的，因此获取裸指针时须谨慎：

* 对 `T` 数组，可用 `base_ptr.add(idx)`，其中 `base_ptr: *mut T` 计算索引 `idx` 的地址。这依赖数组在内存中的布局。
* 但对结构体，通常不知道布局，也不能用 `&mut base_ptr.field`，因为那会创建引用。因此须谨慎使用[裸引用][raw_reference]语法。这在不创建中间引用的情况下创建字段的裸指针：

```rust
use std::{ptr, mem::MaybeUninit};

struct Demo {
    field: bool,
}

let mut uninit = MaybeUninit::<Demo>::uninit();
// `&uninit.as_mut().field` 会创建指向未初始化 `bool` 的引用，因此是未定义行为！
let f1_ptr = unsafe { &raw mut (*uninit.as_mut_ptr()).field };
unsafe { f1_ptr.write(true); }

let init = unsafe { uninit.assume_init() };
```

　　最后说明：阅读旧 Rust 代码时可能遇到已弃用的 `mem::uninitialized`。它曾是栈上处理未初始化内存的唯一方式，但证明无法与语言其余部分正确集成。新代码应始终使用 `MaybeUninit`，有机会时把旧代码迁移过来。

　　以上就是处理未初始化内存的全部！基本上没有任何地方期望收到未初始化内存，若要传递，务必*格外*小心。

[`MaybeUninit`]: ../core/mem/union.MaybeUninit.html
[`ptr`]: ../core/ptr/index.html
[raw_reference]: ../reference/types/pointer.html#r-type.pointer.raw.constructor
[`write`]: ../core/ptr/fn.write.html
[`copy`]: ../std/ptr/fn.copy.html
[`copy_nonoverlapping`]: ../std/ptr/fn.copy_nonoverlapping.html
