+++
title = "18-类型参数"
date = 2026-08-18T08:45:00+08:00
weight = 83
type = "docs"
description = "类型参数 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/parameters.html](https://doc.rust-lang.org/reference/types/parameters.html)

r[type.generic]
# 类型参数

在带有类型参数声明的项的函数体中，其类型参数的名字就是类型：

```rust
fn to_vec<A: Clone>(xs: &[A]) -> Vec<A> {
    if xs.is_empty() {
        return vec![];
    }
    let first: A = xs[0].clone();
    let mut rest: Vec<A> = to_vec(&xs[1..]);
    rest.insert(0, first);
    rest
}
```

此处，`first` 的类型为 `A`，指的是 `to_vec` 的类型参数 `A`；而 `rest` 的类型为 `Vec<A>`，即元素类型为 `A` 的向量。
