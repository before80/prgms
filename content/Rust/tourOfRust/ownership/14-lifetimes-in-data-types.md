+++
title = "14-数据类型中的生命周期"
date = 2026-08-17T22:00:00+08:00
weight = 58
type = "docs"
description = "数据类型中的生命周期 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/56_zh-cn.html](https://tourofrust.com/56_zh-cn.html)

# 数据类型中的生命周期

和函数相同，数据类型也可以用生命周期注解来参数化其成员。 Rust 会验证引用所包含的数据结构永远也不会比引用指向的所有者存活周期更长。 我们不能在运行中拥有一个包括指向虚无的引用结构存在！

## 示例代码

```rust
struct Foo<'a> {
    i:&'a i32
}

fn main() {
    let x = 42;
    let foo = Foo {
        i: &x
    };
    println!("{}",foo.i);
}
```
