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

> **NLL = Non-Lexical Lifetimes**
>
> **中文：非词法生命周期**
>
> 就是你刚刚看所有权文档里这句话：
>
> > 引用作用域到最后一次使用为止（NLL），非声明到块尾。
>
> 1. 先搞懂：什么是「词法 Lexical」
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
> 2. NLL 核心思想（现在所有 Rust 默认开启）
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
>  3. 再举经典例子（TRPL 官方示例）
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
>  4. 重要边界：NLL 不能绕过安全规则
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
> 5. 历史小知识
>
> - Rust 2018 Edition 首次启用 NLL；
> - Rust 1.63（2022）**所有版本默认永久开启 NLL**，旧词法借用检查器彻底移除；
> - 现在写 Rust 不需要关心关闭 / 开启，永久生效。
>
>  6. 和你前面学习的知识点串联（所有权文档原文呼应）
>
> > 借用规则（口诀）：同一时刻：要么一个`&mut`，要么任意多个`&`（不可与`&mut`共存）。**引用作用域到最后一次使用为止（NLL），非声明到块尾。**
>
> 极简记忆口诀
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

>  Deref Coercion
>
> **中文：解引用强制多态 / 解引用强制转换**
>
> 一句话定义
>
> ​	Rust 的一种**隐式自动类型转换**：当一个类型实现了 `Deref` trait，编译器会**自动、透明**地连续调用 `*` 解引用，把 `&T` 转换成 `&U`。
>
> ​	仅发生在**引用**场景，不会获取所有权，是便利语法糖。
>
> > ⚠️ 只作用于函数参数传参的时候！
>>
> > 普通表达式不会自动触发 Deref coercion。
> 
> 前置知识
>
> ```rust
>std::ops::Deref
> ```
> 
> ```rust
>trait Deref {
>    type Target;
>    fn deref(&self) -> &Self::Target;
>  }
>  ```
> 
> 典型实现：
>
> - `String` 实现 `Deref<Target=str>`
>- `Box<T>` 实现 `Deref<Target=T>`
> - `Vec<T>` 实现 `Deref<Target=[T]>`
> 
> 结合你刚学到的知识点举例（最重要）
>
>  例子 1
>
> ```rust
>fn take_str(s: &str) {
>    // ...
>}
> 
>fn main() {
>    let s: String = String::from("hello");
>    take_str(&s); 
>     // ✅ 自动转换！&String → &str
>    // 等价于 take_str(&*s)
> }
> ```
>  
>  过程拆解：
>  
>  1. `&String` 传入
> 2. 编译器调用 `s.deref()` → `&str`
> 3. 隐式完成，不需要手动写 `&*`
>
>    如果函数写成：
>
> 
> ```rust
> fn take_string(s: &String) {}
>```
> 
>​	那就**不能接收字符串字面量 `&"abc"`**，不存在反向转换。
> 
> ​	这就是为什么推荐参数使用 `&str`。
> 
>例子 2：Box<T>
> 
>```rust
> fn print(x: &i32) {}
>
>  fn main() {
>   let b = Box::new(100);
>    print(&b); // &Box<i32> ➜ &i32 自动转换
> }
> ```
> 
>  关键规则（必须记清）
>  
> 1. 触发时机
> 
>**只在函数参数传递时自动触发**
> 
>下面这段**不会自动转换，编译报错**：
>  
>```rust
> let s = String::from("hi");
>let x: &str = &s; // ❌ 赋值语句不触发deref coercion！
> ```
>
> 想要成立必须手动：
> 
> ```rust
> let x: &str = &*s;
>```
> 
>2. 可以链式多次转换
> 
> 比如：
> 
>`&Box<String>` → `&String` → `&str`
>  
>编译器自动一路解引用。
> 
>3. Deref coercion 区分**不可变 / 可变**
> 
>- `Deref`（不可变解引用）：只能用于不可变引用自动转换
> - `DerefMut`（可变解引用）：用于 `&mut T` 自动转换
>
>  **不能把可变引用强制转换成不可变引用之外的反向操作：**
>
> `&str` 无法自动转为 `&mut String`
> 
>4. 和所有权、借用关系
> 
>整个过程全部使用**引用**，**不会移动所有权、不会发生拷贝**，只是类型转换。
> 
>和所有权章节串联（你当前学习链路）
>  
>```rust
> fn first_word(s: &str) -> &str { ... }
>
> let my_string = String::from("hello world");
>first_word(&my_string); // Deref coercion &String→&str
> 
> let my_literal = "hello world";
> first_word(my_literal); // &str 直接传入
> ```
> 
> 同一个函数，既能接收 `&String` 又能接收 `&str`，得益于 Deref 强制转换。
> 
> 这也是 TRPL 第四章 Slice 部分强调该设计的根本原因。
> 
>容易踩坑的误区
> 
>1. ❌ Deref coercion = 自动解引用运算符 `*`    
> 
>  ✅ 它产生的是引用转换 `&T → &U`，不是获取值。
> 
>2. ❌ 任何地方都能自动转换
> 
>  ✅ 
>  
>  仅限函数传参 ，let 赋值、if 判断等普通表达式不会触发。
>  
>3. ❌ 可以绕过借用检查
>  
>  ✅ 只是语法糖，所有权、可变借用互斥规则依然严格生效。
> 
>极简记忆口诀
>  
>​	实现 Deref 的类型，传参进函数时，编译器悄悄帮你 `&*`，一层一层解引用得到目标引用类型。
>  

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
