+++
title = "10-打印 hello, world!"
date = 2026-08-21T12:46:00+08:00
weight = 11
type = "docs"
description = "打印 hello, world! — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_9.html](https://dhghomon.github.io/easy_rust/Chapter_9.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 打印 hello, world!

当你启动一个新的Rust程序时，它总是有这样的代码。

```rust
fn main() {
    println!("Hello, world!");
}
```

- `fn`的意思是函数。
- `main`是启动程序的函数。

- `()`表示我们没有给函数任何变量来启动。

`{}`被称为**代码块**。这是代码所在的空间。

`println!`是一个**宏**，打印到控制台。一个**宏**就像一个函数，为你写代码。宏后面有一个`!`。我们以后会学习如何创建宏。现在，请记住，`!`表示它是一个宏。

为了学习`;`，我们将创建另一个函数。首先，在`main`中，我们将打印一个数字8。

```rust
fn main() {
    println!("Hello, world number {}!", 8);
}
```

`println!`中的`{}`的意思是 "把变量放在这里面"。这样就会打印出`Hello, world number 8!`。


我们可以像之前一样，放更多的东西进去。

```rust
fn main() {
    println!("Hello, worlds number {} and {}!", 8, 9);
}
```

这将打印出 `Hello, worlds number 8 and 9!`。

现在我们来创建函数。

```rust
fn number() -> i32 {
    8
}

fn main() {
    println!("Hello, world number {}!", number());
}
```

这也会打印出 `Hello, world number 8!`。当Rust查看`number()`时，它看到一个函数。这个函数:

- 没有参数(因为它有`()`)
- 返回一个`i32`。`->`(称为 "瘦箭")显示了函数返回的内容

函数内部只有`8`。因为没有`;`，所以这就是它返回的值。如果它有一个`;`，它将不会返回任何东西(它会返回一个`()`)。如果它有 `;`，Rust 不会编译通过，因为需要返回的是 `i32`，而 `;` 返回 `()`，不是 `i32`。

```rust
fn main() {
    println!("Hello, world number {}", number());
}

fn number() -> i32 {
    8;  // ⚠️
}
```

```text
5 | fn number() -> i32 {
  |    ------      ^^^ expected `i32`, found `()`
  |    |
  |    implicitly returns `()` as its body has no tail or `return` expression
6 |     8;
  |      - help: consider removing this semicolon
```

这意味着 "你告诉我`number()`返回的是`i32`，但你加了一个`;`，所以它什么都不返回"。所以编译器建议去掉分号。

你也可以写`return 8;`，但在Rust中，正常情况下只需将`;`改为`return`即可。

当你想给一个函数赋予变量时，把它们放在`()`里面。你必须给它们起个名字，写上类型。

```rust
fn multiply(number_one: i32, number_two: i32) { // 两个 i32 会进入函数。我们叫它们 number_one 和 number_two。
    let result = number_one * number_two;
    println!("{} times {} is {}", number_one, number_two, result);
}

fn main() {
    multiply(8, 9); // 可以直接传入数字
    let some_number = 10; // 或者先声明两个变量
    let some_other_number = 2;
    multiply(some_number, some_other_number); // 再把它们传进函数
}
```

我们也可以返回一个`i32`。只要把最后的分号去掉就可以了:

```rust
fn multiply(number_one: i32, number_two: i32) -> i32 {
    let result = number_one * number_two;
    println!("{} times {} is {}", number_one, number_two, result);
    result // 这就是我们返回的 i32
}

fn main() {
    let multiply_result = multiply(8, 9); // 我们用 multiply() 既打印结果，又把结果赋给 multiply_result
}
```

## 声明变量和代码块

使用`let`声明一个变量(声明一个变量=告诉Rust创建一个变量)。

```rust
fn main() {
    let my_number = 8;
    println!("Hello, number {}", my_number);
}
```

变量在代码块`{}`内开始和结束。在这个例子中，`my_number`在我们调用`println!`之前结束，因为它在自己的代码块里面。

```rust
fn main() {
    {
        let my_number = 8; // my_number 从这里开始
                           // my_number 到这里结束！
    }

    println!("Hello, number {}", my_number); // ⚠️ 没有 my_number，
                                             // println!() 找不到它
}
```

你可以使用代码块来返回一个值。

```rust
fn main() {
    let my_number = {
    let second_number = 8;
        second_number + 9 // 没有分号，所以代码块返回 8 + 9。
                          // 就像函数一样
    };

    println!("My number is: {}", my_number);
}
```

如果在代码块内部添加分号，它将返回 `()` (无)。

```rust
fn main() {
    let my_number = {
    let second_number = 8; // 声明 second_number，
        second_number + 9; // 给 second_number 加 9
                           // 但我们没有返回它！
                           // second_number 现在销毁了
    };

    println!("My number is: {:?}", my_number); // my_number 是 ()
}
```

那么为什么我们要写`{:?}`而不是`{}`呢？我们现在就来谈谈这个问题。
