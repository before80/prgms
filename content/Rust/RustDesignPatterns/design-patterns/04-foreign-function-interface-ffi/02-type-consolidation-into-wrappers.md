+++
title = "02-将类型收拢到包装器中"
date = 2026-08-18T22:10:00+08:00
weight = 41
type = "docs"
description = "将类型收拢到包装器中 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/patterns/ffi/wrappers.html](https://rust-unofficial.github.io/patterns/patterns/ffi/wrappers.html)

# 将类型收拢到包装器中

## 描述 {#description}

此模式旨在优雅地处理多个相关类型，同时尽量缩小内存不安全的表面积。

Rust 别名规则的基石之一是生命周期。这确保了许多类型间的访问模式可以是内存安全的，也包括数据竞争安全。

然而，当 Rust 类型导出到其他语言时，它们通常被转换为指针。在 Rust 中，指针意味着“用户管理被指对象的生命周期。”避免内存不安全是他们的责任。

因此需要对用户代码有一定程度的信任，尤其是围绕释放后使用——对此 Rust 无能为力。然而，某些 API 设计比其他设计给用其他语言编写的代码施加更重的负担。

风险最低的 API 是“合并包装器”：与对象的所有可能交互都收拢进一个“包装器类型”，同时保持 Rust API 干净。

## 代码示例 {#code-example}

为理解这一点，让我们看一个经典的待导出 API 示例：遍历集合。

该 API 如下：

1. 用 `first_key` 初始化迭代器。
2. 每次调用 `next_key` 会推进迭代器。
3. 若迭代器已到末尾，调用 `next_key` 不做任何事。
4. 如上所述，迭代器被“包装进”集合（与原生 Rust API 不同）。

若迭代器高效实现了 `nth()`，则有可能使其对每次函数调用都是短暂的：

```rust,ignore
struct MySetWrapper {
    myset: MySet,
    iter_next: usize,
}

impl MySetWrapper {
    pub fn first_key(&mut self) -> Option<&Key> {
        self.iter_next = 0;
        self.next_key()
    }
    pub fn next_key(&mut self) -> Option<&Key> {
        if let Some(next) = self.myset.keys().nth(self.iter_next) {
            self.iter_next += 1;
            Some(next)
        } else {
            None
        }
    }
}
```

结果是包装器简单且不含 `unsafe` 代码。

## 优点 {#advantages}

这使 API 使用更安全，避免类型间生命周期问题。关于其优点以及它所避免的陷阱，参见
[基于对象的 API](01-object-based-apis/)。

## 缺点 {#disadvantages}

通常，包装类型相当困难，有时对 Rust API 做折衷会使事情更容易。

例如，考虑一个未高效实现 `nth()` 的迭代器。绝对值得加入特殊逻辑，让对象在内部处理迭代，或高效支持仅外部函数 API 会使用的不同访问模式。

### 试图包装迭代器（并失败） {#trying-to-wrap-iterators-and-failing}

要正确地将任意类型的迭代器包装进 API，包装器需要做 C 版代码会做的事：擦除迭代器的生命周期，并手动管理它。

可以说，这 *极其* 困难。

下面说明 *其中* 一个陷阱。

`MySetWrapper` 的第一版会像这样：

```rust,ignore
struct MySetWrapper {
    myset: MySet,
    iter_next: usize,
    // 由 transmute 后的 Box<KeysIter + 'self> 创建
    iterator: Option<NonNull<KeysIter<'static>>>,
}
```

使用 `transmute` 来延长生命周期，并用指针隐藏它，已经很丑陋了。但更糟的是：*任何其他操作都可能导致 Rust `undefined behaviour`*。

考虑包装器中的 `MySet` 可能在迭代期间被其他函数操纵，例如向它正在迭代的键存储新值。API 并不劝阻这一点，事实上一些类似的 C 库期望如此。

`myset_store` 的一个简单实现会是：

```rust,ignore
pub mod unsafe_module {

    // 模块的其他内容

    pub fn myset_store(myset: *mut MySetWrapper, key: datum, value: datum) -> libc::c_int {
        // 不要使用此代码。它不安全，仅用于演示问题。

        let myset: &mut MySet = unsafe {
            // SAFETY: 哎呀，UB 发生在这里！
            &mut (*myset).myset
        };

        /* ...检查并转换 key 与 value 数据... */

        match myset.store(casted_key, casted_value) {
            Ok(_) => 0,
            Err(e) => e.into(),
        }
    }
}
```

若调用此函数时迭代器仍然存在，我们就违反了 Rust 的一条别名规则。根据 Rust，此块中的可变引用必须对该对象有 *独占* 访问。若迭代器仅仅存在，就不是独占，于是我们有了 `undefined behaviour`！[^1]

为避免这一点，我们必须有办法确保可变引用确实是独占的。那基本上意味着在共享引用存在时清除迭代器的共享引用，然后再重建它。在多数情况下，这仍会比 C 版本更低效。

有人可能问：C 怎么能做得更高效？答案是，它作弊了。Rust 的别名规则才是问题，而 C 对指针干脆忽略它们。作为交换，手册中常见声明在某些或所有情况下“非线程安全”的代码。事实上，
[GNU C 库](https://manpages.debian.org/buster/manpages/attributes.7.en.html)
有一整套专门描述并发行为的术语！

Rust 更希望在任何时候都保持一切内存安全，既为了安全，也为了 C 代码无法达到的优化。被拒绝使用某些捷径，是 Rust 程序员需要付出的代价。

[^1]: 对于为此挠头的 C 程序员：迭代器不必在此代码 *期间* 被读取才会造成 UB。独占规则也启用了可能使迭代器共享引用观察到不一致结果的编译器优化（例如为效率而将寄存器溢出到栈，或重排指令）。这些观察可能发生在可变引用创建 *之后的任何时刻*。
