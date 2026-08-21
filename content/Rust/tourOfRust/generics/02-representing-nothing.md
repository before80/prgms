+++
title = "02-表示空"
date = 2026-08-17T22:00:00+08:00
weight = 36
type = "docs"
description = "表示空 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/34_zh-cn.html](https://tourofrust.com/34_zh-cn.html)

# 表示空

在其他语言中，关键字 `null` 用于表示没有值。它给编程语言带来了困难，因为它使我们的程序在与变量字段交互时可能失败。

Rust 没有 `null`，但这并不代表我们不知道表示空的重要性！我们可以使用一个我们已经了解过的工具来简单地表示这一点。

因为缺少 `null` 值，这种为一个或多个替代值提供 `None` 替代表示的模式非常常见，
泛型有助于解决这一难题。

## 示例代码

```rust
enum Item {
    Inventory(String),
    // None represents the absence of an item
    None,
}

struct BagOfHolding {
    item: Item,
}
```
