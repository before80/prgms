+++
title = "01-`?` 用法"
date = 2026-08-20T21:20:00+08:00
weight = 164
type = "docs"
description = "`?` 用法 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/std/result/question_mark.html](https://doc.rust-lang.org/stable/rust-by-example/std/result/question_mark.html)

# `?` 用法

把 result 用 match 连接起来会显得很难看；幸运的是，`?` 运算符可以把这种逻辑变得干净漂亮。`?` 运算符用在返回值为 `Result` 的表达式后面，它等同于这样一个匹配表达式：其中 `Err(err)` 分支展开成提前返回的 `return Err(err)`，而 `Ok(ok)` 分支展开成 `ok` 表达式。

```rust
mod checked {
    #[derive(Debug)]
    enum MathError {
        DivisionByZero,
        NegativeLogarithm,
        NegativeSquareRoot,
    }

    type MathResult = Result<f64, MathError>;

    fn div(x: f64, y: f64) -> MathResult {
        if y == 0.0 {
            Err(MathError::DivisionByZero)
        } else {
            Ok(x / y)
        }
    }

    fn sqrt(x: f64) -> MathResult {
        if x < 0.0 {
            Err(MathError::NegativeSquareRoot)
        } else {
            Ok(x.sqrt())
        }
    }

    fn ln(x: f64) -> MathResult {
        if x < 0.0 {
            Err(MathError::NegativeLogarithm)
        } else {
            Ok(x.ln())
        }
    }

    // 中间函数
    fn op_(x: f64, y: f64) -> MathResult {
        // 如果 `div` “失败” 了，那么返回 `DivisionByZero`
        let ratio = div(x, y)?;

        // 如果 `ln` “失败” 了，那么返回 `NegativeLogarithm`
        let ln = ln(ratio)?;

        sqrt(ln)
    }

    pub fn op(x: f64, y: f64) {
        match op_(x, y) {
            Err(why) => panic!("{}",match why {
                MathError::NegativeLogarithm
                    => "logarithm of negative number",
                MathError::DivisionByZero
                    => "division by zero",
                MathError::NegativeSquareRoot
                    => "square root of negative number",
            }),
            Ok(value) => println!("{}", value),
        }
    }
}

fn main() {
    checked::op(1.0, 10.0);
}
```
记得查阅[文档][docs]，里面有很多匹配/组合 `Result` 的方法。

[docs]: https://rustwiki.org/zh-CN/std/result/index.html
