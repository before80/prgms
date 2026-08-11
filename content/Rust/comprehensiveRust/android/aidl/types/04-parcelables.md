+++
title = "4.2.4 Parcelable"
date = 2026-08-11T11:30:00+08:00
weight = 228
type = "docs"
description = "04-Parcelable — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/aidl/types/parcelables.html](https://google.github.io/comprehensive-rust/android/aidl/types/parcelables.html)

# 4.2.4 Parcelable

Rust 的 Binder 支持直接发送 parcelable：

_birthday_service/aidl/com/example/birthdayservice/BirthdayInfo.aidl_：

```java
package com.example.birthdayservice;

parcelable BirthdayInfo {
    String name;
    int years;
}
```

_birthday_service/aidl/com/example/birthdayservice/IBirthdayService.aidl_：

```java
import com.example.birthdayservice.BirthdayInfo;

interface IBirthdayService {
    /** 同样的事，但使用 parcelable。 */
    String wishWithInfo(in BirthdayInfo info);
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
fn main() {
    binder::ProcessState::start_thread_pool();
    let service = connect().expect("Failed to connect to BirthdayService");

    let info = BirthdayInfo { name: "Alice".into(), years: 123 };
    service.wishWithInfo(&info)?;
}
```
