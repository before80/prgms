+++
title = "4.1.7 更改 API"
date = 2026-08-11T11:30:00+08:00
weight = 222
type = "docs"
description = "07-更改 API — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/aidl/example-service/changing-definition.html](https://google.github.io/comprehensive-rust/android/aidl/example-service/changing-definition.html)

# 4.1.7 更改 API

扩展一下 API：让客户端能为生日贺卡指定一系列行：

```java
package com.example.birthdayservice;

/** 生日服务接口。 */
interface IBirthdayService {
    /** 生成生日快乐消息。 */
    String wishHappyBirthday(String name, int years, in String[] text);
}
```

这会得到更新后的 `IBirthdayService` trait 定义：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
trait IBirthdayService {
    fn wishHappyBirthday(
        &self,
        name: &str,
        years: i32,
        text: &[String],
    ) -> binder::Result<String>;
}
```

> - 注意 AIDL 定义中的 `String[]` 在 Rust 中被翻译为 `&[String]`，即生成的绑定在可能的情况下会使用符合习惯的 Rust 类型：
>   - `in` 数组参数翻译为切片。
>   - `out` 与 `inout` 参数翻译为 `&mut Vec<T>`。
>   - 返回值翻译为返回 `Vec<T>`。

