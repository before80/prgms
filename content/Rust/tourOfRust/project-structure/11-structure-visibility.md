+++
title = "11-结构体可见性"
date = 2026-08-17T22:00:00+08:00
weight = 118
type = "docs"
description = "结构体可见性 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/116_zh-cn.html](https://tourofrust.com/116_zh-cn.html)

# 结构体可见性

就像函数一样，结构体可以使用 `pub` 声明它们想要在模块外暴露的东西。

## 示例代码

```rust
// SeaCreature 结构体在我们的模块外面也能使用了
pub struct SeaCreature {
    pub animal_type: String,
    pub name: String,
    pub arms: i32,
    pub legs: i32,
    // 我们把武器信息保密起来好了
    weapon: String,
}
```
