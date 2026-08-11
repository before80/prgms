+++
title = "10.1.3 克隆"
date = 2026-08-06T17:08:00+08:00
weight = 58
type = "docs"
description = "Arc 的 Clone"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 克隆


> 原文链接: [https://doc.rust-lang.org/nomicon/arc-mutex/arc-clone.html](https://doc.rust-lang.org/nomicon/arc-mutex/arc-clone.html)


　　基础代码有了，接下来要能 clone `Arc`。

　　基本上需要：

1. 递增原子引用计数
2. 用内部指针构造新的 `Arc` 实例

　　首先访问 `ArcInner`：

```rust,ignore
let inner = unsafe { self.ptr.as_ref() };
```

　　更新原子引用计数：

```rust,ignore
let old_rc = inner.rc.fetch_add(1, Ordering::???);
```

　　这里该用什么 ordering？clone 时我们实际上没有需要原子同步的代码，因为 clone 期间不修改内部值。因此可用 Relaxed ordering，表示没有 happens-before 关系但仍是原子的。但在 `Drop` `Arc` 时，递减引用计数需要原子同步。详见 [`Arc` 的 `Drop` 实现一节](arc-drop.md)。关于原子关系与 Relaxed ordering，见[原子操作一节](../atomics.md)。

　　因此代码变为：

```rust,ignore
let old_rc = inner.rc.fetch_add(1, Ordering::Relaxed);
```

　　需要再导入 `Ordering`：

```rust
use std::sync::atomic::Ordering;
```

　　但当前实现有一个问题。若有人对一堆 `Arc` 调用 `mem::forget` 呢？迄今的代码（以及将要写的）假设引用计数准确反映内存中有多少个 `Arc`，但 `mem::forget` 会让这不再成立。因此从这个 `Arc` clone 出越来越多 `Arc` 却不 `Drop`、不递减引用计数时，可能溢出！这会导致释放后使用，**极其糟糕！**

　　为此需要检查引用计数不超过某个任意值（低于 `usize::MAX`，因为我们用 `AtomicUsize` 存引用计数），并*做点什么*。

　　标准库实现选择在任意线程上引用计数达到 `isize::MAX`（约为 `usize::MAX` 的一半）时直接 abort 程序（正常代码中极不可能，若发生则程序可能极度病态），假设不会有约 20 亿个线程（在部分 64 位机器上约为 **9 quintillion**）同时递增引用计数。我们采用同样策略。

　　实现很简单：

```rust,ignore
if old_rc >= isize::MAX as usize {
    std::process::abort();
}
```

　　然后返回新的 `Arc` 实例：

```rust,ignore
Self {
    ptr: self.ptr,
    phantom: PhantomData
}
```

　　把这些包进 `Clone` 实现：

```rust,ignore
use std::sync::atomic::Ordering;

impl<T> Clone for Arc<T> {
    fn clone(&self) -> Arc<T> {
        let inner = unsafe { self.ptr.as_ref() };
        // 这里用 relaxed ordering 没问题，因为我们不需要任何原子
        // 同步——不修改也不访问内部数据。
        let old_rc = inner.rc.fetch_add(1, Ordering::Relaxed);

        if old_rc >= isize::MAX as usize {
            std::process::abort();
        }

        Self {
            ptr: self.ptr,
            phantom: PhantomData,
        }
    }
}
```
