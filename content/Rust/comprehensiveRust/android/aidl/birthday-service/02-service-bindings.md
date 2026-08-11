+++
title = "4.1.2 服务 API"
date = 2026-08-11T11:30:00+08:00
weight = 217
type = "docs"
description = "02-服务 API — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/aidl/example-service/service-bindings.html](https://google.github.io/comprehensive-rust/android/aidl/example-service/service-bindings.html)

# 4.1.2 服务 API

Binder 会为每个接口定义生成一个 trait。

_birthday_service/aidl/com/example/birthdayservice/IBirthdayService.aidl_：

```java
/** 生日服务接口。 */
interface IBirthdayService {
    /** 生成生日快乐消息。 */
    String wishHappyBirthday(String name, int years);
}
```

_out/soong/.intermediates/.../com_example_birthdayservice.rs_：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
trait IBirthdayService {
    fn wishHappyBirthday(&self, name: &str, years: i32) -> binder::Result<String>;
}
```

你的服务需要实现该 trait，客户端则通过该 trait 与服务通信。

> - 指出生成的函数签名（尤其是参数与返回类型）如何对应接口定义。
>   - 作为参数的 `String` 与作为返回类型的 `String` 会映射成不同的 Rust 类型。

