+++
title = "2.6 练习：表达式求值"
date = 2026-08-11T11:30:00+08:00
weight = 74
type = "docs"
description = "练习：表达式求值 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/pattern-matching/exercise.html](https://google.github.io/comprehensive-rust/pattern-matching/exercise.html)

# 2.6 练习：表达式求值

让我们为算术表达式写一个简单的递归求值器。

一个小算术表达式的例子是 `10 + 20`，求值为 `30`。可以把表达式表示成树：

```bob
            .-------.
    .------ |   +   | ------.
    |       '-------'       |
    v                       v
.--------.              .--------.
|   10   |              |   20   |
'--------'              '--------'
```

更大更复杂的表达式可以是 `(10 * 9) + ((3 - 4) * 5)`，求值为 `85`。我们把它表示成更大的树：

```bob
                              .-----.
            .---------------- |  +  | ----------------.
            |                 '-----'                 |
            v                                         v
         .-----.                                   .-----.
   .---- |  *  | ----.                       .---- |  *  | ----.
   |     '-----'     |                       |     '-----'     |
   v                 v                       v                 v
.------.          .-----.                 .-----.           .-----.
|  10  |          |  9  |           .---- |  "-"| ----.     |  5  |
'------'          '-----'           |     '-----'     |     '-----'
                                    v                 v
                                 .-----.           .-----.
                                 |  3  |           |  4  |
                                 '-----'           '-----'
```

在代码中，我们用两种类型表示这棵树：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 对两个子表达式执行的运算。
#[derive(Debug)]
enum Operation {
    Add,
    Sub,
    Mul,
    Div,
}

/// 树形结构的表达式。
#[derive(Debug)]
enum Expression {
    /// 对两个子表达式的运算。
    Op { op: Operation, left: Box<Expression>, right: Box<Expression> },

    /// 字面量值
    Value(i64),
}
```

这里的 `Box` 类型是智能指针，课程后面会详细介绍。可以用测试中看到的 `Box::new` 把表达式「装箱」。要求值已装箱的表达式，用解引用运算符（`*`）「拆箱」：`eval(*boxed_expr)`。

用下面命令新建一个 Cargo 库项目：

```sh
cargo new --lib evaluator
```

把下面的代码复制粘贴到 `src/lib.rs` 文件中。

然后开始实现 `eval`。用 `cargo test` 确保最终库通过测试。可以借助 `todo!()` 让测试逐个通过。也可以用 `#[ignore]` 暂时跳过某个测试：

```none
#[test]
#[ignore]
fn test_value() { .. }
```

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 对两个子表达式执行的运算。
#[derive(Debug)]
enum Operation {
    Add,
    Sub,
    Mul,
    Div,
}

/// 树形结构的表达式。
#[derive(Debug)]
enum Expression {
    /// 对两个子表达式的运算。
    Op { op: Operation, left: Box<Expression>, right: Box<Expression> },

    /// 字面量值
    Value(i64),
}

fn eval(e: Expression) -> i64 {
    todo!()
}

#[test]
fn test_value() {
    assert_eq!(eval(Expression::Value(19)), 19);
}

#[test]
fn test_sum() {
    assert_eq!(
        eval(Expression::Op {
            op: Operation::Add,
            left: Box::new(Expression::Value(10)),
            right: Box::new(Expression::Value(20)),
        }),
        30
    );
}

#[test]
fn test_recursion() {
    let term1 = Expression::Op {
        op: Operation::Mul,
        left: Box::new(Expression::Value(10)),
        right: Box::new(Expression::Value(9)),
    };
    let term2 = Expression::Op {
        op: Operation::Mul,
        left: Box::new(Expression::Op {
            op: Operation::Sub,
            left: Box::new(Expression::Value(3)),
            right: Box::new(Expression::Value(4)),
        }),
        right: Box::new(Expression::Value(5)),
    };
    assert_eq!(
        eval(Expression::Op {
            op: Operation::Add,
            left: Box::new(term1),
            right: Box::new(term2),
        }),
        85
    );
}

#[test]
fn test_zeros() {
    assert_eq!(
        eval(Expression::Op {
            op: Operation::Add,
            left: Box::new(Expression::Value(0)),
            right: Box::new(Expression::Value(0))
        }),
        0
    );
    assert_eq!(
        eval(Expression::Op {
            op: Operation::Mul,
            left: Box::new(Expression::Value(0)),
            right: Box::new(Expression::Value(0))
        }),
        0
    );
    assert_eq!(
        eval(Expression::Op {
            op: Operation::Sub,
            left: Box::new(Expression::Value(0)),
            right: Box::new(Expression::Value(0))
        }),
        0
    );
}

#[test]
fn test_div() {
    assert_eq!(
        eval(Expression::Op {
            op: Operation::Div,
            left: Box::new(Expression::Value(10)),
            right: Box::new(Expression::Value(2)),
        }),
        5
    )
}
```
