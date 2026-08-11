+++
title = "3.7 高阶 trait 约束（HRTB）"
date = 2026-08-06T17:08:00+08:00
weight = 17
type = "docs"
description = "高阶 trait 约束 for<'a>"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 高阶 trait 约束（HRTB）


> 原文链接: [https://doc.rust-lang.org/nomicon/hrtb.html](https://doc.rust-lang.org/nomicon/hrtb.html)


　　Rust 的 `Fn` trait 有点「魔法」。例如，我们可以写出如下代码：

```rust
struct Closure<F> {
    data: (u8, u16),
    func: F,
}

impl<F> Closure<F>
    where F: Fn(&(u8, u16)) -> &u8,
{
    fn call(&self) -> &u8 {
        (self.func)(&self.data)
    }
}

fn do_it(data: &(u8, u16)) -> &u8 { &data.0 }

fn main() {
    let clo = Closure { data: (0, 1), func: do_it };
    println!("{}", clo.call());
}
```

　　若我们像[生命周期章节][lt]那样天真地脱糖这段代码，就会遇到麻烦：

```rust,ignore
// 注意：`&'b data.0` 和 `'x: {` 不是合法语法！
struct Closure<F> {
    data: (u8, u16),
    func: F,
}

impl<F> Closure<F>
    // where F: Fn(&'??? (u8, u16)) -> &'??? u8,
{
    fn call<'a>(&'a self) -> &'a u8 {
        (self.func)(&self.data)
    }
}

fn do_it<'b>(data: &'b (u8, u16)) -> &'b u8 { &'b data.0 }

fn main() {
    'x: {
        let clo = Closure { data: (0, 1), func: do_it };
        println!("{}", clo.call());
    }
}
```

　　我们究竟该如何表达 `F` 的 trait 约束上的生命周期？那里必须提供某个生命周期，但我们关心的生命周期在进入 `call` 函数体之前无法命名！而且，那也不是某个固定的生命周期；`call` 适用于 `&self` 在调用点*任意*具有的生命周期。

　　这项工作需要高阶 trait 约束（Higher-Rank Trait Bounds，HRTB）的魔法。脱糖方式如下：

```rust,ignore
where for<'a> F: Fn(&'a (u8, u16)) -> &'a u8,
```

　　或者：

```rust,ignore
where F: for<'a> Fn(&'a (u8, u16)) -> &'a u8,
```

　　（其中 `Fn(a, b, c) -> d` 本身只是不稳定版「真正」`Fn` trait 的语法糖。）

　　`for<'a>` 可读作「对 `'a` 的所有选择」，本质上产生 F 必须满足的*无限列表*的 trait 约束。很激烈。在 `Fn` trait 之外，我们很少遇到 HRTB；即便遇到，常见情形也有便捷的语法糖。

　　总之，我们可以把原始代码更明确地改写为：

```rust
struct Closure<F> {
    data: (u8, u16),
    func: F,
}

impl<F> Closure<F>
    where for<'a> F: Fn(&'a (u8, u16)) -> &'a u8,
{
    fn call(&self) -> &u8 {
        (self.func)(&self.data)
    }
}

fn do_it(data: &(u8, u16)) -> &u8 { &data.0 }

fn main() {
    let clo = Closure { data: (0, 1), func: do_it };
    println!("{}", clo.call());
}
```

[lt]: ./03-lifetimes.html
