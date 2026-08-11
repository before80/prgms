+++
title = "3 构建规则"
date = 2026-08-11T11:30:00+08:00
weight = 211
type = "docs"
description = "构建规则 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/build-rules.html](https://google.github.io/comprehensive-rust/android/build-rules.html)

# 3 构建规则

Android 构建系统（Soong）通过多种模块支持 Rust：

| 模块类型          | 说明                                                                                               |
| ----------------- | -------------------------------------------------------------------------------------------------- |
| `rust_binary`     | 生成 Rust 二进制。                                                                                 |
| `rust_library`    | 生成 Rust 库，并同时提供 `rlib` 与 `dylib` 变体。                                                  |
| `rust_ffi`        | 生成可供 `cc` 模块使用的 Rust C 库，并同时提供静态与共享变体。                                     |
| `rust_proc_macro` | 生成 `proc-macro` Rust 库。类似于编译器插件。                                                      |
| `rust_test`       | 生成使用标准 Rust 测试框架的 Rust 测试二进制。                                                     |
| `rust_fuzz`       | 生成基于 `libfuzzer` 的 Rust fuzz 二进制。                                                         |
| `rust_protobuf`   | 生成源码并产出为特定 protobuf 提供接口的 Rust 库。                                                 |
| `rust_bindgen`    | 生成源码并产出包含 C 库 Rust 绑定的 Rust 库。                                                      |

接下来我们看 `rust_binary` 与 `rust_library`。

> 讲师还可提到：
>
> - Cargo 并未针对多语言仓库优化，还会从互联网下载包。
>
> - 出于合规与性能考虑，Android 必须将 crate 放在树内。它还必须与 C/C++/Java 代码互操作。Soong 填补了这一空白。
>
> - Soong 与 [Bazel](https://bazel.build/) 有许多相似之处；Bazel 是 Blaze（用于 google3）的开源变体。
>
> - 趣闻：《星际迷航》中的 Data 是 Soong 型 Android。

