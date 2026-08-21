+++
title = "02-`TryFrom` 和 `TryInto`"
date = 2026-08-20T21:20:00+08:00
weight = 33
type = "docs"
description = "`TryFrom` 和 `TryInto` — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/conversion/try_from_try_into.html](https://doc.rust-lang.org/stable/rust-by-example/conversion/try_from_try_into.html)

# `TryFrom` 和 `TryInto`

类似于 [`From` 和 `Into`][from-into]，[`TryFrom`] 和 [`TryInto`] 是类型转换的通用 trait。不同于 `From`/`Into` 的是，`TryFrom` 和 `TryInto` trait 用于易出错的转换，也正因如此，其返回值是 [`Result`] 型。

[from-into]: 01-from-into/
[`TryFrom`]: https://rustwiki.org/zh-CN/std/convert/trait.TryFrom.html
[`TryInto`]: https://rustwiki.org/zh-CN/std/convert/trait.TryInto.html
[`Result`]: https://rustwiki.org/zh-CN/std/result/enum.Result.html

```rust
use std::convert::TryFrom;
use std::convert::TryInto;

#[derive(Debug, PartialEq)]
struct EvenNumber(i32);

impl TryFrom<i32> for EvenNumber {
    type Error = ();

    fn try_from(value: i32) -> Result<Self, Self::Error> {
        if value % 2 == 0 {
            Ok(EvenNumber(value))
        } else {
            Err(())
        }
    }
}

fn main() {
    // TryFrom

    assert_eq!(EvenNumber::try_from(8), Ok(EvenNumber(8)));
    assert_eq!(EvenNumber::try_from(5), Err(()));

    // TryInto

    let result: Result<EvenNumber, ()> = 8i32.try_into();
    assert_eq!(result, Ok(EvenNumber(8)));
    let result: Result<EvenNumber, ()> = 5i32.try_into();
    assert_eq!(result, Err(()));
}
```
