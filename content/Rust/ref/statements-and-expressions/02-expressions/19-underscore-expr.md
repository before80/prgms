+++
title = "19-下划线表达式"
date = 2026-08-18T08:45:00+08:00
weight = 62
type = "docs"
description = "下划线表达式 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/expressions/underscore-expr.html](https://doc.rust-lang.org/reference/expressions/underscore-expr.html)

r[expr.placeholder]
# 下划线表达式

r[expr.placeholder.syntax]
```grammar,expressions
UnderscoreExpression -> `_`
```

r[expr.placeholder.intro]
下划线表达式用符号 `_` 表示，用于在解构赋值中标记占位符。

r[expr.placeholder.lhs-assignment-only]
它们只能出现在赋值的左侧。

r[expr.placeholder.pattern]
注意，这与[通配符模式](../../patterns/#wildcard-pattern)不同。

`_` 表达式的示例：

```rust
let p = (1, 2);
let mut a = 0;
(_, a) = p;

struct Position {
    x: u32,
    y: u32,
}

Position { x: a, y: _ } = Position{ x: 2, y: 3 };

// 未使用的结果：对 `_` 赋值用于表明意图并消除警告
_ = 2 + 2;
// 会触发 unused_must_use 警告
// 2 + 2;

// 在 let 绑定中使用通配符模式的等价做法
let _ = 2 + 2;
```
