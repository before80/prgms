+++
title = "10.1.5 最终代码"
date = 2026-08-06T17:08:00+08:00
weight = 60
type = "docs"
description = "完整的 Arc 实现"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 最终代码


> 原文链接: [https://doc.rust-lang.org/nomicon/arc-mutex/arc-final.html](https://doc.rust-lang.org/nomicon/arc-mutex/arc-final.html)


　　最终代码，附一些注释并调整了 import 顺序：

```rust
use std::marker::PhantomData;
use std::ops::Deref;
use std::ptr::NonNull;
use std::sync::atomic::{self, AtomicUsize, Ordering};

pub struct Arc<T> {
    ptr: NonNull<ArcInner<T>>,
    phantom: PhantomData<ArcInner<T>>,
}

pub struct ArcInner<T> {
    rc: AtomicUsize,
    data: T,
}

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
