+++
title = "第9章 错误处理"
date = 2026-08-05T08:44:00+08:00
weight = 37
type = "docs"
description = "用 Result 与 panic! 处理可恢复与不可恢复错误"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 错误处理 {#error-handling}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch09-00-error-handling.html](https://doc.rust-lang.org/stable/book/ch09-00-error-handling.html)


　　软件里出错在所难免，因此 Rust 提供了多种特性来应对出问题的情况。很多时候，Rust 要求你承认错误可能发生，并在代码能通过编译之前采取某种处理。这一要求能让你在把代码部署到生产环境之前就发现并妥善处理错误，从而写出更稳健的程序。

　　Rust 把错误分成两大类：可恢复错误（recoverable）与不可恢复错误（unrecoverable）。对于可恢复错误——例如“找不到文件”——我们通常只想把问题报告给用户，然后重试操作。不可恢复错误则往往意味着程序里有 bug，例如访问数组越界，这时我们希望立刻停止程序。

　　多数语言并不区分这两类错误，而是用异常（exception）等机制统一处理。Rust 没有异常。它用 `Result<T, E>` 类型表示可恢复错误，用 `panic!` 宏在遇到不可恢复错误时停止执行。本章会先讲如何调用 `panic!`，再讲如何返回 `Result<T, E>` 值，最后讨论在“尝试恢复”与“直接停止”之间该如何权衡。
