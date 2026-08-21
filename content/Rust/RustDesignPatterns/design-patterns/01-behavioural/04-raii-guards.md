+++
title = "04-RAII 守卫"
date = 2026-08-18T22:10:00+08:00
weight = 28
type = "docs"
description = "RAII 守卫 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/patterns/behavioural/RAII.html](https://rust-unofficial.github.io/patterns/patterns/behavioural/RAII.html)

# RAII 守卫

## 描述 {#description}

[RAII][wikipedia] 代表 “Resource Acquisition is Initialisation”（资源获取即初始化），这是个糟糕的名字。该模式的本质是：资源初始化在对象的构造器中完成，收尾在析构器中完成。在 Rust 中，该模式被扩展为：用 RAII 对象作为某种资源的守卫，并依赖类型系统确保访问始终经由守卫对象中介。

## 示例 {#example}

互斥锁守卫是标准库中该模式的经典例子（这是真实实现的简化版）：

```rust,ignore
use std::ops::Deref;

struct Foo {}

struct Mutex<T> {
    // 此处保存对数据 T 的引用。
    //..
}

struct MutexGuard<'a, T: 'a> {
    data: &'a T,
    //..
}

// 加锁是显式的。
impl<T> Mutex<T> {
    fn lock(&self) -> MutexGuard<T> {
        // 锁定底层操作系统互斥锁。
        //..

        // MutexGuard 保存对 self 的引用
        MutexGuard {
            data: self,
            //..
        }
    }
}

// 用于解锁互斥锁的析构器。
impl<'a, T> Drop for MutexGuard<'a, T> {
    fn drop(&mut self) {
        // 解锁底层操作系统互斥锁。
        //..
    }
}

// 实现 Deref 意味着我们可以把 MutexGuard 当作指向 T 的指针来用。
impl<'a, T> Deref for MutexGuard<'a, T> {
    type Target = T;

    fn deref(&self) -> &T {
        self.data
    }
}

fn baz(x: Mutex<Foo>) {
    let xx = x.lock();
    xx.foo(); // foo 是 Foo 上的方法。
              // 借用检查器确保我们无法保存对底层
              // Foo 的引用，使其生命周期超过守卫 xx。

    // 退出此函数并执行 xx 的析构器时，x 会被解锁。
}
```

## 动机 {#motivation}

当资源必须在使用后收尾时，可以用 RAII 来完成收尾。如果在收尾之后再访问该资源是错误的，那么可以用此模式防止这类错误。

## 优点 {#advantages}

防止资源未收尾，以及资源在收尾之后仍被使用的错误。

## 讨论 {#discussion}

RAII 是确保资源被正确释放或收尾的有用模式。我们可以利用 Rust 的借用检查器，在静态层面防止收尾发生后仍使用资源所导致的错误。

借用检查器的核心目标是确保对数据的引用不会比该数据活得更久。RAII 守卫模式之所以有效，是因为守卫对象包含对底层资源的引用，并且只暴露这类引用。Rust 确保守卫不能比底层资源活得更久，经由守卫中介的资源引用也不能比守卫活得更久。要看清这一点，查看不做生命周期省略的 `deref` 签名会有帮助：

```rust,ignore
fn deref<'a>(&'a self) -> &'a T {
    //..
}
```

返回的资源引用与 `self` 具有相同的生命周期（`'a`）。因此借用检查器会确保对 `T` 的引用的生命周期短于 `self` 的生命周期。

注意，实现 `Deref` 并不是该模式的核心部分，它只是让守卫对象用起来更符合人体工学。在守卫上实现 `get` 方法同样可行。

## 参见 {#see-also}

[析构器中的收尾](../../idioms/06-finalisation-in-destructors/)

RAII 是 C++ 中的常见模式：
[cppreference.com](http://en.cppreference.com/w/cpp/language/raii)，
[wikipedia][wikipedia]。

[wikipedia]: https://en.wikipedia.org/wiki/Resource_Acquisition_Is_Initialization

[风格指南条目](https://doc.rust-lang.org/1.0.0/style/ownership/raii.html)
（目前只是占位）。
