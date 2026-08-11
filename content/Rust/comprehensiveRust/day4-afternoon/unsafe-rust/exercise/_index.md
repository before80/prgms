+++
title = "3.7 练习：FFI 封装"
date = 2026-08-11T11:30:00+08:00
weight = 206
type = "docs"
description = "练习：FFI 封装 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-rust/exercise.html](https://google.github.io/comprehensive-rust/unsafe-rust/exercise.html)

# 3.7 练习：FFI 封装

Rust 对通过**外部函数接口**（foreign function interface，FFI）调用函数有很好的支持。我们将用它为 `libc` 中用于读取目录文件名的函数构建一层安全封装——也就是你在 C 里会用到的那些。

建议查阅手册页：

- [`opendir(3)`](https://man7.org/linux/man-pages/man3/opendir.3.html)
- [`readdir(3)`](https://man7.org/linux/man-pages/man3/readdir.3.html)
- [`closedir(3)`](https://man7.org/linux/man-pages/man3/closedir.3.html)

也建议浏览 [`std::ffi`] 模块。那里有本练习需要用到的多种字符串类型：

| 类型                       | 编码           | 用途                         |
| -------------------------- | -------------- | ---------------------------- |
| [`str`] 与 [`String`]      | UTF-8          | Rust 中的文本处理            |
| [`CStr`] 与 [`CString`]    | NUL 结尾       | 与 C 函数通信                |
| [`OsStr`] 与 [`OsString`]  | 操作系统相关   | 与操作系统通信               |

你需要在这些类型之间转换：

- `&str` 到 `CString`：需要为末尾的 `\0` 字符分配空间，
- `CString` 到 `*const c_char`：需要指针才能调用 C 函数，
- `*const c_char` 到 `&CStr`：需要能找到末尾 `\0` 字符的东西，
- `&CStr` 到 `&[u8]`：字节切片是“某些未知数据”的通用接口，
- `&[u8]` 到 `&OsStr`：`&OsStr` 是迈向 `OsString` 的一步，用
  [`OsStrExt`](https://doc.rust-lang.org/std/os/unix/ffi/trait.OsStrExt.html)
  创建它，
- `&OsStr` 到 `OsString`：需要克隆 `&OsStr` 中的数据才能返回，并再次调用 `readdir`。

[Nomicon] 也有一章关于 FFI 的内容非常有用。

[`std::ffi`]: https://doc.rust-lang.org/std/ffi/
[`str`]: https://doc.rust-lang.org/std/primitive.str.html
[`String`]: https://doc.rust-lang.org/std/string/struct.String.html
[`CStr`]: https://doc.rust-lang.org/std/ffi/struct.CStr.html
[`CString`]: https://doc.rust-lang.org/std/ffi/struct.CString.html
[`OsStr`]: https://doc.rust-lang.org/std/ffi/struct.OsStr.html
[`OsString`]: https://doc.rust-lang.org/std/ffi/struct.OsString.html
[Nomicon]: https://doc.rust-lang.org/nomicon/ffi.html

把下面的代码复制到 <https://play.rust-lang.org/>，并补全缺失的函数与方法：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
// TODO: 完成实现后删除本行。
#![allow(unused_imports, unused_variables, dead_code)]

mod ffi {
    use std::os::raw::{c_char, c_int};
    #[cfg(not(target_os = "macos"))]
    use std::os::raw::{c_long, c_uchar, c_ulong, c_ushort};

    // 不透明类型。参见 https://doc.rust-lang.org/nomicon/ffi.html。
    #[repr(C)]
    pub struct DIR {
        _data: [u8; 0],
        _marker: core::marker::PhantomData<(*mut u8, core::marker::PhantomPinned)>,
    }

    // 布局依据 Linux 手册页 readdir(3)；其中 ino_t 与 off_t
    // 按 /usr/include/x86_64-linux-gnu/{sys/types.h, bits/typesizes.h}
    // 中的定义解析。
    #[cfg(not(target_os = "macos"))]
    #[repr(C)]
    pub struct dirent {
        pub d_ino: c_ulong,
        pub d_off: c_long,
        pub d_reclen: c_ushort,
        pub d_type: c_uchar,
        pub d_name: [c_char; 256],
    }

    // 布局依据 macOS 手册页 dir(5)。
    #[cfg(target_os = "macos")]
    #[repr(C)]
    pub struct dirent {
        pub d_fileno: u64,
        pub d_seekoff: u64,
        pub d_reclen: u16,
        pub d_namlen: u16,
        pub d_type: u8,
        pub d_name: [c_char; 1024],
    }

    unsafe extern "C" {
        pub unsafe fn opendir(s: *const c_char) -> *mut DIR;

        #[cfg(not(all(target_os = "macos", target_arch = "x86_64")))]
        pub unsafe fn readdir(s: *mut DIR) -> *const dirent;

        // 参见 https://github.com/rust-lang/libc/issues/414 以及
        // macOS 手册页 stat(2) 中关于 _DARWIN_FEATURE_64_BIT_INODE 的章节。
        //
        // “这些更新可用之前就存在的平台”指的是
        // Intel 与 PowerPC 上的 macOS（相对于 iOS / wearOS 等）。
        #[cfg(all(target_os = "macos", target_arch = "x86_64"))]
        #[link_name = "readdir$INODE64"]
        pub unsafe fn readdir(s: *mut DIR) -> *const dirent;

        pub unsafe fn closedir(s: *mut DIR) -> c_int;
    }
}

use std::ffi::{CStr, CString, OsStr, OsString};
use std::os::unix::ffi::OsStrExt;

#[derive(Debug)]
struct DirectoryIterator {
    path: CString,
    dir: *mut ffi::DIR,
}

impl DirectoryIterator {
    fn new(path: &str) -> Result<DirectoryIterator, String> {
        // 调用 opendir；成功则返回 Ok，
        // 否则返回带消息的 Err。
        todo!()
    }
}

impl Iterator for DirectoryIterator {
    type Item = OsString;
    fn next(&mut self) -> Option<OsString> {
        // 持续调用 readdir，直到得到 NULL 指针。
        todo!()
    }
}

impl Drop for DirectoryIterator {
    fn drop(&mut self) {
        // 按需调用 closedir。
        todo!()
    }
}

fn main() -> Result<(), String> {
    let iter = DirectoryIterator::new(".")?;
    println!("files: {:#?}", iter.collect::<Vec<_>>());
    Ok(())
}
```

> <summary>讲师备注</summary>
>
> FFI 绑定代码通常由 [bindgen] 这类工具生成，而不是像这里这样手写。不过 bindgen 无法在在线 playground 中运行。


[bindgen]: https://github.com/rust-lang/rust-bindgen
