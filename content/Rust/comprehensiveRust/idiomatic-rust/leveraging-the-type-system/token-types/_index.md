+++
title = "3.6 令牌类型"
date = 2026-08-11T11:30:00+08:00
weight = 461
type = "docs"
description = "令牌类型 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/token-types.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/token-types.html)

# 3.6 令牌类型

带私有构造函数的类型可用作不变量的证明。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub mod token {
    // 一个公共类型，其私有字段位于模块边界之后。
    pub struct Token { proof: () }

    pub fn get_token() -> Option<Token> {
        Some(Token { proof: () })
    }
}

pub fn protected_work(token: token::Token) {
    println!("We have a token, so we can make assumptions.")
}

fn main() {
    if let Some(token) = token::get_token() {
        // 我们有令牌，所以可以做这项工作。
        protected_work(token);
    } else {
        // 无法取得令牌，所以不能调用 `protected_work`。
    }
}
```
> - 动机：我们希望限制用户对功能的访问，直到他们完成特定任务。
>
>   我们可以通过结构体与模块的隐私规则，定义 API 消费者无法自行构造的类型来做到这一点。
>
>   [Newtype](../newtype-pattern.md)
>   以类似方式使用隐私规则，限制构造，除非值在运行时保证满足不变量。
>
> - 提问：这里的 `proof: ()` 字段目的是什么？
>
>   若没有 `proof: ()`，`Token` 将没有私有字段，用户就能任意构造 `Token` 值。
>
>   演示：尝试在 `main` 中手动构造令牌并展示编译错误。演示：从 `Token` 中去掉 `proof` 字段，展示若没有私有字段用户将如何构造 `Token`。
>
> - 通过把 `Token` 类型放在模块边界（`token`）之后，该模块外的用户无法自行构造该值，因为他们无权访问 `proof` 字段。
>
>   API 开发者可以定义产生这些令牌的方法与函数。用户则不能。
>
>   令牌成为已满足 API 开发者对这些令牌的访问条件的证明。
>
> - 提问：API 开发者可能如何意外引入绕过方式？
>
>   期望答案如「序列化实现」、其他解析/「从字符串」实现，或 `Default` 的实现。

