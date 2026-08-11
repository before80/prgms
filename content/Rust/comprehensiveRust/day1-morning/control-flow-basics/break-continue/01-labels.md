+++
title = "4.5.1 标签"
date = 2026-08-11T11:30:00+08:00
weight = 32
type = "docs"
description = "01-标签 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/control-flow-basics/break-continue/labels.html](https://google.github.io/comprehensive-rust/control-flow-basics/break-continue/labels.html)

# 4.5.1 标签

`continue` 和 `break` 都可以可选地接受一个标签参数，用于跳出嵌套循环：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let s = [[5, 6, 7], [8, 9, 10], [21, 15, 32]];
    let mut elements_searched = 0;
    let target_value = 10;
    'outer: for i in 0..=2 {
        for j in 0..=2 {
            elements_searched += 1;
            if s[i][j] == target_value {
                break 'outer;
            }
        }
    }
    dbg!(elements_searched);
}
```

> - 带标签的 `break` 也适用于任意块，例如：
>   ```rust
>   // Copyright 2024 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   'label: {
>       break 'label;
>       println!("This line gets skipped");
>   }
>   ```

