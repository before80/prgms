+++
title = "04-认识所有权"
date = 2026-07-28T14:49:00+08:00
weight = 40
type = "docs"
description = "所有权三规则、移动与拷贝、引用借用与 slice 的内存安全精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第4章

# 认识所有权

**所有权**（ownership）：Rust 管理内存的核心规则集，编译期检查，无 GC，运行时零开销。

## 什么是所有权？

### 栈（Stack）与堆（Heap）

| | 栈 | 堆 |
|---|-----|-----|
| 特点 | LIFO，已知固定大小 | 分配器找空间，返回指针 |
| 速度 | 快 | 较慢（需通过指针访问） |
| 存放 | 已知大小数据 | 编译时未知或可变大小数据 |

- 函数调用：参数与局部变量压栈，结束出栈。
- 所有权主要管理 **堆数据** 的分配与释放。

### 所有权规则

1. 每个值有且仅有一个 **所有者**（owner）。
2. 任一时刻只有一个所有者。
3. 所有者离开作用域，值被 **drop**（释放内存）。

### 变量作用域

```rust
{                      // s 尚未有效
    let s = "hello";   // 从此有效
    // 使用 s
}                      // 作用域结束，s 不再有效
```

### `String` 类型

```rust
let mut s = String::from("hello");
s.push_str(", world!");
```

- 字面值 `&str`：硬编码进二进制，不可变。
- `String`：堆上分配，可增长；`String::from("hello")` 请求堆内存。

### 内存与分配

- 离开作用域时 Rust 自动调用 `drop` 释放堆内存（类似 C++ RAII）。

#### 使用移动的变量与数据交互

**Copy 类型（栈上，如 i32）**：

```rust
let x = 5;
let y = x;   // 拷贝，x 仍有效
```

**Move 类型（堆上，如 String）**：

```rust
let s1 = String::from("hello");
let s2 = s1;        // 移动：只拷贝指针/长度/容量，不拷贝堆数据
// println!("{s1}"); // 编译错误：s1 已失效
```

- Rust 的赋值 = **移动**（move），非深拷贝；避免 double free。
- Rust **不会**自动深拷贝堆数据。

#### 作用域与赋值

```rust
let mut s = String::from("hello");
s = String::from("ahoy");  // 旧 "hello" 立即 drop
```

#### 使用克隆的变量与数据交互

需要深拷贝时显式调用（昂贵）：

```rust
let s1 = String::from("hello");
let s2 = s1.clone();
```

#### 只在栈上的数据：拷贝

- 实现 **`Copy` trait** 的类型：赋值后原变量仍有效（整数、bool、f64、char、Copy 元组等）。
- 实现了 **`Drop`** 的类型不能实现 `Copy`。

### 所有权与函数

```rust
fn takes_ownership(s: String) { /* s drop */ }
fn makes_copy(x: i32) { /* x Copy，无影响 */ }

let s = String::from("hello");
takes_ownership(s);  // s 移动进函数，之后不可用

let x = 5;
makes_copy(x);       // x 仍可用
```

### 返回值与作用域

```rust
fn gives_ownership() -> String {
    String::from("yours")
}

fn takes_and_gives_back(s: String) -> String {
    s  // 所有权移回调用方
}
```

- 传参 + 返回所有权较繁琐 → 用 **引用**。

## 引用与借用

```rust
fn calculate_length(s: &String) -> usize {
    s.len()
}

let s1 = String::from("hello");
let len = calculate_length(&s1);  // 借用，s1 仍拥有数据
```

- `&T`：**不可变引用**；`&mut T`：**可变引用**。
- 创建引用 = **借用**（borrowing），不取得所有权。

### 可变引用

```rust
fn change(some_string: &mut String) {
    some_string.push_str(", world");
}

let mut s = String::from("hello");
change(&mut s);
```

**借用规则（口诀）**：

- 同一时刻：**要么** 一个 `&mut`，**要么** 任意多个 `&`（不可与 `&mut` 共存）。
- 防止 **数据竞争**（并发读写无同步）。
- 引用作用域到最后一次使用为止（NLL），非声明到块尾。

> # NLL = Non-Lexical Lifetimes
>
> **中文：非词法生命周期**
>
> 就是你刚刚看所有权文档里这句话：
>
> > 引用作用域到最后一次使用为止（NLL），非声明到块尾。
>
> ## 1. 先搞懂：什么是「词法 Lexical」
>
> **旧版借用检查（无 NLL）：词法生命周期**
>
> 借用存活范围 = **源代码大括号 `{}` 的范围**
>
> 只要引用变量还在代码块里，编译器就认为借用一直有效，**不管你后续还用不用它**。
>
> 示例（**NLL 出现之前，这段代码编译报错**）
>
> ```rust
> let mut s = String::from("hello");
> let r = &s;        // 不可变借用
> println!("{}", r); // r 最后一次使用
> s.push_str("!");   // ❌ 老编译器报错
> ```
>
> 旧逻辑：`r` 直到函数末尾 `}` 都存活 → 不可变借用和可变借用冲突。
>
> 想要正常运行，只能手动加嵌套大括号强行缩短作用域。
>
> ## 2. NLL 核心思想（现在所有 Rust 默认开启）
>
> 编译器不再单纯看大括号，**分析代码执行流（MIR 中间代码）**：
>
> 👉 **借用在【最后一次使用该引用】之后立即结束，不必等到代码块末尾。**
>
> 上面同一段代码，**现代 Rust（开启 NLL）正常编译✅**
>
> ```rust
> let mut s = String::from("hello");
> let r = &s;
> println!("{}", r); // r 在这里用完，借用直接结束
> s.push_str("!");   // ✅ 允许可变借用
> ```
>
> > ⚠️ 重点区分两个概念，非常容易混淆：
> >
> > 1. **引用变量 r 的作用域**：依然到 `}` 结束（变量本身还存在栈上）
> > 2. **借用（borrow）的生命周期**：NLL 判定为 `println!` 之后就失效。
> >
> > **NLL 控制的是「借用时长」，不是变量本身存活时长！**
>
> ## 3. 再举经典例子（TRPL 官方示例）
>
> ```rust
> let mut s = String::from("hello");
> 
> let r1 = &s;
> let r2 = &s;
> println!("{} {}", r1, r2);
> // 👉 r1、r2借用到此全部结束
> 
> let r3 = &mut s; // ✅ NLL允许！借用互不重叠
> println!("{}", r3);
> ```
>
> ## 4. 重要边界：NLL 不能绕过安全规则
>
> NLL 只是**更精准判定借用何时结束**，**不会放宽所有权 / 借用核心规则**：
>
> - 仍然不允许同一时间：可变引用 + 其他引用共存
> - 依然杜绝悬垂引用
> - 不能解决真正存在借用重叠的代码
>
> 下面这段**依然报错**，NLL 救不了：
>
> ```rust
> let mut s = String::from("hi");
> let r = &s;
> s.push("!");   // ❌ 可变借用发生在 r 使用之前，借用重叠
> println!("{}", r);
> ```
>
> ## 5. 历史小知识
>
> - Rust 2018 Edition 首次启用 NLL；
> - Rust 1.63（2022）**所有版本默认永久开启 NLL**，旧词法借用检查器彻底移除；
> - 现在写 Rust 不需要关心关闭 / 开启，永久生效。
>
> ## 6. 和你前面学习的知识点串联（所有权文档原文呼应）
>
> > 借用规则（口诀）：同一时刻：要么一个`&mut`，要么任意多个`&`（不可与`&mut`共存）。**引用作用域到最后一次使用为止（NLL），非声明到块尾。**
>
> ### 极简记忆口诀
>
> 旧规则：活到右大括号；
>
> NLL 新规则：用到哪，借用到哪。

### 悬垂引用

```rust
// 编译失败：返回局部 String 的引用
fn dangle() -> &String {
    let s = String::from("hello");
    &s
}

fn no_dangle() -> String {
    String::from("hello")  // 移动所有权出去
}
```

- Rust 编译器保证引用永远有效（生命周期，第10章详述）。

### 引用的规则

1. 要么一个可变引用，要么多个不可变引用。
2. 引用必须始终有效。

## Slice 类型

**切片**（slice）：集合中连续元素的引用，不拥有数据。

### 字符串 slice

```rust
let s = String::from("hello world");
let hello = &s[0..5];   // 或 &s[..5]
let world = &s[6..11];    // 或 &s[6..]
let whole = &s[..];

// 类型 &str
```

- Range：`[start..end)`，`end` 不含；`..` 可省略起/止。
- 必须在 UTF-8 **字符边界**上切，否则 panic。

```rust
fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();
    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }
    &s[..]
}
```

- 返回 `&str` 而非索引 → 与底层 `String` 绑定，可变借用冲突时 **编译期** 报错。
- 字面值 `"hello"` 类型即 `&str`（二进制中的 slice）。

参数优先写 `&str` 而非 `&String`（更通用，支持 Deref  coercion）。

### 其他类型的 slice

```rust
let a = [1, 2, 3, 4, 5];
let slice = &a[1..3];  // 类型 &[i32]
```

## 总结

- 所有权 + drop：堆内存自动释放
- Move / Copy / clone 三者的区别
- 借用：`&` / `&mut` + 互斥规则
- Slice：`&str`、`&[T]`，引用子序列且编译期保安全
