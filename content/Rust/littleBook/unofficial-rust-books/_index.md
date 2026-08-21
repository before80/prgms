+++
title = "02-非官方 Rust 书籍"
date = 2026-08-21T11:34:00+08:00
weight = 3
type = "docs"
description = "维护于 rust-lang.org 之外的非官方 Rust 书籍目录"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Little Book of Rust Books](https://lborb.github.io/book/)

> 原文链接: [https://lborb.github.io/book/unofficial.html](https://lborb.github.io/book/unofficial.html)

# 非官方 Rust 书籍

下列书籍维护于 [rust-lang.org](https://www.rust-lang.org/) 之外。

## 入门

* [100 Exercises to Learn Rust](https://rust-exercises.com/)
* [A Gentle Introduction To Rust](https://stevedonovan.github.io/rust-gentle-intro/readme.html)
* [*A half-hour to learn Rust*](https://fasterthanli.me/articles/a-half-hour-to-learn-rust)
* [*Common Rust Lifetime Misconceptions*](https://github.com/pretzelhammer/rust-blog/blob/master/posts/common-rust-lifetime-misconceptions.md)
* [Comprehensive Rust 🦀](https://google.github.io/comprehensive-rust/) — Google 为向 Android 工程师教授 Rust 而开发的多日课程
* [`Dyner`](https://dyner.netlify.app/) — Rust 中实验性的 trait（*dyn*）对象
* [Easy Rust](https://dhghomon.github.io/easy_rust/) — 面向非英语母语者
* [Effective Rust](https://www.lurklurk.org/effective-rust/) — Rust 指南[^effectiverust]
* [Error Handling in Rust](https://nrc.github.io/error-docs/)
* [Futures Explained in 200 Lines of Rust](https://web.archive.org/web/20230324130904/https://cfsamson.github.io/books-futures-explained/) — 来自互联网档案馆
* [*Java-Rust Generics*](https://gist.github.com/Kimundi/8391398)
* [Learning Rust](https://quinedot.github.io/rust-learning/index.html) — 由 `quinedot` 整理的资源合集
* [Learning Rust With Entirely Too Many Linked Lists](https://rust-unofficial.github.io/too-many-lists/)
* [*Learn Rust the Dangerous Way*](http://cliffle.com/p/dangerust/)
* [LifetimeKata](https://tfpk.github.io/lifetimekata/)
* [*Pointers*](https://github.com/diwic/reffers-rs/blob/master/docs/Pointers.md)
* [py2rs](https://rochacbruno.github.io/py2rs/) — 从 Python 到 Rust
* [*r4cppp*](https://github.com/nrc/r4cppp/blob/master/hello-world.md) — 面向 C++ 程序员的 Rust 快速入门
* [Rust 101](https://rust-lang.guide/) — Rust 编程语言学习指南
* [Rust Anthology 1](https://brson.github.io/rust-anthology/1/index.html)
* [*Rust Atomics and Locks*](https://marabos.nl/atomics/) — 实践中的底层并发
* [Rust By Practice](https://practice.rs/) — 通过有挑战性的示例、练习与项目练习 Rust
* [Rust Cookbook](https://rust-lang-nursery.github.io/rust-cookbook/) — 示例程序合集
* [rust-cross](https://github.com/japaric/rust-cross#table-of-contents) — 关于交叉编译 Rust 程序你需要知道的一切！
* [Rust Exercises by Ferrous Systems](https://rust-exercises.ferrous-systems.com/)
* [*Rust for Clojurists*](https://gist.github.com/oakes/4af1023b6c5162c6f8f0)
* [Rust for C++ Programmers](https://aminb.gitbooks.io/rust-for-c/content/index.html)
* [*Rust for Node Developers*](https://github.com/Mercateo/rust-for-node-developers/blob/master/setup/README.md)
* [Rust for the Polyglot Programmer](https://www.chiark.greenend.org.uk/~ianmdlvl/rust-polyglot/index.html)
* [*Rustic Symmetries*](https://github.com/kmcallister/rustic-symmetries/blob/master/README.md#rustic-symmetries)
* [*Rust Iterators*](https://github.com/rustomax/rust-iterators/#introduction)
* [*Rust Ownership, the Hard Way*](https://chrismorgan.info/blog/rust-ownership-the-hard-way/)
* [*Rust Training Slides by Ferrous Systems*](https://rust-training.ferrous-systems.com/latest/slides/)
* [Small Rust Tutorial For MLOps](https://nogibjj.github.io/rust-tutorial/) — 为 MLOps 学习 Rust
* [The Node Experiment: Exploring Async Basics with Rust](https://web.archive.org/web/20230125023131/https://cfsamson.github.io/book-exploring-async-basics/) — 来自互联网档案馆

## 应用领域

* 异步
  * [Async programming in Rust with async-std](https://book.async.rs/introduction.html)
  * [Async Raft](https://async-raft.github.io/async-raft/) — 用异步 Rust 实现的 Raft 分布式共识协议
  * [*Learning Async Rust with Entirely Too Many Web Servers*](https://ibraheem.ca/posts/too-many-web-servers/)
  * [The Node Experiment - Exploring Async Basics with Rust](https://cfsamson.github.io/book-exploring-async-basics/)
  * [*Tokio Tutorial*](https://tokio.rs/tokio/tutorial) — 事件驱动、非阻塞 I/O
* [Comparing parallel Rust and C++](https://parallel-rust-cpp.github.io/introduction.html)
* 命令行
  * [Command Line Applications in Rust](https://rust-cli.github.io/book/index.html)
  * [PNGme: An Intermediate Rust Project](https://jrdngr.github.io/pngme_book/) — 编写命令行程序，将秘密消息隐藏进 PNG 文件
* [CXX — Safe Interop Between Rust and C++](https://cxx.rs)
* 嵌入式
  * [Embedded: The Missing Parts](https://emp.jamesmunns.com/)
  * [Embedded Rust on Espressif](https://esp-rs.github.io/std-training/) — 学习在 Espressif ESP32-C3 上使用嵌入式 Rust 的培训材料
  * [The Embedded Rust Book](https://rust-embedded.github.io/book/)
  * [The Embedonomicon](https://docs.rust-embedded.org/embedonomicon/) — 从零构建 `#![no_std]` 应用
  * [The Rust on ESP Book](https://esp-rs.github.io/book/) — 在 Espressif SoC 与模组上使用 Rust 的综合指南
  * [Workbook for Embedded Workshops](https://embedded-trainings.ferrous-systems.com/preparations.html) — 嵌入式 Rust 工作坊
* 外部函数接口（FFI）
  * [*The Rust FFI Omnibus*](http://jakegoulding.com/rust-ffi-omnibus/)
  * [The (unofficial) Rust FFI Guide](https://michael-f-bryan.github.io/rust-ffi-guide/) — 深入 FFI
  * [Using Unsafe for Fun and Profit](https://michael-f-bryan.github.io/rust-ffi-guide/)
* [Real-Time Interrupt-driven Concurrency](https://rtic.rs/)
* [Triangle From Scratch](https://rust-tutorials.github.io/triangle-from-scratch/) — 用 Win32 画三角形，但不依赖外部 crate
* WebAssembly
  * [Rust and WebAssembly](https://rustwasm.github.io/docs/book/)
  * [The `wasm-bindgen` Guide](https://rustwasm.github.io/docs/wasm-bindgen/)
  * [The `wasm-pack` Guide](https://rustwasm.github.io/docs/wasm-pack/)
  * [WASM It](https://azriel.im/wasm_it/)
* [*Writing an OS in Rust*](https://os.phil-opp.com/)
* [Writing Interpreters in Rust: a Guide](https://rust-hosted-langs.github.io/book/introduction.html)

## 其他

* 宏
  * [Advanced Macros](https://www.cs.brandeis.edu/~cs146a/rust/doc-02-21-2015/book/advanced-macros.html)
  * [MacroKata](https://tfpk.github.io/macrokata/) — 通过一系列练习学习宏
  * [The Little Book of Rust Macros](https://veykril.github.io/tlborm/)
  * [*Rust Latam: procedural macros workshop*](https://github.com/dtolnay/proc-macro-workshop#suggested-prerequisites)
* [High Assurance Rust](https://highassurance.rs/) — 开发安全、健壮的软件
* [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)
* [Rust Fuzz Book](https://rust-fuzz.github.io/book/) — 模糊测试
* [Rust Performance](https://nnethercote.github.io/perf-book/)
* [Salsa](https://salsa-rs.github.io/salsa/) — 按需、增量计算框架
* [Secure Rust Guidelines](https://anssi-fr.github.io/rust-guide/)
* [The Little Book of Rust Books](https://lborb.github.io/book/)
* [The Rust Rand Book](https://rust-random.github.io/book/) — Rust 的随机数库
* [Rust Tutorials](https://zicklag.github.io/rust-tutorials/overview.html)
* [Usability of Programming Languages](https://gergelyk.github.io/prog-lang-usability/) — 比较 Rust、Python 与 Crystal 中的基本惯用法

[^effectiverust]: 截至 2022 年 3 月，部分概念仍不完整。
