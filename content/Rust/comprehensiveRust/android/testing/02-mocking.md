+++
title = "5.2 Mocking"
date = 2026-08-11T11:30:00+08:00
weight = 232
type = "docs"
description = "02-Mocking — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/testing/mocking.html](https://google.github.io/comprehensive-rust/android/testing/mocking.html)

# 5.2 Mocking

做 mocking 时，[Mockall] 是广泛使用的库。你需要把代码重构为使用 trait，然后就能快速 mock：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::time::Duration;

#[mockall::automock]
pub trait Pet {
    fn is_hungry(&self, since_last_meal: Duration) -> bool;
}

#[test]
fn test_robot_dog() {
    let mut mock_dog = MockPet::new();
    mock_dog.expect_is_hungry().return_const(true);
    assert!(mock_dog.is_hungry(Duration::from_secs(10)));
}
```

[Mockall]: https://docs.rs/mockall/

> - Mockall 是 Android (AOSP) 中推荐的 mocking 库。[crates.io 上还有其他 mocking 库](https://crates.io/keywords/mock)，尤其是在 mock HTTP 服务方面。其他 mocking 库的工作方式与 Mockall 类似，即都能方便地为给定 trait 得到一个 mock 实现。
>
> - 注意 mocking 有些_有争议_：mock 让你能把测试与依赖完全隔离。直接结果是测试执行更快、更稳定。另一方面，mock 可能配置错误，并返回与真实依赖不同的输出。
>
>   只要可能，建议使用真实依赖。例如，许多数据库允许配置内存后端。这意味着你在测试中能得到正确行为，而且速度快，结束后还会自动清理。
>
>   类似地，许多 Web 框架允许启动绑定到 `localhost` 随机端口的进程内服务器。总是优先这样做，而不是把框架 mock 掉，因为它帮你在真实环境中测试代码。
>
> - Mockall 不在 Rust Playground 中，因此需要在本地环境运行本示例。使用 `cargo add mockall` 可快速把 Mockall 加到现有 Cargo 项目。
>
> - Mockall 功能很丰富。特别是，你可以设置依赖传入参数的期望。这里我们用它来 mock 一只在上次喂食 3 小时后会饿的猫：
>
> ```rust
> // Copyright 2024 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> #[test]
> fn test_robot_cat() {
>     let mut mock_cat = MockPet::new();
>     mock_cat
>         .expect_is_hungry()
>         .with(mockall::predicate::gt(Duration::from_secs(3 * 3600)))
>         .return_const(true);
>     mock_cat.expect_is_hungry().return_const(false);
>     assert!(mock_cat.is_hungry(Duration::from_secs(5 * 3600)));
>     assert!(!mock_cat.is_hungry(Duration::from_secs(5)));
> }
> ```
>
> - 你可以用 `.times(n)` 把 mock 方法可被调用的次数限制为 `n`——若不满足，mock 在 drop 时会自动 panic。

