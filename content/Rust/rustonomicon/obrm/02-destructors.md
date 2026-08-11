+++
title = "6.2 析构函数"
date = 2026-08-06T17:08:00+08:00
weight = 33
type = "docs"
description = "Drop 与析构语义"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 析构函数


> 原文链接: [https://doc.rust-lang.org/nomicon/destructors.html](https://doc.rust-lang.org/nomicon/destructors.html)


　　语言*确实*提供通过 `Drop` trait 的完整自动析构函数，提供如下方法：

```rust,ignore
fn drop(&mut self);
```

　　此方法让类型有时间完成正在做的事。

　　**`drop` 运行后，Rust 会递归尝试 drop `self` 的所有字段。**

　　这是便利特性，免得你为 drop 子项写「析构样板」。若结构体除 drop 子项外没有特殊 drop 逻辑，则完全不必实现 `Drop`！

　　**Rust 1.0 中没有稳定方式阻止此行为。**

　　注意取 `&mut self` 意味着即使能抑制递归 Drop，Rust 也会阻止你从 self move 字段等。对大多数类型完全没问题。

　　例如自定义 `Box` 的 `Drop` 可写成：

```rust
#![feature(ptr_internals, allocator_api)]

use std::alloc::{Allocator, Global, GlobalAlloc, Layout};
use std::mem;
use std::ptr::{drop_in_place, NonNull, Unique};

struct Box<T>{ ptr: Unique<T> }

impl<T> Drop for Box<T> {
    fn drop(&mut self) {
        unsafe {
            drop_in_place(self.ptr.as_ptr());
            let c: NonNull<T> = self.ptr.into();
            Global.deallocate(c.cast(), Layout::new::<T>())
        }
    }
}
# fn main() {}
```

　　这工作良好，因为 Rust drop `ptr` 字段时只看到没有实际 `Drop` 实现的 [Unique]。同样，drop 退出后无法再对 `ptr` 进行 use-after-free。

　　但这不行：

```rust
#![feature(allocator_api, ptr_internals)]

use std::alloc::{Allocator, Global, GlobalAlloc, Layout};
use std::ptr::{drop_in_place, Unique, NonNull};
use std::mem;

struct Box<T>{ ptr: Unique<T> }

impl<T> Drop for Box<T> {
    fn drop(&mut self) {
        unsafe {
            drop_in_place(self.ptr.as_ptr());
            let c: NonNull<T> = self.ptr.into();
            Global.deallocate(c.cast(), Layout::new::<T>());
        }
    }
}

struct SuperBox<T> { my_box: Box<T> }

impl<T> Drop for SuperBox<T> {
    fn drop(&mut self) {
        unsafe {
            // 超优化：替 box 释放其内容，
            // 而不 `drop` 内容
            let c: NonNull<T> = self.my_box.ptr.into();
            Global.deallocate(c.cast::<u8>(), Layout::new::<T>());
        }
    }
}
# fn main() {}
```

　　在 SuperBox 析构函数中释放 box 的 ptr 后，Rust 会继续让 box Drop 自身，一切会因 use-after-free 和 double-free 而崩溃。

　　注意递归 drop 行为适用于所有 struct 和 enum，无论是否实现 Drop。因此

```rust
struct Boxy<T> {
    data1: Box<T>,
    data2: Box<T>,
    info: u32,
}
```

　　在「应当」被 drop 时，`data1` 和 `data2` 字段的析构函数会被调用，即使它自身不实现 Drop。我们说此类类型*需要 Drop*，尽管它本身不是 Drop。

　　同样，

```rust
enum Link {
    Next(Box<Link>),
    None,
}
```

　　当且仅当实例存储 Next 变体时，内部 Box 字段会被 drop。

　　通常这工作得很好，因为重构数据布局时不必操心增删 drop。但仍有许多合理用例需要在析构上做更复杂的事。

　　覆盖递归 drop 并在 `drop` 期间允许 move 出 Self 的经典 safe 解法是用 `Option`：

```rust
#![feature(allocator_api, ptr_internals)]

use std::alloc::{Allocator, GlobalAlloc, Global, Layout};
use std::ptr::{drop_in_place, Unique, NonNull};
use std::mem;

struct Box<T>{ ptr: Unique<T> }

impl<T> Drop for Box<T> {
    fn drop(&mut self) {
        unsafe {
            drop_in_place(self.ptr.as_ptr());
            let c: NonNull<T> = self.ptr.into();
            Global.deallocate(c.cast(), Layout::new::<T>());
        }
    }
}

struct SuperBox<T> { my_box: Option<Box<T>> }

impl<T> Drop for SuperBox<T> {
    fn drop(&mut self) {
        unsafe {
            // 超优化：替 box 释放其内容，
            // 而不 `drop` 内容。须把 `box` 字段设为 `None`，
            // 防止 Rust 尝试 Drop 它。
            let my_box = self.my_box.take().unwrap();
            let c: NonNull<T> = my_box.ptr.into();
            Global.deallocate(c.cast(), Layout::new::<T>());
            mem::forget(my_box);
        }
    }
}
# fn main() {}
```

　　但这语义相当奇怪：你说*应*始终为 Some 的字段*可能*为 None，只因析构函数中的行为。当然反过来也说得通：析构期间可对 self 调用任意方法，这应阻止你在字段去初始化后再这么做。当然它不会阻止你在其中产生任意其他无效状态。

　　总体而言这是可接受的选择，默认应选此方案。
　　不过未来我们期望有一等方式声明字段不应自动 drop。

[Unique]: ../ownership/10-phantom-data.html
