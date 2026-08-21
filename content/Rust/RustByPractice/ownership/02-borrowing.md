+++
title = "02-引用和借用"
date = 2026-08-12T20:00:00+08:00
weight = 12
type = "docs"
description = "引用和借用 — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/ownership/borrowing.html](https://practice-rust-zh.beatai.org/ownership/borrowing.html)

# 引用和借用

### 引用
1. 🌟
```rust
fn main() {
    let x = 5;
    // 填写空白处
    // let p = __;
    let p = &x;

    println!("x 的内存地址是 {:p}", p); // output: 0x16fa3ac84 具体值不一定
}
```

2. 🌟
```rust
fn main() {
    let x = 5;
    let y = &x;

    // 只能修改以下行
    // assert_eq!(5, y);
    assert_eq!(5, *y);
}
```

3. 🌟
```rust
// 修复错误
fn main() {
    let mut s = String::from("hello, ");

    // borrow_object(s)
    borrow_object(&s)
}

fn borrow_object(s: &String) {}
```

4. 🌟
```rust

// 修复错误
fn main() {
    let mut s = String::from("hello, ");

    // push_str(s)
    push_str(&mut s)
}

fn push_str(s: &mut String) {
    s.push_str("world")
}
```

5. 🌟🌟
```rust
fn main() {
    let mut s = String::from("hello, ");

    // 填写空白处，让代码工作
    // let p = __;
    let p = &mut s;

    p.push_str("world");
    println!("{p}");//hello, world
    println!("{s}");//hello, world
}
```

#### ref
`ref` 与 `&` 类似，可以用来获取一个值的引用，但是它们的用法有所不同。

6. 🌟🌟🌟
```rust
fn main() {
    let c = '中';

    let r1 = &c;
    // 填写空白处，但是不要修改其它行的代码
    // let __ r2 = c;
    let ref r2 = c;

    assert_eq!(*r1, *r2);
    
    // 判断两个内存地址的字符串是否相等
    assert_eq!(get_addr(r1),get_addr(r2));
}

// 获取传入引用的内存地址的字符串形式
fn get_addr(r: &char) -> String {
    format!("{:p}", r)
}
```

### 借用规则
7. 🌟
```rust
// 移除代码某个部分，让它工作
// 你不能移除整行的代码！
fn main() {
    let mut s = String::from("hello");

    // let r1 = &mut s;
    let r1 = &s;
    // let r2 = &mut s;
    let r2 = &s;

    println!("{}, {}", r1, r2);
}
```

#### 可变性
8. 🌟 错误: 从不可变对象借用可变
```rust

fn main() {
    // 通过修改下面一行代码来修复错误
    // let s = String::from("hello, ");
    let mut s = String::from("hello, ");

    borrow_object(&mut s)
}

fn borrow_object(s: &mut String) {}
```

9. 🌟🌟 Ok: 从可变对象借用不可变
```rust

// 下面的代码没有任何错误
fn main() {
    let mut s = String::from("hello, ");

    borrow_object(&s);
    
    s.push_str("world");
}

fn borrow_object(s: &String) {}
```

### NLL
10. 🌟🌟
```rust

// 注释掉一行代码让它工作
fn main() {
    let mut s = String::from("hello, ");

    let r1 = &mut s;
    r1.push_str("world");
    let r2 = &mut s;
    r2.push_str("!");
    
    // println!("{}",r1);
}
```

11. 🌟🌟
```rust

fn main() {
    let mut s = String::from("hello, ");

    let r1 = &mut s;
    let r2 = &mut s;

    // 在下面增加一行代码, 人为制造编译错误：cannot borrow `s` as mutable more than once at a time
    // 你不能同时使用 r1 和 r2
    println!("{}", r1);
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/ownership/borrowing.md)找到答案(在 solutions 路径下) 
