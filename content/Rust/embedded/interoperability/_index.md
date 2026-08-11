+++
title = "10-互操作性"
date = 2026-08-01T10:38:00+08:00
weight = 147
type = "docs"
description = "互操作性（Interoperability）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 互操作性 {#interoperability}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/interoperability/](https://doc.rust-lang.org/stable/embedded-book/interoperability/)


Rust 与 C 代码之间的互操作性始终依赖于在两种语言之间转换数据。
为此，`stdlib` 中有一个专用模块
[`std::ffi`](https://doc.rust-lang.org/std/ffi/index.html)。

`std::ffi` 提供了 C 原始类型的类型定义，
例如 `char`、`int` 和 `long`。
它还提供了一些工具，用于转换更复杂的类型，例如字符串，
将 `&str` 与 `String` 映射为更易、更安全处理的 C 类型。

自 Rust 1.30 起，
`std::ffi` 的功能可在 `core::ffi` 或 `alloc::ffi` 中使用，
取决于是否涉及内存分配。
[`cty`] crate 与 [`cstr_core`] crate
也提供类似功能。

[`cstr_core`]: https://crates.io/crates/cstr_core
[`cty`]: https://crates.io/crates/cty

| Rust 类型      | 中间类型     | C 类型         |
|----------------|--------------|----------------|
| `String`       | `CString`    | `char *`       |
| `&str`         | `CStr`       | `const char *` |
| `()`           | `c_void`     | `void`         |
| `u32` 或 `u64` | `c_uint`     | `unsigned int` |
| 等等           | ...          | ...            |

C 原始类型的值可以用作对应的 Rust 类型，反之亦然，
因为前者只是后者的类型别名。
例如，在 `unsigned int` 为 32 位的平台上，
以下代码可以编译。

```rust,ignore
fn foo(num: u32) {
    let c_num: c_uint = num;
    let r_num: u32 = c_num;
}
```

## 与其它构建系统的互操作性 {#interoperability-with-other-build-systems}

在嵌入式项目中纳入 Rust 的常见需求是，将 Cargo 与现有构建系统（例如 make 或 cmake）结合起来。

我们正在 issue tracker 的 [issue #61] 中收集这方面的示例与用例。

[issue #61]: https://github.com/rust-embedded/book/issues/61

## 与 RTOS 的互操作性 {#interoperability-with-rtoss}

将 Rust 与 FreeRTOS 或 ChibiOS 等 RTOS 集成仍在进行中；尤其是从 Rust 调用 RTOS 函数可能比较棘手。

目前，以下项目公开支持 Rust 与 RTOS 的互操作：

* [Zephyr Project](https://docs.zephyrproject.org/latest/develop/languages/rust/index.html)

我们正在 issue tracker 的 [issue #62] 中收集这方面的示例与用例。

[issue #62]: https://github.com/rust-embedded/book/issues/62

## 本章其它页面

- [在 Rust 中使用一点 C](01-a-little-c-with-your-rust/)
- [在 C 中使用一点 Rust](02-a-little-rust-with-your-c/)
