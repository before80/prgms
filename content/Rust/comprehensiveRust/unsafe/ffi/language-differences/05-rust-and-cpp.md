+++
title = "9.4.5 Rust 与 C++"
date = 2026-08-11T11:30:00+08:00
weight = 570
type = "docs"
description = "05-Rust 与 C++ — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/language-differences/rust-and-cpp.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/language-differences/rust-and-cpp.html)

# 9.4.5 Rust 与 C++

| 关注点 | Rust | C++ |
| --- | --- | --- |
| **平凡可重定位性** | 所有移动都是 `memcpy` | 自引用类型、移动构造函数可能有副作用 |
| **析构安全** | 仅在原位置调用 `Drop::drop()` | 析构函数可能在已移动对象上运行 |
| **异常安全** | Panic（abort 或 unwind） | 异常（unwind） |
| **ABI 稳定性** | 明确不稳定 | 取决于编译器厂商 |

> 即使能避免通过 C 互操作，两种语言仍有一些方面会影响 FFI：
>
> _平凡可重定位性_
>
> 无法在 Rust 侧安全移动 C++ 对象；必须 pin 或保留在 C++ 堆上。
>
> 在 Rust 中，对象移动（赋值时或按值传参时发生）总是按位复制。
>
> C++ 允许用户通过重载赋值运算符、定义移动与复制构造函数来自定义语义。
>
> 这会影响互操作，因为自引用类型在高性能 C++ 中很自然。自定义构造函数可以在对象在内存中改变位置时仍维护安全不变量。
>
> 具有相同语义的对象在 Rust 中无法定义。
>
> _析构安全_
>
> C++ 已移动对象的语义无法映射；必须阻止 Rust「移动」C++ 类型。
>
> _异常安全_
>
> 两者都无法安全进入对方；都必须在边界处捕获。

