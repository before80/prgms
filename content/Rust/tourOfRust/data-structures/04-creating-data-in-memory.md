+++
title = "04-在内存中创建数据"
date = 2026-08-17T22:00:00+08:00
weight = 28
type = "docs"
description = "在内存中创建数据 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/26_zh-cn.html](https://tourofrust.com/26_zh-cn.html)

# 在内存中创建数据

当我们在代码中**实例化**一个**结构体**时，我们的程序会在内存中并排创建关联的字段数据。

当我们通过制定所有字段值的方式来实例化时：

`结构体名 { ... }`.

结构体字段可以通过 `.` 运算符来获取。

我们例子的内存详情：
* 引号内的文本是只读数据（例如“ferris”），因此它位于*数据内存区*。
* 函数调用 `String::from` 创建一个结构体 `String`，该结构体与 SeaCreature 的字段并排放置在*栈*中。
  字符串容器通过如下步骤表示可更改的文本：
    1. 在*堆*上创建可修改文本的内存。
    2. 将*堆*中存储对象的内存位置的引用存储在 `String` 结构体中（在以后的课程中会详细介绍）。
* 最后，我们的两个朋友 *Ferris* 和 *Sarah* 有在程序中总是固定的位置的数据结构，所以它们被放在*栈*上。

## 示例代码

```rust
struct SeaCreature {
    animal_type: String,
    name: String,
    arms: i32,
    legs: i32,
    weapon: String,
}

fn main() {
    // SeaCreature的数据在栈上
    let ferris = SeaCreature {
        // String 结构体也在栈上，
        // 但也存放了一个数据在堆上的引用
        animal_type: String::from("螃蟹"),
        name: String::from("Ferris"),
        arms: 2,
        legs: 4,
        weapon: String::from("大钳子"),
    };

    let sarah = SeaCreature {
        animal_type: String::from("章鱼"),
        name: String::from("Sarah"),
        arms: 8,
        legs: 0,
        weapon: String::from("无"),
    };
    
    println!(
        "{} 是只{}。它有 {} 只胳膊 {} 条腿，还有一个{}。",
        ferris.name, ferris.animal_type, ferris.arms, ferris.legs, ferris.weapon
    );
    println!(
        "{} 是只{}。它有 {} 只胳膊 {} 条腿。它没有杀伤性武器…",
        sarah.name, sarah.animal_type, sarah.arms, sarah.legs
    );
}
```
