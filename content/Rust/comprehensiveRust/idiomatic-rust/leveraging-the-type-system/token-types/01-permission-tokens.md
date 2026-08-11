+++
title = "3.6.1 权限令牌"
date = 2026-08-11T11:30:00+08:00
weight = 462
type = "docs"
description = "01-权限令牌 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/token-types/permission-tokens.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/token-types/permission-tokens.html)

# 3.6.1 权限令牌

令牌类型很适合作为已检查权限的证明。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
mod admin {
    pub struct AdminToken(());

    pub fn get_admin(password: &str) -> Option<AdminToken> {
        if password == "Password123" { Some(AdminToken(())) } else { None }
    }
}

// 我们不必检查是否有权限，因为
// AdminToken 参数等价于这样一次检查。
pub fn add_moderator(_: &admin::AdminToken, user: &str) {}

fn main() {
    if let Some(token) = admin::get_admin("Password123") {
        add_moderator(&token, "CoolUser");
    } else {
        eprintln!("Incorrect password! Could not prove privileges.")
    }
}
```

> - 本例展示用密码获取聊天客户端管理员权限，并在获得权限后授予用户版主等级的建模。`AdminToken` 类型充当「正确用户权限的证明」。
>
>   用户在代码中请求密码；若密码正确，我们得到一个 `AdminToken`，可在特定环境（此处是聊天客户端）中执行管理员操作。
>
>   一旦获得权限，我们就可以调用 `add_moderator` 函数。
>
>   没有令牌类型就无法调用该函数，因此只要能调用它，我们就可以假定拥有权限。
>
> - 演示：再次尝试在 `main` 中构造 `AdminToken`，重申有用令牌的基础是防止其被任意构造。

