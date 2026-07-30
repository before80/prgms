+++
title = "03-常见编程概念"
date = 2026-07-28T14:49:00+08:00
weight = 30
type = "docs"
description = "变量、标量与复合类型、函数、注释与控制流的 Rust 精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第3章

# 常见编程概念

变量、基本类型、函数、注释、控制流——几乎每个 Rust 程序都会用到。

## 变量和可变性

- **默认不可变**：`let x = 5;` 不能再赋值。
- **可变**：`let mut x = 5;`
- 不可变利于推导与安全；需要修改时显式 `mut`。

### 常量

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```

- `const`（非 `let`），**必须**标注类型，编译期可求值。
- 命名：全大写 + 下划线；可在全局作用域。

### 遮蔽

```rust
let x = 5;
let x = x + 1;        // 新变量，仍不可变
{
    let x = x * 2;    // 内部作用域遮蔽
    println!("{x}"); // 12
}
println!("{x}");      // 6
```

- 再次 `let` 同名 = 遮蔽，可 **改变类型**（`mut` 不能改类型）。
- 典型：`let spaces = "   "; let spaces = spaces.len();`

## 数据类型

**静态类型**：编译期确定所有变量类型；推断失败时需类型注解。

```rust
let guess: u32 = "42".parse().expect("Not a number!");
```

### 标量类型

四种：**整型、浮点、bool、char**。

#### 整型

| 长度 | 有符号 | 无符号 |
|------|--------|--------|
| 8-bit | `i8` | `u8` |
| 16-bit | `i16` | `u16` |
| 32-bit | `i32` | `u32` |
| 64-bit | `i64` | `u64` |
| 128-bit | `i128` | `u128` |
| 架构相关 | `isize` | `usize` |

- 默认整型：`i32`；索引常用 `usize`。
- 字面值：`98_222`、`0xff`、`0o77`、`0b1111_0000`、`57u8`。
- **整型溢出**：debug 模式 panic；release 可能 wrapping；可用 `wrapping_*` / `checked_*` / `saturating_*`。

#### 浮点型

- `f32` / `f64`，默认 `f64`；IEEE-754。

#### 数值运算

`+ - * / %`；整数除法向零舍入。

#### 布尔类型

`bool`：`true` / `false`。

#### 字符类型

- `char`：4 字节 Unicode 标量；单引号 `'z'`，非 ASCII 亦可。

### 复合类型

**元组**与**数组**。

#### 元组类型

```rust
let tup: (i32, f64, u8) = (500, 6.4, 1);
let (x, y, z) = tup;   // 解构
let five = tup.0;      // 索引访问
```

- 固定长度、可异构；空元组 `()` 叫 **单元**（unit）。

#### 数组类型

```rust
let a = [1, 2, 3, 4, 5];
let a: [i32; 5] = [1, 2, 3, 4, 5];
let a = [3; 5];        // [3,3,3,3,3]
let first = a[0];
```

- 固定长度、同类型、栈上分配；越界访问 **运行时 panic**。
- 长度可变集合用 **Vector**（第8章）。

## 函数

```rust
fn another_function(x: i32) {
    println!("The value of x is: {x}");
}
```

- 命名：**snake_case**；定义位置无关，只要在作用域内可见。
- 参数 **必须** 声明类型。

### 参数

多参数逗号分隔：`fn f(value: i32, unit_label: char)`.

### 语句和表达式

- **语句**：执行操作，**不返回值**（`let`、函数定义、`;` 结尾）。
- **表达式**：求值并产生值（运算、函数/宏调用、块 `{ ... }`）。

```rust
let y = {
    let x = 3;
    x + 1   // 无分号 → 表达式，值为 4
};
```

- 表达式末尾加分号 → 变成语句，返回 `()`。

### 具有返回值的函数

```rust
fn five() -> i32 {
    5       // 隐式返回最后一个表达式
}

fn plus_one(x: i32) -> i32 {
    x + 1   // 勿在末尾加 ;
}
```

- `return` 可提前返回；多数情况用末尾表达式。

## 注释

```rust
// 行注释到行尾

/*
多行需每行 //
*/

fn main() {
    let lucky_number = 7; // 行尾注释
}
```

- 文档注释见第14章（`///`、`//!`）。

## 控制流

### `if` 表达式

```rust
if number < 5 {
    println!("condition was true");
} else {
    println!("condition was false");
}
```

- 条件 **必须是 `bool`**，无隐式转换。
- `if` 是 **表达式**，可赋值：

```rust
let number = if condition { 5 } else { 6 };
```

- 各分支返回值 **类型必须相同**。

#### 使用 `else if` 处理多重条件

按顺序匹配，只执行第一个为真的分支。

#### 在 `let` 语句中使用 `if`

见上 `let number = if ...`。

### 使用循环重复执行

三种：`loop`、`while`、`for`。

#### 使用 `loop` 重复执行代码

```rust
loop {
    println!("again!");
    break;           // 退出
    continue;        // 下一次迭代
}
```

#### 从循环返回值

```rust
let result = loop {
    counter += 1;
    if counter == 10 {
        break counter * 2;
    }
};
```

#### 循环标签：在多个循环之间消除歧义

```rust
'outer: loop {
    loop {
        break 'outer;
    }
}
```

#### `while` 条件循环

```rust
while number != 0 {
    println!("{number}!");
    number -= 1;
}
```

#### 使用 `for` 遍历集合

```rust
let a = [10, 20, 30, 40, 50];
for element in a {
    println!("{element}");
}

for number in (1..4).rev() {
    println!("{number}!");
}
```

- 比 `while` + 索引更安全；Rust 中最常用循环形式。

## 总结

- 变量：`let` / `mut` / `const` / 遮蔽
- 类型：标量四族 + 元组/数组
- 函数：表达式返回、参数需类型
- 控制流：`if`（表达式）、`loop`/`while`/`for`
