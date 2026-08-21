+++
title = "06-where 子句"
date = 2026-08-20T21:20:00+08:00
weight = 94
type = "docs"
description = "where 子句 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/generics/where.html](https://doc.rust-lang.org/stable/rust-by-example/generics/where.html)

# where 子句

约束也可以使用 `where` 分句来表达，它放在 `{` 的前面，而不需写在类型第一次出现之前。另外 `where` 从句可以用于任意类型的限定，而不局限于类型参数本身。

`where` 在下面一些情况下很有用：

* 当分别指定泛型的类型和约束会更清晰时：

```rust
impl <A: TraitB + TraitC, D: TraitE + TraitF> MyTrait<A, D> for YourType {}

// 使用 `where` 从句来表达约束
impl <A, D> MyTrait<A, D> for YourType where
    A: TraitB + TraitC,
    D: TraitE + TraitF {}
```
* 当使用 `where` 从句比正常语法更有表现力时。本例中的 `impl` 如果不用
   `where` 从句，就无法直接表达。

```rust
use std::fmt::Debug;

trait PrintInOption {
    fn print_in_option(self);
}

// 这里需要一个 `where` 从句，否则就要表达成 `T: Debug`（这样意思就变了），
// 或者改用另一种间接的方法。
impl<T> PrintInOption for T where
    Option<T>: Debug {
    // 我们要将 `Option<T>: Debug` 作为约束，因为那是要打印的内容。
    // 否则我们会给出错误的约束。
    fn print_in_option(self) {
        println!("{:?}", Some(self));
    }
}

fn main() {
    let vec = vec![1, 2, 3];

    vec.print_in_option();
}
```
### 参见： {#参见}

相关的 [RFC][where]、[`struct`][struct] 和 [`trait`][trait]

[struct]: ../custom-types/01-structs/
[trait]: ../trait/
[where]: https://github.com/rust-lang/rfcs/blob/master/text/0135-where.md
