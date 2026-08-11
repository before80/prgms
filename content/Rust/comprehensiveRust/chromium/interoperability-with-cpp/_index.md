+++
title = "7 与 C++ 互操作"
date = 2026-08-11T11:30:00+08:00
weight = 270
type = "docs"
description = "与 C++ 互操作 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/interoperability-with-cpp.html](https://google.github.io/comprehensive-rust/chromium/interoperability-with-cpp.html)

# 7 与 C++ 互操作

Rust 社区为 C++/Rust 互操作提供了多种选项，新工具也在不断开发。目前，Chromium 使用一个名为 CXX 的工具。

你在接口定义语言（外形很像 Rust）中描述整个语言边界，然后 CXX 工具为函数与类型在 Rust 与 C++ 两侧生成声明。

<img src="img/overview.svg" alt="cxx 概览图，显示同一接口定义用于创建 C++ 与 Rust 两侧代码，它们再通过最低公分母 C API 通信">

完整用法示例见 [CXX tutorial][1]。

[1]: https://cxx.rs/tutorial.html
[2]: https://cxx.rs/bindings.html

> 讲解该图。说明在幕后，这与你之前手工做的事情相同。指出自动化该过程有以下好处：
>
> - 该工具保证 C++ 与 Rust 两侧匹配（例如，若 `#[cxx::bridge]` 与实际的 C++ 或 Rust 定义不匹配，你会得到编译错误；而不同步的手工绑定会得到未定义行为）
> - 该工具自动生成非 C 特性的 FFI thunk（小型、C-ABI 兼容的自由函数）（例如，使能对 Rust 或 C++ 方法的 FFI 调用；手工绑定需要手动编写此类顶层自由函数）
> - 该工具与库可以处理一组核心类型——例如：
>   - `&[T]` 可以跨 FFI 边界传递，即使它不保证任何特定 ABI 或内存布局。用手工绑定时，`std::span<T>` / `&[T]` 必须手工拆解并由指针与长度重建——鉴于每种语言对空切片的表示略有不同，这容易出错）
>   - 像 `std::unique_ptr<T>`、`std::shared_ptr<T>` 和/或 `Box` 这样的智能指针有原生支持。用手工绑定时，必须传递 C-ABI 兼容的原始指针，这会增加生命周期与内存安全风险。
>   - `rust::String` 与 `CxxString` 类型理解并维护跨语言的字符串表示差异（例如 `rust::String::lossy` 可以从非 UTF-8 输入构建 Rust 字符串，`rust::String::c_str` 可以 NUL 终止字符串）。

