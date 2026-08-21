+++
title = "06-类单元结构体"
date = 2026-08-17T22:00:00+08:00
weight = 30
type = "docs"
description = "类单元结构体 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/28_zh-cn.html](https://tourofrust.com/28_zh-cn.html)

# 类单元结构体

结构体也可以没有任何字段。

就像第一章提到的，一个 *unit* 是空元组 `()` 的别称。这就是为什么，此类结构体被称为 `类单元`。

这种类型的结构体很少用到。

## 示例代码

```rust
struct Marker;

fn main() {
    let _m = Marker;
}
```
