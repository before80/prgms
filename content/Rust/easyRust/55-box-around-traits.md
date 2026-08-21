+++
title = "55-用 Box 包裹 trait"
date = 2026-08-21T12:46:00+08:00
weight = 56
type = "docs"
description = "用 Box 包裹 trait — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_54.html](https://dhghomon.github.io/easy_rust/Chapter_54.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 用 Box 包裹 trait

`Box`对于返回trait非常有用。你可以像这个例子一样用泛型函数写trait:

```rust
use std::fmt::Display;

struct DoesntImplementDisplay {}

fn displays_it<T: Display>(input: T) {
    println!("{}", input);
}

fn main() {}
```

这个只能接受`Display`的东西，所以它不能接受我们的`DoesntImplementDisplay`结构。但是它可以接受很多其他的东西，比如`String`。

你也看到了，我们可以使用 `impl Trait` 来返回其他的trait，或者闭包。`Box`也可以用类似的方式使用。你可以使用 `Box`，否则编译器将不知道值的大小。这个例子表明，trait可以用在任何大小的东西上:

```rust
#![allow(dead_code)] // 让编译器别抱怨
use std::mem::size_of; // 用来获取类型大小

trait JustATrait {} // 我们会给所有类型实现它

enum EnumOfNumbers {
    I8(i8),
    AnotherI8(i8),
    OneMoreI8(i8),
}
impl JustATrait for EnumOfNumbers {}

struct StructOfNumbers {
    an_i8: i8,
    another_i8: i8,
    one_more_i8: i8,
}
impl JustATrait for StructOfNumbers {}

enum EnumOfOtherTypes {
    I8(i8),
    AnotherI8(i8),
    Collection(Vec<String>),
}
impl JustATrait for EnumOfOtherTypes {}

struct StructOfOtherTypes {
    an_i8: i8,
    another_i8: i8,
    a_collection: Vec<String>,
}
impl JustATrait for StructOfOtherTypes {}

struct ArrayAndI8 {
    array: [i8; 1000], // 这个会非常大
    an_i8: i8,
    in_u8: u8,
}
impl JustATrait for ArrayAndI8 {}

fn main() {
    println!(
        "{}, {}, {}, {}, {}",
        size_of::<EnumOfNumbers>(),
        size_of::<StructOfNumbers>(),
        size_of::<EnumOfOtherTypes>(),
        size_of::<StructOfOtherTypes>(),
        size_of::<ArrayAndI8>(),
    );
}
```

当我们打印这些东西的size的时候，我们得到`2, 3, 32, 32, 1002`。所以如果你像下面这样做的话，会得到一个错误：

```rust
// ⚠️
fn returns_just_a_trait() -> JustATrait {
    let some_enum = EnumOfNumbers::I8(8);
    some_enum
}
```

它说：

```text
error[E0746]: return type cannot have an unboxed trait object
  --> src\main.rs:53:30
   |
53 | fn returns_just_a_trait() -> JustATrait {
   |                              ^^^^^^^^^^ doesn't have a size known at compile-time
```

而这是真的，因为size可以是2，3，32，1002，或者其他任何东西。所以我们把它放在一个`Box`中。在这里我们还要加上`dyn`这个关键词。`dyn`这个词告诉你，你说的是一个trait，而不是一个结构体或其他任何东西。

所以你可以把函数改成这样。

```rust
// 🚧
fn returns_just_a_trait() -> Box<dyn JustATrait> {
    let some_enum = EnumOfNumbers::I8(8);
    Box::new(some_enum)
}
```

现在它工作了，因为在栈上只是一个`Box`，我们知道`Box`的大小。

你会经常看到`Box<dyn Error>`这种形式，因为有时你可能会有多个可能的错误。

我们可以快速创建两个错误类型来显示这一点。要创建一个正式的错误类型，你必须为它实现`std::error::Error`。这部分很容易:只要写出 `impl std::error::Error {}`。但错误还需要`Debug`和`Display`，这样才能给出问题的信息。`Debug`只要加上`#[derive(Debug)]`就行，很容易，但`Display`需要`.fmt()`方法。我们之前做过一次。

代码是这样的:

```rust
use std::error::Error;
use std::fmt;

#[derive(Debug)]
struct ErrorOne;

impl Error for ErrorOne {} // 现在它是带 Debug 的错误类型。该实现 Display 了：

impl fmt::Display for ErrorOne {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "You got the first error!") // 只是写出这条消息
    }
}


#[derive(Debug)] // 对 ErrorTwo 做同样的事
struct ErrorTwo;

impl Error for ErrorTwo {}

impl fmt::Display for ErrorTwo {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "You got the second error!")
    }
}

// 写一个只返回 String 或错误的函数
fn returns_errors(input: u8) -> Result<String, Box<dyn Error>> { // 用 Box<dyn Error> 可以返回任何实现了 Error 的类型

    match input {
        0 => Err(Box::new(ErrorOne)), // 别忘了放进 Box
        1 => Err(Box::new(ErrorTwo)),
        _ => Ok("Looks fine to me".to_string()), // 这是成功时的类型
    }

}

fn main() {

    let vec_of_u8s = vec![0_u8, 1, 80]; // 拿三个数字试试

    for number in vec_of_u8s {
        match returns_errors(number) {
            Ok(input) => println!("{}", input),
            Err(message) => println!("{}", message),
        }
    }
}
```

这将打印:

```text
You got the first error!
You got the second error!
Looks fine to me
```

如果我们没有`Box<dyn Error>`，写了这个，我们就有问题了。

```rust
// ⚠️
fn returns_errors(input: u8) -> Result<String, Error> {
    match input {
        0 => Err(ErrorOne),
        1 => Err(ErrorTwo),
        _ => Ok("Looks fine to me".to_string()),
    }
}
```

它会告诉你。

```text
21  | fn returns_errors(input: u8) -> Result<String, Error> {
    |                                 ^^^^^^^^^^^^^^^^^^^^^ doesn't have a size known at compile-time
```

这并不奇怪，因为我们知道，一个trait可以作用于很多东西，而且它们各自有不同的大小。
