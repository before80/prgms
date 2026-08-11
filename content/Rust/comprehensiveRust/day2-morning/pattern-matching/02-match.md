+++
title = "2.2 匹配值"
date = 2026-08-11T11:30:00+08:00
weight = 67
type = "docs"
description = "02-匹配值 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/pattern-matching/match.html](https://google.github.io/comprehensive-rust/pattern-matching/match.html)

# 2.2 匹配值

`match` 关键字可以把一个值与一个或多个_模式_（pattern）进行匹配。模式可以是简单值（类似 C/C++ 的 `switch`），也可以表达更复杂的条件：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[rustfmt::skip]
fn main() {
    let input = 'x';
    match input {
        'q'                       => println!("Quitting"),
        'a' | 's' | 'w' | 'd'     => println!("Moving around"),
        '0'..='9'                 => println!("Number input"),
        key if key.is_lowercase() => println!("Lowercase: {key}"),
        _                         => println!("Something else"),
    }
}
```

模式中的变量（本例中的 `key`）会创建绑定，可在该匹配分支内使用。下一页会进一步介绍。

匹配守卫（match guard）只有在条件为真时才让该分支匹配；条件为假时，`match` 会继续检查后面的分支。

> 要点：
>
> - 可以指出模式中某些特殊字符的含义
>   - `|` 表示「或」
>   - `..` 匹配任意数量的项
>   - `1..=5` 表示闭区间范围
>   - `_` 是通配符
>
> - 匹配守卫作为独立语法特性很重要：当需要比单独模式更简洁地表达复杂条件时，它不可或缺。
> - 匹配守卫与 `=>` 之后的 `if` 表达式不同。`if` 表达式是在匹配分支被选中之后才求值的；若块内 `if` 条件失败，不会回头再考虑原来 `match` 的其他分支。下面例子中，通配分支 `_ =>` 甚至永远不会被尝试。
>
> ```rust
> // Copyright 2024 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> #[rustfmt::skip]
> fn main() {
>     let input = 'a';
>     match input {
>         key if key.is_uppercase() => println!("Uppercase"),
>         key => if input == 'q' { println!("Quitting") },
>         _   => println!("Bug: this is never printed"),
>     }
> }
> ```
>
> - 守卫中的条件会应用到带 `|` 的模式中的每一个表达式。
> - 注意：不能把已有变量直接当作匹配分支的条件——它会被解释为变量名模式，从而创建遮蔽原变量的新绑定。例如：
>   ```rust
>   // Copyright 2024 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   let expected = 5;
>   match 123 {
>       expected => println!("Expected value is 5, actual is {expected}"),
>       _ => println!("Value was something else"),
>   }
>   ```
>   这里本想匹配数字 123，并让第一个分支检查值是否为 5。天真的预期是第一个分支因值不是 5 而不匹配；但实际上这被解释为总会匹配的变量模式，因此总会走第一个分支。若改用常量，就会按预期工作。
>
> # 深入探索
>
> - 另一段可向学员展示的模式语法是 `@`：把模式的一部分绑定到变量。例如：
>
>   ```rust
>   // Copyright 2024 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   let opt = Some(123);
>   match opt {
>       outer @ Some(inner) => {
>           println!("outer: {outer:?}, inner: {inner}");
>       }
>       None => {}
>   }
>   ```
>
>   本例中 `inner` 通过解构从 `Option` 取出值为 123；`outer` 捕获整个 `Some(inner)` 表达式，因此包含完整的 `Option::Some(123)`。这种写法不常见，但在更复杂的模式中可能有用。

