+++
title = "7.2 CXX 的限制"
date = 2026-08-11T11:30:00+08:00
weight = 272
type = "docs"
description = "02-CXX 的限制 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/interoperability-with-cpp/limitations-of-cxx.html](https://google.github.io/comprehensive-rust/chromium/interoperability-with-cpp/limitations-of-cxx.html)

# 7.2 CXX 的限制

## CXX 的限制

使用 CXX 时，最有用的页面莫过于[类型参考][1]。

CXX 从根本上适合这些情形：

- 你的 Rust-C++ 接口足够简单，你可以声明其全部内容。
- 你只使用 CXX 已原生支持的类型，例如 `std::unique_ptr`、`std::string`、`&[u8]` 等。

它有许多限制——例如缺少对 Rust `Option` 类型的支持。

这些限制把我们约束为在 Chromium 中只把 Rust 用于隔离良好的“叶节点”，而不是任意的 Rust-C++ 互操作。在考虑 Chromium 中的 Rust 用例时，一个好的起点是起草语言边界的 CXX 绑定，看看它是否显得足够简单。

[1]: https://cxx.rs/bindings.html

> 此外，目前由于我们 component 构建中的链接细节，一个组件中的 Rust 代码不能依赖另一个组件中的 Rust 代码。这是把 Rust 限制在叶节点使用的另一个原因。
>
> 你还应讨论 CXX 的一些其他棘手点，例如：
>
> - 其错误处理基于 C++ 异常（下一页给出）
> - 函数指针使用起来很别扭。

