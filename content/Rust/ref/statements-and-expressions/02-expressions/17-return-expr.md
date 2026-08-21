+++
title = "17-return 表达式"
date = 2026-08-18T08:45:00+08:00
weight = 60
type = "docs"
description = "return 表达式 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/expressions/return-expr.html](https://doc.rust-lang.org/reference/expressions/return-expr.html)

r[expr.return]
# return 表达式

r[expr.return.syntax]
```grammar,expressions
ReturnExpression -> `return` Expression?
```

r[expr.return.intro]
return 表达式用关键字 `return` 表示。

r[expr.return.behavior]
求值 `return` 表达式会将其参数移动到当前函数调用的指定输出位置，销毁当前函数的活动帧，并将控制转移到调用者帧。

r[expr.return.diverging]
`return` 表达式是[发散][diverging]的，类型为 [`!`]。

`return` 表达式的示例：

```rust
fn max(a: i32, b: i32) -> i32 {
    if a > b {
        return a;
    }
    return b;
}
```

[`!`]: type.never
[diverging]: divergence
