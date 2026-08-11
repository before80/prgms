+++
title = "2.5.1 解答"
date = 2026-08-11T11:30:00+08:00
weight = 45
type = "docs"
description = "01-解答 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/tuples-and-arrays/solution.html](https://google.github.io/comprehensive-rust/tuples-and-arrays/solution.html)

# 2.5.1 解答

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn transpose(matrix: [[i32; 3]; 3]) -> [[i32; 3]; 3] {
    let mut result = [[0; 3]; 3];
    for i in 0..3 {
        for j in 0..3 {
            result[j][i] = matrix[i][j];
        }
    }
    result
}

fn main() {
    let matrix = [
        [101, 102, 103], // <-- 这行注释会让 rustfmt 换行
        [201, 202, 203],
        [301, 302, 303],
    ];

    println!("Original:");
    for row in matrix {
        println!("{row:?}");
    }

    let transposed = transpose(matrix);

    println!("\nTransposed:");
    for row in transposed {
        println!("{row:?}");
    }
}
```

- **数组类型：** 类型 `[[i32; 3]; 3]` 表示大小为 3 的数组，其中每个元素本身又是含 3 个 `i32` 的数组。这是 Rust 中表示多维数组的典型方式。
- **初始化：** 填充之前，我们用零初始化 `result`（`[[0; 3]; 3]`）。Rust 要求所有变量在使用前必须初始化；安全 Rust 中没有“未初始化内存”的概念。
- **Copy 语义：** 由 `Copy` 类型（如 `i32`）组成的数组本身也是 `Copy`。把 `matrix` 传给函数时按值复制。`result` 是一个新的、独立的数组。
- **迭代：** 我们用带范围（`0..3`）的标准 `for` 循环遍历下标。Rust 还有强大的迭代器（稍后会讲），但对矩阵转置来说，下标访问很直接。

> - 提醒一下：`[i32; 3]` 与 `[i32; 4]` 是不同的类型。数组大小是类型签名的一部分。
> - 问学员：若把签名改成 `mut matrix`，修改后再直接返回 `matrix` 会怎样？（答：能工作，但返回的是修改后的**副本**，`main` 中的原数组不会变。）

