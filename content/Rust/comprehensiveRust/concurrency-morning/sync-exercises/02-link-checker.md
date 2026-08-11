+++
title = "6.2 多线程链接检查器"
date = 2026-08-11T11:30:00+08:00
weight = 363
type = "docs"
description = "02-多线程链接检查器 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/sync-exercises/link-checker.html](https://google.github.io/comprehensive-rust/concurrency/sync-exercises/link-checker.html)

# 6.2 多线程链接检查器

让我们用新知识做一个多线程链接检查器。它应从某个网页开始，检查页面上的链接是否有效；再递归检查同一域名上的其他页面，直到所有页面都验证完毕。

为此需要 HTTP 客户端，例如 [`reqwest`][1]；还需要找链接的方式，可用 [`scraper`][2]；最后需要处理错误，我们用 [`thiserror`][3]。

创建新的 Cargo 项目，并把 `reqwest` 作为依赖添加：

```shell
cargo new link-checker
cd link-checker
cargo add --features blocking reqwest
cargo add scraper
cargo add thiserror
```

> 若 `cargo add` 失败并提示 `error: no such subcommand`，请手动编辑 `Cargo.toml`，加入下面列出的依赖。

`cargo add` 调用会把 `Cargo.toml` 更新成类似这样：

```toml
[package]
name = "link-checker"
version = "0.1.0"
edition = "2024"
publish = false

[dependencies]
reqwest = { version = "0.13.1", features = ["blocking"] }
scraper = "0.25.0"
thiserror = "2.0.18"
```

现在可以下载起始页。可先用较小站点试，例如 `https://www.google.org/`。

你的 `src/main.rs` 大致如下：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use reqwest::Url;
use reqwest::blocking::Client;
use scraper::{Html, Selector};
use thiserror::Error;

#[derive(Error, Debug)]
enum Error {
    #[error("request error: {0}")]
    ReqwestError(#[from] reqwest::Error),
    #[error("bad http response: {0}")]
    BadResponse(String),
}

#[derive(Debug)]
struct CrawlCommand {
    url: Url,
    extract_links: bool,
}

fn visit_page(client: &Client, command: &CrawlCommand) -> Result<Vec<Url>, Error> {
    println!("Checking {:#}", command.url);
    let response = client.get(command.url.clone()).send()?;
    if !response.status().is_success() {
        return Err(Error::BadResponse(response.status().to_string()));
    }

    let mut link_urls = Vec::new();
    if !command.extract_links {
        return Ok(link_urls);
    }

    let base_url = response.url().clone();
    let body_text = response.text()?;
    let document = Html::parse_document(&body_text);

    let selector = Selector::parse("a").unwrap();
    let href_values = document
        .select(&selector)
        .filter_map(|element| element.value().attr("href"));
    for href in href_values {
        match base_url.join(href) {
            Ok(link_url) => {
                link_urls.push(link_url);
            }
            Err(err) => {
                println!("On {base_url:#}: ignored unparsable {href:?}: {err}");
            }
        }
    }
    Ok(link_urls)
}

fn main() {
    let client = Client::new();
    let start_url = Url::parse("https://www.google.org").unwrap();
    let crawl_command = CrawlCommand{ url: start_url, extract_links: true };
    match visit_page(&client, &crawl_command) {
        Ok(links) => println!("Links: {links:#?}"),
        Err(err) => println!("Could not extract links: {err:#}"),
    }
}
```

用以下命令运行 `src/main.rs` 中的代码：

```shell
cargo run
```

## 任务

- 用线程并行检查链接：把待检查的 URL 发到通道，让若干线程并行检查。
- 扩展为递归提取 `www.google.org` 域名上所有页面的链接。设一个大约 100 页的上限，以免被站点封禁。

> - 这是一道复杂练习，意在让学员有机会做比其他题更大的项目。成功标准可以是卡住某个「真实」问题，并在其他学员或讲师帮助下解决。


[1]: https://docs.rs/reqwest/
[2]: https://docs.rs/scraper/
[3]: https://docs.rs/thiserror/
