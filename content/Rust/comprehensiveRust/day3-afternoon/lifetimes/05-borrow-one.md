+++
title = "3.5 只借用其中一个"
date = 2026-08-11T11:30:00+08:00
weight = 155
type = "docs"
description = "05-只借用其中一个 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/lifetimes/borrow-one.html](https://google.github.io/comprehensive-rust/lifetimes/borrow-one.html)

# 3.5 只借用其中一个

本例中 `find_nearest` 接受多个借用，但只返回其中一个。生命周期标注显式地把返回的借用与对应的参数借用绑定在一起。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug)]
struct Point(i32, i32);

/// 在 `points` 中搜索最接近 `query` 的点。
/// 假定 `points` 中至少有一个点。
fn find_nearest<'a>(points: &'a [Point], query: &Point) -> &'a Point {
    fn cab_distance(p1: &Point, p2: &Point) -> i32 {
        (p1.0 - p2.0).abs() + (p1.1 - p2.1).abs()
    }

    let mut nearest = None;
    for p in points {
        if let Some((_, nearest_dist)) = nearest {
            let dist = cab_distance(p, query);
            if dist < nearest_dist {
                nearest = Some((p, dist));
            }
        } else {
            nearest = Some((p, cab_distance(p, query)));
        };
    }

    nearest.map(|(p, _)| p).unwrap()
    // query // What happens if we do this instead?
}

fn main() {
    let points = &[Point(1, 0), Point(1, 0), Point(-1, 0), Point(0, -1)];
    let query = Point(0, 2);
    let nearest = find_nearest(points, &query);

    // 此时 `query` 未被借用。
    drop(query);

    dbg!(nearest);
}
```

> - 折叠 `find_nearest` 的定义可能有助于把注意力放在函数签名上。函数内的实际逻辑较复杂，对借用分析而言并不重要。
>
> - 调用 `find_nearest` 时，返回的引用并不借用 `query`，因此在 `nearest` 仍有效时我们可以丢弃它。
>
> - 但如果返回了错误的借用会怎样？把 `find_nearest` 的最后一行改成返回 `query`。向学员展示编译错误。
>
> - 首先必须给 `query` 加上生命周期标注。向学员展示可以为 `find_nearest` 添加第二个生命周期 `'b`。
>
> - 向学员展示新的错误。借用检查器会验证函数体中的逻辑确实返回具有正确生命周期的引用，强制函数遵守签名所设定的契约。
>
> # 延伸阅读
>
> - 错误中的「help」信息指出，我们可以添加生命周期约束 `'b: 'a`，表示 `'b` 至少与 `'a` 一样长，从而允许返回 `query`。这是生命周期子类型（lifetime subtyping）的例子，允许在期望较短生命周期的地方返回较长生命周期。
>
> - 我们也可以通过返回 `'static` 生命周期做类似的事，例如对 `static` 变量的引用。`'static` 保证比任何其他生命周期都长，因此用它替换较短生命周期总是安全的。

