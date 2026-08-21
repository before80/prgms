+++
title = "10-重温error的使用"
date = 2026-08-17T22:00:00+08:00
weight = 101
type = "docs"
description = "重温error的使用 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/99_zh-cn.html](https://tourofrust.com/99_zh-cn.html)

# 重温error的使用

Rust可能有过多的错误表示方法，但标准库有一个通用特性 `std::error::Error` 来描述错误。     

使用智能指针“Box”，我们可以使用类型`Box<dyn std::error::Error>`作为常见的返回错误类型，因为它允许我们在堆上、高级别的传播错误，而不必知道特定的类型。     

在 Rust 之旅的早期，我们了解到 `main` 可以返回一个错误。我们现在可以返回一个类型，该类型能够描述我们程序中可能发生的几乎任何类型的错误，只要错误的数据结构实现了 Rust 的通用`Error`特征。
```rust
fn main() -> Result<(), Box<dyn std::error:Error>>
```

## 示例代码

```rust
use core::fmt::Display;
use std::error::Error;

struct Pie;

#[derive(Debug)]
struct NotFreshError;

impl Display for NotFreshError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "This pie is not fresh!")
    }
}

impl Error for NotFreshError {}

impl Pie {
    fn eat(&self) -> Result<(), Box<dyn Error>> {
        Err(Box::new(NotFreshError))
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let heap_pie = Box::new(Pie);
    heap_pie.eat()?;
    Ok(())
}
```
