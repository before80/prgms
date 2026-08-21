+++
title = "05-作为输出参数"
date = 2026-08-20T21:20:00+08:00
weight = 62
type = "docs"
description = "作为输出参数 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/fn/closures/output_parameters.html](https://doc.rust-lang.org/stable/rust-by-example/fn/closures/output_parameters.html)

# 作为输出参数

闭包作为输入参数是可能的，所以返回闭包作为输出参数（output parameter）也应该是可能的。然而返回闭包类型会有问题，因为目前 Rust 只支持返回具体（非泛型）的类型。按照定义，匿名的闭包的类型是未知的，所以只有使用`impl Trait`才能返回一个闭包。

返回闭包的有效特征是：

- `Fn`
- `FnMut`
- `FnOnce`

除此之外，还必须使用 `move` 关键字，它表明所有的捕获都是通过值进行的。这是必须的，因为在函数退出时，任何通过引用的捕获都被丢弃，在闭包中留下无效的引用。

```rust
fn create_fn() -> impl Fn() {
    let text = "Fn".to_owned();

    move || println!("This is a: {}", text)
}

fn create_fnmut() -> impl FnMut() {
    let text = "FnMut".to_owned();

    move || println!("This is a: {}", text)
}

fn create_fnonce() -> impl FnOnce() {
    let text = "FnOnce".to_owned();
    
    move || println!("This is a: {}", text)
}

fn main() {
    let fn_plain = create_fn();
    let mut fn_mut = create_fnmut();
    let fn_once = create_fnonce();

    fn_plain();
    fn_mut();
    fn_once();
}

```
### 参见： {#参见}

[`Fn`][fn], [`FnMut`][fnmut], [泛型][generics] 和 [impl Trait][impltrait].

[fn]: https://rustwiki.org/zh-CN/std/ops/trait.Fn.html
[fnmut]: https://rustwiki.org/zh-CN/std/ops/trait.FnMut.html
[generics]: ../../generics/
[impltrait]: ../../trait/06-impl-trait/