+++
title = "4.7.1 参考答案"
date = 2026-08-11T11:30:00+08:00
weight = 62
type = "docs"
description = "01-参考答案 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/user-defined-types/solution.html](https://google.github.io/comprehensive-rust/user-defined-types/solution.html)

# 4.7.1 参考答案

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#![allow(dead_code)]

#[derive(Debug)]
/// 电梯系统中控制器必须响应的事件。
enum Event {
    /// 按下了某个按钮。
    ButtonPressed(Button),

    /// 轿厢已到达指定楼层。
    CarArrived(Floor),

    /// 轿厢门已打开。
    CarDoorOpened,

    /// 轿厢门已关闭。
    CarDoorClosed,
}

/// 楼层用整数表示。
type Floor = i32;

/// 行进方向。
#[derive(Debug)]
enum Direction {
    Up,
    Down,
}

/// 用户可操作的按钮。
#[derive(Debug)]
enum Button {
    /// 指定楼层电梯厅中的按钮。
    LobbyCall(Direction, Floor),

    /// 轿厢内的楼层按钮。
    CarFloor(Floor),
}

/// 轿厢已到达指定楼层。
fn car_arrived(floor: i32) -> Event {
    Event::CarArrived(floor)
}

/// 轿厢门已打开。
fn car_door_opened() -> Event {
    Event::CarDoorOpened
}

/// 轿厢门已关闭。
fn car_door_closed() -> Event {
    Event::CarDoorClosed
}

/// 某楼层电梯厅按下了方向按钮。
fn lobby_call_button_pressed(floor: i32, dir: Direction) -> Event {
    Event::ButtonPressed(Button::LobbyCall(dir, floor))
}

/// 轿厢内按下了楼层按钮。
fn car_floor_button_pressed(floor: i32) -> Event {
    Event::ButtonPressed(Button::CarFloor(floor))
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

- **带数据的枚举：** Rust 的 `enum` 变体可以携带数据。`CarArrived(Floor)` 携带一个整数，`ButtonPressed(Button)` 携带嵌套的 `Button` 枚举。这让 `Event` 能以类型安全的方式表示丰富的状态集合。
- **类型别名：** `type Floor = i32` 为 `i32` 起了语义化名称。这能提高可读性，但对编译器而言 `Floor` 仍然只是 `i32`。
- **`#[derive(Debug)]`：** 我们用该属性自动生成代码，以便用 `{:?}` 打印枚举。没有它，就得手动实现 `fmt::Debug` trait。
- **嵌套枚举：** `Button` 枚举嵌在 `Event::ButtonPressed` 中。这种层级结构在 Rust 中很常见，用于为复杂领域建模。

> - 注意：`Event::CarDoorOpened` 是「单元变体」（不携带数据），而 `Event::CarArrived` 是「元组变体」。
> - 可以讨论为何把 `Button` 做成独立枚举，而不是在 `Event` 上直接放 `LobbyCallButtonPressed` 与 `CarFloorButtonPressed` 变体。两种做法都合理，但把相关概念（如按钮）分组通常能让代码更清晰。

