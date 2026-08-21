+++
title = "07-`newtype` 惯用法"
date = 2026-08-20T21:20:00+08:00
weight = 95
type = "docs"
description = "`newtype` 惯用法 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/generics/new_types.html](https://doc.rust-lang.org/stable/rust-by-example/generics/new_types.html)

# `newtype` 惯用法

`newtype` 惯用法（译注：即为不同种类的数据分别定义新的类型）能保证在编译时，提供给程序的都是正确的类型。

比如说，实现一个 “年龄认证” 函数，它要求输入**必须**是 `Years` 类型。

```rust
struct Years(i64);

struct Days(i64);

impl Years {
    pub fn to_days(&self) -> Days {
        Days(self.0 * 365)
    }
}

impl Days {
    /// 舍去不满一年的部分
    pub fn to_years(&self) -> Years {
        Years(self.0 / 365)
    }
}

fn old_enough(age: &Years) -> bool {
    age.0 >= 18
}

fn main() {
    let age = Years(5);
    let age_days = age.to_days();
    println!("Old enough {}", old_enough(&age));
    println!("Old enough {}", old_enough(&age_days.to_years()));
    // println!("Old enough {}", old_enough(&age_days));
}
```
取消最后一行的注释，就可以发现提供给 `old_enough` 的必须是 `Years` 类型。

### See also: {#see-also}

[`structs`][struct]

[struct]: ../custom-types/01-structs/