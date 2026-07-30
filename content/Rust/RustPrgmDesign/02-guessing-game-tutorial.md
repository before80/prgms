+++
title = "02-编写一个猜数字游戏"
date = 2026-07-28T14:49:00+08:00
weight = 20
type = "docs"
description = "猜数字实战：I/O、变量、Result、match、外部 crate 与循环"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第2章

# 编写一个猜数字游戏

规则：程序生成 1–100 随机数，用户猜，提示太大/太小，猜对退出。

## 准备一个新项目

```console
cargo new guessing_game
cd guessing_game
cargo run
```

## 处理一次猜测

### 使用变量储存值

```rust
use std::io;

fn main() {
    println!("Guess the number!");
    println!("Please input your guess.");

    let mut guess = String::new();  // mut = 可变；String::new() 关联函数

    io::stdin()
        .read_line(&mut guess)
        .expect("Failed to read line");

    println!("You guessed: {guess}");
}
```

- `let` 默认不可变；`let mut` 可变。
- `::new`：`String` 的 **关联函数**（不接收实例）。
- `&mut guess`：**引用**，允许多处访问同一数据；可变引用才能被 `read_line` 追加内容。

### 使用 `Result` 类型来处理潜在的错误

- `read_line` 返回 `Result<T, E>` 枚举：`Ok(T)` 成功，`Err(E)` 失败。
- `.expect("msg")`：`Err` 时 panic 并打印消息；生产代码应做 proper 错误处理（第9章）。

### 使用 `println!` 占位符打印值

```rust
let x = 5;
let y = 10;
println!("x = {x} and y + 2 = {}", y + 2);  // x = 5 and y + 2 = 12
```

## 生成一个秘密数字

### 使用 crate 来增加更多功能

- **二进制 crate**：可执行项目；**库 crate**：供他人使用的代码。
- 在 `Cargo.toml` 添加依赖：

```toml
[dependencies]
rand = "0.8.5"
```

- `0.8.5` 即 `^0.8.5`（SemVer）：≥0.8.5 且 <0.9.0。
- `cargo build` 从 [crates.io](https://crates.io/) 下载并编译依赖。

#### _Cargo.lock_ 文件确保可重现构建

- 首次构建写入 `Cargo.lock`，锁定具体版本；应提交到版本控制。
- `cargo update` 在 SemVer 约束内升级依赖。

### 生成一个随机数

```rust
use rand::Rng;

let secret_number = rand::thread_rng().gen_range(1..=100);
```

- `use rand::Rng`：trait 必须在作用域内才能调用 `gen_range`。
- `1..=100`：闭区间 range。
- `cargo doc --open` 查看依赖文档。

## 比较猜测的数字和秘密数字

```rust
use std::cmp::Ordering;

match guess.cmp(&secret_number) {
    Ordering::Less => println!("Too small!"),
    Ordering::Greater => println!("Too big!"),
    Ordering::Equal => println!("You win!"),
}
```

- `match`：模式匹配，第一个匹配的分支执行。
- `guess` 是 `String`，`secret_number` 是数字 → 需类型转换。

**Shadowing + parse**：

```rust
let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

- `trim()` 去掉首尾空白（含 `\n`）。
- `parse()` 返回 `Result`；`: u32` 类型注解。
- **遮蔽**（shadowing）：同名 `let` 绑定新值，可换类型。

## 使用循环来允许多次猜测

```rust
loop {
    // ... 读入、比较 ...
    break;  // 猜对时退出
}
```

### 猜测正确后退出

在 `Ordering::Equal` 分支加 `break`。

### 处理无效输入

用 `match` 替代 `expect`，失败时 `continue`：

```rust
let guess: u32 = match guess.trim().parse() {
    Ok(num) => num,
    Err(_) => continue,
};
```

## 总结

- 新语法预览：`let`/`mut`、`match`、方法、关联函数、外部 crate、`Result`、`loop`/`break`/`continue`
- 第3章补编程概念；第4章起所有权；第6章详讲 `match` 与枚举
