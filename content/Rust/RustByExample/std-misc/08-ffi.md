+++
title = "08-外部语言函数接口"
date = 2026-08-20T21:20:00+08:00
weight = 186
type = "docs"
description = "外部语言函数接口 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/std_misc/ffi.html](https://doc.rust-lang.org/stable/rust-by-example/std_misc/ffi.html)

# 外部语言函数接口

Rust 提供了到 C 语言库的外部语言函数接口（Foreign Function Interface，FFI）。外部语言函数必须在一个 `extern` 代码块中声明，且该代码块要带有一个包含库名称的 `#[link]` 属性。

```rust
use std::fmt;

// 这个 extern 代码块链接到 libm 库
#[link(name = "m")]
extern {
    // 这个外部函数用于计算单精度复数的平方根
    fn csqrtf(z: Complex) -> Complex;

    // 这个用来计算单精度复数的复变余弦
    fn ccosf(z: Complex) -> Complex;
}

// 由于调用其他语言的函数被认为是不安全的，我们通常会给它们写一层安全的封装
fn cos(z: Complex) -> Complex {
    unsafe { ccosf(z) }
}

fn main() {
    // z = -1 + 0i
    let z = Complex { re: -1., im: 0. };

    // 调用外部语言函数是不安全操作
    let z_sqrt = unsafe { csqrtf(z) };

    println!("the square root of {:?} is {:?}", z, z_sqrt);

    // 调用不安全操作的安全的 API 封装
    println!("cos({:?}) = {:?}", z, cos(z));
}

// 单精度复数的最简实现
#[repr(C)]
#[derive(Clone, Copy)]
struct Complex {
    re: f32,
    im: f32,
}

impl fmt::Debug for Complex {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        if self.im < 0. {
            write!(f, "{}-{}i", self.re, -self.im)
        } else {
            write!(f, "{}+{}i", self.re, self.im)
        }
    }
}
```
