+++
title = "3.1 方法"
date = 2026-08-11T11:30:00+08:00
weight = 77
type = "docs"
description = "01-方法 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/methods-and-traits/methods.html](https://google.github.io/comprehensive-rust/methods-and-traits/methods.html)

# 3.1 方法

Rust 允许把函数与你的新类型关联起来。做法是写一个 `impl` 块：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug)]
struct CarRace {
    name: String,
    laps: Vec<i32>,
}

impl CarRace {
    // 无接收者，静态方法
    fn new(name: &str) -> Self {
        Self { name: String::from(name), laps: Vec::new() }
    }

    // 对 self 的独占、可读写借用
    fn add_lap(&mut self, lap: i32) {
        self.laps.push(lap);
    }

    // 对 self 的共享、只读借用
    fn print_laps(&self) {
        println!("Recorded {} laps for {}:", self.laps.len(), self.name);
        for (idx, lap) in self.laps.iter().enumerate() {
            println!("Lap {idx}: {lap} sec");
        }
    }

    // 独占取得 self 的所有权（后面会讲）
    fn finish(self) {
        let total: i32 = self.laps.iter().sum();
        println!("Race {} is finished, total lap time: {}", self.name, total);
    }
}

fn main() {
    let mut race = CarRace::new("Monaco Grand Prix");
    race.add_lap(70);
    race.add_lap(68);
    race.print_laps();
    race.add_lap(71);
    race.print_laps();
    race.finish();
    // race.add_lap(42);
}
```

`self` 参数指定「接收者」——方法作用的对象。方法常见的几种接收者：

- `&self`：用共享、不可变引用从调用方借用对象。之后对象仍可继续使用。
- `&mut self`：用唯一、可变引用从调用方借用对象。之后对象仍可继续使用。
- `self`：取得对象所有权并从调用方移走。方法成为对象的所有者。方法返回时对象会被丢弃（释放），除非所有权被显式传递出去。完全所有权并不自动意味着可变。
- `mut self`：同上，但方法可以修改对象。
- 无接收者：成为结构体上的静态方法。通常用于按约定名为 `new` 的构造函数。

> 要点：
>
> - 通过与函数对比来介绍方法会很有帮助。
>   - 方法在类型实例（如结构体或枚举）上调用，第一个参数用 `self` 表示该实例。
>   - 开发者可能选用方法以利用接收者语法，并让代码更有条理。用方法可以把实现集中放在可预期的位置。
>   - 注意：也可以像关联函数那样显式传入接收者来调用方法，例如 `CarRace::add_lap(&mut race, 20)`。
> - 指出关键字 `self`，即方法接收者。
>   - 说明它是 `self: Self` 的简写，也可以演示如何写出结构体名称。
>   - 解释 `Self` 是 `impl` 块所在类型的别名，可在该块内其他地方使用。
>   - 注意 `self` 的用法与其他结构体类似，可用点号访问各个字段。
>   - 这可能是演示 `&self` 与 `self` 区别的好时机：试着调用两次 `finish`。
>   - 除了 `self` 的各种变体，还允许一些
>     [特殊包装类型](https://doc.rust-lang.org/reference/special-types-and-traits.html)
>     作为接收者类型，例如 `Box<Self>`。

