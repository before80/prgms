+++
title = "3.7.1 解答"
date = 2026-08-11T11:30:00+08:00
weight = 207
type = "docs"
description = "01-解答 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-rust/solution.html](https://google.github.io/comprehensive-rust/unsafe-rust/solution.html)

# 3.7.1 解答

单元测试使用 [`tempfile`](https://docs.rs/tempfile/) crate。用下面命令把它加为开发依赖：

```shell
cargo add --dev tempfile
```

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
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
        let path =
            CString::new(path).map_err(|err| format!("Invalid path: {err}"))?;
        // SAFETY: path.as_ptr() 不可能为 NULL。
        let dir = unsafe { ffi::opendir(path.as_ptr()) };
        if dir.is_null() {
            Err(format!("Could not open {path:?}"))
        } else {
            Ok(DirectoryIterator { path, dir })
        }
    }
}

impl Iterator for DirectoryIterator {
    type Item = OsString;
    fn next(&mut self) -> Option<OsString> {
        // 持续调用 readdir，直到得到 NULL 指针。
        // SAFETY: self.dir 永不为 NULL。
        let dirent = unsafe { ffi::readdir(self.dir) };
        if dirent.is_null() {
            // 已到达目录末尾。
            return None;
        }
        // SAFETY: dirent 非 NULL，且 dirent.d_name 以 NUL 结尾。
        let d_name = unsafe { CStr::from_ptr((*dirent).d_name.as_ptr()) };
        let os_str = OsStr::from_bytes(d_name.to_bytes());
        Some(os_str.to_owned())
    }
}

impl Drop for DirectoryIterator {
    fn drop(&mut self) {
        // 按需调用 closedir。
        // SAFETY: self.dir 永不为 NULL。
        if unsafe { ffi::closedir(self.dir) } != 0 {
            panic!("Could not close {:?}", self.path);
        }
    }
}

fn main() -> Result<(), String> {
    let iter = DirectoryIterator::new(".")?;
    println!("files: {:#?}", iter.collect::<Vec<_>>());
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::error::Error;

    #[test]
    fn test_nonexisting_directory() {
        let iter = DirectoryIterator::new("no-such-directory");
        assert!(iter.is_err());
    }

    #[test]
    fn test_empty_directory() -> Result<(), Box<dyn Error>> {
        let tmp = tempfile::TempDir::new()?;
        let iter = DirectoryIterator::new(
            tmp.path().to_str().ok_or("Non UTF-8 character in path")?,
        )?;
        let mut entries = iter.collect::<Vec<_>>();
        entries.sort();
        assert_eq!(entries, &[".", ".."]);
        Ok(())
    }

    #[test]
    fn test_nonempty_directory() -> Result<(), Box<dyn Error>> {
        let tmp = tempfile::TempDir::new()?;
        std::fs::write(tmp.path().join("foo.txt"), "The Foo Diaries\n")?;
        std::fs::write(tmp.path().join("bar.png"), "<PNG>\n")?;
        std::fs::write(tmp.path().join("crab.rs"), "//! Crab\n")?;
        let iter = DirectoryIterator::new(
            tmp.path().to_str().ok_or("Non UTF-8 character in path")?,
        )?;
        let mut entries = iter.collect::<Vec<_>>();
        entries.sort();
        assert_eq!(entries, &[".", "..", "bar.png", "crab.rs", "foo.txt"]);
        Ok(())
    }
}
```

- **Safety 注释：** 每个 `unsafe` 块前都有 `// SAFETY:` 注释，说明为何该操作是安全的。这是 Rust 中便于审计的标准做法。
- **字符串转换：** 代码演示了 FFI 所需的转换：
  - `&str` -> `CString`：创建供 C 使用的以空字符结尾的字符串。
  - `CString` -> `*const c_char`：把指针传给 C。
  - `*const c_char` -> `&CStr`：包装返回的 C 字符串。
  - `&CStr` -> `&[u8]` -> `&OsStr` -> `OsString`：把字节转回 Rust 的 OS 字符串。
- **RAII（`Drop`）：** 实现 `Drop`，在迭代器离开作用域时自动调用 `closedir`，确保不泄漏文件描述符。
- **Iterator 接口：** 把 C API 封装成 Rust `Iterator`，为底层的 unsafe C 函数提供安全、惯用的接口（`next` 返回 `Option<OsString>`）。

> <summary>讲师备注</summary>
>
> - 说明 `CString` 拥有数据（类似 `String`），而 `CStr` 是借用引用（类似 `&str`）。
> - 在 Unix 系统上需要 `OsStrExt` trait，才能把字节直接转成 `OsStr`。

