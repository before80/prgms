+++
title = "05-trait"
date = 2026-08-20T21:20:00+08:00
weight = 115
type = "docs"
description = "trait — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/scope/lifetime/trait.html](https://doc.rust-lang.org/stable/rust-by-example/scope/lifetime/trait.html)

# trait

trait 方法中生命期的标注基本上与函数类似。注意，`impl` 也可能有生命周期的标注。

```rust
// 带有生命周期标注的结构体。
#[derive(Debug)]
 struct Borrowed<'a> {
     x: &'a i32,
 }

// 给 impl 标注生命周期。
impl<'a> Default for Borrowed<'a> {
    fn default() -> Self {
        Self {
            x: &10,
        }
    }
}

fn main() {
    let b: Borrowed = Default::default();
    println!("b is {:?}", b);
}
```
### 参见： {#参见}

[`trait`][trait]

[trait]: ../../trait/