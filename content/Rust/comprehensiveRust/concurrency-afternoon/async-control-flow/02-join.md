+++
title = "3.2 Join"
date = 2026-08-11T11:30:00+08:00
weight = 376
type = "docs"
description = "02-Join — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/async-control-flow/join.html](https://google.github.io/comprehensive-rust/concurrency/async-control-flow/join.html)

# 3.2 Join

join 操作会等待一组 future 全部就绪，然后返回它们的结果集合。这类似于 JavaScript 中的 `Promise.all`，或 Python 中的 `asyncio.gather`。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use anyhow::Result;
use futures::future;
use reqwest;
use std::collections::HashMap;

async fn size_of_page(url: &str) -> Result<usize> {
    let resp = reqwest::get(url).await?;
    Ok(resp.text().await?.len())
}

#[tokio::main]
async fn main() {
    let urls: [&str; 4] = [
        "https://google.com",
        "https://httpbin.org/ip",
        "https://play.rust-lang.org/",
        "BAD_URL",
    ];
    let futures_iter = urls.into_iter().map(size_of_page);
    let results = future::join_all(futures_iter).await;
    let page_sizes_dict: HashMap<&str, Result<usize>> =
        urls.into_iter().zip(results.into_iter()).collect();
    println!("{page_sizes_dict:?}");
}
```

> 把本示例复制到准备好的 `src/main.rs` 并从那里运行。
>
> - 对于类型互不相交的多个 future，可以使用 `std::future::join!`，但必须在编译期知道有多少个 future。它目前在 `futures` crate 中，很快会在 `std::future` 中稳定。
>
> - `join` 的风险是：其中一个 future 可能永远不会就绪，这会使程序停滞。
>
> - 也可以把 `join_all` 与 `join!` 组合，例如同时 join 对 HTTP 服务的所有请求以及一次数据库查询。试着给 future 加上 `tokio::time::sleep`，并用 `futures::join!`。这不是超时（超时需要 `select!`，下一章说明），但可以演示 `join!`。

