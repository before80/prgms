+++
title = "3.3 `Option`"
date = 2026-08-11T11:30:00+08:00
weight = 105
type = "docs"
description = "03-`Option` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/std-types/option.html](https://google.github.io/comprehensive-rust/std-types/option.html)

# 3.3 `Option`

我们已经见过一些 `Option<T>` 的用法。它要么存储类型为 `T` 的值，要么什么都不存。例如，
[`String::find`](https://doc.rust-lang.org/stable/std/string/struct.String.html#method.find)
返回 `Option<usize>`。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let name = "Löwe 老虎 Léopard Gepardi";
    let mut position: Option<usize> = name.find('é');
    dbg!(position);
    assert_eq!(position.unwrap(), 14);
    position = name.find('Z');
    dbg!(position);
    assert_eq!(position.expect("Character not found"), 0);
}
```

> - `Option` 使用广泛，不只在标准库中。
> - `unwrap` 会返回 `Option` 中的值，否则 panic。`expect` 类似，但可带错误信息。
>   - 你可以在 `None` 时 panic，但不能「不小心」忘记检查 `None`。
>   - 拼凑原型时到处 `unwrap`/`expect` 很常见，但生产代码通常会以更妥善的方式处理 `None`。
>
> - 「niche 优化」意味着：若存在某种不是 `T` 的有效值的表示，则 `Option<T>` 在内存中通常与 `T` 同大小。例如，引用不能为 NULL，因此 `Option<&T>` 自动用 NULL 表示 `None` 变体，从而可以与 `&T` 占用相同内存。

