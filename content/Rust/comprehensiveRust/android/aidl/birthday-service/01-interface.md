+++
title = "4.1.1 接口"
date = 2026-08-11T11:30:00+08:00
weight = 216
type = "docs"
description = "01-接口 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/aidl/example-service/interface.html](https://google.github.io/comprehensive-rust/android/aidl/example-service/interface.html)

# 4.1.1 接口

使用 AIDL 接口声明服务的 API：

_birthday_service/aidl/com/example/birthdayservice/IBirthdayService.aidl_：

```java
package com.example.birthdayservice;

/** 生日服务接口。 */
interface IBirthdayService {
    /** 生成生日快乐消息。 */
    String wishHappyBirthday(String name, int years);
}
```

_birthday_service/aidl/Android.bp_：

```javascript
aidl_interface {
    name: "com.example.birthdayservice",
    srcs: ["com/example/birthdayservice/*.aidl"],
    unstable: true,
    backend: {
        rust: { // Rust 默认未启用
            enabled: true,
        },
    },
}
```

> - 注意 `aidl/` 目录下的目录结构需要与 AIDL 文件中使用的包名匹配，即包名为
>   `com.example.birthdayservice`，文件位于
>   `aidl/com/example/IBirthdayService.aidl`。

