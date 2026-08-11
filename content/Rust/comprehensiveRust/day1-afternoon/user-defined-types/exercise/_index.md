+++
title = "4.7 练习：电梯事件"
date = 2026-08-11T11:30:00+08:00
weight = 61
type = "docs"
description = "练习：电梯事件 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/user-defined-types/exercise.html](https://google.github.io/comprehensive-rust/user-defined-types/exercise.html)

# 4.7 练习：电梯事件

我们将创建一个数据结构，表示电梯控制系统中的事件。由你来定义类型与函数，以构造各种事件。请使用 `#[derive(Debug)]`，以便这些类型能用 `{:?}` 格式化。

本练习只要求创建并填充数据结构，使 `main` 能无错误运行。课程下一部分会讲解如何从这些结构中取出数据。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#![allow(dead_code)]

#[derive(Debug)]
/// 电梯系统中控制器必须响应的事件。
enum Event {
    // TODO: 添加所需变体
}

/// 行进方向。
#[derive(Debug)]
enum Direction {
    Up,
    Down,
}

/// 轿厢已到达指定楼层。
fn car_arrived(floor: i32) -> Event {
    todo!()
}

/// 轿厢门已打开。
fn car_door_opened() -> Event {
    todo!()
}

/// 轿厢门已关闭。
fn car_door_closed() -> Event {
    todo!()
}

/// 某楼层电梯厅按下了方向按钮。
fn lobby_call_button_pressed(floor: i32, dir: Direction) -> Event {
    todo!()
}

/// 轿厢内按下了楼层按钮。
fn car_floor_button_pressed(floor: i32) -> Event {
    todo!()
}

fn main() {
    println!(
        "A ground floor passenger has pressed the up button: {:?}",
        lobby_call_button_pressed(0, Direction::Up)
    );
    println!("The car has arrived on the ground floor: {:?}", car_arrived(0));
    println!("The car door opened: {:?}", car_door_opened());
    println!(
        "A passenger has pressed the 3rd floor button: {:?}",
        car_floor_button_pressed(3)
    );
    println!("The car door closed: {:?}", car_door_closed());
    println!("The car has arrived on the 3rd floor: {:?}", car_arrived(3));
}
```

> - 若学员问起练习顶部的 `#![allow(dead_code)]`：因为我们对 `Event` 类型做的唯一事情就是打印它。由于编译器检查死代码的细微之处，这会让它认为代码未被使用。就本练习而言可以忽略。

