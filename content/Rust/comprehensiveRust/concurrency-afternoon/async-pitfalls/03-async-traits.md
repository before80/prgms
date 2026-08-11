+++
title = "4.3 异步 Trait"
date = 2026-08-11T11:30:00+08:00
weight = 381
type = "docs"
description = "03-异步 Trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/async-pitfalls/async-traits.html](https://google.github.io/comprehensive-rust/concurrency/async-pitfalls/async-traits.html)

# 4.3 异步 Trait

Trait 中的异步方法在 1.75 版本中稳定。这需要支持在 trait 中使用返回位置的 `impl Trait`，因为 `async fn` 的脱糖包含 `-> impl Future<Output = ...>`。

不过，即便有原生支持，围绕 `async fn` 仍有特定陷阱：

- 返回位置的 `impl Trait` 会捕获所有作用域内的生命周期（因此某些借用模式无法表达）。

- 异步 trait 不能与 [trait 对象][trait objects]（`dyn Trait` 支持）一起使用。

[async_trait] crate 通过宏为 `dyn` 支持提供变通方法，但有特定注意事项：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use async_trait::async_trait;
use std::time::Instant;
use tokio::time::{Duration, sleep};

#[async_trait]
trait Sleeper {
    async fn sleep(&self);
}

struct FixedSleeper {
    sleep_ms: u64,
}

#[async_trait]
impl Sleeper for FixedSleeper {
    async fn sleep(&self) {
        sleep(Duration::from_millis(self.sleep_ms)).await;
    }
}

async fn run_all_sleepers_multiple_times(
    sleepers: Vec<Box<dyn Sleeper>>,
    n_times: usize,
) {
    for _ in 0..n_times {
        println!("Running all sleepers...");
        for sleeper in &sleepers {
            let start = Instant::now();
            sleeper.sleep().await;
            println!("Slept for {} ms", start.elapsed().as_millis());
        }
    }
}

#[tokio::main]
async fn main() {
    let sleepers: Vec<Box<dyn Sleeper>> = vec![
        Box::new(FixedSleeper { sleep_ms: 50 }),
        Box::new(FixedSleeper { sleep_ms: 100 }),
    ];
    run_all_sleepers_multiple_times(sleepers, 5).await;
}
```

> - `async_trait` 易于使用，但注意它通过堆分配实现这一点。堆分配有性能开销。
>
> - 语言对 `async trait` 支持的挑战太深，本课无法深入描述。若有兴趣深挖，参见 Niko Matsakis 的[这篇博文][this blog post]。也可参见这些关键词：
>
>   - [RPIT]：是
>     [返回位置 `impl Trait`](../../generics/impl-trait.md) 的缩写。
>   - [RPITIT]：是 trait 中返回位置 `impl Trait`（trait 中的 RPIT）的缩写。
>
> - 试着创建一个休眠随机时长的新 sleeper 结构体，并把它加入 `Vec`。


[async_trait]: https://docs.rs/async-trait/
[trait objects]: ../../smart-pointers/trait-objects.md
[this blog post]: https://smallcultfollowing.com/babysteps/blog/2019/10/26/async-fn-in-traits-are-hard/
[RPIT]: https://doc.rust-lang.org/reference/types/impl-trait.html#abstract-return-types
[RPITIT]: https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits.html
