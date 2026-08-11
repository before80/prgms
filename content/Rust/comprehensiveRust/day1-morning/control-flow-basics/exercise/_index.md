+++
title = "4.8 练习：Collatz 序列"
date = 2026-08-11T11:30:00+08:00
weight = 35
type = "docs"
description = "练习：Collatz 序列 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/control-flow-basics/exercise.html](https://google.github.io/comprehensive-rust/control-flow-basics/exercise.html)

# 4.8 练习：Collatz 序列

[Collatz 序列](https://en.wikipedia.org/wiki/Collatz_conjecture) 对任意大于零的 n<sub>1</sub> 定义如下：

- 若 _n<sub>i</sub>_ 为 1，则序列在 _n<sub>i</sub>_ 处终止。
- 若 _n<sub>i</sub>_ 为偶数，则 _n<sub>i+1</sub> = n<sub>i</sub> / 2_。
- 若 _n<sub>i</sub>_ 为奇数，则 _n<sub>i+1</sub> = 3 * n<sub>i</sub> + 1_。

例如，从 _n<sub>1</sub>_ = 3 开始：

- 3 是奇数，因此 _n<sub>2</sub>_ = 3 * 3 + 1 = 10；
- 10 是偶数，因此 _n<sub>3</sub>_ = 10 / 2 = 5；
- 5 是奇数，因此 _n<sub>4</sub>_ = 3 * 5 + 1 = 16；
- 16 是偶数，因此 _n<sub>5</sub>_ = 16 / 2 = 8；
- 8 是偶数，因此 _n<sub>6</sub>_ = 8 / 2 = 4；
- 4 是偶数，因此 _n<sub>7</sub>_ = 4 / 2 = 2；
- 2 是偶数，因此 _n<sub>8</sub>_ = 1；并且
- 序列终止。

编写一个函数，计算给定初始 `n` 的 Collatz 序列长度。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 计算从 `n` 开始的 Collatz 序列长度。
fn collatz_length(mut n: i32) -> u32 {
  todo!("Implement this")
}

fn main() {
    println!("Length: {}", collatz_length(11)); // 应为 15
}
```
