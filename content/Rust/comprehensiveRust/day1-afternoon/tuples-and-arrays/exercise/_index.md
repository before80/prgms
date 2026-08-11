+++
title = "2.5 练习：嵌套数组"
date = 2026-08-11T11:30:00+08:00
weight = 44
type = "docs"
description = "练习：嵌套数组 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/tuples-and-arrays/exercise.html](https://google.github.io/comprehensive-rust/tuples-and-arrays/exercise.html)

# 2.5 练习：嵌套数组

数组可以包含其他数组：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
let array = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
```

这个变量的类型是什么？

用类似上面的数组，编写函数 `transpose`，对矩阵做转置（把行变成列）：

```bob
           ⎛⎡1 2 3⎤⎞      ⎡1 4 7⎤
"transpose"⎜⎢4 5 6⎥⎟  "=="⎢2 5 8⎥
           ⎝⎣7 8 9⎦⎠      ⎣3 6 9⎦
```

把下面的代码复制到 <https://play.rust-lang.org/> 并实现该函数。该函数只处理 3×3 矩阵。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn transpose(matrix: [[i32; 3]; 3]) -> [[i32; 3]; 3] {
    todo!()
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
