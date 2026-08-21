+++
title = "09-传递借用的数据"
date = 2026-08-17T22:00:00+08:00
weight = 53
type = "docs"
description = "传递借用的数据 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/51_zh-cn.html](https://tourofrust.com/51_zh-cn.html)

# 传递借用的数据

Rust 对于引用的规则也许最好用以下的方式总结：
* Rust 只允许同时存在一个可变引用**或者**多个不可变引用，**不允许可变引用和不可变引用同时存在**。
* 一个引用永远也不会比它的所有者存活得更久。

而在函数间进行引用的传递时，以上这些通常都不会成为问题。

内存细节：
* 上面的第一条规则避免了数据争用的出现。什么是数据争用？在对数据进行读取的时候，数据争用可能会因为同时存在对数据的写入而产生不同步。这一点往往会出现在多线程编程中。
* 而第二条引用规则则避免了通过引用而错误的访问到不存在的数据（在 C 语言中被称之为悬垂指针）。

## 示例代码

```rust
#[derive(Debug)]
struct Foo {
    x: i32,
}

fn do_something(f: &mut Foo) {
    f.x += 1;
    // 可变引用 f 在这里被 dropped 释放
}

fn main() {
    let mut foo = Foo { x: 42 };
    do_something(&mut foo);
    println!("{:?}", foo); //Foo { x: 43 }
    // 因为所有的可变引用都在 do_something 函数内部被释放了
    // 此时我们便可以再创建一个
    do_something(&mut foo);
    println!("{:?}", foo);//Foo { x: 44 }
    // foo 在这里被 dropped 释放
}
```
