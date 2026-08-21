+++
title = "31-泛型"
date = 2026-08-21T12:46:00+08:00
weight = 32
type = "docs"
description = "泛型 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_30.html](https://dhghomon.github.io/easy_rust/Chapter_30.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 泛型

在函数中，你要写出采取什么类型作为输入。

```rust
fn return_number(number: i32) -> i32 {
    println!("Here is your number.");
    number
}

fn main() {
    let number = return_number(5);
}
```

但是如果你想用的不仅仅是`i32`呢？你可以用泛型来解决。Generics的意思是 "也许是一种类型，也许是另一种类型"。

对于泛型，你可以使用角括号，里面加上类型，像这样。`<T>` 这意味着 "任何类型你都可以放入函数中" 通常情况下，generics使用一个大写字母的类型(T、U、V等)，尽管你不必只使用一个字母。

这就是你如何改变函数使其通用的方法。

```rust
fn return_number<T>(number: T) -> T {
    println!("Here is your number.");
    number
}

fn main() {
    let number = return_number(5);
}
```

重要的部分是函数名后的`<T>`。如果没有这个，Rust会认为T是一个具体的(具体的=不是通用的)类型。
 如`String`或`i8`。

如果我们写出一个类型名，这就更容易理解了。看看我们把 `T` 改成 `MyType` 会发生什么。

```rust
fn return_number(number: MyType) -> MyType { // ⚠️
    println!("Here is your number.");
    number
}
```

大家可以看到，`MyType`是具体的，不是通用的。所以我们需要写这个，所以现在就可以了。

```rust
fn return_number<MyType>(number: MyType) -> MyType {
    println!("Here is your number.");
    number
}

fn main() {
    let number = return_number(5);
}
```

所以单字母`T`是人的眼睛，但函数名后面的部分是编译器的 "眼睛"。没有了它，就不通用了。

现在我们再回到类型`T`，因为Rust代码通常使用`T`。

你会记得Rust中有些类型是**Copy**，有些是**Clone**，有些是**Display**，有些是**Debug**，等等。用**Debug**，我们可以用`{:?}`来打印。所以现在大家可以看到，我们如果要打印`T`就有问题了。

```rust
fn print_number<T>(number: T) {
    println!("Here is your number: {:?}", number); // ⚠️
}

fn main() {
    print_number(5);
}
```

`print_number`需要**Debug**打印`number`，但是`T`与`Debug`是一个类型吗？也许不是。也许它没有`#[derive(Debug)]`，谁知道呢？编译器也不知道，所以它给出了一个错误。

```text
error[E0277]: `T` doesn't implement `std::fmt::Debug`
  --> src\main.rs:29:43
   |
29 |     println!("Here is your number: {:?}", number);
   |                                           ^^^^^^ `T` cannot be formatted using `{:?}` because it doesn't implement `std::fmt::Debug`
```

T没有实现**Debug**。那么我们是否要为T实现Debug呢？不，因为我们不知道T是什么。但是我们可以告诉函数。"别担心，因为任何T类型的函数都会有Debug"

```rust
use std::fmt::Debug; // Debug 位于 std::fmt::Debug。现在可以直接写 'Debug'。

fn print_number<T: Debug>(number: T) { // <T: Debug> 是关键部分
    println!("Here is your number: {:?}", number);
}

fn main() {
    print_number(5);
}
```

所以现在编译器知道:"好的，这个类型T要有Debug"。现在代码工作了，因为`i32`有Debug。现在我们可以给它很多类型。`String`, `&str`, 等等，因为它们都有Debug.

现在我们可以创建一个结构，并用#[derive(Debug)]给它Debug，所以现在我们也可以打印它。我们的函数可以取`i32`，Animal结构等。

```rust
use std::fmt::Debug;

#[derive(Debug)]
struct Animal {
    name: String,
    age: u8,
}

fn print_item<T: Debug>(item: T) {
    println!("Here is your item: {:?}", item);
}

fn main() {
    let charlie = Animal {
        name: "Charlie".to_string(),
        age: 1,
    };

    let number = 55;

    print_item(charlie);
    print_item(number);
}
```

这个打印:

```text
Here is your item: Animal { name: "Charlie", age: 1 }
Here is your item: 55
```

有时候，我们在一个通用函数中需要不止一个类型。我们必须写出每个类型的名称，并考虑如何使用它。在这个例子中，我们想要两个类型。首先我们要打印一个类型为T的语句。用`{}`打印比较好，所以我们会要求用`Display`来打印`T`。

其次是类型U，`num_1`和`num_2`这两个变量的类型为U(U是某种数字)。我们想要比较它们，所以我们需要`PartialOrd`。这个特性让我们可以使用`<`、`>`、`==`等。我们也想打印它们，所以我们也需要`Display`来打印`U`。

```rust
use std::fmt::Display;
use std::cmp::PartialOrd;

fn compare_and_display<T: Display, U: Display + PartialOrd>(statement: T, num_1: U, num_2: U) {
    println!("{}! Is {} greater than {}? {}", statement, num_1, num_2, num_1 > num_2);
}

fn main() {
    compare_and_display("Listen up!", 9, 8);
}
```

这就打印出了`Listen up!! Is 9 greater than 8? true`。

所以`fn compare_and_display<T: Display, U: Display + PartialOrd>(statement: T, num_1: U, num_2: U)`说。

- 函数名称是`compare_and_display`,
- 第一个类型是T，它是通用的。它必须是一个可以用{}打印的类型。
- 下一个类型是U，它是通用的。它必须是一个可以用{}打印的类型。另外，它必须是一个可以比较的类型(使用 `>`、`<` 和 `==`)。

现在我们可以给`compare_and_display`不同的类型。`statement`可以是一个`String`，一个`&str`，任何有Display的类型。

为了让通用函数更容易读懂，我们也可以这样写，在代码块之前就写上`where`。

```rust
use std::cmp::PartialOrd;
use std::fmt::Display;

fn compare_and_display<T, U>(statement: T, num_1: U, num_2: U)
where
    T: Display,
    U: Display + PartialOrd,
{
    println!("{}! Is {} greater than {}? {}", statement, num_1, num_2, num_1 > num_2);
}

fn main() {
    compare_and_display("Listen up!", 9, 8);
}
```

当你有很多通用类型时，使用`where`是一个好主意。

还要注意。

- 如果你有一个类型T和另一个类型T，它们必须是相同的。
- 如果你有一个类型T和另一个类型U，它们可以是不同的。但它们也可以是相同的。

比如说

```rust
use std::fmt::Display;

fn say_two<T: Display, U: Display>(statement_1: T, statement_2: U) { // 类型 T 需要 Display，类型 U 也需要 Display
    println!("I have two things to say: {} and {}", statement_1, statement_2);
}

fn main() {

    say_two("Hello there!", String::from("I hate sand.")); // 类型 T 是 &str，类型 U 是 String。
    say_two(String::from("Where is Padme?"), String::from("Is she all right?")); // 两个类型都是 String。
}
```

这个打印:

```text
I have two things to say: Hello there! and I hate sand.
I have two things to say: Where is Padme? and Is she all right?
```
