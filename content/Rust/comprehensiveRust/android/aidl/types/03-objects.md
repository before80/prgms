+++
title = "4.2.3 发送对象"
date = 2026-08-11T11:30:00+08:00
weight = 227
type = "docs"
description = "03-发送对象 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/aidl/types/objects.html](https://google.github.io/comprehensive-rust/android/aidl/types/objects.html)

# 4.2.3 发送对象

AIDL 对象既可以作为具体的 AIDL 类型发送，也可以作为类型擦除后的 `IBinder` 接口发送：

_birthday_service/aidl/com/example/birthdayservice/IBirthdayInfoProvider.aidl_：

```java
package com.example.birthdayservice;

interface IBirthdayInfoProvider {
    String name();
    int years();
}
```

_birthday_service/aidl/com/example/birthdayservice/IBirthdayService.aidl_：

```java
import com.example.birthdayservice.IBirthdayInfoProvider;

interface IBirthdayService {
    /** 同样的事，但使用 binder 对象。 */
    String wishWithProvider(IBirthdayInfoProvider provider);

    /** 同样的事，但使用 `IBinder`。 */
    String wishWithErasedProvider(IBinder provider);
}
```

_birthday_service/src/client.rs_：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 实现 `IBirthdayInfoProvider` 接口的 Rust 结构体。
struct InfoProvider {
    name: String,
    age: u8,
}

impl binder::Interface for InfoProvider {}

impl IBirthdayInfoProvider for InfoProvider {
    fn name(&self) -> binder::Result<String> {
        Ok(self.name.clone())
    }

    fn years(&self) -> binder::Result<i32> {
        Ok(self.age as i32)
    }
}

fn main() {
    binder::ProcessState::start_thread_pool();
    let service = connect().expect("Failed to connect to BirthdayService");

    // 为 `IBirthdayInfoProvider` 接口创建一个 binder 对象。
    let provider = BnBirthdayInfoProvider::new_binder(
        InfoProvider { name: name.clone(), age: years as u8 },
        BinderFeatures::default(),
    );

    // 将该 binder 对象发送给服务。
    service.wishWithProvider(&provider)?;

    // 执行相同操作，但将 provider 作为 `SpIBinder` 传入。
    service.wishWithErasedProvider(&provider.as_binder())?;
}
```

> - 注意 `BnBirthdayInfoProvider` 的用法。它与我们之前见过的 `BnBirthdayService` 作用相同。

