+++
title = "4.1.4 服务端"
date = 2026-08-11T11:30:00+08:00
weight = 219
type = "docs"
description = "04-服务端 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/aidl/example-service/server.html](https://google.github.io/comprehensive-rust/android/aidl/example-service/server.html)

# 4.1.4 服务端

最后，我们可以创建一个暴露该服务的服务端：

_birthday_service/src/server.rs_：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
//! 生日服务。
use birthdayservice::BirthdayService;
use com_example_birthdayservice::aidl::com::example::birthdayservice::IBirthdayService::BnBirthdayService;
use com_example_birthdayservice::binder;

const SERVICE_IDENTIFIER: &str = "birthdayservice";

/// 生日服务的入口点。
fn main() {
    let birthday_service = BirthdayService;
    let birthday_service_binder = BnBirthdayService::new_binder(
        birthday_service,
        binder::BinderFeatures::default(),
    );
    binder::add_service(SERVICE_IDENTIFIER, birthday_service_binder.as_binder())
        .expect("Failed to register service");
    binder::ProcessState::join_thread_pool();
}
```

_birthday_service/Android.bp_：

```javascript
rust_binary {
    name: "birthday_server",
    crate_name: "birthday_server",
    srcs: ["src/server.rs"],
    rustlibs: [
        "com.example.birthdayservice-rust",
        "libbirthdayservice",
    ],
    prefer_rlib: true, // 以避免动态链接错误。
}
```

> 把用户定义的服务实现（本例中是实现了 `IBirthdayService` 的 `BirthdayService` 类型）启动为 Binder 服务，需要多个步骤。如果学员曾用 C++ 或其他语言使用过 Binder，这可能看起来比他们习惯的更复杂。向学员解释每一步为何必要。
>
> 1. 创建服务类型的实例（`BirthdayService`）。
> 2. 将服务对象包装进对应的 `Bn*` 类型（本例为 `BnBirthdayService`）。该类型由 Binder 生成，并提供通用的 Binder 功能，类似于 C++ 中的 `BnBinder` 基类。由于 Rust 没有继承，我们使用组合，把 `BirthdayService` 放进生成的 `BnBinderService` 中。
> 3. 调用 `add_service`，传入服务标识符与你的服务对象（示例中的 `BnBirthdayService` 对象）。
> 4. 调用 `join_thread_pool`，把当前线程加入 Binder 的线程池并开始监听连接。

