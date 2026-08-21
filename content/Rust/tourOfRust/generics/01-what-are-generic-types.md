+++
title = "01-泛型是什么？"
date = 2026-08-17T22:00:00+08:00
weight = 35
type = "docs"
description = "泛型是什么？ — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/33_zh-cn.html](https://tourofrust.com/33_zh-cn.html)

# 泛型是什么？

泛型允许我们不完全定义一个 `struct` 或 `enum`，使编译器能够根据我们的代码使用情况，在编译时创建一个完全定义的版本。

Rust 通常可以通过查看我们的实例化来推断出最终的类型，但是如果需要帮助，你可以使用 `::<T>` 操作符来显式地进行操作，
该操作符也被称为 `turbofish` （它是我的好朋友！）。

## 示例代码

```rust
// 一个部分定义的结构体类型
struct BagOfHolding<T> {
    item: T,
}

fn main() {
    // 注意：通过使用泛型，我们创建了编译时创建的类型，使代码更大
    // Turbofish 使之显式化
    let i32_bag = BagOfHolding::<i32> { item: 42 };
    let bool_bag = BagOfHolding::<bool> { item: true };
    
    // Rust 也可以推断出泛型的类型！
    let float_bag = BagOfHolding { item: 3.14 };

    // 注意：在现实生活中，不要把一袋东西放在另一袋东西里:)
    let bag_in_bag = BagOfHolding {
        item: BagOfHolding { item: "嘭！" },
    };

    println!(
        "{} {} {} {}",
        i32_bag.item, bool_bag.item, float_bag.item, bag_in_bag.item.item
    );
}
```
