+++
title = "10.1.2 基础代码"
date = 2026-08-06T17:08:00+08:00
weight = 57
type = "docs"
description = "Arc 的基础实现"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 基础代码


> 原文链接: [https://doc.rust-lang.org/nomicon/arc-mutex/arc-base.html](https://doc.rust-lang.org/nomicon/arc-mutex/arc-base.html)


　　布局已定，来写 `Arc` 的基础代码。

## 构造 Arc

　　首先要有构造 `Arc<T>` 的方式。

　　这很简单：把 `ArcInner<T>` box 起来，得到指向它的 `NonNull<T>` 指针。

```rust,ignore
impl<T> Arc<T> {
    pub fn new(data: T) -> Arc<T> {
        // 引用计数从 1 开始，因为第一个引用就是当前指针。
        let boxed = Box::new(ArcInner {
            rc: AtomicUsize::new(1),
            data,
        });
        Arc {
            // 这里调用 `.unwrap()` 没问题，因为 `Box::into_raw`
            // 返回的指针保证非 null。
            ptr: NonNull::new(Box::into_raw(boxed)).unwrap(),
            phantom: PhantomData,
        }
    }
}
```

## Send 与 Sync

　　我们在做并发原语，需要能跨线程发送。因此可实现 `Send` 与 `Sync` 标记 trait。更多信息见 [`Send` 与 `Sync` 一节](../send-and-sync.md)。

　　这样是合理的，因为：
* 仅当且仅当它是引用该数据的唯一 `Arc` 时（只在 `Drop` 中发生），才能拿到 `Arc` 内部值的可变引用
* 我们对共享可变引用计数使用原子操作

```rust,ignore
unsafe impl<T: Sync + Send> Send for Arc<T> {}
unsafe impl<T: Sync + Send> Sync for Arc<T> {}
```

　　需要 `T: Sync + Send` 边界，否则可能通过 `Arc` 跨线程边界共享线程不安全的值，导致数据竞争或不健全。

　　例如，若没有这些边界，`Arc<Rc<u32>>` 会是 `Sync` 或 `Send`，意味着可以把 `Rc` 从 `Arc` 里 clone 出来跨线程发送（而不创建全新的 `Rc`），而 `Rc` 不是线程安全的，会产生数据竞争。

## 获取 ArcInner

　　要把 `NonNull<T>` 解引用为 `&T`，可调用 `NonNull::as_ref`。这与典型的 `as_ref` 不同，是不安全的，必须这样写：

```rust,ignore
unsafe { self.ptr.as_ref() }
```

　　这段代码会多次出现（通常配合 `let` 绑定）。

　　这种不安全是合理的：只要这个 `Arc` 还活着，内部指针就有效。

## Deref

　　好。现在能构造 `Arc`（很快也能正确 clone 和销毁），如何访问内部数据？

　　需要实现 `Deref`。

　　先导入 trait：

```rust,ignore
use std::ops::Deref;
```

　　实现如下：

```rust,ignore
impl<T> Deref for Arc<T> {
    type Target = T;

    fn deref(&self) -> &T {
        let inner = unsafe { self.ptr.as_ref() };
        &inner.data
    }
}
```

　　很简单：解引用 `NonNull` 到 `ArcInner<T>`，再取内部数据的引用。

## 代码

　　本节全部代码：

```rust,ignore
use std::ops::Deref;

impl<T> Arc<T> {
    pub fn new(data: T) -> Arc<T> {
        // 引用计数从 1 开始，因为第一个引用就是当前指针。
        let boxed = Box::new(ArcInner {
            rc: AtomicUsize::new(1),
            data,
        });
        Arc {
            // 这里调用 `.unwrap()` 没问题，因为 `Box::into_raw`
            // 返回的指针保证非 null。
            ptr: NonNull::new(Box::into_raw(boxed)).unwrap(),
            phantom: PhantomData,
        }
    }
}

unsafe impl<T: Sync + Send> Send for Arc<T> {}
unsafe impl<T: Sync + Send> Sync for Arc<T> {}


impl<T> Deref for Arc<T> {
    type Target = T;

    fn deref(&self) -> &T {
        let inner = unsafe { self.ptr.as_ref() };
        &inner.data
    }
}
```
