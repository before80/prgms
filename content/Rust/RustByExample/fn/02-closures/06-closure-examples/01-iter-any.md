+++
title = "01-Iterator::any"
date = 2026-08-20T21:20:00+08:00
weight = 64
type = "docs"
description = "Iterator::any — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/fn/closures/closure_examples/iter_any.html](https://doc.rust-lang.org/stable/rust-by-example/fn/closures/closure_examples/iter_any.html)

# Iterator::any

​	`Iterator::any` 是一个函数，若传给它一个迭代器（iterator），当其中任一元素满足谓词（predicate）时它将返回 `true`，否则返回 `false`（译注：谓词是闭包规定的， `true`/`false` 是闭包作用在元素上的返回值）。它的签名如下：

```rust
pub trait Iterator {
    // 被迭代的元素类型。
    type Item;

    // `any` 接受 `&mut self`，意味着调用者可能被借用并修改，
    // 但不会被消费（不会失去所有权）。
    fn any<F>(&mut self, f: F) -> bool where
        // `FnMut` 意味着任何被捕获的变量至多可以被修改，不会被消费。
        // `Self::Item` 是闭包参数的类型，由迭代器决定
        // （例如 `.iter()` 产生 `&T`，`.into_iter()` 产生 `T`）。
        F: FnMut(Self::Item) -> bool;
}
```
```rust
fn main() {
    let vec1 = vec![1, 2, 3];
    let vec2 = vec![4, 5, 6];

    // 对 vec 调用 `iter()` 会举出 `&i32`。通过 `&x` 模式解构为 `i32`。
    println!("2 in vec1: {}", vec1.iter()     .any(|&x| x == 2)); // 2 in vec1: true
    // 对 vec 调用 `into_iter()` 会举出 `i32`。无需解构。
    println!("2 in vec2: {}", vec2.into_iter().any(|x| x == 2)); // 2 in vec2: false
    // `iter()` 只是借用 `vec1` 及其元素，所以之后仍可使用它们
    println!("vec1 len: {}", vec1.len()); // vec1 len: 3
    println!("First element of vec1 is: {}", vec1[0]); // First element of vec1 is: 1

    // `into_iter()` 会移动 `vec2` 及其元素，因此之后不能再使用它们
    // println!("First element of vec2 is: {}", vec2[0]);
    // println!("vec2 len: {}", vec2.len());

    // TODO：取消上面两行的注释，观察编译错误。
    let array1 = [1, 2, 3];
    let array2 = [4, 5, 6];
    // 对数组调用 `iter()` 会举出 `&i32`。
    println!("2 in array1: {}", array1.iter()     .any(|&x| x == 2)); // 2 in array1: true
    // 对数组调用 `into_iter()` 会举出 `i32`。
    println!("2 in array2: {}", array2.into_iter().any(|x| x == 2)); // 2 in array2: false
}
```
### 参见： {#参见}

[`std::iter::Iterator::any`][any]

[any]: https://rustwiki.org/zh-CN/std/iter/trait.Iterator.html#method.any
