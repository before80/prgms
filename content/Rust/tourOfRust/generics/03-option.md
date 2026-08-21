+++
title = "03-Option"
date = 2026-08-17T22:00:00+08:00
weight = 37
type = "docs"
description = "Option — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/35_zh-cn.html](https://tourofrust.com/35_zh-cn.html)

# Option

Rust 有一个内置的泛型枚举叫做 `Option`，它可以让我们不使用 `null` 就可以表示可以为空的值。

```
enum Option<T> {
    None,
    Some(T),
}
```

这个枚举很常见，使用关键字 `Some` 和 `None` 可以在任何地方创建其实例。

## 示例代码

```rust
// 一个部分定义的结构体
struct BagOfHolding<T> {
    // 我们的参数类型T可以传递给其他
    item: Option<T>,
}

fn main() {
    // 注意：一个放 i32 的 bag，里面什么都没有！
    // 我们必须注明类型，否则 Rust 不知道 bag 的类型
    let i32_bag = BagOfHolding::<i32> { item: None };

    if i32_bag.item.is_none() {
        println!("there's nothing in the bag!")
    } else {
        println!("there's something in the bag!")
    }

    let i32_bag = BagOfHolding::<i32> { item: Some(42) };

    if i32_bag.item.is_some() {
        println!("there's something in the bag!")
    } else {
        println!("there's nothing in the bag!")
    }

    // match 可以让我们优雅地解构 Option，并且确保我们处理了所有的可能情况！
    match i32_bag.item {
        Some(v) => println!("found {} in bag!", v),
        None => println!("found nothing"),
    }
}
```
