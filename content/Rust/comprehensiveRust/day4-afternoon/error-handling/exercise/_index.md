+++
title = "2.8 练习：用 `Result` 重写"
date = 2026-08-11T11:30:00+08:00
weight = 194
type = "docs"
description = "练习：用 `Result` 重写 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/error-handling/exercise.html](https://google.github.io/comprehensive-rust/error-handling/exercise.html)

# 2.8 练习：用 `Result` 重写

本练习回顾第 2 天做过的表达式求值器练习。最初的解法忽略了一种可能的错误：除以零！请改写 `eval`，用惯用的错误处理应对这种情况，并在发生时返回错误。我们提供了简单的 `DivideByZeroError` 类型，作为 `eval` 的错误类型。

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

// 表达式求值器的原始实现。请改写为返回 `Result`，
// 并在除以 0 时产生错误。
fn eval(e: Expression) -> i64 {
    match e {
        Expression::Op { op, left, right } => {
            let left = eval(*left);
            let right = eval(*right);
            match op {
                Operation::Add => left + right,
                Operation::Sub => left - right,
                Operation::Mul => left * right,
                Operation::Div => if right != 0 {
                    left / right
                } else {
                    panic!("Cannot divide by zero!");
                },
            }
        }
        Expression::Value(v) => v,
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

> <summary>讲师备注</summary>
>
> - 这里的起始代码与上一练习的解法并不完全相同：我们显式加入了 panic，方便向学生标出错误情形所在。若学生困惑，请指出这一点。

