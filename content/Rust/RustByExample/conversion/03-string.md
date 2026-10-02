+++
title = "03-`ToString` 和 `FromStr`"
date = 2026-08-20T21:20:00+08:00
weight = 34
type = "docs"
description = "`ToString` 和 `FromStr` — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/conversion/string.html](https://doc.rust-lang.org/stable/rust-by-example/conversion/string.html)

# `ToString` 和 `FromStr`

## `ToString` {#tostring}

​	要把任何类型转换成 `String`，只需要实现那个类型的 [`ToString`] trait。然而不要直接这么做，您应该实现[`fmt::Display`][Display] trait，它会自动提供 [`ToString`]，并且还可以用来打印类型，就像 [`print!`][print] 一节中讨论的那样。

```rust
use std::fmt;

struct Circle {
    radius: i32
}

impl fmt::Display for Circle {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Circle of radius {}", self.radius)
    }
}

fn main() {
    let circle = Circle { radius: 6 };
    println!("{}", circle.to_string());//Circle of radius 6
}
```
译注：一个实现 `ToString` 的例子

```rust
use std::string::ToString;

struct Circle {
    radius: i32
}

impl ToString for Circle {
    fn to_string(&self) -> String {
        format!("Circle of radius {:?}", self.radius)
    }
}

fn main() {
    let circle = Circle { radius: 6 };
    println!("{}", circle.to_string());//Circle of radius 6
}
```
## 解析字符串 {#解析字符串}

​	将字符串转换为多种类型是很有用的，但字符串操作中比较常见的一种是将字符串转换为数字。实现这一操作的惯用方法是使用[`parse`](https://doc.rust-lang.org/std/primitive.str.html#method.parse)函数，要么通过类型推断来实现，要么使用“涡轮鱼”语法指定要解析的类型。以下示例展示了这两种方法。

​	只要为目标类型实现了 [`FromStr`](https://doc.rust-lang.org/std/str/trait.FromStr.html) trait，该方法就会将字符串转换为指定类型。标准库中已为众多类型实现了这一trait。

```rust
fn main() {
    let parsed: i32 = "5".parse().unwrap();
    let turbo_parsed = "10".parse::<i32>().unwrap();

    let sum = parsed + turbo_parsed;
    println!{"Sum: {:?}", sum};//Sum: 15
}
```
​	要在用户定义的类型上实现此功能，只需为该类型实现[`FromStr`](https://doc.rust-lang.org/std/str/trait.FromStr.html) trait 即可。

```rust
use std::num::ParseIntError;
use std::str::FromStr;

#[derive(Debug)]
struct Circle {
    radius: i32,
}

impl FromStr for Circle {
    type Err = ParseIntError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.trim().parse() {
            Ok(num) => Ok(Circle{ radius: num }),
            Err(e) => Err(e),
        }
    }
}

fn main() {
    let radius = "    3 ";
    let circle: Circle = radius.parse().unwrap();
    println!("{:?}", circle);//Circle { radius: 3 }
}
```



[`ToString`]: https://rustwiki.org/zh-CN/std/string/trait.ToString.html
[Display]: https://rustwiki.org/zh-CN/std/fmt/trait.Display.html
[print]: ../hello/02-print/
[`parse`]: https://rustwiki.org/zh-CN/std/primitive.str.html#method.parse
[`FromStr`]: https://rustwiki.org/zh-CN/std/str/trait.FromStr.html
