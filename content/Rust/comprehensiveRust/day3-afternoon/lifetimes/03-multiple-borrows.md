+++
title = "3.3 多个借用"
date = 2026-08-11T11:30:00+08:00
weight = 153
type = "docs"
description = "03-多个借用 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/lifetimes/multiple-borrows.html](https://google.github.io/comprehensive-rust/lifetimes/multiple-borrows.html)

# 3.3 多个借用

但当多个借用传入函数、且有一个要返回时呢？

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn multiple(a: &i32, b: &i32) -> &i32 {
    todo!("Return either `a` or `b`")
}

fn main() {
    let mut a = 5;
    let mut b = 10;

    let r = multiple(&a, &b);

    // Which one is still borrowed?
    // Should either mutation be allowed?
    a += 7;
    b += 7;

    dbg!(r);
}
```

> - 这段代码目前无法编译，因为缺少生命周期标注。在让它编译之前，借此机会让学员思考：返回值应延长哪个参数借用。
>
> - 我们向 `multiple` 传入两个借用，其中一个会返回，这意味着我们需要延长其中一个参数生命周期的借用。该延长哪一个？是否需要看 `multiple` 的函数体才能弄清？
>
> - 进行借用检查时，编译器不会查看 `multiple` 的函数体来推理流出的借用，而只查看函数签名。
>
> - 本例中没有足够信息判断返回的引用会借用 `a` 还是 `b`。向学员展示编译错误，并介绍生命周期语法：
>
>   ```rust
>   // Copyright 2025 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   fn multiple<'a>(a: &'a i32, b: &'a i32) -> &'a i32 { ... }
>   ```

