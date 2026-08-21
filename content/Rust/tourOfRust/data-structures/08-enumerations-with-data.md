+++
title = "08-带数据的枚举"
date = 2026-08-17T22:00:00+08:00
weight = 32
type = "docs"
description = "带数据的枚举 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/30_zh-cn.html](https://tourofrust.com/30_zh-cn.html)

# 带数据的枚举

`enum` 的元素可以有一个或多个数据类型，从而使其表现得像 C 语言中的*联合*。

当使用 `match` 对一个 `enum` 进行模式匹配时，可以将变量名称绑定到每个数据值。

`enum` 的内存细节：
* 枚举数据的内存大小等于它最大元素的大小。此举是为了让所有可能的值都能存入相同的内存空间。
* 除了元素数据类型（如果有）之外，每个元素还有一个数字值，用于表示它是哪个标签。

其他细节：
* Rust 的 `enum` 也被称为*标签联合* （tagged-union）
* 把类型组合成一种新的类型，这就是人们所说的 Rust 具有 *代数类型* 的含义。

## 示例代码

```rust
#![allow(dead_code)] // this line prevents compiler warnings

enum Species { Crab, Octopus, Fish, Clam }
enum PoisonType { Acidic, Painful, Lethal }
enum Size { Big, Small }
enum Weapon {
    Claw(i32, Size),
    Poison(PoisonType),
    None
}

struct SeaCreature {
    species: Species,
    name: String,
    arms: i32,
    legs: i32,
    weapon: Weapon,
}

fn main() {
    // SeaCreature's data is on stack
    let ferris = SeaCreature {
        // String struct is also on stack,
        // but holds a reference to data on heap
        species: Species::Crab,
        name: String::from("Ferris"),
        arms: 2,
        legs: 4,
        weapon: Weapon::Claw(2, Size::Small),
    };

    match ferris.species {
        Species::Crab => {
            match ferris.weapon {
                Weapon::Claw(num_claws,size) => {
                    let size_description = match size {
                        Size::Big => "big",
                        Size::Small => "small"
                    };
                    println!("ferris is a crab with {} {} claws", num_claws, size_description)
                },
                _ => println!("ferris is a crab with some other weapon")
            }
        },
        _ => println!("ferris is some other animal"),
    }
}
```
