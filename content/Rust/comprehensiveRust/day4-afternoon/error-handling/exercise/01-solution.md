+++
title = "2.8.1 解答"
date = 2026-08-11T11:30:00+08:00
weight = 195
type = "docs"
description = "01-解答 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/error-handling/solution.html](https://google.github.io/comprehensive-rust/error-handling/solution.html)

# 2.8.1 解答

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

/// 树形结构表示的表达式。
#[derive(Debug)]
enum Expression {
    /// 对两个子表达式的运算。
    Op { op: Operation, left: Box<Expression>, right: Box<Expression> },

    /// 字面量值
    Value(i64),
}

#[derive(PartialEq, Eq, Debug)]
struct DivideByZeroError;

fn eval(e: Expression) -> Result<i64, DivideByZeroError> {
    match e {
        Expression::Op { op, left, right } => {
            let left = eval(*left)?;
            let right = eval(*right)?;
            Ok(match op {
                Operation::Add => left + right,
                Operation::Sub => left - right,
                Operation::Mul => left * right,
                Operation::Div => {
                    if right == 0 {
                        return Err(DivideByZeroError);
                    } else {
                        left / right
                    }
                }
            })
        }
        Expression::Value(v) => Ok(v),
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_error() {
        assert_eq!(
            eval(Expression::Op {
                op: Operation::Div,
                left: Box::new(Expression::Value(99)),
                right: Box::new(Expression::Value(0)),
            }),
            Err(DivideByZeroError)
        );
    }

    #[test]
    fn test_ok() {
        let expr = Expression::Op {
            op: Operation::Sub,
            left: Box::new(Expression::Value(20)),
            right: Box::new(Expression::Value(10)),
        };
        assert_eq!(eval(expr), Ok(10));
    }
}
```

- **`Result` 返回类型：** 函数签名改为返回 `Result<i64, DivideByZeroError>`。这一显式类型签名迫使调用方处理失败的可能性。
- **`?` 运算符：** 在递归调用上使用 `?`：`eval(*left)?`。这样可以干净地传播错误。若 `eval` 返回 `Err`，函数立刻返回该 `Err`；若返回 `Ok(v)`，则把 `v` 赋给 `left`（或 `right`）。
- **`Ok` 包装：** 成功结果必须包在 `Ok(...)` 中。
- **处理除以零：** 显式检查 `right == 0` 并返回 `Err(DivideByZeroError)`，以此取代原代码中的 panic。

> <summary>讲师备注</summary>
>
> - 可说明 `DivideByZeroError` 是单元结构体（无字段），在此足够用，因为没有关于该错误的额外上下文需要提供。
> - 可讨论：`?` 让错误处理几乎像异常一样简洁，但控制流是显式的。

