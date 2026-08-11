+++
title = "02-在 C 中使用一点 Rust"
date = 2026-08-01T10:38:00+08:00
weight = 149
type = "docs"
description = "在 C 中使用一点 Rust（A little Rust with your C）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 在 C 中使用一点 Rust {#a-little-rust-with-your-c}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/interoperability/rust-with-c.html](https://doc.rust-lang.org/stable/embedded-book/interoperability/rust-with-c.html)


在 C 或 C++ 项目中使用 Rust 代码主要由两部分组成。

- 在 Rust 中创建对 C 友好的 API
- 将你的 Rust 项目嵌入外部构建系统

除了 `cargo` 与 `meson`，多数构建系统没有原生 Rust 支持。
因此，编译你的 crate 及其依赖时，最稳妥的做法通常就是使用 `cargo`。

## 搭建项目 {#setting-up-a-project}

像往常一样创建新的 `cargo` 项目。

有一些标志可以告诉 `cargo` 生成系统库，而不是常规的 Rust 目标。
这还允许你为库设置不同的输出名称，
如果你希望它与 crate 的其余部分不同。

```toml
[lib]
name = "your_crate"
crate-type = ["cdylib"]      # 创建动态库
# crate-type = ["staticlib"] # 创建静态库
```

## 构建 `C` API {#building-a-c-api}

因为 C++ 没有供 Rust 编译器对接的稳定 ABI，我们在不同语言之间的任何互操作都使用 `C`。
在 C 与 C++ 代码中使用 Rust 也不例外。

### `#[no_mangle]`

Rust 编译器修饰符号名的方式与原生代码链接器所期望的不同。
因此，任何要从 Rust 导出、供 Rust 之外使用的函数，都需要告知编译器不要对其进行名称修饰。

### `extern "C"`

默认情况下，你在 Rust 中编写的任何函数都会使用
Rust ABI（同样也未稳定）。
相反，在构建对外 FFI API 时，我们需要
告诉编译器使用系统 ABI。

根据平台不同，你可能希望针对特定的 ABI 版本，文档见[此处](https://doc.rust-lang.org/reference/items/external-blocks.html)。

---

把这些部分合在一起，你会得到大致如下的函数。

```rust,ignore
#[no_mangle]
pub extern "C" fn rust_function() {

}
```

就像在 Rust 项目中使用 `C` 代码时一样，你现在需要把数据
转换为应用其余部分能够理解的形式，以及从该形式转换回来。

## 链接与更大的项目上下文 {#linking-and-greater-project-context}

那么，问题的一半已经解决了。
现在该如何使用它？

**这很大程度上取决于你的项目和/或构建系统**

`cargo` 会创建 `my_lib.so`/`my_lib.dll` 或 `my_lib.a` 文件，
取决于你的平台与设置。该库可以简单地由你的构建系统链接。

不过，从 C 调用 Rust 函数需要头文件来声明
函数签名。

你的 Rust-ffi API 中的每个函数都需要有对应的头文件声明。

```rust,ignore
#[no_mangle]
pub extern "C" fn rust_function() {}
```

就会变成

```C
void rust_function();
```

等等。

有一个工具可以自动化这一过程，
名为 [cbindgen]，它会分析你的 Rust 代码，
然后为你的 C 与 C++ 项目生成头文件。

[cbindgen]: https://github.com/eqrion/cbindgen

至此，从 C 使用 Rust 函数
就像包含头文件并调用它们一样简单！

```C
#include "my-rust-project.h"
rust_function();
```
