+++
title = "05-Panic 处理"
date = 2026-08-01T10:38:00+08:00
weight = 43
type = "docs"
description = "Panic 处理（Panicking）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# Panic 处理 {#panicking}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/start/panicking.html](https://doc.rust-lang.org/stable/embedded-book/start/panicking.html)


Panic 是 Rust 语言的核心部分。像索引这样的内置操作会在运行时检查内存安全。当尝试越界索引时，就会导致 panic。

在标准库中，panic 有定义好的行为：它会展开（unwind）发生 panic 的线程的栈，除非用户选择在 panic 时中止（abort）程序。

然而，在没有标准库的程序中，panic 行为是未定义的。可以通过声明一个 `#[panic_handler]` 函数来选择一种行为。该函数在程序的依赖图中必须恰好出现*一次*，并且必须具有以下签名：`fn(&PanicInfo) -> !`，其中 [`PanicInfo`] 是包含 panic 位置信息的结构体。

[`PanicInfo`]: https://doc.rust-lang.org/core/panic/struct.PanicInfo.html

鉴于嵌入式系统从面向用户到安全关键（不能崩溃）范围很广，没有一种放之四海而皆准的 panic 行为，但有许多常用行为。这些常见行为已被打包成定义 `#[panic_handler]` 函数的 crate。一些例子包括：

- [`panic-abort`]。panic 导致执行 abort 指令。
- [`panic-halt`]。panic 导致程序或当前线程通过进入无限循环而停机。
- [`panic-itm`]。panic 消息通过 ITM（一种 ARM Cortex-M 特有外设）记录。
- [`panic-semihosting`]。panic 消息通过半主机技术记录到主机。

[`panic-abort`]: https://crates.io/crates/panic-abort
[`panic-halt`]: https://crates.io/crates/panic-halt
[`panic-itm`]: https://crates.io/crates/panic-itm
[`panic-semihosting`]: https://crates.io/crates/panic-semihosting

你还可以通过在 crates.io 上搜索 [`panic-handler`] 关键字找到更多 crate。

[`panic-handler`]: https://crates.io/keywords/panic-handler

程序只需链接到对应的 crate，即可选择这些行为之一。panic 行为在应用源码中以单行代码表达，不仅有助于文档化，还可用于根据编译配置文件更改 panic 行为。例如：

``` rust,ignore
#![no_main]
#![no_std]

// dev 配置：更容易调试 panic；可在 `rust_begin_unwind` 上设断点
#[cfg(debug_assertions)]
use panic_halt as _;

// release 配置：最小化应用的二进制大小
#[cfg(not(debug_assertions))]
use panic_abort as _;

// ..
```

在本例中，crate 在用 dev 配置构建时（`cargo build`）链接到 `panic-halt` crate，而在用 release 配置构建时（`cargo build --release`）链接到 `panic-abort` crate。

> `use panic_abort as _;` 这种 `use` 语句形式用于确保 `panic_abort` panic 处理函数被包含进最终可执行文件，同时让编译器清楚我们不会显式使用该 crate 中的任何内容。若没有 `as _` 重命名，编译器会警告我们有未使用的导入。
> 有时你可能看到 `extern crate panic_abort`，这是 Rust 2018 edition 之前的旧风格，现在应仅用于 “sysroot” crate（随 Rust 本身分发的那些），如 `proc_macro`、`alloc`、`std` 与 `test`。

## 一个例子 {#an-example}

下面是一个尝试索引数组超出其长度的例子。该操作会导致 panic。

```rust,ignore
#![no_main]
#![no_std]

use panic_semihosting as _;

use cortex_m_rt::entry;

#[entry]
fn main() -> ! {
    let xs = [0, 1, 2];
    let i = xs.len();
    let _y = xs[i]; // 越界访问

    loop {}
}
```

本例选择了 `panic-semihosting` 行为，它会用半主机把 panic 消息打印到主机控制台。

``` text
$ cargo run
     Running `qemu-system-arm -cpu cortex-m3 -machine lm3s6965evb (..)
panicked at 'index out of bounds: the len is 3 but the index is 4', src/main.rs:12:13
```

你可以尝试把行为改成 `panic-halt`，并确认在那种情况下不会打印任何消息。
