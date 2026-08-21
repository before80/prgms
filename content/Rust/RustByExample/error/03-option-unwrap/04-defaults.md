+++
title = "04-默认值：`or`、`or_else`、`get_or_insert`、`get_or_insert_with`"
date = 2026-08-20T21:20:00+08:00
weight = 145
type = "docs"
description = "默认值：`or`、`or_else`、`get_or_insert`、`get_or_insert_with` — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/error/option_unwrap/defaults.html](https://doc.rust-lang.org/stable/rust-by-example/error/option_unwrap/defaults.html)

# 默认值：`or`、`or_else`、`get_or_insert`、`get_or_insert_with`

解包 `Option` 并在其为 `None` 时回退到默认值，有不止一种方式。要选择符合需求的方式，需要考虑：

* 需要立即求值（eager）还是惰性求值（lazy）？
* 需要保留原来的空值不动，还是就地修改？

## `or()` 可链式调用、立即求值、保留空值不变 {#or-可链式调用立即求值保留空值不变}

如下所示，`or()` 可链式调用，并立即求值其参数。注意：由于 `or` 的参数会立即求值，传给 `or` 的变量会被移动（move）。

```rust
#[derive(Debug)]
enum Fruit { Apple, Orange, Banana, Kiwi, Lemon }

fn main() {
    let apple = Some(Fruit::Apple);
    let orange = Some(Fruit::Orange);
    let no_fruit: Option<Fruit> = None;

    let first_available_fruit = no_fruit.or(orange).or(apple);
    println!("first_available_fruit: {:?}", first_available_fruit);
    // first_available_fruit: Some(Orange)

    // `or` 会移动其参数。
    // 上例中 `or(orange)` 返回了 `Some`，因此不会调用 `or(apple)`。
    // 但名为 `apple` 的变量无论如何已被移动，不能再使用。
    // println!("Variable apple was moved, so this line won't compile: {:?}", apple);
    // TODO: 取消上一行注释可查看编译错误
}
```
## `or_else()` 可链式调用、惰性求值、保留空值不变 {#or-else-可链式调用惰性求值保留空值不变}

另一种选择是使用 `or_else`：同样可链式调用，但是惰性求值，如下所示：

```rust
#[derive(Debug)]
enum Fruit { Apple, Orange, Banana, Kiwi, Lemon }

fn main() {
    let no_fruit: Option<Fruit> = None;
    let get_kiwi_as_fallback = || {
        println!("Providing kiwi as fallback");
        Some(Fruit::Kiwi)
    };
    let get_lemon_as_fallback = || {
        println!("Providing lemon as fallback");
        Some(Fruit::Lemon)
    };

    let first_available_fruit = no_fruit
        .or_else(get_kiwi_as_fallback)
        .or_else(get_lemon_as_fallback);
    println!("first_available_fruit: {:?}", first_available_fruit);
    // Providing kiwi as fallback
    // first_available_fruit: Some(Kiwi)
}
```
## `get_or_insert()` 立即求值、就地修改空值 {#get-or-insert-立即求值就地修改空值}

为确保 `Option` 含有值，可用 `get_or_insert` 用回退值就地修改它，如下所示。注意 `get_or_insert` 会立即求值其参数，因此变量 `apple` 会被移动：

```rust
#[derive(Debug)]
enum Fruit { Apple, Orange, Banana, Kiwi, Lemon }

fn main() {
    let mut my_fruit: Option<Fruit> = None;
    let apple = Fruit::Apple;
    let first_available_fruit = my_fruit.get_or_insert(apple);
    println!("first_available_fruit is: {:?}", first_available_fruit);
    println!("my_fruit is: {:?}", my_fruit);
    // first_available_fruit is: Apple
    // my_fruit is: Some(Apple)
    //println!("Variable named `apple` is moved: {:?}", apple);
    // TODO: 取消上一行注释可查看编译错误
}
```
## `get_or_insert_with()` 惰性求值、就地修改空值 {#get-or-insert-with-惰性求值就地修改空值}

不必显式提供回退值，也可以向 `get_or_insert_with` 传入闭包，如下：

```rust
#[derive(Debug)]
enum Fruit { Apple, Orange, Banana, Kiwi, Lemon }

fn main() {
    let mut my_fruit: Option<Fruit> = None;
    let get_lemon_as_fallback = || {
        println!("Providing lemon as fallback");
        Fruit::Lemon
    };
    let first_available_fruit = my_fruit
        .get_or_insert_with(get_lemon_as_fallback);
    println!("first_available_fruit is: {:?}", first_available_fruit);
    println!("my_fruit is: {:?}", my_fruit);
    // Providing lemon as fallback
    // first_available_fruit is: Lemon
    // my_fruit is: Some(Lemon)

    // 若 Option 已有值，则保持不变，且不会调用闭包
    let mut my_apple = Some(Fruit::Apple);
    let should_be_apple = my_apple.get_or_insert_with(get_lemon_as_fallback);
    println!("should_be_apple is: {:?}", should_be_apple);
    println!("my_apple is unchanged: {:?}", my_apple);
    // 输出如下。注意闭包 `get_lemon_as_fallback` 未被调用
    // should_be_apple is: Apple
    // my_apple is unchanged: Some(Apple)
}
```
### 参见： {#参见}

[`closures`][closures]、[`get_or_insert`][get_or_insert]、[`get_or_insert_with`][get_or_insert_with]、[`moved variables`][moved]、[`or`][or]、[`or_else`][or_else]

[closures]: https://doc.rust-lang.org/book/ch13-01-closures.html
[get_or_insert]: https://doc.rust-lang.org/core/option/enum.Option.html#method.get_or_insert
[get_or_insert_with]: https://doc.rust-lang.org/core/option/enum.Option.html#method.get_or_insert_with
[moved]: https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html
[or]: https://doc.rust-lang.org/core/option/enum.Option.html#method.or
[or_else]: https://doc.rust-lang.org/core/option/enum.Option.html#method.or_else
