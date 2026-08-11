+++
title = "3.5.2 一次性值"
date = 2026-08-11T11:30:00+08:00
weight = 455
type = "docs"
description = "02-一次性值 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/borrow-checker-invariants/single-use-values.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/borrow-checker-invariants/single-use-values.html)

# 3.5.2 一次性值

有时我们想要**只能使用一次**的值。密码学中的一个关键例子是「Nonce」。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub struct Key(/* specifics omitted */);

/// 适合密码学用途的一次性数字。
pub struct Nonce(u32);

/// 密码学上可靠的随机生成函数。
pub fn new_nonce() -> Nonce {
    Nonce(4) // chosen by a fair dice roll, https://xkcd.com/221/
}

/// 消费 nonce，但不消费 key 或 data。
pub fn encrypt(nonce: Nonce, key: &Key, data: &[u8]) {}

fn main() {
    let nonce = new_nonce();
    let data_1: [u8; 4] = [1, 2, 3, 4];
    let data_2: [u8; 4] = [4, 3, 2, 1];
    let key = Key(/* specifics omitted */);

    // key 和 data 可以复用、复制等，但 nonce 不行。
    encrypt(nonce, &key, &data_1);
    // encrypt(nonce, &key, &data_2); // 🛠️❌
}
```

> - 问题：我们如何保证一个值只被使用一次？
>
> - 动机：Nonce 是密码学协议中用于防止重放攻击的一段随机、唯一数据。
>
>   背景：实践中人们曾意外复用 nonce。最常见的情况是，这会导致密码学协议完全失效，不再履行其功能。
>
>   取决于 nonce 复用与手头密码学的具体细节，攻击者也可能计算出私钥。
>
> - Rust 有一个实现「一旦用过就不能再用」这一不变量的明显工具：将值作为**拥有的参数**传递。
>
> - 强调：`encrypt` 按值接受 `nonce`（拥有的参数），但按引用接受 `key` 和 `data`。
>
> - 一次性值的技巧如下：
>
>   - 保持构造函数私有，这样用户就不能用相同的内部值构造两次。
>
>   - 不实现 `Clone`/`Copy` trait 或等效方法，这样用户就不能复制我们想保持唯一的数据。
>
>   - 让内部类型不透明（如用 newtype 模式），这样用户就不能自行修改已有值。
>
> - 提问：幻灯片代码中的 newtype 模式还缺什么？
>
>   期望：模块边界。
>
>   演示：没有模块边界时，用户可以自行构造 nonce。
>
>   修复：将 `Key`、`Nonce` 和 `new_nonce` 放在模块后面。
>
> ## 深入探索
>
> - 密码学细节：若 nonce 通过没有真正随机性的伪随机过程创建，仍可能被使用两次。该方法无法防止这一点。此 API 设计防止一种 nonce 重复，但并非所有逻辑 bug。

