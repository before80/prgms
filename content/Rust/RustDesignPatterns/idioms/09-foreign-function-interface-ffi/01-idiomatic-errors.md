+++
title = "01-地道的错误处理"
date = 2026-08-18T22:10:00+08:00
weight = 14
type = "docs"
description = "地道的错误处理 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/ffi/errors.html](https://rust-unofficial.github.io/patterns/idioms/ffi/errors.html)

# 地道的错误处理

## 描述 {#description}

在 C 等外部语言中，错误由返回码表示。然而，Rust 的类型系统能捕获丰富得多的错误信息，并通过完整类型传播。

本最佳实践展示了不同类型的错误码，以及如何以可用的方式对外暴露它们：

1. 扁平枚举应转换为整数并作为错误码返回。
2. 结构化枚举应转换为整数错误码，并附带字符串错误消息作为细节。
3. 自定义错误类型应变得“透明”，并采用 C 表示。

## 代码示例 {#code-example}

### 扁平枚举 {#flat-enums}

```rust,ignore
enum DatabaseError {
    IsReadOnly = 1,    // 用户尝试了写操作
    IOError = 2,       // 用户应读取 C 的 errno() 以得知具体原因
    FileCorrupted = 3, // 用户应运行修复工具来恢复
}

impl From<DatabaseError> for libc::c_int {
    fn from(e: DatabaseError) -> libc::c_int {
        (e as i8).into()
    }
}
```

### 结构化枚举 {#structured-enums}

```rust,ignore
pub mod errors {
    enum DatabaseError {
        IsReadOnly,
        IOError(std::io::Error),
        FileCorrupted(String), // 描述问题的消息
    }

    impl From<DatabaseError> for libc::c_int {
        fn from(e: DatabaseError) -> libc::c_int {
            match e {
                DatabaseError::IsReadOnly => 1,
                DatabaseError::IOError(_) => 2,
                DatabaseError::FileCorrupted(_) => 3,
            }
        }
    }
}

pub mod c_api {
    use super::errors::DatabaseError;
    use core::ptr;

    #[no_mangle]
    pub extern "C" fn db_error_description(
        e: Option<ptr::NonNull<DatabaseError>>,
    ) -> Option<ptr::NonNull<libc::c_char>> {
        // SAFETY: 我们假定 `e` 的生命周期长于
        // 当前栈帧。
        let error = unsafe { e?.as_ref() };

        let error_str: String = match error {
            DatabaseError::IsReadOnly => {
                format!("cannot write to read-only database")
            }
            DatabaseError::IOError(e) => {
                format!("I/O Error: {e}")
            }
            DatabaseError::FileCorrupted(s) => {
                format!("File corrupted, run repair: {}", &s)
            }
        };

        let error_bytes = error_str.as_bytes();

        let c_error = unsafe {
            // SAFETY: 将 error_bytes 复制到已分配的缓冲区，并在末尾写入 '\0'
            // 字节。
            let buffer = ptr::NonNull::<u8>::new(libc::malloc(error_bytes.len() + 1).cast())?;

            buffer
                .as_ptr()
                .copy_from_nonoverlapping(error_bytes.as_ptr(), error_bytes.len());
            buffer.as_ptr().add(error_bytes.len()).write(0_u8);
            buffer
        };

        Some(c_error.cast())
    }
}
```

### 自定义错误类型 {#custom-error-types}

```rust,ignore
struct ParseError {
    expected: char,
    line: u32,
    ch: u16,
}

impl ParseError {
    /* ... */
}

/* 创建第二个版本，作为 C 结构体对外暴露 */
#[repr(C)]
pub struct parse_error {
    pub expected: libc::c_char,
    pub line: u32,
    pub ch: u16,
}

impl From<ParseError> for parse_error {
    fn from(e: ParseError) -> parse_error {
        let ParseError { expected, line, ch } = e;
        parse_error { expected, line, ch }
    }
}
```

## 优点 {#advantages}

这能确保外部语言可以清楚地获取错误信息，同时完全不损害 Rust 代码的 API。

## 缺点 {#disadvantages}

需要写很多代码，而且有些类型可能不容易转换成 C。
