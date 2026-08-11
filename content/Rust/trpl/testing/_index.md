+++
title = "第11章 编写自动化测试"
date = 2026-08-05T08:44:00+08:00
weight = 45
type = "docs"
description = "用 Rust 的测试设施编写自动化测试"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 编写自动化测试 {#writing-automated-tests}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch11-00-testing.html](https://doc.rust-lang.org/stable/book/ch11-00-testing.html)


　　Edsger W. Dijkstra 在 1972 年的文章《谦卑的程序员》（“The Humble Programmer”）中写道：“程序测试可以非常有效地显示 bug 的存在，但对于显示它们的不存在却无可救药地不足。”这并不意味着我们就不该尽可能多地测试！

　　程序中的*正确性（correctness）*指代码在多大程度上做了我们意图让它做的事。Rust 在设计上高度关注程序正确性，但正确性很复杂，也不易证明。Rust 的类型系统承担了很大一部分负担，但类型系统并不能抓住一切。因此，Rust 包含对编写自动化软件测试的支持。

　　假设我们写了一个 `add_two` 函数，把传入的数字加 2。该函数的签名接受一个整数参数并返回一个整数。实现并编译该函数时，Rust 会做你目前学过的全部类型检查与借用检查，例如确保我们没有把 `String` 值或无效引用传给该函数。但 Rust *无法*检查该函数是否精确按我们的意图工作——即返回参数加 2，而不是参数加 10 或参数减 50！这正是测试的用武之地。

　　我们可以编写测试来断言：例如，把 `3` 传给 `add_two` 时，返回值是 `5`。每当我们改动代码，都可以运行这些测试，确保既有的正确行为没有被改变。

　　测试是一门复杂的技能：一章之内无法覆盖如何写好测试的所有细节，但本章会讨论 Rust 测试设施的机制。我们会谈编写测试时可用的注解与宏、运行测试时的默认行为与选项，以及如何把测试组织成单元测试与集成测试。
