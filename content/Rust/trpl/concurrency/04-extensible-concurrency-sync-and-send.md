+++
title = "16.4 用 Send 与 Sync 实现可扩展并发"
date = 2026-08-05T08:44:00+08:00
weight = 78
type = "docs"
description = "用 Send 与 Sync 标记特征扩展 Rust 的并发保证"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用 Send 与 Sync 实现可扩展并发 {#send-sync}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch16-04-extensible-concurrency-sync-and-send.html](https://doc.rust-lang.org/stable/book/ch16-04-extensible-concurrency-sync-and-send.html)


## 用 `Send` 与 `Sync` 实现可扩展并发

　　有趣的是，本章到目前为止讨论的几乎每一项并发功能都属于标准库，而不是语言本身。你处理并发的选择并不限于语言或标准库；你可以编写自己的并发功能，或使用他人编写的功能。

　　不过，嵌入在语言中而非标准库里的关键并发概念，包括 `std::marker` 特征 `Send` 与 `Sync`。

### 在线程间转移所有权

　　`Send` 标记特征表明：实现了 `Send` 的类型，其值的所有权可以在线程之间转移。几乎每个 Rust 类型都实现了 `Send`，但也有例外，包括 `Rc<T>`：它不能实现 `Send`，因为若你克隆一个 `Rc<T>` 值并试图把克隆的所有权转移到另一线程，两个线程可能同时更新引用计数。因此，`Rc<T>` 是为实现在单线程情形下使用的——你不想为线程安全付出性能代价。

　　因此，Rust 的类型系统与特征约束确保你永远不会意外地以不安全方式跨线程发送 `Rc<T>` 值。当我们在示例 16-14 中尝试这样做时，得到错误 `` the trait `Send` is not implemented for `Rc<Mutex<i32>>` ``。当我们改用实现了 `Send` 的 `Arc<T>` 时，代码就能编译了。

　　完全由 `Send` 类型组成的任何类型也会自动被标记为 `Send`。几乎所有原始类型都是 `Send`，原始指针除外——我们会在第 20 章讨论。

### 从多个线程访问

　　`Sync` 标记特征表明：实现了 `Sync` 的类型可以从多个线程安全地被引用。换句话说，若 `&T`（对 `T` 的不可变引用）实现了 `Send`——意味着该引用可以安全发送到另一线程——则任意类型 `T` 就实现了 `Sync`。与 `Send` 类似，原始类型都实现了 `Sync`，完全由实现了 `Sync` 的类型组成的类型也实现了 `Sync`。

　　智能指针 `Rc<T>` 同样不实现 `Sync`，原因与它不实现 `Send` 相同。`RefCell<T>` 类型（第 15 章讨论过）以及相关的 `Cell<T>` 家族也不实现 `Sync`。`RefCell<T>` 在运行时做的借用检查实现不是线程安全的。智能指针 `Mutex<T>` 实现了 `Sync`，可用于与多个线程共享访问，正如你在[「在多个线程间共享访问 `Mutex<T>`」][shared-access]中所见。

### 手动实现 `Send` 与 `Sync` 是不安全的

　　因为完全由其他实现了 `Send` 与 `Sync` 的类型组成的类型也会自动实现 `Send` 与 `Sync`，我们不必手动实现这些特征。作为标记特征，它们甚至没有任何要实现的方法。它们只是用于强制执行与并发相关的不变量。

　　手动实现这些特征涉及编写不安全的 Rust 代码。第 20 章会讨论如何使用不安全的 Rust 代码；目前重要的信息是：构建并非由 `Send` 与 `Sync` 部分组成的新并发类型，需要仔细思考以维持安全保证。[《Rustonomicon》][nomicon] 有更多关于这些保证以及如何维持它们的信息。

## 小结

　　这并不是本书中你最后一次见到并发：下一章聚焦异步编程，第 21 章的项目会把本章概念用在比这里小例子更现实的情形中。

　　如前所述，因为 Rust 处理并发的方式很少属于语言本身，许多并发解决方案以 crate 的形式实现。它们比标准库演进得更快，因此务必在网上搜索当前最先进的 crate，以便在多线程情形中使用。

　　Rust 标准库提供了用于消息传递的通道，以及可在并发上下文中安全使用的智能指针类型，例如 `Mutex<T>` 与 `Arc<T>`。类型系统与借用检查器确保使用这些方案的代码不会最终出现数据竞争或无效引用。一旦代码能编译，你就可以放心它会愉快地在多个线程上运行，而不会有其他语言中常见的那种难以追查的 bug。并发编程不再是需要畏惧的概念：大胆前进，无畏地让你的程序并发起来吧！

[shared-access]: /trpl/concurrency/03-shared-state/#sharing-a-mutext-between-multiple-threads
[nomicon]: https://doc.rust-lang.org/nomicon/index.html
