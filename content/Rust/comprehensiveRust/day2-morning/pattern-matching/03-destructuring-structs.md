+++
title = "2.3 解构结构体"
date = 2026-08-11T11:30:00+08:00
weight = 68
type = "docs"
description = "03-解构结构体 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/pattern-matching/destructuring-structs.html](https://google.github.io/comprehensive-rust/pattern-matching/destructuring-structs.html)

# 2.3 解构结构体

与元组一样，结构体也可以通过匹配来解构：

```rust
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
struct Move {
    delta: (i32, i32),
    repeat: u32,
}

#[rustfmt::skip]
fn main() {
    let m = Move { delta: (10, 0), repeat: 5 };

    match m {
        Move { delta: (0, 0), .. }        => println!("Standing still"),
        Move { delta: (x, 0), repeat }    => println!("{repeat} step x: {x}"),
        Move { delta: (0, y), repeat: 1 } => println!("Single step y: {y}"),
        _                                 => println!("Other move"),
    }
}
```

> - 修改 `m` 中的字面量，使它匹配其他模式。
> - 给 `Movement` 增加新字段，并按需要改模式。
> - 注意 `delta: (x, 0)` 是嵌套模式。
>
> ## 深入探索
>
> - 试一下 `match &m`，并查看捕获的类型。模式语法不变，但捕获会变成共享引用。这就是
>   [match ergonomics](https://rust-lang.github.io/rfcs/2005-match-ergonomics.html)，
>   在为枚举实现方法时写 `match self` 常常很有用。
>   - 对 `match &mut m` 同样成立：捕获会变成独占引用。
> - 捕获与常量表达式的区别有时很难一眼看出。试着把第一个分支里的 `10` 改成变量，会发现它微妙地不工作；改成 `const` 后又会正常。

