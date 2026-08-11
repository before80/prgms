+++
title = "3.5 生命周期省略"
date = 2026-08-06T17:08:00+08:00
weight = 15
type = "docs"
description = "生命周期省略规则"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 生命周期省略


> 原文链接: [https://doc.rust-lang.org/nomicon/lifetime-elision.html](https://doc.rust-lang.org/nomicon/lifetime-elision.html)


　　为使常见模式更易用，Rust 允许在函数签名中*省略*生命周期。

　　*生命周期位置*指类型中可写生命周期的任意位置：

```rust,ignore
&'a T
&'a mut T
T<'a>
```

　　生命周期位置可为「输入」或「输出」：

* 对 `fn` 定义、`fn` 类型及 trait `Fn`、`FnMut`、`FnOnce`，输入指形式参数的类型，输出指结果类型。故 `fn foo(s: &str) -> (&str, &str)` 在输入位置省略了一个生命周期，在输出位置省略了两个。注意 `fn` 方法定义的输入位置*不*包括方法 `impl` 头中的生命周期（默认方法的 trait 头也不包括）。

* 对 `impl` 头，所有类型都是输入。故 `impl Trait<&T> for Struct<&T>` 在输入位置省略了两个生命周期，而 `impl Struct<&T>` 省略了一个。

　　省略规则如下：

* 输入位置每个省略的生命周期成为各自不同的生命周期参数。

* 若恰有一个输入生命周期位置（无论是否省略），该生命周期赋给*所有*省略的输出生命周期。

* 若有多个输入生命周期位置，但其中之一是 `&self` 或 `&mut self`，则 `self` 的生命周期赋给*所有*省略的输出生命周期。

* 否则，省略输出生命周期是错误。

　　示例：

```rust,ignore
fn print(s: &str);                                      // 已省略
fn print<'a>(s: &'a str);                               // 展开后

fn debug(lvl: usize, s: &str);                          // 已省略
fn debug<'a>(lvl: usize, s: &'a str);                   // 展开后

fn substr(s: &str, until: usize) -> &str;               // 已省略
fn substr<'a>(s: &'a str, until: usize) -> &'a str;     // 展开后

fn get_str() -> &str;                                   // 非法

fn frob(s: &str, t: &str) -> &str;                      // 非法

fn get_mut(&mut self) -> &mut T;                        // 已省略
fn get_mut<'a>(&'a mut self) -> &'a mut T;              // 展开后

fn args<T: ToCStr>(&mut self, args: &[T]) -> &mut Command                  // 已省略
fn args<'a, 'b, T: ToCStr>(&'a mut self, args: &'b [T]) -> &'a mut Command // 展开后

fn new(buf: &mut [u8]) -> BufWriter;                    // 已省略
fn new(buf: &mut [u8]) -> BufWriter<'_>;                // 已省略（`rust_2018_idioms`）
fn new<'a>(buf: &'a mut [u8]) -> BufWriter<'a>          // 展开后
```
