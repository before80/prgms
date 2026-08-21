+++
title = "04-特征对象"
date = 2026-08-12T20:00:00+08:00
weight = 29
type = "docs"
description = "特征对象 — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/generics-traits/trait-object.html](https://practice-rust-zh.beatai.org/generics-traits/trait-object.html)

# 特征对象
在[特征练习中](https://practice.rs/generics-traits/traits.html#returning-types-that-implement-traits) 我们已经知道当函数返回多个类型时，`impl Trait` 是无法使用的。

对于数组而言，其中一个限制就是无法存储不同类型的元素，但是通过之前的学习，大家应该知道枚举可以在部分场景解决这种问题，但是这种方法局限性较大。此时就需要我们的主角登场了。

## 使用 `dyn` 返回特征
Rust 编译器需要知道一个函数的返回类型占用多少内存空间。由于特征的不同实现类型可能会占用不同的内存，因此通过 `impl Trait` 返回多个类型是不被允许的，但是我们可以返回一个 `dyn` 特征对象来解决问题。


1. 🌟🌟🌟
```rust

trait Bird {
    fn quack(&self) -> String;
}

struct Duck;
impl Duck {
    fn swim(&self) {
        println!("Look, the duck is swimming")
    }
}
struct Swan;
impl Swan {
    fn fly(&self) {
        println!("Look, the duck.. oh sorry, the swan is flying")
    }
}

impl Bird for Duck {
    fn quack(&self) -> String{
        "duck duck".to_string()
    }
}

impl Bird for Swan {
    fn quack(&self) -> String{
        "swan swan".to_string()
    }
}

fn main() {
    // 填空
    let duck = __;
    duck.swim();

    let bird = hatch_a_bird(2);
    // 变成鸟儿后，它忘记了如何游，因此以下代码会报错
    // bird.swim();
    // 但它依然可以叫唤
    assert_eq!(bird.quack(), "duck duck");

    let bird = hatch_a_bird(1);
    // 这只鸟儿忘了如何飞翔，因此以下代码会报错
    // bird.fly();
    // 但它也可以叫唤
    assert_eq!(bird.quack(), "swan swan");

    println!("Success!")
}   

// 实现以下函数
fn hatch_a_bird...

```
## 在数组中使用特征对象
2. 🌟🌟
```rust
trait Bird {
    fn quack(&self);
}

struct Duck;
impl Duck {
    fn fly(&self) {
        println!("Look, the duck is flying")
    }
}
struct Swan;
impl Swan {
    fn fly(&self) {
        println!("Look, the duck.. oh sorry, the swan is flying")
    }
}

impl Bird for Duck {
    fn quack(&self) {
        println!("{}", "duck duck");
    }
}

impl Bird for Swan {
    fn quack(&self) {
        println!("{}", "swan swan");
    }
}

fn main() {
    // 填空
    let birds __;

    for bird in birds {
        bird.quack();
        // 当 duck 和 swan 变成 bird 后，它们都忘了如何翱翔于天际，只记得该怎么叫唤了。。
        // 因此，以下代码会报错
        // bird.fly();
    }
}
```


## `&dyn` and `Box<dyn>`

3. 🌟🌟
```rust

// 填空
trait Draw {
    fn draw(&self) -> String;
}

impl Draw for u8 {
    fn draw(&self) -> String {
        format!("u8: {}", *self)
    }
}

impl Draw for f64 {
    fn draw(&self) -> String {
        format!("f64: {}", *self)
    }
}

fn main() {
    let x = 1.1f64;
    let y = 8u8;

    // draw x
    draw_with_box(__);

    // draw y
    draw_with_ref(&y);

    println!("Success!")
}

fn draw_with_box(x: Box<dyn Draw>) {
    x.draw();
}

fn draw_with_ref(x: __) {
    x.draw();
}
```

## 静态分发和动态分发Static and Dynamic dispatch
关于这块内容的解析介绍，请参见 [Rust语言圣经](https://course.rs/basic/trait/trait-object.html#特征对象的动态分发)。

4. 🌟🌟
```rust

trait Foo {
    fn method(&self) -> String;
}

impl Foo for u8 {
    fn method(&self) -> String { format!("u8: {}", *self) }
}

impl Foo for String {
    fn method(&self) -> String { format!("string: {}", *self) }
}

// 通过泛型实现以下函数
fn static_dispatch...

// 通过特征对象实现以下函数
fn dynamic_dispatch...

fn main() {
    let x = 5u8;
    let y = "Hello".to_string();

    static_dispatch(x);
    dynamic_dispatch(&y);

    println!("Success!")
}
```

## 对象安全
一个特征能变成特征对象，首先该特征必须是对象安全的，即该特征的所有方法都必须拥有以下特点：

- 返回类型不能是 `Self`.
- 不能使用泛型参数

5. 🌟🌟🌟🌟
```rust

// 使用至少两种方法让代码工作
// 不要添加/删除任何代码行
trait MyTrait {
    fn f(&self) -> Self;
}

impl MyTrait for u32 {
    fn f(&self) -> Self { 42 }
}

impl MyTrait for String {
    fn f(&self) -> Self { self.clone() }
}

fn my_function(x: Box<dyn MyTrait>)  {
    x.f()
}

fn main() {
    my_function(Box::new(13_u32));
    my_function(Box::new(String::from("abc")));

    println!("Success!")
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/generics-traits/trait-object.md)找到答案(在 solutions 路径下) 
