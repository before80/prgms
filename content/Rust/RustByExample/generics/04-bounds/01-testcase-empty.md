+++
title = "01-测试实例：空约束"
date = 2026-08-20T21:20:00+08:00
weight = 92
type = "docs"
description = "测试实例：空约束 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/generics/bounds/testcase_empty.html](https://doc.rust-lang.org/stable/rust-by-example/generics/bounds/testcase_empty.html)

# 测试实例：空约束

约束的工作机制会产生这样的效果：即使一个 `trait` 不包含任何功能，你仍然可以用它作为约束。标准库中的 `Eq` 和 `Ord` 就是这样的 `trait`。

```rust
struct Cardinal;
struct BlueJay;
struct Turkey;

trait Red {}
trait Blue {}

impl Red for Cardinal {}
impl Blue for BlueJay {}

// 这些函数只对实现了相应的 trait 的类型有效。
// 事实上这些 trait 内部是空的，但这没有关系。
fn red<T: Red>(_: &T)   -> &'static str { "red" }
fn blue<T: Blue>(_: &T) -> &'static str { "blue" }

fn main() {
    let cardinal = Cardinal;
    let blue_jay = BlueJay;
    let _turkey   = Turkey;

    // 由于约束，`red()` 不能作用于 blue_jay （蓝松鸟），反过来也一样。
    println!("A cardinal is {}", red(&cardinal));
    println!("A blue jay is {}", blue(&blue_jay));
    //println!("A turkey is {}", red(&_turkey));
    // ^ 试一试：去掉此行注释。
}
```
### 参见： {#参见}

[`std::cmp::Eq`][eq], [`std::cmp::Ord`][ord], 和 [`trait`][traits]

[eq]: https://rustwiki.org/zh-CN/std/cmp/trait.Eq.html
[ord]: https://rustwiki.org/zh-CN/std/cmp/trait.Ord.html
[traits]: ../../trait/