+++
title = "4.1.3 服务实现"
date = 2026-08-11T11:30:00+08:00
weight = 218
type = "docs"
description = "03-服务实现 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/aidl/example-service/service.html](https://google.github.io/comprehensive-rust/android/aidl/example-service/service.html)

# 4.1.3 服务实现

现在可以实现 AIDL 服务了：

_birthday_service/src/lib.rs_：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
//! `IBirthdayService` AIDL 接口的实现。
use com_example_birthdayservice::aidl::com::example::birthdayservice::IBirthdayService::IBirthdayService;
use com_example_birthdayservice::binder;

/// `IBirthdayService` 的实现。
pub struct BirthdayService;

impl binder::Interface for BirthdayService {}

impl IBirthdayService for BirthdayService {
    fn wishHappyBirthday(&self, name: &str, years: i32) -> binder::Result<String> {
        Ok(format!("Happy Birthday {name}, congratulations with the {years} years!"))
    }
}
```

_birthday_service/Android.bp_：

```javascript
rust_library {
    name: "libbirthdayservice",
    crate_name: "birthdayservice",
    srcs: ["src/lib.rs"],
    rustlibs: [
        "com.example.birthdayservice-rust",
    ],
}
```

> - 指出生成的 `IBirthdayService` trait 的路径，并解释每一段为何必要。
> - 注意 `wishHappyBirthday` 以及其他 AIDL IPC 方法接受 `&self`（而不是 `&mut self`）。
>   - 这是必要的，因为 Binder 在线程池上响应传入请求，允许多个请求并行处理。这要求服务方法只能获得对 `self` 的共享引用。
>   - 服务需要修改的任何状态都必须放进类似 `Mutex` 的东西里，以便安全地变更。
>   - 管理服务状态的正确方法高度依赖于你的服务细节。
> - TODO：`binder::Interface` trait 做什么？有没有可覆盖的方法？源码在哪里？

