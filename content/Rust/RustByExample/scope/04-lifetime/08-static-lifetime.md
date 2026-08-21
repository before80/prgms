+++
title = "08-static"
date = 2026-08-20T21:20:00+08:00
weight = 118
type = "docs"
description = "static — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/scope/lifetime/static_lifetime.html](https://doc.rust-lang.org/stable/rust-by-example/scope/lifetime/static_lifetime.html)

# static

`'static` 生命周期是可能的生命周期中最长的，它会在整个程序运行的时期中存在。`'static` 生命周期也可被强制转换成一个更短的生命周期。有两种方式使变量拥有 `'static` 生命周期，它们都把数据保存在可执行文件的只读内存区：

- 使用 `static` 声明来产生常量（constant）。
- 产生一个拥有 `&'static str` 类型的 `string` 字面量。

看下面的例子，了解列举到的各个方法：

```rust
// 产生一个拥有 `'static` 生命周期的常量。
static NUM: i32 = 18;

// 返回一个指向 `NUM` 的引用，该引用不取 `NUM` 的 `'static` 生命周期，
// 而是被强制转换成和输入参数的一样。
fn coerce_static<'a>(_: &'a i32) -> &'a i32 {
    &NUM
}

fn main() {
    {
        // 产生一个 `string` 字面量并打印它：
        let static_string = "I'm in read-only memory";
        println!("static_string: {}", static_string);

        // 当 `static_string` 离开作用域时，该引用不能再使用，不过
        // 数据仍然存在于二进制文件里面。
    }

    {
        // 产生一个整型给 `coerce_static` 使用：
        let lifetime_num = 9;

        // 将对 `NUM` 的引用强制转换成 `lifetime_num` 的生命周期：
        let coerced_static = coerce_static(&lifetime_num);

        println!("coerced_static: {}", coerced_static);
    }

    println!("NUM: {} stays accessible!", NUM);
}
```
### 参见： {#参见}

[`'static` 常量][static_const]

[static_const]: ../../custom-types/03-constants/