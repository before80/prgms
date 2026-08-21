+++
title = "03-切片"
date = 2026-08-12T20:00:00+08:00
weight = 16
type = "docs"
description = "切片 — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/compound-types/slice.html](https://practice-rust-zh.beatai.org/compound-types/slice.html)

# 切片
切片跟数组相似，但是切片的长度无法在编译期得知，因此你无法直接使用切片类型。

1. 🌟🌟 这里, `[i32]` 和 `str` 都是切片类型，但是直接使用它们会造成编译错误，如下代码所示。为了解决，你需要使用切片的引用： `&[i32]`，`&str`。
```rust

// 修复代码中的错误，不要新增代码行!
fn main() {
    let arr = [1, 2, 3];
    let s1: &[i32] = &arr[0..2];

    // let s2: str = "hello, world" as str;
    let s2: &str = "hello, world";
}
```

一个切片引用占用了2个字大小的内存空间( 从现在开始，为了简洁性考虑，如无特殊原因，**我们统一使用切片来特指切片引用** )。 该切片的第一个字是指向数据的指针，第二个字是切片的长度。字的大小取决于处理器架构，例如在 `x86-64` 上，字的大小是 64 位也就是 8 个字节，那么一个切片引用就是 16 个字节大小。

切片( 引用 )可以用来借用数组的某个连续的部分，对应的签名是 `&[T]`，大家可以与数组的签名对比下 `[T; Length]`。

2. 🌟🌟🌟
```rust

fn main() {
    let arr: [char; 3] = ['中', '国', '人'];

    let slice = &arr[..2];
    
    // 修改数字 `8` 让代码工作
    // 小提示: 切片和数组不一样，它是引用。如果是数组的话，那下面的 `assert!` 将会通过： '中'和'国'是char类型，char类型是Unicode编码，大小固定为4字节，两个字符为8字节。
    // assert!(std::mem::size_of_val(&slice) == 8);
    assert!(std::mem::size_of_val(&slice) == 16);
}
```

3. 🌟🌟
```rust
fn main() {
    let arr: [i32; 5] = [1, 2, 3, 4, 5];
    // 填空让代码工作起来
    // let slice: __ = __;
    let slice: &[i32] = &arr[1..4];
    assert_eq!(slice, &[2, 3, 4]);
}
```

### 字符串切片
4. 🌟 
```rust

fn main() {
    let s = String::from("hello");

    let slice1 = &s[0..2];
    // 填空，不要再使用 0..2
    // let slice2 = &s[__];
    let slice2 = &s[..2];

    assert_eq!(slice1, slice2);
}
```

5. 🌟
```rust

fn main() {
    let s = "你好，世界";
    // 修改以下代码行，让代码工作起来
    // let slice = &s[0..2];
    let slice = &s[0..3];

    assert!(slice == "你");
}
```

6. 🌟🌟 `&String` 可以被隐式地转换成 `&str` 类型.
```rust

// 修复所有错误
fn main() {
    let mut s = String::from("hello world");

    // 这里, &s 是 `&String` 类型，但是 `first_character` 函数需要的是 `&str` 类型。
    // 尽管两个类型不一样，但是代码仍然可以工作，原因是 `&String` 会被隐式地转换成 `&str` 类型，如果大家想要知道更多，可以看看 Deref 章节: https://course.rs/advance/smart-pointer/deref.html
    let ch = first_character(&s);

    // s.clear(); // error!
    // println!("the first character is: {}", ch);

    println!("the first character is: {}", ch);    
    s.clear(); // error!
}
fn first_character(s: &str) -> &str {
    &s[..1]
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/compound-types/slice.md)找到答案(在 solutions 路径下) 
