+++
title = "04-元组"
date = 2026-08-12T20:00:00+08:00
weight = 17
type = "docs"
description = "元组 — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/compound-types/tuple.html](https://practice-rust-zh.beatai.org/compound-types/tuple.html)

# 元组
1. 🌟 元组中的元素可以是不同的类型。元组的类型签名是 `(T1, T2, ...)`, 这里 `T1`, `T2` 是相对应的元组成员的类型.
```rust
fn main() {
    let _t0: (u8,i16) = (0, -1);
    // 元组的成员还可以是一个元组
    let _t1: (u8, (i16, u32)) = (0, (-1, 1));
    // 填空让代码工作
    // let t: (u8, __, i64, __, __) = (1u8, 2u16, 3i64, "hello", String::from(", world"));
    let _t: (u8, u16, i64, &str, String) = (1u8, 2u16, 3i64, "hello", String::from(", world"));
}
```

2. 🌟 可以使用索引来获取元组的成员
```rust

// 修改合适的地方，让代码工作
fn main() {
    let t = ("i", "am", "sunface");
    // assert_eq!(t.1, "sunface");
    assert_eq!(t.2, "sunface");
}
```

3. 🌟 过长的元组无法被打印输出
```rust
// 修复代码错误
fn main() {
    // let too_long_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13);
    let too_long_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12);
    println!("too long tuple: {:?}", too_long_tuple);
}
```

4. 🌟 使用模式匹配来解构元组
```rust
fn main() {
    let tup = (1, 6.4, "hello");

    // 填空
    // let __ = tup;
    let (x,z,y) = tup;

    assert_eq!(x, 1);
    assert_eq!(y, "hello");
    assert_eq!(z, 6.4);
}
```

5. 🌟🌟 解构式赋值
```rust
fn main() {
    let (x, y, z);

    // 填空
    // __ = (1, 2, 3);
    (y, z, x) = (1, 2, 3);

    assert_eq!(x, 3);
    assert_eq!(y, 1);
    assert_eq!(z, 2);
}
```

6. 🌟🌟 元组可以用于函数的参数和返回值
```rust

fn main() {
    // 填空，需要稍微计算下
    // let (x, y) = sum_multiply(__);
    let (x, y) = sum_multiply((2,3));
    
    assert_eq!(x, 5);
    assert_eq!(y, 6);
}

fn sum_multiply(nums: (i32, i32)) -> (i32, i32) {
    (nums.0 + nums.1, nums.0 * nums.1)
}
```


> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/compound-types/tuple.md)找到答案(在 solutions 路径下) 
