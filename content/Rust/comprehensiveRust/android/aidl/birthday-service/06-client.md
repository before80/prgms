+++
title = "4.1.6 客户端"
date = 2026-08-11T11:30:00+08:00
weight = 221
type = "docs"
description = "06-客户端 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/aidl/example-service/client.html](https://google.github.io/comprehensive-rust/android/aidl/example-service/client.html)

# 4.1.6 客户端

最后，可以为新服务创建一个 Rust 客户端。

_birthday_service/src/client.rs_：

```rust,ignore
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use com_example_birthdayservice::aidl::com::example::birthdayservice::IBirthdayService::IBirthdayService;
use com_example_birthdayservice::binder;

const SERVICE_IDENTIFIER: &str = "birthdayservice";

/// Call the birthday service.
fn main() -> Result<(), Box<dyn Error>> {
    let name = std::env::args().nth(1).unwrap_or_else(|| String::from("Bob"));
    let years = std::env::args()
        .nth(2)
        .and_then(|arg| arg.parse::<i32>().ok())
        .unwrap_or(42);

    binder::ProcessState::start_thread_pool();
    let service = binder::get_interface::<dyn IBirthdayService>(SERVICE_IDENTIFIER)
        .map_err(|_| "Failed to connect to BirthdayService")?;

    // Call the service.
    let msg = service.wishHappyBirthday(&name, years)?;
    println!("{msg}");
}
```

_birthday_service/Android.bp_：

```javascript
rust_binary {
    name: "birthday_client",
    crate_name: "birthday_client",
    srcs: ["src/client.rs"],
    rustlibs: [
        "com.example.birthdayservice-rust",
    ],
    prefer_rlib: true, // To avoid dynamic link error.
}
```

注意客户端并不依赖 `libbirthdayservice`。

在设备上构建、推送并运行客户端：

```shell
m birthday_client
adb push "$ANDROID_PRODUCT_OUT/system/bin/birthday_client" /data/local/tmp
adb shell /data/local/tmp/birthday_client Charlie 60
```

```text
Happy Birthday Charlie, congratulations with the 60 years!
```

> - `Strong<dyn IBirthdayService>` 是表示客户端已连接服务的 trait 对象。
>   - `Strong` 是 Binder 的自定义智能指针类型。它既处理服务 trait 对象的进程内引用计数，也处理跟踪有多少进程持有该对象引用的全局 Binder 引用计数。
>   - 注意客户端用来与服务通信的 trait 对象，使用的正是服务端实现的同一个 trait。对于给定的 Binder 接口，只生成一个 Rust trait，客户端与服务端共用。
> - 使用注册服务时相同的服务标识符。理想情况下应定义在客户端与服务端都能依赖的公共 crate 中。

