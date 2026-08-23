+++
title = "01-Box"
date = 2026-08-12T20:00:00+08:00
weight = 60
type = "docs"
description = "Box — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust.beatai.org/smart-pointers/box.html](https://practice-rust.beatai.org/smart-pointers/box.html)

# Box

1. 🌟
```rust
// 让代码工作
fn main() {
    // 创建一个包含整数 5 的新 box `b`
    assert_eq!(*b, 5);

    println!("Success!");
}
```

2. 🌟
```rust

// 让代码工作
fn main() {
    let b = Box::new("Hello");
    print_boxed_string(b);
}

fn print_boxed_string(b : _) {
    println!("{}", b);
}
```

3. 🌟
```rust

// 让代码工作
fn main() {
    let b1 = Box::new(5);
    let b2 = b1;
    assert_eq!(_, 5);

    println!("Success!");
}
```

4. 🌟
```rust

// 让代码工作
fn main() {
    // 创建一个包含数组 [1, 2, 3, 4, 5] 的 box `b`
    // 打印 `b` 中的每个整数
}
```


> 你可以在[这里](https://github.com/sunface/rust-by-practice)找到答案（在 solutions 路径下），但请只在需要时使用
