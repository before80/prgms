+++
title = "9.8 练习：C++ 库"
date = 2026-08-11T11:30:00+08:00
weight = 574
type = "docs"
description = "07-练习：C++ 库 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/cpp-library-example.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/cpp-library-example.html)

# 9.8 练习：C++ 库

C++ 头文件：interner.hpp

```cpp
#ifndef INTERNER_HPP
#define INTERNER_HPP

#include <string>
#include <unordered_set>

class StringInterner {
    std::unordered_set<std::string> strings;

public:
    // 返回指向驻留字符串的指针（在 interner 生命周期内有效）
    const char* intern(const char* s) {
        auto [it, _] = strings.emplace(s);
        return it->c_str();
    }

    size_t count() const {
        return strings.size();
    }
};

#endif
```

C 头文件：interner.h

```c
// interner.h（用于 FFI 的 C API）
#ifndef INTERNER_H
#define INTERNER_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct StringInterner StringInterner;

StringInterner* interner_new(void);
void interner_free(StringInterner* interner);
const char* interner_intern(StringInterner* interner, const char* s);
size_t interner_count(const StringInterner* interner);

#ifdef __cplusplus
}
#endif
```

C++ 实现（interner.cpp）

```cpp
#include "interner.hpp"
#include "interner.h"

extern "C" {

StringInterner* interner_new(void) {
    return new StringInterner();
}

void interner_free(StringInterner* interner) {
    delete interner;
}

const char* interner_intern(StringInterner* interner, const char* s) {
    return interner->intern(s);
}

size_t interner_count(const StringInterner* interner) {
    return interner->count();
}

}
```

> 这是一个更大的示例。为字符串驻留器（string interner）编写包装器。你需要引导学员如何创建不透明指针——可直接讲解下方代码，或请学员自行查阅资料。
>
> _建议解法_
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> use std::ffi::{CStr, CString};
> use std::marker::PhantomData;
> use std::os::raw::c_char;
>
> #[repr(C)]
> pub struct StringInternerRaw {
>     _opaque: [u8; 0],
>     _pin: PhantomData<(*mut u8, std::marker::PhantomPinned)>,
> }
>
> unsafe extern "C" {
>     fn interner_new() -> *mut StringInternerRaw;
>
>     fn interner_free(interner: *mut StringInternerRaw);
>
>     fn interner_intern(
>         interner: *mut StringInternerRaw,
>         s: *const c_char,
>     ) -> *const c_char;
>
>     fn interner_count(interner: *const StringInternerRaw) -> usize;
> }
> ```
>
> 原始包装器写好后，请学员创建安全包装器。

