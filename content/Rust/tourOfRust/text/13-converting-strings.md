+++
title = "13-字符串转换"
date = 2026-08-17T22:00:00+08:00
weight = 73
type = "docs"
description = "字符串转换 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/71_zh-cn.html](https://tourofrust.com/71_zh-cn.html)

# 字符串转换

许多类型都可以通过 `to_string` 转换为字符串。


而泛型函数 `parse` 则可将字符串或是字符串常量转换为其它类型，该函数会返回 `Result` 因为转换有可能失败。

## 示例代码

```rust
fn main() -> Result<(), std::num::ParseIntError> {
    let a = 42;
    let a_string = a.to_string();
    let b = a_string.parse::<i32>()?;
    println!("{} {}", a, b);
    Ok(())
}
```
