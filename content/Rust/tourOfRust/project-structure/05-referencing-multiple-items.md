+++
title = "05-引用多个项目"
date = 2026-08-17T22:00:00+08:00
weight = 112
type = "docs"
description = "引用多个项目 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/110_zh-cn.html](https://tourofrust.com/110_zh-cn.html)

# 引用多个项目

在同一个模块路径中可以引用多个项目，比如：

```rust
use std::f64::consts::{PI,TAU}
```

Ferris 不吃桃（TAU），它只吃派（PI）。
