+++
title = "9.7 练习：C 库"
date = 2026-08-11T11:30:00+08:00
weight = 573
type = "docs"
description = "06-练习：C 库 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/c-library-example.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/c-library-example.html)

# 9.7 练习：C 库

```c
#ifndef TEXT_ANALYSIS_H
#define TEXT_ANALYSIS_H

#include <stddef.h>
#include <stdbool.h>

typedef struct TextAnalyst TextAnalyst;

typedef struct {
    const char* start;
    size_t length;
    size_t index;
} Token;

typedef enum {
    TA_OK = 0,
    TA_ERR_NULL_POINTER,
    TA_ERR_OUT_OF_MEMORY,
    TA_ERR_OTHER,
} TAError;

/* 返回 `false` 表示未找到 token。 */
typedef bool (*Tokenizer)(Token* token, void* extra_context);


typedef bool (*TokenCallback)(void* user_context, Token* token, void* result);

/* TextAnalyst 构造函数 */
TextAnalyst* ta_new(void);

/* TextAnalyst 析构函数 */
void ta_free(TextAnalyst* ta);

/* 重置状态以清除当前文档 */
void ta_reset(TextAnalyst* ta);

/* 使用自定义分词器（默认为空白符） */
void ta_set_tokenizer(TextAnalyst* ta, Tokenizer* func);

TAError ta_set_text(TextAnalyst* ta, const char* text, size_t len, bool make_copy);

/* 对每个 token 应用 `callback` */
size_t ta_foreach_token(const TextAnalyst* ta, const TokenCallback* callback, void* user_context);

/* 获取人类可读的错误信息 */
const char* ta_error_string(TAError error);

#endif /* TEXT_ANALYSIS_H */
```

> C 库常用 `void*` 参数隐藏实现细节。
>
> 考虑这个自然语言处理库的头文件，它隐藏了 `TextAnalyst` 与 `Analysis` 类型。
>
> 在 Rust 中可用类似下面的类型来模拟：
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> #[repr(C)]
> pub struct TextAnalyst {
>     _private: [u8; 0],
> }
> ```
>
> 练习：请学员为该库编写包装器。
>
> _建议解法_
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> // ffi.rs
> use std::ffi::c_char;
> use std::os::raw::c_void;
>
> #[repr(C)]
> pub struct TextAnalyst {
>     _private: [u8; 0],
> }
>
> #[repr(C)]
> #[derive(Debug, Clone, Copy)]
> pub struct Token {
>     pub start: *const c_char,
>     pub length: usize,
>     pub index: usize,
> }
>
> #[repr(C)]
> #[derive(Debug, Clone, Copy, PartialEq, Eq)]
> pub enum TAError {
>     Ok = 0,
>     NullPointer = 1,
>     OutOfMemory = 2,
>     Other = 3,
> }
>
> pub type Tokenizer = Option<
>     unsafe extern "C" fn(token: *mut Token, extra_context: *mut c_void) -> bool,
> >;
>
> pub type TokenCallback = Option<
>     unsafe extern "C" fn(
>         user_context: *mut c_void,
>         token: *mut Token,
>         result: *mut c_void,
>     ) -> bool,
> >;
>
> unsafe extern "C" {
>     pub fn ta_new() -> *mut TextAnalyst;
>
>     pub fn ta_free(ta: *mut TextAnalyst);
>
>     pub fn ta_reset(ta: *mut TextAnalyst);
>
>     pub fn ta_set_tokenizer(ta: *mut TextAnalyst, func: *const Tokenizer);
>
>     pub fn ta_set_text(
>         ta: *mut TextAnalyst,
>         text: *const c_char,
>         len: usize,
>         make_copy: bool,
>     ) -> TAError;
>
>     pub fn ta_foreach_token(
>         ta: *const TextAnalyst,
>         callback: *const TokenCallback,
>         user_context: *mut c_void,
>     ) -> usize;
>
>     pub fn ta_error_string(error: TAError) -> *const c_char;
> }
> ```

