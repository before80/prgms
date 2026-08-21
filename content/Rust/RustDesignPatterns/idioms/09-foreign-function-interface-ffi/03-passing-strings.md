+++
title = "03-传递字符串"
date = 2026-08-18T22:10:00+08:00
weight = 16
type = "docs"
description = "传递字符串 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/ffi/passing-strings.html](https://rust-unofficial.github.io/patterns/idioms/ffi/passing-strings.html)

# 传递字符串

## 描述 {#description}

向 FFI 函数传递字符串时，应遵循四条原则：

1. 尽量延长自有字符串的生命周期。
2. 在转换过程中尽量减少 `unsafe` 代码。
3. 如果 C 代码可能修改字符串数据，使用 `Vec` 而不是 `CString`。
4. 除非外部函数 API 有此要求，否则字符串的所有权不应转移给被调用方。

## 动机 {#motivation}

Rust 通过 `CString` 和 `CStr` 类型内置了对 C 风格字符串的支持。不过，从 Rust 函数向外部函数调用传递字符串时，可以采取不同的做法。

最佳实践很简单：以尽量减少 `unsafe` 代码的方式使用 `CString`。不过还有一个次要注意事项：*对象必须活得足够久*，也就是说生命周期应尽量拉长。此外，文档说明在修改后对 `CString` 做“往返”（round-tripping）是 UB，因此那种情况下还需要额外处理。

## 代码示例 {#code-example}

```rust,ignore
pub mod unsafe_module {

    // 模块的其他内容

    extern "C" {
        fn seterr(message: *const libc::c_char);
        fn geterr(buffer: *mut libc::c_char, size: libc::c_int) -> libc::c_int;
    }

    fn report_error_to_ffi<S: Into<String>>(err: S) -> Result<(), std::ffi::NulError> {
        let c_err = std::ffi::CString::new(err.into())?;

        unsafe {
            // SAFETY: 调用一个 FFI，其文档说明该指针是
            // const，因此不应发生修改
            seterr(c_err.as_ptr());
        }

        Ok(())
        // c_err 的生命周期一直持续到这里
    }

    fn get_error_from_ffi() -> Result<String, std::ffi::IntoStringError> {
        let mut buffer = vec![0u8; 1024];
        unsafe {
            // SAFETY: 调用一个 FFI，其文档暗示
            // 输入只需存活到本次调用结束
            let written: usize = geterr(buffer.as_mut_ptr(), 1023).into();

            buffer.truncate(written + 1);
        }

        std::ffi::CString::new(buffer).unwrap().into_string()
    }
}
```

## 优点 {#advantages}

该示例的写法确保了：

1. `unsafe` 块尽可能小。
2. `CString` 活得足够久。
3. 类型转换相关的错误在可能时总是会传播出去。

一个常见错误（常见到已经写进文档）是在第一个代码块中不使用变量：

```rust,ignore
pub mod unsafe_module {

    // 模块的其他内容

    fn report_error<S: Into<String>>(err: S) -> Result<(), std::ffi::NulError> {
        unsafe {
            // SAFETY: 糟糕，这里包含一个悬垂指针！
            seterr(std::ffi::CString::new(err.into())?.as_ptr());
        }
        Ok(())
    }
}
```

这段代码会产生悬垂指针，因为创建指针并不会延长 `CString` 的生命周期，这与创建引用时不同。

另一个经常被提出的问题是：初始化一个 1k 的全零 vector“很慢”。然而，较新版本的 Rust 实际上会把该宏优化成对 `zmalloc` 的调用，也就是说，其速度等同于操作系统返回已清零内存的能力（而这相当快）。

## 缺点 {#disadvantages}

没有？
