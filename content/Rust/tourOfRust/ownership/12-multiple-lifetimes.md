+++
title = "12-多个生命周期"
date = 2026-08-17T22:00:00+08:00
weight = 56
type = "docs"
description = "多个生命周期 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/54_zh-cn.html](https://tourofrust.com/54_zh-cn.html)

# 多个生命周期

生命周期注解可以通过区分函数签名中不同部分的生命周期，来允许我们显式地明确某些编译器靠自己无法解决的场景。

## 示例代码

```rust
struct Foo {
    x: i32,
}

// foo_b 和返回值共享同一生命周期
// foo_a 则拥有另一个不相关联的生命周期
fn do_something<'a, 'b>(foo_a: &'a Foo, foo_b: &'b Foo) -> &'b i32 {
    println!("{}", foo_a.x);
    println!("{}", foo_b.x);
    return &foo_b.x;
}

fn main() {
    let foo_a = Foo { x: 42 };
    let foo_b = Foo { x: 12 };
    let x = do_something(&foo_a, &foo_b);
    // foo_a 在这里被 dropped 释放因为只有 foo_b 的生命周期在此之后还在延续
    println!("{}", x);
    // x 在这里被 dropped 释放
    // foo_b 在这里被 dropped 释放
}
```
