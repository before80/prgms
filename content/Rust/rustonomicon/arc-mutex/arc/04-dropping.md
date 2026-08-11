+++
title = "10.1.4 丢弃"
date = 2026-08-06T17:08:00+08:00
weight = 59
type = "docs"
description = "Arc 的 Drop"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 丢弃


> 原文链接: [https://doc.rust-lang.org/nomicon/arc-mutex/arc-drop.html](https://doc.rust-lang.org/nomicon/arc-mutex/arc-drop.html)


　　现在需要递减引用计数，并在足够低时 drop 数据，否则数据会永远留在堆上。

　　为此实现 `Drop`。

　　基本上需要：

1. 递减引用计数
2. 若数据只剩一个引用，则：
3. 用原子 fence 防止数据使用与删除的重排序
4. drop 内部数据

　　首先访问 `ArcInner`：

```rust,ignore
let inner = unsafe { self.ptr.as_ref() };
```

　　递减引用计数。为简化代码，若 `fetch_sub` 的返回值（递减前的引用计数）不等于 `1`（表示我们不是最后一个引用），可直接返回。

```rust,ignore
if inner.rc.fetch_sub(1, Ordering::Release) != 1 {
    return;
}
```

　　然后需要原子 fence，防止数据使用与删除的重排序。如[标准库 `Arc` 实现][3]所述：

> 这个 fence 用于防止数据使用与删除的重排序。因为它标记为 `Release`，引用计数的递减与此 `Acquire` fence 同步。这意味着数据的使用发生在引用计数递减之前，引用计数递减发生在此 fence 之前，fence 发生在数据删除之前。
>
> 如 [Boost 文档][1] 所解释，
>
> > 必须强制：在一个线程中通过现有引用对对象的任何可能访问，*happens before* 在另一线程中删除该对象。这通过 drop 引用后的「release」操作（通过该引用的任何访问显然必须在此之前发生）以及删除对象前的「acquire」操作来实现。
>
> 特别地，虽然 Arc 的内容通常不可变，但可能对 `Mutex<T>` 等做内部写入。由于 Mutex 在删除时不会被 acquire，我们不能依赖其同步逻辑让线程 A 的写入对线程 B 中运行的析构函数可见。
>
> 另请注意，这里的 Acquire fence 或许可换成 Acquire load，在高竞争情况下可能提升性能。见 [2]。
>
> [1]: https://www.boost.org/doc/libs/1_55_0/doc/html/atomic/usage_examples.html
> [2]: https://github.com/rust-lang/rust/pull/41714
[3]: https://github.com/rust-lang/rust/blob/e1884a8e3c3e813aada8254edfa120e85bf5ffca/library/alloc/src/sync.rs#L1440-L1467

　　做法如下：

```rust
# use std::sync::atomic::Ordering;
use std::sync::atomic;
atomic::fence(Ordering::Acquire);
```

　　最后 drop 数据本身。用 `Box::from_raw` drop boxed 的 `ArcInner<T>` 及其数据。它接受 `*mut T` 而非 `NonNull<T>`，因此需用 `NonNull::as_ptr` 转换。

```rust,ignore
unsafe { Box::from_raw(self.ptr.as_ptr()); }
```

　　这是安全的，因为我们知道持有 `ArcInner` 的最后一个指针，且指针有效。

　　把这些包进 `Drop` 实现：

```rust,ignore
impl<T> Drop for Arc<T> {
    fn drop(&mut self) {
        let inner = unsafe { self.ptr.as_ref() };
        if inner.rc.fetch_sub(1, Ordering::Release) != 1 {
            return;
        }
        // 这个 fence 用于防止数据使用与删除的重排序。
        atomic::fence(Ordering::Acquire);
        // 这是安全的，因为我们知道持有 `ArcInner` 的最后一个指针，
        // 且指针有效。
        unsafe { Box::from_raw(self.ptr.as_ptr()); }
    }
}
```
