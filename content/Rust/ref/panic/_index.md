+++
title = "第14章 Panic"
date = 2026-08-18T08:45:00+08:00
weight = 105
type = "docs"
description = "Panic — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/panic.html](https://doc.rust-lang.org/reference/panic.html)

r[panic]
# Panic

r[panic.intro]
Rust 提供了一种机制，用于阻止函数正常返回，转而“恐慌（panic）”——这是对错误条件的一种响应，在遇到该错误的上下文中通常预期其不可恢复。

r[panic.lang-ops]
某些语言结构（例如越界的[数组索引][array indexing]）会自动引发恐慌。

r[panic.control]
此外，还有一些语言特性可以对恐慌行为提供一定程度的控制：

* [_恐慌处理器_][panic handler]定义了恐慌的行为。
* [FFI ABI](../items/04-functions/#unwinding) 可能改变恐慌的行为方式。

> **注意**
> 标准库通过 [`panic!` 宏][panic!] 提供了显式引发恐慌的能力。

r[panic.panic_handler]
## `panic_handler` 属性

r[panic.panic_handler.intro]
*`panic_handler` 属性*可以应用于函数，以定义恐慌的行为。

r[panic.panic_handler.allowed-positions]
`panic_handler` 属性只能应用于签名为 `fn(&PanicInfo) -> !` 的函数。

> **注意**
> [`PanicInfo`] 结构体包含有关恐慌发生位置的信息。

r[panic.panic_handler.unique]
依赖图中必须有且仅有一个 `panic_handler` 函数。

下面展示了一个 `panic_handler` 函数：它记录恐慌消息，然后使线程停机。

<!-- ignore: test infrastructure can't handle no_std -->
```rust
#![no_std]

use core::fmt::{self, Write};
use core::panic::PanicInfo;

struct Sink {
    // ..
##    _0: (),
}
#
## impl Sink {
##     fn new() -> Sink { Sink { _0: () }}
## }
#
## impl fmt::Write for Sink {
##     fn write_str(&mut self, _: &str) -> fmt::Result { Ok(()) }
## }

#[panic_handler]
fn panic(info: &PanicInfo) -> ! {
    let mut sink = Sink::new();

    // 将 "panicked at '$reason', src/main.rs:27:4" 记录到某个 `sink`
    let _ = writeln!(sink, "{}", info);

    loop {}
}
```

r[panic.panic_handler.std]
### 标准行为

r[panic.panic_handler.std.kinds]
`std` 提供了两种不同的恐慌处理器：

* `unwind` —— 展开栈，并且潜在可恢复。
* `abort` ---- 中止进程，并且不可恢复。

并非所有目标平台都提供 `unwind` 处理器。

> **注意**
> 与 `std` 链接时所使用的恐慌处理器可通过 [`-C panic`] CLI 标志设置。对大多数目标平台而言，默认值为 `unwind`。
>
> 标准库的恐慌行为可在运行时通过 [`std::panic::set_hook`] 函数修改。

r[panic.panic_handler.std.no_std]
链接 [`no_std`] 的二进制文件、dylib、cdylib 或 staticlib 时，需要自行指定恐慌处理器。

r[panic.strategy]
## 恐慌策略

r[panic.strategy.intro]
_恐慌策略_定义了 crate 构建时所支持的恐慌行为种类。

> **注意**
> 可在 `rustc` 中通过 [`-C panic`] CLI 标志选择恐慌策略。
>
> 在生成二进制文件、dylib、cdylib 或 staticlib 并与 `std` 链接时，`-C panic` CLI 标志也会影响所使用的[恐慌处理器][panic handler]。

> **注意**
> 以 `abort` 恐慌策略编译代码时，优化器可以假定不可能跨 Rust 栈帧展开，从而可能同时带来代码体积与运行时速度方面的改进。

> **注意**
> 关于链接具有不同恐慌策略的 crate 的限制，参见 [link.unwinding]。其含义之一是：以 `unwind` 策略构建的 crate 可以使用 `abort` 恐慌处理器，但 `abort` 策略不能使用 `unwind` 恐慌处理器。

r[panic.unwind]
## 展开（Unwinding）

r[panic.unwind.intro]
恐慌既可以是可恢复的，也可以是不可恢复的，不过也可以通过配置（选择非展开的恐慌处理器）使其始终不可恢复。（反过来并不成立：`unwind` 处理器并不保证所有恐慌都可恢复，而只保证通过 `panic!` 宏以及类似的标准库机制引发的恐慌是可恢复的。）

r[panic.unwind.destruction]
当发生恐慌时，`unwind` 处理器会“展开” Rust 栈帧，正如 C++ 的 `throw` 会展开 C++ 栈帧一样，直到恐慌到达恢复点（例如线程边界）。这意味着，当恐慌穿越 Rust 栈帧时，这些栈帧中[实现了 `Drop`][destructors] 的存活对象会调用其 `drop` 方法。因此，当正常执行恢复时，已不可再访问的对象会被“清理”，就好像它们正常离开作用域一样。

> **注意**
> 只要这一资源清理保证得以保留，“展开”的实现不必真正使用目标平台上 C++ 所用的机制。

> **注意**
> 标准库提供了两种从恐慌中恢复的机制：[`std::panic::catch_unwind`]（允许在引发恐慌的线程内恢复）以及 [`std::thread::spawn`]（会自动为被生成的线程设置恐慌恢复，以便其他线程可以继续运行）。

r[panic.unwind.ffi]
### 跨越 FFI 边界的展开

r[panic.unwind.ffi.intro]
使用[适当的 ABI 声明][unwind-abi]，可以跨越 FFI 边界进行展开。这在某些情况下很有用，但也会带来独特的未定义行为机会，尤其是在涉及多种语言运行时时。

r[panic.unwind.ffi.undefined]
以错误的 ABI 进行展开属于未定义行为：

* 从通过以非展开 ABI（例如 `"C"`、`"system"` 等）声明的函数声明或函数指针所调用的外部函数中，引发展开进入 Rust 代码。（例如，当用 C++ 编写的此类函数抛出未捕获的异常并传播到 Rust 时，就会出现这种情况。）
* 从不支持展开的代码（例如使用 `-fno-exceptions` 由 GCC 或 Clang 编译的代码）调用会展开的 Rust `extern` 函数（使用 `extern "C-unwind"` 或其他允许展开的 ABI）

r[panic.unwind.ffi.catch-foreign]
使用 [`std::panic::catch_unwind`]、[`std::thread::JoinHandle::join`] 捕获外部展开操作（例如 C++ 异常），或让其传播到超出 Rust `main()` 函数或线程根，将具有以下两种行为之一，具体发生哪一种是未指定的：

* 进程中止。
* 函数返回包含不透明类型的 [`Result::Err`]。

> **注意**
> 就本保证而言，使用不同实例的 Rust 标准库编译或链接的 Rust 代码算作“外部异常”。因此，一个使用 `panic!` 并链接到某一版本 Rust 标准库的库，若由使用另一版本标准库的应用程序调用，即使该库仅在子线程中使用，也可能导致整个应用程序中止。

r[panic.unwind.ffi.dispose-panic]
目前，对于外部运行时尝试处置或重新抛出 Rust `panic` 载荷时会发生何种行为，没有任何保证。换言之，源自 Rust 运行时的展开必须导致进程终止，或由同一运行时捕获。

[`-C panic`]: ../rustc/codegen-options/index.html#panic
[`no_std`]: names/preludes.md#the-no_std-attribute
[`PanicInfo`]: core::panic::PanicInfo
[array indexing]: expressions/array-expr.md#array-and-slice-indexing-expressions
[attribute]: attributes.md
[destructors]: destructors.md
[panic handler]: #the-panic_handler-attribute
[runtime]: runtime.md
[unwind-abi]: items/functions.md#unwinding
