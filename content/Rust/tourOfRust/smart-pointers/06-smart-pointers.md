+++
title = "06-智能指针"
date = 2026-08-17T22:00:00+08:00
weight = 97
type = "docs"
description = "智能指针 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/95_zh-cn.html](https://tourofrust.com/95_zh-cn.html)

# 智能指针

除了能够使用`&`运算符创建对现有类型数据的引用之外, Rust 给我们提供了能够创建称为*智能指针*的*类引用*结构。   
我们可以在高层次上将引用视为一种类型，它使我们能够访问另一种类型.  智能指针的行为与普通引用不同，因为它们基于程序员编写的内部逻辑进行操作.  作为程序员的你就是*智能*的一部分。  
通常，智能指针实现了 `Deref`、`DerefMut` 和 `Drop` 特征，以指定当使用 `*` 和 `.` 运算符时解引用应该触发的逻辑。

## 示例代码

```rust
use std::ops::Deref;
struct TattleTell<T> {
    value: T,
}
impl<T> Deref for TattleTell<T> {
    type Target = T;
    fn deref(&self) -> &T {
        println!("{} was used!", std::any::type_name::<T>());
        &self.value
    }
}
fn main() {
    let foo = TattleTell {
        value: "secret message",
    };
    // dereference occurs here immediately 
    // after foo is auto-referenced for the
    // function `len`
    println!("{}", foo.len());
}
```
