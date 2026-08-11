+++
title = "7.2.10 为 Android 构建：Genrules"
date = 2026-08-11T11:30:00+08:00
weight = 251
type = "docs"
description = "10-为 Android 构建：Genrules — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/cpp/android-cpp-genrules.html](https://google.github.io/comprehensive-rust/android/interoperability/cpp/android-cpp-genrules.html)

# 7.2.10 为 Android 构建：Genrules

创建两个 genrule：一个生成 CXX 头文件，一个生成 CXX 源文件。它们随后用作 `cc_library_static` 的输入。

```javascript
// 生成包含 C++ 绑定的 C++ 头文件，
// 对应 lib.rs 中导出的 Rust 函数。
genrule {
    name: "libcxx_test_bridge_header",
    tools: ["cxxbridge"],
    cmd: "$(location cxxbridge) $(in) --header > $(out)",
    srcs: ["lib.rs"],
    out: ["lib.rs.h"],
}

// 生成 Rust 将调用的 C++ 代码。
genrule {
    name: "libcxx_test_bridge_code",
    tools: ["cxxbridge"],
    cmd: "$(location cxxbridge) $(in) > $(out)",
    srcs: ["lib.rs"],
    out: ["lib.rs.cc"],
}
```

> - `cxxbridge` 工具是生成桥接模块 C++ 一侧的独立工具。它已包含在 Android 中，并可作为 Soong 工具使用。
> - 按约定，若你的 Rust 源文件是 `lib.rs`，头文件将命名为 `lib.rs.h`，源文件将命名为 `lib.rs.cc`。不过这一命名约定并未强制执行。

