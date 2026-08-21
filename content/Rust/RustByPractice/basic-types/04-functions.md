+++
title = "04-函数"
date = 2026-08-12T20:00:00+08:00
weight = 9
type = "docs"
description = "函数 — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/basic-types/functions.html](https://practice-rust-zh.beatai.org/basic-types/functions.html)

# 函数
1. 🌟🌟🌟
```rust

fn main() {
    // 不要修改下面两行代码!
    let (x, y) = (1, 2);
    let s = sum(x, y);

    assert_eq!(s, 3);
}

// fn sum(x, y: i32) {
//     x + y;
// }
fn sum(x: i32, y: i32) -> i32 {
    x + y
}
```


2. 🌟🌟
```rust
fn main() {
   print();
}

// 使用另一个类型来替代 i32
// fn print() -> i32 {
//    println!("hello,world");
// }
fn print() -> () {
    println!("hello,world");
}
```


3. 🌟🌟🌟

```rust
// 用两种方法求解
fn main() {
    never_return();
}

fn never_return() -> ! {
    // 实现这个函数，不要修改函数签名!
    panic!("I return nothing!")
}

// ---
fn main() {
    never_return();
}

use std::thread;
use std::time;

fn never_return() -> ! {
    // implement this function, don't modify fn signatures
    loop {
        println!("I return nothing");
        // sleeping for 1 second to avoid exhausting the cpu resource
        thread::sleep(time::Duration::from_secs(1))
    }
}
```

4. 🌟🌟 发散函数( Diverging function )不会返回任何值，因此它们可以用于替代需要返回任何值的地方
```rust

fn main() {
    println!("Success!");
}

fn get_option(tp: u8) -> Option<i32> {
    match tp {
        1 => {
            // TODO
        }
        _ => {
            // TODO
        }
    };
    
    // 这里与其返回一个 None，不如使用发散函数替代
    never_return_fn()
}

// 使用三种方法实现以下发散函数
fn never_return_fn() -> ! {
    unimplemented!()
}

fn never_return_fn() -> ! {
    panic!()
}

fn never_return_fn() -> ! {
    todo!();
}

fn never_return_fn() -> ! {
    loop {
        std::thread::sleep(std::time::Duration::from_secs(1))
    }
}

```

5. 🌟🌟
```rust

fn main() {
    // 填空
    // let b = __;
    let b = false;
    let _v = match b {
        true => 1,
        // 发散函数也可以用于 `match` 表达式，用于替代任何类型的值
        false => {
            println!("Success!");
            panic!("we have no value for `false`, but we can panic")
        }
    };

    println!("Exercise Failed if printing out this line!");
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/basic-types/functions.md)找到答案(在 solutions 路径下) 
