+++
title = "3.2 库"
date = 2026-08-11T11:30:00+08:00
weight = 213
type = "docs"
description = "02-库 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/build-rules/library.html](https://google.github.io/comprehensive-rust/android/build-rules/library.html)

# 3.2 库

使用 `rust_library` 可为 Android 创建新的 Rust 库。

这里我们声明对两个库的依赖：

- `libgreeting`，在下方定义，
- `libtextwrap`，已是
  [`external/rust/android-crates-io/crates/`][crates] 中 vendored 的 crate。

[crates]: https://cs.android.com/android/platform/superproject/main/+/main:external/rust/android-crates-io/crates/

_hello_rust/Android.bp_：

```javascript
rust_binary {
    name: "hello_rust_with_dep",
    crate_name: "hello_rust_with_dep",
    srcs: ["src/main.rs"],
    rustlibs: [
        "libgreetings",
        "libtextwrap",
    ],
    prefer_rlib: true, // Need this to avoid dynamic link error.
}

rust_library {
    name: "libgreetings",
    crate_name: "greetings",
    srcs: ["src/lib.rs"],
}
```

_hello_rust/src/main.rs_：

```rust,ignore
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
//! Rust demo.

use greetings::greeting;
use textwrap::fill;

/// Prints a greeting to standard output.
fn main() {
    println!("{}", fill(&greeting("Bob"), 24));
}
```

_hello_rust/src/lib.rs_：

```rust,ignore
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
//! Greeting library.

/// Greet `name`.
pub fn greeting(name: &str) -> String {
    format!("Hello {name}, it is very nice to meet you!")
}
```

像之前一样构建、推送并运行该二进制：

```shell
m hello_rust_with_dep
adb push "$ANDROID_PRODUCT_OUT/system/bin/hello_rust_with_dep" /data/local/tmp
adb shell /data/local/tmp/hello_rust_with_dep
```

```text
Hello Bob, it is very
nice to meet you!
```

> - 走一遍构建步骤，并在模拟器中演示运行。
>
> - 名为 `greetings` 的 Rust crate 必须由名为 `libgreetings` 的规则构建。注意 Rust 代码使用的是 crate 名，这与平常的 Rust 用法一致。
>
> - 同样，构建规则要求我们为所有公开项添加文档注释。

