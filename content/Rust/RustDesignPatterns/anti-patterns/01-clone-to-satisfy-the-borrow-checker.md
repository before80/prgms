+++
title = "01-为通过借用检查而 Clone"
date = 2026-08-18T22:10:00+08:00
weight = 43
type = "docs"
description = "为通过借用检查而 Clone — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/anti_patterns/borrow_clone.html](https://rust-unofficial.github.io/patterns/anti_patterns/borrow_clone.html)

# 为通过借用检查而 Clone

## 描述 {#description}

借用检查器通过确保以下条件之一成立，防止 Rust 用户写出否则不安全的代码：要么只存在一个可变引用，要么可以有许多但全部都是不可变引用。若所写代码不满足这些条件，而开发者靠克隆变量来消除编译器错误，就会出现这种反模式。

## 示例 {#example}

```rust
// 定义任意变量
let mut x = 5;

// 借用 `x` —— 但先克隆它
let y = &mut (x.clone());

// 若没有前两行中的 x.clone()，这一行会因 x 已被借用而编译失败
// 多亏了 x.clone()，x 从未被借用，因此这一行可以运行
println!("{x}");

// 对借用做一些操作，防止 Rust 把它优化掉
*y += 1;
```

## 动机 {#motivation}

特别是对初学者而言，用这种模式来解决与借用检查器相关的困惑问题很有诱惑力。然而，后果很严重。使用 `.clone()` 会复制一份数据。两者之间的改动不同步——就像存在两个完全独立的变量。

也有特例——`Rc<T>` 被设计为智能地处理克隆。它在内部只管理恰好一份数据。对 `Rc` 调用 `.clone()` 会生成一个新的 `Rc` 实例，它指向与源 `Rc` 相同的数据，同时增加引用计数。`Rc` 的线程安全对应物 `Arc` 也是如此。

一般而言，克隆应当是有意为之，并充分理解其后果。若用克隆只是为了让借用检查器的错误消失，这往往表明可能正在使用这种反模式。

尽管 `.clone()` 往往是不良模式的信号，但有时**写出低效代码是可以的**，例如：

- 开发者对所有权还不熟悉
- 代码对速度或内存没有很高约束（如黑客马拉松项目或原型）
- 满足借用检查器实在太复杂，你更想优先可读性而非性能

若怀疑存在不必要的克隆，应先完整理解
[《Rust 程序设计语言》中关于所有权的章节](https://doc.rust-lang.org/book/ownership.html)，
再判断该克隆是否真正必要。

也请务必在项目中始终运行 `cargo clippy`，它能检测出一些 `.clone()` 并不必要的情况。

## 参见 {#see-also}

- [用 `mem::{take(_), replace(_)}` 在变更的枚举中保留所有权值](../idioms/07-mem-take-replace/)
- [`Rc<T>` 文档，它能智能地处理 .clone()](http://doc.rust-lang.org/std/rc/)
- [`Arc<T>` 文档，线程安全的引用计数指针](https://doc.rust-lang.org/std/sync/struct.Arc.html)
- [Rust 中与所有权相关的技巧](https://web.archive.org/web/20210120233744/https://xion.io/post/code/rust-borrowchk-tricks.html)
