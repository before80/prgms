+++
title = "05-多重约束"
date = 2026-08-20T21:20:00+08:00
weight = 93
type = "docs"
description = "多重约束 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/generics/multi_bounds.html](https://doc.rust-lang.org/stable/rust-by-example/generics/multi_bounds.html)

# 多重约束

多重约束（multiple bounds）可以用 `+` 连接。和平常一样，类型之间使用 `,` 隔开。

```rust
use std::fmt::{Debug, Display};

fn compare_prints<T: Debug + Display>(t: &T) {
    println!("Debug: `{:?}`", t);
    println!("Display: `{}`", t);
}

fn compare_types<T: Debug, U: Debug>(t: &T, u: &U) {
    println!("t: `{:?}`", t);
    println!("u: `{:?}`", u);
}

fn main() {
    let string = "words";
    let array = [1, 2, 3];
    let vec = vec![1, 2, 3];

    compare_prints(&string);
    //compare_prints(&array);
    // 试一试 ^ 将此行注释去掉。

    compare_types(&array, &vec);
}
```
### 参见： {#参见}

[`std::fmt`][fmt] 和 [`trait`][traits]

[fmt]: ../hello/02-print/
[traits]: ../trait/