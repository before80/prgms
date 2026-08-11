+++
title = "3.1.1 语义混淆"
date = 2026-08-11T11:30:00+08:00
weight = 427
type = "docs"
description = "01-语义混淆 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/newtype-pattern/semantic-confusion.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/newtype-pattern/semantic-confusion.html)

# 3.1.1 语义混淆

当函数接受多个同类型参数时，调用处含义不清：

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
# struct LoginError;
fn login(username: &str, password: &str) -> Result<(), LoginError> {
    // [...]
    # Ok(())
}

fn main() {
    let password = "password";
    let username = "username";

    // 在代码库的另一处，我们误把参数对调了。
    // 最好情况是 bug，最坏情况是安全漏洞
    login(password, username);
}
```

Newtype 模式可以在编译期防止这类错误：

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
struct Username(String);
struct Password(String);
struct LoginError;

fn login(username: &Username, password: &Password) -> Result<(), LoginError> {
    // [...]
    # Ok(())
}

fn main() {
    let password = Password("password".into());
    let username = Username("username".into());
    login(password, username); // 🛠️❌
}
```

> - 运行两个示例：展示原示例能成功编译，以及修改后示例返回的编译错误。
>
> - 强调**语义**角度。应利用 newtype 模式为不同概念使用不同的类型，从而彻底排除这类错误。
>
> - 不过也要注意：确实存在函数需要接受多个同类型参数的合理场景。若正确性至关重要，可考虑用带命名字段的结构体作为输入：
>   ```rust
>   // Copyright 2025 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   pub struct LoginArguments<'a> {
>       pub username: &'a str,
>       pub password: &'a str,
>   }
>   # fn login(i: LoginArguments) {}
>   # let password = "password";
>   # let username = "username";
>
>   // 无需查看 `login` 函数定义就能发现问题。
>   login(LoginArguments {
>       username: password,
>       password: username,
>   })
>   ```
>   用户在调用处必须为每个字段赋值，从而更容易发现 bug。

