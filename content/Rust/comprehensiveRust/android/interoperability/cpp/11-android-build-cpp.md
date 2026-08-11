+++
title = "7.2.11 为 Android 构建：C++"
date = 2026-08-11T11:30:00+08:00
weight = 252
type = "docs"
description = "11-为 Android 构建：C++ — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/cpp/android-build-cpp.html](https://google.github.io/comprehensive-rust/android/interoperability/cpp/android-build-cpp.html)

# 7.2.11 为 Android 构建：C++

创建一个 `cc_library_static` 来构建 C++ 库，包括 CXX 生成的头文件与源文件。

```javascript
cc_library_static {
    name: "libcxx_test_cpp",
    srcs: ["cxx_test.cpp"],
    generated_headers: [
        "cxx-bridge-header",
        "libcxx_test_bridge_header"
    ],
    generated_sources: ["libcxx_test_bridge_code"],
}
```

> - 指出 `libcxx_test_bridge_header` 与 `libcxx_test_bridge_code` 是 CXX 生成的 C++ 绑定的依赖。下一页会展示如何设置它们。
> - 注意你还需要依赖 `cxx-bridge-header` 库，以便引入通用的 CXX 定义。
> - 在 Android 中使用 CXX 的完整文档见 [Android 文档]。你可能想把该链接分享给学员，以便他们知道以后在哪里可以再次找到这些说明。
>
> [Android 文档]: https://source.android.com/docs/setup/build/rust/building-rust-modules/android-rust-patterns#rust-cpp-interop-using-cxx

