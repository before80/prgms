+++
title = "02-Iterator::find"
date = 2026-08-20T21:20:00+08:00
weight = 65
type = "docs"
description = "Iterator::find — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/fn/closures/closure_examples/iter_find.html](https://doc.rust-lang.org/stable/rust-by-example/fn/closures/closure_examples/iter_find.html)

# Iterator::find

​	`Iterator::find` 是一个函数，在传给它一个迭代器时，将用 `Option` 类型返回第一个满足谓词的元素。它的签名如下：

```rust
pub trait Iterator {
    // 被迭代的元素类型。
    type Item;

    // `find` 接受 `&mut self`，意味着调用者可能被借用并修改，
    // 但不会被消费（不会失去所有权）。
    fn find<P>(&mut self, predicate: P) -> Option<Self::Item> where
        // `FnMut` 意味着任何被捕获的变量至多可以被修改，不会被消费。
        // `&Self::Item` 表示闭包通过引用接收参数。
        P: FnMut(&Self::Item) -> bool;
}
```
```rust
fn main() {
    let vec1 = vec![1, 2, 3];
    let vec2 = vec![4, 5, 6];

    // `vec1.iter()` 产出 `&i32`。
    let mut iter = vec1.iter();

    // `vec2.into_iter()` 产出 `i32`。
    let mut into_iter = vec2.into_iter();

    // `iter()` 产出 `&i32`，而 `find` 将 `&Item` 传给谓词。
    // 由于 `Item = &i32`，闭包参数的类型是 `&&i32`，
    // 我们用模式 `&&x` 将其解引用为 `i32`。
    println!("Find 2 in vec1: {:?}", iter.find(|&&x| x == 2)); // Find 2 in vec1: Some(2)

    // `into_iter()` 产出 `i32`，而 `find` 将 `&Item` 传给谓词。
    // 由于 `Item = i32`，闭包参数的类型是 `&i32`，
    // 我们用模式 `&x` 将其解引用为 `i32`。
    println!("Find 2 in vec2: {:?}", into_iter.find(|&x| x == 2)); // Find 2 in vec2: None
    let array1 = [1, 2, 3];
    let array2 = [4, 5, 6];

    // `array1.iter()` 产出 `&i32`，而 `find` 将 `&Item` 传给谓词。
    // 由于 `Item = &i32`，闭包参数的类型是 `&&i32`。
    println!("Find 2 in array1: {:?}", array1.iter().find(|&&x| x == 2)); // Find 2 in array1: Some(2)
    // `array2.into_iter()` 产出 `i32`（自 Rust 2021 edition 起），而
    // `find` 将 `&Item` 传给谓词。由于 `Item = i32`，
    // 闭包参数的类型是 `&i32`。
    println!("Find 2 in array2: {:?}", array2.into_iter().find(|&x| x == 2)); // Find 2 in array2: None
}
```
​	`Iterator::find`会给你一个物品的参考。但如果你想要 `item`*索引*，可以用 `Iterator::position`。

```rust
fn main() {
    let vec = vec![1, 9, 3, 3, 13, 2];

    // `position` 将迭代器的 `Item` 按值传给谓词。
    // `vec.iter()` 产出 `&i32`，所以谓词收到 `&i32`，
    // 我们用模式 `&x` 将其解引用为 `i32`。
    let index_of_first_even_number = vec.iter().position(|&x| x % 2 == 0);
    assert_eq!(index_of_first_even_number, Some(5));

    // `vec.into_iter()` 产出 `i32`，所以谓词直接收到 `i32`。
    let index_of_first_negative_number = vec.into_iter().position(|x| x < 0);
    assert_eq!(index_of_first_negative_number, None);
}
```



### 参见： {#参见}

[`std::iter::Iterator::find`][find]

[find]: https://rustwiki.org/zh-CN/std/iter/trait.Iterator.html#method.find
