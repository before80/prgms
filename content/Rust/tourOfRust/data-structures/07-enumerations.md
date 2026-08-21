+++
title = "07-枚举"
date = 2026-08-17T22:00:00+08:00
weight = 31
type = "docs"
description = "枚举 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/29_zh-cn.html](https://tourofrust.com/29_zh-cn.html)

# 枚举

枚举允许你使用 `enum` 关键字创建一个新类型，该类型的值可以包含几个带标记的元素。

`match` 有助于确保对所有可能的枚举值进行彻底的处理，使其成为确保高质量代码的强大工具。

## 示例代码

```rust
#![allow(dead_code)] // this line prevents compiler warnings

enum Species {
    Crab,
    Octopus,
    Fish,
    Clam
}

struct SeaCreature {
    species: Species,
    name: String,
    arms: i32,
    legs: i32,
    weapon: String,
}

fn main() {
    let ferris = SeaCreature {
        species: Species::Crab,
        name: String::from("Ferris"),
        arms: 2,
        legs: 4,
        weapon: String::from("claw"),
    };

    match ferris.species {
        Species::Crab => println!("{} is a crab",ferris.name),
        Species::Octopus => println!("{} is a octopus",ferris.name),
        Species::Fish => println!("{} is a fish",ferris.name),
        Species::Clam => println!("{} is a clam",ferris.name),
    }
}
```
