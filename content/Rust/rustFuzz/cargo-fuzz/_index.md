+++
title = "1 使用 cargo-fuzz 进行模糊测试"
date = 2026-08-23T13:50:00+08:00
weight = 10
type = "docs"
description = "cargo-fuzz 与 libFuzzer"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Rust Fuzz Book](https://rust-fuzz.github.io/book/)

# 使用 cargo-fuzz 进行模糊测试 {#cargo-fuzz}


> 原文链接: [https://rust-fuzz.github.io/book/cargo-fuzz.html](https://rust-fuzz.github.io/book/cargo-fuzz.html)


[cargo-fuzz][] 是模糊测试 Rust 代码的推荐工具。

cargo-fuzz 本身不是模糊器，而是调用模糊器的工具。目前它仅支持 [libFuzzer][]（通过 [libfuzzer-sys][] crate），但未来可[扩展以支持其他模糊器][extending]。

[cargo-fuzz]: https://github.com/rust-fuzz/cargo-fuzz
[extending]: https://github.com/rust-fuzz/cargo-fuzz/issues/1
[libfuzzer-sys]: https://github.com/rust-fuzz/libfuzzer
[libFuzzer]: http://llvm.org/docs/LibFuzzer.html
