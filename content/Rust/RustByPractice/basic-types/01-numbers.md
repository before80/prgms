+++
title = "01-数值类型"
date = 2026-08-12T20:00:00+08:00
weight = 6
type = "docs"
description = "数值类型 — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/basic-types/numbers.html](https://practice-rust-zh.beatai.org/basic-types/numbers.html)

# 数值类型

### 整数

1. 🌟 

> Tips: 如果我们没有显式的给予变量一个类型，那编译器会自动帮我们推导一个类型

```rust

// 移除某个部分让代码工作
fn main() {
    let x: i32 = 5;
    let mut y: u32 = 5;

    y = x;
    
    let z = 10; // 这里 z 的类型是? i32
}
```

2. 🌟 
```rust

// 填空
fn main() {
    // let v: u16 = 38_u8 as __;
    let v: u16 = 38_u8 as u16;
}
```

3. 🌟🌟🌟 

> Tips: 如果我们没有显式的给予变量一个类型，那编译器会自动帮我们推导一个类型

```rust

// 修改 `assert_eq!` 让代码工作
fn main() {
    let x = 5;
    // assert_eq!("u32".to_string(), type_of(&x));
    assert_eq!("i32".to_string(), type_of(&x));
}

// 以下函数可以获取传入参数的类型，并返回类型的字符串形式，例如  "i8", "u8", "i32", "u32"
fn type_of<T>(_: &T) -> String {
    format!("{}", std::any::type_name::<T>())
}
```

4. 🌟🌟 
```rust

// 填空，让代码工作
fn main() {
    // assert_eq!(i8::MAX, __); 
    // assert_eq!(u8::MAX, __); 
    assert_eq!(i8::MAX, 127); 
    assert_eq!(u8::MAX, 255); 
}
```

5. 🌟🌟 
```rust

// 解决代码中的错误和 `panic`
fn main() {
   //let v1 = 251_u8 + 8;
   let v1 = 200_u8 + 8;
   // let v2 = i8::checked_add(251, 8).unwrap();
   let v2 = i8::checked_add(100, 8).unwrap();
   println!("{},{}",v1,v2);
}
```

6. 🌟🌟
```rust

// 修改 `assert!` 让代码工作
fn main() {
    let v = 1_024 + 0xff + 0o77 + 0b1111_1111;
    // 1024 + 255 + 63 + 255 = 1597
    // assert!(v == 1579);
    assert!(v == 1597);
}
```


### 浮点数
7. 🌟 

```rust

// 将 ? 替换成你的答案
fn main() {
    let x = 1_000.000_1; // ? => f64
    let y: f32 = 0.12; // f32
    let z = 0.01_f64; // f64
    
    assert_eq!(type_of(&x), "f64".to_string());
    println!("Success!");
}

fn type_of<T>(_: &T) -> String {
    format!("{}", std::any::type_name::<T>())
}
```
8. 🌟🌟 使用两种方法来让下面代码工作


```rust

fn main() {
    // ssert!(0.1+0.2==0.3);
    assert!(0.1_f32+0.2_f32 == 0.3_f32);
    
    assert!((0.1_f64+ 0.2 - 0.3).abs() < 0.001);
}
```

### 序列Range
9. 🌟🌟 两个目标: 1. 修改 `assert!` 让它工作 2. 让 `println!` 输出: 97 - 122

```rust
fn main() {
    let mut sum = 0;
    for i in -3..2 {
        sum += i
    }

    // assert!(sum == -3);
    assert!(sum == -5);

    for c in 'a'..='z' {
        // println!("{}",c);
        println!("{}",c as u8);
    }
}
```

10. 🌟🌟 
```rust

// 填空
use std::ops::{Range, RangeInclusive};
fn main() {
    // assert_eq!((1..__), Range{ start: 1, end: 5 });
    assert_eq!((1..5), Range{ start: 1, end: 5 });
    // assert_eq!((1..__), RangeInclusive::new(1, 5));
    assert_eq!((1..=5), RangeInclusive::new(1, 5));
}
```

### 计算

11. 🌟 
```rust

// 填空，并解决错误
fn main() {
    // 整数加法
    assert!(1u32 + 2 == 3);

    // 整数减法
    assert!(1i32 - 2 == -1);
    assert!(1i8 - 2 == -1);
    
    assert!(3 * 50 == 150);

    // assert!(9.6 / 3.2 == 3.0); // error ! 修改它让代码工作
    assert!(9 / 3 == 3);

    assert!(24 % 5 == 4);
    
    // 逻辑与或非操作
    assert!(true && false == false);
    assert!(true || false == true);
    assert!(!true == false);

    // 位操作
    println!("0011 AND 0101 is {:04b}", 0b0011u32 & 0b0101);
    println!("0011 OR 0101 is {:04b}", 0b0011u32 | 0b0101);
    println!("0011 XOR 0101 is {:04b}", 0b0011u32 ^ 0b0101);
    println!("1 << 5 is {}", 1u32 << 5);
    println!("0x80 >> 2 is 0x{:x}", 0x80u32 >> 2);
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/basic-types/numbers.md)找到答案(在 solutions 路径下) 
