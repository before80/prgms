+++
title = "7.5 练习"
date = 2026-08-11T11:30:00+08:00
weight = 277
type = "docs"
description = "04-练习 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/exercises/chromium/interoperability-with-cpp.html](https://google.github.io/comprehensive-rust/exercises/chromium/interoperability-with-cpp.html)

# 7.5 练习

## 第一部分

- 在你之前创建的 Rust 文件中，添加一个 `#[cxx::bridge]`，指定单个要从 C++ 调用的函数，名为 `hello_from_rust`，不接受参数也不返回值。
- 修改你之前的 `hello_from_rust` 函数，去掉 `extern "C"` 与 `#[unsafe(no_mangle)]`。现在它只是一个标准 Rust 函数。
- 修改你的 `gn` 目标以构建这些绑定。
- 在你的 C++ 代码中，删除对 `hello_from_rust` 的前向声明。改为包含生成的头文件。
- 构建并运行！

## 第二部分

花点时间玩一下 CXX 是个好主意。它帮你思考 Chromium 中的 Rust 实际有多灵活。

一些可尝试的事：

- 从 Rust 回调到 C++。你将需要：
  - 一个可从你的 `cxx::bridge` 中 `include!` 的额外头文件。你需要在该新头文件中声明你的 C++ 函数。
  - 一个调用此类函数的 `unsafe` 块，或者按[此处说明][0]在 `#[cxx::bridge]` 中指定 `unsafe` 关键字。
  - 你可能还需要 `#include "third_party/rust/cxx/v1/crate/include/cxx.h"`
- 把 C++ 字符串从 C++ 传入 Rust。
- 把对 C++ 对象的引用传入 Rust。
- 故意让 Rust 函数签名与 `#[cxx::bridge]` 不匹配，并习惯你看到的错误。
- 故意让 C++ 函数签名与 `#[cxx::bridge]` 不匹配，并习惯你看到的错误。
- 把某个类型的 `std::unique_ptr` 从 C++ 传入 Rust，使 Rust 能拥有某个 C++ 对象。
- 创建一个 Rust 对象并传入 C++，使 C++ 拥有它。（提示：你需要一个 `Box`。）
- 在 C++ 类型上声明一些方法。从 Rust 调用它们。
- 在 Rust 类型上声明一些方法。从 C++ 调用它们。

## 第三部分

既然你理解了 CXX 互操作的优势与限制，想几个接口足够简单、适合在 Chromium 中使用 Rust 的用例。草拟你可能如何定义该接口。

## 在哪里找帮助

- [`cxx` 绑定参考][1]
- [`rust_static_library` gn 模板][2]

> 当学员探索第二部分时，他们一定会有很多关于如何实现这些事以及 CXX 幕后如何工作的问题。
>
> 你可能遇到的一些问题：
>
> - 我看到用类型 Y 初始化类型 X 的变量的问题，而 X 与 Y 都是函数类型。这是因为你的 C++ 函数与 `cxx::bridge` 中的声明不完全匹配。
> - 我似乎能把 C++ 引用自由转换成 Rust 引用。这不会有 UB 风险吗？对 CXX 的_不透明_类型来说不会，因为它们是零大小的。对 CXX 平凡类型来说会，_有可能_造成 UB，尽管 CXX 的设计使得构造这样的例子相当困难。


[0]: https://cxx.rs/extern-c++.html#functions-and-member-functions
[1]: https://cxx.rs/bindings.html
[2]: https://source.chromium.org/chromium/chromium/src/+/main:build/rust/rust_static_library.gni;l=16
