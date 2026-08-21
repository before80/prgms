+++
title = "03-`cfg`"
date = 2026-08-20T21:20:00+08:00
weight = 85
type = "docs"
description = "`cfg` — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/attribute/cfg.html](https://doc.rust-lang.org/stable/rust-by-example/attribute/cfg.html)

# `cfg`

条件编译可能通过两种不同的操作符实现：

* `cfg` 属性：在属性位置中使用 `#[cfg(...)]`
* `cfg!` 宏：在布尔表达式中使用 `cfg!(...)`

两种形式使用的参数语法都相同。

```rust
// 这个函数仅当目标系统是 Linux 的时候才会编译
#[cfg(target_os = "linux")]
fn are_you_on_linux() {
    println!("You are running linux!")
}

// 而这个函数仅当目标系统 **不是** Linux 时才会编译
#[cfg(not(target_os = "linux"))]
fn are_you_on_linux() {
    println!("You are *not* running linux!")
}

fn main() {
    are_you_on_linux();
    
    println!("Are you sure?");
    if cfg!(target_os = "linux") {
        println!("Yes. It's definitely linux!");
    } else {
        println!("Yes. It's definitely *not* linux!");
    }
}
```
### 参见： {#参见}

[引用][ref], [`cfg!`][cfg], 和 [宏][macros].

[cfg]: https://rustwiki.org/zh-CN/std/macro.cfg!.html
[macros]: ../../macros/
[ref]: https://rustwiki.org/zh-CN/reference/conditional-compilation.html
