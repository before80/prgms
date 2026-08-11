+++
title = "2.3 状态机"
date = 2026-08-11T11:30:00+08:00
weight = 370
type = "docs"
description = "03-状态机 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/async/state-machine.html](https://google.github.io/comprehensive-rust/concurrency/async/state-machine.html)

# 2.3 状态机

Rust 会把 async 函数或块转换成实现 `Future` 的隐藏类型，用状态机跟踪函数进度。该转换的细节很复杂，但对其有个示意性理解是有益的。下面的函数

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 两次 D10 掷骰加上修正值求和。
async fn two_d10(modifier: u32) -> u32 {
    let first_roll = roll_d10().await;
    let second_roll = roll_d10().await;
    first_roll + second_roll + modifier
}
```

会被转换成类似这样的东西

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

/// 两次 D10 掷骰加上修正值求和。
fn two_d10(modifier: u32) -> TwoD10 {
    TwoD10::Init { modifier }
}

enum TwoD10 {
    // 函数尚未开始。
    Init { modifier: u32 },
    // 等待第一次 `.await` 完成。
    FirstRoll { modifier: u32, fut: RollD10Future },
    // 等待第二次 `.await` 完成。
    SecondRoll { modifier: u32, first_roll: u32, fut: RollD10Future },
}

impl Future for TwoD10 {
    type Output = u32;
    fn poll(mut self: Pin<&mut Self>, ctx: &mut Context) -> Poll<Self::Output> {
        loop {
            match *self {
                TwoD10::Init { modifier } => {
                    // 为第一次掷骰创建 future。
                    let fut = roll_d10();
                    *self = TwoD10::FirstRoll { modifier, fut };
                }
                TwoD10::FirstRoll { modifier, ref mut fut } => {
                    // 轮询第一次掷骰的子 future。
                    if let Poll::Ready(first_roll) = fut.poll(ctx) {
                        // 为第二次掷骰创建 future。
                        let fut = roll_d10();
                        *self = TwoD10::SecondRoll { modifier, first_roll, fut };
                    } else {
                        return Poll::Pending;
                    }
                }
                TwoD10::SecondRoll { modifier, first_roll, ref mut fut } => {
                    // 轮询第二次掷骰的子 future。
                    if let Poll::Ready(second_roll) = fut.poll(ctx) {
                        return Poll::Ready(first_roll + second_roll + modifier);
                    } else {
                        return Poll::Pending;
                    }
                }
            }
        }
    }
}
```

> 此示例仅作说明，并非 Rust 编译器转换的精确表示。这里需要注意的重要事项是：
>
> - 调用 async 函数除了构造并返回 future 之外什么也不做。
> - 所有局部变量都存储在函数的 future 中，用枚举标识执行当前挂起的位置。
> - async 函数中的 `.await` 被翻译成包含所有存活变量与被等待 future 的新状态。然后 `loop` 处理该更新后的状态，轮询 future 直到返回 `Poll::Ready`。
> - 执行会急切地继续，直到出现 `Poll::Pending`。在这个简单例子中，每个 future 都立即就绪。
> - `main` 包含一个朴素的 executor，只是忙等到 future 就绪。我们很快会讨论真正的 executor。
>
> # 扩展阅读
>
> 想象一下深度嵌套的 async 函数栈对应的 `Future` 数据结构。每个函数的 `Future` 包含它所调用的函数的 `Future` 结构。这可能导致编译器生成的 `Future` 类型出乎意料地大。
>
> 这也意味着递归 async 函数很有挑战性。对比构建递归类型的常见错误，例如
>
> ```rust
> // Copyright 2025 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> enum LinkedList<T> {
>     Node { value: T, next: LinkedList<T> },
>     Nil,
> }
> ```
>
> 递归类型的修复是加一层间接，例如用 `Box`。类似地，递归 async 函数必须装箱递归 future：
>
> ```rust
> // Copyright 2025 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> async fn count_to(n: u32) {
>     if n > 0 {
>         Box::pin(count_to(n - 1)).await;
>         println!("{n}");
>     }
> }
> ```

