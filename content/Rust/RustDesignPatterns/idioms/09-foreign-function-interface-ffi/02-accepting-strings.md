+++
title = "02-接受字符串"
date = 2026-08-18T22:10:00+08:00
weight = 15
type = "docs"
description = "接受字符串 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/ffi/accepting-strings.html](https://rust-unofficial.github.io/patterns/idioms/ffi/accepting-strings.html)

# 接受字符串

## 描述 {#description}

通过指针经 FFI 接受字符串时，应遵循两条原则：

1. 将外部字符串保持为“借用”，而不是直接复制。
2. 尽量减少把 C 风格字符串转换为原生 Rust 字符串时涉及的复杂度和 `unsafe` 代码。

## 动机 {#motivation}

C 中使用的字符串与 Rust 中的行为不同，具体而言：

- C 字符串以空字符结尾，而 Rust 字符串存储自身长度
- C 字符串可以包含任意非零字节，而 Rust 字符串必须是 UTF-8
- C 字符串通过 `unsafe` 指针操作访问和操作，而与 Rust 字符串的交互则通过安全方法完成

Rust 标准库提供了与 `String` 和 `&str` 对应的 C 版本，分别是 `CString` 和 `&CStr`，使我们能避免在 C 字符串与 Rust 字符串之间转换时涉及的大量复杂度和 `unsafe` 代码。

`&CStr` 类型还允许我们处理借用数据，这意味着在 Rust 与 C 之间传递字符串是零成本操作。

## 代码示例 {#code-example}

```rust,ignore
pub mod unsafe_module {

    // 模块的其他内容

    /// 以指定级别记录一条消息。
    ///
    /// # 安全性
    ///
    /// 调用者必须保证 `msg`：
    ///
    /// - 不是空指针
    /// - 指向有效、已初始化的数据
    /// - 指向以空字节结尾的内存
    /// - 在本次函数调用期间不会被修改
    #[no_mangle]
    pub unsafe extern "C" fn mylib_log(msg: *const libc::c_char, level: libc::c_int) {
        let level: crate::LogLevel = match level { /* ... */ };

        // SAFETY: 调用者已经保证这样做是安全的（见文档注释中的
        // `# 安全性` 一节）。
        let msg_str: &str = match std::ffi::CStr::from_ptr(msg).to_str() {
            Ok(s) => s,
            Err(e) => {
                crate::log_error("FFI string conversion failed");
                return;
            }
        };

        crate::log(msg_str, level);
    }
}
```

## 优点 {#advantages}

该示例的写法确保了：

1. `unsafe` 块尽可能小。
2. 生命周期“未被跟踪”的指针变成了“被跟踪”的共享引用

考虑一种替代做法，即实际复制字符串：

```rust,ignore
pub mod unsafe_module {

    // 模块的其他内容

    pub extern "C" fn mylib_log(msg: *const libc::c_char, level: libc::c_int) {
        // 不要使用这段代码。
        // 它又丑又冗长，而且包含一个隐蔽的 bug。

        let level: crate::LogLevel = match level { /* ... */ };

        let msg_len = unsafe { /* SAFETY: strlen 该怎样就怎样，大概？ */
            libc::strlen(msg)
        };

        let mut msg_data = Vec::with_capacity(msg_len + 1);

        let msg_cstr: std::ffi::CString = unsafe {
            // SAFETY: 从预期存活整个栈帧的外部指针复制到
            // 自有内存中
            std::ptr::copy_nonoverlapping(msg, msg_data.as_mut(), msg_len);

            msg_data.set_len(msg_len + 1);

            std::ffi::CString::from_vec_with_nul(msg_data).unwrap()
        }

        let msg_str: String = unsafe {
            match msg_cstr.into_string() {
                Ok(s) => s,
                Err(e) => {
                    crate::log_error("FFI string conversion failed");
                    return;
                }
            }
        };

        crate::log(&msg_str, level);
    }
}
```

这段代码在两方面都不如原先的版本：

1. `unsafe` 代码多得多，更重要的是，需要维持的不变量也更多。
2. 由于需要大量算术运算，这个版本有一个会导致 Rust `undefined behaviour` 的 bug。

这里的 bug 是指针算术上的一个简单错误：字符串被复制了，复制了全部 `msg_len` 个字节。然而，末尾的 `NUL` 终止符没有被复制。

随后 Vector 的大小被*设置*为*零填充字符串*的长度——而不是*调整大小*到该长度（后者本可以在末尾补上一个零）。结果，Vector 的最后一个字节是未初始化内存。当在该代码块底部创建 `CString` 时，它对 Vector 的读取将导致 `undefined behaviour`！

和许多此类问题一样，这个问题很难追查。有时会因为字符串不是 `UTF-8` 而 panic，有时会在字符串末尾放一个奇怪的字符，有时则会直接彻底崩溃。

## 缺点 {#disadvantages}

没有？
