+++
title = "01-在 Rust 中使用一点 C"
date = 2026-08-01T10:38:00+08:00
weight = 148
type = "docs"
description = "在 Rust 中使用一点 C（A little C with your Rust）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 在 Rust 中使用一点 C {#a-little-c-with-your-rust}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/interoperability/c-with-rust.html](https://doc.rust-lang.org/stable/embedded-book/interoperability/c-with-rust.html)


在 Rust 项目中使用 C 或 C++ 主要由两大部分组成：

- 为 Rust 使用而包装已暴露的 C API
- 构建你的 C 或 C++ 代码，以便与 Rust 代码集成

由于 C++ 没有供 Rust 编译器对接的稳定 ABI，建议在将 Rust 与 C 或 C++ 结合时使用 `C` ABI。

## 定义接口 {#defining-the-interface}

在从 Rust 消费 C 或 C++ 代码之前，有必要（在 Rust 中）定义链接代码中存在哪些数据类型与函数签名。在 C 或 C++ 中，你会包含定义这些数据的头文件（`.h` 或 `.hpp`）。在 Rust 中，必须手动将这些定义翻译成 Rust，或使用工具生成这些定义。

首先，我们介绍如何手动将 C/C++ 定义翻译成 Rust。

### 包装 C 函数与数据类型 {#wrapping-c-functions-and-datatypes}

用 C 或 C++ 编写的库通常会提供头文件，定义公共接口中使用的所有类型与函数。示例文件可能如下所示：

```C
/* 文件：cool.h */
typedef struct CoolStruct {
    int x;
    int y;
} CoolStruct;

void cool_function(int i, char c, CoolStruct* cs);
```

翻译成 Rust 后，该接口如下所示：

```rust,ignore
/* 文件：cool_bindings.rs */
#[repr(C)]
pub struct CoolStruct {
    pub x: cty::c_int,
    pub y: cty::c_int,
}

extern "C" {
    pub fn cool_function(
        i: cty::c_int,
        c: cty::c_char,
        cs: *mut CoolStruct
    );
}
```

让我们逐段查看这一定义，解释各部分。

```rust,ignore
#[repr(C)]
pub struct CoolStruct { ... }
```

默认情况下，Rust 不保证 `struct` 中数据的顺序、填充或大小。为了保证与 C 代码的兼容性，我们加入 `#[repr(C)]` 属性，指示 Rust 编译器始终使用与 C 相同的规则来组织结构体中的数据。

```rust,ignore
pub x: cty::c_int,
pub y: cty::c_int,
```

由于 C 或 C++ 对 `int` 或 `char` 的定义很灵活，建议使用 `cty` 中定义的原始数据类型，它会把 C 类型映射到 Rust 类型。

```rust,ignore
extern "C" { pub fn cool_function( ... ); }
```

这条语句定义了一个使用 C ABI、名为 `cool_function` 的函数签名。只定义签名而不定义函数体，意味着该函数的定义需要在别处提供，或从静态库链接到最终库或二进制文件中。

```rust,ignore
    i: cty::c_int,
    c: cty::c_char,
    cs: *mut CoolStruct
```

与上文的数据类型类似，我们使用与 C 兼容的定义来声明函数参数的数据类型。为清晰起见，我们也保留相同的参数名。

这里有一个新类型：`*mut CoolStruct`。由于 C 没有 Rust 引用（形如 `&mut CoolStruct`）的概念，我们改用裸指针。解引用该指针是 `unsafe` 的，且指针实际上可能是 `null`，因此在与 C 或 C++ 代码交互时必须谨慎，以确保 Rust 通常提供的保证。

### 自动生成接口 {#automatically-generating-the-interface}

与其手动生成这些接口（可能繁琐且易错），可以使用名为 [bindgen] 的工具自动完成转换。关于 [bindgen] 的用法说明，请参阅 [bindgen 用户手册]，不过典型流程通常包括以下步骤：

1. 收集你希望与 Rust 一起使用的、定义接口或数据类型的所有 C 或 C++ 头文件。
2. 编写一个 `bindings.h` 文件，其中 `#include "..."` 第 1 步收集的每个文件。
3. 将该 `bindings.h` 文件，连同用于编译代码的任何编译标志，一并交给 `bindgen`。提示：使用 `Builder.ctypes_prefix("cty")` /
  `--ctypes-prefix=cty` 以及 `Builder.use_core()` / `--use-core`，可使生成的代码与 `#![no_std]` 兼容。
4. `bindgen` 会把生成的 Rust 代码输出到终端窗口。该输出可以管道写入项目中的文件，例如 `bindings.rs`。你可以在 Rust 项目中使用该文件，与作为外部库编译并链接的 C/C++ 代码交互。提示：如果生成绑定中的类型以 `cty` 为前缀，别忘了使用 [`cty`](https://crates.io/crates/cty) crate。

[bindgen]: https://github.com/rust-lang/rust-bindgen
[bindgen 用户手册]: https://rust-lang.github.io/rust-bindgen/

## 构建你的 C/C++ 代码 {#building-your-cc-code}

由于 Rust 编译器并不直接知道如何编译 C 或 C++ 代码（或任何其它提供 C 接口的语言的代码），有必要提前编译非 Rust 代码。

对于嵌入式项目，这通常意味着将 C/C++ 代码编译成静态归档（例如 `cool-library.a`），然后在最终链接步骤与 Rust 代码合并。

若你想使用的库已经以静态归档形式分发，则不必重新构建代码。只需按上文所述转换所提供的接口头文件，并在编译/链接时包含该静态归档即可。

若你的代码以源码项目形式存在，则需要将 C/C++ 代码编译为静态库，方法是触发现有构建系统（例如 `make`、`CMake` 等），或将必要的编译步骤移植为使用名为 `cc` 的 crate。这两种方式都需要使用 `build.rs` 脚本。

### Rust `build.rs` 构建脚本 {#rust-buildrs-build-scripts}

`build.rs` 脚本是用 Rust 语法编写的文件，在你的编译机器上执行：在项目依赖构建完成 *之后*，但在项目本身构建 *之前*。

完整参考见[此处](https://doc.rust-lang.org/cargo/reference/build-scripts.html)。`build.rs` 脚本适用于生成代码（例如通过 [bindgen]）、调用外部构建系统如 `Make`，或通过 `cc` crate 直接编译 C/C++。

### 触发外部构建系统 {#triggering-external-build-systems}

对于有复杂外部项目或构建系统的工程，最简单的做法可能是使用 [`std::process::Command`]「外壳调用」其它构建系统：遍历相对路径，执行固定命令（例如 `make library`），然后将得到的静态库复制到 `target` 构建目录中的合适位置。

尽管你的 crate 可能面向 `no_std` 嵌入式平台，但 `build.rs` 只在编译该 crate 的机器上执行。这意味着你可以使用任何能在编译主机上运行的 Rust crate。

[`std::process::Command`]: https://doc.rust-lang.org/std/process/struct.Command.html

### 用 `cc` crate 构建 C/C++ 代码 {#building-cc-code-with-the-cc-crate}

对于依赖或复杂度有限的项目，或难以修改构建系统以生成静态库（而非最终二进制/可执行文件）的项目，改用 [`cc` crate] 可能更容易，它为主机提供的编译器提供了符合习惯的 Rust 接口。

[`cc` crate]: https://github.com/alexcrichton/cc-rs

在最简单的情况下——将单个 C 文件编译为依赖静态库——使用 [`cc` crate] 的示例 `build.rs` 脚本如下：

```rust,ignore
fn main() {
    cc::Build::new()
        .file("src/foo.c")
        .compile("foo");
}
```

`build.rs` 放在包的根目录。然后 `cargo build` 会在构建该包之前编译并执行它。会生成名为 `libfoo.a` 的静态归档，并放在 `target` 目录中。
