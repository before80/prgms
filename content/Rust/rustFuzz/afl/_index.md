+++
title = "2 使用 afl.rs 进行模糊测试"
date = 2026-08-23T13:50:00+08:00
weight = 30
type = "docs"
description = "American fuzzy lop 与 afl.rs"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Rust Fuzz Book](https://rust-fuzz.github.io/book/)

# 使用 afl.rs 进行模糊测试 {#afl}


> 原文链接: [https://rust-fuzz.github.io/book/afl.html](https://rust-fuzz.github.io/book/afl.html)


[American fuzzy lop][american-fuzzy-lop]（AFL）是一款流行、有效且现代的模糊测试工具。[afl.rs][] 允许在 [Rust 编程语言][rust] 编写的代码上运行 AFL。

[american-fuzzy-lop]: http://lcamtuf.coredump.cx/afl/
[Rust]: https://www.rust-lang.org
[afl.rs]: https://github.com/rust-fuzz/afl.rs
