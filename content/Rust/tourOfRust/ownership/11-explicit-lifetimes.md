+++
title = "11-显式生命周期"
date = 2026-08-17T22:00:00+08:00
weight = 55
type = "docs"
description = "显式生命周期 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/53_zh-cn.html](https://tourofrust.com/53_zh-cn.html)

# 显式生命周期

尽管 Rust 不总是在代码中将它展示出来，但编译器会理解每一个变量的生命周期并进行验证以确保一个引用不会有长于其所有者的存在时间。 同时，函数可以通过使用一些符号来参数化函数签名，以帮助界定哪些参数和返回值共享同一生命周期。 生命周期注解总是以 `'` 开头，例如 `'a`，`'b` 以及 `'c`。

## 示例代码

```rust
#[derive(Debug)]
struct Foo {
    x: i32,
}

// 参数 foo 和返回值共享同一生命周期
fn do_something<'a>(foo: &'a Foo) -> &'a i32 {
    return &foo.x;
}

fn main() {
    let mut foo = Foo { x: 42 };
    let x = &mut foo.x;
    *x = 13;
    // x 在这里被 dropped 释放从而允许我们再创建一个不可变引用
    let y = do_something(&foo);
    println!("{}", y); //13
    // y 在这里被 dropped 释放
    // foo 在这里被 dropped 释放
}
```
