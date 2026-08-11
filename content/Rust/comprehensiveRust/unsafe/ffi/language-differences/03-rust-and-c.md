+++
title = "9.4.3 Rust 与 C"
date = 2026-08-11T11:30:00+08:00
weight = 568
type = "docs"
description = "03-Rust 与 C — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/language-differences/rust-and-c.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/language-differences/rust-and-c.html)

# 9.4.3 Rust 与 C

| 关注点 | Rust | C |
| --- | --- | --- |
| **错误** | `Result<T, E>`、`Option<T>` | 魔法返回值、输出参数、全局 `errno` |
| **字符串** | `&str`/`String`（UTF-8，已知长度） | 以空字符结尾的 `char*`，编码未定义 |
| **可空性** | 通过 `Option<T>` 显式表达 | 任意指针可能为 null |
| **所有权** | 仿射类型、生命周期 | 约定 |
| **回调** | `Fn`/`FnMut`/`FnOnce` 闭包 | 函数指针 + `void*` 用户数据 |
| **Panic** | 栈展开（或 abort） | abort |

> 错误：必须将 `Result` 转换为符合 C 约定的形式；C 侧很容易忘记检查错误。
>
> 字符串：存在转换成本；Rust 字符串中的空字节会导致截断；入口需进行 UTF-8 校验。
>
> 可空性：来自 C 的每个指针都必须检查，才能构造 `Option<NonNull<T>>`，这意味着需要 unsafe 块或运行时开销。
>
> 所有权：必须手动记录并强制执行对象生命周期。
>
> 回调：必须将闭包分解为函数指针 + 上下文；上下文的生命周期需手动管理。
>
> Panic：跨 FFI 边界 panic 属于未定义行为；必须在边界处用 `catch_unwind` 捕获。

