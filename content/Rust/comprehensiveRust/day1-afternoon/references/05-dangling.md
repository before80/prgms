+++
title = "3.5 引用有效性"
date = 2026-08-11T11:30:00+08:00
weight = 51
type = "docs"
description = "05-引用有效性 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/references/dangling.html](https://google.github.io/comprehensive-rust/references/dangling.html)

# 3.5 引用有效性

Rust 对引用强制执行若干规则，使它们始终可以安全使用。一条规则是引用永远不能为 `null`，因此无需做 `null` 检查即可安全使用。目前我们要看的另一条规则是：引用不能比它所指向的数据**活得更久**。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let x_ref = {
        let x = 10;
        &x
    };
    dbg!(x_ref);
}
```

> - 这页幻灯片让学员思考：引用并不只是指针，因为 Rust 对引用的规则与其他语言不同。
>
> - 第 3 天讨论 Rust 的所有权系统时，我们会看其余的借用规则。
>
> ## 深入探索
>
> - Rust 中与可空性对应的是 `Option` 类型，可让任意类型“可空”（不只是引用/指针）。不过我们尚未介绍枚举或模式匹配，这里尽量不要展开太多细节。

