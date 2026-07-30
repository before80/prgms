+++
title = "06-枚举和模式匹配"
date = 2026-07-28T14:49:00+08:00
weight = 60
type = "docs"
description = "枚举变体、Option 替代空值、match 与 if let 控制流精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第6章

# 枚举和模式匹配

**枚举**（enum）：列举类型所有可能 **变体**（variants），把含义与数据编码在一起。

## 枚举的定义

```rust
enum IpAddrKind {
    V4,
    V6,
}

let four = IpAddrKind::V4;
let six = IpAddrKind::V6;
```

- 变体在类型命名空间下：`IpAddrKind::V4`。

### 枚举值

变体可 **携带数据**，各变体类型/数量可不同：

```rust
enum IpAddr {
    V4(String),
    V6(String),
}

enum IpAddr {
    V4(u8, u8, u8, u8),
    V6(String),
}

enum Message {
    Quit,                       // 无数据
    Move { x: i32, y: i32 },    // 命名字段
    Write(String),              // 单个值
    ChangeColor(i32, i32, i32), // 多个值
}
```

- 变体名即 **构造函数**：`IpAddr::V4(String::from("127.0.0.1"))`。
- 比「enum + 外部 struct」更简洁；同一 enum 下所有变体是 **同一类型**。

枚举也可 `impl` 方法：

```rust
impl Message {
    fn call(&self) { /* ... */ }
}
```

### `Option` 枚举

Rust **无 null**；用 `Option<T>` 表示「有值 / 无值」：

```rust
enum Option<T> {
    None,
    Some(T),
}
```

- `Some`、`None` 在 prelude 中，无需前缀。
- `Option<T>` 与 `T` **是不同类型**，不能混用：

```rust
let x: i8 = 5;
let y: Option<i8> = Some(5);
// let sum = x + y;  // 编译错误：须先处理 Option
```

- 使用前必须显式处理 `None`，编译器强制，避免空指针类 bug。
- 常用方法见 [Option 文档](https://doc.rust-lang.org/std/option/enum.Option.html)。

## `match` 控制流结构

```rust
enum Coin {
    Penny, Nickel, Dime,
    Quarter(UsState),
}

fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter(state) => {
            println!("State quarter from {state:?}!");
            25
        }
    }
}
```

- `match` 值与 **模式** 比较，第一个匹配的分支执行。
- 分支代码是 **表达式**，整体 `match` 有返回值。
- 多行分支用 `{}`；分支后逗号可选。

### 绑定值的模式

```rust
Coin::Quarter(state) => { /* state 绑定到变体内 UsState */ }
```

### 匹配 `Option<T>`

```rust
fn plus_one(x: Option<i32>) -> Option<i32> {
    match x {
        None => None,
        Some(i) => Some(i + 1),
    }
}
```

- `Some(i)` 将内部值绑定到 `i`。

### 匹配是穷尽的

- 必须覆盖 **所有** 变体，否则编译错误（**exhaustive**）。
- 对 `Option` 忘记 `None` 会被编译器指出。

### 通配模式和 `_` 占位符

```rust
match dice {
    3 => add_fancy_hat(),
    7 => remove_fancy_hat(),
    other => move_player(other),  // 捕获其余值
}

match dice {
    3 => add_fancy_hat(),
    7 => remove_fancy_hat(),
    _ => reroll(),                // 匹配但不绑定
}

match dice {
    3 => add_fancy_hat(),
    7 => remove_fancy_hat(),
    _ => (),                      // 什么都不做
}
```

- 通配分支须放 **最后**。

## `if let` 和 `let else` 简洁控制流

### `if let`

只关心一种模式时，替代冗长 `match`：

```rust
let config_max = Some(3u8);
if let Some(max) = config_max {
    println!("The maximum is configured to be {max}");
}
```

- `if let 模式 = 表达式`：匹配则执行块，否则跳过。
- 可带 `else`，等价于 `match` 的 `_` 分支。
- 失去穷尽性检查，需自行保证覆盖场景。

### `let...else`

模式匹配则绑定到外层；不匹配则 **必须从函数返回**（走 `else`）：

```rust
let Some(max) = config_max else {
    return;  // 或 return default;
};
// 此处 max 已绑定，继续“愉快路径”
```

- 适合「有值继续、无值早退」；比嵌套 `if let` 更清晰。

## 总结

- Enum：变体可携带各异数据；`Option<T>` 替代 null
- `match`：穷尽匹配 + 绑定内部值
- `if let` / `let else`：单模式简写，权衡简洁与穷尽性
- Struct + Enum 是 Rust 自定义类型的两大基础
