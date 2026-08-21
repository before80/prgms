+++
title = "02-Debug 和 Display"
date = 2026-08-12T20:00:00+08:00
weight = 49
type = "docs"
description = "Debug 和 Display — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/formatted-output/debug-display.html](https://practice-rust-zh.beatai.org/formatted-output/debug-display.html)

# Debug 和 Display
想让类型可打印，需要实现 `std::fmt` 的格式化 trait：`std::fmt::Debug` 或 `std::fmt::Display`。

标准库内置类型会自动实现，其他类型需手动实现。

## Debug
`Debug` 很直接：几乎所有类型都能 `derive` 得到 `std::fmt::Debug`；`Display` 则必须手写实现。

实现了 `Debug` 的类型必须用 `{:?}` 占位符打印。

```rust
// 既不能 Display 也不能 Debug
struct UnPrintable(i32);

// 通过 derive 获取 Debug
#[derive(Debug)]
struct DebugPrintable(i32);
```

1. 🌟
```rust

/* 填空并修复错误 */
struct Structure(i32);

fn main() {
    // std 里的类型都已实现 fmt::Debug
    println!("__ months in a year.", 12);

    println!("Now __ will print!", Structure(3));
}
```

2. 🌟🌟 `fmt::Debug` 让类型可打印，但不够优雅；能否换个占位符（不是 `{}`）让输出更美观？
```rust
#[derive(Debug)]
struct Person {
    name: String,
    age: u8
}

fn main() {
    let person = Person { name:  "Sunface".to_string(), age: 18 };

    /* 让它输出:
    Person {
        name: "Sunface",
        age: 18,
    }
    */
    println!("{:?}", person);
}
```

3. 🌟🌟 也可以手写 `Debug` 实现
```rust

#[derive(Debug)]
struct Structure(i32);

#[derive(Debug)]
struct Deep(Structure);


fn main() {    
    // derive 没法控制输出格式，如果只想打印一个 `7` 呢？

    /* 让它输出: Now 7 will print! */
    println!("Now {:?} will print!", Deep(Structure(7)));
}
```

## Display
`Debug` 简单易用，但有时我们要自定义展示格式，这时就需要 `Display`。

`Display` 不能 derive，只能手写实现；占位符是 `{}` 而不是 `{:?}`。

4. 🌟🌟
```rust

/* 补全实现 */
use std::fmt;

struct Point2D {
    x: f64,
    y: f64,
}

impl fmt::Display for Point2D {
    /* 待实现... */
}

impl fmt::Debug for Point2D {
    /* 待实现... */
}

fn main() {
    let point = Point2D { x: 3.3, y: 7.2 };
    assert_eq!(format!("{}",point), "Display: 3.3 + 7.2i");
    assert_eq!(format!("{:?}",point), "Debug: Complex { real: 3.3, imag: 7.2 }");
    
    println!("Success!");
}
```


### `?` 运算符

为包含多个字段的结构体实现 `Display` 时，每个 `write!` 都返回 `fmt::Result`，需要在同一函数里处理。

`?` 运算符可以帮助我们简化这些错误处理。

5. 🌟🌟
```rust

/* 让它运行 */
use std::fmt; 

struct List(Vec<i32>);

impl fmt::Display for List {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // 取出内部的 vec
        let vec = &self.0;

        write!(f, "[")?;

        // 枚举迭代，得到索引 count 与值 v
        for (count, v) in vec.iter().enumerate() {
            // 不是第一个元素就加逗号
            if count != 0 { write!(f, ", ")?; }
            write!(f, "{}", v)?;
        }

        // 收尾
        write!(f, "]")
    }
}

fn main() {
    let v = List(vec![1, 2, 3]);
    assert_eq!(format!("{}",v), "[0: 1, 1: 2, 2: 3]");
    println!("Success!");
}
```


> 参考答案：<https://github.com/sunface/rust-by-practice/blob/master/solutions/formatted-output/debug-display.md>（solutions 路径），仅在需要时查看。
