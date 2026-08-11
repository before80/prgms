+++
title = "第11章 外部函数接口（FFI）"
date = 2026-08-06T17:08:00+08:00
weight = 61
type = "docs"
description = "与 C 等语言互操作"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 外部函数接口（FFI）


> 原文链接: [https://doc.rust-lang.org/nomicon/ffi.html](https://doc.rust-lang.org/nomicon/ffi.html)


## 简介

　　本指南以 [snappy](https://github.com/google/snappy) 压缩/解压库为例，介绍如何为外部代码编写绑定。Rust 目前无法直接调用 C++ 库，但 snappy 提供了 C 接口（见 [`snappy-c.h`](https://github.com/google/snappy/blob/master/snappy-c.h) 文档）。

## 关于 libc

　　许多示例使用 [libc crate][libc]，它提供 C 类型定义等。若自行尝试这些示例，需在 `Cargo.toml` 中添加 `libc`：

```toml
[dependencies]
libc = "0.2.0"
```

[libc]: https://crates.io/crates/libc

## 准备构建脚本

　　[snappy](https://github.com/google/snappy) 默认是静态库，输出产物中不会链接 stdc++。要在 Rust 中使用此外部库，必须手动指定将 stdc++ 链接到项目。最简单的方式是设置构建脚本。

　　先在 `Cargo.toml` 的 `package` 中添加 `build = "build.rs"`：

```toml
[package]
...
build = "build.rs"
```

　　然后在工作区根目录创建 `build.rs`：

```rust
// build.rs
fn main() {
    println!("cargo:rustc-link-lib=dylib=stdc++"); // 某些环境下此行可能不需要。
    println!("cargo:rustc-link-search=<YOUR SNAPPY LIBRARY PATH>");
}
```

　　更多信息见 [The Cargo Book - build script](https://doc.rust-lang.org/cargo/reference/build-scripts.html)。


## 调用外部函数

　　下面是调用外部函数的最小示例，若已安装 snappy 则可编译：

```rust,ignore
use libc::size_t;

#[link(name = "snappy")]
unsafe extern "C" {
    fn snappy_max_compressed_length(source_length: size_t) -> size_t;
}

fn main() {
    let x = unsafe { snappy_max_compressed_length(100) };
    println!("max compressed length of a 100 byte buffer: {}", x);
}
```

　　`extern` 块列出外部库中的函数签名，此处为平台 C ABI。`#[link(...)]` 属性指示链接器链接 snappy 库以解析符号。

　　外部函数假定不安全，调用须包在 `unsafe {}` 中，向编译器承诺块内确实安全。C 库常暴露非线程安全接口，几乎任何接受指针参数的函数对所有可能输入都不成立，因为指针可能悬垂，裸指针超出 Rust 安全内存模型。

　　声明外部函数参数类型时，Rust 编译器无法检查声明是否正确，因此正确声明是保持绑定在运行时正确的部分工作。

　　`extern` 块可扩展覆盖整个 snappy API：

```rust,ignore
use libc::{c_int, size_t};

#[link(name = "snappy")]
unsafe extern "C" {
    fn snappy_compress(input: *const u8,
                       input_length: size_t,
                       compressed: *mut u8,
                       compressed_length: *mut size_t) -> c_int;
    fn snappy_uncompress(compressed: *const u8,
                         compressed_length: size_t,
                         uncompressed: *mut u8,
                         uncompressed_length: *mut size_t) -> c_int;
    fn snappy_max_compressed_length(source_length: size_t) -> size_t;
    fn snappy_uncompressed_length(compressed: *const u8,
                                  compressed_length: size_t,
                                  result: *mut size_t) -> c_int;
    fn snappy_validate_compressed_buffer(compressed: *const u8,
                                         compressed_length: size_t) -> c_int;
}
# fn main() {}
```

## 创建安全接口

　　原始 C API 需要包装以提供内存安全，并运用 vector 等高层概念。库可选择只暴露安全的高层接口，隐藏不安全的内部细节。

　　包装期望缓冲区的函数时，用 `slice::raw` 模块把 Rust vector 当作内存指针操作。Rust vector 保证是连续内存块。length 是当前元素数，capacity 是已分配内存的总元素容量。length 小于等于 capacity。

```rust,ignore
# use libc::{c_int, size_t};
# unsafe fn snappy_validate_compressed_buffer(_: *const u8, _: size_t) -> c_int { 0 }
# fn main() {}
pub fn validate_compressed_buffer(src: &[u8]) -> bool {
    unsafe {
        snappy_validate_compressed_buffer(src.as_ptr(), src.len() as size_t) == 0
    }
}
```

　　上面的 `validate_compressed_buffer` 包装使用了 `unsafe` 块，但通过函数签名不带 `unsafe`，保证对所有输入调用都是安全的。

　　`snappy_compress` 和 `snappy_uncompress` 更复杂，因为还要分配缓冲区存放输出。

　　`snappy_max_compressed_length` 可用于分配容量足够容纳压缩输出的 vector，再作为输出参数传给 `snappy_compress`。还传入输出参数以在压缩后取真实长度并设置 length。

```rust,ignore
# use libc::{size_t, c_int};
# unsafe fn snappy_compress(a: *const u8, b: size_t, c: *mut u8,
#                           d: *mut size_t) -> c_int { 0 }
# unsafe fn snappy_max_compressed_length(a: size_t) -> size_t { a }
# fn main() {}
pub fn compress(src: &[u8]) -> Vec<u8> {
    unsafe {
        let srclen = src.len() as size_t;
        let psrc = src.as_ptr();

        let mut dstlen = snappy_max_compressed_length(srclen);
        let mut dst = Vec::with_capacity(dstlen as usize);
        let pdst = dst.as_mut_ptr();

        snappy_compress(psrc, srclen, pdst, &mut dstlen);
        dst.set_len(dstlen as usize);
        dst
    }
}
```

　　解压类似，因为 snappy 在压缩格式中存储未压缩大小，`snappy_uncompressed_length` 可取得所需缓冲区精确大小。

```rust,ignore
# use libc::{size_t, c_int};
# unsafe fn snappy_uncompress(compressed: *const u8,
#                             compressed_length: size_t,
#                             uncompressed: *mut u8,
#                             uncompressed_length: *mut size_t) -> c_int { 0 }
# unsafe fn snappy_uncompressed_length(compressed: *const u8,
#                                      compressed_length: size_t,
#                                      result: *mut size_t) -> c_int { 0 }
# fn main() {}
pub fn uncompress(src: &[u8]) -> Option<Vec<u8>> {
    unsafe {
        let srclen = src.len() as size_t;
        let psrc = src.as_ptr();

        let mut dstlen: size_t = 0;
        snappy_uncompressed_length(psrc, srclen, &mut dstlen);

        let mut dst = Vec::with_capacity(dstlen as usize);
        let pdst = dst.as_mut_ptr();

        if snappy_uncompress(psrc, srclen, pdst, &mut dstlen) == 0 {
            dst.set_len(dstlen as usize);
            Some(dst)
        } else {
            None // SNAPPY_INVALID_INPUT
        }
    }
}
```

　　然后可添加测试展示用法。

```rust,ignore
# use libc::{c_int, size_t};
# unsafe fn snappy_compress(input: *const u8,
#                           input_length: size_t,
#                           compressed: *mut u8,
#                           compressed_length: *mut size_t)
#                           -> c_int { 0 }
# unsafe fn snappy_uncompress(compressed: *const u8,
#                             compressed_length: size_t,
#                             uncompressed: *mut u8,
#                             uncompressed_length: *mut size_t)
#                             -> c_int { 0 }
# unsafe fn snappy_max_compressed_length(source_length: size_t) -> size_t { 0 }
# unsafe fn snappy_uncompressed_length(compressed: *const u8,
#                                      compressed_length: size_t,
#                                      result: *mut size_t)
#                                      -> c_int { 0 }
# unsafe fn snappy_validate_compressed_buffer(compressed: *const u8,
#                                             compressed_length: size_t)
#                                             -> c_int { 0 }
# fn main() { }
#
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn valid() {
        let d = vec![0xde, 0xad, 0xd0, 0x0d];
        let c: &[u8] = &compress(&d);
        assert!(validate_compressed_buffer(c));
        assert!(uncompress(c) == Some(d));
    }

    #[test]
    fn invalid() {
        let d = vec![0, 0, 0, 0];
        assert!(!validate_compressed_buffer(&d));
        assert!(uncompress(&d).is_none());
    }

    #[test]
    fn empty() {
        let d = vec![];
        assert!(!validate_compressed_buffer(&d));
        assert!(uncompress(&d).is_none());
        let c = compress(&d);
        assert!(validate_compressed_buffer(&c));
        assert!(uncompress(&c) == Some(d));
    }
}
```

## 析构函数

　　外部库常把资源所有权交给调用方。此时必须用 Rust 析构函数提供安全并保证释放这些资源（尤其在 panic 时）。

　　关于析构函数更多信息，见 [Drop trait](../std/ops/trait.Drop.html)。

## 从 C 调用 Rust 代码

　　你可能希望以可从 C 调用的方式编译 Rust 代码。这相当容易，但需要几件事。

### Rust 侧

　　假设 lib crate 名为 `rust_from_c`。`lib.rs` 应包含如下 Rust 代码：

```rust
#[unsafe(no_mangle)]
pub extern "C" fn hello_from_rust() {
    println!("Hello from Rust!");
}
# fn main() {}
```

　　`extern "C"` 使函数遵循 C 调用约定，见下文「[外部调用约定]」。`no_mangle` 属性关闭 Rust 名称修饰，使其有明确定义的可链接符号。

　　要把 Rust 编译为可从 C 调用的共享库，在 `Cargo.toml` 中添加：

```toml
[lib]
crate-type = ["cdylib"]
```

　　（注：也可用 `staticlib`，但还需调整一些链接标志。）

　　运行 `cargo build`，Rust 侧就准备好了。

[Foreign Calling Conventions]: ffi.md#foreign-calling-conventions

### C 侧

　　创建 C 文件调用 `hello_from_rust`，用 `gcc` 编译。

　　C 文件示例：

```c
extern void hello_from_rust();

int main(void) {
    hello_from_rust();
    return 0;
}
```

　　文件命名为 `call_rust.c`，放在 crate 根目录。编译：

```sh
gcc call_rust.c -o call_rust -lrust_from_c -L./target/debug
```

　　`-l` 和 `-L` 告诉 gcc 找到 Rust 库。

　　最后，指定 `LD_LIBRARY_PATH` 从 C 调用 Rust：

```sh
$ LD_LIBRARY_PATH=./target/debug ./call_rust
Hello from Rust!
```

　　就这样！更现实的例子见 [`cbindgen`]。

[`cbindgen`]: https://github.com/eqrion/cbindgen

## 从 C 代码回调 Rust 函数

　　部分外部库要求使用回调，向调用方报告当前状态或中间数据。可以把 Rust 中定义的函数传给外部库。要求是回调函数标记为 `extern` 并使用正确的调用约定，以便 C 代码可调用。

　　然后通过注册调用把回调函数发给 C 库，之后从 C 侧调用。

　　基本示例：

　　Rust 代码：

```rust,no_run
extern fn callback(a: i32) {
    println!("I'm called from C with value {0}", a);
}

#[link(name = "extlib")]
unsafe extern "C" {
   fn register_callback(cb: extern fn(i32)) -> i32;
   fn trigger_callback();
}

fn main() {
    unsafe {
        register_callback(callback);
        trigger_callback(); // 触发回调。
    }
}
```

　　C 代码：

```c
typedef void (*rust_callback)(int32_t);
rust_callback cb;

int32_t register_callback(rust_callback callback) {
    cb = callback;
    return 1;
}

void trigger_callback() {
  cb(7); // 将在 Rust 中调用 callback(7)。
}
```

　　此例中 Rust 的 `main()` 会调用 C 的 `trigger_callback()`，后者再回调 Rust 的 `callback()`。

## 将回调定向到 Rust 对象

　　前述示例展示如何从 C 调用全局函数。但常希望回调指向特定的 Rust 对象，例如代表相应 C 对象包装器的对象。

　　做法是把指向对象的裸指针传给 C 库。C 库可在通知中包含该 Rust 对象指针，使回调能不安全地访问被引用的 Rust 对象。

　　Rust 代码：

```rust,no_run
struct RustObject {
    a: i32,
    // 其他成员...
}

unsafe extern "C" fn callback(target: *mut RustObject, a: i32) {
    println!("I'm called from C with value {0}", a);
    unsafe {
        // 用回调收到的值更新 RustObject：
        (*target).a = a;
    }
}

#[link(name = "extlib")]
unsafe extern "C" {
   fn register_callback(target: *mut RustObject,
                        cb: unsafe extern "C" fn(*mut RustObject, i32)) -> i32;
   fn trigger_callback();
}

fn main() {
    // 创建将在回调中引用的对象：
    let mut rust_object = Box::new(RustObject { a: 5 });

    unsafe {
        register_callback(&mut *rust_object, callback);
        trigger_callback();
    }
}
```

　　C 代码：

```c
typedef void (*rust_callback)(void*, int32_t);
void* cb_target;
rust_callback cb;

int32_t register_callback(void* callback_target, rust_callback callback) {
    cb_target = callback_target;
    cb = callback;
    return 1;
}

void trigger_callback() {
  cb(cb_target, 7); // 将在 Rust 中调用 callback(&rustObject, 7)。
}
```

## 异步回调

　　前述示例中，回调是对外部 C 库函数调用的直接反应。当前线程的控制权从 Rust 切换到 C 再切回 Rust 执行回调，但回调仍在调用触发它的函数的同一线程上执行。

　　当外部库自行 spawn 线程并从那里调用回调时，情况更复杂。此时在回调内访问 Rust 数据结构尤其不安全，必须使用适当的同步机制。除 Mutex 等经典同步外，Rust 还可用 channel（`std::sync::mpsc`）把 C 线程回调中的数据转发到 Rust 线程。

　　若异步回调指向 Rust 地址空间中的特定对象，在相应 Rust 对象被销毁后，**绝对必须**确保 C 库不再执行任何回调。可在对象析构函数中注销回调，并设计库以保证注销后不会再有回调。

## 链接

　　`extern` 块上的 `link` 属性是指示 rustc 如何链接原生库的基本构件。目前 `link` 属性有两种形式：

* `#[link(name = "foo")]`
* `#[link(name = "foo", kind = "bar")]`

　　两种情况下 `foo` 是要链接的原生库名；第二种中 `bar` 是编译器链接的原生库类型。目前已知三种原生库类型：

* 动态库 - `#[link(name = "readline")]`
* 静态库 - `#[link(name = "my_build_dependency", kind = "static")]`
* Framework - `#[link(name = "CoreFoundation", kind = "framework")]`

　　注意 framework 仅 macOS 目标可用。

　　不同 `kind` 值用于区分原生库如何参与链接。从链接角度看，Rust 编译器产生两类产物：部分（rlib/staticlib）与最终（dylib/binary）。原生动态库与 framework 依赖会传播到最终产物边界，静态库依赖不传播，因为静态库直接并入后续产物。

　　此模型的若干用法：

* 原生构建依赖。写 Rust 时有时需要 C/C++ 胶水，但以库形式分发 C/C++ 代码是负担。此时代码归档为 `libfoo.a`，Rust crate 通过 `#[link(name = "foo", kind = "static")]` 声明依赖。

　　  无论 crate 输出哪种形式，原生静态库都会包含在输出中，意味着不必单独分发原生静态库。

* 普通动态依赖。常见系统库（如 `readline`）在大量系统上可用，且常找不到静态副本。当此依赖包含在 Rust crate 中时，部分目标（如 rlib）不会链接该库，但当 rlib 包含在最终目标（如 binary）中时，原生库会被链接。

　　在 macOS 上，framework 的语义与动态库相同。

## Unsafe 块

　　某些操作（如解引用裸指针或调用标记为 unsafe 的函数）只能在 unsafe 块内进行。Unsafe 块隔离不安全，并向编译器承诺不安全不会泄漏出块外。

　　Unsafe 函数则向外界声明这一点。写法如下：

```rust
unsafe fn kaboom(ptr: *const i32) -> i32 { *ptr }
```

　　此函数只能从 `unsafe` 块或另一个 `unsafe` 函数调用。

## 访问外部全局变量

　　外部 API 常导出全局变量，例如跟踪全局状态。要访问这些变量，在 `extern` 块中用 `static` 关键字声明：

```rust,ignore
#[link(name = "readline")]
unsafe extern "C" {
    static rl_readline_version: libc::c_int;
}

fn main() {
    println!("You have readline version {} installed.",
             unsafe { rl_readline_version as i32 });
}
```

　　或者，可能需要修改外部接口提供的全局状态。为此可用 `mut` 声明 static 以便修改。

```rust,ignore
use std::ffi::CString;
use std::ptr;

#[link(name = "readline")]
unsafe extern "C" {
    static mut rl_prompt: *const libc::c_char;
}

fn main() {
    let prompt = CString::new("[my-awesome-shell] $").unwrap();
    unsafe {
        rl_prompt = prompt.as_ptr();

        println!("{:?}", rl_prompt);

        rl_prompt = ptr::null();
    }
}
```

　　注意，与 `static mut` 的所有交互都不安全，读写皆是。处理全局可变状态需要格外小心。

## 外部调用约定

　　大多数外部代码暴露 C ABI，Rust 调用外部函数时默认使用平台的 C 调用约定。部分外部函数（尤其 Windows API）使用其他约定。Rust 提供方式告诉编译器使用哪种约定：

```rust,ignore
#[cfg(all(target_os = "win32", target_arch = "x86"))]
#[link(name = "kernel32")]
#[allow(non_snake_case)]
unsafe extern "stdcall" {
    fn SetEnvironmentVariableA(n: *const u8, v: *const u8) -> libc::c_int;
}
# fn main() { }
```

　　这应用于整个 `extern` 块。支持的 ABI 约束列表：

* `stdcall`
* `aapcs`
* `cdecl`
* `fastcall`
* `thiscall`
* `vectorcall`
　　  目前隐藏在 `abi_vectorcall` gate 后，可能变更。
* `Rust`
* `system`
* `C`
* `win64`
* `sysv64`

　　列表中多数 ABI 不言自明，但 `system` 可能显得奇怪。此约束选择适合与目标库互操作的 ABI。例如在 win32 x86 上意味着使用 `stdcall`；在 x86_64 上 Windows 使用 `C` 调用约定，因此用 `C`。因此前述示例可用 `extern "system" { ... }` 定义适用于所有 Windows 系统的块，而不只是 x86。

## 与外部代码的互操作

　　Rust 保证 `struct` 的布局与 C 在平台上的表示兼容，**仅当**对其应用 `#[repr(C)]` 属性时。`#[repr(C, packed)]` 可布局 struct 成员而不填充。`#[repr(C)]` 也可用于 enum。

　　Rust 的 owned box（`Box<T>`）用非空指针作为指向所含对象的句柄，但不应手动创建，因为它们由内部分配器管理。引用可安全假定为直接指向类型的非空指针。但破坏借用检查或可变性规则不保证安全，若需要可 prefer 裸指针（`*`），因为编译器对它们的假设更少。

　　Vector 与 string 共享相同的基本内存布局，`vec` 与 `str` 模块提供与 C API 协作的工具。但 string 不以 `\0` 结尾。若需要与 C 互操作的 NUL 结尾字符串，应使用 `std::ffi` 模块的 `CString` 类型。

　　[crates.io 上的 `libc` crate][libc] 在 `libc` 模块中包含 C 标准库的类型别名与函数定义，Rust 默认链接 `libc` 与 `libm`。

## 可变参数函数

　　在 C 中，函数可以是「可变参数」（variadic），即接受可变数量参数。Rust 可在外部函数声明的参数列表中用 `...` 实现：

```no_run
unsafe extern "C" {
    fn foo(x: i32, ...);
}

fn main() {
    unsafe {
        foo(10, 20, 30, 40, 50);
    }
}
```

　　普通 Rust 函数*不能*是可变参数的：

```rust,compile_fail
// 这不会编译

fn foo(x: i32, ...) {}
```

## 「可空指针优化」

　　某些 Rust 类型被定义为永不为 `null`，包括引用（`&T`、`&mut T`）、box（`Box<T>`）和函数指针（`extern "abi" fn()`）。与 C 互操作时，常使用可能为 `null` 的指针，似乎需要麻烦的 `transmute` 和/或不安全代码来处理与 Rust 类型的转换。但尝试构造/使用这些无效值**是未定义行为**，因此应使用以下变通方法。

　　作为特例，若 `enum` 恰好包含两个变体，其中一个不含数据，另一个包含上述非空类型之一的字段，则符合「可空指针优化」。这意味着不需要额外空间存 discriminant；空变体通过在非空字段中放入 `null` 值表示。这称为「优化」，但与其他优化不同，对符合类型的保证适用。

　　最常利用可空指针优化的类型是 `Option<T>`，其中 `None` 对应 `null`。因此 `Option<extern "C" fn(c_int) -> c_int>` 是用 C ABI 表示可空函数指针的正确方式（对应 C 类型 `int (*)(int)`）。

　　下面是一个刻意设计的例子。假设某 C 库提供注册回调的设施，在特定情况下调用。回调接收函数指针和整数，应使用该整数作为参数运行函数。因此函数指针在 FFI 边界双向传递。

```rust,ignore
use libc::c_int;

# #[cfg(hidden)]
unsafe extern "C" {
    /// 注册回调。
    fn register(cb: Option<extern "C" fn(Option<extern "C" fn(c_int) -> c_int>, c_int) -> c_int>);
}
# unsafe fn register(_: Option<extern "C" fn(Option<extern "C" fn(c_int) -> c_int>,
#                                            c_int) -> c_int>)
# {}

/// 这个相当无用的函数从 C 接收函数指针和整数，
/// 返回用该整数调用函数的结果。
/// 若未提供函数，默认对整数求平方。
extern "C" fn apply(process: Option<extern "C" fn(c_int) -> c_int>, int: c_int) -> c_int {
    match process {
        Some(f) => f(int),
        None    => int * int
    }
}

fn main() {
    unsafe {
        register(Some(apply));
    }
}
```

　　C 侧代码如下：

```c
void register(int (*f)(int (*)(int), int)) {
    ...
}
```

　　无需 `transmute`！

## FFI 与 unwinding

　　处理 FFI 时务必注意 unwinding。大多数 ABI 字符串有两种变体，一种带 `-unwind` 后缀，一种不带。`Rust` ABI 始终允许 unwinding，因此没有 `Rust-unwind` ABI。

　　若预期 Rust `panic` 或外部（如 C++）异常跨越 FFI 边界，该边界必须使用适当的 `-unwind` ABI 字符串。反之，若不预期 unwinding 跨越 ABI 边界，使用非 `-unwind` ABI 字符串。

> 注：用 `panic=abort` 编译时，`panic!` 仍会立即 abort 进程，与 panic 的函数指定何种 ABI 无关。

　　若 unwinding 操作遇到不允许 unwinding 的 ABI 边界，行为取决于 unwinding 来源（Rust `panic` 或外部异常）：

* `panic` 会导致进程安全 abort。
* 外部异常进入 Rust 会导致未定义行为。

　　注意 `catch_unwind` 与外部异常的交互**未定义**，`panic` 与外部异常捕获机制（尤其 C++ 的 `try`/`catch`）的交互亦然。

### Rust `panic` 与 `"C-unwind"`

```rust,ignore
#[unsafe(no_mangle)]
unsafe extern "C-unwind" fn example() {
    panic!("Uh oh");
}
```

　　此函数（在 `panic=unwind` 下编译）允许 unwinding C++ 栈帧。

```text
[带 `catch_unwind` 的 Rust 函数，停止 unwinding]
      |
     ...
      |
[C++ 帧]
      |                           ^
      | (调用)                    | (unwinding
      v                           |  沿此方向)
[Rust 函数 `example`]             |
      |                           |
      +--- Rust 函数 panic --------+
```

　　若 C++ 帧有对象，其析构函数会被调用。

### C++ `throw` 与 `"C-unwind"`

```rust,ignore
#[link(...)]
unsafe extern "C-unwind" {
    // 可能抛出异常的 C++ 函数
    fn may_throw();
}

#[unsafe(no_mangle)]
unsafe extern "C-unwind" fn rust_passthrough() {
    let b = Box::new(5);
    unsafe { may_throw(); }
    println!("{:?}", &b);
}
```

　　带 `try` 块的 C++ 函数可调用 `rust_passthrough` 并 `catch` 由 `may_throw` 抛出的异常。

```text
[带 `try` 块、调用 `rust_passthrough` 的 C++ 函数]
      |
     ...
      |
[Rust 函数 `rust_passthrough`]
      |                            ^
      | (调用)                     | (unwinding
      v                            |  沿此方向)
[C++ 函数 `may_throw`]             |
      |                            |
      +--- C++ 函数 throw ----------+
```

　　若 `may_throw` 抛出异常，`b` 会被 drop。否则打印 `5`。

### `panic` 可在 ABI 边界被停止

```rust
#[unsafe(no_mangle)]
extern "C" fn assert_nonzero(input: u32) {
    assert!(input != 0)
}
```

　　若用参数 `0` 调用 `assert_nonzero`，无论是否用 `panic=abort` 编译，运行时都保证（安全地）abort 进程。

### 预先捕获 `panic`

　　若编写可能 panic 的 Rust 代码，且不希望 panic 时 abort 进程，必须使用 [`catch_unwind`]：

```rust
use std::panic::catch_unwind;

#[unsafe(no_mangle)]
pub extern "C" fn oh_no() -> i32 {
    let result = catch_unwind(|| {
        panic!("Oops!");
    });
    match result {
        Ok(_) => 0,
        Err(_) => 1,
    }
}

fn main() {}
```

　　请注意 [`catch_unwind`] 只会捕获 unwinding 的 panic，不会捕获 abort 进程的 panic。更多信息见 [`catch_unwind`] 文档。

[`catch_unwind`]: ../std/panic/fn.catch_unwind.html

## 表示不透明 struct

　　有时 C 库想提供指向某物的指针，但不让你知道其内部细节。稳定且简单的方式是使用 `void *` 参数：

```c
void foo(void *arg);
void bar(void *arg);
```

　　Rust 中可用 `c_void` 类型表示：

```rust,ignore
unsafe extern "C" {
    pub fn foo(arg: *mut libc::c_void);
    pub fn bar(arg: *mut libc::c_void);
}
# fn main() {}
```

　　这是完全有效的处理方式。但我们可以做得更好。为解决这个问题，部分 C 库会创建 `struct`，其细节与内存布局私有，从而提供一定程度的类型安全。这些结构称为「不透明」（opaque）。C 示例：

```c
struct Foo; /* Foo 是结构体，但其内容不属于公开接口 */
struct Bar;
void foo(struct Foo *arg);
void bar(struct Bar *arg);
```

　　在 Rust 中，创建自己的不透明类型：

```rust
#[repr(C)]
pub struct Foo {
    _data: (),
    _marker:
        core::marker::PhantomData<(*mut u8, core::marker::PhantomPinned)>,
}
#[repr(C)]
pub struct Bar {
    _data: (),
    _marker:
        core::marker::PhantomData<(*mut u8, core::marker::PhantomPinned)>,
}

unsafe extern "C" {
    pub fn foo(arg: *mut Foo);
    pub fn bar(arg: *mut Bar);
}
# fn main() {}
```

　　通过至少包含一个私有字段且不提供构造函数，我们创建了无法在本模块外实例化的不透明类型。（无字段的 struct 任何人都可实例化。）还要在 FFI 中使用此类型，因此必须加 `#[repr(C)]`。marker 确保编译器不会将 struct 标记为 `Send`、`Sync` 和 `Unpin`。（`*mut u8` 不是 `Send` 或 `Sync`，`PhantomPinned` 不是 `Unpin`）

　　由于 `Foo` 与 `Bar` 类型不同，二者之间有类型安全，不会误把指向 `Foo` 的指针传给 `bar()`。

　　注意，用空 enum 作为 FFI 类型是极坏主意。编译器依赖空 enum 不可 inhabit，因此处理类型为 `&Empty` 的值是巨大陷阱，可能触发未定义行为导致程序出错。

> **注：** 最简单的方式是使用「extern types」。但目前（截至 2021 年 6 月）仍不稳定且有一些未决问题，详见 [RFC 页面][extern-type-rfc] 与 [跟踪 issue][extern-type-issue]。

[extern-type-issue]: https://github.com/rust-lang/rust/issues/43467
[extern-type-rfc]: https://rust-lang.github.io/rfcs/1861-extern-types.html
