+++
title = "01-unsafe 关键字"
date = 2026-08-18T08:45:00+08:00
weight = 109
type = "docs"
description = "unsafe 关键字 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/unsafe-keyword.html](https://doc.rust-lang.org/reference/unsafe-keyword.html)

r[unsafe]
# unsafe 关键字

r[unsafe.intro]
`unsafe` 关键字用于创建或解除证明某事安全的义务。具体而言：

- 用于标记那些*定义*额外安全条件、且这些条件必须在别处得到满足的代码。
  - 这包括 `unsafe fn`、`unsafe static` 和 `unsafe trait`。
- 用于标记程序员*断言*已满足别处所定义安全条件的代码。
  - 这包括 `unsafe {}`、`unsafe impl`、没有启用 [`unsafe_op_in_unsafe_fn`] 的 `unsafe fn`、`unsafe extern`，以及 `#[unsafe(attr)]`。

下文分别讨论这些情形。一些说明性示例见 [关键字文档][keyword]。

r[unsafe.positions]
`unsafe` 关键字可以出现在若干不同上下文中：

- 不安全函数（`unsafe fn`）
- 不安全块（`unsafe {}`）
- 不安全 trait（`unsafe trait`）
- 不安全 trait 实现（`unsafe impl`）
- 不安全外部块（`unsafe extern`）
- 不安全外部静态项（`unsafe static`）
- 不安全属性（`#[unsafe(attr)]`）

r[unsafe.fn]
## 不安全函数（`unsafe fn`）

r[unsafe.fn.intro]
不安全函数是并非在所有上下文中和/或对所有可能输入都安全的函数。我们称它们具有*额外安全条件*，即所有调用者必须满足、且编译器不会检查的要求。例如，[`get_unchecked`] 的额外安全条件是索引必须在边界内。不安全函数应附带文档，说明这些额外安全条件是什么。

r[unsafe.fn.safety]
此类函数必须以关键字 `unsafe` 为前缀，并且只能从 `unsafe` 块内部调用，或在未启用 [`unsafe_op_in_unsafe_fn`] lint 的 `unsafe fn` 内部调用。

r[unsafe.block]
## 不安全块（`unsafe {}`）

r[unsafe.block.intro]
可以用 `unsafe` 关键字为代码块加前缀，以允许使用[不安全性][Unsafety]一章所定义的不安全操作，例如调用其他不安全函数或解引用裸指针。

r[unsafe.block.fn-body]
默认情况下，不安全函数的函数体也被视为不安全块；可通过启用 [`unsafe_op_in_unsafe_fn`] lint 来改变这一点。

通过将操作放入不安全块，程序员声明已妥善满足该块内所有操作的额外安全条件。

不安全块与不安全函数在逻辑上互为对偶：不安全函数定义了调用者必须履行的证明义务，而不安全块则声明块内所调用的函数或操作的相关证明义务均已解除。解除证明义务的方式很多；例如，可以有运行时检查或数据结构不变量保证某些性质必定成立，或者不安全块位于 `unsafe fn` 内部，此时该块可以使用该函数的证明义务来解除块内产生的证明义务。

不安全块用于包装外部库、直接使用硬件，或实现语言中未直接提供的特性。例如，Rust 提供了实现内存安全并发所需的语言特性，但标准库中线程与消息传递的实现使用了不安全块。

Rust 的类型系统是对动态安全要求的保守近似，因此在某些情况下使用安全代码会有性能代价。例如，双向链表不是树结构，在安全代码中只能用引用计数指针表示。通过使用 `unsafe` 块将反向链接表示为裸指针，可以在无需引用计数的情况下实现它。（关于这一特定示例更深入的探讨，见 ["Learn Rust With Entirely Too Many Linked Lists"](https://rust-unofficial.github.io/too-many-lists/)。）

[Unsafety]: unsafety.md

r[unsafe.trait]
## 不安全 trait（`unsafe trait`）

r[unsafe.trait.intro]
不安全 trait 是带有额外安全条件的 trait，这些条件必须由该 trait 的*实现*所满足。不安全 trait 应附带文档，说明这些额外安全条件是什么。

r[unsafe.trait.safety]
此类 trait 必须以关键字 `unsafe` 为前缀，并且只能由 `unsafe impl` 块实现。

r[unsafe.impl]
## 不安全 trait 实现（`unsafe impl`）

实现不安全 trait 时，该实现需要以 `unsafe` 关键字为前缀。通过书写 `unsafe impl`，程序员声明已妥善满足该 trait 所要求的额外安全条件。

不安全 trait 实现与不安全 trait 在逻辑上互为对偶：不安全 trait 定义了实现必须履行的证明义务，而不安全实现则声明所有相关证明义务均已解除。

[keyword]: ../std/keyword.unsafe.html
[`get_unchecked`]: slice::get_unchecked
[`unsafe_op_in_unsafe_fn`]: ../rustc/lints/listing/allowed-by-default.html#unsafe-op-in-unsafe-fn

r[unsafe.extern]
## 不安全外部块（`unsafe extern`）

声明[外部块][external block]的程序员必须确保其中所含项的签名正确。未能做到可能导致未定义行为。书写 `unsafe extern` 即表明该义务已得到满足。

r[unsafe.extern.edition2024]
> [!EDITION-2024]
> 在 2024 edition 之前，允许不带 `unsafe` 限定来声明 `extern` 块。

[external block]: items/external-blocks.md

r[unsafe.attribute]
## 不安全属性（`#[unsafe(attr)]`）

[不安全属性][unsafe attribute]是在使用时具有额外安全条件的属性。编译器无法检查这些条件是否已得到满足。为断言它们已得到满足，这些属性必须包在 `unsafe(..)` 中，例如 `#[unsafe(no_mangle)]`。

[unsafe attribute]: attributes.md
