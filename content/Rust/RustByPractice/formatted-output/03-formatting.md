+++
title = "03-格式化"
date = 2026-08-12T20:00:00+08:00
weight = 50
type = "docs"
description = "格式化 — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/formatted-output/formatting.html](https://practice-rust-zh.beatai.org/formatted-output/formatting.html)

# 格式化

## 位置参数

1.🌟🌟
```rust
/* 填空 */
fn main() {
    println!("{0}, this is {1}. {1}, this is {0}", "Alice", "Bob");// => Alice, this is Bob. Bob, this is Alice
    assert_eq!(format!("{1}{0}", 1, 2), __);
    assert_eq!(format!(__, 1, 2), "2112");
    println!("Success!");
}
```

## 具名参数

2.🌟🌟
```rust
fn main() {
    println!("{argument}", argument = "test"); // => "test"

    /* 填空 */
    assert_eq!(format!("{name}{}", 1, __), "21");
    assert_eq!(format!(__,a = "a", b = 'b', c = 3 ), "a 3 b");
    
    /* 修复错误 */
    // 具名参数必须放在其它参数后面
    println!("{abc} {1}", abc = "def", 2);

    println!("Success!")
}
```

## 字符串对齐

3.🌟🌟 默认情况下，通过空格来填充字符串
```rust
fn main() {
    // 下面两个都是通过 5 个空格来填充
    println!("Hello {:5}!", "x"); // =>  "Hello x    !"  
    println!("Hello {:1$}!", "x", 5); // =>  "Hello x    !"

    /* 填空 */
    assert_eq!(format!("Hello __!", 5, "x"), "Hello x    !");
    assert_eq!(format!("Hello __!", "x", width = 5), "Hello x    !");

    println!("Success!")
}
```

4.🌟🌟🌟 左对齐, 右对齐, 使用指定的字符填充
```rust
fn main() {
    // 左对齐
    println!("Hello {:<5}!", "x"); // => Hello x    !
    // 右对齐
    assert_eq!(format!("Hello __!", "x"), "Hello     x!");
    // 居中对齐
    assert_eq!(format!("Hello __!", "x"), "Hello   x  !");

    // 左对齐，并使用 `&` 填充
    assert_eq!(format!("Hello {:&<5}!", "x"), __);

    println!("Success!")
}
```

5.🌟🌟 我们还能使用 0 来填充数字
```rust
fn main() {
    println!("Hello {:5}!", 5); // => Hello     5!
    println!("Hello {:+}!", 5); // =>  Hello +5!
    println!("Hello {:05}!", 5); // => Hello 00005!
    println!("Hello {:05}!", -5); // => Hello -0005!

    /* 填空 */
    assert!(format!("{number:0>width$}", number=1, width=6) == __);
    
    println!("Success!")
}
```

## 精度
6.🌟🌟 浮点数精度
```rust

/* 填空 */
fn main() {
    let v = 3.1415926;

    println!("{:.1$}", v, 4); // same as {:.4} => 3.1416 

    assert_eq!(format!("__", v), "3.14");
    assert_eq!(format!("__", v), "+3.14");
    assert_eq!(format!("__", v), "3");

    println!("Success!")
}
```

7.🌟🌟🌟 字符串长度
```rust
fn main() {
    let s = "Hello, world!";

    println!("{0:.5}", s); // => Hello

    assert_eq!(format!("Hello __!", 3, "abcdefg"), "Hello abc!");

    println!("Success!")
}
```   

## 二进制, 八进制, 十六进制

- format!("{}", foo) -> "3735928559"
- format!("0x{:X}", foo) -> "0xDEADBEEF"
- format!("0o{:o}", foo) -> "0o33653337357"
  
8.🌟🌟
```rust
fn main() {
    assert_eq!(format!("__", 27), "0b11011");
    assert_eq!(format!("__", 27), "0o33");
    assert_eq!(format!("__", 27), "0x1b");
    assert_eq!(format!("__", 27), "0x1B");

    println!("{:x}!", 27); // 没有前缀的十六进制 => 1b

    println!("{:#010b}", 27); // 使用 0 来填充二进制，宽度为 10 => 0b00011011

    println!("Success!")
}
```

## 捕获环境中的值
9.🌟🌟🌟
```rust
fn get_person() -> String {
    String::from("sunface")
}

fn get_format() -> (usize, usize) {
    (4, 1)
}


fn main() {
    let person = get_person();
    println!("Hello, {person}!");

    let (width, precision) = get_format();
    let scores = [("sunface", 99.12), ("jack", 60.34)];
    /* 让下面的代码输出:
    sunface: 99.1
    jack: 60.3
    */
    for (name, score) in scores {
        println!("{name}: __");
    }
}
```


## Others

**Example**
```rust
fn main() {
    // 指数
    println!("{:2e}", 1000000000); // => 1e9
    println!("{:2E}", 1000000000); // => 1E9

    // 指针地址
    let v= vec![1, 2, 3];
    println!("{:p}", v.as_ptr()); // => 0x600002324050

    // 转义
    println!("Hello {{}}"); // => Hello {}
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/formatted-output/formatting.md)找到答案(在 solutions 路径下) 
