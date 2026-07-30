+++
title = "05-Rust基础入门"
date = 2026-07-28T14:49:00+08:00
weight = 50
type = "docs"
description = "变量、类型、所有权、模式匹配到模块错误处理，Rust 基础全栈精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [Rust语言圣经](https://beatai.org/rust-course/)「Rust 基础入门」

# Rust 基础入门

## 变量绑定与解构

**默认不可变**；需修改加 `mut`。

```rust
let x = 5;       // 不可变
let mut y = 5;   // 可变
y = 6;
```

| 概念 | 语法 | 要点 |
|------|------|------|
| 绑定 | `let a = val` | 所有权语义，非简单赋值 |
| 常量 | `const MAX: u32 = 100_000` | 必须标注类型；编译期确定；不可 `mut` |
| 遮蔽 | `let x = 5; let x = x+1` | 新变量，可改类型 |
| 忽略未用 | `let _x = 5` | 前缀 `_` 抑制警告 |
| 解构 | `let (a, mut b) = (true, false)` | 模式匹配提取 |
| 解构赋值 | `(a, b) = (1, 2)` | 1.59+；`+=` 不支持 |

**mut vs shadow**：`mut` 改同一内存；`shadow` 创建新绑定（可能再分配）。

## 基本类型

静态类型；编译器多数可推导，推不出需标注：`let n: i32 = "42".parse().expect("...")`。

**基本类型一览**：

| 类别 | 类型 |
|------|------|
| 有符号整数 | `i8`…`i128`, `isize` |
| 无符号整数 | `u8`…`u128`, `usize` |
| 浮点 | `f32`, `f64`（默认） |
| 字符 | `char`（4 字节 Unicode） |
| 布尔 | `bool` |
| 字符串切片 | `&str` |
| 单元 | `()` |

### 数值类型

**整数默认 `i32`**；索引常用 `usize`/`isize`（随平台 32/64 位）。

**字面量**：`98_222` `0xff` `0o77` `0b1111` `b'A'`（仅 u8）。

**溢出**：debug 模式 panic；release 补码 wrapping（视为错误）。显式：`wrapping_*` / `checked_*` / `overflowing_*` / `saturating_*`。

**浮点陷阱**：二进制近似；勿用 `==` 比较；`NaN != NaN`；未实现 `Eq` → 不能作 HashMap key。

**运算**：`+ - * / %`；位运算 `& | ^ ! << >>`；移位超位数 compile error。

**Range**：`1..5`（不含 5）；`1..=5`（含 5）；支持数字与 char。

**类型转换**：显式 `as`；非隐式 widening。

### 字符、布尔、单元类型

- `char`：单引号 `'中'`，4 字节
- `bool`：1 字节；用于 `if`
- `()`：零大小；无返回值函数、发散函数对比（`-> !`）

### 语句与表达式

| | 语句 | 表达式 |
|---|------|--------|
| 返回值 | 无 | 有 |
| 分号 | 有 | 末尾无分号才返回值 |
| 例子 | `let x = 5;` | `5 + 6`、`if { a } else { b }` |

`let` 是语句，不能 `let b = (let a = 8)`。块 `{ ...; expr }` 最后一行无分号即返回值。

### 函数

```rust
fn add(i: i32, j: i32) -> i32 { i + 1 }  // 隐式返回
fn dead() -> ! { panic!("...") }          // 永不返回
```

- 蛇形命名 `snake_case`
- 参数必须标注类型
- 末尾表达式无分号 = 返回值；加 `;` 变 `()` 导致类型错误

## 所有权和借用

编译期所有权检查，零运行时 GC 开销。

### 所有权

**三条规则**：

1. 每个值有唯一所有者（变量）
2. 同一时刻只有一个所有者
3. 所有者离开作用域 → `drop`

**栈 vs 堆**：栈固定大小、LIFO；堆动态分配、通过指针访问。

**Move vs Copy**：

| 操作 | 基本类型 (Copy) | String 等 (Move) |
|------|-----------------|------------------|
| `let y = x` | 拷贝栈数据 | 转移所有权，`x` 失效 |
| 函数传参 | 拷贝 | 移动 |
| 深拷贝 | — | `clone()` |

**Copy 类型**：整数、浮点、bool、char、`&T`（非 `&mut T`）、Copy 元组。

**函数**：传 `String` 移入；返回 `String` 移出。避免来回传 → 用借用。

### 引用与借用

```rust
let s1 = String::from("hello");
let len = calculate_length(&s1);  // 不可变借用
fn calculate_length(s: &String) -> usize { s.len() }
```

**解引用**：`*y` 取引用指向的值。

**可变借用**：

```rust
let mut s = String::from("hello");
change(&mut s);
fn change(s: &mut String) { s.push_str(", world"); }
```

**借用规则**：

1. 任意多个 `&T`，或**唯一一个** `&mut T`
2. 引用必须始终有效
3. 不可同时存在 `&T` 与 `&mut T`（NLL：引用活到最后一次使用）

**悬垂引用**：编译拒绝；返回引用需生命周期或返回 owned 值。

## 复合类型

由基本类型组合；String/Vec 等堆上集合另述。

### 字符串与切片

| 类型 | 所有权 | 可变性 | 场景 |
|------|--------|--------|------|
| `String` | 拥有堆数据 | 可变 | 动态文本 |
| `&str` | 借用 | 视原数据 | 字符串切片 |
| 字面量 `&str` | 静态/程序内 | 不可变 | `"hello"` |

**切片**：`&s[0..5]`，左闭右开；UTF-8 边界切割（中文 3 字节）。

```rust
let s = String::from("hello");
let slice: &str = &s[0..2];
```

**常用**：`String::from()` / `.push_str()` / `.len()` / `.as_str()`。

### 元组

固定长度、异构：`let t: (i32, f64) = (500, 6.4);`

- 解构：`let (x, y, z) = t;`
- 索引：`t.0`
- 函数多返回值：`(s, s.len())`

### 结构体

```rust
struct User { active: bool, username: String, email: String }
let u = User { email: s, username: s, active: true, sign_in_count: 1 };
let mut u = u; u.email = String::from("...");
```

- 字段同名简写：`User { email, username, ... }`
- 更新语法：`User { email: e, ..user1 }`（其余从 user1 移/拷贝）
- **元组结构体**：`struct Point(i32, i32);` — 有名类型 + 元组访问
- **单元结构体**：`struct AlwaysEqual;`

### 枚举

```rust
enum Message { Quit, Move { x: i32, y: i32 }, Write(String), ChangeColor(i32,i32,i32) }
let m = Message::Write(String::from("hi"));
```

- 枚举类型 vs 枚举值（成员实例）
- 成员可带不同数据类型
- **`Option<T>`**：`Some(T)` | `None` — 替代 null
- **`Result<T,E>`**：`Ok(T)` | `Err(E)` — 可恢复错误

### 数组

**固定长度**、栈上、同类型：`let a: [i32; 5] = [1,2,3,4,5];` / `let a = [3; 5];`

越界：release 也可能 panic（边界检查）。动态数组用 `Vec`（见集合）。

**数组切片**：`&a[1..3]` → `&[i32]`。

## 流程控制

**if 是表达式**（分支类型须一致）：

```rust
let n = if cond { 5 } else { 6 };
```

**循环**：

| 类型 | 语法 | 用途 |
|------|------|------|
| loop | `loop { break 42; }` | 无限循环 |
| while | `while n != 0 { n -= 1; }` | 条件循环 |
| for | `for i in 1..=5 {}` | 迭代（首选） |

**for 与所有权**：

| 写法 | 所有权 |
|------|--------|
| `for x in v` | move（Copy 类型除外） |
| `for x in &v` | 不可变借用 |
| `for x in &mut v` | 可变借用 |

`enumerate()`：`for (i, v) in a.iter().enumerate()`。

## 模式匹配

### match 和 if let

```rust
match coin {
    Coin::Penny => 1,
    Coin::Nickel | Coin::Dime => 5,  // 多模式 |
    _ => 0,                           // 必须穷尽
}
```

- 每个分支是表达式，返回类型相同
- 可绑定变量、解构

**if let**（单模式，忽略其余）：

```rust
if let Some(v) = opt { println!("{}", v); }
```

**while let**：`while let Some(x) = stack.pop() { ... }`

**match 与 Option**：

```rust
fn plus_one(x: Option<i32>) -> Option<i32> {
    match x { None => None, Some(i) => Some(i + 1) }
}
```

### 解构 Option

`Some(i)` 绑定内部值；`None` 单独分支。

### 模式适用场景

match / if let / while let / for 解构 / let 解构 / 函数参数模式。

### 全模式列表

| 模式 | 示例 |
|------|------|
| 字面量 | `1 => ...` |
| 命名变量 | `Some(y) =>`（注意遮蔽） |
| 多模式 `\|` | `1 \| 2 =>` |
| 范围 `..=` | `1..=5 =>` |
| 解构 struct | `Point { x, y }` |
| 解构 enum | `Message::Write(s) =>` |
| 解构 tuple/array | `(a, b)` `[first, .., last]` |
| ref / ref mut | 借用模式内字段 |
| `@` 绑定 | `n @ 1..=5 =>` |
| `_` 忽略 | `_ =>` |
| `..` 剩余 | `Some(Digit { .. })` |
| 守卫 | `Some(x) if x > 0 =>` |
| `_x` | 忽略且不计未使用警告 |

## 方法 Method

```rust
impl Rectangle {
    fn area(&self) -> u32 { self.width * self.height }
    fn can_hold(&self, other: &Rectangle) -> bool { ... }
    fn square(size: u32) -> Rectangle { ... }  // 关联函数，无 self
}
rect.area();
```

| self 形式 | 含义 |
|-----------|------|
| `&self` | 不可变借用（最常用） |
| `&mut self` | 可变借用 |
| `self` | 获取所有权（少用） |

- 方法与字段可同名：`rect.width()` vs `rect.width`
- **关联函数**：无 `self`，如 `String::from`

## 泛型和特征

### 泛型 Generics

```rust
fn largest<T: PartialOrd>(list: &[T]) -> &T { ... }
struct Point<T> { x: T, y: T }
enum Option<T> { Some(T), None }
```

- 使用前声明 `<T>`
- 单态化：编译期为每个具体类型生成代码
- 泛型需 trait 约束才能调用方法（如 `>` 需 `PartialOrd`）

**const 泛型**：`[T; N]` 中 N 可为泛型常量。

### 特征 Trait

**定义行为集合**（类似接口）：

```rust
pub trait Summary {
    fn summarize(&self) -> String;
}
impl Summary for Post { fn summarize(&self) -> String { ... } }
```

- **孤儿规则**：`impl Trait for Type` 时，Trait 或 Type 至少一个在本 crate 定义
- **默认实现**：trait 内提供方法体；实现可覆盖
- **作为参数**：`fn notify(item: &impl Summary)` 或 `fn notify<T: Summary>(item: &T)`
- **特征约束**：`fn f<T: Display + Clone>(t: T)`
- **where**：`fn f<T>(t: T) where T: Display + Clone`
- **返回 impl Trait**：返回实现某 trait 的类型（单一种具体类型）
- **derive**：`#[derive(Debug, Clone, PartialEq)]` 自动实现

### 特征对象

多态：`Box<dyn Draw>` / `&dyn Summary` — 运行时 vtable。

- `impl Trait` 返回只能一种类型
- `dyn Trait` 可存不同类型于 `Vec<Box<dyn Draw>>`
- 对象安全：方法不能返回 Self、无泛型方法等

### 进一步深入特征

- **关联类型**：`type Item;`（如 `Iterator::Item`），impl 时指定
- **完全限定语法**：`<Type as Trait>::method()`
- **supertrait**：`trait Outline: Display { ... }`
- **newtype 模式**：`struct Wrapper(T);` 绕过孤儿规则

## 集合类型

### 动态数组 Vector

```rust
let mut v: Vec<i32> = Vec::new();
v.push(1);
let v = vec![1, 2, 3];
let third = &v[2];           // panic 越界
let third = v.get(2);        // Option
```

- 同类型、堆上、可变长
- 遍历时勿同时 mut push 与 hold 引用
- `Vec::with_capacity(n)` 预分配

### KV 存储 HashMap

```rust
use std::collections::HashMap;
let mut map = HashMap::new();
map.insert("k", 1);
let v = map.get("k");  // Option<&V>
```

- 需 `use`（不在 prelude）
- 键需 `Eq + Hash`
- 所有权：Copy 键值拷贝；否则 move
- 更新：`entry(key).or_insert(val)` 避免重复查
- 从 Vec 构建：`list.into_iter().collect::<HashMap<_,_>>()`

## 认识生命周期

**生命周期** = 引用的有效作用域；防悬垂引用。

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

- 标注 `'a` 描述**引用间关系**，不改变实际存活时间
- 返回值引用寿命 ≤ 参数中较短者
- **结构体含引用**：`struct Excerpt<'a> { part: &'a str }`
- **生命周期省略（三条规则）**：
  1. 每个引用参数独立生命周期
  2. 仅一个输入生命周期 → 赋给所有输出
  3. 方法有 `&self`/`&mut self` → 赋给输出
- **`'static`**：与程序同寿（字符串字面量）；勿滥用 `T: 'static` 糊弄编译器

## 返回值和错误处理

### panic! 深入剖析

**不可恢复错误**：数组越界、逻辑不可继续。

- 被动：`v[99]` 触发 panic
- 主动：`panic!("msg")`
- `RUST_BACKTRACE=1 cargo run` 看栈
- release 可 `panic = 'abort'` 减小体积

仅真正无法恢复时用 panic；用户输入错误应返回 `Result`。

### 返回值 Result 和 ?

```rust
enum Result<T, E> { Ok(T), Err(E) }

let f = File::open("a.txt")?;
let f = match f {
    Ok(file) => file,
    Err(e) => return Err(e.into()),
};
```

| 方法 | 行为 |
|------|------|
| `unwrap()` | Ok 取值，Err panic |
| `expect("msg")` | 带消息的 unwrap |
| `?` | Err 则 early return；Ok 解包 |
| `map` / `and_then` | 链式处理 |

`?` 用于返回 `Result`/`Option` 的函数；`main` 可 `fn main() -> Result<(), Box<dyn Error>>`。

## 包和模块

### 包 Crate

- **Package**（Cargo 项目）含 `Cargo.toml`
- **Crate** = 编译单元（库或二进制）
- 一个 Package：最多 1 个 lib crate + 多个 bin crate
- `src/main.rs` → bin；`src/lib.rs` → lib

### 模块 Module

```rust
mod front_of_house {
    pub mod hosting {
        pub fn add_to_waitlist() {}
    }
}
front_of_house::hosting::add_to_waitlist();
```

- 树形组织代码
- `pub` 控制可见性
- 模块可嵌套文件：`mod xxx;` → `xxx.rs` 或 `xxx/mod.rs`

### 使用 use 引入模块及受限可见性

```rust
use std::collections::HashMap;
use std::io::{self, Write};
pub use crate::front_of_house::hosting;  // 重新导出
```

- `use` 简化路径；`as` 重命名
- **`pub(in path)` / `pub(crate)` / `pub(super)`** 限制可见范围
- 习惯：`use std::xxx` 放顶部；`use crate::xxx` 引用本 crate

## 注释和文档

| 类型 | 语法 | 用途 |
|------|------|------|
| 行注释 | `//` | 代码说明 |
| 块注释 | `/* */` | 多行 |
| 文档行 | `///` | 项文档，支持 Markdown + 示例 |
| 文档块 | `//!` | crate/模块级文档 |

```bash
cargo doc --open
```

文档注释内 ` ``` ` 代码块可运行：`cargo test` 会测 doc test。

## 格式化输出

**宏**：`print!` / `println!` / `format!` / `eprint!` / `eprintln!`（后两者 → stderr）。

| 占位符 | trait | 用途 |
|--------|-------|------|
| `{}` | Display | 用户友好输出 |
| `{:?}` | Debug | 调试 |
| `{:#?}` | Debug |  pretty 打印 |
| `{value}` | — | 命名参数 |
| `{:04}` | — | 宽度/填充/对齐 |
| `{:.2}` | — | 小数位数 |
| `{:b}` / `{:x}` | — | 二进制/十六进制 |
| `{:>8}` / `{:<8}` / `{:^8}` | — | 右/左/居中 |

**常用**：`println!("{}, world", s);` `format!("{name} is {age}", name="a", age=18);`

自定义 Display/Debug：为类型 `impl fmt::Display` / `impl fmt::Debug`。
