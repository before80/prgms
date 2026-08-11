+++
title = "3.4.1 使用 unsafe 块"
date = 2026-08-11T11:30:00+08:00
weight = 505
type = "docs"
description = "01-使用 unsafe 块 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/warm-up/unsafe-block.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/warm-up/unsafe-block.html)

# 3.4.1 使用 unsafe 块

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let numbers = vec![0, 1, 2, 3, 4];
    let i = numbers.len() / 2;

    let x = *numbers.get_unchecked(i);
    assert_eq!(i, x);
}
```

> 逐步讲解代码。确认听众熟悉解引用运算符。
>
> 尝试编译代码，触发编译器错误。
>
> 添加 unsafe 块：
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> # fn main() {
> #     let numbers = vec![0, 1, 2, 3, 4];
> #     let i = numbers.len() / 2;
> #
>  let x = unsafe { *numbers.get_unchecked(i) };
> #     assert_eq!(i, x);
> # }
> ```
>
> 引导听众进行代码审查。引导学员添加 safety comment。
>
> 添加 safety comment：
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> // SAFETY: `i` 必须在 0..numbers.len() 范围内
> ```
>
> _建议解法_
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> fn main() {
>     let numbers = vec![0, 1, 2, 3, 4];
>     let i = numbers.len() / 2;
>
>     let x = unsafe { *numbers.get_unchecked(i) };
>     assert_eq!(i, x);
> }
> ```

