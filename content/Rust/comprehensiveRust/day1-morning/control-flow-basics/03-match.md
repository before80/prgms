+++
title = "4.3 `match` 表达式"
date = 2026-08-11T11:30:00+08:00
weight = 27
type = "docs"
description = "03-`match` 表达式 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/control-flow-basics/match.html](https://google.github.io/comprehensive-rust/control-flow-basics/match.html)

# 4.3 `match` 表达式

`match` 可用于将一个值与一个或多个选项进行匹配：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let val = 1;
    match val {
        1 => println!("one"),
        10 => println!("ten"),
        100 => println!("one hundred"),
        _ => {
            println!("something else");
        }
    }
}
```

与 `if` 表达式类似，`match` 也可以返回值：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let flag = true;
    let val = match flag {
        true => 1,
        false => 0,
    };
    println!("The value of {flag} is {val}");
}
```

> - `match` 分支从上到下求值，第一个匹配成功的分支会执行对应的主体。
>
> - 分支之间不会像其他语言中的 `switch` 那样发生 fall-through（贯穿）。
>
> - `match` 分支的主体可以是单个表达式，也可以是一个块。严格来说两者相同，因为块也是表达式，但学员此时可能还不完全理解这种对称性。
>
> - `match` 表达式必须是穷尽的（exhaustive），即要么覆盖所有可能的值，要么提供像 `_` 这样的默认分支。穷尽性用枚举最容易演示，但此时尚未介绍枚举。因此我们改用匹配 `bool`——最简单的原始类型——来演示。
>
> - 本页引入 `match` 时不讨论模式匹配（pattern matching），让学员先熟悉语法，而不一次塞入过多信息。模式匹配明天会更详细地讲，这里尽量不要展开太多。
>
> ## 扩展阅读
>
> - 为了进一步说明为何使用 `match`，可以把示例与用 `if` 写出的等价写法对比。第二种匹配 `bool` 的情况中，`if {} else {}` 与 `match` 相当接近。但在第一种检查多个分支的例子中，`match` 通常比 `if {} else if {} else if {} else` 更简洁。
>
> - `match` 还支持匹配守卫（match guards），可添加任意逻辑条件来决定是否进入该分支。但讲匹配守卫需要先解释模式匹配，而本页刻意避免这一点。

