+++
title = "7.1.2 Bindgen"
date = 2026-08-11T11:30:00+08:00
weight = 237
type = "docs"
description = "02-Bindgen — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/with-c/bindgen.html](https://google.github.io/comprehensive-rust/android/interoperability/with-c/bindgen.html)

# 7.1.2 Bindgen

[bindgen](https://rust-lang.github.io/rust-bindgen/introduction.html) 工具可以从 C 头文件自动生成绑定。

为该库创建一个包装头文件（本例中并非严格必需）：

_interoperability/bindgen/libbirthday_wrapper.h_：

```c
#include "libbirthday.h"
```

_interoperability/bindgen/Android.bp_：

```javascript
rust_bindgen {
    name: "libbirthday_bindgen",
    crate_name: "birthday_bindgen",
    wrapper_src: "libbirthday_wrapper.h",
    source_stem: "bindings",
    static_libs: ["libbirthday"],
}
rust_test {
    name: "libbirthday_bindgen_test",
    srcs: [":libbirthday_bindgen"],
    crate_name: "libbirthday_bindgen_test",
    test_suites: ["general-tests"],
    auto_gen_config: true,
    clippy_lints: "none", // 生成的文件，跳过 lint
    lints: "none",
}
```

最后，可以在 Rust 程序中使用这些绑定：

_interoperability/bindgen/Android.bp_：

```javascript
rust_binary {
    name: "print_birthday_card",
    srcs: ["main.rs"],
    rustlibs: ["libbirthday_bindgen"],
    static_libs: ["libbirthday"],
}
```

_interoperability/bindgen/main.rs_：

```rust
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
//! Bindgen 演示。

use birthday_bindgen::{card, print_card};

fn main() {
    let name = std::ffi::CString::new("Peter").unwrap();
    let card = card { name: name.as_ptr(), years: 42 };
    // SAFETY: 我们传入的指针有效，因为它来自 Rust 引用；
    // 其中包含的 `name` 指向上方的 `name`，该值在此期间也保持有效。
    // `print_card` 不会存储任一指针以便在返回后稍后使用。
    unsafe {
        print_card(&card);
    }
}
```

> - Android 构建规则会在幕后自动为你调用 `bindgen`。
>
> - 注意 `main` 中的 Rust 代码仍然难写。良好实践是把 `bindgen` 的输出封装在一个 Rust 库中，向调用方暴露安全接口。

