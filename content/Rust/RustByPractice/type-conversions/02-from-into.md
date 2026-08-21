+++
title = "02-From/Into"
date = 2026-08-12T20:00:00+08:00
weight = 37
type = "docs"
description = "From/Into — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/type-conversions/from-into.html](https://practice-rust-zh.beatai.org/type-conversions/from-into.html)

# From/Into
`From` 特征允许让一个类型定义如何基于另一个类型来创建自己，因此它提供了一个很方便的类型转换的方式。

`From` 和 `Into` 是配对的，我们只要实现了前者，那后者就会自动被实现：只要实现了 `impl From<T> for U`， 就可以使用以下两个方法: `let u: U = U::from(T)` 和 `let u:U = T.into()`，前者由 `From` 特征提供，而后者由自动实现的 `Into` 特征提供。

需要注意的是，当使用 `into` 方法时，你需要进行显式地类型标注，因为编译器很可能无法帮我们推导出所需的类型。


来看一个例子，我们可以简单的将 `&str` 转换成 `String`
```rust
fn main() {
    let my_str = "hello";

    // 以下三个转换都依赖于一个事实：String 实现了 From<&str> 特征
    let string1 = String::from(my_str);
    let string2 = my_str.to_string();
    // 这里需要显式地类型标注
    let string3: String = my_str.into();
}
```

这种转换可以发生是因为标准库已经帮我们实现了 `From` 特征： `impl From<&'_ str> for String`。你还可以在[这里](https://doc.rust-lang.org/stable/std/convert/trait.From.html#implementors))找到其它实现 `From` 特征的常用类型。


1. 🌟🌟🌟
```rust
fn main() {
    // impl From<bool> for i32
    let i1: i32 = false.into();
    let i2: i32 = i32::from(false);
    assert_eq!(i1, i2);
    assert_eq!(i1, 0);

    // 使用两种方式修复错误
    // 1. 哪个类型实现 From 特征 : impl From<char> for ? , 你可以查看一下之前提到的文档，来找到合适的类型
    // 2. 上一章节中介绍过的某个关键字
    let i3: i32 = 'a'.into();

    // 使用两种方法来解决错误
    let s: String = 'a' as String;

    println!("Success!")
}
```

### 为自定义类型实现 `From` 特征
2. 🌟🌟
```rust
// From 被包含在 `std::prelude` 中，因此我们没必要手动将其引入到当前作用域来
// use std::convert::From;

#[derive(Debug)]
struct Number {
    value: i32,
}

impl From<i32> for Number {
    // 实现 `from` 方法
}

// 填空
fn main() {
    let num = __(30);
    assert_eq!(num.value, 30);

    let num: Number = __;
    assert_eq!(num.value, 30);

    println!("Success!")
}
```

3. 🌟🌟🌟 当执行错误处理时，为我们自定义的错误类型实现 `From` 特征是非常有用。这样就可以通过 `?` 自动将某个错误类型转换成我们自定义的错误类型
```rust
use std::fs;
use std::io;
use std::num;

enum CliError {
    IoError(io::Error),
    ParseError(num::ParseIntError),
}

impl From<io::Error> for CliError {
    // 实现 from 方法
}

impl From<num::ParseIntError> for CliError {
    // 实现 from 方法
}

fn open_and_parse_file(file_name: &str) -> Result<i32, CliError> {
    // ? 自动将 io::Error 转换成 CliError
    let contents = fs::read_to_string(&file_name)?;
    // num::ParseIntError -> CliError
    let num: i32 = contents.trim().parse()?;
    Ok(num)
}

fn main() {
    println!("Success!")
}
```


### TryFrom/TryInto
类似于 `From` 和 `Into`, `TryFrom` 和 `TryInto` 也是用于类型转换的泛型特征。

但是又与 `From/Into` 不同, `TryFrom` 和 `TryInto` 可以对转换后的失败进行处理，然后返回一个 `Result`。

4. 🌟🌟
```rust
// TryFrom 和 TryInto 也被包含在 `std::prelude` 中, 因此以下引入是没必要的
// use std::convert::TryInto;

fn main() {
    let n: i16 = 256;

    // Into 特征拥有一个方法`into`,
    // 因此 TryInto 有一个方法是 ?
    let n: u8 = match n.__() {
        Ok(n) => n,
        Err(e) => {
            println!("there is an error when converting: {:?}, but we catch it", e.to_string());
            0
        }
    };

    assert_eq!(n, __);

    println!("Success!")
}
```

5. 🌟🌟🌟
```rust
#[derive(Debug, PartialEq)]
struct EvenNum(i32);

impl TryFrom<i32> for EvenNum {
    type Error = ();

    // 实现 `try_from`
    fn try_from(value: i32) -> Result<Self, Self::Error> {
        if value % 2 == 0 {
            Ok(EvenNum(value))
        } else {
            Err(())
        }
    }
}

fn main() {
    assert_eq!(EvenNum::try_from(8), Ok(EvenNum(8)));
    assert_eq!(EvenNum::try_from(5), Err(()));

    // 填空
    let result: Result<EvenNum, ()> = 8i32.try_into();
    assert_eq!(result, __);
    let result: Result<EvenNum, ()> = 5i32.try_into();
    assert_eq!(result, __);

    println!("Success!")
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/type-conversions/from-into.md)找到答案(在 solutions 路径下) 
