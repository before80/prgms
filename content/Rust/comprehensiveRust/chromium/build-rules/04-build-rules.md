+++
title = "5.4 练习"
date = 2026-08-11T11:30:00+08:00
weight = 264
type = "docs"
description = "04-练习 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/exercises/chromium/build-rules.html](https://google.github.io/comprehensive-rust/exercises/chromium/build-rules.html)

# 5.4 练习

在你的 Chromium 构建中，向 `//ui/base/BUILD.gn` 添加一个新的 Rust 目标，内容为：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
// SAFETY: 不存在其他同名的全局函数。
#[unsafe(no_mangle)]
pub extern "C" fn hello_from_rust() {
    println!("Hello from Rust!")
}
```

**重要：** 注意这里的 `no_mangle` 被 Rust 编译器视为一种 unsafety，因此你需要在 `gn` 目标中允许 unsafe 代码。

把这个新的 Rust 目标作为 `//ui/base:base` 的依赖。在 `ui/base/resource/resource_bundle.cc` 顶部声明该函数（稍后我们会看到绑定生成工具如何自动化这一点）：

```cpp
extern "C" void hello_from_rust();
```

在 `ui/base/resource/resource_bundle.cc` 的某处调用该函数——我们建议放在 `ResourceBundle::MaybeMangleLocalizedString` 顶部。构建并运行 Chromium，确保多次打印出 “Hello from Rust!”。

若你使用 VSCode，现在把 Rust 配置好以便在 VSCode 中良好工作。后续练习会用到。若已成功，你应能在 `println!` 上右键使用“转到定义”。

## 在哪里找帮助

- [`rust_static_library` gn 模板][0]可用的选项
- 关于 [`#[unsafe(no_mangle)]`][1] 的信息
- 关于 [`extern "C"`][2] 的信息
- 关于 gn 的 [`--export-rust-project`][3] 开关的信息
- [如何在 VSCode 中安装 rust-analyzer][4]

> 学员真正跑通这一点非常重要，因为后续练习会建立在此之上。
>
> 本示例不寻常，因为它归结为最低公分母互操作语言 C。C++ 与 Rust 都能原生声明并调用 C ABI 函数。课程稍后，我们将把 C++ 直接连接到 Rust。
>
> 这里需要 `allow_unsafe = true`，因为 `#[unsafe(no_mangle)]` 可能允许 Rust 生成两个同名函数，而 Rust 不再能保证调用的是正确那一个。
>
> 若你需要纯 Rust 可执行文件，也可以使用 `rust_executable` gn 模板。


[0]: https://source.chromium.org/chromium/chromium/src/+/main:build/rust/rust_static_library.gni;l=16
[1]: https://doc.rust-lang.org/beta/reference/abi.html#the-no_mangle-attribute
[2]: https://doc.rust-lang.org/std/keyword.extern.html
[3]: https://gn.googlesource.com/gn/+/main/docs/reference.md#compilation-database
[4]: https://code.visualstudio.com/docs/languages/rust
