+++
title = "03-语句与表达式"
date = 2026-08-12T20:00:00+08:00
weight = 8
type = "docs"
description = "语句与表达式 — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/basic-types/statements-expressions.html](https://practice-rust-zh.beatai.org/basic-types/statements-expressions.html)

# 语句与表达式

### 示例
```rust
fn main() {
    let x = 5u32;

    let y = {
        let x_squared = x * x;
        let x_cube = x_squared * x;

        // 下面表达式的值将被赋给 `y`
        x_cube + x_squared + x
    };

    let z = {
        // 分号让表达式变成了语句，因此返回的不再是表达式 `2 * x` 的值，而是语句的值 `()`
        2 * x;
    };

    println!("x is {:?}", x);
    println!("y is {:?}", y);
    println!("z is {:?}", z);
}
```

### 练习
1. 🌟🌟
```rust
// 使用两种方法让代码工作起来
fn main() {
   let v = {
       let mut x = 1;
       x += 2
   };

   // assert_eq!(v, 3);
   assert_eq!(v, ());
}
```

2. 🌟
```rust

fn main() {
    // let v = (let x = 3);
    let v = {
        let x = 3;
        x
    };

    assert!(v == 3);
}
```

3. 🌟
```rust

fn main() {
    let s = sum(1 , 2);
    assert_eq!(s, 3);
}

fn sum(x: i32, y: i32) -> i32 {
	// x + y;
    x + y
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/basic-types/statements.md)找到答案(在 solutions 路径下) 
