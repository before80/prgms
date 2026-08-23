+++
title = "03-Drop"
date = 2026-08-12T20:00:00+08:00
weight = 62
type = "docs"
description = "Drop — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust.beatai.org/smart-pointers/drop.html](https://practice-rust.beatai.org/smart-pointers/drop.html)

# Drop

`Drop` trait 允许我们在值离开作用域时自定义清理逻辑。Rust 会在变量离开作用域时自动调用 `drop`。

1. 🌟
```rust
// 让代码工作
struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self) {
        println!("Dropping CustomSmartPointer with data `{}`!", self.data);
    }
}

fn main() {
    let c = CustomSmartPointer {
        data: String::from("my stuff"),
    };
    println!("CustomSmartPointer created.");
    println!("About to leave main.");
    println!("Success!");
}
```

2. 🌟
```rust
// 让代码工作
struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self) {
        println!("Dropping `{}`", self.data);
    }
}

fn main() {
    let c = CustomSmartPointer {
        data: String::from("first"),
    };
    let d = CustomSmartPointer {
        data: String::from("second"),
    };
    println!("Created two pointers.");
    drop(c);
    println!("Dropped first pointer early.");
    println!("Success!");
}
```

3. 🌟🌟
```rust
// 填空
struct HasDrop(i32);

impl Drop for HasDrop {
    fn drop(&mut self) {
        println!("Dropped {}", self.0);
    }
}

fn main() {
    let a = HasDrop(1);
    let b = HasDrop(2);
    {
        let c = HasDrop(3);
        println!("inner scope");
    }
    println!("Success!");
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice)找到答案（在 solutions 路径下），但请只在需要时使用
