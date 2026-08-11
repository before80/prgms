+++
title = "3.5 借用检查不变量"
date = 2026-08-11T11:30:00+08:00
weight = 453
type = "docs"
description = "借用检查不变量 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/borrow-checker-invariants.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/borrow-checker-invariants.html)

# 3.5 借用检查不变量

借用检查器（borrow checker）虽为强制内存所有权而引入，也可建模其他问题并防止 API 误用。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 门可以打开或关闭，上锁或解锁需要正确的钥匙。
/// 用共享钥匙与拥有的门来建模。
pub struct DoorKey {
    pub key_shape: u32,
}
pub struct LockedDoor {
    lock_shape: u32,
}
pub struct OpenDoor {
    lock_shape: u32,
}

fn open_door(key: &DoorKey, door: LockedDoor) -> Result<OpenDoor, LockedDoor> {
    if door.lock_shape == key.key_shape {
        Ok(OpenDoor { lock_shape: door.lock_shape })
    } else {
        Err(door)
    }
}

fn close_door(key: &DoorKey, door: OpenDoor) -> Result<LockedDoor, OpenDoor> {
    if door.lock_shape == key.key_shape {
        Ok(LockedDoor { lock_shape: door.lock_shape })
    } else {
        Err(door)
    }
}

fn main() {
    let key = DoorKey { key_shape: 7 };
    let closed_door = LockedDoor { lock_shape: 7 };
    let opened_door = open_door(&key, closed_door);
    if let Ok(opened_door) = opened_door {
        println!("Opened the door with key shape '{}'", key.key_shape);
    } else {
        eprintln!(
            "Door wasn't opened! Your key only opens locks with shape '{}'",
            key.key_shape
        );
    }
}
```

> - 我们已经看到借用检查器防止内存安全 bug（use-after-free、数据竞争）。
>
> - 我们也已用类型塑造并限制 API，例如使用
>   [Typestate 模式](../typestate-pattern.md)。
>
> - 语言特性通常为特定目的引入。
>
>   随着时间推移，用户可能以引入时未预见的方式使用某特性。
>
>   Java 5 于 2004 年引入泛型，
>   [主要声明目的是实现类型安全的集合](https://jcp.org/en/jsr/detail?id=14)。
>
>   起初采用缓慢，但一些新项目从一开始就围绕泛型设计 API。
>
>   此后，语言的用户与开发者将泛型的使用扩展到类型安全 API 设计的其他领域：
>   - 可通过 Java 的 `Class<T>` 或 Guava 的 `TypeToken<T>` 持有类信息。
>   - Builder 模式可用递归泛型实现。
>
>   我们在此目标类似：尽管借用检查器是为防止 use-after-free 与数据竞争而引入，我们将其视为又一种 API 设计工具。
>
>   它可用于建模与防止内存安全 bug 无关的程序属性。
>
> - 要将借用检查器用作问题解决工具，我们需要「忘记」其原始目的是在防止 use-after-free 与数据竞争的上下文中防止可变别名。
>
>   我们应想象自己处于规则相同但含义略有不同的情境中。
>
> - 本例用所有权与借用建模物理门的状态。
>
>   `open_door` **消费**一个 `LockedDoor` 并返回新的 `OpenDoor`。旧的 `LockedDoor` 值不再可用。
>
>   若使用错误的钥匙，门保持锁定。它作为 `Result` 的 `Err` 分支返回。
>
>   尝试使用已被打开的门是编译期错误。
>
> - 类似地，`close_door` 消费一个 `OpenDoor`，从而在编译期防止关闭两次。
>
> - 借用检查器的规则存在是为了防止内存安全 bug，但底层逻辑系统并不「知道」什么是内存。
>
>   借用检查器所做的只是强制执行用户如何排序操作的一组特定规则。
>
>   这只是搭借用检查器规则之便，设计更难或不可能误用的 API 的又一案例。

