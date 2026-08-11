+++
title = "The Rustonomicon"
date = 2026-08-06T17:08:00+08:00
weight = 1
type = "docs"
description = "Unsafe Rust 黑魔法：深入不安全代码的细节"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 导言


> 原文链接: [https://doc.rust-lang.org/nomicon/intro.html](https://doc.rust-lang.org/nomicon/intro.html)


> **警告：**
> 本书尚未完成。
> 要把所有内容都写全、并把过时的部分重写一遍，需要不少时间。
> 请查看 [issue tracker] 了解哪些内容缺失或过时；若发现尚未报告的错误或想法，欢迎在那里开新 issue。

[issue tracker]: https://github.com/rust-lang/nomicon/issues

## Unsafe Rust 的黑魔法

> 知识按「原样」提供，不附带任何明示或默示的保证，包括但不限于：释放难以名状的恐怖、粉碎你的 psyche、让你的心智漂流在不可知的无限宇宙之中。

　　Rustonomicon 深入讲解编写 Unsafe Rust 程序时需要理解的所有棘手细节。

　　若你希望长期从事 Rust 编程并过得长久而愉快，现在就该转身离开，假装从未见过这本书。
　　它并非必需。
　　但若你打算写 unsafe 代码——或只是想探究语言的内里——本书包含大量有用信息。

　　与 *[The Rust Programming Language][trpl]* 不同，我们会假定读者已有相当的基础。
　　尤其应熟悉基本的系统编程与 Rust。
　　若对这些主题尚不自在，建议先读 [The Book][trpl]。
　　话虽如此，我们并不假定你已读过它，并会在合适处偶尔复习基础。
　　你也可以直接跳到本书；只是要知道，我们不会从零讲起一切。

　　本书主要是 [The Reference][ref] 的高层伴侣。
　　Reference 详述语言每一部分的语法与语义，Rustonomicon 则描述如何把这些部分组合使用，以及在此过程中会遇到的问题。

　　Reference 会告诉你引用、析构与栈展开（unwinding）的语法和语义，但不会告诉你把它们组合起来如何导致异常安全（exception-safety）问题，以及如何应对。

　　需要说明的是，Rustonomicon 与 Reference 尚未很好同步，二者可能有重复内容。
　　一般而言，若两文档不一致，应以 Reference 为准（它虽尚未被视作规范文档，但维护得更好）。

　　本书范围包括：（不）安全的含义、语言与标准库提供的 unsafe 原语、用这些原语构造安全抽象的技术、子类型与型变（variance）、异常安全（panic/unwind 安全）、未初始化内存、类型双关（type punning）、并发、与其他语言互操作（FFI）、优化技巧、语言构造如何降级为编译器/OS/硬件原语、如何**不要**惹怒内存模型研究者、你**将会**如何惹怒他们，等等。

　　Rustonomicon 并非穷尽标准库中每个 API 的语义与保证，也不是 Rust 每个特性的百科全书。

　　除非另有说明，本书中的 Rust 代码使用 Rust 2024 edition。

[trpl]: ../book/index.html
[ref]: ../reference/index.html
