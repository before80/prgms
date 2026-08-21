+++
title = "02-返回值 result 和 ?"
date = 2026-08-12T20:00:00+08:00
weight = 41
type = "docs"
description = "返回值 result 和 ? — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/result-panic/result.html](https://practice-rust-zh.beatai.org/result-panic/result.html)

# 返回值 result 和 ?
`Result<T>` 是一个枚举类型用于描述返回的结果或错误，它包含两个成员(变体 variants) :

- `Ok(T)`: 返回一个结果值 T
- `Err(e)`: 返回一个错误，`e` 是具体的错误值

简而言之，如果期待一个正确的结果，就返回 `Ok`，反之则是 `Err`。


1. 🌟🌟
```rust

// 填空并修复错误
use std::num::ParseIntError;

fn multiply(n1_str: &str, n2_str: &str) -> __ {
    let n1 = n1_str.parse::<i32>();
    let n2 = n2_str.parse::<i32>();
    Ok(n1.unwrap() * n2.unwrap())
}

fn main() {
    let result = multiply("10", "2");
    assert_eq!(result, __);

    let result = multiply("t", "2");
    assert_eq!(result.__, 8);

    println!("Success!")
}
```

### ? 
`?` 跟 `unwrap` 非常像，但是 `?` 会返回一个错误，而不是直接 panic.

2. 🌟🌟
```rust

use std::num::ParseIntError;

// 使用 `?` 来实现 multiply
// 不要使用 unwrap !
fn multiply(n1_str: &str, n2_str: &str) -> __ {
}

fn main() {
    assert_eq!(multiply("3", "4").unwrap(), 12);
    println!("Success!")
}
```

3. 🌟🌟
```rust

use std::fs::File;
use std::io::{self, Read};

fn read_file1() -> Result<String, io::Error> {
    let f = File::open("hello.txt");
    let mut f = match f {
        Ok(file) => file,
        Err(e) => return Err(e),
    };

    let mut s = String::new();
    match f.read_to_string(&mut s) {
        Ok(_) => Ok(s),
        Err(e) => Err(e),
    }
}

// 填空
// 不要修改其它代码
fn read_file2() -> Result<String, io::Error> {
    let mut s = String::new();

    __;

    Ok(s)
}

fn main() {
    assert_eq!(read_file1().unwrap_err().to_string(), read_file2().unwrap_err().to_string());
    println!("Success!")
}
```

### map & and_then
[map](https://doc.rust-lang.org/stable/std/result/enum.Result.html#method.map) and [and_then](https://doc.rust-lang.org/stable/std/result/enum.Result.html#method.and_then) 是两个常用的组合器( combinator )，可以用于 `Result<T, E>` (也可用于 `Option<T>`).

4. 🌟🌟 

```rust
use std::num::ParseIntError;

// 使用两种方式填空: map, and then
fn add_two(n_str: &str) -> Result<i32, ParseIntError> {
   n_str.parse::<i32>().__
}

fn main() {
    assert_eq!(add_two("4").unwrap(), 6);

    println!("Success!")
}
```

5. 🌟🌟🌟
```rust
use std::num::ParseIntError;

// 使用 Result 重写后，我们使用模式匹配的方式来处理，而无需使用 `unwrap`
// 但是这种写法实在过于啰嗦..
fn multiply(n1_str: &str, n2_str: &str) -> Result<i32, ParseIntError> {
    match n1_str.parse::<i32>() {
        Ok(n1)  => {
            match n2_str.parse::<i32>() {
                Ok(n2)  => {
                    Ok(n1 * n2)
                },
                Err(e) => Err(e),
            }
        },
        Err(e) => Err(e),
    }
}

// 重写上面的 `multiply` ，让它尽量简洁
// 提示：使用 `and_then` 和 `map`
fn multiply1(n1_str: &str, n2_str: &str) -> Result<i32, ParseIntError> {
    // 实现...
}

fn print(result: Result<i32, ParseIntError>) {
    match result {
        Ok(n)  => println!("n is {}", n),
        Err(e) => println!("Error: {}", e),
    }
}

fn main() {
    let twenty = multiply1("10", "2");
    print(twenty);

    // 下面的调用会提供更有帮助的错误信息
    let tt = multiply("t", "2");
    print(tt);

    println!("Success!")
}
```

### 类型别名
如果我们要在代码中到处使用 `std::result::Result<T, ParseIntError>` ，那毫无疑问，代码将变得特别冗长和啰嗦，对于这种情况，可以使用类型别名来解决。

例如在标准库中，就在大量使用这种方式来简化代码: [`io::Result`](https://doc.rust-lang.org/std/io/type.Result.html).

6. 🌟
```rust
use std::num::ParseIntError;

// 填空
type __;

// 使用上面的别名来引用原来的 `Result` 类型
fn multiply(first_number_str: &str, second_number_str: &str) -> Res<i32> {
    first_number_str.parse::<i32>().and_then(|first_number| {
        second_number_str.parse::<i32>().map(|second_number| first_number * second_number)
    })
}

// 同样, 这里也使用了类型别名来简化代码
fn print(result: Res<i32>) {
    match result {
        Ok(n)  => println!("n is {}", n),
        Err(e) => println!("Error: {}", e),
    }
}

fn main() {
    print(multiply("10", "2"));
    print(multiply("t", "2"));

    println!("Success!")
}
```

### 在 `fn main` 中使用 `Result`
一个典型的 `main` 函数长这样: 
```rust
fn main() {
    println!("Hello World!");
}
```
事实上 `main` 函数还可以返回一个 `Result` 类型：如果 `main` 函数内部发生了错误，那该错误会被返回并且打印出一条错误的 debug 信息。

```rust

use std::num::ParseIntError;

fn main() -> Result<(), ParseIntError> {
    let number_str = "10";
    let number = match number_str.parse::<i32>() {
        Ok(number)  => number,
        Err(e) => return Err(e),
    };
    println!("{}", number);
    Ok(())
}
```
> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/result-panic/result.md)找到答案(在 solutions 路径下)
